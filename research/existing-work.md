# Existing Work and the Genuine Gap

**Last updated:** 2026-11-12
**Purpose:** Map what has already been done, so the project does not repeat it or claim false novelty. The gap is narrower than the brief assumed.

---

## 1. The short version

A lot of work exists on Japanese housing vacancy. The gap is **not**:

- a national vacancy map;
- a municipal vacancy ranking;
- a driver regression;
- a forecast of future vacancy rates.

The gap is an **open, reproducible, multi-wave municipal panel** that:

1. separates **current blight** from **forward pressure**;
2. reports **uncertainty** explicitly;
3. tests whether **markets already price** the measured risk;
4. publishes **data, code, and provenance**, not just a map or a paper.

That is a narrower but defensible contribution.

---

## 2. Prior work by category

### 2.1 Official statistics and government analysis

| Work | What it does | Limitations for this project |
|---|---|---|
| **Statistics Bureau, Housing and Land Survey** | The authoritative vacancy statistics; municipal tables; 5-year waves. | Sample survey; 15,000+ coverage; no mesh; definitions changed across waves. |
| **MLIT, Vacant Houses Act enforcement survey** | Counts of plans, designations, recommendations, executions; prefecture-level. | No municipal list; enforcement activity is endogenous. |
| **MLIT, Real Estate Information Library** | Transaction and land-price data; API. | Not a census of transactions; rural coverage thin. |
| **JRI (2025), 2040 vacancy forecast** | Prefectural panel (2003–2023) of "other vacant" rates; forecasts to 2043. | Prefectural, not municipal; demand-focused; no market-lag test. |
| **Tokyo Foundation (2025)** | Descriptive municipal analysis; shows why total vacancy misleads (secondary homes). | Descriptive; no composite index or validation. |

### 2.2 Academic work

| Work | Method | Relevance |
|---|---|---|
| **LIXIL (2020), 空き家率関数の推計** | Econometric analysis of vacancy-rate determinants. | Establishes drivers; not a municipal risk index. |
| **ResearchSquare (2026), Luo & Gramalla** | 290 Tokyo-metro municipalities, 2018 and 2023; ESDA + Spatial Durbin; core-periphery; pre-1981 stock as a proxy. | Shows spatial spillovers and mechanism reweighting; metro-only, not a national index. |
| **AIJ literature list** | Extensive Japanese research on vacancy occurrence, management, and policy. | Confirms the field is mature; our contribution must be synthesis/reproducibility, not a first-ever study. |
| **Case studies (various)** | Local determinants, management, and policy evaluation. | Useful for case-study design; not comparable nationally. |

### 2.3 Data journalism and dashboards

| Work | What it does | Limitations |
|---|---|---|
| **Nikkei "ふるさとクリック" vacancy map** | Municipal vacancy-rate map and charts. | Descriptive; single indicator; not an index. |
| **KurashiMap rankings** | Municipal vacancy-rate rankings. | Descriptive; no uncertainty; no composition adjustment. |
| **Tokyo City University "空き家予測マップ"** | ML prediction of 2018/2023/2028 vacancy rates for all municipalities, using census and housing-survey data. | Closest prior product, but single outcome; non-commercial/proprietary; not open/reproducible; no risk/activation separation or market validation. |
| **Akiya-akichi maps** | National/prefectural vacancy maps. | Descriptive; often total vacancy, which is composition-sensitive. |

---

## 3. What the prior work establishes

**Fact / strong evidence:**

- Vacancy is at a record high, but the composition matters more than the headline.
- Secondary residences can make a wealthy resort town look "high-vacancy."
- Demographic factors (death rate, out-migration, in-migration) are associated with "other vacant" rates at prefectural level.
- Old-housing share can be negatively associated with vacancy because old stock is demolished.
- Spatial spillovers and core-periphery patterns matter within metro areas.
- Municipal vacancy estimates are noisy; small places are hard to rank.

**Inference:**

- A single composite "risk" score will hide the distinction between current blight and forward pressure.
- A single "opportunity" score will conflate market demand with policy capacity.
- A map without uncertainty will overclaim precision.

**Hypothesis (to test):**

