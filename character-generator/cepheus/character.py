"""Cepheus Engine character generation, following the SRD "Character Creation
Checklist" (Cepheus Engine SRD, chapter 1, p.21-22) step by step:

1. characteristics (2D6 x6)  2. optional homeworld + background skills
3. career choice + qualification (or Drifter / Draft)
4. basic training  5. survival  6. commission & advancement
7. skills and training  8. aging (34+)  9. re-enlistment / retirement (7+ terms)
10. mustering-out benefits  11. next career  12. final details
"""
import random
import re

from . import data, travellermap
from .dice import Rng


def batch_seeds(seed, count):
    """Derive `count` reproducible child seeds from one batch seed."""
    if seed is None:
        return [None] * count
    r = random.Random(int(seed))
    return [r.randrange(2 ** 63) for _ in range(count)]

DEFAULT_OPTIONS = {
    "career": None,            # career key/name for the first career, or None = random
    "max_terms": data.MAX_TERMS_DEFAULT,
    "p_stay": 0.5,             # chance to reenlist when the roll succeeds
    "p_new_career": 0.5,       # chance to start another career instead of finishing
    "p_draft": 0.5,            # chance to submit to the Draft on failed qualification
    "survival_mishap": False,  # optional rule: mishap table instead of death
    "background_skills": True, # step 2 (homeworld step, optional in the SRD)
    "homeworld": True,         # pick a real homeworld from the TravellerMap API (False to disable)
    "sector": None,            # optional sector name/abbreviation for the homeworld
    "species": "human",        # human, avian, esper, insectan, merfolk, reptilian (CE SRD alien species)
    "name": None,
    "gender": None,
}

_BONUS_RE = re.compile(r"^\+(\d+)\s+([A-Za-z]+)$")
_CHAR3 = {"str": "STR", "dex": "DEX", "end": "END", "int": "INT", "edu": "EDU", "soc": "SOC"}


def resolve_career(ref):
    """Accept a career key ('marine') or name ('Marine'); return the career dict."""
    if ref is None:
        return None
    key = str(ref).strip().lower().replace(" ", "_")
    if key in data.CAREER_BY_KEY:
        return data.CAREER_BY_KEY[key]
    if str(ref).strip().lower() in data.CAREER_BY_NAME:
        return data.CAREER_BY_NAME[str(ref).strip().lower()]
    return None


