# Scope of Work — Geomatics Engineer
## Dengue Early-Warning Calibration & Decision-Support Project (Sri Lanka Pilot)

*Standalone briefing. You do not need prior context to act on this document.*

---

## Project in one paragraph
We are **not** building a new dengue model. We take two **existing** model classes off the shelf — (1) a climate-forced mechanistic dengue R0 / Ross–Macdonald / SEIR-SI model and (2) a published DLNM + INLA Bayesian early-warning model — and ask a question nobody has answered for South Asia: *when two early-warning systems have the same statistical accuracy (AUC), do they still lead to different public-health decisions?* Our contribution is **calibration, recalibration, external validation, and decision-curve / net-benefit analysis** of the outbreak alerts, plus **spatial decision-support**. The pilot is **Sri Lanka**, at **MOH-division × epidemiological-week** resolution if the surveillance data supports it, falling back to **district level** only if MOH-level data is not practically accessible.

Your work is the foundation the entire claim rests on. If the climate exposure both models consume is constructed sloppily, our "calibration differences" are just exposure-misclassification artifacts, and the paper dies in peer review. You own making that exposure defensible — and you own turning the abstract result into a map a health ministry can act on.

---

## A. Role title
**Geospatial Lead — Exposure Modeling & Spatial Decision-Support**
(Not "GIS support." You own a scientific work-stream and its results.)

## B. Scientific responsibility
You are accountable for:
1. The **spatially-correct exposure layer** (change-of-support: rasters → areal health units), including its uncertainty.
2. The **spatial validity of the evaluation** (adjacency structure for the spatial model; spatial-block cross-validation that prevents leakage).
3. The **spatial decision-support layer** — where alert decisions flip between models, and what landscape features explain it.

## C. Why your role is central to the paper
- Both models consume **climate aggregated to area-units**. The aggregation method (naive mean vs population-weighted, terrain-corrected) **changes the model probabilities**, hence calibration, hence net benefit. Whoever controls exposure controls the result's credibility.
- A reviewer's first attack will be: *"Your miscalibration is exposure misclassification, not a real model difference."* Your pipeline is the rebuttal.
- Our headline finding — "equal accuracy, different decisions" — is abstract until it is a **map of which divisions flip and why**. That map is yours, and it is what makes the paper operationally useful.

## D. Data layers you own
| Layer | Variable | Purpose |
|---|---|---|
| ERA5-Land | air temp, dewpoint/humidity, precip | mechanistic R0 + DLNM input |
| CHIRPS | rainfall | DLNM input (rainfall lag) |
| MODIS MOD11 | land-surface temperature | temp cross-check / downscaling anchor |
| MODIS MOD13 | NDVI/EVI | vegetation/larval-habitat proxy |
| ESA WorldCover + GHSL | land cover, built-up | urbanization strata |
| JRC Global Surface Water | surface water | breeding-habitat proxy |
| Copernicus DEM / SRTM | elevation | temperature correction + covariate |
| WorldPop | population | exposure weighting + offset/denominator |
| Survey Dept SL boundaries | MOH-division (+ district) | areal units |
| Epidemiology Unit | weekly dengue counts | outcome (interface, not yours to model) |

**Constraint (important):** environmental layers (NDVI, land cover, water, elevation) are used only to (i) improve the climate exposure the existing models already use, (ii) act as strata/effect-modifiers, and (iii) explain *where* miscalibration occurs. They are **not** new predictors added to boost accuracy — that would break our "no new model" design. Do not add features to the forecasting model.

## E. Exact tasks
**WP1 — Acquisition & conditioning.** Acquire all layers; reproject everything to an **equal-area CRS** (SLD99 / Sri Lanka Grid or UTM 44N); repair boundary topology; assign **stable unit IDs**; freeze one boundary vintage for the whole study; quantify per-layer missingness.

**WP2 — Change-of-support exposure (core).**
- Elevation-correct temperature via lapse-rate adjustment (DEM-based, optionally MODIS-LST-anchored) **before** aggregation.
- For each unit × epi-week, compute **population-weighted zonal mean AND within-unit dispersion** (SD/IQR) — carry the heterogeneity, don't discard it.
- Align all time series to **ISO/CDC epidemiological weeks** (match the surveillance calendar exactly).
- Build **DLNM lag matrices** (e.g. 0–12 weeks for temp & rainfall) using only past data.
- Produce **two exposure datasets**: naive areal-mean and population-weighted-corrected.

**WP3 — Spatial structure.** Build and validate the **BYM2 adjacency graph** (queen-contiguity baseline + a distance/mobility-based variant); resolve coastal/border edge effects.

