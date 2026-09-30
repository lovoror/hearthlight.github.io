// Dumps a language's short dictionary entries as `tools/i18n/names-<lang>.json`
// — one flat key -> translation object. The translation guides point at these
// files so a translator can look up how a name was rendered elsewhere.
//
// The list of entries worth keeping is defined by `names-fr.json` itself (the
// hand-picked subset of keys that ship in the game), so every language ends up
// with exactly the same set of keys:
//
//   node tools/i18n/names.mjs zh        (writes tools/i18n/names-zh.json)
//
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '..', '..');
const lang = process.argv[2];
if (!lang) { console.error('usage: node tools/i18n/names.mjs <lang>'); process.exit(2); }

const listFile = path.join(here, 'names-fr.json');
if (!fs.existsSync(listFile)) { console.error(`no ${listFile} to take the key list from`); process.exit(2); }
const keys = Object.keys(JSON.parse(fs.readFileSync(listFile, 'utf8')));

const dictFile = path.join(root, 'src', 'lang', lang, 'index.js');
if (!fs.existsSync(dictFile)) { console.error(`no such dictionary: ${dictFile}`); process.exit(2); }
const mod = await import(pathToFileURL(dictFile).href);
const dict = mod[lang.toUpperCase()];
if (!dict) { console.error(`src/lang/${lang}/index.js exports nothing named ${lang.toUpperCase()}`); process.exit(2); }

const out = {};
const missing = [];
for (const k of keys) {
  if (typeof dict[k] !== 'string') missing.push(k);
  else out[k] = dict[k];
}
const dest = path.join(here, `names-${lang}.json`);
fs.writeFileSync(dest, JSON.stringify(out));
console.log(`${dest} — ${Object.keys(out).length} entries`);
if (missing.length) console.log(`  (${missing.length} keys not in ${lang}: ${missing.slice(0, 5).join(' | ')}…)`);
