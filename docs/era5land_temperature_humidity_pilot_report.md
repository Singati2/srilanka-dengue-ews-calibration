# ERA5-Land Temperature/Humidity Pilot Report — June 2019 (Geomatics WP2)
*Documents a one-month ERA5-Land pilot performed **locally**. The NetCDF and pilot CSV stay in git-ignored quarantine and are **NOT committed**. One month only — no bulk download, no further ERA5-Land download, no outcome↔exposure linkage, no models, frozen outcome dataset unchanged, preregistration unchanged.*

**Date:** 2026-06-11
**Tooling:** cdsapi/xarray/netCDF4 (installed) + geopandas + rasterstats.

## Source & inspection
- **Dataset:** ERA5-Land hourly (`reanalysis-era5-land`), Copernicus CDS; file `era5land_lka_2019_06.nc` (sha256 `ed79d506…`, 1.8 MB).
- **Variables:** `t2m` (2m temperature), `d2m` (2m dewpoint) — both **Kelvin**.
- **Time:** **720 hourly steps** (30 days × 24 h, 2019-06-01→30). **Grid:** 43×26 at **0.1°**, lat 5.8–10.0 / lon 79.5–82.0 (SL bbox), EPSG:4326.
- **Missing values:** ~52% NaN = the **land-sea mask** (ERA5-Land is land-only; the bbox is half ocean). Expected; RDHS polygons are land.

## QC results
| Check | Result |
|---|---|
| Hourly steps | **720** ✅ |
| Variables / units | t2m + d2m, **Kelvin** ✅ |
| SL bbox | ✅ (5.8–10.0 N, 79.5–82.0 E) |
| Dewpoint ≤ temperature everywhere | ✅ |
| Temperature range (land) | 16.54–38.29 °C |
| Dewpoint range (land) | 11.62–28.42 °C |
| **RH range** | **24.33–99.53 %** (0 > 100, 0 < 0) ✅ |

## Conversions & RH derivation
- **K → °C:** subtract 273.15.
- **RH** via **Alduchov–Eskridge Magnus**: `RH = 100·exp(17.625·Td/(243.04+Td)) / exp(17.625·T/(243.04+T))` (T, Td in °C). Documented and within plausible range.

## RDHS weekly aggregation (pilot)
- Hourly RH computed **per cell**, then **ISO-week mean per cell** (correct, RH being nonlinear in T/Td), then **zonal mean** to the 26 RDHS (all_touched=True, NaN masked). Output: `era5land_rdhs_weekly_pilot_2019_06.csv` (sha256 `a08b21b1…`, 130 rows, quarantined).
- **26/26 RDHS** covered for all 5 ISO weeks (W22 partial n_hours=48; W23–26 = 168).
- **Meteorological plausibility — correct:**
  - **Nuwara Eliya** (highlands ~1900 m): coolest ~**23 °C** (ERA5-Land lapse-rate correction captured), RH ~78–84 %.
  - **Kalmunai** (east coast): hottest & driest ~**30 °C, RH ~63–71 %** — consistent with the CHIRPS dry-east June finding.
  - **Colombo** (west coast): warm & humid ~**27 °C, RH ~83–88 %**.
  - The cool-highland / hot-dry-east / warm-humid-west gradient is the expected physical structure → the pipeline reproduces real spatial signal, **cross-consistent with the CHIRPS pilot**.

## Verdict
The ERA5-Land path **works end-to-end**: read NetCDF → K→°C → RH (Magnus) → hourly→weekly → RDHS zonal aggregation, producing physically sensible weekly temperature/dewpoint/RH for all 26 RDHS. No blockers for ERA5-Land bulk.

## Notes for the bulk/exposure build
- ERA5-Land **0.1° (~9 km)** is coarse vs the smallest RDHS; use **fractional / population-weighted** aggregation for the final exposure (matters more for temperature than precipitation).
- Always mask the land-sea NaN.
- Mind the ~2–3-month ERA5-Land latency at the 2025 window edge.
- Compute RH **before** temporal averaging (nonlinear); do not average T and Td then derive RH.

## Status & next step
- **Both climate pilots now pass** (CHIRPS precipitation + ERA5-Land temperature/humidity), QC-clean and mutually consistent (dry/hot east, wet/cool highlands).
- **No bulk download, no exposure-table build, and no modeling** until the 2018–2025 bulk acquisition is approved and the RDHS × epi-week exposure table is built, QC'd, and **frozen** (per `preregistration_analysis_plan_v1.md` §H/§Q).
