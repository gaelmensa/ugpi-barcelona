"""
Build the Green Space Deficit layer for the UGPI project.

Steps:
  1. Load data/processed/barcelona_census_tracts.gpkg
  2. Download a summer-2023 NDVI GeoTIFF via the Copernicus Process API:
       - Three monthly least-cloud-cover composites (June, July, August 2023)
       - Cloud-masked with Sentinel-2 SCL band
       - EPSG:25831 (UTM zone 31N), 10 m resolution, FLOAT32
       - Per-pixel nanmean of the three months → data/raw/ndvi_barcelona_2023.tif
  3. Zonal statistics (rasterstats) — mean NDVI per census tract
  4. Normalise to 1–10 Green Space Deficit Score  (low NDVI → high score)
  5. Save → data/processed/green_space.gpkg
           → outputs/04_green_space.png

Credentials (environment variables):
  CDSE_USERNAME   Copernicus Data Space Ecosystem email
  CDSE_PASSWORD   account password
  Register at https://dataspace.copernicus.eu/
"""

import io
import os
import sys
import tarfile
from pathlib import Path

import numpy as np
import requests
import geopandas as gpd
import pandas as pd
import rasterio
from rasterio.transform import from_bounds
from rasterio.crs import CRS
import matplotlib.pyplot as plt
import matplotlib as mpl
from rasterstats import zonal_stats

# ── endpoints ──────────────────────────────────────────────────────────────────
TOKEN_URL = (
    "https://identity.dataspace.copernicus.eu"
    "/auth/realms/CDSE/protocol/openid-connect/token"
)
PROCESS_API_URL = "https://sh.dataspace.copernicus.eu/api/v1/process"

# ── paths ──────────────────────────────────────────────────────────────────────
DATA_RAW  = Path("data/raw")
DATA_PROC = Path("data/processed")
OUTPUTS   = Path("outputs")

# ── raster parameters ──────────────────────────────────────────────────────────
NODATA     = -9999.0
PIXEL_SIZE = 10          # metres — Sentinel-2 native resolution for B04/B08

# ── summer 2023 months ─────────────────────────────────────────────────────────
MONTHS = [
    ("2023-06-01T00:00:00Z", "2023-07-01T00:00:00Z", "June 2023"),
    ("2023-07-01T00:00:00Z", "2023-08-01T00:00:00Z", "July 2023"),
    ("2023-08-01T00:00:00Z", "2023-09-01T00:00:00Z", "August 2023"),
]

# Cloud-masked NDVI evalscript for the Process API.
# SCL classes considered clear: 4=vegetation, 5=bare soil, 6=water, 11=snow.
# Clouds (8,9,10) and shadows (3) are masked to NODATA.
EVALSCRIPT = """
//VERSION=3
function setup() {
  return {
    input: [{ bands: ["B04", "B08", "SCL", "dataMask"] }],
    output: { bands: 1, sampleType: "FLOAT32" }
  };
}
function evaluatePixel(s) {
  if (!s.dataMask) return [-9999];
  var clear = (s.SCL==4 || s.SCL==5 || s.SCL==6 || s.SCL==11);
  if (!clear) return [-9999];
  return [(s.B08 - s.B04) / (s.B08 + s.B04 + 1e-10)];
}
"""


# ── 1. credentials ─────────────────────────────────────────────────────────────

def get_credentials() -> tuple[str, str]:
    username = os.environ.get("CDSE_USERNAME", "").strip()
    password = os.environ.get("CDSE_PASSWORD", "").strip()
    if not username or not password:
        print("ERROR: CDSE_USERNAME and CDSE_PASSWORD must be set.")
        print("  Register at https://dataspace.copernicus.eu/")
        sys.exit(1)
    return username, password


# ── 2. OAuth token ─────────────────────────────────────────────────────────────

def fetch_token(username: str, password: str) -> str:
    print("Requesting CDSE token …")
    resp = requests.post(
        TOKEN_URL,
        data={
            "client_id": "cdse-public",
            "grant_type": "password",
            "username": username,
            "password": password,
        },
        timeout=30,
    )
    if resp.status_code != 200:
        print(f"ERROR: token request failed — {resp.status_code}")
        try:
            err = resp.json()
            print(f"  {err.get('error', '')}: {err.get('error_description', '')}")
        except Exception:
            print(f"  {resp.text[:300]}")
        sys.exit(1)
    token_data = resp.json()
    print(f"Token obtained. Expires in {token_data.get('expires_in', '?')}s.\n")
    return token_data["access_token"]


# ── 3. Process API — download one monthly GeoTIFF ──────────────────────────────

