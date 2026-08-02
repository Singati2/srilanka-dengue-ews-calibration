# Submission blockers — v6 (author-supplied; not invented)

The v6 manuscript shows only neutral "Pending author confirmation" markers and a single title-page internal-review notice. Nothing below is invented. Do not produce a submission-ready PDF until the mandatory (Yes) items are resolved.

| Item | Required information | Responsible | Blocking? | Status / proposed action |
|---|---|---|---|---|
| Ethics | Institutional determination or approved wording | Ganesh | Yes | Pending |
| Funding | Source/grant numbers or no-specific-funding statement | Both | Yes | Pending |
| Competing interests | Declarations | Both | Yes | Pending |
| CRediT | Roles per author | Both | Yes | Pending |
| Acknowledgments | Names/permissions | Both | No/conditional | Pending |
| Second-author email | Verified institutional email (Bhimsen Khadka) | Bhimsen | Yes | Pending (not in PDF) |
| ORCIDs | Both authors | Each | Journal-dependent | Pending (not in PDF) |
| **OpenDengue V1.3 version-specific DOI (M-6)** | The figshare **version-specific** DOI for the V1.3 Temporal extract, plus access date | Ganesh | Yes (citation) | **Analyzed version verified as V1.3** from local acquisition records (`~/data_quarantine/opendengue_extract_inspection_v1/Temporal_extract_V1_3.zip`; sha256 `7f5df21…`; `reference_audit_v1.md:46`). The record DOI `10.6084/m9.figshare.24259573` resolves to **V1.2**. The bibliography cites the dataset cleanly without asserting the version-specific DOI; pin the V1.3 DOI + access date before submission. State the version in Data Availability. |
| **Repository / archive (M-7)** | Public repository URL, release scope, license, archival platform, and persistent identifier | Ganesh | Yes (data statement) | **Require author confirmation.** No platform, timing, DOI, or license is promised in the manuscript. See `archive_plan_v6.md`. Do not create or publish a Zenodo record. |
| Python software citation / stack versions | Python + key library versions; a Python software citation | Ganesh | No | "Not preserved in the reproducibility record" (S5). R 4.6.0 / dlnm 2.4.10 / mgcv 1.9.4 / tsModel 0.6-2 are verified. |
| Colombia per-model mean predicted probability | Per-model mean predicted probability | Ganesh | No | Not retained; observed prevalence 0.375 (shared common-complete set) is known. |
| Completed SI checklists | Final STROBE / TRIPOD+AI / PROBAST (currently drafts) | Both | Yes | Finalize before submission; record "no graphical calibration curve generated" in TRIPOD+AI. |
| SI tables S7–S10 | Standalone files (values exist in frozen reports) | Both | No | Not provided with the review copy; compile before submission. |
| AI-use disclosure | Author approval of the truthful wording | Both | Yes | Retained verbatim; final approval pending. The internal AI role-panel exercise must not be described as expert validation (see `ai_role_panel_provenance_v6.md`). |
| WER / HDX COD-AB access details | Record URL/version/access dates | Ganesh | No | Author-to-add; not invented. |

**Data Availability (version note for M-6):** The Colombia arm used the OpenDengue Temporal extract **version 1.3** (verified locally; record DOI `10.6084/m9.figshare.24259573` corresponds to an earlier version, V1.2); the version-specific persistent identifier for V1.3 is to be confirmed by the author. This note belongs in Data Availability/blocker records, **not** inside a bibliography entry.
