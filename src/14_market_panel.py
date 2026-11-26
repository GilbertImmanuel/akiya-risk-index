"""Build the municipal market panel from XIT001 and KSJ L01/L02.

The 2018 L01 and L02 shapefiles use different field positions from 2023, so the
field maps below are explicit. Do not replace them with positional assumptions.

Run:
    uv run python src/14_market_panel.py --scope pilot
    uv run python src/14_market_panel.py --scope full
"""

from __future__ import annotations

import argparse
import importlib
import json
import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
import pyogrio

sys.path.insert(0, str(Path(__file__).resolve().parent))
config = importlib.import_module("00_config")

PILOT_PREFECTURES = ["13", "20", "39"]
ALL_PREFECTURES = [f"{code:02d}" for code in range(1, 48)]
YEARS = [2018, 2023]

PANEL = config.DATA_PROCESSED / "vacancy_panel_2018_2023.csv"
PILOT = config.DATA_PROCESSED / "pilot_panel_v2.csv"
CENSUS = config.DATA_INTERIM / "census_2025.csv"
WARD_MAP = config.DATA_INTERIM / "ward_to_city_2023.csv"

L01_FIELDS = {
    2018: {
        "code": "L01_021",
        "use": "L01_025",
        "price": "L01_006",
        "site1": "L01_001",
        "site2": "L01_002",
    },
    2023: {
        "code": "L01_022",
        "use": "L01_027",
        "price": "L01_006",
        "site1": "L01_001",
        "site2": "L01_002",
    },
}
L02_FIELDS = {
    2018: {
        "code": "L02_021",
        "use": "L02_025",
        "price": "L02_006",
        "site1": "L02_001",
        "site2": "L02_002",
    },
    2023: {
        "code": "L02_020",
        "use": "L02_025",
        "price": "L02_006",
        "site1": "L02_001",
        "site2": "L02_002",
    },
}


def to_number(series: pd.Series) -> pd.Series:
    text = series.astype(str).str.replace(",", "", regex=False).str.strip()
    text = text.replace({"": None, "nan": None, "None": None, "-": None})
    return pd.to_numeric(text, errors="coerce")


def classify_asset_type(types: pd.Series) -> pd.Series:
    text = types.fillna("").astype(str).str.strip()
    result = pd.Series("other", index=types.index, dtype="object")
    result[text.str.contains("土地と建物", na=False)] = "house"
    result[text.str.contains("マンション", na=False)] = "condo"
    result[(result == "other") & text.str.contains("宅地", na=False)] = "land"
    return result


def site_key(code: pd.Series, site1: pd.Series, site2: pd.Series) -> pd.Series:
    return (
        code.astype(str).str.strip().str.zfill(5)
        + ":"
        + site1.astype(str).str.strip().str.zfill(3)
        + ":"
        + site2.astype(str).str.strip().str.zfill(3)
    )


def field_map(dataset: str, year: int) -> dict[str, str]:
    if dataset == "L01":
        return L01_FIELDS[year]
    if dataset == "L02":
        return L02_FIELDS[year]
    raise ValueError(f"Unknown dataset {dataset!r}")


def load_ward_map() -> dict[str, str]:
    mapping = pd.read_csv(WARD_MAP, dtype=str, encoding="utf-8-sig")
    return dict(zip(mapping["ward_code"], mapping["city_code"], strict=True))


def ksj_shapefile(dataset: str, year: int) -> Path:
    zip_path = config.DATA_RAW / f"ksj_{dataset}_{year}.zip"
    if not zip_path.exists():
        raise FileNotFoundError(f"Missing {zip_path}; run src/08_download_ksj.py {dataset}_{year}")

    out_dir = config.DATA_INTERIM / "ksj" / f"{dataset.lower()}_{year}"
    shps = list(out_dir.rglob("*.shp")) if out_dir.exists() else []
    if not shps:
        out_dir.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(zip_path) as archive:
            archive.extractall(out_dir)
        shps = list(out_dir.rglob("*.shp"))

    if len(shps) != 1:
        raise ValueError(f"Expected one shapefile in {zip_path}, found {len(shps)}")
    return shps[0]


