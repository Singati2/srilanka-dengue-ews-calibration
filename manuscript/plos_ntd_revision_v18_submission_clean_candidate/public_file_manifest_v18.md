# Public / internal file manifest — v18

Classification of every v18 file. Categories: PUBLIC MANUSCRIPT · PUBLIC SUPPORTING INFORMATION · PUBLIC REPRODUCIBILITY MATERIAL · INTERNAL REVIEW ONLY · EXCLUDE FROM REPOSITORY · PENDING AUTHOR DECISION.

The submission metadata gate has **failed** (see `submission_metadata_gate_v18.md`); therefore no file is presented as submission-ready, and the "PUBLIC" classifications indicate intended destination *once the gate passes*, not current public release.

**Preservation scope (accurate statement).** The v17 source was preserved and verified 31/31 against `v17_state_at_v18_start.sha256`. Git status showed changes confined to the untracked v18 directory; no earlier revision was intentionally modified. No broader byte-for-byte verification of v1–v16 is claimed, because no matching per-revision ledgers were produced for those revisions. `S1`, `S2`, `S3`, and `S10` remain **PENDING AUTHOR DECISION** and are not classified as PUBLIC SUPPORTING INFORMATION until completed and approved.

## Manuscript source and PDFs (repository root)
| File | Classification | Notes |
|---|---|---|
| `dengue_ews_plos_ntd_v18.tex` | PUBLIC MANUSCRIPT | Cleaned source; internal box switched to gated first-page notice |
| `references_v18.bib` | PUBLIC MANUSCRIPT | Bibliography source |
| `build_v18.sh` | PUBLIC REPRODUCIBILITY MATERIAL | Fail-fast build script |
| `dengue_ews_v18_scientifically_clean_not_submission_ready.pdf` | PENDING AUTHOR DECISION | Scientifically clean; not submission-ready until gate passes |
| `dengue_ews_v18_internal_author_completion.pdf` | INTERNAL REVIEW ONLY | Author-completion copy listing unresolved metadata |

## Supporting Information (supporting_information/)
| File | Classification | Notes |
|---|---|---|
| `S1_STROBE_checklist_v18.md` | PENDING AUTHOR DECISION | STROBE checklist — content incomplete (gate item 19) |
| `S2_S3_TRIPOD_AI_PROBAST_v18.md` | PENDING AUTHOR DECISION | TRIPOD+AI / PROBAST — content incomplete (gate item 19) |
| `S4_analysis_plan_chronology_v18.md` | PUBLIC SUPPORTING INFORMATION | Analysis-plan chronology; M4/M5 designation |
| `S5_country_model_specification_v18.md` | PUBLIC SUPPORTING INFORMATION | Per-country M0–M5 specification |
| `S6_bootstrap_protocol_v18.md` | PUBLIC SUPPORTING INFORMATION | Per-analysis bootstrap protocol |
| `S7_srilanka_sensitivity_grid_v18.md` | PUBLIC SUPPORTING INFORMATION | Sri Lanka linkage/climate-lag/anomaly grid |
| `S8_srilanka_targeted_value_v18.md` | PUBLIC SUPPORTING INFORMATION | Sri Lanka targeted-value regime analysis |
| `S9_colombia_threshold_horizon_v18.md` | PUBLIC SUPPORTING INFORMATION | Colombia threshold/horizon/2022-only |
| `S10_reproducibility_inventory_v18.md` | PENDING AUTHOR DECISION | Reproducibility inventory — partial (gate item 20) |
| `S11_srilanka_wild_cluster_bootstrap_t_v18.md` | PUBLIC SUPPORTING INFORMATION | WCB-t sensitivity table |
| `S11_srilanka_wild_cluster_bootstrap_t_results.csv` | PUBLIC SUPPORTING INFORMATION | Machine-readable full-precision bounds |
| `S12_srilanka_wild_bootstrap_method_v18.md` | PUBLIC SUPPORTING INFORMATION | WCB-t method / single-implementation / reproducibility |

## Reproducibility evidence (repository root)
| File | Classification | Notes |
|---|---|---|
| `colombia_2022_week_eligibility_v18.md` | PUBLIC REPRODUCIBILITY MATERIAL | Origin/target date evidence for the 48-week 2022 subset |
| `targeted_value_seed_resolution_v18.md` | PUBLIC REPRODUCIBILITY MATERIAL | Targeted-value seed evidence (20260612) |
| `hybrid_all_test_seed_evidence_v18.md` | PUBLIC REPRODUCIBILITY MATERIAL | All-test hybrid seed evidence (20260612) |

## Gate / cleanup control documents (repository root)
| File | Classification | Notes |
|---|---|---|
| `submission_metadata_gate_v18.md` | INTERNAL REVIEW ONLY | Metadata gate; do not ship in the public package |
| `ai_disclosure_review_v18.md` | INTERNAL REVIEW ONLY | AI-disclosure review notes |
| `public_file_manifest_v18.md` | INTERNAL REVIEW ONLY | This manifest |
| `page_by_page_visual_qc_v18.md` | INTERNAL REVIEW ONLY | QC record |
| `v17_state_at_v18_start.sha256` | INTERNAL REVIEW ONLY | Preservation ledger |

## internal_review_only/ (kept, not deleted; never in the public package)
| File | Classification | Notes |
|---|---|---|
| `submission_blockers_v17.md` | INTERNAL REVIEW ONLY | Superseded by the v18 metadata gate |
| `sensitivity_review_provenance_v17.md` | INTERNAL REVIEW ONLY | AI-review provenance |
| `authorship_confirmation_v17.md` | INTERNAL REVIEW ONLY | Authorship tracking |
| `supporting_information_status_v17.md` | INTERNAL REVIEW ONLY | SI status tracking |
| `page_count_reconciliation_v17.md` | INTERNAL REVIEW ONLY | QC narrative |
| `final_qc_addendum_v17.md` | INTERNAL REVIEW ONLY | QC narrative |
| `page_by_page_visual_qc_v17.md` | INTERNAL REVIEW ONLY | QC narrative |
| `v16_state_at_v17_start.sha256` | INTERNAL REVIEW ONLY | Preservation ledger |

## EXCLUDE FROM REPOSITORY
- Raw third-party source data (OpenDengue, ERA5-Land, CHIRPS, WorldPop, WER) remain quarantined and are cited upstream, not redistributed.
- LaTeX build artifacts (`*.aux`, `*.log`, `*.out`).
