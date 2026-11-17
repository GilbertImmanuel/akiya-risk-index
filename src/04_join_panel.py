"""Assemble the first pilot panel: vacancy + census + fiscal capacity.

This is a Phase 0 pilot, not the final index. It tests the joins and coverage
for Tokyo, Nagano, and Kochi. Rates use households as a provisional denominator
because the total-dwelling table has not been pulled yet; label them as proxies.

Run:
    uv run python src/04_join_panel.py
"""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
config = importlib.import_module("00_config")

PILOT_PREFECTURES = {"13": "Tokyo", "20": "Nagano", "39": "Kochi"}
OUT = config.DATA_PROCESSED / "pilot_panel_v0.csv"


def vacancy(year: int) -> pd.DataFrame:
    path = config.VACANCY_2023_CSV if year == 2023 else config.VACANCY_2018_CSV
    df = pd.read_csv(path, dtype={"region_code": str})
    df = df.loc[df["analysis_unit"]].copy()
    keep = [
        "region_code",
        "region_name",
        "level",
        "vacant_total",
        "vacant_other",
        "vacant_other_dilapidated",
        "vacant_other_detached",
        "vacant_other_detached_dilapidated",
    ]
    df = df[keep]
    return df.rename(columns={c: f"{c}_{year}" for c in keep if c not in {"region_code", "level"}})


def main() -> None:
    v23 = vacancy(2023)
    v18 = vacancy(2018).drop(columns=["level"])

    census = pd.read_csv(config.DATA_INTERIM / "census_2025.csv", dtype={"area_code": str})
    census = census.rename(columns={"area_code": "region_code"})
    census = census[
        [
            "region_code",
            "pop_2020",
            "pop_2025",
            "households_2020",
            "households_2025",
            "pop_change_5y",
            "pop_change_rate_5y",
            "household_change_5y",
            "household_change_rate_5y",
            "area_km2",
            "density",
        ]
    ]

    fiscal = pd.read_csv(config.DATA_INTERIM / "fiscal_2022.csv", dtype={"area_code": str})
    fiscal = fiscal.rename(columns={"area_code": "region_code"})
    fiscal = fiscal[["region_code", "fiscal_strength_index"]]

    panel = v23.merge(v18, on="region_code", how="left")
    panel["has_2018"] = panel["vacant_total_2018"].notna()
    panel = panel.merge(census, on="region_code", how="left")
    panel["has_census"] = panel["pop_2025"].notna()
    panel = panel.merge(fiscal, on="region_code", how="left")
    panel["has_fiscal"] = panel["fiscal_strength_index"].notna()

    panel["prefecture_code"] = panel["region_code"].str[:2]
    panel["prefecture"] = panel["prefecture_code"].map(PILOT_PREFECTURES)
    panel = panel[panel["prefecture"].notna()].copy()

    # Provisional rates: households, not dwellings. Label as proxies.
    panel["other_per_1000_hh_2023"] = (
        panel["vacant_other_2023"] / panel["households_2025"] * 1000
    )
    panel["dilapidated_other_per_1000_hh_2023"] = (
        panel["vacant_other_dilapidated_2023"] / panel["households_2025"] * 1000
    )

    panel = panel.sort_values(
        ["prefecture_code", "dilapidated_other_per_1000_hh_2023"],
        ascending=[True, False],
    ).reset_index(drop=True)
    panel.to_csv(OUT, index=False, encoding="utf-8")

    print("Pilot rows by prefecture:", panel.groupby("prefecture").size().to_dict())
    print("Missing census:", int((~panel["has_census"]).sum()))
    print("Missing 2018 vacancy:", int((~panel["has_2018"]).sum()))
    print("Missing fiscal:", int((~panel["has_fiscal"]).sum()))
    print(f"Wrote {OUT} ({len(panel):,} rows)")

    cols = [
        "prefecture",
        "region_name_2023",
        "vacant_other_2023",
        "vacant_other_dilapidated_2023",
        "dilapidated_other_per_1000_hh_2023",
        "pop_change_rate_5y",
        "fiscal_strength_index",
    ]
    print("\nTop 10 by dilapidated other vacant per 1,000 households:")
    print(panel[cols].head(10).to_string(index=False))


if __name__ == "__main__":
    main()
