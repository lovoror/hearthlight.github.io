#!/usr/bin/env python3
"""Rasterise the Simplified-Chinese glyph set into src/art/cjkfont.js.

The game has no CSS fonts: every glyph is drawn from a hand-written bitmap
atlas (src/engine/font.js, the "Cove 7" Latin font).  Chinese needs ~7 000
ideographs, so instead of hand-writing them we rasterise them once, offline,
from Source Han Sans SC and store them as a compact 1-bit hex table.

  python tools/gen-cjkfont.py            # write src/art/cjkfont.js
  python tools/gen-cjkfont.py --preview  # also write tools/i18n/cjk-preview.png

Geometry (must match src/engine/font.js):
  * cell           12 x 13 texels
  * baseline       cell row 11   (Latin baseline sits at row 7 of its 9-row cell)
  * draw offset    oy = -4       (so CJK ink lines up with the Latin baseline)
  * bits           row-major, 12 bits per row, 3 hex digits per row, MSB = left
"""
import argparse
import glob
import json
import os
import re
import sys

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT_PATH = os.environ.get(
    'CJK_FONT',
    r'G:\soft\font\09_SourceHanSansSC\OTF\SimplifiedChinese\SourceHanSansSC-Normal.otf')
SIZE = 12
BASE_ROW = 11
CELL_W, CELL_H = 12, 13
THRESH = 100

# punctuation and marks that Chinese text needs on top of GB 2312
EXTRA = (
    '\u3000\u3001\u3002\u300c\u300d\u300e\u300f\u3010\u3011\u3014\u3015'
    '\uff01\uff02\uff05\uff08\uff09\uff0a\uff0b\uff0c\uff0d\uff0e\uff0f'
    '\uff1a\uff1b\uff1c\uff1d\uff1e\uff1f\uff20\uff3b\uff3d\uff5b\uff5d'
    '\uff5e\u2018\u2019\u201c\u201d\u2026\u2014\u2013\u00b7\u2192\u2190'
    '\u2665\u2661\u2605\u266a\u2022\u00b0\u00d7\u00b0\u2103'
)


def gb2312_chars():
    """Every character GB 2312 can encode (symbols + 6 763 ideographs)."""
    out = []
    for lead in range(0xA1, 0xF8):
        for trail in range(0xA1, 0xFF):
            try:
                ch = bytes([lead, trail]).decode('gb2312')
            except UnicodeDecodeError:
                continue
            if len(ch) == 1:
                out.append(ch)
    return out


def used_chars():
    """Every non-ASCII character already written into a Chinese dictionary."""
    out = set()
    for path in glob.glob(os.path.join(ROOT, 'src', 'lang', 'zh', '*.js')):
        with open(path, encoding='utf-8') as f:
            text = f.read()
        for ch in text:
            if ord(ch) > 0x7F:
                out.add(ch)
    return out


def build_charset():
    seen = {}
    for ch in gb2312_chars() + list(EXTRA) + sorted(used_chars()):
        if ord(ch) < 0x80:
            continue                      # ASCII lives in the Latin font
        if 0xD800 <= ord(ch) <= 0xDFFF or ord(ch) > 0xFFFF:
            continue                      # no surrogates / astral plane
        seen[ch] = True
    return sorted(seen)


def rasterise(chars, font):
    ascent, _ = font.getmetrics()
    top = BASE_ROW - ascent
    rows = []
    blank = []
    for ch in chars:
        img = Image.new('L', (CELL_W, CELL_H), 0)
        ImageDraw.Draw(img).text((0, top), ch, font=font, fill=255)
        px = img.load()
        glyph = []
        empty = True
        for y in range(CELL_H):
            bits = 0
            for x in range(CELL_W):
                if px[x, y] >= THRESH:
                    bits |= 1 << (CELL_W - 1 - x)
                    empty = False
            glyph.append('%03x' % bits)
        rows.append(''.join(glyph))
        if empty:
            blank.append(ch)
    return rows, blank


def preview(chars, font, path):
    """Draw the generated bitmaps back out, so the shaping can be eyeballed."""
    ascent, _ = font.getmetrics()
    top = BASE_ROW - ascent
    text = ('你好，旅行者！欢迎来到金盏湾。\n'
            'HP 24/30  经验 +120  体力\n'
            '「任务：熄灭的灯」你愿意帮忙吗？\n'
            '魔藏骑警铁匠铺 一二三四五六七八九十\n'
            'ABCDEFGHIJKLM abcdefghijk 0123456789')
    scale, pad = 2, 8
    lines = text.split('\n')
    w = max(len(l) for l in lines) * (CELL_W + 1) + pad * 2
    h = len(lines) * (CELL_H + 2) + pad * 2
    img = Image.new('RGB', (w * scale, h * scale), (24, 20, 32))
    d = ImageDraw.Draw(img)
    for li, line in enumerate(lines):
        for ci, ch in enumerate(line):
            if ch == ' ':
                continue
            ox = (pad + ci * (CELL_W + 1)) * scale
            oy = (pad + li * (CELL_H + 2)) * scale
            if ord(ch) < 0x80:
                cell = Image.new('L', (CELL_W, CELL_H), 0)
                ImageDraw.Draw(cell).text((0, top), ch, font=font, fill=255)
            else:
                cell = Image.new('L', (CELL_W, CELL_H), 0)
                ImageDraw.Draw(cell).text((0, top), ch, font=font, fill=255)
            px = cell.load()
            for y in range(CELL_H):
                for x in range(CELL_W):
                    if px[x, y] >= THRESH:
                        d.rectangle([ox + x * scale, oy + y * scale,
                                     ox + x * scale + scale - 1,
                                     oy + y * scale + scale - 1],
                                    fill=(232, 226, 200))
    img.save(path)
    print('wrote', os.path.relpath(path, ROOT))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--preview', action='store_true')
    ap.add_argument('--out', default=os.path.join(ROOT, 'src', 'art', 'cjkfont.js'))
    args = ap.parse_args()

    if not os.path.exists(FONT_PATH):
        sys.exit('font not found: ' + FONT_PATH)
    font = ImageFont.truetype(FONT_PATH, SIZE)
    chars = build_charset()
    rows, blank = rasterise(chars, font)

    data = ''.join(rows)
    body = [
        '// Generated by tools/gen-cjkfont.py — do not edit by hand.',
        '// Simplified-Chinese glyphs (%d) rasterised from Source Han Sans SC at %d px,'
        % (len(chars), SIZE),
        '// packed 1-bit: 3 hex digits (12 texels) per row, %d rows per glyph, top row first.' % CELL_H,
        '// Register with the font engine via src/i18n.js (addCJK).',
        '',
        'export const CJK_W = %d;' % CELL_W,
        'export const CJK_H = %d;' % CELL_H,
        'export const CJK_OY = %d;   // draw offset so CJK sits on the Latin baseline' % (7 - BASE_ROW),
        'export const CJK_CHARS =',
        '  ' + json.dumps(''.join(chars), ensure_ascii=False) + ';',
        'export const CJK_DATA =',
        '  ' + json.dumps(data, ensure_ascii=False) + ';',
        '',
    ]
    with open(args.out, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(body))
    print('chars  ', len(chars))
    print('glyphs ', len(rows), 'data', len(data), 'hex chars')
    print('blank  ', len(blank), ''.join(blank[:40]))
    print('wrote  ', os.path.relpath(args.out, ROOT), os.path.getsize(args.out), 'B')
    if args.preview:
        preview(chars, font, os.path.join(ROOT, 'tools', 'i18n', 'cjk-preview.png'))


if __name__ == '__main__':
    main()
