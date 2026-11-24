#!/bin/bash
set -e
cd "$(dirname "$0")"
python3 map_wb_estate.py
python3 map_wb_deck1.py
python3 map_wb_deck2.py
python3 map_wb_pad.py
python3 tokens_whitebear.py
echo "White Bear: maps + tokens generes."
