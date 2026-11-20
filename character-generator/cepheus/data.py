"""Static rules data from the Cepheus Engine SRD (Open Gaming Content).

Sources: Cepheus Engine System Reference Document (Samardan Press), chapter 1
"Character Creation" (and chapter 2 "Skills" for cascade specializations).
Career tables are parsed from the SRD markdown into data/careers.json by
tools/parse_srd_careers.py.
"""
import json
from pathlib import Path

CHARACTERISTICS = ["STR", "DEX", "END", "INT", "EDU", "SOC"]
PHYSICAL = ["STR", "DEX", "END"]
MENTAL = ["INT", "EDU", "SOC"]

START_AGE = 18
TERM_YEARS = 4
AGEING_STARTS_AT = 34
MAX_TERMS_DEFAULT = 7
MAX_CHARACTERISTIC = 15
MIN_CHARACTERISTIC = 1
CRISIS_COST = "1D6x10000"  # credits, per aging/injury crisis

_CHAR_NAMES = {"str": "STR", "dex": "DEX", "end": "END", "int": "INT", "edu": "EDU", "soc": "SOC"}


def dm(value):
    """Characteristic modifier: floor(score/3) - 2 (SRD p.24)."""
    return value // 3 - 2


def pseudohex(value):
    if value < 10:
        return str(value)
    if value <= 35:
        return chr(ord("A") + value - 10)
    return "Z"


def upp_string(chars):
    return "".join(pseudohex(chars[c]) for c in CHARACTERISTICS)


def parse_check_text(text):
    """'End 8+' -> ('END', 8)."""
    name, target = text.split()
    return _CHAR_NAMES[name.lower()], int(target.rstrip("+"))


def normalize_skill(name):
    name = name.strip()
    return SKILL_ALIASES.get(name, name)


SKILL_ALIASES = {
    "Pilot": "Piloting",       # typo in some SRD career tables
    "Liaision": "Liaison",     # typo in Colonist rank table
}

# Cascade skills and their specializations (SRD chapter 2, "Cascade Skills").
CASCADES = {
    "Aircraft": ["Airship", "Grav Vehicle", "Rotor Aircraft", "Winged Aircraft"],
    "Animals": ["Farming", "Riding", "Survival", "Veterinary Medicine"],
    "Gun Combat": ["Archery", "Energy Pistol", "Energy Rifle", "Shotgun", "Slug Pistol", "Slug Rifle"],
    "Gunnery": ["Bay Weapons", "Heavy Weapons", "Screens", "Spinal Mounts", "Turret Weapons"],
    "Melee Combat": ["Natural Weapons", "Bludgeoning Weapons", "Piercing Weapons", "Slashing Weapons"],
    "Sciences": ["Life Sciences", "Physical Sciences", "Social Sciences", "Space Sciences"],
    "Vehicle": ["Aircraft", "Mole", "Tracked Vehicle", "Watercraft", "Wheeled Vehicle"],
    "Watercraft": ["Motorboats", "Ocean Ships", "Sailing Ships", "Submarine"],
}
SPEC_TO_CASCADE = {spec: casc for casc, specs in CASCADES.items() for spec in specs}

EDUCATION_SKILLS = [
    "Admin", "Advocate", "Animals", "Carousing", "Comms", "Computer", "Electronics",
    "Engineering", "Life Sciences", "Linguistics", "Mechanics", "Medicine",
    "Physical Sciences", "Social Sciences", "Space Sciences",
]

HOMEWORLD_LAW_SKILLS = {
    "No Law": "Gun Combat", "Low Law": "Gun Combat", "Medium Law": "Gun Combat",
    "High Law": "Melee Combat",
}
HOMEWORLD_TRADE_SKILLS = {
    "Agricultural": "Animals", "Asteroid": "Zero-G", "Desert": "Survival",
    "Fluid Oceans": "Watercraft", "Garden": "Animals", "High Technology": "Computer",
    "High Population": "Streetwise", "Ice-Capped": "Zero-G", "Industrial": "Broker",
    "Low Technology": "Survival", "Poor": "Animals", "Rich": "Carousing",
    "Water World": "Watercraft", "Vacuum": "Zero-G",
}

