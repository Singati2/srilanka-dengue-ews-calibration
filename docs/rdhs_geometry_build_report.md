# 26-RDHS Geometry Build Report (Geomatics WP1)
*Documents a geometry build performed **locally**. The geometry (GeoPackage) and all boundary files stay in git-ignored quarantine and are **NOT committed**. No climate data, no outcome↔exposure linkage, no models, preregistration untouched, frozen outcome dataset unchanged.*

**Date:** 2026-06-11
**Tooling:** geopandas 1.1.3, pyogrio 0.12.1, pyproj 3.7.1, shapely 2.1.2 (installed with approval).

## Inputs (local, quarantined)
- HDX COD-AB Sri Lanka `lka_admin_boundaries.shp.zip` (Survey Department; CC BY-IGO; v03; sha256 `505ec4a7…`).
  - `lka_admin2.shp` = 25 districts; `lka_admin3.shp` = 339 DS divisions; CRS **EPSG:4326**.
- `geomatics_templates/rdhs_crosswalk_template.csv` (district→RDHS aliases).
- `geomatics_templates/kalmunai_ampara_ds_split_template.csv` (12 Kalmunai DS / 7 Ampara DS).

## Build rules
- **24 RDHS = ADM2 districts 1:1**, district name mapped to the frozen RDHS name via crosswalk aliases (`Kilinochchi→Killinochchi`, `Monaragala→Moneragala`; others identical).
- **Kalmunai RDHS** = dissolve of the **12** confirmed Kalmunai DS divisions (`geometry_id = LK52K`).
- **Ampara RDHS** = dissolve of the **7** confirmed Ampara DS divisions (`geometry_id = LK52A`).

## Output (local, quarantined — NOT committed)
- `~/data_quarantine/geomatics/rdhs_geometry/rdhs_26_v1.gpkg` (layer `rdhs_26`, 26 features)
- **SHA256:** `9e5e2c0a541ecac13f5c2aa08ca2d8fca79b36f645f9fad5c8067d74a189ee88` · **size:** 8,683,520 bytes
- Schema: `rdhs_id, rdhs_name, geometry_id, parent_district, province, build_rule, n_ds, geometry` (EPSG:4326).

## QC results
| Check | Result |
|---|---|
| Exactly 26 RDHS geometries | **26** ✅ |
| RDHS names match crosswalk / frozen outcome | **26/26** ✅ (24 districts + Ampara + Kalmunai) |
| No duplicates | 0 ✅ |
| No empty geometries | 0 ✅ |
| No invalid geometries | 0 (pre and post) ✅ |
| CRS documented | **EPSG:4326** ✅ |
| `geometry_id` assigned (unique, non-null) | 26 unique, 0 null ✅ |
| **Ampara + Kalmunai ≈ original Ampara ADM2 area** | 4471.56 km² vs 4474.66 km² (**−0.07%**) ✅ |
| **Total 26-RDHS ≈ Sri Lanka ADM2 total** | 65,995.00 km² vs 66,040.81 km² field (**−0.07%**); == 25-district UTM total exactly ✅ |
| SHA256 recorded | ✅ |

Areas computed in EPSG:32644 (UTM 44N). The uniform −0.07% vs the COD-AB `area_sqkm` field is a projection-method difference (the dissolve conserves area exactly — the 26-RDHS UTM total equals the 25-district UTM total). The two split RDHS sum to the Ampara district area, confirming the dissolve partitioned Ampara without gaps or overlaps.

## RDHS names produced (26)
Ampara, Anuradhapura, Badulla, Batticaloa, Colombo, Galle, Gampaha, Hambantota, Jaffna, Kalmunai, Kalutara, Kandy, Kegalle, Killinochchi, Kurunegala, Mannar, Matale, Matara, Moneragala, Mullaitivu, Nuwara Eliya, Polonnaruwa, Puttalam, Ratnapura, Trincomalee, Vavuniya — i.e., exactly the 26 RDHS of the frozen outcome dataset.

## Status & next step
- The 26-RDHS geometry is built and QC-clean, held in quarantine (not committed).
- **Next (separate, on approval):** assign/confirm the geometry↔crosswalk link (`geometry_id` into `rdhs_crosswalk_template.csv`), derive the BYM2 adjacency graph from these polygons, and attach population denominators (WorldPop annual) — still all WP1/geospatial, **no climate download, no exposure construction, no outcome linkage, no models.**
