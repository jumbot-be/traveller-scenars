"""Client for the TravellerMap API (https://travellermap.com/doc/api).

Used to pick a REAL homeworld (name, UWP, TL, trade codes) instead of
inventing one. Sector data is cached locally (TRAVELLERMAP_CACHE dir, default
~/.cache/traveller-character-api) to avoid hammering the API.

If the API is unreachable, random_world() returns None and the caller skips
the homeworld (we only use official TravellerMap worlds, never invented ones).

Trade codes are derived from the UWP per the Cepheus Engine SRD (chapter
"Worlds", "UWP Values for Trade Codes") - the Tech Level column is what makes
the world's TL matter for character generation (e.g. High Technology requires
TL 12+, Low Technology TL 5 or less).
"""
import json
import os
import time
import urllib.parse
import urllib.request
from pathlib import Path

from . import data

API_BASE = "https://travellermap.com/api"
USER_AGENT = "traveller-character-api/0.1 (+https://github.com/jumbot-be/traveller-scenars)"
DEFAULT_TIMEOUT = 12
CACHE_TTL = 7 * 24 * 3600


def cache_dir():
    return Path(os.environ.get("TRAVELLERMAP_CACHE",
                               Path.home() / ".cache" / "traveller-character-api"))


def _fetch(url, timeout=DEFAULT_TIMEOUT):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT,
                                                "Accept": "application/json"})
    last = None
    for attempt in range(2):  # one retry
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read()
        except Exception as e:
            last = e
    raise last


def _fetch_json(url, timeout=DEFAULT_TIMEOUT):
    return json.loads(_fetch(url, timeout).decode("utf-8"))


def ehex_to_int(c):
    if c is None:
        return None
    c = c.upper()
    if c.isdigit():
        return int(c)
    if "A" <= c <= "F":
        return ord(c) - ord("A") + 10
    return None


def parse_uwp(uwp):
    """'A646930-D' -> dict(starport, size, atmosphere, hydrosphere, population,
    government, law, tl). Values are ints (ehex decoded) or None."""
    out = {"uwp": uwp, "starport": None, "size": None, "atmosphere": None,
           "hydrosphere": None, "population": None, "government": None,
           "law": None, "tl": None}
    if not uwp:
        return out
    core, _, tl = uwp.partition("-")
    if len(core) >= 7:
        out["starport"] = core[0]
        out["size"] = ehex_to_int(core[1])
        out["atmosphere"] = ehex_to_int(core[2])
        out["hydrosphere"] = ehex_to_int(core[3])
        out["population"] = ehex_to_int(core[4])
        out["government"] = ehex_to_int(core[5])
        out["law"] = ehex_to_int(core[6])
    out["tl"] = ehex_to_int(tl[0]) if tl else None
    return out


def _in(v, lo=None, hi=None, values=None):
    if v is None:
        return False
    if values is not None:
        return v in values
    if lo is not None and v < lo:
        return False
    if hi is not None and v > hi:
        return False
    return True


def trade_codes_from_uwp(uwp_dict):
    """Trade codes per the CE SRD 'UWP Values for Trade Codes' table.

    TL matters here: High Technology (Ht) requires TL 12+, Low Technology (Lt)
    TL 5 or less.
    """
    u = uwp_dict
    size, atmo, hydro, pop, gov, law, tl = (u["size"], u["atmosphere"], u["hydrosphere"],
                                             u["population"], u["government"], u["law"], u["tl"])
    codes = []
    if _in(size, values=[0]) and _in(atmo, values=[0]) and _in(hydro, values=[0]):
        codes.append("Asteroid")
    if _in(atmo, lo=4, hi=9) and _in(hydro, lo=4, hi=8) and _in(pop, lo=5, hi=7):
        codes.append("Agricultural")
    if _in(pop, values=[0]) and _in(gov, values=[0]) and _in(law, values=[0]):
        codes.append("Barren")
    if _in(atmo, lo=2) and _in(hydro, values=[0]):
        codes.append("Desert")
    if _in(atmo, lo=10) and _in(hydro, lo=1):
        codes.append("Fluid Oceans")
    if _in(atmo, values=[5, 6, 8]) and _in(hydro, lo=4, hi=9) and _in(pop, lo=4, hi=8):
        codes.append("Garden")
    if _in(pop, lo=9):
        codes.append("High Population")
    if _in(tl, lo=12):
        codes.append("High Technology")
    if _in(atmo, hi=1) and _in(hydro, lo=1):
        codes.append("Ice-Capped")
    if _in(atmo, values=[0, 2, 4, 7, 9]) and _in(pop, lo=9):
        codes.append("Industrial")
    if _in(pop, lo=1, hi=3):
        codes.append("Low Population")
    if _in(tl, hi=5):
        codes.append("Low Technology")
    if _in(atmo, hi=3) and _in(hydro, hi=3) and _in(pop, lo=6):
        codes.append("Non-Agricultural")
    if _in(pop, lo=4, hi=6):
        codes.append("Non-Industrial")
    if _in(atmo, lo=2, hi=5) and _in(hydro, hi=3):
        codes.append("Poor")
    if _in(atmo, values=[6, 8]) and _in(pop, lo=6, hi=8):
        codes.append("Rich")
    if _in(hydro, values=[10]):
        codes.append("Water World")
    if _in(atmo, values=[0]):
        codes.append("Vacuum")
    return codes


