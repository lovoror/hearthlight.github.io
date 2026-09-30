// Hand-made proportional bitmap font ("Cove 7") rendered from a glyph atlas.
// Cap height 7px, x-height 5px, 2px descenders. Supports inline color tags:
//   "Bring me {gold}3 berries{/} please"   (named colors or {#rrggbb})

import { COLORS } from '../art/palette.js';

const G = {
  'A': ['.##.', '#..#', '#..#', '####', '#..#', '#..#', '#..#'],
  'B': ['###.', '#..#', '#..#', '###.', '#..#', '#..#', '###.'],
  'C': ['.##.', '#..#', '#...', '#...', '#...', '#..#', '.##.'],
  'D': ['###.', '#..#', '#..#', '#..#', '#..#', '#..#', '###.'],
  'E': ['####', '#...', '#...', '###.', '#...', '#...', '####'],
  'F': ['####', '#...', '#...', '###.', '#...', '#...', '#...'],
  'G': ['.##.', '#..#', '#...', '#.##', '#..#', '#..#', '.###'],
  'H': ['#..#', '#..#', '#..#', '####', '#..#', '#..#', '#..#'],
  'I': ['###', '.#.', '.#.', '.#.', '.#.', '.#.', '###'],
  'J': ['..##', '...#', '...#', '...#', '#..#', '#..#', '.##.'],
  'K': ['#..#', '#..#', '#.#.', '##..', '#.#.', '#..#', '#..#'],
  'L': ['#...', '#...', '#...', '#...', '#...', '#...', '####'],
  'M': ['#...#', '##.##', '#.#.#', '#.#.#', '#...#', '#...#', '#...#'],
  'N': ['#..#', '##.#', '##.#', '#.##', '#.##', '#..#', '#..#'],
  'O': ['.##.', '#..#', '#..#', '#..#', '#..#', '#..#', '.##.'],
  'P': ['###.', '#..#', '#..#', '###.', '#...', '#...', '#...'],
  'Q': ['.##.', '#..#', '#..#', '#..#', '#..#', '#.#.', '.#.#'],
  'R': ['###.', '#..#', '#..#', '###.', '#.#.', '#..#', '#..#'],
  'S': ['.##.', '#..#', '#...', '.##.', '...#', '#..#', '.##.'],
  'T': ['#####', '..#..', '..#..', '..#..', '..#..', '..#..', '..#..'],
  'U': ['#..#', '#..#', '#..#', '#..#', '#..#', '#..#', '.##.'],
  'V': ['#...#', '#...#', '#...#', '#...#', '.#.#.', '.#.#.', '..#..'],
  'W': ['#...#', '#...#', '#...#', '#.#.#', '#.#.#', '##.##', '#...#'],
  'X': ['#...#', '#...#', '.#.#.', '..#..', '.#.#.', '#...#', '#...#'],
  'Y': ['#...#', '#...#', '.#.#.', '..#..', '..#..', '..#..', '..#..'],
  'Z': ['####', '...#', '..#.', '.#..', '#...', '#...', '####'],

  'a': ['....', '....', '.###', '#..#', '#..#', '#..#', '.###'],
  'b': ['#...', '#...', '###.', '#..#', '#..#', '#..#', '###.'],
  'c': ['...', '...', '.##', '#..', '#..', '#..', '.##'],
  'd': ['...#', '...#', '.###', '#..#', '#..#', '#..#', '.###'],
  'e': ['....', '....', '.##.', '#..#', '####', '#...', '.###'],
  'f': ['.##', '#..', '###', '#..', '#..', '#..', '#..'],
  'g': ['....', '....', '.###', '#..#', '#..#', '#..#', '.###', '...#', '.##.'],
  'h': ['#...', '#...', '###.', '#..#', '#..#', '#..#', '#..#'],
  'i': ['#', '.', '#', '#', '#', '#', '#'],
  'j': ['..#', '...', '..#', '..#', '..#', '..#', '..#', '#.#', '.#.'],
  'k': ['#...', '#...', '#..#', '#.#.', '##..', '#.#.', '#..#'],
  'l': ['#.', '#.', '#.', '#.', '#.', '#.', '.#'],
  'm': ['.....', '.....', '####.', '#.#.#', '#.#.#', '#.#.#', '#.#.#'],
  'n': ['....', '....', '###.', '#..#', '#..#', '#..#', '#..#'],
  'o': ['....', '....', '.##.', '#..#', '#..#', '#..#', '.##.'],
  'p': ['....', '....', '###.', '#..#', '#..#', '#..#', '###.', '#...', '#...'],
  'q': ['....', '....', '.###', '#..#', '#..#', '#..#', '.###', '...#', '...#'],
  'r': ['...', '...', '#.#', '##.', '#..', '#..', '#..'],
  's': ['....', '....', '.###', '#...', '.##.', '...#', '###.'],
  't': ['.#.', '.#.', '###', '.#.', '.#.', '.#.', '..#'],
  'u': ['....', '....', '#..#', '#..#', '#..#', '#..#', '.###'],
  'v': ['.....', '.....', '#...#', '#...#', '.#.#.', '.#.#.', '..#..'],
  'w': ['.....', '.....', '#...#', '#...#', '#.#.#', '#.#.#', '.#.#.'],
  'x': ['....', '....', '#..#', '#..#', '.##.', '#..#', '#..#'],
  'y': ['....', '....', '#..#', '#..#', '#..#', '#..#', '.###', '...#', '.##.'],
  'z': ['....', '....', '####', '...#', '.##.', '#...', '####'],

  '0': ['.##.', '#..#', '#.##', '#..#', '##.#', '#..#', '.##.'],
  '1': ['.#.', '##.', '.#.', '.#.', '.#.', '.#.', '###'],
  '2': ['.##.', '#..#', '...#', '..#.', '.#..', '#...', '####'],
  '3': ['###.', '...#', '...#', '.##.', '...#', '...#', '###.'],
  '4': ['#..#', '#..#', '#..#', '####', '...#', '...#', '...#'],
  '5': ['####', '#...', '#...', '###.', '...#', '...#', '###.'],
  '6': ['.##.', '#...', '#...', '###.', '#..#', '#..#', '.##.'],
  '7': ['####', '...#', '...#', '..#.', '.#..', '.#..', '.#..'],
  '8': ['.##.', '#..#', '#..#', '.##.', '#..#', '#..#', '.##.'],
  '9': ['.##.', '#..#', '#..#', '.###', '...#', '...#', '.##.'],

  ' ': ['...', '...', '...', '...', '...', '...', '...'],
  '.': ['.', '.', '.', '.', '.', '.', '#'],
  ',': ['..', '..', '..', '..', '..', '..', '.#', '#.'],
  '!': ['#', '#', '#', '#', '#', '.', '#'],
  '?': ['.##.', '#..#', '...#', '..#.', '.#..', '....', '.#..'],
  ':': ['.', '.', '#', '.', '.', '.', '#'],
  ';': ['..', '..', '.#', '..', '..', '..', '.#', '#.'],
  "'": ['#', '#', '.', '.', '.', '.', '.'],
  '"': ['#.#', '#.#', '...', '...', '...', '...', '...'],
  '-': ['...', '...', '...', '###', '...', '...', '...'],
  '+': ['...', '...', '.#.', '###', '.#.', '...', '...'],
  '=': ['...', '...', '###', '...', '###', '...', '...'],
  '(': ['.#', '#.', '#.', '#.', '#.', '#.', '.#'],
  ')': ['#.', '.#', '.#', '.#', '.#', '.#', '#.'],
  '[': ['##', '#.', '#.', '#.', '#.', '#.', '##'],
  ']': ['##', '.#', '.#', '.#', '.#', '.#', '##'],
  '/': ['...#', '...#', '..#.', '.##.', '.#..', '#...', '#...'],
  '\\': ['#...', '#...', '.#..', '.##.', '..#.', '...#', '...#'],
  '_': ['....', '....', '....', '....', '....', '....', '....', '####'],
  '*': ['...', '...', '#.#', '.#.', '#.#', '...', '...'],
  '#': ['.....', '.#.#.', '#####', '.#.#.', '#####', '.#.#.', '.....'],
  '%': ['#...#', '#..#.', '...#.', '..#..', '.#...', '.#..#', '#...#'],
  '&': ['.##..', '#..#.', '.##..', '.#.#.', '#..#.', '#...#', '.###.'],
  '<': ['...', '..#', '.#.', '#..', '.#.', '..#', '...'],
  '>': ['...', '#..', '.#.', '..#', '.#.', '#..', '...'],
  '~': ['....', '....', '....', '.#.#', '#.#.', '....', '....'],
  '^': ['.#.', '#.#', '...', '...', '...', '...', '...'],
  '@': ['.###.', '#...#', '#.###', '#.#.#', '#.###', '#....', '.###.'],
  '$': ['.#.', '###', '#..', '###', '..#', '###', '.#.'],
  // Special symbols (mapped from unicode)
  '♥': ['.....', '.....', '##.##', '#####', '#####', '.###.', '..#..'],
  '♡': ['.....', '.....', '##.##', '#.#.#', '#...#', '.#.#.', '..#..'],
  '★': ['..#..', '..#..', '#####', '.###.', '.###.', '##.##', '#...#'],
  '♪': ['..##', '..#.', '..#.', '..#.', '###.', '###.', '....'],
  '•': ['..', '..', '..', '##', '##', '..', '..'],
  '…': ['.....', '.....', '.....', '.....', '.....', '.....', '#.#.#'],
  '→': ['.....', '...#.', '....#', '#####', '....#', '...#.', '.....'],
  '←': ['.....', '.#...', '#....', '#####', '#....', '.#...', '.....'],
  '↑': ['..#..', '.###.', '#.#.#', '..#..', '..#..', '..#..', '.....'],
  '↓': ['.....', '..#..', '..#..', '..#..', '#.#.#', '.###.', '..#..'],
  '·': ['.', '.', '.', '#', '.', '.', '.'],
  '°': ['###', '#.#', '###', '...', '...', '...', '...'],
  '✓': ['.....', '....#', '...#.', '#.#..', '.#...', '.....', '.....'],
  '✕': ['.....', '#...#', '.#.#.', '..#..', '.#.#.', '#...#', '.....'],
  // (a PlayStation pad's buttons, a Nintendo's minus, and a little gamepad)
  '○': ['.....', '.###.', '#...#', '#...#', '#...#', '.###.', '.....'],
  '□': ['.....', '#####', '#...#', '#...#', '#...#', '#####', '.....'],
  '△': ['.....', '..#..', '..#..', '.#.#.', '.#.#.', '#####', '.....'],
  '−': ['...', '...', '...', '###', '...', '...', '...'],
  '⌫': ['..######', '.#.....#', '#..#.#.#', '#...#..#', '#..#.#.#', '.#.....#', '..######'],
  '⏸': ['##.##', '##.##', '##.##', '##.##', '##.##', '##.##', '##.##'],
  '🎲': ['#######', '#.....#', '#.#...#', '#..#..#', '#...#.#', '#.....#', '#######'],
  '🎮': ['.#######.', '#########', '##.###.##', '#...#.#.#', '##.###.##', '###...###', '##.....##'],
  '×': ['.....', '.....', '#...#', '.#.#.', '..#..', '.#.#.', '#...#'],
  '↖': ['####.', '##...', '#.#..', '#..#.', '....#', '.....', '.....'],
  '♛': ['.....', '#.#.#', '#.#.#', '#####', '#####', '#####', '.....'],
  '◂': ['...', '..#', '.##', '###', '.##', '..#', '...'],
  '▸': ['...', '#..', '##.', '###', '##.', '#..', '...'],
  '¢': ['.....', '..#..', '.###.', '#.#..', '#.#..', '.###.', '..#..'],
  // French (and friends): accents sit in the two rows above the x-height;
  // accented capitals trade one row of letter for the mark
  'é': ['...#', '..#.', '.##.', '#..#', '####', '#...', '.###'],
  'è': ['.#..', '..#.', '.##.', '#..#', '####', '#...', '.###'],
  'ê': ['.##.', '#..#', '.##.', '#..#', '####', '#...', '.###'],
  'ë': ['#..#', '....', '.##.', '#..#', '####', '#...', '.###'],
  'à': ['.#..', '..#.', '.###', '#..#', '#..#', '#..#', '.###'],
  'â': ['.##.', '#..#', '.###', '#..#', '#..#', '#..#', '.###'],
  'ä': ['#..#', '....', '.###', '#..#', '#..#', '#..#', '.###'],
  'î': ['.#.', '#.#', '...', '.#.', '.#.', '.#.', '.#.'],
  'ï': ['#.#', '...', '.#.', '.#.', '.#.', '.#.', '.#.'],
  'ô': ['.##.', '#..#', '.##.', '#..#', '#..#', '#..#', '.##.'],
  'ö': ['#..#', '....', '.##.', '#..#', '#..#', '#..#', '.##.'],
  'ù': ['.#..', '..#.', '#..#', '#..#', '#..#', '#..#', '.###'],
  'û': ['.##.', '....', '#..#', '#..#', '#..#', '#..#', '.###'],
  'ü': ['#..#', '....', '#..#', '#..#', '#..#', '#..#', '.###'],
  'ÿ': ['#..#', '....', '#..#', '#..#', '#..#', '#..#', '.###', '...#', '.##.'],
  'ç': ['...', '...', '.##', '#..', '#..', '#..', '.##', '.#.', '##.'],
  'œ': ['......', '......', '.#.##.', '#.#..#', '#.####', '#.#...', '.#.###'],
  'æ': ['......', '......', '.####.', '...#.#', '.#####', '#..#..', '.##.##'],
  'É': ['..#.', '####', '#...', '###.', '#...', '#...', '####'],
  'È': ['.#..', '####', '#...', '###.', '#...', '#...', '####'],
  'Ê': ['.##.', '####', '#...', '###.', '#...', '#...', '####'],
  'Ë': ['#..#', '####', '#...', '###.', '#...', '#...', '####'],
  'À': ['.#..', '.##.', '#..#', '####', '#..#', '#..#', '#..#'],
  'Â': ['.##.', '#..#', '.##.', '#..#', '####', '#..#', '#..#'],
  'Î': ['.#.', '###', '.#.', '.#.', '.#.', '.#.', '###'],
  'Ô': ['.##.', '.##.', '#..#', '#..#', '#..#', '#..#', '.##.'],
  'Ù': ['.#..', '#..#', '#..#', '#..#', '#..#', '#..#', '.##.'],
  'Û': ['.##.', '#..#', '#..#', '#..#', '#..#', '#..#', '.##.'],
  'Ç': ['.##.', '#..#', '#...', '#...', '#...', '#..#', '.##.', '..#.', '.##.'],
  'Œ': ['.#####', '#.#...', '#.#...', '#.###.', '#.#...', '#.#...', '.#####'],
  // (Release v9) Spanish, German, Italian
  'á': ['...#', '..#.', '.###', '#..#', '#..#', '#..#', '.###'],
  'í': ['..#', '.#.', '...', '.#.', '.#.', '.#.', '.#.'],
  'ì': ['#..', '.#.', '...', '.#.', '.#.', '.#.', '.#.'],
  'ó': ['...#', '..#.', '.##.', '#..#', '#..#', '#..#', '.##.'],
  'ò': ['.#..', '..#.', '.##.', '#..#', '#..#', '#..#', '.##.'],
  'ú': ['...#', '..#.', '#..#', '#..#', '#..#', '#..#', '.###'],
  'ñ': ['.#.#', '#.#.', '###.', '#..#', '#..#', '#..#', '#..#'],
  'ß': ['.##.', '#..#', '#.#.', '#..#', '#..#', '#..#', '#.#.'],
  'Á': ['..#.', '.##.', '#..#', '####', '#..#', '#..#', '#..#'],
  'Ä': ['#..#', '.##.', '#..#', '####', '#..#', '#..#', '#..#'],
  'Í': ['..#', '###', '.#.', '.#.', '.#.', '.#.', '###'],
  'Ì': ['#..', '###', '.#.', '.#.', '.#.', '.#.', '###'],
  'Ó': ['..#.', '.##.', '#..#', '#..#', '#..#', '#..#', '.##.'],
  'Ò': ['.#..', '.##.', '#..#', '#..#', '#..#', '#..#', '.##.'],
  'Ö': ['#..#', '.##.', '#..#', '#..#', '#..#', '#..#', '.##.'],
  'Ú': ['..#.', '#..#', '#..#', '#..#', '#..#', '#..#', '.##.'],
  'Ü': ['#..#', '....', '#..#', '#..#', '#..#', '#..#', '.##.'],
  'Ñ': ['.#.#', '#.#.', '#..#', '##.#', '#.##', '#..#', '#..#'],
  '¿': ['....', '..#.', '....', '..#.', '.#..', '#...', '#..#', '.##.'],
  '¡': ['.', '.', '#', '.', '#', '#', '#', '#', '#'],
  '«': ['.....', '.....', '..#.#', '.#.#.', '#.#..', '.#.#.', '..#.#'],
  '»': ['.....', '.....', '#.#..', '.#.#.', '..#.#', '.#.#.', '#.#..'],
  '€': ['..###', '.#...', '####.', '.#...', '####.', '.#...', '..###'],
  '\u00a0': ['...', '...', '...', '...', '...', '...', '...'],
  '\u202f': ['..', '..', '..', '..', '..', '..', '..'],
};

