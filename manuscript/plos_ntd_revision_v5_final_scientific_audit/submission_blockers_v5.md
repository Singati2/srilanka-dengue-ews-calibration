# Submission blockers — v5 (author-supplied; not invented)

The manuscript body shows only neutral "Pending author confirmation" markers and a single internal-review notice on the title page. Do not create a submission-ready PDF until these are resolved. Nothing here is invented.

| Item | Required information | Responsible | Submission-blocking? | Status / proposed action |
|---|---|---|---|---|
| Ethics | Institutional determination (exempt / not-human-subjects) or approved wording | Ganesh | Yes | Pending |
| Funding | Source/grant numbers, or no-specific-funding statement | Both | Yes | Pending |
| Competing interests | Author declarations | Both | Yes | Pending |
| CRediT contributions | Roles per author | Both | Yes | Pending |
| Acknowledgments | Names/permissions | Both | No/conditional | Pending |
| Second-author email | Verified institutional email (Bhimsen Khadka) | Bhimsen | Yes | Pending (not placed in PDF) |
| ORCIDs | Both authors | Each | Journal-dependent | Pending (not placed in PDF) |
| Data/code repository | Public URL + license + archival (Zenodo) DOI | Ganesh | Yes (data statement) | Pending |
| **OpenDengue V1.3 identifier** | Version-specific figshare DOI + access date for the V1.3 Temporal extract | Ganesh | Yes (citation) | The record DOI `10.6084/m9.figshare.24259573` was verified (`reference_audit_v1.md` line 46) to resolve to **V1.2**. The manuscript text and reference state V1.3 (the version used). Do **not** assert V1.3 against the record DOI; pin the version-specific DOI + access date before submission. (Editorial note removed from the bibliography per PLOS style.) |
| **Python software citation** | A citation for the Python modeling environment + key libraries | Ganesh | No (recommended) | No verified Python/library versions are in the committed record (S5: "not preserved"), so no Python software citation was added. Add one (with versions) before submission; do not invent versions. |
| Python stack versions | Python, NumPy, pandas, scikit-learn, SciPy, statsmodels | Ganesh | No | "Not preserved in the current reproducibility record" (S5 Table). R 4.6.0 / dlnm 2.4.10 / mgcv 1.9.4 / tsModel 0.6-2 **are** verified (`canonical_R_dlnm_report.md`). |
| EWARS-csd full author list | (Resolved) | — | No | Verified and corrected in v5: Schlesinger M, Prieto Alvarado FE, Borbón Ramos ME, Sewe MO, Merle CS, Kroeger A, Hussain-Alkhateeb L (source: Front Public Health 2024;12:1323618, publisher page). |
| HDX COD-AB / WER access details | Record URL/version/access dates | Ganesh | No | Author-to-add; not invented |
| Colombia per-model mean predicted probability | Per-model mean predicted probability | Ganesh | No | Not retained in the committed record (only CITL/slope/Brier and the shared observed prevalence 0.375 are committed) |
| SI checklists | Completed STROBE / TRIPOD+AI / PROBAST (currently drafts) | Both | Yes | Finalize before submission |
| SI tables S7–S10 | Standalone files (values exist in frozen reports) | Both | No | Compile from frozen reports before submission; not provided with the review copy |
| AI-use disclosure | Both authors approve the truthful wording | Both | Yes | Current truthful disclosure retained verbatim; final approval pending |
| Line numbers / spacing | (Resolved for review) | — | — | Continuous line numbers + double spacing are enabled in v5. |

**Do not call v5 submission-ready until all mandatory (Yes) items are resolved.** v5 is an internal-review copy.
