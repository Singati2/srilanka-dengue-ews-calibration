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
