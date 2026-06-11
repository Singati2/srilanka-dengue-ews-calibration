# Preregistration / Analysis Plan v1 — Sri Lanka Dengue EWS Calibration
*Design-locking document, written **before** climate-exposure construction and any modeling. Documentation only. No climate data, no outcome↔exposure linkage, no models, frozen outcome dataset unchanged. Raw/heavy data remain git-ignored in quarantine.*

**Date:** 2026-06-11 · **Status:** pre-exposure design lock (v1). Supersedes the earlier skeleton `osf_prereg_skeleton.md` for the now-finalized backbone; the skeleton's prior-work positioning still applies.

---

## A. Study title and objective
**Title:** *Discrimination is not deployment: calibration and decision-curve evaluation of climate-driven dengue early-warning systems in Sri Lanka.*
**Objective:** Test whether two **existing** climate-driven dengue early-warning approaches with comparable discrimination (AUC) lead to **different public-health alert decisions** under calibration and decision-curve / net-benefit analysis across Sri Lanka's RDHS units, 2018–2025. **No new forecasting model is proposed**; the contribution is empirical, regional, and decision-analytic (external validation + calibration + recalibration + net benefit + spatial decision-support). Prior work (Tozan 2023 net-benefit/cost-loss; Gerlee 2026 cost-loss; Johansson 2019 dengue forecasting) is conceded and cited.

## B. Study design
Retrospective **observational** evaluation on a **Sri Lanka RDHS × epidemiological-week panel**, **2018–2025**. No intervention; secondary use of public aggregate surveillance + open climate/population data. Evaluation compares existing model classes on held-out, rolling-origin out-of-sample forecasts.

## C. Spatial unit
- **26 RDHS units** (Regional Director of Health Services areas).
- **Geometry source:** HDX COD-AB Sri Lanka (Survey Department), ADM2 districts + ADM3 DS divisions, EPSG:4326, CC BY-IGO, v03 (valid 2022-08-16). Local geometry `rdhs_26_v1.gpkg` (sha256 `9e5e2c0a…`), QC-clean (areas conserved, 0 invalid).
- **Build rule:** 24 RDHS = districts 1:1; **Kalmunai RDHS = dissolve of 12 DS divisions**, **Ampara RDHS = dissolve of 7 DS divisions** (official RDHS-Kalmunai MOH list; 13 MOH areas → 12 DS because Kalmunai DS = Kalmunai North + South MOH).
- **Crosswalk:** `geomatics_templates/rdhs_crosswalk_template.csv` keyed by `geometry_id` (24 ADM2 p-codes + `LK52K` Kalmunai + `LK52A` Ampara); name aliases recorded (`Killinochchi↔Kilinochchi`, `Moneragala↔Monaragala`).

## D. Temporal unit
**Epidemiological week / WER issue**, ISO/CDC-week aligned, **2018–2025** (8 years; Vol 45–52). Population denominators are annual (Section F).

## E. Outcome
- **Primary outcome:** weekly **dengue current-week case counts** per RDHS (WER Table 1, column A), from the **frozen** dataset `wer_dengue_currentweek_rdhs_2018_2025_v2.0-frozen.csv` (sha256 `99f0b9b1…`, 10,790 rows, 0 invalid, manual-QC 0 mismatches).
- **Cumulative counts (column B): QC-only, NOT an analysis field** (year-1/2 carryover + ~68 mid-year extraction anomalies; not validated).
- **Documented missingness (frozen, accepted):** 33 NA cells (Gampaha 2018 wk23–52 ×30; Puttalam 2019 wk23 / 2021 wk45 / 2021 wk50 ×3) from source-PDF text-layer loss; **1 missing issue: 2022 wk44** (absent from the archive). These are documented, not imputed (Section M).

## F. Population denominator
- **District-anchored rescaled WorldPop denominators**, `rdhs_population_worldpop_district_rescaled_2018_2025.csv` (sha256 `e4585741…`, 208 rows).
- **Source/anchor:** WorldPop G2 R2025A constrained 100m (zonal-sum per RDHS) for the annual trend; **anchored to the 2024 Census** district totals (national 21,781,800 exact). Formula: `pop_adj(d,y)=Census2024(d)×WP(d,y)/WP(d,2024)`; Ampara/Kalmunai split preserved from WorldPop ratio.
- **Temporal rule:** one denominator per **RDHS-year**, **constant within each epidemiological year**. **No weekly interpolation.**
- Rationale: WorldPop's district bias is spatially uneven (−13% to +24%); a national rescale was rejected in favor of district anchoring.

## G. Spatial adjacency
- **Queen contiguity**, **26 nodes / 60 edges**, all real shared land borders (≥ 984 m), **0 cross-sea links**, **1 connected component** (BYM2-ready). Degree min/median/max = 2/4/9. Keyed by `geometry_id`; matches the crosswalk exactly.
- Kalmunai neighbors: Batticaloa, Ampara (degree 2, coastal — justified). Local artifacts: `rdhs_26_adjacency_edges.csv`, `…_neighbors.json` (quarantined).

## H. Exposure plan (climate — to be acquired LATER, not yet done)
- **Candidate sources:** **ERA5-Land** (temperature, humidity/dewpoint) and **CHIRPS** (precipitation); optionally MODIS LST/NDVI for cross-checks. To be confirmed in a separate climate-source reconnaissance.
- **Aggregation:** RDHS × epi-week exposure via **population-weighted** zonal aggregation (with a naive area-weighted version retained for MAUP sensitivity); temperature elevation-corrected before aggregation. CRS reconciled to the RDHS geometry.
- **Lag structure:** distributed-lag (DLNM cross-basis) windows (e.g., 0–12 weeks) to be **fully specified before modeling** and frozen with the exposure table.
- **Hard rule:** climate download, exposure construction, and outcome↔exposure linkage are **out of scope for this document** and require explicit approval.

