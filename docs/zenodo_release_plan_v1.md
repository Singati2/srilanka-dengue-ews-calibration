# Zenodo archival plan v1 (PLAN ONLY — no record created, no DOI reserved)

> Prepared per author decision. **No Zenodo record, release, tag, or DOI is created or reserved.** Repository license is inspected, not changed.

## Repository license (inspected)
- The repository contains a `LICENSE` file (tracked). **[AUTHOR CONFIRMATION REQUIRED: confirm the exact license text/type before archiving; do not change it without approval.]** The proposed Zenodo license should match the existing repository license unless the authors decide otherwise.

## Proposed archived files
- Analysis/generator scripts (`scripts/*.py`), linkage and feature-assembly code, the M0–M5 ladder, recalibration, DCA, and bootstrap code.
- Frozen analysis reports (`docs/*_report.md`), specs, and QC summaries.
- Manuscript revision source (`manuscript/plos_ntd_revision_v1/*.tex`, `references.bib`, `build.sh`) and figure sources.
- Reproducibility artifact inventory and checksums (`source_checksums_v1.txt`).

## Files to EXCLUDE
- Any third-party raw data under quarantine (OpenDengue source files, CHIRPS rasters, ERA5-Land NetCDF, WorldPop rasters, WER source PDFs) — **not redistributed** pending license verification.
- Derived analytic tables — excluded until provenance, licensing, and disclosure-risk review (separate decision).

## Data-redistribution limitations
- OpenDengue, CHIRPS, ERA5-Land, WorldPop, WER: **cite + provide fetch/acquisition instructions only**; do not redistribute source files until terms are verified.

## Repository version / tag proposal
- Propose tagging the post-acceptance commit (e.g., `v1.0-plosntds`) and archiving that tag. **[AUTHOR CONFIRMATION REQUIRED] — not created.**

## Metadata required
- Title, authors + ORCIDs (still needed — see `AUTHOR_METADATA_TODO.md`), affiliations, description, keywords, license, related-identifier (manuscript DOI once assigned), funding.

## Authors / ORCIDs still needed
- Ganesh Shiwakoti ORCID `[AUTHOR CONFIRMATION REQUIRED]`; Bhimsen Khadka ORCID `[AUTHOR CONFIRMATION REQUIRED]`.

## Placeholder DOI language (for the manuscript)
- "Code and derived artifacts will be archived at Zenodo (DOI to be assigned) upon acceptance." Do not publish or reserve a DOI until approved.
