import importlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
bank = importlib.import_module("15_akiya_bank")


def test_parse_era_month() -> None:
    assert bank.parse_era_month("H30.3") == "2018-03"
    assert bank.parse_era_month("H31.1") == "2019-01"
    assert bank.parse_era_month("R1.5") == "2019-05"
    assert bank.parse_era_month("R8.10") == "2026-10"


def test_numbers_from_text() -> None:
    assert bank.numbers_from_text("3,458 4,563 487 1,155") == [3458, 4563, 487, 1155]


def test_constants() -> None:
    assert len(bank.MONTH_LABELS) == 53
    assert len(bank.PREFECTURES) == 47


def test_parse_trend_pairs_values() -> None:
    listings = " ".join(f"{3001 + i:,}" for i in range(53))
    participants = " ".join(str(400 + i) for i in range(53))
    frame = bank.parse_trend(listings + " " + participants)
    assert len(frame) == 53
    assert frame["listing_count"].iloc[0] == 3001
    assert frame["participating_municipalities"].iloc[-1] == 452
    assert frame["month"].iloc[0] == "2018-03"
    assert frame["month"].iloc[-1] == "2026-10"


def test_parse_prefecture_values() -> None:
    rates = " ".join(f"{50 + i / 10:.1f}%" for i in range(47))
    axis = " ".join(f"{i * 10}.0%" for i in range(11))
    frame, average = bank.parse_prefecture(rates + " " + axis + " 全国平均65.5％")
    assert len(frame) == 47
    assert average == 65.5


def test_parse_overview() -> None:
    text = "○1,155自治体の参加 （現在、750自治体が掲載中） 約29,000件の物件が成約済"
    assert bank.parse_overview(text) == (1155, 750, 29000)
