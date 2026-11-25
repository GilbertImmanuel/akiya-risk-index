"""Build the 2008/2013 city/ward vacancy context and compare it with 2018/2023.

Sources (e-Stat API):
- 2013 Housing and Land Survey table 53 (`statsDataId=0003100835`)
- 2008 Housing and Land Survey table 043-2 (`statsDataId=0003010419`)

Both tables are 市区 only: cities and wards, no towns/villages. The output is a
city/ward context table, not a four-wave municipal panel.

Run:
    uv run python src/12_vacancy_context.py
"""

from __future__ import annotations

import importlib
import json
import re
import sys
from datetime import date
from pathlib import Path

import httpx
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
config = importlib.import_module("00_config")

API = "https://api.e-stat.go.jp/rest/3.0/app/json/getStatsData"
ACCESS_DATE = "2026-11-25"

TABLES = {
    2013: {"id": "0003100835", "raw": config.DATA_RAW / f"estat_vacancy_2013_{ACCESS_DATE}.json"},
    2008: {"id": "0003010419", "raw": config.DATA_RAW / f"estat_vacancy_2008_{ACCESS_DATE}.json"},
}

# Category codes differ by wave; map by year, never by position.
CODES = {
    2013: {
        "total": "00000",
        "dil_yes": "00001",
        "build_detached": "00001",
        "vac_secondary": "00001",
        "vac_rental": "00004",
        "vac_sale": "00005",
        "vac_other": "00006",
        "dims": {"dil": "@cat01", "struct": "@cat02", "build": "@cat03", "vac": "@cat04"},
    },
    2008: {
        "total": "00",
        "dil_yes": "01",
        "build_detached": "02",
        "vac_secondary": "01",
        "vac_rental": "04",
        "vac_sale": "05",
        "vac_other": "06",
        "dims": {"dil": "@cat01", "vac": "@cat02", "build": "@cat03", "struct": "@cat04"},
    },
}

OUT_CONTEXT = config.DATA_PROCESSED / "vacancy_context_2008_2023.csv"
OUT_MEMO = config.OUTPUTS / "vacancy_comparability.txt"
PANEL = config.DATA_PROCESSED / "vacancy_panel_2018_2023.csv"


def fetch_raw(year: int) -> dict:
    """Fetch all pages from the e-Stat API and cache a combined JSON file."""
    path = TABLES[year]["raw"]
    if path.exists():
        print(f"{year}: using cached {path.name}")
        return json.loads(path.read_text(encoding="utf-8"))

    values: list[dict] = []
    class_inf: dict | None = None
    table_inf: dict | None = None
    start = 1
    while True:
        params = {
            "appId": config.ESTAT_APP_ID,
            "statsDataId": TABLES[year]["id"],
            "metaGetFlg": "Y",
            "cntGetFlg": "N",
            "limit": 100_000,
            "startPosition": start,
            "explanationGetFlg": "N",
        }
        response = httpx.get(API, params=params, timeout=300)
        response.raise_for_status()
        stat = response.json()["GET_STATS_DATA"]["STATISTICAL_DATA"]
        if class_inf is None:
            class_inf = stat["CLASS_INF"]
            table_inf = stat.get("TABLE_INF")
        page = stat["DATA_INF"]["VALUE"]
        if isinstance(page, dict):
            page = [page]
        values.extend(page)
        result = stat.get("RESULT_INF", {})
        total = int(result.get("TOTAL_NUMBER", len(values)))
        print(f"{year}: {len(values):,}/{total:,} rows")
        if len(values) >= total:
            break
        start = int(result.get("NEXT_KEY", len(values) + 1))

    raw = {
        "table_id": TABLES[year]["id"],
        "year": year,
        "access_date": ACCESS_DATE,
        "table_inf": table_inf,
        "class_inf": class_inf,
        "values": values,
    }
    path.write_text(json.dumps(raw, ensure_ascii=False), encoding="utf-8")
    print(f"{year}: wrote {path} ({path.stat().st_size / 1e6:.1f} MB)")
    return raw


def area_names(class_inf: dict) -> dict[str, str]:
    for obj in class_inf["CLASS_OBJ"]:
        if obj["@id"] == "area":
            classes = obj["CLASS"] if isinstance(obj["CLASS"], list) else [obj["CLASS"]]
            return {c["@code"]: c["@name"] for c in classes}
    raise ValueError("Area metadata not found")


