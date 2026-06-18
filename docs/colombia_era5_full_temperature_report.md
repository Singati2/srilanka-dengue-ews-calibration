# Colombia ERA5-Land Full Weekly Temperature Table (data construction — labels/models NOT run)
*Builds the complete Colombia weekly **ERA5-Land 2 m temperature** table (daily-mean → weekly-mean) keyed by **GID_2**, and joins it to the existing CHIRPS precip table and OpenDengue panel. **No outbreak labels; no models; no AUC/PR-AUC/calibration/DCA/net-benefit/ΔNB/regression/forecast; no external validation. CHIRPS was NOT rerun.** All data quarantined; only this markdown is proposed for commit.*

**Date:** 2026-06-18 · **Status:** data construction (ERA5 temperature) · **Base commit:** cdabd60 · **Builds on:** `docs/colombia_chirps_full_precipitation_report.md`, `docs/colombia_era5_temperature_smoke_report.md`.

## A. ERA5 retrieval strategy
- Dataset **`derived-era5-land-daily-statistics`**, variable **2m_temperature**, statistic **daily_mean**, `frequency=1_hourly`, `time_zone=utc+00:00`, Colombia bbox `area=[N 13.6, W −82.0, S −4.4, E −66.6]`.
- **One CDS request per year**, 2006–2022 (17 requests), covering the OpenDengue/CHIRPS span + 8 warm-up weeks (grid 2006-11-05 → 2022-12-25, 843 weeks).
- **Resumable**: per-year checkpoint (`_temp_ckpt.npz/json`) so completed years are never re-fetched; bounded retries (4/year); clean-stop guards on 3 consecutive CDS failures or implausible temps (>60/<−40 °C). NetCDFs stream-discarded after aggregation.

## B. Why 1-year chunks (proof)
Multi-year requests were **rejected by CDS cost limits** (`403 Forbidden — "cost limits exceeded / request too large"`): probed and confirmed **2-year, 3-year, 4-year, 5-year all REJECTED**; **1-year ACCEPTED** (e.g., request_id `1f30a645-…`). So 1-year is the only permitted chunk — hence 17 sequential requests.

## C. Years completed
**All 17 (2006–2022) — `status: completed`, 0 failed/retried years, 0 implausible-value or CDS-abort triggers.** Per-year request IDs in `era5_file_manifest_v1.csv`. Build runtime **~3,642 min (~60.7 h)** — dominated by CDS queue waits that grew from ~35 min (year 1) to ~4 h/year under server congestion (not our code).

## D. File sizes & checksums
- 17 annual NetCDFs, total **340,861,946 B** (~18–24 MB/year), per-file size + SHA256 + request_id in `era5_file_manifest_v1.csv`. Rasters stream-discarded (not retained).

## E. Temperature aggregation method
- Per ERA5-Land 0.1° grid cell: daily mean 2 m temperature, **K → °C** (−273.15).
- **Weekly mean** per municipality = mean of the 7 daily areal-mean values, via rasterize-once (all_touched) + vectorized `bincount` over the **same 1,065 primary GID_2 polygons** as the CHIRPS table (same defensible polygon rule as the smoke test).

## F. Completeness & sanity checks
- Weekly temperature table: **897,795 rows** (1,065 polygons × 843 weeks), **896,109 complete (99.8%)**, **99.8% every year** (flat).
- The only incomplete units: **2 island municipalities — San Andrés (`COL.27.2_2`), Providencia (`COL.27.3_2`)** — empty in all weeks (ERA5-Land is land-only; tiny Caribbean islands fall outside the land mask), identical to the CHIRPS limitation.
- **Temperature range: 7.2 / 19.7 / 33.5 °C** (min/median/max) — physically plausible (low = high Andes, high = lowlands). No implausible values.
- **Smoke cross-check** vs committed Cesar ERA5 smoke (week 2018-06-03): **max |diff| = 0.048 °C → PASS** (small diff expected: full daily-mean here vs 3-hourly subsample in the smoke).

