# Boundary-Source Reconnaissance — Sri Lanka RDHS/District Geometry (Geomatics WP1)
*Reconnaissance only. Metadata inspection via web search; **no boundary files downloaded**. No climate data, no outcome↔exposure linkage, no models, preregistration untouched, frozen outcome dataset unchanged.*

**Date:** 2026-06-10
**Goal:** verify whether reliable boundary geometry for the 26 RDHS divisions can be obtained — especially the **Ampara + Kalmunai split**.
**Companion inventory:** `geomatics_templates/boundary_source_inventory_template.csv`

## Candidate sources (summary)
| Source | ADM levels | District (ADM2) | DS division (ADM3) | License | Vintage | Supports Kalmunai split |
|---|---|---|---|---|---|---|
| **HDX COD-AB (Survey Dept/OCHA)** | 0–4 (9/25/339/14,043) | ✅ 25 | ✅ **339 DS** | COD-AB/HDX (confirm exact) | reviewed **Oct 2024** | **YES** |
| geoBoundaries | 0–4 | ✅ | ✅ (verify) | **CC BY 4.0** (ADM2 also ODbL) | v6.0.0 | likely |
| GADM v4.1 | Nat/Prov/Dist/DS/GN | ✅ | ✅ DS | free academic, **no redistribution** | v4.1 | yes |
| NSDI gov GIS (REST) | ADM3 DS layer | partial | ✅ (live REST) | gov/NSDI (confirm) | live | yes (official) |
| Dept of Census & Statistics | reference maps | reference | reference | gov | 2012/2024 | reference only |
| MoH GIS Maps | MOH-division web maps | not confirmed dl | not confirmed | MoH | unknown | possible if downloadable |
| **RDHS Kalmunai official site** | RDHS definition | — | — | public web | current | **provides the split logic** |

Full details, URLs, and per-source concerns: see the inventory CSV.

## Key findings
1. **District (ADM2) geometry is abundant and open.** HDX COD-AB has **25 districts** (Survey Department, reviewed Oct 2024). geoBoundaries (CC BY 4.0) and GADM v4.1 also provide it. The 24 clean RDHS map 1:1 to districts → trivially covered.
2. **DS-division (ADM3) geometry exists** — **HDX COD-AB ADM3 = 339 DS divisions** (the layer needed for the Kalmunai split), with GADM and geoBoundaries as alternates and the **NSDI government REST service** as the official live DS layer.
3. **The Ampara/Kalmunai split is well-defined and discoverable.** Per the **official RDHS Kalmunai site**, **Kalmunai RDHS = 13 DS divisions** in the eastern coastal belt of Ampara district (named examples: Kalmunai, Kalmunai North/Tamil, Sammanthurai, Sainthamaruthu, Karaitivu, Ninthavur, Addalaichchenai, Akkaraipattu, Thirukkovil, Pottuvil — exact list to be finalized). The remaining Ampara district DS divisions (interior, e.g., Ampara, Uhana, Dehiattakandiya, Mahaoya, Padiyathalawa, Damana, Lahugala) form **Ampara RDHS**.
   → **Plan:** aggregate the 13 Kalmunai-side ADM3 polygons → Kalmunai RDHS; the complement → Ampara RDHS. This reconstructs all 26 RDHS without needing a dedicated RDHS shapefile.
4. **No confirmed downloadable RDHS/MOH shapefile.** The MoH has a GIS Maps web page but no verified vector RDHS layer; building RDHS from DS aggregation is the reliable route. (An MoH GIS request remains optional upside, not required.)

## Verdict
- **A. Best boundary source:** **HDX COD-AB Sri Lanka** (Survey Department; ADM2 districts + **ADM3 DS divisions**; authoritative; recently reviewed Oct 2024).
- **B. Best fallback:** **geoBoundaries** (CC BY 4.0, ADM0–4) for clean reuse; **GADM v4.1** as a second alternate (has DS level, but no-redistribution license — acceptable since boundary files are never committed); **NSDI REST** as the official DS cross-check.
- **C. Is ADM3/DS geometry available?** **Yes** — 339 DS divisions in HDX COD-AB (plus GADM/geoBoundaries/NSDI).
- **D. Can Kalmunai be split from Ampara?** **Yes — very likely.** The split is defined by an official **13-DS-division** Kalmunai RDHS list; aggregate those ADM3 polygons vs the Ampara complement.
- **E. Is an official RDHS↔DS list still needed?** **Partially obtained, must be finalized.** The Kalmunai RDHS = 13 DS divisions is documented on the official RDHS Kalmunai site; the **exact 13 DS-division names must be extracted and matched to the ADM3 attribute names**, and the Ampara RDHS complement confirmed. Not a blocker, but the precise list is the remaining input.
- **F. Stop risks:**
  - **DS-name matching:** Tamil/Sinhala transliteration variants between the RDHS list and ADM3 attributes (e.g., Karaitivu/Karathivu, Addalaichchenai/Addalachchenai) — needs careful alias mapping.
  - **License confirmation:** verify exact HDX COD-AB license text before adopting (GADM's no-redistribution does not block us since files stay local).
  - **Currency/stability** of the 13-DS Kalmunai definition (confirm it matches the 2018–2025 study period).
  - If the official 13-DS list cannot be pinned down: fall back to the **Ampara+Kalmunai merge** (documented limitation, per the WP1 plan §E option 2).
- **G. Exact next step for the Geomatics engineer:**
  1. **Download HDX COD-AB ADM2 + ADM3** into the **local, git-ignored** `data_quarantine/geomatics/boundary_recon/` (do NOT commit).
  2. **Extract the Ampara district DS-division list from ADM3** and **the official Kalmunai 13-DS list** from the RDHS Kalmunai site; reconcile names (build the alias map).
  3. **Aggregate** the 13 Kalmunai DS polygons → Kalmunai RDHS; complement → Ampara RDHS; join the other 24 RDHS to districts.
  4. **Fill** `geomatics_templates/rdhs_crosswalk_template.csv` (`geometry_id`, `boundary_year`, `match_status`) and record boundary-vintage metadata + checksums (WP1 plan §J).
  5. **Run** the WP1 §K spatial-unit QC checklist (incl. Ampara+Kalmunai area ≈ Ampara district area).
  *(Still no climate download, no exposure construction, no linkage.)*

## Notes
- Boundary files, when downloaded, stay under `data_quarantine/geomatics/boundary_recon/` and are git-ignored (`.shp/.dbf/.shx/.gpkg/.geojson/.zip` are blocked). Only documentation/templates/metadata are committed.
