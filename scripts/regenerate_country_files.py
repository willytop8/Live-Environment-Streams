#!/usr/bin/env python3
"""
Rebuild per-country data/*.json files from streams.geojson.

Usage:
    python scripts/regenerate_country_files.py
"""

import json
import os
import shutil
from collections import defaultdict
from pathlib import Path

GEOJSON_PATH = Path(__file__).parent.parent / "streams.geojson"
DATA_DIR = Path(__file__).parent.parent / "data"


def main():
    with open(GEOJSON_PATH) as f:
        data = json.load(f)

    # Group features by country code
    by_country = defaultdict(list)
    for feat in data["features"]:
        cc = feat["properties"].get("country_code", "XX")
        by_country[cc].append(feat)

    # Clear and rebuild data/
    if DATA_DIR.exists():
        shutil.rmtree(DATA_DIR)
    DATA_DIR.mkdir()

    for cc, features in sorted(by_country.items()):
        country_data = {
            "type": "FeatureCollection",
            "features": features
        }
        outpath = DATA_DIR / f"{cc}.json"
        with open(outpath, "w") as f:
            json.dump(country_data, f, indent=2, ensure_ascii=False)

    print(f"Generated {len(by_country)} country files in data/")
    print(f"Total streams: {len(data['features'])}")

    # Print summary
    for cc, features in sorted(by_country.items(), key=lambda x: -len(x[1]))[:15]:
        print(f"  {cc}: {len(features)} streams")


if __name__ == "__main__":
    main()
