# Knowledge-Graph + Agent-Graph Audit

- Generated: 2026-08-07T04:19:48.733702Z
- Repo: `/tmp/claude-1000/-home-mpcrlab/af40ce96-d2d5-4f3c-9d5a-4c9cb2ee3ec8/scratchpad/v44_build`
- Graph: 913 nodes / 592 edges
- Findings: 1 critical · 4 major · 5 minor
- **SUBMISSION READY: NO**

## Release gates

| Gate | Status | Findings |
|---|---|---|
| REPOSITORY DOCUMENTATION | REVIEW | 2 |
| DATA PROVENANCE | REVIEW | 1 |
| TEMPORAL LEAKAGE | NOT_VERIFIED | 1 |
| SPATIAL CONSISTENCY | PASS | 1 |
| MODEL SPECIFICATION | PASS | 0 |
| CALIBRATION | PASS | 0 |
| REPRODUCIBILITY | NOT_VERIFIED | 1 |
| REFERENCE INTEGRITY | NOT_VERIFIED | 1 |
| RESULT TRACEABILITY | REVIEW | 1 |
| MANUSCRIPT CONSISTENCY | REVIEW | 1 |
| ADVERSARIAL REVIEW | PASS | 0 |
| SUBMISSION DECLARATIONS | FAIL | 1 |

## Findings by gate

### REPOSITORY DOCUMENTATION — REVIEW
- **[major]** 130 absolute machine-specific path(s) in tracked files (portability)  
    - ALT_STATS/PHASE1_GATE.md: /home/mpcrlab/
    - ALT_STATS/PHASE1_GATE.md: /home/mpcrlab/
    - ALT_STATS/PHASE1_GATE.md: /home/mpcrlab/
    - ALT_STATS/environment/requirements-lock.txt: /home/mpcrlab/
    - ALT_STATS/src/freeze_matched_predictions.py: /home/mpcrlab/
    - ALT_STATS/src/freeze_matched_predictions.py: /home/mpcrlab/
    - ALT_STATS/src/freeze_matched_predictions.py: /home/mpcrlab/
    - ALT_STATS/src/freeze_matched_predictions.py: /home/mpcrlab/
- **[minor]** working tree dirty at audit time

### DATA PROVENANCE — REVIEW
- **[major]** 26 data-like csv/json tracked under analysis/ (quarantine risk)  
    - ALT_STATS/PAIRED_ROW_MANIFEST.csv
    - ALT_STATS/frozen/colombia_matched_pairs.csv
    - ALT_STATS/frozen/srilanka_matched_pairs.csv
    - ALT_STATS/logs/freeze_gates.json
    - ALT_STATS/logs/paired_audit.json
    - analysis/geo_effect_decomposition/co_devincl_full_refit_distribution.csv
    - analysis/geo_effect_decomposition/co_geo_partial_refit_distribution.csv
    - analysis/path_b_matched_fixed_effects_original_pipeline/run/path_b_bootstrap_distribution.csv

### TEMPORAL LEAKAGE — NOT_VERIFIED
- **[minor]** static scan only; composite-availability dates, threshold/scaling/recalibration windows, lag construction, and outcome-vs-origin timing are NOT verified here  
    - see composite_leaks_if_joined_by_start() — join dynamic layers on composite_end, not start

### SPATIAL CONSISTENCY — PASS
- **[minor]** manuscript mentions both 32 dept fixed-effect columns and 31 test departments — ensure this is explained  
    - 32 department fixed effects vs 31 analyzed test departments

### MODEL SPECIFICATION — PASS
- (no issues)

### CALIBRATION — PASS
- (no issues)

### REPRODUCIBILITY — NOT_VERIFIED
- **[minor]** reproducibility is presence-only (lockfile/checksum/seeds detected) but NOT re-executed; quarantined inputs cannot be recomputed in this audit  
    - run scripts in a clean env with hash checks to earn a strong PASS

### REFERENCE INTEGRITY — NOT_VERIFIED
- **[minor]** scientific reference support (does each cited source actually support its sentence?) is NOT_VERIFIED — citation-key integrity is checked, but DOI/metadata and claim-support require a network verifier  
    - a valid \cite key does not imply the source supports the claim

### RESULT TRACEABILITY — REVIEW
- **[major]** 117/278 4-dp effect values not matched to a committed result file  
    - -0.0012 (L171: The Python DLNM-style and canonical R \texttt{dlnm} climate specificat)
    - -0.0002 (L173: Because rolling recalibration in the frozen run was applied only to M0)
    - -0.0002 (L176: \caption{Sri Lanka matched climate ablation decision curves (test peri)
    - -0.0002 (L193: Sri Lanka, recalibrated & $+0.0157$ & $+0.0066$ to $+0.0257$ & $-0.000)
    - -0.0346 (L206: Evaluating the frozen matched predictions with strictly proper, thresh)
    - -0.0067 (L206: Evaluating the frozen matched predictions with strictly proper, thresh)
    - -0.0165 (L206: Evaluating the frozen matched predictions with strictly proper, thresh)
    - -0.0011 (L206: Evaluating the frozen matched predictions with strictly proper, thresh)
    - -0.0256 (L206: Evaluating the frozen matched predictions with strictly proper, thresh)
    - -0.0085 (L206: Evaluating the frozen matched predictions with strictly proper, thresh)
    - -0.0043 (L206: Evaluating the frozen matched predictions with strictly proper, thresh)
    - -0.0403 (L206: Evaluating the frozen matched predictions with strictly proper, thresh)

### MANUSCRIPT CONSISTENCY — REVIEW
- **[major]** manuscript asserts a public GitHub repo/commit — must be verified from a clean unauthenticated environment before submission  
    - repository availability claim

### ADVERSARIAL REVIEW — PASS
- (no issues)

### SUBMISSION DECLARATIONS — FAIL
- **[critical]** 9 unresolved placeholder(s) (author-supplied fields block submission)  
    - AUTHOR INPUT REQUIRED x9
