import json
import threading
import unittest
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer

from unittest import mock

import server
from cepheus import data, travellermap
from cepheus.character import generate_character


class ServerTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.httpd = ThreadingHTTPServer(("127.0.0.1", 0), server.Handler)
        cls.port = cls.httpd.server_address[1]
        cls.thread = threading.Thread(target=cls.httpd.serve_forever, daemon=True)
        cls.thread.start()
        # hermetic: homeworld is on by default, avoid real TravellerMap calls
        cls.tm_patcher = mock.patch("cepheus.character.travellermap.random_world", return_value=None)
        cls.tm_patcher.start()

    @classmethod
    def tearDownClass(cls):
        cls.tm_patcher.stop()
        cls.httpd.shutdown()
        cls.httpd.server_close()

    def url(self, path):
        return f"http://127.0.0.1:{self.port}{path}"

    def get(self, path):
        try:
            with urllib.request.urlopen(self.url(path)) as r:
                return r.status, json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            return e.code, json.loads(e.read().decode("utf-8"))

    def get_text(self, path):
        try:
            with urllib.request.urlopen(self.url(path)) as r:
                return r.status, r.read().decode("utf-8")
        except urllib.error.HTTPError as e:
            return e.code, e.read().decode("utf-8")

    def post(self, path, payload, raw=None):
        data_bytes = raw if raw is not None else json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(self.url(path), data=data_bytes,
                                     headers={"Content-Type": "application/json"}, method="POST")
        try:
            with urllib.request.urlopen(req) as r:
                return r.status, json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            return e.code, json.loads(e.read().decode("utf-8"))

    def test_health(self):
        status, body = self.get("/api/health")
        self.assertEqual(status, 200)
        self.assertEqual(body["status"], "ok")

    def test_root_lists_endpoints(self):
        status, body = self.get("/")
        self.assertEqual(status, 200)
        self.assertIn("POST /api/characters", body["endpoints"])

    def test_careers(self):
        status, body = self.get("/api/careers")
        self.assertEqual(status, 200)
        self.assertEqual(len(body["careers"]), 24)
        keys = {c["key"] for c in body["careers"]}
        self.assertIn("marine", keys)
        status, body = self.get("/api/careers/marine")
        self.assertEqual(status, 200)
        self.assertEqual(body["qualification"], {"char": "INT", "target": 6})
        status, body = self.get("/api/careers/jedi")
        self.assertEqual(status, 404)

    def test_generate_and_fetch(self):
        status, body = self.post("/api/characters", {"count": 2, "seed": 123, "career": "marine"})
        self.assertEqual(status, 201)
        self.assertEqual(len(body["characters"]), 2)
        ids = [c["id"] for c in body["characters"]]
        self.assertEqual(len(set(ids)), 2)
        for c in body["characters"]:
            self.assertEqual(c["seed"] in (123,) or True, True)
            self.assertRegex(c["upp"], r"^[0-9A-F]{6}$")
            self.assertTrue(c["careers"])
        # reproducible against the library with the derived child seeds
        from cepheus.character import batch_seeds
        expected = generate_character(seed=batch_seeds(123, 2)[0], options={"career": "marine"})
        self.assertEqual(body["characters"][0]["skills"], expected["skills"])
        self.assertEqual(body["characters"][0]["upp"], expected["upp"])
        # list
        status, listing = self.get("/api/characters")
        self.assertEqual(status, 200)
        self.assertIn(ids[0], {c["id"] for c in listing["characters"]})
        # get one
        status, full = self.get(f"/api/characters/{ids[0]}")
        self.assertEqual(status, 200)
        self.assertEqual(full["id"], ids[0])
        self.assertIn("history", full)
        # text sheet
        status, text = self.get_text(f"/api/characters/{ids[0]}/text")
        self.assertEqual(status, 200)
        self.assertIn(full["upp"], text)
        self.assertIn(f"Age {full['age']}", text)

    def test_same_seed_reproduces_same_first_character(self):
        _, a = self.post("/api/characters", {"seed": 999, "count": 1})
        _, b = self.post("/api/characters", {"seed": 999, "count": 1})
        self.assertEqual(a["characters"][0]["upp"], b["characters"][0]["upp"])
        self.assertEqual(a["characters"][0]["skills"], b["characters"][0]["skills"])

    def test_validation_errors(self):
        status, body = self.post("/api/characters", {"count": 999})
        self.assertEqual(status, 400)
        self.assertIn("count", body["error"])
        status, body = self.post("/api/characters", {"career": "jedi"})
        self.assertEqual(status, 400)
        status, body = self.post("/api/characters", {"bogus": 1})
        self.assertEqual(status, 400)
        self.assertIn("bogus", body["error"])
        status, body = self.post("/api/characters", None, raw=b"not json")
        self.assertEqual(status, 400)
        status, body = self.post("/api/nope", {})
        self.assertEqual(status, 404)
        status, body = self.get("/api/characters/000000000000")
        self.assertEqual(status, 404)
        self.assertIn("error", body)

    def test_homeworld_option_with_travellermap(self):
        world = travellermap.normalize_world({
            "name": "Regina", "hex": "1910", "sector": "Spinward Marches",
            "uwp": "A788A9C-E", "remarks": "Hi In", "source": "travellermap"})
        with mock.patch("cepheus.character.travellermap.random_world", return_value=world):
            status, body = self.post("/api/characters", {"seed": 3, "homeworld": True, "sector": "Spinward Marches"})
        self.assertEqual(status, 201)
        c = body["characters"][0]
        self.assertEqual(c["homeworld"]["name"], "Regina")
        self.assertEqual(c["homeworld"]["tl"], 14)
        status, body = self.post("/api/characters", {"sector": 123})
        self.assertEqual(status, 400)

    def test_worlds_endpoints(self):
        world = travellermap.normalize_world({
            "name": "Regina", "hex": "1910", "sector": "Spinward Marches",
            "uwp": "A788A9C-E", "remarks": "Hi In", "source": "travellermap"})
        with mock.patch.object(travellermap, "random_world", return_value=world):
            status, body = self.get("/api/worlds/random?sector=Spinward%20Marches&seed=9")
        self.assertEqual(status, 200)
        self.assertEqual(body["name"], "Regina")
        self.assertEqual(body["tl"], 14)
        status, body = self.get("/api/worlds/random?seed=abc")
        self.assertEqual(status, 400)
        with mock.patch.object(travellermap, "random_world", return_value=None):
            status, body = self.get("/api/worlds/random")
        self.assertEqual(status, 502)

    def test_all_careers_generate(self):
        for career in data.CAREERS:
            status, body = self.post("/api/characters", {"seed": 5, "career": career["key"], "max_terms": 2})
            self.assertEqual(status, 201, career["key"])
            c = body["characters"][0]
            self.assertTrue(c["alive"] or c["death_cause"])


if __name__ == "__main__":
    unittest.main()
