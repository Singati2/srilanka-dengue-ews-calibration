# Submission blockers — v4 (author-supplied; not invented)

The manuscript body shows only neutral "Pending author confirmation" markers and a running "INTERNAL REVIEW — ADMINISTRATIVE METADATA PENDING" footer. Do not create a submission-ready PDF until these are confirmed.

| Item | Required information | Responsible author | Submission blocking? | Proposed language after confirmation |
|---|---|---|---|---|
| Ethics | Institutional determination (exempt / not human-subjects) or approved wording | Ganesh | Yes | Pending |
| Funding | Funding source/grant numbers, or no-specific-funding confirmation | Both | Yes | Pending |
| Competing interests | Author declarations | Both | Yes | Pending |
| CRediT | Roles for each author | Both | Yes | Pending (draft in `credit_contributions_draft_v4.md`) |
| Acknowledgments | Names/permissions | Both | No/conditional | Pending |
| Bhimsen email | Verified institutional email | Bhimsen | Yes | Pending |
| ORCIDs | Verified ORCIDs (both authors) | Each author | Journal-dependent/likely | Pending |
| Repository / DOI | Public URL, license, archive DOI | Ganesh | Yes (final data statement) | Pending |
| AI disclosure approval | Both authors approve the truthful wording (substance unchanged) | Both | Yes | Current draft retained verbatim |
| OpenDengue access date | Exact download/access date of the V1.3 Temporal extract | Ganesh | No (other provenance stated) | **Not preserved in the current record** — add if recoverable; do not invent |
| Python stack versions | Python, NumPy, pandas, scikit-learn, SciPy, statsmodels | Ganesh | No | "Version not preserved in the current reproducibility record" (S5) |
| Python software citation | a citation for the Python environment used to fit the models | Ganesh | No | Pending (no Python citation in the bib) |
| Colombia per-model calibration | per-model observed prevalence + mean predicted probability | Ganesh | No | Not retained in the committed record (only CITL/slope/Brier are committed) |
| SI checklists | Completed STROBE / TRIPOD+AI / PROBAST (currently drafts) | Both | Yes | Finalize before submission |

**AI-disclosure:** truthful disclosure retained verbatim in Declarations; final author approval pending (tracked here, not as a body instruction). Source evidence for all v4 numeric/citation facts: `v4_verified_evidence_ledger.md`.
