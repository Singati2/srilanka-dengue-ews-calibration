# PROBAST / TRIPOD-AI Scoring Instrument
## Sri Lanka Dengue Early-Warning Decision-Value Pilot — Risk-of-Bias & Reporting-Quality Assessment

**Status:** Pre-specified QC instrument. Built **before** any model is run, so ratings are *a priori*, not post-hoc rationalization.
**Pairs with:** `osf_prereg_srilanka_pilot.md` (the preregistration). Item numbers here cross-reference prereg sections.
**Rule of use:** This is a quality-control instrument, not marketing. A "High risk" rating is a finding to report, not a problem to argue away. Do not soften ratings to protect the narrative.

---

## A. Purpose
1. Provide an **a-priori, auditable** risk-of-bias (PROBAST) and reporting-completeness (TRIPOD-AI) assessment of the two early-warning systems and the evaluation pipeline.
2. Force the design-stage commitments in the preregistration (leakage control, frozen exposure, training-only fitting, single binding go/no-go) to be **scored as evidence**, not assumed.
3. Produce manuscript **Table T4** with defensible, pre-committed ratings.
4. Make any deviation visible: if a planned safeguard is not met, the instrument forces a **High risk** rating and the "exploratory" label (Section H), rather than silent relabeling.

## B. Models assessed
This instrument is applied **independently to each model**, then to the **shared evaluation pipeline**:
1. **Model A — Mechanistic R0 / Ross–Macdonald / SEIR-SI EWS** (published thermal-response R0; R0→P(outbreak) link). Prereg §I.
2. **Model B — DLNM-INLA Bayesian statistical EWS** (cross-basis + BYM2 + RW1 + NB). Prereg §J.
3. **Shared pipeline** — exposure construction (§H), rolling-origin (§K), calibration (§L), recalibration (§M), DCA/net benefit (§N–O), spatial/temporal leakage control (§P), MAUP (§Q).

Each model receives its **own** completed scoring table (B1, B2) plus the **shared** pipeline table (B3). A model can be Low risk while the pipeline is High risk, or vice versa — score them separately; the overall verdict (Section H) combines them.

## C. How it is used in the pilot
- **Pre-run (now):** instrument frozen; raters identified; criteria fixed.
- **During analysis:** as each pipeline stage completes, the responsible lead records evidence (file paths, commit hashes, fold definitions) against the relevant items — but **does not assign ratings yet**.
- **Post-run, pre-interpretation:** **two independent raters** assign ratings from the recorded evidence, blinded to the go/no-go result where feasible; disagreements resolved by a third. Ratings are then locked.
- The completed instrument is an OSF supplement and the source of manuscript Table T4.

---

## D. PROBAST-style risk-of-bias domains
Each domain is rated **Low / Some concerns / High / Not applicable** per model and per pipeline, supported by signalling questions (Section F).

| Domain | Scope in this project |
|---|---|
| **D1 Participants / spatial units** | Selection of MOH-divisions/districts; inclusion/exclusion (§F prereg); representativeness; boundary-vintage stability. |
| **D2 Predictors / exposure construction** | Raster→areal aggregation; population weighting; elevation correction; frozen-before-linkage; lag construction. |
| **D3 Outcome definition** | Outbreak threshold (endemic-channel 75th centile); computed from pre-period only; consistency across units. |
| **D4 Analysis** | Model specification as published (no covert refitting); handling of overdispersion, missing data, denominators. |
| **D5 Validation** | Rolling-origin out-of-sample design; train/test separation; no test-fold inspection. |
| **D6 Calibration** | Reliability/PIT/slope/intercept assessed; recalibration fitted in training only. |
| **D7 Decision-analytic evaluation** | DCA/net benefit at externally-anchored threshold; cost-loss unification; uncertainty quantified. |
| **D8 Spatial / temporal leakage** | Spatial-block CV ≥ autocorrelation range; buffered folds; no future composites; lag windows past-only. |

## E. TRIPOD / TRIPOD-AI-style reporting items
Reporting completeness (distinct from bias). Rated **Reported / Partially reported / Not reported / NA**.

