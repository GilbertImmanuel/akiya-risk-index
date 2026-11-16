# Decision Log

**Last updated:** 2026-11-12
**Purpose:** Record material changes to the brief, with date, old approach, new approach, evidence, and rationale. Reversible choices are logged here too, but identity-changing choices are marked clearly.

---

## User context

The user comes from an **IT background** with no housing or real-estate experience and prefers the **safer option** when a trade-off is uncertain. This has three consequences:

1. **Define terms plainly.** Housing statistics and Japanese policy terms are not assumed knowledge.
2. **Prefer robust, transparent methods** over clever but fragile ones.
3. **Do not overclaim.** A narrower, well-documented scope is better than a national ranking with hidden coverage bias.

---

## Identity-changing decisions (accepted 2026-11-12)

| ID | Old approach (brief) | New approach | Evidence | Rationale | Status |
|---|---|---|---|---|---|
| **D1** | National municipal index for all cities, wards, towns, and villages; smaller villages may need prefectural aggregates | **1,059 clean municipal units (from 1,235 reporting rows) + 6–8 small-municipality case studies** | The 1,235 rows double-count designated cities and their wards; the clean universe is 1,059 units. 682 towns/villages (73.6%) are absent and hold 500,360 vacant dwellings (5.6%). | A national ranking would silently omit the most vacancy-prone places and 5.6% of the vacancy stock. A defined universe plus case studies is honest and feasible. | Accepted |
| **D2** | Interactive map + short report for buyers, researchers, and policymakers | **Interactive map + open data/code + short report/methodology**, aimed at researchers and policymakers; buyer summary as a derivative | Prior maps exist; the gap is reproducibility, uncertainty, and validation. A buyer's guide would exceed the data and create advice risk. | Focus on the research/policy contribution; keep the buyer lens secondary. | Accepted |
| **D3** | Single "risk and opportunity" index | **Risk as the core; activation potential and response capacity as separate lenses** | Risk (blight/pressure) and opportunity (market demand) are different constructs; fiscal capacity is a third. A single net score hides the policy-relevant cases. | Separate lenses are more interpretable and more useful for policy triage. | Accepted |
| **D8** | Buyers, researchers, and local policymakers equally | **Researchers and policymakers primary**; buyer-facing summary as a derivative | The data are strongest for research/policy questions; buyer advice would require property-level and market data we do not have. | Safer and more defensible. | Accepted |

---

## Reversible decisions (accepted 2026-11-12)

| ID | Old approach | New approach | Evidence | Rationale | Status |
|---|---|---|---|---|---|
| **D4** | Vacancy 2003–2023 (five waves) | **2008–2023 core (four waves); 2003 as context**; demography 2000–2025; market 2005–2026 | 2003 predates the Heisei mergers and has greater definitional/coverage risk; 2008–2023 is more comparable | Reduces harmonisation risk without losing the recent trend. | Accepted |
| **D5** | Equal, PCA, and policy weights, undecided headline | **Equal weights headline**; PCA and policy weights as sensitivity | Equal weights are transparent and easy to explain; PCA/policy are checks, not the headline | Safer for a first version; sensitivity still reported. | Accepted |
| **D6** | Assess akiya-bank scraping or structured collection | **Official aggregates + participation lists + manual case-study counts; no scraping** | Portals block automated access (403/CloudFront); listings are ~0.2% of vacant stock; participation is 65.5% | Scraping is legally/technically fragile and the data are not a vacancy census. | Accepted |
| **D7** | 5–10 case studies | **6–8 case studies**, selected after Phase 0 | Depth vs breadth; 6–8 allows coverage of archetypes without overextending | Balanced. | Accepted |

---

## Method decisions (logged, not user-facing)

