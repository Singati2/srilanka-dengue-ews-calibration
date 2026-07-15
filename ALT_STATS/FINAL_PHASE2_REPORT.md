# FINAL_PHASE2_REPORT.md — Phase 2 alternative-statistics analysis

## 1. Executive verdict
A prospectively locked, threshold-free proper-scoring reanalysis of the checksum-frozen
Version 6 matched predictions. Under the matched specification, the full climate model has
**better overall probability accuracy** than the pipeline-matched no-climate model in both
settings and both prediction states (ΔNLL and ΔBrier negative; conditional 95% intervals
exclude zero). This is **concordant in direction** with the Version 6 decision-curve finding
and refines it: proper scores reward calibrated probability improvement across the whole
distribution, whereas the Version 6 net benefit at a single alert threshold was small and
threshold-dependent. Development-inclusive proper-score intervals were not computed (Phase 1
gate), so robustness to model redevelopment is not assessed here, and no operationally
worthwhile increment was elicited. **Recommendation: INCLUDE WITH MAJOR CAVEATS** (see §20).

## 2. Phase 1 gate
Frozen predictions REPRODUCED for both settings (SL <1e-6; Colombia M5_recal fidelity
1.11e-16; matched point +0.00783 vs +0.00786). Refit-both-models pipelines NOT re-executed →
development-inclusive proper-score intervals NOT computed; conditional only. See
`PHASE1_GATE.md`.

## 3. Frozen inputs and checksums
`FROZEN_INPUTS.sha256` (2 files), regenerated via verbatim V6 pipelines and reproduce-gated;
`FROZEN_INPUTS_MANIFEST.md`. Provenance: matched no-climate predictions regenerated, not
stored (deviation D1).

## 4. Canonical row-pair audit
`PAIRED_ROW_MANIFEST.csv` (34,574 rows). 0 duplicate keys, 0 missing probabilities, identical
keys/outcomes per model. Colombia 13,361 (5,015 events, 475 muni / 31 dept); Sri Lanka 3,926
(1,321 events, 26 RDHS). See `PAIRED_ROW_AUDIT.md`.

## 5. Locked analysis chronology
Plan + inputs committed and tagged (`alt-stats-plan-v1`, commit `28c0341e`) BEFORE scoring;
`LOCK_RECORD.md`. Scoring run post-lock. One post-lock **code** bug fix (bootstrap indexed
full array not the resample; deviation D3) — plan unchanged, point estimates unaffected.

## 6. Computational environment
Python 3.10.12; numpy 1.26.4, pandas 2.1.3, scikit-learn 1.7.2, scipy 1.11.4, statsmodels
0.14.6, patsy 1.0.2; seed 20260612; PCG64. V6 Python versions unpinned (reconstruction);
reproduce-gates confirm fidelity. `ENVIRONMENT.md`, `environment/requirements-lock.txt`.

## 7. Primary ΔNLL results
SL recal −0.0207 [−0.0353,−0.0068] (IG +0.030 bits); SL raw −0.0256 [−0.0391,−0.0128];
Colombia recal −0.0089 [−0.0168,−0.0010] (IG +0.013 bits); Colombia raw −0.0085
[−0.0138,−0.0029]. All favor climate; conditional intervals exclude zero.

## 8. Brier-score results
SL recal ΔBS −0.0079 [−0.0130,−0.0031]; SL raw −0.0107 [−0.0156,−0.0061]; Colombia recal
−0.0043 [−0.0078,−0.0008]; Colombia raw −0.0036 [−0.0059,−0.0013]. BSS 0.02–0.06 (descriptive).

## 9. Calibration results
Recalibration reduced CITL toward 0 (SL) or left residual over-prediction (Colombia, both
models). Full-climate ICI marginally better than no-climate in the primary states (SL recal
0.027 vs 0.045; Colombia recal 0.109 vs 0.113). Descriptive/diagnostic, not primary.

## 10. Discrimination results
ΔAUC favors climate with intervals excluding zero (SL recal +0.027 [+0.013,+0.045]; Colombia
+0.012 [+0.002,+0.023]); ΔPR-AUC positive but borderline. Secondary.

## 11. Conditional uncertainty
Paired cluster bootstrap B=5000 (municipality primary for Colombia; RDHS for SL), seed
20260612, 0 failures/5000. B=1000 parity near-identical. Department-clustered Colombia
sensitivity available in replicate store; municipality primary per plan.

## 12. Development-inclusive uncertainty
NOT COMPUTED (Phase 1 gate). Stated throughout. No substitute pipeline built.

## 13. Cross-checks with Version 6
All MATCH within tolerance (`V6_CROSSCHECK.md`): n, prevalence, clusters, per-observation
M5_recal (1.11e-16), matched dNB points. No V6 value overwritten.

## 14. Concordance with decision-curve analysis
Category: **"Probability-accuracy improvement without demonstrated decision value."** Proper
scores favor climate under the matched specification; Version 6 decision-curve net benefit
was small, threshold-dependent, and operationally uncosted. Statement: *Climate improved
overall probability accuracy under the matched specification, but this did not establish
improved decisions at the evaluated alert trade-offs.*

## 15. What Phase 2 fixes
Removes dependence on a single alert threshold; evaluates the frozen matched predictions with
strictly proper, threshold-free scores under a locked rule set; gives a checksum-pinned,
reproducible, cross-checked secondary result.

## 16. What Phase 2 does NOT fix
Post-hoc status of the matched ablation; Colombia complete-case selection; finalized (not
real-time) surveillance; exposure aggregation / spatial support / transportability; absence
of an elicited minimum worthwhile increment; development-inclusive (redevelopment) uncertainty
for the proper scores.

## 17. Deviations from the locked plan
D1 (matched preds regenerated not stored), D2 (DI intervals not computed — gated), D3 (post-
lock bootstrap code bug fix; plan unchanged). See `deviations.md`.

## 18. Reproducibility commands
`python3 ALT_STATS/src/freeze_matched_predictions.py` (reproduce-gate + freeze) →
`python3 ALT_STATS/src/score_route_a.py` (verify checksums + score) →
`python3 ALT_STATS/src/make_figures.py`. Seed 20260612 throughout.

## 19. Submission-language recommendation
Use `MANUSCRIPT_PARAGRAPH.md` verbatim. Frame as a locked secondary robustness reanalysis,
concordant-in-direction with the decision-curve analysis, that improves overall probability
accuracy but does not establish operational decision value; keep post-hoc and
selection/finalized-data caveats.

## 20. Final go/no-go
**INCLUDE WITH MAJOR CAVEATS.** Rationale (reproducibility/fidelity/completeness/limitations,
not favorability): the analysis is checksum-locked, reproduce-gated, cross-checked to V6, and
complete for Route A; but (a) development-inclusive proper-score intervals are absent, so the
conditional intervals must not be read as robustness to redevelopment; (b) the matched
ablation remains post hoc; (c) no operationally worthwhile increment is established. The
direction (climate improves proper scores) is reported exactly as obtained and does not
change this recommendation.
