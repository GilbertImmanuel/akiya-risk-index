# Raw Source Notes

**Last updated:** 2026-11-12
**Purpose:** Exact excerpts, table numbers, and source details for reproducibility. This file is intentionally closer to the sources than the synthesised notes.

---

## 1. 2023 Housing and Land Survey — confirmed summary

**Source:** Statistics Bureau of Japan, *令和5年住宅・土地統計調査 住宅及び世帯に関する基本集計（確報集計）結果の要約*.
**URL:** https://www.stat.go.jp/data/jyutaku/2023/pdf/kihon_gaiyou.pdf (accessed 2026-11-12).

Exact figures:

- Total dwellings: **65,047,000**.
- Vacant dwellings: **9,002,000**.
- Vacancy rate: **13.8%**.
- "Other vacant" (賃貸・売却用及び二次的住宅を除く空き家): **3,856,000**.
- "Other vacant" rate: **5.9%**.
- Rental vacancy: **4,436,000**.
- For-sale vacancy: **326,000**.
- Secondary residences: **384,000**.
- Five-year change in vacant dwellings: **+513,000**.
- Five-year change in "other vacant": **+369,000**.
- Of "other vacant": **2,851,000 detached**, 848,000 apartments, 137,000 row houses.
- 4,753,000 households own a dwelling other than their current home; 1,416,000 own a vacant dwelling; 47.5% of owner-owned vacant dwellings are "other vacant."

Trend table (from the same source):

| Year | Total dwellings (000) | Vacant (000) | Vacancy rate (%) | Other vacant (000) |
|---:|---:|---:|---:|---:|
| 2003 | 53,891 | 6,593 | 12.2 | 2,118 |
| 2008 | 57,586 | 7,568 | 13.1 | 2,681 |
| 2013 | 60,629 | 8,196 | 13.5 | 3,184 |
| 2018 | 62,407 | 8,489 | 13.6 | 3,487 |
| 2023 | 65,047 | 9,002 | 13.8 | 3,856 |

**Note:** The preliminary 2023 release had 65,021,000 dwellings, 8,995,000 vacant, and +507,000. The confirmed release supersedes these. Use the confirmed figures.

---

## 2. Definitions — exact passages

**Source:** Statistics Bureau, *令和5年住宅・土地統計調査 用語の解説*.
**URL:** https://www.stat.go.jp/data/jyutaku/2023/pdf/yougo.pdf (accessed 2026-11-12).

### "Other vacant"

> 賃貸・売却用及び二次的住宅を除く空き家：賃貸用の空き家、売却用の空き家及び二次的住宅以外の人が住んでいない住宅で、例えば、転勤・入院などのため居住世帯が長期にわたって不在の住宅や建て替えなどのために取り壊すことになっている住宅など（注：空き家の種類の判断が困難な住宅を含む。）

**Translation:** Vacant dwellings other than rental, for-sale, and secondary: dwellings with no resident other than those categories, for example dwellings whose resident household is absent long-term due to transfer or hospitalisation, or dwellings scheduled for demolition for rebuilding, etc. (Note: includes dwellings whose vacancy type is difficult to classify.)

### "Ruined house"

> なお、いわゆる「廃屋」については、そのままではそこで家庭生活を営むことが困難なことから、この調査では住宅としていない。

**Translation:** So-called "ruined houses" are not treated as dwellings in this survey because it would be difficult to carry on ordinary family life there as they are.

### "Vacant house"

> 居住世帯のない住宅のうち、一時現在者のみの住宅及び建築中の住宅を除いたもの。

**Translation:** Dwellings with no resident household, excluding dwellings with only temporary occupants and dwellings under construction.

### Vacancy duration

The survey asks `居住世帯のない期間` only in the **乙 survey** for **owner-owned dwellings other than the current home**; it is not a full vacancy-duration variable for all vacant dwellings. There is no municipal vacancy-duration table.

### Mesh statistics

The survey is a sample survey and does **not** produce 1 km mesh vacancy statistics. The Statistics Bureau's FAQ and the survey documentation confirm this.

---

## 3. Municipal table and coverage

**Source:** e-Stat, 2023 table 34-2.
**URL:** https://www.e-stat.go.jp/dbview?sid=0004021631 (accessed 2026-11-12).

Table title:

> 空き家の種類(4区分)、腐朽・破損の有無(2区分)、建て方(2区分)、構造(2区分)別空き家数－全国、都道府県、市区町村

Geographic dimension:

- 1,283 items total;
- 1 national row (`00000`);
- 47 prefectures;
- **1,235 municipal reporting units**.

Coverage calculation (verified by parsing table 34-2 on 2026-11-16):

