# The Empty House Atlas — Research Dossier

**Status:** Phase 0 in progress. The vacancy panel, public map v1, 2018/2023 market panel, and akiya-bank national/prefecture aggregates are built. Next: akiya-bank municipal participation, case studies, and go/no-go.
**Last updated:** 2026-11-27
**Project root:** `C:\Users\Gilbert\Documents\Projects\akiya-risk-index`

---

## What this project is

A reproducible, data-driven study of housing vacancy in Japan at the municipal level. The core intent is to understand **where structural vacancy is accumulating**, **what distinguishes places with different trajectories**, and **whether local housing markets already reflect the risk**.

The working title is *The Empty House Atlas*. The primary product is planned as an interactive map plus open data/code and a short report, aimed at researchers and policymakers. A buyer-facing summary may be derived later, but it is not the core.

This is **not**:
- a property-level prediction tool;
- a causal evaluation of the 2023 Vacant Houses Act;
- commercial valuation or investment advice;
- a claim that Japan has a national "akiya tax" (it does not).

---

## Decisions already made (2026-11-12)

The user accepted the recommended options:

| ID | Decision | Choice |
|---|---|---|
| D1 | Unit and coverage | **1,059 clean municipal units** (792 cities + 23 special wards + 244 towns/villages) **+ 6–8 small-municipality case studies.** The 1,235 table rows include duplicate city/ward levels; the national index does not pretend to rank all 1,741 local governments. |
| D2 | Core deliverable | **Interactive map + open data/code + short report/methodology.** |
| D3 | Second analytical lens | **Both activation potential and response capacity**, with risk as the core. |
| D4 | Time window | **2018–2023 core vacancy panel** (balanced 1,057 units), with **2013/2008 city/ward context**; demography 2000–2025; market data 2005–2026. |
| D5 | Index weights | **Equal weights headline**, with PCA and policy-informed weights as sensitivity checks. |
| D6 | Akiya-bank method | **Official aggregates + participation lists + manual case-study counts; no scraping.** |
| D7 | Case studies | **6–8 municipalities**, selected after Phase 0. |
| D8 | Primary audience | **Researchers and policymakers**, with a buyer-facing summary as a derivative. |

The user comes from an IT background with no housing or real-estate experience and prefers the safer option when a trade-off is uncertain. This dossier therefore defines housing terms, separates fact from inference, and avoids overclaiming.

See `decisions.md` for evidence and rationale.

---

## Read this first (suggested order)

1. **`summary.md`** — the one-page executive summary: what was verified, what changed, and what comes next.
2. **`background.md`** — the verified numbers, what "vacancy" actually means, and why the headline is misleading.
3. **`policy.md`** — what is law, what is implementation guidance, and what is only a proposal.
4. **`data-sources.md`** — what data exists, what it covers, how to get it, and what it cannot do.
5. **`existing-work.md`** — what has already been built or studied, and where the genuine gap is.
6. **`findings.md`** — the synthesised conclusions so far, labelled fact / inference / hypothesis.
7. **`question-and-scope.md`** — the refined question, scope, objectives, and exclusions.
8. **`plan.md`** — the Phase 0/1 work plan, milestones, data schema, and risks.
9. **`open-questions.md`** — what is still unresolved.
10. **`decisions.md`** — material changes to the brief and the reasons.
11. **`log.md`** — the chronological research trail.
12. **`glossary.md`** — plain-language definitions of Japanese housing and policy terms.
13. **`raw/source-notes.md`** — key source excerpts and exact references.

---

## Folder map

| Path | Contents |
|---|---|
| `README.md` | This index and status page. |
| `summary.md` | One-page executive summary: verified, unverified, refined scope, plan, decisions. |
| `background.md` | Verified background, definitions, headline statistics, measurement caveats. |
| `policy.md` | Policy timeline 2014–2026; law vs guidance vs proposal; tax treatment. |
| `data-sources.md` | Source inventory, coverage, access, licences, feasibility verdicts. |
| `existing-work.md` | Government, academic, and data-journalism prior work; gap statement. |
| `findings.md` | Synthesised findings, explicitly labelled. |
| `question-and-scope.md` | Refined primary/secondary questions, scope, objectives, exclusions. |
| `plan.md` | Phase 0/1 plan: milestones, data schema, risks, go/no-go criteria. |
| `open-questions.md` | Unresolved questions and next steps. |
| `decisions.md` | Decision log with date, old approach, new approach, evidence, rationale. |
| `log.md` | Chronological research log: date, query/source, why it mattered. |
| `glossary.md` | Plain-language glossary for a non-housing reader. |
| `raw/source-notes.md` | Raw excerpts and exact source details. |

