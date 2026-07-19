# Analysis Plan v2 — Pre-registration + Implementation Blueprint
## Selected-feature geospatial hybrid, spatially-honest validation, and MAUP sensitivity (single-paper)

*Status: **DRAFT to be frozen before any modeling.** Companion to (does not replace) `single_paper_integrated_plan_v1.md`. Ambition dial DECIDED 2026-07-07: **selected-feature hybrid (spine)**. Placeholders marked **[PI]** are author-owned parameters to confirm; recommended defaults are given. Nothing here is implemented, committed, or pushed.*

> **How to use this document.** Part I is the pre-registration — freeze it (repo tag + OSF) *before* looking at any test-set performance. Part II is the build order. Parts III–VI are endpoints, reproducibility, risk controls, and sign-off. Once Part I is frozen, no change to it is allowed without a dated amendment logged in `study_decision_log.md`.

---

# PART I — PRE-REGISTRATION (freeze before modeling)

## 1. Objective and hypotheses

**Question.** Does a recent-surveillance model augmented with a *small, pre-selected* set of geospatial features improve **calibrated decision value** (decision-curve net benefit) over recent surveillance alone, under spatially-honest validation?

**Primary confirmatory hypothesis (H1).** In **Colombia**, the hybrid (M1 + selected geospatial features) has ΔNB(hybrid − M1) at p\*=0.30 with a cluster-bootstrap 95% CI **excluding 0**, evaluated on **outer spatial-block CV folds**.

**Co-primary robustness (H2).** The benchmark ordering established in v18 (recent-case M1 ≥ climate-only models on net benefit) **survives** spatial-block CV (i.e., is not an artifact of the single temporal split).

**Directional note.** A null on H1 ("geospatial augmentation does not beat recent surveillance on decision value") is a **valid, headline-consistent result** and will be reported as such (honest-null, §10).

## 2. Design

| Element | Specification |
|---|---|
| Settings | **Colombia** (~1,000 municipalities) — *primary/powered*; **Sri Lanka** (26 RDHS) — *confirmatory/sensitivity companion only* |
| Unit | municipality-week (Colombia) / RDHS-week (Sri Lanka) |
| Outcome/label | elevated-activity flag at the **75th-percentile** historical level (primary), h=**4**-week horizon — *identical to v18; do not redefine* |
| Reference threshold | p\*=**0.30** (primary); grid {0.20, 0.30, 0.34, 0.40} exploratory |
| Temporal split | as in v18 (Colombia train ≤2017 / val 2018–19 / test 2020–22; SL as frozen) — retained for comparability with the benchmark |
| Spatial validation | **nested spatial-block CV** (§8), the new out-of-sample engine |
| Governing discipline | **no-new-model rule is retired**; replaced by R1–R5 (pre-registration, nested leakage-proof CV, Colombia-led power, one confirmatory contrast, honest-null) |

## 3. Estimands (locked)

- **Primary (confirmatory, 1 contrast):** ΔNB(hybrid − M1) @ p\*=0.30, h=4, 75th-pct, Colombia, **outer-fold spatial CV**, cluster-bootstrap 95% CI.
- **Co-primary robustness:** spatial-CV vs temporal-split ranking of M0–M3 vs M1 (discrimination, calibration, NB).
- **Secondary/exploratory (FDR-controlled, §9):** MAUP ΔNB across exposure builds A/B/C; per-variable MAUP divergence; stability-selected factor-importance ranking; spatial structure of miscalibration (F8); Sri Lanka companion; threshold/horizon grids; population-product sensitivity.
- **Not estimated:** any formal cross-country heterogeneity/interaction test (no defensible common estimand); cases/lives/costs prevented; deployment readiness.

## 4. Exposure builds (pre-defined)

Nested ladder, each adds one refinement; all weighting in an **equal-area CRS**; every build **row-aligned** to the existing keys and checksummed.

