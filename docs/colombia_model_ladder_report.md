# Colombia M0–M5 Model-Ladder Report (COMPLETED — first model run)
*Fitted and evaluated per `docs/colombia_model_ladder_spec.md`. Regularized L2 logistic regression; train-only preprocessing; C tuned on validation log loss; Platt recalibration on validation; test evaluated once; GID_2 cluster bootstrap (seed 20260612, B=1000). **Colombia data only; no Sri Lanka coefficient transfer; labels/thresholds not recomputed. No external validation.** Generated outputs quarantined; only this report + the script are committed.*

**Date:** 2026-06-18 · **Status:** completed · **Base commit:** 37221a6 · **Spec:** `docs/colombia_model_ladder_spec.md` · **Script:** `scripts/colombia_model_ladder_h4_75pct_v1.py`.

## 1. Input + SHA256 (16-char)
- `…/colombia_label_features_v1/colombia_modeling_table_h4_75pct_v1.csv` — `bfb2a5369f53d4e6…`.

## 2. Outputs (quarantine, read-only; NOT committed) + SHA256 (16-char) / size
- `colombia_model_predictions_h4_75pct_v1.csv` — `a938a138d9ef65e3…` — 3,447,202 B
- `colombia_model_metrics_h4_75pct_v1.csv` — `c2dd62f0c2633b2d…` — 2,419 B
- `colombia_model_dca_h4_75pct_v1.csv` — `7328c763a63f2a4a…` — 4,145 B
- `colombia_model_calibration_h4_75pct_v1.csv` — `6e89bb38f2920f3f…` — 881 B
- `colombia_model_coefficients_h4_75pct_v1.csv` — `53b500df455733c5…` — 9,550 B
- `colombia_model_bootstrap_ci_h4_75pct_v1.csv` — `319b354599a9a3e5…` — 1,535 B
- `colombia_model_contrasts_h4_75pct_v1.csv` — `2b69c97726e3c207…` — 228 B
- `colombia_model_ladder_h4_75pct_v1.meta.json` — `86e7c097c93b9df0…` — 1,751 B
- Dir `~/data_quarantine/colombia_model_pilots/model_ladder_h4_75pct_v1/`, chmod 444.

## 3. Primary row counts (common-complete M1–M5 h=4) — matches spec
- Train 53,711 · Validation 12,713 · Test 13,361 (total 79,785; 703 GID_2 units, 475 in test). **Test prevalence 0.375.**

## 4. Secondary row counts (climate-only full, M2/M3)
- Train 86,701 · Validation 19,356 · Test 21,646 (total 127,703).

## 5. Model definitions
M0 intercept+season · M1 log1p(cases_lag0/1/2/4) · M2 log1p(precip_lag0–8)+temp_lag0–8 · M3 M2+season+department FE · M4 M1+M2 · M5 M4+season+department FE.

## 6. Preprocessing & tuning
- log1p on case & precip lags; continuous predictors standardized on **train mean/SD only**; department one-hot (no target encoding); no test data in preprocessing/tuning; no imputation (common-complete).
- C tuned by **validation log loss** (grid 0.001–10), per model; Platt recalibration fit on **validation**; test scored once.

## 7. Validation-selected C
M0 0.001 · M1 0.01 · M2 0.001 · M3 0.001 · M4 0.01 · M5 0.01. (Validation log loss: M0 0.771 · M1 0.721 · M2 0.757 · M3 0.760 · M4 0.701 · **M5 0.699**.)

## 8. Test metrics (recalibrated; common-complete, n=13,361)
| Model | AUC | PR-AUC | Brier | CITL | slope | NB@0.30 |
|---|---|---|---|---|---|---|
| M0 (climatology) | 0.513 | 0.384 | 0.250 | −0.50 | 3.43 | 0.108 |
| **M1 (recent cases)** | **0.685** | 0.566 | 0.222 | −0.46 | 1.09 | **0.117** |
| M2 (climate-only) | 0.556 | 0.412 | 0.248 | −0.50 | 0.85 | 0.108 |
| M3 (climate+season+dept) | 0.564 | 0.417 | 0.249 | −0.54 | 1.28 | 0.108 |
| M4 (hybrid) | 0.699 | 0.584 | 0.217 | −0.45 | 1.05 | 0.129 |
| **M5 (hybrid+season+dept)** | **0.726** | 0.608 | 0.213 | −0.50 | 1.16 | **0.136** |

- **Decision-curve reference:** at p\*=0.30 with prevalence 0.375, **treat-all NB ≈ 0.107**. M0/M2/M3 collapse to ≈ treat-all (no operational value over default-intervene); M1/M4/M5 exceed it.

## 9. Raw vs recalibrated
Recalibration (Platt on validation) was applied; metrics above are recalibrated. AUC/PR-AUC are unchanged by monotone recalibration; recalibration improved Brier/calibration modestly. **Calibration caveat:** CITL ≈ −0.45 to −0.54 across all models → **systematic over-prediction on the test period** not fully removed by validation-fit recalibration — consistent with a train/val→test temporal shift (the COVID-era test caveat). Calibration slopes are near 1 for M1/M4/M5 (good); M0 (3.43) and M2 (0.85) are poorly calibrated baselines.