---

## Evidence conventions

Every substantive claim should be labelled:

- **Fact** — directly supported by a primary source (statute, official statistic, ministry page).
- **Inference** — a calculation or interpretation from facts; the reasoning is stated.
- **Hypothesis** — a testable proposition not yet established.

Where sources conflict, record both and explain the discrepancy. Do not convert a correlation into a causal claim.

---

## Key findings at a glance

- Japan had **9.002 million vacant dwellings in 2023 (13.8% of the stock)**, up **513,000** from 2018. The broad "other vacant" category is **3.856 million (5.9% of all dwellings)**.
- "Other vacant" is **not** synonymous with abandoned: it includes long-term absence, homes awaiting demolition, and unknown-use cases, and it **excludes `廃屋`** (ruined structures). The better risk measure is **dilapidated "other vacant"**: **895,300** dwellings nationally (23.2% of "other vacant"), of which **715,000 are detached**.
- The 2023 table has **1,235 municipal reporting rows**, but they double-count designated cities and their wards. The clean analysis universe is **1,059 municipal units** (792 cities + 23 special wards + 244 towns/villages). **682 of 926 towns/villages (73.6%) are missing**, and they hold **500,360 vacant dwellings (5.6% of the national total)**. The covered units account for **94.4%** of the vacant stock, but only **90.0%** of the dilapidated “other vacant” stock.
- **Proper vacancy rates are now available** for **1,059/1,059** 2023 units and **1,086/1,086** 2018 units. The highest 2023 dilapidated “other vacant” rates are 川崎町 (12.25%), 新上五島町 (11.89%), 平戸市 (9.29%), 垂水市 (9.29%), and 室戸市 (9.11%). The 2018–2023 balanced panel is **1,057 units**.
- **Accessibility v0 is built** from KSJ N03/N02/S12: **9,007 rail facilities** (8,399 heavy-rail stations, 608 tram-only stops), with **7,479 heavy-rail stations** in the 1,059-unit panel. **126 units (11.9%) have no heavy-rail station**. Station density correlates **+0.701** with population density and **−0.447** with the 2023 dilapidated “other vacant” rate, but only **−0.018** with its 2018–2023 change. Passenger data cover **87.4%** of heavy-rail stations and are secondary.
- The 2023 Act (effective **2023-12-13**) created **`管理不全空家等`**, a pre-`特定空家` category: **guidance → recommendation → residential-land tax exception removed**. The tax consequence is not automatic at the first determination, and the actual bill may rise by less than the often-quoted "6x."
- The **2026-04-01 address-change registration obligation** is a registration rule, **not a tax**. The DPFP's national **"空室税"** bill is **not law**. Kyoto's local non-residential housing tax is now planned for **FY2030**.
- Akiya-bank listings are a **tiny, selected signal**: about **20,089 current listings** against 9.0 million vacant dwellings, in 750 of 1,155 participating municipalities. They cannot validate a national vacancy index on their own.
- The genuine gap is **not another vacancy map**. It is an **open, reproducible, multi-wave municipal panel** that separates current blight from forward pressure, reports uncertainty, and tests whether markets already price the risk.

---

## Next milestone

**Phase 0 go/no-go:** vacancy, total dwellings, proper rates, the 2018–2023 crosswalk, 2013/2008 context, 2025 Census, FY2022 fiscal capacity, accessibility v0, the public map, the 2018/2023 market panel, and the akiya-bank national/prefecture aggregates are built. The municipal akiya-bank list is blocked on the operator pages. Next: **finish Stage D**, then **Stage E — case studies**, and **Stage F — go/no-go**.

See `plan.md` for the full Phase 0/1 plan, milestones, data schema, risks, and go/no-go criteria.
