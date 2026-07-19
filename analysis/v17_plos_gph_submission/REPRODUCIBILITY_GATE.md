# REPRODUCIBILITY_GATE (Phase 8)

| Artifact | Status | Location |
|---|---|---|
| Frozen inputs (V2 linked table) | present (git-untracked) | ~/data_quarantine/analysis_tables/…v2_date_aligned.csv |
| Frozen predictions M1/M4/M5 | present (git-untracked) | ~/data_quarantine/model_pilots/hybrid_model_extension_v1/hybrid_model_predictions_v1.csv |
| Matched comparator predictions | regenerated & validated | recal_matched.py (in-repo) |
| Raw + recalibrated result files | present | sl_matched_recal_results.json; recal_matched_results.json; final_threshold_consistency_check.csv |
| Scripts | present (in-repo) | recal_matched.py; sl_matched_and_recal.py; threshold_sweep.py |
| Reproduction gate | PASS | frozen M1/M4/M5 reproduced to ≤1.1e-16; +0.0157 re-reproduced this session |
| Random seeds | documented | 20260612 |
| Cluster identifiers | documented | 26 RDHS (SL); municipality/GID_2 (CO) |
| Dependency versions | PARTIAL | R 4.6.0 + dlnm (S5); **Python stack versions NOT preserved — author action** |
| Execution instructions / expected outputs | present in scripts | validation gate prints max|Δ| and refuses to report if ≥1e-6 |
| Licenses | TODO | choose MIT/CC-BY-4.0 at deposit |
| Permanent archive (DOI) | NOT CREATED | deposit to Zenodo/OSF — author action |

**What can/can't be reproduced:** the entire modeling, matched decomposition, recalibration, and net-benefit pipeline reproduces from the frozen V2 table to machine precision. Full public reproduction depends on depositing the frozen inputs (or a permitted derived/synthetic route) and pinning the Python environment. State this honestly in the DAS.

**Blocking:** pinned Python environment + archived frozen inputs/predictions with checksums + DOI.
