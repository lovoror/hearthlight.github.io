#!/usr/bin/env python3
"""The US national parks' data pack, for the National Park mode (docs/plans/parks-v10.md).

  python3 tools/parks/fetch.py [steps...] [--only YELL,ZION] [--order CODE,CODE...] [--mirror 0|1|2]

Steps (default: all, in this order): bounds nps wiki maps hfc pois lines osm pack; `refs` on demand.
Writes into tools/parks/cache/ (git-ignored): bounds.geojson, nps.json, wiki.json and, per park:
<code>/maps.json (the maps page's links), hfc.json (the park's maps in the NPS map catalogue),
pois.json (NPS points of interest), lines.geojson (the NPS's trails & roads), osm.json (named
natural features inside the boundary) and pack.md, a digest to read before a park's dossier
(docs/parks/<code>.md) or its game map. `refs` downloads the reference photos listed in
docs/parks/refs/<CODE>.json into <code>/refs/ (with an index.md): references for modelling only,
never committed, never shipped. Standard library only; the NPS API key comes from $NPS_API_KEY
(DEMO_KEY otherwise: 10 calls an hour, one is enough here). Sources & licences:
docs/parks/SOURCES.md. Be gentle with Overpass: one query at a time.
"""
import json, math, os, re, sys, time, html, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
OUT = os.path.join(HERE, 'cache')
UA = 'Hearthlight-parks-research/1.0 (+https://github.com/Hearthlight/hearthlight.github.io)'

# The 63 national parks (NPS unit codes; SEQU & KICA are run together as SEKI).
PARKS = {
  'ACAD': 'Acadia', 'ARCH': 'Arches', 'BADL': 'Badlands', 'BIBE': 'Big Bend', 'BISC': 'Biscayne',
  'BLCA': 'Black Canyon of the Gunnison', 'BRCA': 'Bryce Canyon', 'CANY': 'Canyonlands',
  'CARE': 'Capitol Reef', 'CAVE': 'Carlsbad Caverns', 'CHIS': 'Channel Islands', 'CONG': 'Congaree',
  'CRLA': 'Crater Lake', 'CUVA': 'Cuyahoga Valley', 'DENA': 'Denali', 'DEVA': 'Death Valley',
  'DRTO': 'Dry Tortugas', 'EVER': 'Everglades', 'GAAR': 'Gates of the Arctic', 'GLAC': 'Glacier',
  'GLBA': 'Glacier Bay', 'GRBA': 'Great Basin', 'GRCA': 'Grand Canyon', 'GRSA': 'Great Sand Dunes',
  'GRSM': 'Great Smoky Mountains', 'GRTE': 'Grand Teton', 'GUMO': 'Guadalupe Mountains',
  'HALE': 'Haleakalā', 'HAVO': 'Hawaiʻi Volcanoes', 'HOSP': 'Hot Springs', 'INDU': 'Indiana Dunes',
  'ISRO': 'Isle Royale', 'JEFF': 'Gateway Arch', 'JOTR': 'Joshua Tree', 'KATM': 'Katmai',
  'KEFJ': 'Kenai Fjords', 'KICA': 'Kings Canyon', 'KOVA': 'Kobuk Valley', 'LACL': 'Lake Clark',
  'LAVO': 'Lassen Volcanic', 'MACA': 'Mammoth Cave', 'MEVE': 'Mesa Verde', 'MORA': 'Mount Rainier',
  'NERI': 'New River Gorge', 'NOCA': 'North Cascades', 'NPSA': 'American Samoa', 'OLYM': 'Olympic',
  'PEFO': 'Petrified Forest', 'PINN': 'Pinnacles', 'REDW': 'Redwood', 'ROMO': 'Rocky Mountain',
  'SAGU': 'Saguaro', 'SEQU': 'Sequoia', 'SHEN': 'Shenandoah', 'THRO': 'Theodore Roosevelt',
  'VIIS': 'Virgin Islands', 'VOYA': 'Voyageurs', 'WHSA': 'White Sands', 'WICA': 'Wind Cave',
  'WRST': 'Wrangell–St. Elias', 'YELL': 'Yellowstone', 'YOSE': 'Yosemite', 'ZION': 'Zion',
}
BOUNDS = ('https://services1.arcgis.com/fBc8EJBxQRMcHlei/arcgis/rest/services/'
          'NPS_Land_Resources_Division_Boundary_and_Tract_Data_Service/FeatureServer/2/query')
