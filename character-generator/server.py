#!/usr/bin/env python3
"""Mini HTTP API (Python 3 stdlib only) that generates Cepheus Engine /
Traveller characters on the fly.

Run:
    python3 server.py [--host 127.0.0.1] [--port 8080]

Endpoints (JSON):
    GET  /api/health
    GET  /api/careers
    GET  /api/careers/<key>
    POST /api/characters            body: {"count":1, "seed":null, ...options}
    GET  /api/characters            list of generated characters (summaries)
    GET  /api/characters/<id>       full character sheet (JSON)
    GET  /api/characters/<id>/text  character sheet as plain text

The Discord bot (later) will simply POST /api/characters and read the result.
"""
import argparse
import json
import re
import threading
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from cepheus import __version__, data, travellermap
from cepheus.character import Generator, batch_seeds, resolve_career
from cepheus.dice import Rng

STORE = {}
STORE_LOCK = threading.Lock()

MAX_BODY = 1_000_000
MAX_COUNT = 50

OPTION_RULES = {
    "career": lambda v: isinstance(v, str) and resolve_career(v) is not None,
    "max_terms": lambda v: isinstance(v, int) and not isinstance(v, bool) and 1 <= v <= 12,
    "p_stay": lambda v: isinstance(v, (int, float)) and not isinstance(v, bool) and 0 <= v <= 1,
    "p_new_career": lambda v: isinstance(v, (int, float)) and not isinstance(v, bool) and 0 <= v <= 1,
    "p_draft": lambda v: isinstance(v, (int, float)) and not isinstance(v, bool) and 0 <= v <= 1,
    "survival_mishap": lambda v: isinstance(v, bool),
    "background_skills": lambda v: isinstance(v, bool),
    "homeworld": lambda v: isinstance(v, bool),
    "sector": lambda v: isinstance(v, str) and 1 <= len(v) <= 60,
    "name": lambda v: isinstance(v, str) and 1 <= len(v) <= 60,
    "gender": lambda v: v in ("M", "F"),
}


def validate_request(body):
    """Validate a POST /api/characters body. Returns (payload, error)."""
    if not isinstance(body, dict):
        return None, "body must be a JSON object"
    unknown = set(body) - {"count", "seed", *OPTION_RULES}
    if unknown:
        return None, f"unknown fields: {sorted(unknown)}"
    count = body.get("count", 1)
    if not isinstance(count, int) or isinstance(count, bool) or not 1 <= count <= MAX_COUNT:
        return None, f"count must be an integer between 1 and {MAX_COUNT}"
    seed = body.get("seed")
    if seed is not None and (not isinstance(seed, int) or isinstance(seed, bool)):
        return None, "seed must be an integer or null"
    options = {}
    for key, rule in OPTION_RULES.items():
        if key in body and body[key] is not None:
            if not rule(body[key]):
                return None, f"invalid value for {key!r}: {body[key]!r}"
            options[key] = body[key]
    return {"count": count, "seed": seed, "options": options}, None


def career_summary(career):
    return {
        "key": career["key"],
        "name": career["name"],
        "qualification": career["qualification"],
        "survival": career["survival"],
        "commission": career["commission"],
        "advancement": career["advancement"],
        "reenlistment": career["reenlistment"],
        "ranks": [r["title"] for r in career["ranks"]],
    }


def character_summary(c):
    return {
        "id": c["id"],
        "seed": c["seed"],
        "name": c["name"],
        "upp": c["upp"],
        "age": c["age"],
        "alive": c["alive"],
        "careers": [f"{x['career']} ({x['terms_served']})" for x in c["careers"]],
    }