- **Build A** — area-mean (exists; the v18 baseline).
- **Build B** — population-weighted (WorldPop, fractional-cell overlap, population vintage matched to exposure year; carry within-unit SD/IQR).
- **Build C** — terrain/lapse-rate-corrected temperature (Copernicus GLO-30 DEM, −6.5 °C/km default, corrected at fine grid *before* aggregation; same population weighting as B; temperature-only change). **[PI]** Build C is a scope dial — include if timeline allows.

## 5. Candidate feature panel (pre-registered — Colombia-led)

Only features listed here may enter the hybrid; nothing added later. Static factors are **F8 explainers**; **dynamic factors are the hybrid candidate pool.** All free/open; transforms specified.

**Dynamic candidate pool (weekly; eligible for the hybrid):**
| Feature | Source | Transform |
|---|---|---|
| Temperature (mean/min/max) | ERA5-Land | lag set as in v18 |
| Precipitation | CHIRPS | lag set as in v18 |
| Humidity (RH/d2m) | ERA5-Land | lag set as in v18 |
| **DTR** (diurnal temp range) | ERA5-Land Tmax−Tmin | weekly mean, lagged |
| **VPD / absolute humidity** | ERA5-Land t2m+d2m (Magnus) | weekly mean, lagged |
| **Drought index SPI/SPEI** | CHIRPS (+ERA5 PET) | 1/3/6-month, mapped to weeks, lagged |

**Static F8 explainers (per-unit; explanatory only, NOT hybrid inputs):** built-up/urbanisation (GHSL/WorldCover), elevation (DEM), NDVI (MODIS), distance-to-surface-water (JRC GSW), **healthcare access** (OSM/HDX), **relative wealth/SES** (Meta RWI). Optionals (try-and-prune, FDR-controlled): VIIRS nightlights, TWI/slope, HAND flood-proneness, static gravity connectivity, MODIS LST, land-cover fragmentation, cropland/rice, forest cover, wind. **ENSO/IOD** = temporal stratifier only (no spatial variation). **Dropped (access barrier):** live mobility flows, household water storage, roof material.

**[PI] Confirm the final dynamic pool** — recommended: the 6 rows above. Static optionals are exploratory and do not affect H1.

## 6. Model class and hybrid definition

- **Baseline M1** — recent-cases autoregressive logistic (as v18). Unchanged.
- **Hybrid** — M1's recent-case terms **+** the stability-selected dynamic geospatial features (§7), fit with the **same penalized logistic (L2/ridge)** family and recalibration machinery as the M-ladder. Same software stack, same DCA/net-benefit evaluation.
- **Exploratory reference only (SI):** a geospatial-only model may be reported as a context point; it is **not** a headline deliverable and does not enter H1.

## 7. Feature selection — stability selection (leakage-proof)

- **Method:** stability selection over **inner** CV folds only (§8). For each inner resample, fit an L1/elastic-net screen on the candidate dynamic pool; record selection frequency per feature.
- **Selection threshold:** feature retained if selection frequency ≥ **π = 0.60** **[PI]**.
- **Feature cap (EPV guard):** at most **k = floor(N_events / 20)** features enter the hybrid **[PI]** (events counted on the Colombia training folds; keeps events-per-variable ≥ 20). If more than k pass π, keep the top-k by mean selection frequency.
- **Reporting:** report *all* candidates with their selection frequencies (survivors and non-survivors), plus spatial-importance vs temporal-importance separation.
- **No look-ahead:** selection uses inner folds only; the outer folds that score H1 never inform selection.

## 8. Nested spatial-CV protocol

