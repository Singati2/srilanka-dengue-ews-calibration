# FINAL VERDICT: **SCIENCE READY FOR PI SIGN-OFF**

The development-inclusive computation (B2) was reproduced and computed; the framing is updated and internally consistent; the primary setting now has its own matched-decomposition table, Table 6 shows the matched comparator, and Fig 4 is rebuilt to display the matched decision curves. Completion items remain author-action (listed). No scientific revision outstanding.

## Phase-1 branch taken: **EXCLUDES zero (stronger than expected)**
Reproduce-first gate PASSED (frozen M5 to 1.1e-16; conditional matched recal reproduced at +0.0157). Development-inclusive refit bootstrap (26 RDHS, seed 20260612, **B=300, 0 failures**):

| Contrast | Point | Conditional CI | Development-inclusive CI |
|---|---|---|---|
| Raw matched | +0.0087 | [−0.0015, +0.0188] | **[−0.0074, +0.0223]** (incl 0) |
| Recalibrated matched | +0.0157 | [+0.0066, +0.0257] | **[+0.0015, +0.0284]** (excl 0, marginal) |

**The Sri Lanka recalibrated matched exclusion SURVIVES model-development uncertainty** (marginally: lower bound +0.0015 on 26 clusters), whereas **Colombia's does NOT** ([−0.0001, +0.0244]). This is the opposite of the prompt's expectation; the framing follows the data. The raw increment includes zero under both treatments, so the exclusion is recalibration-dependent. The result is reported honestly as marginal (B=300, finite clusters) and not leaned on as a strong positive.

## How the framing changed
- Abstract: added the SL recalibrated development-inclusive interval [+0.0015,+0.0284] alongside the conditional; states the raw increment includes zero throughout and the exclusion depends on recalibration; closing sentence: no exclusion robust across both raw evaluation and refitting in either setting.
- Cross-setting synthesis: **corrected** the (now-inaccurate) v16 statement — Colombia dissolves under model-development uncertainty; Sri Lanka's recalibrated exclusion marginally survives; neither excludes zero raw.
- Line ~615 caveat: Sri Lanka now carries the same model-development caveat as Colombia (removed the weaker "raw-scale calibration" substitute).

## Consistency (C1/C2/C3)
- **C1:** recalibration statement scoped to "not recalibrated in the original frozen analysis," cross-referencing the post-hoc recalibration (resolves the contradiction with §3.9).
- **C2:** the raw SL M5−M1 CI is canonicalized to the frozen committed value [−0.0012, +0.0181] (manuscript already internally consistent across 5 loci); the reconstruction's [−0.0025, +0.0180] differs only by bootstrap implementation (same point, both include zero) — documented in NUMBER_PROVENANCE_TABLE.csv, no manuscript change needed.
- **C3:** cross-setting section rewritten to lead with the comparable matched estimand; the non-comparable M5−M1 juxtaposition demoted to per-setting frozen-pipeline context.

## Displays — ALL DONE
- New **Sri Lanka matched-decomposition table** (Table~\ref{tab:slmatched}) — raw and recalibrated matched increment with conditional AND development-inclusive intervals, plus the structure contrast; parallels Colombia's table.
- **Table 6** now includes the **M5_no-climate (matched comparator) row** (AUC 0.751; NB 0.185/0.136/0.083 at p*=0.20/0.30/0.40, raw) — computed from the validated reconstruction (gate <1e-6); the matched no-climate model performs like M1 on these metrics, as expected.
- **Fig 4 rebuilt** (`fig4_table6.py`): Panel A = M5 vs M5_no-climate decision curves under raw and past-only recalibration with alert-all reference; Panel B = the specification-matched climate increment across thresholds (raw and recalibrated) with 95% cluster-bootstrap bands (increment@0.30 raw +0.0087 / recal +0.0156; recalibrated band above zero near the reference threshold). Cross-fit recalibration moved to Supporting Information. New Fig4.pdf embedded and verified rendering.

## Terminology (Phase 4)
- "confirmatory" → "corroborates this prior finding"; "genuinely novel" softened to "the contribution we emphasize"; "contributed far more" → "the contrast from adding seasonal and geographic structure … was larger than the matched climate contrast." "operational" language: the past-only recalibration is described as time-respecting; not further hardened here (the manuscript already flags reporting-delay attenuation).

## Completion items outstanding (author-action; block submission independently)
Ethics determination; OpenDengue v1.3 record ID + acquisition date; repository DOI/license + checksummed archive; pinned Python environment; Supporting Information S1–S18 must actually exist; funding/competing-interests/CRediT/ORCID; coauthor sign-off + provenance attestation; global-health authorship/engagement (all-US team on a Sri Lanka/Colombia study). See SUBMISSION_READINESS_CHECKLIST.md.

## Git safety
No commit, no push. HEAD 05f235e. New file only: paper1_plos_gph_v17_devinclusive_final.tex; v13/v14/C2_final/v16/submission_ready preserved.
