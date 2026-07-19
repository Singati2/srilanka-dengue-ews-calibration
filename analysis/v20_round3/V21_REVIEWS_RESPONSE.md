# v21 reviews (Panel-2 + STORM) — response (v20b -> v21)

Both v21 reviews CONVERGE: the science is "essentially review-ready," the Colombia §2 fix is confirmed resolved, and the binding constraint is now the (author-owned) submission package, not the science. Both flag the same editable items. Applied all verified/editable fixes + the two should-fix analyses; author-owned blockers flagged.

## Verified editable fixes applied (both reviews)
1. **Grammar:** "an decision-relevant" -> "a decision-relevant" (my v20b error; both reviews caught it).
2. **Abstract reporting-delay caveat:** removed the overstated "the regime in which an early-warning system operates"; added "under a one-sided feature-censoring emulation of reporting delay" (both reviews: it degrades only surveillance predictors, not a true reporting-triangle).
3. **Removed "structure > climate" from the abstract** (both reviews: conditional-only, under-supported for headline status). Retained in Results.
4. **Department-denominator reconciliation:** one sentence — 32 departments contribute fixed effects, 31 appear in the test set, 28 have both outcome classes (Panel-2 §4.2).
5. **Analysis-status terminology:** M4-M1 -> "Design-locked primary (not registered); does not isolate climate" (removes prespecified/registered ambiguity).

## Should-fix analyses added (both reviews requested; new computations, honest)
6. **A2 differential-shrinkage sensitivity (computed, gate-validated).** Refitting SL M5 and M5_no-climate under a single identical penalty gave a matched increment of +0.0087 to +0.0099 (vs independently-penalized +0.0087) -> the increment is NOT an artifact of differential regularization of shared terms. Reassuring; strengthens the point estimate. (script a2_shrinkage.py)
7. **A3 minimum-detectable-effect.** From the development-inclusive interval SEs, MDE ~0.018-0.023 at 80% power (26 RDHS; ~31 depts); observed increments (+0.0087 to +0.0157) lie below -> the null is informative against large gains but underpowered for small effects. Distinguishes informative vs uninformative null (a PLOS-criterion-relevant honesty gain).

Build: 38 pp, exit 0, 0 undefined, 0 errors, 0 figure-box leakage, 0 broken refs. Abstract 438 words. Arithmetic re-audited clean by both reviews; no regression.

## NOT applied (author-owned or display; flagged, not faked)
- Submission package (HARD GATES, both reviews): ethics determination, OpenDengue v1.3 record ID + acquisition date + checksum, repo DOI/license/checksums, pinned Python env, the S1-S18 files, funding/COI/CRediT/acknowledgments/ORCID, all-author approval, local-engagement statement.
- Figure rebuilds (both REQUIRE): add department-conditional to Fig 5; matched comparator to Fig 2; past-only recalibration primary in Fig 3; annotate Fig 4 conditional bands; geography/completeness figure. Table 8 three-interval redesign.
- PROBAST -> PROBAST+AI (needs full citation); PLOS ref style first-six-authors (refs 42,45 - need full author lists); cite Jan-2026 Mexico ablation (need the citation).
- Compression to 25-28 pp (move git chronology, full ladders, cross-fit, Shapley, speculative 2023 to SI); methodological-framing pivot (F1) - PI-level.

## Both reviews' bottom line
The science is defensible and review-ready; the path to submission is completing the package + display correction + compression + not overstating - none of which can be fabricated. Encouragingly, PLOS GPH is a soundness journal that welcomes null results, so the finding is in scope.
