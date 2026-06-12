# Full 2018–2025 Climate Exposure Table — Build Report (Geomatics WP2)
*Documents the full multi-year exposure build performed **locally**. All climate inputs, annual slices, and the exposure table stay in git-ignored quarantine and are **NOT committed**. No outcome↔exposure linkage, no models, frozen outcome dataset unchanged, preregistration unchanged.*

**Date:** 2026-06-12

## Scope
Extended the validated 2019 method to all remaining years (2018, 2020–2025) and **merged with 2019** into the full **RDHS × epidemiological-week climate exposure table, 2018–2025**.

## Acquisition (all quarantined, 0 failures)
- **ERA5-Land** hourly, **per-month CDS requests** (year requests exceed CDS cost limits): 84/84 months for 2018,2020–2025 (+12 for 2019), hour counts verified including leap years.
- **CHIRPS** daily v2.0 Final: every year downloaded + bbox-clipped (365/yr; 366 for leap 2020 & 2024), −9999 masked; raw ~9.8 GB.

## Method
ERA5 K→°C + RH (Alduchov–Eskridge Magnus, per cell per hour) → hourly→ISO-week; CHIRPS daily→ISO-week (−9999 masked). RDHS aggregation via **precomputed per-RDHS cell masks + NumPy** (not per-call `zonal_stats`, which timed out at scale). One ISO year per slice; **2020 = 53 ISO weeks**.

## Annual slices (per-year QC all clean)
| Year | Rows | ISO weeks | t2m_mean range | partial wks |
|---|---|---|---|---|
| 2018 | 1352 | 52 | 19.7–29.9 °C | 0 |
| 2019 | 1352 | 52 | 20.0–31.2 °C | W01 |
| 2020 | 1378 | **53** | 20.4–30.7 °C | W01, W53 |
| 2021 | 1352 | 52 | 20.1–30.0 °C | W52 |
| 2022 | 1352 | 52 | 19.6–30.1 °C | W52 |
| 2023 | 1352 | 52 | 19.7–31.0 °C | 0 |
| 2024 | 1352 | 52 | 20.3–31.5 °C | 0 |
| 2025 | 1352 | 52 | 19.7–31.0 °C | W01 |

Each year: 26 RDHS, 0 duplicates, 0 nulls, RH within 0–100, dewpoint ≤ temperature, precip ≥ 0, Kalmunai aggregated.

## Full merged table (quarantined, NOT committed)
- `~/data_quarantine/geomatics/climate_exposure/processed_frozen/rdhs_weekly_climate_exposure_2018_2025_v1.csv` (read-only).
- **SHA256:** `dc4de0a3a77f5dde1511a146d4b258512c90822d764f62d5cc91b4841b4e8377` · **10,842 rows**.

### Full-table QC
| Check | Result |
|---|---|
| Rows (417 weeks × 26) | **10,842** ✅ |
| 26 RDHS | ✅ |
| epi_year 2018–2025 | ✅ |
| Duplicate (year,week,rdhs) | 0 ✅ |
| t2m_mean range | 19.6–31.5 °C ✅ |
| RH 0–100 | ✅ |
| Dewpoint ≤ temperature | ✅ |
| Precip nonnegative | ✅ |
| Source coverage | ERA5-Land 96/96 months, CHIRPS all days, 0 failures ✅ |

## Boundary weeks (flagged consistently, NOT imputed)
**6 partial year-edge ISO weeks** (156 rows) flagged `partial_week_boundary`: **2019-W01, 2020-W01, 2025-W01** (missing prior 30–31 Dec) and **2020-W53, 2021-W52, 2022-W52** (missing first 1–3 days of Jan). Years 2018/2023/2024 have none. The missing 1–3 days per week sit in the adjacent year's download; per policy they are **flagged, not imputed**. Optional future refinement: cross-year recomputation of these 6 weeks.

## Verdict & next step
The **full 2018–2025 RDHS × epi-week climate exposure table is built and QC-clean** (10,842 rows; temperature, dewpoint, RH, precipitation), held read-only in quarantine. This is the climate input the modeling phase will consume.
- **Still no outcome↔exposure linkage and no modeling** (per `preregistration_analysis_plan_v1.md`).
- Suggested next steps (each separate, approval-gated): (1) optionally resolve the 6 boundary weeks via cross-year recomputation; (2) optional population-weighted/fractional re-aggregation for MAUP sensitivity; (3) **freeze** the exposure table formally; then (4) the outcome↔exposure linkage + the existing-models calibration/decision-curve pilot.
