"""Assign rail stations to municipalities and compute accessibility metrics.

Stations are first matched to *all* N03 municipality polygons, then reduced to
the 1,059-unit analysis panel. This prevents a station in one of the 682
out-of-scope towns from being attached to a neighbouring panel municipality.

Run:
    uv run python src/11_accessibility.py
"""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
import pyogrio
import shapely
from scipy.stats import spearmanr

sys.path.insert(0, str(Path(__file__).resolve().parent))
config = importlib.import_module("00_config")

N03_SHP = config.DATA_INTERIM / "ksj" / "n03" / "N03-23_230101.shp"
WARD_MAP = config.DATA_INTERIM / "ward_to_city_2023.csv"
STATIONS = config.DATA_INTERIM / "stations.geojson"
BOUNDARIES = config.DATA_INTERIM / "municipal_boundaries.gpkg"
AREA = config.DATA_INTERIM / "municipal_area.csv"
CENSUS = config.DATA_INTERIM / "census_2025.csv"
PANEL = config.DATA_PROCESSED / "vacancy_panel_2018_2023.csv"

OUT_ACCESS = config.DATA_PROCESSED / "accessibility_2023.csv"
OUT_PANEL = config.DATA_PROCESSED / "panel_with_accessibility_2023.csv"
OUT_PILOT = config.DATA_PROCESSED / "pilot_panel_v2.csv"
OUT_ASSIGN = config.DATA_INTERIM / "station_assignments.csv"
OUT_ZERO = config.OUTPUTS / "zero_station_municipalities.csv"
OUT_REPORT = config.OUTPUTS / "accessibility_validation.txt"

EQUAL_AREA = "EPSG:6933"


def assign_stations() -> gpd.GeoDataFrame:
    stations = gpd.read_file(STATIONS)
    print(f"Stations loaded: {len(stations):,}")

    n03 = pyogrio.read_dataframe(N03_SHP, encoding="cp932")
    n03["N03_007"] = n03.N03_007.astype(str).str.zfill(5)
    n03 = n03[n03.N03_004 != "所属未定地"].copy()
    ward_map = pd.read_csv(WARD_MAP, dtype={"ward_code": str, "city_code": str})
    ward_lookup = dict(zip(ward_map.ward_code, ward_map.city_code))
    n03["unit_code"] = n03.N03_007.map(ward_lookup)
    n03["unit_code"] = n03.unit_code.where(n03.unit_code.notna(), n03.N03_007)
    n03 = n03[["N03_007", "unit_code", "geometry"]].rename(columns={"N03_007": "n03_code"})
    n03 = n03.to_crs("EPSG:4326")
    print(f"N03 polygons: {len(n03):,}; unique n03 codes: {n03.n03_code.nunique():,}")

    # 1) Exact spatial match against all municipality polygons.
    joined = gpd.sjoin(
        stations[["station_group_code", "station_name", "geometry"]],
        n03,
        how="left",
        predicate="within",
    )
    dup = joined[joined.station_group_code.duplicated(keep=False)]
    if len(dup):
        print(f"Stations inside multiple polygons: {dup.station_group_code.nunique():,} (keeping first)")
        joined = joined.sort_values(["station_group_code", "n03_code"]).drop_duplicates(
            "station_group_code", keep="first"
        )
    exact = joined.n03_code.notna().sum()
    print(f"Exact within-match: {exact:,} / {len(stations):,}")

    # 2) Nearest-polygon fallback for coastal/underground/reclaimed points.
    unmatched = joined[joined.n03_code.isna()].station_group_code.tolist()
    fallback = None
    if unmatched:
        pts = stations[stations.station_group_code.isin(unmatched)].to_crs(EQUAL_AREA)
        near = gpd.sjoin_nearest(
            pts[["station_group_code", "geometry"]],
            n03.to_crs(EQUAL_AREA),
            how="left",
            distance_col="assign_distance_m",
        ).sort_values(["station_group_code", "assign_distance_m"]).drop_duplicates(
            "station_group_code", keep="first"
        )
        fallback = near[["station_group_code", "n03_code", "unit_code", "assign_distance_m"]].copy()
        fallback["assign_method"] = "nearest_polygon"
        print(f"Nearest-polygon fallback: {len(fallback):,}")
        print(fallback.assign_distance_m.describe().to_string())

    matched = joined[joined.n03_code.notna()][
        ["station_group_code", "n03_code", "unit_code"]
    ].copy()
    matched["assign_method"] = "within"
    matched["assign_distance_m"] = 0.0
    if fallback is not None:
        matched = pd.concat([matched, fallback], ignore_index=True)
    else:
        matched["assign_distance_m"] = matched.assign_distance_m.astype(float)

    out = stations.merge(matched, on="station_group_code", how="left", validate="one_to_one")
    return out