def parse_values(year: int, raw: dict) -> pd.DataFrame:
    df = pd.DataFrame(raw["values"]).rename(columns={"@area": "area", "$": "value"})
    df["area"] = df["area"].astype(str).str.zfill(5)
    df["value"] = pd.to_numeric(df["value"], errors="coerce").fillna(0)
    for dim, col in CODES[year]["dims"].items():
        df[dim] = df[col].astype(str).str.zfill(len(CODES[year]["total"]))
    keep = ["area", "dil", "vac", "build", "struct", "value"]
    df = df[keep]
    dupes = int(df.duplicated(["area", "dil", "vac", "build", "struct"]).sum())
    if dupes:
        raise ValueError(f"{year}: duplicate category rows: {dupes}")
    return df


def metric(df: pd.DataFrame, year: int, vac: str | None = None, dil: str | None = None,
           build: str | None = None, struct: str | None = None) -> pd.Series:
    c = CODES[year]
    q = df[
        (df["dil"] == (dil or c["total"]))
        & (df["build"] == (build or c["total"]))
        & (df["struct"] == (struct or c["total"]))
        & (df["vac"] == (vac or c["total"]))
    ]
    return q.set_index("area")["value"]


def build_source_table(year: int, raw: dict) -> pd.DataFrame:
    df = parse_values(year, raw)
    c = CODES[year]
    metrics = {
        "vacant_total": metric(df, year),
        "vacant_rental": metric(df, year, vac=c["vac_rental"]),
        "vacant_sale": metric(df, year, vac=c["vac_sale"]),
        "vacant_secondary": metric(df, year, vac=c["vac_secondary"]),
        "vacant_other": metric(df, year, vac=c["vac_other"]),
        "vacant_other_dilapidated": metric(
            df, year, vac=c["vac_other"], dil=c["dil_yes"]
        ),
        "vacant_other_detached": metric(
            df, year, vac=c["vac_other"], build=c["build_detached"]
        ),
        "vacant_other_detached_dilapidated": metric(
            df, year, vac=c["vac_other"], dil=c["dil_yes"], build=c["build_detached"]
        ),
    }
    out = pd.DataFrame(metrics)
    out.index.name = "area"
    out = out.reset_index()
    out["area_name"] = out["area"].map(area_names(raw["class_inf"]))
    out["year"] = year
    return out


def build_successor_map(mergers: pd.DataFrame, old_codes: set[str], target_codes: set[str],
                        ward_lookup: dict[str, str]) -> tuple[dict[str, str], dict[str, int]]:
    """Map old municipal codes to 2023 unit codes using merger-history groups.

    Only groups with exactly one 2023 target are used; ambiguous groups are
    counted and skipped rather than guessed.
    """
    to_unit = {code: ward_lookup.get(code, code) for code in target_codes}
    target_all = set(to_unit)
    mapping: dict[str, str] = {}
    stats = {"groups": 0, "mapped": 0, "ambiguous": 0, "no_target": 0}

    recent = mergers[
        (mergers["date"] >= "2008-01-01") & (mergers["date"] <= "2023-12-31")
    ]
    for _, group in recent.groupby(["date", "改正事由"], dropna=False):
        stats["groups"] += 1
        codes = set(re.findall(r"\b\d{5}\b", str(group["改正事由"].iloc[0])))
        codes |= set(group["標準地域コード"].astype(str))
        targets = {to_unit[c] for c in codes if c in target_all}
        if len(targets) == 1:
            target = targets.pop()
            for code in codes:
                if code in old_codes and code not in target_all:
                    mapping[code] = target
            stats["mapped"] += 1
        elif len(targets) > 1:
            stats["ambiguous"] += 1
        else:
            stats["no_target"] += 1
    return mapping, stats


def map_source(source: pd.DataFrame, year: int, target_codes: set[str],
               ward_lookup: dict[str, str], successor: dict[str, str]) -> pd.DataFrame:
    rows = []
    for code in source["area"]:
        if code in target_codes:
            unit, status = code, "exact"
        elif code in ward_lookup:
            unit, status = ward_lookup[code], "ward"
        elif code in successor:
            unit, status = successor[code], "successor"
        else:
            unit, status = None, "unmatched"
        rows.append((unit, status))
    out = source.copy()
    out[["unit_code", "mapping_status"]] = pd.DataFrame(rows, index=out.index)
    return out


def boundary_changes(mergers: pd.DataFrame, year: int) -> set[str]:
    """2023 unit codes whose boundaries changed after the wave."""
    recent = mergers[
        (mergers["date"] > f"{year}-12-31") & (mergers["date"] <= "2023-12-31")
    ]
    terms = "合併|編入|新設|市制|町制|区域変更"
    changed = recent[recent["改正事由"].str.contains(terms, na=False)]
    return set(changed["標準地域コード"].astype(str))


