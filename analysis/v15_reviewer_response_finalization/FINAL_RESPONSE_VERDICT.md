# FINAL RESPONSE VERDICT: **READY FOR PI APPROVAL**

The recalibrated matched contrast was computed and **excludes zero** (+0.0157 [+0.0066, +0.0257]); the recalibration-rescue claim is **kept, now on the matched estimand**. No estimand mixing remains; response ↔ manuscript ↔ abstract are numerically identical.

**One explicit caveat (not a science blocker):** the *journal* point-by-point cannot be finalized because no official decision letter exists (pre-submission). The provided point-by-point is **provisional**, mapped to the author-commissioned internal reviews; remap verbatim when the journal responds. This is the only reason the verdict is not unconditional.

## Verdict basis
- **Task 1 — recal matched computed & excludes zero → claim kept.** recal(M5)−recal(M5_no-climate)=+0.0157 [+0.0066,+0.0257]; validated reconstruction (≤1.1e-16 gate). Unmatched +0.0154 demoted to operational sensitivity.
- **Task 2 — number provenance:** every reported value sourced to file/field/model-pair/raw-or-recal/threshold/CI-method (`NUMBER_PROVENANCE_TABLE.csv`).
- **Task 3 — propagation & consistency:** manuscript corrected and rebuilt clean; `RESPONSE_MANUSCRIPT_CONSISTENCY.md` shows digit-level agreement; no "matched" on M5−M1/M4−M1; no "same/similar magnitude."
- **Task 4 — comments:** no official letter → provisional point-by-point + cover letter.
- **Task 5 — response v2** produced (original preserved).
- **Task 6 — §E corrected** in place + correction note.

## Out of scope, still gating submission (author-owned)
Data/code availability, ethics, funding, competing interests, author contributions, OpenDengue v1.3 record ID + date, pinned Python environment; abstract length; ORCID; S# in-text citations. See `analysis/v15_final/PLOS_GPH_compliance_checklist.md`.

## Recommended next step
PI (Shiwakoti/Khadka/Thapa): (1) approve the recalibrated-matched framing and the post-hoc designation; (2) sign the attestation (`COAUTHOR_SIGNOFF.md`); (3) fill the submission blockers; (4) on decision-letter receipt, convert the provisional point-by-point to the official verbatim mapping.

## Git safety
No commit, no push. HEAD 05f235e. v13/v14 preserved; edits only in `paper1_plos_gph_C2_final.tex`.
