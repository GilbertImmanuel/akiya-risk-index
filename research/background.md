# Background: Verified Numbers, Definitions, and Measurement Caveats

**Last updated:** 2026-11-12
**Purpose:** Establish the verified factual baseline for the project. This file replaces the provisional background in the brief where the two differ.

---

## 1. The headline, verified

The 2023 Housing and Land Survey (令和5年住宅・土地統計調査), conducted on 1 October 2023 and published in confirmed form on 25 September 2024, is the authoritative source.

| Indicator | 2023 confirmed | 2018 | Change |
|---|---:|---:|---:|
| Total dwellings | **65,047,000** | 62,407,000 | +2,639,000 (+4.2%) |
| Vacant dwellings | **9,002,000** | 8,489,000 | **+513,000** |
| Vacancy rate | **13.8%** | 13.6% | +0.2 pp |
| "Other vacant" (賃貸・売却用及び二次的住宅を除く空き家) | **3,856,000** | 3,487,000 | +369,000 |
| "Other vacant" rate | **5.9%** | 5.6% | +0.3 pp |

**Fact.** The brief's 9.0 million / 65.02 million / 13.8% figures are substantively correct, but the confirmed count is **65,047,000 dwellings**, **9,002,000 vacant**, and the five-year increase is **513,000**, not the preliminary 507,000. Use the confirmed figures.

### Longer trend

| Year | Total dwellings (000) | Vacant (000) | Vacancy rate (%) | "Other vacant" (000) |
|---:|---:|---:|---:|---:|
| 2003 | 53,891 | 6,593 | 12.2 | 2,118 |
| 2008 | 57,586 | 7,568 | 13.1 | 2,681 |
| 2013 | 60,629 | 8,196 | 13.5 | 3,184 |
| 2018 | 62,407 | 8,489 | 13.6 | 3,487 |
| 2023 | 65,047 | 9,002 | 13.8 | 3,856 |

**Fact.** Vacant dwellings roughly doubled between 1993 (4.476 million) and 2023 (9.002 million). The stock of dwellings grew faster than the number of households over the period.

### Composition in 2023

| Category | Dwellings (000) | Share of vacant stock |
|---|---:|---:|
| Rental vacancy (賃貸用) | 4,436 | 49.3% |
| For sale (売却用) | 326 | 3.6% |
| Secondary residence (二次的住宅) | 384 | 4.3% |
| **"Other vacant"** | **3,856** | **42.8%** |
| **Total vacant** | **9,002** | **100%** |

**Fact.** Of the 3.856 million "other vacant" dwellings, **2.851 million (74%) are detached houses**, 848,000 are apartments, and 137,000 are row houses. The structural vacancy problem is predominantly a detached-house problem.

**Fact (Phase 0 parse of table 34-2).** **895,300** of the 3,856,000 "other vacant" dwellings are **dilapidated** (23.2%). Of those, **715,000 are detached houses**. This is the national baseline for the headline risk measure: about **0.9 million dilapidated “other vacant” homes**, mostly detached.

**Fact.** 4.753 million households own a dwelling other than their current home; 1.416 million of those households own a vacant dwelling; 47.5% of owner-owned vacant dwellings are "other vacant." This is consistent with inheritance and absentee ownership as important channels, though it does not by itself prove causation.

### 2018 → 2023: measured dilapidation fell

**Fact (Phase 0 parse of tables 35-2 and 34-2).**

| Indicator | 2018 | 2023 | Change |
|---|---:|---:|---:|
| "Other vacant" | 3,487,200 | 3,856,000 | **+368,800 (+10.6%)** |
| Dilapidated "other vacant" | 1,006,000 | 895,300 | **−110,700 (−11.0%)** |
| Dilapidated share of "other vacant" | 28.8% | 23.2% | −5.6 pp |
| Dilapidated detached "other vacant" | 799,900 | 715,000 | **−84,900 (−10.6%)** |

**Inference.** The broad "other vacant" stock grew, but the *measured dilapidated* stock fell. This is not necessarily good news. A Daiwa Real Estate Appraisal analysis of the 2023 survey notes three possible reasons: (1) policy and management efforts, (2) redevelopment of well-located vacant houses during the land-price rise, and (3) some abandoned houses deteriorated into `廃屋` and fell **outside the survey universe**. The third channel means the measured decline can be partly **attrition**, not improvement.