export const FONT_H = 9;       // glyph cell height incl. descenders
export const BASELINE = 7;     // rows above baseline
export let LINE_H = 11;
// Chinese needs taller lines than the 9px Latin cell: see setLineH()
export function setLineH(v) { LINE_H = v | 0; }

// Stacked text (a wrapped paragraph, a list of lines) steps by hand-picked
// numbers tuned on the Latin font's 9 rows of ink. Chinese ink is 13 rows, so
// in Chinese nothing may step tighter than one LINE_H: hand the step through
// here. Every other language gets its own number back untouched, which keeps
// their layout exactly as it was (LINE_H is 11 there).
export function lineStep(n) { return LINE_H > 11 && n < LINE_H ? LINE_H : n; }

// Where a run's ink actually lands, relative to the y handed to drawText:
// Latin ink starts at the y itself and is FONT_H tall; Chinese ink starts
// -oy*scale rows higher (its baseline is matched to Latin's, so it grows
// upwards) and is h*scale tall. Panels that place text by hand — a banner over
// a sub-line, a card with three stacked lines — measure with this instead of
// guessing, or Chinese creeps into whatever sits above it.
export function inkBox(scale = 1) {
  const o = cjk ? cjk.oy : 0, h = cjk ? cjk.h : FONT_H;
  return { top: o * scale, h: h * scale };
}

