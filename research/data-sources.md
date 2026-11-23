# Data Sources: Inventory, Coverage, Access, and Feasibility

**Last updated:** 2026-11-12
**Purpose:** A working inventory of every dataset the project may use, with coverage, access method, licence, and a feasibility verdict. This is the file to update first when a new source is found.

---

## 1. Summary table

| Source | What it gives | Geography / frequency | Access and licence | Verdict |
|---|---|---|---|---|
| **Housing and Land Survey** (住宅・土地統計調査) | Vacancy by 4 categories, dilapidation, building type, structure; municipal tables | 2008, 2013, 2018, 2023; 2023 covers 1,059 clean municipal units (1,235 reporting rows); 5-year waves | e-Stat; CC BY 4.0-compatible; attribution | **Core**, but coverage- and sampling-limited. |
| **2025 Census** (国勢調査) | Population, households, age structure, dwelling tenure | Municipal; 2000–2025; 2025 basic tabulation published 2026-09-29 | e-Stat; CC BY 4.0-compatible | **Core demand data.** |
| **IPSS municipal projections** | Population by age, 2020–2050 | Municipal; 5-year intervals | Free; attribution | **Core pressure variable.** |
| **MLIT Real Estate Information Library API** | Transaction prices, contract prices, land-price points | Transactions 2005 Q3+; contract prices 2021+; quarterly | Free API key; attribution; key must not be shared | **Core market data**, thin in rural areas. |
| **Land price data** (地価公示 / 都道府県地価調査) | Point-level land prices | Annual; municipal aggregation possible | MLIT / prefectures; attribution | **Good but sparse.** |
| **Housing starts / demolitions** | Completions; demolition proxy | Municipal starts; demolition data incomplete | e-Stat / MLIT | **Partial.** Starts good; demolitions residual. |
| **Local finance** (地方財政状況調査) | Fiscal strength index, debt, tax base | Municipal; annual | e-Stat / 総務省; attribution | **Good** for capacity overlay. |
| **Boundaries / accessibility** | Municipal boundaries, rail stations, passengers, DID | National; periodic | 国土数値情報 / GSI; commercial use permitted | **Good.** |
| **Akiya banks** | Participation, listing counts, listed properties | 1,155 participants; 750 listing; 20,089 current listings (Oct 2026) | Official aggregate PDFs and participation lists; portals block automation | **Limited; no scraping.** |
| **Policy designations** | 管理不全 / 特定空家 measures | Prefecture-level only; no municipal list | MLIT PDFs | **Context only.** |
| **Mesh vacancy** | Vacancy at 1 km mesh | **Not produced** by the survey | — | **Not feasible** from national data. |

---

## 2. Housing and Land Survey (the core vacancy source)

### 2.1 Tables to use

| Wave | Table | Title | Notes |
|---|---|---|---|
| 2023 | **34-2** | 空き家の種類(4区分)、腐朽・破損の有無(2区分)、建て方(2区分)、構造(2区分)別空き家数－全国、都道府県、市区町村 | The core table. Includes the 4 vacancy categories, dilapidation, building type, and structure. |
| 2018 | **35-2** | Same structure as 2023 | Directly comparable conceptually, but the Excel layout differs: 11 header rows, 17 columns, and count columns ordered **total, secondary, rental, sale, other**. Label was `その他の住宅`. Parsed; 1,086 clean municipal units. |
| 2013 | **53** | 空き家の種類(4区分)、腐朽・破損の有無(2区分)、建て方(2区分)、構造(2区分)別空き家数－市区 | The API table is **市区 only**; no 町村 table in the API. City/ward context only. |
| 2008 | **043-2** | 空き家の種類(4区分)、腐朽・破損の有無(2区分)、建て方(2区分)、構造(2区分)別空き家数－市区 | The API table is **市区 only**; five-category table 043-1 is prefectural. City/ward context only. |

**Action for Phase 0:** download each table, compare category labels and totals, and build a crosswalk. Do not assume the 2013 and 2008 tables are directly comparable.

### 2.2 Coverage: the critical limitation

The 2023 table's geographic dimension contains **1,283 items**:

- 1 national row;
- 47 prefectures;
- **1,235 municipal reporting units**.

