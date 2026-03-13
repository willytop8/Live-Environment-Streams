# Live Environment Streams

A curated, agent-optimized master repository of live outdoor webcams across the globe. 
(Originally created to make https://www.twitch.tv/alwaysrainsomewhere)

## Usage for Computer Vision
This repository provides immediate access to real-time streams, allowing AI models, agents, and computer vision pipelines to continuously gather environmental data. 

Use cases include:
- Real-time weather detection and tracking
- Day/night cycle analysis
- Urban traffic and pedestrian density estimation
- Coastal condition monitoring (tides, storms)

## Developer Integration
You can seamlessly integrate this database into your application. Below is an example of how to randomly select an active stream and extract its metadata:

```python
import json
import random

with open("streams.geojson", "r") as f:
    data = json.load(f)

# Filter for daytime streams or specific categories (pseudocode)
streams = data["features"]

# Select a random camera
selected = random.choice(streams)
props = selected["properties"]
coords = selected["geometry"]["coordinates"]

print(f"Loading {props['name']} located at {coords}")
print(f"Stream URL: {props['url']}")
```

## Directory Structure
To avoid overwhelming large context windows, the repository maintains both a master list and territorially-segmented data:
- `streams.geojson`: The monolithic collection of all endpoints.
- `data/`: Regional subsets split by Country Code (e.g., `data/US.json`, `data/GB.json`). This structure makes it token-efficient for agents querying specific regions.

<div align="center">
  <!-- GitHub Topics -->
  <code>#dataset</code> <code>#computer-vision</code> <code>#live-weather</code> <code>#machine-learning</code> <code>#webcams</code>
  <code>#hls-streams</code> <code>#rtsp</code> <code>#geojson</code> <code>#osint</code> <code>#environment-monitoring</code>
  <code>#surveillance</code> <code>#smart-cities</code> <code>#weather-api</code> <code>#data-engineering</code> <code>#traffic-cameras</code>
  <code>#streaming-media</code> <code>#python</code> <code>#ai-agents</code> <code>#live-feeds</code> <code>#geospatial</code>
</div>