def fetch_monthly_tiff(
    token: str,
    bbox: list[float],
    width: int,
    height: int,
    time_from: str,
    time_to: str,
    label: str,
) -> bytes:
    print(f"  Downloading {label} GeoTIFF ({width}×{height} px) …", end=" ", flush=True)

    payload = {
        "input": {
            "bounds": {
                "bbox": bbox,
                "properties": {
                    "crs": "http://www.opengis.net/def/crs/EPSG/0/32631"
                },
            },
            "data": [{
                "type": "sentinel-2-l2a",
                "dataFilter": {
                    "timeRange": {"from": time_from, "to": time_to},
                    "mosaickingOrder": "leastCC",
                },
            }],
        },
        "output": {
            "width": width,
            "height": height,
            "responses": [{
                "identifier": "default",
                "format": {
                    "type": "image/tiff",
                    "parameters": {"encoding": "FLOAT32"},
                },
            }],
        },
        "evalscript": EVALSCRIPT,
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "image/tiff",
    }

    resp = requests.post(PROCESS_API_URL, json=payload, headers=headers, timeout=120)
    print(f"status={resp.status_code}")

    if resp.status_code != 200:
        print(f"  ERROR: {resp.text[:400]}")
        sys.exit(1)

    return _extract_tiff_bytes(resp)


def _extract_tiff_bytes(resp: requests.Response) -> bytes:
    """Return raw GeoTIFF bytes from a Process API response (direct or tar)."""
    ct = resp.headers.get("Content-Type", "")
    if "tiff" in ct or "octet-stream" in ct:
        return resp.content
    if "tar" in ct:
        with tarfile.open(fileobj=io.BytesIO(resp.content)) as tf:
            for member in tf.getmembers():
                if member.name.endswith((".tif", ".tiff")):
                    return tf.extractfile(member).read()
        raise RuntimeError("No .tif file found inside tar response")
    # Unknown format — try interpreting as raw TIFF anyway
    return resp.content


# ── 4. Average monthly rasters → final GeoTIFF ────────────────────────────────

def build_average_tiff(
    tiff_bytes_list: list[bytes],
    out_path: Path,
    fallback_bbox: list[float],
    width: int,
    height: int,
) -> None:
    """
    Stack monthly NDVI arrays, compute per-pixel nanmean, and write to out_path.
    Uses the geotransform/CRS from the first API response; falls back to the
    computed bbox + EPSG:25831 if the response lacks georeferencing.
    """
    arrays: list[np.ndarray] = []
    profile = None

    for tiff_bytes in tiff_bytes_list:
        with rasterio.open(io.BytesIO(tiff_bytes)) as src:
            arr = src.read(1).astype(np.float32)
            arr[arr == NODATA] = np.nan
            arrays.append(arr)
            if profile is None:
                profile = src.profile.copy()

    ndvi_mean = np.nanmean(np.stack(arrays, axis=0), axis=0)
    ndvi_out  = np.where(np.isnan(ndvi_mean), NODATA, ndvi_mean).astype(np.float32)

    # Ensure the output is properly georeferenced in EPSG:25831
    if profile is None or profile.get("crs") is None:
        xmin, ymin, xmax, ymax = fallback_bbox
        profile = {
            "driver": "GTiff",
            "dtype": "float32",
            "width": width,
            "height": height,
            "count": 1,
            "crs": CRS.from_epsg(32631),
            "transform": from_bounds(xmin, ymin, xmax, ymax, width, height),
        }
    else:
        profile["crs"] = profile.get("crs") or CRS.from_epsg(32631)

    profile.update(dtype="float32", nodata=NODATA, count=1, compress="lzw")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with rasterio.open(out_path, "w", **profile) as dst:
        dst.write(ndvi_out, 1)

    valid_px   = int(np.sum(ndvi_out != NODATA))
    mean_valid = float(np.nanmean(ndvi_out[ndvi_out != NODATA]))
    print(
        f"\nAveraged raster saved: {out_path}"
        f"\n  {profile['width']}×{profile['height']} px | "
        f"{valid_px:,} valid pixels | mean NDVI = {mean_valid:.4f}"
    )


# ── 5. Zonal statistics ────────────────────────────────────────────────────────

def compute_zonal_stats(gdf: gpd.GeoDataFrame, raster_path: Path) -> gpd.GeoDataFrame:
    print(f"\nZonal statistics for {len(gdf)} census tracts …")
    stats = zonal_stats(
        gdf,
        str(raster_path),
        stats=["mean"],
        nodata=NODATA,
        all_touched=False,
    )
    gdf = gdf.copy()
    gdf["mean_ndvi"] = [s["mean"] for s in stats]

    n_valid   = gdf["mean_ndvi"].notna().sum()
    ndvi_min  = gdf["mean_ndvi"].min()
    ndvi_max  = gdf["mean_ndvi"].max()
    ndvi_mean = gdf["mean_ndvi"].mean()
    print(
        f"  Valid tracts: {n_valid}/{len(gdf)}"
        f" | NDVI range: {ndvi_min:.4f}–{ndvi_max:.4f}"
        f" | mean: {ndvi_mean:.4f}"
    )
    return gdf


