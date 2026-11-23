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

## 2025 Census — municipal population and households

### Table 1-2: population 2020, households 2025/2020, area, density

- **File:** `estat_census2025_table1-2_2026-11-16.json`
- **Source:** e-Stat API, 2025 Census table 1-2 (`statsDataId=0004050417`)
- **Access date:** 2026-11-16
- **SHA-256:** `EE52EE6EC75C96C9189353EC2B98A29F2D31C18CCC23F995867FB6A6E2A15BB2`
- **Size:** 1,989,314 bytes
- **Records:** 19,610 (10 indicators × 1,961 areas)
- **Licence:** e-Stat terms; CC BY 4.0-compatible.

### Table 1-1: 2025 population

- **File:** `estat_census2025_table1-1_2026-11-16.json`
- **Source:** e-Stat API, 2025 Census table 1-1 (`statsDataId=0004050397`)
- **Access date:** 2026-11-16
- **SHA-256:** `D8ABC7EB37E2D3510167D231A26F14D9DAC030D7E607271A86FFF98136E1E490`
- **Size:** 373,418 bytes
- **Records:** 1,961 (total population by area)
- **Licence:** e-Stat terms; CC BY 4.0-compatible.

### Discrepancy

The API table's national 2025 population is **123,049,524**, while the summary PDF headline is **122,972,528** (difference **76,996**). The API table is internally consistent with its 2020 baseline and five-year change. Use the API table for municipal joins; cite the headline separately and note the difference. The cause is not yet established (possible tabulation/universe difference).

## Municipal fiscal strength index (FY2022)

- **File:** `estat_ssdse_fiscal_2022_2026-11-17.json`
- **Source:** e-Stat API, Social and Demographic Statistics System (SSDSE), table D 行政基盤 (`statsDataId=0000020204`), indicator `D2201_財政力指数（市町村財政）`
- **Fiscal year:** 2022 (`cdTime=2022100000`)
- **Access date:** 2026-11-17
- **SHA-256:** `9AA33FE168974AD210AB67E1501EB51885AA10ABCA9C3BF23947EB3209A610BB`
- **Size:** 385,779 bytes
- **Rows:** 1,913 areas
- **Licence:** e-Stat terms; CC BY 4.0-compatible.

### Notes

- FY2023 and FY2024 return no data in this table; FY2022 is the latest available.
- 195 areas have no index: all 195 are wards (171 designated-city wards + 23 special wards + 1 special-wards group). The index is municipal, not ward-level.
- Coverage in the 2023 analysis universe: **1,036 of 1,059 units (97.8%)**; the only missing units are the 23 special wards.

## Total-dwelling tables (2023 and 2018)

### 2023 table 1-2-1

- **File:** `estat_2023_table1-2-1_2026-11-23.json`
- **Source:** e-Stat API, 2023 Housing and Land Survey table 1-2-1 (`statsDataId=0004021421`)
- **Access date:** 2026-11-23
- **SHA-256:** `333673980F872AB3A77E53F914C892FFD35455D5D6C07301FBA73ADA5358EEA3`
- **Size:** 1,749,881 bytes
- **Rows:** 15,396 (12 categories × 1,283 areas)
- **Licence:** e-Stat terms; CC BY 4.0-compatible.

### 2018 table 1-2-1

- **File:** `estat_2018_table1-2-1_2026-11-23.json`
- **Source:** e-Stat API, 2018 Housing and Land Survey table 1-2-1 (`statsDataId=0003355290`)
- **Access date:** 2026-11-23
- **SHA-256:** `5D84E3CF44F414865BE83074423B0D0E216536FE14FA33146A9E07EF6AA27432`
- **Size:** 1,785,570 bytes
- **Rows:** 15,720 (12 categories × 1,310 areas)
- **Licence:** e-Stat terms; CC BY 4.0-compatible.

### Category-code trap

The category codes differ between waves:

- 2023: `221` = other vacant, `222` = rental, `223` = sale, `224` = secondary.
- 2018: `221` = secondary, `222` = rental, `223` = sale, `224` = other vacant.

Map by code per year, not by position.

### Validation

| | 2023 | 2018 |
|---|---:|---:|
| Total dwellings | 65,046,700 | 62,407,400 |
| Vacant total | 9,001,600 | 8,488,600 |
| Other vacant | 3,856,000 | 3,487,200 |
| Clean-unit coverage | 1,059/1,059 | 1,086/1,086 |
| Vacancy-count mismatches vs 34-2/35-2 | 0 | 0 |

**Coverage of national totals (2023 clean units):** total dwellings 96.6%; vacant 94.4%; other vacant 91.5%; dilapidated other vacant **90.0%**.

**Important:** the 682 missing municipalities hold **327,880 other vacant (8.5%)** and **89,240 dilapidated other vacant (10.0%)**. The risk measure has a larger coverage gap than the headline vacancy count.