POIS = ('https://mapservices.nps.gov/arcgis/rest/services/NationalDatasets/'
        'NPS_Public_POIs_Geographic/FeatureServer/0/query')
LINES = {'trails': ('https://mapservices.nps.gov/arcgis/rest/services/NationalDatasets/'
                     'NPS_Public_Trails_Geographic/FeatureServer/0/query', 'TRLNAME,TRLCLASS,TRLUSE,TRLSURFACE,SEASDESC'),
         'roads': ('https://mapservices.nps.gov/arcgis/rest/services/NationalDatasets/'
                   'NPS_Public_Roads_Geographic/FeatureServer/0/query', 'RDNAME,RDCLASS,RDSURFACE,RDONEWAY,RTENUMBER,SEASDESC')}
OVERPASS = ['https://maps.mail.ru/osm/tools/overpass/api/interpreter', 'https://overpass-api.de/api/interpreter',
            'https://overpass.kumi.systems/api/interpreter']
# NPS point types that only clutter a map at our scale.
NOISE = {'ATM', 'Bench', 'Bicycle Rack', 'Bike Rack', 'CNG', 'Campfire Ring', 'Campsite', 'Drinking Water',
         'Dump Station', 'Electric Vehicle Parking', 'Fee Booth', 'Fish Cleaning', 'Flush Toilet',
         'Food Box / Food Cache', 'Gate', 'Information Board', 'Location Sign', 'Mile Marker',
         'Navigation Aid', 'None', 'Parking Lot', 'Pen', 'Picnic Table', 'Place Sign', 'Potable Water',
         'Regulatory Sign', 'Restroom', 'Sanitary Disposal Station', 'Shed', 'Showers', 'Sign',
         'Telephone', 'Trail Marker', 'Trail Sign', 'Vault Toilet', 'Vehicle Charging', 'Webcam',
         'Wheelchair Accessible', 'Dumpster', 'Recycling', 'Trash', 'Water Access', 'Mooring',
         'Backcountry Campsite', 'Interpretive Sign', 'Gateway Sign', 'Shelter', 'Building'}


def get(url, data=None, tries=3, timeout=200, headers=None):
  for i in range(tries):
    try:
      req = urllib.request.Request(url, data=data, headers=dict({'User-Agent': UA}, **(headers or {})))
      with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode('utf-8', 'replace')
    except Exception as e:
      if i == tries - 1: raise
      print('  retry', url[:80], e, file=sys.stderr); time.sleep(5 * (i + 1))


def jget(url, **kw): return json.loads(get(url, **kw))
def path(*p): return os.path.join(OUT, *p)
def save(obj, *p):
  os.makedirs(os.path.dirname(path(*p)), exist_ok=True)
  with open(path(*p), 'w', encoding='utf-8') as f: json.dump(obj, f, ensure_ascii=False, indent=1)
def load(*p):
  try:
    with open(path(*p), encoding='utf-8') as f: return json.load(f)
  except FileNotFoundError: return None


def rings(geom):
  if not geom: return []
  if geom['type'] == 'Polygon': return geom['coordinates']
  return [r for poly in geom['coordinates'] for r in poly]


def inside(rs, lon, lat):  # even-odd over every ring (holes too)
  c = False
  for r in rs:
    j = len(r) - 1
    for i in range(len(r)):
      xi, yi = r[i][0], r[i][1]; xj, yj = r[j][0], r[j][1]
      if (yi > lat) != (yj > lat) and lon < (xj - xi) * (lat - yi) / ((yj - yi) or 1e-12) + xi: c = not c
      j = i
  return c


