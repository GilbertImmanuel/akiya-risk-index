# Findings: What We Have Established So Far

**Last updated:** 2026-11-23
**Purpose:** Synthesise the research into a small number of claims, each labelled **Fact**, **Inference**, or **Hypothesis**. This is the file to update as the data audit progresses.

---

## Finding 1 — Vacancy is at a record high, but the headline is composition-sensitive

**Fact.** In 2023, Japan had **9,002,000 vacant dwellings**, or **13.8%** of the **65,047,000** dwelling stock. The five-year increase was **513,000**. The "other vacant" category was **3,856,000**, or **5.9%** of all dwellings.

**Fact.** The vacancy stock is not homogeneous: 4,436,000 rental vacancies, 326,000 for sale, 384,000 secondary residences, and 3,856,000 "other vacant." A high total vacancy rate can be driven by secondary homes (e.g., Karuizawa) rather than structural blight.

**Implication:** never rank municipalities on total vacancy alone. Report the composition.

---

## Finding 2 — "Other vacant" is a residual category, not a synonym for abandoned

**Fact.** The 2023 definition includes long-term absence due to transfer or hospitalisation, homes awaiting demolition, storage, unknown use, and genuine abandonment. It **excludes `廃屋`** (ruined structures not counted as dwellings).

**Implication:** the broad "other vacant" rate overstates abandonment in some places and understates the worst blight. The project needs a narrower measure.

---

## Finding 3 — Dilapidated "other vacant" is the best available national risk proxy

**Inference.** The municipal tables publish `腐朽・破損の有無` alongside the vacancy categories for 2008, 2013, 2018, and 2023. Combining "other vacant" with "dilapidated" isolates the part of the residual category most likely to represent blight. It is still a **lower bound** because `廃屋` is excluded and because the survey is sample-based.

**Proposed headline measure:** **dilapidated "other vacant" detached houses per 1,000 dwellings**, with the broad "other vacant" rate as context.

**Fact (Phase 0 parse of table 34-2):** **895,300** of the 3,856,000 "other vacant" dwellings are dilapidated (23.2%); **715,000 of those are detached**. This is the national baseline for the headline risk measure.

**Why detached:** 74% of "other vacant" dwellings are detached houses (2.851m of 3.856m). The structural problem is predominantly a detached-house problem.

### Finding 3b — Measured dilapidation fell between 2018 and 2023, but partly by attrition

**Fact (Phase 0 parse).** The broad "other vacant" stock rose from **3,487,200 to 3,856,000 (+10.6%)**, but the **dilapidated** "other vacant" stock fell from **1,006,000 to 895,300 (−11.0%)**. The dilapidated share fell from **28.8% to 23.2%**. Dilapidated detached "other vacant" fell from **799,900 to 715,000**.

**Inference.** This is not necessarily improvement. A Daiwa Real Estate Appraisal analysis notes that some abandoned houses deteriorated into `廃屋` and left the survey universe, alongside policy/redevelopment effects. The measured decline can therefore be partly **attrition**. The headline risk measure is a lower bound that can fall mechanically when the worst structures become statistically invisible.

**Implication:** do not assume a monotonic risk trend. Separate "dilapidated but still a dwelling" from "ruined and outside the survey"; use case studies to understand which is happening.

---

## Finding 4 — The national municipal table covers most of the population but not most of the places

**Fact (Phase 0 parse).** The 2023 table has 1,283 geographic rows: 1 national + 47 prefectures + **1,235 municipal reporting rows**. The 1,235 rows are **not a clean municipality count**: they include 792 cities (20 designated + 772 non-designated), 23 special wards, 244 towns/villages, 175 designated-city wards, and 1 Tokyo special-wards group. To avoid double counting, the analysis uses **1,059 clean municipal units**: 792 cities + 23 special wards + 244 towns/villages.

**Fact (Phase 0 parse).** Japan has 926 towns/villages; the table covers **244**, so **682 (73.6%) are missing**. The 1,059 covered units account for **8,501,240 vacant dwellings (94.4%)**; the missing municipalities hold **500,360 vacant dwellings (5.6%)**, **327,880 “other vacant” (8.5%)**, and **89,240 dilapidated “other vacant” (10.0%)**.

**Implication:** the national index must be explicitly scoped to the **1,059 clean municipal units**. The 682 missing towns/villages need a separate case-study/coverage-extension track. A map that colours all of Japan would be misleading, and the 10% uncovered dilapidated stock must be stated, not hidden.

