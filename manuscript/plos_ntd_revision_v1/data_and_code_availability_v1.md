# Data and Code Availability — DRAFT (author confirmation required)

> Do **not** state that data are publicly available from the repository unless they actually are. The repository contains no committed heavy data; source datasets are third-party and conservatively cited/fetched, not redistributed.

## Data Availability Statement (draft)
This study used publicly accessible third-party source datasets and locally derived analytic tables.

- **Dengue surveillance.** Sri Lanka: Weekly Epidemiological Report, Epidemiology Unit, Ministry of Health, Sri Lanka (cited; official archive). Colombia: dengue case counts obtained from OpenDengue (Temporal extract, V1.3; cited), whose upstream source is national surveillance (SIVIGILA/INS). [AUTHOR CONFIRMATION REQUIRED: confirm OpenDengue redistribution terms before sharing any source files.]
- **Climate.** ERA5-Land (Copernicus Climate Data Store) and CHIRPS (Climate Hazards Center, UC Santa Barbara) — cited; acquisition scripts/instructions provided; downloaded NetCDF/raster files are **not** redistributed.
- **Population.** WorldPop (R2025A, 100 m) — cited; acquisition instructions provided; raw rasters **not** redistributed.
- **Boundaries.** Sri Lanka administrative boundaries (HDX COD-AB) — cited.
- **Derived analytic tables.** A derived-table inventory is prepared; release is pending provenance, licensing, and disclosure-risk review (see `docs/zenodo_release_plan_v1.md`). [AUTHOR CONFIRMATION REQUIRED: which derived tables may be released.]

Acquisition/fetch scripts and provenance documentation are in the project repository. Persistent identifiers (Zenodo DOI) are **not yet created**; placeholder language: "Code and derived artifacts will be archived at Zenodo (DOI to be assigned) upon acceptance."

## Code and Software Availability (draft)
Analysis code (data linkage, the M0–M5 ladder, recalibration, decision-curve analysis, and bootstrap) is maintained in the project repository and will be archived with a persistent identifier and an open license (see Zenodo plan). [AUTHOR CONFIRMATION REQUIRED: public repository URL; license; exact software/package versions, e.g. Python scikit-learn/statsmodels, R and the `dlnm` package.] No author-generated code that underpins the findings is withheld.
