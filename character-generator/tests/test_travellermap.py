import json
import os
import tempfile
import unittest
import urllib.error
from unittest import mock

from cepheus import travellermap
from cepheus.character import generate_character
from cepheus.dice import Rng

FAKE_UNIVERSE = {"Sectors": [
    {"X": 0, "Y": 0, "Milieu": "M1105", "Abbreviation": "Spin",
     "Tags": "Official OTU", "Names": [{"Text": "Spinward Marches"}]},
]}

FAKE_SEC_TSV = (
    "Sector\tSS\tHex\tName\tUWP\tBases\tRemarks\tZone\tPBG\tAllegiance\tStars\t{Ix}\t(Ex)\t[Cx]\tNobility\tW\tRU\r\n"
    "Spin\tC\t1910\tRegina\tA788A9C-E\tNS\tHi In\t\t567\tImDd\tG5 V\t{ 5 }\t(B7C+5)\t[0000]\tB\t13\t4620\r\n"
    "Spin\tC\t1911\tEmpty Rock\tB000000-0\t\tBa\t\t000\tIm\tK0 V\t{ 0 }\t(000+0)\t[0000]\t\t0\t0\r\n"
    "Spin\tC\t2001\tLowtech\tD893614-5\t\tNi Lt\t\t312\tImDd\tG0 V\t{ -3 }\t(851-5)\t[4333]\tB\t14\t-200\r\n"
)


def fake_fetch(url, timeout=20):
    if "/universe" in url:
        return json.dumps(FAKE_UNIVERSE).encode()
    if "/sec" in url:
        return json.dumps(FAKE_SEC_TSV).encode()
    raise AssertionError(f"unexpected url {url}")


class TestUwpParsing(unittest.TestCase):
    def test_parse_uwp(self):
        u = travellermap.parse_uwp("A646930-D")
        self.assertEqual(u["starport"], "A")
        self.assertEqual(u["size"], 6)
        self.assertEqual(u["atmosphere"], 4)
        self.assertEqual(u["hydrosphere"], 6)
        self.assertEqual(u["population"], 9)
        self.assertEqual(u["government"], 3)
        self.assertEqual(u["law"], 0)
        self.assertEqual(u["tl"], 13)

    def test_trade_codes_tl_matters(self):
        efate = travellermap.parse_uwp("A646930-D")  # TL 13
        self.assertEqual(set(travellermap.trade_codes_from_uwp(efate)),
                         {"High Population", "Industrial", "High Technology"})
        lowtech = travellermap.parse_uwp("D893614-5")  # TL 5
        codes = set(travellermap.trade_codes_from_uwp(lowtech))
        self.assertIn("Low Technology", codes)
        self.assertNotIn("High Technology", codes)
        self.assertIn("Non-Industrial", codes)

    def test_law_descriptor(self):
        self.assertEqual(travellermap.law_descriptor(0), "No Law")
        self.assertEqual(travellermap.law_descriptor(3), "Low Law")
        self.assertEqual(travellermap.law_descriptor(6), "Medium Law")
        self.assertEqual(travellermap.law_descriptor(12), "High Law")

    def test_remarks_extraction(self):
        codes = travellermap.trade_codes_from_remarks("Hi In An Ht Di(Daccamites)")
        self.assertIn("High Population", codes)
        self.assertIn("Industrial", codes)
        self.assertIn("High Technology", codes)
        self.assertNotIn("Ancient", codes)


