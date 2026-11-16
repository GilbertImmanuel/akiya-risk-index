"""Parse the Housing and Land Survey municipal vacancy tables (2018, 2023).

The raw Excel layouts differ by wave:

- 2023 table 34-2: 9 header rows, 10 columns.
- 2018 table 35-2: 11 header rows, 17 columns, with extra sequence columns.

Both tables encode the hierarchy in a `地域識別コード` column:

    a = national / prefecture
    1 = designated city (and the Tokyo special-wards group)
    0 = ward (designated-city ward or Tokyo special ward)
    2 = city (non-designated)
    3 = town / village

The table contains both designated-city totals and their ward rows, so summing
every row double-counts. This script produces a tidy table with one analysis
unit per place:

    designated city (city level)
    special ward (individual)
    city (non-designated)
    town / village

Run:
    uv run python src/02_parse_vacancy.py
"""

from __future__ import annotations

import importlib
import sys
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
config = importlib.import_module("00_config")

CANONICAL_COUNTS = ["vacant_total", "other", "rental", "sale", "secondary"]
KEYS = ["region_code", "region_name"]

DILAP_MAP = {
    "0_総数": "total",
    "1_腐朽・破損あり": "dilapidated",
    "2_腐朽・破損なし": "not_dilapidated",
}
STRUCTURE_MAP = {
    "0_総数": "total",
    "1_木造": "wood",
    "2_非木造": "nonwood",
}


@dataclass(frozen=True)
class Layout:
    year: int
    path: Path
    skiprows: int
    hierarchy_col: int
    region_col: int
    dilap_col: int
    building_col: int
    structure_col: int
    count_cols: tuple[int, int, int, int, int]
    count_order: tuple[str, str, str, str, str]
    building_map: dict[str, str]


LAYOUTS = {
    2023: Layout(
        year=2023,
        path=config.VACANCY_2023_XLSX,
        skiprows=9,
        hierarchy_col=0,
        region_col=1,
        dilap_col=2,
        building_col=3,
        structure_col=4,
        count_cols=(5, 6, 7, 8, 9),
        count_order=("vacant_total", "other", "rental", "sale", "secondary"),
        building_map={
            "0_総数": "total",
            "2_一戸建": "detached",
            "3_長屋建・共同住宅・その他": "multi",
        },
    ),
    2018: Layout(
        year=2018,
        path=config.VACANCY_2018_XLSX,
        skiprows=11,
        hierarchy_col=4,
        region_col=5,
        dilap_col=7,
        building_col=9,
        structure_col=11,
        count_cols=(12, 13, 14, 15, 16),
        count_order=("vacant_total", "secondary", "rental", "sale", "other"),
        building_map={
            "00_総数": "total",
            "11_一戸建": "detached",
            "20_長屋建・共同住宅・その他": "multi",
        },
    ),
}

OUTPUTS = {
    2023: config.VACANCY_2023_CSV,
    2018: config.VACANCY_2018_CSV,
}

EXPECTED = {
    2023: {
        "national": {
            "vacant_total": 9_001_600,
            "vacant_other": 3_856_000,
            "vacant_rental": 4_435_800,
            "vacant_sale": 326_200,
            "vacant_secondary": 383_500,
        },
        "counts": {
            "national": 1,
            "prefecture": 47,
            "designated_city": 20,
            "special_wards_group": 1,
            "special_ward": 23,
            "designated_city_ward": 175,
            "city": 772,
            "town_village": 244,
        },
        "analysis_units": 1059,
        "covered_vacancy": 8_501_240,
    },
    2018: {
        "national": {
            "vacant_total": 8_488_600,
            "vacant_other": 3_487_200,
            "vacant_rental": 4_327_200,
            "vacant_sale": 293_200,
            "vacant_secondary": 381_000,
        },
        "counts": {
            "national": 1,
            "prefecture": 47,
            "designated_city": 20,
            "special_wards_group": 1,
            "special_ward": 23,
            "designated_city_ward": 175,
            "city": 772,
            "town_village": 271,
        },
        "analysis_units": 1086,
        "covered_vacancy": 8_077_270,
    },
}


def load_raw(layout: Layout) -> pd.DataFrame:
    """Read one Excel layout and normalise the labels and count columns."""
    raw = pd.read_excel(layout.path, header=None, skiprows=layout.skiprows, dtype=object)
    cols = [
        layout.hierarchy_col,
        layout.region_col,
        layout.dilap_col,
        layout.building_col,
        layout.structure_col,
        *layout.count_cols,
    ]
    df = raw.iloc[:, cols].copy()
    df.columns = [
        "hierarchy",
        "region",
        "dilapidation",
        "building",
        "structure",
        *layout.count_order,
    ]
    df = df[
        ["hierarchy", "region", "dilapidation", "building", "structure", *CANONICAL_COUNTS]
    ]

    df = df[df["region"].notna()].copy()
    df["hierarchy"] = df["hierarchy"].astype(str)
    df["region"] = df["region"].astype(str)
    df = df[df["region"].str.contains("_", regex=False)].copy()

    parts = df["region"].str.split("_", n=1, expand=True)
    df["region_code"] = parts[0]
    df["region_name"] = parts[1]

    df["dilapidation"] = df["dilapidation"].map(DILAP_MAP).fillna(df["dilapidation"])
    df["building"] = df["building"].map(layout.building_map).fillna(df["building"])
    df["structure"] = df["structure"].map(STRUCTURE_MAP).fillna(df["structure"])

    for column in CANONICAL_COUNTS:
        df[column] = pd.to_numeric(df[column], errors="coerce").fillna(0).astype("int64")

    return df


