import importlib
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
market = importlib.import_module("14_market_panel")


def test_classify_asset_type() -> None:
    types = pd.Series(["宅地(土地)", "宅地(土地と建物)", "中古マンション等", "林地", "農地"])
    expected = ["land", "house", "condo", "other", "other"]
    assert market.classify_asset_type(types).tolist() == expected


def test_site_key_zero_pads() -> None:
    key = market.site_key(pd.Series(["1101"]), pd.Series(["1"]), pd.Series(["2"]))
    assert key.iloc[0] == "01101:001:002"


def test_field_maps() -> None:
    assert market.field_map("L01", 2018)["code"] == "L01_021"
    assert market.field_map("L01", 2023)["code"] == "L01_022"
    assert market.field_map("L02", 2018)["code"] == "L02_021"
    assert market.field_map("L02", 2023)["code"] == "L02_020"


def test_to_number_handles_commas_and_blanks() -> None:
    values = market.to_number(pd.Series(["1,200", "", "3.5"]))
    assert values.iloc[0] == 1200
    assert pd.isna(values.iloc[1])
    assert values.iloc[2] == 3.5
