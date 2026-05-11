# Urban Greening Priority Index (UGPI) — Barcelona

A decision support tool for Barcelona city planners that combines satellite imagery and census data into a single priority score (1–10) for every census tract in the city, identifying where green infrastructure investment is most urgently needed.

**Live site:** https://gaelmensa.github.io/ugpi-barcelona

---

## What it does

The UGPI assigns a composite priority score to each of Barcelona's 1,068 census tracts by combining three data layers:

- **Heat Score** — Land Surface Temperature from Landsat 8 thermal imagery (Summer 2023, 30m)
- **Green Space Deficit Score** — Inverted NDVI from Sentinel-2 imagery (Summer 2023, 10m)
- **Social Vulnerability Score** — Elderly population share + inverse disposable income per capita

Default weights: 33% Heat + 33% Green Space Deficit + 34% Social Vulnerability. All weights are adjustable in real time in the interactive map.

The interactive map lets planners toggle between layers, adjust weights, filter by priority threshold, compare individual tracts, simulate greening interventions, and export results as CSV.

---

## Repository structure

```
ugpi-barcelona/
├── data/
│   ├── raw/              # Census shapefiles, CSVs, satellite GeoTIFFs
│   └── processed/        # ugpi_final.gpkg — master output (1,068 tracts, 17 columns)
├── docs/                 # GitHub Pages website (HTML pages + interactive map)
│   └── ugpi_interactive_map.html
├── scripts/              # Python pipeline (run in order)
│   ├── build_social_vulnerability.py
│   ├── build_green_space.py
│   ├── build_heat.py
│   ├── build_ugpi.py
│   └── build_interactive_map.py
├── requirements.txt
└── README.md
```

---

## How to run

### 1. Clone and set up

```bash
git clone https://github.com/gaelmensa/ugpi-barcelona.git
cd ugpi-barcelona
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Run the pipeline

The processed satellite data is already included in `data/raw/` so you can skip directly to step 4 if you do not want to re-download satellite imagery.

**Steps 2–3 require a free Copernicus Data Space account** ([register here](https://dataspace.copernicus.eu)):

```bash
export CDSE_USERNAME=your_email
export CDSE_PASSWORD=your_password

python scripts/build_green_space.py   # Downloads Sentinel-2 NDVI → data/raw/ndvi_barcelona_2023.tif
python scripts/build_heat.py          # Downloads Landsat LST → data/raw/lst_barcelona_2023.tif
```

**Steps 4–5 require no credentials:**

```bash
python scripts/build_social_vulnerability.py   # → data/processed/social_vulnerability.gpkg
python scripts/build_ugpi.py                   # → data/processed/ugpi_final.gpkg
python scripts/build_interactive_map.py        # → docs/ugpi_interactive_map.html
```

Open `docs/ugpi_interactive_map.html` in any browser.

---

## Data sources

| Layer | Source | Resolution | Period |
|---|---|---|---|
| Land Surface Temperature | Landsat 8, Band B10, via Copernicus CDSE | 30 m | Summer 2023 |
| NDVI | Sentinel-2 L2A, Bands B8+B4, via Copernicus CDSE | 10 m | Summer 2023 |
| Elderly population | Idescat Municipal Register | Census tract | 2024 |
| Income per capita | Barcelona Open Data portal | Census tract | 2022 |
| Census tract boundaries | ICGC shapefile | 1:5,000 | 2025 |

All sources are free and open access.

---

## Key results

- 1,068 census tracts scored across 10 districts
- UGPI range: 2.26 to 9.12 — mean 6.52
- Highest priority district: Nou Barris (mean UGPI 7.01)
- Highest priority tract: 08019303026, Sants-Montjuic (UGPI 9.12)

---

## Project context

PAIBS (Perspectives on AI, Business and Data) — ESADE Business School, 2025–2026
Group 8: Narcis Agusti, Albert Blade, Yago Granada, Gael Mensa, Victor Perez
Supervisor: Marc Herrera
