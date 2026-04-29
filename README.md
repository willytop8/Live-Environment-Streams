# Live Environment Streams

A curated, agent-optimized repository of live outdoor webcam streams across the globe.
Originally created to power [twitch.tv/alwaysrainsomewhere](https://www.twitch.tv/alwaysrainsomewhere).

**5,172 streams · 80 countries · 19 sources · 3,027 directly usable**

## Data quality

Not all streams are equal. The schema includes fields that tell you exactly what you're getting:

| Field | What it tells you |
|-------|-------------------|
| `url_type` | Whether the URL is a direct HLS manifest, a YouTube link, or an HTML page requiring browser extraction |
| `coordinates_quality` | Whether coordinates point to the actual camera (`exact`), a nearby city (`city`), or a country capital fallback (`country_centroid`) |
| `status` | Whether the stream has been verified working (`active`), not yet tested (`unverified`), or confirmed dead (`deprecated`) |
| `source_url_requires` | Special handling needed: `browser` for HTML pages, `token_refresh` for expiring auth tokens, or `null` for direct access |

**Recommended query for agent pipelines** — get only streams you can use immediately:

```python
usable = [
    f for f in streams
    if f["properties"]["url_type"] in ("hls", "youtube")
    and f["properties"]["coordinates_quality"] != "country_centroid"
    and f["properties"]["source_url_requires"] is None
]
# Returns ~2,401 streams with direct URLs and accurate coordinates
```

## Usage

```python
import json
import random

with open("streams.geojson", "r") as f:
    data = json.load(f)

streams = data["features"]
selected = random.choice(streams)
props = selected["properties"]
coords = selected["geometry"]["coordinates"]

print(f"Loading {props['name']} at {coords}")
print(f"URL: {props['url']} (type: {props['url_type']})")
print(f"Environment: {props['environment']}")
print(f"Source: {props['source_family']} | Coords: {props['coordinates_quality']}")
```

Filter by environment or quality:

```python
# Coastal streams with direct HLS and real coordinates
coastal_hls = [
    f for f in streams
    if f["properties"]["environment"] == "coastal"
    and f["properties"]["url_type"] == "hls"
    and f["properties"]["coordinates_quality"] == "exact"
]

# All streams for a specific country
us_streams = [f for f in streams if f["properties"]["country_code"] == "US"]
```

## GeoJSON schema

Each `Feature` in `streams.geojson`:

```json
{
  "type": "Feature",
  "geometry": {
    "type": "Point",
    "coordinates": [-77.4875, 38.7749]
  },
  "properties": {
    "name": "I-95 at Route 123",
    "display_name": "Woodbridge",
    "url": "https://example.com/stream.m3u8",
    "country_code": "US",
    "environment": "traffic",
    "source_family": "vdot",
    "quality_tier": "standard",
    "scene_type": "traffic",
    "url_type": "hls",
    "coordinates_quality": "exact",
    "status": "unverified",
    "last_verified": null,
    "source_url_requires": null
  }
}
```

### Property reference

| Property | Type | Description |
|----------|------|-------------|
| `name` | string | Descriptive camera name |
| `display_name` | string | Human-readable location label (city/landmark) |
| `url` | string | Stream URL (HLS manifest, YouTube link, or HTML page) |
| `country_code` | string | ISO 3166-1 alpha-2 country code |
| `environment` | string | Scene category (see table below) |
| `source_family` | string | Data source identifier (see `sources.json`) |
| `quality_tier` | string | `standard`, `unknown`, or `low` |
| `scene_type` | string | Granular scene label (traffic, beach, marina, etc.) |
| `url_type` | string | `hls`, `youtube`, `html_page`, or `http_image` |
| `coordinates_quality` | string | `exact`, `city`, or `country_centroid` |
| `status` | string | `active`, `unverified`, or `deprecated` |
| `last_verified` | string/null | ISO 8601 timestamp of last successful probe |
| `source_url_requires` | string/null | `browser`, `token_refresh`, or `null` |

### Environment values

| Environment | Count | Description |
|-------------|------:|-------------|
| `traffic` | 2,369 | Road/highway cameras |
| `urban` | 1,920 | City and town views |
| `coastal` | 319 | Beach and coastal |
| `mountain` | 168 | Mountain and alpine |
| `marina` | 128 | Marinas and harbors |
| `waterway` | 103 | Rivers and canals |
| `lake` | 86 | Lake views |
| `nature` | 43 | Nature and wildlife |
| `other` | 36 | Webcam, harbor, transport, landmark |

### URL types

| Type | Count | How to use |
|------|------:|------------|
| `hls` | 3,003 | Pass directly to ffmpeg or yt-dlp |
| `html_page` | 2,106 | Requires browser/JS to extract stream URL |
| `http_image` | 39 | HTTP endpoint serving JPEG snapshots |
| `youtube` | 24 | Use yt-dlp to extract HLS manifest |

### Coordinates quality

| Quality | Count | Accuracy |
|---------|------:|----------|
| `exact` | 3,812 | Camera-level geocoded |
| `city` | 303 | City/interchange level (~10km) |
| `country_centroid` | 1,057 | Fallback to capital — do not use for geo-queries |

## Source breakdown

| Source | Streams | Type | Countries |
|--------|--------:|------|-----------|
| skylinewebcams | 2,771 | Scenic/tourism | 65+ |
| vdot | 1,168 | Virginia DOT traffic | US |
| mdsha | 404 | Maryland SHA traffic | US |
| autobahn_nrw | 281 | German Autobahn (NRW) | DE |
| deldot | 261 | Delaware DOT traffic | US |
| nysdot | 91 | New York State DOT | US |
| opencctv | 30 | Open CCTV feeds | Multi |
| ladot | 30 | Los Angeles DOT | US |
| youtube | 24 | YouTube Live | Multi |
| vegvesen | 22 | Norwegian roads | NO |
| ktict | 20 | Korea traffic | KR |
| iticfoundation | 20 | Thailand cameras | TH |
| taiwan_freeway | 18 | Taiwan highways | TW |
| paspro | 12 | Indonesia traffic | ID |
| vdotcameras | 8 | VDOT secondary | US |
| earthcam | 6 | EarthCam network | Multi |
| panama_canal | 4 | Panama Canal views | PA |
| quebec511 | 1 | Quebec traffic | CA |
| brownrice | 1 | Japan | JP |

Full per-source metadata in `sources.json`.

## Country coverage (top 20)

| Country | Streams | Country | Streams |
|---------|--------:|---------|--------:|
| US | 2,255 | GB | 43 |
| IT | 1,055 | FR | 38 |
| DE | 334 | HR | 36 |
| ES | 267 | MX | 36 |
| GR | 237 | CZ | 31 |
| NO | 91 | PE | 24 |
| BR | 78 | TW | 24 |
| CA | 63 | CH | 23 |
| MT | 60 | PH | 23 |
| TH | 53 | RO | 23 |

80 countries total.

## Directory structure

```
streams.geojson          # Master file (all 5,172 streams)
sources.json             # Per-source metadata (license, notes, refresh method)
data/                    # Per-country GeoJSON subsets (e.g. data/US.json)
scripts/
  validate.py            # Probe stream URLs, update status/last_verified
  geocode_swc.py         # Fix fallback coordinates for SWC streams
  regenerate_country_files.py  # Rebuild data/ from streams.geojson
  stats.py               # Print dataset statistics
.github/workflows/
  validate.yml           # Weekly automated validation
```

## Known limitations

1. **Skyline Webcams HTML pages (2,106 streams):** These are HTML page URLs, not direct stream URLs. An agent needs a browser or scraper to extract the actual HLS manifest. Marked with `url_type: "html_page"` and `source_url_requires: "browser"`.

2. **SWC token expiry (665 streams):** The 665 SWC streams with direct `.m3u8` URLs use auth tokens that expire. Marked with `source_url_requires: "token_refresh"`.

3. **Fallback coordinates (1,057 streams):** These streams have coordinates pointing to country capitals (Rome, NYC, Madrid, etc.) instead of actual camera locations. Marked with `coordinates_quality: "country_centroid"`. Run `scripts/geocode_swc.py` to fix.

4. **No live verification yet:** All streams launch as `status: "unverified"`. The GitHub Actions workflow will progressively verify them.

## Contributing

To add a new source:

1. Add streams to `streams.geojson` following the schema above — all new fields are required.
2. Add source metadata to `sources.json`.
3. Run `python scripts/regenerate_country_files.py` to update `data/`.
4. Run `python scripts/stats.py` to verify counts.
5. Update this README with new totals.

<div align="center">
  <code>#dataset</code> <code>#computer-vision</code> <code>#live-weather</code> <code>#machine-learning</code> <code>#webcams</code>
  <code>#hls-streams</code> <code>#geojson</code> <code>#environment-monitoring</code>
  <code>#traffic-cameras</code> <code>#ai-agents</code> <code>#geospatial</code>
</div>
