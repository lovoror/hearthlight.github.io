#!/usr/bin/env python3
"""The parks atlas: docs/parks/parks.json and the tables of docs/parks/README.md.

  python3 tools/parks/atlas.py            (--check: each dossier against the template)

Reads each park's meta (tools/parks/cache/<CODE>/meta.json, written with its dossier), the
boundaries (bounds.geojson) and the NPS regions, applies the atlas's decisions below (the trip,
the final tier), writes docs/parks/parks.json and rewrites the README's generated tables (between
its `<!-- atlas:… -->` markers, each present exactly once). Standard library only.
"""
import json, math, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
CACHE = os.path.join(HERE, 'cache')
DOCS = os.path.join(ROOT, 'docs', 'parks')

# The road trip's legs (docs/plans/parks-v10.md §6.3), in the order they are shown.
TRIPS = [
  ('Grand Circle', 'the Colorado Plateau: canyons, arches, hoodoos, cliff dwellings',
   ['ZION', 'BRCA', 'CARE', 'CANY', 'ARCH', 'MEVE', 'BLCA', 'GRCA', 'PEFO']),
  ('Desert Southwest', 'deserts, dunes, caves and the Rio Grande',
   ['JOTR', 'DEVA', 'SAGU', 'GRBA', 'WHSA', 'CAVE', 'GUMO', 'BIBE']),
  ('Rocky Road', 'geysers, peaks, glaciers and the high dunes',
   ['YELL', 'GRTE', 'GLAC', 'ROMO', 'GRSA']),
  ('Pacific Crest', 'volcanoes, giant trees, rainforest and the Pacific coast',
   ['OLYM', 'MORA', 'NOCA', 'CRLA', 'LAVO', 'REDW', 'YOSE', 'SEQU', 'KICA', 'PINN', 'CHIS']),
  ('Alaska Frontier', 'wilderness by bus, boat and bush plane',
   ['DENA', 'KATM', 'GLBA', 'KEFJ', 'WRST', 'LACL', 'GAAR', 'KOVA']),
  ('Great Plains', 'badlands, prairie and the Little Missouri',
   ['BADL', 'WICA', 'THRO']),
  ('Lakes & Rivers', 'the Great Lakes, the Mississippi, springs and caves',
   ['VOYA', 'ISRO', 'INDU', 'CUVA', 'JEFF', 'HOSP', 'MACA']),
  ('Appalachians & the East', 'old mountains, the Atlantic coast and a floodplain forest',
   ['ACAD', 'SHEN', 'GRSM', 'NERI', 'CONG']),
  ('Islands', 'the Florida keys, the Caribbean and the Pacific islands',
   ['EVER', 'BISC', 'DRTO', 'VIIS', 'HAVO', 'HALE', 'NPSA']),
]
TRIP_OF = {c: t for t, _, cs in TRIPS for c in cs}
# The first wave (tier 1, the first release): one of each great landscape, the pilot first — the
# README's « Tiers » says why. A dossier that suggested tier 1 and isn't in it opens tier 2.
FIRST_WAVE = ['ZION', 'ACAD', 'YELL', 'YOSE', 'GRCA', 'GRSM', 'ARCH', 'GRTE', 'OLYM', 'HAVO']
TIERS = {}  # (any other tier the atlas sets over a dossier's suggestion)
REGIONS = {'AKR': 'Alaska', 'IMR': 'Intermountain', 'MWR': 'Midwest', 'NER': 'Northeast',
           'PWR': 'Pacific West', 'SER': 'Southeast', 'NCR': 'National Capital'}


HEADINGS = ['## Official visitor maps', '## Reading the map', '### Districts & areas', '### Roads & entrances',
            '### Places (with coordinates)', '### Signature trails & routes', '### Water', '### Relief', '### Sketch',
            '## Look & feel', '## Moments', '## For the game', '## Sources']


def check(code):  # a dossier against the template: its headings in order, enough places, a sketch
  path = os.path.join(DOCS, code.lower() + '.md')
  if not os.path.exists(path): return ['no dossier']
  s = open(path, encoding='utf-8').read(); out = []
  if not s.startswith('# ') or '`%s`' % code not in s.split('\n', 1)[0]: out.append('title line')
  heads = [l.strip() for l in s.split('\n') if l.startswith('#')]
  at = -1
  for h in HEADINGS:
    if h not in heads: out.append('missing ' + h); continue
    if heads.index(h) < at: out.append('out of order ' + h)
    at = heads.index(h)
  places = s.split('### Places (with coordinates)')[-1].split('\n### ')[0]
  n = len(re.findall(r'^\|[^|]+\|[^|]+\|[^|\d-]{0,12}-?\d+\.\d{2,}', places, re.M))
  rows = len(re.findall(r'^\|', places, re.M)) - 2
  if n < 12 and rows < 15: out.append('only %d places with coordinates (%d rows)' % (n, rows))
  if '```' not in s: out.append('no sketch')
  if not os.path.exists(os.path.join(CACHE, code, 'meta.json')): out.append('no meta.json')
  return out


def load(*p):
  try:
    with open(os.path.join(*p), encoding='utf-8') as f: return json.load(f)
  except FileNotFoundError: return None