The 1,235 rows are **not a clean municipality count**. They include:

- **792 cities** (20 designated + 772 non-designated);
- **23 special wards** (Tokyo);
- **244 towns/villages**;
- **175 designated-city wards**;
- **1 Tokyo special-wards group** (`特別区部`).

The designated-city wards and the special-wards group duplicate the city-level rows. To avoid double counting, the analysis uses **1,059 clean municipal units**:

> 792 cities + 23 special wards + 244 towns/villages = **1,059**.

Japan has **926 towns/villages** (743 towns + 183 villages). Therefore **682 towns/villages (73.6%) are missing** from the table.

**Coverage of the vacancy stock:** the 1,059 clean units account for **8,501,240 vacant dwellings**, or **94.4%** of the national **9,001,600**. The **500,360 vacant dwellings (5.6%)** in the missing municipalities are not separately reported. The gap is larger for the risk measure: the missing municipalities hold **327,880 “other vacant” (8.5%)** and **89,240 dilapidated “other vacant” (10.0%)**. This is a substantive gap, not just a place-count issue.

### 2.2a Total-dwelling tables

- **2023 table 1-2-1:** `statsDataId=0004021421`; 15,396 rows; 1,283 areas.
- **2018 table 1-2-1:** `statsDataId=0003355290`; 15,720 rows; 1,310 areas.
- **Validation:** total dwellings 65,046,700 (2023) / 62,407,400 (2018); vacant 9,001,600 / 8,488,600; other vacant 3,856,000 / 3,487,200. Vacancy counts match tables 34-2 / 35-2 with **0 mismatches**; total-dwelling coverage is **1,059/1,059** and **1,086/1,086**.
- **Category-code trap:** 2023 `221` = other vacant; 2018 `221` = secondary. Map by year-specific code, not position.
- **Coverage of national totals (2023 units):** total dwellings 96.6%; vacant 94.4%; other vacant 91.5%; dilapidated other vacant **90.0%**.

**Coverage changed between waves.** 2018 has **1,086 clean municipal units** (271 towns/villages) and covers **8,077,270 vacant dwellings (95.2%)**; 2023 has **1,059** (244 towns/villages) and covers **8,501,240 (94.4%)**. The 27-unit difference is **threshold-driven, not merger-driven**: the e-Stat merger history shows no municipal mergers in 2018–2023; 29 towns/villages dropped out and 2 entered. The balanced 2018–2023 panel is **1,057 units**.

**What to do:**
- Define the national index universe as the **1,059 clean municipal units**.
- Treat the **682 missing towns/villages** as a separate case-study/coverage-extension track.
- Do not present the map as "all Japan."
- Report the **5.6% uncovered vacancy** explicitly; do not imply the covered units are the whole country.

### 2.3 Sample design and error

- The 2023 survey sampled about **200,000 unit districts** and about **3.4 million dwellings** — roughly **5% of the dwelling stock**.
- Target standard error: **5% for cities**, **10% for towns/villages with 15,000+ population**.
- The survey is a stratified two-stage sample; municipal figures are **estimates**, not exact counts.
- Small municipalities have small samples, so vacancy rates and five-year changes are noisy. Rankings of small places are unstable.

**What to do:** report uncertainty; use simulation and/or empirical-Bayes smoothing; avoid overinterpreting small rank differences.

### 2.4 Definitions and caveats

- `空き家` excludes `一時現在者のみ` and `建築中`.
- `賃貸・売却用及び二次的住宅を除く空き家` includes long-term absence, demolition-planned homes, storage, unknown use, and genuine abandonment.
- `廃屋` is **not** counted as a dwelling; the worst blight is outside the survey.
- The 2023 survey renamed the category from `その他の住宅`; the definition is essentially the same.
- The survey **does not produce mesh statistics**.

### 2.5 Access

- **e-Stat file downloads:** Excel/CSV, no login required for standard file downloads.
- **e-Stat API:** requires a free application ID; useful for reproducible extraction.
- **Licence:** e-Stat content is CC BY 4.0-compatible; attribution required; commercial use allowed.
- **Recommended access:** e-Stat API for the panel; preserve the raw files and the query parameters.

---