- Markets lag measured vacancy risk in some places and anticipate it in others; the difference is related to accessibility, demand, and the composition of vacancy.
- Akiya-bank listings are a symptom of marketable vacancy and program participation, not a leading indicator of structural risk.
- Policy designations reflect administrative capacity more than underlying blight.

---

## 4. The gap, stated precisely

> There is no open, reproducible, multi-wave **municipal** panel that separates **current structural vacancy risk** from **forward pressure**, reports **uncertainty**, and tests whether **local housing markets and policy signals already reflect** the measured risk.

The closest products are:

- **Tokyo City University's prediction map** — but it predicts a single vacancy rate, is not open/reproducible, and does not separate risk from activation or validate against market outcomes.
- **JRI's forecast** — but it is prefectural and demand-focused.
- **Tokyo Foundation's analysis** — but it is descriptive.
- **Academic spatial models** — but they are metro-specific and not a public tool.

---

## 5. How this project differs

| Dimension | Prior work | This project |
|---|---|---|
| Geography | National descriptive maps; prefectural panels; metro case studies | 1,059 clean municipal units, with explicit coverage limits and small-municipality case studies |
| Time | Mostly 2018/2023 or prefectural 2003–2023 | 2008–2023 municipal panel, 2003 context, 2025 census demand data |
| Outcome | Total vacancy or a single predicted rate | Dilapidated "other vacant" as headline; broad rate as context |
| Structure | One score or one map | Risk, activation potential, and response capacity as separate lenses |
| Uncertainty | Rarely reported | Simulation/smoothing and rank-stability reporting |
| Validation | Limited | Market-lag test, akiya-bank participation, prefecture-level designations, case studies |
| Openness | Often proprietary or static | Open data, code, data dictionary, provenance, licence notes |
| Policy | Often conflates law and proposal | Explicit law/guidance/proposal separation |

---

## 6. What we should not claim

- **Do not claim** "no one has studied Japanese vacancy." The field is mature.
- **Do not claim** "first national municipal vacancy map." Several exist.
- **Do not claim** causal effects of the 2023 Act. The project is descriptive/correlational.
- **Do not claim** property-level predictions or investment advice.
- **Do not claim** full national coverage. The measured universe is 1,059 clean municipal units; 682 towns/villages and 5.6% of the vacant stock are outside it.

---

## 7. Sources

- Statistics Bureau, 2023 Housing and Land Survey: https://www.stat.go.jp/data/jyutaku/2023/tyousake.html (accessed 2026-11-12).
- MLIT, Vacant Houses Act enforcement survey: https://www.mlit.go.jp/jutakukentiku/house/content/001984996.pdf (accessed 2026-11-12).
- JRI, *2040年代の全国・都道府県別 空き家数・空き家率の推計*: https://www.jri.co.jp/file/report/researchfocus/pdf/15673.pdf (accessed 2026-11-12).
- Tokyo Foundation, *市区町村別に見た日本の空き家の現状*: https://www.tkfd.or.jp/research/detail.php?id=4644 (accessed 2026-11-12).
- LIXIL, *空き家率関数の推計*: https://www.lij.jp/html/jli/jli_2020/2020summer_p117.pdf (accessed 2026-11-12).
- Luo & Gramalla, *Spatiotemporal analysis of spatial heterogeneity and mechanism reweighting in housing vacancy regimes after COVID-19* (ResearchSquare preprint, 2026): https://www.researchsquare.com/article/rs-9484871/latest.pdf (accessed 2026-11-12).
- Tokyo City University prediction map coverage: https://www.projectdesign.jp/articles/news/d6af2736-aacc-4862-ae2c-c4de5fcba13e (accessed 2026-11-12).
- Nikkei "ふるさとクリック" vacancy map: https://vdata.nikkei.com/newsgraphics/regional-regeneration/vacant-house-rate-map/ (accessed 2026-11-12).
- KurashiMap vacancy rankings: https://kurashimap.jp/ranking/vacancy-low (accessed 2026-11-12).
- AIJ vacancy literature list: https://news-sv.aij.or.jp/shien/s2/akiya/chart.html (accessed 2026-11-12).
