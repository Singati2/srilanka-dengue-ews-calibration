# Task 1 — Recalibration estimand audit AND computation

## 1a. What "+0.015" was
The manuscript's Sri Lanka "+0.015 [+0.006, +0.025]" was **recal(M5) − recal(M1)** — the *unmatched* frozen contrast.
- Source: `analysis/v12_referee_response/run/sl_matched_recal_results.json`, field `B_pastonly_recal.dNB_M5_M1_recal` = 0.01539, CI `dNB_M5_M1_recal_ci` = [0.006, 0.02504].
- Model pair: recalibrated M5 vs recalibrated **frozen M1** (M1 fit near-unpenalized C=1e6, AR-only standardization — different from M5). Procedure: past-only rolling-52-week intercept recalibration, eligibility `target_week < prediction_week`, 26-RDHS cluster bootstrap (seed 20260612), test rows (n=3,926). **Not the matched estimand.**

## 1b. Branch: UNMATCHED (expected) → computed the recalibrated MATCHED contrast
Script: `recal_matched.py` (reproduces frozen M1/M4/M5 to ≤1.1e-16 before reporting; gate enforced). Applied the **identical** past-only rolling-52 recalibration (same window, rolling form, leakage-free eligibility, early-week handling, evaluation rows) to the independently refit **M5_no-climate**, then computed recal(M5) − recal(M5_no-climate) at p*=0.30 with the same 26-RDHS cluster bootstrap (seed 20260612). This is a post-fit transform; no fitted model was altered. Results (`recal_matched_results.json`):

| Contrast | Point | 95% CI | Zero? |
|---|---|---|---|
| Raw matched  M5 − M5_no-climate | **+0.0087** | [−0.0015, +0.0188] | includes |
| **Recalibrated MATCHED  recal(M5) − recal(M5_no-climate)** | **+0.0157** | **[+0.0066, +0.0257]** | **EXCLUDES** |
| Recalibrated unmatched  recal(M5) − recal(M1) | +0.0154 | [+0.0064, +0.0255] | excludes |
| Raw frozen  M5 − M1 | +0.0081 | [−0.0025, +0.0180] | includes |

Selected penalty C = 10.0 for both M5 and M5_no-climate. Validation max|Δ|: M1 8.9e-16, M4/M5 1.1e-16.

## Finding (branch outcome)
**The recalibrated MATCHED CI excludes zero → the "recalibration rescues the Sri Lanka matched increment from zero" claim is SUPPORTED, now stated on the matched contrast: +0.0157 (95% CI +0.0066 to +0.0257).** The paper's "+0.015" (unmatched recal M5−M1 = +0.0154) was numerically almost identical by coincidence, but is now reported only as an explicitly labeled frozen-pipeline **operational sensitivity**, never as the matched increment.

## 1c. Consequence stated in the paper
The Sri Lanka matched climate increment is **not distinguishable from zero on raw predictions (+0.0087, CI includes zero)** and **separates from zero only after past-only recalibration (+0.0157, CI excludes zero)** — its separation from zero is recalibration-dependent, and is no longer asserted on the strength of the unmatched M5−M1.
