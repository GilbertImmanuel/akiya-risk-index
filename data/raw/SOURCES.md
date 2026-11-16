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
