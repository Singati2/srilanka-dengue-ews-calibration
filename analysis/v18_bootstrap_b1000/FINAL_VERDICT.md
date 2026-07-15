# FINAL VERDICT: **HEADLINE DISSOLVED AT B=1000 — SYMMETRIC-NULL REFRAME PENDING PI**

The paper's most contested exclusion was re-estimated at the same resampling depth (B=1000) as every other interval in the manuscript. It **does not hold**: the Sri Lanka recalibrated matched increment's development-inclusive interval crosses zero at B=1000. The manuscript is reframed to the fully symmetric, honest conclusion; the reframe is a PI-level scientific call.

## The gate
Reproduce-first PASSED (frozen M5 to 1.1e-16; conditional matched recal reproduced at +0.0157). B=1000, 1000/1000 replicates, 0 failures, identical procedure (only B and output path changed; script diff = 0 otherwise).

| Recalibrated matched dev-inclusive | Lower bound | Zero? |
|---|---|---|
| B=300 | +0.0015 | excludes (marginal) |
| **B=1000** | **−0.0002** | **includes** |

Point estimates (+0.0087, +0.0157) and all conditional CIs unchanged. Raw matched dev-inclusive [−0.0079, +0.0245] (includes zero). Colombia dev-inclusive [−0.0001, +0.0244] (includes zero). The B=300 exclusion was a shallow-bootstrap artifact.

## The reframe (symmetric-null)
- Abstract, §3.8 cross-setting, line-~615 caveat, Results recalibration paragraph, and the Sri Lanka matched table (Table 6) all rewritten: the recalibrated increment excludes zero **only under conditional resampling** and includes zero once both models are refit; the raw increment includes zero throughout.
- **Headline:** *no matched exclusion is robust across both raw evaluation and model refitting in either setting.* Sri Lanka's exclusion additionally requires recalibration; Colombia's dissolves under refitting. Neither is leaned on as a positive.
- All "survives model-development uncertainty" positive phrasing removed; the cross-tier statement is now symmetric (both hold only under conditional resampling and dissolve under refitting).

## Verifications (Task 3)
- **C2 disclosure — done.** The two-bootstrap reconciliation for raw M5−M1 ([−0.0012,+0.0181] committed vs [−0.0025,+0.0180] reconstruction; same point +0.0081, both include zero) was previously only in the provenance CSV; **one sentence added to SI (S14 Text).**
- **Table 6 M5_no-climate row — genuinely computed, not a copy of M1.** Full precision (n=3,926): M1 AUC 0.751480 / NB 0.184857 / 0.136635 / 0.082527; matched AUC 0.751293 / NB 0.184794 / 0.136016 / 0.082781. They differ at every metric (NB0.30 even rounds differently, 0.137 vs 0.136); max|p_M1−p_matched| = 2.9e-3. See VERIFICATIONS.md.

## Scientific bottom line
Unchanged in direction, now stated symmetrically and honestly: recent surveillance is a strong benchmark; the specification-matched climate increment is small, positive in point estimate, and **not robustly distinguishable from zero in either setting once model-development uncertainty is included**; predictive/decision-analytic, not causal, not transportable.

## Still author-action (unchanged)
Ethics, OpenDengue v1.3 ID, archive DOI/checksums, pinned Python env, SI S1–S18 must exist, funding/CI/CRediT/ORCID, coauthor attestation, global-health authorship. The symmetric reframe is a PI-level scientific decision to approve.

## Git safety
No commit, no push. HEAD 05f235e. New file only: paper1_plos_gph_v18_b1000_final.tex; v13/v14/C2_final/v16/submission_ready/v17 all preserved.
