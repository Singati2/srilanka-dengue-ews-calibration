# S9 Table — Colombia exceedance-threshold and horizon sensitivity (transcribed; no recomputation)
Sources: `docs/colombia_outbreak_threshold_sensitivity_report.md`, `docs/colombia_horizon_sensitivity_report.md` (frozen). External framework replication.

## (a) Stricter exceedance-threshold (train-only percentile), h=4, p*=0.30
| Label | test prevalence | ΔNB(M5−M1) | 95% CI |
|---|---|---|---|
| 75th (primary) | 0.375 | +0.0188 | [+0.0117, +0.0260] |
| 80th | 0.331 | +0.0157 | [+0.0082, +0.0236] |
| 90th | ~0.235 | +0.0092 | [+0.0003, +0.0183] |

## (b) Horizon sensitivity (M5−M1)
| h | test prevalence | ΔNB(M5−M1) | ΔAUC |
|---|---|---|---|
| 1 | 0.404 | ~+0.015 to +0.019 | ~+0.040 (h≤4) |
| 2 | 0.394 | ~+0.015 to +0.019 | ~+0.040 |
| 4 (primary) | 0.375 | +0.0188 | +0.040 |
| 8 | 0.332 | ~+0.015 to +0.019 | declining |
| 12 | 0.303 | ~+0.014 | ~+0.024 |

The increment is approximately flat across horizons (does not grow with lead time). Intervals pointwise, multiplicity-unadjusted. Values transcribed verbatim from the frozen reports.

## (c) Colombia 2022-only sensitivity (secondary; pandemic-period subset), h=4, 75th-percentile label, p*=0.30
Secondary evaluation restricted to calendar year 2022 (excluding 2020–2021), using the frozen recalibrated (post-Platt) predictions `colombia_model_predictions_h4_75pct_v1.csv` (sha256 `a938a138…`). No model refit, no recomputation; values transcribed from the audited v2 outputs (`colombia_2022_only_v2` report; underlying `colombia_2022_only_results.csv` / `colombia_2022_only_contrasts.csv`, v1 run retained unchanged). Not interpreted as pandemic-free or post-pandemic validation.

**Design and protocol.** Resampling unit: municipality (GID_2). B = 1000. Seed = 20260630. Interval method: percentile (2.5/97.5). Bootstrap failures: 0. Pointwise and multiplicity-unadjusted. Reference threshold p*=0.30 (planned reference threshold). Eligible **prediction-origin** weeks: **48, not 52** — the 2022 origins run from 2022-01-02 to 2022-11-27 (weekly cadence verified). Under the four-week-ahead horizon, the four December-2022 origin weeks would require four-week-ahead targets in January 2023 (2022-12-04→2023-01-01; 2022-12-11→2023-01-08; 2022-12-18→2023-01-15; 2022-12-25→2023-01-22), beyond the available target period; the latest target used corresponds to the 2022-11-27 origin (target 2022-12-25). This distinguishes the prediction-origin date (max 2022-11-27), the target date (max used 2022-12-25), and the underlying OpenDengue outcome-series end (not independently documented here and not claimed). So 48 = 52 − 4. Full date evidence: `colombia_2022_week_eligibility_v17.md`; verified against the frozen prediction file `colombia_model_predictions_h4_75pct_v1.csv` (sha256 `a938a138…`, maximum week_start 2022-11-27).

**Subset size.** 4,802 municipality-weeks; 274 municipalities; 48 eligible prediction weeks; 2,202 elevated-activity events; prevalence 0.4586. Alert-all net benefit at p*=0.30 = 0.2265; alert-none net benefit = 0 (by definition).

**Per-model performance (2022 subset).**
| Model | AUC | PR-AUC | Brier | CITL | Calib. slope | NB@0.30 |
|---|---|---|---|---|---|---|
| M0 | 0.504 | 0.465 | 0.250 | −0.159 | 0.468 | 0.227 |
| M1 | 0.674 | 0.624 | 0.227 | −0.122 | 1.041 | 0.230 |
| M2 | 0.635 | 0.564 | 0.243 | −0.197 | 2.774 | 0.227 |
| M3 | 0.585 | 0.535 | 0.245 | −0.197 | 1.686 | 0.227 |
| M4 | 0.709 | 0.663 | 0.218 | −0.176 | 1.124 | 0.239 |
| M5 | 0.728 | 0.682 | 0.213 | −0.195 | 1.215 | 0.245 |

**Contrasts (municipality-cluster bootstrap, percentile).**
| Contrast | point | 95% percentile interval |
|---|---|---|
| ΔAUC(M5−M1) | +0.0546 | +0.0336 to +0.0768 |
| ΔNB(M5−M1) @0.30 | +0.0150 | +0.0067 to +0.0249 |
| ΔNB(M4−M1) @0.30 | +0.0097 | +0.0048 to +0.0150 |

For comparison, the full 2020–2022 test period gave ΔNB(M5−M1) +0.0188 (95% CI +0.0117 to +0.0260) and ΔAUC +0.040. The 2022-only M5−M1 estimate (+0.0150) is modestly smaller; the higher 2022 prevalence (0.4586) made alert-all (0.2265) far more competitive, so absolute net-benefit levels are higher and not directly comparable to the full period.

**Limitation.** Municipality-cluster resampling preserved within-municipality dependence but did not separately model common calendar-week shocks across municipalities. A two-way (municipality × calendar-week) cluster analysis was not conducted.