# Trade codes: short code + UWP condition (CE SRD, chapter "Worlds", "UWP Values
# for Trade Codes") + short description (classic Traveller OGL wording).
TRADE_CODE_INFO = {
    "Agricultural": {"code": "Ag", "condition": "atmo 4-9, hydro 4-8, pop 5-7",
                     "description": "Monde agricole, produit nourriture et matieres organiques"},
    "Asteroid": {"code": "As", "condition": "size 0, atmo 0, hydro 0",
                 "description": "Ceinture d'asteroides, aucun monde habitable de taille planetaire"},
    "Barren": {"code": "Ba", "condition": "pop 0, gov 0, law 0",
               "description": "Monde desert, sans population ni gouvernement"},
    "Desert": {"code": "De", "condition": "atmo 2+, hydro 0",
               "description": "Monde aride, peu de precipitations"},
    "Fluid Oceans": {"code": "Fl", "condition": "atmo 10+, hydro 1+",
                     "description": "Surface presque entierement liquide"},
    "Garden": {"code": "Ga", "condition": "atmo 5/6/8, hydro 4-9, pop 4-8",
               "description": "Monde de type terrestre, vegetation abondante"},
    "High Population": {"code": "Hi", "condition": "pop 9+",
                        "description": "Milliards d'habitants"},
    "High Technology": {"code": "Ht", "condition": "TL 12+",
                        "description": "Technologie avancee, niveau technologique 12 ou plus"},
    "Ice-Capped": {"code": "Ic", "condition": "atmo 0-1, hydro 1+",
                   "description": "Glace couvrant la majeure partie de la surface"},
    "Industrial": {"code": "In", "condition": "atmo 0/2/4/7/9, pop 9+",
                   "description": "Monde industrialise, forte production manufacturiere"},
    "Low Population": {"code": "Lo", "condition": "pop 1-3",
                       "description": "Moins d'un million d'habitants"},
    "Low Technology": {"code": "Lt", "condition": "TL 5 ou moins",
                       "description": "Technologie primitive, niveau technologique 5 ou moins"},
    "Non-Agricultural": {"code": "Na", "condition": "atmo 0-3, hydro 0-3, pop 6+",
                         "description": "Monde impropre a l'agriculture"},
    "Non-Industrial": {"code": "Ni", "condition": "pop 4-6",
                       "description": "Peu ou pas d'industrie"},
    "Poor": {"code": "Po", "condition": "atmo 2-5, hydro 0-3",
             "description": "Economie primitive, peu de commerce"},
    "Rich": {"code": "Ri", "condition": "atmo 6 ou 8, pop 6-8",
             "description": "Niveau de vie eleve, industrie et/ou agriculture developpees"},
    "Water World": {"code": "Wa", "condition": "hydro 10",
                    "description": "Monde ocean, hydrographie 10"},
    "Vacuum": {"code": "Va", "condition": "atmo 0",
               "description": "Sans atmosphere"},
}


# Starport classes (CE SRD, chapter "Worlds", "Starport Class Services").
STARPORT_CLASS = {
    "A": "Excellent", "B": "Good", "C": "Routine", "D": "Poor", "E": "Frontier", "X": "None",
}


def trade_code_label(name):
    """'Garden' -> 'Ga Garden - Monde de type terrestre, vegetation abondante'."""
    info = TRADE_CODE_INFO.get(name)
    if not info:
        return name
    return f"{info['code']} {name} - {info['description']}"

# The Draft (SRD p.28), 1D6.
DRAFT = ["aerospace_defense", "marine", "maritime_defense", "navy", "scout", "surface_defense"]

# Aging table (SRD p.30). Roll 2D6 minus total terms served; the table is
# indexed by that net result: -6 or less ... 1+ (no effect).
AGING_TABLE = [
    (-6, [("physical", 3, 2), ("mental", 1, 1)]),
    (-5, [("physical", 3, 2)]),
    (-4, [("physical", 2, 2), ("physical", 1, 1)]),
    (-3, [("physical", 1, 2), ("physical", 2, 1)]),
    (-2, [("physical", 3, 1)]),
    (-1, [("physical", 2, 1)]),
    (0, [("physical", 1, 1)]),
    (1, []),
]