## 3. Census 2025

- **What:** population, households, age structure, dwelling tenure, employment status (later releases).
- **Geography:** municipal; 2000, 2005, 2010, 2015, 2020, 2025.
- **Timing:** 2025 population census basic tabulation published **29 September 2026**; some tables later.
- **API tables used:**
  - table 1-2, `statsDataId=0004050417`: 2020 population, 2025/2020 households, area, density.
  - table 1-1, `statsDataId=0004050397`: 2025 population.
  - 1,961 areas (national, prefectures, municipalities/wards).
- **Use:** denominator variables, demand pressure, household change, ageing.
- **Caveat:** census population and housing-survey households are not identical concepts; do not mix them without checking.
- **Discrepancy:** the API table’s national 2025 population is **123,049,524**, while the summary PDF headline is **122,972,528** (difference **76,996**). The API table is internally consistent with its 2020 baseline and five-year change. Use the API table for municipal joins; cite the headline separately and note the difference. Cause not yet established.

**Verdict:** core.

---

## 4. IPSS municipal projections

- **What:** population by age, 2020–2050, 5-year intervals.
- **Geography:** municipal.
- **Use:** forward pressure; not a forecast of vacancy.
- **Caveat:** projections assume migration and fertility trends; they are scenarios, not predictions. Use them as a pressure indicator, not a dependent variable.

**Verdict:** core pressure variable.

---

## 5. MLIT Real Estate Information Library API

- **Endpoint:** `XIT001` for transaction/contract prices; land-price endpoints for official land prices.
- **Coverage:** transaction prices from **2005 Q3**; contract prices from **2021**; quarterly; municipal `city` parameter.
- **Fields:** price, floor area, land area, building year, structure, use, address (masked), nearest station, etc.
- **Access:** free API key via application; key must not be shared; attribution required.
- **Licence:** provided information may be used freely with attribution; check the terms for redistribution of processed data.
- **Caveats:**
  - Self-reported/administrative records, not a census of transactions.
  - Rural municipalities may have very few records.
  - Land and land+building transactions must not be mixed.
  - Contract prices and transaction prices are different series.
- **Use:** municipal median price, price growth, transaction count/liquidity, price dispersion.

**Verdict:** core market data, with a rural-coverage caveat. Pilot three prefectures before committing.

---

## 6. Land price data

- **Sources:** 地価公示 (official land prices, 1 January) and 都道府県地価調査 (prefectural land prices, 1 July).
- **Geography:** point-level; aggregate to municipality.
- **Use:** land-price level and trend; more consistent than transaction prices, but sparse in rural areas.
- **Caveats:** standard sites are not a random sample; municipal medians can be based on very few points; use 3-year pooling where needed.

**Verdict:** good, with a thin-cell flag.

---

## 7. Housing starts and demolitions

- **Starts:** 建築着工統計, municipal; e-Stat.
- **Demolitions:** 建築物滅失統計調査 exists, but the JRI study notes that its volume is smaller than the residual estimate from stock + completions, so it does not cover all demolitions.
- **Recommended approach:** use starts directly; estimate demolitions residually:
  `demolition_proxy = stock_t-1 + completions_t − stock_t`
  and label it a proxy. Do not present it as an exact demolition count.
- **Use:** supply inertia, stock growth, replacement rate.

**Verdict:** starts good; demolitions partial.

---

## 8. Local finance

- **Source:** 地方財政状況調査 (e-Stat / 総務省), 市町村別決算状況調; **SSDSE table D 行政基盤** (`statsDataId=0000020204`), indicator `D2201_財政力指数（市町村財政）`.
- **What:** fiscal strength index, debt, tax base, expenditure.
- **Geography:** municipal; annual.
- **Latest available in SSDSE:** **FY2022** (`cdTime=2022100000`); FY2023/2024 return no data in this table.
- **Coverage:** 1,913 areas; **1,036 of 1,059** analysis units (97.8%). The 23 Tokyo special wards have no index because the index is municipal, not ward-level.
- **Use:** response-capacity overlay; not a risk outcome.
- **Caveat:** fiscal years and municipal boundaries must be aligned with the survey waves. The FY2022 index lags the 2023 vacancy survey; label the lag.

