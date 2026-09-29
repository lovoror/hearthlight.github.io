# The parks atlas

The 63 US national parks, read from the maps the parks hand their visitors. They are the base
for **Hearthlight Parks**, the mode where you walk the national parks in the game's style, solo,
with friends or in a shared open world. The design is in
[`docs/plans/parks-v10.md`](../plans/parks-v10.md).

## What's here

- **63 dossiers**, one per park (`<code>.md`, e.g. [`yell.md`](yell.md)), all on the same
  [template](_template.md):
  - **the official maps** (links);
  - **reading the map**: a walk-through precise enough to redraw it, with districts, roads and
    entrances, 25–45 places with coordinates, signature trails, water, relief and an ASCII sketch;
  - **look & feel**: vegetation by elevation, a palette, wildlife, flora, seasons, night, sounds;
  - **moments**: the signature events with their real timing;
  - **for the game**: scale and shape, hubs and set pieces, activities, passport stamps, ideas for
    friends and for the open world, Leave No Trace rules, implementation challenges;
  - **sources**.
- **[`parks.json`](parks.json)**: the same, machine-readable. It has, for each park: code, names,
  states, dates, area, visits, elevations, bounding box, biomes, signature places, moments,
  wildlife, map links, stamps, hubs, vehicles, tier, the proposed map size and challenges.
- **[`SOURCES.md`](SOURCES.md)**: where everything comes from, what phase 2 can build from (NPS
  and USGS public-domain data), and the naming and trademark rules for the game.
- **The tools**:
  - `tools/parks/fetch.py`: each park's data pack, into `tools/parks/cache/` (git-ignored): the
    boundary, the NPS points of interest, trails and roads, the named natural features, and the
    map links.
  - `tools/parks/atlas.py`: rebuilds `parks.json` and the tables below.

## Numbers

<!-- atlas:stats -->
- 63 parks; 212,284 km² in all; 93,892,121 recreation visits in 2025.
- Busiest: Great Smoky Mountains (11,527,939), Zion (4,984,525), Yellowstone (4,762,988). Quietest: Kobuk Valley (7,786), Gates of the Arctic (14,923), Lake Clark (19,778).
- Largest: Wrangell–St. Elias (33,683 km²), Gates of the Arctic (30,448 km²), Denali (19,186 km²). Smallest: Gateway Arch (0.8 km²), Hot Springs (22.5 km²), New River Gorge (28.4 km²).
<!-- /atlas:stats -->

## Tiers

- **Tier 1**: icons with dense, varied visitor places and a strong identity. They are full maps
  (768–1536 tiles a side) and make the first release.
- **Tier 2**: full maps built afterwards, a road-trip leg at a time.
- **Tier 3**: « vignettes », smaller maps around one to three set pieces. These are the remote
  Alaskan wilderness, the tiny or urban parks and the one-note parks.

**The first wave** (tier 1) takes one of each great landscape. The choice weighs fame, how dense
the visitor places are, and what the engine already knows how to draw:

| # | Park | Landscape | Why in the first wave |
|---|---|---|---|
| 1 | [Zion](zion.md) | red-rock canyon, a river to wade | **the pilot**: compact, one shuttle road, famous trails; it tests strong relief and the rim cut-away |
| 2 | [Acadia](acad.md) | Atlantic coast, granite summits | compact and varied; it tests the sea, the tides and a sunrise moment |
| 3 | [Yellowstone](yell.md) | geysers, wildlife valleys | the flagship; Prism Springs already has timed geysers and travertine |
| 4 | [Yosemite](yose.md) | granite walls, great falls | Elderbough already has granite walls, Half Dome and a great fall |
| 5 | [Grand Canyon](grca.md) | the canyon | the world's canyon: a rim village, mules, trails into the depths |
| 6 | [Great Smoky Mountains](grsm.md) | Appalachian forest | the most visited park: coves, cabins, a crest, the fireflies |
| 7 | [Arches](arch.md) | slickrock arches | compact; one parametric arch model gives dozens of landmarks |
| 8 | [Grand Teton](grte.md) | an alpine skyline over lakes | compact, and joined to Yellowstone by road |
| 9 | [Olympic](olym.md) | rain forest and Pacific surf | three worlds around one ring road, with tides |
| 10 | [Hawaiʻi Volcanoes](havo.md) | a live volcano | Emberpeak already has lava; the eruption is a shared moment |

