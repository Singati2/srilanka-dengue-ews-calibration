# Study Decision Log

*A running, reverse-chronological record of the study's **new directions, approaches, and decisions** — what changed, why, and what it affects. Maintained by the Geospatial Lead.*

**Update discipline:** append a new dated entry (newest at top) whenever (a) a scope/method decision is settled, (b) the direction or approach changes, (c) a deliverable is produced/frozen, or (d) an open question is opened or closed. Keep it short; link to the spec/report that carries the detail. This log is the single place to answer "what's new and what did we decide?" without re-reading every doc.

**How to read the tags:** `DECISION` = a settled choice · `DIRECTION` = a change in approach/emphasis · `DELIVERABLE` = an artifact produced · `OPEN` = a question raised, not yet closed.

---

## 2026-08-05 — M6 moved from plan to build: Python notebook workflow, batches A and C extracted

**Context.** Started implementing the M6 geomatics-only model (`docs/M6.md`) as a step-by-step Jupyter workflow rather than a script, so every intermediate is inspectable. This is **new work only** — it does not touch, port or re-run the frozen v6 pipeline the manuscript's reproducibility claim rests on (`v6-analysis-frozen`, `alt-stats-results-v1/v2`, seed 20260612).

**`DECISION` — spec conflict resolved in favour of `M6.md`.** `M6.md` §0 defines M6 as geomatics-only with *no reanalysis climate*, while `maup_sensitivity_and_spatial_cv_plan.md` §4a lists temperature/precipitation/humidity among the geomatics factors. The notebooks follow **`M6.md`**: admitting reanalysis climate would collapse M6 into "M2 plus extras" and make the research question unanswerable. Dynamic *remotely-sensed* layers (LST, NDVI, surface water, nightlights) are in — they are satellite observations, not reanalysis.

**`DECISION` — no Google Earth Engine.** All layers come from anonymous public downloads: Copernicus GLO-30 via AWS Open Data, MODIS via Microsoft Planetary Computer STAC. Pinned granule IDs plus checksummed local rasters are more reproducible than a GEE run, whose collections can be revised underneath you. Supersedes the 2026-07-07 note adopting GEE as the derivation environment.

**`DECISION` — CRS correction to the plan.** `maup_sensitivity_and_spatial_cv_plan.md` §5 recommends SLD99 or UTM 44N for area weighting; **both are transverse Mercator — conformal, not equal-area.** The notebooks use a Lambert azimuthal equal-area projection centred on the island for all area-bearing computation. Measured effect for Sri Lanka is small (per-unit area error −0.044% to −0.080%) but it is the correct default and will matter more for Colombia, which spans far more latitude.

**`DECISION` — batch C (dynamic) built before batch B (static).** Most M6 variables are static per district, and a model built only from those emits one constant prediction per district for every week: against a weekly label it can express *which* districts differ but never *when*, so it scores near chance **by construction**. That null would be structural, not empirical, and must not be reported as "geomatics carries no signal". The dynamic layers decide whether M6 is answerable at all, so they were settled first.

**`DECISION` — MODIS extraction rules** (recorded because each alternative fails silently):
- **Terra only.** `modis-11A2-061` and `modis-13Q1-061` each contain *both* Terra (`MOD*`, ~10:30 overpass) and Aqua (`MYD*`, ~13:30). Selection is on the product id prefix — not the STAC `platform` field, which is empty for some items. Aqua is a legitimate later gap-filling sensitivity as a **separate column**, never merged into the Terra one.
- **Duplicate granules resolved to newest `created`** (21 LST, 12 VI reprocessing pairs), so selection is deterministic rather than arrival-ordered.
- **LST QA = mandatory QA ≤ 1 AND average error ≤ 2 K**, adopted after measuring the alternatives. Mandatory-QA-0-only retains 14–42% of land pixels and empties whole districts; worse, what it drops is the cloudy, wet weeks — biasing the series warm and dry in exactly the conditions a dengue model cares about.
- **No resampling of the data.** Zonal reduction happens on the native MODIS sinusoidal grid (itself equal-area); the geometry is reprojected to the data once instead of the data being warped 700 times.

