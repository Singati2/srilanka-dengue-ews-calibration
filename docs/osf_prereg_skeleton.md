# OSF Preregistration — Sri Lanka Dengue Early-Warning Decision-Value Pilot

**Status:** Preregistration skeleton (pilot gate). To be frozen on OSF *before* exposure data are linked to outcome data.
**Type:** Confirmatory pilot / publishability gate. This is **not** the full paper; it is a pre-specified test of whether a full paper is warranted.

> **Framing constraint (read first).** We do **not** propose a new dengue model and we do **not** claim methodological novelty. Calibration assessment of epidemic forecasts and net-benefit / cost-loss valuation of early-warning systems are established prior work — notably **Tozan et al. 2023 (*AJTMH*)**, a net-benefit framework for EWS-triggered vector-borne-disease response, and the meteorological **cost-loss value model (Murphy 1985)**, of which decision-curve analysis (Vickers & Elkin 2006) is an algebraic re-parameterization. Our contribution is an **empirical, regional, decision-relevant evaluation** using two existing model classes, with a recalibration control arm and a defensible geospatial exposure layer. We position DCA as the clinical-prediction parameterization of cost-loss, not as our invention.

---

## A. Project title
*Discrimination is not deployment: a preregistered pilot of calibration and decision-curve evaluation of two existing climate-driven dengue early-warning systems in Sri Lanka.*

## B. Research question
For climate-driven dengue early-warning in Sri Lanka, do two existing early-warning systems with **equivalent discrimination (AUC)** yield **different public-health alert decisions** under decision-curve / net-benefit analysis at an operationally anchored threshold — and does that difference **survive recalibration**?

## C. Primary hypothesis
**H1.** Conditional on statistically indistinguishable out-of-sample discrimination (ΔAUC 95% CI includes 0), the mechanistic-R0 EWS and the DLNM-INLA EWS will differ in **net benefit at the cost-anchored alert threshold** by a margin whose 95% CI excludes 0, and at least one model will cross a decision boundary relative to the default "alert-always / alert-never" strategies that the other does not (a **decision flip**).

## D. Secondary hypotheses
- **H2.** The two models are mis-calibrated to differing degrees / directions (calibration slope and calibration-in-the-large differ).
- **H3.** Post-hoc recalibration **reduces but does not fully eliminate** the net-benefit gap (irreducible decision loss).
- **H4.** Decision-flips are **spatially structured** — flip occurrence is associated with landscape covariates (urbanization, elevation, NDVI, surface water).
- **H5.** Net benefit is **sensitive to exposure construction** (population-weighted/terrain-corrected vs naive areal mean) — MAUP effect.

## E. Data sources
- **Outcome:** Sri Lanka Epidemiology Unit weekly dengue notifications (MOH-division preferred; district fallback).
- **Climate:** ERA5-Land (temperature, humidity, precipitation); CHIRPS (rainfall); MODIS MOD11 (LST, downscaling anchor).
- **Environmental:** MODIS MOD13 (NDVI/EVI); ESA WorldCover + GHSL (land cover, built-up); JRC Global Surface Water; Copernicus DEM/SRTM (elevation).
- **Population/boundaries:** WorldPop (vintage-matched); Sri Lanka Survey Department admin boundaries (MOH-division + district).
- All sources public/open; provenance recorded in Table T1.

## F. Inclusion / exclusion criteria (spatial units and weeks)
**Pre-specified, applied before outcome linkage:**
- **Spatial unit:** MOH-division if a continuous weekly series of ≥ **8 years** is obtainable for ≥ **80%** of divisions; otherwise district (25 units). Decision recorded and time-stamped before analysis.
- **Study window:** longest common period with complete climate + outcome coverage (target ≥ 10 years); exact dates frozen at registration.
- **Include** units with ≥ 8 years of continuous weekly reporting and < **10%** missing weeks (gap-filled and flagged).
- **Exclude** units with > 10% missing weeks, unstable boundaries that cannot be crosswalked, or population denominators unavailable.
- **Exclude** the **quarantined pipeline-debug subset** (see Z) from all confirmatory analyses.

## G. Outcome definition / outbreak threshold
- **Unit of analysis:** unit × epidemiological week (ISO/CDC weeks).
- **Outbreak indicator (binary):** week in which observed incidence exceeds the **endemic-channel threshold** = the historical (pre-period) moving **75th centile** of weekly incidence for that unit and calendar week, computed from seasons *strictly preceding* each forecast origin (no future leakage). Primary definition frozen at registration.
- **Forecast target:** P(outbreak) at **4-week lead** (sensitivity: 8-week lead).
- The outbreak threshold is defined from historical data and published convention, **not tuned** on the evaluation period (consistent with "pilot never sets thresholds").