| Decision | Choice | Why |
|---|---|---|
| Headline risk measure | **Dilapidated "other vacant" detached houses per 1,000 dwellings** | Closest available proxy to blight; uses a published municipal variable; avoids treating all "other vacant" as abandoned. |
| Broad vacancy measure | Report as context, not headline | Composition-sensitive; secondary homes can dominate. |
| Current vs pressure | Separate sub-indices; composite as a summary | Avoids mixing stock and flow; easier to explain. |
| Uncertainty | Simulation and/or empirical-Bayes smoothing; rank-stability reporting | Survey estimates are noisy; rankings need error bands. |
| Coverage | 1,059 clean municipal units; 682 missing towns/villages (500,360 vacant dwellings) as a separate track | Honest scope; avoids a misleading national map. |
| Policy variables | Descriptive context, not validation | Designations are endogenous to administrative capacity. |
| Akiya-bank variables | Participation dummy + aggregate trend + manual case-study counts | No scraping; avoids treating listings as vacancy. |
| Pilot prefectures | Tokyo, Nagano, Kochi | Contrasting demand, secondary-home, and rural/thin-market conditions. |

---

## Detailed rationale

### D1 — Why not all municipalities?

The 2023 municipal table's geographic dimension has 1,283 items: 1 national row, 47 prefectures, and 1,235 municipal reporting rows. The 1,235 rows are not a clean municipality count: they include 792 cities (20 designated + 772 non-designated), 23 special wards, 244 towns/villages, 175 designated-city wards, and 1 Tokyo special-wards group. The clean analysis universe is 1,059 units (792 + 23 + 244). Japan has 926 towns/villages, so 682 (73.6%) are absent; those missing municipalities hold 500,360 vacant dwellings (5.6% of the national total).

The missing places are not a random sample. They are small, rural, and often have high vacancy. A national ranking that excludes them would be biased in the direction of understating the problem. The honest options are:

- restrict the index to the measured universe and say so;
- model the missing places with strong assumptions;
- use prefectural aggregates;
- do case studies.

We chose the first plus case studies. Modelling 682 municipalities would require a separate project and would produce false precision.

### D2 — Why not a buyer's guide?

A buyer's guide would need:

- property-level condition and legal status;
- local market liquidity and price data at a finer geography than we have;
- renovation costs, seismic risk, and tax/legal advice;
- a clear separation of information from recommendation.

The available data are municipal and sample-based. A buyer's guide would overreach. A research/policy tool is more defensible and still useful.

### D3 — Why separate activation and capacity?

"Opportunity" is ambiguous. For a buyer, it means expected return; for a policymaker, it means the ability to reuse the stock; for a municipality, it means fiscal/administrative capacity. Combining them into one score hides the trade-offs.

The project will report:

- **Risk** — current blight + forward pressure.
- **Activation potential** — accessibility, demand, price momentum, liquidity.
- **Response capacity** — fiscal strength, plan adoption, support corporations.

The policy matrix (risk × capacity) and the market matrix (risk × activation) are different views of the same municipalities. That is a feature, not a bug.

### D6 — Why no akiya-bank scraping?

The portals blocked automated requests during the audit (403/CloudFront). The terms do not support scraping. The data are also a poor fit: 20,089 current listings against 9.0m vacant dwellings, with duplicates across two operators and owner-consent selection. Scraping would be fragile, legally risky, and analytically misleading. Official aggregates, participation lists, and manual case-study counts are sufficient for the questions we can answer.

---

## Open decisions (reversible)

| ID | Question | Options | Recommendation | Status |
|---|---|---|---|---|
| E1 | Case-study shortlist | 6–8 from the candidate list | Select after Phase 0 using data | Open |
| E2 | Buyer-facing summary | Yes / no / later | Later, as a derivative | Open |
| E3 | Capacity in v1 | Include / defer | Include as an overlay if time allows | Open |
| E4 | Uncertainty method | Simulation / empirical Bayes / both | Both, with simulation as the minimum | Open |
| E5 | Request akiya-bank aggregates | Yes / no | Yes, as a supplement; do not block on it | Open |
| E6 | OSM/Overpass | Use / avoid | Use only if needed; isolate ODbL layers | Open |

---

## Format for future entries

When a material change is made, add a row with:

- **Date**
- **Decision ID**
- **Old approach**
- **New approach**
- **Evidence** (source + what it showed)
- **Rationale**
- **Reversible?** (yes/no)
- **Status** (proposed/accepted/rejected/superseded)

Do not overwrite old entries. If a decision is reversed, mark it `superseded` and add a new row.