## I. Modeling scope
- Evaluate **existing early-warning approaches only**:
  1. **Mechanistic:** a published climate-forced R0 / Ross–Macdonald / SEIR-SI model (Mordecai/Huber thermal responses) → outbreak-probability via a pre-registered R0→P link fitted on training folds only.
  2. **Statistical:** a published **DLNM + INLA BYM2** Bayesian early-warning model (EWARS-csd / Lowe family) using the adjacency graph (G).
- **No new forecasting model is claimed.** Baseline/reference = the standard "alert-always / alert-never" strategies and a seasonal-naïve benchmark. Focus is **calibration, recalibration, and decision value**, not maximizing discrimination.

## J. Primary evaluation metrics
- **Primary:** **decision-curve / net-benefit analysis** at policy-relevant thresholds (operational metric), plus **probabilistic calibration** — reliability diagrams, PIT, **calibration-in-the-large**, **calibration slope**, **Brier score** (with decomposition).
- **Recalibration arm:** isotonic / Platt fit on training folds, applied to test; re-evaluate calibration + net benefit.
- **Secondary:** **discrimination** (AUC + CI) and sharpness (CRPS). Discrimination is explicitly *not* the deciding metric.
- **Headline test:** two models with statistically indistinguishable AUC that **differ in net benefit at the operational threshold** (a deployment decision flip), with the gap surviving recalibration.

## K. Alert-threshold policy
- **Outbreak definition (primary):** week exceeding the historical (pre-period) moving 75th-centile endemic-channel threshold per RDHS, computed from seasons strictly preceding each origin (leakage-safe).
- **Decision threshold(s):** decision-curve net benefit evaluated across a **policy-relevant threshold-probability band**, with a **primary cost-anchored threshold** `p* = C/(C+L)` derived from **external** vector-control-vs-missed-outbreak cost inputs (Tozan/Lee), set **before** seeing results.
- **No post-hoc threshold tuning** on the outcome data.

## L. Spatial decision-value analysis
- **Decision-flip mapping by RDHS:** where the two models recommend different actions at `p*`.
- **Net benefit by threshold**, per RDHS and pooled; reliability/calibration by RDHS.
- **Maps produced after model evaluation** (not before), using the frozen geometry; flip occurrence regressed on landscape covariates (urbanization, elevation, NDVI) as exploratory spatial decision-support.

## M. Missing-data policy
- **Outcome gaps:** the 33 NA cells + 2022 wk44 are **flagged, never silently imputed**; analyses report them and run with/without affected RDHS-weeks as a robustness check.
- **Climate missingness:** raster gap fractions documented; gap-fill method pre-specified and flagged; weeks failing QC excluded transparently.
- **Population:** complete (208/208); no imputation needed.
- **Principle:** no silent imputation anywhere; every fill is flagged and sensitivity-tested.

## N. Sensitivity analyses
- **Denominator:** raw WorldPop vs **census-rescaled** (primary) — confirm relative incidence/decision conclusions are robust to the denominator choice.
- **Adjacency:** base queen graph vs the sub-1 km-edge or point-touch variants (report-only; expected connected).
- **Lag window:** alternative DLNM lag spans.
- **Outbreak threshold / cost ratio:** vary the endemic-channel centile and the cost-anchored `p*` across the plausible band.
- **MAUP / exposure construction:** population-weighted vs area-weighted exposure (when exposure is built).

## O. Go/no-go criteria
- **Supports a publishable pilot (GO):** matched discrimination (ΔAUC 95% CI includes 0) **and** a material net-benefit difference at `p*` (CI excludes 0, exceeds a pre-set minimal important difference) **and** the gap **survives recalibration** **and** the flips are spatially coherent.
- **Downgrade to a methods/data note:** no decision flip, or the AUC-better model is also net-benefit-better everywhere, or recalibration erases the gap → report as a calibration-reporting-standards / data-resource contribution, not the headline.
- **Stop modeling escalation:** if the pilot (single hardened pass) shows no material, recalibration-robust decision difference, **do not escalate** to broader model/feature search — report the null honestly.

## P. Reproducibility & data governance
- **GitHub contains documentation, scripts, and small templates only.** Raw/quarantined data (WER PDFs, frozen outcome CSV, geometry GPKG, WorldPop rasters, census tables, denominator/adjacency files) are **git-ignored** and never committed.
- **Checksums + metadata** recorded for every frozen artifact (outcome `99f0b9b1…`, geometry `9e5e2c0a…`, denominators `e4585741…`).
- A **forbidden-file guard** is run before every commit.
- **Public data-release decision deferred** (data are governed by source terms — Epidemiology Unit / WorldPop CC BY 4.0 / COD-AB CC BY-IGO / Census). The institutional data request remains optional/upside.

## Q. Exact next step after this preregistration
1. **Climate-source reconnaissance** (ERA5-Land + CHIRPS): products, versions, coverage 2018–2025, licenses, access — **documentation/metadata only, no bulk download** without approval.
2. Then (on approval): climate acquisition → **population-weighted RDHS × epi-week exposure table** → freeze the exposure table (checksum) → specify/freeze DLNM lag windows.
3. **No modeling until the exposure table is frozen** and this plan is registered.

*Design lock: spatial unit, temporal unit, outcome, denominators, adjacency, primary metric (net benefit at cost-anchored `p*`), threshold policy, and go/no-go are fixed here, before any climate/exposure or modeling work.*
