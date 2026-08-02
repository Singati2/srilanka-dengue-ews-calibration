# Numeric Crosswalk — Validity-Corrected Candidate
Every number entered into the candidate traces to a frozen Stage-2 source. No value was recomputed. Source root: `analysis/path_b_matched_fixed_effects_original_pipeline/run/` (files: `path_b_point_estimates.json`, `path_b_bootstrap_summary.csv`, `path_b_model_summary.csv`).

| Manuscript location | Number (as printed) | Frozen source | Field/row | Verified |
|---|---|---|---|---|
| Abstract, Results, Discussion, Conclusion | matched climate ΔNB(M5−matched)=+0.0078 [+0.0039,+0.0119] | path_b_bootstrap_summary.csv | dNB_climate_M5_matched (point +0.00783) | ✓ |
| Results, Methods | matched−M1 ΔNB=+0.0110 [+0.0060,+0.0164] | path_b_bootstrap_summary.csv | dNB_nonclimate_matched_M1 (+0.01095) | ✓ |
| Abstract, Results, Discussion | M4−M1 ΔNB=+0.0122 [+0.0073,+0.0171] | path_b_bootstrap_summary.csv | dNB_M4_M1 (+0.01224) | ✓ |
| Abstract, Results (compound), Table | M5−M1 ΔNB=+0.0188 [+0.0117,+0.0260] | path_b_bootstrap_summary.csv / frozen contrasts | dNB_M5_M1 (+0.01878) | ✓ (Gate A reproduced frozen +0.018775) |
| Results table (tab:matcheddecomp) | NB@0.30: M1 0.1171, matched 0.1280, M4 0.1293, M5 0.1358 | path_b_model_summary.csv | NB column | ✓ |
| Results table, Methods | feature counts M1 4 / matched 40 / M4 22 / M5 58 | path_b_model_summary.csv; path_b_design_matrix_columns.txt | nfeat | ✓ |
| Methods, table caption | bootstrap seed 20260612, B=1000, 0 failures; n=13,361; prev 0.375 | path_b_point_estimates.json | boot_B, boot_failures, test_prevalence | ✓ |
| Limitations (exploratory) | LODO compound ΔNB(M5−M1)=−0.0007 [−0.0104,+0.0098] | exp/spatial_cv_out.json (exploratory, plain-logistic; NOT the frozen pipeline) | dnb_m5m1_spatial | ✓ (labeled exploratory) |
| (unchanged) SL M5−M1=+0.0081 [−0.0012,+0.0181] | v18 frozen (S8) | — | ✓ (carried over, not changed) |

Rounding note: printed 4-dp values (+0.0078, +0.0110, +0.0122) are the verified +0.00783 / +0.01095 / +0.01224 rounded; ±0.005 is an internal descriptive band.
