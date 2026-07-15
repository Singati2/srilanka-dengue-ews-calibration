# AUDIT MANIFEST — v13 specification audit (Phase 0)

- Repository: ~/srilanka-dengue-ews-calibration ; git HEAD 05f235e ; branch as at session start.
- Manuscript under audit: manuscript/paper1_validity_corrected_candidate/paper1_plos_gph.tex (untracked working copy; 39 pp).
- Preserved prior versions (untouched): paper1_best_v10..v16.tex, paper1_plos_gph pre-SL states, all in the manuscript dir and ~/Downloads.
- Authoritative frozen inputs (read-only, in data_quarantine/, git-ignored):
  - Base linked table: analysis_tables/dengue_climate_population_linked_2018_2025_v2_date_aligned.csv
  - SL scripts: model_pilots/hybrid_model_extension_v1/_run_hybrid_model_extension.py ; model_pilots/rolling_recalibration_v1/_run_rolling_recal.py ; model_pilots/pilot_h4_75pct_v1/_fit_eval.py
  - SL frozen predictions: hybrid_model_extension_v1/hybrid_model_predictions_v1.csv ; pilot_h4_75pct_v1/predictions_h4_75pct_v1.csv
  - Design-lock specs: docs/hybrid_model_extension_spec.md (SL) ; docs/colombia_model_ladder_spec.md (CO)
- Reconstruction script (audit): analysis/v12_referee_response/run/sl_matched_and_recal.py ; results sl_matched_recal_results.json
- Git safety: no commit, no push, no overwrite of preserved versions. Working tree only.