| # | TRIPOD-AI item | What must appear |
|---|---|---|
| R1 | Title / abstract | Identifies study as development-free external evaluation of existing models; states design. |
| R2 | Data source | All layers, sources, versions/vintages, resolutions (Table T1). |
| R3 | Eligibility | Unit and week inclusion/exclusion (§F prereg), with counts and exclusions. |
| R4 | Outcome definition | Outbreak threshold, lead time, leakage-safe computation. |
| R5 | Predictor definition | Exposure variables, aggregation method, lag structure, both exposure datasets. |
| R6 | Missing data | Raster gap fractions, gap-fill method, sensitivity. |
| R7 | Model specification | Exact published model, parameters/priors, source citations, what was/wasn't fitted. |
| R8 | Validation design | Rolling-origin + spatial-block scheme, fold definitions. |
| R9 | Performance metrics | Discrimination (AUC + CI), sharpness (CRPS), with uncertainty. |
| R10 | Calibration | Reliability, PIT, slope, intercept, Brier decomposition; pre/post recalibration. |
| R11 | Decision-curve / net benefit | DCA across thresholds, anchored threshold, ΔNB + CI, decision-flip. |
| R12 | Reproducibility | Code repository, commit hash, environment, data-access statement. |
| R13 | Limitations | Under-reporting, link-function dependence, single-country, threshold sensitivity. |

---

## F. Scoring table (fillable)
Rating options: **Low risk · Some concerns · High risk · Not applicable** (PROBAST items); **Reported · Partial · Not reported · NA** (TRIPOD items R1–R13). Complete one copy per model (A, B) plus one for the shared pipeline.

| Item | Domain | Criterion / signalling question | Rating | Evidence required | Notes |
|---|---|---|---|---|---|
| P1 | D1 | Were spatial units selected by pre-specified inclusion/exclusion (§F prereg), not by outcome? | ☐ | Frozen unit list + timestamp before linkage | |
| P2 | D1 | Is the boundary vintage fixed and crosswalked across the study period? | ☐ | Boundary version ID; crosswalk table | |
| P3 | D1 | Are units representative (not cherry-picked high-incidence)? | ☐ | Incidence distribution of included vs excluded | |
| P4 | D2 | Was exposure aggregated by the **frozen** population-weighted/elevation-corrected method **before** outcome linkage? | ☐ | Pipeline commit hash predating linkage | **Core — see G2** |
| P5 | D2 | Were lag matrices built from past data only (no future climate leaking into a week)? | ☐ | Lag-construction code; window definitions | |
| P6 | D2 | Is within-unit exposure heterogeneity carried (not silently averaged away)? | ☐ | Dispersion fields in exposure table | |
| P7 | D3 | Was the outbreak threshold computed from **pre-period** data only (no future leakage)? | ☐ | Threshold code referencing prior seasons only | **Core — see G1** |
| P8 | D3 | Is the outbreak definition applied consistently across all units? | ☐ | Single definition function, no per-unit tuning to outcome | |
| P9 | D4 | Were both models used **as published** with no covert refitting of structure/parameters? | ☐ | Parameter/prior source citations; diff vs published | |
| P10 | D4 | Was the R0→P(outbreak) link fitted **only on training folds**? | ☐ | Link-fit code scoped to train indices | **Core — see G3** |
| P11 | D4 | Were missing data and denominators handled per plan? | ☐ | Missingness log; offset definition | |
| P12 | D5 | Is rolling-origin validation **truly out-of-sample** (no test data in training at any origin)? | ☐ | Fold index audit; refit-per-origin logs | **Core — see G4** |
| P13 | D5 | Was there **no test-fold inspection** before the locked run? | ☐ | Access log / analyst attestation | |
| P14 | D6 | Were calibration metrics computed on out-of-sample predictions? | ☐ | Metric code on test predictions only | |
| P15 | D6 | Was recalibration fitted **only inside training/calibration folds**? | ☐ | Recalibration-fit code scoped to train | **Core — see G5** |
| P16 | D7 | Was the cost-anchored threshold set from **external** sources, not optimized on outcome data? | ☐ | Cost-input citations; threshold derivation predates results | **Core — see G7** |
| P17 | D7 | Is decision uncertainty quantified (block-bootstrap CI on ΔNB)? | ☐ | Bootstrap code respecting spatial/temporal structure | |
| P18 | D8 | Were **spatial blocks** ≥ autocorrelation range used, with buffered folds? | ☐ | Variogram range; block/buffer definitions | **Core — see G6** |
| P19 | D8 | Were future composites (e.g., annual NDVI) excluded from past weeks? | ☐ | Composite-window audit | |
| P20 | D5/H | Was the go/no-go decision computed **once** on the locked analysis and treated as binding? | ☐ | Single decision log; commit hash | **Core — see G8** |
| R1–R13 | TRIPOD | Reporting items (Section E) | ☐ | Manuscript section refs | One row each |