The first Excel column (`地域識別コード`) encodes the hierarchy:

- `a` = national / prefecture (48 regions)
- `1` = designated city + Tokyo special-wards group (21 regions)
- `0` = ward (198 regions: 175 designated-city wards + 23 special wards)
- `2` = non-designated city (772 regions)
- `3` = town / village (244 regions)

The 1,235 municipal reporting rows are **not a clean municipality count**:

- 792 cities (20 designated + 772 non-designated)
- 23 special wards
- 244 towns/villages
- 175 designated-city wards (duplicate city-level rows)
- 1 Tokyo special-wards group (duplicate of the 23 special wards)
- = 1,235.

Clean analysis universe:

- 792 cities + 23 special wards + 244 towns/villages = **1,059 units**.
- Duplicate rows excluded: 175 + 1 = 176; 1,059 + 176 = 1,235.

Coverage:

- Japan has 926 towns/villages (743 towns + 183 villages).
- Covered: 244; missing: **682 (73.6%)**.
- Covered vacancy: **8,501,240**.
- National vacancy: **9,001,600**.
- Uncovered vacancy: **500,360 (5.6%)**.
- Covered share: **94.4%**.

National risk measure:

- Dilapidated "other vacant": **895,300** (23.2% of 3,856,000).
- Dilapidated detached "other vacant": **715,000**.

### 2018 table 35-2 — national totals and layout

**Source:** e-Stat, 2018 table 35-2.
**File list:** https://www.e-stat.go.jp/stat-search/files?page=1&layout=datalist&lid=000001238098
**Download:** https://www.e-stat.go.jp/stat-search/file-download?statInfId=000031865730&fileKind=0

National totals (2018):

- Total vacant: **8,488,600**.
- "Other vacant": **3,487,200**.
- Rental: **4,327,200**.
- For sale: **293,200**.
- Secondary: **381,000**.
- Dilapidated "other vacant": **1,006,000** (28.8%).
- Dilapidated detached "other vacant": **799,900**.

Layout differences from 2023:

- 11 header rows; 17 columns.
- Hierarchy in column E, region in F, dilapidation in H, building in J, structure in L.
- Count columns M–Q are ordered **total, secondary, rental, sale, other** (2023 is total, other, rental, sale, secondary).
- Building labels: `00_総数`, `11_一戸建`, `20_長屋建・共同住宅・その他`.
- 2018 covers **1,086 clean municipal units** (271 towns/villages); 2023 covers **1,059** (244 towns/villages).
- 2018 covered vacancy: **8,077,270 (95.2%)**; uncovered **411,330 (4.85%)**.
- **Crosswalk:** 1,056 matched, 1 name change (28221 篠山市→丹波篠山市), 29 only in 2018, 2 only in 2023; balanced panel **1,057**.
- **Merger check:** e-Stat merger history shows 18 status changes in 2018–2023 but **no municipal mergers**; the coverage change is threshold-driven.

**2018 → 2023 comparison:**

| Indicator | 2018 | 2023 | Change |
|---|---:|---:|---:|
| "Other vacant" | 3,487,200 | 3,856,000 | +368,800 (+10.6%) |
| Dilapidated "other vacant" | 1,006,000 | 895,300 | −110,700 (−11.0%) |
| Dilapidated share | 28.8% | 23.2% | −5.6 pp |
| Dilapidated detached "other vacant" | 799,900 | 715,000 | −84,900 (−10.6%) |

**Caveat:** the decline in measured dilapidation is partly attributed to `廃屋` attrition — the worst structures leaving the survey universe — alongside policy and redevelopment effects. See Daiwa Real Estate Appraisal (2024) for the three-channel discussion.

### Wave-specific table numbers

| Wave | Table | Notes |
|---|---|---|
| 2023 | 34-2 | 4 categories; dilapidation; building type; structure. |
| 2018 | 35-2 | Same structure; label `その他の住宅`. |
| 2013 | 53 | `市区` table; separate `町村` table needed. |
| 2008 | 043-1 | 5 categories; needs reconciliation. |

---

## 4. Sample design

**Sources:** Statistics Bureau survey documentation; 2023 survey summary; e-Stat survey plan.
**URLs:** https://www.stat.go.jp/data/jyutaku/2023/pdf/g_sui.pdf ; https://www.stat.go.jp/data/jyutaku/2023/pdf/kihon_gaiyou.pdf

Exact points:

- About **200,000 unit districts**.
- About **17 dwellings per unit district**.
- About **3.4 million dwellings/households** in the sample.
- Roughly **5% of the dwelling stock**.
- Target standard error: **5% for cities**, **10% for towns/villages with 15,000+ population**.
- The survey is a stratified two-stage sample; municipal figures are estimates.

