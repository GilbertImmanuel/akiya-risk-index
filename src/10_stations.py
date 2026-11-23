"""Build the rail-station facility layer from KSJ N02 and S12 (FY2023).

N02 represents each station as a short LineString, once per line/operator.
Stations are collapsed to facilities with the N02 group code (same name within
300 m) and located by the representative point of the merged platform geometry.

Passenger rail only: funicular (code 13) and trolleybus (code 17) are excluded.
S12 passenger counts are operator-level; only records flagged as "listed at this
line's station" (duplicate code 1) carry values, so group sums do not double
count.

Run:
    uv run python src/10_stations.py
"""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd
from shapely.ops import unary_union

sys.path.insert(0, str(Path(__file__).resolve().parent))
config = importlib.import_module("00_config")

N02 = config.DATA_INTERIM / "ksj" / "N02-23_Station.geojson"
S12 = config.DATA_INTERIM / "ksj" / "S12-24_NumberOfPassengers.geojson"
OUT_CSV = config.DATA_INTERIM / "stations.csv"
OUT_GEOJSON = config.DATA_INTERIM / "stations.geojson"

EXCLUDED_RAIL_TYPES = {"13", "17"}  # funicular, trolleybus
TRAM_TYPE = "21"  # 軌道 (street tram); reported separately from heavy rail


def build_stations() -> gpd.GeoDataFrame:
    n02 = gpd.read_file(N02)
    print(f"N02 station records: {len(n02):,}")

    n02 = n02[~n02.N02_001.isin(EXCLUDED_RAIL_TYPES)].copy()
    print(f"After excluding funicular/trolleybus: {len(n02):,} records")

    rows = []
    for code, group in n02.groupby("N02_005g", sort=True):
        geom = unary_union(group.geometry.values)
        point = geom.representative_point()
        rows.append(
            {
                "station_group_code": code,
                "station_name": group.N02_005.iloc[0],
                "operators": ";".join(sorted(group.N02_004.dropna().unique())),
                "lines": ";".join(sorted(group.N02_003.dropna().unique())),
                "rail_types": ";".join(sorted(group.N02_001.unique())),
                "n_line_records": len(group),
                "geometry": point,
            }
        )
    stations = gpd.GeoDataFrame(rows, crs=n02.crs)
    print(f"Station facilities: {len(stations):,}")

    s12 = gpd.read_file(S12)
    # Only records that carry data for their own line (duplicate code 1) and
    # actually report a value (existence code 1). Records with no data or
    # withheld data store 0, which must not be read as a real zero.
    data = s12[(s12.S12_054 == 1) & (s12.S12_055 == 1)].copy()
    pax = (
        data.groupby("S12_001g")
        .agg(
            passengers_2023=("S12_057", "sum"),
            n_passenger_records=("S12_057", "size"),
        )
        .reset_index()
        .rename(columns={"S12_001g": "station_group_code"})
    )
    # Groups with no data at all stay missing, not zero.
    stations = stations.merge(pax, on="station_group_code", how="left")
    stations["passengers_2023"] = stations.passengers_2023.astype("Float64")
    stations["has_passenger_data"] = stations.passengers_2023.notna()

    no_s12 = stations[~stations.has_passenger_data]
    print(f"Facilities without S12 data: {len(no_s12):,} ({len(no_s12)/len(stations):.1%})")
    print(f"Passenger total (daily, FY2023): {stations.passengers_2023.sum():,.0f}")

    stations["lon"] = stations.geometry.x
    stations["lat"] = stations.geometry.y
    stations["has_tram"] = stations.rail_types.str.split(";").apply(lambda x: TRAM_TYPE in x)
    stations["has_heavy_rail"] = stations.rail_types.str.split(";").apply(
        lambda x: any(t != TRAM_TYPE for t in x)
    )
    print(
        f"Heavy-rail facilities: {stations.has_heavy_rail.sum():,}; "
        f"tram-only stops: {(~stations.has_heavy_rail).sum():,}"
    )
    return stations


def main() -> None:
    stations = build_stations()

    cols = [
        "station_group_code",
        "station_name",
        "operators",
        "lines",
        "rail_types",
        "n_line_records",
        "lon",
        "lat",
        "passengers_2023",
        "has_passenger_data",
        "n_passenger_records",
        "has_heavy_rail",
        "has_tram",
    ]
    stations[cols].to_csv(OUT_CSV, index=False, encoding="utf-8-sig")
    stations[cols + ["geometry"]].to_file(OUT_GEOJSON, driver="GeoJSON")
    print(f"\nWrote {OUT_CSV} and {OUT_GEOJSON}")

    print("\nLargest stations:")
    print(
        stations.nlargest(10, "passengers_2023")[
            ["station_name", "operators", "passengers_2023"]
        ].to_string(index=False)
    )
    print("\nFacilities by number of line records:")
    print(stations.n_line_records.value_counts().sort_index().to_string())


if __name__ == "__main__":
    main()
