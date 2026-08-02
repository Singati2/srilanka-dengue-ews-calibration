# Submission blockers — v13 (carried forward from v12; not invented)

v13 is an integrity cleanup; it resolved no administrative blocker and invented no metadata. The title page remains "Internal review copy—not for submission."

## Placeholders vs blockers
- Literal LaTeX placeholder tokens in the source: 0 (no `TODO`/`FIXME`/`XXX`/`[TO CONFIRM]`/`<<>>`).
- Unresolved submission blockers (metadata/approvals): 14 categories, all OPEN.

| # | Blocker | Status | Owner |
|---|---|---|---|
| 1 | Ethics determination (IRB/exempt/not-human-subjects + reference) | OPEN | Ganesh |
| 2 | Funding statement | OPEN | All |
| 3 | Competing interests | OPEN | All |
| 4 | CRediT author contributions (per author) | OPEN | All |
| 5 | Acknowledgments | OPEN | All |
| 6 | Coauthor emails — Ganesh (institutional vs gmail), Bhimsen, Ajay | OPEN | Each |
| 7 | ORCIDs — all three authors | OPEN | Each |
| 8 | Author-order and manuscript approval, accountability | OPEN | All |
| 9 | Public repository URL | OPEN | Ganesh |
| 10 | Code/data license | OPEN | Ganesh |
| 11 | Archival DOI (e.g., Zenodo) | OPEN | Ganesh |
| 12 | OpenDengue version/DOI reconciliation (see below) | OPEN | Ganesh |
| 13 | AI-disclosure approval (truthful wording retained; all authors to approve) | OPEN | All |
| 14 | Final approval of SI S1–S3 (STROBE/TRIPOD+AI/PROBAST) and S10 (reproducibility inventory) | OPEN — drafts | All |

## Blocker 12 — OpenDengue version/DOI reconciliation (kept here, not in the bibliography)
- **Locally analyzed Colombia file version:** OpenDengue **Temporal extract V1.3** — verified locally: `Temporal_extract_V1_3.zip`, sha256 `7f5df2174404313a36596342bb26e4614c3c08577fab75550725e195326bcda6`, 54,872,272 bytes (acquisition spec `colombia_external_replication_build_spec.md`).
- **Figshare record DOI cited:** `10.6084/m9.figshare.24259573`. Prior reference audit found this DOI resolves to an OpenDengue **V1.2** record; it is not a version-specific V1.3 DOI.
- **Record-version identifier:** a version-specific figshare DOI for V1.3 is not pinned.
- **Acquisition date:** not documented in the committed acquisition spec (file was already downloaded read-only); to be recorded by the author.
- **Action:** pin the version-specific DOI (or an access date) for the analyzed V1.3 extract; do not assert in the bibliography that the cited DOI is specifically V1.3. The manuscript body reports the analyzed-file version (V1.3) at the acquisition-verified level only.

## v13 integrity-cleanup notes (not blockers)
- Corrected M4/M5 estimand wording; corrected Colombia 48-week explanation (origin vs target dates); removed Colombia M4 from the main text (retained in S9); removed zero-crossing verdict language; corrected Table 6 title; resolved the targeted-value seed (20260612).
- New evidence files: `colombia_2022_week_eligibility_v13.md`, `targeted_value_seed_resolution_v13.md`.

**Not submission-ready** until all 14 blockers are resolved.