def step_bounds(codes):
  feats = []
  for code in codes:  # one by one: the Alaskan parks are huge
    q = urllib.parse.urlencode({'where': "UNIT_CODE='%s'" % code, 'outFields': 'UNIT_CODE,UNIT_NAME,STATE,REGION',
                                'returnGeometry': 'true', 'outSR': 4326, 'maxAllowableOffset': 0.001, 'f': 'geojson'})
    fc = jget(BOUNDS + '?' + q)
    for f in fc['features']:
      xs = [p[0] for r in rings(f['geometry']) for p in r]; ys = [p[1] for r in rings(f['geometry']) for p in r]
      f['properties']['bbox'] = [round(min(xs), 4), round(min(ys), 4), round(max(xs), 4), round(max(ys), 4)]
      feats.append(f)
    print('bounds', code, len(fc['features']))
  old = load('bounds.geojson') or {'features': []}
  keep = [f for f in old['features'] if f['properties']['UNIT_CODE'] not in codes]
  save({'type': 'FeatureCollection', 'features': keep + feats}, 'bounds.geojson')


def bound(code):
  fc = load('bounds.geojson') or {'features': []}
  fs = [f for f in fc['features'] if f['properties']['UNIT_CODE'] == code]
  if not fs: return None, []
  rs = [r for f in fs for r in rings(f['geometry'])]
  b = [min(f['properties']['bbox'][0] for f in fs), min(f['properties']['bbox'][1] for f in fs),
       max(f['properties']['bbox'][2] for f in fs), max(f['properties']['bbox'][3] for f in fs)]
  return b, rs


def step_nps(codes):
  key = os.environ.get('NPS_API_KEY', 'DEMO_KEY')
  d = jget('https://developer.nps.gov/api/v1/parks?limit=500&api_key=' + key)
  out = {}
  for p in d['data']:
    c = p['parkCode'].upper()
    if c in PARKS:
      out[c] = {k: p.get(k) for k in ('fullName', 'designation', 'states', 'latitude', 'longitude', 'url',
                                      'description', 'weatherInfo', 'directionsInfo')}
      out[c]['activities'] = [a['name'] for a in p.get('activities', [])]
      out[c]['topics'] = [a['name'] for a in p.get('topics', [])]
  save(out, 'nps.json'); print('nps', len(out))


def step_wiki(codes):
  w = jget('https://en.wikipedia.org/w/api.php?action=parse&page=List_of_national_parks_of_the_United_States'
           '&prop=wikitext&format=json')['parse']['wikitext']['*']
  out = {}
  for row in w.split('\n|-')[1:]:
    m = re.search(r'!scope="row"[^|\n]*\|\s*\[\[([^|\]]+)(?:\|([^\]]+))?\]\]', row)  # (UNESCO rows carry a style)
    if not m: continue
    name = html.unescape(m.group(2) or m.group(1)).replace('\xa0', ' ')
    coord = re.search(r'\{\{coord\|(-?[\d.]+)\|(-?[\d.]+)', row)
    est = re.search(r'\{\{dts\|([^|}]+)', row)
    acres = re.search(r'\{\{convert\|([\d,.]+)\|acre', row)
    vis = re.search(r'\n\|\s*([\d,]{4,})\s*\n', row)
    desc = row.split('\n|')[-1]
    desc = re.sub(r'<ref[^>]*/>|<ref.*?</ref>', '', desc, flags=re.S)
    desc = re.sub(r'\[\[(?:[^|\]]*\|)?([^\]]+)\]\]', r'\1', desc); desc = re.sub(r"'{2,}", '', desc).strip()
    a = float(acres.group(1).replace(',', '')) if acres else None
    out[name] = {'established': est and est.group(1).strip(), 'acres': a, 'km2': a and round(a * 0.00404686, 1),
                 'visitors2025': vis and int(vis.group(1).replace(',', '')),
                 'coord': coord and [float(coord.group(1)), float(coord.group(2))], 'description': desc}
  save(out, 'wiki.json'); print('wiki', len(out))


def step_maps(codes):
  for code in codes:
    links, seen = [], set()
    for page in ('maps.htm', 'brochures.htm'):
      url = 'https://www.nps.gov/%s/planyourvisit/%s' % (code.lower(), page)
      try: s = get(url, tries=2, timeout=60)
      except Exception as e: print('  maps', code, page, e); continue
      for m in re.finditer(r'<a\b[^>]*href="([^"]+\.(?:pdf|jpe?g|png|gif))"[^>]*>(.*?)</a>', s, re.S | re.I):
        href = urllib.parse.urljoin(url, html.unescape(m.group(1)))
        text = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', m.group(2)))).strip()
        if href not in seen: seen.add(href); links.append({'text': text[:120], 'url': href, 'page': page})
      if links and page == 'maps.htm': break
    save(links, code, 'maps.json'); print('maps', code, len(links))


