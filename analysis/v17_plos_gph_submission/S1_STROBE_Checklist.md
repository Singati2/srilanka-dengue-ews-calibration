# S1 Checklist — STROBE Statement

**DOCX conversion pending — this is the Markdown checklist.** (The journal requests a checklist file; a DOCX can be generated later from this Markdown source.)

Checklist of items that should be included in reports of observational studies (STROBE, cohort / cross-sectional; items 1–22). This study is a **retrospective, observational, decision-analytic evaluation** of climate-informed dengue early-warning (elevated-activity alerting) models: Sri Lanka RDHS-week (2018–2025, primary) and Colombia municipality-week (2020–2022, secondary case study). The analytic unit is a spatial-unit × epidemiological-week observation; the "cohort" is the panel of unit-weeks with a four-week-ahead alert outcome.

Manuscript audited: `manuscript/paper1_validity_corrected_candidate/paper1_plos_gph_submission_ready.tex`. Section names below refer to that file.

---

## Title and Abstract

**Item 1(a)** — Indicate the study's design with a commonly used term in the title or the abstract.
- **PARTIAL.** Title ("Does climate information add decision value beyond dengue surveillance? A specification-matched evaluation in Sri Lanka and Colombia") names the comparison but not a standard design term. Abstract supplies the design: *"We conducted a retrospective decision-analytic evaluation of short-horizon elevated-activity dengue alerting in two settings…"* (Abstract). The word "observational" / "cohort" is not in the title; "retrospective decision-analytic evaluation" appears in abstract and Methods.

**Item 1(b)** — Provide in the abstract an informative and balanced summary of what was done and what was found.
- **ADDRESSED.** Unstructured abstract summarizes objective, two settings/dates, methods (calibration, recalibration, decision-curve net benefit, cluster bootstrap, specification-matched contrast), and balanced results incl. point estimates and CIs: *"the post-hoc specification-matched climate increment in net benefit was small: +0.0087 … (95% confidence interval −0.0015 to +0.0188, including zero) and +0.0157 after past-only recalibration … Colombia, the matched increment was +0.0078 (conditional interval +0.0039 to +0.0119) but included zero once model-development uncertainty was added."* (Abstract). Includes limitations/generalizability caveat: *"These findings are predictive and decision-analytic rather than causal, and are specific to the settings evaluated."*

---

## Introduction

**Item 2** — Background/rationale: explain the scientific background and rationale for the investigation being reported.
- **ADDRESSED.** Introduction. Motivates climate-informed EWS, critiques discrimination-only evaluation and weak comparators, and states the gap: *"a climate-informed model that appears useful against a climatological or null baseline may add little beyond information agencies already hold"* and the EWARS-csd example *"…not benchmarked against a recent-case model or evaluated by decision-curve net benefit—the evaluation gap this study addresses."* (Introduction).

**Item 3** — Objectives: state specific objectives, including any prespecified hypotheses.
- **ADDRESSED.** Introduction (final sentence): *"Our objective is to determine whether climate information adds operational decision value beyond recent dengue surveillance when models are calibrated, evaluated at policy-relevant thresholds, and compared using a specification-matched non-climate baseline."* Prespecified primary estimand stated in Methods (Uncertainty…): *"The planned primary Sri Lanka hybrid contrast was ΔNB(M4−M1) … at p*=0.30 under the h=4, 75th-percentile outcome definition."*

---

## Methods

**Item 4** — Study design: present key elements of study design early in the paper.
- **ADDRESSED.** Methods §"Study design and reporting": *"We conducted a retrospective decision-evaluation of dengue early-warning models using weekly surveillance, climate, population, and spatial data … judged by discrimination, calibration, time-updated recalibration, and decision-curve net benefit."* Reporting guided by STROBE + TRIPOD+AI + PROBAST.

**Item 5** — Setting: describe the setting, locations, and relevant dates, including periods of recruitment, exposure, follow-up, and data collection.
- **ADDRESSED.** Methods §"Settings and spatial units" (26 RDHS units for Sri Lanka; Colombia municipality/GID_2). Dates: Sri Lanka fit 2018–2022, test 2023–2025 (§"Model ladder and fitting"); Colombia split train 2006–2017, validation 2018–2019, test 2020–2022 (Results §"Colombia…"). Data-acquisition provenance for Colombia (OpenDengue Temporal extract v1.3; acquisition date not preserved) in §"Surveillance outcomes and alert labels".

**Item 6(a)** — Participants: give eligibility criteria, and the sources and methods of selection of participants (cohort).
- **ADDRESSED.** Unit of analysis defined: *"one Regional Director of Health Services (RDHS) division and one epidemiological week as the unit"* (§"Study design"). Eligibility = complete-case: *"Rows with missing outcome, exposure, or population were excluded from the complete-case frame"* (§"Climate exposures and temporal alignment"); Colombia common-complete intersection defined by M1–M5 predictors (Results §"Colombia"; §"Colombia complete-case selection").

