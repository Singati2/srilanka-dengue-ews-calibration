# Bulk Climate Acquisition & Exposure-Table Build Plan (Geomatics WP2)
*Documentation only. **No bulk download, no further ERA5-Land/CHIRPS download, no outcome↔exposure linkage, no models.** Frozen outcome dataset and preregistration unchanged. All climate files stay git-ignored in quarantine.*

**Date:** 2026-06-11

## A. Purpose
Move from the validated one-month pilots to the **full 2018–2025 RDHS × epidemiological-week climate exposure table**, built once, QC'd, and **frozen** with a checksum. **No modeling until the exposure table is frozen** (per `preregistration_analysis_plan_v1.md` §H/§Q).

## B. Inputs already validated
- **CHIRPS pilot** (June 2019): download→clip→−9999 mask→RDHS weekly worked; correct dry-east monsoon signal. (`chirps_precipitation_pilot_report.md`)
- **ERA5-Land pilot** (June 2019): NetCDF→K→°C→RH(Magnus)→hourly→weekly→RDHS worked; correct cool-highland/hot-dry-east signal. (`era5land_temperature_humidity_pilot_report.md`)
- **RDHS geometry** `rdhs_26_v1.gpkg` (EPSG:4326, sha256 `9e5e2c0a…`).
- **Population denominators** (district-anchored, census-rescaled) `…district_rescaled…csv` (sha256 `e4585741…`) — used as **aggregation weights** (population-weighted exposure).
- **Adjacency graph** (26 nodes / 60 edges) — for later BYM2, not exposure.
- **Frozen dengue outcome** `…v2.0-frozen.csv` (sha256 `99f0b9b1…`) — **kept separate; NOT linked in this phase.**

## C. Climate products
- **ERA5-Land** (`reanalysis-era5-land`, hourly, 0.1°): **2m_temperature**, **2m_dewpoint_temperature**. License: Copernicus.
- **CHIRPS** daily v2.0 Final (0.05°): **precipitation**. License: public domain.
- **Period:** 2018–2025. **Sri Lanka bbox:** North 10.0, West 79.5, South 5.8, East 82.0.

## D. Download strategy
- **Chunk to avoid huge requests:** ERA5-Land **one request per year** (or per month if a year request is rejected/too large), SL bbox only, 2 variables, hourly. CHIRPS **per-year per-day** GeoTIFFs, **bbox-clipped immediately** (never retain global daily in bulk — the 30-day global gz was 121 MB; 8 yr global ≈ tens of GB).
- **Quarantine everything** under `~/data_quarantine/geomatics/climate_bulk/{era5land,chirps}/` (git-ignored).
- **Provenance per file:** source URL / CDS request dict, file name, size, **sha256**, retrieval date, product version.
- **ERA5-Land 2025 latency (explicit):** ERA5-Land has ~2–3-month latency; recent 2025 epi-weeks may be unavailable at build time. Policy: include **complete weeks only**; mark trailing incomplete/unavailable 2025 weeks with `era5_qc_flag = unavailable_latency` (not imputed); document the last complete week. CHIRPS (preliminary product) may cover more recent weeks — flag any preliminary-vs-final mix.

## E. ERA5-Land processing
1. Read hourly NetCDF (xarray); mask the **land-sea NaN**.
2. **K → °C** (−273.15) for t2m and d2m.
3. **RH** via Alduchov–Eskridge Magnus: `RH = 100·exp(17.625·Td/(243.04+Td)) / exp(17.625·T/(243.04+T))` (T, Td in °C). Compute RH **per cell per hour** (RH is nonlinear — derive before any temporal averaging).
4. **Hourly → daily → epidemiological week**: daily mean/min/max of t2m; daily mean d2m and RH; then epi-week means (and t2m weekly min/max from daily extremes). Epi-weeks aligned to the **WER/ISO-week** convention used by the frozen outcome.
5. **QC:** dimensions, **720 hourly steps/30-day month** (year ≈ 8760/8784), time continuity, units (K in, °C out), missingness = land-sea mask only, value ranges (t2m, d2m °C plausible; dewpoint ≤ temperature).

## F. CHIRPS processing
1. Per-day global GeoTIFF → **clip to SL bbox** (rasterio) → quarantine clipped tif.
2. **Explicit −9999 nodata masking** (CHIRPS omits the nodata tag).
3. **Daily → epidemiological week**: weekly precip **sum** (mm) and **mean daily** (mm/day) per RDHS.
4. **QC:** file count per year (365/366), CRS EPSG:4326, resolution 0.05°, bbox bounds, **no missing days** (flag any), precip nonnegative after masking.

