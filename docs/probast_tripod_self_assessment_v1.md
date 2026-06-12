# PROBAST / TRIPOD-AI Self-Assessment (v1)
*Structured risk-of-bias and reporting-completeness self-assessment of the **as-run** dengue EWS decision-value pilot, scored against the committed instrument `docs/probast_tripod_scoring_instrument.md`. Assessment only — **no models run, no metrics computed, no data modified, no manuscript prose**. All evidence is drawn from already-committed `docs/*` reports. Ratings follow the instrument's strict rules (Section H): absence of evidence on a leakage dimension is **not** scored Low, and a High-risk finding is reported as-is.*

**Date:** 2026-06-12 · **Scored against:** instrument commit-state at HEAD (sections D, E, G, H).

## 1. Scope
- This is a **retrospective model-evaluation / decision-evaluation** study on a Sri Lanka RDHS × epi-week panel (2018–2025).
- **Not a deployment trial; not a prospective/real-time test.**
- It evaluates **existing model classes** (M0 climatological, M1 lagged-AR, M2 climate-only, M3 climate+season+RDHS) and **recalibration**, not a new production EWS.
- **Design-vs-instrument note:** the instrument anticipated a *confirmatory* design (rolling-origin + spatial-block CV, two named published forecasters, externally-anchored cost threshold, block-bootstrap CIs, PIT/CRPS, population-weighted/elevation-corrected exposure). The pilot **as run** used a simpler design (single temporal holdout, M0–M3 classes, full-curve DCA with a pre-specified p\*=0.30 reference, area-based exposure). These differences are scored honestly below and drive the bottom-line **EXPLORATORY** label (§7), consistent with how the project has framed every report ("pilot-level," "leans toward").

## 2. PROBAST-style domains (D1–D8)
Rating scale: **Low / Some concerns / High / Unclear**.

| Domain | Rating | Evidence (committed) | Concern | Manuscript reporting action |
|---|---|---|---|---|
| **D1 Participants / spatial-temporal units** | **Low** | All 26 RDHS included (no outcome-based selection); boundary vintage fixed (HDX COD-AB; geometry frozen `9e5e2c0a`); crosswalk documented — `rdhs_geometry_build_report.md`, `kalmunai_rdhs_ds_assignment.md` | Units are administrative; no exclusion by incidence | Report unit list, boundary version, full 2018–2025 coverage (TRIPOD R3) |
| **D2 Predictors / exposure construction** | **Some concerns** | Exposure **frozen before linkage** (G2 pass; freeze `8495401` precedes linkage `482f4a2`); lags past-only; ERA5-Land + CHIRPS, RH via Magnus — `exposure_freeze_v1.md`, `climate_exposure_*` | **Area-based `all_touched`** aggregation, **not** population-weighted/elevation-corrected; within-unit heterogeneity not carried; MAUP sensitivity documented but **not run** | State aggregation method and its limits; flag population-weighting/MAUP as future work (R5) |
| **D3 Outcome / alert labels** | **Low** | RDHS-specific 75th-pct threshold from **train 2018–2022 only** (G1 pass; leakage-safe), single consistent rule — `pilot_*_report.md`, `label_horizon_*` | Percentile-based label (not an external clinical cutoff); train→test base-rate shift 24.2%→33.6% | Report threshold derivation, leakage-safety, and base-rate shift explicitly (R4) |
| **D4 Analysis** | **Some concerns** | M0–M3 used as specified, no covert refitting; standardization/M0/coefficients **train-only**; deterministic (reproduced to ≤8.9e-16) — `pilot_*`, `rolling_recalibration_*` | **Simple existing classes**, not two named published forecasters; lag values mean-imputed (train mean) where unavailable; logistic L2 C=1e6 (≈MLE) | Report exact model specs, the imputation rule, and "existing classes, no new forecaster" (R7) |
| **D5 Validation / temporal split** | **Some concerns** | **Truly out-of-sample temporal holdout** (G4 pass: test 2023–2025 never in train 2018–2022) — all reports | **Single split**, not **rolling-origin** (instrument primary); no spatial-block CV | Report the holdout; state rolling-origin + spatial-block CV as the confirmatory follow-up (R8) |
| **D6 Calibration** | **Low** | CITL/slope/Brier on **out-of-sample test**; recalibration **train-only / date-enforced** leakage rule (G5 pass) — `rolling_recalibration_extension_report.md` | No PIT histogram (decile reliability done instead) | Report reliability + pre/post recalibration; add PIT for completeness (R10) |
| **D7 Decision-analytic evaluation** | **Some concerns** | Full DCA curve p\*=0.05–0.50 + alert-all/none comparators; p\*=0.30 **pre-specified** reference (no post-hoc threshold optimization) — `pilot_*_report.md` | **No externally-anchored cost threshold** derived (G7 partial); **no block-bootstrap CI on ΔNB** (P17 not done) — point estimates only | Add a cost-anchored p\* with citation **and** block-bootstrap ΔNB CIs (R11) |
| **D8 Spatial / temporal leakage** | **Low (temporal) / Some concerns (uncertainty)** | Temporal: future never in train; lags past-only; recalibration uses only completed targets before week t (date-enforced) — `rolling_recalibration_*` | Spatial autocorrelation across adjacent RDHS-weeks **not** a train/test leak under the temporal split, **but** pooled metrics lack uncertainty quantification (no spatial/temporal block bootstrap) | Add block-bootstrap CIs respecting RDHS-week structure; note temporal separation is clean (R9/R11) |

