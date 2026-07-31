# Submission metadata gate — v18

Evidence-based gate for a clean submission package. Status is one of VERIFIED / PARTIALLY VERIFIED / OPEN, assigned only from inspected evidence. A stated artifact does not imply author approval. **Nothing is invented** (no emails, ORCIDs, grant/ethics numbers, licenses, dates, URLs, or approvals).

## GATE RESULT: **FAILED** (mandatory items OPEN)
Summary: VERIFIED 1 · PARTIALLY VERIFIED 4 · OPEN 15 (20 items). Because mandatory items remain OPEN, **no submission-ready PDF is produced**; the scientifically-cleaned, not-submission-ready PDF is produced instead. (Item 1, corresponding-author email, moved PARTIALLY VERIFIED → VERIFIED: a reachable corresponding-author email exists on the title page; the qualifications below are author-choice items, not mandatory blockers.)

| # | Item | Status | Evidence inspected | Information available | Information missing | Responsible | Required action |
|---|---|---|---|---|---|---|---|
| 1 | Corresponding-author email | VERIFIED | Title page: `ganshiwakoti@gmail.com` | A reachable corresponding-author email is present on the title page | None mandatory (author-choice items in note below) | Ganesh | Confirm this is the address he wants published (see note) |
| 2 | All coauthor emails | OPEN | Title page shows no emails for Khadka or Thapa | — | Emails for Bhimsen Khadka and Ajay Kumar Thapa | Each | Provide coauthor emails |
| 3 | All author affiliations | PARTIALLY VERIFIED | Title page: FAU (Math & Statistics); UT Dallas (Mathematical Sciences); FAU (Civil, Environmental and Geomatics Engineering) | Three specific affiliations stated | Author confirmation of exact departmental wording | Each | Confirm affiliations |
| 4 | ORCIDs | OPEN | No ORCID iDs present in the source | — | Real ORCID iD for each author | Each | Register/retrieve real iDs; do not guess digits |
| 5 | Author order | PARTIALLY VERIFIED | Title page order: Shiwakoti, Khadka, Thapa | Intended order documented | Explicit all-author approval of order | All | Record approval of the order |
| 6 | CRediT contributions | OPEN | Declarations: "Pending author confirmation"; no roles assigned | — | Per-author CRediT roles (scaffold below) | All | Each author self-assigns roles |
| 7 | Manuscript approval | OPEN | Title page marked not-for-submission; no approval record | — | All-author approval of final manuscript | All | Record approval |
| 8 | Accountability confirmation | OPEN | No ICMJE accountability record | — | Accountability agreement by each author | All | Record confirmation |
| 9 | Ethics determination | OPEN | Declarations: "A formal institutional determination is pending"; no determination artifact | Study uses aggregate public data | A real IRB/HRPP determination (approval/exemption/not-human-subjects) + reference ID and date | Ganesh | Obtain FAU determination; transcribe exactly. Do NOT self-certify |
| 10 | Funding | OPEN | Declarations: "Pending author confirmation" | — | Confirmed funding sources/grant numbers or the "no specific funding" statement | All | Confirm and enter |
| 11 | Competing interests | OPEN | Declarations: "Pending author confirmation" | — | Each author's COI disclosure | All | Collect and enter. Do not assume "none" |
| 12 | Acknowledgments | OPEN | Declarations: "Pending author confirmation" | — | Confirmed acknowledgments (or "none") | All | Confirm and enter |
| 13 | Repository URL | OPEN | Data-availability: repository "pending"; no public URL exists | Frozen artifacts preserved locally | A published public repository and its URL | Ganesh | Publish repository; record URL. Do not claim public availability until public |
| 14 | Code license | OPEN | Data-availability: license "pending" | — | OSI-approved code license | Ganesh | Set and state license |
| 15 | Derived-data license / terms | OPEN | Data-availability: license "pending" | — | CC-BY-compatible derived-data terms | Ganesh | Set and state terms |
| 16 | Archival DOI (or accepted interim wording) | OPEN | Data-availability: persistent identifier "pending" | — | A minted archival DOI, or agreed interim "to be assigned upon acceptance" | Ganesh | Deposit and record, or approve interim wording |
| 17 | OpenDengue citation and access-date | PARTIALLY VERIFIED | Methods/DAS: analyzed file V1.3 verified locally (`Temporal_extract_V1_3.zip`, sha256 `7f5df217…`); general Figshare DOI `10.6084/m9.figshare.24259573` cited | Analyzed file version + general record DOI | Version-specific V1.3 record DOI (if minted) or a recorded access date | Ganesh | Pin version-specific DOI or record access date; do not assert the general DOI is specifically V1.3 |
| 18 | AI-disclosure approval | PARTIALLY VERIFIED | "Use of AI assistance" statement present and refined (see `ai_disclosure_review_v18.md`) | Disclosure text drafted and in the manuscript | All-author approval + journal AI-policy check | All | Approve wording; verify journal policy before submission |
| 19 | SI S1–S3 author completion | OPEN | S1 (STROBE locators), S2/S3 (TRIPOD+AI/PROBAST judgments) are incomplete works-in-progress | Draft scaffolds exist | Completion + author sign-off | All | Complete and approve |
| 20 | SI S10 author completion | OPEN | S10 reproducibility inventory is partial | Partial inventory exists | Completion of the checksum manifest | Ganesh | Complete and approve |

### Note on item 1 (corresponding-author email)
- The existence of a reachable corresponding-author email is **VERIFIED**: `ganshiwakoti@gmail.com` appears on the title page.
- **Ganesh must confirm** that this is the address he wants published.
- An institutional address may be substituted by author choice or where a documented journal requirement applies.
- The absence of an institutional address is **not itself a mandatory blocker** without evidence of such a requirement. No other email address is invented here.

## CRediT contributions scaffold (roles OPEN — authors to assign; not invented)
| CRediT role | Ganesh Shiwakoti | Bhimsen Khadka | Ajay Kumar Thapa |
|---|---|---|---|
| Conceptualization | OPEN | OPEN | OPEN |
| Methodology | OPEN | OPEN | OPEN |
| Software | OPEN | OPEN | OPEN |
| Formal analysis | OPEN | OPEN | OPEN |
| Data curation | OPEN | OPEN | OPEN |
| Writing – original draft | OPEN | OPEN | OPEN |
| Writing – review & editing | OPEN | OPEN | OPEN |
| Visualization | OPEN | OPEN | OPEN |
| Supervision | OPEN | OPEN | OPEN |
| Project administration | OPEN | OPEN | OPEN |

## Consequence
Mandatory items 2, 4, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16, 19, 20 are OPEN. The gate therefore **fails**; only `dengue_ews_v18_scientifically_clean_not_submission_ready.pdf` and `dengue_ews_v18_internal_author_completion.pdf` are produced. No file is labeled "submission-ready".
