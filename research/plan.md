# Roadmap: Phase 0 Completion and Public v1

**Last updated:** 2026-11-25
**Purpose:** Updated roadmap after the accessibility v0 and GitHub Pages milestones. Phase 0 completes the data foundation; Phase 1 builds, validates, and publishes v1.

---

## 1. Guiding constraints

- **Scope:** **1,059 clean municipal units** (from 1,235 reporting rows) + **6–8 small-municipality case studies**. The 682 missing towns/villages hold 500,360 vacant dwellings (5.6%).
- **Core panel:** 2018–2023 vacancy (balanced 1,057 units); 2013/2008 city/ward context; 2003 context deferred.
- **Market window:** 2018 and 2023 for v1; the API supports 2005+ for later extension.
- **Deliverable:** interactive map + open data/code + short report/methodology.
- **Methods:** transparent, reproducible, uncertainty-aware; no causal claims; no investment advice.
- **Data:** public sources; no akiya-bank scraping; no proprietary prediction map as input.

---

## 2. Current status

**Complete**

- Source and licence audit; e-Stat and MLIT API credentials active.
- 2023 and 2018 vacancy tables; total dwellings; proper vacancy rates.
- 2018–2023 municipal crosswalk; balanced panel 1,057 units.
- 2025 Census population/households; FY2022 fiscal capacity.
- Accessibility v0: 1,059-unit boundary layer, 9,007 station facilities, density and passenger metrics.
- 2013/2008 city/ward context: 812/815 and 805/815 units, with boundary flags.
- Public map v1: 1,059 features, six fixed-break indicators, Leaflet, Lighthouse 100.
- Market data: 2018/2023 XIT001 transactions; L01/L02 land prices; 2,118-row panel; 62.5% strict coverage.
- Akiya-bank aggregates: 53-month national trend and 47 prefecture rates.
- Public GitHub repository and GitHub Pages site.

**Remaining**

- Akiya-bank municipal participation list (blocked: AtHome maintenance, LIFULL CloudFront).
- Case studies.
- Go/no-go memo.
- Phase 1 index, validation, and publication.

---

## 3. Phase 0 — Complete the data foundation

### Stage A — 2013/2008 city/ward context — **complete**

- [x] Pull 2013 table 53 (`0003100835`) and 2008 table 043-2 (`0003010419`).
- [x] Inspect hierarchy, coverage, and category labels.
- [x] Build a historical code crosswalk from 2008/2013 to 2023, accounting for Heisei mergers.
- [x] Dissolve designated-city wards; keep the 23 special wards separate.
- [x] Harmonise categories and build `vacancy_context_2008_2023.csv`.
- [x] Validate totals and overlap with 2018/2023.
- [x] Write a comparability memo.

**Result:** 2013 covers **812/815** city/ward units; 2008 covers **805/815**. The missing units were towns/villages in those waves. 2013 has **1** post-2013 boundary change; 2008 has **35** post-2008 changes. Vacant-count correlation with 2018 is **0.995** (2013) and **0.990** (2008). Decision: use both as **city/ward context with boundary flags**; do not build a four-wave municipal panel.

**Outputs:** `data/processed/vacancy_context_2008_2023.csv`, `outputs/vacancy_comparability.txt`, `src/12_vacancy_context.py`.

---

### Stage B — Public map v1 — **complete**

- [x] Export simplified municipal GeoJSON for 1,059 units.
- [x] Include vacancy, census, fiscal, and accessibility attributes.
- [x] Add `panel.json` and `meta.json`; document the schema.
- [x] Replace the placeholder geometry in `docs/map.qmd`.
- [x] Add metric selector, legend, popup, and missing-value styling.
- [x] Update `docs/index.qmd`; test locally and on GitHub Pages.

**Result:** 1,059 features; six fixed-break indicators; simplified to 500 m and 0.001°; 1.42 MB GeoJSON, 0.27 MB gzip. Leaflet 1.9 replaced MapLibre after MapLibre failed to initialise in the test browser. Lighthouse 100 accessibility, 100 best practices, 100 SEO.

