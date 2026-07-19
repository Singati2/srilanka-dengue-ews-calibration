# route_a_results.md — Route A (frozen-prediction proper scoring) results

Post-lock. Lock commit `28c0341e`, tag `alt-stats-plan-v1`. Frozen checksums verified before
run. Development-inclusive intervals NOT computed (Phase 1 gate); all intervals below are
**conditional** paired cluster-bootstrap (B=5000, seed 20260612, 0 failures/5000 in every
cell). Orientation: negative ΔNLL / ΔBrier favors the full climate model.

## Primary — ΔNLL (nats) and information gain
| Setting | State | mean NLL full | mean NLL no-clim | ΔNLL | cond. 95% CI | IG (bits) | frac favoring climate |
|---|---|---|---|---|---|---|---|
| Sri Lanka | recalibrated (primary) | 0.54058 | 0.56128 | **−0.02070** | [−0.03525, −0.00679] | +0.0299 | 0.999 |
| Sri Lanka | raw (secondary) | 0.54057 | 0.56615 | −0.02558 | [−0.03912, −0.01283] | +0.0369 | 1.000 |
| Colombia | recalibrated (primary) | 0.61616 | 0.62511 | **−0.00894** | [−0.01683, −0.00100] | +0.0129 | 0.984 |
| Colombia | raw (secondary) | 0.59713 | 0.60567 | −0.00854 | [−0.01383, −0.00294] | +0.0123 | 0.999 |

## Key secondary — ΔBrier (BSS descriptive)
| Setting | State | Brier full | Brier no-clim | ΔBS | cond. 95% CI | BSS |
|---|---|---|---|---|---|---|
| Sri Lanka | recal | 0.17866 | 0.18653 | −0.00788 | [−0.01297, −0.00311] | +0.042 |
| Sri Lanka | raw | 0.18009 | 0.19075 | −0.01067 | [−0.01561, −0.00608] | +0.056 |
| Colombia | recal | 0.21267 | 0.21694 | −0.00427 | [−0.00776, −0.00081] | +0.020 |
| Colombia | raw | 0.20533 | 0.20897 | −0.00364 | [−0.00591, −0.00126] | +0.017 |

## Discrimination (secondary)
| Setting | State | ΔAUC | cond. CI | ΔPR-AUC | cond. CI |
|---|---|---|---|---|---|
| Sri Lanka | recal | +0.0274 | [+0.013, +0.045] | +0.0162 | [−0.002, +0.036] |
| Sri Lanka | raw | +0.0202 | [+0.003, +0.040] | +0.0159 | [−0.007, +0.042] |
| Colombia | recal | +0.0121 | [+0.002, +0.023] | +0.0111 | [−0.002, +0.026] |
| Colombia | raw | +0.0121 | [+0.002, +0.023] | +0.0111 | [−0.002, +0.026] |

## Calibration (descriptive/diagnostic)
| Setting | State | model | CITL | slope | ICI | mean p | prev |
|---|---|---|---|---|---|---|---|
| Sri Lanka | recal | full | +0.033 | 0.872 | 0.0270 | 0.331 | 0.336 |
| Sri Lanka | recal | no-clim | +0.020 | 0.941 | 0.0453 | 0.333 | 0.336 |
| Colombia | recal | full | −0.505 | 1.160 | 0.1094 | 0.485 | 0.375 |
| Colombia | recal | no-clim | −0.510 | 1.204 | 0.1128 | 0.488 | 0.375 |
(full table in `results/calibration_metrics.csv`; Colombia recal shows residual over-prediction in both models — a known V6 finding — with the full model marginally better ICI.)

## Numerical stability
- Clipping sensitivity (ε=1e-15 primary vs ε=1e-12): **not material** in any cell
  (|Δ(ΔNLL)| below max(1e-4, 5% of |ΔNLL|)).
- B=1000 parity CIs nearly identical to B=5000 (e.g. SL recal ΔNLL parity [−0.0351,−0.0060]
  vs primary [−0.0352,−0.0068]).
- Bootstrap failures: **0/5000** every cell (< 2% threshold); single-outcome-class replicates: 0.

## Reading (locked interpretation rules)
Under the matched specification, the full climate model has **better overall probability
accuracy** than the pipeline-matched no-climate model in both settings and both prediction
states: ΔNLL and ΔBrier are negative with conditional intervals excluding zero, and the
fraction of replicates favoring climate is 0.98–1.00 (a descriptive bootstrap sign
frequency, **not** a probability of benefit). Discrimination also favors climate (ΔAUC
intervals exclude zero; ΔPR-AUC borderline). These are **conditional** intervals; because
the development-inclusive refit bootstrap was not re-executed, robustness to model
redevelopment is **not** assessed here. No minimum worthwhile ΔNLL/ΔBS was elicited, so the
analysis **quantifies predictive-score differences but does not establish an operationally
worthwhile increment**. The underlying matched full-versus-no-climate ablation remained
**post hoc** relative to Version 6; the scoring rules were locked before their computation
but after the Version 6 findings were known.