def load_ksj(
    dataset: str, year: int, ward_map: dict[str, str], panel_codes: set[str]
) -> pd.DataFrame:
    fields = field_map(dataset, year)
    shp = ksj_shapefile(dataset, year)
    columns = [fields["site1"], fields["site2"], fields["code"], fields["use"], fields["price"]]
    df = pyogrio.read_dataframe(shp, encoding="cp932", columns=columns, read_geometry=False)
    df = df.rename(columns={original: canonical for canonical, original in fields.items()})
    df["site1"] = df["site1"].astype(str).str.strip().str.zfill(3)
    df["site2"] = df["site2"].astype(str).str.strip().str.zfill(3)
    df["code"] = df["code"].astype(str).str.strip().str.zfill(5)
    df["price"] = to_number(df["price"])
    df["use"] = df["use"].fillna("").astype(str).str.strip()
    if dataset == "L02":
        df["usecode"] = df["site1"]
    df["region_code"] = df["code"].map(ward_map).fillna(df["code"])
    df = df[df["region_code"].isin(panel_codes)].copy()

    if dataset == "L01":
        residential = df["use"].eq("住宅")
        mixed = int(df["use"].str.startswith("住宅").sum() - residential.sum())
    else:
        residential = df["usecode"].eq("000")
        mixed = 0

    valid = residential & (df["price"] > 0)
    dropped_price = int((residential & ~(df["price"] > 0)).sum())
    df = df[valid].copy()
    df["site_key"] = site_key(df["code"], df["site1"], df["site2"])
    if df["site_key"].duplicated().any():
        duplicates = int(df["site_key"].duplicated().sum())
        raise ValueError(f"{dataset} {year}: {duplicates} duplicate site keys")

    print(
        f"  {dataset} {year}: {len(df):,} residential points in panel units "
        f"({df['region_code'].nunique():,} units); mixed-use L01 points {mixed:,}; "
        f"dropped non-positive price {dropped_price:,}"
    )
    return df


def aggregate_land_prices(
    dataset: str, ward_map: dict[str, str], panel_codes: set[str]
) -> pd.DataFrame:
    frames = {}
    for year in YEARS:
        print(f"{dataset} {year}:")
        frames[year] = load_ksj(dataset, year, ward_map, panel_codes)

    levels = []
    for year, df in frames.items():
        agg = (
            df.groupby("region_code")
            .agg(points=("price", "size"), median=("price", "median"))
            .reset_index()
        )
        agg["year"] = year
        levels.append(agg)
    levels = pd.concat(levels, ignore_index=True)

    left = frames[2018][["site_key", "price", "region_code"]].rename(
        columns={"price": "price_2018", "region_code": "region_2018"}
    )
    right = frames[2023][["site_key", "price", "region_code"]].rename(
        columns={"price": "price_2023", "region_code": "region_2023"}
    )
    if left["site_key"].duplicated().any() or right["site_key"].duplicated().any():
        raise ValueError(f"{dataset}: duplicate site keys in a single year")
    matched = left.merge(right, on="site_key", how="inner")
    moved = int((matched["region_2018"] != matched["region_2023"]).sum())
    matched["change"] = (matched["price_2023"] / matched["price_2018"] - 1) * 100
    matched_agg = (
        matched.groupby("region_2023")
        .agg(matched_sites=("change", "size"), matched_change=("change", "median"))
        .reset_index()
        .rename(columns={"region_2023": "region_code"})
    )
    matched_agg["year"] = 2023

    out = levels.merge(matched_agg, on=["region_code", "year"], how="left")
    mask_2023 = out["year"] == 2023
    out.loc[mask_2023, "matched_sites"] = out.loc[mask_2023, "matched_sites"].fillna(0).astype(int)
    out = out.rename(
        columns={
            "points": f"{dataset.lower()}_price_points",
            "median": f"{dataset.lower()}_price_median_yen_m2",
            "matched_sites": f"{dataset.lower()}_matched_sites",
            "matched_change": f"{dataset.lower()}_matched_change_5y_pct",
        }
    )
    print(f"{dataset} matched sites: {len(matched):,}; units with changed boundary: {moved:,}")
    return out