---

## Finding 4b — The 2018–2023 coverage change is threshold-driven, not merger-driven

**Fact (Phase 0 crosswalk).** The e-Stat municipal merger history shows **18 status changes** between 2018 and 2023, but **no municipal mergers**. The vacancy-table coverage changed because **29 towns/villages dropped out** of the 2023 table and **2 entered**. One code has a name change (28221 篠山市 → 丹波篠山市).

**Fact (Phase 0 crosswalk).** The balanced 2018–2023 panel is **1,057 municipal units**: 1,056 matched + 1 name change. The 29 dropped and 2 added units are excluded from the balanced panel but retained in the full crosswalk.

**Implication:** for 2018–2023, the municipal-code crosswalk is simple; the harder harmonisation problem starts with 2013 and 2008. Do not attribute the 27-unit coverage change to mergers.

### Finding 4c — The 2013/2008 API tables are city/ward only

**Fact (Phase 0 API check).** The e-Stat API's 2013 table 53 (`statsDataId=0003100835`) and 2008 table 043-2 (`statsDataId=0003010419`) are **市区 only** (cities/wards). They do not include towns/villages. The 2008 table 043-1 is prefectural, not municipal.

**Implication:** a four-wave municipal panel that includes towns/villages is **not available from the API**. The core panel is **2018–2023** (balanced 1,057 units); 2013/2008 are used as **city/ward context** only. Extracting the 2013/2008 町村 tables from printed reports would be a separate manual project and is not part of Phase 1.

---

## Finding 4d — Proper dwelling denominators change the risk picture

**Fact (Phase 0 Installment 2).** Total dwellings are now available for **1,059/1,059** 2023 units and **1,086/1,086** 2018 units. The vacancy counts match the vacancy tables exactly (0 mismatches). The full 2018–2023 vacancy panel has **1,059 units**, of which **1,057** are balanced.

**Fact (2023 proper rates).** The highest **dilapidated “other vacant” / total dwellings** rates are:

| Municipality | Prefecture | Rate |
|---|---|---:|
| 川崎町 | Miyagi | **12.25%** |
| 新上五島町 | Nagasaki | **11.89%** |
| 平戸市 | Nagasaki | **9.29%** |
| 垂水市 | Kagoshima | **9.29%** |
| 室戸市 | Kochi | **9.11%** |
| さつま町 | Kagoshima | **9.04%** |
| いの町 | Kochi | **8.75%** |
| 伊佐市 | Kagoshima | **8.61%** |
| 三種町 | Akita | **8.60%** |
| 珠洲市 | Ishikawa | **8.51%** |

**Fact (2018→2023 change).** The largest increases are 川崎町 (+8.48 pp), さつま町 (+6.51), 有田川町 (+5.48), 新上五島町 (+5.23), and 平戸市 (+4.79). Some high-rate places improved (室戸市 −3.21 pp).

**Proxy comparison.** The household proxy and the proper rate have a Spearman correlation of **0.991** overall, but the proxy misranks places with secondary homes or large households: 軽井沢町 is rank 9 on the proxy and rank 35 on the proper rate. The proper denominator is required for the index.

**Caveat:** municipal survey estimates are noisy; the top rates and changes should be read with uncertainty bands. This is not a causal claim.

---

## Finding 5 — Demand factors dominate prior prefectural studies, but supply and demolition matter

**Fact / association.** JRI's 2003–2023 prefectural panel finds that death rates, out-migration, and in-migration are significantly associated with "other vacant" rates; old-housing share is negatively associated, consistent with old stock being demolished. The model fits well (adjusted R² ≈ 0.88), but it is prefectural and correlational.

**Hypothesis.** At municipal level, demand contraction explains the **level** of structural vacancy, while supply inertia — continued construction, low demolition, old stock — explains **persistence**. The relative importance may differ between urban shrinkage and rural decline.

**Implication:** include both demand and supply variables; do not assume population alone is sufficient.

---

## Finding 6 — Household growth is masking population decline

**Fact.** The 2025 Census shows population at **122.97m**, down **2.5%** from 2020, while general households rose to **57.18m (+1.477m)** and persons per household fell to **2.10**. **91.2% of municipal units lost population**, and 28.4% lost ≥10%.

**Implication:** vacancy is not a simple population story. Ageing and single-person households can keep household numbers up even as population falls. Use both population and household change; the gap between dwelling growth and household growth is a useful pressure variable.