# ── 6. Normalise to 1–10 Green Space Deficit Score ────────────────────────────

def deficit_score(series: pd.Series) -> pd.Series:
    """Lower NDVI → higher deficit score. Range 1–10, NaN preserved."""
    mn, mx = series.min(), series.max()
    return 1.0 + 9.0 * (mx - series) / (mx - mn)


# ── 7. Map ─────────────────────────────────────────────────────────────────────

def save_map(gdf: gpd.GeoDataFrame, out_path: Path) -> None:
    print("Rendering map …")

    fig, ax = plt.subplots(figsize=(12, 10))

    gdf.plot(
        column="Green_Space_Deficit_Score",
        cmap="RdYlGn_r",
        linewidth=0.1,
        edgecolor="white",
        legend=False,
        missing_kwds={"color": "lightgrey", "label": "No data"},
        ax=ax,
        vmin=1,
        vmax=10,
    )

    sm = mpl.cm.ScalarMappable(
        cmap="RdYlGn_r",
        norm=mpl.colors.Normalize(vmin=1, vmax=10),
    )
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=ax, fraction=0.03, pad=0.02)
    cbar.set_label(
        "Green Space Deficit Score  (1 = high greenery,  10 = bare / built-up)",
        fontsize=11,
    )
    cbar.set_ticks([1, 3, 5, 7, 10])

    ax.set_title(
        "Green Space Deficit Score — Barcelona Census Tracts\n"
        "Sentinel-2 NDVI, summer 2023 (June–August mean, 10 m)",
        fontsize=13,
        pad=14,
    )
    ax.set_axis_off()

    plt.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved: {out_path}")


# ── main ───────────────────────────────────────────────────────────────────────

def main() -> None:
    # ── census tracts ──────────────────────────────────────────────────────────
    print("Loading census tracts …")
    gdf = gpd.read_file(DATA_PROC / "barcelona_census_tracts.gpkg")
    print(f"  {len(gdf)} tracts, CRS={gdf.crs}")

    # The Copernicus Process API for S2L2A only accepts EPSG:32631 (WGS84 UTM 31N),
    # not EPSG:25831 (ETRS89 UTM 31N). Reproject to 32631 for the API request and
    # for zonal stats alignment; results are joined back to the original 25831 GDF.
    gdf_32631 = gdf.to_crs("EPSG:32631")

    # Snap bounding box to pixel grid
    xmin, ymin, xmax, ymax = gdf_32631.total_bounds
    xmin = int(xmin // PIXEL_SIZE) * PIXEL_SIZE
    ymin = int(ymin // PIXEL_SIZE) * PIXEL_SIZE
    xmax = (int(xmax // PIXEL_SIZE) + 1) * PIXEL_SIZE
    ymax = (int(ymax // PIXEL_SIZE) + 1) * PIXEL_SIZE

    bbox   = [xmin, ymin, xmax, ymax]
    width  = int((xmax - xmin) / PIXEL_SIZE)
    height = int((ymax - ymin) / PIXEL_SIZE)
    print(f"  Raster bbox (EPSG:32631): {bbox}")
    print(f"  Output size: {width}×{height} pixels at {PIXEL_SIZE} m\n")

    # ── auth ───────────────────────────────────────────────────────────────────
    username, password = get_credentials()
    token = fetch_token(username, password)

    # ── download three monthly composites ─────────────────────────────────────
    print("Downloading monthly NDVI composites from Copernicus Process API …")
    tiff_bytes_list: list[bytes] = []
    for time_from, time_to, label in MONTHS:
        tiff_bytes_list.append(
            fetch_monthly_tiff(token, bbox, width, height, time_from, time_to, label)
        )

    # ── average and save GeoTIFF ───────────────────────────────────────────────
    out_tif = DATA_RAW / "ndvi_barcelona_2023.tif"
    build_average_tiff(tiff_bytes_list, out_tif, bbox, width, height)

    # ── zonal statistics (use EPSG:32631 GDF to match the raster) ─────────────
    gdf_32631 = compute_zonal_stats(gdf_32631, out_tif)
    gdf["mean_ndvi"] = gdf_32631["mean_ndvi"].values

    # ── deficit score ──────────────────────────────────────────────────────────
    gdf["Green_Space_Deficit_Score"] = deficit_score(gdf["mean_ndvi"])

    print("\nGreen Space Deficit Score stats:")
    print(gdf["Green_Space_Deficit_Score"].describe().round(3).to_string())

    # ── save GeoPackage ────────────────────────────────────────────────────────
    out_gpkg = DATA_PROC / "green_space.gpkg"
    gdf.to_file(out_gpkg, driver="GPKG")
    print(f"\nSaved: {out_gpkg}  ({len(gdf)} rows, {len(gdf.columns)} columns)")

    # ── map ────────────────────────────────────────────────────────────────────
    save_map(gdf, OUTPUTS / "04_green_space.png")


if __name__ == "__main__":
    main()
