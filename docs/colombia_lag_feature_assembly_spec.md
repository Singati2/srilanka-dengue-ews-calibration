# Colombia Lag-Feature Value Assembly Specification (memo only — NO features assembled)
*Defines how Colombia lag-feature values will be assembled before any modeling table is built. **Specification only: no feature values, no modeling table, no labels/thresholds recomputed, no models, no metrics, no external validation, no data files created or committed.** Mirrors the Sri Lanka framework using Colombia's completed climate grid + completed labels.*

**Date:** 2026-06-18 · **Status:** specification only · **Base commit:** 55aa66c · **Builds on:** `docs/colombia_label_construction_report.md`, `docs/colombia_label_specification.md`, `docs/colombia_chirps_full_precipitation_report.md`, `docs/colombia_era5_full_temperature_report.md`.

## 1. Purpose
- Define lag-feature assembly rules for the Colombia external **framework-replication** arm before creating any modeling table.
- Preserve a **strict no-leakage** design (only information at/before week t feeds features; future used only as the label).
- Mirror the Sri Lanka feature framework (recent-case AR baseline, climate cross-basis lags, hybrid) where possible.
- Use Colombia's **completed** climate grid and **completed** labels — recompute nothing.
- **Specification only; no features assembled in this step.**

## 2. Prediction unit
- **Primary row:** one **`GID_2` × prediction week t`**.
- A prediction row must have: valid `GID_2`; `week_start` = t; observed `dengue_total` at t; a train/val/test split; **≥1 defined future label** among h∈{1,2,4,8,12}; climate grid available for lags 0–8.
- **Primary h=4 modeling row** later requires: `label_h4` defined **and** climate lags 0–8 available.
- **Expected corrected h=4 climate-modelable count** (from `colombia_label_construction_report.md`): **127,703** total — train 86,701 / val 19,356 / test 21,646. *(This is the M2/M3 climate-modelable set; M1/M4/M5 will be smaller — see §7a.)*

## 3. Climate-grid source (lag values)
- Pull lag values from the **full climate grid**: `~/data_quarantine/colombia_climate_linkage_full_v1/colombia_weekly_climate_precip_temp_gid2_v1.csv`.
- **Do NOT** use the unbalanced OpenDengue reporting panel to determine climate-lag availability (this was the corrected bug — climate lags are governed by the gap-free grid).
- Climate lag k at week t uses climate at **week t−k** for the **same `GID_2`**. The 8 warm-up weeks (grid start 2006-11-05) support lag-8 from the first study week.
- **No imputation** of climate values.

## 4. Outcome/label source
- Labels from `~/data_quarantine/colombia_label_features_v1/colombia_labels_h1_h2_h4_h8_h12_v1.csv`.
- **Do NOT** recompute thresholds or labels; **do NOT** alter the no-assume-zero future-outcome rule; **do NOT** redefine any horizon. (Thresholds file `colombia_label_thresholds_train_only_v1.csv` is read-only reference.)

## 5. Core lag features (per row, k = 0..8)
- **Precipitation:** `precip_lag0` … `precip_lag8` — source `precip_mm_week` (weekly CHIRPS precip sum at week t−k).
- **Temperature:** `temp_lag0` … `temp_lag8` — source `temp_C_week` (weekly ERA5-Land mean 2 m temp at week t−k).
- **No future climate values** (k < 0) are permitted.

## 6. Optional summary features (define now, build only if later approved)
- **Precip:** `precip_mean_lag0_2`, `precip_mean_lag0_4`, `precip_mean_lag0_8`, `precip_sum_lag0_2`, `precip_sum_lag0_4`, `precip_sum_lag0_8`.
- **Temp:** `temp_mean_lag0_2`, `temp_mean_lag0_4`, `temp_mean_lag0_8`, `temp_min_lag0_8`, `temp_max_lag0_8`.
- **Optional anomalies:** climate anomalies vs **train-period municipality-specific week-of-year climatology** — only if specified later; climatology estimated from **training period only** (no leakage).

## 7. Recent-surveillance features (for M1/M4/M5)
- Per prediction week t: `cases_lag0` = `dengue_total` at t; `cases_lag1` = t−1; `cases_lag2` = t−2; `cases_lag4` = t−4.
- **Availability rule:** recent-case lags depend on **observed OpenDengue outcome rows**, NOT the climate grid. **Absent prior dengue rows are NOT assumed zero** in the primary feature set; missing recent-case lags are **flagged**.
- A **sensitivity** feature set may later use absent-as-zero panel completion — **not primary**.

### 7a. Differential modelable counts (important — report separately)
Because recent-case lags are **panel-limited** (unbalanced reporting) while climate lags are **grid-complete**:
- **M2/M3 (climate-only) modelable** ≈ the 127,703 h=4 climate-modelable set (label + climate lags).
- **M1/M4/M5 (recent-surveillance / hybrid) modelable** will be **smaller** — additionally requires `cases_lag{0,1,2,4}` present (contiguous recent reporting). The assembly step **must report M1/M4/M5 modelable counts separately** (label + climate lags + recent-case lags), by split, and **must not** silently equate them to 127,703.
- **Comparison row-set rule:** For head-to-head M1–M5 comparisons, the future modeling specification must define whether metrics are evaluated on model-specific available rows or a common complete-case row set; the primary comparison should prefer a common complete-case set when feasible (so M1–M5 are scored on identical rows and differences reflect the models, not the sample).

## 8. Primary feature sets for later modeling (no fitting now)
- **M0:** intercept / climatology only (optional season terms if defined later).
- **M1 (recent-surveillance baseline):** `cases_lag0, cases_lag1, cases_lag2, cases_lag4`.
- **M2 (climate-only):** `precip_lag0..8`, `temp_lag0..8`.
- **M3 (climate + season + location):** M2 + seasonal terms (§9) + location fixed effects / grouped encoding (in the model spec).
- **M4 (hybrid):** M1 recent-case lags + M2 climate features.
- **M5 (hybrid + season + location):** M4 + season terms + location fixed effects / grouped encoding.
- **No models fit in this step.**

## 9. Seasonal terms (deterministic calendar — no leakage)
- `sin(2π·woy/52.1775)`, `cos(2π·woy/52.1775)` (week-of-year first harmonic); optional second harmonic `sin/cos(4π·woy/52.1775)`. Deterministic from the calendar week; cause no leakage.

## 10. Train/validation/test split (committed; unchanged)
- Train 2006-12-31→2017-12-31 · Validation 2018-01-01→2019-12-31 · Test 2020-01-01→2022-12-25.
- **Do not change the split.** Keep the **COVID-era test-window caveat** from the label-construction report (reporting continued 2020–2022; remains an interpretation caveat).

## 11. Expected future quarantine outputs (NOT now)
Dir `~/data_quarantine/colombia_label_features_v1/`:
- `colombia_lag_feature_values_v1.csv`
- `colombia_modeling_table_h4_75pct_v1.csv`
- `colombia_modeling_table_all_horizons_v1.csv`
- `colombia_feature_assembly_diagnostics_v1.csv`
- `colombia_feature_assembly_v1.meta.json`

Future safe repo report: `docs/colombia_lag_feature_assembly_report.md`.

## 12. Quality checks required later (in the assembly report)
- Input + output file paths and **SHA256** checksums.
- Row counts by split.
- **h=4 modelable rows** (climate-modelable **and** M1/M4/M5 recent-surveillance-modelable, separately — §7a).
- Full lag-0–8 climate availability (expected 100%).
- Recent-case lag availability (`cases_lag{0,1,2,4}`) by split.
- Missingness by feature group.
- Duplicate `GID_2 × week_start` check.
- Confirmation of **no leakage**; that **labels/thresholds were not recomputed**; that **no models/metrics/external validation** were run.

## 13. Stop rules for the later feature-assembly step
Stop and report (await approval) if:
- Required input files missing or required columns absent.
- Duplicate `GID_2 × week_start` keys appear unexpectedly (note: the Socorro/Palmas-del-Socorro fold is already resolved upstream; any *new* duplicate is unexpected).
- Climate lag-0–8 availability is **not 100%** for the corrected primary panel.
- h=4 climate-modelable rows differ materially from **127,703** without explanation.
- Recent-case lag availability is **too sparse** for M1/M4/M5 (report the count; do not silently proceed).
- **Any feature uses future information.**
- The train/val/test split is changed or cannot be applied.
- Labels or thresholds are accidentally recomputed.
- **Do not force through silently; report and ask before changing definitions.**

## 14. Confirmation
- **No lag-feature values assembled.**
- **No modeling table created.**
- **No labels or thresholds recomputed.**
- **No models run.**
- **No metrics computed** (no AUC/PR-AUC/calibration/DCA/net-benefit/ΔNB/regression/forecast).
- **No external validation performed.**
- **No data files created or committed.**
- **This is a specification-only markdown commit candidate** (pending approval).