- **Autocorrelation range:** fit the reference model, extract residuals, estimate the residual spatial-autocorrelation range per country (empirical variogram and/or Moran's I decay). Records the buffer width (SL) and minimum block size (Colombia).
- **Outer folds (evaluation):** Colombia — **leave-one-department-out**, buffered so no train/test pair sits within the autocorrelation range; balance folds on prevalence and unit-week count. SL — **buffered LOOCV** (26 folds), companion only.
- **Inner folds (selection + tuning):** within each outer training set, a further spatial-block split for stability selection (§7) and λ tuning. **Selection and evaluation never share data.**
- **Temporal honesty:** lags built from the past only inside every fold → **spatio-temporal nested CV**.
- **Leakage audit (deliverable):** verify 0 train/test neighbor pairs within range; verify temporal ordering; write `leakage_audit_memo_v1.md`.

## 9. Inference and multiplicity

- **One confirmatory contrast** (H1). Reported with a cluster-bootstrap 95% CI (**B = 1000**, cluster = municipality/RDHS, percentile + concordant wild-cluster-bootstrap-t as a check; **[PI]** confirm seed convention, e.g. `2026MMDD`).
- **Co-primary H2** reported descriptively (ranking survival).
- **Everything else exploratory:** FDR control (Benjamini–Hochberg) across each exploratory family (MAUP variables, F8 covariates, thresholds/horizons). No exploratory result is stated as confirmatory.
- **MAUP direction:** report divergences and decision-flip counts **with CIs**; **do not** describe MAUP as "conservative" — direction is indeterminate.

## 10. Success / stop criteria and honest-null

- **H1 "supported":** Colombia ΔNB(hybrid − M1) CI excludes 0 at p\*=0.30 under outer-fold spatial CV.
- **H1 "null":** CI includes 0 → reported as "geospatial augmentation did not improve calibrated decision value beyond recent surveillance under spatially-honest validation" — a headline-consistent contribution.
- **Hard stop (no fishing):** if the pre-registered pool + stability rule yields no stable features, the hybrid = M1 and H1 is reported null. Do **not** relax π or the pool post hoc to manufacture a hybrid.

## 11. Analyst degrees of freedom locked here

Label definition, horizon, p\*, split, candidate pool, transforms, model family, π, feature cap, CV scheme, bootstrap B/cluster, FDR families, primary contrast. Any change after freeze = dated amendment in `study_decision_log.md`, disclosed in the paper.

---

# PART II — IMPLEMENTATION BLUEPRINT (build order)

**Phase 0 — Staging & freeze (BLOCKING).** Stage every input (Build-A CSV, WorldPop, DEM GLO-30, Colombia boundaries + OpenDengue V1.3 with version+access date, GEE layers, saved predictions out of quarantine). Reproject to equal-area CRS. **Freeze Part I** (repo tag `plan_v2_frozen` + OSF pre-registration). *No modeling until this tag exists.*

**WS-A — Exposure builds.** Script `build_exposure_popweighted_v1.py` → Build B; `build_exposure_terraincorrected_v1.py` → Build C; append DTR/VPD/SPI columns (recipes in the co-author HTML §5.2). Row-aligned, checksummed, FREEZE_LOG. → `…_v2_popweighted.csv`, `…_v3_terraincorrected.csv`.

**WS-B — Spatial folds.** `estimate_autocorr_range_v1.py` (variogram/Moran's I, both countries) → `build_spatial_folds_v1.py` (Colombia LODO buffered; SL buffered-LOOCV) → `leakage_audit_v1.py` → `leakage_audit_memo_v1.md`. Fold-definition files are versioned artifacts.

**WS-C — Stability selection (Colombia).** `stability_selection_v1.py` over inner folds on the dynamic pool → selection-frequency table + spatial/temporal importance → the retained ≤k feature set. → `feature_selection_report_v1.md`.

**WS-D — Hybrid + primary contrast.** `fit_hybrid_v1.py`: M1 + selected features, penalized logistic, recalibration → evaluate on outer folds with the M-ladder calibration/DCA/net-benefit machinery → cluster-bootstrap ΔNB(hybrid − M1) (H1) → SL confirmatory run. → `hybrid_primary_result_v1.md`.

**WS-E — MAUP sensitivity + F8.** `maup_decision_sensitivity_v1.py`: ladder→calibration→NB across builds A/B/C, per-variable + pooled, decision-flip counts with CIs (F7). `f8_miscalibration_panel_v1.py`: per-unit calibration/ΔNB regressed on static covariate panel, FDR-controlled, Colombia-led (F8). → `maup_report_v1.md`, `f8_report_v1.md`.

**WS-F — Integration.** Operational translation (per-100-unit-week) for both settings; cross-setting descriptive table (no heterogeneity test).

**WS-G — Reproducibility + admin (PARALLEL, start now — see Part IV).**

**Dependencies:** Phase 0 → all. WS-A,B → WS-C → WS-D. WS-B → WS-E. WS-G ∥ everything.

---

# PART III — Planned endpoints, tables, figures

- **Primary:** ΔNB(hybrid − M1) @0.30 (Colombia, spatial CV) + CI. **H2:** ranking-survival table (temporal vs spatial CV).
- **New SI:** S13 spatial-autocorrelation ranges + fold definitions · S14 stability-selection frequencies (all candidates) · S15 nested-CV protocol + leakage memo · S16 MAUP three-build sensitivity · S17 F8 covariate panel (FDR) · S18 hybrid model card + EPV.
- **New figures:** F2 exposure contrast (A/B/C) · F7 MAUP net-benefit sensitivity + decision-flips · F8 miscalibration/decision-flip map · F9 hybrid vs M1 decision curve under spatial CV.
- **Reuse verbatim from v18:** benchmark ladder tables/figures + operational-translation language.

---

# PART IV — Reproducibility & environment (parallel track; unblocks submission independently)

- **Environment capture (fixes audit gap):** commit `requirements.txt`/`environment.yml` + `.python-version` (or a container); record the **primary Python modeling-stack versions** now (they were not preserved for v18 — capture the current canonical env and disclose it transparently, not as the historical one). R stack already documented.
- **Deposit:** code + fold definitions + model cards to a public repo; mint **Zenodo DOI**; add **license**; OpenDengue **version + access date**. Predictions moved out of `data_quarantine` into the deposit (respecting data-sharing terms).
- **Reporting instruments:** finalize S1 STROBE, S2 TRIPOD+AI, S3 PROBAST (now genuinely relevant since a model is developed — TRIPOD+AI applies to the hybrid).
- **Declarations:** ethics determination (do not self-certify), funding, competing interests, CRediT, ORCID, all-author approval.

---

# PART V — Risk controls (mapping)

| Panel risk | Control in this plan |
|---|---|
| n=26 underpowering | §2 Colombia leads; SL companion only |
| selection leakage | §7–§8 nested spatial CV; select inner, score outer |
| multiplicity / forking paths | §7 pre-registered π + cap; §9 one confirmatory + FDR |
| estimand drift | §3 locked estimand; v18 benchmark reused verbatim |
| publication-bias trap | §1/§10 reframed so null is headline-consistent and reported |
| MAUP mis-spin | §9 report flips with CIs, no "conservative" claim |
| staging slippage | Part II Phase 0 critical path; §4/§5 scope dials trim in order |
| software provenance | Part IV environment capture + honest disclosure |

---

# PART VI — Sign-off checklist (freeze gate)

- [ ] **[PI]** ratifies reframe (development-and-evaluation) and R1–R5.
- [ ] **[PI]** confirms: final dynamic pool (§5), π (§7), feature cap k (§7), bootstrap seed (§9), Build C in/out (§4).
- [ ] Part I frozen: repo tag `plan_v2_frozen` + OSF pre-registration ID recorded in `study_decision_log.md`.
- [ ] Phase 0 staging complete + checksummed.
- [ ] WS-G admin/repro track opened in parallel.

*Only after every box above may modeling (WS-A onward) begin. This document changed no code, data, or manuscript; nothing was staged, committed, or pushed. `single_paper_integrated_plan_v1.md` is unmodified.*