// A glyph is { w, h, x, y, oy }: the atlas cell plus how far below the line's
// top edge it is drawn (oy = 0 for Latin, negative for CJK, whose ink reaches
// higher because it is rasterised at 12px instead of 9px).
const glyphs = {};
let atlas = null;
let cjk = null;                 // { chars, data, w, h, oy } — see addCJK()
let cjkSet = null;
let built = false;
const tinted = new Map();
const TINT_MAX = 4;             // tinted atlas copies kept around (they are big)

const PACK_W = 1024;

// Register an exotic script (Chinese) rasterised offline: `chars` is a string of
// code points, `data` one hex string of `h` rows x 3 hex digits per glyph
// (12 texels a row, most significant bit leftmost).
export function addCJK(chars, data, w, h, oy) {
  cjk = { chars, data, w, h, oy };
  cjkSet = new Set(chars);
  glyphs_cjk_reset();
}
function glyphs_cjk_reset() {
  built = false;
  atlas = null;
  tinted.clear();
}

function build() {
  // Normalize rows & lay the glyphs out in shelves PACK_W wide
  const items = [];
  for (const ch of Object.keys(G)) {
    const rows = G[ch];
    items.push({ ch, rows, w: Math.max(...rows.map((r) => r.length)), h: rows.length, oy: 0 });
  }
  if (cjk) {
    const { chars, data, w, h, oy } = cjk;
    const stride = h * 3;
    for (let i = 0; i < chars.length; i++) {
      items.push({ ch: chars[i], hex: data.substr(i * stride, stride), w, h, oy });
    }
  }
  let x = 0, y = 0, shelf = 0;
  for (const it of items) {
    if (x + it.w > PACK_W) { x = 0; y += shelf + 1; shelf = 0; }
    it.x = x; it.y = y; x += it.w + 1;
    if (it.h > shelf) shelf = it.h;
  }
  atlas = document.createElement('canvas');
  atlas.width = PACK_W;
  atlas.height = Math.max(1, y + shelf);
  const ctx = atlas.getContext('2d');
  const img = ctx.createImageData(atlas.width, atlas.height);
  const D = img.data;
  for (const it of items) {
    const put = (gx, gy) => {
      const p = (gy * atlas.width + gx) * 4;
      D[p] = D[p + 1] = D[p + 2] = 255;
      D[p + 3] = 255;
    };
    if (it.rows) {
      it.rows.forEach((row, ry) => {
        for (let i = 0; i < row.length; i++) if (row[i] === '#') put(it.x + i, it.y + ry);
      });
    } else {
      for (let ry = 0; ry < it.h; ry++) {
        const bits = parseInt(it.hex.substr(ry * 3, 3), 16);
        if (!bits) continue;
        for (let i = 0; i < it.w; i++) if (bits & (1 << (it.w - 1 - i))) put(it.x + i, it.y + ry);
      }
    }
    glyphs[it.ch] = { w: it.w, h: it.h, x: it.x, y: it.y, oy: it.oy };
  }
  ctx.putImageData(img, 0, 0);
  built = true;
  tinted.clear();
}

