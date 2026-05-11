# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

All scripts must be run from the repo root with the virtualenv active:

```bash
source .venv/bin/activate
```

Run a script:
```bash
python scripts/build_interactive_map.py   # regenerate the interactive HTML map
python scripts/build_ugpi.py              # recompute UGPI scores → ugpi_final.gpkg
python scripts/build_social_vulnerability.py
python scripts/build_green_space.py       # requires CDSE_USERNAME / CDSE_PASSWORD env vars
python scripts/build_heat.py              # requires CDSE_USERNAME / CDSE_PASSWORD env vars
```

Install dependencies:
```bash
pip install -r requirements.txt
```

There are no tests or linters configured.

## Architecture

The pipeline runs in strict dependency order — each stage writes a GeoPackage that the next stage reads:

```
data/raw/  (shapefiles, CSVs, GeoTIFFs)
    │
    ├─ build_social_vulnerability.py  →  data/processed/social_vulnerability.gpkg
    ├─ build_green_space.py           →  data/processed/green_space.gpkg
    ├─ build_heat.py                  →  data/processed/heat.gpkg
    │
    └─ build_ugpi.py   (joins the three above)
                       →  data/processed/ugpi_final.gpkg
                       →  outputs/06_ugpi_final.png  +  outputs/06_ugpi_panel.png
                              │
                              └─ build_interactive_map.py
                                 →  outputs/ugpi_interactive_map.html
```

**`build_interactive_map.py`** is the most complex script and the one most actively developed. Its structure:

- `load_and_prepare()` — reads `ugpi_final.gpkg`, simplifies geometry, reprojects to EPSG:4326, adds a `District` column (from `MUNDISSEC[6:8]` mapped via `DISTRICT_NAMES`), a `Label` column (`"District · TXXX"`), and pre-formatted string columns (`_ugpi`, `_heat`, etc.) for display.
- Large HTML string constants (`INFO_PANEL_HTML`, `LEGEND_HTML`, `TOP20_PANEL_HTML`, `EXPORT_BTN_HTML`, `POPUP_CSS`) — injected verbatim into the map as Folium `Element`s.
- `LAYER_TOGGLE_JS_TEMPLATE` — a Python triple-quoted string containing the entire Leaflet/JS logic. It uses `.format(layer_var=geojson_layer.get_name())` so all literal JS braces must be doubled (`{{` / `}}`). Use `\\'` (not `\'`) inside this string to produce a JS single-quote escape — Python consumes a single backslash, so `\'` becomes `'` which breaks JS string literals.
- `build_map()` — assembles the Folium map, injects district GeoJSON inline as `<script>var _districtData = ...;</script>`, adds all HTML/JS elements, then adds the formatted JS template last.

**Key JS architecture inside `LAYER_TOGGLE_JS_TEMPLATE`:**

- `_activeKey` tracks the current layer (`'ugpi'`, `'heat'`, `'green'`, `'social'`).
- `_replaceHoverHandlers()` — replaces Folium's baked-in highlight handlers (which hardcode the UGPI colormap) with closures that read `_activeKey` at runtime.
- `_districtLayer` / `_inDistrictView` — district choropleth state; district GeoJSON is stored in `window._districtData` injected from Python.
- Weight recalculation updates `p.UGPI` and `p._ugpi` in-place on each feature's properties so the export CSV always reflects current weights.

**Scoring convention:** all three component scores and UGPI are normalised to 1–10 where 10 = highest priority / most critical. UGPI = weighted mean of Heat Score, Green Space Deficit Score, and Social Vulnerability Score (default equal weights 33/33/34).

**`MUNDISSEC` field:** a string identifier where characters at index 6–7 are the 2-digit district code (`"01"`–`"10"`), used throughout all scripts to map tracts to districts.
