# Plan — MAUP / Exposure-Sensitivity (WP5) & Spatial-Block Cross-Validation (WP4)

*Working plan owned by the Geospatial Lead. Status: **SCOPE LOCKED 2026-07-07** — the four open decisions are settled (see §1a); execution-ready pending PI ratification and data staging. No implementation started.*
*Companion to `geomatics_scope_of_work.md` (WP4, WP5) and the freeze/linkage rules in `project_overview.md`.*

---

## 1. Why these two tasks

The paper's headline is **"two equally accurate warning systems can recommend different public-health actions."** Two reviewer attacks can sink that claim, and both are answered by the work below:

- **"Your miscalibration is just exposure misclassification, not a real model difference."**
  → **WP5 (MAUP / exposure sensitivity)** separates *real* miscalibration from *exposure-construction artifact* by re-running the whole decision analysis under two exposure builds (naive area-mean vs population-weighted) and asking whether the exposure choice *alone* moves net benefit or flips decisions.

- **"Your external validation leaks — neighboring units share information across train/test."**
  → **WP4 (spatial-block cross-validation)** defines leakage-proof folds (block size ≥ the residual autocorrelation range, buffered) so the out-of-sample claim is spatially honest, not just temporally honest.

WP5 is designated a **primary result (F7)**; WP4 is the **validation backbone** that makes external validation defensible. Both are co-authorship-level deliverables per the SOW (§K).

---

## 1a. Decisions locked (2026-07-07)

The four open scope questions in §6 are settled (Geospatial Lead; to be ratified by PI):

| # | Question | Decision |
|---|---|---|
| D1 | Spatial-CV setting | **Both**, each scheme sized to the number of areas: Sri Lanka via **buffered leave-one-out (LOOCV)**, Colombia via **spatial block CV** (leave-one-department-out). SL is the compact-country sensitivity companion; Colombia carries the well-powered spatial test. |
| D2 | Number of exposure builds | **Three** — (A) naive area-mean, (B) population-weighted, (C) elevation / lapse-rate–corrected temperature. |
| D3 | Analysis resolution | **Keep 26 RDHS** (SL) / municipality (Colombia). No re-extraction to MOH-division. |
| D4 | Extras in-scope for this paper | **All four:** per-variable MAUP · spatial-structure-of-miscalibration map (WP6 bridge, F8) · cross-setting MAUP (repeat weather contrast in Colombia) · population-product sensitivity (WorldPop vs GHSL vs census). |

**Cross-validation design (D1 detail).** "Spatial CV" stops a held-out area's near neighbors — which share weather and outbreak timing — from leaking the answer through the training set.
- **Sri Lanka (26 RDHS):** leave-one-district-out, **buffered** — when a district is held out, its within-range neighbors are also dropped from training. 26 folds; honest at small n but low-powered (a sensitivity companion, not the headline test).
- **Colombia (~1,000 municipalities):** **spatial block CV** — group municipalities into contiguous blocks larger than the autocorrelation range (or leave one whole department out), with a buffer strip so train/test units are never within range.
- **Both:** temporal honesty preserved inside every spatial fold (lags built from the past only) → spatio-temporal CV.

**Scope note:** D4 accepts the full extras set — a deliberately comprehensive paper. Population-product sensitivity is the lowest-priority extra and the first candidate to trim if the timeline slips.

---

## 2. Current state — what already exists (build on, don't rebuild)