---

## 5. Policy timeline — exact dates and status

**Source:** MLIT, *空家等対策の推進に関する特別措置法関連情報*.
**URL:** https://www.mlit.go.jp/jutakukentiku/house/jutakukentiku_house_tk3_000035.html (accessed 2026-11-12).

Exact markers:

- **【令和５年12月13日施行】** 空家等対策の推進に関する特別措置法の一部を改正されました。
- **【令和８年９月３日施行】** 「地域の自主性及び自立性を高めるための改革の推進を図るための関係法律の整備に関する法律」の施行に伴い空家等対策の推進に関する特別措置法の一部が改正されました。

**2023 amendment page:** https://www.mlit.go.jp/jutakukentiku/house/jutakukentiku_house_tk3_000138.html

**2025 enforcement survey:** https://www.mlit.go.jp/jutakukentiku/house/content/001984996.pdf

---

## 6. Tax treatment — exact law excerpt

**Source:** MLIT, *地方税法（抄）*.
**URL:** https://www.mlit.go.jp/jutakukentiku/house/content/002019832.pdf (accessed 2026-11-12).

> 第三百四十九条の三の二 専ら人の居住の用に供する家屋又はその一部を人の居住の用に供する家屋で政令で定めるものの敷地の用に供されている土地で政令で定めるもの（前条（第十一項を除く。）の規定の適用を受けるもの並びに空家等対策の推進に関する特別措置法（平成二十六年法律第百二十七号）第十三条第二項の規定により所有者等（同法第五条に規定する所有者等をいう。以下この項において同じ。）に対し勧告がされた同法第十三条第一項に規定する管理不全空家等及び同法第二十二条第二項の規定により所有者等に対し勧告がされた同法第二条第二項に規定する特定空家等の敷地の用に供されている土地を除く。…）

**Meaning:** the residential-land exception does not apply to land under a `管理不全空家等` or `特定空家等` for which a **勧告** has been issued.

**Tax rates:**

- Small residential land (≤200 m²): fixed-asset tax base **1/6**; urban-planning tax base **1/3**.
- General residential land (>200 m²): fixed-asset tax base **1/3**; urban-planning tax base **2/3**.
- After a recommendation: excluded from the exception; taxable value can revert to full.

**Caveat:** the final tax bill may rise by less than the tax-base change because of burden-adjustment measures and municipal ordinances.

---

## 7. Enforcement statistics

**Source:** MLIT, *空家等対策の推進に関する特別措置法の施行状況等について（令和7年3月31日時点）*.
**URL:** https://www.mlit.go.jp/jutakukentiku/house/content/001984996.pdf (accessed 2026-11-12).

Key figures:

- Survey universe: **1,741 municipalities**.
- `管理不全空家等` guidance: **3,211 cases (185 municipalities)**.
- `管理不全空家等` recommendations: **378 cases (40 municipalities)**.
- FY2023: 666 guidance, 0 recommendations.
- FY2024: 2,545 guidance, 378 recommendations.
- Vacant-house plans: **1,541 municipalities (88.5%)**.
- Support corporations: **95 corporations (64 municipalities)**; 120 more under consideration in 98 municipalities.
- Promotion zones: **4 zones (4 cities)**; 36 more under consideration in 27 municipalities.
- `特定空家等` cumulative: 42,768 advice/guidance cases (875 municipalities); 4,153 recommendations (495); 551 orders (237); 286 administrative executions (175); 592 simplified executions (296); 12 emergency executions (10).
- FY2024 `特定空家等`: 4,026 advice/guidance; 600 recommendations; 101 orders; 71 administrative executions; 81 simplified executions; 9 emergency executions.

---

## 8. 2026 registration obligation

**Source:** Ministry of Justice, *住所等変更登記の義務化特設ページ*.
**URL:** https://www.moj.go.jp/MINJI/minji05_00687.html (accessed 2026-11-12).

Exact points:

- 住所や氏名・名称の変更の日から**2年以内**に登記.
- 正当な理由なく義務に違反した場合、**5万円以下の過料**.
- 義務化前（**令和8年4月1日**より前）の変更も対象; **令和10年3月末**までに登記.
- 「スマート変更登記」制度も開始.

**Note:** This is a registration obligation under the Real Estate Registration Act, not a tax.

---

## 9. Kyoto local tax

**Source:** Kyoto City, *非居住住宅利活用促進税について＜令和12年度課税開始予定＞*.
**URL:** https://www.city.kyoto.lg.jp/gyozai/page/0000296672.html (accessed 2026-11-12).

