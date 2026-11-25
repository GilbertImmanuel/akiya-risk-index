# The Empty House Atlas

A reproducible, municipal-level study of housing vacancy in Japan: where
structural vacancy is accumulating, what distinguishes places with different
trajectories, and whether local housing markets already reflect the risk.

**Status:** Phase 0 in progress. The vacancy, 2013/2008 context, census, fiscal,
and accessibility baseline is built. Next: public map v1, market data, and the
index.

---

## What this is

- A **municipal panel** built from Japan's official statistics.
- A **risk index** focused on dilapidated “other vacant” housing, with separate
  lenses for activation potential and municipal response capacity.
- An **interactive map and report** aimed at researchers and policymakers.
- **Not** a property-level prediction tool, a causal evaluation of the 2023
  Vacant Houses Act, or investment advice.

The research question, scope, and caveats are documented in
[`research/question-and-scope.md`](research/question-and-scope.md). The
one-page summary is [`research/summary.md`](research/summary.md).

---

## Stack

| Layer | Choice |
|---|---|
| Analysis | Python 3.12, uv, pandas, DuckDB, Parquet |
| Geospatial | geopandas, shapely, pyogrio, pyproj |
| Statistics | statsmodels, linearmodels, scikit-learn, scipy |
| Report | Quarto |
| Interactivity | Observable JS (`{ojs}`), Observable Plot, `Inputs` |
| Map | MapLibre GL JS |
| Frontend language | Plain JavaScript (ES modules) |
| Deployment | GitHub Pages (static) |

All core data sources are free. See [`DATA_LICENCES.md`](DATA_LICENCES.md) and
[`research/data-sources.md`](research/data-sources.md).

---

## Repository layout

```
.
├── data/
│   ├── raw/            # untouched downloads (git-ignored)
│   ├── interim/        # parsed tables (git-ignored)
│   └── processed/      # analysis panel
├── src/                # numbered pipeline scripts
├── docs/               # Quarto website
│   ├── _quarto.yml
│   ├── index.qmd
│   ├── map.qmd         # MapLibre + OJS prototype
│   └── data/           # precomputed JSON/GeoJSON for the browser
├── outputs/            # figures, tables, exports
├── research/           # evidence dossier
├── tests/              # tests (placeholder for now)
├── .github/workflows/  # GitHub Pages deployment
├── pyproject.toml
└── README.md
```

---

## Quick start

### 1. Python environment

```bash
uv sync
```

If the geospatial wheels fail on Windows, use a conda-forge environment instead:

```bash
micromamba create -n akiya -c conda-forge python=3.12 geopandas pyogrio shapely pyproj duckdb
micromamba activate akiya
```

### 2. API keys

Copy `.env.example` to `.env` and fill in:

- `ESTAT_APP_ID` — free from https://www.e-stat.go.jp/api/
- `REINFOLIB_API_KEY` — free from https://www.reinfolib.mlit.go.jp/api/request/

### 3. Quarto

Install Quarto: https://quarto.org/docs/get-started/

Then:

```bash
quarto preview docs
quarto render docs
```

The built site is written to `docs/_site/`.

---

## Data

The primary dataset is the **2023 Housing and Land Survey**, municipal table
34-2, from e-Stat. Its 1,235 municipal reporting rows double-count designated
cities and their wards; the clean analysis universe is **1,059 municipal units**
(792 cities + 23 special wards + 244 towns/villages). **682 of 926
towns/villages (73.6%) are absent**, and they hold **500,360 vacant dwellings
(5.6% of the national total)**. The project handles them through case studies,
not a national ranking.

Key caveats:

- “Other vacant” is **not** synonymous with “abandoned.”
- The survey excludes `廃屋` (ruined structures).
- Municipal estimates are sample-based and noisy.
- Policy designations reflect enforcement capacity, not only blight.
- There is **no national akiya tax**.

Read [`research/summary.md`](research/summary.md) before using the data.

---

## Deployment

The site is designed for a separate public repo and GitHub Pages:

```
https://gilbertimmanuel.github.io/akiya-risk-index/
```

The workflow in `.github/workflows/pages.yml` renders the Quarto site and
deploys it to GitHub Pages.

All site assets use relative paths because the site is served from a
subpath.

---

## Licence

Code: MIT (see [`LICENSE`](LICENSE)).
Data: source-specific terms (see [`DATA_LICENCES.md`](DATA_LICENCES.md)).
