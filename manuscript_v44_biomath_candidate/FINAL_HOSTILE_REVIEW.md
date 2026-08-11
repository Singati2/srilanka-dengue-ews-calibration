# FINAL_HOSTILE_REVIEW

Six internal self-critique perspectives on the final candidate. **Not independent external reviewers.**

## 1. Statistical prediction
Matched contrast well-specified (M5 vs M5$_{\text{no-climate}}$, 18-column climate difference); tuning distinction stated (independent penalty selection, `FITTED_PARAMETER_IDENTITY = NOT REQUIRED`); proper scores oriented; calibration separate; conditional vs development-inclusive uncertainty preserved with the Colombia fixed-FE caveat. **OK.**

## 2. Decision theory
$V_k$ metric-oriented (larger=better), $\Delta V_{C,k}=V_k(\mathcal I^{SC})-V_k(\mathcal I^S)$ identifiable at a glance; net benefit in Vickers sense with cost–loss weight; ornamental formalism removed (no σ-algebra, no spatial operator or $\Delta V_G$ in Methods). No math-overclaim. **OK.**

## 3. Dengue epidemiology
Elevated-activity threshold exceedance, explicitly not outbreak; no causal overreach ("predictive feature-block contrast, not causal"); comparator = recent surveillance; short-lead ($h=4$) plausibility argued via autocorrelation; Sri Lanka and Colombia kept as two case studies, no formal heterogeneity. **OK.**

## 4. Temporal / geospatial validity
Forecast-origin admissibility as a plain condition; **no satellite/M6 result imported**; **no WP5 result imported**; spatial operator is a Discussion note flagged pending; no spatial-validation overclaim (Moran's I inconclusive, stated). **OK.**

## 5. Reproducibility
Every headline number traces to canonical v44 (`BIOMATH_NUMERIC_CROSSWALK.md`, 241/241); `+0.0099` provenance = pre-existing (commit 0b8bbff, 2026-07-15; `SINGLE_PENALTY_0099_PROVENANCE.md`); figure provenance documented (frozen figs unavailable → placeholders); canonical source hashes unchanged; **no hidden refits** (no model fit/refit in this task). **OK** (figures are a documented pre-submission item, not a review-branch blocker).

## 6. Hostile PLOS/GeoHealth editor
1. **What is new?** The joint evaluation architecture (matched climate ablation + calibration + proper scores + decision-curve net benefit + development-inclusive uncertainty) and the metric-oriented incremental estimand; a hedged DCA-in-population-dengue-EWS gap.
2. **Why exist?** It shows apparent climate value can be an artifact of a weak comparator/metric; a cautionary, methodological result.
3. **Null + equations?** The finding is deflationary but valid; the equations clarify the estimand rather than inflate it.
4. **Matched ablation convincing?** Yes — feature-block evidenced; comparator-gap shrinkage quantified (CO +0.0188→+0.0078).
5. **DCA novelty supported?** As a hedged "did not identify a prior…," yes; not as "first-ever."
6. **Title overstated?** No — decision-analytic, no "biomathematics," no country comparison.
7. **Colombia overinterpreted?** No — selected higher-incidence subset, boundary-adjacent DI bound, no transportability claim.
8. **Too long?** Main text is lean; the framework subsection is ~6 equations; SI carries machinery.
9. **Math helpful or distracting?** Helpful after tightening (ornament removed).
10. **Survive desk review?** At a methodology/decision or geo-epi venue (PLOS GPH / GeoHealth / BMC Med Res Methodol / Diag Progn Res), plausibly yes, contingent on author-owned submission items and figures.

## Verdict: **`MINOR_REVISION_INTERNAL`**
The candidate is coherent, faithful, and defensible. Residual items are author-owned/pre-submission (frozen figures; ethics/ORCIDs/funding/COI/Zenodo DOI+license/OpenDengue v1.3 id), not correctness defects. **Not `DO_NOT_PUSH`.** Suitable to land as a review-only branch + draft PR.
