# Research Log

**Last updated:** 2026-11-23
**Purpose:** A chronological record of searches, sources, and what they changed. This is the audit trail for the dossier.

---

## 2026-11-25 — Roadmap revised after accessibility and Pages milestones

- **Action:** Rewrote `plan.md` around the remaining Phase 0 stages: **A** 2013/2008 context, **B** public map v1, **C** market data, **D** akiya-bank, **E** case studies, **F** go/no-go, then Phase 1a–1d.
- **Rationale:** A closes the last e-Stat-only vacancy task; B uses existing data and replaces the placeholder map; C unblocks the market-lag question; D is independent; E needs C; F is the gate.
- **Changes:** Updated the data schema for the actual accessibility v0 fields and the market v1 fields; updated milestones M0–M2 to complete; added map-performance risk; changed the market window to 2018/2023 for v1.
- **Next:** Stage A — pull 2013 table 53 and 2008 table 043-2.

---

## 2026-11-23 — Accessibility v0 (N03/N02/S12)

- **Action:** Downloaded KSJ **N03** (2023-01-01 boundaries), **N02** (FY2023 rail), and **S12** (FY2023 passengers); recorded URLs, sizes, and SHA-256 in `data/raw/SOURCES.md` and `data/raw/ksj_manifest.json`.
- **Boundaries:** built `data/interim/municipal_boundaries.gpkg`; 1,059/1,059 panel units, designated-city wards dissolved, special wards separate, `所属未定地` excluded; median area ratio vs census **1.0000**.
- **Stations:** 10,240 N02 records → 9,007 facilities after excluding funicular/trolleybus; 8,399 heavy-rail, 608 tram-only. Representative points from platform LineStrings; grouped by N02 group code.
- **Spatial join:** first matched to all N03 municipality polygons, then restricted to the panel, so stations in the 682 missing towns are not reassigned to neighbours. 7,479 heavy-rail stations in the panel; 924 outside; 126 units (11.9%) have no heavy-rail station.
- **Passengers:** S12 FY2023; no-data records store 0, so only duplicate code 1 + existence code 1 were summed. 6,536/7,479 heavy stations (87.4%) have data.
- **Associations:** station density vs population density **ρ=+0.701**; vs 2023 dilapidated other-vacancy rate **ρ=−0.447**; vs 2018–2023 change in that rate **ρ=−0.018**. Descriptive, not causal.
- **Outputs:** `accessibility_2023.csv`, `panel_with_accessibility_2023.csv`, `pilot_panel_v2.csv`, `station_assignments.csv`, `zero_station_municipalities.csv`, `accessibility_validation.txt`.
- **Caveat:** passenger metrics are secondary and coverage-sensitive; nearest-station distance and travel time deferred to Phase 1.
- **Next:** market data (MLIT key pending; CSV fallback), akiya-bank participation, case studies, go/no-go memo.

---

## 2026-11-23 — Total dwellings and proper vacancy rates

- **Action:** Pulled 2023/2018 table 1-2-1 (`0004021421` / `0003355290`) and built `dwellings_2023.csv`, `dwellings_2018.csv`, `vacancy_panel_2018_2023.csv`, and `pilot_panel_v1.csv`.
- **Validation:** total dwellings 65,046,700 / 62,407,400; **1,059/1,059** and **1,086/1,086** coverage; vacancy counts match tables 34-2/35-2 with **0 mismatches**.
- **Coverage:** the 682 missing municipalities hold 500,360 vacant (5.6%), 327,880 other vacant (8.5%), and **89,240 dilapidated other vacant (10.0%)** — the risk measure has a larger coverage gap.
- **Proper rates:** top 2023 dilapidated other-vacancy rates are 川崎町 12.25%, 新上五島町 11.89%, 平戸市 9.29%, 垂水市 9.29%, 室戸市 9.11%. Largest increases: 川崎町 +8.48 pp, さつま町 +6.51, 有田川町 +5.48, 新上五島町 +5.23, 平戸市 +4.79.
- **Proxy comparison:** household proxy vs proper rate Spearman **0.991**; 軽井沢町 is proxy rank 9 vs proper rank 35. The proxy misranks secondary-home/large-household places; the proper denominator is required.
- **Caveat:** municipal survey estimates are noisy; the top rates/changes need uncertainty bands.