**WP4 — Spatial validity.** Compute residual **variogram/autocorrelation range**; define **spatial-block cross-validation** folds with block size ≥ that range, buffered so neighbors don't straddle train/test.

**WP5 — MAUP / exposure sensitivity (primary result).** Re-run net benefit under naive vs population-weighted exposure; quantify whether exposure construction *alone* flips decisions.

**WP6 — Spatial decision-support (co-author payload).** Map per-unit calibration (slope/intercept) and decision-flips; regress flip-occurrence on urbanization / elevation / NDVI / surface water.

## F. Input files / data sources
- ERA5-Land — Copernicus CDS (hourly → weekly).
- CHIRPS — UCSB Climate Hazards Center (daily → weekly).
- MODIS MOD11/MOD13 — NASA LP DAAC / Google Earth Engine.
- ESA WorldCover (10 m), GHSL built-up — Copernicus / JRC.
- JRC Global Surface Water (30 m).
- Copernicus DEM / SRTM (30 m).
- WorldPop (100 m, vintage matched to study years).
- Admin boundaries — Sri Lanka Survey Department (MOH-division + district).
- Dengue weekly counts — Sri Lanka Epidemiology Unit (provided to you; interface only).

## G. Output files / tables / figures
- **Exposure table** (unit × week × covariate, weighted + naive + dispersion) — the dataset both models consume.
- **Adjacency graph** object (+ variant) and **spatial-block CV fold** definitions.
- **T1** Data sources / resolution / provenance / QA table.
- **T3** Spatial regression: landscape predictors of miscalibration & decision-flips.
- **F1** Study area + surveillance coverage/missingness.
- **F2** Exposure-construction contrast (weighted − naive).
- **F3** Elevation-corrected R0 suitability map (with math lead).
- **F6** Decision-flip map (where the two models disagree).
- **F7** MAUP/exposure sensitivity on net benefit.
- **Memos:** leakage audit; adjacency sensitivity.
- **Pipeline:** scripted, versioned, raw → unit-week table (R `terra`/`sf`/`exactextractr` or Python `rasterio`/`geopandas`/`xarray` + GEE).

