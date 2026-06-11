# CHIRPS Precipitation Pilot Report — June 2019 (Geomatics WP2)
*Documents a one-month CHIRPS pilot performed **locally**. CHIRPS GeoTIFFs and the pilot CSV stay in git-ignored quarantine and are **NOT committed**. CHIRPS only — no ERA5-Land, no CDS, no new packages. No outcome↔exposure linkage, no models, frozen outcome dataset unchanged, preregistration unchanged.*

**Date:** 2026-06-11
**Tooling:** rasterio + rasterstats + geopandas (already installed; no new install).

## Scope
Validate the CHIRPS → RDHS weekly-precipitation pipeline on **one pilot month (June 2019)** over a Sri Lanka bounding box, before any bulk 2018–2025 download.

## Source & processing
- **Product:** CHIRPS daily v2.0 Final, global p05 (`…/global_daily/tifs/p05/2019/chirps-v2.0.2019.06.DD.tif.gz`), **public domain**, daily precipitation (mm/day).
- 30 daily global `.tif.gz` downloaded → gunzip → **clipped to SL bbox** (W 79.5, S 5.8, E 82.0, N 10.0) with rasterio → 30 clipped GeoTIFFs (quarantined).

## QC results
| Check | Result |
|---|---|
| Daily files | **30/30** ✅ |
| CRS | **EPSG:4326** ✅ (matches `rdhs_26_v1.gpkg`) |
| Resolution | **0.05°** ✅ |
| Clip bounds cover SL bbox | ✅ |
| Nodata | CHIRPS omits a declared nodata; **−9999 masked explicitly** ✅ |
| Precipitation (masked) | min **0.0**, max **129.62** mm/day, **no negatives** ✅ |
| Missing days | **0** ✅ |
| Download / clipped size | 121 MB raw_gz → **332 KB** clipped (SL subset) |

## RDHS weekly aggregation (pilot)
- Per-day RDHS **zonal mean** (rasterstats, `all_touched=True`, nodata=−9999) on the 26 RDHS polygons, grouped to **ISO weeks** → weekly sum + mean-daily.
- **26/26 RDHS aggregated every week** (including tiny coastal Kalmunai). ISO weeks 22–26 (wk22 partial n=2; wk23–26 full n=7). Output: `chirps_rdhs_weekly_pilot_2019_06.csv` (130 rows, quarantined).
- **Meteorological plausibility — correct SW-monsoon June pattern:**
  - **Colombo** (west, monsoon-exposed): ~157 / 126 / 167 / 52 mm per week — wet.
  - **Kalmunai** (east coast): ~3.3 / 1.3 / 2.7 / 3.8 mm — dry (east-coast rain shadow in June).
  - **Nuwara Eliya** (highlands): ~94 / 49 / 78 / 47 mm — moderate (orographic).
  - The wet-west / dry-east / moderate-highland gradient is exactly the expected Southwest-monsoon signal → the pipeline reproduces real spatial structure.

## Verdict
The CHIRPS path **works end-to-end**: download → clip → mask → RDHS weekly zonal aggregation, producing meteorologically sensible weekly precipitation for all 26 RDHS in EPSG:4326 at 0.05°. No blockers for CHIRPS bulk.

## Notes for the bulk/exposure build
- Pass **nodata = −9999 explicitly** (CHIRPS tif omits the tag).
- `all_touched=True` covers sub-cell RDHS; for the final exposure consider **fractional / population-weighted** aggregation (matters more for the coarser ERA5-Land 0.1° temperature grid than for CHIRPS).
- Subset to the SL bbox (or use GEE) — never pull global CHIRPS daily in bulk (the 30-day global gz was 121 MB; a full 2018–2025 global pull would be ~10s of GB).

## Status & next step
- CHIRPS pilot complete and QC-clean (quarantined, not committed).
- **ERA5-Land pilot is still gated** on CDS credentials + the `cdsapi`/`xarray`/`netCDF4` install (both pending; see `climate_acquisition_pilot_plan.md`).
- **No bulk download, no exposure-table build, and no modeling** until both pilots pass and the bulk plan is approved.