---

## 2026-11-17 — Fiscal capacity and pilot panel v0

- **Action:** Pulled the municipal fiscal strength index from SSDSE table D 行政基盤 (`statsDataId=0000020204`, indicator D2201) for FY2022; built `data/interim/fiscal_2022.csv`. Built the first pilot panel for Tokyo, Nagano, and Kochi (`data/processed/pilot_panel_v0.csv`).
- **Fiscal result:** 1,913 areas; 1,036 of 1,059 analysis units covered (97.8%). The 23 Tokyo special wards have no index because the index is municipal, not ward-level. FY2023/2024 return no data in this table; FY2022 is the latest.
- **Pilot result:** 89 units (Tokyo 51, Nagano 25, Kochi 13). No missing 2018 vacancy or 2025 census; 23 special wards missing fiscal.
- **Preliminary pattern:** using dilapidated “other vacant” per 1,000 households as a provisional proxy, Kochi’s rural cities and Nagano’s towns/cities rank highest; Tokyo’s wards/suburbs lower. Not a final ranking.
- **Next:** total dwellings (proper denominator), accessibility, market data (MLIT key pending), akiya-bank participation, case studies, go/no-go memo.

---

## 2026-11-16 — 2025 Census municipal data pulled

- **Action:** Used the e-Stat API to pull 2025 Census table 1-2 (`0004050417`) and table 1-1 (`0004050397`); built `data/interim/census_2025.csv`.
- **Result:** 1,961 areas; 2020 population 126,146,099; 2025 population 123,049,524; total households 57,124,507.
- **Discrepancy:** the API table’s national 2025 population is **123,049,524**, while the summary PDF headline is **122,972,528** (difference **76,996**). The API table is internally consistent with its 2020 baseline and five-year change. Use the API table for municipal joins; cite the headline separately.
- **Households:** the table’s total households are **57,124,507**; the summary’s general households are **57,182,000**. Do not mix the concepts.
- **Next:** local finance/accessibility and the Tokyo/Nagano/Kochi pilot; MLIT key pending.

---

## 2026-11-16 — e-Stat API active; 2013/2008 are city/ward only

- **Action:** Tested the e-Stat application ID from `.env` and queried the 2013/2008 table lists.
- **Result:** 2013 table 53 (`statsDataId=0003100835`) and 2008 table 043-2 (`statsDataId=0003010419`) are **市区 only**. They do not include towns/villages. The 2008 table 043-1 is prefectural.
- **Decision (D4 updated):** core panel is **2018–2023** (balanced 1,057 units); 2013/2008 are **city/ward context only**. A four-wave municipal panel including towns/villages is not available from the API.
- **Why it mattered:** this avoids a false four-wave panel and keeps the municipal coverage honest. It also confirms the project’s core comparison is 2018–2023.
- **Next:** optionally parse the 2013/2008 市区 tables; build the Tokyo/Nagano/Kochi pilot.

---

## 2026-11-16 — 2018–2023 crosswalk built; no mergers in the period

- **Action:** Downloaded the e-Stat municipal merger/boundary-change history (3,507 rows) and built `src/03_crosswalk.py`.
- **Result:** 18 status changes between 2018 and 2023, but **no municipal mergers**. The vacancy-table coverage change is **threshold-driven**: 29 towns/villages dropped out of 2023 and 2 entered. One name change (28221 篠山市 → 丹波篠山市).
- **Balanced panel:** **1,057 units** (1,056 matched + 1 name change). The 29 dropped and 2 added units are retained in the full crosswalk but excluded from the balanced panel.
- **Output:** `data/processed/municipality_crosswalk_2018_2023.csv`.
- **Why it mattered:** the 2018–2023 panel is simpler than assumed; the harder harmonisation problem starts with 2013 and 2008.

---

## 2026-11-16 — 2018 table parsed; measured dilapidation fell