def select(
    df: pd.DataFrame,
    *,
    dilapidation: str,
    building: str,
    structure: str,
    column: str,
    name: str,
) -> pd.DataFrame:
    """Select one cell per region and rename it."""
    mask = (
        (df["dilapidation"] == dilapidation)
        & (df["building"] == building)
        & (df["structure"] == structure)
    )
    out = df.loc[mask, KEYS + [column]].copy()
    if out.duplicated(KEYS).any():
        raise ValueError(f"Duplicate rows for {name}")
    out = out.rename(columns={column: name})
    return out.set_index(KEYS)


def classify(hierarchy: str, code: str) -> str:
    """Return a descriptive level for each region."""
    if hierarchy == "a":
        return "national" if code == "00000" else "prefecture"
    if hierarchy == "1":
        return "special_wards_group" if code == "13100" else "designated_city"
    if hierarchy == "0":
        return "special_ward" if code.startswith("131") else "designated_city_ward"
    if hierarchy == "2":
        return "city"
    if hierarchy == "3":
        return "town_village"
    return "unknown"


def build_table(df: pd.DataFrame, year: int) -> pd.DataFrame:
    """Build one row per region with the indicators used by the index."""
    parts = [
        select(
            df,
            dilapidation="total",
            building="total",
            structure="total",
            column="vacant_total",
            name="vacant_total",
        ),
        select(
            df,
            dilapidation="total",
            building="total",
            structure="total",
            column="other",
            name="vacant_other",
        ),
        select(
            df,
            dilapidation="total",
            building="total",
            structure="total",
            column="rental",
            name="vacant_rental",
        ),
        select(
            df,
            dilapidation="total",
            building="total",
            structure="total",
            column="sale",
            name="vacant_sale",
        ),
        select(
            df,
            dilapidation="total",
            building="total",
            structure="total",
            column="secondary",
            name="vacant_secondary",
        ),
        select(
            df,
            dilapidation="dilapidated",
            building="total",
            structure="total",
            column="other",
            name="vacant_other_dilapidated",
        ),
        select(
            df,
            dilapidation="total",
            building="detached",
            structure="total",
            column="other",
            name="vacant_other_detached",
        ),
        select(
            df,
            dilapidation="dilapidated",
            building="detached",
            structure="total",
            column="other",
            name="vacant_other_detached_dilapidated",
        ),
    ]

    result = pd.concat(parts, axis=1).reset_index()
    hierarchy = (
        df[["region_code", "hierarchy"]]
        .drop_duplicates()
        .set_index("region_code")["hierarchy"]
    )
    result["hierarchy"] = result["region_code"].map(hierarchy)
    result["level"] = [
        classify(h, c) for h, c in zip(result["hierarchy"], result["region_code"])
    ]
    result["analysis_unit"] = result["level"].isin(
        ["designated_city", "special_ward", "city", "town_village"]
    )
    result["year"] = year
    return result.sort_values(["level", "region_code"]).reset_index(drop=True)


def validate(result: pd.DataFrame, year: int) -> None:
    """Check national totals, hierarchy counts, and coverage."""
    expected = EXPECTED[year]
    national = result.loc[result["level"] == "national"].iloc[0]
    for key, value in expected["national"].items():
        actual = int(national[key])
        if actual != value:
            raise ValueError(f"{year}: national mismatch for {key}: {actual} != {value}")

    counts = result["level"].value_counts().to_dict()
    for level, expected_count in expected["counts"].items():
        actual = counts.get(level, 0)
        if actual != expected_count:
            raise ValueError(f"{year}: expected {expected_count} {level}, found {actual}")

    analysis = result.loc[result["analysis_unit"]]
    n_analysis = len(analysis)
    if n_analysis != expected["analysis_units"]:
        raise ValueError(
            f"{year}: expected {expected['analysis_units']} analysis units, "
            f"found {n_analysis}"
        )

    summed = int(analysis["vacant_total"].sum())
    national_total = int(national["vacant_total"])
    gap = national_total - summed
    if expected["covered_vacancy"] is not None:
        if summed != expected["covered_vacancy"]:
            raise ValueError(
                f"{year}: expected covered {expected['covered_vacancy']:,}, "
                f"found {summed:,}"
            )
    else:
        print(f"{year}: covered vacancy = {summed:,}; uncovered = {gap:,}")

    # Prefecture rows should sum to the national total, up to rounding.
    pref = result.loc[result["level"] == "prefecture", "vacant_total"].sum()
    if abs(int(pref) - national_total) > 1_000:
        raise ValueError(
            f"{year}: prefecture sum {int(pref):,} differs from {national_total:,}"
        )

    print(
        f"{year} QA passed:",
        f"vacant={national_total:,}",
        f"other={national['vacant_other']:,}",
        f"dilapidated_other={national['vacant_other_dilapidated']:,}",
        f"analysis_units={n_analysis}",
        f"covered={summed:,}",
        f"uncovered={gap:,}",
        f"covered_share={summed / national_total:.1%}",
    )


def main() -> None:
    for year in (2023, 2018):
        layout = LAYOUTS[year]
        if not layout.path.exists():
            raise FileNotFoundError(f"Raw file not found: {layout.path}")
        df = load_raw(layout)
        result = build_table(df, year)
        validate(result, year)
        out = OUTPUTS[year]
        result.to_csv(out, index=False, encoding="utf-8")
        print(f"Wrote {out} ({len(result):,} rows)")


if __name__ == "__main__":
    main()
