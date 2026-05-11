"""
Build the Urban Greening Priority Index (UGPI) — final combination layer.

Steps:
  1. Load data/processed/social_vulnerability.gpkg
               data/processed/green_space.gpkg
               data/processed/heat.gpkg
  2. Join all three to the base census tracts using MUNDISSEC
  3. UGPI = mean(Social_Vulnerability_Score,
                 Green_Space_Deficit_Score,
                 Heat_Score)   — equal weights
  4. Save → data/processed/ugpi_final.gpkg
  5. Single UGPI map  → outputs/06_ugpi_final.png
     2×2 panel map    → outputs/06_ugpi_panel.png
  6. Print top-10 highest-priority tracts
"""

from pathlib import Path

import geopandas as gpd
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable

# ── paths ──────────────────────────────────────────────────────────────────────
DATA_PROC = Path("data/processed")
OUTPUTS   = Path("outputs")

# ── scoring columns ────────────────────────────────────────────────────────────
SCORE_COLS = [
    "Social_Vulnerability_Score",
    "Green_Space_Deficit_Score",
    "Heat_Score",
]

# ── Barcelona district names ───────────────────────────────────────────────────
DISTRICT_NAMES = {
    "01": "Ciutat Vella",
    "02": "Eixample",
    "03": "Sants-Montjuïc",
    "04": "Les Corts",
    "05": "Sarrià-Sant Gervasi",
    "06": "Gràcia",
    "07": "Horta-Guinardó",
    "08": "Nou Barris",
    "09": "Sant Andreu",
    "10": "Sant Martí",
}

# ── map config for each subplot ────────────────────────────────────────────────
PANEL_CONFIG = [
    {
        "col":   "Social_Vulnerability_Score",
        "cmap":  "Reds",
        "title": "Social Vulnerability Score",
        "label": "Score  (1 = low,  10 = high)",
    },
    {
        "col":   "Green_Space_Deficit_Score",
        "cmap":  "RdYlGn_r",
        "title": "Green Space Deficit Score",
        "label": "Score  (1 = high greenery,  10 = bare / built-up)",
    },
    {
        "col":   "Heat_Score",
        "cmap":  "YlOrRd",
        "title": "Heat Score",
        "label": "Score  (1 = cooler,  10 = hottest)",
    },
    {
        "col":   "UGPI",
        "cmap":  "YlOrRd",
        "title": "Urban Greening Priority Index (UGPI)",
        "label": "UGPI  (1 = lower priority,  10 = highest)",
    },
]


# ── helpers ────────────────────────────────────────────────────────────────────

def _add_colorbar(fig, ax, cmap: str, vmin: float, vmax: float, label: str) -> None:
    sm = ScalarMappable(cmap=cmap, norm=Normalize(vmin=vmin, vmax=vmax))
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=ax, fraction=0.03, pad=0.02)
    cbar.set_label(label, fontsize=9)
    cbar.set_ticks([vmin, (vmin + vmax) / 2, vmax])
    cbar.ax.tick_params(labelsize=8)


# ── 1. load and join ───────────────────────────────────────────────────────────

def load_and_join() -> gpd.GeoDataFrame:
    print("Loading layers …")
    sv   = gpd.read_file(DATA_PROC / "social_vulnerability.gpkg")
    gs   = gpd.read_file(DATA_PROC / "green_space.gpkg")
    heat = gpd.read_file(DATA_PROC / "heat.gpkg")

    # Keep all identifiers and raw indicators from social_vulnerability as the base
    base_cols = [
        "MUNDISSEC", "MUNICIPI", "DISTRICTE", "SECCIO",
        "join_key", "pct_elderly", "total_pop", "Import_Euros",
        "elderly_score", "income_score", "Social_Vulnerability_Score",
        "geometry",
    ]
    gdf = sv[base_cols].copy()

    gdf = gdf.merge(
        gs[["MUNDISSEC", "mean_ndvi", "Green_Space_Deficit_Score"]],
        on="MUNDISSEC",
        how="left",
    )
    gdf = gdf.merge(
        heat[["MUNDISSEC", "mean_lst", "Heat_Score"]],
        on="MUNDISSEC",
        how="left",
    )

    print(
        f"  Joined: {len(gdf)} tracts | "
        f"missing scores: {gdf[SCORE_COLS].isna().any(axis=1).sum()}"
    )
    return gdf


# ── 2. compute UGPI ────────────────────────────────────────────────────────────