- **Action:** Downloaded 2018 table 35-2 (`statInfId=000031865730`) and refactored `src/02_parse_vacancy.py` to handle both 2018 and 2023 layouts.
- **Result:** 2018 national totals: 8,488,600 vacant; 3,487,200 "other vacant"; 1,006,000 dilapidated "other vacant"; 799,900 dilapidated detached. 2018 covers 1,086 clean units (271 towns/villages), 95.2% of the vacancy stock; 411,330 (4.85%) uncovered.
- **Comparison:** broad "other vacant" **+10.6%** (2018→2023), but dilapidated "other vacant" **−11.0%** (1,006,000 → 895,300). The dilapidated share fell from 28.8% to 23.2%. Part of the decline is likely `廃屋` attrition — the worst structures leaving the survey — alongside policy/redevelopment effects.
- **Why it mattered:** the measured risk trend is not monotonic. The headline measure is a lower bound that can fall when the worst structures leave the statistics. The dossier now carries this caveat.
- **Next:** 2013 table 53 (+ 町村) and 2008 table 043-1.

---

## 2026-11-16 — Phase 0 parse corrects the coverage calculation

- **Action:** Downloaded the 2023 table 34-2 Excel from e-Stat (`statInfId=000040209901`) and parsed it with `src/02_parse_vacancy.py`.
- **Result:** The table's 1,235 municipal reporting rows are **not a clean municipality count**. They include duplicate hierarchy levels: 792 cities (20 designated + 772 non-designated), 23 special wards, 244 towns/villages, 175 designated-city wards, and 1 Tokyo special-wards group. The clean analysis universe is **1,059 units**.
- **Coverage:** 682 of 926 towns/villages (73.6%) are missing. The covered units account for **8,501,240 vacant dwellings (94.4%)**; the missing municipalities hold **500,360 (5.6%)**.
- **National risk measure:** **895,300 dilapidated "other vacant"** dwellings (23.2% of 3,856,000), of which **715,000 are detached**.
- **Supersedes:** the earlier provisional figures of 1,235 units, 249 covered towns/villages, and 677 missing. Those were based on the table's row count, not the hierarchy.
- **Why it mattered:** the coverage gap is not just a place-count issue; 5.6% of the vacant stock is outside the measured universe. The dossier and memory were updated.

---

## 2026-11-12

### 1. Project state check

- **Action:** Listed the project root and searched for existing files.
- **Result:** Empty project; no existing `research/` notes. This dossier starts from scratch.
- **Why it mattered:** No prior work to preserve or contradict.

### 2. Headline vacancy statistics

- **Query:** 2023 住宅・土地統計調査 空き家 900万 13.8%.
- **Sources:** Statistics Bureau summary PDF; e-Stat table 34-2; secondary summaries.
- **Result:** Confirmed 9.0m vacant / 13.8%; later confirmed exact figures: 9,002,000 vacant / 65,047,000 dwellings / +513,000 from 2018. The brief's 507,000 was the preliminary figure.
- **Why it mattered:** Established the verified headline and the first correction.

### 3. Municipal vacancy table

- **Query:** e-Stat 住宅・土地統計調査 市区町村別 空き家の種類.
- **Source:** e-Stat table 34-2, `https://www.e-stat.go.jp/dbview?sid=0004021631`.
- **Result:** Found the table "空き家の種類(4区分)、腐朽・破損の有無(2区分)、建て方(2区分)、構造(2区分)別空き家数－全国、都道府県、市区町村." The dimension list has 1,283 items; parsing showed 1 national row, 47 prefectures, and 1,235 municipal units.
- **Why it mattered:** Confirmed that municipal 4-category vacancy data and dilapidation data exist.

### 4. Coverage calculation

- **Action:** Compared the 1,235 municipal units with 2024 municipality counts (792 cities, 23 special wards, 171 designated-city wards, 926 towns/villages).
- **Result:** About 249 towns/villages covered; about 677 (73%) missing. About 39% of all 1,741 local governments are absent.
- **Why it mattered:** Identified the biggest scope problem in the brief. This drove decision D1.

### 5. 2018 comparability

- **Query:** 平成30年住宅・土地統計調査 表番号 空き家の種類 4区分 市区町村.
- **Result:** 2018 table 35-2 has the same 4-category / dilapidation / building-type structure. The label was `その他の住宅`.
- **Why it mattered:** 2018–2023 is a comparable core.

