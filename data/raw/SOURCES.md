# Raw Data Sources

## 2023 Housing and Land Survey — table 34-2

- **File:** `estat_34-2_2023_2026-11-16.xlsx`
- **Survey:** 令和5年住宅・土地統計調査 (2023 Housing and Land Survey)
- **Table:** 第34－2表 空き家の種類(4区分)、腐朽・破損の有無(2区分)、建て方(2区分)、構造(2区分)別空き家数－全国、都道府県、市区町村
- **Source:** e-Stat / Statistics Bureau of Japan
- **Database page:** https://www.e-stat.go.jp/dbview?sid=0004021631
- **Download URL:** https://www.e-stat.go.jp/stat-search/file-download?statInfId=000040209901&fileKind=0
- **statInfId:** `000040209901`
- **Access date:** 2026-11-16
- **SHA-256:** `D8CF31401BDA0B51864B1E74A5CD3005C14565656A89B4025FEF4D23189C601A`
- **Size:** 1,337,516 bytes
- **Licence:** e-Stat terms; CC BY 4.0-compatible; attribution required.

### Structure

- One sheet: `e034_2`.
- 9 header rows; 26,943 data rows.
- 1,283 geographic rows: 1 national + 47 prefectures + 1,235 municipal reporting rows.
- 21 rows per region: 3 dilapidation categories × 7 building/structure combinations.
- Column A (`地域識別コード`): hierarchy code (`a` = national/prefecture; `1` = designated city / special-wards group; `0` = ward; `2` = city; `3` = town/village).
- Columns F–J: vacant total, other vacant, rental, sale, secondary.

### Parser

- `src/02_parse_vacancy.py`
- Output: `data/interim/vacancy_2023.csv`
- QA: national totals and hierarchy counts validated; covered vacancy 8,501,240 vs national 9,001,600; uncovered 500,360 (5.6%).

## 2018 Housing and Land Survey — table 35-2

- **File:** `estat_35-2_2018_2026-11-16.xlsx`
- **Survey:** 平成30年住宅・土地統計調査 (2018 Housing and Land Survey)
- **Table:** 第35－2表 空き家の種類(4区分)，腐朽・破損の有無(2区分)，建て方(2区分)，構造(2区分)別空き家数－全国，都道府県，市区町村
- **Source:** e-Stat / Statistics Bureau of Japan
- **File list:** https://www.e-stat.go.jp/stat-search/files?page=1&layout=datalist&lid=000001238098
- **Download URL:** https://www.e-stat.go.jp/stat-search/file-download?statInfId=000031865730&fileKind=0
- **statInfId:** `000031865730`
- **Access date:** 2026-11-16
- **SHA-256:** `3B6687F59B2461B3D8CDC0CB4E3DD4E6B93D19298AAAADEB179A28C9C00CDD0D`
- **Size:** 1,919,651 bytes
- **Licence:** e-Stat terms; CC BY 4.0-compatible; attribution required.

### Structure

- One sheet: `e035_2`.
- 11 header rows; 27,510 data rows.
- 1,310 geographic rows: 1 national + 47 prefectures + 1,262 municipal reporting rows.
- 21 rows per region: 3 dilapidation categories × 7 building/structure combinations.
- Column E = hierarchy code; column F = region; column H = dilapidation; column J = building; column L = structure.
- Count columns M–Q are ordered **total, secondary, rental, sale, other** (different from 2023).
- 2018 covers 271 towns/villages; 2023 covers 244. The difference is partly municipal mergers and partly municipalities falling below the 15,000 reporting threshold.

### Parser

- `src/02_parse_vacancy.py` (generic for 2018 and 2023)
- Output: `data/interim/vacancy_2018.csv`
- QA: national totals and hierarchy counts validated; covered vacancy 8,077,270 vs national 8,488,600; uncovered 411,330 (4.85%).

## Municipal merger and boundary-change history

- **File:** `estat_municipal_mergers_2026-11-16.csv`
- **Source:** e-Stat, 廃置分合等情報
- **Page:** https://www.e-stat.go.jp/municipalities/cities/absorption-separation-of-municipalities
- **Download:** generated from the page's form with `op=download&file_format=csv&charset=UTF-8&bom=1`
- **Access date:** 2026-11-16
- **SHA-256:** `9D34AAC7B05D571D92AFE66AB4C1A226B8CB0CF8052817ECB419FDF9A80D69A0`
- **Size:** 700,270 bytes
- **Rows:** 3,507
- **Licence:** e-Stat terms; CC BY 4.0-compatible; attribution required.

### 2018–2023 check

- 18 entries between 2018-01-01 and 2023-12-31.
- None are municipal mergers; they are city-status changes, a name change, and a town-to-city change.
- The 2018→2023 vacancy-table coverage change is therefore **threshold-driven**, not merger-driven.
- Crosswalk result: 1,056 matched, 1 name change, 29 only in 2018, 2 only in 2023; balanced panel **1,057** units.
