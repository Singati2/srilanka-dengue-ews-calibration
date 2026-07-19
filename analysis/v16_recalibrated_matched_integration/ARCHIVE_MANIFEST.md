# ARCHIVE_MANIFEST — reproducibility artifacts to deposit (Zenodo/OSF)

NOTE: No external archive has been created yet. This manifest lists the artifacts to deposit; do not cite a DOI until deposited.

## Scripts & results (in repo, git-untracked data referenced)
- e1969a26601caef9  analysis/v15_reviewer_response_finalization/recal_matched.py
- 836964d3255e10f9  analysis/v15_reviewer_response_finalization/recal_matched_results.json
- 9a249f0c69ccab2e  analysis/v12_referee_response/run/sl_matched_and_recal.py
- e432549e7b60c9a4  analysis/v12_referee_response/run/sl_matched_recal_results.json
- 7a139d6c6b612dac  analysis/v15_final/threshold_sweep.py

## Frozen inputs (git-untracked, ~/data_quarantine — deposit with checksums)
- 3a197d610fde721f  /home/mpcrlab/data_quarantine/analysis_tables/dengue_climate_population_linked_2018_2025_v2_date_aligned.csv
- 0f505fed6a99b2f3  /home/mpcrlab/data_quarantine/model_pilots/hybrid_model_extension_v1/hybrid_model_predictions_v1.csv
- 07f5916a9c53a4fa  /home/mpcrlab/data_quarantine/model_pilots/pilot_h4_75pct_v1/predictions_h4_75pct_v1.csv

Seed: 20260612 | Clusters: 26 RDHS | n_test: 3926 | recal: past-only rolling-52, eligibility target_week<prediction_week
Also deposit: pinned Python environment (currently NOT preserved — author action), R 4.6.0 + dlnm versions (S5).
