# Data Folder

| Folder | Contents | Committed? |
|---|---|---|
| `raw/` | Untouched downloads from e-Stat, MLIT, census, etc. | **No** (git-ignored; reproducible) |
| `interim/` | Parsed/cleaned tables before the final join. | **No** (git-ignored) |
| `processed/` | Analysis panel, index outputs, GeoParquet. | Maybe; depends on size and licence. |

## Conventions

- Keep raw files exactly as downloaded.
- Record the source URL, access date, and checksum in `data/raw/SOURCES.md`.
- Use ISO dates in filenames: `estat_34-2_2023_2026-11-16.xlsx`.
- Processed files: `panel_v1.parquet`, `index_v1.csv`.

## Reproducibility

All raw data should be re-downloadable from the source. The pipeline scripts in
`src/` document the URL and transformation for each file. If a source changes,
record the version/access date.
