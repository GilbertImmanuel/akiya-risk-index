"""Export the public map data for the Quarto site.

Inputs:
- data/processed/panel_with_accessibility_2023.csv
- data/interim/census_2025.csv (population change)
- data/interim/fiscal_2022.csv (fiscal strength)
- data/interim/municipal_boundaries.gpkg

Outputs:
- docs/data/municipalities.geojson
- docs/data/panel.json
- docs/data/meta.json

Run:
    uv run python src/07_export_map.py
"""

from __future__ import annotations

import gzip
import importlib
import json
import sys
from datetime import date
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
import shapely
from shapely.geometry import mapping

sys.path.insert(0, str(Path(__file__).resolve().parent))
config = importlib.import_module("00_config")

PANEL = config.DATA_PROCESSED / "panel_with_accessibility_2023.csv"
CENSUS = config.DATA_INTERIM / "census_2025.csv"
FISCAL = config.DATA_INTERIM / "fiscal_2022.csv"
BOUNDARIES = config.DATA_INTERIM / "municipal_boundaries.gpkg"
OUT_GEOJSON = config.DOCS_DATA / "municipalities.geojson"
OUT_PANEL = config.DOCS_DATA / "panel.json"
OUT_META = config.DOCS_DATA / "meta.json"

LEVEL_LABELS = {
    "city": "City",
    "designated_city": "Designated city",
    "special_ward": "Special ward",
    "town_village": "Town or village",
}

METRICS = [
    {
        "key": "dilapidated",
        "field": "dilapidated_other_rate_2023",
        "class_field": "class_dilapidated",
        "label": "Dilapidated other-vacancy rate",
        "short_label": "Dilapidated vacancy",
        "definition": "Dwellings classified as dilapidated “other vacant” as a share of all dwellings in 2023.",
        "unit": "%",
        "format": "percent",
        "breaks": [1, 2, 3, 5],
        "labels": ["<1%", "1–2%", "2–3%", "3–5%", "≥5%"],
        "colors": ["#F2E6E2", "#E3B9B0", "#D18778", "#B95645", "#8C2F25"],
        "no_data": "#B9C2C8",
        "direction": "higher_worse",
        "source": "2023 Housing and Land Survey, tables 34-2 and 1-2-1",
        "note": "",
    },
    {
        "key": "vacancy",
        "field": "vacancy_rate_2023",
        "class_field": "class_vacancy",
        "label": "Total vacancy rate",
        "short_label": "Total vacancy",
        "definition": "All vacant dwellings as a share of all dwellings in 2023.",
        "unit": "%",
        "format": "percent",
        "breaks": [10, 15, 20, 25],
        "labels": ["<10%", "10–15%", "15–20%", "20–25%", "≥25%"],
        "colors": ["#F2E6E2", "#E8C4BB", "#D89484", "#BE5F4D", "#8C2F25"],
        "no_data": "#B9C2C8",
        "direction": "higher_worse",
        "source": "2023 Housing and Land Survey, tables 34-2 and 1-2-1",
        "note": "Includes rental, sale, secondary, and other vacant dwellings.",
    },
    {
        "key": "dilapidated_change",
        "field": "dilapidated_other_rate_change_2018_2023",
        "class_field": "class_dilapidated_change",
        "label": "Change in dilapidated other-vacancy rate",
        "short_label": "Dilapidated change",
        "definition": "Change in the dilapidated “other vacant” share of dwellings between 2018 and 2023, in percentage points.",
        "unit": "pp",
        "format": "pp",
        "breaks": [-2, -1, 0, 1],
        "labels": ["<-2", "-2 to -1", "-1 to 0", "0 to 1", "≥1"],
        "colors": ["#2C6C8A", "#8FB3C4", "#E8EDF0", "#D89A8A", "#A63A2B"],
        "no_data": "#B9C2C8",
        "direction": "diverging",
        "source": "2018 and 2023 Housing and Land Survey",
        "note": "Two municipalities lack a 2018 comparison.",
    },
    {
        "key": "population_change",
        "field": "pop_change_rate_5y",
        "class_field": "class_population_change",
        "label": "Population change, 2020–2025",
        "short_label": "Population change",
        "definition": "Change in municipal population between the 2020 and 2025 Censuses.",
        "unit": "%",
        "format": "percent",
        "breaks": [-10, -5, 0, 5],
        "labels": ["<-10%", "-10 to -5%", "-5 to 0%", "0 to 5%", "≥5%"],
        "colors": ["#A63A2B", "#D89A8A", "#E8EDF0", "#8FB3C4", "#2C6C8A"],
        "no_data": "#B9C2C8",
        "direction": "diverging",
        "source": "2020 and 2025 Censuses",
        "note": "",
    },
    {
        "key": "fiscal",
        "field": "fiscal_strength_index",
        "class_field": "class_fiscal",
        "label": "Fiscal strength index",
        "short_label": "Fiscal strength",
        "definition": "Municipal fiscal strength index for FY2022. Higher values indicate stronger own-source fiscal capacity.",
        "unit": "index",
        "format": "index",
        "breaks": [0.3, 0.5, 0.7, 0.9],
        "labels": ["<0.3", "0.3–0.5", "0.5–0.7", "0.7–0.9", "≥0.9"],
        "colors": ["#E4EFEC", "#B7D6D0", "#7FB5AA", "#4A8C80", "#245E55"],
        "no_data": "#B9C2C8",
        "direction": "higher_better",
        "source": "FY2022 local finance survey",
        "note": "The 23 special wards have no municipal fiscal-strength index.",
    },
    {
        "key": "station_density",
        "field": "station_density_per_100km2",
        "class_field": "class_station_density",
        "label": "Heavy-rail station density",
        "short_label": "Station density",
        "definition": "Heavy-rail stations per 100 square kilometres in 2023. Tram stops are excluded.",
        "unit": "per 100 km²",
        "format": "density",
        "breaks": [0, 1, 3, 10, 30],
        "labels": ["No station", "0–1", "1–3", "3–10", "10–30", "≥30"],
        "colors": ["#D8DEE2", "#E4EEF3", "#BCD5E2", "#84B0C7", "#4D86A6", "#245F7E"],
        "no_data": "#B9C2C8",
        "direction": "higher_better",
        "source": "KSJ N02 and S12, FY2023",
        "note": "126 municipalities have no heavy-rail station. That is a measured zero, not missing data.",
    },
]


