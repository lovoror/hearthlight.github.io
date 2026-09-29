# Parks v10 « National Park » — walking the US national parks

The brief (2026-09-29), in the user's words:

> Mon idée, en gardant le moteur / multi etc., avoir un autre mode dont le but serait de se
> balader dans les parcs nationaux USA. Pour démarrer : lister tous les parcs US et leurs cartes
> détaillées en te basant sur les cartes qu'ils proposent aux visiteurs — dans un second temps on
> recréera tout ça dans le style du jeu.
>
> Pour ce mode, j'aimerais donner la possibilité d'y jouer en solo/multi ou dans un monde
> « ouvert » où tous les gens connectés se voient (ce serait le mode par défaut), en mode MMO cute,
> avec un système robuste si possible. On en profitera pour rajouter la possibilité d'envoyer du
> texte qui apparaît comme une bulle du personnage qui parle, depuis le téléphone ou l'interface
> (ordi).

The decisions, later that day:

> Pour le nom du mode, ça peut être juste « National Park ». J'imagine bien une carte du monde un
> peu comme dans Mario, qui montre les USA, avec les parcs en grands points d'intérêt dans lesquels
> on pourrait spawn (ils ne sont pas collés les uns aux autres) ; à l'entrée/sortie de chaque parc,
> ou depuis l'intérieur d'un parc, on pourrait en choisir un autre. OK pour démarrer par Zion.
>
> L'idée de ce mode serait plus chill que l'autre : pas d'histoire, juste se balader avec ses amis,
> découvrir des choses — on se concentre sur l'expérience. Un van pour se déplacer sur les routes,
> les animaux emblématiques du parc, des activités réelles : un peu un walking simulator. Bien sûr,
> cacher des easter eggs pour avoir des « découvertes » ; on essaiera d'ajouter des choses à faire
> au-delà pour que ce soit fun.
>
> Les parcs devront être vraiment réalistes : quelqu'un qui a vu les parcs doit pouvoir reconnaître
> les routes, les chemins, les endroits phares. De vraies photos des lieux importants pourraient
> aider.
>
> Prépare un prompt pour un autre agent : une première version jouable — tout le moteur du monde
> partagé + un premier parc, pas en ligne pour l'instant, avec le système de notes qui fait
> reprendre jusqu'à un état satisfaisant pour un premier parc « complet », et la messagerie.

**Status: P0 — the preliminary documentation, done (2026-09-29).** Nothing is built yet. P0 is
made of:
- this plan;
- the atlas in [`docs/parks/`](../parks/README.md):
  - **63 park dossiers** (~14,000 lines), each read from the park's official visitor maps;
  - 25–45 places with coordinates per full park;
  - the moments, the wildlife and ideas for the game;
- the machine-readable catalogue `docs/parks/parks.json`;
- the sources and licences in `docs/parks/SOURCES.md`;
- the tools `tools/parks/fetch.py` (each park's data pack) and `tools/parks/atlas.py` (the atlas's
  tables and a check of every dossier against the template).

Ten researcher agents wrote the dossiers in parallel, one per region. What they found in common is
§7.7.

**Next: the first playable version**, local only and unpublished: the messaging, the park engine,
**Zion** complete, the shared-world engine on `localhost`, and the US world map. The building
agent's brief is [`parks-v10-brief.md`](parks-v10-brief.md); its bar is the rubric of §10.1.

Phase 2 builds from here: turning each park into a game map, in the order of §10.

## 0. Publication rules (the user, 2026-09-29: « bien faire attention, et tout le temps »)

1. **The repository is public, so every push is checked first.** Nothing goes in that isn't
   safe:
   - no secrets, keys or tokens;
   - no private infrastructure details: server addresses beyond what `config.js` and the
     workflows already publish, SSH, dashboards, credentials;
   - no personal data or local paths;
   - no copied text or images from brochures or third parties. Facts, names and links only; the
     dossiers paraphrase.
   - no precise location of a closed or fragile place: a gated cave, an archaeological or sacred
     site off the public trails, a nest, a protected tree. The dossiers write « not given ».
   - no data under a licence that forbids it (`docs/parks/SOURCES.md`).

   Before each commit, search the files being added for personal traces:
   - the user's real name or e-mail address;
   - home and local paths (`/Users/`, `/private/tmp`, scratch folders);
   - the VPS's IP address, and any e-mail or IP address;
   - the words key, token and secret.

   Stage only the files you meant to add.
2. **The National Park mode is not released.** Nothing of it is reachable in any playable version (the
   Pages site, the desktop app, the VPS test copy, a demo) until the user decides otherwise.
   - While it is being built, it sits behind a local-only development flag: `?parks=1`, honoured
     only with `?debug=1` on `localhost`.
   - It stays off the title screen, out of release notes, trailers and social posts.
   - The Pages workflow and the desktop copy leave `src/parks/` out.
   - `server/world.mjs` is not deployed.
   - The public part is only this plan and the atlas in `docs/parks/`, which the Pages site does
     not publish anyway: it ships only `index.html`, `pad.html`, `play.html`, `src/` and
     `vendor/`.

---

## 1. The idea (decided)

**« National Park »** is the mode's name, kept as it is in every language. It is a third mode next
to the story and the Party Mode: **stroll through the 63 US national parks, rebuilt in
Hearthlight's style, with friends, for the pleasure of it.**
- **Chill: no story, no combat, no levels.** It is a walking simulator you share: walk, drive,
  look, discover. The experience is the game.
- **Real parks you recognise.** Someone who has been there should recognise the roads, the trails
  and the famous places without a label.
  - Each map follows the park's official visitor map.
  - Its landmarks are modelled from real reference photos (§7.8).
  - The art stays ours: tiles and terraces, toon light, the chibis.
- **Compressed where the park is empty.** Hotspots stay near true scale; the wilderness between
  them is squeezed.
- **Getting around like a visitor.** On foot, by bike, or in **your van** on the park roads. Where
  the park runs a shuttle, you ride it: Zion's canyon is shuttle-only most of the year, so you
  park the van and take the bus.
- **The park's own animals**, alive and wary: keep your distance.
- **Real activities**: hiking, wading, a permit lottery, a ranger talk, a sunrise, camping under
  the stars.
- **Being there when the park does its thing**: Old Faithful, the firefall, the synchronous
  fireflies, the bats at dusk.
- **Discoveries and easter eggs** are hidden everywhere (§8.8), so there is always something to
  find. More things to do come later (§8.9).
