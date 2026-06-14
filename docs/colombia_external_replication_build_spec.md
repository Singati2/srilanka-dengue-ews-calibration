# Colombia External-Replication Build Specification (spec only — build NOT run)
*Pre-specified plan for the **first external-replication arm**: re-fit and re-evaluate the **same decision-evaluation framework** locally in Colombia using OpenDengue weekly Admin2 data. **This is a replication of the framework, NOT transfer of Sri Lanka coefficients.** No build is run here: no models, no labels, no climate linkage, no metrics, no additional downloads. This document is the only proposed commit.*

**Date:** 2026-06-14 · **Status:** specification only · **Base commit:** b0e7566 · **Builds on:** `docs/opendengue_external_validation_feasibility_spec.md` (4d52f21), `docs/opendengue_catalog_inspection_report.md` (fbf0946), `docs/opendengue_extract_coverage_inspection_report.md` (b0e7566), and the Sri Lanka primary pilot/sensitivity/recalibration/CI/DLNM/hybrid/Stage-1A pipeline.

## 0. One-line aim
Test **transportability of the empirical finding** — "recent-cases surveillance is hard to beat operationally; calibration drift is correctable; targeted climate value is threshold/regime-dependent" — by replicating the framework in an independent country with verified weekly subnational data. **Allowed claim:** "the pattern replicated / did not replicate in Colombia." **Forbidden claim:** "Sri Lanka model validated globally," "deployment-ready," any coefficient transfer.

## 1. Data inputs (all to quarantine; read-only; no new download beyond §1.2)
### 1.1 Outcome (already in quarantine — no new download)
- **Source:** `Temporal_extract_V1_3.zip` (OpenDengue V1.3), already downloaded read-only to `~/data_quarantine/opendengue_extract_inspection_v1/`; sha256 `7f5df2174404313a36596342bb26e4614c3c08577fab75550725e195326bcda6`; 54,872,272 bytes.
- **Working tier (frozen at build start):** `adm_0_name == 'COLOMBIA'` ∧ `S_res == 'Admin2'` ∧ `T_res == 'Week'` → **199,458 weekly observations · 989 municipalities · 33 Admin1 departments · 2006–2022**, `dengue_total` 0% NaN among present rows.
- **Panel reality (carried from coverage report):** **unbalanced panel** — only 127/989 municipalities (13%) report in every year; median 14/17 years per unit. Handle as unbalanced (see §4).
- **Date alignment (a strength vs Sri Lanka):** OpenDengue provides `calendar_start_date`/`calendar_end_date` per row → ISO-week alignment is **direct from the file**, removing the WER issue-number↔ISO offset pitfall that required the v2 rebuild in Sri Lanka. Verify start/end span exactly 7 days; reject rows that do not.

### 1.2 Climate exposure (new download, gated separately — NOT in this spec's scope to fetch)
- **Temperature / humidity:** ERA5-Land (hourly→weekly aggregation), global.
- **Precipitation:** CHIRPS (pentad/daily→weekly), global.
- **Aggregation:** municipality-level weekly means via **area-weighted zonal statistics** over Colombia Admin2 polygons (primary); centroid extraction as a documented fallback for slivers.
- **Linkage window:** match each municipality-week to climate at lags **0–8 weeks** (same lag window as the Sri Lanka cross-basis).

### 1.3 Boundaries & (optional) denominators
- **Admin2 polygons:** GADM v4.1 Colombia Admin2 (municipalities) — for zonal stats and the municipality crosswalk.
- **Population denominators (OPTIONAL, only for the incidence-label sensitivity):** DANE municipal population (DIVIPOLA-coded). Not required for the primary label (§3).

## 2. Crosswalk & integrity stop-gates (must pass before any modeling)
1. **Municipality crosswalk:** map OpenDengue `adm_2_name` (+ `FAO_GAUL_code` where present) → GADM Admin2 → DANE DIVIPOLA. **Stop-gate:** if > 5% of weekly observations cannot be matched to a polygon, stop and report; do not silently drop.
2. **Department check:** confirm the 33 Admin1 names map to Colombia's 32 departments + Bogotá D.C. (the verified clean list). **The 42 figure from mixed tiers must not appear in the working data.**
3. **Temporal integrity:** every working row has a 7-day `calendar_start/end`; no duplicate municipality-week rows; flag and resolve any duplicates by the OpenDengue `case_definition_standardised` priority rule (document the rule).
4. **Climate-coverage check:** every retained municipality-week has non-missing ERA5/CHIRPS at all required lags, or is dropped with the drop count logged (no imputation in the primary).
5. **Leakage tripwire:** all thresholds, spline knots, regime cutpoints, and recalibration parameters are estimated on **train rows only**; assert no test row informs any fitted quantity.