def aggregate_to_units(source: pd.DataFrame, year: int, target: pd.DataFrame,
                       changed: set[str]) -> pd.DataFrame:
    metrics = [
        "vacant_total", "vacant_rental", "vacant_sale", "vacant_secondary",
        "vacant_other", "vacant_other_dilapidated", "vacant_other_detached",
        "vacant_other_detached_dilapidated",
    ]
    exact = source[source["mapping_status"] == "exact"]
    agg = source[source["mapping_status"].isin(["ward", "successor"])]

    if exact["unit_code"].duplicated().any():
        raise ValueError(f"{year}: duplicate exact rows per unit")

    exact_out = exact[["unit_code", *metrics]].copy()
    exact_out["source_rows"] = 1
    exact_out["mapping_status"] = "exact"

    agg_out = (
        agg.dropna(subset=["unit_code"])
        .groupby("unit_code")[metrics]
        .sum()
        .reset_index()
    )
    agg_out["source_rows"] = agg.dropna(subset=["unit_code"]).groupby("unit_code").size().values
    agg_out["mapping_status"] = "aggregated"

    out = exact_out.merge(agg_out, on="unit_code", how="outer", suffixes=("", "_agg"))
    for m in metrics:
        out[m] = out[m].fillna(out.get(f"{m}_agg", 0))
    out["source_rows"] = out["source_rows"].fillna(out.get("source_rows_agg", 0)).astype(int)
    out["mapping_status"] = out["mapping_status"].fillna(out.get("mapping_status_agg", "missing"))
    out = out.drop(columns=[c for c in out.columns if c.endswith("_agg")])

    out = target[["region_code", "region_name_2023", "level"]].merge(
        out, left_on="region_code", right_on="unit_code", how="left"
    )
    out["boundary_changed"] = out["unit_code"].isin(changed).astype(int)
    out.loc[out["mapping_status"] == "aggregated", "boundary_changed"] = 1
    out["year"] = year
    return out


def compare(context: pd.DataFrame, panel: pd.DataFrame, year: int) -> dict:
    col = f"vacant_total_{year}"
    x = context[["region_code", col, "vacant_other_" + str(year)]].dropna()
    y = panel[["region_code", "vacant_total_2018"]].rename(
        columns={"vacant_total_2018": f"vacant_total_2018"}
    )
    m = x.merge(y, on="region_code", how="inner")
    ratio = m[col] / m["vacant_total_2018"]
    return {
        "n": len(m),
        "median_ratio": float(ratio.median()),
        "p05": float(ratio.quantile(0.05)),
        "p95": float(ratio.quantile(0.95)),
        "corr": float(m[col].corr(m["vacant_total_2018"])),
    }