## G. OpenDengue join result (via GID_2)
| Metric | Count | Share |
|---|---|---|
| OpenDengue weekly Admin2 rows | 199,458 | 100% |
| Rows mapped to a primary GID_2 | 198,695 | 99.6% |
| Rows flagged excluded (newly-created) | 763 | 0.38% |
| Rows linked to CHIRPS precip | 198,266 | 99.4% |
| Rows linked to ERA5 temp | 198,266 | 99.4% |
| GID_2 mapped but no temp (islands) | 429 | 0.22% |

## H. Rows linked to BOTH CHIRPS + ERA5
**198,266 OpenDengue rows (99.4%)** have **both** weekly precipitation and weekly temperature — the modelable climate-linked panel. The 429 unlinked are the 2 island municipalities (no land-grid climate); 763 are the excluded newly-created units.

## I. Lag 0–8 feasibility (only — no lags/labels created)
- Weekly temperature grid is **gap-free** (0 internal gaps ≠ 7 days), so lags 0–8 are a deterministic `groupby('GID_2').shift(k)`.
- **835 of 843 weeks** support full lag-0–8 (first 8 = warm-up) × **1,063 polygons with temperature** ⇒ ~889k climate rows with full lag-8 availability, aligned with the CHIRPS grid. **No lags computed here.**

## J. Runtime / disk
- Build runtime **~60.7 h** (queue-bound; 17 requests), data downloaded **~341 MB** (stream-discarded). Persistent quarantine footprint for this step **~178 MB** (weekly temp table 48 MB + combined precip+temp 66 MB + OD-with-temp 24 MB + manifests/meta). Aggregation memory trivial (one year at a time).

## K. Remaining risks before labels/models
1. **2 island municipalities** lack both CHIRPS and ERA5 (land masks) — decide ocean-inclusive products vs exclusion (0.22% of rows).
2. **Strong panel imbalance** persists (sparse case reporting; climate grid complete) — modeling must handle it.
3. **Humidity** not built (optional; ERA5-Land 2 m dewpoint → RH is a future add via the same pipeline).
4. **CDS throughput** is the binding cost for any ERA5 refresh (~60 h here) — plan around it.
5. Labels/threshold/lag construction and modeling remain **separately gated** and **not started**.

## L. Confirmation — CHIRPS not rerun
- CHIRPS was **read only** for the precip+temp join; `colombia_weekly_climate_gid2_v1.csv` and its manifest/meta were **not modified or re-downloaded**.

## M. Confirmation — nothing modeled
- **No outbreak labels, no models, no AUC/PR-AUC/calibration/DCA/net-benefit/ΔNB/regression/forecast, no external validation.** Only climate construction + GID_2 joins + lag-feasibility counting.
- No Sri Lanka frozen data or prior outputs read for modeling, modified, or overwritten.

## N. Outputs (quarantine, read-only; NOT committed) + SHA256 (16-char) / size
- `colombia_weekly_era5_temperature_gid2_v1.csv` — `b65b9150c20d4734…` — 48,587,297 B (897,795 rows)
- `colombia_weekly_climate_precip_temp_gid2_v1.csv` — `b4c164d24744c1a5…` — 65,783,432 B (precip + temp, 897,795 rows)
- `colombia_opendengue_climate_linked_with_temp_v1.csv` — `248bb73a11e8e433…` — 23,704,912 B (199,458 OD rows + precip + temp)
- `era5_file_manifest_v1.csv` — `9e871f3dd386fbb9…` — 2,001 B (17 NetCDFs: year, request_id, bytes, SHA)
- `colombia_era5_temperature_full_v1.meta.json` — `ca419eff3db4a28b…` — 625 B
- All under `~/data_quarantine/colombia_climate_linkage_full_v1/`, read-only. **No data files committed** — only this markdown report is proposed for commit (pending approval).
