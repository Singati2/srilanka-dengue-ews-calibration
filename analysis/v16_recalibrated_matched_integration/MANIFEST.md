# MANIFEST — v16 recalibrated matched integration

Repo /home/mpcrlab/srilanka-dengue-ews-calibration | branch main | HEAD 05f235e | no commit/push
New manuscript: manuscript/paper1_validity_corrected_candidate/paper1_plos_gph_C2_recalibrated_matched_final.{tex,pdf} (40 pp, exit 0, 0 undefined, 0 errors)
Preserved (untouched): paper1_plos_gph.tex (v13), _v14.tex, _C2_final.tex

## Reproduce-first gate: PASS
Re-ran recal_matched.py this session; deterministic output; frozen M1/M4/M5 reproduced to <=1.1e-16; matched recal = 0.01565 -> +0.0157 [+0.0066,+0.0257].

## Result JSONs / scripts
- analysis/v15_reviewer_response_finalization/recal_matched.py (+ recal_matched_results.json)
- analysis/v12_referee_response/run/sl_matched_and_recal.py (+ sl_matched_recal_results.json)
- analysis/v15_final/threshold_sweep.py (+ final_threshold_consistency_check.csv)

## Checksums (sha256, first16)
- 898ad62e3075b34d  manuscript/paper1_validity_corrected_candidate/paper1_plos_gph_C2_recalibrated_matched_final.tex
- e1969a26601caef9  analysis/v15_reviewer_response_finalization/recal_matched.py
- 836964d3255e10f9  analysis/v15_reviewer_response_finalization/recal_matched_results.json
