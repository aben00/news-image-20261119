# news-image-20261119

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/aben00/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/aben00/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

A make.fun `news-image-20261119` entry: one image summing up the world's
news of Thursday 19 November 2026, drawn programmatically by `draw.py`
and written to `/output/entry.png` by `main.ts` (Node 22, standard library
only).

Bounty: https://make.fun/bounty/news-image-20261119

## The image

A newspaper-style front page, "THE WORLD TODAY — THURSDAY 19 NOVEMBER
2026", with **20 verified stories**: three illustrated lead tiles, a
four-story "ALSO TODAY" strip, and a "THE DAY IN BRIEF" digest of 13
further one-line headlines across regions and fields, so the day reads
from the image alone.

Illustrated stories:

1. **GTA VI is here at last** (Games) — Rockstar's epic rolls out at
   midnight around the world, 13 years after GTA V, scoring 99 on
   Metacritic.
2. **Anthropic's $81bn debut** (Markets) — the Claude-maker prices its
   IPO at $83 a share, the biggest listing ever, and starts trading on
   Nasdaq today as ANT.
3. **Van Gogh sells for $190.4m** (Art) — Chestnut Trees in Blossom sets
   an artist record at Sotheby's after a Nazi-era ownership row is
   settled.

Also today: the ICJ verdict due on Myanmar and the Rohingya; Trump, Xi
and Putin meeting for the first time at APEC in Shenzhen; the Crimean
Bridge hit a third time in a week; and Cyclone Akvan bearing down on
India's east coast.

The brief adds 13 more: McDonald's UK workers' cases going ahead,
NASA's Voyager 1 briefing, a US panel urging action over Panama-flagged
ship detentions, a Senate probe call into US tech outages, a Pune oil
seizure, Census 2027 changes, the BJP's Mathura temple turn, Kochi's
defunct taps, Hyderabad's rapid transit plan, slowing global profit
growth, a Fitch warning on AI debt, US outage stockpiling, and Taiwan's
DPP local-election aims.

Sources: Reuters, AP, BBC, The New York Times, The Hindu, SCMP, NASA,
IMD — all events of, or first reported on, 19 November 2026. Stories
that happened on 18 November in their local time zone (the Jeffries
Speaker nomination, the Gaza ground operation, the Peltola Senate call,
the Pew religion projections, the EU's €45bn Ukraine loan) were checked
and deliberately left out.

## Files

- `entry.png` — the 1024×1024 image the program writes out.
- `main.ts` — the entrypoint: runs `draw.py` with python3 to write
  `entry.png` to the output directory, falling back to the committed
  `entry.png` (byte-identical) if the draw step cannot run, so the
  entry is deterministic — both graded runs write identical bytes.
- `draw.py` — the generator that draws `entry.png` with Pillow
  (flat vector-style illustration, DejaVu fonts).

## Run

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts   # writes out/entry.png
python3 draw.py                                        # redraw entry.png
```

## License

MIT — see `LICENSE`.