**Outputs:** `docs/data/municipalities.geojson`, `panel.json`, `meta.json`; `docs/map.js`, `docs/map.qmd`, `docs/styles.css`; `src/07_export_map.py`.

---

### Stage C — Market data — **complete**

- [x] Pull XIT001 for Tokyo, Nagano, and Kochi, 2018 and 2023.
- [x] Download L01/L02 land-price files for 2018 and 2023.
- [x] Parse and filter: land-only, land+house, condos; residential focus.
- [x] Map designated-city wards to cities; keep special wards separate.
- [x] Build the pilot market panel; QA coverage and thin cells.
- [x] Decide whether to pull all 47 prefectures. **Yes: pilot strict coverage 64.0%.**
- [x] Pull the full market data if coverage is workable.
- [x] Join to the vacancy/accessibility panel; build pilot v3.

**Headline:** official residential land price median and matched-site five-year change. Transactions are secondary.

**Result:** 2,118 rows (1,059 units x 2 years). Strict coverage **62.5%** (662 units); any market data **100%**. Designated cities 19/20; special wards 19/23; cities 539/772; towns/villages 85/244 (34.8%). XIT001 records: 314,309 in 2018 and 292,780 in 2023. L01 matched sites: 16,451; L02: 12,643. The 2018 L01/L02 schemas use different field positions from 2023, so the parser keeps explicit field maps.

**Output:** `data/processed/market_panel.csv`, `panel_with_market.csv`, `market_panel_pilot.csv`, `pilot_panel_v3.csv`; `src/13_market_pull.py`, `src/14_market_panel.py`.

---

### Stage D — Akiya-bank participation — **partial**

Independent of the MLIT data; can run alongside Stage C.

- [ ] Compile the official municipal participation list. **Blocked:** AtHome returned 503 emergency maintenance and LIFULL returned 403 CloudFront on 2026-11-27. Retry or save the official pages manually; do not bypass.
- [x] Extract the aggregate listing trend.
- [ ] Build the participation table: participation dummy, listing status, counts.
- [x] Confirm no scraping is needed; document terms.
- [ ] Join as a descriptive variable.

**Result:** 53-month national trend (March 2018 to October 2026): participants **487 to 1,155**, listings **3,458 to 20,010**. The chart labels **20,089** current listings; the October month-end bar is **20,010**. Current: **1,155** participants, **750** listing municipalities, **~29,000** cumulative transactions. Prefecture rates: **47**, national average **65.5%**, range **12.2% (Okinawa) to 100.0% (Toyama, Oita)**.

**Outputs:** `data/processed/akiya_bank_trend.csv`, `akiya_bank_prefecture.csv`, `akiya_bank_summary.csv`; `src/15_akiya_bank.py`. The municipal participation table is pending a current official list.

---

### Stage E — Case studies

After market data, so selection uses the full risk/activation/capacity picture.

- [ ] Build a provisional archetype shortlist.
- [ ] Select 6–8 municipalities covering the required archetypes.
- [ ] Check local data and document availability.
- [ ] Write the case-study protocol.
- [ ] Start local document collection.
- [ ] Draft case-study notes.

**Output:** shortlist, protocol, and case-study notes.

---

### Stage F — Go/no-go memo

The Phase 0 gate.

- [ ] Check join coverage across vacancy, census, and fiscal: target ≥90%.
- [ ] Check market coverage: target ≥60%, or a defensible pooling strategy.
- [ ] Record the 2013/2008 comparability decision.
- [ ] Confirm akiya-bank participation is compilable without scraping.
- [ ] Confirm 6–8 case studies are feasible.
- [ ] Revise scope if any gate fails.
- [ ] Write `docs/phase0_go_no_go.md`.

**Output:** a written go/no-go decision.

---

## 4. Phase 1 — Build, validate, publish

### 1a. Panel build

- [ ] Join vacancy, census, fiscal, accessibility, market, and akiya-bank data.
- [ ] Add IPSS projections and housing starts; build the demolition proxy.
- [ ] QA missingness, outliers, duplicate codes, and boundary changes.
- [ ] Write the data dictionary and QA report.
- [ ] Output `panel_v1.parquet` (or CSV).

### 1b. Index construction

