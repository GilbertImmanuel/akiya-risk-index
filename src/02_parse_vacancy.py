"""Parse the 2023 Housing and Land Survey municipal vacancy table (34-2).

The raw Excel has one sheet with nine header rows and 26,943 data rows. The
first column is a hierarchy code:

    a = national / prefecture
    1 = designated city (and the Tokyo special-wards group)
    0 = ward (designated-city ward or Tokyo special ward)
    2 = city (non-designated)
    3 = town / village

Each region has 21 rows: 3 dilapidation categories x 7 building/structure
combinations. The table contains both designated-city totals and their ward
rows, so summing every row double-counts. This script produces a tidy table
with a single analysis unit per place:

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
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
config = importlib.import_module("00_config")

RAW = config.VACANCY_2023_XLSX
OUT = config.VACANCY_2023_CSV

COLUMNS = [
    "hierarchy",
    "region",
    "dilapidation",
    "building",
    "structure",
    "vacant_total",
    "other",
    "rental",
    "sale",
    "secondary",
]

KEYS = ["region_code", "region_name"]


def load_raw(path: Path) -> pd.DataFrame:
    """Read the raw Excel and split the region label into code and name."""
    df = pd.read_excel(path, header=None, skiprows=9, names=COLUMNS)
    parts = df["region"].str.split("_", n=1, expand=True)
    df["region_code"] = parts[0]
    df["region_name"] = parts[1]
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


def build_table(df: pd.DataFrame) -> pd.DataFrame:
    """Build one row per region with the indicators used by the index."""
    parts = [
        # All vacant dwellings, by category.
        select(
            df,
            dilapidation="0_総数",
            building="0_総数",
            structure="0_総数",
            column="vacant_total",
            name="vacant_total",
        ),
        select(
            df,
            dilapidation="0_総数",
            building="0_総数",
            structure="0_総数",
            column="other",
            name="vacant_other",
        ),
        select(
            df,
            dilapidation="0_総数",
            building="0_総数",
            structure="0_総数",
            column="rental",
            name="vacant_rental",
        ),
        select(
            df,
            dilapidation="0_総数",
            building="0_総数",
            structure="0_総数",
            column="sale",
            name="vacant_sale",
        ),
        select(
            df,
            dilapidation="0_総数",
            building="0_総数",
            structure="0_総数",
            column="secondary",
            name="vacant_secondary",
        ),
        # Dilapidated "other vacant": the headline risk measure.
        select(
            df,
            dilapidation="1_腐朽・破損あり",
            building="0_総数",
            structure="0_総数",
            column="other",
            name="vacant_other_dilapidated",
        ),
        # Detached "other vacant", all conditions.
        select(
            df,
            dilapidation="0_総数",
            building="2_一戸建",
            structure="0_総数",
            column="other",
            name="vacant_other_detached",
        ),
        # Dilapidated detached "other vacant".
        select(
            df,
            dilapidation="1_腐朽・破損あり",
            building="2_一戸建",
            structure="0_総数",
            column="other",
            name="vacant_other_detached_dilapidated",
        ),
    ]

    result = pd.concat(parts, axis=1).reset_index()
    # Merge the hierarchy code back on, using the unique region mapping.
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
    result["year"] = 2023
    result = result.sort_values(["level", "region_code"]).reset_index(drop=True)
    return result


def validate(result: pd.DataFrame) -> None:
    """Check national totals, hierarchy counts, and double-counting."""
    national = result.loc[result["level"] == "national"].iloc[0]
    expected = {
        "vacant_total": 9_001_600,
        "vacant_other": 3_856_000,
        "vacant_rental": 4_435_800,
        "vacant_sale": 326_200,
        "vacant_secondary": 383_500,
    }
    for key, value in expected.items():
        actual = int(national[key])
        if actual != value:
            raise ValueError(f"National total mismatch for {key}: {actual} != {value}")

    counts = result["level"].value_counts().to_dict()
    expected_counts = {
        "national": 1,
        "prefecture": 47,
        "designated_city": 20,
        "special_wards_group": 1,
        "special_ward": 23,
        "designated_city_ward": 175,
        "city": 772,
        "town_village": 244,
    }
    for level, expected_count in expected_counts.items():
        actual = counts.get(level, 0)
        if actual != expected_count:
            raise ValueError(f"Expected {expected_count} {level}, found {actual}")

    analysis = result.loc[result["analysis_unit"]]
    n_analysis = len(analysis)
    if n_analysis != 1059:
        raise ValueError(f"Expected 1,059 analysis units, found {n_analysis}")

    # The analysis units do NOT sum to the national total. The difference is the
    # vacancy in municipalities below the 15,000-population reporting threshold.
    # That gap is a substantive finding, not a bug.
    summed = int(analysis["vacant_total"].sum())
    national_total = int(national["vacant_total"])
    gap = national_total - summed
    if summed != 8_501_240:
        raise ValueError(f"Expected covered vacancy 8,501,240, found {summed:,}")
    if gap != 500_360:
        raise ValueError(f"Expected coverage gap 500,360, found {gap:,}")

    # Prefecture rows should sum to the national total, up to rounding.
    pref = result.loc[result["level"] == "prefecture", "vacant_total"].sum()
    if abs(int(pref) - national_total) > 200:
        raise ValueError(
            f"Prefecture sum {int(pref):,} differs from national {national_total:,}"
        )

    print(
        "National QA passed:",
        f"vacant={national_total:,}",
        f"other={national['vacant_other']:,}",
        f"dilapidated_other={national['vacant_other_dilapidated']:,}",
    )
    print(
        "Hierarchy:",
        f"designated_city={counts.get('designated_city', 0)}",
        f"special_ward={counts.get('special_ward', 0)}",
        f"city={counts.get('city', 0)}",
        f"town_village={counts.get('town_village', 0)}",
        f"analysis_units={n_analysis}",
    )
    print(
        "Coverage:",
        f"covered_vacancy={summed:,}",
        f"uncovered_vacancy={gap:,}",
        f"covered_share={summed / national_total:.1%}",
    )


def main() -> None:
    if not RAW.exists():
        raise FileNotFoundError(f"Raw file not found: {RAW}")
    df = load_raw(RAW)
    result = build_table(df)
    validate(result)
    result.to_csv(OUT, index=False, encoding="utf-8")
    print(f"Wrote {OUT} ({len(result):,} rows)")


if __name__ == "__main__":
    main()
