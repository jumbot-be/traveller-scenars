#!/bin/sh
# HARD VACUUM 01 : PIRATE BAIT - regenere les 23 PNG (stdlib Python uniquement)
set -e
cd "$(dirname "$0")"
python3 map_outpost.py
python3 map_hotcomet.py
python3 map_chiaroscuro.py
python3 map_dragonclaw.py
python3 map_asteroid.py
python3 tokens.py
python3 exterior_views.py
echo "termine : $(ls *.png | wc -l) PNG"
