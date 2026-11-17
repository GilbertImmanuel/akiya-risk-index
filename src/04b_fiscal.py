"""Parse the municipal fiscal strength index from the Social and Demographic
Statistics System (SSDSE).

Source: e-Stat API, SSDSE table D 行政基盤 (`statsDataId=0000020204`),
indicator `D2201_財政力指数（市町村財政）`, fiscal year 2022.

FY2022 is the latest year available in this table (FY2023/2024 return no data).
The index is a ratio; higher means stronger own-source fiscal capacity.

Run:
    uv run python src/04b_fiscal.py
"""

from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
config = importlib.import_module("00_config")

RAW = config.DATA_RAW / "estat_ssdse_fiscal_2022_2026-11-17.json"
OUT = config.DATA_INTERIM / "fiscal_2022.csv"


def area_names(class_inf: dict) -> dict[str, str]:
    for obj in class_inf["CLASS_OBJ"]:
        if obj["@id"] == "area":
            classes = obj["CLASS"] if isinstance(obj["CLASS"], list) else [obj["CLASS"]]
            return {c["@code"]: c["@name"] for c in classes}
    raise ValueError("Area metadata not found")


def main() -> None:
    raw = json.loads(RAW.read_text(encoding="utf-8"))
    stat = raw["GET_STATS_DATA"]["STATISTICAL_DATA"]
    names = area_names(stat["CLASS_INF"])
    values = stat["DATA_INF"]["VALUE"]
    df = pd.DataFrame(values).rename(columns={"@area": "area_code"})
    df["fiscal_strength_index"] = pd.to_numeric(df["$"], errors="coerce")
    df["area_name"] = df["area_code"].map(names)
    df = df[["area_code", "area_name", "fiscal_strength_index"]].sort_values("area_code")

    if len(df) != 1913:
        raise ValueError(f"Expected 1,913 areas, found {len(df)}")
    if df["fiscal_strength_index"].isna().any():
        missing = int(df["fiscal_strength_index"].isna().sum())
        print(f"Warning: {missing} areas have no fiscal strength index (wards).")

    # Check coverage against the 2023 analysis universe. Special wards are
    # expected to be missing because the index is municipal, not ward-level.
    vacancy = pd.read_csv(config.VACANCY_2023_CSV, dtype={"region_code": str})
    vacancy = vacancy.loc[vacancy["analysis_unit"], ["region_code", "level"]]
    check = vacancy.merge(
        df, left_on="region_code", right_on="area_code", how="left"
    )
    missing = check[check["fiscal_strength_index"].isna()]
    print(
        "Fiscal coverage in 2023 universe:",
        f"{len(check) - len(missing)}/{len(check)}",
    )
    if not missing.empty:
        print("Missing by level:", missing.groupby("level").size().to_dict())

    df.to_csv(OUT, index=False, encoding="utf-8")
    print(
        "Fiscal QA:",
        f"areas={len(df)}",
        f"min={df['fiscal_strength_index'].min():.3f}",
        f"median={df['fiscal_strength_index'].median():.3f}",
        f"max={df['fiscal_strength_index'].max():.3f}",
    )
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
