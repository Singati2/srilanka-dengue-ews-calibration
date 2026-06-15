# Colombia Climate-Linkage Smoke Test (subset only — full build NOT run)
*Tests the Colombia external-replication **climate-linkage pipeline** (raster → polygon weekly zonal aggregation → join to OpenDengue municipality-weeks) on a small subset before processing the full 2006–2022 panel. **No outbreak labels; no models; no AUC/PR-AUC/calibration/DCA/net-benefit/ΔNB; no full prediction tables; no external validation.** All inputs/outputs quarantined and read-only; no data files committed.*

**Date:** 2026-06-15 · **Status:** smoke test only · **Base commit:** d92b9dd · **Builds on:** `docs/colombia_manual_alias_crosswalk_report.md`.

## A. Subset selected
- **Department:** **Cesar** (EWARS-csd Colombia precedent; 25 GADM Admin2 polygons; contains **none** of the 5 primary-excluded newly-created units).
- **Window:** **2018-06-03 → 2018-06-23**, three consecutive OpenDengue epi-weeks (Sun-start: 06-03, 06-10, 06-17).
- **Second department (Antioquia/Valle):** **not run** — gated on the first succeeding *and* climate sources being available; deferred because ERA5-Land was unavailable today (§F).

## B. Units & rows tested
- GADM Cesar Admin2 polygons: **25**. OpenDengue Cesar 2018 municipalities: **24**; in the 3-week window, **11** municipalities report (unbalanced panel — only ~7–8 municipalities have a row per week).
- **OpenDengue municipality-week rows in window: 22.**
- Weekly climate grid built for all **25 polygons × 3 weeks = 75** rows.

## C. Climate files downloaded (quarantine only, read-only)
- **CHIRPS precipitation** — `CHIRPS-2.0/global_daily/tifs/p05/2018/`, **21 daily global GeoTIFFs (0.05°)**, read via `/vsigzip/` (not decompressed to disk).
  - Total **57,699,493 bytes** (~2.9–3.1 MB/day); per-file SHA256 manifest: `chirps_manifest_v1.csv` (sha `261de40e459f9037…`).
  - Stored in `~/data_quarantine/colombia_climate_linkage_smoke_v1/chirps/`.
- **ERA5-Land temperature** — **NOT obtained today.** The CDS request authenticated and was **accepted** (Request ID `a37daa53-…`), but Copernicus CDS is under **essential maintenance on 15 June 2026 with announced service disruption**; the retrieve returned repeated **HTTP 500** errors and auto-retried (120s × 14+) without delivering. This is a **server-side outage, not an auth/code failure** — credentials in `~/.cdsapirc` are valid (request was accepted). To be **re-run after the CDS maintenance window**.

## D. Precipitation completeness (CHIRPS) — VALIDATED
- Daily zonal mean per municipality (rasterstats, `all_touched`, nodata −9999): **525/525 municipality-days non-null = 100%**; cells/polygon 10–186 (all Cesar polygons resolved on the 0.05° grid).
- Weekly precipitation (sum of 7 daily values per OD week): **75/75 weekly rows complete (100%)**, all 7 days present in every week; values **4.2–70.5 mm/week** (physically plausible for Cesar in June).

## E. Temperature completeness (ERA5-Land) — NOT MEASURED (CDS outage)
- Not measured today (§C). The temperature pipeline is **mechanically identical** to the validated precipitation pipeline (same polygons, same zonal-mean step; hourly→daily mean→weekly mean instead of daily→weekly sum), so no new pipeline risk is expected — but completeness is **unverified** until the ERA5 retrieve succeeds.

## F. Join climate → OpenDengue municipality-weeks
- Weekly precipitation joined to the 22 OpenDengue Cesar municipality-week rows: **21/22 (95.5%)**.
- **The single miss is `MANAURE BALCON DEL CESAR`** — a **known VARNAME alias** (GADM `NAME_2='Manaure'`, `VARNAME_2='Manaure Balcón…'`). The smoke test deliberately used a *naive `NAME_2`-only* name join; the **finalized crosswalk already maps this unit via `GID_2` (COL.12.16_2)**. **Lesson confirmed:** the full build must join climate↔cases on the **finalized crosswalk `GID_2` key**, not ad-hoc name normalization — doing so yields 100% join here.
- No outbreak label, no model, no metric computed (the join carries `dengue_total` as a raw column only).