**Item 6(b)** — (Cohort, matched studies) give matching criteria and number of exposed/unexposed. *(Adapted: specification-matched model contrast.)*
- **ADDRESSED (adapted).** The "matching" here is model-specification matching, not subject matching. Methods §"Estimand hierarchy and the specification-matched climate contrast" and §"Post hoc specification-matched decomposition (Colombia)": M5 vs M5_no-climate share *"the same case-history, seasonal, and geographic terms, the same preprocessing, model family, and training and evaluation rows … refitted independently."* Colombia removes 18 climate columns; Sri Lanka matched no-climate baseline = cases + seasonal harmonics + RDHS FE.

**Item 7** — Variables: clearly define all outcomes, exposures, predictors, potential confounders, and effect modifiers. Give diagnostic criteria, if applicable.
- **ADDRESSED.** Outcome/alert label: unit-specific 75th-percentile weekly-incidence exceedance, h=4 (§"Surveillance outcomes and alert labels"). Predictors/exposures: recent-case lags, climate cross-basis (Sri Lanka: temp/precip/humidity, lags 0–8, df=3; Colombia: linear precip/temp lags 0–8, no humidity), seasonal harmonics, geographic fixed effects (§"Model ladder and fitting"). Effect-modifier-type analyses (threshold, horizon, regime) specified in §"Uncertainty…" and §"Additional post hoc analyses".

**Item 8** — Data sources/measurement: for each variable of interest, give sources of data and details of methods of assessment (measurement). Describe comparability of assessment methods if >1 group.
- **ADDRESSED.** §"Surveillance outcomes and alert labels" (Sri Lanka WER; Colombia OpenDengue Temporal v1.3); §"Population denominators" (WorldPop anchored to 2024 Census); §"Climate exposures and temporal alignment" (ERA5-Land temp/humidity via Magnus formula; CHIRPS precipitation; WER-issue-to-ISO-week date-based linkage audit). Cross-setting non-comparability explicitly flagged: *"the two settings are best read as two differently-constructed case studies rather than a like-for-like replication."*

**Item 9** — Bias: describe any efforts to address potential sources of bias.
- **ADDRESSED.** Look-ahead/leakage: held-out test not used for fitting/scaling/penalty/threshold, past-only recalibration (§"Model ladder and fitting", §"Calibration and time-updated recalibration"). WER-to-ISO linkage bias addressed by date-based join with naive-linkage sensitivity (§"Climate exposures…"). Selection bias in Colombia common-complete sample examined incl. IPW sensitivity (§"Colombia complete-case selection"). Reporting-delay bias emulated by feature censoring (§"Robustness of the Colombia climate increment"). Structural-mismatch bias motivates the specification-matched contrast.

**Item 10** — Study size: explain how the study size was arrived at.
- **PARTIAL.** Sample sizes are fully reported as consequences of the available data windows and complete-case filtering (Results §"Cohort and data alignment": 10,516 modelable rows; train 6,590, test 3,926; Colombia 13,361 common-complete). No formal sample-size / power / precision calculation is presented (none is expected for a fixed retrospective panel, but no statement to that effect is given).

**Item 11** — Quantitative variables: explain how quantitative variables were handled in the analyses. Describe which groupings were chosen and why.
- **ADDRESSED.** Continuous incidence dichotomized at the training-period 75th percentile (primary) with 90th-percentile sensitivity (§"Surveillance outcomes and alert labels"). Threshold-probability grid for net benefit, primary p*=0.30 (§"Decision-curve analysis and the reference threshold"). Climate handled via DLNM cross-basis / linear lags; recent-case lags with training-period imputation for early-series missing lags (§"Model ladder and fitting").

**Item 12(a)** — Statistical methods: describe all statistical methods, including those used to control for confounding.
- **ADDRESSED.** §"Model ladder and fitting" (penalized L2 logistic, training-only C selection), §"Calibration and time-updated recalibration", §"Decision-curve analysis and the reference threshold" (net-benefit formula given), §"Uncertainty, multiplicity, and analysis status". Non-climate confounding structure controlled via the specification-matched no-climate baseline.

**Item 12(b)** — Describe any methods used to examine subgroups and interactions.
- **ADDRESSED (with explicit disclaimer).** Threshold, horizon (h=1,2,4,8,12), stricter-percentile, train-defined regime, and department-stratified analyses (§"Additional post hoc analyses"; Results §"Horizon", §"Threshold and stricter-outcome robustness", §"Rolling-origin and spatial-block validation"). No formal interaction/heterogeneity test between settings: *"No formal interaction or heterogeneity analysis was performed, and equivalence was not assessed"* (§"Cross-setting synthesis").

