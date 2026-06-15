# Colombia CHIRPS Full Weekly Precipitation Table (data construction — labels/models NOT run)
*Builds the complete Colombia weekly **CHIRPS precipitation** table for the OpenDengue Admin2 panel, keyed by **GID_2**. **No outbreak labels; no models; no AUC/PR-AUC/calibration/DCA/net-benefit/ΔNB/regression/forecast; no external validation. ERA5-Land temperature DEFERRED until CDS is stable (not run).** All climate data quarantined; only this markdown is proposed for commit.*

**Date:** 2026-06-15 · **Status:** data construction (CHIRPS precip only) · **Base commit:** 83be9fa · **Builds on:** `docs/colombia_manual_alias_crosswalk_report.md`, `docs/colombia_era5_temperature_smoke_report.md`.

## A. Inputs & exact source paths
- **OpenDengue** weekly Admin2 panel: `~/data_quarantine/opendengue_extract_inspection_v1/Temporal_extract_V1_3.zip` (read in-memory).
- **GADM v4.1 Admin2** polygons: `~/data_quarantine/colombia_external_replication_feasibility_v1/gadm41_COL_2.json.zip`.
- **Finalized crosswalk:** `colombia_crosswalk_v1.csv` (auto exact+alias) + `colombia_manual_alias_crosswalk_v1.csv` (9 manual includes; 5 newly-created flagged `review`/excluded) — same dir.
- **CHIRPS v2.0** precipitation: annual **daily NetCDF p05 (0.05°)**, `https://data.chc.ucsb.edu/products/CHIRPS-2.0/global_daily/netcdf/p05/chirps-v2.0.<YEAR>.days_p05.nc`.

## B. Crosswalk / GID_2 mapping
- **Spatial key = GID_2** (not municipality names). OpenDengue→GID_2 map: **1,066 entries** (1,057 auto + 9 manual includes).
- Polygons aggregated: **1,065 distinct GID_2** (one GID_2 serves two OD name-variants).
- **Method note:** the build was switched from 5,901 daily-GeoTIFF requests to **17 annual NetCDFs** after the per-day approach tripped CHC server **rate-limiting** (sustained >1 req/s caused ~100% silent download failures). The NetCDF path uses retries + integrity checks + fail-fast and is rate-limit-safe.

## C. Excluded / flagged newly-created municipalities (primary)
- **5 newly-created municipalities excluded from the primary table** (absent from GADM v4.1): Tuchín, Albania–La Guajira, Norosí, Guachené, San José de Uré → **763 OpenDengue rows flagged `excluded_newly_created`**. Parent-polygon routing remains **sensitivity-only** (not applied here).

## D. CHIRPS download / aggregation result
- **Years:** 2006–2022 (**17 annual NetCDFs**), covering the OpenDengue span **plus 8 warm-up weeks** (grid start **2006-11-05**).
- **Downloaded:** **20.0 GB** across 17 files (stream-discard: each NetCDF deleted after aggregation → quarantine dir is only **66 MB**). Per-file size + SHA256 in `climate_file_manifest_v1.csv`. **0 missing years.**
- **Aggregation:** rasterize-once (all_touched) → per-day areal **mean** per polygon (vectorized `bincount`) → **weekly = sum of the 7 daily means** (matches the smoke-test definition).
- **Runtime:** **30.3 min** total.
- **Correctness:** built-in **smoke cross-check** vs committed Cesar values — 75 weekly cells, **max |diff| = 0.081 mm → PASS**. *(An earlier run had an aggregation bug — cell-sums not divided to a daily mean — caught by a sanity check showing impossible values; fixed, re-validated on the actual build path, and re-run.)*
- **Precip sanity:** min 0.0, **median 33.0**, max **529.4 mm/week** (physically plausible; high end in Pacific/Chocó).

