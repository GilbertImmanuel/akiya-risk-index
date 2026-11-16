"""Parse the 2025 Census municipal population/household tables.

Sources (e-Stat API):
- 2025 Census table 1-2 (`statsDataId=0004050417`): 2020 population,
  2025/2020 households, area, density, sex ratio.
- 2025 Census table 1-1 (`statsDataId=0004050397`): 2025 population.

The five-year change is computed from the 2020 and 2025 population, not taken
from the table's change column (the table's retabulated baseline differs from
the official headline).

Run:
    uv run python src/04_census.py
"""

from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
config = importlib.import_module("00_config")

RAW_TABLE_1_2 = config.DATA_RAW / "estat_census2025_table1-2_2026-11-16.json"
RAW_TABLE_1_1 = config.DATA_RAW / "estat_census2025_table1-1_2026-11-16.json"
OUT = config.DATA_INTERIM / "census_2025.csv"

TAB_MAP = {
    "2025_03": "pop_2020",
    "2025_13": "households_2025",
    "2025_15": "households_2020",
    "2025_36": "household_change_5y",
    "2025_37": "household_change_rate_5y",
    "2025_46": "sex_ratio",
    "2025_47": "area_km2",
    "2025_48": "density",
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


def main() -> None:
    raw_12 = json.loads(RAW_TABLE_1_2.read_text(encoding="utf-8"))
    raw_11 = json.loads(RAW_TABLE_1_1.read_text(encoding="utf-8"))

    stat_12 = raw_12["GET_STATS_DATA"]["STATISTICAL_DATA"]
    stat_11 = raw_11["GET_STATS_DATA"]["STATISTICAL_DATA"]
    names = area_names(stat_12["CLASS_INF"])

    values_12 = stat_12["DATA_INF"]["VALUE"]
    df = pd.DataFrame(values_12).rename(columns={"@area": "area_code", "@tab": "tab"})
    df["value"] = pd.to_numeric(df["$"], errors="coerce")
    wide = df.pivot_table(
        index="area_code", columns="tab", values="value", aggfunc="first"
    ).reset_index()
    wide = wide.rename(columns=TAB_MAP)

    pop_2025 = pd.DataFrame(stat_11["DATA_INF"]["VALUE"]).rename(
        columns={"@area": "area_code", "$": "pop_2025"}
    )
    pop_2025["pop_2025"] = pd.to_numeric(pop_2025["pop_2025"], errors="coerce")
    wide = wide.merge(pop_2025[["area_code", "pop_2025"]], on="area_code", how="left")

    wide["area_name"] = wide["area_code"].map(names)
    wide["level"] = wide["area_code"].map(classify)
    wide["pop_change_5y"] = wide["pop_2025"] - wide["pop_2020"]
    wide["pop_change_rate_5y"] = wide["pop_change_5y"] / wide["pop_2020"] * 100

    # The API table's national 2025 population is 123,049,524, about 77k above
    # the headline 122,972,528 in the summary PDF. The table is internally
    # consistent with its 2020 baseline and five-year change; record the
    # discrepancy rather than forcing the headline.
    expected = {
        "pop_2020": 126_146_099,
        "pop_2025": 123_049_524,
        "households_2025": 57_124_507,
        "pop_change_5y": -3_096_575,
    }
    national = wide.loc[wide["level"] == "national"].iloc[0]
    for key, value in expected.items():
        actual = int(national[key])
        if actual != value:
            raise ValueError(f"National mismatch for {key}: {actual} != {value}")

    if len(wide) != 1961:
        raise ValueError(f"Expected 1,961 areas, found {len(wide)}")

    wide = wide.sort_values("area_code").reset_index(drop=True)
    wide.to_csv(OUT, index=False, encoding="utf-8")
    print(
        "Census QA passed:",
        f"areas={len(wide)}",
        f"pop_2020={int(national['pop_2020']):,}",
        f"pop_2025={int(national['pop_2025']):,}",
        f"households_2025={int(national['households_2025']):,}",
        f"change={int(national['pop_change_5y']):,}",
    )
    print(
        "Note: API 2025 population is 123,049,524; the summary headline is "
        "122,972,528 (difference 76,996). Recorded, not forced."
    )
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