function atlasFor(color) {
  if (!built) build();
  const hit = tinted.get(color);
  if (hit) { tinted.delete(color); tinted.set(color, hit); return hit; }
  const c = document.createElement('canvas');
  c.width = atlas.width;
  c.height = atlas.height;
  const cx = c.getContext('2d');
  cx.drawImage(atlas, 0, 0);
  cx.globalCompositeOperation = 'source-in';
  cx.fillStyle = color;
  cx.fillRect(0, 0, c.width, c.height);
  tinted.set(color, c);
  while (tinted.size > TINT_MAX) tinted.delete(tinted.keys().next().value);
  return c;
}

const ACCENTS = /[̀-ͯ]/g;
// (asked for every glyph drawn: characters without a glyph of their own are looked up once)
const NORM = new Map();
function normChar(ch) {
  if (cjkSet && cjkSet.has(ch)) return ch;
  if (glyphs[ch] || G[ch]) return ch;
  let n = NORM.get(ch);
  if (n === undefined) { n = normSlow(ch); NORM.set(ch, n); }
  return n;
}
function normSlow(ch) {
  const plain = ch.normalize('NFD').replace(ACCENTS, '');
  if (G[plain]) return plain;
  if (ch === '’' || ch === '‘') return "'";
  if (ch === '“' || ch === '”') return '"';
  if (ch === '—' || ch === '–') return '-';
  return '?';
}