- **The US world map** (§6.3): a Mario-like overworld of the United States with the parks as big
  points of interest. You spawn in one, and leave it (by a park entrance, or from the park's
  menu) to choose another.
- **Shared by default.** Everyone online in the same park sees each other: a small, gentle MMO.
  Speech bubbles, quick phrases, waves, group photos and campfire circles.
- **Party and solo stay first-class**: the couch with phones as controllers, or one player,
  even offline.
- **We keep the engine**:
  - the big world's streaming, relief, water and painter workers;
  - Party Mode's phones, split screen, relay and remote play;
  - the solo « party of one »;
  - the vehicles, mounts, swimming and camps.

## 2. Pillars

1. **The real park, in our style.** You could hold the NPS brochure next to the screen and find
   your way. Names, roads, trails, rivers and landmarks go where the map puts them, and so do the
   sightlines (Half Dome from Glacier Point). The art is ours: stylised, compressed, cozy.
2. **Walk, look, share. No story, no combat.** The verbs are walk, hike, climb, paddle, ride, drive,
   photograph, spot, sketch, stamp, learn, camp and chat. There is no gloom in the real parks, and
   nobody dies. A slip sends you back to the trail.
3. **Together by default.** The open world is the default. Party and solo are one tap away, and
   the same save carries between them.
4. **True and respectful.**
   - Facts come from the parks themselves, and rangers say true things.
   - Leave No Trace is the rules of play.
   - Native lands and sacred places are told the way the parks tell them. No silly gameplay on
     them.
5. **Procedural everything, as always.** No image or audio files. Maps are compact data plus
   code, and photos are the player's own renders.

## 3. Three ways to play

| Way | Who | The simulation | The network |
|---|---|---|---|
| **Open world** (default) | anyone online: one player, or a household (a big screen + phones) | each client simulates its own avatars; the world server shares presence | WebSocket to the world server (`server/world.mjs`, §5) |
| **Party** | 1–8 at one big screen, phones as pads (+ remote players by link) | the big screen (host), as today | the existing relay (`server/relay.mjs`) |
| **Solo** | one player: keyboard, gamepad or a phone | local, as `src/solo/wild.js` | none (works offline) |

- **The title screen.** « Parks » opens the road-trip map (§6.3). A park's card offers
  **Play** (the open world, preselected), **With friends here** (Party) and **Alone** (Solo).
  The choice is remembered.
- **A household in the open world.** A Party can go online together. The big screen opens one
  world connection that carries its local players' avatars (up to 8, each counted against the
  instance's cap). Phones keep talking to the relay, which talks to the host, as today. Remote
  players streamed by the host (`play.html`) belong to the household. The split screen simply
  shows strangers too.
- **Offline is a mode, not an error.** If the world server can't be reached, the same park runs
  as solo or Party. A small badge says « offline » and the game reconnects in the background.
  Everything personal (§8.2) is saved locally, like today's saves, with the optional online
  backup.

## 4. Talking: speech bubbles, quick phrases, emotes (every mode)

This is built first (P1): it is small, useful in today's Party Mode, and the MMO's first brick.
The engine already has most of it:
- `Player.say(text, t)` and `setEmote(kind, t)` in `src/party/party.js` and `src/solo/wild.js`;
- the paper bubble in the pixel font, `bubble()` in `src/ui/ui.js`, drawn over every view with
  side-by-side stacking;
- the emote icons (heart, star, note, exclaim, question, sweat, sparkle, zzz).

### 4.1 Sending
- **Phone (`pad.html`)**: a speech-bubble button on the pad opens a sheet with:
  - a text field on the phone's own keyboard (80 characters);
  - **quick phrases**: a grid of 12 a page (greetings · park talk · help);
  - the emotes (wave, cheer, laugh, heart, sit, photo pose, point…);
  - the last things you said.

  Sending closes the sheet. While the sheet is open, a « … » bubble floats over your hero.
- **Keyboard**: `ctl('chat')`, T by default (T is free; Enter is the arrows player's action),
  opens a paper chat line at the bottom of that player's view. Enter sends and Esc closes. While
  it is open, that player's keys type instead of move; the others keep playing.
- **Gamepad**: hold `ctl('talk')` (Y in the parks, where no combat button is needed) for a
  wheel of 8 quick phrases and emotes. « Write… » opens the on-screen keyboard
  (`src/ui/osk.js`).
- **Remote play (`play.html`)**: a text box in its controller panel, plus T.
- **Solo**: bubbles too. NPCs react to the quick phrases (a ranger waves back at « Hello! »).

### 4.2 Showing
- The bubble sits above the head in every view that frames the player. It lasts 2.5 s plus
  60 ms a character, at most 8 s. A newer message replaces it after at least 1 s on screen.
- **Quick phrases travel as ids** and each screen shows them **in its own language**
  (`t('Look at that!')` → « Regarde ça ! »). Strangers from five languages can talk without
  typing.
- The chat log:
  - the phone gets a « Chat » page with the last 50 lines;
  - the big screen can show a small fading log in a corner (a setting);
  - in the open world, bubbles of players out of view go to the log only.
- The pixel font covers Latin script with French, Spanish, German and Italian accents.
  - Common emoji and emoticons map to the emote icons (❤ → heart, :) → smile).
  - Other scripts show as a small « ? » for now. Growing the font is a later option.

### 4.3 Safety (see §5.7 for the open world)
- **Local party** (same room): no filter by default, with a « family filter » setting.
- **Remote party** (invited by link): the same, plus mute per player.
- **Open world**: quick phrases and emotes always work. Free text is filtered and
  rate-limited, and you can mute, block and report (§5.7).

### 4.4 Code touch points
- `src/pad/pad.js`: the sheet, and the messages `{t:'say', text}` and `{t:'quick', id}`.
- `src/party/inputs.js` and `net.js`: routing.
- `Player.say`.
- A new `src/parks/chat.js`: the phrase list, the local filter, the log, emoji → emotes. It is
  shared by Party, solo and the open world.
- i18n: the phrases are `t()` keys, in all four dictionaries.

## 5. The open world's server (robust by design)

### 5.1 Shape
- **`server/world.mjs`**: a Node service using `ws`, like the relay, with its own systemd unit
  on the same VPS and nginx at `/world`. `config.js` gains `world`.
  - It shares helpers with `relay.mjs`: token buckets, origin checks, stats.
  - A separate process means a crash or restart of one never takes the other down.
- **Clients simulate; the server relays and referees.** It carries positions, bubbles, emotes,
  small instance props (§5.3), community counters and the clock. There is no combat, so
  movement can be client-driven with server checks.