def add_boundary_distance(stations: gpd.GeoDataFrame, boundaries: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """Distance from each assigned station to its municipality boundary (metres)."""
    b = boundaries.to_crs(EQUAL_AREA).set_index("unit_code")
    s = stations.to_crs(EQUAL_AREA)
    dist = pd.Series(np.nan, index=stations.index, dtype=float)
    for unit_code, idx in s.groupby("unit_code").groups.items():
        if unit_code not in b.index:
            continue
        geom = b.loc[unit_code, "geometry"]
        pts = s.loc[idx, "geometry"].array
        dist.loc[idx] = shapely.distance(pts, geom.boundary)
    stations = stations.copy()
    stations["boundary_distance_m"] = dist.values
    return stations


def main() -> None:
    stations = assign_stations()
    boundaries = gpd.read_file(BOUNDARIES, layer="municipalities_2023")
    panel = pd.read_csv(PANEL, dtype={"region_code": str})
    panel_codes = set(panel.region_code)

    stations["in_panel"] = stations.unit_code.isin(panel_codes)
    n_out = (~stations.in_panel).sum()
    print(f"Stations outside the 1,059-unit panel: {n_out:,}")

    stations = add_boundary_distance(stations, boundaries)
    stations["near_boundary"] = stations.boundary_distance_m < 100
    print(f"Stations within 100 m of a boundary: {stations.near_boundary.sum():,}")

    assignments = stations[
        [
            "station_group_code",
            "station_name",
            "unit_code",
            "in_panel",
            "assign_method",
            "assign_distance_m",
            "boundary_distance_m",
            "near_boundary",
            "passengers_2023",
            "has_passenger_data",
        ]
    ].copy()
    assignments.to_csv(OUT_ASSIGN, index=False, encoding="utf-8-sig")

    panel_stations = stations[stations.in_panel].copy()
    heavy = panel_stations[panel_stations.has_heavy_rail]
    tram = panel_stations[~panel_stations.has_heavy_rail]

    agg = (
        heavy.groupby("unit_code")
        .agg(
            station_count=("station_group_code", "nunique"),
            station_passengers_sum=("passengers_2023", lambda x: x.sum(min_count=1)),
            stations_with_passenger_data=("has_passenger_data", "sum"),
        )
        .reset_index()
    )
    tram_agg = (
        tram.groupby("unit_code")
        .agg(
            tram_stop_count=("station_group_code", "nunique"),
            tram_passengers_sum=("passengers_2023", lambda x: x.sum(min_count=1)),
        )
        .reset_index()
    )

    area = pd.read_csv(AREA, dtype={"unit_code": str})[
        ["unit_code", "unit_name_2023", "level", "area_km2"]
    ]
    census = pd.read_csv(CENSUS, dtype={"area_code": str})[
        ["area_code", "pop_2025", "density"]
    ].rename(columns={"area_code": "unit_code", "density": "census_density"})
    acc = (
        area.merge(agg, on="unit_code", how="left")
        .merge(tram_agg, on="unit_code", how="left")
        .merge(census, on="unit_code", how="left")
    )
    acc["station_count"] = acc.station_count.fillna(0).astype(int)
    acc["stations_with_passenger_data"] = acc.stations_with_passenger_data.fillna(0).astype(int)
    acc["tram_stop_count"] = acc.tram_stop_count.fillna(0).astype(int)
    acc["rail_stop_count_all"] = acc.station_count + acc.tram_stop_count
    acc["station_density_per_100km2"] = acc.station_count / acc.area_km2 * 100
    acc["stations_per_10k_pop"] = acc.station_count / acc.pop_2025 * 10_000
    acc["tram_stops_per_10k_pop"] = acc.tram_stop_count / acc.pop_2025 * 10_000
    acc["passengers_per_capita"] = acc.station_passengers_sum / acc.pop_2025
    acc["passenger_data_share"] = np.where(
        acc.station_count > 0, acc.stations_with_passenger_data / acc.station_count, 0.0
    )
    acc["population_density"] = acc.pop_2025 / acc.area_km2

    zero = acc[acc.station_count == 0].sort_values("pop_2025", ascending=False)
    zero.to_csv(OUT_ZERO, index=False, encoding="utf-8-sig")

    # Unit-level accessibility table (1,059 rows).
    acc_cols = [
        "unit_code",
        "unit_name_2023",
        "level",
        "area_km2",
        "pop_2025",
        "census_density",
        "population_density",
        "station_count",
        "station_density_per_100km2",
        "stations_per_10k_pop",
        "station_passengers_sum",
        "stations_with_passenger_data",
        "passenger_data_share",
        "passengers_per_capita",
        "tram_stop_count",
        "tram_stops_per_10k_pop",
        "tram_passengers_sum",
        "rail_stop_count_all",
    ]
    acc[acc_cols].to_csv(OUT_ACCESS, index=False, encoding="utf-8-sig")

    # Merge onto the vacancy panel.
    cols = [
        "unit_code",
        "population_density",
        "pop_2025",
        "area_km2",
        "station_count",
        "station_density_per_100km2",
        "stations_per_10k_pop",
        "station_passengers_sum",
        "stations_with_passenger_data",
        "passenger_data_share",
        "passengers_per_capita",
        "tram_stop_count",
        "tram_stops_per_10k_pop",
        "tram_passengers_sum",
        "rail_stop_count_all",
    ]
    panel_out = panel.merge(acc[cols], left_on="region_code", right_on="unit_code", how="left")
    panel_out = panel_out.drop(columns=["unit_code"])
    panel_out.to_csv(OUT_PANEL, index=False, encoding="utf-8-sig")

    pilot = panel_out[panel_out.region_code.str[:2].isin(["13", "20", "39"])].copy()
    pilot.to_csv(OUT_PILOT, index=False, encoding="utf-8-sig")

    # Validation report.
    lines = []
    lines.append("Accessibility v0 validation\n" + "=" * 40)
    lines.append("Headline = heavy-rail stations (JR, private, subway, monorail, AGT, maglev).")
    lines.append("Tram-only stops (軌道) are reported separately, not in station_count.")
    lines.append(f"Stations in N02 (after exclusions): {len(stations):,}")
    lines.append(
        f"  heavy-rail facilities: {int(stations.has_heavy_rail.sum()):,}; "
        f"tram-only stops: {int((~stations.has_heavy_rail).sum()):,}"
    )
    lines.append(f"Assigned within panel: {len(panel_stations):,}")
    lines.append(f"  heavy: {len(heavy):,}; tram-only: {len(tram):,}")
    lines.append(f"Outside panel: {(~stations.in_panel).sum():,}")
    lines.append(f"Unassigned (no polygon): {stations.unit_code.isna().sum():,}")
    lines.append(f"Units in panel: {len(panel_out):,}")
    lines.append(f"Units with accessibility row: {panel_out.station_count.notna().sum():,}")
    lines.append(f"Units with zero heavy-rail stations: {len(zero):,} ({len(zero)/len(acc):.1%})")
    lines.append(f"Total heavy-rail stations assigned to panel: {int(acc.station_count.sum()):,}")
    lines.append(f"Total tram-only stops assigned to panel: {int(acc.tram_stop_count.sum()):,}")
    lines.append(
        f"Heavy-rail passenger data coverage: {acc.stations_with_passenger_data.sum():,} / "
        f"{acc.station_count.sum():,} stations "
        f"({acc.stations_with_passenger_data.sum()/acc.station_count.sum():.1%})"
    )
    rho, p = spearmanr(acc.station_density_per_100km2, acc.population_density)
    lines.append(f"Spearman station density vs population density: rho={rho:.3f}, p={p:.2e}")
    rho2, p2 = spearmanr(acc.station_count, acc.pop_2025)
    lines.append(f"Spearman station count vs population: rho={rho2:.3f}, p={p2:.2e}")
    lines.append("\nTop 15 by station count:")
    lines.append(
        acc.nlargest(15, "station_count")[
            ["unit_code", "unit_name_2023", "station_count", "station_density_per_100km2", "pop_2025"]
        ].to_string(index=False)
    )
    lines.append("\nTop 10 by station density (per 100 km2):")
    lines.append(
        acc.nlargest(10, "station_density_per_100km2")[
            ["unit_code", "unit_name_2023", "station_count", "station_density_per_100km2"]
        ].to_string(index=False)
    )
    lines.append("\nZero heavy-rail stations, largest population:")
    lines.append(zero.head(15)[["unit_code", "unit_name_2023", "level", "pop_2025", "tram_stop_count"]].to_string(index=False))
    lines.append("\nTop 10 by tram-stop count:")
    lines.append(
        acc.nlargest(10, "tram_stop_count")[
            ["unit_code", "unit_name_2023", "station_count", "tram_stop_count", "pop_2025"]
        ].to_string(index=False)
    )
    lines.append("\nTokyo special wards, top 8 by heavy-rail station count:")
    lines.append(
        acc[acc.level == "special_ward"]
        .nlargest(8, "station_count")[
            ["unit_code", "unit_name_2023", "station_count", "tram_stop_count", "pop_2025"]
        ]
        .to_string(index=False)
    )
    lines.append("\nNagano sample:")
    lines.append(
        acc[(acc.unit_code.str[:2] == "20") & (acc.station_count > 0)]
        .head(8)[["unit_code", "unit_name_2023", "station_count", "pop_2025"]]
        .to_string(index=False)
    )
    lines.append("\nKochi sample:")
    lines.append(
        acc[(acc.unit_code.str[:2] == "39") & (acc.station_count > 0)]
        .head(8)[["unit_code", "unit_name_2023", "station_count", "pop_2025"]]
        .to_string(index=False)
    )
    report = "\n".join(lines)
    OUT_REPORT.write_text(report + "\n", encoding="utf-8")
    print("\n" + report)

    print(f"\nWrote {OUT_ACCESS}, {OUT_PANEL}, {OUT_PILOT}, {OUT_ASSIGN}, {OUT_ZERO}, {OUT_REPORT}")


if __name__ == "__main__":
    main()