**`DELIVERABLE` — three executed notebooks** (`notebooks/`, outputs committed; feature tables stay in gitignored `data_quarantine/m6_geomatics/`):
- **00 — spatial frame.** Independently reproduces the recorded 26-node/60-edge queen adjacency and the `rdhs_26_v1.gpkg` checksum (9e5e2c0a).
- **01 — batch A terrain.** Elevation, slope, TWI, HAND for all 26 RDHS from Copernicus GLO-30. Cross-checks: max elevation 2,514 m vs Pidurutalagala 2,524 m; raster land area 66,040 km² vs vector 66,041 km². **Finding: batch A is strongly collinear** — 19 of 28 pairs exceed |r| > 0.8, so eight terrain features span roughly two independent dimensions. Feature importance will be unstable; stability selection is required, as §4a anticipates.
- **02 — batch C dynamic.** MOD11A2 LST day/night (8-day, 1 km) and MOD13Q1 NDVI/EVI (16-day, 250 m), 2017-11 to 2025-12, with per-unit coverage carried alongside every mean. Window starts 2017-11 so an 8-week lag exists for the first 2018 epi-week.

**`OPEN` — leakage rule for the temporal join, to be enforced in assembly.** An 8-day composite dated 2020-06-01 summarises 2020-06-01 to 06-08; joining it to the epi-week beginning 06-01 puts post-week observations into a predictor. Assembly must use only composites whose **end** date precedes the week being predicted, then lag 0–8 weeks from there (mirroring M2). Relatedly, **cloud gaps must be filled with past data only** — `interpolate()` across a gap reaches into the future. Composite start *and* end dates are carried in the frozen tables so this can be enforced.

**`DELIVERABLE` — notebook 03, batch B statics** (executed same day). Land cover, fragmentation, surface water, population and nightlights for all 26 RDHS; 18 features. Sources: Impact Observatory `io-lulc-annual-v02` (10 m, annual 2018–2023), JRC GSW v1.4, WorldPop UN-adjusted, HREA.

**`DECISION` — two substitutions, both under the "genuine access barrier / document it" rule:**
- **`io-lulc-annual-v02` replaces ESA WorldCover** for built-up/forest/cropland. WorldCover has only 2020 and 2021 epochs; vintage is the binding constraint (below). One classification then supplies three variables consistently.
- **HREA replaces monthly VIIRS DNB** for nightlights. EOG's monthly composites need a registered account. HREA is the same sensor, hosted anonymously, but **annual** — so nightlights drops from a dynamic layer to a slow one. Moot in practice: HREA ends 2019.

**`OPEN` → `DECISION` — the vintage gate cannot be met, so it is reported instead.** `M6.md` §6 requires each layer's year to match the analysis window. **No batch-B source reaches the end of the 2018–2025 window**: land cover ends 2023, population 2020, nightlights 2019, surface water is a 2020 epoch. Resolution: build annually where possible, carry the last year forward, and **publish the carry-forward table** (notebook 03 §11) so a reader sees which district-weeks rest on extrapolation.

**`DIRECTION` — do NOT join land cover year-by-year; use a single epoch.** This reverses the plan's assumption. Measured in notebook 03 §4: island built-up runs 16.7% (2018) → 18.5% (2020) → 17.3% (2023), **0 of 26 districts move monotonically**, and median year-to-year movement (0.76 pp) is comparable to net change across the whole record (0.94 pp). Settlement does not un-build, so most of the annual variation is the classifier relabelling the same ground. A year-matched join would feed reclassification noise to the model as if it were urbanisation. Jaffna and Killinochchi are the genuine exceptions (~1.1 pp/yr, post-conflict resettlement). Per-year tables frozen anyway as the evidence, and to keep the call reversible.

**`DIRECTION` — the urban heat island is absent at 26-district resolution, and that is a MAUP result, not a data error.** Notebook 03 §10 cross-checks batch B against A and C; four relationships hold strongly between products sharing no inputs (trees~NDVI +0.87, NDVI~LST −0.79, nightlights~built-up +0.93, pop-density~built-up +0.91). Built-up~daytime-LST is ~**+0.05**. Elevation is *not* the confounder (corr(built-up, elevation) ≈ −0.03, partial correlation unchanged): district-mean LST is governed by moisture/vegetation, and the dry zone is hot with almost no built-up, cancelling Colombo. The UHI is a few-km phenomenon inside units averaging ~2,500 km². **This is the study's own MAUP thesis appearing in its covariates** — a real physical effect erased purely by the choice of areal unit. Consequence: an M6 null on built-up means "invisible at this unit", never "no urban effect", and M6 feature importances must not be read as mechanism.

