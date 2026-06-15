# Colombia ERA5-Land Temperature Smoke Test (re-attempt; subset only — full build NOT run)
*Re-runs **only the ERA5-Land temperature leg** of the Colombia climate-linkage smoke test (CHIRPS precipitation was already validated). **No outbreak labels; no models; no AUC/PR-AUC/calibration/DCA/net-benefit/ΔNB/regression/forecast; no external validation.** All climate files quarantined and read-only; no data files committed.*

**Date:** 2026-06-15 · **Status:** smoke test only · **Base commit:** 19930d5 · **Builds on:** `docs/colombia_climate_linkage_smoke_report.md`.

## A. Context
- **CHIRPS precipitation was already validated in commit `19930d5`** (Cesar, 25 polygons, 3 weeks, 75/75 weekly rows complete). **Not re-downloaded here.**
- ERA5-Land temperature was previously blocked by a Copernicus CDS maintenance/HTTP-500 outage. This step **re-attempted only the ERA5-Land leg**.

## B. CDS / ERA5 request result — SUCCEEDED (after the maintenance tail)
- Dataset `reanalysis-era5-land`, variable **2 m temperature**, Cesar bbox `area=[N 11.0, W −74.3, S 7.5, E −72.8]`, window **2018-06-03 → 2018-06-09**, **3-hourly**, NetCDF.
- The request hit **3 × HTTP 500** during the tail of the 15 June CDS maintenance window, then auto-recovered: status **accepted → successful (10:31)**, file delivered. Total wall time ≈ **1,839 s** (~31 min, dominated by CDS queue/maintenance, not data volume). **Auth valid; server-side delay only.**

## C. ERA5 file size / metadata
- `era5land_cesar_2018jun_wk1.nc` — **85,272 bytes** (sha256 `b972f9a66f41369a…`).
- Variable `t2m` (Kelvin); **56 timesteps** (7 days × 8 three-hourly); grid **36 lat × 16 lon = 576 cells** at **0.1°** (~11 km). Converted **K → °C** (−273.15); hourly/3-hourly → **daily mean** (7 daily fields).

## D. Temperature aggregation completeness — VALIDATED
- Daily municipality zonal means (rasterstats, `all_touched`, nodata = NaN): **175/175 municipality-days non-null = 100%** (25 polygons × 7 days).
- **Cells per polygon: 3–54** (coarse 0.1° grid → small municipalities capture few cells; `all_touched` ensures every polygon gets ≥3).
- Daily zonal temperature **20.8–30.1 °C**, mean **25.8 °C** (plausible for Cesar; note the raw grid min of 5.6 °C is a single high-elevation Sierra Nevada cell inside the bbox, smoothed out in municipality means).
- Weekly mean temperature: **25/25 weekly rows complete (100%)**, range **21.0–29.1 °C**.
- Runtime: zonal aggregation **< 1 s**; disk: 85 KB NetCDF + small derived tables.

## E. Join to OpenDengue (via finalized crosswalk GID_2, not names)
- ERA5 covers OpenDengue week **2018-06-03** (the single week in the ERA5 window); that week has **7** Cesar municipality-week rows.
- **GID_2 join:** OD `adm_2_name` → crosswalk `gadm_gid2` → ERA5 weekly temp. **7/7 rows mapped to a GID_2; 7/7 joined to temperature (100%).**
- **No labels/models/metrics** — the join carries `dengue_total` as a raw column only.

## F. Does GID_2 resolve the previous alias issue?
- **Yes (structurally).** The naive-name miss `MANAURE BALCON DEL CESAR` maps through the crosswalk to **GID_2 `COL.12.16_2`** (GADM `NAME_2='Manaure'`, `alias` tier), which **has** an ERA5 weekly temperature (**20.98 °C**). Manaure simply had **no case-row in week 2018-06-03**, so it is not in this week's join set — but the GID_2 route attaches climate to it correctly whenever it does report. The GID_2 key removes the name-matching fragility seen with the precipitation naive-name join.

## G. Lags 0–8 feasibility
- Unchanged and confirmed: weekly climate series are **continuous/gap-free**, so lags 0–8 are a deterministic `groupby('GID_2').shift(k)`. Only the first 8 weeks of each unit's series lack full lag-8 (covered by the **2006–2007 warm-up**). The 1-week ERA5 window here is sufficient to confirm the per-unit weekly grid is well-formed; lag depth is a function of window length, not pipeline correctness.

## H. Remaining risks before the full Colombia climate table
1. **CDS throughput/availability:** today's retrieve took ~31 min through the maintenance tail. The full 2006–2022 panel needs either **many bbox requests** or the CDS **ARCO/Zarr `reanalysis-era5-land-timeseries`** endpoint (advertised by the API) for efficient long time-series — plan around CDS load.
2. **ERA5-Land resolution (0.1°):** small municipalities get few cells (min 3 with `all_touched`); consider **area-weighting or nearest-cell** for tiny polygons in the full build.
3. **CHIRPS disk** (~18–19 GB if all daily global rasters fetched) remains the main scaling cost — cache the small weekly municipality table, not the rasters.
4. **Humidity** (2 m dewpoint → RH) not tested; optional add-on, same pipeline.
5. **Join key:** the full build **must** use GID_2 (confirmed), not names.

## I. Quarantined outputs (read-only; NOT committed) + SHA256 (16-char) / size
- `era5land_cesar_2018jun_wk1.nc` — `b972f9a66f41369a…` — 85,272 B
- `era5_cesar_daily_tC.nc` — (derived daily °C field)
- `cesar_weekly_temp_smoke_v1.csv` — `fbe523c6f09923ca…` — 1,568 B
- `cesar_od_temp_join_smoke_v1.csv` — `91442fc8fc21dc64…` — 320 B
- (CHIRPS files from commit 19930d5 unchanged; not re-downloaded)
- All under `~/data_quarantine/colombia_climate_linkage_smoke_v1/`, read-only.

## J. Recommendation
- **Both climate legs are now validated** (CHIRPS precip in `19930d5`; ERA5-Land temperature here). **Recommend proceeding to the full Colombia 2006–2022 climate table build as the next separately-gated step**, with: GID_2 join; CHIRPS cached to a weekly municipality table; ERA5-Land via the ARCO/Zarr time-series endpoint (or batched bbox requests) to avoid CDS-queue bottlenecks; 2006–2007 reserved for lag warm-up. **None of that is run here.**

## K. Confirmations
- **Smoke test only:** no labels, no models, no AUC/PR-AUC/calibration/DCA/net-benefit/ΔNB/regression/forecast, no external validation; one department / one week processed for ERA5.
- **No CHIRPS re-download;** no full 2006–2022 climate table built; no additional CHIRPS files.
- **No Sri Lanka frozen data or prior outputs read for modeling, modified, or overwritten.**
- **No data files committed** — only this markdown report is proposed for commit.