**Verdict:** good, with a special-ward gap and a one-year lag.

---

## 9. Boundaries and accessibility

- **Boundaries:** 国土数値情報 N03 (administrative areas), GSI; municipal codes; commercial use permitted.
- **Rail:** 国土数値情報 N02 (railway lines/stations); station passenger data (S12) where available.
- **Accessibility metrics:** station count per 10,000 population; distance from the municipal population centroid to the nearest station; DID share.
- **Travel time:** requires a routing engine and OSM/MLIT road data; defer to Phase 2 unless a precomputed dataset is available.
- **OSM/Overpass:** ODbL 1.0; attribution and share-alike for derived databases; rate-limited. Prefer 国土数値情報 for the core index to avoid ODbL complications.
- **Use:** activation-potential lens.

**Verdict:** good for simple metrics; travel time is a Phase 2 enhancement.

---

## 10. Akiya banks

- **National portal:** two operators, LIFULL HOME'S and AtHome, under the MLIT "全国版空き家・空き地バンク."
- **Scale (October 2026):**
  - **1,155 participating municipalities** (65.5% of municipalities);
  - **750 municipalities currently listing**;
  - **20,089 current listings** (duplicates across the two operators);
  - **~29,000 cumulative transactions**.
- **Access:** official aggregate PDFs and participation lists are public. The portal pages block automated access (403/CloudFront); robots/terms must be respected.
- **What it measures:** marketed supply with owner consent in participating municipalities — **not** the vacant stock.
- **Use:**
  - participation dummy (municipal);
  - aggregate listing trend (national/time series);
  - manual listing counts in 6–8 case-study municipalities;
  - request aggregate counts from operators/municipalities if needed.
- **Do not:** scrape listings; treat listings as a census of vacancy; compare raw counts across municipalities without controlling for population/program participation.

**Verdict:** limited but usable as a selected signal. No scraping.

---

## 11. Policy designations

- **Published:** MLIT's annual enforcement survey, prefecture-level tables; counts of municipalities with guidance/recommendations; no municipal list.
- **Key numbers (as of 31 March 2025):** 3,211 `管理不全` guidance cases in 185 municipalities; 378 recommendations in 40 municipalities; 42,768 cumulative `特定空家` advice/guidance cases in 875 municipalities.
- **Use:** prefecture-level context; case studies; not a municipal validation variable.
- **Caveat:** designations reflect administrative capacity and political will; they are endogenous.

**Verdict:** context only.

---

## 12. Coverage-extension candidates (for the 682 missing towns/villages)

These are **not** part of the national index in Phase 1; they are options for the case-study/coverage-extension track.

| Option | What it gives | Caveat |
|---|---|---|
| Municipal vacant-house surveys | Local counts, sometimes address-level | Inconsistent definitions, years, and quality; need manual collection. |
| Fixed-asset tax records (家屋台帳) | Dwelling/building counts, floor area | Not a vacancy measure; may allow a housing-surplus proxy. |
| 住民基本台帳 | Population/households for all municipalities | Does not measure vacancy. |
| Tokyo City University prediction map | Predicted vacancy rates for all municipalities | Proprietary/non-commercial; single outcome; not reproducible; use only as a reference, not as input. |
| Microdata application | Survey microdata for research | Application/approval process; disclosure control; not a quick fix. |

**Recommendation:** use 6–8 case studies with local surveys and documents; do not model all 682 municipalities in Phase 1.

---

## 13. Licence matrix

| Source | Licence / terms | Commercial use | Attribution | Redistribution | Notes |
|---|---|---|---|---|---|
| e-Stat | CC BY 4.0-compatible | Yes | Required | Yes | Include “processed by” note. |
| MLIT Real Estate Library | Free use with attribution; API terms | Yes | Required | Check terms for processed data | Do not share API key. |
| 国土数値情報 / GSI | Government standard terms; commercial use permitted | Yes | Required | Yes | Check individual dataset terms. |
| OSM / Overpass | ODbL 1.0 | Yes | Required | Share-alike for derived databases | Isolate OSM-derived layers if possible. |
| Akiya-bank portals | Operator terms; automated access blocked | Unclear | — | No | Do not scrape; use official aggregates/lists. |
| MLIT policy PDFs | Government standard terms | Yes | Required | Yes | — |

