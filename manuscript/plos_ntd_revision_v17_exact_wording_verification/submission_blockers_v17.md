# Submission blockers — v17 (evidence-reconciled; not invented)

Each of the 16 line-items is assigned **OPEN**, **PARTIALLY VERIFIED**, or **VERIFIED** from preserved evidence. Per the reconciliation rule, a technically verified artifact does **not** imply author approval is verified; evidence completeness and approval status are separated where they differ. Nothing is invented.

**Summary:** OPEN 12 · PARTIALLY VERIFIED 4 · VERIFIED 0. Not submission-ready.

| # | Blocker | Status | Evidence inspected | What is already known | What remains required | Owner | Exact action before submission |
|---|---|---|---|---|---|---|---|
| 1 | Institutional ethics determination | OPEN | Declarations "Ethics" line (tex): "A formal institutional determination is pending author/institutional confirmation." No determination artifact on file. | Study uses aggregate, publicly accessible surveillance data. | An actual IRB/HRPP determination (approval, exemption, or not-human-subjects) with reference ID and date. | Ganesh | Obtain the FAU determination; replace the Ethics line with final wording + reference/date. Do not self-certify. |
| 2 | Funding statement | OPEN | Declarations "Funding": "Pending author confirmation." | — | Confirmed funding sources/grant numbers, or the "no specific funding" statement. | All | Enter the Funding Statement in the submission system; replace the placeholder. |
| 3 | Competing-interest declaration | OPEN | Declarations "Competing interests": "Pending author confirmation." | — | Each author's COI disclosure. | All | Collect and enter the COI statement. |
| 4 | CRediT author contributions | OPEN | Declarations "Author contributions": "Pending author confirmation." No roles assigned. | Three authors listed on the title page. | Per-author CRediT roles reflecting actual contributions. | All | Each author self-assigns CRediT roles; replace placeholder. |
| 5 | Acknowledgments | OPEN | Declarations "Acknowledgments": "Pending author confirmation." | — | Final acknowledgments text (or "none"). | All | Confirm and enter. |
| 6 | All author emails | PARTIALLY VERIFIED | Title page shows corresponding email `ganshiwakoti@gmail.com`; no institutional address; coauthor (Khadka, Thapa) emails absent. `authorship_confirmation_v17.md` records institutional email OPEN. | A reachable corresponding-author email exists. | Institutional corresponding-author email; emails for the two coauthors. | Each | Provide institutional + coauthor emails; update title page/submission system. |
| 7 | All author ORCIDs | OPEN | No ORCID iDs in the tex (only the pending-notice box mentions "ORCIDs"). | Three named authors. | Real ORCID iD for each author (corresponding-author ORCID mandatory). | Each | Register/retrieve real iDs; enter in submission system and title page. Do not guess digits. |
| 8 | Author-order approval | OPEN | `authorship_confirmation_v17.md`: author order documented, "Approves author order" = OPEN for all three. | The intended author order (Shiwakoti, Khadka, Thapa) is documented. | Explicit approval of the order by all three authors. | All | Obtain and record each author's approval of the order. |
| 9 | Final manuscript approval | OPEN | Title page marked "Internal review copy---not for submission"; `authorship_confirmation_v17.md` "Approves manuscript" = OPEN. | A complete internal-review manuscript exists. | All-author approval of the final manuscript. | All | Obtain and record each author's final approval. |
| 10 | Accountability confirmation | OPEN | `authorship_confirmation_v17.md` "Accountability confirmation" = OPEN. | — | ICMJE accountability agreement by each author. | All | Obtain and record. |
| 11 | AI-disclosure approval | PARTIALLY VERIFIED | The "Use of AI assistance" statement is present and truthfully worded in the tex Declarations; `authorship_confirmation_v17.md` "Approves AI disclosure" = OPEN. | The disclosure text is drafted and in the manuscript. | All-author approval of the AI-disclosure wording. | All | Obtain and record author approval of the existing statement. |
| 12 | Repository URL | OPEN | Data-availability line: repository details "pending author confirmation." No public repository URL exists. | Frozen code/derived artifacts are preserved locally under the manuscript/quarantine tree. | A published public repository and its URL. | Ganesh | Publish the frozen repository; record the URL in the DAS. |
| 13 | Code and derived-data licensing | OPEN | Data-availability line: license "pending author confirmation." | — | OSI-approved code license; CC-BY-compatible derived-data terms. | Ganesh | Set licenses; state in the DAS. |
| 14 | Archival DOI | OPEN | Data-availability line: persistent identifier "pending author confirmation." | — | A minted archival DOI (Zenodo/Dryad) for the frozen commit. | Ganesh | Deposit and record the DOI (interim "to be assigned upon acceptance" acceptable). |
| 15 | OpenDengue version-specific citation / access-date resolution | PARTIALLY VERIFIED | Locally analyzed file `Temporal_extract_V1_3.zip` verified (sha256 `7f5df217…`, V1.3); general Figshare DOI `10.6084/m9.figshare.24259573` cited; S10 records no version-specific DOI and no preserved acquisition date. | The analyzed archive is V1.3 (locally verified) and the general record is correctly cited. | A version-specific V1.3 record DOI (if minted) or a recorded access date. | Ganesh | Pin the version-specific DOI or record the access date; keep the general-record DOI labeled general. |
| 16 | Final approval of SI S1–S3 and S10 | PARTIALLY VERIFIED | SI list marks S1–S3 as "draft" and S10 as "partial; author to finalize"; the files exist as standalone drafts. | Draft artifacts for S1 (STROBE), S2/S3 (TRIPOD+AI/PROBAST), and S10 (reproducibility inventory) exist. | Finalization and author approval of these SI items. | All | Finalize S1–S3 and S10; record author approval. |

## Item 15 — OpenDengue version/DOI reconciliation (detail; internal, not in the bibliography)
- Locally analyzed file: `Temporal_extract_V1_3.zip`, sha256 `7f5df2174404313a36596342bb26e4614c3c08577fab75550725e195326bcda6`, 54,872,272 bytes; version V1.3 verified locally.
- Cited general Figshare record DOI: `10.6084/m9.figshare.24259573`.
- Record linkage: the general record and the analyzed archive are not linked through a preserved version-specific record identifier; access date not preserved.
- The manuscript reports the analyzed-file version (V1.3) at the locally verified level only (Methods; S10); the bibliography cites the general Temporal-extract record DOI without asserting it is version-specific to V1.3.

## Status rationale (evidence vs approval)
- No item is **VERIFIED**: every item ultimately requires author/institutional action or approval that is not on file.
- **PARTIALLY VERIFIED** items (6, 11, 15, 16) each have a preserved artifact or partial evidence (a corresponding-author email; a drafted AI-disclosure statement; a locally verified V1.3 file with a cited general DOI; draft S1–S3/S10 files), but author approval and/or completion is outstanding.
- **OPEN** items have no resolving artifact on file.

**Not submission-ready** until the 12 OPEN items are resolved and the 4 PARTIALLY VERIFIED items are completed and approved.
