# Colombia Model-Ladder Specification (memo only — NO models run)
*Defines the Colombia model ladder and evaluation plan before any fitting. **Specification only: no models, no predictions, no metrics (AUC/PR-AUC/calibration/DCA/net-benefit/ΔNB), no regressions/forecasts, no external validation, no labels/thresholds recomputed, no data files created or committed.** Replicates the Sri Lanka decision-evaluation framework (no coefficient transfer) on Colombia's completed feature panel.*

**Date:** 2026-06-18 · **Status:** specification only · **Base commit:** 82cb580 · **Builds on:** `docs/colombia_lag_feature_assembly_report.md`, `docs/colombia_label_construction_report.md`.

## 1. Purpose
- Define the Colombia model ladder (M0–M5) before any model fitting.
- **Replicate the Sri Lanka decision-evaluation framework** (recent-surveillance vs climate vs hybrid, with calibration + decision-curve net benefit) — **not** transfer Sri Lanka coefficients.
- Compare models under a strict **no-leakage temporal split**.
- Preserve Colombia-specific panel limitations already documented (unbalanced reporting; COVID-era test caveat; 2 island units excluded).
- **Specification only; no models are run in this step.**

## 2. Primary endpoint
- **Primary label:** `label_h4` (Colombia h=4, train-only per-municipality 75th-percentile count threshold).
- **Primary evaluation period:** **test split 2020-01-01 → 2022-12-25**.
- **Primary decision threshold:** **p\* = 0.30** (matching Sri Lanka), for net-benefit/decision-curve evaluation later.
- Keep the **COVID-era test caveat** (reporting continued 2020–2022 — no collapse — but interpret test-period results with that context).
- **Do not redefine labels or thresholds.**

## 3. Primary row set — common-complete M1–M5 (head-to-head)
Use the **common complete-case h=4 set** for the primary M1–M5 comparison: `label_h4` defined **and** climate lag0–8 complete **and** `cases_lag{0,1,2,4}` complete.
- **Expected: 79,785 rows** — train 53,711 / val 12,713 / test 13,361.
- **Rationale:** all models scored on **identical rows**, so differences reflect model behavior, not sample composition. The larger M2/M3 climate-only set is **secondary** (§4).

## 4. Secondary row set — climate-only full
- M2/M3 may **additionally** be evaluated on their full climate-modelable h=4 set: **127,703 rows** — train 86,701 / val 19,356 / test 21,646.
- **Explicitly labeled secondary** — not directly comparable to M1/M4/M5 unless all models are scored on the same rows. Reported as a sensitivity, never as the head-to-head result.

## 5. Train / validation / test split (committed; unchanged)
- Train 2006-12-31→2017-12-31 · Validation 2018-01-01→2019-12-31 · Test 2020-01-01→2022-12-25.
- **Validation used only** for tuning/hyperparameter/recalibration selection. **Test used once** for final evaluation. **No split change without approval.**

## 6. Model ladder
- **M0 — climatology / baseline.** **Primary M0 = intercept + seasonal terms** (Colombia has strong dengue seasonality); intercept-only retained as a diagnostic baseline.
- **M1 — recent-surveillance baseline:** `cases_lag0, cases_lag1, cases_lag2, cases_lag4` (log1p transform pre-specified in §8).
- **M2 — climate-only:** `precip_lag0..8`, `temp_lag0..8`. Optional summary features only if pre-specified here; **no post-hoc additions**.
- **M3 — climate + season + location:** M2 + seasonal sin/cos + location effects (§9).
- **M4 — hybrid:** M1 recent-case features + M2 climate features.
- **M5 — hybrid + season + location:** M4 + seasonal terms + location effects.

## 7. Model implementation (primary class)
- **Regularized logistic regression** (`sklearn.linear_model.LogisticRegression`) for comparability + interpretability, mirroring the Sri Lanka logistic calibration framework.
- **Penalty:** L2 primary. **C** selected on **validation only** (grid, §10). **Solver:** `lbfgs` (or `saga` if high-dimensional sparse location FE). **class_weight:** optional, selected on **validation only** (default none; balanced as a documented alternative).
- **Excluded from the primary replication:** random forests, XGBoost, neural nets, other flexible ML — unless separately specified later.