- **Nearly stateless.** Presence lives in memory. Only moderation (mutes, bans, reports) and
  counters persist, in `STATS_DIR`, like the relay's counters.

### 5.2 Instances & interest
- **Instances.** Each park has one or more instances. The hard cap is ~60 avatars, to be set by
  perf tests (§5.6).
  - A newcomer joins the busiest instance under a soft cap (~40), so parks feel alive.
  - Households and friends always land together (a friend's code, like party codes).
  - Empty instances close after a grace period.
- **Interest by chunk.** Cells are the streamer's 32×32-tile chunks. Each client subscribes to
  the 5×5 cells around each of its views; a split screen takes the union. It hears only about
  avatars in those cells: enter, leave and moves, plus bubbles and emotes.
- **Ticks.** The server batches at 10 Hz: one message per client per tick with every
  neighbour's update. Positions are quantised to 1/16 tile, headings to 8 bits.
  - Clients interpolate others about 150 ms behind and extrapolate briefly when a packet is late.
  - Players walk through each other: no body-blocking on narrow trails.

### 5.3 What is shared, what is computed locally
- **Deterministic from `(park seed, server time)`**: computed identically on every client, so no
  messages are needed.
  - wildlife herds and their routes (everyone sees the bison cross the road together);
  - the rangers' routines, the weather, and the moments' schedule (§8.3: « next eruption in
    6 min » is the same for everyone).
  - Clients only need clock sync: a ping-based offset, within ±50 ms.
- **Server-held, small, with a TTL**: campfires lit, tents pitched at campground sites, seats at
  a ranger talk. Also **community counters** (« 1,204 visitors saw Old Faithful today ») and
  community goals (the instance counts 100 bison together, and the ranger throws a little
  celebration).
- **Personal**, on the client with the optional online backup: the passport, the field guide,
  photos, trails, outfits and Young Ranger badges.

### 5.4 Protocol sketch (JSON first, binary later if it matters)
```
C→S hello   {v, park, household:[{name, look}], resume?}     S→C welcome {instance, ids, time, seed}
C→S move    {a, x, z, y, h, anim, ride}          (≤10 Hz, only when it changed; 1 Hz keep-alive)
C→S say     {a, text} | {a, q: phraseId}         C→S emote {a, e}
C→S prop    {kind: 'fire'|'tent'|'seat', spot}   C→S sub {cells}      C→S report {who, why}
S→C tick    {moves, enter, leave, says, emotes, props}                 (one per client per tick)
S→C event   {kind, …}  (a counter, a goal reached, a server notice)
S→C notice  {kind: 'filtered'|'muted'|'restart'|'update', …}           ping / pong (clock sync)
```

### 5.5 Robustness checklist
- **Versioned protocol.** Too old a client gets a friendly « a new version is out » and the page
  reloads.
- **Resume.** A dropped connection keeps its avatars for 60 s: the hero sits down and fades
  instead of vanishing. Reconnects back off exponentially with jitter (0.5 s → 30 s) and come
  back with a resume token.
- **Offline fallback** (§3): the park keeps running locally, with the deterministic world
  (§5.3) on the local clock.
- **Restarts and updates.**
  - The server announces them (`notice restart in 60 s`). Clients reconnect afterwards and
    re-announce themselves, and instances rebuild from the resume tokens.
  - Deploys reuse the VPS update script that already ships the relay, with its backup and a way
    back (kept with the VPS scripts, outside this repo). A kill switch (`world: null` in
    `config.js`) turns the open world off and leaves Party and Solo.
- **Backpressure.** Each client has a send queue checked against `bufferedAmount`.
  - Stale move updates are dropped; chat and events never are.
  - A client that stays more than 2 MB behind is dropped, as the relay does.
- **Limits** (token buckets, as in `relay.mjs`):
  - connections and households per IP; avatars per household (8);
  - messages a second and message sizes;
  - instance and global caps; idle time-outs.
- **Validation.**
  - Speed checks per ride (walk, run, bike, horse, car, boat).
  - Positions must stay inside the park's bounds.
  - Jumps happen only at fast-travel points; the server knows them from the park's data.
  - A suspicious client gets a snap-back, not a ban.
- **Observability.** `/health`, and `/stats` (instances, avatars, messages a second, drops,
  filter hits, reports) on the existing dashboard.
- **Tests.**
  - Unit tests: `server/world.test.mjs`.
  - A load test: `server/worldload.mjs`, 1,000 bot avatars in 20 instances, walking and chatting.
  - Browser bots: `tools/parkbots.js`, like `partybots.js`.
  - Chaos tests: kill the server mid-walk, drop 10 % of packets, and add 300 ms of latency.

### 5.6 Capacity (estimates to confirm by the load test)
- **Down**: ~20 neighbours × ~10 bytes × 10 ticks ≈ 2–4 KB/s per client. **Up**: ~0.3 KB/s.
- 1,000 players online → ~3–4 MB/s out of the VPS. Batching makes that ~10k messages a second,
  the same order as the relay's load test (100 parties of 8 at ~28 % of a core).
- **Client side**, drawing 30–60 extra chibis needs LOD and a cap:
  - the nearest 40 avatars are drawn in full;
  - further ones are simple sprites;
  - beyond that, only dots on the minimap.

### 5.7 Moderation
- **Names.** The creator's name is filtered in the open world. If it is refused, the player
  gets a cute generated one (« Mossy Marmot ») and can try another.
- **Free text.**
  - At most 80 characters; 1 message per 1.5 s, bursts of 3; repeats are dropped.
  - Filtered per language: word lists for en, fr, es, de, it, with normalisation of accents,
    spacing and leetspeak.
  - URLs, e-mail addresses, phone numbers and @handles are blocked.
  - The server's filter is the authority; the client's is only a courtesy that explains the
    refusal.
- **Mute and block** are per player, local and remembered. **Report** sends the last 20 lines
  seen from that player to a moderation log kept 7 days.
- **Automatic measures.**
  - Auto-mute after repeated filter hits.
  - Temporary bans by device id plus a salted IP hash; no raw IP is kept, like today's counters.
- **The dashboard** gets a « reports » page with mute and ban actions.
- **No private messages** at first. Bubbles are public and local, with party chat inside a
  household.

### 5.8 Privacy & legal notes
- `PRIVACY.md` must say:
  - chat is relayed, not stored, except excerpts from reported players (7 days);
  - the identifiers are a random device id and a daily-salted IP hash.
- **Minors.** A family setting, « quick phrases only », is the default under it. Open question
  §11.3 covers COPPA and GDPR-K.
- **Park names are geographic and free to use.** Some things must be handled carefully:
  - **Never draw the NPS arrowhead** (a protected emblem).
  - « Passport To Your National Parks » is a registered trademark (of America's National Parks),
    so the game says **« Park Passport »**.
  - « Junior Ranger » is the NPS's programme, so the game says **« Young Ranger »**.
  - The credits say that Hearthlight is not affiliated with or endorsed by the National Park
    Service.
- **Sources.** NPS maps and data are US-government works in the public domain. OpenStreetMap is
  ODbL, so shipped data derived from it credits « © OpenStreetMap contributors ».
  `docs/parks/SOURCES.md` has the details.

## 6. The parks

### 6.1 The atlas
[`docs/parks/README.md`](../parks/README.md) lists the 63 parks: code, state, region, tier,
biomes, signature places, the proposed map size and a link to each dossier. Every dossier
(`docs/parks/<code>.md`) follows the same template (`docs/parks/_template.md`):
- **the official maps** (links);
- **reading the map**: a walk-through precise enough to redraw it, plus districts, roads,
  25–45 places with coordinates, signature trails, water, relief and an ASCII sketch;
- **look & feel**: vegetation bands, a palette, wildlife, flora, seasons, night, sounds;
- **moments**: the signature events with their real timing;
- **for the game**: scale, hubs, set pieces, activities, stamps, co-op and open-world ideas,
  Leave No Trace rules, implementation challenges;
- **sources**.

The raw data behind each dossier (the NPS boundary, points of interest, trails and roads, and
OSM named features) is rebuilt at will by `tools/parks/fetch.py` into `tools/parks/cache/`
(git-ignored).

### 6.2 Tiers and the first set
- **Tier 1**: icons with dense, varied visitor places. They are full maps (768–1536 tiles a side)
  and make the first release.
- **Tier 2**: full maps built afterwards, a region at a time.
- **Tier 3**: « vignettes », smaller maps (256–512 tiles) around one to three set pieces. These
  are the remote Alaskan wilderness, the tiny urban parks and the one-note parks.

The atlas has the final table: 10 parks in tier 1, 36 in tier 2 and 17 in tier 3. Each dossier's
own suggestion stays in `parks.json`.

**The first wave** (tier 1) takes one of each great landscape. In build order:
1. Zion
2. Acadia
3. Yellowstone
4. Yosemite
5. the Grand Canyon
6. the Great Smoky Mountains
7. Arches
8. Grand Teton
9. Olympic
10. Hawaiʻi Volcanoes

Three of them reuse what the engine already draws: Prism Springs' geysers, Elderbough's granite
valley, Emberpeak's lava. The atlas's README says why each one is there.

The **pilot** (P2–P3) should be compact, iconic, clear in its topology and cheap in new tech.
The proposal is **Zion**:
- one canyon with a shuttle road, a river you wade (the Narrows) and famous trails (Angels
  Landing's chains, Emerald Pools);
- the tunnel and switchbacks, and 600 m walls that test the relief and the rim cut-away (§7.7);
- all in ~596 km², proposed as a 1024 × 1024-tile map.

**Acadia** comes second: coast, tides, a sunrise summit, carriage roads and a lighthouse.

### 6.3 The US world map (a Mario-like overworld)
- **The map** is the United States drawn in code like a *Super Mario World* overworld.
  - State outlines come from the US Census cartographic boundaries (public domain), simplified
    to compact polylines in `src/parks/data/usa.js`.
  - Soft relief and colours per region: deserts, forests, mountains, coasts.
  - The parks are **big points of interest**, each with a little landmark of its own (Half Dome,
    Old Faithful, the Arch…) rather than a dot.
- **The parks are apart.** Each one is its own map, and the overworld is how you go from one to
  another.
  - Your **van** drives along the overworld's stylised roads between the pins; the drive is a
    short, cosy transition.
  - Alaska, Hawaiʻi, American Samoa and the Virgin Islands are insets, reached by plane or ferry.
  - The van is also your home between parks: its stickers are your passport's cover.
- **Spawn in a park**: at its main entrance or visitor centre, or next to your friends.
- **Leave a park** by driving out through an entrance station (the gate opens onto the
  overworld), or from anywhere inside with the park menu's « Change park ».
- **In the open world**, each pin shows how many people are in that park and where your friends
  are. A household travels together.
- **In the first version**, Zion is open and the other 62 pins are on the map as « coming soon ».
- **Trips group the parks** (the legs of the road trip) and give themed collections; a leg's pins
  light up as you visit them:
  - the Grand Circle (Utah, Arizona, Colorado, New Mexico);
  - the Pacific Crest (Washington, Oregon, California);
  - the Rocky Road (Montana, Wyoming, Colorado);
  - the Alaska Frontier;
  - the Appalachians and the East;
  - Lakes & Rivers (the Midwest);
  - the Islands (Florida's keys, the Caribbean, the Pacific).

## 7. From the visitor map to a game map

### 7.1 Principles
1. **Topology first.** Keep:
   - the order of places along roads, the loops and junctions;
   - which side of the river things are on, and which way water flows;
   - the sightlines: what you see from where.
2. **Variable scale (a « rubber sheet »).**
   - **Hotspots** stay near true scale, 1 tile ≈ 2–4 m: villages, geyser basins, viewpoints,
     trailheads, typically 0.3–3 km across.
   - **Corridors** (roads, trails, rivers) are compressed 5–20× between them.
   - **Wilderness fill** is generated in the park's biomes, heavily compressed or cut.
3. **Time targets decide the compression.**
   - Hub to a nearby sight: 20–60 s on foot.
   - Hub to the next hub: 40–90 s in a vehicle.
   - A signature trail: 2–5 minutes.
   - Map sizes: tier 1, 768–1536 tiles a side; vignettes, 256–512.
4. **Real names, real relative positions, real silhouettes** for the landmarks. When the
   brochure and reality disagree, follow the brochure: it is what visitors carry.

### 7.2 The layout format (one file per park: `src/parks/data/<code>.js`)
```js
export default {
  code: 'ZION', name: 'Zion National Park', size: [W, H], seed,
  anchors: [{ id, lat, lon, at: [x, z] }],            // the warp's control points
  hubs: [{ id, name, kind: 'visitor'|'lodge'|'camp'|'trailhead', at, r, stamp }],
  roads: [{ id, name, pts, kind: 'road'|'shuttle'|'dirt'|'boardwalk', oneWay, season }],
  trails: [{ id, name, pts, grade, chains, wade }], rivers: [{ pts, width, flow }],
  lakes: [poly], coast: [poly], relief: 'levels RLE (0–7)', biomes: [{ tile, poly }],
  flora: [{ kind, density, poly }], pieces: [{ id, model, at, params }],
  moments: [{ id, at, every: [min, max], season, hour }], wildlife: [{ species, poly, when }],
  stamps: [{ id, at }], photos: [{ id, at, look, frame }], rangers: [{ id, at, talks }],
};
```

### 7.3 The pipeline (`tools/parks/`)
1. **`fetch.py`** (done). The data pack: the NPS boundary, the NPS API text, Wikipedia's figures,
   the official map links, the NPS points of interest, the NPS trails and roads, and OSM named
   natural features.
2. **`dem.py`** (to write). Elevation from USGS 3DEP (the National Map; 10–30 m, public domain)
   or the AWS Terrain Tiles, resampled into the park's local metric frame.
3. **`warp.mjs`** (to write). The rubber sheet.
   - Anchors map real positions to game positions, through a piecewise-affine warp over their
     Delaunay triangulation (a thin-plate spline as an option).
   - It projects every feature and resamples the DEM onto the game grid.
   - Elevation is quantised into the engine's 0–7 levels with the park's own breaks, so a canyon
     reads as a canyon, not a ramp.
4. **`draft.mjs`** (to write). Writes the first `src/parks/data/<code>.js` and a preview PNG in
   `screenshots/` (like `tools/bigmap.mjs`), to compare side by side with the brochure.
5. **The hand pass.** Place the set pieces, fix the sightlines, tune distances in play, and
   score /10 against the brochure and against fun.

### 7.4 Terrain vocabulary: real landscapes → Hearthlight
| Real landscape (parks) | What Hearthlight already has | What to add |
|---|---|---|
| sandstone canyons (Zion, Grand Canyon, Black Canyon) | `CANYON`, `MESA` faces, relief 0–7 | banded strata faces (the Grand Canyon's layers), narrows, slot canyons |
| slickrock, arches, fins (Arches, Canyonlands, Capitol Reef) | `MESA`, `ROCK` | arches and fins as 3D pieces, potholes |
| hoodoos (Bryce, Badlands) | — | instanced spire fields; banded badlands |
| geysers, hot springs, sinter (Yellowstone, Lassen) | Prism Springs: Grand Prismatic rings, sinter, orange mats, travertine, timed geysers | mudpots, fumaroles, boardwalk tiles |
| granite domes and walls, great falls (Yosemite, Kings Canyon) | Elderbough: granite walls, Half Dome, El Capitan, a great fall | domes and exfoliation slabs as pieces |
| giant sequoias and redwoods (Sequoia, Redwood) | one Great Tree | instanced giant trunks, fern understory |
| alpine peaks, glaciers, turquoise lakes (Glacier, Rainier, North Cascades, Grand Teton) | Aurora Tundra, Frostpeak: glacier tongues, snow, 3D peaks | a glaciated volcano cone (Rainier) |
| volcanoes and lava (Hawaiʻi Volcanoes, Haleakalā, Lassen) | Emberpeak: lava, lava falls, ash, obsidian, basalt | pāhoehoe/ʻaʻā fields, cinder cones, lava tubes, steam vents |
| deserts: dunes, cacti (Joshua Tree, Saguaro, Death Valley, White Sands, Great Sand Dunes) | Sunscorch Dunes, `DUNE`, buttes | saguaro, Joshua tree, cholla, creosote; white gypsum dunes |
| salt flats (Death Valley) | Saltmirror: salt, the mirror | salt polygons |
| swamps, mangroves (Everglades, Congaree, Biscayne) | Croakmire (bayou, bog), Glowtide (mangroves) | sawgrass prairie, cypress knees, hammocks |
| reefs and tropical beaches (Virgin Islands, Dry Tortugas, Biscayne, American Samoa) | Coral Lagoon, `CORAL` | a snorkel view (the underwater layer) |
| temperate rainforest (Olympic) | Deep Whisperwood | moss-hung trees, nurse logs |
| Appalachian forests (Great Smoky Mountains, Shenandoah, New River Gorge) | Emberleaf (autumn), forests | blue haze, grassy balds |
| prairie (Wind Cave, Theodore Roosevelt, Badlands) | Golden Steppe | prairie-dog towns |
| tundra, taiga, Arctic dunes (Alaska) | Aurora Tundra | spruce taiga, braided rivers, tussocks |
| caves (Carlsbad, Mammoth, Wind Cave, Lehman, Nāhuku) | dungeons (dark caves, x ≥ 3000) | formations, ranger-lit tour routes |
| fjords and tidewater glaciers (Kenai Fjords, Glacier Bay) | Lantern Bay (fjord), glaciers | calving fronts, icebergs |
| towns and history (Gateway Arch, Hot Springs, Cuyahoga Valley) | town buildings, masonry | the Arch, bathhouses, a canal towpath |

### 7.5 Set pieces
Every dossier lists its landmarks to model: Half Dome, Old Faithful, Delicate Arch, General
Sherman, the Gateway Arch, Bass Harbor Head Light, Fort Jefferson, Clingmans Dome's tower, the
Desert View Watchtower, Wizard Island, Brooks Falls…
- They are procedural 3D models like `src/models/v7/landmarks7.js`, parametric where possible:
  one arch model gives Delicate, Landscape, Mesa and the Windows.
- Expect ~150 over the 63 parks; tier 1 needs about 40.

### 7.6 Engine work
- **Park maps are big outdoor instances.** `src/saga/instance.js` already builds « a little map
  of the big world's tiles », painted in workers, streamed, walked with the same collision and lit
  at its own hour. A park is a larger one:
  - in its own slot off the main world (x ≥ 10000);
  - with its own size, palettes, weather and lighting.
  - The streamer, painter, collision and minimap take a map descriptor instead of the `BIG`
    constant, which is imported in 8 files today.
- **New tiles, painters and plants** (§7.4). Water that moves: tides (Acadia, Olympic), rapids for
  rafting (the Colorado, the New River), wading (the Narrows), a snorkel layer.
- **Caves** use the dungeon tech (x ≥ 3000), with lantern-lit ranger tours.
- **Vehicles**:
  - shuttle buses on routes with stops (Zion, Yosemite, Acadia's Island Explorer, Denali);
  - Glacier's red buses;
  - canoe and kayak, raft, horse and mule, ferry;
  - the bush plane (a fast-travel scene), the snowcoach, the tram, the scenic train (Cuyahoga
    Valley), a 4WD jeep (Great Sand Dunes' Medano Pass road), houseboats (Voyageurs).
- **A photo mode.** Aim, zoom and frame. The shot is a render of the canvas, saved to the album.
  It is the player's own picture, not a shipped asset.
- **Seasons and weather per park.** The night sky: stars, the aurora (ch9 has one), fireflies
  (ch8 has them), bioluminescence.

### 7.7 Systems the maps asked for
Read side by side, the 63 maps kept asking for the same things. The ten researchers' reports
raised them again and again. Build each one once, as a shared system:

1. **The rim and canopy cut-away.** The camera looks north, so in a canyon the south wall hides
   the floor you walk on: Zion, the Grand Canyon below the South Rim, Black Canyon,
   Canyonlands, Yosemite Valley under Glacier Point, Kings Canyon, Bumpass Hell. Giant trees
   hide the forest floor the same way (sequoias, redwoods). One fade or cut-away for whatever
   stands between the camera and the heroes. Three researchers raised it on their own: it is
   P2's first engine task.
   - With it, an **overlook camera**: at a railed overlook the camera turns toward the view.
     Bryce's rim faces east, Mesa Verde's alcoves face every way, and Denali's Mountain rises to
     the south (a south-facing photo mode).
   - Slot canyons keep their width and compress their depth: the Narrows, Wall Street, Black
     Canyon's narrows.
2. **One park clock, shared by everyone online**:
   - **Geysers with prediction windows.** Geyser gazers call eruptions for everyone, the Old
     Faithful benches get a countdown board, and a rare Steamboat eruption is an event for the
     whole server.
   - **Tides**: Olympic's headlands and Hole-in-the-Wall, Acadia's Bar Island bar and Thunder
     Hole.
   - **Synchronous fireflies** (Elkmont, Congaree): every player sees the same flashes.
   - Kīlauea's fountain episodes, capped sunrises (Haleakalā, Cadillac Mountain), and the
     firefall's ten minutes in February.
   - Denali's « the Mountain is out » (about 30 % of days) as shared weather.
   - The caribou crossings at Onion Portage and Anaktuvuk Pass as scheduled world events.
3. **Water level as a park setting**:
   - tides;
   - floods: Congaree's boardwalk under water, Cuyahoga's towpath;
   - rapids: the New River, the Colorado;
   - wet and dry seasons: the Everglades;
   - Medano Creek's surge, which could follow the real snowpack.
4. **Seasons as map states**:
   - roads that open in segments between snow walls: Going-to-the-Sun, Trail Ridge, Lassen,
     Crater Lake's rim;
   - winter modes: snowcoaches in Yellowstone, ice roads on Voyageurs' lakes, Isle Royale
     closed from November to April;
   - nesting closures (Bush Key), and missile tests closing White Sands' only road.
5. **The journey as a playable crossing.** Ferries, seaplanes and bush planes, shuttle buses,
   the scenic train and the Wilderness Waterway are short crossings that double as a party
   lobby.
   - « One boat, many roles »: a captain reads the depth colours while the others spot
     wildlife.
   - Boat timetables with a horn call-back (Channel Islands).
   - Map edges reached only by boat or plane: Stehekin, Manuʻa, Kīpahulu, Isle Royale.
   - One Alaska bush-plane network linking the vignettes by their real flight distances (King
     Salmon → Brooks Camp 33 mi). Floats or wheels decide where a plane can land, the weather
     can hold it, and the party shares one plane with a weight limit.
6. **One underwater layer for the marine parks** (Biscayne, Dry Tortugas, Virgin Islands,
   American Samoa…):
   - water depth painted from the brochure's legend, so boats run aground on the white flats;
   - snorkel finds go in the field guide;
   - a stamp for each wreck on Biscayne's Maritime Heritage Trail.
7. **Two worlds stacked.**
   - Caves as instanced levels under the surface (the engine's dungeon caves): Mammoth Cave
     with its rooms marked on the ground above, Carlsbad, Wind Cave, Lehman Caves, Nāhuku.
   - Hot Springs' 4,400-year water cycle as a cross-section.
   - Time as a layer: Glacier Bay's dated ice fronts (1750 → today) as a glacier-retreat slider,
     and Exit Glacier's dated moraine signs.
8. **A field guide with stories**:
   - individual animals: Pinnacles' condors wear numbered wing tags;
   - lineages: the Bronx Zoo bison went to Wind Cave in 1913, Theodore Roosevelt's to the
     Badlands in 1963;
   - the safe distance drawn as a comfort ring, from 15 ft for alligators to 100 yd for bears.
9. **Road-trip seams between parks**:
   - the Rockefeller Parkway joins Grand Teton to Yellowstone at Flagg Ranch;
   - the Blue Ridge Parkway carries Skyline Drive on to the Smokies, with mileposts as
     coordinates and fast travel;
   - the Guadalupe Ridge Trail links Carlsbad Caverns to Guadalupe Peak;
   - Route 66, 100 years old in 2026, runs by Petrified Forest and the Grand Canyon;
   - Sequoia and Kings Canyon share one map with separate stamps;
   - Waterton's boat to Goat Haunt crosses a border.
   - **Across the chasm**: Black Canyon's rims are 335 m apart at Chasm View but 2–3 hours
     apart by road, and Canyonlands' districts are linked only by the rivers. Players see and
     wave across, then take the long way.
10. **Respect as gameplay**:
    - Closed and sacred places stay closed. Turning back earns a « respect badge » (Hyperion,
      Lechuguilla).
    - In American Samoa, ask permission and keep the evening prayer hour and Sunday quiet.
    - At petroglyphs, look and never touch.
    - Petrified Forest's « bad luck » letters: return the pocketed wood.
    - The Native place-name tables printed on the Denali, Wrangell–St. Elias and Lake Clark maps
      become things you learn from rangers and collect.
11. **Desert and night rules.** Heat, water and shade are one desert system (strongest in Death
    Valley). Most desert parks are International Dark Sky Parks, which gives a shared set of
    night moments.
12. **Party games only one park could give**:
    - the rim-to-rim key swap: half the party starts on each rim, and they trade car keys at
      Phantom Ranch;
    - postcards mailed by mule;
    - the llama string to LeConte Lodge;
    - Denali's bus « spot & stop », where the first to spot an animal stops the bus for
      everyone;
    - the firefly lottery as the party's ticket;
    - the group photo straddling the state line at Newfound Gap;
    - Brooks Falls' bear platform, with its real 40-person limit and queue: a ready-made gathering
      spot for the open world, with a « bear book » and the Fat Bear Week vote;
    - the parks' real rules as gentle loops:
      - Angels Landing's permit lottery, with results at 4 pm;
      - ranger tour slots: the Fiery Furnace, Mesa Verde's cliff dwellings;
      - Bryce's « Hike the Hoodoos » benchmark rubbings;
      - Capitol Reef's orchards, from blossom to ripe fruit, then pick and pay at the scale,
        and the Gifford House pies;
      - the Zion and Bryce shuttles as fast travel with narrated stops.

### 7.8 Realism: recognisable, from reference photos
- **The bar.** Someone who has been to the park recognises, without labels, its roads, its trails
  and its famous places:
  - the silhouette of each landmark;
  - what stands left and right of the road;
  - the colours at that hour.
- **Reference views.** Each park gets a list, `docs/parks/refs/<CODE>.json`. Every entry gives the
  view, where the camera stands and which way it looks, what must match, the image URL, the
  source page, the credit and the licence. Zion's list is the first.
  `python3 tools/parks/fetch.py refs --only ZION` downloads the images into the git-ignored cache
  (`tools/parks/cache/ZION/refs/`), to look at while modelling.
- **Rules for the photos.** They are references only: never in the repo, never in the game, never
  shown to players; the game stays procedural. Prefer NPS public-domain photos, then freely
  licensed ones (Wikimedia Commons, with the licence noted), and no people as subjects.
- **The recognition test** (part of the scoring, §10.1). For each reference view, take a
  screenshot from the same spot and direction. Compare them side by side (silhouettes, layout,
  colours) and fix until a visitor would say « that's the Watchman from the bridge ».
- **The scale, again.** The warp of §7.1 keeps the recognisable places near true proportions.
  Compression goes to the in-between, never to what a visitor photographs.

## 8. What players do

### 8.1 The loop
1. **Arrive** at the visitor centre: a stamp, a ranger's welcome, and the park map on the phone.
2. **Choose** a trail or a sight. The map shows the moments' countdowns.
3. **Walk, spot, sketch, photograph and learn.** A moment happens and everyone gathers.
4. **Rest** at a campground or lodge (tents, a campfire, the stars).
5. **Drive on** to the next park.

### 8.2 Collections (personal, saved like today's progress)
- **The Park Passport**: the real cancellation-stamp spots (visitor centres…), dated with the
  in-game date. Bonus stamps come from moments (« Old Faithful — seen erupting »).
- **The field guide**: a species card when you spot an animal **at a proper distance** with
  binoculars. The card shows the voxel model and ranger facts.
- **The herbarium**: plants you sketch. Look, don't pick.
- **The photo album**: the famous frames score « postcards » when framed right, and free photos
  go in too.
- **Trails and summits**: a patch on your backpack for every named trail finished, and a pin
  for every summit.
- **Young Ranger badges**: each park has a booklet of 4–6 activities:
  - a quiz with a ranger;
  - a scavenger hunt;
  - a litter pick;
  - an animal count;
  - a night-sky or listening activity.
- **Souvenirs**: hats and shirts from each park (cosmetic only), and stickers for the van.

### 8.3 Moments
Each park's signature events are listed with their real timing in the dossiers. In the game their
timing is compressed, but they stay readable and predictable: a board at the visitor centre and a
countdown on the phone. Examples:
- Old Faithful's eruptions;
- Yosemite's February firefall;
- the synchronous fireflies (Great Smoky Mountains, Congaree);
- Carlsbad's bat flight at dusk;
- the bears at Brooks Falls in the salmon run;
- the elk rut;
- sunrise on Cadillac Mountain and Haleakalā;
- Thunder Hole at mid-tide;
- Medano Creek's surge;
- the aurora;
- the desert superbloom.

### 8.4 Rangers, facts and tone
- A ranger per hub, warm and a little funny, the way the game's cast is. Prism Springs'
  Ranger Rhoda, who loves rules, is the template.
- Every fact is true and sourced from the dossiers, in short lines.
- The Duchess, the gloom and the story's villains stay in the story. The parks are for wonder.
- A few Hearthlight friends may visit as cameos (Pim with his trade cart, Perkins' post).

### 8.5 Getting around
- On foot, running, or by bike (the `bike` key exists).
- Park vehicles (§7.6).
- Fast travel between visited visitor centres, trailheads and shuttle stops. `travel.js`'s
  waystones become exactly that.

### 8.6 Leave No Trace, as the rules of play
- **Stay on the boardwalk** in thermal areas. Step off and a ranger's whistle walks you back.
- **Keep your distance** from wildlife: 25 yd (23 m) from bison, elk and most animals, 100 yd
  (91 m) from bears and wolves, as the NPS asks. Closer, and the animal leaves or bluff-charges,
  and the field guide doesn't count it.
- **Pack out your trash.** Litter is also a small co-op chore: a Young Ranger activity.
- **Don't feed the animals.** Keep quiet hours at campgrounds, follow the fire rules, and take
  nothing but photos.

### 8.7 Controls in the parks
With no combat, the buttons change job. All of them are named with `ctl()` on the device in hand.

| Action | Gamepad | Keyboard | Phone |
|---|---|---|---|
| act | A | E | act |
| jump / back | B | Space | jump |
| camera (photo mode) | X | the special key | camera |
| talk (the wheel) | Y | T | talk |
| binoculars / map / guide on the hotbar | LB / RB | the hotbar keys | the pad's tabs |

The phone's pad relabels its buttons to match: act, jump, camera, talk.

### 8.8 Discoveries and easter eggs
Every park hides things to find, logged in the journal's « Discoveries » page with a count per park
(« 23 / 40 »):
- **Nature off the beaten path**: a hidden alcove, a hanging garden, an arch seen from one spot
  only, a seep with a snail that lives nowhere else.
- **Wildlife rarities**: a condor with its wing-tag number, a desert tortoise after the rain, a
  ringtail by the campground at night, a tarantula crossing in October.
- **The park's history**: the CCC's stonework, the tunnel's windows, an old ranch, the first
  ranger's cabin, each with a ranger's true story.
- **Moments**: being there when it happens, like the Watchman glowing at sunset, the monsoon's
  instant waterfalls or snow on red rock.
- **Hearthlight nods**, the true easter eggs: a wink at the game's world, such as a lost lantern,
  Pim's trade cart at a gateway town's market, or a rubber hen. They stay tasteful and rare, and
  never bend the park's truth.
- **Sky and time**: the stars of a Dark Sky Park, a meteor shower, a moonbow.

Discoveries give stamps, stickers for the van and outfits, never power.

### 8.9 More to do, after the first version
Once the experience is right, add the things that make it fun beyond walking:
- photo challenges;
- co-op hunts (a park « bingo »);
- bike or kayak races;
- a Young Ranger booklet per park;
- community goals;
- seasonal events.

They are all built on the shared systems of §7.7.

## 9. What we reuse

| Need | Existing system |
|---|---|
| a streamed map with relief, water, trees, painting workers | `src/world/big/*`, `src/saga/instance.js` |
| 1–8 players, phones, split screen, remote play | `src/party/*`, `src/pad/*`, `server/relay.mjs` |
| solo on the same systems | `src/solo/wild.js` (the party of one) |
| vehicles, mounts, swimming | `vehicles.js`, `mounts.js`, `swim.js` |
| campfires, sleeping | `camp.js` |
| fast travel | `travel.js` (waystones → trailheads & shuttle stops) |
| maps & marks (big screen and phone) | `worldmap.js`, `mapmarks.js`, `src/pad/padmap.js` |
| timed world events | `events.js` (shooting stars…), the timed geysers of Prism Springs |
| NPCs, dialogue, quests, scenes | the saga engine (`saga.js`, `stage.js`) — rangers & Young Ranger booklets |
| photo & timing mini-games | the `snap`, `seek`, `net` steps (`games7/8/9.js`) |
| bubbles, emotes | `Player.say`, `setEmote`, `bubble()` |
| five languages | `t()` + `src/lang/{fr,es,de,it}` |
| saves & online backup | local saves + `server/saves.mjs` |
| the VPS, deploys, counters | the VPS update scripts, `server/stats.mjs`, the dashboard |

## 10. Milestones

- **P0 — the atlas & this plan** (done, 2026-09-29).
- **The first playable version (P1–P4 for Zion, plus the world map), local only and
  unpublished.** This is the building agent's brief, [`parks-v10-brief.md`](parks-v10-brief.md).
  It covers the messaging, the park engine, Zion complete, the shared-world engine on `localhost`
  and the US world map, and it runs until the rubric of §10.1 is at 9 or more everywhere.
- **P1 — bubbles & quick chat** in today's Party and solo (phone, keyboard, gamepad, remote) and
  in 5 languages. It is useful right away and it is the MMO's first brick.
- **P2 — the park engine and pipeline**:
  - map descriptors instead of `BIG`, and the park instance;
  - `dem.py`, `warp.mjs`, `draft.mjs`;
  - the pilot park's terrain, with screenshots next to its brochure.
- **P3 — the pilot park, playable** solo and in Party: hubs, shuttle, trails, stamps, moments,
  wildlife, rangers, photo mode, a Young Ranger booklet. Iterate to 9/10.
- **P4 — the open world**: `server/world.mjs`, moderation, bots, the load and chaos tests, and
  a kill switch. It is tested locally (and on a private test instance if the user wants one); it
  is not deployed publicly before the release is decided (§0).
- **P5 — the first wave of parks (tier 1)**, from reference photos like Zion.
- **P6 — release** « National Park 1.0 », **only when the user decides it** (§0): the flag comes off, the
  Pages and desktop copies take `src/parks/`, and the world server is deployed. Then tier 2 and
  tier 3, a region at a time.

### 10.1 The bar for a « complete » park: the scoring rubric
After each milestone, every area is scored /10 with evidence. Work goes on until every area is at
9 or more, the game's usual bar:

| Area | What 9/10 means | How it is judged |
|---|---|---|
| **Recognisable** | a visitor recognises every reference view without labels | the recognition test (§7.8): a screenshot per reference view, side by side |
| **Faithful map** | roads, trails, stops and landmarks in the brochure's order and places; distances feel like the park's | the game map laid over the brochure; walking and driving times against §7.1's targets |
| **Beautiful** | the park's colours, light and textures; walls, river, trees; day, night and weather | screenshots at the real camera and zoom, in split screen too |
| **Feel** | walking, climbing, wading, the van, the shuttle and a bike all feel good; nowhere to get stuck | bots walk every trail and drive every road; hands-on play |
| **Alive** | the emblematic animals live their lives and keep their distance; visitors, rangers, the shuttle | watching at dawn, noon, dusk and night |
| **Discoveries & activities** | 1–2 hours of things to find and do: discoveries, stamps, photo spots, the field guide, ranger talks, the park's real rules as loops | a count, and a full playthrough |
| **World map** | a readable, charming Mario-like overworld; smooth ins and outs | screenshots; transitions timed |
| **Shared world** | robust with 60 players in an instance: resume, offline fallback, no desync, bounded bandwidth | the numbers of the unit, load and chaos tests |
| **Messaging** | bubbles from phone, keyboard and gamepad; quick phrases in 5 languages; safe | tests on each device |
| **Performance** | smooth in solo, with 8 split views, and with 40 avatars in view | frame-time measures (`tools/perf.js`) |
| **Quality gates** | 0 console errors, 0 i18n missing, checks and tests pass | the tools |

## 11. Open questions (for the user)

- ~~The name~~ → **« National Park »** (decided 2026-09-29).
- ~~The pilot~~ → **Zion** (decided). The rest of the first wave stays as proposed in §6.2.
- ~~Story or not~~ → **no story**: chill, a walking simulator with friends (decided).

3. **Free text in the open world**: on by default? An age question? « Quick phrases only » as the
   family default?
4. **The clock in the open world**:
   - a shared, accelerated day per park (~60 min), with the real calendar's season?
   - or real local time at the park (sunrise at Acadia when it really rises)?
5. **Progression**: all parks open from the start, or opened along the road trip?
6. **Heroes**: the same hero and wardrobe as the story, with separate park progress (proposed)?
7. **Cameos**: Hearthlight characters in the parks, or rangers only?
8. **Hosting**: one VPS at first (enough by the estimates). A second region (US) later?

## 12. Risks

- **Scope.** 63 parks: use tiers, vignettes and a pipeline that does ~70 % of each map.
- **Fidelity vs fun.** Real parks are mostly empty. Compression, moments and density at the hubs
  carry the fun.
- **Online safety.** Chat moderation is a real, ongoing cost. Quick phrases by default, and the
  kill switch.
- **Performance.** Large maps and many avatars need LOD, caps and the per-chunk interest.
- **Respect and accuracy.** Native heritage, sacred places and true facts: the dossiers cite
  their sources, and the rangers' lines are reviewed against them.
