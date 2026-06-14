# Hybrid (Surveillance + Climate) Model Extension — Report
*Executed per the locked spec (`docs/hybrid_model_extension_spec.md`, commit 1d8e268). All computed artifacts are **quarantined and git-ignored**; only this markdown report is proposed for commit. No frozen outcome/exposure/population, no v1/v2 table, and no prior pilot/sensitivity/recalibration/CI/DLNM output was modified. No new labels; no installs. The climate component is the **Python DLNM-style cross-basis approximation**, not canonical R `dlnm`.*

**Date:** 2026-06-14

## 1. Setup & row matching
- Same registered cell: 75th-pct label, h=4, train 2018–2022 / test 2023–2025, same filter.
- **Exact primary-row match (stop-gate passed):** train 6,590, **test 3,926 — identical rows to the committed primary predictions** (`07f5916a…`); M1 reused on those rows; M4/M5 scored on the same rows; labels matched.

## 2. Models fit
- **M1** — recent-cases AR baseline (committed; reference).
- **M4 (primary hybrid)** — recent-cases AR features **+** DLNM-style climate cross-basis (lags 0–8 wk; temp/precip/RH; df=3), one penalized logistic. 31 features.
- **M5 (steelman sensitivity)** — M4 + season harmonics + RDHS fixed effects. 60 features.

## 3. Tuning (train-only)
Penalty strength **C selected by rolling-origin internal validation on the training years only** (fold = predict each later train-year from earlier ones), grid C∈{0.1,1,10}, criterion = mean validation AUC. Selected: **M4 C=0.1**, **M5 C=10**. No test data used for selection; spline knots, imputation, scaling all train-only.

## 4. Fit diagnostics
Both converged, **no separation**, no fallback needed. M4 max|coef| 0.93; M5 1.26. CV-AUC by C: M4 {0.1:0.767, 1:0.763, 10:0.762}; M5 {0.1:0.750, 1:0.758, 10:0.760}.

## 5. Metrics (test, prevalence 0.336)
| Model | AUC | PR-AUC | Brier | CITL | slope | NB@0.30 |
|---|---|---|---|---|---|---|
| **M1 lagged-AR** | 0.7515 | 0.652 | 0.191 | +0.513 | 1.246 | **0.1366** |
| M4 hybrid | 0.7643 | 0.641 | 0.187 | +0.449 | 1.225 | 0.1284 |
| M5 hybrid + season + RDHS | **0.7715** | **0.667** | **0.180** | +0.440 | 1.077 | **0.1447** |

## 6. ΔAUC / ΔNB vs M1 — RDHS cluster bootstrap (seed 20260612, B=1000, 0 failures)
| Comparison | metric | point | 95% CI | excludes 0? |
|---|---|---|---|---|
| M4 − M1 | ΔAUC | +0.013 | [−0.020, 0.046] | **No** |
| M4 − M1 | ΔNB@0.30 | −0.008 | [−0.028, 0.013] | **No** (favors M1) |
| **M5 − M1** | ΔAUC | **+0.020** | **[0.003, 0.040]** | **Yes (M5 better)** |
| M5 − M1 | ΔNB@0.30 | +0.008 | [−0.001, 0.018] | **No (just touches 0)** |

## 7. DCA threshold band (net benefit)
| p\* | M1 | M4 | M5 |
|---|---|---|---|
| 0.20 | 0.1849 | 0.1931 | **0.1944** |
| 0.30 | 0.1366 | 0.1284 | **0.1447** |
| 0.40 | 0.0825 | 0.0869 | **0.1066** |

M5's net benefit exceeds M1 at **all three** band thresholds (point estimates); M4 is mixed (above at 0.20/0.40, below at 0.30).