## 8. Feature preprocessing (train-only fitted)
- **log1p** transform recent-case lags and precipitation features (counts/precip are right-skewed).
- **Standardize** continuous predictors using **training-set mean/SD only**; apply the same train-fitted transform to validation/test. **Never** fit scaling on validation/test.
- **No imputation** of missing recent-case lags in the primary common-complete analysis (rows are complete by construction there).
- **No future information** in any feature.

## 9. Location effects
- **Primary:** **department-level (Admin1, 33) fixed effects** — robust, low-dimensional, avoids the high-dimensional/sparse 1,063-GID_2 design.
- **Alternative:** GID_2 fixed effects with regularization if computationally feasible (documented if used).
- **Encoding rule:** plain categorical (one-hot/dummy) encoding allowed; **target/mean encoding NOT allowed** unless strictly train-only and separately specified (leakage risk). The modeling run must state which option was used and why.

## 10. Hyperparameter selection (validation only)
- **Primary tuning criterion: validation log loss (Brier as secondary)** — selects for **probability quality / calibration**, which is the paper's focus, and avoids tuning to a decision threshold.
- Tune **C** on the validation split by log loss; **report validation net benefit @ p\*=0.30 as a diagnostic only**.
- **Never tune to test net benefit or any test metric.** Recalibration parameters (§11) also selected using train/validation only.

## 11. Evaluation metrics for later (NOT computed now)
- Discrimination: **AUC, PR-AUC**; overall: **Brier**.
- Calibration: **calibration-in-the-large (intercept), calibration slope**, reliability/ECE (calibration belt if used in the SL arm).
- **Recalibration:** train-fit Platt and rolling/time-updated recalibration (mirroring the SL recalibration extension), selection on train/val only.
- Decision-analytic: **net benefit @ p\*=0.30**; decision curve over **p = 0.05–0.50**; **continuous net benefit**.
- **Contrasts:** **ΔAUC** and **ΔNB** of M1 vs M2/M3/M4/M5, on the **common-complete** primary set (M2/M3 full-row as secondary).
- **Uncertainty (framework-aligned):** **municipality (GID_2) cluster bootstrap, seed 20260612, B=1000** for ΔAUC/ΔNB 95% CIs (matching the Sri Lanka RDHS-cluster bootstrap design); report proportion of bootstrap > 0.

## 12. Expected future outputs (NOT now)
Quarantine dir `~/data_quarantine/colombia_model_pilots/model_ladder_h4_75pct_v1/`:
- `colombia_model_predictions_h4_75pct_v1.csv`
- `colombia_model_metrics_h4_75pct_v1.csv`
- `colombia_model_dca_h4_75pct_v1.csv`
- `colombia_model_calibration_h4_75pct_v1.csv`
- `colombia_model_coefficients_h4_75pct_v1.csv`
- `colombia_model_ladder_h4_75pct_v1.meta.json`

Future safe repo report: `docs/colombia_model_ladder_report.md`.

## 13. Stop rules for the later modeling step
Stop and report (await approval) if:
- The required modeling table is missing.
- Common-complete h=4 count differs materially from **79,785** without explanation.
- The train/val/test split differs from spec.
- Labels or thresholds are recomputed.
- **Any test information** is used for preprocessing or tuning.
- Any model fails to converge without documented handling.
- Calibration/DCA code is inconsistent with the Sri Lanka implementation.
- Metrics are computed on different row sets without explicit labeling.
- **Model-specific row-set results are confused with common-complete primary results.**
- *Do not force through silently; report and ask.*

## 14. Interpretation rules (pre-specified)
- If **M1 beats M2/M3** on common-complete rows → recent surveillance dominates climate-only in Colombia.
- If **M4/M5 beats M1** → climate adds incremental value beyond recent surveillance.
- If **M4/M5 improves AUC but not net benefit** → discrimination gain does **not** necessarily translate to operational value (the paper's core point).
- If **climate-only wins only on the larger climate-only set** but not common-complete → treat as **sample-dependent / secondary**, not a real climate advantage.
- **No deployment-readiness claims.** This is **external framework replication**, not global validation, and the COVID-era test caveat applies.

## 15. Confirmation
- **No models run.** **No predictions generated.** **No metrics computed.** **No calibration/DCA/net-benefit computed.**
- **No labels or thresholds recomputed.** **No external validation performed.**
- **No data files created or committed.**
- **This is a specification-only markdown commit candidate** (pending approval).
