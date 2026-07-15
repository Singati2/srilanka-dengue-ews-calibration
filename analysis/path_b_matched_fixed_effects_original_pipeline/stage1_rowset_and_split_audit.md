# Stage 1 — Row-set and Split Audit

Read-only; counts read from the frozen modeling table and confirmed against the script's own guard (script:103–106).

## Primary row set
- Definition: `common_complete_M1_to_M5_h4 == True` (script:102) — rows where all of M1–M5 have complete features, so every model is scored on identical observations.
- Split counts (observed == script's hard-coded expectation, so no drift):
  | split | rows |
  |---|---|
  | train (2006–2017) | 53,711 |
  | val (2018–2019) | 12,713 |
  | **test (2020–2022)** | **13,361** |
- Departments: **32**; test prevalence **0.3753**.
- The script raises `RuntimeError` if these counts differ (script:105–106), so any Stage-2 rerun that proceeds has, by construction, the identical row set.

## Split semantics
- Train → fit + train-only scaler; Validation → tune `C` (log loss) and fit Platt recalibration; Test → scored **once**. (script:42–51, 71–82.)
- The matched baseline uses the **same** split and the **same** three roles — no change.

## Fairness confirmation for the matched contrast
- M1, M5, and `M5_no_climate_matched` will all be scored on the **same 13,361 test rows** with the **same `label_h4`** outcome.
- Horizon (h=4) and threshold (p*=0.30) are fixed constants (script:15); unchanged.
- The only structural difference between M5 and the matched baseline is the presence/absence of the 18 climate columns; all rows, preprocessing, penalty/tuning, and recalibration are identical.

## Not modified
No original file altered. No rows recomputed. Labels/thresholds are consumed as-is from the frozen table (`labels_thresholds_recomputed=False` in the frozen meta.json).
