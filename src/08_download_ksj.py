"""Download KSJ (国土数値情報) data.

Sources:
- N03 行政区域: municipal boundaries, 2023-01-01.
- N02 鉄道: rail lines and stations, FY2023 (data as of 2023-12-31).
- S12 駅別乗降客数: station passengers, FY2023.
- L01 地価公示: official land prices, 2018 and 2023.
- L02 都道府県地価調査: prefectural land prices, 2018 and 2023.

Files are large; this script streams them to data/raw/ and writes a manifest
with URL, size, access date, and SHA-256. Run once per file or all at once:

    uv run python src/08_download_ksj.py N02 S12
    uv run python src/08_download_ksj.py L01_2018 L01_2023 L02_2018 L02_2023

Re-running skips a file whose size matches the expected size.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import date
from pathlib import Path

import httpx

sys.path.insert(0, str(Path(__file__).resolve().parent))
from importlib import import_module

config = import_module("00_config")

FILES = {
    "N03": {
        "filename": "ksj_N03_2023.zip",
        "url": "https://nlftp.mlit.go.jp/ksj/gml/data/N03/N03-2023/N03-20230101_GML.zip",
        "expected_bytes": 448_421_619,
        "dataset": "N03 行政区域",
        "vintage": "2023-01-01",
        "licence": "Open data (CC BY 4.0) since 2018; attribution required.",
    },
    "N02": {
        "filename": "ksj_N02_2023.zip",
        "url": "https://nlftp.mlit.go.jp/ksj/gml/data/N02/N02-23/N02-23_GML.zip",
        "expected_bytes": 17_518_918,
        "dataset": "N02 鉄道",
        "vintage": "FY2023 (2023-12-31)",
        "licence": "Open data (CC BY 4.0) since 2020; attribution required.",
    },
    "S12": {
        "filename": "ksj_S12_2023.zip",
        "url": "https://nlftp.mlit.go.jp/ksj/gml/data/S12/S12-24/S12-24_GML.zip",
        "expected_bytes": 6_244_895,
        "dataset": "S12 駅別乗降客数",
        "vintage": "FY2023",
        "licence": "Open data (CC BY 4.0); attribution required.",
    },
    "L01_2018": {
        "filename": "ksj_L01_2018.zip",
        "url": "https://nlftp.mlit.go.jp/ksj/gml/data/L01/L01-18/L01-18_GML.zip",
        "expected_bytes": 16_074_319,
        "dataset": "L01 地価公示",
        "vintage": "2018-01-01",
        "licence": (
            "Free for commercial use with attribution (pre-2019 terms); "
            "not the post-2019 open-data terms."
        ),
    },
    "L01_2023": {
        "filename": "ksj_L01_2023.zip",
        "url": "https://nlftp.mlit.go.jp/ksj/gml/data/L01/L01-23/L01-23_GML.zip",
        "expected_bytes": 19_915_437,
        "dataset": "L01 地価公示",
        "vintage": "2023-01-01",
        "licence": "Open data since 2019; attribution required.",
    },
    "L02_2018": {
        "filename": "ksj_L02_2018.zip",
        "url": "https://nlftp.mlit.go.jp/ksj/gml/data/L02/L02-18/L02-18_GML.zip",
        "expected_bytes": 17_519_541,
        "dataset": "L02 都道府県地価調査",
        "vintage": "2018-07-01",
        "licence": "Open data since 2018; attribution required.",
    },
    "L02_2023": {
        "filename": "ksj_L02_2023.zip",
        "url": "https://nlftp.mlit.go.jp/ksj/gml/data/L02/L02-23/L02-23_GML.zip",
        "expected_bytes": 17_598_886,
        "dataset": "L02 都道府県地価調査",
        "vintage": "2023-07-01",
        "licence": "Open data since 2018; attribution required.",
    },
}

MANIFEST = config.DATA_RAW / "ksj_manifest.json"


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


def download(key: str) -> None:
    meta = FILES[key]
    target = config.DATA_RAW / meta["filename"]

    if target.exists() and target.stat().st_size == meta["expected_bytes"]:
        print(f"{key}: already present ({target.stat().st_size:,} bytes), skipping")
    else:
        print(f"{key}: downloading {meta['url']}")
        tmp = target.with_suffix(".zip.part")
        with httpx.stream("GET", meta["url"], follow_redirects=True, timeout=120.0) as response:
            response.raise_for_status()
            total = int(response.headers.get("Content-Length", 0))
            done = 0
            with tmp.open("wb") as handle:
                for chunk in response.iter_bytes(chunk_size=1024 * 1024):
                    handle.write(chunk)
                    done += len(chunk)
                    if total:
                        pct = done / total * 100
                        print(f"\r  {done/1e6:8.1f} / {total/1e6:.1f} MB ({pct:5.1f}%)", end="")
        print()
        tmp.replace(target)

    size = target.stat().st_size
    if size != meta["expected_bytes"]:
        print(f"  WARNING: size {size:,} != expected {meta['expected_bytes']:,}")

    manifest = load_manifest()
    manifest[key] = {
        "filename": meta["filename"],
        "dataset": meta["dataset"],
        "vintage": meta["vintage"],
        "url": meta["url"],
        "access_date": date.today().isoformat(),
        "bytes": size,
        "sha256": sha256(target),
        "licence": meta["licence"],
    }
    save_manifest(manifest)
    print(f"{key}: saved {target.name} ({size:,} bytes) sha256={manifest[key]['sha256']}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("keys", nargs="+", choices=sorted(FILES), help="N03, N02, S12")
    args = parser.parse_args()
    for key in args.keys:
        download(key)


if __name__ == "__main__":
    main()
