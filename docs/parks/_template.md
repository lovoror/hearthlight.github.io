# <Park full name> — `<CODE>`

> <State(s)> · established <Month D, YYYY> · <area> km² (<acres> acres) · <visits> recreation visits (2025) ·
> <lowest>–<highest> m · NPS region <IMR/PWR/…>
>
> <Two sentences: what this park is, and what walking around it in Hearthlight should feel like.>

| | |
|---|---|
| Bounding box (W, S, E, N) | from the NPS boundary |
| Centre | lat, lon |
| Extent | ~W km east–west × H km north–south |
| Biomes | the 3–6 landscapes a player walks through |
| Climate & best season | … |
| Getting in | entrances, the gateway towns, road / boat / plane only |
| Proposed tier | 1 · 2 · 3 — one line why (see `docs/parks/README.md`) |

## Official visitor maps

- **Park map (Unigrid brochure)**: <URL> — edition/year, what the map side shows (and its insets).
- <Other maps: trail map, shuttle map, district maps, winter map, backcountry map, accessibility…> — <URL> — what each adds.
- Maps page: `https://www.nps.gov/<code>/planyourvisit/maps.htm`

## Reading the map

<Prose, north up, written so that someone who never saw the map could redraw it: the park's shape
and orientation, its districts, the road network (entrances, the main road or loop, where each
road goes, one-way sections, seasonal closures, shuttle-only roads), where the visitor hubs sit,
where the wild or roadless parts are, how water and relief organise everything. 3–6 paragraphs.>

### Districts & areas

| Area | Where (relative position · lat, lon) | Character | What's there |
|---|---|---|---|

### Roads & entrances

| Road / entrance | From → to | Length | Notes (season, one-way, shuttle, unpaved, tunnel…) |
|---|---|---|---|

### Places (with coordinates)

| Place | Kind | Lat, Lon | Elev. m | Why it matters here |
|---|---|---|---|---|

<20–45 rows: visitor centres, viewpoints, summits, lakes, falls, geysers, arches, historic
buildings, lodges, campgrounds, trailheads, the places on the brochure's insets. 4 decimals.
Never give coordinates for closed or fragile places (a gated cave, an archaeological or sacred
site off the public trails, a nest, a protected tree such as Hyperion): write « not given ».>

### Signature trails & routes

| Trail | Length (round trip) | Climb | Starts at | What you see |
|---|---|---|---|---|

### Water

<Rivers (and which way they flow), lakes, coast, falls, springs, tides, ice.>

### Relief

<Lowest and highest points, how the land steps (plateaus, canyon rims, ridges, valleys, dunes,
caves), what to turn into cliffs, banks, stairs and 3D peaks in the game.>

### Sketch

```
<An ASCII sketch, north up, ~70×24 characters: the boundary, roads (= or -), trails (.), water (~),
peaks (^), the hubs (#), the signature places by initials, with a legend below.>
```

## Look & feel

- **Vegetation by elevation**: <bands and signature plants>.
- **Ground, rock & water colours**: <a palette of 6–10 hex colours with what each paints>.
- **Wildlife** (the field guide): <8–15 species — where and when to meet them>.
- **Flora** (the herbarium): <5–10 signature plants and their season>.
- **Weather & seasons**: <what each season looks like; snow, monsoon, fog, fire, ice>.
- **Night**: <dark sky, stars, aurora, bioluminescence, fireflies, bats…>.
- **Sounds**: <what the soundscape is made of>.

## Moments

<The park's signature events, with their real timing — e.g. a geyser's interval, a seasonal
bloom, an animal migration, a sunrise spot, a tide, a firefall, a light show. 4–10 bullets.>

## For the game

- **Scale & shape**: <the proposed game map size in tiles (a tile ≈ 1–2 m at the hero's scale),
  what stays near true scale (the hotspots, with their real size) and what is compressed (the
  connective wilderness), what is cut.>
- **Hubs & set pieces**: <the places players gather; the 3D landmarks to model; the interiors.>
- **Activities**: <hiking, photo spots (list them), wildlife spotting, ranger programmes, junior
  ranger ideas, water (swim, canoe, raft, boat), vehicles (car, shuttle, bike, horse/mule, boat,
  plane, train), winter, caves, climbing.>
- **Passport stamps**: <where the real cancellation stamps are (visitor centres…)>.
- **With friends / with the world**: <co-op moments for a party, gathering spots for the open
  world (where strangers would naturally meet), group photos.>
- **Rules of the park** (Leave No Trace, as gameplay): <keep distance from X, stay on the
  boardwalk, pack out trash, don't feed…>.
- **Implementation challenges**: <what the engine doesn't do yet: caves, geysers, glaciers, tides,
  sea, vertical cliffs, snow…>.

## Sources

- <Every page and map used, as links.>
