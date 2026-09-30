"""Compose a contact sheet of crops out of screenshots/, for eyeballing UI at 2x.

  python tools/i18n/sheet.py out.png 'shot:left,top,right,bottom' 'shot:...' ...

`shot` is a file name inside screenshots/ without the .png suffix. Crop boxes are
in source pixels; each crop is upscaled 2x with NEAREST and packed into a grid
that is at most 3 tiles wide.
"""
import sys
from PIL import Image, ImageDraw

OUT = sys.argv[1]
tiles = []
for spec in sys.argv[2:]:
    name, _, box = spec.partition(':')
    im = Image.open('screenshots/%s.png' % name).convert('RGB')
    if box:
        x0, y0, x1, y1 = (int(v) for v in box.split(','))
        im = im.crop((x0, y0, x1, y1))
    im = im.resize((im.width * 2, im.height * 2), Image.NEAREST)
    tiles.append((name, im))

cols = 2 if len(tiles) > 1 else 1
rows = (len(tiles) + cols - 1) // cols
cw = max(t[1].width for t in tiles) + 8
ch = max(t[1].height for t in tiles) + 18
sheet = Image.new('RGB', (cw * cols, ch * rows), (24, 20, 32))
d = ImageDraw.Draw(sheet)
for i, (name, im) in enumerate(tiles):
    x = (i % cols) * cw
    y = (i // cols) * ch
    d.text((x + 4, y + 4), name, fill=(255, 220, 120))
    sheet.paste(im, (x + 4, y + 16))
sheet.save(OUT)
print(OUT, sheet.size)
