# Pilot Report — Existing-Model Calibration / Decision-Curve Evaluation (h=4, RDHS 75th-pct)
*First hardened single-pass pilot, executed exactly per the locked spec (`docs/pilot_existing_model_calibration_dca_spec.md`, commit ee41b46). All computed artifacts (predictions, metrics, DCA, thresholds, model frame) are **quarantined and git-ignored**; only this markdown report is proposed for commit. No frozen outcome/exposure/population or linked-analysis CSV was modified. This is a calibration/decision-evaluation of **existing model classes** — no new forecasting model is proposed.*

**Date:** 2026-06-12

## 1. Input & integrity
- Primary table: `~/data_quarantine/analysis_tables/dengue_climate_population_linked_2018_2025_v2_date_aligned.csv`
- **SHA256 re-verified:** `3a197d610fde721ffdf2be6388df88fea675a5b49bf131a0919fd89ec2518e91` ✅ (read-only, unmodified).

## 2. Row counts
- Primary filter (`3 flags==0 ∧ 2018≤epi_year≤2025`): **10,705 rows**, 26 RDHS, 0 missing (outcome/exposure/pop), 0 duplicate (gid×year×week).
- After h=4 target construction: **10,516 rows** (dropped **189** where the t+4 outcome is unavailable — end-of-series or a missing-outcome week).

## 3. Target construction (h = 4 weeks)
For each RDHS *i*, week *t*, the target is the alert state **4 calendar weeks ahead** (`week_start + 28 days`, gap-safe date join — not a positional shift, so it never crosses a dropped week). Predictors use information available **through week *t*** only.

## 4. Threshold / label construction (no leakage)
- Alert label = future incidence(t+4) **> RDHS-specific 75th percentile** of weekly incidence.
- Thresholds estimated on **training predictor weeks (2018–2022) only**, per RDHS (range **0.7–13.3 /100k** across the 26 divisions; 221–255 training weeks each). Frozen before touching test. Saved: `thresholds_h4_75pct_v1.csv`.

## 5. Event prevalence & train/test split
| Split (by predictor week *t*) | n | events | prevalence |
|---|---|---|---|
| Train 2018–2022 | 6,590 | 1,593 | **24.2%** |
| Test 2023–2025 | 3,926 | 1,321 | **33.6%** |
| Overall | 10,516 | 2,914 | 27.7% |

Per-RDHS: 0 divisions with zero events in either split (train events 51–65; test events 9–113). The **train→test prevalence rise (24%→34%)** reflects higher dengue incidence in 2023–2025 relative to the 2018–2022 endemic baseline — a central driver of the calibration findings below.

## 6. Stop-rule checks (all PASS — models were fit)
| Rule | Result |
|---|---|
| Overall / train / test prevalence within 5–70% | PASS (27.7 / 24.2 / 33.6%) |
| Test events ≥ 50 | PASS (1,321) |
| ≤3 RDHS with zero train events | PASS (0) |
| ≤3 RDHS with zero test events | PASS (0) |
| GLM convergence / no separation | PASS (all 4 converged; max|coef| ≤ 1.47; no separation) |
| DCA not dominated across the *entire* plausible band | PASS (models beat comparators on 39/46 thresholds) |

## 7. Models (formulas/features)
All output a predicted alert probability `P(y_{i,t+4}=1 | info ≤ t)`; continuous predictors standardized on train; logistic via lbfgs (L2 C=1e6 ≈ MLE).
- **M0 — Seasonal climatological baseline:** training event frequency by (RDHS × ISO-week-of-year), shrunk (pseudo-count K=3) toward the RDHS training mean; fallback RDHS → global. No test leakage.
- **M1 — Lagged dengue AR:** incidence at t, t−1, t−2, t−4 (date-based; train-mean-imputed where unavailable) + annual & semiannual harmonics + RDHS fixed effects (33 features).
- **M2 — Climate-only:** 6 contemporaneous climate variables (t2m mean/min/max, RH, precip sum, precip mean-daily) (6 features). The week-*t* climate values are available at prediction time and precede the t+4 target by 4 weeks; the explicit lag sweep is sensitivity **S2**.
- **M3 — Climate + seasonality + RDHS FE:** M2 climate + annual/semiannual harmonics + RDHS fixed effects (35 features) — the primary "existing climate-driven EWS" form.

## 8. Model-fit status
All four models **converged with no separation** (M1 max|coef| 1.47; M2 0.61; M3 1.06). No penalized fallback was needed.

## 9. Calibration (test) — primary axis
| Model | Brier | Calibration-in-the-large (CITL intercept) | Calibration slope | Mean predicted | Observed |
|---|---|---|---|---|---|
| M0 climatological | 0.222 | **+0.530** | 0.664 | 0.238 | 0.336 |
| M1 lagged-AR | 0.191 | **+0.513** | 1.246 | 0.246 | 0.336 |
| M2 climate-only | 0.220 | **+0.479** | 1.027 | 0.243 | 0.336 |
| M3 climate+season+RDHS | 0.220 | **+0.596** | 0.738 | 0.229 | 0.336 |

**Key finding:** every model **under-predicts** on the test period (positive CITL; mean predicted ~0.23–0.25 vs observed 0.336) — calibration-in-the-large has drifted because the models were trained on a 24% base-rate period and tested on a 34% base-rate period. Calibration *slope* varies: M2 ≈ 1.03 (well-spread), M1 ≈ 1.25, M0/M3 ≈ 0.66–0.74 (over-spread). M3 raw decile reliability is monotonic but sits below the diagonal throughout (e.g. predicted 0.48 → observed 0.58 in the top decile).