# Injury table (SRD p.29), 1D6. Effects are applied by the generator.
INJURY_TABLE = [
    "nearly_killed",        # one physical -1D6, both others -2 (or one -4)
    "severely_injured",     # one physical -1D6
    "missing_eye_or_limb",  # STR or DEX -2
    "scarred",              # any one physical -2
    "injured",              # any one physical -1
    "lightly_injured",      # no permanent effect
]

# Survival mishaps (SRD p.28, optional rule), 1D6.
SURVIVAL_MISHAPS = [
    "injured_in_action",    # as injury table 2, or twice on injury table take lower
    "honorable_discharge",
    "legal_battle",         # honorable discharge, debt Cr10,000
    "dishonorable_discharge",
    "dishonorable_prison",  # +4 years prison, lose all benefits
    "medical_discharge",    # roll on injury table
]


def retirement_pay(terms_in_service):
    """Annual pension for 5+ terms in a single service (SRD p.31)."""
    if terms_in_service < 5:
        return 0
    return 8000 + 2000 * (terms_in_service - 4)


CAREERS = json.loads((Path(__file__).parent / "data" / "careers.json").read_text(encoding="utf-8"))
CAREER_BY_KEY = {c["key"]: c for c in CAREERS}
CAREER_BY_NAME = {c["name"].lower(): c for c in CAREERS}

FIRST_NAMES_M = [
    "Adrien", "Alex", "Antoine", "Armand", "Barnab\u00e9", "Boris", "C\u00e9dric", "Cl\u00e9ment",
    "Damien", "Dorian", "Elias", "Emilien", "Fabien", "Franck", "Friedrich", "Gaspard",
    "Georges", "Hugo", "Ivan", "Jacques", "Jonas", "Julien", "Karl", "Kenji", "Leo",
    "Luc", "Louis", "Marc", "Mateo", "Mathieu", "Milan", "Nikolai", "Noah", "Oscar",
    "Pablo", "Paul", "Peter", "Philémon", "Piotr", "Quentin", "Raphaël", "Romain",
    "Samuel", "Sasha", "Sebastian", "Stefan", "Théo", "Thibault", "Ulysse", "Victor",
    "Vincent", "Wendell", "Xavier", "Yann", "Yusuf", "Zacharie", "Émile", "Étienne",
    "Hökan", "J\u00fcrgen", "S\u00f8ren", "Marek", "Tomas", "Rui", "Bruno", "Anders",
]
FIRST_NAMES_F = [
    "Adèle", "Alice", "Amélie", "Anna", "Brigitte", "Camille", "Chloé", "Claire",
    "Clémence", "Dana", "Delphine", "Elsa", "Emma", "Fatou", "Fleur", "Gisèle",
    "Hana", "Inès", "Ingrid", "Julia", "Karina", "Katya", "Léa", "Lena",
    "Lise", "Mara", "Mira", "Mona", "Nadia", "Nina", "Noémie", "Olga",
    "Paula", "Quinn", "Rosa", "Sara", "Sofia", "Tania", "Ursula", "Vera",
    "Wanda", "Xenia", "Yuki", "Zoé", "Anaïs", "Béatrice", "Célia", "Élise",
    "Hélène", "Joséphine", "Louise", "Margot", "Salomé", "Agathe", "Romane", "Alba",
    "Freya", "Sigrid", "Anya", "Lena", "Mira", "Eszter", "Nadia", "Petra",
]
FAMILY_NAMES = [
    "Almeida", "Barros", "Benali", "Costa", "Dubois", "Durand", "Fabre", "Fontaine",
    "Gagnon", "Garcia", "Haddad", "Ivanov", "Jansen", "Keller", "Kowalski", "Larsen",
    "Lefebvre", "Lindqvist", "Mendes", "Moreau", "Novak", "Okafor", "Olsen", "Petrov",
    "Petrova", "Quintero", "Rossi", "Roy", "Silva", "Szabo", "Tremblay", "Ueda",
    "Vargas", "Wojcik", "Xu", "Yilmaz", "Zhang", "Berger", "Blanchard", "Bonnet",
    "Carrier", "Chevalier", "Dufour", "Gauthier", "Girard", "Lacroix", "Lemaire", "Leroy",
    "Marchand", "Martin", "Mercier", "Meyer", "Muller", "Nguyen", "Perrin", "Roche",
    "Rousseau", "Schmidt", "Tanaka", "Vidal", "Weber", "Aalto", "Bakker", "Castillo",
    "Dubois", "Ekström", "Fischer", "Grimaldi", "Hoffmann", "Ibrahim", "Jensen", "Kaur",
]

