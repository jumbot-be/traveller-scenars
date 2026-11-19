import unittest

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
