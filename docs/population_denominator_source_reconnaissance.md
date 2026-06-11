# Population-Denominator Source Reconnaissance (Geomatics WP1)
*Reconnaissance only — web metadata inspection; **no population rasters or tables downloaded**. No climate data, no outcome↔exposure linkage, no models, preregistration untouched, frozen outcome dataset unchanged. No raster tooling installed.*

**Date:** 2026-06-11
**Goal:** identify the safest source + workflow for **annual population denominators** for the 26 RDHS polygons (`rdhs_26_v1.gpkg`), 2018–2025.
**Companion inventory:** `geomatics_templates/population_denominator_inventory_template.csv`

## Candidate sources (summary)
| Source | Resolution | Years (2018–2025) | License | RDHS zonal sum | Kalmunai split | Role |
|---|---|---|---|---|---|---|
| **WorldPop Individual-countries** (unconstrained, UN-adj) | 100m, EPSG:4326 | **2018–2020** | CC BY 4.0 | ✅ | ✅ | primary (2018–2020) |
| **WorldPop Global 2015–2030** (annual) | 100m, EPSG:4326 | **2021–2025** (and 2018–2025) | CC BY 4.0 | ✅ | ✅ | primary (2021–2025) |
| Sri Lanka **Dept of Census & Statistics** | district + DS (tabular) | district 2014–2024; DS 2012/2024 | gov | n/a (tabular) | ✅ (DS-level) | **validation** (+ tabular alternative) |
| GPWv4.11 (SEDAC) | ~1km | 2020 (5-yearly) | CC BY 4.0 | coarse | partial | fallback |
| GHS-POP (JRC R2023) | 100m/1km (5-yr epochs) | 2020/2025 | open | ✅ | partial | fallback |

Full URLs/concerns in the inventory CSV.

## Key findings
1. **WorldPop is the right gridded source.** 100m GeoTIFF in **EPSG:4326 — the same CRS as `rdhs_26_v1.gpkg`** — so zonal sums over the RDHS polygons (including the dissolved `LK52K`/`LK52A`) are direct. 100m is fine even for the smallest DS (Sainthamaruthu ≈ 3.35 km² ≈ ~335 cells); a 1 km grid (GPW) would be far too coarse there.
2. **2018–2025 coverage is achievable** but spans two WorldPop products: the **Individual-countries annual series (UN-adjusted) covers 2018–2020**; the **WorldPop Global 2015–2030** product extends annual coverage to **2025**. The exact Global product/version and its Sri Lanka annual coverage must be confirmed at download time (the later years are projections).
3. **Sri Lanka census is the authoritative validation source.** The **2024 Census** (pop 21,781,800; vs 2012's 20,359,439) plus **mid-year district estimates 2014–2024** give district control totals; **DS-level census tables (2012/2024)** allow cross-checking the Kalmunai/Ampara split.
4. **Custom RDHS zonal sums need raster tooling.** WorldPop hub provides totals only for *its own* admin units, not our RDHS polygons — so summing WorldPop cells within the 26 RDHS requires a raster-zonal-stats library (rasterio + rasterstats / exactextract, or GDAL). **Not currently installed.**
5. **A no-raster alternative exists.** Because we already have the DS↔RDHS assignment and census DS-level tables, denominators can be built *purely from census tables*: 24 RDHS = district mid-year estimates; Ampara district apportioned to Ampara/Kalmunai RDHS via DS-level census shares. This needs **no raster install** but only has DS granularity at census years (2012/2024).

## Recommended denominator strategy
**Primary: WorldPop annual gridded, zonal-sum per RDHS** — one population value per RDHS per epidemiological year 2018–2025, **constant within each epi-year**, computed by summing WorldPop 100m cells within each RDHS polygon (`geometry_id`). Same method for all 26 units, including the split. **No weekly interpolation** (unjustified for dengue denominators).
**Validation: Sri Lanka census** — cross-check WorldPop RDHS/district sums against mid-year district estimates (2014–2024) and the 2024 census DS-level totals for the Kalmunai/Ampara split (expect close agreement; investigate >~5% discrepancies).
**Lighter alternative (no raster install):** census-table-based denominators (district mid-year for the 24 RDHS + DS-share apportionment for the split). Use if we prefer to avoid raster tooling; document the apportionment assumption.

## Strict verdict
- **A. Best population source:** **WorldPop** (100m annual, EPSG:4326, CC BY 4.0) — gridded, geometry-CRS-aligned, handles the split.
- **B. Best validation source:** **Sri Lanka Dept of Census & Statistics** (2024 census + 2014–2024 mid-year district estimates; DS-level 2012/2024).
- **C. Does WorldPop support 2018–2025?** **Yes** — 2018–2020 via the Individual-countries annual series; 2021–2025 via WorldPop Global 2015–2030 (confirm exact product/version at download).
- **D. Are RDHS zonal sums feasible?** **Yes** — WorldPop and the geometry share EPSG:4326; sum cells per polygon.
- **E. Can Kalmunai/Ampara be handled?** **Yes** — zonal-sum over the dissolved `LK52K`/`LK52A` polygons; cross-validate with 2024 census DS-level.
- **F. Is raster tooling needed?** **Yes, for the WorldPop (primary) path** — `rasterio` + `rasterstats` (or `exactextract`). **Not installed → requires approval.** The census-table alternative (E above) needs **no** raster tooling.
- **G. Exact next step:**
  1. **Choose the path:** (i) WorldPop gridded (needs raster-tool install — ASK), or (ii) census-table-only (no install).
  2. If WorldPop: on approval, install `rasterio rasterstats` (or `exactextract`), download the SL annual rasters **into git-ignored quarantine** (`data_quarantine/geomatics/population/`), zonal-sum per RDHS for 2018–2025, write `population_year` into the crosswalk, and cross-validate vs census.
  3. If census-only: pull the district mid-year (2014–2024) + DS-level (2024) tables into quarantine and build denominators by table aggregation/apportionment.
  *(Still no climate download, no exposure construction, no outcome↔exposure linkage, no models. Population rasters/tables stay quarantined and git-ignored.)*

## Note
No population data was downloaded in this reconnaissance. Any future population download stays under git-ignored quarantine (`*.tif/.tiff/.nc/.zip` are blocked); only documentation/templates are committed.