**Item 12(c)** — Explain how missing data were addressed.
- **ADDRESSED.** Complete-case frame; *"genuinely missing issues were retained as documented missingness rather than imputed"* and duplicate excluded (§"Climate exposures…"); *"early-series missing lags used training-period imputation rules"* (§"Model ladder and fitting"); Colombia common-complete selection with IPW sensitivity and explicit statement that inference applies to the analyzed subset (§"Colombia complete-case selection").

**Item 12(d)** — (Cohort) if applicable, explain how loss to follow-up was addressed. *(Adapted: clustering / correlated data.)*
- **ADDRESSED (adapted).** No person-level follow-up loss; correlated panel structure handled by cluster bootstrap resampling the spatial unit (RDHS / municipality), retaining all weeks within a sampled unit (§"Uncertainty, multiplicity, and analysis status"). Limited-cluster caution stated (26 RDHS; 8-cluster regime intervals flagged non-interpretable).

**Item 12(e)** — Describe any sensitivity analyses.
- **ADDRESSED (extensive).** §"Additional post hoc analyses" and Results: cross-fitted vs past-only recalibration, completeness thresholds K∈{1,10,20,40}, rolling-origin windows, department-stratified, horizon, functional-form (DLNM cross-basis), reporting-delay censoring, pre-pandemic split, 2022-only subset, IPW selection, naive linkage, wild-cluster-bootstrap-t. All labeled pointwise / multiplicity-unadjusted.

---

## Results

**Item 13(a)** — Report numbers of individuals at each stage (eligible, examined, confirmed eligible, included in analysis).
- **ADDRESSED.** Results §"Cohort and data alignment": *"10,705 modelable RDHS-week rows, reduced to 10,516 after constructing the four-week-ahead target. Training (2018–2022) had 6,590 observations … the test period (2023–2025) had 3,926 observations and 1,321 events."* Colombia flow in §"Colombia complete-case selection": *"Of 127,703 municipality-weeks, 79,785 were common-complete; … 13,361 (62%) were common-complete."*

**Item 13(b)** — Give reasons for non-participation at each stage.
- **ADDRESSED.** Row losses attributed to four-week-ahead target construction and to missing outcome/exposure/population (complete-case); Colombia exclusions to incomplete case/climate lags. Systematic differences between included/excluded units quantified (§"Colombia complete-case selection": mean recent cases 11.1 vs 1.9; prevalence 0.375 vs 0.180).

**Item 13(c)** — Consider use of a flow diagram.
- **PARTIAL.** Fig 1 (`Fig1.pdf`) is a study-pipeline/WER-to-ISO-alignment figure, not a formal STROBE participant flow diagram with per-stage exclusion counts. No CONSORT-style flow diagram.

**Item 14(a)** — Descriptive data: give characteristics of study participants and information on exposures and potential confounders.
- **PARTIAL.** Alert prevalence and event counts reported by period (train 24.2% → test 33.6% Sri Lanka; Colombia test prevalence 0.375), and included-vs-excluded unit characteristics for Colombia. No full Table 1 of climate-exposure distributions or unit-level covariate summaries.

**Item 14(b)** — Indicate the number of participants with missing data for each variable of interest.
- **PARTIAL.** Aggregate completeness reported (row counts before/after target; Colombia 62% common-complete; Fig 6 completeness by year). Per-variable missingness counts are not tabulated in the main text (deferred to Supporting Information S7).

**Item 14(c)** — (Cohort) summarise follow-up time.
- **ADDRESSED (adapted).** Follow-up = fixed h=4-week-ahead horizon plus horizon sensitivities h=1–12; test-period spans stated (Sri Lanka 2023–2025; Colombia 2020–2022, 152 test weeks; 2022 subset 48 eligible origin weeks).

**Item 15** — Outcome data: report numbers of outcome events or summary measures over time.
- **ADDRESSED.** Alert-event counts: Sri Lanka train 1,593, test 1,321 events; Colombia 2022 subset 2,202 events. Outcome prevalences reported for every analysis (0.336 Sri Lanka test; 0.375 Colombia; 0.4586 in 2022 subset; ≈0.235 under 90th-percentile).

**Item 16(a)** — Main results: give unadjusted estimates and, if applicable, confounder-adjusted estimates and their precision (e.g. 95% CI). Make clear which confounders were adjusted for and why included.
- **ADDRESSED.** Point estimates with 95% CIs throughout Results. Primary Sri Lanka ΔNB(M4−M1) = −0.008 (95% CI −0.028 to +0.013); specification-matched ΔNB(M5−M5_no-climate) = +0.0087 (95% CI −0.0015 to +0.0188) raw and +0.0157 (95% CI +0.0066 to +0.0257) recalibrated; Colombia matched +0.0078 (conditional 95% CI +0.0039 to +0.0119; development-inclusive −0.0001 to +0.0244). "Adjusted vs unadjusted" is operationalized as compound vs specification-matched contrasts (Table `tab:matcheddecomp`; §"Specification-matched decomposition…").

