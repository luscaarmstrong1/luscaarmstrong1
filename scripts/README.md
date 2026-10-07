# Profile art maintenance

Run from the repository root using Python 3.12:

```sh
pip install -r scripts/requirements.txt
python scripts/fetch_contributions.py
python scripts/render_heatmap_svg.py
python scripts/make_info_card.py
python scripts/validate.py
python -m unittest discover -s scripts -p 'test_*.py'
```

Replace assets/source-photo.png with your own photograph, then:

```sh
pip install -r scripts/requirements-portrait.txt
python scripts/prep_photo.py
python scripts/make_ascii_svg.py
```

rembg downloads its model on first use. If unavailable, preprocessing retains the background and reports a warning. Use --skip-rembg to bypass deliberately. Gentle CLAHE preserves facial tones.

Edit ROWS in make_info_card.py. Facts come from the existing professional profile and public repository manifests/languages.

Set STATIC=1 to generate without animation. PowerShell: $env:STATIC='1'; regenerate; Remove-Item Env:STATIC. SVG base attributes show the final frame. SMIL plays once and freezes; reduced-motion shows the final frame. Reopening may replay animation. GitHub caches images, so updates may appear with a delay. The two-column table may remain compact on small screens.

The scraper supports data-count, tooltips and accessibility labels/descriptions. Missing dates, conflicting cells or unknown counts fail without replacing valid JSON. GitHub levels are preserved. Calendar totals cover the displayed range; last_year covers exactly the final 365 dates. Current streak allows the final day to remain zero while in progress. Public calendar may include anonymous private contributions if enabled by the account. Best-day ties choose the earliest date. Monthly totals include partial edge months. No changing fetch timestamp is stored, avoiding unchanged-data commits.

Open SVGs in a browser to review animation. Actions → Update profile art → Run workflow → main. Scheduled at 06:17 UTC (03:17 São Paulo). Jobs are serialized and stage only JSON and heatmap. No custom token required.

Previous profile: docs/previous-profile.md. Original SVGs remain in assets/. Previous snake workflow retains manual dispatch only.
