"""Sanity-checks a built APK: what is inside, and what the packaged config says.

  python tools/apkcheck.py android/Hearthlight.apk
  python tools/apkcheck.py android/Hearthlight.apk --extract <dir>

--extract unpacks the APK's assets/ into <dir> with the prefix stripped, so the
result is exactly what the WebView serves: a plain copy of the game.
"""
import os
import re
import sys
import zipfile

argv = [a for a in sys.argv[1:]]
extract = None
if '--extract' in argv:
    i = argv.index('--extract')
    extract = argv[i + 1]
    del argv[i:i + 2]
path = argv[0] if argv else 'android/Hearthlight.apk'

if extract:
    z = zipfile.ZipFile(path)
    n = 0
    for info in z.infolist():
        if not info.filename.startswith('assets/') or info.is_dir():
            continue
        rel = info.filename[len('assets/'):]
        dest = os.path.join(extract, *rel.split('/'))
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with z.open(info) as src, open(dest, 'wb') as out:
            out.write(src.read())
        n += 1
    print('extracted %d asset files to %s' % (n, extract))
    sys.exit(0)

z = zipfile.ZipFile(path)
names = z.namelist()
print('%s: %d entries' % (path, len(names)))
strays = [n for n in names if n.startswith('.') or '/.' in n or '__MACOSX' in n]
print('stray hidden entries: %d %s' % (len(strays), strays[:4]))
for n in ['AndroidManifest.xml', 'resources.arsc', 'classes.dex', 'assets/index.html',
          'assets/config.js', 'assets/src/main.js', 'assets/src/lang/zh/index.js',
          'assets/src/lang/zh/story.js', 'assets/src/art/cjkfont.js',
          'assets/src/engine/font.js', 'assets/vendor/three/three.module.js',
          'assets/res/../META-INF/MANIFEST.MF']:
    if n.endswith('MANIFEST.MF'):
        n = [m for m in names if m.endswith('MANIFEST.MF')]
        print('   signature: %s' % (n or 'NONE'))
        continue
    print('%s %-38s %s' % ('OK  ' if n in names else 'MISS', n,
                           z.getinfo(n).file_size if n in names else ''))
cfg = z.read('assets/config.js').decode('utf-8')
for key in ('relay', 'pad', 'stats', 'onlineRelay', 'onlinePad', 'saves'):
    m = re.search(r"(?<![A-Za-z])%s: '([^']*)'" % key, cfg)
    print('  config.%s = %r' % (key, m.group(1) if m else None))
total = sum(i.file_size for i in z.infolist())
print('uncompressed: %.2f MB' % (total / 1048576.0))
