# Processed data

## Market panel

`market_panel.csv` is the long market panel: one row per municipal unit and year (2018 and 2023), 2,118 rows. `panel_with_market.csv` is the wide join to the vacancy and accessibility panel, 1,059 rows. `market_panel_pilot.csv` and `pilot_panel_v3.csv` are the 89-unit Tokyo, Nagano, and Kochi pilot.

### Fields

| Field | Definition |
|---|---|
| `region_code` | Five-digit municipal code for the 2023 analysis unit. Designated-city wards are mapped to their city; special wards stay separate. |
| `year` | 2018 or 2023. |
| `transaction_count_land` | Reported residential land-only transactions. |
| `transaction_count_house` | Reported residential land-and-building transactions. |
| `transaction_count_condo` | Reported residential condominium transactions. |
| `transaction_count` | Sum of the three transaction counts. |
| `transaction_land_median_unit_price_yen_m2` | Median land-only unit price, yen per square metre. |
| `transaction_house_median_price_yen` | Median land-and-building total price, yen. Not a unit price. |
| `transaction_condo_median_unit_price_yen_m2` | Median condominium unit price, yen per square metre. |
| `transaction_liquidity_per_1000_dwellings` | Reported residential transactions per 1,000 dwellings. |
| `l01_price_points` | Residential official land price points (地価公示). |
| `l01_price_median_yen_m2` | Median residential official land price, yen per square metre. |
| `l01_matched_sites` | L01 sites matched between 2018 and 2023. Defined for 2023; blank for 2018. |
| `l01_matched_change_5y_pct` | Median matched-site change, 2018 to 2023, percent. Defined for 2023 only. |
| `l02_price_points` | Residential prefectural land price survey points (都道府県地価調査). Robustness series. |
| `l02_price_median_yen_m2` | Median residential prefectural survey price, yen per square metre. |
| `l02_matched_sites` | L02 sites matched between 2018 and 2023. Defined for 2023; blank for 2018. |
| `l02_matched_change_5y_pct` | Median matched-site L02 change, 2018 to 2023, percent. Defined for 2023 only. |
| `land_price_thin` | Fewer than five L01 residential points. |
| `transaction_thin` | Fewer than ten reported residential transactions. |
| `market_thin` | `land_price_thin` or `transaction_thin`. |
| `has_market_data` | Any L01, L02, or transaction data. A measured zero is distinct from missing. |

### Coverage

The strict definition requires at least five L01 residential points in both years, at least three matched L01 sites in 2023, and at least ten reported residential transactions in 2023.

- **Strict:** 662 of 1,059 units, 62.5%.
- **Any market data:** 1,059 of 1,059 units.
- **Designated cities:** 19 of 20.
- **Special wards:** 19 of 23.
- **Cities:** 539 of 772.
- **Towns and villages:** 85 of 244, 34.8%.
- **Strongest prefectures:** Nara and Aichi at 100%; Osaka at 97.4%.
- **Weakest prefectures:** Oita at 13.3%; Kochi at 15.4%; Saga at 26.7%.

The 2018 row has no five-year change because 2013 land prices were not pulled. The matched change is a 2018 to 2023 measure and is defined only for 2023.

Twelve units have no residential L01 points in 2023. Two units have no reported residential transactions in 2023. The L02 survey covers all 1,059 units in 2023, but it is a robustness series, not the headline.

### Caveats

- XIT001 records are reported or administrative records, not a census of transactions. Rural counts are thin. Use transaction counts as a liquidity signal, not a precise volume.
- The market panel uses transaction prices only (`priceClassification=01`). Contract prices start in 2021 and are a different series.
- L01 2018 predates the 2019 open-data terms. It is free for commercial use with attribution under the older KSJ terms. The derived municipal medians are published with attribution.
- Do not combine land-only, land-and-building, and condominium prices in one median. They are different assets.

### Regeneration

```bash
uv run python src/08_download_ksj.py L01_2018 L01_2023 L02_2018 L02_2023
uv run python src/13_market_pull.py --scope pilot
uv run python src/14_market_panel.py --scope pilot
uv run python src/13_market_pull.py --scope full
uv run python src/14_market_panel.py --scope full
uv run pytest
```

Raw downloads are git-ignored. The manifests `data/raw/reinfolib_manifest.json` and `data/raw/ksj_manifest.json` are committed. The processed CSVs are committed.

### Attribution

Source: MLIT Real Estate Information Library; MLIT National Land Numerical Information L01 and L02; Statistics Bureau of Japan for total dwellings.

## Akiya-bank aggregates

`akiya_bank_trend.csv` is the national monthly series from the MLIT chart (March 2018 to October 2026). `akiya_bank_prefecture.csv` has the 47 prefecture participation rates. `akiya_bank_summary.csv` has the current counts.

### Fields

| File | Fields |
|---|---|
| `akiya_bank_trend.csv` | `month`, `participating_municipalities`, `listing_count` |
| `akiya_bank_prefecture.csv` | `prefecture_code`, `prefecture`, `participation_rate_pct` |
| `akiya_bank_summary.csv` | `as_of`, `participating_municipalities`, `listing_municipalities`, `latest_month_listings`, `chart_label_listings`, `cumulative_transactions`, `national_participation_rate_pct`, `note` |

### Counts as of October 2026

- **1,155** participating municipalities.
- **750** municipalities listing.
- **20,089** current listings on the chart label; the October 2026 month-end bar is **20,010**. Both are retained.
- **~29,000** cumulative transactions.
- National participation rate **65.5%**. Prefecture range: **12.2%** (Okinawa) to **100.0%** (Toyama and Oita). Rates are by municipality, not by population.

### Caveats

- Participation is not vacancy. Listings are marketed supply with owner consent, not a vacancy census.
- The municipal participation list is not included. AtHome returned **503 emergency maintenance** and LIFULL returned **403 CloudFront** on 2026-11-27. The Wayback snapshots are stale and were not used as current. Do not scrape or bypass.
- The trend chart's month labels are part of the image; the script hard-codes the 53 labels. Update them when MLIT advances the PDF.

### Regeneration

```bash
uv run python src/15_akiya_bank.py
```
