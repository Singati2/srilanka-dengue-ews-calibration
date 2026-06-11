# RDHS Crosswalk — Geometry-ID Update (Geomatics WP1)
*Documentation only. The geometry (GPKG) and boundary files stay in git-ignored quarantine and are NOT committed. No climate data, no outcome↔exposure linkage, no models, preregistration untouched, frozen outcome dataset unchanged.*

**Date:** 2026-06-11
**File updated:** `geomatics_templates/rdhs_crosswalk_template.csv` (tracked, safe — names/codes only, no geometry).

## A. Purpose
Write the final `geometry_id` (and source/vintage/match_status) into the RDHS crosswalk so each of the 26 RDHS outcome units is unambiguously linked to its polygon in the local quarantined geometry (`rdhs_26_v1.gpkg`). This closes the outcome↔geometry link needed before population denominators and the adjacency graph.

## B. Source of geometry IDs
Geometry IDs were read directly from the QC-clean local geometry **`~/data_quarantine/geomatics/rdhs_geometry/rdhs_26_v1.gpkg`** (layer `rdhs_26`, SHA256 `9e5e2c0a541ecac13f5c2aa08ca2d8fca79b36f645f9fad5c8067d74a189ee88`), itself built from **HDX COD-AB Sri Lanka ADM2/ADM3** (Survey Department via HDX/OCHA; CC BY-IGO; v03, valid_on 2022-08-16; EPSG:4326).

## C. Geometry-ID rule
- **24 standard RDHS** = their COD-AB **ADM2 p-code** (e.g., Colombo = `LK11`).
- **Kalmunai RDHS** = **`LK52K`** (dissolve of 12 Kalmunai DS divisions).
- **Ampara RDHS** = **`LK52A`** (dissolve of 7 Ampara DS divisions).

Fields set for all 26 rows: `geometry_source_candidate` = "HDX COD-AB Sri Lanka ADM2/ADM3, Survey Department via HDX/OCHA"; `boundary_year` = "2022-08-16 / v03".

## D. The 24 district 1:1 geometry IDs
| RDHS | geometry_id | RDHS | geometry_id |
|---|---|---|---|
| Colombo | LK11 | Trincomalee | LK53 |
| Gampaha | LK12 | Kurunegala | LK61 |
| Kalutara | LK13 | Puttalam | LK62 |
| Kandy | LK21 | Anuradhapura | LK71 |
| Matale | LK22 | Polonnaruwa | LK72 |
| Nuwara Eliya | LK23 | Badulla | LK81 |
| Galle | LK31 | Moneragala | LK82 |
| Matara | LK32 | Ratnapura | LK91 |
| Hambantota | LK33 | Kegalle | LK92 |
| Jaffna | LK41 | Killinochchi | LK45 |
| Mannar | LK42 | Batticaloa | LK51 |
| Vavuniya | LK43 | | |
| Mullaitivu | LK44 | | |

`match_status = confirmed_1to1` for all 24.

**Alias notes (frozen → COD-AB ADM2):** `Killinochchi → Kilinochchi` (one L); `Moneragala → Monaragala`. `Nuwara Eliya` and `Mullaitivu` match COD-AB spelling directly (no alias needed).

## E. Kalmunai and Ampara split IDs
| RDHS | geometry_id | match_status | note |
|---|---|---|---|
| Kalmunai | **LK52K** | `confirmed_ds_dissolve_12` | dissolved from 12 confirmed Kalmunai DS divisions (official RDHS-Kalmunai MOH list) |
| Ampara | **LK52A** | `confirmed_ds_dissolve_7` | dissolved from 7 complement-confirmed Ampara DS divisions |

## F. Verification checks (all passed)
- 26 rows in crosswalk ✅
- 26 non-missing `geometry_id` ✅
- 26 unique `geometry_id` ✅
- all 26 RDHS names present ✅
- Ampara `geometry_id` = `LK52A` ✅
- Kalmunai `geometry_id` = `LK52K` ✅
- `match_status` = 24 × confirmed_1to1, 1 × confirmed_ds_dissolve_12, 1 × confirmed_ds_dissolve_7 ✅
- **row order preserved** (unchanged from prior version) ✅

## G. Is the crosswalk ready for population denominators?
**Yes.** Every RDHS outcome unit now has a stable `geometry_id` linking it to its polygon in `rdhs_26_v1.gpkg`. Population denominators (WorldPop annual, zonal-sum per RDHS polygon) and the BYM2 adjacency graph can both key off these IDs. (`population_source_candidate = WorldPop_annual`, `population_year = TBD` remain as placeholders for that step.)

## H. Exact next step
1. (Geospatial, on approval) Derive the **BYM2 adjacency graph** from the 26 polygons (queen contiguity, with the coastal/no-cross-sea check) keyed on `geometry_id`.
2. (Geospatial, on approval) Attach **annual population denominators** (WorldPop, zonal-sum per RDHS, 2018–2025), fill `population_year`, cross-validate against census district totals.
*(Still no climate download, no exposure construction, no outcome↔exposure linkage, no models.)*
