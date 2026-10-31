#!/bin/sh
# Regenerate every asset, data file and the preview. Run from anywhere: sh tools/build_all.sh
set -e
cd "$(dirname "$0")"
python3 layout.py
for g in make_assets make_ui make_themes make_collection make_events make_seasons make_sweets make_bombs make_bombs_color make_blockers make_ui_kit chrome make_levels make_scenes make_index check_assets; do python3 $g.py; done