Exact points:

- 課税開始時期: **令和12年度**（令和12年1月1日の利用状況によるもの）から.
- システム開発の影響で、令和11年度から**1年延期**.
- 対象: 市街化区域内の非居住住宅（その所在地に住所を有する者がいない住宅）.
- 税率: 家屋価値割 **0.7%**; 立地床面積割 **0.15% / 0.3% / 0.6%** depending on value.
- 免税点: 家屋価値割の課税標準額が30万円未満（導入当初5年間は100万円未満）.
- 課税免除: 事業用、賃貸・売却予定、固定資産税非課税/免除、歴史的建造物等.
- 徴収猶予: 所有者の死亡、居住者の死亡等、3年間.

---

## 10. National tax proposal

**Sources:** Jiji Press, Nikkei, Asahi coverage, 11 December 2025; DPFP policy page.
**Status:** private member's bill; not law as of 2026-11-12.

Key points:

- The DPFP submitted a bill to create a **`空室税`** (vacancy tax) on housing without a residential use, aimed at speculative/investment housing in urban areas.
- It is not a rural akiya tax and not a detailed enacted tax design.
- The 2026 tax reform outline does not introduce a national vacancy tax.

---

## 11. MLIT Real Estate Information Library API

**Source:** MLIT, *XIT001 不動産価格（取引価格・成約価格）情報取得API*.
**URL:** https://www.reinfolib.mlit.go.jp/help/apiManual/xit001/ (accessed 2026-11-12).

Exact points:

- `year`: YYYY; transaction prices from **2005** (only Q3/Q4 in 2005); contract prices from **2021**.
- `quarter`: 1–4.
- `city`: municipal code.
- `priceClassification`: transaction vs contract.
- API key: `Ocp-Apim-Subscription-Key`; free application; key must not be shared.
- Attribution required.

---

## 12. Akiya-bank data

**Sources:** MLIT, *空き家・空き地バンク総合情報ページ*; *参画自治体数・物件掲載件数推移*.
**URLs:** https://www.mlit.go.jp/totikensangyo/const/sosei_const_tk3_000131.html ; https://www.mlit.go.jp/totikensangyo/const/content/002045627.pdf (accessed 2026-11-12).

Exact points (as of October 2026):

- **1,155 participating municipalities**.
- **750 municipalities currently listing**.
- **20,089 current listings** (two operators combined; duplicates exist).
- **~29,000 cumulative transactions**.
- National participation rate: **65.5%**.
- Portal access: automated requests blocked (403/CloudFront); terms do not support scraping.

---

## 13. Coverage-extension notes

- **Municipal vacant-house surveys:** inconsistent definitions, years, and quality; useful for case studies, not a national panel.
- **Fixed-asset tax records:** may allow a housing-surplus proxy, but not a vacancy measure.
- **Tokyo City University prediction map:** predicted 2018/2023/2028 vacancy rates for all municipalities; non-commercial/proprietary; use only as a reference, not as input.
- **Microdata:** application/approval process; disclosure control; not a quick fix.

---

## 14. Discrepancies and unresolved items

| Item | What we saw | Resolution |
|---|---|---|
| Five-year vacancy increase | 507k preliminary vs 513k confirmed | Use **513k**. |
| Total dwellings | 65.02m brief vs 65.047m confirmed | Use **65,047,000**. |
| Vacant dwellings | 9.0m brief vs 9.002m confirmed | Use **9,002,000**. |
| "Other vacant" meaning | Brief: abandoned/inherited/unusable | Survey: residual category; use **dilapidated other vacant** as risk proxy. |
| 2023 Act "designation" | Brief: designate poorly managed houses | Statute: determination + guidance/recommendation; tax trigger is the **勧告**. |
| "6x tax" | Media shorthand | Taxable value up to **6x**; actual bill may rise less. |
| 2026 "akiya tax" | Media/policy debate | No national akiya tax; DPFP bill not law; Kyoto local tax FY2030; registration obligation separate. |
| Akiya-bank coverage | "National" portal | 1,155 participants / 750 listing / 20,089 listings; not a vacancy census. |
| 2013/2008 comparability | Main tables differ | Table-by-table audit needed; open question A1/A2. |
| Municipal designations | Prefecture-level only | No municipal list; use context/case studies. |
| Rural market coverage | Sparse | Pilot Tokyo/Nagano/Kochi; flag insufficient evidence. |
| 2026 amendment detail | MLIT page + secondary commentary | Read the amended statute; do not overstate. |
| Tax assessment timing | 1 January base date | Confirm exact transition in Phase 0. |