**`OPEN` — population denominator loses ~3.5% at the coast.** WorldPop totals inside the 26 RDHS polygons are 20.9–21.1 M against ~21.4–21.9 M nationally; pixels are assigned whole to the unit containing their centre and Sri Lanka is all coastline. Quantified in notebook 03 §7 as a capture fraction. **This propagates directly into WP5's population-weighted exposure build**, whose denominator is the same quantity, and the affected districts are the dense coastal ones. Needs a decision in WP5: accept and report, or switch to fractional-coverage weighting at the boundary.

**`OPEN` — still outstanding for M6:** batch D (healthcare access, relative wealth, connectivity, rice-paddy phenology). Note that `M6.md` §9.5's interim gate — fit M6 on batch A + B before the full ladder — is now known to be **structurally unrunnable as written**: A + B are entirely static, so against a weekly label they cannot express *when* (notebook 02 §15). The honest version tests A + B against a cross-sectional baseline, not a weekly one. Modelling (notebooks 05–08) remains **blocked on outcome-table staging**, unchanged from 2026-07-07.

---

## 2026-07-07 — Scope for WP4/WP5 locked; plan promoted from draft to phased

**Context.** Resumed the geospatial work-stream (WP4 spatial cross-validation, WP5 MAUP/exposure sensitivity). The geospatial risk-factor literature review (`dengue_geospatial_risk_factors_review.html`, 59 sources, produced 2026-07-02) was in hand and informed the calls below.

**`DECISION` — four open scope questions settled** (detail + rationale in `maup_sensitivity_and_spatial_cv_plan.md` §1a):
- **D1 — Cross-validation setting: BOTH countries, scheme sized to n.** Sri Lanka (26 RDHS) → **buffered leave-one-out (LOOCV)** — hold out one district, drop its within-range neighbors from training to stop leakage. Colombia (~1,000 municipalities) → **spatial block CV** (leave-one-department-out). Colombia carries the well-powered external-validation claim; SL is the compact-country sensitivity companion. Temporal honesty (past-only lags) preserved inside every fold → spatio-temporal CV.
- **D2 — Three exposure builds**, a nested ladder each adding one refinement: **A** area-mean (exists) → **B** population-weighted → **C** elevation/lapse-rate–corrected temperature (Copernicus GLO-30 DEM, −6.5 °C/km start). Terrain correction promoted from "brainstorm/maybe" to in-scope because elevation is the top-ranked geospatial *modifier* in the lit review and should move temperature most in the central highlands.
- **D3 — Resolution stays at 26 RDHS / municipality.** No re-extraction to MOH-division (would require rebuilding the frozen outcome table).
- **D4 — All four extras IN this paper:** per-variable MAUP (precip vs temp) · spatial-structure-of-miscalibration map (WP6 bridge, F8) · cross-setting MAUP (repeat weather contrast in Colombia) · population-product sensitivity (WorldPop vs GHSL vs census; lowest priority, first to trim).

**`DIRECTION` — deliberately comprehensive paper.** D4 accepts the full extras set rather than deferring most to "Paper 2." Paper-2 backlog now: uncertainty propagation, human-mobility/connectivity, boundary-vintage sensitivity, rice-paddy/LULC phenology.

**`DELIVERABLE` — plan doc promoted.** `maup_sensitivity_and_spatial_cv_plan.md` moved from *DRAFT — for discussion* to *SCOPE LOCKED* with: a new §1a (locked decisions), three-build WP5 (§3.1/3.1b + per-variable/cross-setting/population-product/F8 subsections), a two-country WP4 (§4.2 SL buffered LOOCV, §4.3 Colombia block CV, §4.6 power caveat), an expanded deliverables checklist, and a new §7 phased execution sequence (Phase 0 data staging → Phase 5 write-up).

**`DELIVERABLE` — HTML implementation plan.** `wp4_wp5_implementation_plan.html` — self-contained, browser-friendly rendering of the plan in the project's house style (locked decisions, three-build ladder, two-country CV side-by-side, phased sequence, guardrails). Now also carries **plain-language "In plain language" notes** on the builds, the CV design, and each of the four extras. Markdown plan remains source of truth if the two ever disagree.

**`DIRECTION` — lit-review factors mapped to plan roles.** Reconciled the 23-factor geospatial review with the plan under the no-new-model rule (HTML §5; MD plan §3.7). A factor may enter **only** as (A) exposure construction [elevation→Build C, population→Build B] or (B) an F8 miscalibration explainer [urbanisation, elevation, NDVI, distance-to-surface-water]; the other 14 factors are logged for Paper 2.

