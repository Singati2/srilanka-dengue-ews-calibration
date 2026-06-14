# Canonical R `dlnm` Climate Comparator — Report
*Executed per the locked spec (`docs/canonical_R_dlnm_install_and_run_spec.md`, commit 8a92041) using **real R `dlnm` 2.4.10** (loaded successfully). All computed artifacts are **quarantined and git-ignored**; only this markdown report is proposed for commit. No frozen outcome/exposure/population, no v1/v2 table, and no prior pilot/sensitivity/recalibration/CI/Python-DLNM/hybrid output was modified. **This is canonical `dlnm::crossbasis` + GLM — NOT EWARS-csd Bayesian INLA.***

**Date:** 2026-06-14

## 1. Environment (verified, recorded)
- **R 4.6.0** (2026-04-24); **dlnm 2.4.10** (current CRAN, Depends R≥4.4); **mgcv 1.9.4**; tsModel 0.6-2. `library(dlnm)`/`library(mgcv)` loaded successfully → the "canonical R dlnm" condition is met (not the Python approximation).
- `sessionInfo`: `~/data_quarantine/model_pilots/canonical_R_dlnm_v1/R_sessionInfo_v1.txt` (sha256 `e5f28716…`).

## 2. Identical-row stop-gate (passed)
Train 6,590 / **test 3,926** — the **identical committed test rows**; labels match the committed primary predictions exactly; all comparators (M1/M2/M3/Python-DLNM/M5) present on all 3,926 rows. Test prevalence 0.336.

## 3. Model actually fit
Per climate variable (temperature `t2m_mean_c`, precipitation `precip_sum_mm`, relative humidity `rh_mean_percent`): `crossbasis(Q, lag=c(0,8), argvar=list(fun="ns", df=3), arglag=list(fun="ns", df=3))` where Q is the n×9 lag matrix. **Value and lag spline knots resolved on TRAIN and reused on TEST** (via `attr(cb,"argvar")`/`arglag`) — no test leakage. Logistic `glm(y ~ cb_temp + cb_precip + cb_rh, family=binomial)` fit on train (27 cross-basis features); scored on the identical test rows.

## 4. Diagnostics
**Converged: yes; no separation** (max|coef| 4.03; 27 features). No stop-gate triggered. Deterministic.

## 5. Metrics (test, prevalence 0.336)
| Model | AUC | PR-AUC | Brier | CITL | slope | NB@0.30 |
|---|---|---|---|---|---|---|
| M1 lagged-AR | **0.7515** | 0.652 | 0.191 | +0.513 | 1.246 | **0.1366** |
| M2 climate-only | 0.6429 | 0.460 | 0.220 | +0.479 | 1.027 | 0.0687 |
| M3 climate+season+RDHS | 0.6519 | 0.476 | 0.220 | +0.596 | 0.738 | 0.0780 |
| Python DLNM (approx) | 0.7135 | 0.545 | 0.203 | +0.438 | 0.944 | 0.1112 |
| **Canonical R DLNM** | **0.7139** | 0.541 | 0.203 | +0.438 | 0.905 | **0.1120** |
| M5 hybrid (reference) | 0.7715 | 0.667 | 0.180 | +0.440 | 1.077 | 0.1447 |

## 6. DCA threshold band (net benefit)
| p\* | M1 | M2 | M3 | Python-DLNM | **Canonical R DLNM** | M5 (ref) |
|---|---|---|---|---|---|---|
| 0.20 | 0.1849 | 0.1644 | 0.1469 | 0.1794 | 0.1811 | 0.1944 |
| 0.30 | **0.1366** | 0.0687 | 0.0780 | 0.1112 | 0.1120 | 0.1447 |
| 0.40 | **0.0825** | 0.0123 | 0.0391 | 0.0569 | 0.0530 | 0.1066 |