**Implication for the index:** do not assume a monotonic increase in risk. The headline measure is a lower bound that can fall when the worst structures leave the statistics. The project should distinguish:
- **dilapidated but still a dwelling** — measured by the survey;
- **ruined and outside the survey** — not measured, but still a policy problem.

This also means the 2018–2023 comparison is not a clean "risk trend" without the `廃屋` caveat.

**Coverage comparison:** 2018 covers 1,086 clean municipal units (95.2% of the national vacancy stock); 2023 covers 1,059 (94.4%). The 27-unit difference is partly municipal mergers and partly municipalities falling below the 15,000 reporting threshold. The uncovered vacancy rose from 411,330 (4.85%) to 500,360 (5.56%).

---

## 2. What "vacant" actually means

The survey's definitions matter more than the headline. A **dwelling** (住宅) is a structurally independent unit with at least one living room, a dedicated kitchen sink, a dedicated toilet, and a dedicated entrance. A **`廃屋`** — a ruined structure that cannot support ordinary family life as-is — is **not counted as a dwelling** and therefore falls outside the vacancy statistics entirely.

The survey divides dwellings into:

1. **Occupied dwellings** (居住世帯のある住宅).
2. **Dwellings with no usual resident** (居住世帯のない住宅), which are further divided into:
   - **temporary occupants only** (一時現在者のみ) — e.g., daytime use, people sleeping in shifts;
   - **vacant dwellings** (空き家);
   - **under construction** (建築中の住宅).

**Vacant dwellings** are then split into four categories:

| Category | Japanese | Meaning |
|---|---|---|
| Rental vacancy | 賃貸用の空き家 | Vacant and offered for rent, new or used. |
| For-sale vacancy | 売却用の空き家 | Vacant and offered for sale, new or used. |
| Secondary residence | 二次的住宅 | A villa or occasional-use home; not the household's usual residence. |
| **"Other vacant"** | **賃貸・売却用及び二次的住宅を除く空き家** | Everything else: long-term absence due to transfer or hospitalisation, homes awaiting demolition, and cases where the use is difficult to classify. |

**Critical correction to the brief.** "Other vacant" is **not** a synonym for "abandoned, inherited, or unusable." It is a residual category that includes:

- houses whose owners are temporarily absent for work or hospital;
- houses scheduled for demolition or rebuilding;
- houses used for storage or other purposes;
- houses whose status is unknown;
- genuinely abandoned or neglected houses.

Conversely, the worst ruined structures (`廃屋`) are **excluded** from the survey universe. The survey therefore both **over-includes** some non-abandoned homes and **under-includes** the most blighted structures. This is why the project should use **dilapidated "other vacant"** — the subset with `腐朽・破損あり` — as the headline risk measure, while reporting the broad rate as context.

**Fact.** The 2023 survey renamed the category from the 2018 label `その他の住宅` ("other dwellings") to `賃貸・売却用及び二次的住宅を除く空き家` ("vacant dwellings excluding rental, sale, and secondary"). The definition is essentially the same; the label change signals policy attention, not a new phenomenon.

---

## 3. Why composition matters more than the headline

A high total vacancy rate can mean very different things:

- **Karuizawa, Nagano**: a very high total vacancy rate, driven by secondary residences. The "other vacant" rate is below the national median. A naive ranking would mislabel it as a distressed place.
- **A declining rural town**: a high "other vacant" rate, often with a high dilapidated share, is closer to the policy problem.
- **A large city**: a high rental vacancy rate may reflect normal market churn, not blight.

**Fact.** The Tokyo Foundation's 2025 analysis shows that secondary-residence rates vary enormously across municipalities (median 0.3%, maximum 63% in Karuizawa), and that total vacancy rankings can be misleading. The brief's instinct to focus on "other vacant" is correct, but the measure needs further refinement.

**Inference.** The most defensible headline measure is:

> **Dilapidated "other vacant" detached houses per 1,000 dwellings** (or as a share of the dwelling stock).

