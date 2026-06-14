# Specification — Hybrid (Surveillance + Climate) Model Extension (design-lock)
*Pre-computation design lock for testing whether a **hybrid** recent-cases + lagged-nonlinear-climate model can outperform the recent-cases baseline (M1). **No models run; no metrics computed; no labels created; no data modified.** Documentation only. Extends the committed primary pilot / S1–S3 / recalibration / CI / DLNM evidence; does not change the primary analysis or headline.*

**Date:** 2026-06-14 · **Status:** specification only — locks models, evaluation, and **strict winning criteria** before any computation, to prevent post-hoc model shopping or threshold tuning.

## 1. Purpose
- Test whether **adding lagged nonlinear climate information to the recent-cases baseline** improves **operational decision value**.
- This is the **legitimate route to a model-winning paper**: not "climate-only vs surveillance" (which lost — see DLNM report `00111b2`), but **hybrid surveillance + climate vs surveillance-only (M1)**.
- Motivation from committed evidence: M1 beats simple climate (M2/M3) and the DLNM-style climate-only model; the DLNM cross-basis significantly beats M2/M3 (climate signal is real) but still loses to M1 at p\*=0.30. The open question is whether climate adds **incremental** operational value **on top of** recent cases.

## 2. Primary hypothesis
**M4 (hybrid) improves over M1 on the primary registered decision metric** — pre-specified:
- ΔNB at **p\*=0.30**, **h=4 weeks**, **75th-pct label**, **test 2023–2025**, **same modelable rows** as the primary pilot;
- **win declared only if the RDHS-cluster bootstrap 95% CI for ΔNB(M4 − M1) excludes 0 (positive).**

## 3. Primary model candidates (no model zoo)
- **M1 — recent-cases AR baseline:** the existing committed model (incidence lags t, t−1, t−2, t−4 + harmonics + RDHS FE), reused/refit identically on the same train; reference.
- **M4 — hybrid (primary new model):** M1's **lagged dengue features** **+** the **DLNM-style climate cross-basis** (lags 0–8 wk; temperature, precipitation, relative humidity; natural cubic spline value × lag, df=3), in **one penalized logistic regression**; all preprocessing train-only.
- **M5 — hybrid + season + RDHS FE (steelman sensitivity):** M4 plus annual/semiannual harmonics and RDHS fixed effects; penalized logistic; reported as a sensitivity, not the primary.
- **Optional M6 (NOT this run; pre-approval required):** gradient-boosting / ensemble hybrid — explicitly **deferred**.

The contrast that matters is **M4 vs M1** (does climate add value on top of surveillance?) and **M4 vs the DLNM climate-only** (does surveillance add value on top of climate?).

## 4. Evaluation cell (identical to primary)
h=4; 75th-pct label (train-only thresholds); train 2018–2022 / test 2023–2025; same filter & **same modelable rows**; metrics on the **identical test rows** as M1/M2/M3/DLNM; DCA at **p\*=0.30** plus band **p\*=0.20–0.40** (full curve 0.05–0.50 also produced).

## 5. Leakage & tuning rules
- **All** preprocessing, spline knots, scaling, imputation, and **regularization tuning** learned on **train only**.
- **No** test data used for model selection; **no** post-hoc feature selection using test outcomes; **no** threshold optimization on test.
- If penalty strength is tuned, use **train-only rolling-origin validation** or a **fixed small grid** (e.g., C ∈ {0.1, 1, 10}), selection criterion = train/internal-validation likelihood — **reported**.
- **M4 vs M5 are both reported**; neither is chosen on test performance. M4 is the locked primary regardless of which scores higher.
- **Stop** if leakage or test/train row mismatch cannot be avoided.

## 6. Complexity control
- Penalized logistic regression (L2; mild L2 default, tuned per §5).
- **Fixed** climate variables (temp, precip, RH) and **fixed** lag window (0–8 wk) — already justified by committed S2 / DLNM reports; **no** scanning of many df/lag combinations.
- DLNM basis **df=3 primary**; **df=4 only as the already-specified sensitivity**.
- Feature count kept modest (M4 ≈ AR lags + harmonics + RDHS FE + 27 cross-basis terms); report it.
- **Stop** if separation or unstable coefficients cannot be resolved by mild regularization (one fallback, then stop and report).

## 7. Metrics
AUC, PR-AUC, Brier, calibration-in-the-large, calibration slope, net benefit at p\*=0.30, threshold-band DCA; **ΔAUC and ΔNB vs M1** on identical rows; **RDHS-cluster bootstrap 95% CI** (seed 20260612, B=1000, as in the committed CI/DLNM steps) for ΔAUC and ΔNB(M4 − M1) and (M5 − M1).

## 8. Winning criteria (strict, pre-specified)
**A primary model-winning claim is permitted ONLY if ALL hold:**
1. M4 (or M5) has **higher NB@p\*=0.30 than M1**; **and**
2. **ΔNB(model − M1) 95% CI excludes 0** (positive); **and**
3. calibration is **not meaningfully worse** than M1 (CITL/slope not materially degraded; recalibration option noted); **and**
4. the advantage is **not limited to one cherry-picked threshold** (holds across the p\*=0.20–0.40 band, not solely at 0.30); **and**
5. **no leakage and no row mismatch** (stop-gate passed).

**If only AUC improves but ΔNB does not** (CI includes 0 or NB not higher): **do not** call it model-winning → report as *"discrimination improvement without an operational decision-value gain."*

**If M4/M5 loses to M1** (or ties): report honestly → the existing **calibration / decision-evaluation / data-resource** framing stands; the paper remains as currently positioned. **No headline change without team review** in any case.

## 9. Outputs (LATER, not now) — quarantined only
Future directory: `~/data_quarantine/model_pilots/hybrid_model_extension_v1/`
- `hybrid_metrics_v1.csv`, `hybrid_dca_v1.csv`, `hybrid_predictions_v1.csv`, `hybrid_ci_v1.csv`, `hybrid_diagnostics_v1.csv`, `hybrid_model_extension.meta.md`.
CSVs read-only with SHA256; **none committed**. Future safe report: `docs/hybrid_model_extension_report.md`. Prior pilot/sensitivity/recalibration/CI/DLNM directories **not** overwritten.

## 10. Confirmation
- **No models run; no metrics computed; no labels created; no data modified.**
- **Only this markdown spec was created.** Nothing committed. Preregistration unchanged.

## Next step (separate, approval-gated)
On approval: verify the primary test-row set, fit M4 (and M5 sensitivity) with train-only tuning, score the identical test rows, compute metrics + ΔAUC/ΔNB vs M1 with bootstrap CIs, apply the §8 winning criteria, write quarantined outputs + a safe markdown report. Nothing runs until directed.
