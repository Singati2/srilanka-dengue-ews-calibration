# PLOS NTD Revision v5 (final scientific audit) — Governance Manifest

> **Provenance.** Revision v5 was created from the preserved source that generated `Dengue (3).pdf` after a complete 22-page (now 21-page) scientific and visual audit. Earlier revisions remain unchanged. The reviewed PDF `~/Downloads/Dengue (3).pdf` (sha256 `32cbb363…`) is a recompile that is byte-different but **text-identical** to `manuscript/plos_ntd_revision_v4_full_audit/dengue_ews_plos_ntd_v4.tex` (`94860499…`, line numbers removed); hash ledger in `source_state_at_v5_start.sha256`.

> **Scope.** Final scientific-integrity, inference, reference, journal-format, and page-layout correction. **No model, bootstrap, confidence interval, calibration, recalibration, sensitivity, threshold, heterogeneity test, biomodel, or dataset transformation was run.** Only frozen reports, committed scripts, saved outputs, and verified bibliographic sources were used. Reference metadata and the official EWARS-csd author list were verified against publisher pages (a permitted verified-bibliographic-source step).

## What changed in v5 (writing/layout/reference only)
- §2/§5 Abstract: removed "not significant"; estimate-and-uncertainty language; 293 words.
- §3: removed "confirmatory"/"registered primary contrast"; benchmark-comparison wording; retained "no prospective public registration is claimed."
- §4: corrected p*=0.30 interpretation (0.429 TP-equivalents per false alert; 2.33 false alerts per true alert).
- §6 Author Summary: neutral inference wording; 200 words.
- §7: neutral sensitivity language (no "excludes zero"/"borderline").
- §8: cross-setting caption rewritten as publication prose (no overlap commentary).
- §9/§10: Colombia calibration verified post-Platt; observed prevalence 0.375 restored as known for the common-complete M0–M5 set; only per-model mean predicted probability unretained.
- §11: Table 4 M4 row added (frozen values); three contrasts with explicit subtraction orientation.
- §12: Figure 3 Panel B made zero-based.
- §13: Table 2 zero formatting normalized; no full-grid-in-SI claim.
- §14: sentence-case title + short title + dedicated title page.
- §15: continuous line numbers + double spacing; per-page internal-review footer replaced by a title-page notice and a light running header.
- §16: references converted to Vancouver (inline; NLM abbreviations; first-six-et-al); OpenDengue editorial note removed; EWARS-csd author list corrected (Schlesinger M et al.).
- §17: R 4.6.0 / dlnm 2.4.10 / mgcv 1.9.4 / tsModel 0.6-2 verified from committed records; Python stack "not preserved."
- §18: SI captions limited to existing draft files (S1–S6); S7–S10 marked not-provided.
- §21: American English + notation consistency confirmed.

## Governance attestations
- No metric recomputed; no model/bootstrap/CI/calibration/recalibration/sensitivity/threshold/heterogeneity/biomodel/dataset run.
- No missing administrative value invented; placeholders are neutral and tracked in `submission_blockers_v5.md`.
- Revisions v1, v2, v3, v4 unchanged (`source_state_at_v5_start.sha256`, verified ALL-MATCH at build time).
- `Final Version.pdf` unchanged.
- Nothing staged, committed, pushed, released, archived, uploaded, or submitted.

## Deliverables (in `manuscript/plos_ntd_revision_v5_final_scientific_audit/`)
`dengue_ews_plos_ntd_v5.tex`, `references_v5.bib`, `dengue_ews_plos_ntd_v5_internal_review.pdf`, `dengue_ews_plos_ntd_v5_internal_review_grayscale.pdf`, `build_v5.sh`, `page_by_page_audit_v5.md`, `numeric_fidelity_check_v5.md`, `reference_integrity_report_v5.md`, `supporting_information_status_v5.md`, `submission_blockers_v5.md`, `revision_manifest_v5.md`, `source_state_at_v5_start.sha256`, `supporting_information/`. Review copies in `~/Downloads/dengue_v5_final_scientific_audit/`.