This isolates the part of the residual category most likely to represent blight, and it uses a variable (`腐朽・破損の有無`) that is published in the municipal tables for 2008, 2013, 2018, and 2023. It still excludes `廃屋`, so it is a **lower bound** on severe blight.

---

## 4. The 2025 demographic context

The 2025 Census (published 29 September 2026) changes the demand-side picture:

| Indicator | 2025 | Change from 2020 |
|---|---:|---:|
| Population | **122,972,528** | **−3,173,571 (−2.5%)** |
| Annual population change | — | −0.51% per year |
| General households | **57,182,000** | **+1,477,000** |
| Persons per household | **2.10** | continued decline |
| Population aged 65+ | 29.4% | — |
| Population under 15 | 10.9% | — |
| Municipalities losing population | **1,568 of 1,719 (91.2%)** | — |
| Municipalities losing ≥10% | 28.4% | — |

**Fact.** Japan's population is falling, but the number of households is still rising, because of ageing, single-person households, and smaller household sizes. Vacancy is therefore not a simple function of population decline. A place can lose population while household numbers hold up, and a place can gain households while its housing stock grows faster.

**Inference.** The demand side should be modelled with **both population and household change**, not population alone. The supply side should include **dwelling completions, demolitions, and the age/quality of the stock**. The gap between dwelling growth and household growth is a useful summary pressure variable.

---

## 5. Drivers: what is established, what is plausible

The brief lists demographic decline, ageing, inheritance and absentee ownership, weak local demand, tax and construction incentives, fragmented or unknown ownership, and limited market liquidity. The evidence strength differs.

| Driver | Evidence status | Notes |
|---|---|---|
| Demographic decline and ageing | **Strong association** | JRI's prefectural panel finds death rates, out-migration, and in-migration are significantly associated with "other vacant" rates. The 2025 Census shows 91.2% of municipalities shrinking. |
| Inheritance and absentee ownership | **Strong descriptive evidence** | 1.416 million households own a vacant dwelling; 47.5% of owner-owned vacant dwellings are "other vacant." The 2024 inheritance-registration obligation and the 2026 address-change obligation are policy responses to ownership opacity. |
| Weak local demand / market liquidity | **Association** | Thin transactions and declining prices are correlated with vacancy in many places, but the direction of causality is not established. |
| Tax and construction incentives | **Plausible; not estimated here** | The residential-land tax exception lowers the holding cost of land with a house, and demolition can raise the tax base. This can discourage demolition and redevelopment. The project will not attempt a causal estimate. |
| Fragmented or unknown ownership | **Qualitative / case evidence** | Frequently cited by municipalities; hard to measure nationally. The inheritance-registration reforms are relevant. |
| Construction incentives / stock growth | **Association** | Japan has continued to build while the population falls; the dwelling stock grew 4.2% between 2018 and 2023 while households grew 4.1%. The gap is small in aggregate but large in some regions. |

**Hypothesis (to test, not assume).** Demand contraction dominates the **level** of structural vacancy, while supply inertia — continued construction, low demolition, old stock — explains **why vacancy persists** rather than clearing. The relative importance may differ between urban shrinkage and rural decline.

---

## 6. What "risk" means in this project

The brief refers to blight, fire and safety risk, weaker neighbouring property values, and municipal fiscal stress. These are plausible and documented in case literature, but this project will **not** estimate them causally. We will treat them as the **policy motivation**, not as measured outcomes.

For the index, "risk" has two components:

1. **Current risk** — the observed stock of dilapidated "other vacant" dwellings, the broad "other vacant" rate, and persistence across survey waves.
2. **Forward pressure** — demographic decline, ageing, household shrinkage, net migration, dwelling growth exceeding household growth, old stock, and weak demolition.

This separation avoids double-counting the same phenomenon and makes the index easier to explain.

"Opportunity" is deliberately **not** used as a synonym for investment return. The project will use **activation potential** (can the local market absorb and reuse the stock?) and **response capacity** (can the municipality act?). See `findings.md`.

---

## 7. Measurement caveats

These are not footnotes; they determine what the index can honestly claim.