| Artifact | What it is | Status |
|---|---|---|
| `rdhs_weekly_climate_exposure_2018_2025_v2_boundary_resolved.csv` | Weekly climate exposure, **area-weighted** (`all_touched` mask + NumPy). 10,842 rows = 417 ISO weeks × 26 RDHS. SHA256 `3900082b…` | ✅ Built (freeze candidate) |
| `…population_denominator_district_rescaled_2018_2025.csv` | WorldPop → 2024-census-anchored population, 208 rows (26 RDHS × 8 yr). SHA256 `e4585741…` | ✅ Built |
| `rdhs_26_v1.gpkg` | 26-RDHS geometry, EPSG:4326. SHA256 `9e5e2c0a…` | ✅ Built |
| Adjacency graph | Queen contiguity, 26 nodes / 60 edges, connected, no cross-sea edges | ✅ Built |
| WorldPop 100 m constrained raster (2018–2025) | Source grid for population weights | ✅ In quarantine |
| Model ladder + calibration + DCA/net-benefit code | `scripts/colombia_model_ladder_*`, `decision_threshold_dnb_robustness_*`; SL DLNM comparator | ✅ Runnable |

**Key gap:** everything downstream currently consumes the **area-weighted** exposure. There is **no population-weighted exposure table** and **no spatial-block CV**. All validation to date uses a single **temporal** split (SL: train 2018–2022 / test 2023–2025; Colombia: train ≤2017 / val 2018–19 / test 2020–22).

---

## 3. WP5 — MAUP / Exposure-Sensitivity

**Goal:** produce two additional exposure tables — **Build B (population-weighted)** and **Build C (terrain-corrected temperature)** — as drop-in twins of the existing area-weighted **Build A**, then quantify how much the *exposure construction alone* changes calibration and net benefit. The three builds form a nested ladder, each adding one refinement: **A** = area-mean, raw grid → **B** = population-weighted, raw grid → **C** = population-weighted, lapse-rate–corrected temperature.