# Official alien species of the CE SRD ("On Alien Species", chapter 1).
# char_rolls: how each characteristic is generated instead of plain 2D6
# ("1D6", "3D6", "2D6+2", "2D6-2", ...). ageing_starts: age at which aging rolls begin.
SPECIES = {
    "human": {
        "name": "Human", "char_rolls": {}, "traits": [],
        "maturity": 18, "ageing_starts": 34, "height_cm": None, "mass_kg": None,
    },
    "avian": {
        "name": "Avian", "char_rolls": {"STR": "1D6", "DEX": "3D6", "END": "1D6"},
        "traits": ["Flyer (9m)", "Low Gravity Adaptation", "Natural Pilot", "Slow Speed (4.5m)", "Small"],
        "maturity": 22, "ageing_starts": 46,
        "height_cm": "105+(2D6x2)", "mass_kg": "20+(2D6x2)",
    },
    "esper": {
        "name": "Esper", "char_rolls": {}, "traits": ["Psionic"],
        "maturity": 18, "ageing_starts": 34, "height_cm": None, "mass_kg": None,
    },
    "insectan": {
        "name": "Insectan", "char_rolls": {"DEX": "2D6+2"}, "soc_name": "Caste",
        "traits": ["Armored", "Bad First Impression", "Caste", "Cold-blooded", "Fast Speed (9m)",
                   "Great Leaper", "Hive Mentality"],
        "bonus_skills": ["Athletics"],  # Great Leaper trait
        "maturity": 18, "ageing_starts": 34,
        "height_cm": "160+(2D6x5)", "mass_kg": "60+(2D6x5)",
    },
    "merfolk": {
        "name": "Merfolk", "char_rolls": {},
        "traits": ["Amphibious", "Aquatic", "Natural Swimmer", "Water Dependent"],
        "maturity": 18, "ageing_starts": 34, "height_cm": None, "mass_kg": None,
    },
    "reptilian": {
        "name": "Reptilian", "char_rolls": {"STR": "2D6+1", "DEX": "2D6+1", "END": "2D6-2"},
        "traits": ["Anti-Psionic", "Fast Speed (9m)", "Heat Endurance", "Low-Light Vision",
                   "Natural Weapon (teeth)", "Low Gravity Adaptation"],
        "bonus_skills": ["Melee Combat (Natural Weapons)"],  # Natural Weapon trait
        "maturity": 22, "ageing_starts": 42,
        "height_cm": "155+(2D6x5)", "mass_kg": "50+(2D6x5)",
    },
    # Major races of the Official Traveller Universe (Traveller Wiki /
    # Mongoose Traveller data). char_rolls expressed as 2D6 +/- modifiers
    # (CE "Notable/Weak characteristic" style).
    "aslan": {
        "name": "Aslan", "char_rolls": {"STR": "2D6+2", "DEX": "2D6-2"},
        "traits": ["Dewclaw (Natural Weapon, 1D+2)", "Heightened Senses (DM+1 Recon/Survival)"],
        "bonus_skills": ["Melee Combat (Natural Weapons)"],
        "maturity": 18, "ageing_starts": 34,
        "homeworld": "Kusyu (Dark Nebula 1226)",
        "description": "Race majeure felinoide de l'Aslan Hierate. Maux de griffes (dewclaw), sens aiguises.",
    },
    "vargr": {
        "name": "Vargr", "char_rolls": {"STR": "2D6-1", "DEX": "2D6+1", "END": "2D6-1"},
        "traits": ["Bite (Natural Weapon, 1D+1)", "Heightened Senses", "Adapted Charisma (DM+1 Persuade/Leadership informel)"],
        "bonus_skills": ["Melee Combat (Natural Weapons)"],
        "maturity": 18, "ageing_starts": 34,
        "description": "Race majeure canine des Vargr Extents, partiellement uplift par les Anciens.",
    },
    "kkree": {
        "name": "K'kree", "char_rolls": {"STR": "2D6+6", "INT": "2D6+2", "EDU": "2D6+2"},
        "traits": ["Big and Tough (degats END reduits de moitie)", "Claustrophobic", "Gregarious",
                   "Speed of Hoof", "Militant Herbivore"],
        "maturity": 18, "ageing_starts": 34,
        "homeworld": "Kirur (Ruupiin 1315)",
        "description": "Hexapodes centauroïdes herbivores des Two Thousand Worlds, tres puissants et grégaires.",
    },
    "droyne": {
        "name": "Droyne", "char_rolls": {"STR": "1D+1", "DEX": "1D+1", "END": "1D+1",
                                        "INT": "1D+1", "EDU": "1D+1", "SOC": "1D+1"},
        "caste_table": True, "psi_always_rolled": True,
        "traits": ["Wings (Flight)", "Claws (Natural Weapon, 1D+2)", "Caste (remplace le statut social)"],
        "bonus_skills": ["Melee Combat (Natural Weapons)", "Athletics (Flying)"],
        "maturity": 12, "ageing_starts": 28,  # aging from 4th term
        "description": "Hexapodes ailés de la Droyne Ascendancy, organisés en castes (tirage 1D6 à l'adolescence).",
    },
    "hiver": {
        "name": "Hiver", "char_rolls": {"STR": "2D6-2", "INT": "2D6+2", "EDU": "2D6+2"},
        "soc_name": "Resolve",
        "traits": ["No vocal cords (sign language / Voder)", "No Psionics", "Indirect Approach"],
        "maturity": 14, "ageing_starts": 38,  # aging from 6th term
        "description": "Hexapodes manipulateurs de la Hive Federation ; Resolve (RES) remplace SOC, pas de psionics.",
    },
}