## G. Project-specific critical checks (each maps to a "Core" item above)
These eight are **gating**. Any one rated High risk forces pipeline High risk (Section H).

| ID | Check | Pass condition | Maps to |
|---|---|---|---|
| **G1** | Outbreak threshold defined without future leakage | Threshold uses only seasons strictly preceding each origin | P7 |
| **G2** | Exposure rasters aggregated by frozen method before outcome linkage | Exposure pipeline commit hash predates first outcome-linkage commit | P4 |
| **G3** | R0→P(outbreak) link fitted only on training folds | Link coefficients estimated per-origin on train indices only | P10 |
| **G4** | Rolling-origin validation truly out-of-sample | No origin's test weeks appear in its own training set | P12 |
| **G5** | Recalibration fitted only inside training/calibration folds | Isotonic/Platt fit on train, applied to held-out test | P15 |
| **G6** | Spatial blocks prevent spatial leakage | Block size ≥ empirical autocorrelation range; folds buffered | P18 |
| **G7** | Cost thresholds externally anchored, not optimized on outcome | Threshold from published cost inputs; derivation timestamped pre-results | P16 |
| **G8** | Go/no-go computed once and binding | Single, logged computation; no re-running to change the verdict | P20 |

## H. Final-scoring rules (strict — do not soften)
**Per-model and per-pipeline overall risk:**
- **Low overall risk** — *all* PROBAST domains Low, **and** all eight Core checks (G1–G8) pass. No exceptions: "Some concerns" in any leakage domain (D2/D5/D6/D8) caps the overall at **Some concerns** at best.
- **Some concerns** — no domain is High and no Core check fails, but ≥1 non-leakage domain is "Some concerns."
- **High overall risk** — **any** of:
  - any PROBAST domain rated High, **or**
  - **any** Core check (G1–G8) fails, **or**
  - leakage cannot be ruled out from the recorded evidence (absence of evidence = High, not Low).

**What forces the pilot to be labeled EXPLORATORY (not confirmatory):**
- Any failure of G1–G8 (leakage, post-hoc threshold tuning, multiple go/no-go computations), **or**
- Any deviation from the preregistered analysis (per prereg §Z.5), **or**
- The spatial-unit decision or cost threshold being made/changed **after** seeing outcome-linked results.
If labeled exploratory, the manuscript must say so in the title/abstract and the go/no-go (prereg §T) is **non-binding** — findings become hypothesis-generating only.

**Non-negotiable:** a High-risk rating is reported as-is. The instrument does not permit upgrading a rating to preserve publishability; an honestly High-risk pilot is reported as High-risk (and, if leakage is involved, as exploratory).

## I. Planned Table T4 format (manuscript)
Compact published version:

| Domain | Model A (Mechanistic) | Model B (DLNM-INLA) | Shared pipeline |
|---|---|---|---|
| Participants / units | ☐ | ☐ | — |
| Predictors / exposure | ☐ | ☐ | ☐ |
| Outcome definition | ☐ | ☐ | ☐ |
| Analysis | ☐ | ☐ | — |
| Validation | ☐ | ☐ | ☐ |
| Calibration | ☐ | ☐ | ☐ |
| Decision-analytic | ☐ | ☐ | ☐ |
| Spatial/temporal leakage | — | — | ☐ |
| **Overall** | ☐ | ☐ | ☐ |

Footnote lists which of G1–G8 passed/failed. Full signalling-question table (Section F) goes to the supplement.

## J. Connection to the OSF preregistration
- Each Core check (G1–G8) operationalizes a freeze rule or design commitment in `osf_prereg_srilanka_pilot.md`: G1↔§G, G2↔§H/§Z, G3↔§I, G4↔§K, G5↔§M, G6↔§P, G7↔§O, G8↔§T/§Z.7.
- This instrument is registered as an **OSF supplement** alongside the prereg, before model runs, so the bias assessment is itself pre-committed.
- If any Core check fails, prereg §Z.5 (deviation → exploratory) and §H/§U (kill/label conditions) are triggered; the go/no-go in §T is downgraded to non-binding.
- No change to the preregistration is required by this instrument. *Optional, non-substantive cross-reference:* a one-line pointer may be added to prereg §X ("PROBAST/TRIPOD-AI scoring per `probast_tripod_scoring_instrument.md`") if desired — not required for validity.
