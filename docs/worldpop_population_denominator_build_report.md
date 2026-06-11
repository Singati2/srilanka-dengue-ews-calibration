# WorldPop Population-Denominator Build Report (Geomatics WP1)
*Documents a population-denominator build performed **locally**. WorldPop rasters and the denominator CSV stay in git-ignored quarantine and are **NOT committed**. No climate data, no outcome↔exposure linkage, no models, preregistration untouched, frozen outcome dataset unchanged.*

**Date:** 2026-06-11
**Tooling:** geopandas 1.1.3, rasterio 1.4.4, rasterstats 0.21.0 (installed with approval), pyproj/shapely.

## Source (WorldPop — quarantined, not committed)
- **Product:** WorldPop Global2 — *Individual countries 2015–2030*, **100m, R2025A v1, constrained** (`G2_CN_POP_R25A_100m`).
- **URL pattern:** `https://data.worldpop.org/GIS/Population/Global_2015_2030/R2025A/{year}/LKA/v1/100m/constrained/lka_pop_{year}_CN_100m_R2025A_v1.tif`
- **License:** WorldPop / CC BY 4.0 (https://hub.worldpop.org/data/licence.txt).
- **Why this product:** the only **single consistent** WorldPop product covering **all of 2018–2025** for Sri Lanka. (The UN-adjusted unconstrained series `wpgpunadj` is 2000–2020 only; mixing it with a 2021–2025 product would create a methodological discontinuity.) **2021–2025 are projections.** Constrained method; **not UN-adjusted** (validation flag below).
- **Grid:** CRS EPSG:4326, ~100m (0.000833°), nodata −99999, float32 — matches the RDHS geometry CRS.
- 8 rasters, ~17–18 MB each (~140 MB total), downloaded read-only with per-file sha256.

## Method
Zonal **sum** of WorldPop cells within each of the 26 RDHS polygons (`rdhs_26_v1.gpkg`) via `rasterstats` (nodata −99999, all_touched=False), per year 2018–2025 → one population per RDHS-year, **constant within each epidemiological year** (no weekly interpolation). The two split RDHS (`LK52K` Kalmunai, `LK52A` Ampara) are summed over their dissolved polygons exactly like the 24 districts.

## Output (quarantined, NOT committed)
- `~/data_quarantine/geomatics/population_worldpop/processed_quarantine/rdhs_population_worldpop_2018_2025_quarantine.csv`
- **SHA256:** `8b8f6f6bb88db9a0e7525342f6eea154d7f991668d2eb80914ad8023d568a1c2` · 208 rows.
- Schema: `rdhs_id, rdhs_name, geometry_id, parent_district, province, year, population`.

## QC results
| Check | Result |
|---|---|
| 26 RDHS × 8 years = 208 rows | **208** ✅ |
| No missing RDHS-year combos | ✅ |
| population > 0 every RDHS-year | ✅ (min 103,689) |
| No duplicate RDHS-year | ✅ |
| Numeric values | ✅ |
| Extreme YoY changes (>5%) | **0** ✅ |
| National total plausibility | ✅ (see below) |
| Ampara + Kalmunai plausibility | ✅ (see below) |

## National-total plausibility (H)
| Year | WorldPop national sum |
|---|---|
| 2018 | 22,143,987 |
| 2020 | 22,458,615 |
| 2024 | 23,008,642 |
| 2025 | 23,138,801 |

**Validation flag:** WorldPop 2024 (23.01M) is **+5.6% above the 2024 Census (21,781,800)** — a known WorldPop/UN-WPP over-projection (the 2024 census revised Sri Lanka's population downward). Relative spatial distribution across RDHS is sound; the **absolute level runs ~5–6% high vs census**. Options for the validation step: keep WorldPop as-is (relative incidence preserved) or **rescale to census national/district totals** if absolute rates matter.

## Ampara + Kalmunai plausibility (I)
Combined (= Ampara district): 763,103 (2018) → **847,385 (2024)**. Split in 2024: **Ampara RDHS 321,298**, **Kalmunai RDHS 526,087** — the coastal 12-DS Kalmunai is denser than the interior 7-DS Ampara, as expected. ~11% above the census-era Ampara district estimate, consistent with the national over-count.

Sanity: smallest RDHS (2024) = Mannar 108k / Mullaitivu 113k / Killinochchi 133k (sparse north); largest = Gampaha 2.63M / Colombo 2.27M / Kurunegala 1.98M — all correct.

## Status & next step
- Annual RDHS denominators (2018–2025) built and QC-clean, held in quarantine (not committed).
- **Next (validation, on approval):** pull Sri Lanka **census / DCS** district mid-year estimates (2018–2024) + 2024 DS-level into quarantine; cross-validate RDHS/district totals; decide whether to **census-rescale** the WorldPop denominators; fill `population_year` provenance in the crosswalk.
- After that, WP1 (spatial backbone: geometry + adjacency + denominators) is complete — still **before** any climate download, exposure construction, outcome↔exposure linkage, or modeling.