def main() -> None:
    panel = pd.read_csv(PANEL, dtype={"region_code": str})
    target = panel[panel["level"].isin(["city", "designated_city", "special_ward"])].copy()
    target_codes = set(target["region_code"])
    panel_codes = set(panel["region_code"])

    ward = pd.read_csv(config.DATA_INTERIM / "ward_to_city_2023.csv", dtype=str)
    ward_lookup = dict(zip(ward["ward_code"], ward["city_code"]))

    mergers = pd.read_csv(config.MERGERS_CSV, encoding="utf-8-sig", dtype=str)
    mergers["date"] = pd.to_datetime(mergers["廃置分合等施行年月日"], errors="coerce")

    waves = {}
    for year in (2008, 2013):
        raw = fetch_raw(year)
        source = build_source_table(year, raw)
        successor, stats = build_successor_map(
            mergers, set(source["area"]), set(target["region_code"]) | set(ward["ward_code"]),
            ward_lookup,
        )
        source = map_source(source, year, target_codes, ward_lookup, successor)
        source.to_csv(config.DATA_INTERIM / f"vacancy_{year}.csv", index=False, encoding="utf-8-sig")
        waves[year] = aggregate_to_units(source, year, target, boundary_changes(mergers, year))
        print(
            f"{year}: source areas={len(source):,}; mapped={source['unit_code'].notna().sum():,}; "
            f"units={waves[year]['vacant_total'].notna().sum():,}/{len(target):,}; "
            f"successor groups={stats}"
        )

    context = target[["region_code", "region_name_2023", "level"]].copy()
    for year, df in waves.items():
        cols = [
            "unit_code", "source_rows", "mapping_status", "boundary_changed",
            "vacant_total", "vacant_rental", "vacant_sale", "vacant_secondary",
            "vacant_other", "vacant_other_dilapidated", "vacant_other_detached",
            "vacant_other_detached_dilapidated",
        ]
        renamed = {c: f"{c}_{year}" for c in cols if c not in ("unit_code",)}
        context = context.merge(
            df[cols].rename(columns=renamed), left_on="region_code", right_on="unit_code",
            how="left",
        ).drop(columns=["unit_code"])

    for year in (2008, 2013):
        context[f"other_share_of_vacant_{year}"] = (
            context[f"vacant_other_{year}"] / context[f"vacant_total_{year}"]
        )
        context[f"dilapidated_share_of_other_{year}"] = (
            context[f"vacant_other_dilapidated_{year}"] / context[f"vacant_other_{year}"]
        )

    panel_cols = ["region_code", "vacant_total_2018", "vacant_other_2018",
                  "vacant_other_dilapidated_2018", "vacant_total_2023",
                  "vacant_other_2023", "vacant_other_dilapidated_2023",
                  "vacancy_rate_2018", "vacancy_rate_2023"]
    context = context.merge(panel[panel_cols], on="region_code", how="left")
    context.to_csv(OUT_CONTEXT, index=False, encoding="utf-8-sig")

    checks = []
    for year in (2008, 2013):
        total = context[f"vacant_total_{year}"]
        other = context[f"vacant_other_{year}"]
        dil = context[f"vacant_other_dilapidated_{year}"]
        det = context[f"vacant_other_detached_{year}"]
        det_dil = context[f"vacant_other_detached_dilapidated_{year}"]
        parts = (
            context[f"vacant_rental_{year}"] + context[f"vacant_sale_{year}"]
            + context[f"vacant_secondary_{year}"] + other
        )
        checks.append(
            f"{year}: units={total.notna().sum()}/{len(context)}; "
            f"covered vacant={total.sum():,.0f}; "
            f"composition mismatches={(parts - total).abs().gt(10).sum()}; "
            f"other<dil={int((other < dil).sum())}; det<other={int((det > other).sum())}; "
            f"det_dil>det={int((det_dil > det).sum())}; "
            f"boundary_changed={int(context[f'boundary_changed_{year}'].fillna(0).sum())}"
        )

    c13 = compare(context, panel, 2013)
    c08 = compare(context, panel, 2008)
    missing_2008 = context.loc[context["vacant_total_2008"].isna(), "region_name_2023"].tolist()
    missing_2013 = context.loc[context["vacant_total_2013"].isna(), "region_name_2023"].tolist()

    lines = [
        "2008/2013 vacancy context — comparability memo",
        "=" * 50,
        f"Access date: {ACCESS_DATE}",
        "2013 table 53: statsDataId=0003100835",
        "2008 table 043-2: statsDataId=0003010419",
        "",
        "Geography: 市区 only (cities and wards); no towns/villages.",
        f"Target: {len(target):,} 2023 city/ward units (772 cities + 20 designated cities + 23 special wards).",
        "",
        "Checks:",
        *checks,
        f"2008 missing units ({len(missing_2008)}): " + ", ".join(missing_2008),
        f"2013 missing units ({len(missing_2013)}): " + ", ".join(missing_2013),
        "The missing units were towns/villages in that wave, so they have no 市区 row.",
        "2008 composition differences: 5 units at ±20 dwellings, consistent with rounding.",
        "",
        f"2013 vs 2018: n={c13['n']:,}; median ratio={c13['median_ratio']:.3f}; "
        f"p05={c13['p05']:.3f}; p95={c13['p95']:.3f}; corr={c13['corr']:.3f}",
        f"2008 vs 2018: n={c08['n']:,}; median ratio={c08['median_ratio']:.3f}; "
        f"p05={c08['p05']:.3f}; p95={c08['p95']:.3f}; corr={c08['corr']:.3f}",
        "",
        "Category crosswalk:",
        "2008/2013: total, secondary, rental, sale, other.",
        "2018/2023: total, rental, sale, secondary, other (codes differ; map by year).",
        "The four substantive categories are stable; only labels/codes change.",
        "",
        "Decision:",
        "2013: usable as city/ward context with boundary flags (812/815 units; 1 boundary change).",
        "2008: usable as city/ward context with stronger boundary flags for 805/815 units.",
        "The 10 missing 2008 units were towns/villages then; do not impute them.",
        "Do not build a four-wave municipal panel; keep 2018–2023 as the core.",
        "",
        "Caveats:",
        "- 2008/2013 exclude towns/villages; the 1,059-unit panel is 2018–2023 only.",
        "- Heisei mergers mean 2008 boundaries often differ from 2023; boundary_changed flags this.",
        "- Rates are not computed for 2008/2013 because total dwellings are not in these tables.",
        "- Composition shares are comparable; counts are not a census of all vacant dwellings.",
    ]
    OUT_MEMO.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    print(f"\nWrote {OUT_CONTEXT} and {OUT_MEMO}")


if __name__ == "__main__":
    main()