export function glyphWidth(ch) {
  if (!atlas) build();
  return glyphs[normChar(ch)].w;
}

// Parse "{gold}text{/}" tags into segments [{text,color}]
export function parseRich(text, baseColor) {
  const segs = [];
  const stack = [baseColor];
  let buf = '';
  for (let i = 0; i < text.length; i++) {
    const ch = text[i];
    if (ch === '{') {
      const end = text.indexOf('}', i);
      if (end > i) {
        const tag = text.slice(i + 1, end);
        if (buf) { segs.push({ text: buf, color: stack[stack.length - 1] }); buf = ''; }
        if (tag === '/') { if (stack.length > 1) stack.pop(); }
        else stack.push(tag.startsWith('#') ? tag : COLORS[tag] || baseColor);
        i = end;
        continue;
      }
    }
    buf += ch;
  }
  if (buf) segs.push({ text: buf, color: stack[stack.length - 1] });
  return segs;
}

export function stripTags(text) {
  return text.replace(/\{[^}]*\}/g, '');
}

export function measure(text, scale = 1) {
  if (!atlas) build();
  const plain = stripTags(String(text));
  let w = 0, max = 0;
  for (const ch of plain) {
    if (ch === '\n') { max = Math.max(max, w); w = 0; continue; }
    w += glyphs[normChar(ch)].w + 1;
  }
  max = Math.max(max, w);
  return Math.max(0, max - 1) * scale;
}