### 6. 2013 and 2008 comparability

- **Queries:** 平成25年 / 平成20年 住宅・土地統計調査 市区町村 空き家.
- **Result:** 2013 table 53 is `市区` only; a separate `町村` table must be identified. 2008 table 043-1 uses 5 vacancy categories. Both need a table-by-table audit.
- **Why it mattered:** The four-wave panel is feasible but not automatic. This is open question A1/A2.

### 7. Definitions

- **Source:** Statistics Bureau, *令和5年住宅・土地統計調査 用語の解説*, `https://www.stat.go.jp/data/jyutaku/2023/pdf/yougo.pdf`.
- **Result:** `賃貸・売却用及び二次的住宅を除く空き家` includes long-term absence, demolition-planned homes, storage, unknown use, and genuine abandonment. `廃屋` is not counted as a dwelling. The survey does not produce mesh statistics.
- **Why it mattered:** Corrected the brief's "abandoned, inherited, or unusable" framing and set up the dilapidated-subset measure.

### 8. Sample design

- **Source:** Statistics Bureau survey documentation.
- **Result:** About 200,000 unit districts, ~3.4m dwellings (~5% of stock); target SE 5% for cities, 10% for 15k+ towns.
- **Why it mattered:** Municipal estimates are noisy; uncertainty must be reported.

### 9. Confirmed 2023 details

- **Source:** `https://www.stat.go.jp/data/jyutaku/2023/pdf/kihon_gaiyou.pdf`.
- **Result:** 65,047k dwellings; 9,002k vacant; 13.8%; 3,856k other vacant; 4,436k rental; 326k sale; 384k secondary; 74% of other vacant detached; 1.416m households own a vacant dwelling; 47.5% of owner-owned vacant dwellings are other vacant.
- **Why it mattered:** Provided the exact composition and the detached-house focus.

### 10. 2025 Census

- **Source:** `https://www.stat.go.jp/data/kokusei/2025/kekka/pdf/summary_01.pdf`.
- **Result:** 122,972,528 population; −2.5% from 2020; 57,182k households; +1,477k; 2.10 persons/household; 91.2% of municipal units shrinking; 28.4% shrinking ≥10%.
- **Why it mattered:** Added the demand-side context and the household-growth nuance.

### 11. Policy timeline

- **Source:** MLIT Vacant Houses Act page, `https://www.mlit.go.jp/jutakukentiku/house/jutakukentiku_house_tk3_000035.html`.
- **Result:** 2023 amendment effective 2023-12-13; 2026 amendment effective 2026-09-03; links to the 2023 amendment page and enforcement survey.
- **Why it mattered:** Corrected the brief's policy dates.

### 12. 2023 amendment details

- **Source:** MLIT 2023 amendment page, `https://www.mlit.go.jp/jutakukentiku/house/jutakukentiku_house_tk3_000138.html`.
- **Result:** `管理不全空家等` is a pre-`特定空家` category; guidance → recommendation; support corporations and promotion zones.
- **Why it mattered:** Clarified the legal sequence and the tax trigger.

### 13. Tax treatment

- **Sources:** MLIT tax overview, `https://www.mlit.go.jp/jutakukentiku/house/content/002019834.pdf`; Local Tax Act excerpt, `https://www.mlit.go.jp/jutakukentiku/house/content/002019832.pdf`.
- **Result:** Residential land exception 1/6 (≤200㎡) / 1/3 (>200㎡); removed after a recommendation for `特定空家` or `管理不全`; actual bill may rise less than 6x.
- **Why it mattered:** Corrected the "6x tax" oversimplification.

### 14. Enforcement statistics

- **Source:** MLIT 2025 enforcement survey, `https://www.mlit.go.jp/jutakukentiku/house/content/001984996.pdf`; press release.
- **Result:** 3,211 `管理不全` guidance cases in 185 municipalities; 378 recommendations in 40; 1,541 municipalities with plans; 95 support corporations in 64 municipalities; 4 promotion zones.
- **Why it mattered:** Established the scale of enforcement and its endogeneity.

### 15. 2026 registration obligation

