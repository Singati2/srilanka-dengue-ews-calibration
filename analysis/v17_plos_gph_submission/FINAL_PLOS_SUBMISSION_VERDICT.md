# FINAL PLOS SUBMISSION VERDICT: **READY AFTER ADMINISTRATIVE BLOCKERS**

Every **scientific, estimand, reproducibility, and technical/format gate passes.** What remains is author-owned administrative material and PI/coauthor sign-off — no scientific revision is required.

## Submission-blocking gates (Phase-15 list)
| # | Gate | Status |
|---|---|---|
| 1 | Matched/unmatched estimands not mixed | ✅ PASS |
| 2 | Post-hoc estimand not called prespecified | ✅ PASS (scoped to ladder/M1) |
| 3 | Raw interval including zero not hidden | ✅ PASS (abstract states it) |
| 4 | Recalibrated matched result reproducible | ✅ PASS (+0.0157 re-reproduced; frozen ≤1.1e-16) |
| 5 | Ethics approval/exemption documented | ❌ BLOCKED (author/institution) |
| 6 | Data-use permissions resolved | ❌ BLOCKED |
| 7 | Data Availability Statement accurate/complete | ⚠ draft; OpenDengue v1.3 ID + DOI pending |
| 8 | Author code available (archive) | ❌ BLOCKED (Zenodo/OSF DOI) |
| 9 | Frozen predictions + checksums preserved/archived | ⚠ preserved locally; archive pending |
| 10 | Author attestation (SL M1 fixed before results) | ❌ pending sign-off |
| 11 | CRediT roles approved | ❌ pending |
| 12 | Corresponding-author ORCID | ❌ missing |
| 13 | Funding + competing interests verified | ❌ pending |
| 14 | Figures/tables/refs/citations compile | ✅ PASS (40 pp, 0 undefined, 0 errors) |
| 15 | No official-reviewer-response language | ✅ PASS (all internal-labeled) |

## Scientific hierarchy (as stated in the manuscript)
- **Prespecified, design-locked:** M4−M1 (Sri Lanka) — non-nested, does not isolate climate; secondary.
- **Post-hoc, principal interpretable (exploratory):** M5−M5_no-climate — raw +0.0087 [−0.0015,+0.0188] (incl 0); recalibrated +0.0157 [+0.0066,+0.0257] (excl 0, marginal, 26 clusters, conditional).
- **Unmatched sensitivities:** M5−M1 +0.0081; recal(M5)−recal(M1) +0.0154.
- **Colombia matched:** +0.0078 [+0.0039,+0.0119]; dev-inclusive includes zero.

## What the authors must do before submitting
Ethics determination · OpenDengue v1.3 ID + acquisition date · Zenodo/OSF archive DOI + license · pinned Python environment · funding + competing-interests + CRediT + ORCIDs · ≥4 reviewer suggestions · all-author approval + M1 attestation. (Detail in PLOS_GPH_COMPLIANCE_CHECKLIST.md, ETHICS_EQUITY_AUTHORSHIP_AUDIT.md, and the drafted statement files.)

Recommended (not blocking): move 4 figures to Supporting Information (FIGURE_TABLE_PLAN.md); consider local-country scientific engagement/authorship for the two-LMIC study (equity).

## Git safety
No commit, no push. HEAD 05f235e. Preserved: v13, v14, C2_final, v16. New file only: paper1_plos_gph_submission_ready.tex/.pdf.