**Risk-of-bias summary:** No demonstrated leakage on the dimensions addressed — the four leakage-relevant Core checks that the design touches **pass** (G1 outcome-threshold, G2 frozen-exposure-before-linkage, G3 train-only fitting, G5 train-only/date-enforced recalibration), and validation is genuinely out-of-sample (G4). The **Some concerns** ratings reflect **design scope** (single split vs rolling-origin; no spatial-block CV; area-based exposure; no uncertainty intervals; no external cost anchor), **not** evidence of leakage. Core checks **not satisfied as specified**: **G6** (spatial-block CV — not implemented), **G7** (external cost anchor / ΔNB CI — partial), **G8** (multiple pre-specified gated computations rather than a single binding go/no-go). Per instrument §H, this **caps the pipeline at "Some concerns"** and **labels the pilot EXPLORATORY**.

## 3. TRIPOD-AI reporting checklist (R1–R13)
Rating: **Reported / Partial / Not reported / NA** — and what the manuscript must include.

| # | Item | Status in committed evidence | Manuscript must report |
|---|---|---|---|
| R1 | Title/abstract identifies design | Partial (framing in reports) | "Development-free evaluation of existing models," exploratory label |
| R2 | Data source & versions | Reported | All layers (WER, COD-AB, WorldPop, ERA5-Land, CHIRPS), versions, resolutions (Table T1) |
| R3 | Eligibility / analysis frame | Reported | Filter, 10,705 modelable rows, counts/exclusions |
| R4 | Outcome definition | Reported | 75th/90th-pct labels, horizon, leakage-safe train-only derivation |
| R5 | Predictor definitions | Partial | Climate variables, **area-based** aggregation, lag structure; note no population-weighting |
| R6 | Missing data | Reported | Missingness flags, no imputation of outcomes; lag mean-imputation |
| R7 | Model specification | Reported | M0–M3 exact specs; "existing classes, nothing new fitted on test" |
| R8 | Validation design | Reported (single split) | Temporal holdout; state rolling-origin as follow-up |
| R9 | Performance metrics | Partial | AUC/PR-AUC **with CIs** (currently no CIs) |
| R10 | Calibration | Reported | CITL/slope/Brier/decile, pre/post recalibration; add PIT |
| R11 | Decision-curve / net benefit | Partial | DCA + p\*=0.30; add ΔNB **CIs** and an anchored threshold |
| R12 | Reproducibility | Reported | Repo, commit hashes, quarantine discipline, checksums |
| R13 | Limitations | Reported (handoff) | Single country/period, no external/prospective validation, threshold sensitivity |

