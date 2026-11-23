"""Parse the total-dwelling tables for 2023 and 2018.

Sources:
- 2023 Housing and Land Survey table 1-2-1 (`statsDataId=0004021421`)
- 2018 Housing and Land Survey table 1-2-1 (`statsDataId=0003355290`)

The category codes differ between waves:

2023: 221 = other vacant, 222 = rental, 223 = sale, 224 = secondary
2018: 221 = secondary, 222 = rental, 223 = sale, 224 = other vacant

This script maps by year, not by label position.

Run:
    uv run python src/04c_dwellings.py
"""

from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
config = importlib.import_module("00_config")

LAYOUTS = {
    2023: {
        "raw": config.DATA_RAW / "estat_2023_table1-2-1_2026-11-23.json",
        "out": config.DATA_INTERIM / "dwellings_2023.csv",
        "expected_total": 65_047_000,
        "expected_vacant": 9_002_000,
        "expected_other": 3_856_000,
        "categories": {
            "0": "total_dwellings",
            "22": "vacant_total",
            "221": "vacant_other",
            "222": "vacant_rental",
            "223": "vacant_sale",
            "224": "vacant_secondary",
        },
    },
    2018: {
        "raw": config.DATA_RAW / "estat_2018_table1-2-1_2026-11-23.json",
        "out": config.DATA_INTERIM / "dwellings_2018.csv",
        "expected_total": 62_407_000,
        "expected_vacant": 8_489_000,
        "expected_other": 3_487_000,
        "categories": {
            "0": "total_dwellings",
            "22": "vacant_total",
            "221": "vacant_secondary",
            "222": "vacant_rental",
            "223": "vacant_sale",
            "224": "vacant_other",
        },
    },
}


def area_names(class_inf: dict) -> dict[str, str]:
    for obj in class_inf["CLASS_OBJ"]:
        if obj["@id"] == "area":
            classes = obj["CLASS"] if isinstance(obj["CLASS"], list) else [obj["CLASS"]]
            return {c["@code"]: c["@name"] for c in classes}
    raise ValueError("Area metadata not found")


def classify(code: str) -> str:
    if code == "00000":
        return "national"
    if code.endswith("000"):
        return "prefecture"
    return "municipality"


def parse_year(year: int, layout: dict) -> pd.DataFrame:
    raw = json.loads(layout["raw"].read_text(encoding="utf-8"))
    stat = raw["GET_STATS_DATA"]["STATISTICAL_DATA"]
    names = area_names(stat["CLASS_INF"])

    df = pd.DataFrame(stat["DATA_INF"]["VALUE"]).rename(
        columns={"@area": "area_code", "@cat01": "cat01"}
    )
    df["value"] = pd.to_numeric(df["$"], errors="coerce")
    df = df[df["cat01"].isin(layout["categories"])].copy()

    wide = df.pivot_table(
        index="area_code", columns="cat01", values="value", aggfunc="first"
    ).reset_index()
    wide = wide.rename(columns=layout["categories"])
    wide["area_name"] = wide["area_code"].map(names)
    wide["level"] = wide["area_code"].map(classify)
    wide["year"] = year

    national = wide.loc[wide["level"] == "national"].iloc[0]
    checks = {
        "total_dwellings": layout["expected_total"],
        "vacant_total": layout["expected_vacant"],
        "vacant_other": layout["expected_other"],
    }
    for key, expected in checks.items():
        actual = int(national[key])
        # The published headline is rounded; the API table is the precise count.
        if abs(actual - expected) > 1_000:
            raise ValueError(f"{year}: {key} {actual:,} differs from {expected:,}")

    expected_areas = 1283 if year == 2023 else 1310
    if len(wide) != expected_areas:
        raise ValueError(f"{year}: expected {expected_areas} areas, found {len(wide)}")

    wide = wide.sort_values("area_code").reset_index(drop=True)
    wide.to_csv(layout["out"], index=False, encoding="utf-8")
    print(
        f"{year} dwellings QA passed:",
        f"areas={len(wide)}",
        f"total={int(national['total_dwellings']):,}",
        f"vacant={int(national['vacant_total']):,}",
        f"other={int(national['vacant_other']):,}",
    )
    print(f"Wrote {layout['out']}")
    return wide


def coverage_check(year: int, dwellings: pd.DataFrame) -> None:
    """Check total-dwelling coverage and vacancy-count agreement."""
    path = config.VACANCY_2023_CSV if year == 2023 else config.VACANCY_2018_CSV
    v = pd.read_csv(path, dtype={"region_code": str})
    v = v.loc[v["analysis_unit"]].copy()
    m = v.merge(
        dwellings,
        left_on="region_code",
        right_on="area_code",
        how="left",
        suffixes=("", "_1_2_1"),
    )
    missing = int(m["total_dwellings"].isna().sum())
    print(
        f"{year}: total-dwelling coverage "
        f"{len(m) - missing}/{len(m)} analysis units"
    )
    if missing:
        print("Missing:", m.loc[m["total_dwellings"].isna(), "region_code"].tolist()[:20])
    for col in ("vacant_total", "vacant_other"):
        mismatches = int((m[col] != m[f"{col}_1_2_1"]).sum())
        print(f"{year}: {col} mismatches vs 1-2-1: {mismatches}")


def main() -> None:
    for year, layout in LAYOUTS.items():
        dwellings = parse_year(year, layout)
        coverage_check(year, dwellings)


if __name__ == "__main__":
    main()
