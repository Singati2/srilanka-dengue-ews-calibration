# PLOS_SUBMISSION_MANIFEST (Phase 0)

Repo /home/mpcrlab/srilanka-dengue-ews-calibration | branch main | HEAD 05f235e | no commit/push
Submission manuscript: manuscript/paper1_validity_corrected_candidate/paper1_plos_gph_submission_ready.{tex,pdf} (40 pp; exit 0; 0 undefined; 0 errors)
Preserved untouched: paper1_plos_gph.tex(v13), _v14, _C2_final, _C2_recalibrated_matched_final(v16)

## PLOS format compliance (verified)
- Double spacing (setspace \doublespacing): ON | Line numbers (lineno): ON | Page numbers: ON
- Heading levels: 3 (section/subsection/subsubsection) | Footnotes: none | References: Vancouver numbered (natbib)
- Title 132 chars (<=200); Short title 55 (<=70); Abstract 361 words (<=500), no citations, no undefined abbrev
- Figures: 9 external Fig1-Fig9.pdf (separate files exist); captions in-text after first cite; tables in-text

## Verified result values (re-reproduced this session, gate <=1.1e-16)
- SL raw matched M5-M5_no-climate = +0.0087 [-0.0015,+0.0188] (incl 0)
- SL recal matched recal(M5)-recal(M5_no-climate) = +0.0157 [+0.0066,+0.0257] (excl 0, marginal, 26 clusters, conditional)
- SL unmatched sensitivities: M5-M1 +0.0081 [-0.0025,+0.0180]; recal(M5)-recal(M1) +0.0154 [+0.0064,+0.0255]
- CO matched +0.0078 [+0.0039,+0.0119] (conditional); development-inclusive [-0.0001,+0.0244] (incl 0)

## Key scripts / results (checksums first16)
- e1969a26601caef9  analysis/v15_reviewer_response_finalization/recal_matched.py
- 836964d3255e10f9  analysis/v15_reviewer_response_finalization/recal_matched_results.json
- 9a249f0c69ccab2e  analysis/v12_referee_response/run/sl_matched_and_recal.py
- 7a139d6c6b612dac  analysis/v15_final/threshold_sweep.py

## Submission-readiness of key items
- Manuscript science + format: READY
- Ethics determination: BLOCKED (author/institution)
- Data/code archive DOI: BLOCKED (not yet deposited)
- Funding / competing interests / CRediT / ORCID: BLOCKED (author)
- OpenDengue v1.3 record ID + acquisition date: BLOCKED (author)
- Pinned Python environment: BLOCKED (not preserved)