def load_transactions(
    year: int, prefectures: list[str], ward_map: dict[str, str], panel_codes: set[str]
) -> pd.DataFrame:
    frames = []
    for prefecture in prefectures:
        path = config.DATA_RAW / f"reinfolib_XIT001_{prefecture}_{year}.json"
        if not path.exists():
            raise FileNotFoundError(f"Missing {path}; run src/13_market_pull.py first")
        payload = json.loads(path.read_text(encoding="utf-8"))
        if payload.get("status") != "OK":
            raise ValueError(f"XIT001 status {payload.get('status')!r} in {path.name}")
        records = payload.get("data", [])
        if not records:
            raise ValueError(f"XIT001 returned no records in {path.name}")
        frames.append(pd.DataFrame(records))

    df = pd.concat(frames, ignore_index=True)
    required = [
        "Type",
        "Region",
        "Use",
        "MunicipalityCode",
        "TradePrice",
        "Area",
        "UnitPrice",
        "PriceCategory",
        "Period",
    ]
    missing = [column for column in required if column not in df.columns]
    if missing:
        raise ValueError(f"XIT001 missing columns: {missing}")

    categories = df["PriceCategory"].fillna("").astype(str).str.strip()
    if not categories.eq("不動産取引価格情報").all():
        raise ValueError(
            f"Unexpected XIT001 price categories: {categories.value_counts().to_dict()}"
        )
    period_years = df["Period"].fillna("").astype(str).str.extract(r"(\d{4})")[0]
    wrong_year = int(period_years.ne(str(year)).sum())
    if wrong_year:
        print(f"  warning: {wrong_year:,} records do not report {year} in Period")

    df["year"] = year
    df["code"] = df["MunicipalityCode"].astype(str).str.strip().str.zfill(5)
    df["region_code"] = df["code"].map(ward_map).fillna(df["code"])
    df["asset_type"] = classify_asset_type(df["Type"])
    region = df["Region"].fillna("").astype(str).str.strip()
    use = df["Use"].fillna("").astype(str).str.strip()

    land = df["asset_type"].eq("land") & region.eq("住宅地")
    house = df["asset_type"].eq("house") & region.eq("住宅地") & use.str.contains("住宅", na=False)
    condo = df["asset_type"].eq("condo") & use.str.contains("住宅", na=False)
    residential = land | house | condo

    price = to_number(df["TradePrice"])
    area = to_number(df["Area"]).where(lambda values: values > 0)
    unit = to_number(df["UnitPrice"])
    df["price_value"] = np.nan
    df.loc[land, "price_value"] = unit.where(unit > 0, price / area)
    df.loc[house, "price_value"] = price
    df.loc[condo, "price_value"] = price / area

    print(f"  {year}: {len(df):,} records; types {df['asset_type'].value_counts().to_dict()}")
    print(
        f"  residential land={int(land.sum()):,}, "
        f"house={int(house.sum()):,}, condo={int(condo.sum()):,}"
    )

    df = df[residential].copy()
    before = len(df)
    df = df[df["price_value"].notna() & (df["price_value"] > 0)]
    df = df[df["region_code"].isin(panel_codes)]
    print(f"  usable: {len(df):,} of {before:,}; units {df['region_code'].nunique():,}")
    return df[["region_code", "year", "asset_type", "price_value"]]


def aggregate_transactions(df: pd.DataFrame) -> pd.DataFrame:
    count = df.pivot_table(
        index=["region_code", "year"], columns="asset_type", values="price_value", aggfunc="size"
    ).reindex(columns=["land", "house", "condo"], fill_value=0)
    median = df.pivot_table(
        index=["region_code", "year"], columns="asset_type", values="price_value", aggfunc="median"
    ).reindex(columns=["land", "house", "condo"])
    out = count.add_prefix("transaction_count_").join(median.add_prefix("transaction_median_"))
    out["transaction_count"] = out.filter(like="transaction_count_").sum(axis=1)
    out = out.rename(
        columns={
            "transaction_median_land": "transaction_land_median_unit_price_yen_m2",
            "transaction_median_house": "transaction_house_median_price_yen",
            "transaction_median_condo": "transaction_condo_median_unit_price_yen_m2",
        }
    )
    return out.reset_index()


