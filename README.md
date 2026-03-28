# Live Environment Streams

A curated, agent-optimized master repository of live outdoor webcams across the globe.
(Originally created to power https://www.twitch.tv/alwaysrainsomewhere)

**5,242 streams · 80 countries · 25 sources**

## Usage for Computer Vision

This repository provides immediate access to real-time streams, allowing AI models, agents, and computer vision pipelines to continuously gather environmental data.

Use cases include:
- Real-time weather detection and tracking
- Day/night cycle analysis
- Urban traffic and pedestrian density estimation
- Coastal condition monitoring (tides, storms)

## Developer Integration

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
print(f"Display name: {props['display_name']}")
print(f"URL: {props['url']}")
print(f"Environment: {props['environment']}")
print(f"Source: {props['source_family']} | Quality: {props['quality_tier']} | Scene: {props['scene_type']}")
```

Filter by environment or quality tier:

```python
# Coastal premium streams only
coastal = [
    f for f in streams
    if f["properties"]["environment"] == "coastal"
    and f["properties"]["quality_tier"] == "premium"
]

# All streams for a specific country
us_streams = [f for f in streams if f["properties"]["country_code"] == "US"]
```

## GeoJSON Schema

Each `Feature` in `streams.geojson` has the following structure:

```json
{
  "type": "Feature",
  "geometry": {
    "type": "Point",
    "coordinates": [longitude, latitude]
  },
  "properties": {
    "name": "Camera descriptive name",
    "display_name": "Human-readable label (city/location name)",
    "url": "Direct stream URL (.m3u8, YouTube, etc.)",
    "country_code": "ISO 3166-1 alpha-2 (e.g. US, DE, JP)",
    "environment": "Scene category (see table below)",
    "source_family": "Data source identifier (e.g. skylinewebcams, vdot)",
    "quality_tier": "premium | high | standard | low",
    "scene_type": "Granular scene label (e.g. traffic, beach, marina)"
  }
}
```

### Environment Values

| Environment | Description | Count |
|-------------|-------------|------:|
| `traffic` | Road/highway traffic cameras | 2,439 |
| `urban` | City and town cameras | 1,920 |
| `coastal` | Beach and coastal views | 319 |
| `mountain` | Mountain and alpine scenes | 168 |
| `marina` | Marinas and harbors | 128 |
| `waterway` | Rivers and canals | 103 |
| `lake` | Lake views | 86 |
| `nature` | Nature, wildlife, volcanic | 43 |
| `other` | Uncategorized | 36 |

### Quality Tiers

| Tier | Count | Notes |
|------|------:|-------|
| `premium` | 2,805 | HD/4K, reliable uptime |
| `standard` | 976 | SD, generally stable |
| `high` | 79 | High-definition |
| `low` | 1,382 | Lower resolution or less reliable |

## Source Breakdown

| Source Family | Streams | Type |
|---------------|--------:|------|
| skylinewebcams | 2,771 | Scenic/tourism webcams |
| vdot | 1,168 | Virginia DOT traffic |
| mdsha | 404 | Maryland SHA traffic |
| autobahn_nrw | 281 | German Autobahn (NRW) |
| deldot | 261 | Delaware DOT traffic |
| nysdot | 91 | New York State DOT |
| caltrans | 62 | California DOT traffic |
| opencctv | 30 | Open CCTV feeds |
| ladot | 30 | Los Angeles DOT |
| youtube | 24 | YouTube Live streams |
| vegvesen | 22 | Norwegian road authority |
| ktict | 20 | Korea traffic cameras |
| iticfoundation | 20 | ITIC Foundation |
| taiwan_freeway | 18 | Taiwan freeway cameras |
| paspro | 12 | PasPro traffic |
| vdotcameras | 8 | VDOT secondary feeds |
| earthcam | 6 | EarthCam network |
| panama_canal | 4 | Panama Canal views |
| others | 30 | Various regional sources |

## Country Coverage (Top 20)

| Country | Streams | Country | Streams |
|---------|--------:|---------|--------:|
| US | 2,317 | GB | 43 |
| IT | 1,055 | FR | 38 |
| DE | 334 | HR | 36 |
| ES | 267 | MX | 36 |
| GR | 237 | CZ | 31 |
| NO | 91 | PE | 24 |
| BR | 78 | TW | 24 |
| CA | 63 | CH | 23 |
| MT | 60 | PH | 23 |
| TH | 53 | RO | 23 |

80 countries total. Full per-country files available in `data/`.

## Directory Structure

- `streams.geojson` — monolithic master file (all 5,242 streams)
- `data/` — per-country subsets (e.g. `data/US.json`, `data/DE.json`) for token-efficient agent queries

<div align="center">
  <code>#dataset</code> <code>#computer-vision</code> <code>#live-weather</code> <code>#machine-learning</code> <code>#webcams</code>
  <code>#hls-streams</code> <code>#rtsp</code> <code>#geojson</code> <code>#osint</code> <code>#environment-monitoring</code>
  <code>#surveillance</code> <code>#smart-cities</code> <code>#weather-api</code> <code>#data-engineering</code> <code>#traffic-cameras</code>
  <code>#streaming-media</code> <code>#python</code> <code>#ai-agents</code> <code>#live-feeds</code> <code>#geospatial</code>
</div>
