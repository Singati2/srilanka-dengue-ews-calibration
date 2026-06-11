# District-Anchored Rescaled Population-Denominator Build Report (Geomatics WP1)
*Documents a denominator build performed **locally**. The rescaled CSV, WorldPop rasters, and census tables stay in git-ignored quarantine and are **NOT committed**. No climate data, no outcome↔exposure linkage, no models, preregistration untouched, frozen outcome dataset unchanged.*

**Date:** 2026-06-11

## What was built
Annual RDHS-year population **denominators rescaled to the 2024 Census** at the district level, per the approved formula (validation plan `population_denominator_dcs_validation_plan.md`). The rescale corrects WorldPop's **spatially-uneven** district bias (−13% to +24%) while keeping WorldPop's annual trend and the Ampara/Kalmunai internal split.

## Inputs (quarantined)
- WorldPop RDHS denominators (G2 R2025A constrained, 100m) — sha256 `8b8f6f6b…`.
- Census 2024 district totals (DCS CPH-2024; national 21,781,800).
- RDHS crosswalk + Kalmunai/Ampara split template.

## Formula
- 1:1 district-RDHS *d*: `pop_adj(d,y) = Census2024(d) × WP(d,y)/WP(d,2024)`
- Ampara split: anchor `AmparaDistrict_adj(y) = Census2024(Ampara) × [WP(A,y)+WP(K,y)]/[WP(A,2024)+WP(K,2024)]`, then split by the WorldPop per-year ratio.

## Output (quarantined, NOT committed)
- `~/data_quarantine/geomatics/population_worldpop/processed_rescaled/rdhs_population_worldpop_district_rescaled_2018_2025.csv`
- **SHA256:** `e4585741be94a33f069b64a91b802f5e70979ab4c5d0c0496e4fe10ba37d5d3a` · 208 rows.
- Columns: `rdhs_id, rdhs_name, geometry_id, parent_district, province, year, population_worldpop_raw, population_rescaled, census_anchor_year, census_anchor_district, census_anchor_population, rescale_factor_2024, rescale_method, notes`.

## QC results
| Check | Result |
|---|---|
| 26 RDHS × 8 years = 208 rows | **208** ✅ |
| No duplicate / no missing RDHS-year | ✅ / ✅ |
| population_rescaled > 0 (min 112,935) | ✅ |
| Numeric | ✅ |
| Extreme YoY changes (>5%) | **0** ✅ |
| **2024 == Census for every 1:1 district** | ✅ exact (none mismatched) |
| **Ampara + Kalmunai 2024 == Census Ampara district** | ✅ **744,551.0** (diff +0.00) |
| **National 2024 == 21,781,800** | ✅ exact |
| Ampara:Kalmunai internal ratio preserved (all years) | ✅ |

## Key figures
- **National 2024 after rescaling: 21,781,800** (matches census exactly; raw WorldPop was 23,008,642 → −5.3%).
- National raw→rescaled by year: −5.0% (2018) … −5.4% (2025) — smooth, no discontinuities.
- **Rescale factors (2024):** min **0.804 (Moneragala)** [was +24% over], max **1.146 (Mannar)** [was −13% under], Kalmunai 0.879. Range reflects exactly the spatially-uneven bias the rescale corrects.

## Caveats
- WorldPop temporal trend assumed valid; 2018–2023 levels back-projected from the 2024 anchor (not each-year census-validated).
- Census figures transcribed; confirm vs the DCS **final** district table pre-publication (~0.1% Colombo difference noted).
- Ampara/Kalmunai split uses the WorldPop ratio; optionally refine with 2024 DS-level census.
- 2025 = WorldPop-trend extrapolation off the 2024 census anchor (no 2025 census yet).

## Status & next step
- District-anchored denominators built and QC-clean (quarantined, not committed). This is the denominator the pipeline will consume.
- **Remaining WP1 item:** the **BYM2 adjacency graph** from the 26 polygons. After that, WP1 (geometry + denominators + adjacency) is complete — still **before** any climate download, exposure construction, outcome↔exposure linkage, or modeling.
