# Changelog

## [2.0.0] - 2026-04-29

### Removed
- 62 Caltrans streams (`wzmedia.dot.ca.gov`) — confirmed returning 403, blacklisted in production
- 8 Indonesian toll road streams (5 source families: margaharjaya, waskitabumiwira, wikaserangpanimbang, serbaraja_toll, tangerangkab) — geo-blocked, unreachable from US/EU servers

### Added
- `url_type` field: `hls`, `youtube`, `html_page`, `http_image` — tells agents what kind of URL they're getting
- `coordinates_quality` field: `exact`, `city`, `country_centroid` — flags 1,057 streams with fake fallback coordinates
- `status` field: `active`, `unverified`, `deprecated` — all streams start as `unverified`
- `last_verified` field: ISO 8601 timestamp, null until validation pipeline runs
- `source_url_requires` field: `browser`, `token_refresh`, or null — flags streams needing special handling
- `sources.json`: per-source-family metadata (full name, license type, notes)
- `scripts/validate.py`: probe stream URLs and update status/last_verified
- `scripts/geocode_swc.py`: fix fallback coordinates using Nominatim geocoding
- `scripts/regenerate_country_files.py`: rebuild data/ from streams.geojson
- `scripts/stats.py`: print dataset statistics
- `.github/workflows/validate.yml`: weekly automated validation via GitHub Actions
- `CHANGELOG.md`: this file

### Changed
- `quality_tier` values reset — 2,106 HTML-page streams previously marked "premium" now marked "unknown"
- `display_name` enriched for DOT and autobahn sources (extracted locality from name field)
- README rewritten with data quality section, known limitations, contributing guide
- `llms.txt` rewritten with agent query patterns and data quality caveats
- Stream count: 5,242 → 5,172

## [1.0.0] - 2026-04-28

### Added
- Initial release with 5,242 streams across 80 countries
- GeoJSON schema with name, url, country_code, environment, source_family, quality_tier, scene_type
- Per-country data files in data/
- llms.txt for LLM/agent consumption
