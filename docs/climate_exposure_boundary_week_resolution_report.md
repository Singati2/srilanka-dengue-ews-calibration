# Climate Exposure — Boundary-Week Resolution Report (Geomatics WP2)
*Documents resolution of the 6 partial year-edge ISO weeks, performed **locally**. All climate inputs and exposure tables stay in git-ignored quarantine and are **NOT committed**. No outcome↔exposure linkage, no models, frozen outcome dataset unchanged, preregistration unchanged. v1 retained unchanged for provenance.*

**Date:** 2026-06-12

## Purpose
Before formal exposure freeze, resolve the 6 boundary weeks flagged `partial_week_boundary` in the full table v1 by recomputing them with full 7-day spans using **adjacent-year ERA5-Land + CHIRPS files already available locally**.

## Inputs & checksums
- **v1 (input):** `…/processed_frozen/rdhs_weekly_climate_exposure_2018_2025_v1.csv` — SHA256 `dc4de0a3a77f5dde1511a146d4b258512c90822d764f62d5cc91b4841b4e8377` (10,842 rows). **Unchanged / not overwritten.**
- **v2 (output):** `…/processed_frozen/rdhs_weekly_climate_exposure_2018_2025_v2_boundary_resolved.csv` — SHA256 `3900082bcda70e87b4a87d6c3e44384d2543b4d3ed50f27f43dd8c572d81ee5d` · 3,116,015 bytes · **10,842 rows** · read-only, quarantined.

## Method (same as v1 build)
26-RDHS geometry `rdhs_26_v1.gpkg`; ERA5-Land 2m_temperature + 2m_dewpoint; **RH = Alduchov–Eskridge Magnus (A=17.625, B=243.04), computed per cell per hour before weekly averaging**; **precomputed RDHS cell masks + NumPy** aggregation (no per-call zonal_stats); CHIRPS −9999 masked. For each boundary week the full 7 calendar days were assembled from the spanning ERA5 monthly NetCDFs and the 7 CHIRPS daily clipped GeoTIFFs.

## Adjacent-day availability (all present locally)
Every boundary week's required adjacent-year ERA5 month and CHIRPS day existed locally (0 missing), so **all 6 were fully resolvable**.

## Resolution results
| Week | 7-day span | n_era5_hours | n_chirps_days | Status |
|---|---|---|---|---|
| 2019-W01 | 2018-12-31 → 2019-01-06 | 168 | 7 | **resolved** |
| 2020-W01 | 2019-12-30 → 2020-01-05 | 168 | 7 | **resolved** |
| 2020-W53 | 2020-12-28 → 2021-01-03 | 168 | 7 | **resolved** |
| 2021-W52 | 2021-12-27 → 2022-01-02 | 168 | 7 | **resolved** |
| 2022-W52 | 2022-12-26 → 2023-01-01 | 168 | 7 | **resolved** |
| 2025-W01 | 2024-12-30 → 2025-01-05 | 168 | 7 | **resolved** |

- **Fully resolved:** all 6.
- **Remaining flagged:** none.
- Exactly **156 rows changed** vs v1 (6 weeks × 26 RDHS); all other 10,686 rows byte-identical.

## v2 full QC
| Check | Result |
|---|---|
| Rows | 10,842 ✅ |
| 26 RDHS | ✅ |
| epi_year 2018–2025 | ✅ |
| Duplicate (year,week,rdhs) | 0 ✅ |
| Nulls | 0 ✅ |
| t2m_mean range | 19.6–31.5 °C ✅ |
| RH within 0–100 | ✅ |
| Dewpoint ≤ temperature | ✅ |
| Precip nonnegative | ✅ |
| **n_era5_hours = 168 for ALL rows** | ✅ |
| **n_chirps_days = 7 for ALL rows** | ✅ |
| Remaining partial boundary weeks | **NONE** ✅ |
| Source coverage | complete (no flagged gaps) ✅ |
| Kalmunai aggregated | ✅ |

## Confirmations
- **No outcome↔exposure linkage occurred** — v2 contains climate variables only; the frozen dengue outcome was not touched.
- **No models were run.**
- **All exposure CSVs and climate data remain quarantined** under `~/data_quarantine/geomatics/climate_exposure/` (v1 + v2 + slices + NetCDFs + GeoTIFFs); none committed.
- **v1 retained unchanged** for provenance; v2 is the boundary-clean candidate for the formal freeze.

## Next step
With all boundary weeks resolved, v2 is ready for the **formal exposure freeze** (separate, approval-gated), after which the first **outcome↔exposure linkage** and the existing-models calibration/decision-curve pilot can proceed (per `preregistration_analysis_plan_v1.md`). Nothing links or models until directed.
