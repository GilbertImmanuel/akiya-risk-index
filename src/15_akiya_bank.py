"""Build the national akiya-bank aggregate tables from the official MLIT PDFs.

The municipal participation lists are not scraped. The two operator pages were
unavailable when this was built (AtHome maintenance, LIFULL CloudFront block),
so this script covers the national trend, the prefecture rates, and the current
summary only.

Run:
    uv run python src/15_akiya_bank.py
"""

from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import re
import sys
from datetime import date
from pathlib import Path

import httpx
import pandas as pd
from pypdf import PdfReader

sys.path.insert(0, str(Path(__file__).resolve().parent))
config = importlib.import_module("00_config")

PDFS = {
    "overview": {
        "filename": "akiya_bank_overview_2026-10.pdf",
        "url": "https://www.mlit.go.jp/totikensangyo/const/content/002045626.pdf",
        "dataset": "Akiya-bank overview",
    },
    "trend": {
        "filename": "akiya_bank_trend_2026-10.pdf",
        "url": "https://www.mlit.go.jp/totikensangyo/const/content/002045627.pdf",
        "dataset": "Akiya-bank participation and listing trend",
    },
    "prefecture": {
        "filename": "akiya_bank_prefecture_2026-10.pdf",
        "url": "https://www.mlit.go.jp/totikensangyo/const/content/002045629.pdf",
        "dataset": "Akiya-bank prefecture participation rates",
    },
}

MANIFEST = config.DATA_RAW / "akiya_bank_manifest.json"
OUT_TREND = config.DATA_PROCESSED / "akiya_bank_trend.csv"
OUT_PREFECTURE = config.DATA_PROCESSED / "akiya_bank_prefecture.csv"
OUT_SUMMARY = config.DATA_PROCESSED / "akiya_bank_summary.csv"

# shortcut: fixed to the October 2026 PDF; update when MLIT advances the vintage.
AS_OF = "2026-10-31"

# The month labels are part of the chart image, not the PDF text layer.
# shortcut: hard-coded to the October 2026 chart; update when the PDF advances.
MONTH_LABELS = [
    "H30.3", "H30.5", "H30.7", "H30.9", "H30.11", "H31.1", "H31.3",
    "R1.5", "R1.7", "R1.9", "R1.11", "R2.1", "R2.3", "R2.5", "R2.7",
    "R2.9", "R2.11", "R3.1", "R3.3", "R3.5", "R3.7", "R3.9", "R3.11",
    "R4.1", "R4.3", "R4.5", "R4.7", "R4.9", "R4.11", "R5.1", "R5.3",
    "R5.5", "R5.7", "R5.9", "R5.11", "R6.1", "R6.3", "R6.5", "R6.7",
    "R6.9", "R6.11", "R7.1", "R7.3", "R7.5", "R7.7", "R7.9", "R7.11",
    "R8.1", "R8.3", "R8.5", "R8.7", "R8.9", "R8.10",
]

