# Live Environment Streams

A curated, agent-optimized repository of live outdoor webcam streams across the globe.
Originally created to power [twitch.tv/alwaysrainsomewhere](https://www.twitch.tv/alwaysrainsomewhere).

**5,997 streams · 98 countries · 67 sources · 4,226 verified active · 4,229 directly usable**

## Data quality

Not all streams are equal. The schema includes fields that tell you exactly what you're getting:

| Field | What it tells you |
|-------|-------------------|
| `url_type` | Whether the URL is a direct HLS manifest, a YouTube link, or an HTML page requiring extraction |
| `coordinates_quality` | Whether coordinates are camera-level (`exact`), city-level (`city`), or a capital fallback (`country_centroid`) |
| `status` | `active` = verified working by the production pipeline; `unverified` = not yet probed |
| `last_verified` | When the stream last passed a live probe (ffprobe-based, from the production selector) |
| `resolution` | Probed video resolution where known (e.g. `1920x1080`) |
| `source_url_requires` | Special handling: `browser` for HTML pages, `token_refresh` for expiring auth tokens, or `null` |

Unlike most webcam lists, `active` status here is not a one-time HTTP 200 check — it reflects
continuous validation by a production streaming system that actually plays these feeds 24/7.

**Recommended query for agent pipelines** — get only streams you can use immediately:

```python
usable = [
    f for f in streams
    if f["properties"]["status"] == "active"
    and f["properties"]["url_type"] in ("hls", "youtube")
    and f["properties"]["source_url_requires"] is None
]
# ~2,929 verified streams with direct URLs
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
print(f"Environment: {props['environment']} | Resolution: {props['resolution']}")
print(f"Source: {props['source_family']} | Status: {props['status']}")
```

Filter by environment or quality:

```python
# Verified coastal streams with direct HLS
coastal_hls = [
    f for f in streams
    if f["properties"]["environment"] == "coastal"
    and f["properties"]["url_type"] == "hls"
    and f["properties"]["status"] == "active"
]

# All streams for a specific country
us_streams = [f for f in streams if f["properties"]["country_code"] == "US"]

# HD streams only
hd = [f for f in streams
      if f["properties"]["resolution"]
      and int(f["properties"]["resolution"].split("x")[1]) >= 720]
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
    "resolution": "1280x720",
    "coordinates_quality": "exact",
    "status": "active",
    "last_verified": "2026-06-11T22:14:09+00:00",
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
| `quality_tier` | string | `premium`, `high`, `standard`, or `low` (production scoring tier) |
| `scene_type` | string | Granular scene label (traffic, beach, marina, etc.) |
| `url_type` | string | `hls`, `youtube`, or `html_page` |
| `resolution` | string/null | Probed video resolution (`WxH`), where known |
| `coordinates_quality` | string | `exact`, `city`, or `country_centroid` |
| `status` | string | `active` or `unverified` |
| `last_verified` | string/null | ISO 8601 timestamp of last successful live probe |
| `source_url_requires` | string/null | `browser`, `token_refresh`, or `null` |

### Environment values

| Environment | Count | Description |
|-------------|------:|-------------|
| `traffic` | 3,551 | Road/highway cameras |
| `urban` | 1,375 | City and town views |
| `coastal` | 461 | Beach and coastal |
| `mountain` | 161 | Mountain, ski, and volcano |
| `harbor` | 119 | Ports and harbors |
| `lake` | 89 | Lake views |
| `nature` | 78 | Nature and wildlife |
| `waterway` | 71 | Rivers, canals, waterfalls |
| `landmark` | 54 | Landmarks, temples, squares |
| `marina` | 32 | Marinas |
| `transport` | 6 | Airports and stations |

### URL types

| Type | Count | How to use |
|------|------:|------------|
| `hls` | 3,754 | Pass directly to ffmpeg or yt-dlp |
| `html_page` | 1,768 | Extract the stream URL from the page (most are SkylineWebcams — fetch the page and pull the `m3u8`) |
| `youtube` | 475 | Use yt-dlp to extract the HLS manifest |

### Coordinates quality

| Quality | Count | Accuracy |
|---------|------:|----------|
| `exact` | 2,373 | Camera-level geocoded |
| `city` | 3,614 | City/interchange level (~10 km) |
| `country_centroid` | 10 | Capital fallback — do not use for geo-queries |

## Source breakdown (top 20)

| Source | Streams | Type | Countries |
|--------|--------:|------|-----------|
| skylinewebcams | 1,684 | Scenic/tourism | 65+ |
| vdot | 1,168 | Virginia DOT traffic | US |
| opencctv | 746 | Open CCTV feeds | Multi |
| mdsha | 404 | Maryland SHA traffic | US |
| deldot | 261 | Delaware DOT traffic | US |
| autobahn_nrw | 252 | German Autobahn (NRW) | DE |
| trafficvision | 245 | Traffic aggregator | Multi |
| manual | 224 | Hand-curated feeds | Multi |
| skyline-youtube | 167 | SkylineWebcams via YouTube | Multi |
| itic | 88 | Thailand traffic | TH |
| youtube | 86 | YouTube Live | Multi |
| worldviewstream | 82 | Scenic network | Multi |
| balticlivecam | 64 | Baltic live cams | Multi |
| camguide | 53 | Scenic network | Multi |
| webcamera_pl | 52 | Polish webcams | PL |
| iowa_dot | 50 | Iowa DOT traffic | US |
| atcs-tasikmalaya | 31 | Indonesia traffic | ID |
| beachcam_meo | 31 | Portuguese beaches | PT |
| OpenTrafficCamMap | 31 | Open traffic map | US |
| nysdot | 23 | New York State DOT | US |

Full per-source metadata (all 67 sources, with active counts) in `sources.json`.

## Country coverage (top 24)

| Country | Streams | Country | Streams |
|---------|--------:|---------|--------:|
| US | 2,210 | MT | 59 |
| IT | 828 | GB | 37 |
| TH | 462 | PT | 36 |
| DE | 290 | PH | 33 |
| KR | 241 | TW | 31 |
| ES | 226 | CZ | 28 |
| GR | 164 | HR | 23 |
| ID | 220 | FR | 26 |
| PL | 148 | RO | 26 |
| TR | 147 | KG | 21 |
| JP | 129 | NZ | 13 |
| NO | 74 | IS | 13 |

98 countries total. Recent expansion focused on rain-prone, previously under-covered
regions: Japan (129), New Zealand, Iceland, Norway, Ireland, SE Asia, and the Pacific Northwest.

## Directory structure

```
streams.geojson          # Master file (all 5,997 streams)
sources.json             # Per-source metadata (license, notes, refresh method, active counts)
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

1. **SkylineWebcams pages (~1,750 streams):** Published as page URLs because their direct
   HLS manifests use auth tokens that expire within hours. Fetch the page and extract the
   `m3u8` at play time. Marked `url_type: "html_page"`, `source_url_requires: "token_refresh"`.

2. **YouTube extraction fragility (475 streams):** YouTube Live extraction via yt-dlp
   breaks periodically — keep yt-dlp current. Some streams rotate video IDs when the
   broadcaster restarts; prefer resolving from the channel when a watch URL dies.

3. **City-level coordinates (3,614 streams):** Geocoded to the nearest town rather than
   the exact camera position. Fine for weather lookups (~10 km), not for precise mapping.

4. **`unverified` ≠ dead (1,771 streams):** These simply haven't been probed by the
   production pipeline yet. Dead and rejected streams are excluded from this dataset entirely.

## Contributing

To add a new source:

1. Add streams to `streams.geojson` following the schema above — all fields are required (`resolution` may be `null`).
2. Add source metadata to `sources.json`.
3. Run `python scripts/regenerate_country_files.py` to update `data/`.
4. Run `python scripts/stats.py` to verify counts.
5. Update this README with new totals.

<div align="center">
  <code>#dataset</code> <code>#computer-vision</code> <code>#live-weather</code> <code>#machine-learning</code> <code>#webcams</code>
  <code>#hls-streams</code> <code>#geojson</code> <code>#environment-monitoring</code>
  <code>#traffic-cameras</code> <code>#ai-agents</code> <code>#geospatial</code>
</div>
