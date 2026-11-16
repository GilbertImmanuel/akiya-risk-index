# Findings: What We Have Established So Far

**Last updated:** 2026-11-12
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

---

## Finding 4 — The national municipal table covers most of the population but not most of the places

**Fact (Phase 0 parse).** The 2023 table has 1,283 geographic rows: 1 national + 47 prefectures + **1,235 municipal reporting rows**. The 1,235 rows are **not a clean municipality count**: they include 792 cities (20 designated + 772 non-designated), 23 special wards, 244 towns/villages, 175 designated-city wards, and 1 Tokyo special-wards group. To avoid double counting, the analysis uses **1,059 clean municipal units**: 792 cities + 23 special wards + 244 towns/villages.

**Fact (Phase 0 parse).** Japan has 926 towns/villages; the table covers **244**, so **682 (73.6%) are missing**. The 1,059 covered units account for **8,501,240 vacant dwellings (94.4%)**; the missing municipalities hold **500,360 vacant dwellings (5.6%)**.

**Implication:** the national index must be explicitly scoped to the **1,059 clean municipal units**. The 682 missing towns/villages need a separate case-study/coverage-extension track. A map that colours all of Japan would be misleading, and the 5.6% uncovered vacancy must be stated, not hidden.

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