---

## 14. Access plan for Phase 0

1. **e-Stat:** register for a free API application ID; download 2023 table 34-2, 2018 table 35-2, 2013 table 53, and 2008 table 043-1; preserve raw files and query parameters.
2. **MLIT:** apply for a Real Estate Library API key; test `XIT001` for Tokyo, Nagano, and Kochi; check record counts and rural coverage.
3. **Census:** download 2000–2025 municipal population/household tables; align codes.
4. **IPSS:** download the 2023 municipal projections.
5. **Local finance:** download the municipal fiscal-strength tables for the relevant years.
6. **Boundaries/accessibility:** download N03 and N02; compute station density/distance.
7. **Akiya banks:** compile the official participation lists; extract the aggregate trend PDF; select case-study municipalities for manual counts.
8. **Policy:** download the MLIT enforcement survey and the 2023/2026 amendment pages.

---

## 15. Do-not-use list

- **Do not scrape akiya-bank listings.** The portals block automated access and the terms do not support it. Use official aggregates, participation lists, and manual case-study counts.
- **Do not treat policy designations as an unbiased risk measure.** They reflect enforcement capacity.
- **Do not use mesh vacancy data.** The survey does not produce it.
- **Do not rank all 1,741 municipalities.** The measured universe is 1,059 clean municipal units.
- **Do not mix transaction prices and contract prices.** They are different series.
- **Do not present the 6x tax-base change as a 6x tax bill.** Burden adjustment and municipal rules matter.
- **Do not describe the DPFP `空室税` bill or the Kyoto tax as a national akiya tax.**

---

## Sources

- e-Stat, 2023 table 34-2: https://www.e-stat.go.jp/dbview?sid=0004021631 (accessed 2026-11-12).
- e-Stat, 2018 table 35-2 and 2013 table 53 (search via e-Stat; table numbers confirmed in the 2018/2013 table lists).
- Statistics Bureau, *令和5年住宅・土地統計調査 調査の結果*: https://www.stat.go.jp/data/jyutaku/2023/tyousake.html (accessed 2026-11-12).
- Statistics Bureau, *令和5年住宅・土地統計調査 用語の解説*: https://www.stat.go.jp/data/jyutaku/2023/pdf/yougo.pdf (accessed 2026-11-12).
- Statistics Bureau, *令和7年国勢調査 人口等基本集計*: https://www.stat.go.jp/data/kokusei/2025/kekka/pdf/summary_01.pdf (accessed 2026-11-12).
- IPSS, *日本の地域別将来推計人口 令和5(2023)年推計*: https://www.ipss.go.jp/pp-shicyoson/j/shicyoson23/t-page.asp (accessed 2026-11-12).
- MLIT, *不動産情報ライブラリ API 操作説明 XIT001*: https://www.reinfolib.mlit.go.jp/help/apiManual/xit001/ (accessed 2026-11-12).
- MLIT, *不動産情報ライブラリ利用規約*: https://www.reinfolib.mlit.go.jp/help/termsOfUse/ (accessed 2026-11-12).
- MLIT, *全国版空き家・空き地バンク*: https://www.mlit.go.jp/totikensangyo/const/sosei_const_tk3_000131.html (accessed 2026-11-12).
- MLIT, *全国版空き家・空き地バンク 参画自治体数・物件掲載件数推移*: https://www.mlit.go.jp/totikensangyo/const/content/002045627.pdf (accessed 2026-11-12).
- MLIT, *空家等対策の推進に関する特別措置法の施行状況等について（令和7年3月31日時点）*: https://www.mlit.go.jp/jutakukentiku/house/content/001984996.pdf (accessed 2026-11-12).
- e-Stat, *利用規約*: https://www.e-stat.go.jp/terms-of-use (accessed 2026-11-12).
- 国土数値情報: https://nlftp.mlit.go.jp/ksj/ (accessed 2026-11-12).
- JRI, *2040年代の全国・都道府県別 空き家数・空き家率の推計*: https://www.jri.co.jp/file/report/researchfocus/pdf/15673.pdf (accessed 2026-11-12).