class Handler(BaseHTTPRequestHandler):
    server_version = f"traveller-character-api/{__version__}"

    def log_message(self, fmt, *args):
        pass

    def _send_json(self, obj, status=200):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_text(self, text, status=200):
        body = text.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _error(self, status, msg):
        self._send_json({"error": msg}, status)

    def _read_json(self):
        length = int(self.headers.get("Content-Length") or 0)
        if length > MAX_BODY:
            return None, "body too large"
        raw = self.rfile.read(length) if length else b""
        if not raw:
            return {}, None
        try:
            return json.loads(raw.decode("utf-8")), None
        except (ValueError, UnicodeDecodeError):
            return None, "body is not valid JSON"

    def do_GET(self):
        path = urlparse(self.path).path.rstrip("/") or "/"
        if path == "/" or path == "/api":
            self._send_json({
                "service": "traveller-character-api",
                "version": __version__,
                "rules": "Cepheus Engine SRD (OGL), 24 careers",
                "endpoints": [
                    "GET /api/health",
                    "GET /api/careers",
                    "GET /api/careers/<key>",
                    "POST /api/characters",
                    "GET /api/characters",
                    "GET /api/characters/<id>",
                    "GET /api/characters/<id>/text",
                    "GET /api/worlds/sectors",
                    "GET /api/worlds/random?sector=<name>&seed=<int>",
                ],
            })
        elif path == "/api/health":
            self._send_json({"status": "ok", "service": "traveller-character-api", "version": __version__})
        elif path == "/api/careers":
            self._send_json({"careers": [career_summary(c) for c in data.CAREERS]})
        elif path.startswith("/api/careers/"):
            key = path[len("/api/careers/"):].lower().replace(" ", "_")
            career = data.CAREER_BY_KEY.get(key)
            if career is None:
                self._error(404, f"unknown career: {key}")
            else:
                self._send_json(career)
        elif path == "/api/worlds/sectors":
            try:
                self._send_json({"sectors": travellermap.list_sectors()})
            except Exception as e:
                self._error(502, f"TravellerMap API unreachable: {e}")
        elif path == "/api/worlds/random":
            q = parse_qs(urlparse(self.path).query)
            sector = q.get("sector", [None])[0]
            seed = q.get("seed", [None])[0]
            try:
                seed = int(seed) if seed is not None else None
            except ValueError:
                self._error(400, "seed must be an integer")
                return
            world = travellermap.random_world(Rng(seed), sector=sector)
            if world is None:
                self._error(502, "TravellerMap API unreachable or no inhabited world found")
            else:
                self._send_json(world)
        elif path == "/api/characters":
            with STORE_LOCK:
                self._send_json({"characters": [character_summary(c["json"]) for c in STORE.values()]})
        elif path.startswith("/api/characters/"):
            rest = path[len("/api/characters/"):]
            m = re.match(r"^([0-9a-f]{12})(?:/text)?$", rest)
            if not m:
                self._error(404, "not found")
                return
            cid = m.group(1)
            with STORE_LOCK:
                char = STORE.get(cid)
            if char is None:
                self._error(404, f"no character with id {cid}")
            elif rest.endswith("/text"):
                self._send_text(char["text"])
            else:
                self._send_json(char["json"])
        else:
            self._error(404, "not found")

    def do_POST(self):
        path = urlparse(self.path).path.rstrip("/")
        if path != "/api/characters":
            self._error(404, "not found")
            return
        body, err = self._read_json()
        if err:
            self._error(400, err)
            return
        payload, err = validate_request(body)
        if err:
            self._error(400, err)
            return
        characters = []
        for seed in batch_seeds(payload["seed"], payload["count"]):
            gen = Generator(seed=seed, options=payload["options"])
            char = gen.generate()
            cid = uuid.uuid4().hex[:12]
            with STORE_LOCK:
                STORE[cid] = {"id": cid, "json": {**char, "id": cid}, "text": gen.to_text()}
            characters.append({**char, "id": cid})
        self._send_json({"characters": characters}, status=201)

    def do_PUT(self):
        self._error(405, "method not allowed")

    def do_DELETE(self):
        self._error(405, "method not allowed")


def main():
    parser = argparse.ArgumentParser(description="Cepheus Engine character API (stdlib only)")
    parser.add_argument("--host", default="127.0.0.1", help="bind host (default 127.0.0.1, loopback only)")
    parser.add_argument("--port", type=int, default=8080)
    args = parser.parse_args()
    server = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"traveller-character-api {__version__} listening on http://{args.host}:{args.port} (Ctrl-C to stop)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
