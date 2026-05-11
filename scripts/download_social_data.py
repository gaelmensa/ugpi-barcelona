"""
Download demographic data for Barcelona census tracts from the Barcelona Open Data portal.

Datasets fetched:
  1. Population by sex per census tract, 2024          (pad_mdbas_sexe)
  2. Population by 5-year age group per census tract, 2024  (pad_mdbas_edat-q)
  3. Disposable household income per capita, 2022      (renda_disponible_llars_per_persona)

Output: data/raw/population_by_sex.csv
        data/raw/population_by_age.csv
        data/raw/income_per_capita.csv
"""

from pathlib import Path
import pandas as pd
import requests

BASE = "https://opendata-ajuntament.barcelona.cat/data/api/action/datastore_search"
PAGE_SIZE = 1000
OUT_DIR = Path(__file__).resolve().parents[1] / "data" / "raw"

DATASETS = [
    {
        "name": "Population by sex, 2024 (pad_mdbas_sexe)",
        "resource_id": "3febe572-f530-4f89-8e9c-5c23c7d3d807",
        "filename": "population_by_sex.csv",
    },
    {
        "name": "Population by 5-year age group, 2024 (pad_mdbas_edat-q)",
        "resource_id": "1587842e-6f6d-443c-8a74-8d391efb768b",
        "filename": "population_by_age.csv",
    },
    {
        "name": "Disposable household income per capita, 2022",
        "resource_id": "3df0c5b9-de69-4c94-b924-57540e52932f",
        "filename": "income_per_capita.csv",
    },
]


def fetch_all_records(resource_id: str) -> list[dict]:
    records = []
    offset = 0

    # First request also tells us the total
    total = None

    while True:
        resp = requests.get(
            BASE,
            params={"resource_id": resource_id, "limit": PAGE_SIZE, "offset": offset},
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()

        if not data.get("success"):
            raise RuntimeError(f"API error: {data.get('error')}")

        result = data["result"]
        if total is None:
            total = result["total"]

        batch = result["records"]
        records.extend(batch)

        fetched = len(records)
        print(f"  fetched {fetched:>6} / {total} records", end="\r")

        if fetched >= total or not batch:
            break

        offset += PAGE_SIZE

    print()  # newline after \r progress
    return records


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    for ds in DATASETS:
        print(f"\n{'=' * 65}")
        print(f"Dataset : {ds['name']}")
        print(f"Resource: {ds['resource_id']}")

        records = fetch_all_records(ds["resource_id"])
        df = pd.DataFrame(records).drop(columns=["_id"], errors="ignore")

        out_path = OUT_DIR / ds["filename"]
        df.to_csv(out_path, index=False)

        saved_rows = sum(1 for _ in open(out_path)) - 1  # rows excluding header
        print(f"Shape   : {df.shape[0]} rows × {df.shape[1]} columns")
        print(f"Columns : {list(df.columns)}")
        print(f"Saved   : {out_path}")
        print(f"CSV rows: {saved_rows}  {'✓ matches' if saved_rows == df.shape[0] else '✗ MISMATCH'}")


if __name__ == "__main__":
    main()