PREFECTURES = [
    ("01", "北海道"), ("02", "青森県"), ("03", "岩手県"), ("04", "宮城県"),
    ("05", "秋田県"), ("06", "山形県"), ("07", "福島県"), ("08", "茨城県"),
    ("09", "栃木県"), ("10", "群馬県"), ("11", "埼玉県"), ("12", "千葉県"),
    ("13", "東京都"), ("14", "神奈川県"), ("15", "新潟県"), ("16", "富山県"),
    ("17", "石川県"), ("18", "福井県"), ("19", "山梨県"), ("20", "長野県"),
    ("21", "岐阜県"), ("22", "静岡県"), ("23", "愛知県"), ("24", "三重県"),
    ("25", "滋賀県"), ("26", "京都府"), ("27", "大阪府"), ("28", "兵庫県"),
    ("29", "奈良県"), ("30", "和歌山県"), ("31", "鳥取県"), ("32", "島根県"),
    ("33", "岡山県"), ("34", "広島県"), ("35", "山口県"), ("36", "徳島県"),
    ("37", "香川県"), ("38", "愛媛県"), ("39", "高知県"), ("40", "福岡県"),
    ("41", "佐賀県"), ("42", "長崎県"), ("43", "熊本県"), ("44", "大分県"),
    ("45", "宮崎県"), ("46", "鹿児島県"), ("47", "沖縄県"),
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def load_manifest() -> dict:
    if MANIFEST.exists():
        return json.loads(MANIFEST.read_text(encoding="utf-8"))
    return {}


def save_manifest(manifest: dict) -> None:
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def download(force: bool) -> dict[str, Path]:
    out_dir = config.DATA_RAW / "akiya_bank"
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest = load_manifest()
    paths = {}

    for key, meta in PDFS.items():
        target = out_dir / meta["filename"]
        if not target.exists() or force:
            print(f"{key}: downloading {meta['url']}")
            with httpx.stream("GET", meta["url"], follow_redirects=True, timeout=120.0) as response:
                response.raise_for_status()
                with target.open("wb") as handle:
                    for chunk in response.iter_bytes(chunk_size=1024 * 1024):
                        handle.write(chunk)
        manifest[key] = {
            "filename": target.name,
            "dataset": meta["dataset"],
            "url": meta["url"],
            "access_date": date.today().isoformat(),
            "bytes": target.stat().st_size,
            "sha256": sha256(target),
            "licence": "MLIT public document; attribution required.",
        }
        paths[key] = target
        print(f"{key}: {target.stat().st_size:,} bytes")

    save_manifest(manifest)
    return paths


def pdf_text(path: Path) -> str:
    reader = PdfReader(path)
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def parse_era_month(label: str) -> str:
    era = label[0]
    year_part, month_part = label[1:].split(".")
    if era == "H":
        year = 2018 + int(year_part) - 30
    elif era == "R":
        year = 2018 + int(year_part)
    else:
        raise ValueError(f"Unknown era in {label!r}")
    month = int(month_part)
    if not 1 <= month <= 12:
        raise ValueError(f"Bad month in {label!r}")
    return f"{year:04d}-{month:02d}"


def numbers_from_text(text: str) -> list[int]:
    return [int(value.replace(",", "")) for value in re.findall(r"\d{1,3}(?:,\d{3})*", text)]


def parse_trend(text: str) -> pd.DataFrame:
    values = numbers_from_text(text)
    if len(values) < 106:
        raise ValueError(f"Trend PDF yielded only {len(values)} numbers")
    listings = values[:53]
    participants = values[53:106]

    if len(MONTH_LABELS) != 53:
        raise ValueError("Expected 53 month labels")
    if not all(value > 3000 for value in listings):
        raise ValueError(f"Unexpected listing values: {listings[:3]}")
    if not all(value < 1200 for value in participants):
        raise ValueError(f"Unexpected participant values: {participants[:3]}")
    if not all(a <= b for a, b in zip(participants[:-1], participants[1:], strict=True)):
        raise ValueError("Participating municipality count is not non-decreasing")

    return pd.DataFrame(
        {
            "month": [parse_era_month(label) for label in MONTH_LABELS],
            "participating_municipalities": participants,
            "listing_count": listings,
        }
    )


def parse_prefecture(text: str) -> tuple[pd.DataFrame, float]:
    rates = [float(value) for value in re.findall(r"(\d+(?:\.\d+)?)%", text)]
    if len(rates) < 58:
        raise ValueError(f"Prefecture PDF yielded only {len(rates)} percentages")
    values = rates[:47]
    axis = rates[47:58]
    if len(PREFECTURES) != 47:
        raise ValueError("Expected 47 prefectures")
    if not all(0 <= value <= 100 for value in values):
        raise ValueError("Prefecture rate outside 0-100")
    if axis != [float(value) for value in range(0, 101, 10)]:
        raise ValueError(f"Unexpected chart axis values: {axis}")

    tail = text.partition("全国平均")[2]
    average = re.search(r"(\d+(?:\.\d+)?)", tail)
    if not average:
        raise ValueError("National average not found")

    frame = pd.DataFrame(
        {
            "prefecture_code": [code for code, _ in PREFECTURES],
            "prefecture": [name for _, name in PREFECTURES],
            "participation_rate_pct": values,
        }
    )
    return frame, float(average.group(1))


def parse_overview(text: str) -> tuple[int, int, int]:
    participants = re.search(r"([\d,]+)\s*自治体の参加", text)
    listing = re.search(r"([\d,]+)\s*自治体が掲載中", text)
    transactions = re.search(r"約\s*([\d,]+)\s*件の物件が成約済", text)
    if not participants or not listing or not transactions:
        raise ValueError("Overview counts not found")
    return (
        int(participants.group(1).replace(",", "")),
        int(listing.group(1).replace(",", "")),
        int(transactions.group(1).replace(",", "")),
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--force", action="store_true", help="Re-download the PDFs")
    args = parser.parse_args()

    paths = download(args.force)
    trend = parse_trend(pdf_text(paths["trend"]))
    prefecture, national_average = parse_prefecture(pdf_text(paths["prefecture"]))
    participants, listing_municipalities, transactions = parse_overview(pdf_text(paths["overview"]))

    last_month_participants = int(trend["participating_municipalities"].iloc[-1])
    if participants != last_month_participants:
        print(
            "Warning: overview participants "
            f"{participants:,} != trend last month {last_month_participants:,}"
        )

    summary = pd.DataFrame(
        [
            {
                "as_of": AS_OF,
                "participating_municipalities": participants,
                "listing_municipalities": listing_municipalities,
                "latest_month_listings": int(trend["listing_count"].iloc[-1]),
                "chart_label_listings": int(trend["listing_count"].iloc[-2]),
                "cumulative_transactions": transactions,
                "national_participation_rate_pct": national_average,
                "note": (
                    "The chart labels 20,089 current listings; the October 2026 "
                    "month-end bar is 20,010. Both are retained."
                ),
            }
        ]
    )

    trend.to_csv(OUT_TREND, index=False, encoding="utf-8")
    prefecture.to_csv(OUT_PREFECTURE, index=False, encoding="utf-8")
    summary.to_csv(OUT_SUMMARY, index=False, encoding="utf-8")

    print(
        f"Trend: {len(trend)} rows, {trend['month'].iloc[0]} to {trend['month'].iloc[-1]}; "
        f"participants {trend['participating_municipalities'].iloc[0]:,} to "
        f"{trend['participating_municipalities'].iloc[-1]:,}; "
        f"listings {trend['listing_count'].iloc[0]:,} to {trend['listing_count'].iloc[-1]:,}"
    )
    print(
        f"Prefecture: {len(prefecture)} rows; national average {national_average:.1f}%; "
        f"range {prefecture['participation_rate_pct'].min():.1f} to "
        f"{prefecture['participation_rate_pct'].max():.1f}"
    )
    print(
        f"Summary: {participants:,} participants; {listing_municipalities:,} listing; "
        f"{transactions:,} cumulative transactions"
    )
    print(f"Wrote {OUT_TREND}")
    print(f"Wrote {OUT_PREFECTURE}")
    print(f"Wrote {OUT_SUMMARY}")


if __name__ == "__main__":
    main()