## 10. Net benefit @ p\*=0.30
M1 0.117 · M4 0.129 · **M5 0.136** vs treat-all ≈ 0.107 and climate-only/M0 ≈ 0.108. Full decision curve (p=0.05–0.50) in `…_dca_…csv`.

## 11. ΔAUC and ΔNB vs M1 (test) + bootstrap 95% CI (GID_2 cluster, B=1000, 0 failures)
| Contrast | ΔAUC [95% CI] | ΔNB@0.30 [95% CI] | Verdict |
|---|---|---|---|
| M2 vs M1 | −0.128 [−0.172, −0.084] | −0.009 [−0.0125, −0.0059] | **climate-only WORSE** (CI excl 0) |
| M3 vs M1 | −0.121 [−0.170, −0.073] | −0.009 [−0.0125, −0.0059] | **climate-only WORSE** |
| M4 vs M1 | +0.013 [+0.003, +0.025] | +0.012 [+0.007, +0.017] | **hybrid BETTER** (CI excl 0) |
| **M5 vs M1** | **+0.040 [+0.024, +0.058]** | **+0.018 [+0.012, +0.026]** | **hybrid BETTER** (CI excl 0) |

## 12. Bootstrap CI summary (per-model, B=1000, failure rate 0.0%)
- AUC: M1 0.685 [0.649, 0.720]; M4 0.698 [0.660, 0.733]; M5 0.725 [0.688, 0.758]; M2 0.556 [0.530, 0.582].
- NB@0.30: M1 0.117 [0.070, 0.168]; M4 0.129 [0.083, 0.178]; M5 0.135 [0.090, 0.184].
- 0/1000 replicates dropped (no single-class test resamples).

## 13. Secondary (climate-only full set, 127,703) — clearly labeled secondary
- M2: AUC 0.532, NB@0.30 ≈ 0.001; M3: AUC 0.546, NB@0.30 ≈ 0.001 (recalibrated). Climate-only is **weak and operationally ≈ treat-none** on the full set too. **Not compared head-to-head with M1/M4/M5** (different rows); confirms the primary climate-only finding is not an artifact of the common-complete subset.

## 14. Interpretation (per committed spec §14)
- **Recent surveillance dominates climate-only:** M1 ≫ M2/M3 (ΔAUC ≈ −0.12 to −0.13, ΔNB ≈ −0.009; CIs exclude 0). Climate-only ≈ treat-all/no operational value. **Replicates the Sri Lanka finding.**
- **Climate adds confirmed incremental value in the hybrid:** M4 and **M5 beat M1 on both ΔAUC and ΔNB with bootstrap CIs excluding 0** (M5 ΔNB +0.018 [0.012, 0.026]). M5 improves **both discrimination and net benefit** → the gain is operational, not discrimination-only.
- **Relation to Sri Lanka:** SL Stage-1A found *no* confirmed targeted climate value at p\*=0.30 in a powered regime (near-miss); **Colombia, with a larger sample, shows a confirmed hybrid net-benefit gain at p\*=0.30.** This is a genuine cross-setting *difference*, reported as a replication result — not a claim that climate "wins" generally (climate-only remains weak; the value is strictly *incremental, in the hybrid*).
- **Caveats:** test-period over-prediction (CITL ≈ −0.5; COVID-era/temporal drift) means absolute NB should be read with the recalibration caveat; ΔNB (within-test, same recalibration) is the more robust contrast. **No deployment-readiness claim; external framework replication, not global validation.**

## 15. Stop-rule assessment (final)
| Stop rule | Status |
|---|---|
| Input table present | PASS |
| Common-complete count == 79,785 | PASS (53,711/12,713/13,361) |
| Split matches spec | PASS |
| Labels/thresholds recomputed | PASS (no; SHAs unchanged) |
| Test info in preprocessing/tuning | PASS (none) |
| Model convergence | PASS (all converged) |
| Calibration/DCA consistent w/ SL | PASS (Platt + NB@p\*, continuous DCA) |
| Metrics on mismatched row sets | PASS (secondary explicitly labeled) |
| Bootstrap failure rate | PASS (0.0%) |
| Output overwrite without versioning | PASS (new v1 dir) |

## 16. Confirmations — labels/thresholds/Sri Lanka data unchanged
- Labels SHA `bd37e68a…`, thresholds SHA `23710e8c…`, input table SHA `bfb2a536…` — all **unchanged**. No Sri Lanka data or coefficients used; no label/threshold recompute.

## 17. Confirmation — no data files committed
- All 8 model outputs remain read-only in quarantine; **only this report + `scripts/colombia_model_ladder_h4_75pct_v1.py` are proposed for commit** (pending approval). No external validation run.

## 18. Next gate (separate)
Robustness extensions if desired (secondary horizons h1/2/8/12; 90th-pct label sensitivity; absent-as-zero panel-completion sensitivity; GID_2-FE alternative) and the cross-arm write-up positioning Colombia alongside Sri Lanka — all gated and not started.