ALIAS = {'SEQU': 'SEKI', 'KICA': 'SEKI'}  # (one unit in the NPS's national datasets)


NPG = 'https://www.nps.gov/npgallery/api/'


def step_hfc(codes):  # the park's official maps in the NPS map catalogue, with their PDFs
  tpl = jget(NPG + 'archivesearch/load/305fb7af-a71b-469b-941e-a98b439c882f')['searchTemplate']
  for code in codes:
    st = dict(tpl); st.pop('operand', None); st['pageSize'] = 100
    st['Operand'] = {'LeftOperand': {'Term': 'RelatedCollection', 'Attribute': 'HFC Cartography', 'MatchType': 'matchText'},
                     'RightOperand': {'Term': 'unitcode', 'Attribute': ALIAS.get(code, code), 'MatchType': 'containsText'},
                     'Operator': 'AND'}
    r = json.loads(get(NPG + 'search/execute', data=json.dumps(st).encode(), tries=2, timeout=120,
                       headers={'Content-Type': 'application/json'}))
    out = []
    for x in r.get('Results') or []:
      a = x.get('Asset') or {}; dl = {d.get('Label'): d.get('Url') for d in a.get('Downloads') or []}
      out.append({'title': a.get('Title'), 'file': a.get('OriginalFileName'), 'date': (a.get('ImageCreateDate') or {}).get('Text'),
                  'pdf': dl.get('PDF version'), 'jpg': dl.get('JPG version') or dl.get('Original Size')})
    save(out, code, 'hfc.json'); print('hfc', code, len(out))


def step_pois(codes):
  for code in codes:
    feats, off = [], 0
    rs = bound(code)[1] if code in ALIAS else None
    while True:
      q = urllib.parse.urlencode({'where': "UNITCODE='%s'" % ALIAS.get(code, code), 'outFields': 'POINAME,MAPLABEL,POITYPE,SEASONAL,SEASDESC',
                                  'returnGeometry': 'true', 'outSR': 4326, 'f': 'json', 'resultOffset': off,
                                  'resultRecordCount': 2000})
      d = jget(POIS + '?' + q)
      fs = d.get('features', []); feats += fs; off += len(fs)
      if not d.get('exceededTransferLimit') or not fs: break
    out, seen = [], set()
    for f in feats:
      a, g = f['attributes'], f.get('geometry') or {}
      t, n = str(a.get('POITYPE')), (a.get('POINAME') or a.get('MAPLABEL') or '').strip()
      if t in NOISE or 'x' not in g or not n or n == t: continue
      if rs and not inside(rs, g['x'], g['y']): continue
      k = (n, t, round(g['y'], 3), round(g['x'], 3))
      if k in seen: continue
      seen.add(k); out.append({'name': n, 'type': t, 'lat': round(g['y'], 5), 'lon': round(g['x'], 5),
                               'seasonal': a.get('SEASDESC') or None})
    out.sort(key=lambda p: (p['type'], p['name']))
    save(out, code, 'pois.json'); print('pois', code, len(feats), '->', len(out))


OSM_Q = '''[out:json][timeout:180];
(node["name"]["natural"~"^(peak|volcano|arch|spring|hot_spring|geyser|fumarole|cave_entrance|waterfall|cliff|rock|stone|saddle|valley|glacier|beach|cape|bay|island|islet|dune|sinkhole|ridge|hill|mountain_range|strait|reef|tree)$"]({b});
 node["name"]["waterway"="waterfall"]({b}); node["name"]["geological"]({b});
 way["name"]["natural"~"^(water|glacier|beach|dune|arch|cliff|ridge|valley|bay|cape|wetland|sand|bare_rock|reef|strait|isthmus|peninsula)$"]({b});
 relation["name"]["natural"~"^(water|glacier|bay|wetland|valley|ridge|mountain_range|peninsula)$"]({b});
 way["name"]["waterway"~"^(river|canal)$"]({b}); relation["name"]["waterway"="river"]({b});
 node["name"]["place"~"^(island|islet|locality)$"]({b}); way["name"]["place"~"^(island|islet)$"]({b});
 relation["name"]["place"~"^(island|archipelago)$"]({b});
{roads});
out tags center qt;'''
ROADS = '''
 way["name"]["highway"~"^(primary|secondary|tertiary|unclassified)$"]({b});
 way["name"]["highway"~"^(path|footway|track)$"]["name"~"Trail|Loop|Path|Route|Walk|Boardwalk|Nature"]({b});'''
