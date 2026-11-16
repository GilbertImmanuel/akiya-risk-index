# Source Pipeline

Numbered scripts, run in order. Phase 0 placeholders are marked
`NotImplementedError`; they will be filled as the audit progresses.

| Script | Purpose |
|---|---|
| `00_config.py` | Paths, environment variables, constants. |
| `01_download.py` | Download raw data from e-Stat, MLIT, census, etc. |
| `02_parse_vacancy.py` | Parse the Housing and Land Survey municipal tables. |
| `03_crosswalk.py` | Harmonise municipal codes across mergers. |
| `04_census.py` | Parse the 2025 Census municipal population/household tables. |
| `04_join_panel.py` | Join vacancy, demography, market, fiscal, accessibility. |
| `05_index.py` | Build risk, activation, and capacity indices. |
| `06_validate.py` | Schema checks, uncertainty, sensitivity, validation. |
| `07_export_map.py` | Export GeoJSON/JSON for the Quarto site. |

## Conventions

- Raw files go in `data/raw/` and are never overwritten.
- Intermediate tables go in `data/interim/`; the final panel in `data/processed/`.
- Use `uv run python src/01_download.py` etc.
- Do not hard-code API keys; read them from `.env`.
- Log the source URL and access date for every download.
- Keep scripts deterministic; no manual edits to processed data.