- **Source:** MOJ, `https://www.moj.go.jp/MINJI/minji05_00687.html`.
- **Result:** 2026-04-01; within 2 years; pre-existing changes by 2028-03-31; penalty up to ¥50,000; not a tax.
- **Why it mattered:** Separated registration reform from the vacancy-tax debate.

### 16. Kyoto local tax

- **Source:** Kyoto City, `https://www.city.kyoto.lg.jp/gyozai/page/0000296672.html`.
- **Result:** `非居住住宅利活用促進税` planned for FY2030, one-year delay from FY2029 due to system development; local tax, not national.
- **Why it mattered:** Corrected the "2026 akiya tax" assumption.

### 17. National tax proposal

- **Sources:** Jiji / Nikkei / Asahi coverage, 11 December 2025; DPFP policy page.
- **Result:** DPFP `空室税` bill submitted; aimed at non-residential/investment housing in urban areas; not law.
- **Why it mattered:** Separated proposal from law.

### 18. MLIT transaction API

- **Source:** `https://www.reinfolib.mlit.go.jp/help/apiManual/xit001/`.
- **Result:** XIT001; 2005 Q3+; contract prices 2021+; municipal `city` parameter; free API key; attribution.
- **Why it mattered:** Confirmed the market data are feasible.

### 19. Akiya-bank feasibility

- **Sources:** MLIT national akiya-bank page, `https://www.mlit.go.jp/totikensangyo/const/sosei_const_tk3_000131.html`; participation trend PDF.
- **Result:** 1,155 participating municipalities; 750 listing; 20,089 current listings; ~29,000 cumulative transactions (Oct 2026); portals block automated access (403/CloudFront).
- **Why it mattered:** Decided D6: no scraping; use official aggregates/participation/manual counts.

### 20. Existing work

- **Sources:** Tokyo City University prediction map coverage; Tokyo Foundation 2025; JRI 2025; LIXIL 2020; ResearchSquare 2026; Nikkei/KurashiMap.
- **Result:** A crowded field, but no open, reproducible, multi-wave municipal risk+activation index with uncertainty and market validation.
- **Why it mattered:** Defined the gap and the positioning.

### 21. e-Stat licence

- **Source:** `https://www.e-stat.go.jp/terms-of-use`.
- **Result:** CC BY 4.0-compatible; commercial use allowed; attribution required.
- **Why it mattered:** Confirmed the open-data path.

### 22. Decisions recorded

- **Action:** Recorded D1–D8 in `decisions.md`; user accepted all recommended options.
- **Result:** Scope is now: 1,235-unit universe + 6–8 case studies; map + open data/code + report; risk + activation + capacity lenses; 2008–2023 core; equal weights headline; official akiya-bank aggregates; researchers/policymakers primary.
- **Why it mattered:** The project has a stable identity for Phase 0.

---

## Discrepancies and how they were resolved

| Discrepancy | Sources | Resolution |
|---|---|---|
| 507k vs 513k five-year vacancy increase | Preliminary vs confirmed 2023 survey | Use **513k** (confirmed). |
| 65.02m vs 65.047m dwellings | Brief vs confirmed survey | Use **65,047,000**. |
| "Other vacant" = abandoned | Brief vs survey definition | Use the survey definition; call it **residual/other vacant**, not abandoned; use **dilapidated other vacant** as the risk proxy. |
| 9.0m vacant vs 8.995m/9.002m | Preliminary vs confirmed | Use **9,002,000**. |
| 2023 Act "designation" | Brief vs statute/guidance | Use **determination + guidance/recommendation**; the tax trigger is the **勧告**. |
| "6x tax" | Media shorthand vs tax law | Say **taxable value up to 6x**; actual bill may rise less. |
| 2026 "akiya tax" | Media/policy debate vs law | No national akiya tax; DPFP bill not law; Kyoto local tax FY2030; registration obligation separate. |
| Akiya-bank coverage | Portal marketing vs actual data | 1,155 participants, 750 listing, 20,089 listings; not a vacancy census. |

---

## Next log entry

Phase 0: download and parse the 2023 table; reconcile 2018/2013/2008; build the code crosswalk; pilot Tokyo/Nagano/Kochi; test akiya-bank participation data.
