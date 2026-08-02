# PLOS NTD Revision v2 — Governance Manifest

> **Provenance (required language).** This LaTeX manuscript source was reconstructed from the June 26, 2026 manuscript PDF and user-supplied manuscript text. It is not the original authoring source. Revision v2 was derived from the preserved working state of revision v1 after an interrupted editing session. Revision v1 was modified during that interrupted session; its current state is preserved without further modification (checksum ledger `v1_state_at_v2_start.sha256`), and all subsequent corrections are made only in `manuscript/plos_ntd_revision_v2/`. `Final Version.pdf` remains the unchanged historical tracked manuscript.

**v2 created:** 2026-06-27 (from v1 source copies; build artifacts excluded). **Original v1 created:** 2026-06-26
**Repository:** ~/srilanka-dengue-ews-calibration
**Base commit (HEAD at revision start):** `a32afd73897eeb1f5574747180535e3289813370` (`a32afd7`), `main` == `origin/main`.
**Original manuscript (historical input, MUST remain unchanged):** `Final Version.pdf`, SHA256 `e20f0daca0980881e6287911169b5196abab956501db14ca34324630234dc256`.

**Source provenance (required language):** This LaTeX source was reconstructed from the June 26, 2026 manuscript PDF and user-supplied manuscript text. It is not the original authoring source. `Final Version.pdf` is the tracked manuscript of record; `manuscript/dengue_ews_manuscript.tex` (repo root) is the earlier untracked reconstructed source and is not overwritten by this revision.

**Created in this revision (untracked, uncommitted):** `dengue_ews_plos_ntd_v1.tex`, `references.bib`, `build.sh`, `revision_manifest_v1.md`, `source_checksums_v1.txt`, `AUTHOR_METADATA_TODO.md`, `cover_letter_v1.md`, `data_and_code_availability_v1.md`, `credit_contributions_draft_v1.md`, `ai_use_disclosure_and_log_v1.md`, `ethics_funding_competing_interests_placeholders_v1.md`, `visual_style_guide_v1.md`, `figure_plan_v1.md`, `claim_source_crosswalk_v1.md`, `supporting_information/{SI_outline,STROBE_checklist_draft,PROBAST_TRIPOD_internal_assessment}_v1.md`; plus `docs/zenodo_release_plan_v1.md` and addendum corrections to the four audit docs.
**Checksum ledger:** `source_checksums_v1.txt` (original PDF + all `docs/*.md` + all `scripts/*.py`, 90 files).
**Background model processes at start:** none (only OS daemons `networkd-dispatcher`, `unattended-upgrades`).

## Governance attestations
- No metric recomputed; no model run; no frozen result altered.
- No missing value invented — administrative metadata uses explicit `[TO CONFIRM: …]` placeholders.
- No mathematical biomodel added (excluded per gate; see `docs/mathematical_biomodel_feasibility_memo_v1.md`).
- COVID-period sensitivity NOT implemented (not separately approved; retained only as a Discussion limitation).
- Original PDF and all prior reports untouched; this revision is isolated under `manuscript/plos_ntd_revision_v1/`.
- Nothing staged, committed, pushed, or uploaded.

## Source reports used (frozen evidence)
Numbers in the revision were taken **only** from these committed artifacts (verified 200/0 in the prior fidelity audit and re-mapped in `docs/claim_to_evidence_matrix_v1.md`):
- Sri Lanka primary / DCA: `docs/pilot_h4_75pct_calibration_dca_report.md`, `docs/decision_threshold_dnb_robustness_report.md`
- Sensitivity: `docs/pilot_h4_75pct_sensitivity_report.md`, `docs/wer_2021_calendar_anomaly_decision_memo.md`
- Recalibration: `docs/rolling_recalibration_extension_report.md`
- DLNM / hybrid: `docs/dlnm_climate_comparator_report.md`, `docs/canonical_R_dlnm_report.md`, `docs/hybrid_model_extension_report.md`
- Targeted value / horizon / label: `docs/targeted_value_climate_stage1a_h4_report.md`, `docs/label_horizon_robustness_report.md`
- Colombia: `docs/colombia_model_ladder_report.md`, `docs/colombia_horizon_sensitivity_report.md`, `docs/colombia_outbreak_threshold_sensitivity_report.md`
- Build/QC: `docs/analysis_table_linkage_v2_date_aligned_report.md`, `docs/rdhs_geometry_build_report.md`, `docs/rdhs_adjacency_graph_build_report.md`, `docs/worldpop_population_denominator_build_report.md`, `docs/population_denominator_rescaled_build_report.md`
- Generators: `scripts/colombia_outbreak_threshold_sensitivity_v1.py`, `scripts/colombia_model_ladder_h4_75pct_v1.py`, `scripts/decision_threshold_dnb_robustness_v1.py`, `scripts/colombia_horizon_sensitivity_v1.py`, and lag/label assembly scripts.
- Audits: `docs/manuscript_peer_review_v1.md`, `docs/plos_ntd_submission_requirements_audit_v1.md`, `docs/reference_audit_v1.md`, `docs/claim_to_evidence_matrix_v1.md`, `docs/mathematical_biomodel_feasibility_memo_v1.md`

## Decisions ledger (from the gate instruction)
| Decision | Setting |
|---|---|
| Source format | LaTeX |
| Authorship | Ganesh Shiwakoti and Bhimsen Khadka (unchanged) |
| Framing | surveillance-benchmarked evaluation as protagonist; modest, setting-dependent, horizon-flat hybrid |
| "registered" | → "prespecified" / "primary reference threshold" (no registration DOI confirmed) |
| ΔNB translation | ≈1.9 net true-positive equivalents per 100 OR (equivalently, not additionally) ≈4.4 fewer false-alert equivalents per 100 (2.7–6.1) — alternative rescalings of the same +0.0188, not observed outcomes |
| Colombia | external framework replication (not external model validation) |
| Two-setting difference | NOT formally shown to differ; no heterogeneity test designed/performed |
| Biomodel | excluded (Paper-2 / reviewer-contingent) |
| COVID sensitivity | NOT run this step; Discussion limitation only |
| Reference style | Vancouver numbered |
| Palette | colorblind-safe (Okabe–Ito), grayscale-legible |
| Commit/push | NO |

## Unresolved (placeholders carried into the draft — gate Q3–Q14)
Affiliations, emails, corresponding author; ORCIDs; CRediT contributions; funding/grants; competing interests; ethics/IRB status; acknowledgments; OSF/registration DOI; Zenodo license; data-redistribution rights per source; exact AI tools/uses to confirm for the disclosure.