## G. RDHS aggregation
- **26 RDHS polygons** (`geometry_id`), EPSG:4326 (matches both grids).
- **Baseline:** area-weighted zonal mean.
- **Preferred:** **population-weighted, fractional-cell** extraction (exactextract-style) using the WorldPop weights — **not centroid sampling** — so each grid cell contributes by its fractional overlap × population. Matters most for the coarse **ERA5-Land 0.1° (~9 km)** grid.
- **Small-RDHS attention (Kalmunai, Sainthamaruthu):** ensure sub-cell RDHS receive the overlapping land cell(s) (fractional weighting or `all_touched` fallback); verify none return NULL; record `aggregation_method` per variable.
- Keep an **area-weighted version** alongside the population-weighted one for the MAUP sensitivity (per prereg §N).

## H. Exposure-table schema (proposed)
**Local frozen output:** `~/data_quarantine/geomatics/climate_exposure/processed_frozen/rdhs_weekly_climate_exposure_2018_2025_v1.csv`

| Column | Description |
|---|---|
| `rdhs_name` | RDHS name (26) |
| `geometry_id` | LK pcode / LK52K / LK52A |
| `epi_year` | epidemiological year |
| `epi_week` | epi week (1–52/53) |
| `week_start` / `week_end` | ISO/epi-week dates |
| `t2m_mean_c` | weekly mean 2m temperature (°C) |
| `t2m_min_c` / `t2m_max_c` | weekly min/max (from daily extremes) |
| `d2m_mean_c` | weekly mean dewpoint (°C) |
| `rh_mean_percent` | weekly mean RH (%) |
| `precip_sum_mm` | weekly precipitation total (mm) |
| `precip_mean_daily_mm` | weekly mean daily precip (mm/day) |
| `n_era5_hours` | hours contributing (e.g., 168; partial weeks fewer) |
| `n_chirps_days` | days contributing (e.g., 7) |
| `era5_qc_flag` | ok / partial_week / unavailable_latency |
| `chirps_qc_flag` | ok / missing_day(s) / preliminary |
| `aggregation_method` | e.g., pop_weighted_fractional / area_weighted |
| `source_version` | ERA5-Land + CHIRPS v2.0 Final (+ build date) |
| `notes` | free text |

Expected ≈ **26 RDHS × (8 yr × ~52 wk) ≈ 10,800 rows** (exact = sum of epi-weeks 2018–2025).

## I. QC checks for final exposure table
- **Row count** = 26 × (number of epi-weeks in 2018–2025); **no duplicate** RDHS-week.
- **No missing weeks** unless a source is genuinely unavailable (then flagged, not imputed).
- **Plausible ranges:** t2m/d2m °C in island-tropical range; **RH within 0–100%** (tiny tolerance); **precip ≥ 0**.
- **Dewpoint ≤ temperature** per RDHS-week.
- **No silent imputation** — every gap carries a `*_qc_flag`.
- **Spatial cross-check:** monsoon pattern (wet/cool highlands, hot/dry east) holds and is consistent across ERA5-Land and CHIRPS, matching the pilots.
- Report `*_qc_flag` distribution.

## J. Freeze procedure
1. Write the **local frozen CSV** (+ area-weighted sensitivity variant) to quarantine — **never committed**.
2. Write **local metadata** (inputs + per-file checksums, formula, QC, flags).
3. Record the **SHA256** of the frozen exposure CSV.
4. Mark read-only; immutable (any change → new version + checksum).
5. **Commit only a safe markdown build report** after approval (no CSV).

## K. Stop conditions
- **Missing ERA5-Land weeks** (beyond the documented 2025 latency edge) → stop, investigate.
- **Failed/over-large CDS requests** → reduce chunk size; if persistent, stop and report.
- **Unexpected file size** (e.g., accidental global CHIRPS pull) → stop.
- **Wrong CRS/bounds** on any file → stop.
- **CHIRPS nodata failure** (−9999 not masked → garbage precip) → stop.
- **Implausible RDHS aggregation** (NULLs, out-of-range, broken spatial pattern) → stop.
- **2025 latency** leaving large gaps → decide window truncation (e.g., end at last complete epi-week) before proceeding.
- In every case: document, **do not impute silently**, do not proceed to linkage/modeling.

## L. Exact next step after this plan
1. **Approve bulk acquisition in small chunks.**
2. **Start with one full year — 2019** (already partly validated by the June pilots) — build the 2019 RDHS-week exposure slice, run Section I QC, confirm before doing all years.
3. Extend to 2018, 2020–2025 once the 2019 slice is clean.
4. Build, QC, and **freeze** the full 2018–2025 exposure table.
5. **No outcome↔exposure linkage and no modeling until the exposure table is frozen.**
