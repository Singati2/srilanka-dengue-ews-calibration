# E1 — Decision-Threshold / ΔNB Robustness Specification (memo only — NO analysis run)
*Specifies a threshold-robustness check: is the hybrid model's net-benefit advantage over recent-case surveillance robust across operational decision thresholds p\*=0.10–0.50, or only at the registered p\*=0.30? **Specification only: no analysis run, no metrics computed, no models refit, no predictions generated, no labels/thresholds recomputed, no data/quarantine outputs modified, no data files created or committed.** Reuses already-generated predictions/DCA outputs only.*

**Date:** 2026-06-18 · **Status:** specification only · **Base commit:** b315b97 · **Builds on:** `docs/paper_strategy_reframe_memo.md` (experiment E1), `docs/colombia_model_ladder_report.md`, `docs/colombia_horizon_sensitivity_report.md`.

## 1. Purpose
- Assess whether the **hybrid-vs-surveillance ΔNB advantage is robust across p\*=0.10–0.50**.
- Protect against the reviewer criticism that **p\*=0.30 was cherry-picked**.
- **Keep p\*=0.30 as the registered primary threshold;** threshold robustness is **sensitivity/supporting evidence**, not a re-registration.

## 2. Scientific rationale
- Decision-curve analysis is **threshold-dependent**; a model can help at one action threshold and not another.
- The paper is framed around **decision value (net benefit), not AUC** — so the operational claim specifically requires showing whether ΔNB is stable across plausible action thresholds.

## 3. Primary settings
- **Colombia h=4 primary:** M5 vs M1 and M4 vs M1.
- **Colombia horizon sensitivity:** M5 vs M1 across h=1,2,4,8,12.
- **Sri Lanka primary (conditional):** hybrid/climate models vs M1 — **only if** stored Sri Lanka per-row predictions or threshold-resolved DCA outputs are available in the repo/quarantine; otherwise report Colombia-only and flag Sri Lanka as **pending/locate-first** (do not fabricate).

## 4. Threshold grid
- **Reporting grid:** p\* = 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50.
- May also use the existing full DCA grid (p=0.05–0.50) for the curve figures, but the **robustness reporting/CI grid is 0.10–0.50**.

## 5. Primary estimands (per threshold)
- NB(M1), NB(M4), NB(M5), treat-all NB, treat-none NB (=0).
- ΔNB(M4 − M1), **ΔNB(M5 − M1)** ← **primary estimand across p\*=0.10–0.50**.

## 6. Uncertainty
- **What already exists vs what must be recomputed (key implementation note):** the committed bootstrap files (`…bootstrap_ci_h4_75pct_v1.csv`, `…horizon_bootstrap_ci_v1.csv`) contain ΔNB CIs **only at p\*=0.30**; the committed DCA files contain **point** NB per model across thresholds. **Threshold-specific ΔNB CIs do not yet exist** → the later run must recompute them **by reusing the stored per-test-row predictions** (`colombia_model_predictions_h4_75pct_v1.csv`, `colombia_horizon_predictions_v1.csv`, which hold per-row recalibrated probabilities + `y` + `GID_2`). **No model refit, no new predictions.**
- **Bootstrap:** GID_2 cluster bootstrap (Colombia) / RDHS cluster bootstrap (Sri Lanka); **B=1000 if feasible; seed 20260612 (Colombia)**; resample clusters with replacement (all weeks of a unit kept together); **percentile 95% CI for ΔNB at each threshold**; report **failure rate** (exclude/flag any degenerate resample). **Do not compute now.**

## 7. Data/source rules
- Use **already-generated prediction/DCA outputs only**; **do not refit models, recompute predictions, or alter model outputs.**
- **Do not overwrite** the committed h=4 (`model_ladder_h4_75pct_v1/`) or horizon (`horizon_sensitivity_v1/`) directories.

## 8. Outputs to generate later (NOT now)
Quarantine dir `~/data_quarantine/colombia_model_pilots/decision_threshold_dnb_robustness_v1/`:
- `decision_threshold_dnb_metrics_v1.csv` · `decision_threshold_dnb_ci_v1.csv` · `decision_threshold_dnb_curves_v1.csv` · `decision_threshold_dnb_robustness_v1.meta.json`.

Future safe repo files: `scripts/decision_threshold_dnb_robustness_v1.py`, `docs/decision_threshold_dnb_robustness_report.md`.

## 9. Planned figures/tables
- **Figure:** ΔNB(M5−M1) vs threshold (p\*=0.10–0.50) with 95% CI (Colombia h=4).
- **Figure:** Colombia h=4 decision curve — M1/M4/M5/treat-all/treat-none.
- **Heatmap:** horizon (h=1,2,4,8,12) × threshold (0.10–0.50) of ΔNB(M5−M1).
- **Table:** thresholds at which ΔNB(M5−M1) 95% CI excludes 0 (per setting/horizon).

## 10. Stop rules for the later run
Stop and report (await approval) if:
- Required prediction/DCA outputs are missing.
- The h=4 result **cannot be reproduced** from existing outputs (point ΔNB@0.30 must match the committed +0.018/+0.019).
- The threshold grid differs from spec without approval.
- Row sets differ across compared models (must be the same common-complete rows per setting/horizon).
- Bootstrap failure rate is high.
- Outputs would overwrite prior results (use the new versioned dir).
- The analysis accidentally **refits models or recomputes predictions**.
- *Do not force through silently; report and ask.*

## 11. Interpretation rules
- ΔNB(M5−M1) **positive with CI excluding 0 across most thresholds** → hybrid advantage is **threshold-robust**.
- Positive **only near p\*=0.30** → **threshold-sensitive** (temper the operational claim).
- ΔNB **crosses zero at many thresholds** → soften the operational claim.
- If M4/M5 improve **AUC but not ΔNB** → do **not** claim operational benefit.
- **Do not change the h=4 primary result;** this is sensitivity evidence.

## 12. Confirmation
- **No analysis run. No metrics computed. No models refit. No predictions generated. No labels/thresholds recomputed. No data/quarantine outputs modified.**
- **Specification-only memo.** **No data files committed** (pending approval).
