#!/usr/bin/env python3
"""Draw the news-image-20261119 ROUND 2 entry: a newspaper front page,
THE WORLD TODAY, summing up Thursday 19 November 2026 in 35 verified
stories -- 4 illustrated leads, a pinned world map, 8 illustrated
mini-tiles and a 3-column brief index.

Deterministic: no clock, no network, no randomness at draw time.
Run:  python3 draw.py [output-path]   (default: entry.png beside this file)
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 230)
INK = (22, 22, 22)
RED = (176, 30, 42)
BLUE = (28, 76, 134)
TEAL = (16, 108, 102)
GOLD = (198, 152, 40)
GREY = (92, 88, 78)
RULE = (62, 58, 50)
OCEAN = (203, 224, 234)
LAND = (168, 188, 148)
LAND_EDGE = (110, 132, 96)

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")


def font(name, size):
    return ImageFont.truetype(str(FONT_DIR / name), size)


def serif_b(s):
    return font("DejaVuSerif-Bold.ttf", s)


def serif(s):
    return font("DejaVuSerif.ttf", s)


def sans_b(s):
    return font("DejaVuSans-Bold.ttf", s)


def sans(s):
    return font("DejaVuSans.ttf", s)


def wrap(d, text, fnt, max_w):
    """Greedy word wrap; returns lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(d, x, y, lines, fnt, fill, leading):
    for line in lines:
        d.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def vgrad(d, x0, y0, x1, y1, colours):
    """Vertical gradient built from flat horizontal bands."""
    n = len(colours)
    h = y1 - y0
    for i, c in enumerate(colours):
        d.rectangle([x0, y0 + i * h // n, x1, y0 + (i + 1) * h // n], fill=c)


def frame(d, x, y, w, h, width=2):
    d.rectangle([x, y, x + w, y + h], outline=RULE, width=width)


# ---------------------------------------------------------------- world map
# Simplified continent outlines as (lon, lat) vertices, drawn in an
# equirectangular strip: lon -180..180 across, lat 75..-55 down.
CONTINENTS = [
    # North America
    [(-168, 66), (-156, 71), (-140, 70), (-128, 71), (-115, 68), (-102, 68),
     (-92, 66), (-85, 66), (-82, 69), (-76, 62), (-68, 58), (-60, 55),
     (-55, 52), (-60, 47), (-65, 44), (-70, 42), (-74, 39), (-76, 35),
     (-80, 32), (-81, 26), (-84, 30), (-89, 29), (-91, 19), (-96, 16),
     (-102, 18), (-105, 20), (-110, 23), (-114, 28), (-117, 33),
     (-122, 37), (-124, 42), (-124, 49), (-130, 54), (-137, 58),
     (-148, 60), (-158, 58), (-165, 60), (-168, 66)],
    # Greenland
    [(-58, 64), (-52, 60), (-42, 60), (-32, 68), (-22, 70), (-25, 74),
     (-35, 76), (-50, 76), (-58, 74), (-60, 70), (-58, 64)],
    # South America
    [(-80, 10), (-77, 8), (-72, 12), (-64, 10), (-60, 8), (-54, 6),
     (-51, 4), (-50, 0), (-44, -3), (-38, -5), (-35, -8), (-37, -13),
     (-39, -18), (-41, -23), (-48, -27), (-52, -32), (-57, -38),
     (-62, -41), (-66, -45), (-68, -50), (-70, -54), (-73, -50),
     (-73, -42), (-72, -35), (-71, -28), (-70, -20), (-75, -15),
     (-79, -8), (-81, -4), (-80, 0), (-80, 6), (-80, 10)],
    # Europe
    [(-10, 36), (-9, 38), (-9, 43), (-2, 44), (-1, 46), (-4, 48),
     (0, 50), (2, 51), (4, 53), (7, 54), (8, 57), (10, 59), (12, 58),
     (18, 56), (21, 55), (24, 58), (26, 60), (30, 61), (28, 65),
     (24, 68), (20, 70), (16, 71), (13, 69), (12, 66), (10, 64),
     (6, 62), (5, 59), (5, 58), (1, 57), (-3, 54), (-5, 50),
     (-7, 48), (-9, 46), (-10, 42), (-10, 36)],
    # Africa
    [(-6, 35), (0, 36), (10, 37), (15, 32), (20, 32), (25, 32),
     (30, 31), (32, 30), (34, 28), (35, 24), (37, 20), (39, 16),
     (41, 12), (44, 11), (48, 11), (51, 11), (50, 6), (47, 2),
     (42, -2), (40, -6), (38, -12), (36, -18), (34, -22), (32, -26),
     (30, -30), (27, -33), (22, -35), (19, -34), (16, -30), (14, -24),
     (12, -18), (12, -12), (10, -5), (9, 0), (9, 4), (5, 5),
     (0, 6), (-6, 5), (-10, 6), (-13, 8), (-16, 12), (-17, 15),
     (-17, 20), (-16, 24), (-14, 28), (-10, 31), (-6, 35)],
    # Asia (mainland)
    [(28, 36), (30, 36), (34, 36), (36, 36), (36, 33), (38, 32),
     (40, 32), (43, 31), (46, 30), (48, 30), (50, 29), (52, 28),
     (55, 27), (57, 26), (60, 25), (62, 25), (65, 25), (67, 24),
     (70, 22), (72, 20), (74, 17), (76, 12), (77, 8), (80, 10),
     (80, 14), (82, 17), (85, 19), (87, 22), (89, 22), (91, 22),
     (93, 18), (95, 16), (97, 14), (98, 10), (100, 8), (101, 6),
     (103, 2), (104, 2), (105, 9), (106, 10), (108, 12), (109, 15),
     (109, 19), (110, 20), (112, 22), (114, 22), (116, 23), (118, 25),
     (120, 28), (121, 32), (120, 35), (122, 37), (124, 40), (126, 40),
     (128, 38), (130, 38), (130, 42), (132, 43), (135, 43), (138, 46),
     (141, 46), (142, 50), (141, 53), (142, 55), (145, 59), (150, 59),
     (155, 56), (158, 53), (160, 56), (162, 58), (165, 60), (170, 60),
     (170, 63), (173, 65), (178, 65), (178, 68), (173, 69), (168, 66),
     (162, 66), (156, 64), (150, 66), (145, 68), (140, 70), (135, 71),
     (130, 72), (125, 73), (120, 73), (115, 73), (110, 74), (105, 74),
     (100, 73), (95, 72), (90, 71), (85, 70), (80, 68), (75, 66),
     (72, 62), (70, 58), (68, 54), (66, 50), (64, 46), (62, 44),
     (60, 42), (58, 39), (56, 38), (54, 37), (52, 38), (50, 40),
     (48, 41), (46, 42), (44, 42), (42, 42), (40, 41), (38, 40),
     (36, 38), (34, 38), (30, 38), (28, 36)],
    # South-East Asian islands
    [(95, 5), (98, 4), (100, 0), (102, -2), (105, -5), (108, -7),
     (112, -7), (115, -8), (118, -9), (120, -10), (119, -8), (115, -6),
     (110, -6), (106, -6), (102, -3), (98, 1), (95, 5)],
    [(109, 1), (111, 2), (114, 4), (117, 6), (119, 5), (118, 1),
     (116, -2), (113, -3), (110, -2), (109, 1)],
    # New Guinea
    [(131, -1), (134, -2), (137, -3), (140, -3), (143, -4), (146, -6),
     (149, -8), (150, -9), (147, -9), (144, -8), (141, -8), (138, -7),
     (135, -5), (132, -3), (131, -1)],
    # Australia
    [(113, -22), (114, -28), (115, -32), (116, -35), (119, -34),
     (122, -34), (125, -33), (129, -32), (132, -32), (134, -33),
     (136, -35), (139, -36), (140, -38), (143, -39), (146, -39),
     (149, -37), (150, -35), (153, -32), (153, -28), (152, -25),
     (150, -23), (148, -20), (146, -19), (144, -15), (142, -11),
     (141, -13), (139, -15), (137, -12), (135, -12), (133, -12),
     (130, -13), (128, -14), (126, -14), (124, -16), (122, -17),
     (120, -19), (117, -20), (114, -22), (113, -22)],
    # New Zealand
    [(167, -45), (169, -43), (171, -42), (173, -40), (175, -38),
     (176, -38), (174, -41), (172, -43), (169, -46), (167, -45)],
]

PINS = [
    # (lon, lat, label for the key)
    (-77.0, 39.0, "Washington"),
    (-72.3, 18.5, "Port-au-Prince"),
    (-0.1, 51.5, "London"),
    (4.3, 52.1, "The Hague"),
    (13.4, 52.5, "Berlin"),
    (34.5, 31.5, "Gaza"),
    (45.3, 2.0, "Mogadishu"),
    (37.9, 14.7, "Badme"),
    (56.5, 26.5, "Hormuz"),
    (114.1, 22.5, "Shenzhen"),
    (127.0, 37.5, "Seoul"),
    (106.9, 47.9, "Ulaanbaatar"),
    (106.8, -6.2, "Jakarta"),
    (85.8, 19.8, "Odisha"),
    (174.8, -41.3, "Wellington"),
]


def project(x0, y0, w, h, lon, lat):
    """Equirectangular: lon -180..180, lat 75..-55."""
    px = x0 + (lon + 180.0) / 360.0 * w
    py = y0 + (75.0 - lat) / 130.0 * h
    return px, py


def draw_map(d, x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=OCEAN, outline=RULE, width=2)
    # faint graticule
    for lon in range(-150, 181, 30):
        gx, _ = project(x0, y0, w, h, lon, 0)
        d.line([gx, y0, gx, y0 + h], fill=(190, 208, 220), width=1)
    for lat in (60, 30, 0, -30):
        _, gy = project(x0, y0, w, h, 0, lat)
        d.line([x0, gy, x0 + w, gy], fill=(190, 208, 220), width=1)
    for poly in CONTINENTS:
        pts = [project(x0, y0, w, h, lon, lat) for lon, lat in poly]
        d.polygon(pts, fill=LAND, outline=LAND_EDGE)
    # numbered pins
    for i, (lon, lat, _label) in enumerate(PINS, start=1):
        px, py = project(x0, y0, w, h, lon, lat)
        r = 7
        d.ellipse([px - r, py - r, px + r, py + r], fill=RED,
                  outline=(255, 255, 255), width=1)
        num = str(i)
        nw = d.textlength(num, font=sans_b(9))
        d.text((px - nw / 2, py - 6), num, font=sans_b(9),
               fill=(255, 255, 255))

# ---------------------------------------------------------------- pictures
def pic_gta(d, x, y, w, h):
    """Vice City at dusk: purple-orange sky, low sun, skyline, water."""
    vgrad(d, x, y, x + w, y + h,
          [(44, 22, 72), (92, 36, 94), (172, 60, 88), (228, 114, 62),
           (246, 166, 90), (250, 204, 128)])
    d.ellipse([x + w - 96, y + 8, x + w - 48, y + 56], fill=(255, 214, 128))
    d.ellipse([x + w - 88, y + 16, x + w - 56, y + 48], fill=(255, 238, 182))
    base = y + h - 22
    towers = [(0, 62, 30), (36, 44, 28), (70, 68, 26), (102, 38, 34),
              (142, 58, 28), (176, 48, 26), (208, 66, 24)]
    for bx, by, bw in towers:
        d.rectangle([x + bx, y + by, x + bx + bw, base], fill=(28, 15, 50))
        for wy in range(by + 8, base - y - 4, 12):
            for wx in range(bx + 5, bx + bw - 4, 11):
                if (wx * 5 + wy * 3) % 4 < 2:
                    d.rectangle([x + wx, y + wy, x + wx + 4, y + wy + 4],
                                fill=(255, 212, 118))
    d.rectangle([x, base, x + w, y + h], fill=(22, 46, 90))
    for i in range(5):
        d.line([x + 14 + i * 46, base + 6 + i * 2, x + 50 + i * 46, base + 6 + i * 2],
               fill=(255, 188, 108), width=2)
    # palm silhouettes at both edges
    for px, ph in ((26, 40), (w - 30, 46)):
        d.line([x + px, base, x + px + 4, base - ph], fill=(14, 9, 28), width=5)
        top = (x + px + 4, base - ph)
        for dx, dy in ((-24, 2), (-18, -12), (-6, -20), (8, -20), (18, -12), (24, 0)):
            d.line([top, (top[0] + dx, top[1] + dy)], fill=(14, 9, 28), width=3)


def pic_anthropic(d, x, y, w, h):
    """A share chart rocketing up on a dark trading board, ANT ticker."""
    d.rectangle([x, y, x + w, y + h], fill=(13, 27, 52))
    for gy in range(y + 16, y + h - 8, 22):
        d.line([x + 8, gy, x + w - 8, gy], fill=(36, 60, 98), width=1)
    bars = [20, 28, 24, 38, 46, 42, 58, 70, 66, 86, 100, 118]
    scale = (h - 30) / 128.0
    bars = [int(b * scale) for b in bars]
    bw = (w - 30) // len(bars)
    for i, bh in enumerate(bars):
        bx = x + 15 + i * bw
        col = (44, 188, 118) if i > 5 else (88, 138, 198)
        d.rectangle([bx, y + h - 12 - bh, bx + bw - 5, y + h - 12], fill=col)
    pts = [(x + 15 + i * bw, y + h - 20 - bh) for i, bh in enumerate(bars)]
    d.line(pts, fill=(255, 255, 255), width=3, joint="curve")
    for px_, py_ in pts[::3]:
        d.ellipse([px_ - 4, py_ - 4, px_ + 4, py_ + 4], fill=(255, 255, 255))
    d.text((x + 13, y + 8), "ANT", font=sans_b(28), fill=(255, 255, 255))
    d.text((x + 13, y + 40), "NASDAQ", font=sans_b(12), fill=(138, 168, 218))
    d.text((x + w - 86, y + 10), "+$81bn", font=sans_b(15), fill=(120, 230, 170))


def pic_icj(d, x, y, w, h):
    """The Hague: court columns, the scales of justice, a gavel."""
    vgrad(d, x, y, x + w, y + h,
          [(18, 38, 74), (32, 62, 108), (58, 92, 140), (90, 124, 168)])
    # colonnade
    col_top, col_bot = y + 12, y + h - 22
    for cx in (14, 58, 102, 146, 190):
        d.rectangle([x + cx, col_top + 4, x + cx + 14, col_bot], fill=(228, 220, 200))
        d.rectangle([x + cx - 3, col_top, x + cx + 17, col_top + 5], fill=(240, 234, 216))
        d.rectangle([x + cx - 3, col_bot, x + cx + 17, col_bot + 5], fill=(240, 234, 216))
    d.rectangle([x, col_bot + 5, x + w, col_bot + 10], fill=(240, 234, 216))
    # scales of justice, centre foreground
    cx, cy = x + w // 2, y + h // 2 + 4
    d.line([cx, cy - 22, cx, cy + 20], fill=GOLD, width=4)
    d.line([cx - 28, cy - 18, cx + 28, cy - 18], fill=GOLD, width=3)
    for s in (-1, 1):
        d.line([cx + s * 28, cy - 18, cx + s * 17, cy + 2], fill=GOLD, width=2)
        d.line([cx + s * 28, cy - 18, cx + s * 39, cy + 2], fill=GOLD, width=2)
        d.polygon([(cx + s * 28 - 11, cy + 2), (cx + s * 28 + 11, cy + 2),
                   (cx + s * 28, cy + 12)], fill=GOLD)
    d.ellipse([cx - 5, cy - 27, cx + 5, cy - 17], fill=GOLD)
    d.rectangle([x + 18, y + h - 12, x + w - 18, y + h - 5], fill=(120, 88, 52))
    d.text((x + 12, y + h - 30), "I C J", font=sans_b(12), fill=(255, 255, 255))


def pic_shenzhen(d, x, y, w, h):
    """Shenzhen skyline at night with three flags above a summit table."""
    vgrad(d, x, y, x + w, y + h,
          [(16, 24, 52), (30, 48, 92), (52, 82, 130), (96, 126, 168)])
    d.ellipse([x + 18, y + 8, x + 50, y + 40], fill=(255, 226, 140))
    base = y + h - 24
    towers = [(0, 50, 26), (30, 36, 24), (58, 54, 30), (92, 30, 22),
              (118, 46, 28), (150, 38, 24), (178, 56, 26), (208, 44, 24)]
    for bx, by, bw in towers:
        d.rectangle([x + bx, y + by, x + bx + bw, base], fill=(18, 28, 54))
        for wy in range(by + 7, base - y - 4, 11):
            for wx in range(bx + 5, bx + bw - 4, 10):
                if (wx * 3 + wy * 7) % 5 < 2:
                    d.rectangle([x + wx, y + wy, x + wx + 3, y + wy + 4],
                                fill=(255, 220, 130))
    # three flags on poles above the table
    for fx in (52, 116, 180):
        d.line([x + fx, base - 16, x + fx, base], fill=(220, 214, 196), width=2)
    d.rectangle([x + 52, base - 16, x + 76, base - 6], fill=(178, 32, 44))
    d.rectangle([x + 116, base - 16, x + 140, base - 6], fill=(255, 255, 255))
    d.rectangle([x + 116, base - 12, x + 140, base - 10], fill=(28, 76, 160))
    d.rectangle([x + 180, base - 16, x + 204, base - 6], fill=(200, 40, 40))
    for sx, sy in ((58, base - 14), (64, base - 11), (58, base - 8)):
        d.ellipse([x + sx, y + sy, x + sx + 3, y + sy + 3], fill=(255, 220, 90))
    # summit table
    d.rectangle([x, base, x + w, y + h], fill=(96, 62, 36))
    d.rectangle([x + 30, base - 4, x + w - 30, base], fill=(140, 96, 56))


# ---- small icon illustrations for the mini tiles (64 x 66) ----
def icon_gulf(d, x, y, w, h):
    """Night sky, a missile streak and a burst over the Gulf."""
    vgrad(d, x, y, x + w, y + h, [(20, 30, 60), (50, 70, 110), (90, 110, 150)])
    d.ellipse([x + 44, y + 8, x + 54, y + 18], fill=(255, 240, 180))
    d.line([x + 8, y + 46, x + 40, y + 18], fill=(255, 200, 90), width=3)
    d.line([x + 12, y + 52, x + 34, y + 30], fill=(255, 230, 160), width=2)
    for dx, dy, r in ((44, 34, 7), (52, 28, 5), (38, 26, 4)):
        d.ellipse([x + dx - r, y + dy - r, x + dx + r, y + dy + r],
                  fill=(255, 150, 50))
    d.rectangle([x, y + h - 12, x + w, y + h], fill=(24, 60, 96))
    d.polygon([(x + 18, y + h - 12), (x + 26, y + h - 26), (x + 34, y + h - 12)],
              fill=(40, 40, 40))


def icon_gaza(d, x, y, w, h):
    """A tank silhouette crossing sand at dawn."""
    vgrad(d, x, y, x + w, y + h, [(240, 200, 130), (226, 160, 100), (200, 130, 80)])
    d.ellipse([x + 46, y + 6, x + 58, y + 18], fill=(255, 244, 200))
    d.rectangle([x, y + h - 20, x + w, y + h], fill=(190, 150, 90))
    d.rectangle([x + 12, y + 30, x + 44, y + 44], fill=(60, 58, 50))
    d.rectangle([x + 20, y + 24, x + 34, y + 30], fill=(60, 58, 50))
    d.line([x + 34, y + 26, x + 56, y + 20], fill=(60, 58, 50), width=4)
    for wx in range(12, 46, 8):
        d.ellipse([x + wx, y + 44, x + wx + 6, y + 50], fill=(40, 38, 34))


def icon_akvan(d, x, y, w, h):
    """A cyclone spiral over a dark sea."""
    vgrad(d, x, y, x + w, y + h, [(70, 100, 140), (110, 140, 170), (150, 175, 200)])
    cx, cy = x + w // 2, y + 28
    for r in (22, 17, 12, 7):
        d.arc([cx - r, cy - r, cx + r, cy + r], start=200 - r * 8,
              end=340 - r * 8, fill=(255, 255, 255), width=3)
    d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=(255, 255, 255))
    d.rectangle([x, y + h - 14, x + w, y + h], fill=(24, 70, 110))
    d.line([x + 8, y + h - 8, x + 24, y + h - 8], fill=(255, 255, 255), width=2)
    d.line([x + 36, y + h - 5, x + 56, y + h - 5], fill=(255, 255, 255), width=2)


def icon_mongolia(d, x, y, w, h):
    """A ger (yurt) on the steppe under a big sky."""
    vgrad(d, x, y, x + w, y + h, [(120, 170, 220), (170, 200, 230), (200, 220, 200)])
    d.ellipse([x + 46, y + 8, x + 58, y + 20], fill=(255, 246, 200))
    d.rectangle([x, y + h - 16, x + w, y + h], fill=(120, 160, 90))
    d.polygon([(x + 14, y + 34), (x + 32, y + 18), (x + 50, y + 34)],
              fill=(178, 32, 44))
    d.rectangle([x + 14, y + 34, x + 50, y + 48], fill=(240, 230, 200))
    d.rectangle([x + 28, y + 34, x + 36, y + 48], fill=(120, 80, 40))
    d.line([x + 32, y + 18, x + 32, y + 12], fill=(90, 60, 30), width=2)


def icon_court(d, x, y, w, h):
    """A judge's gavel striking its block."""
    d.rectangle([x, y, x + w, y + h], fill=(28, 48, 84))
    d.rectangle([x + 16, y + 44, x + 48, y + 52], fill=(150, 110, 60))
    d.rectangle([x + 22, y + 40, x + 42, y + 44], fill=(120, 86, 44))
    d.line([x + 18, y + 34, x + 46, y + 14], fill=(190, 140, 80), width=5)
    d.rectangle([x + 40, y + 6, x + 54, y + 18], fill=(190, 140, 80))
    d.rectangle([x + 12, y + 26, x + 26, y + 38], fill=(190, 140, 80))
    d.text((x + 8, y + 54), "SEOUL", font=sans_b(9), fill=(200, 210, 230))


def icon_serbia(d, x, y, w, h):
    """A parliament dome and a crowd of raised hands."""
    vgrad(d, x, y, x + w, y + h, [(200, 220, 240), (170, 195, 220), (140, 170, 200)])
    d.rectangle([x + 12, y + 30, x + 52, y + 52], fill=(240, 236, 220))
    d.pieslice([x + 18, y + 12, x + 46, y + 34], start=180, end=360,
               fill=(178, 32, 44))
    d.line([x + 32, y + 12, x + 32, y + 6], fill=(120, 100, 70), width=2)
    for cx in (20, 28, 36, 44, 52):
        d.rectangle([x + cx - 2, y + 36, x + cx + 2, y + 46], fill=(90, 80, 60))
    for i, cx in enumerate((10, 20, 30, 40, 50, 58)):
        d.ellipse([x + cx - 4, y + 54 - (i % 2) * 3, x + cx + 4, y + 62 - (i % 2) * 3],
                  fill=(40, 60, 90))
        d.line([x + cx, y + 52 - (i % 2) * 3, x + cx + 3, y + 44 - (i % 2) * 3],
               fill=(40, 60, 90), width=2)


def icon_somalia(d, x, y, w, h):
    """A blue flag with a white star, and a departing plane."""
    vgrad(d, x, y, x + w, y + h, [(140, 190, 230), (180, 210, 240), (210, 225, 240)])
    d.line([x + 16, y + 10, x + 16, y + 52], fill=(80, 70, 60), width=3)
    d.rectangle([x + 16, y + 10, x + 46, y + 30], fill=(40, 110, 200))
    cx, cy = x + 31, y + 20
    d.polygon([(cx, cy - 6), (cx + 2, cy - 1), (cx + 7, cy - 1), (cx + 3, cy + 2),
               (cx + 4, cy + 7), (cx, cy + 4), (cx - 4, cy + 7), (cx - 3, cy + 2),
               (cx - 7, cy - 1), (cx - 2, cy - 1)], fill=(255, 255, 255))
    d.polygon([(x + 40, y + 46), (x + 58, y + 40), (x + 58, y + 46),
               (x + 48, y + 50), (x + 40, y + 50)], fill=(60, 60, 60))
    d.line([x + 44, y + 44, x + 60, y + 34], fill=(200, 200, 200), width=1)


def icon_vangogh(d, x, y, w, h):
    """Blossom tree after Van Gogh: swirling sky, white blossom."""
    vgrad(d, x, y, x + w, y + h,
          [(52, 96, 168), (84, 132, 190), (140, 176, 205), (196, 210, 160)])
    for cx, cy, r in ((12, 10, 10), (34, 8, 8), (54, 12, 9)):
        d.arc([x + cx - r, y + cy - r, x + cx + r, y + cy + r],
              start=200, end=340, fill=(250, 214, 90), width=3)
    d.rectangle([x, y + h - 16, x + w, y + h], fill=(96, 128, 52))
    d.polygon([(x + 28, y + h), (x + 31, y + 30), (x + 35, y + 30),
               (x + 38, y + h)], fill=(96, 62, 30))
    for cx, cy, r in ((24, 26, 10), (34, 20, 11), (44, 27, 10), (32, 32, 9)):
        d.ellipse([x + cx - r, y + cy - r, x + cx + r, y + cy + r],
                  fill=(74, 122, 52))
    for i in range(18):
        px_ = 14 + (i * 53) % 38
        py_ = 12 + (i * 31) % 26
        col = (255, 255, 255) if i % 3 else (244, 178, 198)
        d.ellipse([x + px_, y + py_, x + px_ + 4, y + py_ + 4], fill=col)

# ---------------------------------------------------------------- page
def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("entry.png")
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    m = 24  # margin

    # masthead
    title = "THE WORLD TODAY"
    tf = serif_b(62)
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, 14), title, font=tf, fill=INK)
    d.line([m, 90, W - m, 90], fill=INK, width=3)
    d.line([m, 95, W - m, 95], fill=INK, width=1)

    # date band
    d.rectangle([m, 102, W - m, 142], fill=RED)
    date = "THURSDAY  19  NOVEMBER  2026"
    df = sans_b(27)
    dw = d.textlength(date, font=df)
    d.text(((W - dw) / 2, 109), date, font=df, fill=(255, 255, 255))
    d.text((m + 2, 148), "ONE DAY'S WORLD NEWS", font=sans_b(12), fill=GREY)
    right = "35 STORIES  ·  6 CONTINENTS  ·  ALL VERIFIED"
    d.text((W - m - d.textlength(right, font=sans_b(12)), 148),
           right, font=sans_b(12), fill=GREY)

    # ---- four illustrated lead tiles
    leads = [
        ("GAMES  ·  VICE CITY", "GTA VI is here at last",
         "Rolls out at midnight worldwide - 99 on Metacritic, 6m watching.",
         pic_gta),
        ("MARKETS  ·  NASDAQ", "Anthropic's $81bn debut",
         "Record $81bn raise, $1.5trn valuation; trading starts today as ANT.",
         pic_anthropic),
        ("LAW  ·  THE HAGUE", "Myanmar guilty of genocide",
         "Genocide against the Rohingya, the court rules - a first for any state.",
         pic_icj),
        ("SUMMIT  ·  SHENZHEN", "Trump, Xi and Putin meet",
         "First three-way meeting agrees stable energy flows - no word on Ukraine.",
         pic_shenzhen),
    ]
    tw_ = 239
    ty, th = 166, 216
    for i, (kick, head, deck, painter) in enumerate(leads):
        x = m + i * (tw_ + 6)
        frame(d, x, ty, tw_, th)
        painter(d, x + 2, ty + 2, tw_ - 4, 100)
        d.line([x, ty + 102, x + tw_, ty + 102], fill=RULE, width=1)
        cx = x + 10
        d.text((cx, ty + 108), kick, font=sans_b(11), fill=RED)
        y = para(d, cx, ty + 126, wrap(d, head, serif_b(19), tw_ - 20),
                 serif_b(19), INK, 23)
        para(d, cx, y + 2, wrap(d, deck, sans(12), tw_ - 20), sans(12),
             (40, 38, 34), 14)

    # ---- world map with numbered pins + key
    my = 390
    d.text((m, my), "THE WORLD ON ONE MAP", font=sans_b(14), fill=RED)
    d.line([m + 188, my + 9, W - m, my + 9], fill=RULE, width=1)
    map_x, map_y, map_w, map_h = m, 404, 640, 152
    draw_map(d, map_x, map_y, map_w, map_h)
    # pin key, two columns to the right of the map
    key_x = [676, 840]
    key_items = [(f"{i}", label) for i, (_lo, _la, label) in enumerate(PINS, 1)]
    for col in range(2):
        items = key_items[col * 8:(col + 1) * 8]
        yy = map_y + 2
        for num, label in items:
            d.ellipse([key_x[col], yy + 1, key_x[col] + 13, yy + 14], fill=RED)
            nw = d.textlength(num, font=sans_b(8))
            d.text((key_x[col] + (13 - nw) / 2, yy + 2), num, font=sans_b(8),
                   fill=(255, 255, 255))
            d.text((key_x[col] + 18, yy + 1), label, font=sans(11), fill=INK)
            yy += 18
    d.text((676, map_y + 152 - 12), "15 pins: where the day happened.",
           font=sans(10), fill=GREY)

    # ---- eight illustrated mini-tiles
    ay = 564
    d.text((m, ay), "ALSO TODAY", font=sans_b(14), fill=RED)
    d.line([m + 108, ay + 9, W - m, ay + 9], fill=RULE, width=1)
    minis = [
        ("Gulf strikes", "Iran fires on a US base in Kuwait; US hits "
         "Qeshm Island.", icon_gulf),
        ("Gaza tank raid", "Israel crosses the ceasefire line; some 6,000 "
         "people flee.", icon_gaza),
        ("Cyclone Akvan", "70,000+ moved to safety in Odisha as the storm "
         "nears.", icon_akvan),
        ("Mongolia quits", "President Khurelsukh resigns over a railway "
         "scandal.", icon_mongolia),
        ("Seoul court", "Court voids Han's 15-year term; martial law "
         "unconstitutional.", icon_court),
        ("Serbia turns", "Student-led Cupic elected speaker, ending the "
         "14-year grip.", icon_serbia),
        ("Somalia expels", "UAE envoy given 72 hours to leave in a "
         "sovereignty row.", icon_somalia),
        ("Van Gogh $190.4m", "Chestnut Trees in Blossom sets an artist "
         "record at Sotheby's.", icon_vangogh),
    ]
    mw, mh = 239, 64
    for i, (head, sub, painter) in enumerate(minis):
        row, col = divmod(i, 4)
        x = m + col * (mw + 6)
        y = ay + 24 + row * (mh + 4)
        frame(d, x, y, mw, mh, width=1)
        painter(d, x + 1, y + 1, 62, mh - 2)
        tx = x + 68
        yy = para(d, tx, y + 5, wrap(d, head, sans_b(12), mw - 74),
                  sans_b(12), INK, 14)
        para(d, tx, yy + 1, wrap(d, sub, sans(10), mw - 74), sans(10),
             (60, 58, 52), 12)

    # ---- the day in brief: 23 items, 3 columns
    byy = 726
    d.text((m, byy), "THE DAY IN BRIEF", font=sans_b(14), fill=RED)
    d.line([m + 158, byy + 9, W - m, byy + 9], fill=RULE, width=1)
    brief = [
        ("US SENATE", "Rejects War Powers bid to end the Iran war, 51-48."),
        ("BERLIN", "Leaders reaffirm Ukraine backing; Macron: reopen Kyiv's NATO question."),
        ("IRAQ", "Baghdad deal with Kataib Hezbollah averts a Jurf al-Sakhar clash."),
        ("LONDON", "Tribunal confirms the state ordered Apple to open encrypted data."),
        ("COLORADO", "Judge holds ICE officials in contempt over a re-arrest."),
        ("GUYANA", "Ex-Trump aide's Essequibo idea alarms; US says policy unchanged."),
        ("HAITI", "Florida pastor convicted over President Moise's assassination."),
        ("KOREA EXAM", "550,000 sit the college test amid AI-cheating fears."),
        ("NVIDIA", "Board rejects Huang's CEO comeback; revenue doubles to $115.8bn."),
        ("MUSK", "Says he felt 'pretty foolish' over midterm spending scale."),
        ("COP31", "Climate talks drop fossil-fuel language from the text."),
        ("INDONESIA", "A strong El Nino fuels severe wildfires."),
        ("GULF", "Two US aircraft carriers depart the Middle East."),
        ("HORN", "Ethiopia and Eritrea mass forces at the border; Badme clashes reported."),
        ("DHAKA", "Garment workers protest into a third week over pay."),
        ("KNESSET", "Matan Kahana elected speaker with 66 votes."),
        ("RIYADH", "Houthi missile dealt with; IEA warns on Hormuz energy."),
        ("UK-EU", "London and Brussels meet to rebuild post-Brexit ties."),
        ("BRAZIL", "Rare images of an isolated Indigenous group released."),
        ("AIR NZ", "Charged with misleading flyers over compensation rights."),
        ("WELLINGTON", "Nicholls' 113* rescues NZ v India, 243/5 on day one."),
        ("TOKYO-DELHI", "Japan and India deepen military ties; joint training agreed."),
        ("ARCTIC", "Denmark approves a US-Greenland defence deal."),
    ]
    col_w = 312
    col_x = [m, m + col_w + 20, m + 2 * (col_w + 20)]
    cols = [brief[:8], brief[8:16], brief[16:]]
    for col, items in enumerate(cols):
        y = byy + 22
        for lead, text in items:
            lead_f, body_f = sans_b(12), sans(12)
            lines = wrap(d, f"{lead} - {text}", body_f, col_w)
            lead_w = d.textlength(lead + " - ", font=lead_f)
            d.text((col_x[col], y), lead + " - ", font=lead_f, fill=INK)
            d.text((col_x[col] + lead_w, y), lines[0][len(lead) + 3:],
                   font=body_f, fill=(40, 38, 34))
            yy = y + 13
            for extra in lines[1:]:
                d.text((col_x[col], yy), extra, font=body_f, fill=(40, 38, 34))
                yy += 13
            y = yy + 2

    # footer
    d.line([m, 978, W - m, 978], fill=RULE, width=1)
    foot = ("Sources: Reuters  ·  AP  ·  BBC  ·  The Guardian  ·  SCMP  ·  IMD  ·  ANI    —    "
            "All stories of, or first reported on, Thursday 19 November 2026.")
    ff = sans(11)
    fw = d.textlength(foot, font=ff)
    d.text(((W - fw) / 2, 988), foot, font=ff, fill=GREY)

    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, format="PNG", optimize=True)
    print(f"wrote {out} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
