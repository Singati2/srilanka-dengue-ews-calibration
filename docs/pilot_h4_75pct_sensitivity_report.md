# Pilot Sensitivity Report — S1–S3 for the h=4 / RDHS-75th-pct calibration-DCA pilot
*Preregistered sensitivity analyses (per `preregistration_analysis_plan_v1.md` addendum and `docs/pilot_existing_model_calibration_dca_spec.md`). All computed artifacts are **quarantined and git-ignored**; only this markdown report is proposed for commit. No frozen outcome/exposure/population or linked-analysis CSV was modified. No models beyond the preregistered S1–S3 (no new label thresholds, horizons, rolling recalibration, or feature search).*

**Date:** 2026-06-12

## Recap of the primary pilot (v2, h=4, RDHS-75th-pct)
On the date-aligned v2 table (test 2023–2025): all models **under-predict** (positive calibration-in-the-large); **M1 lagged-AR dominates** (AUC 0.752, Brier 0.191, best net benefit); climate-only/climate+season models (M2/M3) do **not** beat the recent-cases baseline. S1–S3 test whether these conclusions are artifacts of the linkage rule, the contemporaneous-climate choice, or the late-2021 anomaly handling.

## Method (common to all sensitivities)
Identical pipeline to the primary pilot: h=4 calendar target (+28 d, gap-safe); RDHS-specific 75th-pct labels from **training 2018–2022 only**; split train 2018–2022 / test 2023–2025; models M0–M3 (logistic, lbfgs, standardized on train); DCA p\*=0.05–0.50. Input checksums re-verified (v2 `3a197d61…`, v1 `d892f62f…`).

## Stop-rule results (all PASS — every sensitivity was fit)
| Sensitivity | n train | n test | test events | test prev | RDHS 0-events (tr/te) | all checks |
|---|---|---|---|---|---|---|
| S1 v1 literal-week | 6,590 | 3,952 | 1,314 | 33.3% | 0 / 0 | PASS |
| S3 drop late-2021 | 6,230 | 3,926 | 1,239 | 31.6% | 0 / 0 | PASS |
| S2 (v2, per lag) | 6,590 | 3,926 | 1,321 | 33.6% | 0 / 0 | PASS |
All GLMs converged with no separation (max|coef| ≤ 1.47). DCA not dominated across the whole band (S1: models beat comparators on 36/46 thresholds; S3: 42/46).

## S1 — Naive v1 literal-week linkage
| Model | AUC (v1) | AUC (v2 primary) | Brier | CITL | Slope |
|---|---|---|---|---|---|
| M0 | 0.634 | 0.629 | 0.219 | +0.517 | 0.682 |
| M1 | 0.753 | 0.752 | 0.189 | +0.507 | 1.233 |
| M2 | **0.622** | **0.643** | 0.222 | +0.475 | 0.851 |
| M3 | **0.646** | **0.652** | 0.220 | +0.565 | 0.669 |

**Finding:** naive literal-week linkage **slightly degrades the climate models** (M2 AUC 0.622 vs 0.643; M3 0.646 vs 0.652), in the expected direction — the 1–2-week misalignment blunts climate signal — while M1 (depends on past cases, not climate alignment) is unchanged (0.753). Calibration drift persists (all CITL positive). **Conclusions unchanged:** M1 still dominates; date-alignment helps climate marginally but does not rescue it. Net benefit @ p\*=0.30: M1 0.136 ≫ M0 0.085 > M3 0.077 > M2 0.052.

## S2 — Climate lag sweep (L = 0…8 weeks; climate at t−L)
Full curve (no post-hoc headline selection):

| Lag | M2 AUC | M2 Brier | M2 CITL | M2 NB@.30 | M3 AUC | M3 Brier | M3 CITL | M3 NB@.30 |
|---|---|---|---|---|---|---|---|---|
| 0 | 0.643 | 0.220 | +0.479 | 0.069 | 0.652 | 0.220 | +0.596 | 0.078 |
| 1 | 0.648 | 0.218 | +0.458 | 0.075 | 0.651 | 0.218 | +0.537 | 0.082 |
| 2 | 0.657 | 0.216 | +0.445 | **0.088** | **0.658** | 0.217 | +0.559 | 0.085 |
| 3 | 0.652 | 0.216 | +0.432 | 0.085 | 0.650 | 0.217 | +0.521 | 0.085 |
| 4 | **0.660** | **0.214** | +0.425 | 0.087 | 0.654 | **0.216** | +0.526 | **0.088** |
| 5 | 0.653 | 0.216 | +0.425 | 0.084 | 0.650 | 0.216 | +0.521 | 0.086 |
| 6 | 0.626 | 0.220 | +0.437 | 0.069 | 0.645 | 0.217 | +0.528 | 0.081 |
| 7 | 0.610 | 0.222 | +0.431 | 0.062 | 0.642 | 0.218 | +0.525 | 0.078 |
| 8 | 0.610 | 0.223 | +0.423 | 0.060 | 0.646 | 0.218 | +0.519 | 0.074 |

