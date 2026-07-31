# Reference integrity report — v4 (§19)

Verified via primary sources in the grounded evidence pass (`v4_verified_evidence_ledger.md`, Q6–Q7) and the prior `docs/reference_audit_v1.md`. Build: 35 entries, 0 undefined citations, 0 `[?]`, populated numbered list.

| Key | Verified authors/venue/year | DOI / identifier | Correction in v4 | Source |
|---|---|---|---|---|
| Clarke2024OpenDengue | Clarke J, Lim A, Gupte P, Pigott DM, van Panhuis WG, Brady OJ — *Scientific Data* 11:296, 2024 | 10.1038/s41597-024-03120-7 | none | Crossref/publisher |
| OpenDengue2024 (dataset) | OpenDengue database, Temporal extract V1.3 | 10.6084/m9.figshare.24259573 | **year 2024 → 2025; title clarified** | figshare |
| WorldPop2025 / Tatem2017 | WorldPop R2025A; Tatem AJ *Sci Data* 4:170004 (2017) | 10.1038/sdata.2017.4 | none | publisher |
| SriLankaCensus2025 | Dept. of Census & Statistics, Sri Lanka — 2024 census; district totals released 30 Oct 2025 | n/a | year 2025 retained (release year), confirmed | official release |
| ERA5LandCDS / MunozSabater2021 | Copernicus CDS ERA5-Land; Muñoz-Sabater et al. *ESSD* 13:4349 (2021) | 10.24381/cds.e2161bac; 10.5194/essd-13-4349-2021 | none | CDS / publisher |
| Funk2015 / CHIRPS | Funk et al. *Scientific Data* 2:150066 (2015) | 10.1038/sdata.2015.66 | none | publisher |
| HDXCODABSriLanka | HDX / OCHA / Survey Dept of Sri Lanka COD-AB | n/a (URL/access date author-to-add) | none | HDX |
| SriLankaWER | Epidemiology Unit, MoH Sri Lanka, WER | n/a (access URL/date author-to-add) | none | official archive |
| **RCoreTeam2026** (was RCoreTeam2024) | R Core Team, R 4.6.0 | n/a | **DEFECT FIXED: year 2024 → 2026 (R 4.6.0, released 2026-04-24); key renamed; cited only for R, not for Python** | recorded version |

## Defects identified and fixed in v4
1. **R citation year/version mismatch:** the R Core Team reference was dated 2024 but the analysis used R 4.6.0 (2026-04-24). Corrected to 2026 and "(version 4.6.0)".
2. **Software citation misuse:** the Methods previously read "Analyses used Python and R [R citation]", citing R for Python. Corrected: the penalized logistic models were fit in Python (version not recorded — author item); the canonical DLNM comparator in R 4.6.0 with `dlnm`. No Python software citation exists in the bib (author item).
3. **OpenDengue dataset entry:** year 2024 → 2025; title clarified.

## Author-to-confirm (grey-literature/dataset access details, not invented)
WER access URL + date range; HDX COD-AB record URL/version/access date; OpenDengue exact download date; SriLankaCensus2025 exact title/URL; a Python software citation.

**Style:** numbered Vancouver-compatible (`unsrtnat`, order of appearance). PLOS NTD reference guidance (numbered Vancouver) confirmed from official PLOS pages in the evidence pass.
