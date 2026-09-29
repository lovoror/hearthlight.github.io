# Sources, data & licences — the parks atlas

Where the dossiers come from, what the future park maps can be built from, and under which terms.
The rule of thumb is simple: **US federal works (NPS, USGS, Census) are in the public domain**. Use
them first. Everything else is credited or used only as research.

## 1. The official visitor maps (what the dossiers read)

- **Each park's maps page**: `https://www.nps.gov/<code>/planyourvisit/maps.htm` (a few parks use
  `brochures.htm`; Sequoia & Kings Canyon share `/seki/`). It links the **Unigrid brochure**: the
  folded black-banded map every visitor gets at the gate, one side a map, the other side the
  park's story. It also links the other maps: trails, shuttles, districts, winter, accessibility.
- **The NPS map catalogue**, « Find a National Park Service Map »
  (<https://www.nps.gov/subjects/gisandmapping/nps-maps.htm>). Harpers Ferry Center's 1,000+
  maps as JPEG, PDF or production files. The old `nps.gov/carto/hfc/carto/media/<CODE>map1.pdf`
  links now redirect there.
- **NPGallery's « HFC Cartography » collection**
  (<https://npgallery.nps.gov/HFC/SearchResults?pagesize=100&collection=HFC+Cartography>): 900+
  standalone park-map PDFs (`GetAsset/<id>`), each with a long text description of its labels.
  It is the way in for the parks whose maps page has no brochure: Biscayne, Virgin Islands,
  New River Gorge…
- **The maps pages' built-in viewer.** Many maps pages embed the NPS map viewer, which serves the
  Harpers Ferry Center brochure map as Zoomify tiles at
  `https://www.nps.gov/maps/hfc/park-maps/<code>/brochure-map/`. The tile sets of every park are
  listed in the public carto.nps.gov table `"nps-hfc".maps`. Stitched at full resolution (~5000 px),
  they give the brochure map even when no PDF is linked (Badlands, Wind Cave, Guadalupe Mountains,
  Theodore Roosevelt…).
- **Terms**: the NPS maps are works of the US government, in the public domain (17 U.S.C. §105).
  We still never reproduce them as images in the game (the game draws everything in code), and
  **never the NPS arrowhead emblem**, which is protected. The maps are read to understand the
  layout, then redrawn in our style.
- **How the dossiers read them.** The PDF is downloaded to a scratch folder, never into the repo.
  The map page is rendered with PyMuPDF / `pdftoppm`: whole at ~100 dpi, then 4–8 crops at
  ~200 dpi. The labels are extracted with their positions (`page.get_text('words')`).

## 2. Data for the maps (what phase 2 builds from)

| Data | Source | Access | Terms |
|---|---|---|---|
| Park boundaries | NPS Land Resources Division — authoritative tracts & boundaries | ArcGIS REST: `services1.arcgis.com/fBc8EJBxQRMcHlei/…/NPS_Land_Resources_Division_Boundary_and_Tract_Data_Service/FeatureServer/2` | public domain |
| Points of interest (visitor centres, trailheads, overlooks, campgrounds, lodges, shuttle stops…) | NPS Public POIs | `mapservices.nps.gov/arcgis/rest/services/NationalDatasets/NPS_Public_POIs_Geographic/FeatureServer/0` | public domain |
| Trails (name, class, use, surface, season) | NPS Public Trails | `…/NationalDatasets/NPS_Public_Trails_Geographic/FeatureServer/0` | public domain |
| Roads (name, class, surface, one-way, route number, season) | NPS Public Roads | `…/NationalDatasets/NPS_Public_Roads_Geographic/FeatureServer/0` | public domain |
| Buildings, parking lots | NPS Public Buildings / ParkingLots | `…/NationalDatasets/NPS_Public_Buildings_Geographic`, `…_ParkingLots_Geographic` | public domain |
| Park facts (description, weather, activities, topics) | NPS API | `https://developer.nps.gov/api/v1/parks` (free key; `DEMO_KEY` allows ~10 calls an hour) | public domain |
| Visitation | NPS Visitor Use Statistics | <https://irma.nps.gov/Stats/> (the dossiers use the 2025 figures as listed on Wikipedia) | public domain |
| Elevation (DEM) | USGS 3D Elevation Program (3DEP), The National Map | 1/3″ (~10 m) and 1″ (~30 m) DEMs; Alaska 5 m IfSAR — <https://apps.nationalmap.gov/downloader/> | public domain |
| Elevation (tiles, quick) | AWS Open Data « Terrain Tiles » | `s3.amazonaws.com/elevation-tiles-prod/` (terrarium PNGs) | mixed sources; credit per its docs |
| Rivers, lakes | USGS National Hydrography Dataset (NHD) | The National Map | public domain |
| Place names | USGS GNIS (Geographic Names Information System) | The National Map / GNIS downloads | public domain |
| State outlines (the road-trip map) | US Census cartographic boundary files | <https://www.census.gov/geographies/mapping-files.html> | public domain |
| Named natural features (peaks with elevations, lakes, falls, arches, glaciers…) | OpenStreetMap, through Overpass | the mirrors listed in `tools/parks/fetch.py` | **ODbL**: credit « © OpenStreetMap contributors »; a shipped database derived from it stays ODbL |
| Areas, dates, summaries | Wikipedia, « List of national parks of the United States » | MediaWiki API | text CC BY-SA: facts only, no copied prose |

## 3. The data pack (`tools/parks/fetch.py`)

```sh
python3 tools/parks/fetch.py                  # everything, all 63 parks (OSM takes a while)
python3 tools/parks/fetch.py pois lines pack --only YELL,ZION
```

It writes into `tools/parks/cache/` (git-ignored):
- `bounds.geojson`: the 63 boundaries, simplified to ~100 m, with their bounding boxes;
- `nps.json` and `wiki.json`;
- per park, `<CODE>/`:
  - `maps.json`: links from the park's maps page;
  - `pois.json`: NPS points of interest, noise types dropped;
  - `lines.geojson`: NPS trails & roads, ~20 m;
  - `osm.json`: OSM named features inside the boundary;
  - `pack.md`: a readable digest of all of it.

Notes:
- **Sequoia & Kings Canyon** are one unit (`SEKI`) in the NPS national datasets. The tool splits
  the points by boundary. SEKI has no trails or roads in those datasets.
- **Overpass**: the public servers are shared and often busy, so the tool asks one park at a time
  and falls back across mirrors. For the huge parks (Alaska, Death Valley…) it skips named lake
  outlines. It never asks OSM for roads or trails: the NPS's own are better and public domain.
- **Order of trust**: when sources disagree, trust the park's current brochure and website first,
  then the NPS datasets, then USGS, then OSM and Wikipedia. The dossiers say which one they used.

## 4. Other useful references

- Harpers Ferry Center, NPS map symbols and patterns (the look of the brochures):
  <https://www.nps.gov/subjects/gisandmapping/map-symbols-patterns-for-nps-maps.htm>.
- **NPMaps** (npmaps.com) and **Wikimedia Commons**: unofficial, well-kept mirrors of the NPS maps
  (public domain), including older editions. They are handy when a park's page no longer links
  its brochure, which was the case for about a dozen parks in 2026.
- **America's National Parks' cancellation list**: the official list of passport stamps and where
  they are kept. The dossiers' « Passport stamps » lines come from it when a park publishes no
  list of its own.
- The parks' « places to go », « things to do », Junior Ranger, passport-stamp and nature pages,
  cited per dossier.

## 5. Naming & trademarks, for the game

- Park names are geographic names: free to use.
- The NPS arrowhead: never. The game has its own ranger badge, drawn in code.
- « Passport To Your National Parks » is a registered trademark (America's National Parks), so the
  game says « Park Passport ». « Junior Ranger » is the NPS's programme, so the game says
  « Young Ranger ».
- The credits say that Hearthlight is not affiliated with or endorsed by the National Park
  Service, and list the data credits (« © OpenStreetMap contributors » if any OSM-derived data
  ships).
- Native names, lands and sacred places are named the way the parks name them. Tribal
  co-management (e.g. the Badlands' South Unit with the Oglala Lakota) is said plainly.