## 3. Outcome label (train-only; pre-specified)
- **Primary label (self-contained):** per-municipality **75th-percentile of weekly `dengue_total` (case counts)**, computed on **train-period rows only**; week flagged outbreak if count > that municipality's train 75th pct. Chosen so the arm needs **no denominator sourcing** → keeps the "manageable first arm" property.
- **Sensitivity label S-ext1 (incidence):** if DANE denominators are linked, per-municipality **75th-pct of weekly incidence per 100k** (train-only) — the closest analog to the Sri Lanka RDHS label. Pre-registered as a sensitivity, not the primary.
- **Low-event guard:** municipalities with < 10 train outbreak-positive weeks are flagged unstable and excluded from per-unit estimates (kept in pooled estimates with a flag), mirroring the Sri Lanka low-event handling.

## 4. Unbalanced-panel & feature construction
- Build per-municipality weekly series ordered by `calendar_start_date`.
- **AR features (M1 core):** lagged case counts/incidence at lags needed for the h=4 forecast. Where a preceding week is **absent** (panel gap), the dependent lag is **missing** and that target row is dropped from modeling (no carry-forward in the primary). Log dropped-row counts per municipality.
- **Minimum history:** a municipality enters modeling only if it has ≥ 52 contiguous train weeks (one seasonal cycle) for stable lag/knot estimation; shorter series flagged and excluded (counts logged).
- **Clustering unit:** **municipality (Admin2)** — the bootstrap resampling cluster. Colombia has ~700–830 reporting municipalities/year ≫ 10, so cluster power is ample even after the history filter.

## 5. Models (re-fit locally; canonical R where the Sri Lanka arm used it)
Mirror the Sri Lanka ladder; all coefficients estimated **in Colombia, train-only**:
- **M0 — climatological baseline:** seasonal (week-of-year) outbreak rate only.
- **M1 — recent-cases AR baseline:** lagged cases/incidence (the key operational comparator).
- **M2 — climate-only:** canonical **R `dlnm` 2.4.10** cross-basis `crossbasis(Q, lag=c(0,8), argvar=ns df=3, arglag=ns df=3)` on temperature + precipitation, GLM logistic — same construction validated against the Sri Lanka Python approximation.
- **M3 — climate + season + department FE.**
- **M5 — hybrid:** M1 AR terms + climate cross-basis + season + department (Admin1) fixed effects. (M4 = hybrid without FE, optional, as in Sri Lanka.)
- **Horizon:** **h = 4 weeks primary** (matches Sri Lanka). Secondary h ∈ {1, 8} only if directed (not in primary scope).

## 6. Evaluation (identical metric stack to Sri Lanka)
- **Discrimination:** AUC, PR-AUC.
- **Overall accuracy:** Brier.
- **Calibration:** calibration-in-the-large (CITL), calibration slope; **recalibration** via train-fit Platt and rolling/time-updated recalibration (same as the Sri Lanka recalibration extension).
- **Decision-analytic (primary):** decision-curve **net benefit**; **continuous net benefit**.
- **Primary estimand:** **ΔNB(M5 − M1) at the registered p\* = 0.30**, with **municipality-cluster bootstrap, seed 20260612, B = 1000** (same seed/B as Sri Lanka), reported with 95% CI and proportion of bootstrap > 0.
- **Regime analysis (Stage 1A analog, train-defined):** incidence regime (median split of per-municipality mean train incidence) and AR-strength regime (median split of per-municipality lag-1 autocorrelation); conditional ΔNB by regime; **underpowered flag if < 10 municipalities in a cell** (here unlikely given unit counts — a contrast with the Sri Lanka 26-RDHS limitation, and a reason Colombia adds power).
- **Train/test split (temporal, pre-specified):** **train 2008–2017, test 2018–2022** (2006–2007 reserved for lag warm-up; 2018–2022 gives a multi-year test incl. the 2019 epidemic). **COVID check:** inspect 2020–2021 reporting continuity before locking the split; if a gross discontinuity is found, document and, per the stop rule, prefer a pre-2020 test window — decided from *train-visible diagnostics only*.