# (the huge parks — Alaska, Death Valley — skip named lake outlines, roads & trails: the servers time out)
BIG_BOX = 2.0
MIRROR = None


def kind(t):
  for k in ('natural', 'waterway', 'geological', 'place', 'highway'):
    if t.get(k): return t[k] if k != 'highway' else ('trail' if t[k] in ('path', 'footway', 'track') else 'road')
  return '?'


def step_osm(codes):
  for n, code in enumerate(codes):
    b, rs = bound(code)
    if not b: print('osm', code, 'no bounds'); continue
    big = (b[2] - b[0]) * (b[3] - b[1]) > BIG_BOX
    q = OSM_Q.replace('{roads}', '')  # (roads & trails: the NPS's own, step `lines`; ROADS if ever needed)
    if big: q = q.replace(' way["name"]["natural"~"^(water|', ' way["name"]["natural"~"^(')
    q = q.replace('{b}', '%.4f,%.4f,%.4f,%.4f' % (b[1], b[0], b[3], b[2]))
    d = None
    for url in ([OVERPASS[MIRROR]] if MIRROR is not None else OVERPASS):
      try:
        s = get(url, data=urllib.parse.urlencode({'data': q}).encode(), tries=1, timeout=200)
        if s.lstrip().startswith('{'): d = json.loads(s); break
        print('  overpass', url, s[:200].replace('\n', ' '))
      except Exception as e: print('  overpass', url, e)
      time.sleep(10)
    if d is None: print('osm', code, 'FAILED'); continue
    by = {}
    for e in d['elements']:
      t = e.get('tags', {}); c = e.get('center', e)
      if 'lat' not in c or not inside(rs, c['lon'], c['lat']): continue
      k = kind(t); key = (t['name'], k)
      it = by.setdefault(key, {'name': t['name'], 'kind': k, 'lat': round(c['lat'], 4), 'lon': round(c['lon'], 4),
                               'ele': t.get('ele'), 'pts': 0, 'box': [c['lon'], c['lat'], c['lon'], c['lat']]})
      it['pts'] += 1; bx = it['box']
      it['box'] = [min(bx[0], c['lon']), min(bx[1], c['lat']), max(bx[2], c['lon']), max(bx[3], c['lat'])]
    out = []
    for it in by.values():
      if it['pts'] > 1: it['span'] = [round(v, 3) for v in it['box']]
      del it['box']
      if it['pts'] == 1: del it['pts']
      out.append(it)
    out.sort(key=lambda i: (i['kind'], -float(re.sub(r'[^\d.]', '', str(i.get('ele') or 0)) or 0), i['name']))
    save(out, code, 'osm.json'); print('osm', code, len(d['elements']), '->', len(out), '(%d/%d)' % (n + 1, len(codes)))
    time.sleep(3)


def line_km(g):  # a (multi)line's length, equirectangular
  parts = g['coordinates'] if g['type'] == 'MultiLineString' else [g['coordinates']]
  d = 0
  for pts in parts:
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
      d += math.hypot((x1 - x0) * 111.32 * math.cos(math.radians((y0 + y1) / 2)), (y1 - y0) * 110.57)
  return d


def first_pt(g):
  c = g['coordinates']
  return c[0] if g['type'] == 'LineString' else c[0][0]