## E. ERA5-Land temperature
- **DEFERRED until CDS stable — not run today** (per your decision). Marked `era5_temperature: DEFERRED_until_CDS_stable` in meta. The validated ERA5 pipeline (commit 83be9fa) will add a `temp_C_week` column later, joined on the same GID_2 / week_start keys.

## F. Joined OpenDengue row counts (GID_2 route)
| Metric | Count | Share |
|---|---|---|
| OpenDengue weekly Admin2 rows | 199,458 | 100% |
| Rows mapped to a primary GID_2 | 198,695 | **99.6%** |
| Rows flagged excluded (newly-created) | 763 | 0.38% |
| Rows linked to CHIRPS precip | **198,266** | **99.4%** |
| GID_2 mapped but no precip (islands) | 429 | 0.22% |

## G. Climate completeness
- Weekly climate table: **897,795 rows** (1,065 polygons × 843 weeks), **896,109 complete (99.8%)**.
- The only incomplete units are **2 island municipalities — San Andrés (`COL.27.2_2`) and Providencia (`COL.27.3_2`)** — empty in **all** weeks because CHIRPS is land-masked over these small Caribbean islands. → the 429 unlinked OD rows above. **Honest limitation:** these 2 islands need an ocean-inclusive precip product or explicit exclusion in the eventual analysis (negligible: 0.22% of rows).

## H. Lag 0–8 feasibility (only — no labels/models)
- Weekly climate grid is **gap-free** (0 internal gaps ≠ 7 days across all polygons), so lags are a deterministic `groupby('GID_2').shift(k)`.
- **835 of 843 weeks** support full lag-0–8 (the first 8 = reserved warm-up) × **1,063 polygons with precip** ⇒ **≈ 889k** climate rows with full lag-8 availability. **No lag computed here; feasibility only.**

## I. Runtime / disk
- Build runtime **30.3 min**; bandwidth **20.0 GB** (17 requests, stream-discard). Persistent quarantine footprint **66 MB** (two CSVs + manifest + meta; daily rasters not retained). Aggregation memory trivial (one year's Colombia subset at a time).

## J. Remaining risks before labels/models
1. **Temperature missing** — ERA5-Land deferred; the climate panel is precip-only until the CDS retrieve runs.
2. **2 island municipalities** lack CHIRPS (land mask) — decide ocean-inclusive product vs exclusion.
3. **Strong panel imbalance** — reporting municipalities/week range **98–415** (median 213) of 1,065; the case panel is sparse/unbalanced (climate grid is complete, cases are not). Modeling must handle this (as pre-specified in the build spec).
4. **CHIRPS rate-limit lesson** — any future per-file fetching must throttle/batch (the annual-NetCDF route avoids it).
5. Label/threshold/lag construction and any modeling remain **separately gated** and **not started**.

## K. Confirmation — nothing modeled
- **No outbreak labels, no models, no AUC/PR-AUC/calibration/DCA/net-benefit/ΔNB/regression/forecast, no external validation.** ERA5-Land not run. Only descriptive climate construction + GID_2 join + lag-feasibility counting.
- No Sri Lanka frozen data or prior outputs read for modeling, modified, or overwritten.

## L. Outputs (quarantine, read-only; NOT committed) + SHA256 (16-char) / size
- `colombia_weekly_climate_gid2_v1.csv` — `e8bd104c07982a1c…` — 47,483,695 B (897,795 rows)
- `colombia_opendengue_climate_linked_v1.csv` — `5d4d646e9d8f756c…` — 20,835,894 B (199,458 OD rows + precip)
- `climate_file_manifest_v1.csv` — `c1bc5f62fd718117…` — 1,395 B (17 NetCDFs, size+SHA)
- `colombia_climate_linkage_full_v1.meta.json` — `8f14735e31a709eb…` — 783 B
- All under `~/data_quarantine/colombia_climate_linkage_full_v1/`, chmod 444. **No data files committed** — only this markdown report is proposed for commit (pending approval).
