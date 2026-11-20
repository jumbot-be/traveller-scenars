import unittest
from unittest import mock

from cepheus import data
from cepheus.character import Generator, batch_seeds, generate_character, resolve_career


def gen(seed, **options):
    return generate_character(seed=seed, options=options or None)


class TestData(unittest.TestCase):
    def test_24_careers(self):
        self.assertEqual(len(data.CAREERS), 24)
        for c in data.CAREERS:
            self.assertEqual(len(c["ranks"]), 7)
            self.assertEqual(len(c["service_skills"]), 6)
            self.assertEqual(len(c["personal_development"]), 6)
            self.assertEqual(len(c["specialist"]), 6)
            self.assertEqual(len(c["advanced_education"]), 6)
            self.assertEqual(len(c["material_benefits"]), 7)
            self.assertEqual(len(c["cash_benefits"]), 7)
            self.assertIn("char", c["qualification"])
            self.assertIn("char", c["survival"])
            self.assertIsInstance(c["reenlistment"], int)

    def test_dm_table(self):
        self.assertEqual(data.dm(2), -2)
        self.assertEqual(data.dm(3), -1)
        self.assertEqual(data.dm(6), 0)
        self.assertEqual(data.dm(9), 1)
        self.assertEqual(data.dm(12), 2)
        self.assertEqual(data.dm(15), 3)

    def test_pseudohex(self):
        self.assertEqual(data.pseudohex(7), "7")
        self.assertEqual(data.pseudohex(12), "C")
        self.assertEqual(data.pseudohex(15), "F")
        chars = {"STR": 7, "DEX": 7, "END": 5, "INT": 4, "EDU": 7, "SOC": 12}
        self.assertEqual(data.upp_string(chars), "77547C")

    def test_resolve_career(self):
        self.assertEqual(resolve_career("marine")["key"], "marine")
        self.assertEqual(resolve_career("Marine")["key"], "marine")
        self.assertEqual(resolve_career("surface_defense")["name"], "Surface System Defense")
        self.assertIsNone(resolve_career("jedi"))