class TestRandomWorld(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.env = mock.patch.dict(os.environ, {"TRAVELLERMAP_CACHE": self.tmp.name})
        self.env.start()

    def tearDown(self):
        self.env.stop()
        self.tmp.cleanup()

    def test_random_world_from_api(self):
        with mock.patch.object(travellermap, "_fetch", side_effect=fake_fetch):
            w = travellermap.random_world(Rng(1), sector="Spinward Marches")
        self.assertIsNotNone(w)
        self.assertEqual(w["source"], "travellermap")
        self.assertIn(w["name"], {"Regina", "Lowtech"})  # Empty Rock (pop 0) excluded
        self.assertIsNotNone(w["tl"])
        self.assertIn("tl", w)
        self.assertTrue(w["trade_codes"])
        self.assertTrue(w["url"].startswith("https://travellermap.com/"))

    def test_random_world_deterministic_with_seed(self):
        with mock.patch.object(travellermap, "_fetch", side_effect=fake_fetch):
            a = travellermap.random_world(Rng(7))
            b = travellermap.random_world(Rng(7))
        self.assertEqual(a["name"], b["name"])

    def test_random_world_offline_returns_none(self):
        def boom(url, timeout=20):
            raise urllib.error.URLError("no network")
        with mock.patch.object(travellermap, "_fetch", side_effect=boom):
            self.assertIsNone(travellermap.random_world(Rng(1)))

    def test_unknown_sector(self):
        with mock.patch.object(travellermap, "_fetch", side_effect=fake_fetch):
            self.assertIsNone(travellermap.random_world(Rng(1), sector="No Such Sector"))


class TestHomeworldIntegration(unittest.TestCase):
    def test_homeworld_real_world_with_tl(self):
        world = travellermap.normalize_world({
            "name": "Regina", "hex": "1910", "sector": "Spinward Marches", "subsector": "C",
            "uwp": "A788A9C-E", "remarks": "Hi In", "source": "travellermap",
        })
        with mock.patch("cepheus.character.travellermap.random_world", return_value=world):
            c = generate_character(seed=5, options={"homeworld": True})
        hw = c["homeworld"]
        self.assertEqual(hw["name"], "Regina")
        self.assertEqual(hw["tl"], 14)
        self.assertEqual(hw["source"], "travellermap")
        self.assertIn("High Technology", hw["trade_codes"])  # TL 14 -> Ht
        self.assertTrue(any("Homeworld skills from Regina" in h for h in c["history"]))
        # first two background skills come from the homeworld (law level + trade code)
        bases = [b.split(" (")[0] for b in c["background_skills"][:2]]
        self.assertIn(bases[0], {"Gun Combat", "Melee Combat"})  # law 12 -> High Law -> Melee Combat
        self.assertIn(bases[1], {"Computer", "Streetwise", "Broker"})  # Ht/Hi/In trade codes

    def test_homeworld_fallback_synthetic(self):
        with mock.patch("cepheus.character.travellermap.random_world", return_value=None):
            c = generate_character(seed=5, options={"homeworld": True})
        self.assertEqual(c["homeworld"]["source"], "synthetic")
        self.assertIsNotNone(c["homeworld"]["tl"])
        self.assertTrue(any("TravellerMap" in h for h in c["history"]))

    def test_no_homeworld_by_default(self):
        c = generate_character(seed=5)
        self.assertIsNone(c["homeworld"])

    def test_trade_code_details_in_sheet(self):
        from cepheus.character import Generator
        world = travellermap.normalize_world({
            "name": "Spirelle", "hex": "1927", "sector": "Spinward Marches",
            "uwp": "C766846-8", "remarks": "Ga Ri", "source": "travellermap"})
        self.assertIn("Garden", world["trade_codes"])
        self.assertIn("Rich", world["trade_codes"])
        details = {d["name"]: d for d in world["trade_code_details"]}
        self.assertEqual(details["Garden"]["code"], "Ga")
        self.assertIn("terrestre", details["Garden"]["description"])
        self.assertEqual(details["Rich"]["condition"], "atmo 6 ou 8, pop 6-8")
        with mock.patch("cepheus.character.travellermap.random_world", return_value=world):
            g = Generator(seed=5, options={"homeworld": True})
            c = g.generate()
        self.assertEqual(c["homeworld"]["trade_code_details"][0]["name"], c["homeworld"]["trade_codes"][0])
        text = g.to_text()
        self.assertIn("Spirelle", text)
        self.assertIn("C766846-8", text)
        self.assertIn("Ga Garden - ", text)
        self.assertIn("Codes commerciaux:", text)


if __name__ == "__main__":
    unittest.main()
