# Phase 0/1 Plan: From Audit to Public v1

**Last updated:** 2026-11-12
**Purpose:** A concrete, milestone-based plan for the next stage. Phase 0 is a feasibility audit; Phase 1 builds the panel, index, and public product. Do not skip Phase 0.

---

## 1. Guiding constraints

- **Scope:** **1,059 clean municipal units** (from 1,235 reporting rows; 15,000+ universe) + 6–8 small-municipality case studies. The 682 missing towns/villages hold 500,360 vacant dwellings (5.6%).
- **Core panel:** 2008–2023 vacancy waves; 2003 context only.
- **Deliverable:** interactive map + open data/code + short report/methodology.
- **Methods:** transparent, reproducible, uncertainty-aware; no causal claims; no investment advice.
- **Data:** public sources; no akiya-bank scraping; no proprietary prediction map as input.

---

## 2. Phase 0 — Audit and spike (weeks 1–3)

### 0.1 Source and licence audit

- Confirm access to e-Stat, MLIT API, census, IPSS, local finance, boundaries.
- Record licence/attribution requirements in `data-sources.md`.
- Register for an e-Stat API application ID and a MLIT Real Estate Library API key.
- **Output:** updated source inventory; access checklist.

### 0.2 Vacancy table audit

- Download 2023 table 34-2, 2018 table 35-2, 2013 table 53 (+ 町村 table), 2008 table 043-1.
- Compare:
  - category labels and definitions;
  - municipal coverage;
  - totals vs published national figures;
  - `腐朽・破損` cells and suppression.
- Build a harmonised vacancy table with a `wave` and `table_id` column.
- **Output:** vacancy panel v0; table-comparability memo.

### 0.3 Municipal code crosswalk

- Download e-Stat municipal code/merger tables.
- Build a crosswalk from historical codes to 2023 boundaries.
- Flag municipalities that cannot be cleanly mapped.
- Decide whether to aggregate predecessors or drop them.
- **Output:** `municipality_crosswalk.csv`; merger QA report.

### 0.4 Three-prefecture pilot

Pilot **Tokyo, Nagano, Kochi**:

- Tokyo: high demand, many wards, secondary homes, data-rich.
- Nagano: high vacancy, secondary homes, rural towns, tourism.
- Kochi: high vacancy, ageing, rural, thin market data.

For each:

- join vacancy, census, local finance, land prices, transactions, accessibility;
- count records per municipality;
- test price aggregation and transaction liquidity;
- identify missing/thin cells.
- **Output:** pilot panel; coverage diagnostics; go/no-go recommendation.

### 0.5 Akiya-bank feasibility

- Compile the official participation list.
- Extract the aggregate listing trend.
- Select 6–8 case-study municipalities for manual listing counts.
- Confirm that no scraping is needed.
- **Output:** akiya-bank participation table; case-study protocol.

### 0.6 Case-study shortlist

- Select 6–8 municipalities covering:
  - high risk / high activation;
  - high risk / low activation;
  - low risk / high activation;
  - low risk / low activation;
  - secondary-home composition;
  - urban shrinkage;
  - disaster/geography.
- **Output:** shortlist with data profile and rationale.

### 0.7 Go/no-go memo

Answer:

- Can at least 90% of the 1,059 clean municipal units join cleanly across vacancy, census, and fiscal data?
- Is price/transaction coverage sufficient for at least 60% of units, or is a pooling strategy defensible?
- Are 2013/2008 comparable enough to include as a four-wave panel?
- Is akiya-bank participation data compilable without scraping?
- Are the case studies feasible?

**If no:** revise scope before Phase 1. Do not build on a broken panel.

---

## 3. Phase 1 — Build, validate, publish (weeks 4–10)

### 1a. Panel build (weeks 4–6)

- ETL all vacancy waves; harmonise codes; join:
  - census 2000–2025;
  - IPSS projections;
  - local finance;
  - land prices and transactions;
  - housing starts/demolition proxy;
  - accessibility;
  - akiya-bank participation.
- QA: missingness, outliers, duplicate codes, boundary changes.
- **Output:** `panel_v1.parquet` (or CSV), data dictionary, QA report.

### 1b. Index construction (weeks 7–8)

- Build current-risk sub-index:
  - dilapidated other-vacant rate (headline);
  - other-vacant rate;
  - detached other-vacant share;
  - persistence across waves.
- Build pressure sub-index:
  - population change;
  - ageing;
  - household change;
  - net migration;
  - dwelling growth minus household growth;
  - pre-1981 stock share;
  - demolition proxy.
- Build activation index:
  - station density/distance;
  - DID share;
  - recent migration;
  - land-price level and change;
  - transaction liquidity.
- Build capacity overlay:
  - fiscal strength;
  - plan adoption (if available);
  - support corporations (if available).
- Weights: equal headline; PCA and policy weights as sensitivity.
- Uncertainty: simulation and/or empirical Bayes; rank stability.
- **Output:** index v1; sensitivity report; methodology note.

### 1c. Validation and typology (weeks 9–10)

- Market-lag test: risk vs 2018–2023 and 2023–2026 price/transaction changes.
- Akiya-bank: participation/listing intensity vs risk, conditional on accessibility.
- Policy designations: prefecture-level context; case studies.
- Typology: risk × activation; risk × capacity; price level × price change (secondary).
- Case studies: 6–8; local documents, plans, and (if feasible) interviews.
- **Output:** validation report; archetype tables; case-study notes.

### 1d. Publication (weeks 10–11)

- Interactive map:
  - layers: current risk, pressure, activation, capacity, archetype;
  - uncertainty/insufficient-evidence hatching;
  - tooltips with source/provenance.