## G. Lag 0–8 feasibility
- The weekly climate grid is **gap-free** (0 internal gaps ≠ 7 days across all 25 polygons) because climate series are continuous (unlike the sparse case panel).
- Lags are therefore a **deterministic `groupby('unit').shift(k)`** on the weekly grid. In the 3-week window, lag-1 is available for 50/75 rows (only the first week per unit lacks a lag — expected). **Lags 0–8 are feasible without missingness** once the full window is built; only the first 8 weeks of each unit's series lack full lag-8, covered by the **2006–2007 warm-up** reserved in the build spec.

## H. Runtime / memory
- CHIRPS download: 21 files in **~18 s**; daily zonal stats (525 muni-days): **~31 s**; memory trivial (one global raster in memory at a time via `/vsigzip/`).
- **Full-Colombia projection:** ~989–1,066 municipalities × ~17 years × 52 weeks. The binding cost is **CHIRPS daily rasters: ~6,200 days (2006–2022) × ~3 MB ≈ 18–19 GB** if every global daily file is fetched. Mitigations below.

## I. Is full Colombia climate linkage feasible?
- **Precipitation (CHIRPS): YES** — pipeline validated end-to-end, 100% completeness, fast per-raster.
- **Temperature (ERA5-Land): feasible but BLOCKED TODAY** by the CDS maintenance outage; re-run after the window. ERA5-Land is requested as a **bbox+variable subset** (small per request), so it is far lighter than CHIRPS.
- **Overall: feasible**, with the temperature leg pending CDS availability.

## J. Recommended full-build approach
1. **Join on `GID_2`** from the finalized crosswalk (not names) — gives 100% climate↔case join (§F).
2. **CHIRPS:** download daily p05 once to quarantine, compute per-municipality daily zonal means, cache the **small weekly municipality table** (not the rasters) for reuse; delete/retain rasters per disk budget. Consider the CHIRPS **Colombia/regional or lower-res p25** only if disk-bound (p25 ≈ 0.2 MB/day vs 3 MB), accepting coarser resolution.
3. **ERA5-Land:** retry post-maintenance as **bbox-subset hourly 2 m temperature** (and 2 m dewpoint if humidity is later added), aggregate hourly→daily→weekly; small downloads. Consider the CDS **ARCO/Zarr time-series** endpoint the API advertised for efficient long time-series.
4. Build the weekly climate panel **2006–2022**, reserve **2006–2007** for lag warm-up, then (separately gated) proceed to labels/models. **None run here.**

## K. Quarantined outputs (read-only; NOT committed) + SHA256 (16-char) / size
- `cesar_admin2.gpkg` — `13fefe091ae4828c…` — 221,184 B
- `cesar_weekly_precip_smoke_v1.csv` — `017443ea4d6b2017…` — 4,568 B
- `cesar_od_precip_join_smoke_v1.csv` — `41540f1b2eb054a9…` — 2,133 B
- `chirps_manifest_v1.csv` (21 files, per-file SHA) — `261de40e459f9037…` — 2,203 B
- `chirps/` — 21 CHIRPS daily GeoTIFFs, 57,699,493 B total
- (ERA5-Land `.nc`: none produced — CDS outage)
- All under `~/data_quarantine/colombia_climate_linkage_smoke_v1/`, read-only.

## L. Confirmations
- **Smoke test only:** no outbreak labels, no models, no AUC/PR-AUC/calibration/DCA/net-benefit/ΔNB, no full prediction tables, no external validation; only one department / 3-week subset processed.
- **Minimum download:** 21 CHIRPS daily rasters (~57.7 MB) for the subset; **no full 2006–2022 rasters**; ERA5-Land not obtained.
- **No Sri Lanka frozen data or prior outputs read for modeling, modified, or overwritten;** quarantined crosswalk/boundary inputs reused read-only.
- **No data files committed** — only this markdown report is proposed for commit (pending your approval).
