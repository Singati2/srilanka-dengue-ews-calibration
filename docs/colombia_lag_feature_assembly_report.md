# Colombia Lag-Feature Assembly Report (COMPLETED — feature values only; NO models)
*Assembled per `docs/colombia_lag_feature_assembly_spec.md`. **Feature values + modelable flags only. No models, no metrics (AUC/PR-AUC/calibration/DCA/net-benefit/ΔNB), no external validation. Labels and thresholds were NOT recomputed.** Climate lags from the full gap-free grid; recent-case lags from the observed OpenDengue panel (absent = missing, not zero). Generated tables are quarantined; only this report + the script are committed.*

**Date:** 2026-06-18 · **Status:** completed · **Base commit:** 84ad43f · **Spec:** `docs/colombia_lag_feature_assembly_spec.md` · **Script:** `scripts/colombia_lag_feature_assembly_v1.py`.

## 1. Inputs + SHA256 (16-char)
- climate grid `…/colombia_climate_linkage_full_v1/colombia_weekly_climate_precip_temp_gid2_v1.csv` — `b4c164d24744c1a5…`
- labels `…/colombia_label_features_v1/colombia_labels_h1_h2_h4_h8_h12_v1.csv` — `bd37e68ab37eeabb…`
- thresholds (read-only reference) `colombia_label_thresholds_train_only_v1.csv` — `23710e8cf82a1472…`
- lag-availability (reference) `colombia_lag_feature_availability_v1.csv` — `89bf2125bf53d2dd…`

## 2. Outputs (quarantine, read-only; NOT committed) + SHA256 (16-char) / size
- `colombia_lag_feature_values_v1.csv` — `d380a9e752275958…` — 131,698,269 B (feature matrix, 198,195 rows)
- `colombia_modeling_table_all_horizons_v1.csv` — `d7512eeffd29ebda…` — 139,793,530 B (features + labels h1/h2/h4/h8/h12 + flags)
- `colombia_modeling_table_h4_75pct_v1.csv` — `bfb2a5369f53d4e6…` — 88,863,580 B (label_h4-defined rows + features + flags)
- `colombia_feature_assembly_diagnostics_v1.csv` — `a1c73402ae17dd4b…` — 1,321 B
- `colombia_feature_assembly_v1.meta.json` — `fdf49cb15d5398c2…` — 1,864 B
- All under `~/data_quarantine/colombia_label_features_v1/`, chmod 444.

## 3. Row counts by split (base panel = 198,195)
- Train 135,468 · Validation 27,224 · Test 35,503.

## 4. Climate-lag availability (verification)
- **Full lag-0–8 (precip + temp) complete: 198,195 / 198,195 = 100.0%** — pulled from the gap-free climate grid (warm-up weeks cover lag-8). No imputation; no future values.

## 5. Recent-case lag availability (observed panel; absent = missing)
| Feature | present | % of panel |
|---|---|---|
| cases_lag0 (t) | 198,195 | 100.0% |
| cases_lag1 (t−1) | 132,303 | 66.8% |
| cases_lag2 (t−2) | 130,500 | 65.8% |
| cases_lag4 (t−4) | 127,703 | 64.4% |
- Missing recent-case lags are **flagged** (`cases_lag{1,2,4}_missing`), not imputed; absent-as-zero is **not** used (a possible later sensitivity only).

## 6. M2/M3 climate-modelable h=4
- **127,703** (train 86,701 / val 19,356 / test 21,646) — matches the corrected expectation; the binding constraint is the future-outcome label, not climate lags.

## 7. M1 / M4 / M5 / common-complete h=4
- **modelable_M1_h4 = modelable_M4_M5_h4 = common_complete_M1_to_M5_h4 = 79,785** (train 53,711 / val 12,713 / test 13,361).
- **Smaller than M2/M3 (127,703)** because M1/M4/M5 additionally require `cases_lag{0,1,2,4}` present (contiguous recent reporting in the unbalanced panel) — exactly the differential flagged in spec §7a. The three coincide because the common-complete condition (label + climate + recent-case lags) is the binding set for all recent-surveillance/hybrid models.
- **Comparison guidance (per spec):** the head-to-head M1–M5 comparison should use the **common complete-case set (79,785 h=4 rows)** so all models are scored on identical rows; model-specific supersets may be reported as secondary.

## 8. Feature missingness by group
- **Climate lags (precip_lag0–8, temp_lag0–8):** 0 missing (100% complete).
- **Climate summaries:** complete wherever the underlying lags are (100%).
- **Recent-case lags:** lag0 0% missing; lag1 33.2%; lag2 34.2%; lag4 35.6% (panel-limited; flagged).
- **Seasonal terms:** deterministic, 0 missing.

## 9. Duplicate `GID_2 × week_start` check
- **0 duplicates** (Socorro/Palmas-del-Socorro fold already resolved upstream).

## 10. Labels / thresholds not recomputed
- Confirmed — label and threshold files read-only; SHAs unchanged after assembly (`bd37e68a…` labels, `23710e8c…` thresholds). No horizon redefined.

## 11. No leakage
- Climate lag k uses week t−k only; recent-case lags use t−j (observed) only; seasonal terms are deterministic-calendar. The future outcome enters **only** as the label. Thresholds remain train-only (unchanged).

## 12. Stop-rule assessment (final)
| Stop rule | Status |
|---|---|
| Inputs/columns present | PASS |
| Duplicate keys | PASS (0) |
| Climate lag-0–8 = 100% | PASS |
| M2/M3 h4 == 127,703 | PASS |
| Recent-case lags too sparse for M1/M4/M5 | PASS — reduced to 79,785 but ample (53,711 train) |
| Any feature uses future info | PASS (none) |
| Split changed | PASS (unchanged) |
| Labels/thresholds recomputed | PASS (no) |
| Model fitting began | PASS (none) |

## 13. Confirmations
- **No models, no metrics, no external validation.** Feature values + modelable flags only.
- **No labels or thresholds recomputed.** No Sri Lanka data or prior climate/label outputs modified (inputs read-only).
- **Generated data kept out of git** (quarantine, read-only); only this report + `scripts/colombia_lag_feature_assembly_v1.py` are proposed for commit (pending approval).

## 14. Next gate (separate)
Model specification + fitting (M0–M5) with calibration / decision-curve net-benefit evaluation on the **common complete-case h=4 set (79,785 rows; 1,063 units)** — gated and not started.
