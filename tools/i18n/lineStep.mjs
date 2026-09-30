// One-off codemod (not part of the game's tooling): Chinese ink is 13 rows tall
// against the Latin font's 9, so every stacked-text step that was hand-tuned on
// the Latin font gets widened in Chinese. font.lineStep(n) returns n unchanged
// in every other language, so the shots in fr/es/de/it cannot move.
//
//   node tools/i18n/lineStep.mjs            # dry run: prints every change
//   node tools/i18n/lineStep.mjs --write
import fs from 'node:fs';
import path from 'node:path';

const ROOT = 'src';
const WRITE = process.argv.includes('--write');
const N = '(9|10|11|12)';
const stepRe = new RegExp('\\b([ij]) \\* ' + N + '\\b', 'g');
const lenRe = new RegExp('(\\.length \\* )' + N + '\\b', 'g');

function walk(dir, out = []) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, e.name);
    if (e.isDirectory()) walk(p, out);
    else if (e.name.endsWith('.js')) out.push(p);
  }
  return out;
}

const changed = [];
for (const file of walk(ROOT)) {
  const src = fs.readFileSync(file, 'utf8');
  if (!src.includes('drawText(')) continue;
  const lines = src.split('\n');
  let hit = 0;
  for (let i = 0; i < lines.length; i++) {
    const l = lines[i];
    const before = l;
    let after = l;
    // the step between stacked lines
    if (l.includes('drawText(') && !l.includes('fillRect(')) after = after.replace(stepRe, (m, v, n) => `${v} * lineStep(${n})`);
    // and any height a block of text reserves for itself
    after = after.replace(lenRe, (m, pre, n) => `${pre}lineStep(${n})`);
    if (after !== before) { lines[i] = after; hit++; changed.push(`${file}:${i + 1}\n  - ${before.trim()}\n  + ${after.trim()}`); }
  }
  if (!hit) continue;
  let out = lines.join('\n');
  // make sure lineStep is imported from the font module this file already uses
  const rel = path.relative(path.dirname(file), path.join(ROOT, 'engine/font.js')).replace(/\\/g, '/');
  const spec = rel.startsWith('.') ? rel : './' + rel;
  const imp = new RegExp(`import \\{([^}]*)\\} from '([^']*font\\.js)';`);
  const m = out.match(imp);
  if (m && !m[1].includes('lineStep')) {
    out = out.replace(imp, (s, names, from) => `import {${names.trim().replace(/,$/, '')}, lineStep } from '${from}';`);
  } else if (!m) {
    const last = [...out.matchAll(/^import .*;$/gm)].pop();
    out = out.slice(0, last.index + last[0].length) + `\nimport { lineStep } from '${spec}';` + out.slice(last.index + last[0].length);
  }
  if (WRITE) fs.writeFileSync(file, out);
}

console.log(changed.join('\n'));
console.log(`\n${changed.length} line(s) in ${new Set(changed.map((c) => c.split(':')[0])).size} file(s)${WRITE ? ' — written' : ' — dry run'}`);