**Finding:** climate models **do improve modestly with a 2–4 week lag** (M2 best AUC 0.660 at L4 and best NB@.30 0.088 at L2; M3 best AUC 0.658 at L2, best NB@.30 0.088 at L4) — confirming the spec's hypothesis that contemporaneous-only (L0) climate mildly understated climate value. Beyond ~L5 performance decays. **But even at their best lag, climate models stay far below M1** (max climate AUC 0.660 ≪ M1 0.752; max climate NB@.30 0.088 ≪ M1 0.137). Calibration-in-the-large remains positive at every lag (no lag fixes the drift). Reported as the full curve; no single lag is promoted to a headline.

## S3 — Drop late-2021 anomaly window (2021 wk 39–52 excluded before modeling)
| Model | AUC | Brier | CITL | Slope | NB@.30 |
|---|---|---|---|---|---|
| M0 | 0.623 | 0.213 | +0.441 | 0.633 | 0.069 |
| M1 | 0.753 | 0.182 | +0.425 | 1.250 | 0.120 |
| M2 | 0.632 | 0.212 | +0.391 | 0.884 | 0.053 |
| M3 | 0.646 | 0.210 | +0.466 | 0.672 | 0.066 |

**Finding:** dropping the late-2021 window barely moves anything — M1 AUC unchanged (0.753), climate AUC similar (0.63–0.65), the ordering preserved, calibration drift slightly smaller but still present (CITL +0.39 to +0.47). **The primary conclusion does not depend on the late-2021 calendar-anomaly handling.**

## Cross-cutting answers
- **Does any climate model beat M1?** On **discrimination: no** — max climate AUC anywhere is 0.660, vs M1 ≈ 0.752–0.753 in every sensitivity. On **net benefit**: only in the narrow low-threshold band (p\*≤~0.16, where alert-all is itself competitive) — across 414 S2 lag×threshold cells M2 exceeds M1 at just 54 (all low-p\*) and M3 at 4; in S1/S3, M2>M1 at ≤7/46 and M3>M1 at ≤2/46. In the **operational mid-high threshold range, M1 dominates throughout**. On **calibration**, no climate model is materially better-calibrated than M1.
- **Does calibration drift remain?** **Yes — in every sensitivity, every model, every lag** (positive calibration-in-the-large; under-prediction on the higher-incidence 2023–2025 test period). Neither date-alignment, climate lagging, nor dropping late-2021 removes it.
- **Primary conclusion survives:** robust across linkage rule, climate lag, and anomaly handling.

## Interpretation (still pilot-level)
S1–S3 reinforce the primary signal and the lean (prereg §O) toward a **calibration-reporting / data-resource contribution** rather than "climate EWS beats surveillance": existing climate-driven forms do not outperform a simple recent-cases baseline, and a temporal calibration drift persists that AUC alone hides and that training recalibration did not fix. The S2 lag result (climate best at ~2–4 weeks) is a fair, pre-specified robustness check — not evidence that climate wins.

## Output files (quarantined, read-only, NOT committed) + SHA256
- `sensitivity_metrics_h4_75pct_v1.csv` — `d14da0101b3251a161482d2693aef99efbd6c0ff946df3b2fd2379517e7c1426`
- `sensitivity_dca_h4_75pct_v1.csv` — `78a2e6f4d91e99151df285a1d9935f3a96fc810fddb096dc22ca57d521720e73`
- `sensitivity_stop_rules_h4_75pct_v1.csv` — `78c5becf1c36be74415265bdf9107d7165e9a32a4076cad9f81091deecb13091`
- `sensitivity_lag_sweep_h4_75pct_v1.csv` — `b5858ea916ed587dd7153989f8458abcf2c8e8bf34e6862c6cd299ca3505c268`
- Metadata: `sensitivity_outputs.meta.md` (all under `~/data_quarantine/model_pilots/pilot_h4_75pct_sensitivities_v1/`).

## Confirmations
- Only the preregistered S1–S3 were run; no new labels/horizons/rolling recalibration/feature search; no post-hoc lag selection for the headline (full curve reported).
- **No frozen outcome/exposure/population or linked-analysis CSV (v1/v2) was modified or overwritten**; input checksums re-verified. The primary pilot directory was not overwritten.
- **No data files are committed** — all sensitivity outputs are quarantined/git-ignored; only this markdown report is proposed for commit.
- Preregistration unchanged.

## Next steps (separate, approval-gated)
Time-updated / rolling recalibration (fair within-frame fix for the calibration drift); 90th-pct label and h = 1/2/8/12 horizon variants. Nothing runs until directed.
