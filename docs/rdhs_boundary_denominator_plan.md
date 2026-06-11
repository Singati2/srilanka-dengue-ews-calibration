# Geomatics WP1 — RDHS Boundary Crosswalk & Population-Denominator Plan
*Planning only. No climate data downloaded/processed, no outcome↔exposure linkage, no models, preregistration untouched, frozen outcome dataset unchanged. Code/docs/templates only.*

**Companion template:** `geomatics_templates/rdhs_crosswalk_template.csv`
**Spatial unit:** the 26 RDHS divisions of the frozen WER current-week outcome (see `data_dictionary/wer_currentweek_data_dictionary.md`).

## A. Purpose
Establish a defensible, frozen mapping from the **26 WER RDHS divisions** (the outcome's spatial unit) to (a) standard administrative geometry (district/province), (b) a single fixed boundary vintage, and (c) population denominators — so incidence, the model offset, the spatial adjacency graph, and (later) population-weighted exposure are all built on one auditable spatial backbone.

## B. Why this must happen BEFORE climate linkage / modeling
- Both the mechanistic R0 input and the DLNM-INLA model consume climate **aggregated to the RDHS unit**; that aggregation is undefined until RDHS polygons + a frozen vintage exist.
- Incidence and the model offset require **denominators per RDHS-year**.
- The BYM2 spatial random effect is a function of the RDHS adjacency graph (derived from the polygons).
- Constructing exposure or linking before the spatial backbone is frozen would bake in change-of-support errors that later masquerade as miscalibration — the exact artifact this project is designed to detect, not introduce. **Spatial backbone first; linkage later.**

## C. The 26 RDHS divisions
Colombo, Gampaha, Kalutara, Kandy, Matale, Nuwara Eliya, Galle, Hambantota, Matara, Jaffna, Killinochchi, Mannar, Vavuniya, Mullaitivu, Batticaloa, Ampara, Trincomalee, Kalmunai, Kurunegala, Puttalam, Anuradhapura, Polonnaruwa, Badulla, Moneragala, Ratnapura, Kegalle.

**Alias handling (frozen → official, for boundary joins):**
- `Killinochchi` → **Kilinochchi** (one L)
- `Moneragala` → **Monaragala**
- `Nuwara Eliya` → source variants `Nuwaraeliya` / `Nuwara-Eliya`
- `Mullaitivu` → source variant `Mullaittivu`
- `Kalmunai` → **not a district** (see E)

## D. RDHS → district / province mapping strategy
Sri Lanka has **25 districts / 9 provinces**, but the WER reports **26 RDHS**. Mapping is **1:1 RDHS↔district for 24 units**, with **Ampara district served by TWO RDHS (Ampara + Kalmunai)**.
1. For the 24 clean RDHS: join to district (ADM2) geometry by official name after alias normalization.
2. For Ampara district: split into **Ampara RDHS** and **Kalmunai RDHS** by aggregating Divisional-Secretariat (DS / ADM3) divisions to each RDHS (see E).
3. Province (ADM1) is pre-filled in the crosswalk template.

Province groupings (for reference): Western (Colombo, Gampaha, Kalutara); Central (Kandy, Matale, Nuwara Eliya); Southern (Galle, Matara, Hambantota); Northern (Jaffna, Kilinochchi, Mannar, Vavuniya, Mullaitivu); Eastern (Batticaloa, Ampara + Kalmunai, Trincomalee); North Western (Kurunegala, Puttalam); North Central (Anuradhapura, Polonnaruwa); Uva (Badulla, Monaragala); Sabaragamuwa (Ratnapura, Kegalle).

## E. Known complicated units (split / non-standard)
- **Kalmunai (THE key case):** a coastal RDHS *inside* Ampara district (created for service delivery in the predominantly Tamil/Muslim coastal belt). **No standard ADM2 polygon exists for it.** Options, in order of preference:
  1. **DS-division aggregation:** obtain ADM3 (DS division) boundaries and assign the Kalmunai-side DS divisions (e.g., Kalmunai, Kalmunai Tamil Division, Sainthamaruthu, Karaitivu, Ninthavur, Addalaichchenai, Pottuvil — **confirm against the official RDHS↔DS list**) to Kalmunai RDHS; the remaining Ampara DS divisions to Ampara RDHS.
  2. **Merge fallback:** if a reliable RDHS↔DS assignment cannot be sourced, **merge Ampara + Kalmunai into a single "Ampara district" spatial unit** for exposure/denominator purposes (outcome rows stay separate but share the Ampara polygon/denominator) — **document as a deliberate limitation.**
- **Ampara RDHS:** the complement of Kalmunai within Ampara district; depends on the same DS split.
- All other 24 RDHS are 1:1 with districts (no split).

## F. Candidate boundary sources
- **HDX (Humanitarian Data Exchange) — Sri Lanka administrative boundaries** (OCHA / Survey Department): ADM0–ADM4 (province/district/DS/GN). **Best** — has the ADM3 (DS) layer needed for the Kalmunai split.
- **geoBoundaries** (wmgeolab): open ADM1/ADM2; permissive license; district-level.
- **GADM v4.1:** ADM1 (province) / ADM2 (district); districts only — cannot do the Kalmunai split.
- **WorldPop-compatible boundaries:** admin sets aligned to WorldPop rasters; useful for consistent zonal stats.
- **Official Sri Lanka Survey Department / Dept of Census & Statistics** GIS (if directly downloadable): authoritative for district + DS + GN.
- **RDHS / MOH boundary source:** the Ministry of Health / Epidemiology Unit may publish RDHS or MOH-area GIS; discover if available (would make the Kalmunai split exact). Not assumed.

## G. Recommended boundary source (+ fallback)
- **Primary: HDX Sri Lanka ADM2 (district) + ADM3 (DS division).** ADM2 for the 24 clean RDHS; aggregate ADM3 to reconstruct the Ampara/Kalmunai split.
- **Fallback: GADM / geoBoundaries ADM2** (districts only) → forces the Ampara+Kalmunai merge (Section E option 2), documented as a limitation.

## H. Candidate population-denominator sources
- **Sri Lanka Census of Population and Housing** (Dept of Census & Statistics): authoritative district- and DS-level counts. Confirm latest vintage (2012 full census; check for the 2024 census release). Best for cross-validation and DS-level Kalmunai denominators.
- **WorldPop annual gridded population** (~100 m, constrained/unconstrained): zonal-sum within ANY polygon (incl. the Kalmunai split) and **annual** values across the study window. **Best operational choice** for per-RDHS-year denominators.
- **GPW v4 (SEDAC)** or **GHS-POP:** fallback gridded sources.

## I. Recommended denominator strategy
- **Primary: annual population per RDHS** from **WorldPop annual gridded** (zonal-sum within each RDHS polygon), one value per RDHS per epi-year 2018–2025, **vintage-matched** (use the latest available WorldPop year for years beyond its coverage, documented).
- **Cross-validate** WorldPop RDHS/district sums against census district totals (expect close agreement).
- **Do NOT** use a single fixed baseline (loses ~8 years of differential growth).
- **Do NOT** interpolate weekly population — unjustified for dengue denominators; hold population constant within each epi-year.
- Kalmunai denominator follows the boundary decision (DS-aggregation sum, or shared-with-Ampara if merged).

## J. Boundary-vintage documentation requirements (freeze these)
For every geometry/population layer adopted, record:
- **source** (name + URL), **year / version**, **download date**,
- **CRS / projection** (store native; reproject to a local equal-area CRS — SLD99 / UTM 44N — for area & zonal stats),
- **admin level** (ADM1/2/3),
- **modifications made** (dissolves, DS aggregations for Kalmunai, topology fixes, ID assignment),
- **checksum (sha256)** of the adopted boundary file.
Freeze ONE boundary vintage for the entire study; any change → a new versioned freeze. (Boundary files themselves are git-ignored — only metadata/checksums are committed.)

## K. Spatial-unit QC checklist
- [ ] **26/26 RDHS matched** to a geometry (after alias normalization).
- [ ] **No duplicate** RDHS↔polygon assignments.
- [ ] **No unmatched** RDHS and no orphan polygons.
- [ ] **No invalid geometries** (validity/repair; check self-intersections).
- [ ] **Area sanity checks** (RDHS/district areas vs published km²; Ampara+Kalmunai area ≈ Ampara district area).
- [ ] **Population sanity checks** (WorldPop RDHS sums vs census district totals within tolerance).
- [ ] **Province/district consistency** (each RDHS in the correct province per crosswalk).
- [ ] **Coastal/island no-data checks** (no spurious cross-sea adjacency; islands assigned correctly).
- [ ] **Kalmunai / Ampara split decision documented** (DS-aggregation vs merge) with the exact DS list used.
- [ ] Stable `geometry_id` assigned and recorded in the crosswalk.

## L. Stop conditions
- **RDHS geometries cannot be matched reliably** (DS layer unavailable AND district names won't join) → stop; escalate to PI; consider an institutional MOH GIS request.
- **Only province-level (ADM1) boundaries available** → district/RDHS analysis infeasible at the required resolution → stop and reassess the unit (do not silently coarsen to province).
- **Population denominators cannot be assigned consistently** across RDHS-years → stop; the offset/incidence cannot be defined.
- In every stop case: document the blocker; do not improvise a coarser unit or an undocumented denominator.

## M. Exact next action for the Geomatics engineer
1. **Acquire the HDX Sri Lanka admin boundary set (ADM2 + ADM3)** and confirm it contains DS divisions for Ampara. *(Boundary files stay in a local git-ignored folder — never committed.)*
2. **Obtain the official RDHS↔DS-division assignment** for Ampara/Kalmunai (Ministry of Health / Epidemiology Unit list) to drive the split.
3. **Fill `geomatics_templates/rdhs_crosswalk_template.csv`**: set `geometry_id`, `boundary_year`, `population_year`, and `match_status` for all 26; resolve the Kalmunai split (DS aggregation or documented merge).
4. **Run the Section K QC checklist**; record the boundary-vintage metadata (Section J) including checksum.

*(Still no climate download, no exposure construction, no linkage — those are WP2 and beyond.)*
