# Point-by-point response — PROVISIONAL

**Status flag (Task 4):** No official journal decision letter or external referee comments for `paper1_plos_gph` exist in the repository — this manuscript is **pre-submission**. The only review material on record is **author-commissioned internal / AI peer review** (e.g. `docs/manuscript_peer_review_v1.md`, and the STORM / expert-panel / estimand-audit reviews the authors ran). A journal point-by-point response **cannot be finalized** until the decision letter arrives. The mapping below is provisional, against the internal reviews that drove this revision; **remap to the official comments verbatim when they are received.**

| # | Internal review theme (source) | Response | Change + location |
|---|---|---|---|
| R1 | SL M1 mis-described as cases-only (estimand audit) | Corrected to structured; country-specific ladder | Methods ladder; §D.1 block; Table (analysis status) |
| R2 | Is the SL M1 structure intended or a bug? (specification audit) | Adjudicated INTENDED-STRUCTURED via dated design-lock spec; provenance CONFIRMED (non-cryptographic) | Methods/pre-specification para; Supplementary Reproducibility Note |
| R3 | Run the SL specification-matched decomposition (both harsh reviews) | Ran it; +0.0087 raw [−0.0015,+0.0188] | Results (SL structured-climate); Table |
| R4 | M4−M1 called "confounded" / treated as isolating climate | Relabeled non-nested, structurally mismatched; demoted secondary | Abstract, Results L357, Discussion L381 |
| R5 | Don't call M5−M1 "matched" (recal-resolved prompt) | Corrected everywhere; ≈0.0006 reconciliation added | Results L263, L357; Discussion L383, L393; abstract |
| R6 | "+0.015 recalibrated" is unmatched, not the matched estimand (recal-resolved prompt) | **Computed recal(M5)−recal(M5_no-climate) = +0.0157 [+0.0066,+0.0257], excludes zero**; +0.0154 unmatched demoted to operational sensitivity | Abstract, Results recal subsection, Discussion |
| R7 | "Same/similar magnitude" across settings overstates | Replaced with consistent-sign / not-equal-magnitude wording | Abstract, Results, Discussion (all loci) |
| R8 | Add past-only recalibration; don't present cross-fit as deployable | Added past-only; cross-fit flagged optimistic/non-deployable | Recalibration subsection |
| R9 | Colombia complete-case selection bias | IPW sensitivity + disclosure that estimand is the analysed subset | Colombia selection subsection |
| R10 | Bootstrap omits development uncertainty; few clusters | Stated conditional-on-frozen-predictions; 26-RDHS caution; CO development-inclusive interval (incl. 0) | Uncertainty subsection; Discussion |
| R11 | Reproducibility / provenance hardening | Attestation + checksummed-archive recommendation | Supplementary Reproducibility Note; COAUTHOR_SIGNOFF |

The thematic summary is in `cover_letter_revision_summary.md`; the full revised response text is `reviewer_response_final_v2.md`.
