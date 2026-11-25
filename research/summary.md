# Session Summary: What Was Verified, What Changed, and What Comes Next

**Date:** 2026-11-23
**Purpose:** A one-page executive summary of the research dossier. Read this after `README.md`; details are in the linked files.

---

## 1. What was verified

- **2023 vacancy headline:** **9,002,000 vacant dwellings / 65,047,000 dwellings / 13.8%**, up **513,000** from 2018 (confirmed figures, not the preliminary 507,000). "Other vacant" = **3,856,000 (5.9%)**.
- **Composition:** 4,436,000 rental vacancies, 326,000 for sale, 384,000 secondary residences, 3,856,000 "other vacant." **74% of "other vacant" is detached housing.**
- **Dilapidated "other vacant": 895,300** (23.2% of "other vacant"), of which **715,000 are detached**. This is the national baseline for the headline risk measure.
- **2018 → 2023:** broad "other vacant" rose **+10.6%**, but dilapidated "other vacant" fell **−11.0%** (1,006,000 → 895,300). Part of the decline is likely `廃屋` attrition — the worst structures leaving the survey — not improvement. Do not treat the measured trend as monotonic risk.
- **Definition:** "Other vacant" includes long-term absence, demolition-planned homes, storage, unknown use, and genuine abandonment. It **excludes `廃屋`** (ruined structures). It is not a synonym for "abandoned."
- **Coverage:** The 2023 table has **1,235 municipal reporting rows**, but they double-count designated cities and their wards. The clean analysis universe is **1,059 municipal units** (792 cities + 23 special wards + 244 towns/villages). **682 of 926 towns/villages (73.6%) are missing**, and they hold **500,360 vacant dwellings (5.6% of the national total)**. The covered units account for **94.4%** of the vacant stock, but only **90.0%** of the dilapidated “other vacant” stock — the risk measure has a larger coverage gap.
- **Proper rates available:** total dwellings now cover **1,059/1,059** 2023 units and **1,086/1,086** 2018 units. The highest 2023 dilapidated “other vacant” rates are 川崎町 (12.25%), 新上五島町 (11.89%), 平戸市 (9.29%), 垂水市 (9.29%), and 室戸市 (9.11%). The full 2018–2023 panel has **1,057 balanced units**.
- **2018–2023 crosswalk:** the coverage change is **threshold-driven, not merger-driven** (no municipal mergers in the period). The balanced panel is **1,057 units** (1,056 matched + 1 name change).
- **Accessibility v0:** **9,007 rail facilities** in 2023 (8,399 heavy-rail stations, 608 tram-only stops). The 1,059-unit panel contains **7,479 heavy-rail stations**; **126 units (11.9%) have none**. Station density correlates **+0.701** with population density and **−0.447** with the 2023 dilapidated “other vacant” rate, but only **−0.018** with its 2018–2023 change. Treat this as a descriptive activation variable, not a causal effect.
- **Demography:** The 2025 Census shows **122.97m people**, down **2.5%** from 2020; **57.18m households**, up **1.477m**; **91.2%** of municipal units lost population.
- **Policy:** The 2023 Act took effect **2023-12-13** and created `管理不全空家等` (guidance → recommendation → tax exception removed). The **2026-04-01 address-change registration** is a registration rule, not a tax. There is **no national akiya tax**; the DPFP `空室税` bill is not law; Kyoto's local tax is planned for **FY2030**.
- **Akiya banks:** **1,155 participating municipalities**, **750 currently listing**, **20,089 current listings**, ~29,000 cumulative transactions (Oct 2026). Listings are ~0.2% of the vacant stock; they are a selected signal, not a vacancy census.
- **Existing work:** National maps, prefectural forecasts, academic driver studies, and metro spatial models exist. The gap is an open, reproducible, multi-wave municipal risk/activation panel with uncertainty and market validation.

---

## 2. What could not be verified

- Exact **municipal-level** `管理不全`/`特定空家` designation counts (published data are prefecture-level).
- Whether the **2013 and 2008** municipal tables are directly comparable to 2018/2023 in coverage and category definitions.
- Whether **rural transaction/land-price** coverage is sufficient for an activation index.
- Whether akiya-bank **municipal listing counts** can be obtained without scraping.
- The detailed legal effect of the **September 2026 amendment** beyond the primary MLIT page (partly based on a law-firm commentary).
- Exact **tax-assessment timing** after a `管理不全` recommendation.
- Whether the **2025 Census municipal tables** are complete for all variables.
- How reliable the **`腐朽・破損` cells** are at municipal level.

