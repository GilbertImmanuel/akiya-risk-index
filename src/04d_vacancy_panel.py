"""Build the core 2018–2023 vacancy panel with proper dwelling denominators.

This is the full 2023 analysis universe (1,059 units), not the pilot. It uses:
- vacancy counts from tables 34-2 (2023) and 35-2 (2018);
- total dwellings from tables 1-2-1 (2023, 2018);
- the 2018–2023 crosswalk.

Rates are per total dwellings. The balanced 2018–2023 panel is 1,057 units;
the 2 units added in 2023 have no 2018 observation.

Run:
    uv run python src/04d_vacancy_panel.py
"""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
config = importlib.import_module("00_config")

OUT = config.DATA_PROCESSED / "vacancy_panel_2018_2023.csv"


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
    panel = vacancy(2023)
    panel = panel.merge(vacancy(2018).drop(columns=["level"]), on="region_code", how="left")
    panel = panel.merge(dwellings(2023), on="region_code", how="left")
    panel = panel.merge(dwellings(2018), on="region_code", how="left")

    panel["has_2018"] = panel["vacant_total_2018"].notna()
    panel["has_dwellings_2023"] = panel["total_dwellings_2023"].notna()
    panel["has_dwellings_2018"] = panel["total_dwellings_2018"].notna()

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

    panel["other_vacancy_rate_change_2018_2023"] = (
        panel["other_vacancy_rate_2023"] - panel["other_vacancy_rate_2018"]
    )
    panel["dilapidated_other_rate_change_2018_2023"] = (
        panel["dilapidated_other_rate_2023"] - panel["dilapidated_other_rate_2018"]
    )

    # QA: 1,059 units; 1,057 balanced; no missing 2023 dwellings/rates.
    if len(panel) != 1059:
        raise ValueError(f"Expected 1,059 rows, found {len(panel)}")
    if int(panel["has_2018"].sum()) != 1057:
        raise ValueError(f"Expected 1,057 balanced units, found {int(panel['has_2018'].sum())}")
    if not panel["has_dwellings_2023"].all():
        raise ValueError("Missing 2023 total dwellings")
    if panel[["vacancy_rate_2023", "other_vacancy_rate_2023", "dilapidated_other_rate_2023"]].isna().any().any():
        raise ValueError("Missing 2023 rates")

    panel = panel.sort_values("dilapidated_other_rate_2023", ascending=False).reset_index(drop=True)
    panel.to_csv(OUT, index=False, encoding="utf-8")

    print(
        "Vacancy panel QA:",
        f"rows={len(panel)}",
        f"balanced={int(panel['has_2018'].sum())}",
        f"missing_2023_dwellings={int((~panel['has_dwellings_2023']).sum())}",
        f"missing_2018_dwellings={int((~panel['has_dwellings_2018']).sum())}",
    )
    national = {
        "total_dwellings": 65_046_700,
        "vacant_total": 9_001_600,
        "vacant_other": 3_856_000,
        "vacant_other_dilapidated": 895_300,
    }
    covered = {
        "total_dwellings": int(panel["total_dwellings_2023"].sum()),
        "vacant_total": int(panel["vacant_total_2023"].sum()),
        "vacant_other": int(panel["vacant_other_2023"].sum()),
        "vacant_other_dilapidated": int(panel["vacant_other_dilapidated_2023"].sum()),
    }
    print("Coverage of national totals:")
    for key, value in national.items():
        print(
            f"  {key}: {covered[key]:,} / {value:,} "
            f"({covered[key] / value:.1%})"
        )
    print(f"Wrote {OUT}")

    cols = [
        "region_code",
        "region_name_2023",
        "level",
        "dilapidated_other_rate_2023",
        "other_vacancy_rate_2023",
        "dilapidated_other_rate_2018",
        "dilapidated_other_rate_change_2018_2023",
    ]
    print("\nTop 10 by 2023 dilapidated other-vacancy rate:")
    print(panel[cols].head(10).to_string(index=False))
    print("\nTop 10 by 2018→2023 increase:")
    print(
        panel.sort_values("dilapidated_other_rate_change_2018_2023", ascending=False)[cols]
        .head(10)
        .to_string(index=False)
    )


if __name__ == "__main__":
    main()