class TestGeneration(unittest.TestCase):
    def setUp(self):
        # keep tests hermetic: no real TravellerMap calls (homeworld skipped)
        patcher = mock.patch("cepheus.character.travellermap.random_world", return_value=None)
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_determinism(self):
        a = gen(1234)
        b = gen(1234)
        self.assertEqual(a, b)
        self.assertEqual(a["seed"], 1234)

    def test_batch_seeds(self):
        seeds = batch_seeds(7, 3)
        self.assertEqual(len(seeds), 3)
        self.assertEqual(len(set(seeds)), 3)
        self.assertEqual(seeds, batch_seeds(7, 3))
        self.assertEqual(batch_seeds(None, 2), [None, None])

    def test_characteristics_and_structure(self):
        for seed in range(150):
            c = gen(seed)
            self.assertEqual(len(c["characteristics"]), 6)
            for ch, v in c["characteristics"].items():
                self.assertGreaterEqual(v["value"], 0)
                self.assertEqual(v["dm"], data.dm(v["value"]))
                if c["alive"]:
                    self.assertGreaterEqual(v["value"], 1)
                    self.assertLessEqual(v["value"], 15)
            self.assertRegex(c["upp"], r"^[0-9A-F]{6}$")
            self.assertGreaterEqual(c["age"], 18)
            self.assertGreaterEqual(c["age"], 18 + 4 * sum(x["terms_served"] for x in c["careers"]) - 4)
            self.assertTrue(c["careers"])
            for career in c["careers"]:
                self.assertIn(career["key"], data.CAREER_BY_KEY)
                if c["alive"] and career["discharge"] != "dishonorable":
                    expected_max = career["terms_served"] + max(0, career["rank"] - 3)
                    self.assertLessEqual(len(career["benefits"]), expected_max)

    def test_skills_are_valid(self):
        for seed in range(150):
            c = gen(seed)
            for skill, level in c["skills"].items():
                self.assertGreaterEqual(level, 0)
                base = skill.split(" (")[0]
                if base in data.CASCADES or skill in data.SPEC_TO_CASCADE:
                    self.assertIn("(", skill, f"cascade skill without specialization: {skill}")

    def test_max_terms_respected(self):
        for seed in range(100):
            c = gen(seed, max_terms=3)
            served = sum(x["terms_served"] for x in c["careers"])
            # natural 12 on reenlistment can force extra terms past the limit
            self.assertLessEqual(served, 3 + sum(1 for x in c["careers"] for t in x["terms"]
                                                 if t.get("reenlistment", {}).get("total") == 12))

    def test_aging_only_from_34(self):
        for seed in range(100):
            c = gen(seed, max_terms=7)
            for career in c["careers"]:
                for t in career["terms"]:
                    if "aging" in t:
                        self.assertGreaterEqual(c["age"], 34)

    def test_death_happens_without_mishap_rule(self):
        deaths = sum(1 for seed in range(400) if not gen(seed)["alive"])
        self.assertGreater(deaths, 0)
        for seed in range(400):
            c = gen(seed)
            if not c["alive"]:
                self.assertIn("survival", c["death_cause"])

    def test_mishap_rule_deaths_are_crises(self):
        for seed in range(400):
            c = gen(seed, survival_mishap=True)
            if not c["alive"]:
                self.assertIn("crisis", c["death_cause"])

    def test_specific_career(self):
        for seed in range(20):
            c = gen(seed, career="navy")
            if c["careers"]:
                self.assertIn(c["careers"][0]["key"],
                              {"navy", "drifter", "aerospace_defense", "marine", "maritime_defense", "scout", "surface_defense"})

    def test_unknown_option_rejected(self):
        with self.assertRaises(ValueError):
            generate_character(seed=1, options={"jedi": True})

    def test_unknown_species_rejected(self):
        with self.assertRaises(ValueError):
            generate_character(seed=1, options={"species": "elf"})

    def test_species_initial_characteristic_rolls(self):
        def initial(seed, species):
            g = Generator(seed=seed, options={"species": species, "homeworld": False})
            g._roll_characteristics()
            return g.chars
        for seed in range(60):
            ch = initial(seed, "avian")
            self.assertTrue(1 <= ch["STR"] <= 6)   # 1D6
            self.assertTrue(1 <= ch["END"] <= 6)   # 1D6
            self.assertTrue(3 <= ch["DEX"] <= 18)  # 3D6
            ch = initial(seed, "insectan")
            self.assertTrue(4 <= ch["DEX"] <= 14)  # 2D6+2
            ch = initial(seed, "reptilian")
            self.assertTrue(3 <= ch["STR"] <= 13)  # 2D6+1
            self.assertTrue(1 <= ch["END"] <= 10)  # 2D6-2, min 1
            ch = initial(seed, "human")
            self.assertTrue(2 <= ch["STR"] <= 12)  # 2D6

    def test_species_mechanics(self):
        for seed in range(40):
            c = gen(seed, species="avian")
            self.assertEqual(c["species"], "Avian")
            self.assertGreaterEqual(c["age"], 22)           # maturity
            self.assertIn("Flyer (9m)", c["traits"])
            self.assertIsNotNone(c["appearance"])
        for seed in range(40):
            c = gen(seed, species="insectan")
            self.assertIn("Caste", c["traits"])
            self.assertTrue(any(k.startswith("Athletics") for k in c["skills"]))
        for seed in range(40):
            c = gen(seed, species="reptilian")
            self.assertGreaterEqual(c["age"], 22)
            self.assertTrue(any(k.startswith("Melee Combat (Natural Weapons)") for k in c["skills"]))
        for seed in range(40):
            c = gen(seed, species="esper")
            self.assertEqual(c["species"], "Esper")
            self.assertIn("Psionic", c["traits"])
            if c["psi"]:
                self.assertIn(f"-{data.pseudohex(c['psi'])}", c["upp"])
        c = gen(1, species="merfolk")
        self.assertIn("Aquatic", c["traits"])
        c = gen(1, species="aviaire")  # alias FR
        self.assertEqual(c["species_key"], "avian")

    def test_major_races_rolls(self):
        def initial(seed, species):
            g = Generator(seed=seed, options={"species": species, "homeworld": False})
            g._roll_characteristics()
            return g
        for seed in range(60):
            g = initial(seed, "aslan")
            self.assertTrue(4 <= g.chars["STR"] <= 14)   # 2D6+2
            self.assertTrue(1 <= g.chars["DEX"] <= 10)   # 2D6-2, min 1
            g = initial(seed, "vargr")
            self.assertTrue(1 <= g.chars["STR"] <= 11)   # 2D6-1
            self.assertTrue(3 <= g.chars["DEX"] <= 13)   # 2D6+1
            self.assertTrue(1 <= g.chars["END"] <= 11)   # 2D6-1
            g = initial(seed, "kkree")
            self.assertTrue(8 <= g.chars["STR"] <= 15)   # 2D6+6, cap 15
            self.assertTrue(4 <= g.chars["INT"] <= 14)   # 2D6+2
            g = initial(seed, "hiver")
            self.assertTrue(1 <= g.chars["STR"] <= 10)   # 2D6-2
            self.assertTrue(4 <= g.chars["EDU"] <= 14)   # 2D6+2
            g = initial(seed, "droyne")
            self.assertIsNotNone(g.caste)
            self.assertIn(g.caste, {"Worker", "Warrior", "Drone", "Technician", "Sport", "Leader"})
            self.assertTrue(2 <= g.chars["STR"] <= 13)   # 1D+1 + caste mods, cap 15
        c = gen(3, species="kkree")
        self.assertEqual(c["species"], "K'kree")
        self.assertIn("homeworld", c)  # homeworld on by default
        c = gen(3, species="hiver")
        self.assertEqual(c["species"], "Hiver")
        c = gen(3, species="k'kree")  # alias with apostrophe
        self.assertEqual(c["species_key"], "kkree")

    def test_species_names(self):
        from cepheus import data as d
        for seed in range(30):
            for key in d.SPECIES:
                c = gen(seed, species=key)
                n = len(c["name"].split())
                self.assertTrue(2 <= n <= 5, f"{key}: {c['name']}")
                if key != "human":
                    # non-human names must not come from the human name lists
                    self.assertNotIn(c["name"].split()[0], d.FIRST_NAMES_M + d.FIRST_NAMES_F)
        # humans keep first+family as the first two parts
        c = gen(11, species="human")
        self.assertIn(c["name"].split()[0], d.FIRST_NAMES_M + d.FIRST_NAMES_F)

    def test_text_sheet(self):
        c = gen(42)
        g = Generator(seed=42)
        g.generate()
        text = g.to_text()
        self.assertIn(c["upp"], text)
        self.assertIn(f"Age {c['age']}", text)
        self.assertIn(c["name"], text)


if __name__ == "__main__":
    unittest.main()
