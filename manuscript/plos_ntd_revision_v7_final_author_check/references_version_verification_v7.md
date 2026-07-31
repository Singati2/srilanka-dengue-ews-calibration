# References & software-version verification — v7 (§20)

## OpenDengue release (analyzed version)
- **Verified V1.3** from local acquisition records, NOT from the website: `~/data_quarantine/opendengue_extract_inspection_v1/Temporal_extract_V1_3.zip`; sha256 `7f5df21…` (`docs/reference_audit_v1.md:46`, `docs/colombia_chirps_full_precipitation_report.md:7`).
- Record DOI `10.6084/m9.figshare.24259573` resolves to **V1.2**; the version-specific V1.3 DOI is not verified → author-to-confirm (blocker). Bibliography cites the dataset cleanly; version stated in Methods/Data Availability, not as a bibliography warning.

## R / packages
- **Verified** from `docs/canonical_R_dlnm_report.md` (recorded `sessionInfo`, sha256 `e5f28716…`): R 4.6.0 (2026-04-24); dlnm 2.4.10; mgcv 1.9.4; tsModel 0.6-2.

## Python stack
- **Not preserved** in the reproducibility record (no environment/requirements file committed). Stated as such in S5; do not guess. A Python software citation is an author item.

## Style
- Vancouver (inline numbered, surname+initials, first-six-et-al, NLM abbreviations). 35 entries; EWARS-csd authors corrected (Schlesinger M et al.).