## H. Exposure construction plan *(Geospatial Lead)*
- Reproject all layers to an **equal-area CRS** (SLD99 / UTM 44N).
- **Elevation-correct temperature** (lapse-rate, DEM-based, MODIS-LST-anchored) before aggregation.
- Compute **population-weighted zonal mean + within-unit dispersion** per unit-week.
- Align to ISO/CDC weeks; build **DLNM lag matrices (0–12 weeks)** using past data only.
- Produce **two frozen exposure datasets**: (i) population-weighted/terrain-corrected (primary) and (ii) naive areal mean (for H5/MAUP).
- Exposure datasets are frozen and version-tagged **before** linkage to outcomes.

## I. Mathematical model specification (existing, published)
- **Model:** climate-forced **Ross–Macdonald / SEI-SEIR** with **temperature-dependent trait thermal responses taken as published** from Mordecai et al. 2017 and Huber et al. 2017 (biting rate, EIP, vector mortality, carrying capacity; transmission window ~18–34 °C, peak ~26–29 °C). **No biological parameters refit.**
- **Output:** temperature-dependent **R0(T)** (relative suitability) per unit-week.
- **R0 → P(outbreak) link:** a single **pre-specified logistic mapping**, with coefficients fit **only on training folds** within rolling-origin CV; the link form is frozen at registration and its sensitivity reported. (This is the only fitted element on the mechanistic side; it is acknowledged as a potential confounder — see Y.)

## J. Statistical model specification (existing, published)
- **Model:** **DLNM cross-basis** (Gasparrini) on temperature and rainfall + **Bayesian hierarchical spatiotemporal model via INLA**, specified as the published **EWARS-csd / Lowe** family: **BYM2** spatial random effect + **RW1** temporal effect + seasonal terms, **negative-binomial** likelihood, population offset.
- Hyperpriors and basis knots set to published defaults, frozen at registration.
- **Output:** posterior predictive **P(outbreak)** per unit-week, directly comparable to the mechanistic exceedance probability.

## K. Rolling-origin validation design
- **Expanding-window rolling-origin** out-of-sample evaluation: refit both models at each origin using only past data; forecast 4 weeks ahead; advance the origin; concatenate out-of-sample predictions.
- First origin after a minimum **5-year** training burn-in; origins advance by 4 weeks (or by season — frozen at registration).
- All calibration, DCA, and discrimination metrics computed on **out-of-sample** predictions only.

## L. Calibration metrics
On pooled out-of-sample predictions, per model:
- **Reliability diagram** and **PIT histogram**.
- **Calibration-in-the-large** (intercept) and **calibration slope** (Van Calster hierarchy).
- **Brier score** with **Murphy decomposition** (reliability / resolution / uncertainty).
- **CRPS** for sharpness (reported; acknowledged as decision-agnostic, distinct from DCA).

## M. Recalibration arm
- Pre-specified method: **isotonic regression** (primary) and **Platt/logistic** (secondary), fit on training folds, applied to test folds.
- Recompute calibration metrics and **net benefit** post-recalibration.
- Note: recalibration is monotone → AUC is unchanged by construction; the recalibrated-vs-raw contrast is a **clean same-AUC demonstration** (secondary to the mechanistic-vs-statistical contrast).

## N. Decision-curve / net-benefit analysis
- **Vickers net benefit** across threshold probabilities p_t:
  NB(p_t) = (TP/N) − (FP/N)·[p_t/(1−p_t)].
- Compare: Model A, Model B, **alert-always**, **alert-never**, across the policy-relevant p_t range.
- **Explicitly unified with the cost-loss value model** (Murphy 1985; Tozan 2023): p_t encodes the cost:loss odds C/L = p_t/(1−p_t).
- Report ΔNB(A−B) with **bootstrap 95% CI** (block bootstrap respecting spatial/temporal structure), pre- and post-recalibration.

## O. Cost-anchored threshold definition
- **Primary operational threshold** p_t* derived from the **cost:loss ratio of vector-control response vs missed outbreak**, anchored to published economic inputs (Tozan et al. 2023; Lee et al. 2015 dengue-EWS cost-effectiveness): p_t* = C/(C+L).
- A **plausible range** [p_t,low, p_t,high] is pre-specified for sensitivity (reflecting cost uncertainty).
- Thresholds set from external sources, **not** optimized on outcome data.

## P. Spatial-block validation / leakage control *(Geospatial Lead)*
- Estimate residual **variogram / autocorrelation range**; set **spatial-block CV** block size ≥ range; **buffer** folds so neighboring units do not straddle train/test.
- Combine spatial blocking with the temporal rolling-origin scheme (spatiotemporal CV).
- **Leakage audit memo** required before primary analysis: confirm no train/test neighbor pairs within autocorrelation range; no future composites injected into past weeks.

