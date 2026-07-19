# Stage 1 — Original Colombia Pipeline Inventory

Read-only. No model was fit or scored. All artifacts identified from dated repository evidence + on-disk frozen outputs; hashes in `stage1_source_hashes.sha256`.

## The exact frozen pipeline
**Generator script:** `scripts/colombia_model_ladder_h4_75pct_v1.py` (186 lines, committed 2026-06-18, sha256 `0d88ea02…`). Docstring: "Colombia M0-M5 model-ladder evaluation … Regularized L2 logistic; train-only preprocessing; C tuned on validation log loss; Platt recalibration on validation; test evaluated once; GID_2 cluster bootstrap (seed 20260612, B=1000)."
**Spec of record:** `docs/colombia_model_ladder_spec.md` (commit 37221a6), referenced in the script's meta output (script:171).

## Inputs
| Artifact | Path | Role | sha256 |
|---|---|---|---|
| Modeling table | `data_quarantine/colombia_label_features_v1/colombia_modeling_table_h4_75pct_v1.csv` | features + label_h4 + split + flags (127,703 rows) | `bfb2a536…` |

## Frozen outputs (the numbers to reproduce/decompose)
| Artifact | Path | sha256 |
|---|---|---|
| Predictions (test, M0–M5 raw+recal) | `…/model_ladder_h4_75pct_v1/colombia_model_predictions_h4_75pct_v1.csv` | `a938a138…` |
| Contrasts (dAUC, dNB@.30) | `…/colombia_model_contrasts_h4_75pct_v1.csv` | `2b69c977…` |
| Coefficients (per model) | `…/colombia_model_coefficients_h4_75pct_v1.csv` | `53b500df…` |
| Bootstrap CI | `…/colombia_model_bootstrap_ci_h4_75pct_v1.csv` | `319b3545…` |
| Metrics (AUC/PR/Brier/CITL/slope/NB) | `…/colombia_model_metrics_h4_75pct_v1.csv` | `c2dd62f0…` |
| Run metadata | `…/colombia_model_ladder_h4_75pct_v1.meta.json` | `86e7c097…` |

## Frozen result confirmed on disk (transcribed, not recomputed)
- `M5_vs_M1`: dAUC = **+0.04029**, dNB@0.30 = **+0.018775**; bootstrap dNB 95% CI **[+0.0117, +0.0260]** (median +0.0183).
- `M4_vs_M1`: dNB@0.30 = **+0.012242**, dAUC +0.01355.
- `M2_vs_M1`: dNB = −0.00942; `M3_vs_M1`: dNB = −0.00942.
- Test prevalence 0.3753; row counts train 53,711 / val 12,713 / test 13,361; 32 departments.

## Environment
Python 3.10.12; scikit-learn (LogisticRegression, lbfgs); statsmodels 0.14.6 (Logit, CITL/slope). R 4.6.0 present but not used by this script. No committed requirements/lockfile (known reproducibility gap).

## Provenance note (bearing on Path B necessity)
The frozen **M4−M1 = +0.0122** (climate added to cases, *no* fixed effects) is **materially non-zero**, which **contradicts** the earlier plain-logistic re-analysis approximation (which gave ≈ 0 for a no-FE climate hybrid). This confirms the approximation is **not** a faithful substitute for this pipeline and that the matched contrast must be computed in the original pipeline before any conclusion.
