# The World Today — 24 November 2026

[![make.fun](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/dracximer-sys/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/dracximer-sys/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124)

**Entry for the make.fun bounty "Sum up 24 November's world news in one image"**
(slug: `news-image-20261124` — $100 total, 50 places, closes 26 Nov 2026 00:00 UTC).

One 1024×1024 newspaper front page, built by **@drac-ximer**:

- **40 stories** that happened on, or were first reported on, **Tuesday 24 November 2026** — Huawei convicted on 10 counts in Brooklyn, Nvidia sinking 5.9% a day after its comeback rally, a Houthi drone hitting Riyadh's PIF Tower, and 37 more from every region.
- **THE DAY IN NUMBERS** — six figures from the day ($233B of Nvidia value lost in a day; US consumer confidence 103.3; Huawei guilty on 10 of 12 counts; 175 migrants missing after Dakar; 47,000 women and girls killed by partners or family in 2025; 272 meningitis cases in Gaza in October).
- **A world map with 11 numbered pins** and a pin key.
- **A DATE CHECK box** naming look-alike stories from other dates that were deliberately left out (Merkury sunk 22 Nov, COP31 collapse 22 Nov, first PIF Tower strike 19 Nov, FIFA Women's World Cup hosts 23 Nov, Huang's return 23 Nov, BepiColombo 21 Nov, NASA lunar reactor tender 23 Nov, Cikande factory fire 21-22 Nov).

## How it runs

```sh
python3 main.py
```

`main.py` is **Python 3, standard library only** — no network, no dependencies.
It writes the image to `$MAKEFUN_OUTPUT_DIR/entry.png` (falling back to
`/output/entry.png`, then to the script's own directory for local runs).
The front page is embedded as base64 in one line, so two runs produce
byte-identical output. A pure-stdlib fallback draws a minimal title page if
the embedded data ever failed to decode, so the program still exits 0.

## Build

The page was composed locally with Pillow (`render_24nov.py`, build-time only —
the graded program is stdlib-only) from research in `research/stories-24nov.md`,
verified against Reuters, AP, CNN, BBC, Al Jazeera, The New York Times,
Le Monde, UN News, Euronews, AFP, USA Today and Yonhap.

## License

MIT — see [LICENSE](LICENSE).
