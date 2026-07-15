# Matched recalibration verification (reproduce-first gate: PASS)

I re-ran `recal_matched.py` this session (did not trust the audit JSON blindly). Output was deterministic and identical to the prior run.

- **Reproduction gate:** frozen M1/M4/M5 test predictions reproduced to max|Δ| = 8.9e-16 (M1), 1.1e-16 (M4/M5) over n=3,926 rows; script exits without reporting if any |Δ| ≥ 1e-6.
- **Both matched models recalibrated identically:** M5 and M5_no-climate each recalibrated with the same past-only rolling-52-week intercept recalibration, same eligibility `target_week < prediction_week`, same evaluation rows, same weekly loop. (M1 also recalibrated for the unmatched sensitivity.)
- **Recalibrated matched contrast:** recal(M5) − recal(M5_no-climate) = **+0.01565 → +0.0157**, 95% CI [+0.00655, +0.02569] → **[+0.0066, +0.0257]**, 26-RDHS cluster bootstrap, seed 20260612. **Excludes zero (marginal).**
- **Reproduced +0.0157? YES.**
- Selected penalty C=10.0 for both M5 and M5_no-climate. Bootstrap conditional on frozen fitted predictions (omits model-development uncertainty).
- **Operational availability:** eligibility uses only forecast–outcome pairs whose targets were observed before the prediction week; recent outcomes required for recalibration would need to be available in deployment (stated as a limitation).
