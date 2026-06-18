# Colombia Horizon-Sensitivity Specification (memo only — NO sensitivity run)
*Specifies extending the completed Colombia h=4 model ladder to h=1,2,8,12 under the identical framework. **Specification only: no models, no predictions, no metrics (AUC/PR-AUC/calibration/DCA/net-benefit/ΔNB/bootstrap), no labels/thresholds recomputed, no feature changes, no data modified, no quarantine outputs modified, no data files created or committed.** h=4 remains the primary registered Colombia result; horizon results are secondary/supplementary.*

**Date:** 2026-06-18 · **Status:** specification only · **Base commit:** 635b856 · **Builds on:** `docs/colombia_model_ladder_report.md`, `docs/colombia_model_ladder_spec.md`, `docs/cross_country_interpretation_memo.md`.

## 1. Purpose
- Test whether climate/hybrid **incremental value is horizon-dependent** in Colombia.
- Extend the completed h=4 ladder to **h=1,2,8,12** using the **same** features, models, split, recalibration, and bootstrap.
- **Keep h=4 as the primary registered result;** treat horizon sweep as **secondary/supplementary**, not a replacement.

## 2. Scientific rationale
- Recent dengue cases should be strongest at **short** horizons (autocorrelation / outbreak momentum).
- Climate may become **more useful at longer horizons** if it acts as a leading indicator.
- The cross-country memo selected horizon sensitivity as the most valuable next sensitivity (Colombia-specific lead-time evidence: hydroclimate skillful at 3–6-month leads where AR fails).
- **Delayed-surveillance** remains a runner-up but is more assumption-dependent (OpenDengue has finalized counts, not reporting-delay vintages).

## 3. Horizons
- Evaluate later: **h=1, 2, 4, 8, 12**.
- **h=4 already completed/committed** (primary).
- Sensitivity adds **h=1, 2, 8, 12**; h=4 may be **re-run only as a reproducibility anchor** — must be **byte-identical** to the committed h=4 result or **clearly versioned**, and must **not** overwrite or replace it.

## 4. Labels (do not recompute)
- Use already-created labels from `~/data_quarantine/colombia_label_features_v1/colombia_modeling_table_all_horizons_v1.csv`: `label_h1, label_h2, label_h4, label_h8, label_h12`.
- **Do not recompute labels or thresholds** (train-only 75th-pct, no-assume-zero rule unchanged).

## 5. Feature set (do not change)
- Identical to h=4: climate `precip_lag0–8`, `temp_lag0–8`; recent-case `cases_lag0/1/2/4`; seasonal `sin/cos_woy_1/2`; department fixed effects.
- **No new features; no climate anomalies; no absent-as-zero sensitivity.**

## 6. Row-set rule (per horizon)
For each horizon h, the **primary common-complete M1–M5 row set** requires: `label_h{h}` defined **AND** climate lags 0–8 complete **AND** `cases_lag0/1/2/4` complete, within the committed train/val/test split.
- **Implementation note (keying):** climate-lag and recent-case-lag completeness are **horizon-invariant** (they concern weeks t−k); **only `label_h{h}` definedness (the t+h outcome) varies by horizon.** So per-horizon common-complete = `(climate_lag_complete) ∧ (cases_lag_complete) ∧ (label_h{h} defined)` — **recompute the flag for each h**; do **not** reuse the h=4 `common_complete_M1_to_M5_h4` flag for other horizons.
- **Expected:** common-complete n **decreases as h grows** (fewer t+h outcomes exist), e.g., labelable was 127,703 at h=4 vs 119,085 at h=12 — a normal consequence, not a fault.
- **Report row counts by horizon × split before fitting.** Stop if any horizon's test n is unexpectedly small or has only one outcome class (§13).

## 7. Model ladder (identical to h=4)
- M0 season baseline · M1 recent cases · M2 climate-only · M3 climate+season+department · M4 hybrid · M5 hybrid+season+department.
- Regularized L2 logistic regression; **C tuned by validation log loss** per (horizon, model); **validation only**; **test used once**.

## 8. Primary comparison within each horizon
- **Primary:** **M5 vs M1** (hybrid incremental). Also report **M4 vs M1** and **M2/M3 vs M1** (climate-only).
- **Primary sensitivity question:** *Does ΔNB(M5 − M1) at p\*=0.30 become larger at longer horizons (h=8, h=12)?*

## 9. Metrics for the later run (specify only)
AUC; PR-AUC; Brier; calibration intercept (CITL); calibration slope; net benefit @ p\*=0.30; DCA curve p=0.05–0.50; ΔAUC vs M1; ΔNB vs M1; bootstrap 95% CI for ΔAUC and ΔNB.

## 10. Bootstrap uncertainty (same as h=4)
- **GID_2 cluster bootstrap, seed 20260612, B=1000** (B=200 runtime pilot only if necessary, then stop/report before replacing with B=1000); resample GID_2 units with replacement **within each horizon's test set**; report **failure rate**; exclude single-class resamples for AUC and report failures.

## 11. Recalibration (same as h=4)
- Validation-only Platt/logistic recalibration; report **raw and recalibrated** separately where feasible; **never tune recalibration on test**.

## 12. Expected outputs later (NOT now)
Quarantine dir `~/data_quarantine/colombia_model_pilots/horizon_sensitivity_v1/`:
- `colombia_horizon_predictions_v1.csv` · `colombia_horizon_metrics_v1.csv` · `colombia_horizon_dca_v1.csv` · `colombia_horizon_bootstrap_ci_v1.csv` · `colombia_horizon_contrasts_v1.csv` · `colombia_horizon_sensitivity_v1.meta.json`.

Future safe repo files: `scripts/colombia_horizon_sensitivity_v1.py`, `docs/colombia_horizon_sensitivity_report.md`. **The h=4 committed outputs (`model_ladder_h4_75pct_v1/`) must not be overwritten** (new versioned dir).

## 13. Stop rules for the later run
Stop and report (await approval) if:
- The all-horizons modeling table is missing or required `label_h{h}` columns are absent.
- Any horizon's row count is unexpectedly low, or any horizon's **test split has only one class**.
- Labels or thresholds are recomputed; the train/val/test split changes; test data are used in preprocessing/tuning.
- Any model fails to converge without documented handling.
- The **h=4 re-run differs materially** from the committed h=4 result without explanation.
- Metrics for different horizons use **inconsistent row-set rules**, or model-specific row sets are confused with common-complete primary sets.
- Output would **overwrite prior h=4 outputs** without versioning.
- *Do not force through silently; report and ask.*

## 14. Interpretation rules (pre-specified)
- If **ΔNB(M5−M1) increases at h=8/h=12** → supports **horizon-dependent climate value**.
- If **M1 still dominates at all horizons** → climate adds limited incremental value despite the Colombia h=4 hybrid gain.
- If **climate-only improves at longer horizons but hybrid does not** → interpret cautiously.
- If **AUC improves but ΔNB does not** → operational value not confirmed.
- **Do not change the primary h=4 conclusion;** horizon results are secondary.

## 15. Manuscript use
- Supplementary/secondary results; candidate **heatmap (horizon × model ΔNB)** and **line plot ΔNB(M5−M1) across horizons**. **Not** a replacement for the h=4 primary result.

## 16. Confirmation
- **No models run. No predictions generated. No metrics computed. No labels/thresholds recomputed. No data modified. No quarantine outputs modified.**
- **Specification-only markdown memo.** **No data files committed** (pending approval).
