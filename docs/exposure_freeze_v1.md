# Exposure Freeze v1 — Sri Lanka Dengue EWS Calibration
*Official freeze record for the climate-exposure input. Documentation only. The frozen exposure CSV and all climate data remain git-ignored in quarantine and are NOT committed. No outcome↔exposure linkage, no models, preregistration and frozen outcome dataset unchanged.*

## 1. Freeze date
**2026-06-12**

## 2. Frozen exposure table path (LOCAL/QUARANTINED — not committed)
`~/data_quarantine/geomatics/climate_exposure/processed_frozen/rdhs_weekly_climate_exposure_2018_2025_v2_boundary_resolved.csv`
- Read-only (`-r--r--r--`), 3,116,015 bytes. Metadata sidecar: `…_v2_boundary_resolved.meta.md`.
- Predecessor `…_v1.csv` (SHA256 `dc4de0a3a77f5dde1511a146d4b258512c90822d764f62d5cc91b4841b4e8377`) retained unchanged for provenance.

## 3. SHA256 checksum (verified at freeze)
`3900082bcda70e87b4a87d6c3e44384d2543b4d3ed50f27f43dd8c572d81ee5d`

## 4. Row count
**10,842** = 417 ISO weeks × 26 RDHS.

## 5. Spatial unit
**26 RDHS divisions** (geometry `rdhs_26_v1.gpkg`, EPSG:4326, sha256 `9e5e2c0a…`; Kalmunai/Ampara DS-dissolve split; keyed by `geometry_id`).

## 6. Temporal unit
**Epidemiological week** (ISO weeks), aligned to the WER convention used by the frozen outcome.

## 7. Years covered
**2018–2025** (8 years; 2020 = 53 ISO weeks; all others 52).

## 8. Climate variables included
- `t2m_mean_c`, `t2m_min_c`, `t2m_max_c` — 2m temperature (°C), from **ERA5-Land** hourly.
- `d2m_mean_c` — 2m dewpoint (°C), from ERA5-Land.
- `rh_mean_percent` — relative humidity (%), **Alduchov–Eskridge Magnus** (A=17.625, B=243.04), computed per cell per hour before weekly averaging.
- `precip_sum_mm`, `precip_mean_daily_mm` — precipitation, from **CHIRPS** daily v2.0 Final (−9999 masked).
- Provenance/QC columns: `n_era5_hours, n_chirps_days, era5_qc_flag, chirps_qc_flag, aggregation_method, source_version, notes`.
- Aggregation: precomputed per-RDHS cell masks + NumPy (ERA5-Land 0.1°, CHIRPS 0.05°).

## 9. Boundary-week resolution status
**All 6 year-edge ISO weeks resolved** (2019-W01, 2020-W01, 2020-W53, 2021-W52, 2022-W52, 2025-W01) using adjacent-year data. **0 partial-week flags remain**; every row has `n_era5_hours = 168` and `n_chirps_days = 7`.

## 10. QC summary (at freeze)
| Check | Result |
|---|---|
| Rows | 10,842 ✅ |
| 26 RDHS | ✅ |
| epi_year 2018–2025 | ✅ |
| Duplicate (year,week,rdhs) | 0 ✅ |
| Nulls | 0 ✅ |
| RH within 0–100 | ✅ |
| Dewpoint ≤ temperature | ✅ |
| Precipitation nonnegative | ✅ |
| n_era5_hours = 168 (all rows) | ✅ |
| n_chirps_days = 7 (all rows) | ✅ |
| Partial-week flags | 0 ✅ |
| Kalmunai aggregated | ✅ |
| t2m_mean range | 19.6–31.5 °C ✅ |

## 11. Provenance (committed build/QC reports)
- 2019 slice build report — commit **`10490b0`** (`docs/climate_exposure_2019_slice_build_report.md`)
- Full 2018–2025 build report — commit **`5684fb1`** (`docs/climate_exposure_2018_2025_full_build_report.md`)
- Boundary-week resolution report — commit **`f5a806f`** (`docs/climate_exposure_boundary_week_resolution_report.md`)
- Source reconnaissance / pilots / bulk plan: `climate_source_reconnaissance.md`, `chirps_precipitation_pilot_report.md`, `era5land_temperature_humidity_pilot_report.md`, `climate_bulk_acquisition_and_exposure_table_plan.md`.

## 12. Quarantine statement
The frozen exposure CSV (v2), its predecessor v1, all 8 annual slices, the 96 ERA5-Land NetCDFs, and ~2,920 CHIRPS GeoTIFFs (~10 GB) remain **git-ignored in `~/data_quarantine/geomatics/climate_exposure/`** and are **not committed**. Only documentation is committed.

## 13. No-linkage statement
The exposure table has **not** been linked to the dengue outcome. It contains climate variables + RDHS/epi-week keys only.

## 14. No-modeling statement
**No models have been run.**

## 15. Official frozen exposure input
**`rdhs_weekly_climate_exposure_2018_2025_v2_boundary_resolved.csv` (SHA256 `3900082b…`) is the official frozen exposure input** for all future outcome↔exposure linkage and modeling in this project. Any change requires a new versioned freeze (v2.x / v3) with a new checksum and freeze record; this file is immutable.

## Change policy
Immutable. Integrity re-check anytime:
```
sha256sum -c <<< "3900082bcda70e87b4a87d6c3e44384d2543b4d3ed50f27f43dd8c572d81ee5d  rdhs_weekly_climate_exposure_2018_2025_v2_boundary_resolved.csv"
```
