"""Assemble the pilot panel: vacancy + total dwellings + census + fiscal.

Pilot for Tokyo, Nagano, and Kochi. Rates now use total dwellings from the
Housing and Land Survey table 1-2-1, not the household proxy. The proxy columns
are retained for comparison.

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
OUT = config.DATA_PROCESSED / "pilot_panel_v1.csv"


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


def dwellings(year: int) -> pd.DataFrame:
    path = config.DATA_INTERIM / f"dwellings_{year}.csv"
    df = pd.read_csv(path, dtype={"area_code": str})
    df = df.rename(columns={"area_code": "region_code"})
    keep = ["region_code", "total_dwellings", "vacant_total", "vacant_other"]
    df = df[keep]
    return df.rename(
        columns={
            "total_dwellings": f"total_dwellings_{year}",
            "vacant_total": f"vacant_total_{year}_1_2_1",
            "vacant_other": f"vacant_other_{year}_1_2_1",
        }
    )


def main() -> None:
    v23 = vacancy(2023)
    v18 = vacancy(2018).drop(columns=["level"])
    d23 = dwellings(2023)
    d18 = dwellings(2018)

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
    panel = panel.merge(d23, on="region_code", how="left")
    panel = panel.merge(d18, on="region_code", how="left")
    panel["has_dwellings_2023"] = panel["total_dwellings_2023"].notna()
    panel["has_dwellings_2018"] = panel["total_dwellings_2018"].notna()
    panel = panel.merge(census, on="region_code", how="left")
    panel["has_census"] = panel["pop_2025"].notna()
    panel = panel.merge(fiscal, on="region_code", how="left")
    panel["has_fiscal"] = panel["fiscal_strength_index"].notna()

    panel["prefecture_code"] = panel["region_code"].str[:2]
    panel["prefecture"] = panel["prefecture_code"].map(PILOT_PREFECTURES)
    panel = panel[panel["prefecture"].notna()].copy()

    # Proper rates: per total dwellings.
    for year in (2023, 2018):
        panel[f"vacancy_rate_{year}"] = (
            panel[f"vacant_total_{year}"] / panel[f"total_dwellings_{year}"] * 100
        )
        panel[f"other_vacancy_rate_{year}"] = (
            panel[f"vacant_other_{year}"] / panel[f"total_dwellings_{year}"] * 100
        )
        if year == 2023:
            panel["dilapidated_other_rate_2023"] = (
                panel["vacant_other_dilapidated_2023"]
                / panel["total_dwellings_2023"]
                * 100
            )
        else:
            panel["dilapidated_other_rate_2018"] = (
                panel["vacant_other_dilapidated_2018"]
                / panel["total_dwellings_2018"]
                * 100
            )

    # Change between the two vacancy waves.
    panel["other_vacancy_rate_change_2018_2023"] = (
        panel["other_vacancy_rate_2023"] - panel["other_vacancy_rate_2018"]
    )
    panel["dilapidated_other_rate_change_2018_2023"] = (
        panel["dilapidated_other_rate_2023"] - panel["dilapidated_other_rate_2018"]
    )

    # Keep the household proxy for comparison.
    panel["other_per_1000_hh_2023"] = (
        panel["vacant_other_2023"] / panel["households_2025"] * 1000
    )
    panel["dilapidated_other_per_1000_hh_2023"] = (
        panel["vacant_other_dilapidated_2023"] / panel["households_2025"] * 1000
    )

    # Cross-check the two vacancy tables for the pilot units.
    for year in (2023, 2018):
        for col in ("vacant_total", "vacant_other"):
            a = panel[f"{col}_{year}"]
            b = panel[f"{col}_{year}_1_2_1"]
            mismatches = int((a != b).sum())
            if mismatches:
                print(f"WARNING: {year} {col} mismatches: {mismatches}")

    panel = panel.sort_values(
        ["prefecture_code", "dilapidated_other_rate_2023"],
        ascending=[True, False],
    ).reset_index(drop=True)
    panel.to_csv(OUT, index=False, encoding="utf-8")

    print("Pilot rows by prefecture:", panel.groupby("prefecture").size().to_dict())
    print("Missing census:", int((~panel["has_census"]).sum()))
    print("Missing 2018 vacancy:", int((~panel["has_2018"]).sum()))
    print("Missing 2023 dwellings:", int((~panel["has_dwellings_2023"]).sum()))
    print("Missing 2018 dwellings:", int((~panel["has_dwellings_2018"]).sum()))
    print("Missing fiscal:", int((~panel["has_fiscal"]).sum()))
    print(f"Wrote {OUT} ({len(panel):,} rows)")

    # Proxy vs proper-rate comparison.
    corr = panel[["other_vacancy_rate_2023", "other_per_1000_hh_2023"]].corr(
        method="spearman"
    ).iloc[0, 1]
    panel["rank_proper"] = panel["other_vacancy_rate_2023"].rank(ascending=False)
    panel["rank_proxy"] = panel["other_per_1000_hh_2023"].rank(ascending=False)
    panel["rank_diff"] = panel["rank_proxy"] - panel["rank_proper"]
    print(f"\nSpearman correlation (proxy vs proper other-vacancy rate): {corr:.3f}")
    print("Largest rank changes (proxy minus proper):")
    cols = [
        "prefecture",
        "region_name_2023",
        "other_vacancy_rate_2023",
        "other_per_1000_hh_2023",
        "rank_proper",
        "rank_proxy",
        "rank_diff",
    ]
    print(
        panel.reindex(panel["rank_diff"].abs().sort_values(ascending=False).index)[cols]
        .head(10)
        .to_string(index=False)
    )

    print("\nTop 10 by proper dilapidated other-vacancy rate:")
    cols = [
        "prefecture",
        "region_name_2023",
        "dilapidated_other_rate_2023",
        "other_vacancy_rate_2023",
        "pop_change_rate_5y",
        "fiscal_strength_index",
    ]
    print(
        panel.sort_values("dilapidated_other_rate_2023", ascending=False)[cols]
        .head(10)
        .to_string(index=False)
    )

    print("\nLargest 2018→2023 increase in dilapidated other-vacancy rate:")
    cols = [
        "prefecture",
        "region_name_2023",
        "dilapidated_other_rate_2018",
        "dilapidated_other_rate_2023",
        "dilapidated_other_rate_change_2018_2023",
    ]
    print(
        panel.sort_values("dilapidated_other_rate_change_2018_2023", ascending=False)[cols]
        .head(10)
        .to_string(index=False)
    )

    print("\nLargest 2018→2023 decrease in dilapidated other-vacancy rate:")
    print(
        panel.sort_values("dilapidated_other_rate_change_2018_2023")[cols]
        .head(10)
        .to_string(index=False)
    )


if __name__ == "__main__":
    main()
