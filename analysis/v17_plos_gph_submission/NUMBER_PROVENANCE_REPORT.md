# NUMBER_PROVENANCE_REPORT (Phase 1)

Every submission-facing value re-verified against authoritative files this session; the recalibrated matched contrast was re-reproduced (deterministic; frozen predictions ≤1.1e-16). See NUMBER_PROVENANCE_TABLE.csv for the machine-readable mapping.

| Value | Point | 95% CI | Estimand | Raw/Recal | Source |
|---|---|---|---|---|---|
| SL matched (raw) | +0.0087 | −0.0015,+0.0188 (incl 0) | M5−M5_no-climate | raw | recal_matched_results.json / sl_matched_recal_results.json |
| SL matched (recalibrated) | +0.0157 | +0.0066,+0.0257 (excl 0, marginal) | recal(M5)−recal(M5_no-climate) | past-only recal | recal_matched_results.json |
| SL unmatched (raw) | +0.0081 | −0.0025,+0.0180 | M5−M1 | raw | recal_matched_results.json |
| SL unmatched (recal) | +0.0154 | +0.0064,+0.0255 | recal(M5)−recal(M1) | past-only recal | recal_matched_results.json |
| SL M4−M1 | −0.008 → +0.010 | −0.011,+0.030 (incl 0) | M4−M1 | raw→recal | sl_matched_recal_results.json |
| SL non-climate structure | +0.0462 | +0.0199,+0.0741 | matched−cases | raw | sl_matched_recal_results.json |
| CO matched | +0.0078 | +0.0039,+0.0119 (conditional) | M5−M5_no-climate | validation-recal | manuscript Table (original submission) |
| CO matched (dev-inclusive) | — | −0.0001,+0.0244 (incl 0) | M5−M5_no-climate | refit bootstrap | manuscript |

**No unverified number remains in a submission-facing file.** All abstract/results/discussion values match this table (consistency confirmed in v16 CONSISTENCY_CROSSCHECK and re-checked after the abstract rewrite: +0.0087, +0.0157 [+0.0066,+0.0257], +0.0078 all present and identical).
