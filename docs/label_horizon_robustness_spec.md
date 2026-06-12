# Specification — Label / Horizon Robustness Extension (design-lock)
*Pre-computation design lock for the final label/horizon robustness extension. **No models were run; no labels created; no AUC/calibration/DCA/net-benefit/forecast computed.** No frozen outcome/exposure/population, no v1/v2 linked table, and no existing pilot / sensitivity / recalibration output is modified — this memo is documentation only. It extends, and does not replace, the committed primary pilot, S1–S3, and rolling-recalibration results.*

**Date:** 2026-06-12 · **Status:** specification only — locks the grid **before** any computation to prevent post-hoc horizon/threshold selection.

## 1. Purpose
Test whether the study's main conclusion depends on the primary **alert definition** (RDHS 75th-pct) and **forecast horizon** (h=4).
- **Primary question:** does **M1 (recent-cases AR) still dominate M2/M3 (climate)** on discrimination and net benefit when the alert threshold and horizon change?
- Secondary: does the calibration-drift story (correctable by rolling-52 recalibration) hold across labels/horizons?

## 2. Primary baseline to compare against
- **Existing primary result:** h=4 weeks, RDHS-specific 75th-pct label.
- **Committed main conclusion:** M1 dominates climate models (AUC, net benefit); the 2023–2025 calibration drift is real but **operationally correctable** by rolling-52 intercept-only recalibration; **even after recalibration, M2/M3 do not beat M1**.
Every grid cell below is interpreted **relative to this baseline**, not as a new headline.

## 3. Robustness grid (limited, pre-specified — no post-hoc additions)
- **Alert thresholds:** RDHS-specific **75th pct** (primary reference) · **90th pct** (sensitivity).
- **Forecast horizons:** **h = 1, 2, 4, 8, 12 weeks**.
- **Primary robustness combinations (the cells that must run):**
  - 90th-pct × h=4
  - 75th-pct × h = 1, 2, 8, 12
- **Optional cells (run only if computationally easy):** 90th-pct × h = 1, 2, 8, 12.
- 75th-pct × h=4 is the already-committed primary (re-reported as the reference row).
- **No thresholds beyond 75th/90th**; no horizons beyond {1,2,4,8,12}; nothing added post hoc.

## 4. Data & linkage
- **v2 date-aligned table only** (`…_v2_date_aligned.csv`, sha256 `3a197d61…`).
- **Primary modeling filter:** `outcome_missing_flag==0 ∧ exposure_missing_flag==0 ∧ population_missing_flag==0 ∧ 2018 ≤ epi_year ≤ 2025`.
- **Split:** train 2018–2022 / test 2023–2025 (by predictor week *t*).
- **Thresholds estimated on training data only** (per RDHS); no test leakage. Standardization, M0 climatology, and any recalibration are likewise train-only.

## 5. Target construction (per horizon h)
- Target = alert state at **week_start + 7·h days** (calendar date join, **gap-safe** — never a positional shift across dropped weeks).
- Drop rows where the t+h outcome is unavailable (end-of-series or a missing-outcome week); rows dropped per horizon are reported.
- Label event = future incidence(t+h) > RDHS-specific threshold (75th or 90th pct, train-estimated).

## 6. Models (unchanged ladder)
M0 climatological · M1 lagged dengue AR · M2 climate-only · M3 climate + seasonality + RDHS fixed effects. **No new model classes, no feature search, no hyperparameter tuning on test.** Identical specification, standardization (train mean/SD), and solver (logistic, lbfgs, L2 C=1e6) as the primary pilot, refit per grid cell on the cell's training labels.

## 7. Recalibration handling (kept focused)
- **First:** evaluate **raw** predictions for each label/horizon cell.
- **Then:** apply only the **rolling-52-week intercept-only** recalibration (the best simple method in the committed extension) as a secondary operational-calibration check, using the same date-enforced leakage rule (eligible only if target week < prediction week *t*).
- **Do not** rerun the full R0–R4 ladder for every grid cell.
- Report **raw and rolling-52** results **separately** for each cell.

## 8. Metrics (per cell × {raw, rolling-52})
Row counts; event prevalence (overall/train/test); stop-rule result; Brier; calibration-in-the-large; calibration slope; mean predicted vs observed; AUC; PR-AUC; DCA on p\*=0.05–0.50; **net benefit at p\*=0.30**.

## 9. Stop rules (per cell)
- Overall/test event prevalence interpretable: **not <5% or >70%**.
- Enough train/test events (e.g. test events ≥ 50); **flag** horizons/thresholds with sparse events.
- RDHS zero-event counts checked (train and test).
- GLM convergence / no separation.
- A failing cell is **reported as failed/limited, not forced** into interpretation.

## 10. Interpretation rules (pre-committed)
- **If M1 dominates across thresholds/horizons** → the main conclusion is **robust**.
- **If M2/M3 beat M1 only at a specific horizon/threshold** → report as **conditional**; do not overgeneralize.
- **If the 90th-pct label is too sparse** → treat as **limited power**, not as negative evidence against climate models.
- **If rolling recalibration fixes calibration but M1 still dominates** → same conclusion as the current study.
- **Do not** promote the most favorable horizon/threshold to a new headline; report the full grid.

## 11. Outputs to be generated later (NOT now) — quarantined only
Directory: `~/data_quarantine/model_pilots/label_horizon_robustness_v1/`
- `label_horizon_metrics_v1.csv`
- `label_horizon_dca_v1.csv`
- `label_horizon_stop_rules_v1.csv`
- `label_horizon.meta.md`
CSVs made read-only with SHA256 recorded; **none committed**. Safe repo report later: `docs/label_horizon_robustness_report.md` (the only artifact proposed for commit).

## 12. Confirmation
- This memo is **documentation only**; no models run, no labels created, no metrics computed.
- **No data files modified; no frozen files modified; no outputs committed.** The primary pilot, sensitivity, and recalibration directories are untouched. Preregistration unchanged.

## Next step (separate, approval-gated)
On approval, run the pre-specified grid (raw + rolling-52), write the quarantined outputs + a safe markdown report, and apply the §10 interpretation rules. Nothing runs until directed.