def compute_ugpi(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    gdf = gdf.copy()
    gdf["UGPI"] = gdf[SCORE_COLS].mean(axis=1)

    print("\nComponent score ranges:")
    for col in SCORE_COLS + ["UGPI"]:
        s = gdf[col]
        print(f"  {col:<35s}  {s.min():.3f} – {s.max():.3f}  (mean {s.mean():.3f})")

    return gdf


# ── 3. print top 10 ────────────────────────────────────────────────────────────

def print_top10(gdf: gpd.GeoDataFrame) -> None:
    print("\n─── Top 10 highest-priority census tracts ───────────────────────────")

    top = (
        gdf.nlargest(10, "UGPI")
        .reset_index(drop=True)
    )
    top.index += 1  # 1-based rank

    # Map district code to name (MUNDISSEC chars 6–7 are the 2-digit district)
    top["District"] = (
        top["MUNDISSEC"].str[6:8].map(DISTRICT_NAMES).fillna(top["DISTRICTE"])
    )

    display = top[[
        "District", "MUNDISSEC",
        "UGPI",
        "Social_Vulnerability_Score",
        "Green_Space_Deficit_Score",
        "Heat_Score",
    ]].rename(columns={
        "Social_Vulnerability_Score": "SocVuln",
        "Green_Space_Deficit_Score":  "GreenDef",
        "Heat_Score":                 "Heat",
    })

    # Format numbers
    for col in ["UGPI", "SocVuln", "GreenDef", "Heat"]:
        display[col] = display[col].map("{:.2f}".format)

    print(display.to_string())
    print("─" * 72)


# ── 4. single UGPI map ─────────────────────────────────────────────────────────

def save_ugpi_map(gdf: gpd.GeoDataFrame, out_path: Path) -> None:
    print("\nRendering single UGPI map …")

    vmin, vmax = 1, 10
    cmap = "YlOrRd"

    fig, ax = plt.subplots(figsize=(12, 10))

    gdf.plot(
        column="UGPI",
        cmap=cmap,
        linewidth=0.1,
        edgecolor="white",
        legend=False,
        missing_kwds={"color": "lightgrey"},
        ax=ax,
        vmin=vmin,
        vmax=vmax,
    )

    sm = ScalarMappable(cmap=cmap, norm=Normalize(vmin=vmin, vmax=vmax))
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=ax, fraction=0.03, pad=0.02)
    cbar.set_label("UGPI  (1 = lower priority,  10 = highest priority)", fontsize=11)
    cbar.set_ticks([1, 3, 5, 7, 10])

    ugpi_mean = gdf["UGPI"].mean()
    n_high    = (gdf["UGPI"] >= 7).sum()
    ax.set_title(
        "Urban Greening Priority Index — Barcelona Census Tracts\n"
        f"Summer 2023  |  mean = {ugpi_mean:.2f}  |  {n_high} tracts ≥ 7.0 (high priority)",
        fontsize=13,
        pad=14,
    )
    ax.set_axis_off()

    plt.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Saved: {out_path}")


# ── 5. 2×2 panel map ──────────────────────────────────────────────────────────

def save_panel_map(gdf: gpd.GeoDataFrame, out_path: Path) -> None:
    print("Rendering 2×2 panel map …")

    fig, axes = plt.subplots(2, 2, figsize=(20, 17))
    fig.suptitle(
        "Urban Greening Priority Index — Component Scores & Final Index\n"
        "Barcelona Census Tracts, Summer 2023",
        fontsize=15,
        y=0.98,
    )

    vmin, vmax = 1, 10

    for ax, cfg in zip(axes.flat, PANEL_CONFIG):
        col   = cfg["col"]
        cmap  = cfg["cmap"]
        title = cfg["title"]
        label = cfg["label"]

        gdf.plot(
            column=col,
            cmap=cmap,
            linewidth=0.1,
            edgecolor="white",
            legend=False,
            missing_kwds={"color": "lightgrey"},
            ax=ax,
            vmin=vmin,
            vmax=vmax,
        )

        _add_colorbar(fig, ax, cmap, vmin, vmax, label)

        mean_val = gdf[col].mean()
        ax.set_title(f"{title}\n(mean = {mean_val:.2f})", fontsize=11, pad=8)
        ax.set_axis_off()

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Saved: {out_path}")


# ── main ───────────────────────────────────────────────────────────────────────

def main() -> None:
    OUTPUTS.mkdir(parents=True, exist_ok=True)

    gdf = load_and_join()
    gdf = compute_ugpi(gdf)

    # Save GeoPackage
    out_gpkg = DATA_PROC / "ugpi_final.gpkg"
    gdf.to_file(out_gpkg, driver="GPKG")
    print(f"\nSaved: {out_gpkg}  ({len(gdf)} rows, {len(gdf.columns)} columns)")

    print_top10(gdf)

    save_ugpi_map(gdf, OUTPUTS / "06_ugpi_final.png")
    save_panel_map(gdf, OUTPUTS / "06_ugpi_panel.png")


if __name__ == "__main__":
    main()