**`DECISION` — all 23 lit-review factors screened against 4 tests (free data · district×week derivable · role A/B only · evidence-worth-it); include-then-prune.** Resolves the earlier "three candidates" open item. Detail + source-linked table + step-by-step recipes in HTML §5; MD plan §3.7.
- **Added to the exposure layer (weekly, free, transforms of held data):** DTR, absolute humidity/VPD, drought index SPI/SPEI. *(The three former candidates are now IN.)*
- **Added as F8 map covariates (static per district, free):** healthcare access (OSM/HDX distance-to-facility — reporting completeness drives miscalibration), Relative Wealth Index/SES (Meta RWI on HDX).
- **Optional — kept, freely downloadable, prune if flat (10):** nightlights (VIIRS), TWI/slope (DEM), flood-proneness HAND (DEM), static connectivity (WorldPop+OSM), land-surface temp/UHI (MODIS), land-cover fragmentation (WorldCover), cropland/rice (WorldCover), forest (Hansen/WorldCover), wind (ERA5-Land), + ENSO/IOD as a temporal-only stratifier.
- **Dropped → Paper 2 — ONLY 3, all for non-free data (reason stated):** mobility live weekly flows (gated Meta/telco), household water storage (DHS/JMP survey micro-data), housing/roof (DHS/paid VHR imagery).

**`DIRECTION` — geomatics stress test added to the plan (optional, PI sign-off).** User proposed a geomatics-only model → feature-importance → selected-geomatics hybrid. Reconciled with the no-new-model rule by framing it as a **value-of-geomatics stress test** of the existing conclusion (not a proposed predictor): 3 steps (broad geomatics-only model incl. dynamic + static factors → **stability feature-selection inside the WP4 spatial folds** → selected-geomatics hybrid with recent cases, judged by the M-ladder calibration + net-benefit lens). Key guardrails flagged: **no selection leakage** (nested CV via the spatial folds), **no lone winner** (importance unstable under collinearity → stability selection + ranges), honest-null accepted. If geomatics *materially* helps → that's a new finding = Paper 2, escalate to PI. Plain-language write-up: HTML §6; spec: MD plan §4a; new execution Phase 4. **`OPEN`: awaiting PI sign-off before this rung is run.**

**`DIRECTION` — max-inclusion of freely-downloadable factors (user directive, supersedes the earlier evidence-based drops).** Keep **every** factor whose data is free and easily downloadable (include-then-prune); drop **only** for a genuine access barrier, with the reason recorded. This moved 6 previously-dropped-but-free factors (land-surface temp, fragmentation, cropland, forest, wind, ENSO/IOD) back to OPTIONAL — now 20 of 23 kept, 3 dropped. Larger optional panel → mandatory pre-specification + FDR control (F8 stays exploratory-explanatory). Google Earth Engine adopted as the free derivation environment for the static covariates.

**`OPEN` / blocking before any implementation:**
1. **PI ratification** of the §1a scope.
2. **Data staging** — this checkout holds only code + docs; every input (frozen Build-A exposure CSV, WorldPop rasters, RDHS/Colombia geometries, OpenDengue outcome, DEM) lives outside the repo and must be staged before Phase 1.

**Guardrails reaffirmed:** no data committed (code + reports only); honest-null clause (SOW §N) — a well-characterized "exposure construction doesn't change the decision" is a publishable result, not a failure; geospatial modifiers stay *explanatory* (miscalibration), never new accuracy predictors (no-new-model rule).

---

## Prior context (pre-log, for continuity)

- **2026-07-02 — `DELIVERABLE`:** geospatial & remotely-sensed dengue risk-factor literature review (`dengue_geospatial_risk_factors_review.html`, 59 sources) — ranked catalogue of geomatics-derivable drivers/modifiers/confounders to guide the exposure-layer extension.
- **2026-07-01 — `DELIVERABLE`:** `study_guide.html` (plain-language onboarding) and the first draft of `maup_sensitivity_and_spatial_cv_plan.md`.
- **Standing study finding (from the manuscript, in major revision):** recent case counts (M1) beat climate-only early-warning models; climate adds only a small hybrid increment (M5) — confirmed in Colombia, not in Sri Lanka. Paper's headline: *two equally accurate warning systems can recommend different public-health actions* — evaluated via calibration + decision-curve / net-benefit. Target: PLOS NTDs.
