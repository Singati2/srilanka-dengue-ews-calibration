# Study Decision Log

*A running, reverse-chronological record of the study's **new directions, approaches, and decisions** — what changed, why, and what it affects. Maintained by the Geospatial Lead.*

**Update discipline:** append a new dated entry (newest at top) whenever (a) a scope/method decision is settled, (b) the direction or approach changes, (c) a deliverable is produced/frozen, or (d) an open question is opened or closed. Keep it short; link to the spec/report that carries the detail. This log is the single place to answer "what's new and what did we decide?" without re-reading every doc.

**How to read the tags:** `DECISION` = a settled choice · `DIRECTION` = a change in approach/emphasis · `DELIVERABLE` = an artifact produced · `OPEN` = a question raised, not yet closed.

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