Each dossier's own suggestion stays in `parks.json` (`tier_suggested`). Glacier, the Everglades,
Bryce Canyon, Joshua Tree, Mount Rainier and Sequoia were suggested for tier 1: they open the
second wave.

<!-- atlas:tiers -->
- **Tier 1** (10): [Zion](zion.md), [Acadia](acad.md), [Yellowstone](yell.md), [Yosemite](yose.md), [Grand Canyon](grca.md), [Great Smoky Mountains](grsm.md), [Arches](arch.md), [Grand Teton](grte.md), [Olympic](olym.md), [Hawaiʻi Volcanoes](havo.md)
- **Tier 2** (36): [Badlands](badl.md), [Big Bend](bibe.md), [Bryce Canyon](brca.md), [Canyonlands](cany.md), [Capitol Reef](care.md), [Carlsbad Caverns](cave.md), [Crater Lake](crla.md), [Cuyahoga Valley](cuva.md), [Denali](dena.md), [Death Valley](deva.md), [Everglades](ever.md), [Glacier](glac.md), [Great Sand Dunes](grsa.md), [Guadalupe Mountains](gumo.md), [Haleakalā](hale.md), [Hot Springs](hosp.md), [Indiana Dunes](indu.md), [Isle Royale](isro.md), [Joshua Tree](jotr.md), [Kings Canyon](kica.md), [Lassen Volcanic](lavo.md), [Mammoth Cave](maca.md), [Mesa Verde](meve.md), [Mount Rainier](mora.md), [New River Gorge](neri.md), [North Cascades](noca.md), [Petrified Forest](pefo.md), [Redwood](redw.md), [Rocky Mountain](romo.md), [Sequoia](sequ.md), [Shenandoah](shen.md), [Theodore Roosevelt](thro.md), [Virgin Islands](viis.md), [Voyageurs](voya.md), [Wind Cave](wica.md), [Wrangell–St. Elias](wrst.md)
- **Tier 3** (17): [Biscayne](bisc.md), [Black Canyon](blca.md), [Channel Islands](chis.md), [Congaree](cong.md), [Dry Tortugas](drto.md), [Gates of the Arctic](gaar.md), [Glacier Bay](glba.md), [Great Basin](grba.md), [Gateway Arch](jeff.md), [Katmai](katm.md), [Kenai Fjords](kefj.md), [Kobuk Valley](kova.md), [Lake Clark](lacl.md), [American Samoa](npsa.md), [Pinnacles](pinn.md), [Saguaro](sagu.md), [White Sands](whsa.md)
<!-- /atlas:tiers -->

## The road trip

The parks are grouped in legs of the road trip, the meta map of the mode:

<!-- atlas:trips -->
- **Grand Circle** (9): [Zion](zion.md), [Bryce Canyon](brca.md), [Capitol Reef](care.md), [Canyonlands](cany.md), [Arches](arch.md), [Mesa Verde](meve.md), [Black Canyon](blca.md), [Grand Canyon](grca.md), [Petrified Forest](pefo.md)
- **Desert Southwest** (8): [Joshua Tree](jotr.md), [Death Valley](deva.md), [Saguaro](sagu.md), [Great Basin](grba.md), [White Sands](whsa.md), [Carlsbad Caverns](cave.md), [Guadalupe Mountains](gumo.md), [Big Bend](bibe.md)
- **Rocky Road** (5): [Yellowstone](yell.md), [Grand Teton](grte.md), [Glacier](glac.md), [Rocky Mountain](romo.md), [Great Sand Dunes](grsa.md)
- **Pacific Crest** (11): [Olympic](olym.md), [Mount Rainier](mora.md), [North Cascades](noca.md), [Crater Lake](crla.md), [Lassen Volcanic](lavo.md), [Redwood](redw.md), [Yosemite](yose.md), [Sequoia](sequ.md), [Kings Canyon](kica.md), [Pinnacles](pinn.md), [Channel Islands](chis.md)
- **Alaska Frontier** (8): [Denali](dena.md), [Katmai](katm.md), [Glacier Bay](glba.md), [Kenai Fjords](kefj.md), [Wrangell–St. Elias](wrst.md), [Lake Clark](lacl.md), [Gates of the Arctic](gaar.md), [Kobuk Valley](kova.md)
- **Great Plains** (3): [Badlands](badl.md), [Wind Cave](wica.md), [Theodore Roosevelt](thro.md)
- **Lakes & Rivers** (7): [Voyageurs](voya.md), [Isle Royale](isro.md), [Indiana Dunes](indu.md), [Cuyahoga Valley](cuva.md), [Gateway Arch](jeff.md), [Hot Springs](hosp.md), [Mammoth Cave](maca.md)
- **Appalachians & the East** (5): [Acadia](acad.md), [Shenandoah](shen.md), [Great Smoky Mountains](grsm.md), [New River Gorge](neri.md), [Congaree](cong.md)
- **Islands** (7): [Everglades](ever.md), [Biscayne](bisc.md), [Dry Tortugas](drto.md), [Virgin Islands](viis.md), [Hawaiʻi Volcanoes](havo.md), [Haleakalā](hale.md), [American Samoa](npsa.md)
<!-- /atlas:trips -->

## All the parks

*Generated by `tools/parks/atlas.py`. « Est. » is the year the park became a national park,
per the NPS: the Everglades' 1947 dedication, for instance, where Wikipedia's list gives the 1934
authorisation. « km² » is the national park itself, without its preserve (Denali, Wrangell–St.
Elias, New River Gorge… — their dossiers give both). « Map (tiles) » is the dossier's proposed
game-map size, at a tile of ~1–2 m for the hero, with the hotspots near true scale and the
wilderness compressed.*