**Item 16(b)** — Report category boundaries when continuous variables were categorized.
- **ADDRESSED.** Percentile-exceedance boundaries (75th primary, 90th sensitivity) and net-benefit threshold grid (p*=0.20/0.30/0.34/0.40; grid 0.05–0.50) reported in Tables `tab:slthresh`, `tab:dlnmhybrid` and text.

**Item 16(c)** — Translate estimates of relative risk into absolute risk for a meaningful time period.
- **ADDRESSED (adapted).** Net-benefit differences translated to decision-analytic units: Colombia ΔNB +0.0188 ≈ *"1.9 additional net true-positive equivalents per 100 municipality-weeks … or approximately 4.4 fewer false-alert equivalents per 100"* (Results §"Colombia"), with explicit caveat these are not observed outbreaks/lives.

**Item 17** — Other analyses: report other analyses done—e.g. subgroups and interactions, and sensitivity analyses.
- **ADDRESSED.** Results §"Horizon", §"Threshold and stricter-outcome robustness", §"Cross-setting synthesis", §"Additional sensitivity, selection, and validation analyses" (recalibration sensitivity, complete-case selection/IPW, rolling-origin, department-stratified, horizon). All flagged secondary/exploratory, pointwise, multiplicity-unadjusted; analysis-status Table `tab:analysisstatus`.

---

## Discussion

**Item 18** — Key results: summarise key results with reference to study objectives.
- **ADDRESSED.** Discussion opening: *"The central lesson of this evaluation is methodological… The design-locked primary contrast… was null (ΔNB(M4−M1) = −0.008…)."* and Summary paragraph: *"recent dengue surveillance remained a demanding benchmark, and climate-only models added limited standalone decision value… adding climate to an otherwise matched baseline produced a small positive net-benefit increment of +0.0078…."*

**Item 19** — Limitations: discuss limitations, taking into account sources of potential bias or imprecision. Discuss both direction and magnitude of any potential bias.
- **ADDRESSED (thorough).** Dedicated limitations paragraphs (Discussion): retrospective finalized (non-real-time) counts, no true reporting triangles, single temporal holdout for Sri Lanka, change-of-support/MAUP from areal aggregation, few clusters (26 RDHS / 8-cluster regimes), complete-case selection direction-of-bias uncertain, calibration-dependence of the Sri Lanka increment, pandemic-era Colombia window, no formal heterogeneity test. Direction of bias discussed where determinable and flagged uncertain where not.

**Item 20** — Interpretation: give a cautious overall interpretation of results considering objectives, limitations, multiplicity of analyses, results from similar studies, and other relevant evidence.
- **ADDRESSED.** Discussion interprets the matched increment as *"small and not robustly distinguishable from zero"*, situates against prior literature (Johansson 2016; Benedum 2020; EWARS-csd; seasonal-lead skill Beal 2025, D-MOSS), and cautions against attributing the compound advantage to climate. Multiplicity explicitly acknowledged (no adjustment; pointwise intervals).

**Item 21** — Generalizability: discuss the generalisability (external validity) of the study results.
- **ADDRESSED.** Discussion: *"The findings do not establish that coefficients or thresholds transport to other settings, and we make no claim of deployment readiness, transportability, causal climate effects, cost-effectiveness, rare-epidemic prediction, or universal hybrid benefit."* Colombia framed as *"a second, differently-constructed case study, not external model validation"*; complete-case sample generalizes only to the analyzed subset; conclusions scoped to short-to-medium leads.

---

## Other information

**Item 22** — Funding: give the source of funding and the role of the funders for the present study and, if applicable, for the original study on which the present article is based.
- **NOT ADDRESSED — placeholder only.** Declarations §"Funding": *"Pending author confirmation."* Ethics, data/code availability (repository URL/DOI/license), competing interests, author contributions, and acknowledgments are likewise marked "Pending author confirmation." These must be completed before submission.

---

### Summary of STROBE status
- **Fully addressed:** 1(b), 2, 3, 4, 5, 6(a), 6(b, adapted), 7, 8, 9, 11, 12(a), 12(b), 12(c), 12(d, adapted), 12(e), 13(a), 13(b), 14(c, adapted), 15, 16(a), 16(b), 16(c, adapted), 17, 18, 19, 20, 21.
- **Partial:** 1(a) (design term not in title), 10 (no explicit sample-size/precision rationale), 13(c) (pipeline figure, not a participant flow diagram), 14(a) (no full Table 1), 14(b) (per-variable missingness deferred to SI).
- **Not addressed:** 22 (funding and all other Declarations are placeholders pending author confirmation).
