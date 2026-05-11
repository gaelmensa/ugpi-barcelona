"""
Download Sentinel-2 NDVI data for Barcelona using the
Copernicus Data Space Ecosystem (CDSE) Statistical API.

Credentials are read from environment variables — never hardcoded:
  CDSE_USERNAME   your CDSE account email
  CDSE_PASSWORD   your CDSE account password

Register for free at: https://dataspace.copernicus.eu/

Output: data/raw/ndvi_barcelona_2023.json
"""

import json
import os
import sys
from pathlib import Path

import requests

# ── endpoints ──────────────────────────────────────────────────────────────────
TOKEN_URL = (
    "https://identity.dataspace.copernicus.eu"
    "/auth/realms/CDSE/protocol/openid-connect/token"
)
STATISTICAL_API_URL = "https://sh.dataspace.copernicus.eu/api/v1/statistics"

# ── area of interest — Barcelona bounding box (WGS 84) ─────────────────────────
BBOX = [2.05, 41.31, 2.23, 41.47]  # [west, south, east, north]

# ── summer 2023: one request per month ─────────────────────────────────────────
MONTHS = [
    ("2023-06-01T00:00:00Z", "2023-07-01T00:00:00Z", "June 2023"),
    ("2023-07-01T00:00:00Z", "2023-08-01T00:00:00Z", "July 2023"),
    ("2023-08-01T00:00:00Z", "2023-09-01T00:00:00Z", "August 2023"),
]

# Cloud-masked NDVI evalscript.  dataMask output is required by the Statistical API.
EVALSCRIPT = """
//VERSION=3
function setup() {
  return {
    input: [{
      bands: ["B04", "B08", "SCL", "dataMask"]
    }],
    output: [
      { id: "ndvi", bands: 1, sampleType: "FLOAT32" },
      { id: "dataMask", bands: 1 }
    ]
  };
}

function evaluatePixel(s) {
  // SCL classes considered clear: 4=vegetation, 5=bare soil,
  // 6=water, 11=snow — excludes clouds (8,9,10) and shadows (3)
  var clear = (s.SCL == 4 || s.SCL == 5 || s.SCL == 6 || s.SCL == 11) ? 1 : 0;
  var ndvi = (s.B08 - s.B04) / (s.B08 + s.B04 + 1e-10);
  return {
    ndvi: [ndvi],
    dataMask: [s.dataMask * clear]
  };
}
"""


# ── 1. credentials ─────────────────────────────────────────────────────────────

def get_credentials() -> tuple[str, str]:
    username = os.environ.get("CDSE_USERNAME", "").strip()
    password = os.environ.get("CDSE_PASSWORD", "").strip()
    if not username or not password:
        print("ERROR: credentials not found in environment.")
        print("  Set CDSE_USERNAME and CDSE_PASSWORD before running this script.")
        print("  Register for free at https://dataspace.copernicus.eu/")
        print()
        print("  Example (bash):")
        print("    export CDSE_USERNAME='your@email.com'")
        print("    export CDSE_PASSWORD='yourpassword'")
        sys.exit(1)
    return username, password


# ── 2. token ───────────────────────────────────────────────────────────────────

def fetch_token(username: str, password: str) -> str:
    print(f"Requesting token from:\n  {TOKEN_URL}")
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
    print(f"Token response status: {resp.status_code}")

    if resp.status_code != 200:
        print(f"ERROR: token request failed — {resp.status_code}")
        try:
            err = resp.json()
            print(f"  {err.get('error', '')}: {err.get('error_description', '')}")
        except Exception:
            print(f"  {resp.text[:300]}")
        sys.exit(1)

    token_data = resp.json()
    token = token_data["access_token"]
    expires_in = token_data.get("expires_in", "?")
    print(f"Token obtained. Expires in {expires_in}s.\n")
    return token


# ── 3. Statistical API request ─────────────────────────────────────────────────

def build_request(time_from: str, time_to: str) -> dict:
    return {
        "input": {
            "bounds": {
                "bbox": BBOX,
                "properties": {
                    "crs": "http://www.opengis.net/def/crs/OGC/1.3/CRS84"
                },
            },
            "data": [
                {
                    "type": "sentinel-2-l2a",
                    "dataFilter": {
                        "mosaickingOrder": "leastCC"  # prefer least cloud cover
                    },
                }
            ],
        },
        "aggregation": {
            "timeRange": {"from": time_from, "to": time_to},
            "aggregationInterval": {"of": "P1M"},  # one interval = whole month
            "resx": 0.001,   # degrees — ≈ 100 m at Barcelona latitude (CRS84 units)
            "resy": 0.001,
            "evalscript": EVALSCRIPT,
        },
        "calculations": {
            "default": {}  # returns mean, stDev, percentiles, noDataPixels, etc.
        },
    }


def fetch_ndvi_stats(token: str, time_from: str, time_to: str, label: str) -> dict:
    print(f"Fetching NDVI stats for {label} …")
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    payload = build_request(time_from, time_to)
    resp = requests.post(
        STATISTICAL_API_URL,
        headers=headers,
        json=payload,
        timeout=120,
    )
    print(f"  Status: {resp.status_code}")

    if resp.status_code != 200:
        print(f"  ERROR: {resp.text[:400]}")
        return {"label": label, "error": resp.status_code, "detail": resp.text[:400]}

    result = resp.json()

    # Extract the mean NDVI from the nested response
    try:
        intervals = result["data"]
        for interval in intervals:
            outputs = interval.get("outputs", {})
            ndvi_stats = outputs.get("ndvi", {}).get("bands", {}).get("B0", {})
            mean_ndvi = ndvi_stats.get("stats", {}).get("mean")
            sample_count = ndvi_stats.get("stats", {}).get("sampleCount")
            print(f"  Mean NDVI: {mean_ndvi:.4f}  (n={sample_count} pixels)")
    except Exception as exc:
        print(f"  Could not parse result: {exc}")

    return {"label": label, "raw": result}


# ── 4. main ────────────────────────────────────────────────────────────────────

def main():
    username, password = get_credentials()
    token = fetch_token(username, password)

    results = []
    for time_from, time_to, label in MONTHS:
        stats = fetch_ndvi_stats(token, time_from, time_to, label)
        results.append(stats)
        print()

    out_path = Path("data/raw/ndvi_barcelona_2023.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(results, indent=2))
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    main()