## 4. Main strengths
- **Preregistered analysis-frame addendum** (date-aligned linkage rule + S1–S3 fixed before modeling) — `6720a58`.
- **Date-aligned linkage** correcting the WER issue-number↔ISO-week offset — `482f4a2`, `2b07d46`.
- **Clear baseline comparison** (M1 recent-cases AR as the benchmark every climate model must beat).
- **Calibration + decision-curve, not AUC alone** — calibration-in-the-large/slope/Brier + full DCA.
- **S1–S3 sensitivities** (naive linkage, lag sweep, drop-late-2021) — `0034932`.
- **Time-updated rolling recalibration** with date-enforced leakage rule — `86f9015`.
- **Label/horizon robustness** (75/90 pct × h=1–12) — `afbb52e`.
- **Strict data governance:** all heavy artifacts quarantined/checksummed; only safe markdown committed; forbidden-file guard every commit; deterministic reproducibility (≤8.9e-16).

## 5. Main limitations
- **Retrospective only** — no prospective or real-time evaluation.
- **One country / one dataset** (Sri Lanka 2018–2025); **no external validation**.
- **No deployment** — operational performance unproven.
- **Simple existing model classes / limited climate features** — not the full universe of published EWS forecasters.
- **Percentile-based alert thresholds** (75th/90th), not externally-anchored clinical/operational cutoffs.
- **RDHS-level aggregation** may mask sub-division heterogeneity (MAUP; area-based exposure).
- **Single temporal split; no rolling-origin or spatial-block CV; no ΔNB uncertainty intervals.**
- **Long-lead (h=8–12) climate AUC advantage does not establish decision value** — it does not flip net benefit at the registered p\*=0.30.

## 6. Manuscript reporting actions (checklist for the team)
**Methods must include:** data layers/versions (R2); eligibility & 10,705-row frame (R3); leakage-safe 75th/90th-pct labels (R4); M0–M3 specs + "existing classes, nothing fitted on test" (R7); area-based exposure + lag construction + no population-weighting (R5); temporal-holdout validation + statement that rolling-origin/spatial-block CV is follow-up (R8); recalibration leakage rule (D6/G5); explicit **EXPLORATORY** label.
**Results must include:** discrimination **with CIs** (R9 — to be added); calibration pre/post recalibration (R10); full DCA + p\*=0.30 + ΔNB CIs (R11 — CIs to be added); S1–S3 and label/horizon tables; the M1-dominates / climate-competitive-only-at-long-leads nuance.
**Discussion must include:** why recent cases beat climate short-term; conditional long-lead climate value; AUC-insufficiency; DCA rationale; recalibration as deployment lesson; the §5 limitations; exploratory status (findings hypothesis-generating).
**Supplement should include:** full metrics/DCA/stop-rule tables (from quarantined CSVs); S2 lag-sweep curve; per-cell label/horizon results; reproducibility/commit-hash + data-access statement; the filled instrument Table T4.

## 7. Bottom-line assessment
- **Overall risk of bias (pipeline): Some concerns**; **pilot status: EXPLORATORY / hypothesis-generating** (per instrument §H — G6 not implemented, G7 partial, G8 multiple pre-specified computations; design deviates from the anticipated confirmatory plan). No demonstrated leakage on the dimensions addressed (G1, G2, G3, G5 pass; G4 out-of-sample).
- **Publishable IF framed as a calibration / decision-evaluation / data-resource study** with honest limitations and CIs added.
- **Not publishable as a "new climate EWS wins" claim** — the evidence does not support it (climate never beats M1 on the registered decision metric).
- **Risk-of-bias issues are manageable if reported transparently:** add ΔNB/AUC uncertainty intervals, a cost-anchored threshold, rolling-origin/spatial-block validation, and the exploratory label; none of these overturn the current findings, they harden them.

## Confirmation
- **No models were run; no metrics computed.** All content is an appraisal of already-committed reports.
- **No data modified; no data files created.** Only this markdown assessment was created.
- This document contains **no manuscript prose** — only ratings, evidence mapping, and reporting actions.