def step_lines(codes):  # the NPS's own trails & roads (public domain), simplified to ~20 m
  for code in codes:
    feats = []
    rs = bound(code)[1] if code in ALIAS else None
    for kind, (url, fields) in LINES.items():
      off = 0
      while True:
        q = urllib.parse.urlencode({'where': "UNITCODE='%s'" % ALIAS.get(code, code), 'outFields': fields, 'returnGeometry': 'true',
                                    'outSR': 4326, 'maxAllowableOffset': 0.0002, 'geometryPrecision': 5,
                                    'f': 'geojson', 'resultOffset': off, 'resultRecordCount': 1000})
        fc = jget(url + '?' + q)
        fs = [f for f in fc.get('features', []) if f.get('geometry')]
        if rs: fs = [f for f in fs if inside(rs, *first_pt(f['geometry']))]
        for f in fs: f['properties']['kind'] = kind
        feats += fs; off += len(fc.get('features', []))
        more = fc.get('exceededTransferLimit') or (fc.get('properties') or {}).get('exceededTransferLimit')
        if not more or not fc.get('features'): break
    save({'type': 'FeatureCollection', 'features': feats}, code, 'lines.geojson')
    print('lines', code, len(feats))


def lines_summary(code):
  fc = load(code, 'lines.geojson')
  if not fc: return None
  by = {}
  for f in fc['features']:
    p = f['properties']; k = p['kind']
    n = (p.get('TRLNAME') or p.get('RDNAME') or '').strip() or '(unnamed)'
    it = by.setdefault((k, n), {'km': 0, 'tags': set(), 'at': None})
    it['km'] += line_km(f['geometry'])
    for t in (p.get('TRLCLASS'), p.get('TRLUSE'), p.get('TRLSURFACE'), p.get('RDCLASS'), p.get('RDSURFACE'),
              'one-way' if p.get('RDONEWAY') in ('Yes', 'Y', 'One-Way', 'One Way') else None, p.get('RTENUMBER'), p.get('SEASDESC')):
      if t and str(t) not in ('Unknown', 'None', 'No', 'N'): it['tags'].add(str(t)[:40])
    if not it['at']:
      c = f['geometry']['coordinates']; c = c[0] if f['geometry']['type'] == 'LineString' else c[0][0]
      it['at'] = (c[1], c[0])
  return by


def plain(s):  # a name without accents, ʻokina or dash variants, for matching
  import unicodedata
  s = unicodedata.normalize('NFKD', s.replace('ʻ', '').replace('–', '-').replace('—', '-'))
  return ''.join(ch for ch in s if not unicodedata.combining(ch)).lower().strip()


def km(b):
  lat = (b[1] + b[3]) / 2
  return round((b[2] - b[0]) * 111.32 * math.cos(math.radians(lat))), round((b[3] - b[1]) * 110.57)


