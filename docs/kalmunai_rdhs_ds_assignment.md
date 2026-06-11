# Kalmunai vs Ampara RDHS — DS-Division Assignment (Geomatics WP1)
*Documentation only. No geometry processing, no geo-library install, no climate data, no linkage, no models, preregistration untouched, frozen outcome dataset unchanged.*

**Date:** 2026-06-11
**Companion template:** `geomatics_templates/kalmunai_ampara_ds_split_template.csv`

## A. Purpose
Resolve which of Ampara district's 19 DS divisions (HDX COD-AB ADM3) belong to **Kalmunai RDHS** vs **Ampara RDHS**, so the two RDHS polygons can later be built by dissolving DS divisions. The 24 other RDHS map 1:1 to districts; this is the only split.

## B. Official source used
**Regional Directorate of Health Services – Kalmunai (Eastern Province Health Department), "MOH Offices under RDHS Kalmunai":**
https://healthdept.ep.gov.lk/rdhs-kl/moh-offices-under-rdhs-kalmunai/ — retrieved 2026-06-11. Authority: Eastern Province Department of Health Services (official). The page explicitly lists the MOH offices under RDHS Kalmunai (the "About Us" page additionally states RDHS Kalmunai comprises 13 DS divisions / 13 MOH divisions, bounded "Thuraineelavanai on the north, Kumana on the south, Ampara line on the west").

## C. Official list (13 MOH areas under RDHS Kalmunai)
1. MOH Addalaichenai · 2. MOH Akkaraipattu · 3. MOH Alayadivembu · 4. MOH Irakkamam · 5. **MOH Kalmunai North** · 6. **MOH Kalmunai South** · 7. MOH Karaitivu · 8. MOH Navithanveli · 9. MOH Nintavur · 10. MOH Pottuvil · 11. MOH Sainthamaruthu · 12. MOH Sammanthurai · 13. MOH Thirukkovil

### Key reconciliation (resolves the "13 vs 12" question)
These are **13 MOH areas**, but **Kalmunai DS division = 2 MOH areas (Kalmunai North + Kalmunai South)**. Mapping MOH → DS division therefore yields **12 distinct DS divisions** under Kalmunai RDHS — **not 13**. The "13 DS divisions" stated on the RDHS site refers to the MOH-area count. At the **DS-division (ADM3) level used for the polygon dissolve, Kalmunai RDHS = 12 DS; Ampara RDHS = 7 DS** (12 + 7 = 19 ✓).

## D. HDX COD-AB list (19 DS divisions of Ampara district, ADM3)
Addalaichenai, Akkaraipattu, Alayadivembu, Ampara, Damana, Dehiattakandiya, Irakkamam, Kalmunai, Karaitivu, Lahugala, Mahaoya, Navithanveli, Nintavur, Padiyathalawa, Pottuvil, Sainthamaruthu, Sammanthurai, Tirukkovil, Uhana.

## E. Final Kalmunai RDHS assignment (12 DS — confirmed by official MOH list)
| DS (COD-AB) | P-code | Basis |
|---|---|---|
| Addalaichenai | LK5233 | MOH Addalaichenai |
| Akkaraipattu | LK5236 | MOH Akkaraipattu |
| Alayadivembu | LK5239 | MOH Alayadivembu |
| Irakkamam | LK5234 | MOH Irakkamam |
| Kalmunai | LK5221 | MOH Kalmunai North + South |
| Karaitivu | LK5227 | MOH Karaitivu |
| Navithanveli | LK5216 | MOH Navithanveli |
| Nintavur | LK5230 | MOH Nintavur (alias Ninthavur) |
| Pottuvil | LK5248 | MOH Pottuvil |
| Sainthamaruthu | LK5225 | MOH Sainthamaruthu |
| Sammanthurai | LK5218 | MOH Sammanthurai |
| Tirukkovil | LK5245 | MOH Thirukkovil (alias) |

## F. Final Ampara RDHS complement (7 DS — complement of the official Kalmunai list)
| DS (COD-AB) | P-code | Basis |
|---|---|---|
| Ampara | LK5215 | not in Kalmunai MOH list |
| Damana | LK5242 | not in Kalmunai MOH list |
| Dehiattakandiya | LK5203 | not in Kalmunai MOH list |
| Lahugala | LK5251 | not in Kalmunai MOH list |
| Mahaoya | LK5209 | not in Kalmunai MOH list |
| Padiyathalawa | LK5206 | not in Kalmunai MOH list |
| Uhana | LK5212 | not in Kalmunai MOH list |

## G. Alias mapping (RDHS source → COD-AB ADM3)
- `Thirukkovil` (MOH) → **Tirukkovil** (COD-AB)
- `Ninthavur` → **Nintavur**
- `Addalaichchenai` → **Addalaichenai**
- `Kalmunai North` + `Kalmunai South` (MOH) → **Kalmunai** (single DS)

## H. Remaining uncertainty
- **All 19 DS are now assigned.** Earlier borderline cases are resolved: **Navithanveli → Kalmunai** (explicit MOH), **Damana, Lahugala → Ampara** (absent from the Kalmunai MOH list).
- The 12 Kalmunai DS are **confirmed by a named MOH office** each. The 7 Ampara DS are **complement-confirmed** (not in the Kalmunai list, within the complete 19-DS Ampara set). An official **Ampara RDHS MOH list** would provide positive confirmation of the complement — a nice-to-have, not a blocker.
- Caveat: assumes MOH↔DS alignment within Ampara (standard in Sri Lanka). Verify no DS is split across both RDHS (none indicated).

## I. Is the split ready for polygon dissolve?
**Yes.** Every one of Ampara's 19 ADM3 DS divisions has a definitive RDHS assignment (12 Kalmunai + 7 Ampara), with p-codes for an unambiguous join to COD-AB ADM3. The dissolve is now deterministic: dissolve the 12 Kalmunai DS → Kalmunai RDHS polygon; the 7 Ampara DS → Ampara RDHS polygon; join the other 24 RDHS 1:1 to districts.

## J. Exact next step
1. (No install) Finalize the RDHS crosswalk so all 26 RDHS have a defined geometry rule (24 districts 1:1; Ampara = 7-DS dissolve; Kalmunai = 12-DS dissolve).
2. When approved to build geometry: **install a geo library (geopandas/fiona or GDAL) — ASK FIRST**, then execute the dissolve by p-code, assign stable `geometry_id`s, and run WP1 §K QC (e.g., Kalmunai + Ampara RDHS area ≈ Ampara district 4,474.66 km²; 26/26 RDHS matched; no slivers).
3. (Optional) Cross-confirm the 7-DS Ampara complement against an official Ampara RDHS MOH list.
*(Still no climate download, no exposure construction, no linkage.)*