def assign_class(values: pd.Series, breaks: list[float], zero_is_class: bool = False) -> pd.Series:
    numeric = pd.to_numeric(values, errors="coerce")
    if zero_is_class:
        adjusted = numeric.where(numeric > 0, -1)
        classes = np.digitize(adjusted.fillna(-2), breaks, right=False) + 1
    else:
        classes = np.digitize(numeric.fillna(-np.inf), breaks, right=False) + 1
    classes[numeric.isna()] = 0
    return pd.Series(classes.astype(int), index=values.index)


def round_coords(obj, ndigits: int = 3):
    if isinstance(obj, (list, tuple)):
        return [round_coords(item, ndigits) for item in obj]
    if isinstance(obj, float):
        return round(obj, ndigits)
    return obj


def clean(value):
    if pd.isna(value):
        return None
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        return float(value)
    return value


def write_json(path: Path, payload) -> None:
    text = json.dumps(payload, ensure_ascii=False, separators=(",", ":"), allow_nan=False)
    path.write_text(text, encoding="utf-8")
    compressed = gzip.compress(text.encode("utf-8"))
    print(f"{path.name}: {len(text) / 1e6:.2f} MB raw, {len(compressed) / 1e6:.2f} MB gzip")


def main() -> None:
    panel = pd.read_csv(PANEL, dtype={"region_code": str})
    census = pd.read_csv(CENSUS, dtype={"area_code": str})
    fiscal = pd.read_csv(FISCAL, dtype={"area_code": str})

    if len(panel) != 1059:
        raise ValueError(f"Expected 1,059 panel rows, found {len(panel)}")

    prefectures = census.loc[census["level"] == "prefecture", ["area_code", "area_name"]]
    pref_map = {code[:2]: name for code, name in zip(prefectures["area_code"], prefectures["area_name"])}

    pop = census[["area_code", "pop_change_rate_5y"]].rename(columns={"area_code": "region_code"})
    fis = fiscal[["area_code", "fiscal_strength_index"]].rename(columns={"area_code": "region_code"})

    df = panel.merge(pop, on="region_code", how="left", validate="one_to_one")
    df = df.merge(fis, on="region_code", how="left", validate="one_to_one")
    df["prefecture"] = df["region_code"].str[:2].map(pref_map)
    df["level_label"] = df["level"].map(LEVEL_LABELS)

    for metric in METRICS:
        metric["zero_is_class"] = metric["key"] == "station_density"
        df[metric["class_field"]] = assign_class(
            df[metric["field"]], metric["breaks"], metric.get("zero_is_class", False)
        )

    boundaries = gpd.read_file(BOUNDARIES, layer="municipalities_2023")
    boundaries = boundaries.to_crs(4326)
    merged = boundaries.merge(
        df,
        left_on="unit_code",
        right_on="region_code",
        how="left",
        validate="one_to_one",
    )
    if len(merged) != 1059 or merged["region_code"].isna().any():
        raise ValueError("Boundary and panel merge did not produce 1,059 matched units")

    simplified = merged.to_crs(6933)
    simplified["geometry"] = simplified.geometry.simplify(500, preserve_topology=True)
    simplified = simplified.to_crs(4326)
    simplified["geometry"] = shapely.set_precision(simplified.geometry, 0.001)
    invalid = ~simplified.geometry.is_valid
    if invalid.any():
        print(f"Repairing {int(invalid.sum())} simplified geometries")
        simplified.loc[invalid, "geometry"] = simplified.loc[invalid, "geometry"].make_valid()
    simplified = simplified[~simplified.geometry.is_empty].copy()
    if len(simplified) != 1059 or not simplified.geometry.is_valid.all():
        raise ValueError("Simplified boundary layer failed validation")

    points = simplified.geometry.representative_point()
    simplified["lon"] = points.x.round(4)
    simplified["lat"] = points.y.round(4)

    features = []
    panel_records = []
    for row in simplified.itertuples():
        data = row._asdict()
        props = {
            "code": data["unit_code"],
            "name": data["unit_name_2023"],
            "prefecture": data["prefecture"],
            "level": data["level_label"],
        }
        for metric in METRICS:
            props[metric["class_field"]] = int(data[metric["class_field"]])
        features.append(
            {
                "type": "Feature",
                "properties": props,
                "geometry": round_coords(mapping(data["geometry"])),
            }
        )

        record = {
            "code": data["unit_code"],
            "name": data["unit_name_2023"],
            "prefecture": data["prefecture"],
            "level": data["level_label"],
            "lat": clean(data["lat"]),
            "lon": clean(data["lon"]),
            "station_count": int(data["station_count"]),
        }
        for metric in METRICS:
            value = data[metric["field"]]
            record[metric["key"]] = round(float(value), 2) if pd.notna(value) else None
        panel_records.append(record)

    geojson = {"type": "FeatureCollection", "features": features}
    meta = {
        "build_date": date.today().isoformat(),
        "unit_count": 1059,
        "coverage": {
            "missing_towns_villages": 682,
            "fiscal_no_data": int(df["fiscal_strength_index"].isna().sum()),
            "change_no_data": int(df["dilapidated_other_rate_change_2018_2023"].isna().sum()),
            "zero_station": int((df["station_density_per_100km2"] == 0).sum()),
        },
        "metrics": {
            metric["key"]: {
                key: value
                for key, value in metric.items()
                if key not in {"field", "class_field", "zero_is_class"}
            }
            for metric in METRICS
        },
        "sources": [
            "Housing and Land Survey 2023, Statistics Bureau of Japan",
            "2018 Housing and Land Survey",
            "2020 and 2025 Censuses",
            "FY2022 local finance survey",
            "KSJ N02 and S12, FY2023",
            "GSI pale basemap",
        ],
    }

    write_json(OUT_GEOJSON, geojson)
    write_json(OUT_PANEL, panel_records)
    write_json(OUT_META, meta)

    print(f"Features: {len(features):,}; panel records: {len(panel_records):,}")
    print(
        "Coverage:",
        f"fiscal no data {meta['coverage']['fiscal_no_data']},",
        f"change no data {meta['coverage']['change_no_data']},",
        f"zero station {meta['coverage']['zero_station']}",
    )


if __name__ == "__main__":
    main()
