# Open Questions and Unresolved Decisions

**Last updated:** 2026-11-12
**Purpose:** Track what we do not know yet, why it matters, and what the next step is. Update this file rather than relying on memory.

---

## A. Data questions

| # | Question | Why it matters | Next step | Status |
|---|---|---|---|---|
| A1 | Are the 2013 and 2008 municipal vacancy tables directly comparable to 2018/2023 in category definitions, coverage, and table geography? | The four-wave panel depends on it. If not, the core panel shrinks to 2018–2023. | Download the tables, compare labels/totals, build a crosswalk. | Open |
| A2 | Does the 2013 `町村` table cover all towns/villages, or only 15,000+? | Determines whether 2013 can be combined with 2023 coverage. | Locate the 2013 町村 tables; compare the municipal list. | Open |
| A3 | Are municipal-level `管理不全`/`特定空家` designation counts published anywhere? | The brief asks where designations are concentrated. Prefecture-level only is a weaker answer. | Search MLIT/prefectural open data; consider FOIA requests; use case studies. | Open |
| A4 | Is rural transaction/land-price coverage sufficient for an activation index? | If not, the activation lens becomes urban-only. | Pilot Tokyo, Nagano, Kochi; count records per municipality; test pooling. | Open |
| A5 | Can akiya-bank municipal listing counts be obtained without scraping? | The portals block automation; listing counts would be a useful validation signal. | Use official aggregates/participation lists; ask LIFULL/AtHome/municipalities; manual counts in case studies. | Open |
| A6 | What exactly changed in the September 2026 amendment? | The brief must not overstate it. | Read the amended statute and the 16th decentralization act materials; compare the guidelines. | Open |
| A7 | What is the exact tax-assessment timing after a `管理不全` recommendation? | The fiscal-risk discussion depends on it. | Read the Local Tax Act and municipal guidance; confirm the 1 January base date effect. | Open |
| A8 | Are the 2025 Census municipal tables complete for our variables? | Demand-side data need to align with 2023 vacancy. | Check the e-Stat release calendar; download and QA. | Open |
| A9 | How reliable are the `腐朽・破損` cells at municipal level? | The headline risk measure depends on them; small samples may produce unstable cells. | Compare 2018/2023 cells; test suppression/small counts; simulate error. | Open |
| A10 | What is the best demolition proxy? | Supply inertia needs a demolition variable; the official statistics are incomplete. | Compare residual estimate vs 建築物滅失統計; document the choice. | Open |

---

## B. Method questions

| # | Question | Why it matters | Next step | Status |
|---|---|---|---|---|
| B1 | Should the index use equal weights, PCA, or policy weights as the headline? | We chose equal weights for interpretability, with PCA/policy as sensitivity. Confirm the sensitivity results before publishing. | Run all three; compare ranks/top-20; report. | Decided (D5); validate |
| B2 | How should uncertainty be presented? | Rankings of small municipalities are unstable. | Simulate survey error; empirical-Bayes smoothing; rank-stability bands. | Open |
| B3 | Should the index use a single composite risk score or separate current-risk and pressure sub-indices? | A single score is easier to communicate; sub-indices are more transparent. | Build both; use sub-indices in the report; show the composite as a summary. | Open |
| B4 | How should wards be treated? | Wards are separate reporting units in the survey; municipal policy often operates at the city level. | Keep wards separate for measurement; aggregate to city for policy analysis where needed. | Open |
| B5 | Should the activation lens use price levels, price changes, or both? | "Cheap but recovering" needs both; thin data may make one unreliable. | Use both; require a minimum number of observations; flag insufficient evidence. | Open |
| B6 | Should response capacity be a separate index or an overlay? | D3 chose both activation and capacity; capacity may be better as an overlay. | Build capacity as an overlay; test whether it changes the archetypes. | Open |
| B7 | How should municipal mergers be handled? | 2008 municipalities may not match 2023 boundaries. | Build a crosswalk; aggregate predecessors to 2023 boundaries; document assumptions. | Open |
| B8 | Should 2003 be included in the core panel? | It adds history but also pre-Heisei-merger and definitional problems. | Use 2003 as context only; test robustness. | Decided (D4); document |
| B9 | How should tourism/remote-work demand be proxied? | These are part of activation potential but not directly measured at municipal level. | Use census commuting/day-night ratios, accommodation statistics where available, and case-study evidence; avoid overclaiming. | Open |
| B10 | Should the index be updated annually or only with survey waves? | Vacancy data are 5-yearly; market data are quarterly. | Publish a static v1 for 2023; design an update path for market data. | Open |

---

## C. Scope questions

| # | Question | Why it matters | Next step | Status |
|---|---|---|---|---|
| C1 | Should we model the 682 missing towns/villages? | Coverage bias is the biggest limitation; they hold 500,360 vacant dwellings (5.6%). | Phase 1: case studies only. Revisit after v1; a model would need strong assumptions. | Decided (D1); revisit |
| C2 | Which 6–8 case-study municipalities? | Case studies ground the index and test the archetypes. | Shortlist after Phase 0 using data; ensure coverage of high/low risk, high/low activation, high/low capacity. | Open |
| C3 | Should the buyer-facing summary be produced at all? | D8 makes it a derivative, not the core. | Decide after v1; keep it descriptive and non-advisory. | Open |
| C4 | Should the project include a policy brief? | Useful for policymakers; may be a better dissemination product than a long report. | Consider a 2-page brief alongside the report. | Open |
| C5 | Should the project include a forecasting component? | Overlaps JRI/TCU; adds complexity. | Not in Phase 1; revisit after v1. | Decided (out of scope) |
| C6 | Should the project attempt a causal evaluation of the 2023 Act? | The brief says no unless a clean natural experiment emerges. | Keep descriptive; revisit only if a credible identification strategy appears. | Decided (out of scope) |

---

## D. Communication questions

| # | Question | Why it matters | Next step | Status |
|---|---|---|---|---|
| D1 | How do we explain "other vacant" without implying "abandoned"? | The brief's framing was misleading; the public may repeat it. | Use the glossary and a short definition box in the report; say "residual vacancy" or "other vacant," not "abandoned." | Open |
| D2 | How do we show uncertainty on a map? | A choropleth implies precision. | Use hatch/opacity for low-confidence areas; add error bands in tables; publish a methods note. | Open |
| D3 | How do we avoid investment advice? | The "opportunity" framing can look like a buy signal. | Use "activation potential" and "response capacity"; add disclaimers; no property-level recommendations. | Open |
| D4 | How do we explain the 1,059-unit universe to a general audience? | "Why is my town missing?" will be a common question; 682 towns/villages are absent. | Publish a coverage note and a searchable list of covered/missing municipalities. | Open |
| D5 | How do we present the policy timeline without implying a national akiya tax? | The brief conflated law and proposal. | Use the law/guidance/proposal table from `policy.md`; explicitly say "no national akiya tax." | Open |

---

## E. Decisions still needed

The identity-changing decisions (D1–D3, D8) are resolved. Remaining decisions are reversible or methodological:

- **E1:** Confirm the 6–8 case-study shortlist after Phase 0.
- **E2:** Confirm whether to publish the buyer-facing summary.
- **E3:** Confirm whether to include response capacity in v1 or defer to v2.
- **E4:** Confirm the uncertainty method (simulation vs empirical Bayes vs both).
- **E5:** Confirm whether to request akiya-bank aggregate data from operators.
- **E6:** Confirm whether to use OSM/Overpass at all, given ODbL share-alike.

These can be decided during Phase 0/1; they do not change the project identity.
