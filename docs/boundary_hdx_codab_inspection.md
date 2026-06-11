# HDX COD-AB Sri Lanka — Local Boundary Inspection (Geomatics WP1)
*Inspection of locally-downloaded HDX COD-AB boundaries. **Boundary files are NOT committed** (held under `data_quarantine/geomatics/boundary_recon/`, git-ignored). No climate data, no outcome↔exposure linkage, no models, preregistration untouched, frozen outcome dataset unchanged.*

**Date:** 2026-06-11

## Provenance & metadata
| Field | Value |
|---|---|
| Dataset | Sri Lanka – Subnational Administrative Boundaries (COD-AB) |
| Source | Survey Department of Sri Lanka, via HDX / OCHA |
| Dataset page | https://data.humdata.org/dataset/cod-ab-lka |
| License | **CC BY-IGO** (Creative Commons Attribution for Intergovernmental Organisations) |
| Dataset date range | 2022-08-16 → 2025-10-30 |
| Attribute `valid_on` | Excel serial 44789 = **2022-08-16**; `version` = **v03** |
| Last modified (HDX) | 2026-01-26 |
| **CRS** | **GCS_WGS_1984 (EPSG:4326)** — read from `lka_admin2.prj` / `lka_admin3.prj` |

### Files downloaded (local, git-ignored)
| File | Size (bytes) | SHA256 |
|---|---|---|
| `lka_admin_boundaries.xlsx` (attribute table, inspected) | 3,530,929 | `b47d718c6d6e8d67b93a9769a2dc9f0bd73afcfa250c379110aacc3e4b52c95f` |
| `lka_admin_boundaries.shp.zip` (geometry package, quarantined) | 118,094,199 | `505ec4a7881664f109001c672877825183c121edaf0015b4468e41e9c9ed94bf` |
| `hdx_meta.json` (HDX API metadata) | 42,202 | — |

Geometry package confirmed to contain `lka_admin2.shp` + `lka_admin3.shp` (+ `.prj/.dbf/.shx`).

## Layer inspection (from the XLSX attribute table; pure-Python reader, no GDAL)
| Layer | Records | Status |
|---|---|---|
| `lka_admin0` (national) | 1 | ok |
| `lka_admin1` (provinces) | **9** | ✅ matches expected |
| `lka_admin2` (districts) | **25** | ✅ matches expected |
| `lka_admin3` (DS divisions) | **339** | ✅ matches expected (~339) |
| `lka_admin4` (GN divisions) | 14,043 | ok |

### Attribute fields (ADM3)
`adm3_name, adm3_name1..3 (multilingual), adm3_pcode, adm2_name, adm2_pcode, adm1_name, adm1_pcode, adm0_name, adm0_pcode, valid_on, valid_to, area_sqkm, version, lang.., center_lat, center_lon`. (ADM2 analogous with `adm2_*`.) P-codes are hierarchical (district `LK52` = Ampara; DS = `LK52xx`).

## District ↔ RDHS name check (ADM2)
All **25 district names match exactly** the official RDHS names in our crosswalk (COD-AB uses `Kilinochchi`, `Monaragala`, `Nuwara Eliya`, `Mullaitivu` — exactly the alias targets). **No unmatched district.** The 24 clean RDHS join 1:1 to districts by name; Ampara district is the split case below.

## Ampara district → DS divisions (ADM3) — the split building blocks
Ampara district (`LK52`) contains **19 DS divisions** in COD-AB:

Addalaichenai (LK5233), Akkaraipattu (LK5236), Alayadivembu (LK5239), **Ampara (LK5215)**, Damana (LK5242), Dehiattakandiya (LK5203), Irakkamam (LK5234), **Kalmunai (LK5221)**, Karaitivu (LK5227), Lahugala (LK5251), Mahaoya (LK5209), Navithanveli (LK5216), Nintavur (LK5230), Padiyathalawa (LK5206), Pottuvil (LK5248), Sainthamaruthu (LK5225), Sammanthurai (LK5218), Tirukkovil (LK5245), Uhana (LK5212).

→ The **Kalmunai/Ampara RDHS split is constructible by aggregating these 19 ADM3 polygons** into two groups (Kalmunai RDHS ≈ 13 coastal DS, Ampara RDHS ≈ 6 interior DS), once the exact RDHS↔DS assignment is confirmed. Candidate assignment in `geomatics_templates/kalmunai_ampara_ds_split_template.csv` (DS names are real, from this inspection; RDHS assignment is candidate, to be confirmed).

## Verdict (A–H)
- **A. Did HDX ADM2 load correctly?** **Yes** — 25 district records, attribute fields intact (attribute layer; geometry package present, geometry read deferred — see G).
- **B. Did HDX ADM3 load correctly?** **Yes** — 339 DS-division records, hierarchical p-codes link DS→district.
- **C. Are 25 districts present?** **Yes — exactly 25**, all matching RDHS names.
- **D. Are DS divisions present for Ampara?** **Yes — 19 DS divisions** enumerated with p-codes and areas.
- **E. Can the Kalmunai/Ampara split be constructed?** **Yes** — by aggregating Ampara's 19 ADM3 DS polygons into Kalmunai (≈13) vs Ampara (≈6) RDHS, contingent only on confirming which 13 DS are Kalmunai's.
- **F. What DS list is still needed / confirmed?** Confirmed: the **19 candidate DS divisions of Ampara district** (from COD-AB). Still needed: the **official RDHS-Kalmunai 13-DS assignment** (from healthdept.ep.gov.lk/rdhs-kl) to resolve ~3 borderline DS (e.g., Damana, Navithanveli, Lahugala). High-confidence coastal (Kalmunai) and interior (Ampara) cores are already assignable.
- **G. Risks remaining:**
  - **Geometry reading not yet performed** — no GDAL/geopandas/fiona installed; only attributes inspected. Constructing the actual aggregated polygons (and area QC) needs a geo library → **will require a package install (ask before installing).**
  - **Borderline DS assignment** (~3 of 19) needs the official RDHS list to finalize the 13/6 split.
  - DS-name transliteration variants (Tirukkovil/Thirukkovil, Nintavur/Ninthavur, Addalaichenai/Addalaichchenai) — build an alias map when matching to the RDHS source.
  - Confirm the v03 (2022) vintage is acceptable for the 2018–2025 study period (boundaries stable over this window — verify).
- **H. Exact next step:**
  1. Obtain the **official Kalmunai RDHS 13-DS list** and finalize `kalmunai_ampara_ds_split_template.csv` (`assigned_rdhs`, `match_status`).
  2. When ready to build geometry: **install a geo library (geopandas/fiona or GDAL) — ASK FIRST**, then dissolve ADM3→RDHS (aggregate Ampara DS to Kalmunai/Ampara; join 24 districts 1:1), assign stable `geometry_id`s, and run the WP1 §K QC (incl. Ampara+Kalmunai area ≈ Ampara district `area_sqkm` = 4474.66 km²).
  3. Fill the RDHS crosswalk geometry fields; record boundary-vintage metadata + checksums (already captured above).
  *(Still no climate download, no exposure construction, no linkage.)*
