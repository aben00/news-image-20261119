#!/usr/bin/env python3
"""Draw the news-image-20261119 entry: a newspaper front page, THE WORLD TODAY,
summing up Thursday 19 November 2026 in 20 verified stories.

Deterministic: fixed seed, no clock, no network, no randomness at draw time.
Run:  python3 draw.py [output-path]   (default: entry.png beside this file)
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 229)
INK = (20, 20, 20)
RED = (178, 32, 44)
BLUE = (29, 78, 137)
TEAL = (18, 110, 105)
GOLD = (201, 154, 39)
GREY = (90, 86, 76)
RULE = (60, 56, 48)

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")


def font(name, size):
    return ImageFont.truetype(str(FONT_DIR / name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(d, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
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


def band(d, x0, y0, x1, y1, colours):
    """Vertical gradient made of horizontal bands."""
    n = len(colours)
    h = y1 - y0
    for i, c in enumerate(colours):
        d.rectangle([x0, y0 + i * h // n, x1, y0 + (i + 1) * h // n], fill=c)


def tile_frame(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], outline=RULE, width=2)
    d.line([x, y, x + w, y], fill=INK, width=2)


# ---------------------------------------------------------------- pictures
def pic_gta(d, x, y, w, h):
    """Vice City at dusk: orange-purple sky, sun, skyline, palms, water."""
    band(d, x, y, x + w, y + h,
         [(46, 24, 74), (94, 38, 96), (176, 62, 90), (232, 116, 64),
          (247, 168, 92), (250, 205, 130)])
    d.ellipse([x + w - 108, y + 14, x + w - 48, y + 74], fill=(255, 214, 130))
    d.ellipse([x + w - 100, y + 22, x + w - 56, y + 66], fill=(255, 236, 180))
    # skyline
    skyline = [(0, 88, 34, 118), (40, 66, 70, 118), (76, 96, 104, 118),
               (110, 58, 146, 118), (152, 84, 182, 118), (188, 70, 214, 118),
               (220, 94, 250, 118), (256, 78, 288, 118), (292, 100, 320, 118)]
    for bx0, by0, bx1, _ in skyline:
        d.rectangle([x + bx0, y + by0, x + bx1, y + 118], fill=(30, 16, 52))
        for wy in range(by0 + 10, 114, 14):
            for wx in range(bx0 + 6, bx1 - 4, 12):
                if (wx * 7 + wy * 3) % 5 < 2:
                    d.rectangle([x + wx, y + wy, x + wx + 4, y + wy + 5],
                                fill=(255, 214, 120))
    # water
    d.rectangle([x, y + 118, x + w, y + h], fill=(24, 48, 92))
    for i in range(6):
        d.line([x + 12 + i * 52, y + 126 + i * 3, x + 52 + i * 52, y + 126 + i * 3],
               fill=(255, 190, 110), width=2)
    # palm silhouettes: curved trunks, drooping fronds
    for px, ph in ((30, 52), (292, 60)):
        d.line([x + px, y + 118, x + px + 5, y + 118 - ph], fill=(16, 10, 30), width=5)
        top = (x + px + 5, y + 118 - ph)
        for dx, dy in ((-26, 2), (-20, -12), (-8, -20), (6, -22), (18, -14), (26, -2)):
            d.line([top, (top[0] + dx, top[1] + dy)], fill=(16, 10, 30), width=3)


def pic_anthropic(d, x, y, w, h):
    """A share-price chart rocketing up on a dark board, ANT ticker."""
    d.rectangle([x, y, x + w, y + h], fill=(14, 28, 54))
    for gy in range(y + 18, y + h - 8, 24):
        d.line([x + 8, gy, x + w - 8, gy], fill=(38, 62, 100), width=1)
    bars = [22, 30, 26, 40, 48, 44, 62, 74, 70, 92, 108, 128]
    bw = (w - 32) // len(bars)
    for i, bh in enumerate(bars):
        bx = x + 16 + i * bw
        col = (46, 190, 120) if i > 5 else (90, 140, 200)
        d.rectangle([bx, y + h - 12 - bh, bx + bw - 5, y + h - 12], fill=col)
    pts = [(x + 16 + i * bw, y + h - 20 - bh) for i, bh in enumerate(bars)]
    d.line(pts, fill=(255, 255, 255), width=3, joint="curve")
    for px_, py_ in pts[::3]:
        d.ellipse([px_ - 4, py_ - 4, px_ + 4, py_ + 4], fill=(255, 255, 255))
    d.text((x + 14, y + 10), "ANT", font=SANS_B(30), fill=(255, 255, 255))
    d.text((x + 14, y + 44), "NASDAQ", font=SANS_B(13), fill=(140, 170, 220))


def pic_vangogh(d, x, y, w, h):
    """Chestnut Trees in Blossom, after Van Gogh: swirling sky, blossom tree."""
    band(d, x, y, x + w, y + h,
         [(52, 96, 168), (84, 132, 190), (140, 176, 205), (196, 210, 160)])
    # thin swirl arcs high in the sky
    for cx, cy, r, col in ((52, 26, 30, (250, 214, 90)), (120, 18, 24, (255, 236, 150)),
                           (262, 22, 28, (250, 214, 90))):
        d.arc([x + cx - r, y + cy - r, x + cx + r, y + cy + r],
              start=200, end=340, fill=col, width=4)
    # sun, top right, clear of the tree
    d.ellipse([x + w - 66, y + 8, x + w - 26, y + 48], fill=(255, 222, 110))
    # ground
    d.rectangle([x, y + 118, x + w, y + h], fill=(96, 128, 52))
    d.rectangle([x, y + 118, x + w, y + 123], fill=(70, 96, 38))
    # trunk, leaning slightly, fully visible
    d.polygon([(x + 148, y + h), (x + 156, y + 74), (x + 166, y + 74),
               (x + 176, y + h)], fill=(96, 62, 30))
    d.line([x + 156, y + 96, x + 132, y + 72], fill=(96, 62, 30), width=6)
    d.line([x + 166, y + 90, x + 192, y + 68], fill=(96, 62, 30), width=6)
    # blossom canopy: modest clusters around the crown, sky still visible
    blobs = [(112, 62, 30), (160, 46, 34), (206, 60, 30), (132, 84, 26),
             (188, 84, 26), (160, 74, 30)]
    for cx, cy, r in blobs:
        d.ellipse([x + cx - r, y + cy - r, x + cx + r, y + cy + r], fill=(74, 122, 52))
    for i in range(64):
        px_ = 84 + (i * 137) % 152
        py_ = 26 + (i * 89) % 76
        col = (255, 255, 255) if i % 3 else (244, 178, 198)
        d.ellipse([x + px_, y + py_, x + px_ + 5, y + py_ + 5], fill=col)


# ---------------------------------------------------------------- page
def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("entry.png")
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    m = 24  # margin

    # masthead
    title = "THE WORLD TODAY"
    tf = SERIF_B(64)
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, 14), title, font=tf, fill=INK)
    d.line([m, 92, W - m, 92], fill=INK, width=3)
    d.line([m, 97, W - m, 97], fill=INK, width=1)

    # date band
    d.rectangle([m, 104, W - m, 144], fill=RED)
    date = "THURSDAY  19  NOVEMBER  2026"
    df = SANS_B(27)
    dw = d.textlength(date, font=df)
    d.text(((W - dw) / 2, 111), date, font=df, fill=(255, 255, 255))
    d.text((m + 2, 150), "ONE DAY'S WORLD NEWS", font=SANS_B(12), fill=GREY)
    right = "20 STORIES  ·  ALL VERIFIED"
    d.text((W - m - d.textlength(right, font=SANS_B(12)), 150),
           right, font=SANS_B(12), fill=GREY)

    # ---- three lead tiles
    tiles = [
        ("GAMES  ·  VICE CITY", "GTA VI is here at last",
         "Rockstar's epic rolls out at midnight around the world, 13 years "
         "after GTA V - and scores 99 on Metacritic.", pic_gta),
        ("MARKETS  ·  NASDAQ", "Anthropic's $81bn debut",
         "Claude-maker prices its IPO at $83 a share - the biggest listing "
         "ever - and starts trading today as ANT.", pic_anthropic),
        ("ART  ·  NEW YORK", "Van Gogh sells for $190.4m",
         "Chestnut Trees in Blossom sets an artist record at Sotheby's after "
         "a Nazi-era ownership row is settled.", pic_vangogh),
    ]
    tw_ = 314
    ty, th = 172, 296
    for i, (kick, head, deck, painter) in enumerate(tiles):
        x = m + i * (tw_ + 11)
        tile_frame(d, x, ty, tw_, th)
        painter(d, x + 2, ty + 2, tw_ - 4, 148)
        d.line([x, ty + 150, x + tw_, ty + 150], fill=RULE, width=1)
        cx = x + 12
        d.text((cx, ty + 158), kick, font=SANS_B(12), fill=RED)
        y = para(d, cx, ty + 178, wrap(d, head, SERIF_B(23), tw_ - 24),
                 SERIF_B(23), INK, 27)
        para(d, cx, y + 4, wrap(d, deck, SANS(13), tw_ - 24), SANS(13), (40, 38, 34), 17)

    # ---- also today: four secondary stories
    ay = 484
    d.text((m, ay), "ALSO TODAY", font=SANS_B(14), fill=RED)
    d.line([m + 108, ay + 9, W - m, ay + 9], fill=RULE, width=1)
    second = [
        ("ICJ VERDICT DUE", "The Hague rules today on Myanmar and the Rohingya",
         "The Gambia v. Myanmar, 10:00"),
        ("SUMMIT IN SHENZHEN", "Trump, Xi and Putin meet for the first time",
         "Trilateral talks at APEC"),
        ("CRIMEAN BRIDGE", "Hit a third time in a week; traffic halted",
         "Russia blames Ukraine"),
        ("CYCLONE AKVAN", "Severe storm bears down on India's east coast",
         "Red alerts; landfall due Fri"),
    ]
    bw = 238
    by = ay + 26
    bh = 104
    for i, (kick, head, sub) in enumerate(second):
        x = m + i * (bw + 6)
        d.rectangle([x, by, x + bw, by + bh], outline=RULE, width=1)
        d.rectangle([x, by, x + bw, by + 22], fill=BLUE)
        d.text((x + 8, by + 4), kick, font=SANS_B(11), fill=(255, 255, 255))
        y = para(d, x + 8, by + 30, wrap(d, head, SANS_B(13), bw - 16),
                 SANS_B(13), INK, 16)
        d.text((x + 8, by + bh - 18), sub, font=SANS(11), fill=GREY)

    # ---- the day in brief
    byy = 630
    d.text((m, byy), "THE DAY IN BRIEF", font=SANS_B(14), fill=RED)
    d.line([m + 158, byy + 9, W - m, byy + 9], fill=RULE, width=1)
    brief = [
        ("McDONALD'S UK", "Judge lets 450 workers' cases go ahead over teen safety."),
        ("VOYAGER 1", "NASA briefs today on the probe, now a full light-day away."),
        ("CHINA SHIPS", "US panel urges Congress to punish Beijing over Panama-flagged detentions."),
        ("TECH OUTAGES", "Senate minority leader seeks a security probe."),
        ("PUNE", "Food watchdog seizes 20,085 litres of substandard oil."),
        ("CENSUS 2027", "'Other' religions list goes predictive; 200+ entries dropped."),
        ("INDIA POLITICS", "BJP turns to the Mathura temple issue amid cadre unease."),
        ("KOCHI", "City spends Rs 4 crore a year on 2,000 defunct public taps."),
        ("HYDERABAD", "A 35-km personal rapid transit network is explored."),
        ("PROFITS", "Wall Street banks see global profit growth slowing to 16%."),
        ("BONDS", "Fitch warns the AI debt boom could jolt corporate bonds."),
        ("OUTAGES", "US service failures spark stockpiling of essentials."),
        ("TAIWAN", "DPP aims to hold five cities in local elections."),
    ]
    col_w = 478
    col_x = [m, m + col_w + 20]
    left, right = brief[:7], brief[7:]
    for col, items in enumerate((left, right)):
        y = byy + 28
        for lead, text in items:
            lead_f, body_f = SANS_B(14), SANS(14)
            first = f"{lead} - {text}"
            lines = wrap(d, first, body_f, col_w)
            # bold the lead-in on the first line
            lead_w = d.textlength(lead + " - ", font=lead_f)
            d.text((col_x[col], y), lead + " - ", font=lead_f, fill=INK)
            d.text((col_x[col] + lead_w, y), lines[0][len(lead) + 3:],
                   font=body_f, fill=(40, 38, 34))
            yy = y + 18
            for extra in lines[1:]:
                d.text((col_x[col], yy), extra, font=body_f, fill=(40, 38, 34))
                yy += 18
            y = yy + 12

    # footer
    d.line([m, 978, W - m, 978], fill=RULE, width=1)
    foot = ("Sources: Reuters  ·  AP  ·  BBC  ·  The New York Times  ·  The Hindu  ·  SCMP  ·  NASA  ·  IMD    —    "
            "All stories of, or first reported on, Thursday 19 November 2026.")
    ff = SANS(11)
    fw = d.textlength(foot, font=ff)
    d.text(((W - fw) / 2, 988), foot, font=ff, fill=GREY)

    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, format="PNG", optimize=True)
    print(f"wrote {out} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
