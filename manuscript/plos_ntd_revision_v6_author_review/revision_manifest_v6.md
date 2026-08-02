# PLOS NTD Revision v6 (author review) — Governance Manifest

> **Provenance.** v6 was created from the frozen v5 source (`plos_ntd_revision_v5_final_scientific_audit/dengue_ews_plos_ntd_v5.tex`) after adjudicating an **internal AI-assisted role-based review** (not external peer review; see `ai_role_panel_provenance_v6.md`). The v5 reviewer-critique memo was modified after v5 was described as preserved; this is documented honestly in `v5_state_after_expert_memo_update.sha256`. No further v5 file was modified after that ledger. All v6 work is isolated in this directory.

> **Analysis freeze maintained (Step 6).** No model, calibration measure, bootstrap, confidence interval, threshold/sensitivity/horizon/heterogeneity analysis, or biomodel was run or recomputed. The following remain **reviewer-contingent or Paper-2 work and were NOT implemented and are NOT claimed as completed or required for this revision**: reporting-delay simulation; rolling-origin validation; COVID/pandemic exclusion; harmonized climate modeling; spatial-block validation; formal heterogeneity testing; new calibration curves; new bootstrap procedures; stakeholder threshold elicitation.

## Writing changes integrated into v6 (approved only)
1. Graphical-calibration disclosure (M-1) — Methods: curves not generated in the frozen analysis.
2. Careful Colombia slope interpretation (M-2) — safe range wording; no per-model dispersion labels; no "Platt does not correct slope."
3. Non-stakeholder-derived threshold clarification (M-3) — stakeholder clause only.
4. Revised reporting-delay limitation (M-4) — predictor+outcome framing; rejected the near-real-time climate claim; climate latency not evaluated.
5. OpenDengue verification/blocker handling (M-6) — version verified V1.3 locally; bibliography clean; version-specific DOI in blocker/Data Availability.
6. Neutral finite-cluster bootstrap wording (M-8).
7. Cross-setting consistency review (M-9) — verified; no change needed.
8. AI-role-panel provenance correction (internal documentation).
- Plus Step-8 fixes: continuous line numbers re-enabled (double-spaced review copy); "steelman" terminology removed; Figure 3 Panel A anchored at the AUC no-skill baseline (0.5); Colombia secondary climate-only result de-duplicated.

## Rejected / deferred
- Rejected: Sri Lanka operational translation (M-5); unconditional Zenodo promise (M-7).
- Deferred to author: OpenDengue V1.3 version-specific DOI (M-6); repository/archive choices (M-7, see `archive_plan_v6.md`).

## Governance attestations
- No frozen result changed; no analysis rerun; no new calibration curve generated.
- Revisions v1–v4 unchanged; no additional v5 file modified after the new checksum ledger.
- No administrative value invented; placeholders neutral and tracked in `submission_blockers_v6.md`.
- Nothing staged, committed, pushed, released, archived, uploaded, or submitted.

## Deliverables (this directory)
`dengue_ews_plos_ntd_v6.tex`, `references_v6.bib`, `build_v6.sh`, internal-review + grayscale PDFs, `v5_state_after_expert_memo_update.sha256`, `ai_role_panel_provenance_v6.md`, `expert_memo_adjudication_v6.md`, `submission_blockers_v6.md`, `archive_plan_v6.md`, `revision_manifest_v6.md`, `supporting_information/`.