// Draw text. opts: { color, shadow (color|false), align: 'left'|'center'|'right', scale, maxChars }
// Returns width drawn.
export function drawText(ctx, text, x, y, opts = {}) {
  if (!atlas) build();
  const { color = COLORS.ink, shadow = null, align = 'left', scale = 1, maxChars = Infinity, outline = null } = opts;
  text = String(text);
  const w = measure(text, scale);
  let cx = Math.round(align === 'center' ? x - w / 2 : align === 'right' ? x - w : x);
  const cy = Math.round(y);
  if (outline) {
    for (const [ox, oy] of [[-1, 0], [1, 0], [0, -1], [0, 1], [-1, -1], [1, -1], [-1, 1], [1, 1]]) {
      drawRun(ctx, text, cx + ox * scale, cy + oy * scale, outline, scale, maxChars, true);
    }
  }
  if (shadow) drawRun(ctx, text, cx, cy + scale, shadow, scale, maxChars, true);
  drawRun(ctx, text, cx, cy, color, scale, maxChars, false);
  return w;
}

function drawRun(ctx, text, x, y, color, scale, maxChars, flat) {
  const segs = parseRich(text, color);
  let cx = x, count = 0;
  for (const seg of segs) {
    const img = atlasFor(flat ? color : seg.color);
    for (const ch of seg.text) {
      if (count >= maxChars) return;
      count++;
      if (ch === '\n') continue;
      const g = glyphs[normChar(ch)];
      ctx.drawImage(img, g.x, g.y, g.w, g.h, cx, y + g.oy * scale, g.w * scale, g.h * scale);
      cx += (g.w + 1) * scale;
    }
  }
}