def main():
  bounds = load(CACHE, 'bounds.geojson') or {'features': []}
  reg, bbox = {}, {}
  for f in bounds['features']:
    p = f['properties']; c = p['UNIT_CODE']; reg[c] = REGIONS.get(p.get('REGION'), p.get('REGION'))
    b = p['bbox']; o = bbox.get(c)
    bbox[c] = b if not o else [min(o[0], b[0]), min(o[1], b[1]), max(o[2], b[2]), max(o[3], b[3])]
  parks, missing = [], []
  for code in sorted(TRIP_OF):
    m = load(CACHE, code, 'meta.json')
    if not m: missing.append(code); continue
    m['code'] = code
    m['tier'] = TIERS.get(code) or (1 if code in FIRST_WAVE else max(2, m.get('tier_suggested') or 2))
    m['trip'] = TRIP_OF[code]
    m['region'] = reg.get(code)
    if code in bbox:
      b = bbox[code]; m['bbox'] = b
      m['centre'] = [round((b[1] + b[3]) / 2, 4), round((b[0] + b[2]) / 2, 4)]
      lat = (b[1] + b[3]) / 2
      m['extent_km'] = [round((b[2] - b[0]) * 111.32 * math.cos(math.radians(lat))), round((b[3] - b[1]) * 110.57)]
    m['dossier'] = 'docs/parks/%s.md' % code.lower()
    m['has_dossier'] = os.path.exists(os.path.join(DOCS, code.lower() + '.md'))
    parks.append(m)
  with open(os.path.join(DOCS, 'parks.json'), 'w', encoding='utf-8') as f:
    json.dump({'about': 'The 63 US national parks for the National Park mode — see docs/parks/README.md',
               'parks': parks}, f, ensure_ascii=False, indent=1)
  by = {p['code']: p for p in parks}

  def cell(s): return str(s).replace('|', '/').replace('\n', ' ')
  def num(n): return '{:,}'.format(n) if isinstance(n, (int, float)) else '—'
  rows = ['| Park | State | Est. | km² | Visits 2025 | Tier | Landscapes | Signature places | Map (tiles) |',
          '|---|---|---|---:|---:|:---:|---|---|---|']
  trips = []
  for trip, about, codes in TRIPS:
    done = [c for c in codes if c in by]
    rows.append('| **%s** — *%s* | | | | | | | | |' % (trip, about))
    for c in done:
      p = by[c]
      name = '[%s](%s.md) `%s`' % (p.get('short') or p.get('name'), c.lower(), c)
      rows.append('| %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (
        name, ' '.join(p.get('states') or []), (p.get('established') or '')[:4],
        num(round(p['area_km2'])) if p.get('area_km2') else '—', num(p.get('visitors_2025')), p.get('tier') or '—',
        cell(', '.join((p.get('biomes') or [])[:3])), cell(', '.join((p.get('signature') or [])[:4])),
        '×'.join(str(v) for v in p.get('game_tiles') or []) or '—'))
    trips.append('- **%s** (%d): %s' % (trip, len(codes), ', '.join(
      '[%s](%s.md)' % (by[c].get('short') or c, c.lower()) if c in by else c for c in codes)))
  tier_lines = []
  for t in (1, 2, 3):
    cs = [p for p in parks if p.get('tier') == t]
    if t == 1: cs.sort(key=lambda p: FIRST_WAVE.index(p['code']))
    tier_lines.append('- **Tier %d** (%d): %s' % (t, len(cs), ', '.join(
      '[%s](%s.md)' % (p.get('short') or p['code'], p['code'].lower()) for p in cs)))
  stats = [
    '- %d parks; %s km² in all; %s recreation visits in 2025.' % (
      len(parks), num(round(sum(p.get('area_km2') or 0 for p in parks))),
      num(sum(p.get('visitors_2025') or 0 for p in parks))),
    '- Busiest: %s. Quietest: %s.' % (
      ', '.join('%s (%s)' % (p.get('short'), num(p.get('visitors_2025'))) for p in sorted(parks, key=lambda p: -(p.get('visitors_2025') or 0))[:3]),
      ', '.join('%s (%s)' % (p.get('short'), num(p.get('visitors_2025'))) for p in sorted(parks, key=lambda p: (p.get('visitors_2025') or 1e12))[:3])),
    '- Largest: %s. Smallest: %s.' % (
      ', '.join('%s (%s km²)' % (p.get('short'), num(round(p.get('area_km2') or 0))) for p in sorted(parks, key=lambda p: -(p.get('area_km2') or 0))[:3]),
      ', '.join('%s (%s km²)' % (p.get('short'), num(round(p.get('area_km2') or 0, 1))) for p in sorted(parks, key=lambda p: (p.get('area_km2') or 1e12))[:3])),
  ]
  blocks = {'table': rows, 'trips': trips, 'tiers': tier_lines, 'stats': stats}
  path = os.path.join(DOCS, 'README.md')
  s = open(path, encoding='utf-8').read()
  for k, lines in blocks.items():
    a, b = '<!-- atlas:%s -->' % k, '<!-- /atlas:%s -->' % k
    assert s.count(a) == 1 and s.count(b) == 1, 'marker %s must appear once' % k
    i, j = s.index(a) + len(a), s.index(b)
    s = s[:i] + '\n' + '\n'.join(lines) + '\n' + s[j:]
  with open(path, 'w', encoding='utf-8') as f: f.write(s)
  print('atlas: %d parks, %d without meta%s' % (len(parks), len(missing), (': ' + ' '.join(missing)) if missing else ''))


if __name__ == '__main__':
  if '--check' in sys.argv:
    bad = 0
    for code in sorted(TRIP_OF):
      issues = check(code)
      if issues: bad += 1; print('%s: %s' % (code, '; '.join(issues)))
    print('check: %d of %d dossiers need a look' % (bad, len(TRIP_OF)))
  else: main()
