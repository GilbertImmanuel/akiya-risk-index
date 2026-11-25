# Source Pipeline

Numbered scripts, run in order. Most Phase 0 data steps are implemented;
index and map export remain placeholders.

| Script | Purpose |
|---|---|
| `00_config.py` | Paths, environment variables, constants. |
| `01_download.py` | Download raw data from e-Stat, MLIT, census, etc. |
| `02_parse_vacancy.py` | Parse the Housing and Land Survey municipal tables. |
| `03_crosswalk.py` | Harmonise municipal codes across mergers. |
| `04_census.py` | Parse the 2025 Census municipal population/household tables. |
| `04b_fiscal.py` | Parse the municipal fiscal strength index (FY2022, SSDSE). |
| `04c_dwellings.py` | Parse total dwellings and vacancy categories (2023/2018 tables 1-2-1). |
| `04d_vacancy_panel.py` | Build the full 2018–2023 vacancy panel with proper rates. |
| `04_join_panel.py` | Join vacancy, demography, market, fiscal, accessibility (pilot). |
| `05_index.py` | Build risk, activation, and capacity indices. |
| `06_validate.py` | Schema checks, uncertainty, sensitivity, validation. |
| `07_export_map.py` | Export GeoJSON/JSON for the Quarto site. |
| `08_download_ksj.py` | Download KSJ N03/N02/S12 with checksums. |
| `09_municipal_boundaries.py` | Build the 1,059-unit dissolved boundary layer. |
| `10_stations.py` | Build station facilities and join S12 passengers. |
| `11_accessibility.py` | Spatial join, accessibility metrics, pilot v2. |
| `12_vacancy_context.py` | Parse 2013/2008 city/ward tables; build context and comparability memo. |

## Conventions

- Raw files go in `data/raw/` and are never overwritten.
- Intermediate tables go in `data/interim/`; the final panel in `data/processed/`.
- Use `uv run python src/01_download.py` etc.
- Do not hard-code API keys; read them from `.env`.
- Log the source URL and access date for every download.
- Keep scripts deterministic; no manual edits to processed data.