# Trade-code short codes as they appear in TravellerMap 'Remarks' (T5).
TRADE_CODE_SHORT = {
    "Ag": "Agricultural", "As": "Asteroid", "Ba": "Barren", "De": "Desert",
    "Fl": "Fluid Oceans", "Ga": "Garden", "Hi": "High Population", "Ht": "High Technology",
    "Ic": "Ice-Capped", "In": "Industrial", "Lo": "Low Population", "Lt": "Low Technology",
    "Na": "Non-Agricultural", "Ni": "Non-Industrial", "Po": "Poor", "Ri": "Rich",
    "Va": "Vacuum", "Wa": "Water World",
}


def trade_codes_from_remarks(remarks):
    """Extract the standard trade-code short codes present in a Remarks field."""
    if not remarks:
        return []
    found = []
    for tok in remarks.replace("(", " ").replace(")", " ").split():
        tok = tok.rstrip(":")
        if tok in TRADE_CODE_SHORT:
            found.append(TRADE_CODE_SHORT[tok])
    return found


def law_descriptor(law):
    """SRD law-level descriptors used by the homeworld-skills table."""
    if law is None or law == 0:
        return "No Law"
    if law <= 3:
        return "Low Law"
    if law <= 6:
        return "Medium Law"
    return "High Law"


def list_sectors(official_only=True, use_cache=True):
    """Sectors from /api/universe. Returns [{'name', 'abbreviation', 'tags'}]."""
    cache = cache_dir() / "universe.json"
    if use_cache and cache.exists() and time.time() - cache.stat().st_mtime < CACHE_TTL:
        try:
            return json.loads(cache.read_text(encoding="utf-8"))
        except ValueError:
            pass
    params = {"requireData": 1}
    if official_only:
        params["tag"] = "Official"
    data = _fetch_json(f"{API_BASE}/universe?{urllib.parse.urlencode(params)}")
    sectors = []
    for s in data.get("Sectors", []):
        name = s.get("Names", [{}])[0].get("Text") or s.get("Abbreviation")
        sectors.append({"name": name, "abbreviation": s.get("Abbreviation"),
                        "tags": s.get("Tags", "")})
    cache.parent.mkdir(parents=True, exist_ok=True)
    cache.write_text(json.dumps(sectors, ensure_ascii=False), encoding="utf-8")
    return sectors


def resolve_sector(ref, sectors=None):
    """Resolve a sector name or abbreviation (e.g. 'Spinward Marches', 'spin')
    to its abbreviation. Returns None if unknown."""
    sectors = sectors if sectors is not None else list_sectors()
    ref = (ref or "").strip().lower()
    for s in sectors:
        if s["abbreviation"].lower() == ref or s["name"].lower() == ref:
            return s["abbreviation"]
    return None