## Q. MAUP / exposure-construction sensitivity analysis *(Geospatial Lead)*
- Re-run the **entire** discrimination + calibration + DCA pipeline under the **naive areal-mean** exposure dataset.
- Report whether exposure construction **alone** changes ΔNB sign or any decision flip.
- Outcome feeds H5 and Figure F7; interpreted as a precondition result, not a competing finding.

## R. Primary endpoint
**ΔNB(A−B) at the cost-anchored threshold p_t\*, on out-of-sample rolling-origin predictions, conditional on matched discrimination (ΔAUC 95% CI includes 0), pre-recalibration**, with its block-bootstrap 95% CI; plus the **binary decision-flip indicator** (do A and B recommend different actions relative to alert-always/alert-never at p_t\*).

## S. Secondary endpoints
- Calibration slope/intercept and PIT per model (H2).
- ΔNB at p_t* **post-recalibration** and the % of the gap closed (H3).
- Spatial regression: association of decision-flip occurrence with landscape covariates (H4, Table T3).
- MAUP sensitivity: ΔNB under naive vs weighted exposure (H5, Figure F7).
- Robustness: 8-week lead; alternative outbreak definition; cost-threshold range.

## T. Go/no-go criterion (binary)
**GO** to the full multi-country paper **iff ALL three hold:**
1. **Matched discrimination:** ΔAUC 95% CI includes 0 (the models are genuinely comparable in accuracy); **and**
2. **Material decision difference:** ΔNB at p_t* has a 95% CI **excluding 0** *and* exceeds the pre-specified **minimal important difference** (MID = net benefit equivalent to ≥ **1 additional correct alert per 100 unit-weeks** at p_t*); **and**
3. **Survives recalibration:** the recalibrated ΔNB 95% CI still **excludes 0**, OR a decision flip relative to default strategies persists post-recalibration.

**NO-GO** if any of the three fails.

## U. What result kills the paper (NO-GO / do not write)
- ΔNB CI at p_t* **includes 0** (no material decision difference); **or**
- The AUC-better model is also the net-benefit-better model **across the entire** p_t range (discrimination already suffices); **or**
- Recalibration **erases** the gap (lesson collapses to "just recalibrate" — too weak to publish as framed); **or**
- The decision flip is shown by MAUP analysis to be an **artifact of exposure construction** rather than a genuine model difference (kills the main thesis; may survive only as a separate exposure-methods note).

In any of these cases: **report the null honestly, do not reframe to manufacture a finding, do not proceed to the full paper.**

## V. What result makes it publishable (GO)
- Matched AUC **and** a material ΔNB at the operational threshold **and** persistence after recalibration **and** spatial structure to the flips **and** robustness to exposure construction → a genuine, operationally-useful finding ("equal accuracy, different action, not recalibratable away, and mappable"). Target tier: PLoS NTD / Lancet Reg. Health–SE Asia / BMC Medicine.

## W. Planned figures / tables
- **F1** Study area + surveillance coverage/missingness — Geospatial Lead.
- **F2** Exposure-construction contrast (weighted − naive) — Geospatial Lead.
- **F3** Elevation-corrected R0 suitability map — Geospatial + math lead.
- **F4** Reliability diagrams + PIT, both models — Stats lead.
- **F5** Decision curves (net benefit vs threshold), ± recalibration — Stats lead.
- **F6** Decision-flip map — Geospatial Lead.
- **F7** MAUP/exposure sensitivity on net benefit — Geospatial Lead.
- **T1** Data sources/resolution/provenance/QA — Geospatial Lead.
- **T2** Discrimination/calibration/net-benefit summary — Stats lead.
- **T3** Spatial predictors of miscalibration/flips — Geospatial Lead.
- **T4** PROBAST/TRIPOD scoring — Joint.

## X. Roles and responsibilities
- **PI / biostatistics lead (you):** design, decision-analytic framework, calibration/DCA analysis, manuscript.
- **Statistical modeling lead:** DLNM-INLA implementation, rolling-origin, recalibration arm, F4/F5/T2.
- **Mathematical modeling lead:** R0/thermal-response model, R0→P link, F3.
- **Geospatial Lead (Geomatics engineer):** exposure construction (H), adjacency graph (J input), spatial-block CV (P), MAUP sensitivity (Q), decision-flip mapping (F6, T3), F1/F2/F7/T1. *Co-author contingent on owning H/P/Q and the spatial decision-support analysis (see SOW).*
- **All:** PROBAST scoring (T4), approval, accountability.