def step_pack(codes):
  nps, wiki = load('nps.json') or {}, load('wiki.json') or {}
  for code in codes:
    b, _ = bound(code); p = nps.get(code, {}); name = PARKS[code]
    w = wiki.get(name) or next((v for k, v in wiki.items() if plain(k) == plain(name)), {})
    L = ['# %s (%s) — data pack' % (p.get('fullName') or name, code), '']
    if b: L += ['- bbox (W,S,E,N): %s — about %d × %d km' % (b, *km(b))]
    L += ['- centre (NPS): %s, %s · states: %s' % (p.get('latitude'), p.get('longitude'), p.get('states')),
          '- established %s · %s acres (%s km²) · %s recreation visits in 2025' % (
            w.get('established'), w.get('acres'), w.get('km2'), w.get('visitors2025')),
          '- NPS page: %s' % p.get('url'), '', '## NPS description', '', p.get('description') or '', '',
          '## Weather (NPS)', '', p.get('weatherInfo') or '', '', '## Wikipedia summary', '', w.get('description') or '',
          '', '## Activities (NPS)', '', ', '.join(p.get('activities') or []), '', '## Official maps (links)', '']
    for m in load(code, 'maps.json') or []: L.append('- %s — %s' % (m['text'] or '(no text)', m['url']))
    hfc = load(code, 'hfc.json') or []
    if hfc:
      L += ['', '## The NPS map catalogue (NPGallery « HFC Cartography »)', '']
      L += ['- %s (%s, %s) — %s' % (m['title'], m.get('file') or '?', m.get('date') or '?', m.get('pdf') or m.get('jpg') or '—') for m in hfc]
    L += ['', '## NPS points of interest (name — lat, lon)', '']
    pois = load(code, 'pois.json') or []
    types = {}
    for q in pois: types.setdefault(q['type'], []).append(q)
    for t in sorted(types, key=lambda t: -len(types[t])):
      L.append('- **%s** (%d): %s' % (t, len(types[t]), '; '.join('%s %.4f,%.4f' % (q['name'], q['lat'], q['lon'])
                                                                  for q in types[t][:60])))
    by = lines_summary(code)
    if by:
      for kind in ('roads', 'trails'):
        rows = sorted(((n, v) for (k, n), v in by.items() if k == kind), key=lambda r: -r[1]['km'])
        L += ['', '## NPS %s (name — km inside the data, tags, a start point)' % kind, '']
        L += ['- %s — %.1f km%s%s' % (n, v['km'], ' · ' + ', '.join(sorted(v['tags'])) if v['tags'] else '',
                                     ' · from %.4f,%.4f' % v['at'] if v['at'] else '') for n, v in rows[:90]]
    L += ['', '## OpenStreetMap named features inside the boundary (name — lat, lon, ele m; span = extent)', '']
    osm = load(code, 'osm.json')
    if osm is None: L.append('(not fetched yet)')
    kinds = {}
    for o in osm or []: kinds.setdefault(o['kind'], []).append(o)
    for k in sorted(kinds, key=lambda k: -len(kinds[k])):
      items = kinds[k][:80]
      L.append('- **%s** (%d): %s' % (k, len(kinds[k]), '; '.join(
        '%s %.4f,%.4f%s%s' % (o['name'], o['lat'], o['lon'], ' %sm' % o['ele'] if o.get('ele') else '',
                              ' span%s' % o['span'] if o.get('span') else '') for o in items)))
    with open(path(code, 'pack.md'), 'w', encoding='utf-8') as f: f.write('\n'.join(L) + '\n')
    print('pack', code)


def step_refs(codes):  # the reference photos of docs/parks/refs/<CODE>.json, for modelling — local only
  for code in codes:
    lst = os.path.join(ROOT, 'docs', 'parks', 'refs', code + '.json')
    if not os.path.exists(lst): continue
    with open(lst, encoding='utf-8') as f: refs = json.load(f)
    os.makedirs(path(code, 'refs'), exist_ok=True)
    rows, n = ['# %s — reference views (never commit or ship these images)' % code, ''], 0
    for i, r in enumerate(refs, 1):
      ext = os.path.splitext(urllib.parse.urlparse(r['image']).path)[1].lower()
      name = '%02d-%s%s' % (i, r['id'], ext if ext in ('.jpg', '.jpeg', '.png', '.webp') else '.jpg')
      out = path(code, 'refs', name)
      if not os.path.exists(out):
        try:
          req = urllib.request.Request(r['image'], headers={'User-Agent': UA})
          with urllib.request.urlopen(req, timeout=120) as resp, open(out, 'wb') as f: f.write(resp.read())
          n += 1; time.sleep(1)
        except Exception as e: print('  refs', code, r['id'], e); continue
      rows.append('- `%s` — **%s** (%s, %s, facing %s): %s' % (name, r['view'], r['where'],
                                                            '%.4f,%.4f' % (r['lat'], r['lon']), r['facing'], r['match']))
    with open(path(code, 'refs', 'index.md'), 'w', encoding='utf-8') as f: f.write('\n'.join(rows) + '\n')
    print('refs', code, len(refs), 'listed,', n, 'downloaded')


STEPS = ['bounds', 'nps', 'wiki', 'maps', 'hfc', 'pois', 'lines', 'osm', 'pack']  # (refs: on demand)

if __name__ == '__main__':
  args = sys.argv[1:]
  only = order = None
  if '--only' in args: i = args.index('--only'); only = args[i + 1].upper().split(','); del args[i:i + 2]
  if '--order' in args: i = args.index('--order'); order = args[i + 1].upper().split(','); del args[i:i + 2]
  if '--mirror' in args: i = args.index('--mirror'); MIRROR = int(args[i + 1]); del args[i:i + 2]  # (one Overpass server only)
  codes = order or only or sorted(PARKS)
  for s in args or STEPS:
    globals()['step_' + s](codes)