**Recalibration:** Platt (intercept+slope) fit on **training** predictions and applied to test **does not** correct the cross-period drift (recalibrated CITL still +0.51 to +0.65), because a train-fit recalibration cannot anticipate the test-period base-rate rise. This is the central calibration lesson: **in-period recalibration does not fix temporal calibration drift.**

## 10. Discrimination (test) — secondary
| Model | AUC | PR-AUC |
|---|---|---|
| M0 climatological | 0.629 | 0.459 |
| **M1 lagged-AR** | **0.752** | **0.652** |
| M2 climate-only | 0.643 | 0.460 |
| M3 climate+season+RDHS | 0.652 | 0.476 |

Recent surveillance counts (M1) carry most of the discriminative signal; **climate-only models (M2/M3) add little over the climatological baseline** (AUC 0.64–0.65 vs 0.63).

## 11. Decision-curve / net-benefit (test)
Threshold grid p\* = 0.05–0.50 (step 0.01); comparators alert-all / alert-none. Saved: `dca_h4_75pct_v1.csv`.
- **Decision value exists** in the mid-to-high threshold band: models beat both comparators on **39/46 thresholds**; alert-all dominates only at low p\* ≤ 0.16 (expected when threshold ≪ prevalence). No region where every model is dominated → no stop.
- **M1 is the strongest** (top net benefit on 38/46 thresholds; beats both comparators on 80% of the grid). Climate-only M2 is top only in the narrow low-threshold band (7 thresholds); M3 top once.

Net benefit at representative thresholds:
| p\* | alert-all | alert-none | M0 | M1 | M2 | M3 |
|---|---|---|---|---|---|---|
| 0.20 | 0.171 | 0 | 0.161 | **0.185** | 0.164 | 0.147 |
| 0.30 | 0.052 | 0 | 0.084 | **0.137** | 0.069 | 0.078 |
| 0.34 | −0.005 | 0 | 0.059 | **0.111** | 0.032 | 0.060 |
| 0.40 | −0.106 | 0 | 0.025 | **0.083** | 0.012 | 0.039 |

## 12. Interpretation (pilot-level, not a final claim)
This single hardened pass is coherent and points to a clear, honest pilot signal aligned with the project's calibration/decision-reporting thesis:
- **Discrimination alone is misleading:** climate models look "ok" on AUC yet, like all models here, **drift in calibration-in-the-large** across the 2018–2022 → 2023–2025 boundary, and **training recalibration does not repair it**.
- **The climate-driven EWS forms (M2/M3) do not beat a simple recent-cases AR baseline (M1)** on discrimination *or* net benefit — a result worth reporting plainly.
- Decision value is real but **threshold-dependent**, concentrated in the mid-high p\* band.
- Per prereg §O, this leans toward a **calibration-reporting / data-resource contribution** rather than a "climate EWS beats surveillance" headline — to be confirmed against the planned sensitivities (S1 naive-week linkage, S2 lag sweep, S3 drop-late-2021) and recalibration variants before any conclusion.

## 13. Output files (quarantined, read-only, NOT committed) + SHA256
- `predictions_h4_75pct_v1.csv` — `07f5916a9c53a4fa13e4f2fc55c78e4d9ccb680057bc1c18df2f9a780cd71c69`
- `metrics_h4_75pct_v1.csv` — `a5366123ac82415ff84cc70bc03c4fb46a95c27b1a8d3efa2eadda4a36d976de`
- `dca_h4_75pct_v1.csv` — `ffd5563a5d27689fc23a3a021395d9aa5f8e61532e9de02105ce535cb27390a2`
- `thresholds_h4_75pct_v1.csv` — `bbb1843d15d85efe68f10f69c7c6ce7f193ef7a84f51b15e03b745e0ee2c0cfc`
- Metadata: `pilot_h4_75pct_v1.meta.md` (all under `~/data_quarantine/model_pilots/pilot_h4_75pct_v1/`).

## 14. Confirmations
- Models were run **only as specified** (M0–M3, single hardened pass); no hyperparameter tuning on test; no post-hoc threshold optimization (full DCA curve reported).
- **No frozen outcome/exposure/population or linked-analysis CSV was modified or overwritten** (input checksum re-verified).
- **No data files are committed** — all pilot outputs are quarantined and git-ignored; only this markdown report is proposed for commit.
- **Reproducibility:** the fit/evaluation script was rerun end-to-end after removing a trailing non-computational token (a stray heredoc terminator that had caused a post-output `NameError` / exit-code-1 without affecting any computation); the clean rerun **exits 0** and reproduces **byte-identical** outputs (all four CSV checksums unchanged) — no substantive metric changes.
- Preregistration unchanged.

## 15. Next steps (separate, approval-gated)
1. **Sensitivities** S1 (naive v1 literal-week linkage), S2 (climate-lag sweep 0–8 wk), S3 (drop late-2021 window).
2. Calibration-drift handling: evaluate a **time-updated / rolling recalibration** (vs the train-only recalibration shown here) as a fair within-frame fix.
3. 90th-pct label sensitivity and h = 1/2/8/12 horizons. Nothing runs until directed.