## 8. Strict winning criteria (pre-registered) — evaluated
| Criterion | M4 (primary) | M5 (steelman) |
|---|---|---|
| 1. NB@0.30 higher than M1 | ✗ (0.128 < 0.137) | ✓ (0.145 > 0.137) |
| 2. ΔNB 95% CI excludes 0 (positive) | ✗ | ✗ (CI [−0.001, 0.018] just includes 0) |
| 3. Calibration not meaningfully worse | ✓ | ✓ |
| 4. Advantage robust across p\*=0.20–0.40 | ✗ | ✓ (point estimates) |
| 5. Same rows, no leakage, no instability | ✓ | ✓ |
| **MODEL-WINNING?** | **No** | **No** (criterion 2 fails) |

## 9. Verdict (locked rules applied)
- **Not model-winning by the strict pre-registered criteria.** **M4 (primary hybrid) does not beat M1** — its net benefit at p\*=0.30 is slightly *lower*, and neither ΔAUC nor ΔNB is significant. Adding the climate cross-basis to the AR baseline did **not** yield an operational decision-value gain.
- **M5 (steelman hybrid) is a genuine near-miss, reported honestly, not as a win:** it shows a **statistically significant discrimination gain** over M1 (ΔAUC +0.020, CI excludes 0), the best Brier/calibration, and **higher net benefit than M1 across the whole p\*=0.20–0.40 band** — but the **ΔNB@0.30 95% CI just includes 0** ([−0.001, 0.018]), so the operational gain is **not confirmed** at the registered threshold. Per the locked rule, this is **"discrimination improvement without a confirmed operational decision-value gain"** — explicitly **not** a model-winning result.
- **Interpretation (honest):** climate *likely* adds *some* incremental value on top of surveillance (M5's direction is consistent and its AUC gain is significant), but this single-country, single-period pilot is **underpowered to confirm an operational net-benefit gain** at p\*=0.30 — the ΔNB CI sits right at the boundary. This motivates a **future, better-powered/confirmatory study** (more years and/or multi-country) as the path to a model-winning claim. It is **neither a flat null nor a win.**
- **No headline change.** The current **calibration / decision-evaluation / data-resource** framing stands; **M5 is flagged for team review** as the most promising direction. **Do not** claim a hybrid win; **do not** claim climate has no value.

## 10. Output files (quarantined, read-only, NOT committed) + SHA256
- `hybrid_model_metrics_v1.csv` — `53afbd2147a810298c855ec9a7b9f86f91fabccb456102cf4e57726c4073604b`
- `hybrid_model_dca_v1.csv` — `56404c8687fd613f6e83e901239f697de7d3cfe460e8a971c8dccec5afe55b5a`
- `hybrid_model_predictions_v1.csv` — `0f505fed6a99b2f367bf2ffa795dce54d6b1ed2fef0f930dc5cda5894030cb93`
- `hybrid_model_ci_v1.csv` — `e441f059905e7813a97860bae9d5ca921fd1a4a4e09a01979459aa3a066e3e59`
- `hybrid_model_diagnostics_v1.csv` — `e7f0acaf2a0473e20eafe77b5aa49bb8a4c11eb88ad5a597f0f77cbd395ac4b6`
- Metadata: `hybrid_model.meta.md` (all under `~/data_quarantine/model_pilots/hybrid_model_extension_v1/`).

## 11. Confirmations
- M4 + M5 only (no M6/boosting/ensemble); train-only tuning; no test-based model selection; both models reported.
- **No new labels; no frozen files modified; no prior pilot/sensitivity/recalibration/CI/DLNM output overwritten** (new directory only; input checksums re-verified; exact row match).
- **No data files committed** — only this markdown report is proposed for commit. Preregistration unchanged. Climate component is a cross-basis approximation, not R `dlnm`.

## 12. Next steps (separate, approval-gated)
Team review of the M5 near-miss; optional rolling-52 recalibration of M4/M5; a power/sample-size note for a confirmatory hybrid study; canonical R `dlnm` only if R installed. Nothing runs until directed.