These are tracked in `open-questions.md`.

---

## 3. Refined question and scope

**Primary question:**

> Which Japanese municipalities face persistent structural vacancy risk, and is that risk already reflected in local housing markets — or is it accumulating in places where prices and transactions have not yet adjusted?

**Scope:** **1,059 clean municipal units** (from 1,235 reporting rows; 15,000+ universe) + 6–8 small-municipality case studies; vacancy **2018–2023 core** (balanced 1,057 units), with **2013/2008 city/ward context** and 2003 context; demography 2000–2025; market data 2005–2026; policy 2014–2026. No property-level prediction, no causal evaluation of the 2023 Act, no investment advice.

**Deliverable:** interactive map + open data/code + short report/methodology, aimed at researchers and policymakers.

See `question-and-scope.md`.

---

## 4. Proposed plan

- **Phase 0 (weeks 1–3):** source/licence audit; 2023 table parse; 2018/2013/2008 reconciliation; municipal-code crosswalk; pilot Tokyo/Nagano/Kochi; akiya-bank feasibility; case-study shortlist; go/no-go memo.
- **Phase 1a (weeks 4–6):** build the harmonised panel; QA.
- **Phase 1b (weeks 7–8):** risk, activation, and capacity indices; equal/PCA/policy weights; uncertainty.
- **Phase 1c (weeks 9–10):** market-lag tests; akiya-bank/policy validation; archetypes; case studies.
- **Phase 1d (weeks 10–11):** map, report, open data/code, methodology.

**Go/no-go:** ≥90% join rate across vacancy/census/fiscal; ≥60% usable market coverage or a defensible pooling strategy; 2018–2023 clean; akiya-bank data compilable without scraping.

See `plan.md`.

---

## 5. Decisions needed / already made

The user accepted all recommended options on 2026-11-12:

| ID | Decision | Choice |
|---|---|---|
| D1 | Unit and coverage | 1,059-unit clean universe + 6–8 case studies |
| D2 | Deliverable | Map + open data/code + report |
| D3 | Second lens | Activation + capacity, risk core |
| D4 | Time window | 2018–2023 core; 2013/2008 city/ward context |
| D5 | Weights | Equal headline + PCA/policy sensitivity |
| D6 | Akiya banks | Official aggregates/participation + manual counts; no scraping |
| D7 | Case studies | 6–8, selected after Phase 0 |
| D8 | Audience | Researchers/policymakers; buyer summary derivative |

Remaining decisions are reversible/methodological and can be made during Phase 0/1 (see `decisions.md`).

---

## 6. What I would change about the brief

1. **Reframe "other vacant"** — it is a residual category, not "abandoned"; use **dilapidated "other vacant"** as the headline risk measure.
2. **Confront coverage bias** — the national index cannot honestly cover all 1,741 municipalities; restrict it to **1,059 clean municipal units** and treat the **682 missing towns/villages** separately. The missing places hold **500,360 vacant dwellings (5.6%)**.
3. **Use 2018–2023 as the core panel**, with 2013/2008 as city/ward context — the API's 2013/2008 four-category tables are 市区 only, so a four-wave municipal panel would lose all towns/villages.
4. **Update the policy timeline** — 2023 Act effective Dec 2023; Sept 2026 amendment; 2026 registration; Kyoto tax FY2030; DPFP bill not law; no national akiya tax.
5. **Replace "opportunity" with "activation potential"** — more defensible for a policy/research audience and avoids investment advice.
6. **Treat akiya banks and designations as selected/endogenous signals** — they are not unbiased validation.
7. **Make uncertainty a first-class output** — municipal estimates are noisy; rankings need error bands.
8. **Do not promise mesh-level vacancy case studies** — the survey does not produce mesh data.
9. **Use two lenses, not one composite** — risk + activation, with fiscal capacity as an overlay.
10. **The "cheap but recovering" archetype is conditional** — only where price/transaction data are sufficient; otherwise say "insufficient evidence."

---

## 7. Next step

Phase 0 is well advanced: the vacancy panel, total dwellings, crosswalk, 2025 Census, fiscal capacity, accessibility v0, and the public site are built. The next step is **Stage A — 2013/2008 city/ward context**. After that: **Stage B — public map v1**, **Stage C — market data**, **Stage D — akiya-bank**, **Stage E — case studies**, and **Stage F — go/no-go**.
