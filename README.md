# PMS Database ●11 — Mocha clear-rate folders

**[Open / import the table](https://sehun-joo.github.io/pms11-clear-rate/)**

All **485 level 11 charts** in the larger PMS Database snapshot, regrouped into player-clear-rate folders. Add the page URL to your BMS/PMS player's difficulty-table settings.

Snapshot date: **2026-10-23**. Rates are not live. This does not alter the original difficulty table or any local song files.

## Calculation

1. Use the public Mocha chart page's **TOTAL USER / CLEAR USER / RATE** statistics. The first RATE is the player rate; the second is the per-play rate and is not used.
2. Where no usable player rate is displayed, use `(CLEAR + HARD + EX-HARD + FULL COMBO) / all players × 100`, but only when complete public lamp data is available. This fallback excludes Easy/Assist and follows the requested four lamp categories literally.
3. Zero players, missing statistics, incomplete lamp data or retrieval failures belong in **No data**, never the 0% band.

Mocha's displayed rate is used as published. Its underlying lamp threshold is not assumed to equal the fallback formula. `rate_method` distinguishes the two; `mocha-stats.json` records the observed numerator, denominator, displayed percentage, URL, chart title and retrieval status. Rates are rounded by Mocha; folders follow the displayed value rather than inventing extra precision.

The 10-point bands are **90–100%, 80–under 90%, …, 0–under 10%**, in descending order, followed by No data. Exact 90% belongs in the top band, exact 80% in the next, and so on. The browser sorts within each band by rate descending, then player count descending. A player's own within-folder sort may differ. Samples below 10 players are marked but remain in their rate band; the browser can filter for larger samples.

## Source coverage and identity

- [PMS Database insane page](https://pmsdifficulty.xxxxxxxx.jp/insane_PMSdifficulty.html)
- [PMS Database score JSON](https://pmsdatabase.github.io/insane_pmsdatabase/insane_pmsdatabase_score.json)
- [Mocha IR](https://mocha-repository.info/), with each chart's public `song.php?sha256=…` URL recorded individually.

`source-level11.json` preserves every source row whose level is exactly 11. All have SHA-256 hashes, so Mocha lookups use chart hashes, not ambiguous title searches. This is the larger database requested, including entries marked removed from its smaller curated counterpart. The original source fields, hashes, credits and download links remain intact; the custom table replaces the level with a rate band, preserves `original_level: "11"`, and adds dated statistics to the comment.

Only aggregate chart statistics are published, not player names or rankings. The collector reads public HTML pages; it does not call private IR APIs. The newer Mocha landing page requires login to explore; this snapshot uses the publicly accessible original Mocha chart pages. Browser filters do not change imported coverage. Rates reflect Mocha participants and are a guide to selection, not a calibrated difficulty measure.

## Rebuild

Python 3 standard library only:

```sh
python build.py --base-url https://sehun-joo.github.io/pms11-clear-rate
```

The build consumes committed snapshots and makes no network requests. GitHub Pages publishes `dist` through the included workflow. Refresh the source and aggregate statistics together after reviewing collection results; do not replace unavailable rates with zero.

Independent fan table. Chart files and audio are not hosted; use the original credited download links.
