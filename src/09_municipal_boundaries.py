"""Build the 1,059-unit municipal boundary layer from KSJ N03 (2023-01-01).

Designated-city wards are dissolved into their city; the 23 special wards stay
separate. N03 reports 19 of the 20 designated cities only through their wards,
so the city polygon is rebuilt from ward polygons. "所属未定地" (undetermined
jurisdiction) rows are excluded.

Run:
    uv run python src/09_municipal_boundaries.py
"""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd
import pyogrio

sys.path.insert(0, str(Path(__file__).resolve().parent))
config = importlib.import_module("00_config")

N03_SHP = config.DATA_INTERIM / "ksj" / "n03" / "N03-23_230101.shp"
PANEL = config.DATA_PROCESSED / "vacancy_panel_2018_2023.csv"
CENSUS = config.DATA_INTERIM / "census_2025.csv"
OUT_GPKG = config.DATA_INTERIM / "municipal_boundaries.gpkg"
OUT_AREA = config.DATA_INTERIM / "municipal_area.csv"
OUT_WARD_MAP = config.DATA_INTERIM / "ward_to_city_2023.csv"

EQUAL_AREA = "EPSG:6933"
WGS84 = "EPSG:4326"


def main() -> None:
    panel = pd.read_csv(PANEL, dtype={"region_code": str})
    keep = set(panel.region_code)
    unit_level = dict(zip(panel.region_code, panel.level))
    unit_name = dict(zip(panel.region_code, panel.region_name_2023))

    n03 = pyogrio.read_dataframe(N03_SHP, encoding="cp932")
    n03["N03_007"] = n03.N03_007.astype(str).str.zfill(5)
    print(f"N03 rows: {len(n03):,}; unique codes: {n03.N03_007.nunique():,}")

    # "所属未定地" rows carry a municipality code but are not municipality area.
    undetermined = n03.N03_004 == "所属未定地"
    print(f"Excluded 所属未定地 rows: {undetermined.sum():,}")
    n03 = n03[~undetermined].copy()

    # Designated cities: map ward polygons to the city code. Match on the
    # prefecture code prefix + N03_003 (郡・政令都市名) + ward name ending in 区.
    designated = panel[panel.level == "designated_city"]
    ward_rows = []
    ward_map: dict[str, str] = {}
    for row in designated.itertuples():
        pref = row.region_code[:2]
        wards = n03[
            (n03.N03_007.str[:2] == pref)
            & (n03.N03_003 == row.region_name_2023)
            & (n03.N03_004.str.endswith("区"))
        ]
        if wards.empty:
            raise ValueError(f"No ward polygons for {row.region_name_2023} ({row.region_code})")
        codes = sorted(wards.N03_007.unique())
        ward_rows.extend(
            {"ward_code": code, "city_code": row.region_code, "city_name": row.region_name_2023}
            for code in codes
        )
        for code in codes:
            ward_map[code] = row.region_code
        print(f"  {row.region_name_2023}: {len(codes)} wards, {len(wards)} polygons")

    pd.DataFrame(ward_rows).to_csv(OUT_WARD_MAP, index=False, encoding="utf-8-sig")

    n03["unit_code"] = n03.N03_007.map(ward_map)
    n03["unit_code"] = n03.unit_code.where(n03.unit_code.notna(), n03.N03_007)

    subset = n03[n03.unit_code.isin(keep)].copy()
    missing = sorted(keep - set(subset.unit_code))
    print(f"Rows kept: {len(subset):,}; units: {subset.unit_code.nunique():,}; missing: {len(missing)}")
    if missing:
        raise ValueError(f"Missing units: {missing}")

    invalid = ~subset.geometry.is_valid
    if invalid.any():
        print(f"Repairing invalid geometries: {invalid.sum():,} rows")
        subset.loc[invalid, "geometry"] = subset.loc[invalid, "geometry"].make_valid()

    print("Dissolving to analysis units ...")
    counts = subset.groupby("unit_code").size().rename("n_source_polygons").reset_index()
    boundaries = subset[["unit_code", "geometry"]].dissolve(by="unit_code", as_index=False)
    boundaries = boundaries.merge(counts, on="unit_code", how="left")
    boundaries["geometry"] = boundaries.geometry.make_valid()
    boundaries = boundaries[~boundaries.geometry.is_empty].copy()

    if list(boundaries.unit_code) != sorted(boundaries.unit_code):
        boundaries = boundaries.sort_values("unit_code").reset_index(drop=True)

    boundaries["unit_name_2023"] = boundaries.unit_code.map(unit_name)
    boundaries["level"] = boundaries.unit_code.map(unit_level)

    areas = boundaries.to_crs(EQUAL_AREA).area / 1e6
    boundaries["area_km2"] = areas.round(6).values
    zero = boundaries[boundaries.area_km2 <= 0]
    print(f"Zero-area units: {len(zero)}")
    if len(zero):
        print(zero[["unit_code", "unit_name_2023", "area_km2"]].to_string(index=False))

    census = pd.read_csv(CENSUS, dtype={"area_code": str})[["area_code", "area_km2"]]
    census = census.rename(columns={"area_code": "unit_code", "area_km2": "census_area_km2"})
    check = boundaries[["unit_code", "unit_name_2023", "area_km2"]].merge(census, on="unit_code", how="left")
    check["ratio"] = check.area_km2 / check.census_area_km2
    print("\nArea comparison vs census (N03 / census):")
    print(check.ratio.describe().to_string())
    worst = check.assign(diff=(check.ratio - 1).abs()).nlargest(10, "diff")
    print("\nLargest area differences:")
    print(worst[["unit_code", "unit_name_2023", "area_km2", "census_area_km2", "ratio"]].to_string(index=False))

    print(f"\nTotal N03 area: {boundaries.area_km2.sum():,.0f} km2")
    print(f"National land area (2023): 377,975 km2 (reference)")

    out = boundaries[["unit_code", "unit_name_2023", "level", "n_source_polygons", "area_km2", "geometry"]]
    out.to_file(OUT_GPKG, layer="municipalities_2023", driver="GPKG")
    boundaries[["unit_code", "unit_name_2023", "level", "n_source_polygons", "area_km2"]].to_csv(
        OUT_AREA, index=False, encoding="utf-8-sig"
    )
    print(f"\nWrote {OUT_GPKG} and {OUT_AREA}")


if __name__ == "__main__":
    main()
