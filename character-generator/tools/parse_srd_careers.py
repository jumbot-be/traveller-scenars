#!/usr/bin/env python3
"""Parse the Cepheus Engine SRD character-creation markdown (career tables)
and emit cepheus/data/careers.json.

Source (Open Gaming Content, OGL): Cepheus Engine SRD, chapter 1
"Character Creation", section "Career Tables".
HTML/markdown mirror: https://github.com/orffen/cepheus-srd
Official PDF: DriveThruRPG "Cepheus Engine System Reference Document" (Samardan Press).

Usage:
    python3 tools/parse_srd_careers.py /path/to/cepheus-srd/src/book1/character-creation.md
"""
import json
import re
import sys
from pathlib import Path

COLUMN_KEYS = {
    "Athlete": "athlete",
    "Aerospace Defense": "aerospace_defense",
    "Agent": "agent",
    "Barbarian": "barbarian",
    "Belter": "belter",
    "Bureaucrat": "bureaucrat",
    "Colonist": "colonist",
    "Diplomat": "diplomat",
    "Drifter": "drifter",
    "Entertainer": "entertainer",
    "Hunter": "hunter",
    "Marine": "marine",
    "Maritime Defense": "maritime_defense",
    "Mercenary": "mercenary",
    "Merchant": "merchant",
    "Navy": "navy",
    "Noble": "noble",
    "Physician": "physician",
    "Pirate": "pirate",
    "Rogue": "rogue",
    "Scientist": "scientist",
    "Scout": "scout",
    "Surface Defense": "surface_defense",
    "Technician": "technician",
}

DISPLAY_NAMES = {
    "athlete": "Athlete",
    "aerospace_defense": "Aerospace System Defense",
    "agent": "Agent",
    "barbarian": "Barbarian",
    "belter": "Belter",
    "bureaucrat": "Bureaucrat",
    "colonist": "Colonist",
    "diplomat": "Diplomat",
    "drifter": "Drifter",
    "entertainer": "Entertainer",
    "hunter": "Hunter",
    "marine": "Marine",
    "maritime_defense": "Maritime System Defense",
    "mercenary": "Mercenary",
    "merchant": "Merchant",
    "navy": "Navy",
    "noble": "Noble",
    "physician": "Physician",
    "pirate": "Pirate",
    "rogue": "Rogue",
    "scientist": "Scientist",
    "scout": "Scout",
    "surface_defense": "Surface System Defense",
    "technician": "Technician",
}

SECTION_LABELS = {
    "Qualifications": ("qualification", "single"),
    "Survival": ("survival", "single"),
    "Commission": ("commission", "single"),
    "Advancement": ("advancement", "single"),
    "Re-enlistment": ("reenlistment", "single"),
    "Ranks and Skills": ("ranks", "numbered"),
    "Material Benefits": ("material_benefits", "numbered"),
    "Cash Benefits": ("cash_benefits", "numbered"),
    "Cost Benefits": ("cash_benefits", "numbered"),
    "Personal Development": ("personal_development", "numbered"),
    "Service Skills": ("service_skills", "numbered"),
    "Specialist": ("specialist", "numbered"),
    "Adv Education": ("advanced_education", "numbered"),
}

CHAR_MAP = {"str": "STR", "dex": "DEX", "end": "END", "int": "INT", "edu": "EDU", "soc": "SOC"}


def cells(line):
    parts = [c.strip() for c in line.strip().strip("|").split("|")]
    return [p.replace("\\[", "[").replace("\\]", "]").replace("\\u2014", "\u2014").strip() for p in parts]


def clean(value):
    if value in ("\u2014", "--", "", "-"):
        return None
    return value


def parse_check(value):
    # "End 8+" -> {"char": "END", "target": 8}
    m = re.match(r"^(Str|Dex|End|Int|Edu|Soc)\s+(\d+)\+?$", value, re.I)
    if not m:
        raise ValueError(f"bad check: {value!r}")
    return {"char": CHAR_MAP[m.group(1).lower()], "target": int(m.group(2))}


def parse_rank_cell(value):
    # "Airman [Aircraft-1]" -> {"title": "Airman", "skill": "Aircraft"}
    m = re.match(r"^(.*?)\s*\[([^\]]+)-1\]$", value)
    if m:
        return {"title": m.group(1).strip() or None, "skill": m.group(2).strip()}
    return {"title": clean(value) or None, "skill": None}


def parse_career_tables(md_path):
    lines = Path(md_path).read_text(encoding="utf-8").splitlines()
    careers = {}
    columns = []
    section = None
    for line in lines:
        if not line.startswith("|"):
            continue
        c = cells(line)
        if not c or c[0] in ("---",):
            continue
        if c[0] == "Career":
            columns = [COLUMN_KEYS[x] for x in c[1:] if x in COLUMN_KEYS]
            for key in columns:
                careers.setdefault(key, {"key": key, "name": DISPLAY_NAMES[key]})
            section = None
            continue
        if c[0] in ("Skills and Training",):
            continue
        if c[0] in SECTION_LABELS:
            section, kind = SECTION_LABELS[c[0]]
            if kind == "single":
                for key, value in zip(columns, c[1:]):
                    careers[key][section] = clean(value)
            continue
        if c[0].isdigit() and columns:
            idx = int(c[0])
            for key, value in zip(columns, c[1:]):
                if section == "ranks":
                    careers[key].setdefault("ranks", {})[idx] = parse_rank_cell(value)
                elif section == "material_benefits":
                    careers[key].setdefault("material_benefits", {})[idx] = clean(value)
                elif section == "cash_benefits":
                    v = clean(value)
                    careers[key].setdefault("cash_benefits", {})[idx] = int(v) if v is not None else None
                else:
                    careers[key].setdefault(section, {})[idx] = clean(value)
    for key, career in careers.items():
        for field in ("qualification", "survival", "commission", "advancement"):
            if career.get(field):
                career[field] = parse_check(career[field])
        if career.get("reenlistment"):
            career["reenlistment"] = int(career["reenlistment"].rstrip("+"))
        for section in ("material_benefits", "cash_benefits", "personal_development",
                        "service_skills", "specialist", "advanced_education", "ranks"):
            if section in career:
                career[section] = [career[section][i] for i in sorted(career[section])]
    return [careers[k] for k in careers]


def main():
    if len(sys.argv) != 2:
        sys.exit("usage: parse_srd_careers.py <character-creation.md>")
    careers = parse_career_tables(sys.argv[1])
    assert len(careers) == 24, f"expected 24 careers, got {len(careers)}"
    for c in careers:
        assert c.get("qualification") and c.get("survival") and c.get("reenlistment")
        assert len(c["ranks"]) == 7 and len(c["service_skills"]) == 6
        assert len(c["material_benefits"]) == 7 and len(c["cash_benefits"]) == 7
        assert len(c["personal_development"]) == 6 and len(c["specialist"]) == 6 and len(c["advanced_education"]) == 6
    out = Path(__file__).resolve().parent.parent / "cepheus" / "data" / "careers.json"
    out.write_text(json.dumps(careers, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"wrote {out} ({len(careers)} careers)")


if __name__ == "__main__":
    main()