class Generator:
    def __init__(self, seed=None, options=None):
        self.rng = Rng(seed)
        self.seed = self.rng.seed
        self.opts = dict(DEFAULT_OPTIONS)
        if options:
            unknown = set(options) - set(DEFAULT_OPTIONS)
            if unknown:
                raise ValueError(f"unknown options: {sorted(unknown)}")
            self.opts.update(options)
        self.species_key = data.resolve_species(self.opts.get("species"))
        if self.species_key is None:
            raise ValueError(f"unknown species: {self.opts.get('species')!r} "
                             f"(valid: {sorted(data.SPECIES)})")
        self.species = data.SPECIES[self.species_key]
        self.caste = None
        self.ageing_starts = self.species["ageing_starts"]
        self.psi = None
        self.appearance = None
        self.chars = {}
        self.skills = {}
        self.age = self.species["maturity"]
        self.credits = 0
        self.debt = 0
        self.equipment = []
        self.passages = []
        self.ship_shares = 0
        self.pension_annual = 0
        self.careers = []
        self.left = set()
        self.alive = True
        self.death_cause = None
        self.crisis = False
        self.draft_used = False
        self.background = []
        self.homeworld = None
        self.homeworld_error = None
        self.log = []

    # ------------------------------------------------------------------ util
    def say(self, msg):
        self.log.append(msg)

    def dm(self, char):
        return data.dm(self.chars[char])

    def roll2(self):
        dice = self.rng.d6(2)
        return dice, sum(dice)

    def check(self, char, target, extra=0, natural_two_fails=False):
        dice, total = self.roll2()
        mod = self.dm(char) + extra
        ok = total + mod >= target
        if natural_two_fails and dice == [1, 1]:
            ok = False
        return {"dice": dice, "char": char, "dm": mod, "total": total + mod,
                "target": target, "success": ok}

    def change_char(self, char, delta, source):
        if delta > 0:
            self.chars[char] = min(data.MAX_CHARACTERISTIC, self.chars[char] + delta)
            self.say(f"{char} +{delta} ({source}) -> {self.chars[char]}")
            return
        self.chars[char] += delta
        if self.chars[char] <= 0:
            self.chars[char] = 0
            self._crisis(char, source)
        else:
            self.say(f"{char} {delta} ({source}) -> {self.chars[char]}")

    def _crisis(self, char, source):
        """Characteristic reduced to 0: crisis. Death unless 1D6x10,000 Cr paid."""
        cost = self.rng.d6_sum() * 10000
        self.say(f"CRISIS: {char} reduced to 0 by {source}; medical care costs Cr{cost:,}")
        if self.credits >= cost:
            self.credits -= cost
            self.chars[char] = data.MIN_CHARACTERISTIC
            self.crisis = True
            self.say(f"Paid Cr{cost:,}: {char} restored to 1. Character now fails all qualification rolls.")
        else:
            self.alive = False
            self.death_cause = f"{source} crisis: {char} reduced to 0 (could not pay Cr{cost:,} medical care)"
            self.say(f"DEATH: {self.death_cause}")

    def resolve_skill(self, name):
        name = data.normalize_skill(name)
        if name in data.CASCADES:
            spec = self.rng.choice(data.CASCADES[name])
            return f"{name} ({spec})"
        if name in data.SPEC_TO_CASCADE:
            casc = data.SPEC_TO_CASCADE[name]
            return f"{casc} ({name})"
        return name

    def gain_skill(self, name):
        key = self.resolve_skill(name)
        self.skills[key] = self.skills.get(key, 0) + 1
        self.say(f"Skill gained: {key}-{self.skills[key]}")
        return key

    def set_skill0(self, name):
        key = self.resolve_skill(name)
        if key not in self.skills:
            self.skills[key] = 0
        return key

    def apply_table_entry(self, entry, source):
        """A Skills-and-Training table entry: '+1 Dex' or a skill name."""
        m = _BONUS_RE.match(entry)
        if m:
            char = _CHAR3[m.group(2).lower()]
            self.change_char(char, int(m.group(1)), source)
            return {"type": "characteristic", "char": char, "delta": int(m.group(1))}
        key = self.gain_skill(entry)
        return {"type": "skill", "skill": key, "level": self.skills[key]}

    # ------------------------------------------------------------- chargen
    def generate(self):
        self._roll_characteristics()
        if self.opts["homeworld"]:
            self._pick_homeworld()
        if self.opts["background_skills"]:
            self._background_skills()
        while self.alive:
            if self.total_terms() >= self.opts["max_terms"]:
                break
            first = not self.careers
            if first:
                career = resolve_career(self.opts["career"]) or self.rng.choice(data.CAREERS)
            else:
                if self.rng.random() >= self.opts["p_new_career"]:
                    break
                pool = [c for c in data.CAREERS if c["key"] not in self.left and c["key"] != "drifter"]
                if not pool:
                    career = data.CAREER_BY_KEY["drifter"]
                else:
                    career = self.rng.choice(pool)
            self._run_career(career, first=first)
            if not self.alive:
                break
            if self.total_terms() >= self.opts["max_terms"]:
                break
        self._final_details()
        return self.to_dict()

    def total_terms(self):
        return sum(1 for c in self.careers for t in c["terms"] if t.get("survived"))

    def _roll_char_spec(self, spec):
        m = re.match(r"^(\d+)D6?([+-]\d+)?$", spec)
        n, mod = int(m.group(1)), int(m.group(2) or 0)
        dice = self.rng.d6(n)
        return sum(dice) + mod, dice, spec

    def _roll_characteristics(self):
        self.say(f"Species: {self.species['name']}")
        caste_mods = {}
        self.caste = None
        if self.species.get("caste_table"):
            roll = self.rng.d6_sum()
            self.caste, caste_mods = data.DROYNE_CASTES[roll]
            bonus = data.DROYNE_CASTING_BONUS
            caste_mods = {c: caste_mods.get(c, 0) + bonus.get(c, 0) for c in data.CHARACTERISTICS}
            self.say(f"Droyne caste roll 1D6={roll}: {self.caste} (mods {caste_mods})")
        for c in data.CHARACTERISTICS:
            spec = self.species["char_rolls"].get(c, "2D6")
            value, dice, spec = self._roll_char_spec(spec)
            value += caste_mods.get(c, 0)
            self.chars[c] = max(data.MIN_CHARACTERISTIC, min(data.MAX_CHARACTERISTIC, value))
            self.say(f"{c}: {spec}={dice} -> {self.chars[c]} (DM{data.dm(self.chars[c]):+d})")
        for skill in self.species.get("bonus_skills", []):
            self.set_skill0(skill)
            self.say(f"Species trait skill: {self.resolve_skill(skill)}-0")

    def _pick_homeworld(self):
        world = travellermap.random_world(self.rng, sector=self.opts.get("sector"))
        if world is None:
            self.homeworld_error = "TravellerMap API unreachable (or unknown sector): no homeworld"
            self.say(f"Homeworld indisponible: {self.homeworld_error}")
        else:
            self.say(f"Homeworld from TravellerMap: {world['name']} ({world['sector']} {world['hex']}) "
                     f"UWP {world['uwp']} TL {world['tl']} trade codes: {', '.join(world['trade_codes']) or 'none'}")
        self.homeworld = world

    def _background_skills(self):
        n = max(1, 3 + self.dm("EDU"))
        picks = []
        if self.homeworld:
            hw = self.homeworld
            picks.append(data.HOMEWORLD_LAW_SKILLS.get(hw["law_descriptor"], "Gun Combat"))
            trade_skills = [data.HOMEWORLD_TRADE_SKILLS[c] for c in hw["trade_codes"]
                            if c in data.HOMEWORLD_TRADE_SKILLS]
            if trade_skills:
                picks.append(self.rng.choice(trade_skills))
            self.say(f"Homeworld skills from {hw['name']}: law {hw['law_descriptor']}, "
                     f"TL {hw['tl']}, trade codes {', '.join(hw['trade_codes']) or 'none'}")
        rest = self.rng.shuffle(data.EDUCATION_SKILLS)
        chosen = []
        for name in picks + rest:
            if len(chosen) >= n:
                break
            key = self.resolve_skill(name)
            if key in chosen:
                continue
            chosen.append(key)
            self.set_skill0(name)
        self.background = chosen
        self.say(f"Background skills ({n} = 3 + EDU DM): {', '.join(k + '-0' for k in chosen)}")

    def _qualify(self, career):
        if self.crisis:
            return {"auto_fail": "injury/aging crisis", "success": False}
        extra = -2 * len(self.careers)
        return self.check(career["qualification"]["char"], career["qualification"]["target"], extra=extra)

    def _run_career(self, career, first):
        drafted = False
        qual = self._qualify(career)
        if not qual.get("success"):
            self.say(f"Failed to qualify for {career['name']} (roll {qual.get('total')}, target {qual.get('target')})")
            if not self.draft_used and self.rng.random() < self.opts["p_draft"]:
                self.draft_used = True
                drafted = True
                career = data.CAREER_BY_KEY[self.rng.choice(data.DRAFT)]
                self.say(f"Submitted to the Draft -> {career['name']}")
            else:
                career = data.CAREER_BY_KEY["drifter"]
                self.say("Entering the Drifter career instead")
        record = {"career": career["name"], "key": career["key"], "drafted": drafted,
                  "qualification": qual, "terms": [], "rank": 0, "title": None,
                  "discharge": None, "benefits": [], "pension": 0}
        self.careers.append(record)
        self.say(f"== Career: {career['name']} ==")
        # basic training (step 4) + rank 0 skill
        if first:
            for entry in career["service_skills"]:
                if entry:
                    self.set_skill0(entry)
            self.say(f"Basic training: all Service Skills at level 0 ({', '.join(career['service_skills'])})")
        else:
            entry = self.rng.choice([e for e in career["service_skills"] if e])
            self.set_skill0(entry)
            self.say(f"Basic training: one Service Skill at level 0 ({entry})")
        rank0 = career["ranks"][0]
        if rank0.get("skill"):
            self.gain_skill(rank0["skill"])
            self.say(f"Rank 0 skill: {rank0['skill']}")
        # terms loop (steps 5-9)
        while self.alive:
            term_no = len(record["terms"]) + 1
            term = {"term": term_no}
            self.say(f"-- Term {term_no} in {career['name']} --")
            surv = self.check(career["survival"]["char"], career["survival"]["target"], natural_two_fails=True)
            term["survival"] = surv
            term["survived"] = surv["success"]
            self.say(f"Survival: 2D6={surv['dice']} DM{data.dm(self.chars[surv['char']]):+d} -> {surv['total']} vs {surv['target']}+ -> {'OK' if surv['success'] else 'FAILED'}")
            if not surv["success"]:
                if self.opts["survival_mishap"]:
                    self._survival_mishap(career, record, term)
                else:
                    self.alive = False
                    self.death_cause = f"failed survival roll in {career['name']} term {term_no} (2D6={surv['dice']}, total {surv['total']} vs {surv['target']}+)"
                    self.say(f"DEATH: {self.death_cause}")
                record["terms"].append(term)
                break
            # commission & advancement (step 6)
            skill_rolls = 2 if not career.get("commission") else 1
            if career.get("commission") and record["rank"] == 0 and not (drafted and term_no == 1):
                com = self.check(career["commission"]["char"], career["commission"]["target"])
                term["commission"] = com
                if com["success"]:
                    record["rank"] = 1
                    skill_rolls += 1
                    self.say(f"Commissioned: rank 1 ({career['ranks'][1]['title']})")
                    if career["ranks"][1].get("skill"):
                        self.gain_skill(career["ranks"][1]["skill"])
            if career.get("advancement") and 1 <= record["rank"] < 6:
                adv = self.check(career["advancement"]["char"], career["advancement"]["target"])
                term["advancement"] = adv
                if adv["success"]:
                    record["rank"] += 1
                    skill_rolls += 1
                    self.say(f"Advanced to rank {record['rank']} ({career['ranks'][record['rank']]['title']})")
                    if career["ranks"][record["rank"]].get("skill"):
                        self.gain_skill(career["ranks"][record["rank"]]["skill"])
            # skills and training (step 7)
            tables = ["personal_development", "service_skills", "specialist"]
            if self.chars["EDU"] >= 8:
                tables.append("advanced_education")
            gained = []
            for _ in range(skill_rolls):
                table = self.rng.choice(tables)
                roll = self.rng.d6_sum()
                entry = career[table][roll - 1]
                if entry is None:
                    continue
                gained.append({"table": table, "roll": roll, "entry": entry,
                               "result": self.apply_table_entry(entry, f"{career['name']} {table} {roll}")})
            term["skills"] = gained
            record["terms"].append(term)
            # aging (step 8)
            self.age += data.TERM_YEARS
            if self.age >= self.ageing_starts and self.alive:
                term["aging"] = self._aging()
            if not self.alive:
                break
            # re-enlistment (step 9)
            dice, total = self.roll2()
            reen = {"dice": dice, "total": total, "target": career["reenlistment"]}
            term["reenlistment"] = reen
            if total == 12:
                self.say(f"Re-enlistment: natural 12 -> must serve another term")
                continue
            if self.total_terms() >= self.opts["max_terms"]:
                self.say(f"Re-enlistment: {total} but {self.total_terms()} terms served -> must retire")
                break
            if total >= career["reenlistment"] and self.rng.random() < self.opts["p_stay"]:
                self.say(f"Re-enlistment: {total} vs {career['reenlistment']}+ -> stays for another term")
                continue
            self.say(f"Re-enlistment: {total} vs {career['reenlistment']}+ -> leaves {career['name']}")
            break
        record["title"] = career["ranks"][record["rank"]]["title"] or career["name"]
        # mustering out (step 10)
        if self.alive and record["discharge"] != "dishonorable":
            self._muster_out(career, record)
        elif record["discharge"] == "dishonorable":
            self.say(f"Dishonorable discharge from {career['name']}: all benefits lost")
        self.left.add(career["key"])
        self.say(f"== {career['name']} ends: rank {record['rank']} ({record['title']}), {sum(1 for t in record['terms'] if t.get('survived'))} term(s) ==")

    def _survival_mishap(self, career, record, term):
        roll = self.rng.d6_sum()
        mishap = data.SURVIVAL_MISHAPS[roll - 1]
        term["mishap"] = {"roll": roll, "effect": mishap}
        self.say(f"Survival mishap (1D6={roll}): {mishap}")
        self.age += 2  # forced out after half a term
        if mishap == "injured_in_action":
            r1, r2 = self.rng.d6_sum(), self.rng.d6_sum()
            self._injury(min(r1, r2))
        elif mishap == "legal_battle":
            record["discharge"] = "honorable"
            self.debt += 10000
            self.say("Legal battle: debt of Cr10,000")
        elif mishap in ("honorable_discharge",):
            record["discharge"] = "honorable"
        elif mishap in ("dishonorable_discharge", "dishonorable_prison"):
            record["discharge"] = "dishonorable"
            if mishap == "dishonorable_prison":
                self.age += 4
                self.say("Extra 4 years in prison")
        elif mishap == "medical_discharge":
            record["discharge"] = "honorable"
            self._injury(self.rng.d6_sum())
        # no benefit roll for the current (half) term

    def _injury(self, roll):
        effect = data.INJURY_TABLE[roll - 1]
        self.say(f"Injury table (1D6={roll}): {effect}")
        if effect == "nearly_killed":
            chars = self.rng.shuffle(data.PHYSICAL)
            self.change_char(chars[0], -self.rng.d6_sum(), "nearly killed")
            if self.alive:
                self.change_char(chars[1], -2, "nearly killed")
            if self.alive:
                self.change_char(chars[2], -2, "nearly killed")
        elif effect == "severely_injured":
            self.change_char(self.rng.choice(data.PHYSICAL), -self.rng.d6_sum(), "severely injured")
        elif effect == "missing_eye_or_limb":
            self.change_char(self.rng.choice(["STR", "DEX"]), -2, "missing eye or limb")
        elif effect == "scarred":
            self.change_char(self.rng.choice(data.PHYSICAL), -2, "scarred")
        elif effect == "injured":
            self.change_char(self.rng.choice(data.PHYSICAL), -1, "injured")
        else:
            self.say("Lightly injured: no permanent effect")

    def _aging(self):
        dice, total = self.roll2()
        net = total - self.total_terms()
        for threshold, effects in data.AGING_TABLE:
            if net <= threshold:
                break
        event = {"dice": dice, "terms_dm": -self.total_terms(), "net": net, "effects": []}
        self.say(f"Aging at {self.age}: 2D6={dice} - {self.total_terms()} terms = {net} -> {effects or 'no effect'}")
        for kind, count, amount in effects:
            if not self.alive:
                break
            if kind == "physical":
                for char in self.rng.shuffle(data.PHYSICAL)[:count]:
                    self.change_char(char, -amount, f"aging (net {net})")
                    event["effects"].append({"char": char, "delta": -amount})
            else:
                char = self.rng.choice(data.MENTAL)
                self.change_char(char, -amount, f"aging (net {net})")
                event["effects"].append({"char": char, "delta": -amount})
        return event

    def _muster_out(self, career, record):
        terms = sum(1 for t in record["terms"] if t.get("survived"))
        num_benefits = terms + max(0, record["rank"] - 3)
        if num_benefits <= 0:
            return
        self.say(f"Mustering out of {career['name']}: {num_benefits} benefit roll(s) ({terms} terms + rank bonus)")
        cash_left = 3
        has_gambling = any(k.startswith("Gambling") for k in self.skills)
        retired = terms >= 5
        for _ in range(num_benefits):
            if cash_left > 0 and self.rng.random() < 0.5:
                cash_left -= 1
                roll = self.rng.d6_sum() + (1 if (has_gambling or retired) else 0)
                roll = min(roll, 7)
                amount = career["cash_benefits"][roll - 1] or 0
                self.credits += amount
                record["benefits"].append(f"Cash Cr{amount:,} (1D6={roll})")
                self.say(f"Benefit: cash Cr{amount:,} (roll {roll})")
            else:
                roll = self.rng.d6_sum() + (1 if record["rank"] >= 5 else 0)
                roll = min(roll, 7)
                entry = career["material_benefits"][roll - 1]
                self._apply_material(entry, roll, record)
        pension = data.retirement_pay(terms)
        if pension:
            record["pension"] = pension
            self.pension_annual = max(self.pension_annual, pension)
            self.say(f"Retirement pension: Cr{pension:,}/year ({terms} terms in {career['name']})")

    def _apply_material(self, entry, roll, record):
        if entry is None:
            record["benefits"].append(f"nothing (roll {roll})")
            self.say(f"Benefit roll {roll}: no benefit")
            return
        m = _BONUS_RE.match(entry)
        if m:
            char = _CHAR3[m.group(2).lower()]
            self.change_char(char, int(m.group(1)), "mustering-out benefit")
            record["benefits"].append(f"{entry} (roll {roll})")
            return
        if entry == "1D6 Ship Shares":
            n = self.rng.d6_sum()
            self.ship_shares += n
            record["benefits"].append(f"{n} Ship Shares (roll {roll})")
            self.say(f"Benefit: {n} ship shares (Cr2,000,000 each)")
            return
        if entry == "Weapon":
            if not any(e.startswith("Weapon") for e in self.equipment):
                self.equipment.append("Weapon (service issue)")
                record["benefits"].append(f"Weapon (roll {roll})")
                self.say(f"Benefit: weapon (roll {roll})")
            else:
                casc = self.rng.choice(["Gun Combat", "Melee Combat"])
                spec = self.rng.choice(data.CASCADES[casc])
                key = self.gain_skill(f"{casc} ({spec})")
                record["benefits"].append(f"Weapon taken as skill {key} (roll {roll})")
            return
        if entry in ("Low Passage", "Mid Passage", "High Passage"):
            self.passages.append(entry)
        elif entry in ("Explorers' Society", "Courier Vessel", "Research Vessel"):
            if entry not in self.equipment:
                self.equipment.append(entry)
            else:
                self.say(f"Benefit roll {roll}: {entry} already held, no additional benefit")
                record["benefits"].append(f"{entry} (duplicate, roll {roll})")
                return
        record["benefits"].append(f"{entry} (roll {roll})")
        self.say(f"Benefit: {entry} (roll {roll})")

    def _eval_formula(self, formula):
        m = re.match(r"^(\d+)\+\(2D6x(\d+)\)$", formula)
        base, mult = int(m.group(1)), int(m.group(2))
        return base + self.rng.d6_sum(2) * mult

    def _final_details(self):
        gender = self.opts["gender"] or self.rng.choice(["M", "F"])
        if self.opts["name"]:
            name = self.opts["name"]
        else:
            name = data.make_name(self.rng, self.species_key, gender)
        self.name = name
        self.gender = gender
        if self.species.get("height_cm"):
            self.appearance = {
                "height_cm": self._eval_formula(self.species["height_cm"]),
                "mass_kg": self._eval_formula(self.species["mass_kg"]),
            }
        if "Psionic" in self.species["traits"] or self.species.get("psi_always_rolled"):
            # PSI = 2D6 - terms served (SRD psionics chapter)
            psi = self.rng.d6_sum(2) - self.total_terms()
            self.psi = max(0, psi)
            self.say(f"Psionic Strength (2D6 - {self.total_terms()} terms): PSI {self.psi}")

    def upp(self):
        s = data.upp_string(self.chars)
        if self.psi:
            s += f"-{data.pseudohex(self.psi)}"
        return s

    # ------------------------------------------------------------------ out
    def to_dict(self):
        return {
            "seed": self.seed,
            "name": self.name,
            "gender": self.gender,
            "species": self.species["name"],
            "species_key": self.species_key,
            "species_description": self.species.get("description"),
            "caste": self.caste,
            "traits": self.species["traits"],
            "psi": self.psi,
            "appearance": self.appearance,
            "age": self.age,
            "upp": self.upp(),
            "characteristics": {c: {"value": self.chars[c], "dm": data.dm(self.chars[c])} for c in data.CHARACTERISTICS},
            "skills": dict(sorted(self.skills.items())),
            "careers": [{
                "career": c["career"], "key": c["key"], "drafted": c["drafted"],
                "qualification": c["qualification"], "terms_served": sum(1 for t in c["terms"] if t.get("survived")),
                "rank": c["rank"], "title": c["title"], "discharge": c["discharge"],
                "benefits": c["benefits"], "pension_annual": c["pension"],
                "terms": c["terms"],
            } for c in self.careers],
            "background_skills": self.background,
            "homeworld": self.homeworld,
            "homeworld_error": self.homeworld_error,
            "credits": self.credits,
            "debt": self.debt,
            "passages": self.passages,
            "ship_shares": self.ship_shares,
            "equipment": self.equipment,
            "pension_annual": self.pension_annual,
            "alive": self.alive,
            "death_cause": self.death_cause,
            "history": self.log,
        }

    def to_text(self):
        d = self.to_dict()
        lines = []
        lines.append(f"{d['name']} {d['upp']} Age {d['age']} ({d['species']}" + (f", caste {d['caste']}" if d.get("caste") else "") + ")")
        if d["traits"]:
            lines.append("Traits: " + ", ".join(d["traits"]))
        if d["appearance"]:
            lines.append(f"Apparence: {d['appearance']['height_cm']} cm, {d['appearance']['mass_kg']} kg")
        if not d["homeworld"] and d.get("homeworld_error"):
            lines.append(f"Homeworld: indisponible ({d['homeworld_error']})")
        if d["homeworld"]:
            hw = d["homeworld"]
            loc = f"{hw['sector']} {hw['hex']}" if hw.get("sector") else "?"
            tl = data.pseudohex(hw["tl"]) if hw.get("tl") is not None else "?"
            lines.append(f"Homeworld: {hw['name']} ({loc}) - TL {tl}")
            fields = []
            if hw.get("starport"):
                sp = data.STARPORT_CLASS.get(hw["starport"])
                fields.append(f"spatioport {hw['starport']}" + (f" ({sp})" if sp else ""))
            for key, label in (("size", "taille"), ("atmosphere", "atmosphere"), ("hydrosphere", "hydrosphere"),
                               ("population", "population"), ("government", "gouvernement")):
                if hw.get(key) is not None:
                    fields.append(f"{label} {data.pseudohex(hw[key])}")
            if hw.get("law") is not None:
                fields.append(f"loi {data.pseudohex(hw['law'])} ({hw.get('law_descriptor')})")
            lines.append(f"  UWP: {hw.get('uwp') or '?'} ({', '.join(fields)})")
            codes = "; ".join(data.trade_code_label(c) for c in hw.get("trade_codes") or []) or "aucun"
            lines.append(f"  Codes commerciaux: {codes}")
        careers = ", ".join(f"{c['career']} ({c['terms_served']} term{'s' if c['terms_served'] != 1 else ''})" for c in d["careers"])
        lines.append(f"{careers} Cr{d['credits']:,}")
        skills = ", ".join(f"{k}-{v}" for k, v in d["skills"].items())
        lines.append(skills)
        if d["passages"]:
            lines.append("Passages: " + ", ".join(d["passages"]))
        if d["equipment"]:
            lines.append("Equipment: " + ", ".join(d["equipment"]))
        if d["ship_shares"]:
            lines.append(f"Ship shares: {d['ship_shares']} (Cr{d['ship_shares'] * 2000000:,})")
        if d["pension_annual"]:
            lines.append(f"Pension: Cr{d['pension_annual']:,}/year")
        if not d["alive"]:
            lines.append(f"DECEASED: {d['death_cause']}")
        return "\n".join(lines)


def generate_character(seed=None, options=None):
    """Generate one character; returns the character dict (see Generator.to_dict)."""
    gen = Generator(seed=seed, options=options)
    return gen.generate()