1. **The survey is a sample survey.** The 2023 survey sampled about 200,000 unit districts and about 3.4 million dwellings (roughly 5% of the stock). The target standard error is 5% for cities and 10% for towns/villages with 15,000+ population. Municipal vacancy rates and five-year changes are therefore **estimates**, not exact counts.
2. **Small-area estimates are noisy.** A town with a 10% vacancy rate and a small sample can easily have a true rate several points higher or lower. Rankings of small municipalities are unstable. Uncertainty must be reported.
3. **Coverage is incomplete.** The 2023 table has 1,283 geographic rows: 1 national + 47 prefectures + 1,235 municipal reporting rows. The 1,235 rows are **not a clean municipality count**: they include 792 cities (20 designated + 772 non-designated), 23 special wards, 244 towns/villages, 175 designated-city wards, and 1 Tokyo special-wards group. To avoid double counting, the analysis uses **1,059 clean municipal units**: 792 cities + 23 special wards + 244 towns/villages. Japan has 926 towns/villages, so **682 (73.6%) are missing**. The covered units account for **8,501,240 vacant dwellings (94.4% of the national 9,001,600)**; the **500,360 vacant dwellings (5.6%)** in the missing municipalities are not separately reported. The missing places are likely disproportionately rural and higher-vacancy on average (inference, not directly measured).
4. **The survey does not produce mesh vacancy statistics.** It is a sample survey; 1 km mesh tables are not available. District/mesh case studies need municipal surveys, microdata, or local data.
5. **Definitions changed across waves.** The 2008 table uses five vacancy categories; 2013 uses four; 2018 and 2023 use four with a label change. Table-by-table reconciliation is required.
6. **Municipal mergers change the units.** The 2005–2010 Heisei mergers and later mergers mean that a 2008 municipality may not correspond to a 2023 municipality. A crosswalk to 2023 boundaries is required; some predecessors can be aggregated, others cannot.
7. **`廃屋` is excluded.** The most severely ruined structures are not counted, so the survey-based measure is a lower bound on severe blight.
8. **"Other vacant" is heterogeneous.** It mixes temporary absence, demolition-planned homes, storage, unknown use, and genuine abandonment. The dilapidated subset is a better proxy, not a perfect one.
9. **Ecological fallacy.** A municipal-level association does not imply that any particular household or property behaves that way. The project will not make property-level claims.
10. **Policy designations are endogenous.** Municipal designation counts reflect administrative capacity and political will, not only underlying blight. They are not a clean validation variable.

---

## 8. Implications for the index

- **Headline risk measure:** dilapidated "other vacant" detached houses per 1,000 dwellings, with the broad "other vacant" rate as context.
- **Do not rank all 1,741 municipalities.** Use the 1,059 clean municipal units and treat the 682 missing towns/villages separately.
- **Report uncertainty.** Use the survey's target standard errors, simulation, and/or empirical-Bayes smoothing; show rank stability.
- **Separate current risk from forward pressure.** Do not mix stock and flow in one opaque score.
- **Use demand and supply variables together.** Population alone will mislead; include households, migration, dwelling growth, and demolition.
- **Treat policy and akiya-bank signals as selected.** They are descriptive context, not unbiased validation.

---

## Sources

- Statistics Bureau of Japan, *令和5年住宅・土地統計調査 住宅及び世帯に関する基本集計（確報集計）結果の要約*: https://www.stat.go.jp/data/jyutaku/2023/pdf/kihon_gaiyou.pdf (accessed 2026-11-12).
- Statistics Bureau, *令和5年住宅・土地統計調査 用語の解説*: https://www.stat.go.jp/data/jyutaku/2023/pdf/yougo.pdf (accessed 2026-11-12).
- e-Stat, 2023 table 34-2: https://www.e-stat.go.jp/dbview?sid=0004021631 (accessed 2026-11-12).
- Statistics Bureau, *令和7年国勢調査 人口等基本集計 結果の要約*: https://www.stat.go.jp/data/kokusei/2025/kekka/pdf/summary_01.pdf (accessed 2026-11-12).
- Tokyo Foundation, *市区町村別に見た日本の空き家の現状* (23 January 2025): https://www.tkfd.or.jp/research/detail.php?id=4644 (accessed 2026-11-12).
- JRI, *2040年代の全国・都道府県別 空き家数・空き家率の推計* (2025): https://www.jri.co.jp/file/report/researchfocus/pdf/15673.pdf (accessed 2026-11-12).
