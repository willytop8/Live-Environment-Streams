#!/usr/bin/env python3
"""
Extract location names from Skyline Webcams URL paths and geocode them.
Uses the free Nominatim API (OpenStreetMap) — please respect rate limits.
Requires: requests (pip install requests)

Usage:
    python scripts/geocode_swc.py                # Geocode all fallback-coord SWC streams
    python scripts/geocode_swc.py --dry-run      # Show extracted names without geocoding
    python scripts/geocode_swc.py --limit 50     # Process first N entries
"""

import json
import re
import time
import argparse
from pathlib import Path
from urllib.parse import unquote

GEOJSON_PATH = Path(__file__).parent.parent / "streams.geojson"

FALLBACK_COORDS = {
    (12.49, 41.9), (-74.01, 40.71), (-3.7, 40.42), (14.51, 35.9),
    (-79.42, 43.7), (11.1217, 46.0748), (13.4, 52.52), (10.75, 59.91),
    (25.1442, 35.3387), (8.9463, 44.4056)
}

# Map SWC URL country slugs to country names for geocoding context
COUNTRY_MAP = {
    "italia": "Italy", "espana": "Spain", "united-states": "United States",
    "deutschland": "Germany", "france": "France", "grecia": "Greece",
    "brasil": "Brazil", "canada": "Canada", "malta": "Malta",
    "croatia": "Croatia", "mexico": "Mexico", "czech-republic": "Czech Republic",
    "romania": "Romania", "peru": "Peru", "switzerland": "Switzerland",
    "philippines": "Philippines", "thailand": "Thailand", "norway": "Norway",
    "united-kingdom": "United Kingdom", "hungary": "Hungary", "japan": "Japan",
    "portugal": "Portugal", "turkey": "Turkey", "colombia": "Colombia",
    "israel": "Israel", "egypt": "Egypt", "india": "India",
    "australia": "Australia", "new-zealand": "New Zealand",
    "south-africa": "South Africa", "singapore": "Singapore",
    "china": "China", "vietnam": "Vietnam", "argentina": "Argentina",
}


def extract_location_from_url(url: str) -> tuple:
    """Extract country and city from SWC URL path."""
    match = re.search(r'/webcam/([^/]+)/([^/]+)/([^/]+)/([^/]+)\.html', url)
    if not match:
        return None, None, None
    country_slug = match.group(1)
    region = unquote(match.group(2)).replace("-", " ").title()
    city = unquote(match.group(3)).replace("-", " ").title()
    country = COUNTRY_MAP.get(country_slug, country_slug.replace("-", " ").title())
    return country, region, city


def geocode_nominatim(city: str, country: str) -> tuple:
    """Geocode using Nominatim. Returns (lon, lat) or None."""
    import requests
    try:
        resp = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params={"q": f"{city}, {country}", "format": "json", "limit": 1},
            headers={"User-Agent": "LiveEnvironmentStreams/1.0"},
            timeout=10,
        )
        results = resp.json()
        if results:
            return (float(results[0]["lon"]), float(results[0]["lat"]))
    except Exception as e:
        print(f"  Geocoding error for {city}, {country}: {e}")
    return None


def main():
    parser = argparse.ArgumentParser(description="Geocode SWC streams with fallback coords")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--limit", type=int)
    args = parser.parse_args()

    with open(GEOJSON_PATH) as f:
        data = json.load(f)

    targets = [
        f for f in data["features"]
        if f["properties"].get("source_family") == "skylinewebcams"
        and tuple(f["geometry"]["coordinates"]) in FALLBACK_COORDS
    ]

    if args.limit:
        targets = targets[:args.limit]

    print(f"Found {len(targets)} SWC streams with fallback coordinates")

    geocoded = 0
    failed = 0
    cache = {}

    for i, feat in enumerate(targets):
        url = feat["properties"]["url"]
        country, region, city = extract_location_from_url(url)

        if not city:
            failed += 1
            continue

        if args.dry_run:
            print(f"  {feat['properties']['name']} -> {city}, {region}, {country}")
            continue

        cache_key = f"{city},{country}"
        if cache_key in cache:
            coords = cache[cache_key]
        else:
            coords = geocode_nominatim(city, country)
            cache[cache_key] = coords
            time.sleep(1.1)  # Nominatim rate limit: 1 req/sec

        if coords:
            feat["geometry"]["coordinates"] = list(coords)
            feat["properties"]["coordinates_quality"] = "city"
            geocoded += 1
        else:
            failed += 1

        if (i + 1) % 25 == 0:
            print(f"  Progress: {i + 1}/{len(targets)} "
                  f"(geocoded={geocoded}, failed={failed})")

    if not args.dry_run:
        with open(GEOJSON_PATH, "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"\nDone. Geocoded {geocoded}, failed {failed}")
    else:
        if len(targets) > 20:
            print(f"  ... showing first 20 of {len(targets)}")


if __name__ == "__main__":
    main()