def prefecture_map() -> dict[str, str]:
    census = pd.read_csv(CENSUS, dtype={"area_code": str})
    prefectures = census.loc[census["level"] == "prefecture", ["area_code", "area_name"]]
    return dict(
        zip(prefectures["area_code"].str[:2], prefectures["area_name"], strict=True)
    )


def coverage_summary(wide: pd.DataFrame, base: pd.DataFrame, label: str) -> None:
    strict = (
        wide["l01_price_points_2018"].ge(5)
        & wide["l01_price_points_2023"].ge(5)
        & wide["l01_matched_sites_2023"].ge(3)
        & wide["transaction_count_2023"].ge(10)
    )
    any_market = (
        wide["l01_price_points_2023"].gt(0)
        | wide["l02_price_points_2023"].gt(0)
        | wide["transaction_count_2023"].gt(0)
    )
    wide = wide.assign(strict=strict, any_market=any_market)
    print(
        f"\n{label}: strict coverage {strict.mean():.1%}; "
        f"any market data {any_market.mean():.1%}"
    )

    info = base[["region_code", "level"]].copy()
    info["prefecture_code"] = info["region_code"].str[:2]
    info["prefecture"] = info["prefecture_code"].map(prefecture_map())
    summary = info.merge(
        wide[["region_code", "strict", "any_market"]], on="region_code", how="left"
    )
    summary["strict"] = summary["strict"].fillna(False)
    summary["any_market"] = summary["any_market"].fillna(False)

    by_prefecture = summary.groupby("prefecture").agg(
        units=("region_code", "size"),
        strict=("strict", "sum"),
        any_market=("any_market", "sum"),
    )
    by_prefecture["strict_share"] = by_prefecture["strict"] / by_prefecture["units"]
    by_prefecture["any_market_share"] = by_prefecture["any_market"] / by_prefecture["units"]
    print("\nBy prefecture:")
    print(
        by_prefecture.sort_values("strict_share", ascending=False).to_string(
            float_format="{:.3f}".format
        )
    )

    by_level = summary.groupby("level").agg(
        units=("region_code", "size"),
        strict=("strict", "sum"),
        any_market=("any_market", "sum"),
    )
    by_level["strict_share"] = by_level["strict"] / by_level["units"]
    by_level["any_market_share"] = by_level["any_market"] / by_level["units"]
    print("\nBy level:")
    print(by_level.to_string(float_format="{:.3f}".format))


