"""Build the 2018–2023 municipal-code crosswalk.

The 2018 and 2023 vacancy tables use standard municipal codes. Between the two
waves, the merger history shows no municipal mergers affecting the table; the
coverage change is threshold-driven:

- 29 codes appear only in 2018 (likely below the 15,000 reporting threshold in 2023);
- 2 codes appear only in 2023 (likely crossed the threshold);
- 1 code has a name change (28221 篠山市 -> 丹波篠山市);
- the balanced 2018–2023 panel is 1,057 units.

Run:
    uv run python src/03_crosswalk.py
"""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
config = importlib.import_module("00_config")

KEYS = ["region_code"]
NAME_COLS = ["region_code", "region_name", "level"]


def load_vacancy(path: Path, year: int) -> pd.DataFrame:
    df = pd.read_csv(path, dtype={"region_code": str})
    df = df.loc[df["analysis_unit"]].copy()
    df = df[NAME_COLS].rename(
        columns={
            "region_name": f"region_name_{year}",
            "level": f"level_{year}",
        }
    )
    return df


def check_mergers(path: Path) -> None:
    """Fail if the merger history shows a 2018–2023 municipal merger."""
    if not path.exists():
        print("Merger file not found; skipping merger check.")
        return
    df = pd.read_csv(path, encoding="utf-8-sig")
    df["date"] = pd.to_datetime(df["廃置分合等施行年月日"], errors="coerce")
    recent = df[(df["date"] >= "2018-01-01") & (df["date"] <= "2023-12-31")]
    merger_terms = ("編入", "合併", "新設合併")
    mergers = recent[recent["改正事由"].str.contains("|".join(merger_terms), na=False)]
    if not mergers.empty:
        raise ValueError("Unexpected 2018–2023 merger in the table:\n" + mergers.to_string())
    print(f"Merger check: {len(recent)} status changes, no municipal mergers.")


def build_crosswalk(a: pd.DataFrame, b: pd.DataFrame) -> pd.DataFrame:
    out = a.merge(b, on="region_code", how="outer", suffixes=("_2018", "_2023"))

    status = []
    note = []
    for _, row in out.iterrows():
        name_18 = row.get("region_name_2018")
        name_23 = row.get("region_name_2023")
        if pd.notna(name_18) and pd.notna(name_23):
            if name_18 == name_23:
                status.append("matched")
                note.append("")
            else:
                status.append("name_changed")
                note.append("Same code; name changed.")
        elif pd.notna(name_18):
            status.append("only_2018")
            note.append("In 2018 coverage; absent from 2023 coverage (likely below 15,000 threshold).")
        else:
            status.append("only_2023")
            note.append("In 2023 coverage; absent from 2018 coverage (likely crossed 15,000 threshold).")

    out["status"] = status
    out["note"] = note
    out["balanced_panel"] = out["status"].isin(["matched", "name_changed"])
    out = out.sort_values("region_code").reset_index(drop=True)

    # Keep a stable, readable column order.
    out = out[
        [
            "region_code",
            "region_name_2018",
            "region_name_2023",
            "level_2018",
            "level_2023",
            "status",
            "balanced_panel",
            "note",
        ]
    ]
    return out


def main() -> None:
    a = load_vacancy(config.VACANCY_2018_CSV, 2018)
    b = load_vacancy(config.VACANCY_2023_CSV, 2023)
    check_mergers(config.MERGERS_CSV)
    out = build_crosswalk(a, b)

    counts = out["status"].value_counts().to_dict()
    balanced = int(out["balanced_panel"].sum())
    print("Crosswalk status:", counts)
    print(f"Balanced 2018–2023 panel: {balanced} units")
    if balanced != 1057:
        raise ValueError(f"Expected 1,057 balanced units, found {balanced}")

    out.to_csv(config.CROSSWALK_2018_2023, index=False, encoding="utf-8")
    print(f"Wrote {config.CROSSWALK_2018_2023} ({len(out):,} rows)")


if __name__ == "__main__":
    main()
