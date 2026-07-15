# Phase 1 — Sri Lanka development-inclusive uncertainty (RESULT)

**Reproduce-first gate PASSED:** reconstructed M5 reproduces frozen predictions to max|Δ| = 1.1e-16; conditional matched recal reproduced at +0.01565 (+0.0157) and raw at +0.0087 before the loop. Script: `sl_devinclusive.py` (results `SL_devinclusive_results.json`).

## Procedure
Cluster-bootstrap of the 26 RDHS units (seed 20260612, **B = 300**, 0 failures). Within each replicate: refit **M5** and **M5_no-climate** on the resampled training rows with the same rolling-origin L2 penalty selection; apply the identical past-only rolling-52-week intercept recalibration (per-week, eligibility target_week < prediction week) to both; evaluate on the replicate's test rows; compute raw M5−M5_no-climate and recal(M5)−recal(M5_no-climate). Percentile intervals across replicates = development-inclusive CIs. The cr() spline bases are held fixed (fit once on the original training data); the refitting captures coefficient, penalty-selection, and recalibration variability plus test resampling — the same development-uncertainty sources as Colombia's development-inclusive bootstrap. B = 300 for tractability (per-replicate refit + recalibration); the 2.5/97.5 percentiles are the reported bounds and are themselves finite-cluster-limited on 26 clusters.

## Result

| Contrast | Point | Conditional 95% CI | Development-inclusive 95% CI (B=300) | Zero? |
|---|---|---|---|---|
| Raw  M5 − M5_no-climate | +0.0087 | [−0.0015, +0.0188] | **[−0.0074, +0.0223]** (median +0.0078) | includes (both) |
| Recalibrated  recal(M5) − recal(M5_no-climate) | +0.0157 | [+0.0066, +0.0257] | **[+0.0015, +0.0284]** (median +0.0143) | **excludes (both)**, marginal |

## Branch taken: **EXCLUDES zero (stronger than expected)**
The recalibrated Sri Lanka matched increment excludes zero under **both** conditional and development-inclusive resampling — the exclusion **survives model-development uncertainty**, though marginally (development-inclusive lower bound +0.0015 on 26 clusters, B=300). The **raw** increment includes zero under both treatments. Recalibration shifts the whole distribution up (dev-inclusive median +0.0078 raw → +0.0143 recalibrated) and moves the lower bound from −0.0074 to +0.0015.

## Honest characterization (drives the framing)
- Sri Lanka's matched climate increment is distinguishable from zero **only after recalibration**; the raw increment is not (either interval treatment).
- That recalibrated exclusion is **marginal** but survives model-development uncertainty.
- **Colombia's** conditional exclusion does **not** survive model-development uncertainty (development-inclusive [−0.0001, +0.0244] includes zero).
- The two settings are therefore a **different tier, but not symmetric**: Sri Lanka's recalibrated exclusion is the more robust to refitting; Colombia's is not; neither raw increment excludes zero. This corrects the prior manuscript statement that "under development-inclusive uncertainty, neither setting shows a robust exclusion."

## Phase 1c — paired raw→recalibrated
Recalibration raised the matched increment from +0.0087 (raw, interval includes zero) to +0.0157 (recalibrated, interval excludes zero); the development-inclusive median rose from +0.0078 to +0.0143. We describe this as a calibration-state difference in interval exclusion, not as a demonstration that recalibration significantly changed the increment (the point shift +0.0070 is within uncertainty).