## H. Quality-control checks
- **Spatial leakage:** no train/test neighbor pairs within the autocorrelation range; folds buffered.
- **Temporal leakage:** lag windows and composites built strictly from past data; never use an annual NDVI/land-cover composite that injects future months into earlier weeks.
- **CRS/area:** all weighting in equal-area projection; never area-weight in WGS84 degrees. Validate zonal means against any point weather-station data.
- **Boundary-vintage drift:** one frozen admin version; MOH↔district reconciliations explicit; stable IDs across time.
- **Raster QA:** MODIS cloud/gap fraction logged; weeks with excessive missingness flagged; gap-fill method sensitivity-tested.
- **Population vintage:** matched to study period (don't weight 2012 exposure with 2020 population).
- **Edge effects:** no spurious cross-sea adjacency.
- **Reproducibility:** end-to-end re-runnable from raw.

## I. Acceptance criteria
- Exposure table accepted by **both** modeling leads (math + stats).
- Weighted-vs-naive divergence quantified (WP2/WP5).
- Adjacency graph connected, no cross-sea neighbors, sensitivity documented.
- CV folds pass the leakage audit.
- T1, T3 and F1, F2, F6, F7 produced to publication quality.
- Full pipeline re-runs raw → table; QC checklist all green.

## J. Timeline / milestones (effort units, not calendar)
1. **M1 — Data conditioned (WP1):** ~1 unit. Boundaries frozen, CRS harmonized, missingness mapped.
2. **M2 — Exposure table v1 (WP2):** ~2 units. *Blocks all modeling — protect this.*
3. **M3 — Spatial structure + CV (WP3+WP4):** ~1 unit. Hand graph + folds to stats lead.
4. **M4 — MAUP sensitivity (WP5):** ~1 unit. (After first model runs return.)
5. **M5 — Decision-support layer (WP6):** ~1.5 units. (After calibration/net-benefit results return.)

WP2 and WP6 carry the intellectual weight — budget time there, not on WP1.

## K. What counts as co-author-level contribution
- Owning and **writing** WP2 (change-of-support exposure as a reproducible scientific artifact).
- Leading **WP5** (MAUP/exposure sensitivity) as a standalone result.
- Leading **WP6** (spatial structure of miscalibration & decision-flips) and its interpretation.
- Designing **WP4** spatial-block CV and the leakage audit.
- Drafting his Methods subsections + the geospatial figures/tables, approving the manuscript, accountable for the spatial work.
(ICMJE: substantial contribution to design/analysis + drafting + approval + accountability.)

## L. What does NOT count as co-author-level contribution
- Running zonal statistics to someone else's spec and exporting maps.
- Reprojecting/clipping rasters with no analytical decisions (WP1 alone).
- Making figures from results he did not analyze.
- "I downloaded and cleaned the data" without owning WP2/WP5/WP6.
A clean WP1 plus pretty maps = **acknowledgment**, not authorship. The line is producing an intellectual result, not a service deliverable.

## M. How your work connects to the rest of the project
**1. Mathematical R0 / mechanistic model.** The temperature-dependent R0 (thermal-response Ross–Macdonald) is only as valid as its temperature input. Coarse climate over Sri Lanka's central highlands biases R0; your **elevation-corrected, population-weighted temperature** is the physically correct driver. You quantify how much R0 and its outbreak-probability move under correct vs naive exposure.

**2. DLNM / INLA statistical model.** You provide two inputs it cannot run without: the **DLNM cross-basis climate series** (your aggregated, lagged exposure) and the **BYM2 adjacency graph** (the spatial random effect is entirely a function of your neighborhood structure). You also define the **spatial-block CV folds** used for external validation.

**3. Calibration analysis.** Calibration compares predicted outbreak probabilities to observed frequencies. If exposure is misclassified, models look miscalibrated for the wrong reason. Your weighted-vs-naive contrast separates *real* miscalibration from *exposure-artifact* miscalibration — directly defending the core finding.

**4. Decision-curve / net-benefit analysis.** Two contributions: (i) **WP5** shows whether exposure construction *alone* can flip net benefit — making exposure rigor a precondition for the whole decision claim; (ii) **WP6** maps *which* MOH-divisions flip and regresses flips on landscape features, converting an abstract metric into deployable guidance (e.g., statistical EWS in dense urban divisions, mechanistic in highland low-base-rate divisions).

## N. Risks and stop conditions
- **MOH-level data not accessible →** fall back to **district level**; document the resolution loss. (Decision gate at M1.)
- **MODIS cloud cover too high in monsoon →** rely on ERA5-Land for the climate drivers; use MODIS only where QA passes; record the substitution.
- **Surveillance series too short/sparse for variogram & spatial CV →** reduce units or extend years; if neither works, **flag to PI before modeling** — underpowered spatial CV invalidates external validation.
- **Boundary changes within study period →** freeze one vintage and crosswalk; if crosswalk is ambiguous for many units, restrict to stable units.
- **Hard stop:** if weighted-vs-naive exposure produces *no* material difference *and* no spatial structure in miscalibration, WP5/WP6 have null results — report honestly; do not manufacture a finding.

## O. Figure / table ownership
| Item | Description | Owner |
|---|---|---|
| F1 | Study area + surveillance coverage/missingness | **Geospatial Lead** |
| F2 | Exposure-construction contrast (weighted − naive) | **Geospatial Lead** |
| F3 | Elevation-corrected R0 suitability map | Geospatial Lead + math lead |
| F4 | Reliability diagrams + PIT | Stats lead |
| F5 | Decision-curve (net benefit) ± recalibration | Stats lead |
| F6 | Decision-flip map | **Geospatial Lead** |
| F7 | MAUP/exposure sensitivity on net benefit | **Geospatial Lead** |
| T1 | Data sources/resolution/provenance/QA | **Geospatial Lead** |
| T2 | Discrimination/calibration/net-benefit summary | Stats lead |
| T3 | Spatial predictors of miscalibration/flips | **Geospatial Lead** |
| T4 | PROBAST domains | Joint |

## P. Paragraph to send him
> We want you to lead the geospatial exposure-modeling and spatial decision-support work-stream on the Sri Lanka dengue early-warning study — not as GIS support, but as the owner of a scientific component the main result depends on. Concretely: you build the population-weighted, terrain-corrected climate-exposure layer that both the mechanistic and statistical models consume, you construct the spatial adjacency and leakage-proof cross-validation that make our external validation defensible, and you produce the analysis showing *where* the two models' alert decisions diverge and what landscape features explain it. The headline of this paper — that two equally accurate early-warning systems can recommend different public-health actions — is only credible if the exposure is constructed correctly, and only useful if we can map where the decisions flip. Both of those are yours. If you own the exposure pipeline, the MAUP/exposure-sensitivity result, and the spatial decision-support analysis, you are a co-author, not an acknowledgment. Two decisions to settle before you start: (1) whether we work at MOH-division level (preferred) or district level, depending on what surveillance data you can actually get; and (2) confirming the exposure-sensitivity analysis as a primary result of the paper.
