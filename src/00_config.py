"""Project paths and configuration.

Keep all path logic here so the numbered scripts stay short.
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
DATA_RAW = ROOT / "data" / "raw"
DATA_INTERIM = ROOT / "data" / "interim"
DATA_PROCESSED = ROOT / "data" / "processed"
OUTPUTS = ROOT / "outputs"
DOCS = ROOT / "docs"
DOCS_DATA = DOCS / "data"

for path in (DATA_RAW, DATA_INTERIM, DATA_PROCESSED, OUTPUTS, DOCS_DATA):
    path.mkdir(parents=True, exist_ok=True)

load_dotenv(ROOT / ".env")

ESTAT_APP_ID = os.getenv("ESTAT_APP_ID", "")
REINFOLIB_API_KEY = os.getenv("REINFOLIB_API_KEY", "")

# Primary survey tables. Confirm exact file IDs in Phase 0.
VACANCY_TABLES = {
    2023: "34-2",
    2018: "35-2",
    2013: "53",
    2008: "043-1",
}

# Phase 0: downloaded vacancy tables.
VACANCY_2023_XLSX = DATA_RAW / "estat_34-2_2023_2026-11-16.xlsx"
VACANCY_2023_CSV = DATA_INTERIM / "vacancy_2023.csv"
VACANCY_2018_XLSX = DATA_RAW / "estat_35-2_2018_2026-11-16.xlsx"
VACANCY_2018_CSV = DATA_INTERIM / "vacancy_2018.csv"