### 3.1 Build B — population-weighted exposure table
- [ ] Reproject boundaries, WorldPop, and climate grids to an **equal-area CRS** (SLD99 / Sri Lanka Grid, or UTM 44N). **Never area-weight in WGS84 degrees.**
- [ ] For each RDHS × ISO-week × variable (`t2m mean/min/max`, `d2m`, `RH`, `precip sum/mean`), compute a **population-weighted zonal mean**: weight each climate cell by the WorldPop population falling in it (fractional-cell / `exactextract`-style overlap, not `all_touched`).
- [ ] Match the **population vintage to the exposure year** (don't weight 2019 climate with 2025 population).
- [ ] Also carry **within-unit dispersion** (SD and IQR) per unit-week — heterogeneity is a covariate for WP6, don't discard it.
- [ ] Output `…climate_exposure_2018_2025_v2_popweighted.csv`, **row-aligned** (same 10,842 keys) to Build A so they diff cleanly. Checksum + freeze candidate.

### 3.1b Build C — elevation / lapse-rate–corrected temperature exposure table
- [ ] Obtain a DEM (**Copernicus GLO-30**, 30 m; SRTM fallback) over both countries; reproject to the same equal-area CRS.
- [ ] Lapse-rate–correct the ERA5-Land temperature fields (`t2m mean/min/max`, and `d2m` for humidity) to the DEM at the **fine grid, before aggregation** — start with the standard environmental rate (−6.5 °C/km); sensitivity with a locally-fit or MODIS-LST-anchored rate.
- [ ] Aggregate the corrected fine grid using the **same population weighting as Build B**, so Build C isolates the *terrain* effect on top of population weighting (clean single-axis step B→C).
- [ ] Precipitation/RH (not lapse-corrected) are carried through unchanged, so Build C differs from Build B on **temperature only**.
- [ ] Output `…climate_exposure_2018_2025_v3_terraincorrected.csv`, row-aligned to Builds A/B. Checksum + freeze candidate.

### 3.2 Exposure contrast (Figure F2)
- [ ] Compute per unit-week `weighted − naive` (A→B) and `terrain − weighted` (B→C) for each variable; summarize the distribution (national, and by RDHS).
- [ ] **Per-variable (extra D4):** report divergence **separately per variable** — expect precipitation (CHIRPS, patchy convective) to diverge far more than temperature (ERA5-Land, smooth); expect Build C to move temperature most in the central highlands.
- [ ] **F2**: map/plot the exposure-construction contrast. Expect the largest divergence where population is concentrated off the areal centroid (urban Colombo/Gampaha; highland vs valley population in Nuwara Eliya/Kandy/Badulla).

### 3.3 Decision-sensitivity re-run (Figure F7 — the primary result)
- [ ] Re-run the **full ladder → calibration → net-benefit** pipeline across **all three builds** (A/B/C), holding everything else fixed (same labels, split, threshold p*).
- [ ] Report ΔAUC, Δcalibration (slope/intercept), and **ΔNB at p\*** attributable to exposure construction, with cluster-bootstrap CIs (reuse the established bootstrap protocol/seed).
- [ ] **Decision-flip count:** for how many unit-weeks does the alert decision (predicted risk vs p*) change sign between builds?
- [ ] **Cross-setting (extra D4):** repeat the contrast (F2) and the decision-sensitivity re-run in **Colombia** — does exposure construction matter more in a large, heterogeneous country than in compact Sri Lanka?
- [ ] **F7**: MAUP/exposure sensitivity on net benefit.

### 3.5 Population-product sensitivity (extra D4 — lowest priority)
- [ ] Rebuild Build B weights under an alternative population product (**GHSL-POP**, and census-only district totals) alongside WorldPop.
- [ ] Recompute ΔNB at p* under each layer; report whether the *choice of population product itself* moves net benefit (a meta-MAUP check). First candidate to trim if the timeline slips.

### 3.6 Spatial structure of miscalibration — decision-flip map (extra D4, WP6 bridge, Figure F8)
- [ ] Regress per-unit calibration slope/intercept (and per-unit ΔNB) on the top geospatial modifiers from the lit review — **urbanisation/built-up, elevation, NDVI, distance-to-surface-water** — to locate where miscalibration and exposure-driven flips concentrate.
- [ ] **F8:** decision-flip / miscalibration map. Keep modifiers strictly **explanatory** (why calibration varies in space), **not** new accuracy predictors — the no-new-model rule holds.

### 3.7 Factor screening — what's in, what's out, and why (all data free)
Every one of the 23 catalogued factors (`dengue_geospatial_risk_factors_review.html`) is screened against four tests: (1) **free & openly downloadable**; (2) derivable at **district × epi-week** (exposure) or **static per district** (F8); (3) fits **role A (exposure)** or **role B (F8 explainer)** — never a new predictor; (4) evidence ≥ moderate *or* near-zero cost. Include-then-prune: bring in what passes, drop later if it carries no signal. Full source-linked table + step-by-step derivation recipes are in **`wp4_wp5_implementation_plan.html` §5**.

**Role A — exposure layer (weekly; all free, transforms of already-held data):**
- Baseline temperature / rain / humidity (ERA5-Land + CHIRPS); elevation → Build C; population → Build B.
- **ADDED:** **DTR** (ERA5-Land `Tmax−Tmin`), **absolute humidity / VPD** (ERA5-Land `t2m+d2m`), **drought index SPI/SPEI** (from CHIRPS; PET from ERA5). Recipes: HTML §5.2. Appended as new columns to every build, row-aligned.

**Role B — F8 miscalibration explainers (static per district; explanatory only; GEE-derived):**
- Built-up/urbanisation (GHSL/WorldCover), elevation, NDVI (MODIS/Sentinel-2), distance-to-surface-water (JRC GSW).
- **ADDED:** **healthcare access** (OSM/HDX distance-to-facility — reporting completeness directly drives miscalibration), **Relative Wealth Index / SES** (Meta RWI on HDX).
- **Optional — freely downloadable, kept to try & prune (drop only if flat):** nighttime lights (VIIRS), TWI/slope (DEM), flood-proneness HAND (DEM), static connectivity gravity index (WorldPop+OSM), land-surface temperature/UHI (MODIS), land-cover fragmentation (WorldCover + edge metric), cropland/rice (WorldCover), forest cover (Hansen/WorldCover), wind speed (ERA5-Land, weekly). Plus **ENSO/IOD** (NOAA) as a **temporal-only stratifier** — spatially constant, so not a district covariate.

**Dropped — ONLY where data is not freely accessible at our resolution (3 factors, reason stated):**
- Human-mobility **live weekly flows** — Meta Data-for-Good / telco flows are gated / not weekly-free. (The free static gravity proxy is kept above.)
- Household water storage — DHS/JMP survey micro-data; not freely mappable at district × week.
- Housing/roof material — DHS or paid very-high-res imagery; overlaps built-up.

**Inclusion rule (per user directive):** keep **every** factor with free, easily-downloadable data (include-then-prune); drop only for a genuine access barrier, and record the reason. This keeps 20 of 23.

**Honest handling for F8 (mandatory with a large panel):** pre-specify every covariate up front, treat as exploratory-explanatory, control the false-discovery rate (report all tried, not just the significant), and never re-import a "significant" covariate as an accuracy predictor.

### 3.4 WP5 acceptance & stop condition
- Both exposure tables accepted by the modeling leads; weighted-vs-naive divergence quantified.
- **Hard stop (honest-null clause, per SOW §N):** if weighted vs naive shows *no* material difference in exposure **and** no material movement in net benefit/decisions, report it as a clean null — *do not manufacture a finding.* A well-characterized null ("exposure construction does not change the decision") is itself a publishable, reviewer-disarming result.

---

## 4. WP4 — Spatially-Honest Cross-Validation (two-country design)

**Goal:** augment the single temporal split with a spatially-honest test in **both** settings, each scheme sized to the number of areas (decision D1), and audit that the external-validation claim survives.

### 4.1 Estimate the autocorrelation range (both settings)
- [ ] Fit the reference model; extract residuals on the outcome grid.
- [ ] Estimate the **residual spatial autocorrelation range** via an empirical variogram and/or Moran's I decay across the adjacency graph — **separately for Sri Lanka and Colombia**.
- [ ] Record each range (in km and in "graph hops") — it sets the buffer width (SL) and the minimum block size (Colombia).

### 4.2 Sri Lanka — buffered leave-one-out (LOOCV)
- [ ] For each of the 26 RDHS, hold it out as the test unit; train on the remainder **minus the held-out unit's within-range neighbors** (the buffer).
- [ ] Record per fold how many units the buffer removes and the resulting train/test sizes — document the power cost honestly.
- [ ] Emit the fold/buffer definition (held-out unit → buffered-out neighbors) as a versioned artifact.

### 4.3 Colombia — spatial block CV
- [ ] Partition municipalities into contiguous spatial blocks with block size **≥ the autocorrelation range** (or use **leave-one-department-out** as the interpretable default), **buffered** so train and test units never sit within-range of each other.
- [ ] Graph-partition the adjacency graph if departments are too coarse or unbalanced; keep folds balanced on outbreak prevalence and number of unit-weeks.
- [ ] Emit **fold-definition files** (unit → fold id) as versioned artifacts.

### 4.4 Leakage audit (memo, both settings)
- [ ] Verify **no train/test neighbor pair** falls within the autocorrelation range (violations = 0 required).
- [ ] Verify **temporal leakage** is still respected inside each spatial fold (lags built from the past only → spatio-temporal CV).
- [ ] Write a short **leakage-audit memo** (named deliverable) covering both schemes.

### 4.5 Re-validation & comparison (both settings)
- [ ] Re-run discrimination + calibration + net-benefit under the spatially-honest CV in each country; compare to the temporal-only split.
- [ ] Report whether the M1-beats-climate / hybrid-increment conclusions **survive** spatial CV (expected: yes — that is the point of the check).

### 4.6 Power caveat (must flag to PI)
- **Sri Lanka at n=26 stays low-powered even with LOOCV:** buffered leave-one-out maximizes training data per fold, but each test fold is a single district and the buffer further shrinks the effective sample. Per SOW §N, treat the SL spatial result as a **compact-country sensitivity companion**, with **Colombia's block CV carrying the well-powered external-validation claim.** Flag both to PI before quoting results.

---

## 4a. Geomatics stress test — value-of-geomatics (optional; PI sign-off)

**Question:** do the geomatics factors actually add *decision value* over the recent-case baseline, and which ones matter? Framed as a **stress test of the existing conclusion**, not a proposed new predictor (stays inside the no-new-model rule; a full standalone geomatics predictor = Paper 2). Plain-language version: HTML §6.

**Three steps:**
1. **Geomatics-only model** using both dynamic factors (temperature, precip, humidity, DTR, absolute humidity, drought index, surface-water extent, NDVI, LST — the time-varying signal) and static factors (elevation, built-up, wealth, distance-to-water — the spatial baseline).
2. **Stability feature-selection** run **inside the WP4 spatial folds** (leakage-proof): repeat over folds, keep factors chosen consistently, report importance with uncertainty. Separate spatial-importance (which district) from temporal-importance (which week). Yields the "which factor matters most" ranking.
3. **Selected-geomatics hybrid** — fold the consistent winners into a hybrid with recent cases (M1); evaluate with the **same AUC + calibration + net-benefit + ΔNB** machinery as the M-ladder.

**Guardrails specific to this test:**
- **No selection leakage:** feature selection and evaluation on disjoint folds (nested CV via the WP4 spatial folds) — else both the "important" set and the score are optimistically biased.
- **No lone winner:** with collinear geospatial factors, importance is unstable → use stability selection, report ranges.
- **Honest-null:** "geomatics adds no decision value over recent cases" is a *thesis-reinforcing* result, not a failure. If geomatics *does* help materially → new finding → Paper 2 territory; escalate to PI.

## 5. Dependencies, sequencing & guardrails

1. **Order:** WP5.1 (build pop-weighted table) → WP5.2/3 (contrast + sensitivity) can proceed independently of WP4. WP4 needs a fitted model for residuals; run after a first model pass.
2. **Freeze discipline:** the new pop-weighted table and fold definitions are new artifacts → checksum + FREEZE_LOG entry before any result is quoted. **Never commit the CSVs/rasters** — code + reports only (`.gitignore` rules).
3. **Reproducibility:** everything scripted raw → table; tooling `exactextractr`/`terra`/`sf` (R) or `rasterio`/`geopandas`/`xarray` (Python).
4. **CRS invariant:** all weighting in equal-area projection; validate zonal means against any station data if available.

**Deliverables checklist:**
- **Exposure tables:** `…_v2_popweighted.csv` (Build B) · `…_v3_terraincorrected.csv` (Build C) · population-product variants of Build B (WorldPop / GHSL / census)
- **Figures:** exposure-contrast **F2** (SL + Colombia) · MAUP net-benefit sensitivity **F7** · decision-flip / miscalibration map **F8**
- **CV artifacts:** SL buffered-LOOCV fold/buffer definitions · Colombia block-CV fold-definition files · **leakage-audit memo** (both settings)
- **Writing:** Methods subsections for WP4 (two-country CV) + WP5 (three-build MAUP, per-variable, cross-setting, population-product)

---

## 6. Brainstorm — candidate additions (open for discussion)

*Seed list. Add / cut / re-prioritize here — this section is meant to grow.*

- **Elevation-corrected temperature (WP2 spillover).** Lapse-rate correct temperature (DEM-based, optionally MODIS-LST-anchored) *before* aggregation. In Sri Lanka's central highlands this may move temperature more than population-weighting does — arguably a *third* exposure build worth adding to the MAUP contrast (naive vs pop-weighted vs terrain-corrected). Big potential result; also more scope.
- **Which variables are MAUP-sensitive?** Precipitation (CHIRPS, convective, spatially patchy) may diverge far more under weighting than temperature (ERA5-Land, smooth). Worth reporting per-variable, not just pooled.
- **Cross-setting MAUP.** Repeat the naive-vs-weighted contrast in **Colombia** too — does exposure construction matter more in a large, heterogeneous country than in compact Sri Lanka? Strengthens generalizability of the WP5 claim.
- **Spatial structure of miscalibration (bridge to WP6).** Regress per-unit calibration slope/intercept on urbanization / elevation / NDVI / surface water — turns WP5 into the WP6 decision-flip map. Where do the exposure-driven flips concentrate?
- **CV design choice.** Compare spatial-block CV vs **leave-one-department/region-out (LODO)** vs rolling-origin + spatial block (spatio-temporal CV). Which is the fair external-validation standard here?
- **Uncertainty propagation.** Carry exposure uncertainty (within-unit dispersion, WorldPop error) *into* the model as measurement error, and see if it widens the net-benefit CIs enough to change conclusions.
- **Sensitivity to population product.** WorldPop vs GHSL vs census-only weights — does the *choice of population layer* itself move net benefit? (A meta-MAUP check.)
- **Boundary-vintage sensitivity.** Does the Kalmunai/Ampara split method perturb any of this? Probably minor, but cheap to confirm.
- **Operational translation.** Express any exposure-driven decision change in the same plain units the paper now uses ("≈ N alert decisions per 100 unit-weeks") so F7 reads as an operational, not abstract, effect.

### Open decisions — SETTLED 2026-07-07 (see §1a)
1. **Spatial-CV setting →** both; SL buffered LOOCV + Colombia block CV. ✅
2. **Exposure builds →** three (naive · pop-weighted · terrain-corrected). ✅
3. **Analysis resolution →** keep 26 RDHS / municipality; no MOH-division. ✅
4. **Scope guard →** all four extras IN. ✅

**In-scope tags for the brainstorm list above:** elevation-corrected temperature = **IN** (Build C) · per-variable MAUP = **IN** · cross-setting MAUP = **IN** · spatial structure of miscalibration = **IN** (F8) · population-product sensitivity = **IN** (lowest priority) · CV design comparison = **partly IN** (the two-country design *is* the comparison). **Paper 2:** uncertainty propagation · human-mobility/connectivity · boundary-vintage sensitivity · rice-paddy/LULC phenology.

---

## 7. Execution sequence (phased — no work started)

**Phase 0 — data staging & sign-off (blocking).**
- PI ratifies the §1a scope.
- Stage the inputs that are **currently outside this checkout** (only a README is on disk here): frozen area-weighted exposure CSV (Build A) · WorldPop rasters · RDHS geometry + adjacency · Colombia municipality boundaries + OpenDengue outcome · DEM (Copernicus GLO-30).

**Phase 1 — exposure builds (WP5.1).** Build B (pop-weighted) → contrast vs A (F2); Build C (terrain-corrected) on top of B; population-product variants of B. Freeze + checksum each; FREEZE_LOG entries.

**Phase 2 — decision-sensitivity re-run (WP5.2/3/5).** Ladder → calibration → net-benefit across A/B/C, per-variable + pooled, SL + Colombia. F7 + decision-flip counts.

**Phase 3 — spatially-honest CV (WP4).** Estimate autocorrelation range (both) → SL buffered-LOOCV folds + Colombia block-CV folds → leakage-audit memo → re-validate → compare to temporal split.

**Phase 4 — geomatics stress test (§4a; optional, PI sign-off).** Geomatics-only model (dynamic + static) → stability feature-selection inside the Phase-3 spatial folds → selected-geomatics hybrid with recent cases → evaluate with the M-ladder calibration + net-benefit machinery. Honest-null accepted.

**Phase 5 — miscalibration bridge (WP6, F8).** Regress per-unit calibration / ΔNB on geospatial modifiers; decision-flip map.

**Phase 6 — write-up.** Methods + results subsections for WP4/WP5 (+ §4a stress test if run); operational translation ("≈ N alert decisions per 100 unit-weeks").

Honest-null clauses (SOW §N) apply throughout: a well-characterized "no change" is a publishable result, not a failure.
