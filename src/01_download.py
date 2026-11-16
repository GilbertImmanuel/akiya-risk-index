"""Download raw source data.

Phase 0 TODO:
- Download 2023 Housing and Land Survey table 34-2.
- Download 2018 table 35-2, 2013 table 53 (+ 町村), 2008 table 043-1.
- Download census, local finance, land price, and transaction data.
- Record source URL, access date, and checksum in data/raw/SOURCES.md.

Do not hard-code API keys; use ESTAT_APP_ID / REINFOLIB_API_KEY from .env.
"""

from __future__ import annotations


def main() -> None:
    raise NotImplementedError("Phase 0: implement the download step.")


if __name__ == "__main__":
    main()