# Droyne castes (1D6 at adolescence) and their characteristic modifiers,
# plus the universal casting bonus (Mongoose Traveller / Traveller Wiki data).
DROYNE_CASTES = {
    1: ("Worker", {"STR": 2, "END": 4}),
    2: ("Warrior", {"STR": 3, "DEX": 1, "END": 2}),
    3: ("Drone", {"DEX": 1, "INT": 3, "EDU": 2}),
    4: ("Technician", {"DEX": 2, "INT": 3, "EDU": 1}),
    5: ("Sport", {"DEX": 1, "END": 1, "INT": 2, "EDU": 2}),
    6: ("Leader", {"INT": 4, "EDU": 2}),
}
DROYNE_CASTING_BONUS = {"STR": 1, "DEX": 1, "END": 1, "INT": 1, "EDU": 1}

SPECIES_ALIASES = {
    "human": "human", "humain": "human", "humans": "human",
    "avian": "avian", "avians": "avian", "aviaire": "avian", "aviaires": "avian",
    "esper": "esper", "expers": "esper", "espers": "esper",
    "insectan": "insectan", "insectans": "insectan", "insectoïde": "insectan", "insectoide": "insectan",
    "merfolk": "merfolk", "merfolks": "merfolk", "sirène": "merfolk", "sirene": "merfolk",
    "reptilian": "reptilian", "reptilians": "reptilian", "reptilien": "reptilian", "reptiliens": "reptilian",
    "aslan": "aslan", "aslans": "aslan",
    "vargr": "vargr", "vargrs": "vargr", "vargre": "vargr",
    "kkree": "kkree", "k'kree": "kkree", "k_kree": "kkree", "kree": "kkree",
    "droyne": "droyne", "droynes": "droyne",
    "hiver": "hiver", "hivers": "hiver", "hivern": "hiver",
}


def resolve_species(ref):
    if ref is None:
        return "human"
    return SPECIES_ALIASES.get(str(ref).strip().lower())
