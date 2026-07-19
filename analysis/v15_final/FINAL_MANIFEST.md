# FINAL_MANIFEST (Phase 1) — repo & evidence check

Repo: /home/mpcrlab/srilanka-dengue-ews-calibration | branch: main | HEAD: 05f235e (unchanged; nothing committed/pushed)

## §A determinations vs files on disk
- Reproduction PASS: validation max|Δ| M1=8.9e-16, M4=M5=1.1e-16 over 3,926 rows — CONFIRMED in sl_matched_recal_results.json and re-confirmed by analysis/v15_final/threshold_sweep.py (gate enforced).
- Design intent INTENDED-STRUCTURED: docs/hybrid_model_extension_spec.md L17 (SL structured) vs docs/colombia_model_ladder_spec.md L35 (CO cases-only) — CONFIRMED.
- Provenance CONFIRMED (non-cryptographic): spec 1d8e268 (2026-06-14 13:24) DAG-ancestor of report 02f986e (14:33) on main; mtimes spec 13:15 < predictions 13:32; frozen CSVs git-untracked (author attestation required).
- Matched pair VALID: M5_no-climate independently refit (fit_eval('matched')), differs from M5 only by DLNM climate block.
- No §A determination contradicts the files. No STOP condition.

## Key file checksums (sha256, first 16)
- 3bb8a175798fef61  manuscript/paper1_validity_corrected_candidate/paper1_plos_gph_C2_final.tex
- 46746c8746998b90  manuscript/paper1_validity_corrected_candidate/paper1_plos_gph_v14.tex
- 63498471455b101b  manuscript/paper1_validity_corrected_candidate/paper1_plos_gph.tex
- 9a249f0c69ccab2e  analysis/v12_referee_response/run/sl_matched_and_recal.py
- e432549e7b60c9a4  analysis/v12_referee_response/run/sl_matched_recal_results.json
- 7a139d6c6b612dac  analysis/v15_final/threshold_sweep.py
- 4777b004dcb51c0e  analysis/v15_final/final_threshold_consistency_check.csv
- a396fd29cc747d25  docs/hybrid_model_extension_spec.md
- 20d3104fd8947a0d  docs/colombia_model_ladder_spec.md
## Authoritative frozen inputs (read-only, git-untracked, ~/data_quarantine)
- 3a197d610fde721f  /home/mpcrlab/data_quarantine/analysis_tables/dengue_climate_population_linked_2018_2025_v2_date_aligned.csv
- 0f505fed6a99b2f3  /home/mpcrlab/data_quarantine/model_pilots/hybrid_model_extension_v1/hybrid_model_predictions_v1.csv
- 07f5916a9c53a4fa  /home/mpcrlab/data_quarantine/model_pilots/pilot_h4_75pct_v1/predictions_h4_75pct_v1.csv
