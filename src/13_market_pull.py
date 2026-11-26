"""Download MLIT XIT001 transaction prices for the market panel.

The API accepts a prefecture code (`area`), so the pilot needs six calls and
the full pull needs 94, not one call per municipality. Raw JSON is cached in
data/raw/ and a committed manifest records the query, access date, and SHA-256.

Run:
    uv run python src/13_market_pull.py --scope pilot
    uv run python src/13_market_pull.py --scope full
"""

from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import sys
import time
from datetime import date
from pathlib import Path

import httpx
from tenacity import retry, retry_if_exception, stop_after_attempt, wait_exponential

sys.path.insert(0, str(Path(__file__).resolve().parent))
config = importlib.import_module("00_config")

API_URL = "https://www.reinfolib.mlit.go.jp/ex-api/external/XIT001"
PILOT_PREFECTURES = ["13", "20", "39"]
ALL_PREFECTURES = [f"{code:02d}" for code in range(1, 48)]
YEARS = [2018, 2023]
MANIFEST = config.DATA_RAW / "reinfolib_manifest.json"


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


def retryable(error: BaseException) -> bool:
    if isinstance(error, httpx.HTTPStatusError):
        return error.response.status_code in {429, 500, 502, 503, 504}
    return isinstance(error, httpx.TransportError)


@retry(
    retry=retry_if_exception(retryable),
    stop=stop_after_attempt(4),
    wait=wait_exponential(multiplier=2, min=2, max=30),
    reraise=True,
)
def fetch(prefecture: str, year: int) -> dict:
    response = httpx.get(
        API_URL,
        params={"year": year, "area": prefecture, "priceClassification": "01"},
        headers={"Ocp-Apim-Subscription-Key": config.REINFOLIB_API_KEY},
        timeout=180.0,
        follow_redirects=True,
    )
    response.raise_for_status()
    payload = response.json()
    if payload.get("status") != "OK":
        raise ValueError(f"XIT001 status {payload.get('status')!r} for {prefecture} {year}")
    if not isinstance(payload.get("data"), list) or not payload["data"]:
        raise ValueError(f"XIT001 returned no records for {prefecture} {year}")
    return payload


def record_count(payload: dict) -> int:
    return len(payload.get("data", []))


def describe(payload: dict) -> str:
    records = payload.get("data", [])
    periods = sorted(
        {
            str(item.get("Period", "")).strip()
            for item in records
            if item.get("Period")
        }
    )
    codes = {str(item.get("MunicipalityCode", "")).strip().zfill(5) for item in records}
    period_text = f"{periods[0]} to {periods[-1]}" if periods else "no period"
    return f"{len(records):,} records, {period_text}, {len(codes):,} municipalities"


def pull_one(prefecture: str, year: int, manifest: dict, force: bool) -> None:
    key = f"XIT001_{prefecture}_{year}"
    target = config.DATA_RAW / f"reinfolib_XIT001_{prefecture}_{year}.json"

    if target.exists() and not force:
        payload = json.loads(target.read_text(encoding="utf-8"))
        print(f"{key}: cached, {describe(payload)}")
    else:
        print(f"{key}: fetching")
        payload = fetch(prefecture, year)
        target.write_text(
            json.dumps(payload, ensure_ascii=False, separators=(",", ":")),
            encoding="utf-8",
        )
        print(f"{key}: saved, {describe(payload)}")
        time.sleep(1.0)

    manifest[key] = {
        "filename": target.name,
        "source": "MLIT Real Estate Information Library XIT001",
        "url": API_URL,
        "query": {"year": year, "area": prefecture, "priceClassification": "01"},
        "access_date": date.today().isoformat(),
        "bytes": target.stat().st_size,
        "sha256": sha256(target),
        "records": record_count(payload),
        "licence": "Free use with attribution; API key required.",
    }
    save_manifest(manifest)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scope", choices=["pilot", "full"], default="pilot")
    parser.add_argument("--force", action="store_true", help="Re-download cached files")
    args = parser.parse_args()

    if not config.REINFOLIB_API_KEY:
        raise SystemExit("REINFOLIB_API_KEY is not set in .env")

    prefectures = PILOT_PREFECTURES if args.scope == "pilot" else ALL_PREFECTURES
    manifest = load_manifest()
    print(f"Scope: {args.scope}; prefectures: {len(prefectures)}; years: {YEARS}")
    for prefecture in prefectures:
        for year in YEARS:
            pull_one(prefecture, year, manifest, args.force)

    print(f"Manifest: {MANIFEST}")
    print(f"Files: {len(manifest)} XIT001 entries")


if __name__ == "__main__":
    main()