## 7. Pre-registration & honesty discipline
- This arm is **pre-specified before running** (this document); fold a one-paragraph addendum into the preregistration noting Colombia as the external-replication arm, the count-based primary label, the temporal split, and the registered p\* = 0.30, **before** the build.
- **Headline lock:** the Sri Lanka headline does **not** change based on Colombia; Colombia is reported as "pattern replicated / partially / not replicated."
- **EWARS-csd Colombia precedent (DOI-verified 2026-06-14):** Schlesinger M, et al. (2024), *Frontiers in Public Health*, "Enabling countries to manage outbreaks: statistical, operational, and contextual analysis of the early warning and response system (EWARS-csd) for dengue outbreaks," **DOI 10.3389/fpubh.2024.1323618** — a municipal-level EWARS-csd validation in Colombia (11 municipalities, Bolívar & Cesar, 2015–2020). **Use only as a precedent** that climate-informed early warning has operational footing in Colombian municipalities — **not** as evidence that this paper's external replication is already done; our arm is a fresh, pre-specified re-fit/re-evaluation with calibration + decision-curve net benefit, which Schlesinger 2024 does not perform.

## 8. Governance (identical to all prior steps)
- All heavy artifacts under `~/data_quarantine/` (climate rasters, polygons, intermediate panels, predictions); outputs **read-only (chmod 444)** with **SHA256** recorded in a local metadata file.
- **Only safe markdown** (this spec, then a build report) is committed; **no CSV/JSON/zip/raster/shapefile** is ever staged.
- Forbidden-file guard run before every commit; separate commits per document for provenance.
- New download (ERA5/CHIRPS/GADM/DANE) is a **separately gated step** — not authorized by this spec.

## 9. Deliverables (when the build is later approved)
1. `docs/colombia_external_replication_report.md` — coverage-after-linkage, model metrics, calibration/recalibration, DCA/net benefit, ΔNB(M5−M1)@0.30 with municipality-cluster bootstrap CI, regime table, and the replication verdict.
2. Quarantined (not committed): linked panel, predictions, metrics/DCA/CI CSVs, R `sessionInfo`, runner scripts, SHA256 metadata.

## 10. Stop rules (report "not feasible / inconclusive" instead of forcing a result)
- > 5% municipality-weeks unmatchable to a polygon; or climate linkage missing for a large fraction of municipality-weeks.
- Train outbreak-positive weeks too few for a stable 75th-pct label across most municipalities.
- A dominant COVID-era discontinuity that makes the 2018–2022 test window unfair (then fall back to a pre-2020 window, decided from train diagnostics).
- Cluster count after the history filter < 10 (not expected for Colombia).

## 11. Honest limitations (stated up front)
- **Replication, not transfer:** no Sri Lanka coefficients are carried; only the *framework* and *registered decision rule* are reused.
- **Counts, not incidence, in the primary label** (denominator-free by design); the incidence label is a pre-registered sensitivity contingent on DANE linkage.
- **OpenDengue case definitions** are standardized but heterogeneous in origin; `case_definition_standardised` is logged and, where mixed within a municipality, resolved by a documented priority rule.
- **Unbalanced panel** (13% present every year) → modeling set is a filtered subset; all drops are counted and reported (no silent truncation).
- **Climate aggregation** to municipality polygons introduces exposure-measurement error (area-weighted zonal stats mitigate, not eliminate).

## 12. Confirmations
- **Specification only.** No build run: **no models fit, no labels created, no climate linkage, no metrics/AUC/calibration/DCA/net-benefit, no additional data downloaded, no data modified.**
- No frozen Sri Lanka outcome/exposure/population, no v1/v2 table, and no prior pilot/sensitivity/recalibration/CI/DLNM/hybrid/Stage-1A output is read, modified, or overwritten by this document.
- **No data files committed** — only this markdown specification is proposed for commit. No external-validation claim is made.