<!-- atlas:table -->
| Park | State | Est. | km² | Visits 2025 | Tier | Landscapes | Signature places | Map (tiles) |
|---|---|---|---:|---:|:---:|---|---|---|
| **Grand Circle** — *the Colorado Plateau: canyons, arches, hoodoos, cliff dwellings* | | | | | | | | |
| [Zion](zion.md) `ZION` | UT | 1919 | 596 | 4,984,525 | 1 | river canyon floor, slot canyon, hanging gardens | Zion Canyon Scenic Drive, The Narrows, Angels Landing, Emerald Pools | 1024×1024 |
| [Bryce Canyon](brca.md) `BRCA` | UT | 1928 | 145 | 1,967,367 | 2 | hoodoo amphitheaters (breaks), ponderosa pine plateau & meadows, spruce-fir-aspen high rim with bristlecones | Bryce Amphitheater, Thor's Hammer, Navajo Loop & Wall Street, Queen's Garden | 512×1024 |
| [Capitol Reef](care.md) `CARE` | UT | 1971 | 979 | 1,388,476 | 2 | Fremont River oasis with historic orchards, slickrock domes, cliffs & slot canyons, pinyon-juniper benches | Waterpocket Fold, Fruita orchards (U-pick), Capitol Dome, Hickman Bridge | 512×1024 |
| [Canyonlands](cany.md) `CANY` | UT | 1964 | 1,366 | 796,057 | 2 | mesa-top grassland & pinyon-juniper, White Rim sandstone bench, banded spires, grabens & slickrock | Mesa Arch, Grand View Point, The Confluence, White Rim Road & Shafer Trail | 1024×1024 |
| [Arches](arch.md) `ARCH` | UT | 1971 | 310 | 1,511,740 | 1 | slickrock & sandstone fins, pinyon-juniper on red sand, Salt Valley grassland | Delicate Arch, The Windows & Turret Arch, Balanced Rock, Landscape Arch | 768×1024 |
| [Mesa Verde](meve.md) `MEVE` | CO | 1906 | 212 | 463,130 | 2 | pinyon-juniper mesa tops, Gambel oak & mountain shrub rim, burned forest regrowing | Cliff Palace, Balcony House, Spruce Tree House, Long House & Step House (Wetherill Mesa) | 768×768 |
| [Black Canyon](blca.md) `BLCA` | CO | 1999 | 125 | 250,086 | 3 | pinyon-juniper rims, Gambel oak & serviceberry thickets, sagebrush flats (North Rim) | Painted Wall, Chasm View, The Narrows, South Rim Road overlooks | 512×384 |
| [Grand Canyon](grca.md) `GRCA` | AZ | 1919 | 4,863 | 4,430,653 | 1 | ponderosa pine rim forest, spruce-fir and aspen plateau, pinyon-juniper canyon slopes | Mather Point, Grand Canyon Village and El Tovar, Desert View Watchtower, Bright Angel Trail | 1536×1024 |
| [Petrified Forest](pefo.md) `PEFO` | AZ | 1962 | 896 | 315,951 | 2 | shortgrass prairie, Painted Desert badlands, blue and banded badlands with log fields | Painted Desert rim, Painted Desert Inn, Route 66 and the 1932 Studebaker, Puerco Pueblo | 512×1024 |
| **Desert Southwest** — *deserts, dunes, caves and the Rio Grande* | | | | | | | | |
| [Joshua Tree](jotr.md) `JOTR` | CA | 1994 | 3,218 | 2,932,644 | 2 | Joshua tree woodland, granite boulder piles, pinyon-juniper ridges | Joshua trees, Hidden Valley and Intersection Rock, Skull Rock and Jumbo Rocks, Arch Rock | 1024×768 |
| [Death Valley](deva.md) `DEVA` | CA NV | 1994 | 13,793 | 1,320,134 | 2 | salt pan, sand dunes, creosote bajadas and badlands | Badwater Basin, Zabriskie Point, Mesquite Flat Sand Dunes, Artists Palette | 1024×1536 |
| [Saguaro](sagu.md) `SAGU` | AZ | 1994 | 376 | 847,749 | 3 | Sonoran desert scrub, desert washes, desert grassland | giant saguaro forests, Cactus Forest Loop Drive, Bajada Scenic Loop, Signal Hill petroglyphs | 1024×512 |
| [Great Basin](grba.md) `GRBA` | NV | 1986 | 312 | 161,210 | 3 | sagebrush steppe, pinyon-juniper woodland, aspen and fir creek canyons | Wheeler Peak, Lehman Caves, Wheeler Peak Scenic Drive, bristlecone pine grove | 512×768 |
| [White Sands](whsa.md) `WHSA` | NM | 2019 | 592 | 659,742 | 3 | white gypsum dunes, vegetated interdunes, alkali playas | Dunes Drive and the Heart of the Sands, sledding the gypsum dunes, Alkali Flat Trail, Interdune Boardwalk | 512×384 |
| [Carlsbad Caverns](cave.md) `CAVE` | NM | 1930 | 189 | 410,778 | 2 | Chihuahuan Desert escarpment, limestone canyons, pinyon-juniper reef ridge | the Big Room, the Natural Entrance and its switchbacks, the bat flight at the Natural Entrance, King's Palace | 640×384 |
| [Guadalupe Mountains](gumo.md) `GUMO` | TX | 1972 | 350 | 206,423 | 2 | Chihuahuan Desert salt basin, gypsum dunes, grassy foothills | Guadalupe Peak, the Top of Texas, El Capitan, McKittrick Canyon, the Salt Basin Dunes | 768×544 |
| [Big Bend](bibe.md) `BIBE` | TX | 1944 | 3,242 | 568,104 | 2 | Chihuahuan Desert flats, volcanic badlands, sky-island pine-oak woodland | Chisos Basin and the Window, Santa Elena Canyon, Emory Peak and the South Rim, Boquillas crossing and Boquillas Canyon | 1280×1152 |
| **Rocky Road** — *geysers, peaks, glaciers and the high dunes* | | | | | | | | |
| [Yellowstone](yell.md) `YELL` | WY MT ID | 1872 | 8,983 | 4,762,988 | 1 | geyser basins & travertine terraces, lodgepole pine plateau forest, sagebrush & grass valleys | Old Faithful, Grand Prismatic Spring, Grand Canyon of the Yellowstone & the Lower Falls, Mammoth Hot Springs Terraces | 1536×1536 |
| [Grand Teton](grte.md) `GRTE` | WY | 1929 | 1,255 | 3,800,648 | 1 | alpine peaks & glaciers, subalpine canyons & cirque lakes, glacial piedmont lakes & lodgepole moraines | the Cathedral Group (Grand Teton, Mount Owen, Teewinot), Jenny Lake, Hidden Falls & Inspiration Point, Mount Moran over Oxbow Bend, the Mormon Row barns | 768×1280 |
| [Glacier](glac.md) `GLAC` | MT | 1910 | 4,100 | 3,136,557 | 2 | cedar-hemlock valleys & big lakes, burned lodgepole & wet meadows, subalpine meadows & krummholz | Going-to-the-Sun Road, Logan Pass & Hidden Lake Overlook, Lake McDonald, St. Mary Lake & Wild Goose Island | 1280×1024 |
| [Rocky Mountain](romo.md) `ROMO` | CO | 1915 | 1,076 | 4,171,431 | 2 | montane meadows with ponderosa, aspen & lodgepole, subalpine spruce-fir forest with lake chains, alpine tundra & fellfield | Trail Ridge Road, Alpine Visitor Center, Bear Lake & Dream Lake, Longs Peak & the Diamond | 1024×1024 |
| [Great Sand Dunes](grsa.md) `GRSA` | CO | 2004 | 434 | 432,498 | 2 | dunefield, sand-sheet grassland & shrubland, sabkha salt wetlands | the dunefield (Star Dune & Hidden Dune, ~225 m), High Dune on First Ridge, Medano Creek's surge flow, the Medano Pass Primitive Road | 768×768 |
| **Pacific Crest** — *volcanoes, giant trees, rainforest and the Pacific coast* | | | | | | | | |
| [Olympic](olym.md) `OLYM` | WA | 1938 | 3,734 | 3,584,187 | 1 | wild ocean beaches & sea stacks, temperate rain forest, lowland lakes & old-growth | Hoh Rain Forest (Hall of Mosses), Hurricane Ridge, Lake Crescent, Rialto Beach & Hole-in-the-Wall | 1536×1280 |
| [Mount Rainier](mora.md) `MORA` | WA | 1899 | 957 | 1,635,342 | 2 | old-growth lowland forest, montane fir forest, subalpine wildflower meadows | Mount Rainier (Columbia Crest), Paradise & the Skyline Trail, Sunrise & the Emmons Glacier, Reflection Lakes | 1280×1280 |
| [North Cascades](noca.md) `NOCA` | WA | 1968 | 2,043 | 46,925 | 2 | west-side old-growth forest, turquoise reservoir lakes & the Skagit River, glaciers & granite spires | Diablo Lake Overlook, Ross Lake, North Cascades Highway (SR 20), Cascade Pass | 1280×1152 |
| [Crater Lake](crla.md) `CRLA` | OR | 1902 | 742 | 632,242 | 2 | caldera lake & cliffs, subalpine rim forest, pumice flats & the Pumice Desert | Crater Lake, Wizard Island, Phantom Ship, Rim Drive | 1024×1024 |
| [Lassen Volcanic](lavo.md) `LAVO` | CA | 1916 | 431 | 504,777 | 2 | volcanic peaks and lava domes, hydrothermal basins, red fir and mountain hemlock forest | Lassen Peak, Bumpass Hell, Sulphur Works, Lake Helen | 1024×768 |
| [Redwood](redw.md) `REDW` | CA | 1968 | 562 | 1,202,480 | 2 | old-growth coast redwood forest, rocky Pacific coast with beaches, sea stacks and tidepools, river mouths, estuaries and lagoons | Tall Trees Grove, Fern Canyon, Gold Bluffs Beach, Lady Bird Johnson Grove | 640×1536 |
| [Yosemite](yose.md) `YOSE` | CA | 1890 | 3,083 | 4,278,413 | 1 | glacier-carved granite valley with meadows and black oaks, mixed-conifer forest and giant sequoia groves, subalpine domes, lodgepole pine and lakes | Yosemite Valley, Half Dome, El Capitan, Yosemite Falls | 1280×1536 |
| [Sequoia](sequ.md) `SEQU` | CA | 1890 | 1,635 | 1,378,337 | 2 | giant sequoia groves in mixed-conifer forest, foothill oak woodland and chaparral, glaciated granite valleys | General Sherman Tree, Giant Forest, Moro Rock, Tunnel Log | 1024×1024 |
| [Kings Canyon](kica.md) `KICA` | CA | 1940 | 1,869 | 779,791 | 2 | giant sequoia groves, glacial canyon floor with meadows and black oaks, chaparral canyon walls | General Grant Tree, Grant Grove, Kings Canyon Scenic Byway, Cedar Grove | 1024×768 |
| [Pinnacles](pinn.md) `PINN` | CA | 2013 | 108 | 343,208 | 3 | chaparral hills, volcanic spires and cliffs, talus-cave gorges | High Peaks, Steep & Narrow, Bear Gulch Cave, Balconies Cave | 768×576 |
| [Channel Islands](chis.md) `CHIS` | CA | 1980 | 1,010 | 227,186 | 3 | sea cliffs, arches and sea caves, giant kelp forests and rocky reefs, coastal sage scrub and grassland on marine terraces | East Anacapa, Inspiration Point and Arch Rock, Anacapa Island Light, Scorpion Anchorage and the sea caves, Cavern Point and Potato Harbor | 1280×768 |
| **Alaska Frontier** — *wilderness by bus, boat and bush plane* | | | | | | | | |
| [Denali](dena.md) `DENA` | AK | 1917 | 19,186 | 543,300 | 2 | boreal taiga, alpine tundra, braided glacial rivers | Mount McKinley (Denali), Denali Park Road, Sled dog kennels, Polychrome Pass | 1536×640 |
| [Katmai](katm.md) `KATM` | AK | 1980 | 14,870 | 34,479 | 3 | salmon rivers and glacial lakes in spruce–birch forest, volcanic ash desert, glaciated volcanoes and alpine tundra | Brooks Falls, Brooks Camp, Valley of Ten Thousand Smokes, Novarupta and Mount Katmai | 1024×768 |
| [Glacier Bay](glba.md) `GLBA` | AK | 1980 | 13,045 | 740,044 | 3 | temperate rainforest, post-glacial young land, fjord and island waters | Margerie Glacier, Tarr Inlet and the Grand Pacific Glacier, Bartlett Cove, Xunaa Shuká Hít (Huna Ancestors' House) | 1280×1024 |
| [Kenai Fjords](kefj.md) `KEFJ` | AK | 1980 | 2,710 | 425,369 | 3 | icefield and nunataks, glacier valley and outwash plain, coastal spruce–hemlock rainforest | Exit Glacier, Harding Icefield, Harding Icefield Trail, Holgate Glacier | 1024×1024 |
| [Wrangell–St. Elias](wrst.md) `WRST` | AK | 1980 | 33,683 | 108,840 | 2 | boreal spruce–aspen forest, alpine tundra, glaciers and icefields | Kennecott Mines National Historic Landmark, Root Glacier, McCarthy Road, Mount Wrangell | 1536×1024 |
| [Lake Clark](lacl.md) `LACL` | AK | 1980 | 10,602 | 19,778 | 3 | boreal forest around glacial lakes, tundra lake country, glaciated volcanoes and mountains | Lake Clark (Qizhjeh Vena), Port Alsworth and Tanalian Falls, Richard Proenneke's cabin at Twin Lakes, Redoubt and Iliamna volcanoes | 1024×768 |
| [Gates of the Arctic](gaar.md) `GAAR` | AK | 1980 | 30,448 | 14,923 | 3 | northern boreal forest at the tree line, tussock and alpine tundra, glaciated Brooks Range peaks | Frigid Crags and Boreal Mountain (the Gates), Arrigetch Peaks, Anaktuvuk Pass, North Fork Koyukuk River | 1024×768 |
| [Kobuk Valley](kova.md) `KOVA` | AK | 1980 | 7,085 | 7,786 | 3 | active Arctic sand dunes, northern boreal forest along the river, tussock and alpine tundra | Great Kobuk Sand Dunes, Onion Portage (Paatitaaq), Kobuk River, Little Kobuk Sand Dunes | 1024×768 |
| **Great Plains** — *badlands, prairie and the Little Missouri* | | | | | | | | |
| [Badlands](badl.md) `BADL` | SD | 1978 | 982 | 1,139,361 | 2 | eroded badlands, mixed-grass prairie, juniper draws | the Badlands Wall and Loop Road, the Door, Window and Notch trails, Yellow Mounds and the Pinnacles, Sage Creek bison and Roberts Prairie Dog Town | 1024×384 |
| [Wind Cave](wica.md) `WICA` | SD | 1903 | 138 | 606,258 | 2 | mixed-grass prairie, ponderosa pine forest, limestone canyons | Wind Cave's boxwork and ranger cave tours, the breathing natural entrance, bison on the prairie, Rankin Ridge lookout tower | 512×480 |
| [Theodore Roosevelt](thro.md) `THRO` | ND | 1978 | 285 | 729,893 | 2 | Little Missouri badlands, mixed-grass prairie, cottonwood river bottoms | South Unit Scenic Loop Drive, Maltese Cross Cabin, River Bend and Oxbow overlooks (North Unit), Painted Canyon | 640×512 |
| **Lakes & Rivers** — *the Great Lakes, the Mississippi, springs and caves* | | | | | | | | |
| [Voyageurs](voya.md) `VOYA` | MN | 1975 | 883 | 206,326 | 2 | big boreal lakes & islands, granite knobs with jack and red pine, boreal mixed forest | Kabetogama Peninsula, Kettle Falls Hotel & dams, Ellsworth Rock Gardens, houseboating on the border lakes | 1280×896 |
| [Isle Royale](isro.md) `ISRO` | MI | 1940 | 2,314 | 29,091 | 2 | boreal spruce-fir coast, northern hardwood ridges, open basalt ridge tops | Greenstone Ridge Trail, Rock Harbor, Windigo & Washington Creek moose, Rock Harbor Lighthouse & Edisen Fishery | 1280×832 |
| [Indiana Dunes](indu.md) `INDU` | IN | 2019 | 66 | 2,629,497 | 2 | Lake Michigan beach & foredunes, high dunes & blowouts, black oak savanna | West Beach & the Dune Succession Trail, Mount Baldy moving dune, 3 Dune Challenge (Mount Tom), Cowles Bog | 1280×576 |
| [Cuyahoga Valley](cuva.md) `CUVA` | OH | 2000 | 132 | 3,025,325 | 2 | river floodplain & canal, mixed hardwood forest, hemlock ravines & waterfalls | Ohio & Erie Canal Towpath Trail, Cuyahoga Valley Scenic Railroad, Brandywine Falls, The Ledges | 512×1152 |
| [Gateway Arch](jeff.md) `JEFF` | MO IL | 2018 | 1 | 2,209,028 | 3 | designed urban park (lawns, plane-tree allées, ponds), native meadow & pollinator garden, Mississippi River & levee | Gateway Arch (630 ft), Tram ride to the top, Museum at the Gateway Arch (underground), Old Courthouse & the Dred Scott case | 512×768 |
| [Hot Springs](hosp.md) `HOSP` | AR | 1921 | 22 | 2,494,611 | 2 | historic spa town (Bathhouse Row), oak-hickory-shortleaf pine ridges, novaculite outcrops and glades | Bathhouse Row, Fordyce Bathhouse Visitor Center, Grand Promenade, Hot Water Cascade & Display Springs | 768×576 |
| [Mammoth Cave](maca.md) `MACA` | KY | 1941 | 292 | 660,734 | 2 | deep cave passages & domes, oak-hickory and mixed forest on karst ridges, Green River valley with bluffs and islands | Historic Entrance & the Rotunda, Frozen Niagara, Mammoth Dome & Fat Man's Misery, Grand Avenue & the Snowball Room | 1024×768 |
| **Appalachians & the East** — *old mountains, the Atlantic coast and a floodplain forest* | | | | | | | | |
| [Acadia](acad.md) `ACAD` | ME | 1919 | 199 | 4,079,318 | 1 | granite summits and ledges, rocky coast and tide pools, spruce-fir and birch-aspen forest | Cadillac Mountain sunrise, Park Loop Road & Ocean Drive, Jordan Pond House popovers, Carriage roads and their stone bridges | 1536×1024 |
| [Shenandoah](shen.md) `SHEN` | VA | 1935 | 811 | 1,682,152 | 2 | oak-hickory ridge forest, waterfall hollows, mountain meadow | Skyline Drive and its overlooks, Big Meadows, Old Rag scramble, Skyland & Stony Man | 1024×2048 |
| [Great Smoky Mountains](grsm.md) `GRSM` | TN NC | 1934 | 2,114 | 11,527,939 | 1 | cove hardwood forest, spruce-fir crest, grassy and heath balds | Cades Cove, Kuwohi (Clingmans Dome) tower, Newfound Gap Road, Mount Le Conte & LeConte Lodge | 2048×1024 |
| [New River Gorge](neri.md) `NERI` | WV | 2020 | 28 | 1,958,440 | 2 | whitewater river, mixed-hardwood gorge slopes, sandstone cliffs and rims | New River Gorge Bridge, Bridge Day, Lower Gorge whitewater, Endless Wall climbing | 1024×2048 |
| [Congaree](cong.md) `CONG` | SC | 2003 | 108 | 287,833 | 3 | old-growth bottomland hardwood forest, cypress-tupelo sloughs and oxbow lakes, blackwater creek | Boardwalk Loop, Cedar Creek Canoe Trail, Champion trees, Synchronous fireflies | 1024×512 |
| **Islands** — *the Florida keys, the Caribbean and the Pacific islands* | | | | | | | | |
| [Everglades](ever.md) `EVER` | FL | 1947 | 6,106 | 778,198 | 2 | sawgrass marsh & sloughs (River of Grass), pine rockland, tropical hardwood hammock | Anhinga Trail, Shark Valley tram road & observation tower, Pa-hay-okee Overlook, Flamingo on Florida Bay | 1536×1280 |
| [Biscayne](bisc.md) `BISC` | FL | 1980 | 700 | 486,567 | 3 | mangrove shoreline, shallow seagrass bay, northern Florida Keys hardwood hammock | Boca Chita Key lighthouse, Stiltsville, Maritime Heritage Trail shipwrecks, Elliott Key | 768×1152 |
| [Dry Tortugas](drto.md) `DRTO` | FL | 1992 | 262 | 89,355 | 3 | coral reef & seagrass basin, open Gulf channels, sand & coral-rubble keys | Fort Jefferson, Garden Key moat wall snorkel, Bush Key sooty tern colony, Loggerhead Key lighthouse | 896×640 |
| [Virgin Islands](viis.md) `VIIS` | VI | 1956 | 61 | 471,074 | 2 | coral reefs & seagrass bays, white-sand beaches & salt ponds, moist tropical forest | Trunk Bay Underwater Trail, Annaberg sugar mill ruins, Reef Bay Trail & Taíno petroglyphs, Cinnamon Bay | 1280×896 |
| [Hawaiʻi Volcanoes](havo.md) `HAVO` | HI | 1916 | 1,395 | 1,877,854 | 1 | active caldera, craters & steam vents, fresh lava fields & lava tubes, ʻōhiʻa–tree-fern rain forest & kīpuka | Kaluapele & Halemaʻumaʻu (Kīlauea summit), Kīlauea Iki, Nāhuku lava tube, Chain of Craters Road | 1280×1024 |
| [Haleakalā](hale.md) `HALE` | HI | 1961 | 136 | 853,711 | 2 | alpine cinder desert & summit, the crater's cinder cones, subalpine shrubland | Sunrise at Puʻuʻulaʻula summit, Haleakalā Crater, Keoneheʻeheʻe (Sliding Sands) Trail, ʻāhinahina (silversword) | 1024×768 |
| [American Samoa](npsa.md) `NPSA` | AS | 1988 | 33 | 43,258 | 3 | tropical rain forest & cloud forest, coastal littoral forest & sea cliffs, white coral-sand beaches | Pola Island & Vatia, Mount ʻAlava, Ofu Beach & lagoon, Taʻū's Lata Mountain & sea cliffs | 768×640 |
<!-- /atlas:table -->