## 7. ΔAUC / ΔNB with RDHS-cluster bootstrap 95% CI (seed 20260612, B=1000, 0 failures)
| Comparison | metric | point | 95% CI | excludes 0? | favored |
|---|---|---|---|---|---|
| **R-DLNM − Python-DLNM** | ΔAUC | +0.0003 | [−0.005, 0.007] | **No** | — (indistinguishable) |
| **R-DLNM − Python-DLNM** | ΔNB@0.30 | +0.0008 | [−0.005, 0.007] | **No** | — (indistinguishable) |
| **R-DLNM − M1** | ΔAUC | **−0.038** | [−0.066, −0.008] | **Yes** | **M1** |
| **R-DLNM − M1** | ΔNB@0.30 | **−0.025** | [−0.041, −0.006] | **Yes** | **M1** |
| R-DLNM − M2 | ΔAUC | +0.071 | [0.028, 0.110] | Yes | R-DLNM |
| R-DLNM − M2 | ΔNB@0.30 | +0.043 | [0.016, 0.070] | Yes | R-DLNM |
| R-DLNM − M3 | ΔAUC | +0.062 | [0.033, 0.091] | Yes | R-DLNM |
| R-DLNM − M3 | ΔNB@0.30 | +0.034 | [0.017, 0.054] | Yes | R-DLNM |

R-DLNM vs Python-DLNM per-row max|Δ prob| = 0.150 (aggregate metrics statistically indistinguishable). Bootstrap failure rate 0% (0/8000).

## 8. Does the canonical run change the scientific conclusion?
**No — it strengthens it, and validates the approximation.**
- **The Python cross-basis is validated:** canonical R `dlnm` 2.4.10 is **statistically indistinguishable** from the Python approximation on both AUC and net benefit (ΔAUC and ΔNB CIs include 0). This **removes the "Python approximation, not real DLNM" reviewer objection** — the prior DLNM/hybrid results stand as reported.
- **Recent-cases surveillance is hard to beat operationally — now with canonical DLNM:** the real `dlnm` model **still significantly loses to M1** on both AUC (ΔAUC −0.038, CI excludes 0) and net benefit at the registered p\*=0.30 (ΔNB −0.025, CI excludes 0). M1 leads across the operational band (0.30, 0.40).
- **Climate structure helps but isn't enough:** canonical R DLNM **significantly beats the simple climate logistics M2/M3** (ΔAUC/ΔNB exclude 0) — consistent with the Python result.
- **No model-winning claim;** canonical R DLNM did **not** beat M1 on ΔNB. **No headline change.** The M5 hybrid remains the near-miss (reference row), unchanged.

## 9. Scope note (important)
This is **canonical R `dlnm::crossbasis` + frequentist GLM** with the *current* CRAN `dlnm` 2.4.10 — the field-standard DLNM construction. It is **not** the full **EWARS-csd DLNM + INLA Bayesian** operational system (Schlesinger 2024); an INLA implementation is a separate, heavier, gated step. The manuscript may now state "canonical R `dlnm`" for this comparator (the package loaded and ran), while still scoping the spatial-Bayesian EWARS comparison as future work.

## 10. Output files (quarantined, read-only, NOT committed) + SHA256
- `canonical_R_dlnm_predictions_v1.csv` — `8a69cae9…01557c`
- `canonical_R_dlnm_metrics_v1.csv` — `ef30b3ff…d1f6cf`
- `canonical_R_dlnm_dca_v1.csv` — `c2db5530…04dbd`
- `canonical_R_dlnm_ci_v1.csv` — `bf567919…b0e859`
- `canonical_R_dlnm_diagnostics_v1.csv` — `7701c217…60ec1d`
- `R_sessionInfo_v1.txt` — `e5f28716…1fd063`
- Metadata: `canonical_R_dlnm.meta.md`; runner `_run_canonical_R_dlnm.R`; design `_design_for_R.csv` (all under `~/data_quarantine/model_pilots/canonical_R_dlnm_v1/`).

## 11. Confirmations
- Canonical R `dlnm` 2.4.10 used (loaded); Python approximation **not** used for this fit (only for identical-row metric computation with the established harness).
- **No new labels; no frozen data/v1/v2 modified; no prior pilot/sensitivity/recalibration/CI/Python-DLNM/hybrid output overwritten** (new directory only; identical-row stop-gate passed).
- **No data files committed** — only this markdown report is proposed for commit. Preregistration unchanged.