## Y. Limitations
- **Passive surveillance / under-reporting** in dengue notifications; outbreak label is noisy.
- **Single country pilot** — generalizability deferred to the multi-country full study.
- **R0→P link dependence** — the mechanistic-side mapping is a modeling choice that could confound calibration; mitigated by pre-registration + sensitivity, not eliminated.
- **No entomological/serotype covariates** — serotype replacement dynamics unmodeled.
- **Outbreak-definition sensitivity** — primary definition is one of several defensible choices; tested in secondary analyses.
- **Cost inputs** for the threshold are borrowed/uncertain; addressed via threshold-range sensitivity.

## Z. Analysis freeze rules
1. This document is frozen and time-stamped on OSF **before** exposure data are linked to outcome data.
2. A separate **quarantined pipeline-debug subset** (pre-specified units/years) is used only to debug code; it is **excluded** from all confirmatory analyses and never informs metrics, thresholds, or model choices.
3. Outbreak definition, primary cost-anchored threshold, MID, model specifications, and all endpoints are fixed at registration; **no test-fold inspection** before the analysis run.
4. The spatial-unit decision (MOH-division vs district) is made and recorded **before** outcome linkage.
5. Any deviation from this plan is reported in the manuscript as **exploratory** and labeled as such.
6. Analysis code is version-tagged at the freeze commit; the exact commit hash is recorded on OSF.
7. The **go/no-go decision (Section T) is computed once** on the locked analysis and is binding.

---

### Prior work (verified) — embedded as context, NOT as novelty claims

**Corrected novelty statement (read before drafting).** We make **no methodological-novelty claim**. Two specific prior results bound our framing and are explicitly conceded:
- The abstract insight that **forecast skill (discrimination / proper scores) does not equal decision value** for epidemic forecasts is **already published** — Gerlee et al. (2026), for influenza. We do **not** claim this insight.
- **Probabilistic evaluation of dengue forecasts** is an established paradigm — Johansson et al. (2019, PNAS). We build on it, we do not introduce it.
- **Net-benefit valuation of EWS-triggered vector-borne-disease response** already exists — Tozan et al. (2023). DCA is an algebraic re-parameterization of the **cost-loss value model** (Murphy 1985; Vickers & Elkin 2006); we state this equivalence rather than claim invention.

**Our claimed contribution is therefore strictly empirical and regional:** the first preregistered, **equal-AUC head-to-head** of two existing climate-driven dengue EWS in **South Asia**, evaluated with **calibration + a recalibration control arm + cost-anchored decision-curve net benefit + spatial decision-flip mapping** on defensibly constructed exposure. A literature sweep (verified, current to June 2026) found **no single paper combining** {South Asia dengue EWS · existing climate-driven model comparison · calibration/recalibration · decision-curve/cost-loss net benefit · cost-anchored operational threshold · decision-flip/deployment recommendation}; the intersection is empty.

**Verified citations to embed:**
- **Gerlee, P. et al. (2026).** *Evaluating infectious disease forecasts in a cost-loss situation.* arXiv **2601.05921** (preprint, posted 2026-01-09; not yet peer-reviewed). https://arxiv.org/abs/2601.05921 — cost-loss Value Score on FluSight influenza; value ranking ≠ skill ranking. *Concedes the conceptual "skill ≠ value" point; differs from us in disease (influenza), region (US), metric (cost-loss VS not Vickers DCA), and design (no calibration, no equal-AUC model-pair decision flip).*
- **Johansson, M.A. et al. (2019).** *An open challenge to advance probabilistic forecasting for dengue epidemics.* **PNAS** 116(48):24268–24274. DOI 10.1073/pnas.1909865116. — multi-team probabilistic dengue forecasting challenge (Peru, Puerto Rico). *Establishes probabilistic dengue-forecast evaluation; no net benefit, no calibration/recalibration, no South Asia, no cost threshold.*
- **Tozan, Y., Kim, S., Sewe, M., Rocklöv, J. (2023).** Net-benefit framework for VBD EWS-triggered response. *AJTMH.* https://pmc.ncbi.nlm.nih.gov/articles/PMC9978551/
- **Murphy (1985); Vickers & Elkin (2006)** — cost-loss value model / decision-curve analysis (DCA ↔ cost-loss equivalence).
- **Lowe et al. (2013/2018); EWARS-csd (Schlesinger 2024)** — DLNM + INLA Bayesian dengue EWS (the statistical model class).
- **Mordecai et al. (2017); Huber et al. (2017)** — temperature-dependent transmission / R0 (the mechanistic model class).
- **Lee et al. (2015)** — cost-effectiveness of dengue early-warning systems (cost inputs for the threshold).
- **Van Calster et al.** — calibration hierarchy; **PROBAST / TRIPOD** — risk-of-bias / reporting standards.

*Verification status (2026-06): Gerlee 2026 and Johansson 2019 independently confirmed (existence, full citation, scope). Exact-match search returned no paper covering the full six-element intersection → idea not preempted. Remaining to confirm at submission time: peer-review status of Gerlee 2026 (currently a preprint).*