// Punctuation that may not open a line / may not close one (Chinese typesetting)
const CJK_NO_START = '，。、！？：；）】》」』”’…—·〉〕》';
const CJK_NO_END = '（【《「『“‘〈〔';

// Split a paragraph into unbreakable atoms: Latin words (spaces separate them),
// and single characters for scripts written without spaces.
function atoms(para) {
  const out = [];
  let word = '';
  for (const ch of para) {
    if (ch === ' ') { if (word) { out.push(word); word = ''; } out.push(' '); continue; }
    if (cjkSet && cjkSet.has(ch)) { if (word) { out.push(word); word = ''; } out.push(ch); continue; }
    word += ch;
  }
  if (word) out.push(word);
  return out;
}

// Word-wrap text (tags preserved) into lines that fit maxWidth.
export function wrap(text, maxWidth, scale = 1) {
  const out = [];
  for (const para of String(text).split('\n')) {
    const list = atoms(para);
    let line = '';
    for (let i = 0; i < list.length; i++) {
      const a = list[i];
      if (a === ' ' && !line) continue;
      if (!line || measure(line + a, scale) <= maxWidth) { line += a; continue; }
      // The atom does not fit. Closing punctuation hangs past the margin rather
      // than starting the next line, and an opening bracket always travels with
      // the character that follows it.
      if (CJK_NO_START.includes(a)) { out.push(line + a); line = ''; continue; }
      if (CJK_NO_END.includes(line[line.length - 1])) {
        const br = line[line.length - 1];
        out.push(line.slice(0, -1));
        line = br + a;
        continue;
      }
      out.push(line);
      line = a === ' ' ? '' : a;
    }
    out.push(line);
  }
  // carry open color tags across line breaks
  let open = null;
  return out.map((l) => {
    const prefix = open ? `{${open}}` : '';
    const tags = [...l.matchAll(/\{([^}]*)\}/g)].map((m) => m[1]);
    for (const t of tags) open = t === '/' ? null : t;
    return prefix + l + (open ? '{/}' : '');
  });
}

export function visibleLength(text) {
  return stripTags(text).length;
}