- [ ] Current-risk sub-index: dilapidated “other vacant,” other-vacant rate, detached share, persistence.
- [ ] Pressure sub-index: population, ageing, households, migration, dwelling growth, old stock, demolition proxy.
- [ ] Activation sub-index: station density, market level/change, transaction liquidity, migration, DID share.
- [ ] Capacity overlay: fiscal strength, plan adoption, support corporations.
- [ ] Equal weights headline; PCA and policy weights as sensitivity.
- [ ] Uncertainty and rank stability.
- [ ] Output `index_v1.csv`, sensitivity report, methodology note.

### 1c. Validation and typology

- [ ] Market-lag test: risk versus 2018–2023 and 2023–2026 price/transaction changes.
- [ ] Akiya-bank signal: participation/listing intensity versus risk, conditional on accessibility.
- [ ] Policy designations: prefecture-level context and case studies.
- [ ] Typology: risk × activation, risk × capacity, price level × price change.
- [ ] Integrate case-study evidence.
- [ ] Output validation report and archetype tables.

### 1d. Publication v1

- [ ] Map v2 with risk, pressure, activation, capacity, and archetype layers.
- [ ] Uncertainty and insufficient-evidence hatching.
- [ ] Scatter plots: risk versus price momentum; risk versus fiscal capacity.
- [ ] Tables: top/bottom, archetypes, case studies.
- [ ] Report: 10–15 pages plus methodology and caveats.
- [ ] Open data/code: panel, codebook, scripts, licences.
- [ ] Public v1 release.

---

## 5. Data schema (minimum viable)

| Table | Key fields |
|---|---|
| `municipality` | `municipality_code`, `name_ja`, `name_en`, `prefecture`, `type`, `area_km2`, `centroid_lat`, `centroid_lon`, `boundary_year` |
| `vacancy` | `municipality_code`, `year`, `total_dwellings`, `vacant_total`, `rental`, `sale`, `secondary`, `other_vacant`, `other_vacant_dilapidated`, `other_vacant_detached`, `vacancy_rate`, `other_vacancy_rate`, `table_id`, `context_flag` |
| `demography` | `municipality_code`, `year`, `population`, `households`, `age_0_14`, `age_15_64`, `age_65_plus`, `deaths`, `net_migration`, `day_night_ratio` |
| `housing` | `municipality_code`, `year`, `starts`, `demolition_proxy`, `stock`, `pre1981_share`, `avg_floor_area` |
| `market` | `municipality_code`, `year`, `land_price_median`, `land_price_matched_change_5y`, `land_price_points`, `transaction_count`, `transaction_liquidity`, `land_transaction_median_unit_price`, `house_transaction_median_price`, `condo_transaction_median_unit_price`, `thin_flag` |
| `fiscal` | `municipality_code`, `fiscal_year`, `fiscal_strength_index`, `debt_service_ratio`, `tax_revenue_per_capita` |
| `accessibility` | `municipality_code`, `station_count`, `station_density_per_100km2`, `stations_per_10k_pop`, `station_passengers_sum`, `passenger_data_share`, `tram_stop_count`; `nearest_station_km`, `did_share`, `travel_time_to_100k_city` deferred |
| `policy` | `municipality_code`, `year`, `plan_adopted`, `akiya_bank_participant`, `designation_count_pref` |
| `index` | `municipality_code`, `version`, `risk_current`, `risk_pressure`, `risk_composite`, `activation`, `capacity`, `archetype`, `uncertainty`, `insufficient_evidence` |
| `provenance` | `dataset`, `source_url`, `access_date`, `licence`, `transformation`, `notes` |

---

## 6. Milestones