def build_panel(scope: str) -> None:
    panel = pd.read_csv(PANEL, dtype={"region_code": str})
    pilot = pd.read_csv(PILOT, dtype={"region_code": str})
    universe = pilot["region_code"].tolist() if scope == "pilot" else panel["region_code"].tolist()
    panel_codes = set(universe)
    prefectures = PILOT_PREFECTURES if scope == "pilot" else ALL_PREFECTURES
    ward_map = load_ward_map()

    transaction_frames = []
    for year in YEARS:
        print(f"XIT001 {year}:")
        transaction_frames.append(load_transactions(year, prefectures, ward_map, panel_codes))
    transactions = aggregate_transactions(pd.concat(transaction_frames, ignore_index=True))

    l01 = aggregate_land_prices("L01", ward_map, panel_codes)
    l02 = aggregate_land_prices("L02", ward_map, panel_codes)

    grid = pd.MultiIndex.from_product(
        [universe, YEARS], names=["region_code", "year"]
    ).to_frame(index=False)
    out = (
        grid.merge(transactions, on=["region_code", "year"], how="left")
        .merge(l01, on=["region_code", "year"], how="left")
        .merge(l02, on=["region_code", "year"], how="left")
    )

    dwellings = panel[["region_code", "total_dwellings_2018", "total_dwellings_2023"]].melt(
        id_vars="region_code", var_name="year_label", value_name="total_dwellings"
    )
    dwellings["year"] = dwellings["year_label"].str.extract(r"(\d{4})").astype(int)
    out = out.merge(dwellings.drop(columns="year_label"), on=["region_code", "year"], how="left")

    type_count_cols = [
        "transaction_count_land",
        "transaction_count_house",
        "transaction_count_condo",
    ]
    out[type_count_cols] = out[type_count_cols].fillna(0).astype(int)
    out["transaction_count"] = out[type_count_cols].sum(axis=1)
    out["l01_price_points"] = out["l01_price_points"].fillna(0).astype(int)
    out["l02_price_points"] = out["l02_price_points"].fillna(0).astype(int)
    mask_2023 = out["year"] == 2023
    out.loc[mask_2023, "l01_matched_sites"] = out.loc[mask_2023, "l01_matched_sites"].fillna(0)
    out.loc[mask_2023, "l02_matched_sites"] = out.loc[mask_2023, "l02_matched_sites"].fillna(0)
    out["l01_matched_sites"] = out["l01_matched_sites"].astype("Int64")
    out["l02_matched_sites"] = out["l02_matched_sites"].astype("Int64")
    out["transaction_liquidity_per_1000_dwellings"] = (
        out["transaction_count"] / out["total_dwellings"].where(out["total_dwellings"] > 0) * 1000
    )
    out = out.drop(columns="total_dwellings")

    out["land_price_thin"] = out["l01_price_points"] < 5
    out["transaction_thin"] = out["transaction_count"] < 10
    out["market_thin"] = out["land_price_thin"] | out["transaction_thin"]
    out["has_market_data"] = (
        out["l01_price_points"].gt(0)
        | out["l02_price_points"].gt(0)
        | out["transaction_count"].gt(0)
    )
    out = out.sort_values(["region_code", "year"]).reset_index(drop=True)

    if out[["region_code", "year"]].duplicated().any():
        raise ValueError("Duplicate region_code and year in market panel")
    if len(out) != len(universe) * len(YEARS):
        raise ValueError(f"Expected {len(universe) * len(YEARS)} rows, found {len(out)}")
    if not (out["transaction_count"] == out[type_count_cols].sum(axis=1)).all():
        raise ValueError("transaction_count does not equal the asset-type counts")
    if not (out["market_thin"] == (out["land_price_thin"] | out["transaction_thin"])).all():
        raise ValueError("market_thin is inconsistent")
    for column in ["l01_price_median_yen_m2", "l02_price_median_yen_m2"]:
        points = out[column.replace("_median_yen_m2", "_points")]
        if not out.loc[points > 0, column].gt(0).all():
            raise ValueError(f"{column} is missing where points exist")

    market_path = config.DATA_PROCESSED / (
        "market_panel_pilot.csv" if scope == "pilot" else "market_panel.csv"
    )
    out.to_csv(market_path, index=False, encoding="utf-8")
    print(f"\nWrote {market_path} ({len(out):,} rows)")

    wide = out.pivot(index="region_code", columns="year")
    wide.columns = [f"{column}_{year}" for column, year in wide.columns]
    wide = wide.reset_index()

    if scope == "pilot":
        pilot_out = pilot.merge(wide, on="region_code", how="left")
        if len(pilot_out) != len(pilot) or pilot_out["region_code"].duplicated().any():
            raise ValueError("Pilot v3 row count or key check failed")
        pilot_path = config.DATA_PROCESSED / "pilot_panel_v3.csv"
        pilot_out.to_csv(pilot_path, index=False, encoding="utf-8")
        print(f"Wrote {pilot_path} ({len(pilot_out):,} rows)")
        coverage_summary(wide, pilot, "Pilot")
    else:
        full_out = panel.merge(wide, on="region_code", how="left")
        if len(full_out) != len(panel) or full_out["region_code"].duplicated().any():
            raise ValueError("Full panel row count or key check failed")
        full_path = config.DATA_PROCESSED / "panel_with_market.csv"
        full_out.to_csv(full_path, index=False, encoding="utf-8")
        print(f"Wrote {full_path} ({len(full_out):,} rows)")
        coverage_summary(wide, panel, "Full panel")

    print(f"Scope: {scope}; market rows: {len(out):,}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scope", choices=["pilot", "full"], default="pilot")
    args = parser.parse_args()
    build_panel(args.scope)


if __name__ == "__main__":
    main()
