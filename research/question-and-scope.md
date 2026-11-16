# Refined Research Question and Scope

**Last updated:** 2026-11-12
**Purpose:** State the refined question, scope, objectives, and exclusions in one place. This supersedes the provisional question and scope in the original brief.

---

## 1. Primary question

> **Which Japanese municipalities face persistent structural vacancy risk, and is that risk already reflected in local housing markets — or is it accumulating in places where prices and transactions have not yet adjusted?**

This preserves the brief's core intent but sharpens the contribution. The project is not just another ranking; it tests whether the market has priced the risk.

---

## 2. Secondary questions

1. **Composition:** How does vacancy composition vary across municipalities and waves — dilapidated "other vacant," detached houses, rental, sale, secondary residences?
2. **Drivers:** Is municipal vacancy growth more closely associated with **demand contraction** (population, ageing, migration) or **supply inertia** (stock growth, low demolition, old stock)?
3. **Market adjustment:** Do land prices and transaction activity lead, lag, or ignore measured vacancy risk?
4. **Akiya banks:** Does akiya-bank participation/listing intensity correlate with risk, conditional on accessibility and program participation — leading indicator or symptom?
5. **Policy:** How does 2023 Act enforcement vary at prefecture level, and how does it relate to risk and fiscal capacity? (Descriptive, not causal.)
6. **Typology:** Which municipalities combine high risk with high activation potential (reuse priority) versus high risk with low activation and low fiscal capacity (demolition/consolidation priority)?

---

## 3. Scope

| Dimension | Decision |
|---|---|
| **Geography** | Japan, municipal level. |
| **Primary universe** | The **1,059 clean municipal units** in the 2023 Housing and Land Survey: 792 cities (20 designated + 772 non-designated), 23 special wards, and 244 towns/villages with 15,000+ population. The 1,235 table rows include 175 designated-city wards and 1 Tokyo special-wards group, which duplicate city-level rows and are excluded from the analysis. |
| **Secondary universe** | The **682 small towns/villages** absent from the survey: **6–8 case studies and a coverage-extension appendix**, not the national index. They hold **500,360 vacant dwellings (5.6% of the national total)**. |
| **Unit** | Municipality; wards separate where the survey reports them; district-level only in case studies. |
| **Vacancy time window** | **2018–2023** core (balanced 1,057 units); 2013/2008 city/ward context only; 2003 context. |
| **Demography** | 2000–2025 (census; 2025 basic tabulation published 2026-09-29). |
| **Market data** | Land prices and transactions 2005–2026. |
| **Policy** | 2014–2026. |
| **Projections** | IPSS municipal projections 2020–2050 as a pressure indicator, not a forecast of vacancy. |

### Exclusions

- **No property-level prediction.** The project does not predict which individual house will become vacant.
- **No causal evaluation of the 2023 Act.** The Act is national, implementation is staggered by municipal capacity, and designation is endogenous. A causal design is out of scope unless a credible natural experiment emerges.
- **No commercial valuation or investment advice.** The project is a research/policy tool.
- **No national "akiya tax" assumption.** No such tax exists in law.
- **No full national coverage claim.** The measured universe is **1,059 clean municipal units**; the **682 missing towns/villages** are handled separately. The covered units account for 94.4% of the vacant stock; the missing places hold 5.6%.

---

## 4. Objectives

1. Build a reproducible municipal panel harmonising vacancy, demographic, housing-market, fiscal, and geospatial data across survey waves and municipal mergers.
2. Construct separate **risk**, **activation potential**, and **response capacity** lenses, with equal weights as the headline and PCA/policy weights as sensitivity.
3. Classify municipalities into policy-relevant archetypes (risk × activation; risk × capacity; price level × price change as a secondary view).
4. Validate against market outcomes, akiya-bank participation, prefecture-level policy designations, and case studies.
5. Publish an interactive map, open data/code, and a short report/methodology note.
6. Document limitations: survey sampling error, coverage bias, municipal mergers, definitional changes, and the ecological fallacy.

---

## 5. Audience and deliverable

**Primary audience:** researchers and policymakers.
**Secondary audience:** a buyer-facing summary as a derivative, not the core.

**Core deliverable:** interactive map + open data/code + short report/methodology.
**Optional derivatives:** a 2-page policy brief; a buyer-facing summary with explicit non-advice disclaimers.

---

## 6. What changed from the brief, and why

| Brief | Refined | Why |
|---|---|---|
| National municipal index for all municipalities | **1,059 clean municipal units** + case studies | The 1,235 table rows double-count city/ward levels; 682 towns/villages (73.6%) are absent and hold 500,360 vacant dwellings (5.6%); a national ranking would be biased. |
| Vacancy 2003–2023 | 2018–2023 core; 2013/2008 city/ward context; 2003 context | The API's 2013/2008 four-category tables are 市区 only; a four-wave municipal panel would lose all towns/villages. |
| "Other vacant" as the core risk measure | **Dilapidated "other vacant"** as headline; broad rate as context | "Other vacant" includes long-term absence and demolition-planned homes; it is not "abandoned." |
| Single risk-and-opportunity index | Risk core + activation + capacity lenses | Risk, market demand, and fiscal capacity are different constructs; a single net score hides policy-relevant cases. |
| Buyers, researchers, policymakers equally | Researchers/policymakers primary; buyer summary derivative | The data are municipal and sample-based; a buyer's guide would overreach. |
| Akiya-bank scraping/structured collection | Official aggregates + participation + manual counts | Portals block automation; listings are ~0.2% of vacant stock; not a vacancy census. |
| Policy designations as validation | Descriptive context + case studies | Designations reflect administrative capacity, not only blight. |
| National "akiya tax" concern | No national akiya tax; separate DPFP bill, Kyoto local tax, and registration reform | The brief conflated law, proposal, and local tax. |

---

## 7. Working hypotheses

- **H1 (composition):** Municipalities with high total vacancy but low "other vacant" are dominated by secondary residences; they should not be ranked as structurally distressed.
- **H2 (drivers):** Demand contraction explains the level of structural vacancy; supply inertia explains persistence.
- **H3 (market lag):** In some municipalities, measured risk is not yet reflected in prices/transactions; in others, it is already discounted.
- **H4 (akiya banks):** Listing intensity is a symptom of marketable vacancy and program participation, not a leading indicator of structural risk.
- **H5 (policy):** Designation intensity reflects administrative capacity more than underlying blight.
- **H6 (typology):** The risk × activation and risk × capacity matrices identify different policy priorities (reuse vs demolition/consolidation vs monitoring).

These are hypotheses to test, not conclusions.

---

## 8. Success criteria

The project succeeds if it produces:

1. A documented, reproducible municipal panel with provenance.
2. A risk measure that is more defensible than total vacancy.
3. Explicit uncertainty and coverage limits.
4. A validation test that adds something beyond existing maps.
5. A public product that a researcher or policymaker can use without being misled.

It does **not** need to rank every municipality or predict individual properties.