---

## Finding 7 — Market lag is plausible but not yet tested

**Hypothesis.** In some municipalities, measured structural vacancy may not yet be reflected in land prices or transaction activity; in others, the market may already discount it. The difference may be related to accessibility, demand, and the composition of vacancy (secondary vs structural).

**Why it matters:** this is the project's main analytical contribution. A ranking alone would repeat existing maps; a market-lag test would add something new.

**What would falsify it:** if price/transaction changes are uncorrelated with measured risk across specifications, or if the correlation is entirely explained by demand controls, the "lag" story is weak.

---

## Finding 8 — Akiya banks are a tiny, selected signal

**Fact.** As of October 2026, the national akiya-bank portal had **1,155 participating municipalities**, **750 currently listing**, **20,089 current listings**, and **~29,000 cumulative transactions**. Participation is 65.5% of municipalities, but listing is concentrated.

**Inference.** 20,089 listings against 9.0m vacant dwellings (and 3.86m "other vacant") is about **0.2%** of the vacant stock. The portal measures **marketed supply with owner consent in participating municipalities**, not vacancy. It cannot validate a national index on its own.

**Hypothesis.** Akiya-bank listing intensity is a **symptom** of marketable vacancy and program participation, not a leading indicator of structural risk. It may be a leading indicator in accessible places with demand, and a symptom in remote places.

**Implication:** use participation as a municipal covariate; use aggregate listing trends as context; use manual counts in case studies. No scraping.

---

## Finding 9 — Policy designations measure enforcement, not underlying blight

**Fact.** As of 31 March 2025, `管理不全空家等` guidance was **3,211 cases in 185 municipalities**, and recommendations were **378 cases in 40 municipalities**. `特定空家等` advice/guidance was **42,768 cumulative cases in 875 municipalities**. The counts are prefecture-level; no municipal list is published.

**Inference.** A municipality with a well-staffed program may report more designations than a similarly blighted municipality with no capacity. Designations are **endogenous to administrative effort**.

**Implication:** do not use designations as an unbiased municipal validation variable. Use them descriptively at prefecture level and in case studies.

---

## Finding 10 — Measurement uncertainty is large enough to change rankings

**Fact.** The Housing and Land Survey samples about **3.4 million dwellings (~5% of the stock)**, with target standard errors of **5% for cities** and **10% for 15,000+ towns**. Small-area estimates are noisy.

**Inference.** Rankings of small municipalities are unstable; a one-point difference in a vacancy rate is often not meaningful. Uncertainty must be a first-class output, not an appendix.

**Implication:** use simulation and/or empirical-Bayes smoothing; report rank stability; mark "insufficient evidence" where data are thin.

---

## Finding 11 — The genuine gap is synthesis, validation, and openness

**Inference.** Existing work already provides national maps, prefectural forecasts, academic driver studies, and metro spatial models. The missing product is an **open, reproducible, multi-wave municipal panel** that separates current blight from forward pressure, reports uncertainty, and tests market/policy signals.

**Implication:** position the project as a **research and policy tool**, not a first-ever vacancy study or a prediction competition.

---

## Finding 12 — The "cheap but recovering" archetype is conditional

**Hypothesis.** A price-level × price-change typology can distinguish "cheap but recovering" from "cheap and deteriorating," but only where municipal price/transaction data are sufficient. In rural municipalities with few transactions or land-price points, the quadrant would be noise.

**Implication:** do not force every municipality into a quadrant. Use an explicit "insufficient evidence" category, and treat the price typology as a secondary view, not the core index.

---

## Finding 13 — Rail access is associated with lower structural vacancy, but not with recent change

**Fact (Phase 0 accessibility build).** The 2023 station layer contains **9,007 facilities**: **8,399 heavy-rail stations** (JR, private, subway, monorail, AGT, guided rail, maglev) and **608 tram-only stops**. After assigning stations to municipalities, **7,479 heavy-rail stations** fall inside the 1,059-unit panel; **924** fall in the 682 out-of-scope towns/villages.

**Fact.** **126 units (11.9%) have no heavy-rail station**. Fifteen of these have a rail line crossing the municipality but no station (e.g., 綾瀬市, 阿見町, 十和田市); the rest are genuinely rail-free. Zero-station status is therefore an access measure, not a data failure.

**Fact (association, not causation).** Across the 1,059 units:

| Pair | Spearman ρ | Interpretation |
|---|---:|---|
| Station density vs population density | **+0.701** | Rail access tracks urbanity, as expected. |
| Station density vs 2023 dilapidated “other vacant” rate | **−0.447** | More accessible places have lower structural vacancy. |
| Station density vs 2023 total vacancy rate | **−0.365** | Same direction, weaker. |
| Station density vs 2018–2023 change in dilapidated “other vacant” rate | **−0.018** | No association. |
| Station density vs 2018–2023 change in broad “other vacant” rate | **−0.220** | Weak negative association. |

**Inference.** Accessibility is a plausible part of the **activation lens**: places with more rail stations also have lower structural vacancy today. But the association is confounded with population density, age structure, and regional demand. The near-zero correlation with the **change** in dilapidated vacancy suggests accessibility explains the **level** of risk more than the **trajectory**.

**Fact.** Passenger data are incomplete: **87.4%** of heavy-rail stations in the panel have S12 values. Coverage is especially thin for JR Hokkaido/Tohoku unmanned stations and JR Kyushu stations outside the top 300. Passenger-based metrics are secondary; station count and density are the robust v0 measures.

**Implication:** use station count/density as the first activation variable, with `passenger_data_share` as a quality flag. Do not use `passengers_per_capita` as a headline without a coverage threshold. Revisit nearest-station distance and travel time in Phase 1 with a population-weighted centroid or grid.

---

## Pilot v0 observations (preliminary, not a final ranking)

**Fact (Phase 0 pilot).** The first pilot panel covers **89 units** in Tokyo (51), Nagano (25), and Kochi (13). All have 2018 vacancy data and 2025 census data; 23 Tokyo special wards lack the municipal fiscal strength index.

**Preliminary pattern (descriptive, not causal).** Using **dilapidated “other vacant” per 1,000 households** as a provisional proxy:

- Kochi’s rural cities (土佐清水市, 室戸市, いの町, 須崎市, 宿毛市) show the highest values, alongside steep population decline and low fiscal strength.
- Nagano’s towns/cities (下諏訪町, 佐久市, 伊那市, 大町市, 東御市) are next.
- Tokyo’s special wards and suburban cities are lower on this proxy, though some have large absolute vacancy counts.

**Caveats:** households are not dwellings; the real denominator must come from the total-dwelling table. The pilot is not representative and the index weights are not yet applied. Treat this as a data-join test, not a finding about which places are “most at risk.”

---

## What would change these conclusions

- **If the 2013/2008 tables are not comparable** to 2018/2023, the panel shrinks to two waves and the persistence analysis weakens.
- **If rural price/transaction coverage is too thin**, the activation lens becomes urban-only; the project should say so.
- **If akiya-bank participation is unrelated to risk** after controls, the "symptom vs leading indicator" question may be unanswerable with available data.
- **If municipal designation counts become available** and are less endogenous than assumed, they could become a stronger validation variable.
- **If the 2025 Census municipal tables are delayed or incomplete**, the demand side may need to rely on 2020 census plus annual estimates.

---

## Sources

- Statistics Bureau, 2023 Housing and Land Survey summary: https://www.stat.go.jp/data/jyutaku/2023/pdf/kihon_gaiyou.pdf (accessed 2026-11-12).
- Statistics Bureau, 2023 survey definitions: https://www.stat.go.jp/data/jyutaku/2023/pdf/yougo.pdf (accessed 2026-11-12).
- e-Stat, 2023 table 34-2: https://www.e-stat.go.jp/dbview?sid=0004021631 (accessed 2026-11-12).
- Statistics Bureau, 2025 Census summary: https://www.stat.go.jp/data/kokusei/2025/kekka/pdf/summary_01.pdf (accessed 2026-11-12).
- JRI, 2040 vacancy forecast: https://www.jri.co.jp/file/report/researchfocus/pdf/15673.pdf (accessed 2026-11-12).
- MLIT, 2025 enforcement survey: https://www.mlit.go.jp/jutakukentiku/house/content/001984996.pdf (accessed 2026-11-12).
- MLIT, national akiya-bank page: https://www.mlit.go.jp/totikensangyo/const/sosei_const_tk3_000131.html (accessed 2026-11-12).
- Tokyo Foundation, municipal vacancy analysis: https://www.tkfd.or.jp/research/detail.php?id=4644 (accessed 2026-11-12).
