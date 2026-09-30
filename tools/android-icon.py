# Hearthlight's launcher icon, drawn here like everything else it ships: a
# 24x24 lantern, nearest-neighbour up to the mipmap sizes Android asks for.
#   python tools/android-icon.py
import os
import sys

try:
    from PIL import Image
except ImportError:
    sys.exit('需要 Pillow：python -m pip install pillow')

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'android', 'res')

# '.' background, 'a' brass, 'A' lit brass, 'b' glass, 'B' glass near the flame, 'c' flame
ART = [
    '........................',
    '..........aaaa..........',
    '..........a..a..........',
    '..........a..a..........',
    '.......AAAAAAAAAA.......',
    '......aaaaaaaaaaaa......',
    '......aaaaaaaaaaaa......',
    '.......aaaaaaaaaa.......',
    '.......abbbbbbbba.......',
    '.......adbbbbbbda.......',
    '.......adbBBBbbda.......',
    '.......adbbccbbda.......',
    '.......adbBccBdba.......',
    '.......adbBccBdba.......',
    '.......adbccccdba.......',
    '.......adbbccbbda.......',
    '.......adbbbBbbda.......',
    '.......adbbbbbbda.......',
    '.......adbbbbbbda.......',
    '.......addbbbbdda.......',
    '......aaaaaaaaaaaa......',
    '.......aaaaaaaaaa.......',
    '.........aaaaaa.........',
    '........................',
]
INK = {
    'a': (107, 79, 51, 255),
    'A': (146, 112, 72, 255),
    'b': (246, 198, 91, 255),
    'd': (214, 148, 58, 255),
    'B': (255, 236, 170, 255),
    'c': (255, 250, 220, 255),
}
NIGHT = (36, 27, 46, 255)       # #241b2e, the panels' background
SIZE = len(ART)                 # the art is square; the grid is the icon
SIZES = {'mdpi': 48, 'hdpi': 72, 'xhdpi': 96, 'xxhdpi': 144, 'xxxhdpi': 192}


def tile(round_icon=False):
    im = Image.new('RGBA', (SIZE, SIZE), NIGHT)
    px = im.load()
    for y, row in enumerate(ART):
        for x, ch in enumerate(row):
            if ch in INK:
                px[x, y] = INK[ch]
    if round_icon:
        # square off the corners so a round launcher mask has nothing to cut
        c = (SIZE - 1) / 2.0
        r = SIZE * 0.525
        for y in range(SIZE):
            for x in range(SIZE):
                if (x - c) ** 2 + (y - c) ** 2 > r * r:
                    px[x, y] = (0, 0, 0, 0)
    return im


def main():
    for folder, size in SIZES.items():
        d = os.path.join(OUT, 'mipmap-' + folder)
        os.makedirs(d, exist_ok=True)
        for name, rnd in (('ic_launcher.png', False), ('ic_launcher_round.png', True)):
            img = tile(rnd).resize((size, size), Image.NEAREST)
            img.save(os.path.join(d, name))
            print('wrote', os.path.relpath(os.path.join(d, name)))


if __name__ == '__main__':
    main()