def sector_worlds(sector, use_cache=True):
    """All worlds of a sector via /api/sec?type=TabDelimited (cached).

    Returns a list of normalized world dicts (see normalize_world).
    """
    abbr = resolve_sector(sector) or sector
    cache = cache_dir() / f"sector_{abbr}.json"
    if use_cache and cache.exists() and time.time() - cache.stat().st_mtime < CACHE_TTL:
        try:
            return json.loads(cache.read_text(encoding="utf-8"))
        except ValueError:
            pass
    url = f"{API_BASE}/sec?{urllib.parse.urlencode({'sector': abbr, 'type': 'TabDelimited', 'header': 1})}"
    raw = _fetch(url)
    text = raw.decode("utf-8")
    try:
        decoded = json.loads(text)
        if isinstance(decoded, str):
            text = decoded
    except ValueError:
        pass
    worlds = []
    for line in text.splitlines():
        line = line.strip("\r\n")
        if not line or line.startswith("#"):
            continue
        parts = line.split("\t")
        if len(parts) < 5 or parts[0] == "Sector":
            continue
        sector_name, ss, hexn, name, uwp = parts[0], parts[1], parts[2], parts[3], parts[4]
        remarks = parts[6] if len(parts) > 6 else ""
        bases = parts[5] if len(parts) > 5 else ""
        allegiance = parts[9] if len(parts) > 9 else ""
        worlds.append(normalize_world({
            "name": name, "hex": hexn, "uwp": uwp, "remarks": remarks,
            "bases": bases, "allegiance": allegiance,
            "sector": sector_name, "subsector": ss, "source": "travellermap",
        }))
    cache.parent.mkdir(parents=True, exist_ok=True)
    cache.write_text(json.dumps(worlds, ensure_ascii=False), encoding="utf-8")
    return worlds


def normalize_world(raw):
    """Normalize a TravellerMap world record; derive TL, trade codes, law descriptor."""
    uwp = parse_uwp(raw.get("uwp", ""))
    codes = trade_codes_from_uwp(uwp)
    for c in trade_codes_from_remarks(raw.get("remarks", "")):
        if c not in codes:
            codes.append(c)
    world = {
        "name": raw.get("name"),
        "hex": raw.get("hex"),
        "sector": raw.get("sector"),
        "subsector": raw.get("subsector"),
        "uwp": raw.get("uwp"),
        "starport": uwp["starport"],
        "starport_class": data.STARPORT_CLASS.get(uwp["starport"]),
        "size": uwp["size"],
        "atmosphere": uwp["atmosphere"],
        "hydrosphere": uwp["hydrosphere"],
        "population": uwp["population"],
        "government": uwp["government"],
        "law": uwp["law"],
        "tl": uwp["tl"],
        "law_descriptor": law_descriptor(uwp["law"]),
        "trade_codes": codes,
        "trade_code_details": [
            {"name": c, **data.TRADE_CODE_INFO.get(c, {"code": None, "condition": None, "description": None})}
            for c in codes
        ],
        "bases": raw.get("bases"),
        "allegiance": raw.get("allegiance"),
        "remarks": raw.get("remarks"),
        "source": raw.get("source", "travellermap"),
    }
    world["url"] = world_url(world)
    return world


def world_url(world):
    if not world.get("sector") or not world.get("hex"):
        return None
    q = urllib.parse.urlencode({"sector": world["sector"], "hex": world["hex"]})
    return f"https://travellermap.com/?{q}"


def inhabited(world):
    return world.get("population") not in (None, 0) and world.get("uwp") not in (None, "", "X")


def random_world(rng, sector=None, official_only=True):
    """Pick a random inhabited world from TravellerMap.

    rng: a cepheus.dice.Rng (deterministic when seeded).
    sector: optional sector name or abbreviation; None = random official sector.
    Returns a normalized world dict, or None if the API is unreachable or the
    sector is unknown.
    """
    try:
        sectors = list_sectors(official_only=official_only)
        if not sectors:
            return None
        if sector:
            abbr = resolve_sector(sector, sectors)
            if abbr is None:
                raise ValueError(f"unknown sector: {sector}")
            chosen = next(s for s in sectors if s["abbreviation"] == abbr)
        else:
            chosen = rng.choice(sectors)
        worlds = [w for w in sector_worlds(chosen["abbreviation"]) if inhabited(w)]
        if not worlds:
            return None
        return rng.choice(worlds)
    except (urllib.error.URLError, ValueError, KeyError, OSError, TimeoutError):
        return None
