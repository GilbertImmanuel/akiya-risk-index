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

## KSJ N03 — administrative boundaries (2023-01-01)

- **File:** `ksj_N03_2023.zip`
- **Dataset:** 国土数値情報 N03 行政区域, 2023年（令和5年）版
- **Vintage:** 2023-01-01
- **Source:** MLIT, National Land Information Division
- **Data list:** https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-N03-2023.html
- **Download URL:** https://nlftp.mlit.go.jp/ksj/gml/data/N03/N03-2023/N03-20230101_GML.zip
- **Access date:** 2026-11-23
- **SHA-256:** `D0CF37CF450438A62B14007179CBC7BD47B085F20465F6A32F7EAAD8AC962E7A`
- **Size:** 448,421,619 bytes
- **Licence:** Open data (CC BY 4.0) for 2018 onward; attribution required.

### Structure

- GML zip also contains a shapefile and GeoJSON; the shapefile was used for speed.
- 122,929 polygons; 1,917 unique 5-digit codes.
- Fields: `N03_001` prefecture, `N03_002` subprefecture, `N03_003` county/designated-city name, `N03_004` municipality/ward name, `N03_007` administrative code.
- CRS: JGD2011 (EPSG:6668). DBF attribute encoding is Shift-JIS (`cp932`).

### Parser and outputs

- `src/09_municipal_boundaries.py`
- Outputs: `data/interim/municipal_boundaries.gpkg` (1,059 dissolved units), `data/interim/municipal_area.csv`, `data/interim/ward_to_city_2023.csv`.
- Designated-city wards dissolved into their city; 23 special wards kept separate; `所属未定地` rows excluded.
- **QA:** 1,059/1,059 panel units, 0 missing, 0 zero-area. Area ratio vs census: median 1.0000, min 0.959 (みやき町), max 1.114 (潟上市), consistent with boundary/reclamation vintage differences.

## KSJ N02 — railway stations and lines (FY2023)

- **File:** `ksj_N02_2023.zip`
- **Dataset:** 国土数値情報 N02 鉄道, 2023年度（令和5年度）版
- **Vintage:** as of 2023-12-31
- **Data list:** https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-N02-2023.html
- **Download URL:** https://nlftp.mlit.go.jp/ksj/gml/data/N02/N02-23/N02-23_GML.zip
- **Access date:** 2026-11-23
- **SHA-256:** `E91ECDEE90966877C6119AB94DC92EE6562EB9D89194F8A0A91F71B179C82A40`
- **Size:** 17,518,918 bytes
- **Licence:** Open data (CC BY 4.0) since 2020; attribution required.

### Structure

- `Station` layer: 10,240 LineString records; 10,160 station codes; 9,059 group codes.
- Fields: `N02_001` rail type, `N02_002` operator type, `N02_003` line name, `N02_004` operator, `N02_005` station name, `N02_005c` station code, `N02_005g` group code.
- Station geometries are short platform segments, not points; a representative point is taken after grouping.
- CRS: JGD2011 (EPSG:6668); UTF-8 GeoJSON extracted from the zip.

### Parser and outputs

- `src/10_stations.py`
- Outputs: `data/interim/stations.csv`, `data/interim/stations.geojson` (9,007 facilities).
- Rail types excluded: `13` funicular (鋼索鉄道) and `17` trolleybus (無軌条鉄道).
- `station_count` headline excludes tram-only stops (`21` 軌道); tram stops are reported separately.
- **QA:** 10,240 records → 10,184 after exclusions → 9,007 facilities; 8,399 heavy-rail facilities and 608 tram-only stops.

## KSJ S12 — station passengers (FY2023)

- **File:** `ksj_S12_2023.zip`
- **Dataset:** 国土数値情報 S12 駅別乗降客数, 2023年度（令和5年度）版
- **Vintage:** FY2023 (file `S12-24`, compiled 2024)
- **Data list:** https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-S12-2023.html
- **Download URL:** https://nlftp.mlit.go.jp/ksj/gml/data/S12/S12-24/S12-24_GML.zip
- **Access date:** 2026-11-23
- **SHA-256:** `37E7B9B39586C324B70267A9E7118C9FA8D73AA2A8CC7C5E32665B8BD80E974F`
- **Size:** 6,244,895 bytes
- **Licence:** Open data (CC BY 4.0); attribution required.

### Structure

- 10,531 LineString records; 10,182 station codes; 9,076 group codes.
- Identifiers: `S12_001` station name, `S12_001c` station code, `S12_001g` group code, `S12_002` operator, `S12_003` line, `S12_004` rail type, `S12_005` operator type.
- Per-year blocks of four fields: duplicate code, data-existence code, notes, passengers. FY2023 = `S12_054`–`S12_057`.
- `S12_054` duplicate code: `1` listed at this line's station, `2` listed at another line's station, `3` no station.
- `S12_055` data-existence code: `1` data present, `2` no data, `3` not public, `4` no station.
- **Trap:** no-data records store `0`, not null. Only records with duplicate code `1` and existence code `1` are summed.

### Parser and outputs

- `src/10_stations.py`
- Join by station group code; group sums are operator-level, not unique traveller counts.
- **QA:** 8,134 valid FY2023 records, 1,268 no-data records, 255 no-station records, 874 records listed under another line; total **117,888,360** daily passengers. Passenger data missing for **1,274 of 9,007** facilities (14.1%); heavy-rail station coverage in the panel is **6,536 / 7,479 (87.4%)**.
- **Definition:** 乗降客数 counts **boardings + alightings**, not unique travellers. Per-capita values can exceed 1 in employment centres (e.g., 千代田区 68) because residents are few relative to commuters.