| Milestone | Status | Success criterion |
|---|---|---|
| **M0 — Source/licence matrix** | **Complete** | All core sources confirmed; credentials active; licences recorded. |
| **M1 — 2023/2018 vacancy + pilot** | **Complete** | 2023 and 2018 parsed; joins tested; QA report. |
| **M2 — Core panel + accessibility v0** | **Complete** | 2018–2023 harmonised (1,057 units); accessibility metrics; boundary layer. |
| **M2b — 2013/2008 context** | **Complete** | 812/815 and 805/815 city/ward units; boundary flags; comparability memo. |
| **M3 — Public map v1** | **Complete** | 1,059 features; six indicators; simplified boundaries; Lighthouse 100. |
| **M4 — Market panel** | **Complete** | 2,118 rows; 62.5% strict coverage; 100% any market data; pilot/full decision made. |
| **M5 — Akiya-bank participation** | **Partial** | National trend and prefecture rates complete; municipal list blocked; no scraping. |
| **M6 — Case studies** | Stage E | 6–8 municipalities selected; protocol and notes. |
| **M7 — Go/no-go** | Stage F | All criteria assessed; scope confirmed or revised. |
| **M8 — Index v1** | Phase 1b | Risk/activation/capacity indices; weights; uncertainty. |
| **M9 — Validation + archetypes** | Phase 1c | Market-lag tests; akiya-bank signal; case studies; archetype tables. |
| **M10 — Public v1** | Phase 1d | Map, report, open data/code, methodology, caveats. |

---

## 7. Risks and mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| 2013/2008 tables not comparable | Medium | High | Audit early; fall back to 2018–2023 core; document. |
| Rural market data too thin | Observed | Medium | 34.8% of towns/villages meet strict coverage; use L02 as robustness; flag thin cells; the activation lens is urban-weighted. |
| Coverage bias (682 missing towns/villages; 500,360 vacant dwellings) | Certain | High | Define universe; case studies; coverage appendix; no “all Japan” claim; state the 5.6% uncovered vacancy. |
| Sampling error / unstable rankings | High | High | Uncertainty bands; empirical Bayes; avoid overranking small differences. |
| Municipal mergers | Medium | Medium | Crosswalk; aggregate predecessors; document unmapped units. |
| Akiya-bank data unavailable | Medium | Low | Official aggregates/participation; manual counts; do not block on it. |
| Designation data not municipal | High | Medium | Prefecture-level context; case studies; reframe the question. |
| 2026 amendment interpretation | Low | Medium | Read the amended statute; label secondary sources. |
| Licensing (OSM, MLIT, portals) | Medium | Medium | Attribution; ODbL isolation; no scraping; legal review if needed. |
| Investment-advice risk | Medium | High | Policy framing; disclaimers; no property-level recommendations. |
| Scope creep (forecasting, causal evaluation) | High | Medium | Keep Phase 1 descriptive; defer extensions. |
| Map performance / heavy geometry | Medium | Medium | Simplify and quantise polygons; target a small GeoJSON; test on mobile. |

---

## 8. Go/no-go criteria

Proceed to Phase 1 only if:

1. **Join rate:** ≥90% of the 1,059 clean municipal units join across vacancy, census, and fiscal data.
2. **Market coverage:** ≥60% of units have usable price/transaction data, or a defensible pooling/flagging strategy.
3. **Comparability:** 2018–2023 is clean; 2013/2008 are either usable with flags or excluded.
4. **Akiya-bank:** participation data compilable without scraping; case-study counts feasible.
5. **Case studies:** 6–8 municipalities have enough local data/documents to be credible.

If any criterion fails, revise the scope before building.

---

## 9. What not to do

- Do not scrape akiya-bank listings.
- Do not rank all 1,741 municipalities.
- Do not treat “other vacant” as “abandoned.”
- Do not present the 6x tax-base change as a 6x tax bill.
- Do not claim a national akiya tax.
- Do not use policy designations as an unbiased risk measure.
- Do not build a forecasting model in Phase 1.
- Do not give property-level or investment advice.

---

## 10. Resourcing

The remaining Phase 0 work is feasible for one person part-time over roughly 3–5 weeks, depending on how thin the market data are. Phase 1 is roughly 8–12 weeks part-time. The sequence matters more than the calendar:

1. Stage A — 2013/2008 context.
2. Stage B — public map v1.
3. Stage C — market data.
4. Stage D — akiya-bank (can overlap with C).
5. Stage E — case studies.
6. Stage F — go/no-go.
7. Phase 1a–1d.

If a stage fails its coverage test, revise the scope rather than forcing the next stage.
