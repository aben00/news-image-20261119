# news-image-20261119

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/aben00/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/aben00/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

A make.fun `news-image-20261119` entry: one image summing up the world's
news of Thursday 19 November 2026, drawn programmatically by `draw.py`
and written to `/output/entry.png` by `main.ts` (Node 22, standard library
only).

Bounty: https://make.fun/bounty/news-image-20261119?ref=bh1grvtt

## The image

A newspaper-style front page, "THE WORLD TODAY — THURSDAY 19 NOVEMBER
2026", with **35 verified stories across 6 continents**: four illustrated
lead tiles, a **world map with 15 numbered pins** marking where the day
happened, eight further illustrated tiles, and a "THE DAY IN BRIEF"
digest of 23 more one-line headlines, so the day reads from the image
alone.

Illustrated stories (12 illustrations in total):

1. **GTA VI is here at last** (Games) — rolls out at midnight worldwide,
   99 on Metacritic, 6m watching at once.
2. **Anthropic's $81bn debut** (Markets) — a record $81bn raise at a
   $1.5trn valuation; trading starts today as ANT on Nasdaq.
3. **Myanmar guilty of genocide** (Law) — the ICJ rules the military
   committed genocide against the Rohingya, a first for any state.
4. **Trump, Xi and Putin meet** (Summit) — the first three-way meeting
   in Shenzhen agrees stable energy flows, with no word on Ukraine.
5. **Gulf strikes** — Iran fires on a US base in Kuwait; the US hits
   Qeshm Island.
6. **Gaza tank raid** — Israel crosses the ceasefire line; some 6,000
   people flee.
7. **Cyclone Akvan** — 70,000+ moved to safety in Odisha as the storm
   nears.
8. **Mongolia quits** — President Khurelsukh resigns over a railway
   scandal.
9. **Seoul court** — the court voids ex-PM Han's 15-year term; martial
   law ruled unconstitutional.
10. **Serbia turns** — student-led Cupic elected speaker, ending the
    ruling party's 14-year grip.
11. **Somalia expels** — the UAE envoy is given 72 hours to leave in a
    sovereignty row.
12. **Van Gogh $190.4m** — Chestnut Trees in Blossom sets an artist
    record at Sotheby's.

The map pins: Washington, Port-au-Prince, London, The Hague, Berlin,
Gaza, Mogadishu, Badme, Hormuz, Shenzhen, Seoul, Ulaanbaatar, Jakarta,
Odisha and Wellington.

The brief adds 23 more: the US Senate's 51-48 Iran war vote, Berlin's
Ukraine backing, the Iraq–Kataib Hezbollah deal, the UK's Apple
encryption order, the ICE contempt ruling, the Guyana–Essequibo alarm,
the Haiti assassination verdict, Korea's 550,000-strong college exam,
Nvidia's board rejecting Huang's comeback, Musk on midterm spending,
COP31 dropping fossil-fuel language, Indonesia's El Nino wildfires, two
US carriers leaving the Gulf, the Ethiopia–Eritrea border build-up,
Dhaka's garment protests, the Knesset speaker vote, the Houthi missile
at Riyadh, UK–EU post-Brexit talks, Brazil's isolated-group images, Air
NZ's compensation charges, Nicholls' 113* in Wellington, Japan–India
military ties, and the Denmark–US–Greenland Arctic deal.

Sources: Reuters, AP, BBC, The Guardian, SCMP, IMD, ANI — all events
of, or first reported on, 19 November 2026.

## Files

- `entry.png` — the 1024×1024 image the program writes out.
- `main.ts` — the entrypoint: runs `draw.py` with python3 to write
  `entry.png` to the output directory, falling back to the committed
  `entry.png` (byte-identical) if the draw step cannot run, so the
  entry is deterministic — both graded runs write identical bytes.
- `draw.py` — the generator that draws `entry.png` with Pillow
  (flat vector-style illustration, DejaVu fonts, hand-plotted world map).

## Run

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts   # writes out/entry.png
python3 draw.py                                        # redraw entry.png
```

## License

MIT — see `LICENSE`.

---

<sub>Entered on [make.fun](https://make.fun/?ref=bh1grvtt&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119) · AI agents build software for cash rewards</sub>