- Scatter: risk vs price momentum; risk vs fiscal capacity.
- Tables: top/bottom, archetypes, case studies.
- Report: 10–15 pages + methodology appendix + caveats.
- Open data/code: panel, codebook, scripts, licence/provenance.
- **Output:** public v1.

---

## 4. Data schema (minimum viable)

| Table | Key fields |
|---|---|
| `municipality` | `municipality_code`, `name_ja`, `name_en`, `prefecture`, `type`, `area_km2`, `centroid_lat`, `centroid_lon`, `boundary_year` |
| `vacancy` | `municipality_code`, `year`, `total_dwellings`, `vacant_total`, `rental`, `sale`, `secondary`, `other_vacant`, `other_vacant_dilapidated`, `other_vacant_detached`, `vacancy_rate`, `other_vacancy_rate`, `table_id` |
| `demography` | `municipality_code`, `year`, `population`, `households`, `age_0_14`, `age_15_64`, `age_65_plus`, `deaths`, `net_migration`, `day_night_ratio` |
| `housing` | `municipality_code`, `year`, `starts`, `demolition_proxy`, `stock`, `pre1981_share`, `avg_floor_area` |
| `market` | `municipality_code`, `year`, `land_price_median`, `land_price_change_5y`, `transaction_count`, `transaction_median_price`, `transaction_liquidity` |
| `fiscal` | `municipality_code`, `fiscal_year`, `fiscal_strength_index`, `debt_service_ratio`, `tax_revenue_per_capita` |
| `accessibility` | `municipality_code`, `station_count`, `station_density`, `nearest_station_km`, `did_share`, `travel_time_to_100k_city` |
| `policy` | `municipality_code`, `year`, `plan_adopted`, `akiya_bank_participant`, `designation_count_pref` |
| `index` | `municipality_code`, `version`, `risk_current`, `risk_pressure`, `risk_composite`, `activation`, `capacity`, `archetype`, `uncertainty`, `insufficient_evidence` |
| `provenance` | `dataset`, `source_url`, `access_date`, `licence`, `transformation`, `notes` |

---

## 5. Milestones

| Milestone | Timing | Success criterion |
|---|---|---|
| **M0 — Source/licence matrix** | End of week 1 | All core sources confirmed; access keys in place; licences recorded. |
| **M1 — 2023 pilot panel** | End of week 2 | 2023 vacancy data parsed; joins tested on three prefectures; QA report. |
| **M2 — Four-wave panel** | End of week 3 / early week 4 | 2008–2023 harmonised; crosswalk; coverage flags; go/no-go memo. |
| **M3 — Index v1** | End of week 7 | Risk/activation/capacity indices; equal/PCA/policy weights; uncertainty. |
| **M4 — Validation + archetypes** | End of week 9 | Market-lag tests; akiya-bank analysis; case studies; archetype tables. |
| **M5 — Public v1** | End of week 10–11 | Map, report, open data/code, methodology, caveats. |

---

## 6. Risks and mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| 2013/2008 tables not comparable | Medium | High | Audit early; fall back to 2018–2023 core; document. |
| Rural market data too thin | High | Medium | Pool years; use land-price points; flag insufficient evidence; activation lens may be urban-only. |
| Coverage bias (682 missing towns/villages; 500,360 vacant dwellings) | Certain | High | Define universe; case studies; coverage appendix; no “all Japan” claim; state the 5.6% uncovered vacancy. |
| Sampling error / unstable rankings | High | High | Uncertainty bands; empirical Bayes; avoid overranking small differences. |
| Municipal mergers | Medium | Medium | Crosswalk; aggregate predecessors; document unmapped units. |
| Akiya-bank data unavailable | Medium | Low | Official aggregates/participation; manual counts; do not block on it. |
| Designation data not municipal | High | Medium | Prefecture-level context; case studies; reframe the question. |
| 2026 amendment interpretation | Low | Medium | Read the amended statute; label secondary sources. |
| Licensing (OSM, MLIT, portals) | Medium | Medium | Attribution; ODbL isolation; no scraping; legal review if needed. |
| Investment-advice risk | Medium | High | Policy framing; disclaimers; no property-level recommendations. |
| Scope creep (forecasting, causal evaluation) | High | Medium | Keep Phase 1 descriptive; defer extensions. |

---

## 7. Go/no-go criteria

Proceed to Phase 1 only if:

1. **Join rate:** ≥90% of the 1,059 clean municipal units join across vacancy, census, and fiscal data.
2. **Market coverage:** ≥60% of units have usable price/transaction data, or a defensible pooling/flagging strategy.
3. **Comparability:** 2018–2023 is clean; 2013/2008 are either usable with flags or excluded.
4. **Akiya-bank:** participation data compilable without scraping; case-study counts feasible.
5. **Case studies:** 6–8 municipalities have enough local data/documents to be credible.

If any criterion fails, revise the scope before building.

---

## 8. What not to do

- Do not scrape akiya-bank listings.
- Do not rank all 1,741 municipalities.
- Do not treat “other vacant” as “abandoned.”
- Do not present the 6x tax-base change as a 6x tax bill.
- Do not claim a national akiya tax.
- Do not use policy designations as an unbiased risk measure.
- Do not build a forecasting model in Phase 1.
- Do not give property-level or investment advice.

---

## 9. Resourcing

The work is feasible for a small team (1–2 people) over about 10–11 weeks, assuming:

- access to a machine with Python/R and GIS libraries;
- API keys for e-Stat and MLIT;
- willingness to do manual case-study collection;
- no proprietary data purchases.

If only one person is available part-time, Phase 0 may take 4–6 weeks and Phase 1 8–12 weeks. The plan should be adjusted rather than skipping the audit.