### Combined accessibility outputs

- `src/11_accessibility.py`
- `data/processed/accessibility_2023.csv` — 1,059-unit unit-level table.
- `data/processed/panel_with_accessibility_2023.csv` — vacancy panel plus accessibility.
- `data/processed/pilot_panel_v2.csv` — 89-unit pilot.
- `data/interim/station_assignments.csv` — station-to-municipality assignment log.
- `outputs/accessibility_validation.txt`, `outputs/zero_station_municipalities.csv` — QA.

### Notes and caveats

- N02 station points are representative points of platform segments. 375 panel stations lie within 100 m of a municipal boundary; 48 within 1 m. Assignment uses the containing polygon; one station (大井競馬場前, Tokyo Monorail) needed a nearest-polygon fallback at 1.42 km.
- 924 stations fall in the 682 out-of-scope municipalities and are excluded from the panel.
- 126 of 1,059 units (11.9%) have no heavy-rail station; 15 of these have a rail line crossing the polygon but no station. This is a real access measure, not a data failure.
- Passenger data are secondary: JR Hokkaido/Tohoku unmanned stations and JR Kyushu stations outside the top 300 are missing. Use `passenger_data_share` before comparing `passengers_per_capita`.

## 2013 Housing and Land Survey — table 53

- **File:** `estat_vacancy_2013_2026-11-25.json`
- **Survey:** 平成25年住宅・土地統計調査 (2013 Housing and Land Survey)
- **Table:** 第53表 空き家の種類(4区分)，腐朽・破損の有無(2区分)，建て方(2区分)，構造(2区分)別空き家数―市区
- **Source:** e-Stat API, `statsDataId=0003100835`
- **Access date:** 2026-11-25
- **SHA-256:** `EB3F6F2A1E4BBFF5369399101ABF9D468F6C84F4E39FEA36827FDEB005DCE91B`
- **Size:** 17,025,550 bytes
- **API rows:** 103,740
- **Areas:** 988 (市区 only; cities and wards, no towns/villages)
- **Licence:** e-Stat terms; CC BY 4.0-compatible; attribution required.

### Structure

- `cat01` = dilapidation (`00000` total, `00001` dilapidated, `00002` not)
- `cat02` = structure (`00000` total, `00002` wooden, `00005` non-wooden)
- `cat03` = building type (`00000` total, `00001` detached, `00004` terraced/apartment/other)
- `cat04` = vacancy type (`00000` total, `00001` secondary, `00004` rental, `00005` sale, `00006` other)
- `cat05` = vacant households (total only)

### Parser and outputs

- `src/12_vacancy_context.py`
- Outputs: `data/interim/vacancy_2013.csv`, `data/processed/vacancy_context_2008_2023.csv`, `outputs/vacancy_comparability.txt`.
- **Validation:** 812/815 target city/ward units; 3 missing units (滝沢市, 那珂川市, 富谷市) were towns/villages in 2013. Composition checks pass. 2013 vs 2018 vacant-count correlation **0.995**; median ratio **0.942**.

## 2008 Housing and Land Survey — table 043-2

- **File:** `estat_vacancy_2008_2026-11-25.json`
- **Survey:** 平成20年住宅・土地統計調査 (2008 Housing and Land Survey)
- **Table:** 第043-2表 空き家の種類(4区分)，腐朽・破損の有無(2区分)，建て方(2区分)，構造(2区分)別空き家数―市区
- **Source:** e-Stat API, `statsDataId=0003010419`
- **Access date:** 2026-11-25
- **SHA-256:** `19157BDC7CC3B73FB5ACAC9073B8AC30D004B17F898C6BA883A501987FCA320C`
- **Size:** 13,556,422 bytes
- **API rows:** 101,850
- **Areas:** 970 (市区 only; cities and wards, no towns/villages)
- **Licence:** e-Stat terms; CC BY 4.0-compatible; attribution required.

### Structure

- `cat01` = dilapidation (`00` total, `01` dilapidated, `02` not)
- `cat02` = vacancy type (`00` total, `01` secondary, `04` rental, `05` sale, `06` other)
- `cat03` = building type (`00` total, `02` detached, `05` terraced/apartment/other)
- `cat04` = structure (`00` total, `01` wooden, `02` non-wooden)

### Parser and outputs

- `src/12_vacancy_context.py`
- Outputs: `data/interim/vacancy_2008.csv`, `data/processed/vacancy_context_2008_2023.csv`, `outputs/vacancy_comparability.txt`.
- **Validation:** 805/815 target city/ward units; 10 missing units were towns/villages in 2008. Five units have ±20-dwelling composition rounding differences. 2008 vs 2018 vacant-count correlation **0.990**; median ratio **0.857**.

### Decision

- **2013:** usable as city/ward context with boundary flags.
- **2008:** usable as city/ward context with stronger boundary flags; do not impute the 10 units that were not 市区 in 2008.
- **Do not build a four-wave municipal panel.** The 2018–2023 panel remains the core; 2008/2013 are context only.
- **Caveat:** rates are not computed for 2008/2013 because these tables do not include total dwellings. The context file reports counts and composition shares.
