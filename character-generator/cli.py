#!/usr/bin/env python3
"""CLI: generate Cepheus Engine characters without the HTTP server.

Examples:
    python3 cli.py --seed 42
    python3 cli.py --count 5 --career marine --text
    python3 cli.py --seed 7 --survival-mishap --homeworld --out pj.json
"""
import argparse
import json
import sys

from cepheus.character import DEFAULT_OPTIONS, Generator, batch_seeds, resolve_career


def main():
    p = argparse.ArgumentParser(description="Generate Cepheus Engine (SRD) characters")
    p.add_argument("--count", type=int, default=1, help="number of characters (1-50)")
    p.add_argument("--seed", type=int, default=None, help="RNG seed (reproducible batch)")
    p.add_argument("--career", default=None, help="first career key or name (default: random)")
    p.add_argument("--max-terms", type=int, default=DEFAULT_OPTIONS["max_terms"])
    p.add_argument("--p-stay", type=float, default=DEFAULT_OPTIONS["p_stay"])
    p.add_argument("--p-new-career", type=float, default=DEFAULT_OPTIONS["p_new_career"])
    p.add_argument("--p-draft", type=float, default=DEFAULT_OPTIONS["p_draft"])
    p.add_argument("--survival-mishap", action="store_true", help="optional rule: mishap instead of death on failed survival")
    p.add_argument("--homeworld", dest="homeworld", action="store_true", default=True,
                   help="monde natal reel via l'API TravellerMap (defaut)")
    p.add_argument("--no-homeworld", dest="homeworld", action="store_false",
                   help="desactiver le monde natal")
    p.add_argument("--sector", default=None, help="sector name/abbreviation for the homeworld (e.g. 'Spinward Marches', 'spin')")
    p.add_argument("--no-background", action="store_true", help="skip background skills")
    p.add_argument("--name", default=None)
    p.add_argument("--gender", choices=["M", "F"], default=None)
    p.add_argument("--text", action="store_true", help="print plain-text sheets instead of JSON")
    p.add_argument("--out", default=None, help="write output to this file instead of stdout")
    args = p.parse_args()

    if args.career is not None and resolve_career(args.career) is None:
        p.error(f"unknown career: {args.career} (see cepheus/data/careers.json)")
    if not 1 <= args.count <= 50:
        p.error("count must be between 1 and 50")

    options = {
        "career": args.career,
        "max_terms": args.max_terms,
        "p_stay": args.p_stay,
        "p_new_career": args.p_new_career,
        "p_draft": args.p_draft,
        "survival_mishap": args.survival_mishap,
        "background_skills": not args.no_background,
        "homeworld": args.homeworld,
        "sector": args.sector,
        "name": args.name,
        "gender": args.gender,
    }
    gens = [Generator(seed=s, options=options) for s in batch_seeds(args.seed, args.count)]
    characters = [g.generate() for g in gens]

    if args.text:
        output = "\n\n".join(g.to_text() for g in gens) + "\n"
    else:
        output = json.dumps({"characters": characters}, ensure_ascii=False, indent=1) + "\n"

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(output)
    else:
        sys.stdout.write(output)


if __name__ == "__main__":
    main()
