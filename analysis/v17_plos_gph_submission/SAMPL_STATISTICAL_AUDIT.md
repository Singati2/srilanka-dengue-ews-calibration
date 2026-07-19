# SAMPL Statistical-Reporting Audit

**Guidelines:** SAMPL (Statistical Analyses and Methods in the Published Literature; Lang & Altman).
**Manuscript audited:** `manuscript/paper1_validity_corrected_candidate/paper1_plos_gph_submission_ready.tex` (PLOS Global Public Health submission candidate).
**Study:** retrospective, observational, decision-analytic evaluation of climate-informed dengue elevated-activity alerting — Sri Lanka RDHS-week 2018–2025 (primary) and Colombia municipality-week 2020–2022 (secondary case study).

Each item is rated **Adequate / Partial / Missing**, with manuscript location or the specific gap. All quotes are verbatim from the manuscript; **no software versions are invented here** — version claims are reproduced only where the manuscript states them.

---

## 1. Study design
**Adequate.** Methods §"Study design and reporting": *"We conducted a retrospective decision-evaluation of dengue early-warning models…"*; primary/secondary framing and estimand roles laid out in Table `tab:analysisstatus`. Design term also in Abstract ("retrospective decision-analytic evaluation").

## 2. Setting and dates
**Adequate.** Sri Lanka fit 2018–2022 / test 2023–2025 (§"Model ladder and fitting"); Colombia train 2006–2017 / validation 2018–2019 / test 2020–2022 (Results §"Colombia"). Spatial frames (26 RDHS; Colombia municipality/GID_2) in §"Settings and spatial units". Colombia data provenance (OpenDengue Temporal extract v1.3) stated, with the caveat that the **version-specific record identifier and acquisition date were not preserved** (§"Surveillance outcomes and alert labels").

## 3. Eligibility / inclusion criteria
**Adequate.** Complete-case unit-week frame; Sri Lanka: *"Rows with missing outcome, exposure, or population were excluded from the complete-case frame."* Colombia common-complete intersection defined by M1–M5 predictors, with a dedicated §"Colombia complete-case selection" quantifying selection and stating inference applies to the analyzed subset.

## 4. Outcome definition (elevated-activity label, horizon h=4)
**Adequate.** §"Surveillance outcomes and alert labels": unit-specific **training-period 75th-percentile** weekly-incidence exceedance; **primary horizon h=4** by date-based join (*"the calendar week beginning 28 days later"*), not a positional shift; 90th-percentile stricter label and h=1,2,8,12 as sensitivities. Labeled as elevated-activity alerting (≈1/3 of weeks), explicitly not rare-epidemic prediction.

## 5. Predictors
**Adequate.** §"Model ladder and fitting": M0–M5 ladder; recent-case incidence lags; climate block (Sri Lanka DLNM-style cross-basis temp/precip/humidity, lags 0–8, df=3; Colombia linear precip/temp lags 0–8, no humidity); seasonal harmonics; geographic fixed effects. Per-country feature differences explicitly flagged; full lists deferred to S5 Table.

## 6. Missing-data handling
**Adequate.** Documented missingness retained rather than imputed; duplicate WER issue excluded; *"early-series missing lags used training-period imputation rules"* (§"Model ladder and fitting", §"Climate exposures…"). Colombia complete-case with IPW sensitivity (§"Colombia complete-case selection"). Minor gap: per-variable missingness counts not tabulated in main text (deferred to SI).

## 7. Exclusions
**Adequate.** Sri Lanka: rows lost to target construction (10,705→10,516) and complete-case filtering; duplicate issue 53 excluded, missing issue 43 retained as missingness. Colombia: 127,703 → 79,785 common-complete; test 21,646 → 13,361 (62%); included-vs-excluded differences quantified.

## 8. Sample sizes
**Adequate.** Sri Lanka Results §"Cohort and data alignment": train 6,590 (1,593 events), **test 3,926 (1,321 events)**. Colombia **common-complete test n=13,361** (prevalence 0.375); 2022 subset 4,802 (2,202 events). No formal power/precision calculation (acceptable for a fixed retrospective panel, but not explicitly stated as such).

## 9. Clustering (26 RDHS; municipality)
**Adequate.** §"Uncertainty, multiplicity, and analysis status": cluster bootstrap resamples the spatial unit (RDHS Sri Lanka, municipality/GID_2 Colombia), retaining all weeks within a sampled unit; *"The Sri Lanka cluster bootstrap resampled 26 RDHS units."* Limited-cluster coverage caveat stated; 8-cluster regime intervals explicitly declared not interpretable as valid bootstrap CIs.

## 10. Model tuning (L2 penalty; C selection)
**Adequate.** §"Model ladder and fitting": *"The primary logistic models used L2 (ridge) penalization; the regularization strength was selected on the training data only,"* with convergence/separation stop rules (none triggered). Rolling-origin/exploratory refits used fixed C=1.0 for tractability (§"Additional post hoc analyses"). Note: frozen Sri Lanka M1 near-unpenalized (C=10^6, AR-only standardization) — disclosed as the reason M5−M1 is not specification-matched (Results §"Sri Lanka structured-climate and hybrid results").

## 11. Recalibration (cross-fit vs past-only rolling-52)
**Adequate.** §"Calibration and time-updated recalibration": primary = **rolling 52-week intercept-only** past-only recalibration; rolling-104, expanding-window, and intercept+slope variants evaluated. Colombia uses **validation-period Platt scaling**. §"Recalibration sensitivity…" contrasts past-only rolling-52 (leakage-free, operational) with cross-fitted ISO-week-parity Platt (*"leakage-controlled but internal and optimistic"* upper bound). Numerical effects and the recalibration-dependence of the Sri Lanka matched increment (+0.0087 raw → +0.0157 recalibrated) reported with CIs.

## 12. Uncertainty quantification (what the bootstrap does / doesn't capture)
**Adequate.** §"Uncertainty…": *"Each replicate recomputed net benefit … on the frozen, already-fitted test-set predictions; it did not refit the prediction models, repeat penalty selection, or refit recalibration. The intervals therefore reflect conditional test-set sampling uncertainty and do not capture model-development uncertainty."* B=1000 percentile intervals, zero failures. **Colombia development-inclusive** refit-bootstrap reported for the matched increment (widens to −0.0001 to +0.0244, includes zero). Seed **20260612** stated for the Sri Lanka targeted-value regime bootstrap and the Colombia matched decomposition; *"seeds are recorded [in S6 Table] where preserved"* — i.e., not all seeds preserved.

## 13. Sensitivity analyses (threshold, horizon, reporting-delay, pre-pandemic, IPW selection)
**Adequate.** All present: threshold grid (§"Threshold and stricter-outcome robustness"); horizon h=1–12 (§"Horizon", Fig 9); reporting-delay feature-censoring (§"Robustness of the Colombia climate increment", 3-week matched +0.0049); pre-pandemic split (+0.0199, confounded by 2016 Zika / 2019 epidemic); IPW selection (§"Colombia complete-case selection", IPW +0.0079 vs unweighted +0.0078). Each explicitly labeled post hoc / pointwise / multiplicity-unadjusted, with limitations of each stated (esp. reporting-delay is emulation, not true reporting triangles).

## 14. Software names + versions
**Partial (correctly flagged by authors).**
- **R:** *"the canonical distributed-lag nonlinear comparator was fit in R 4.6.0 with the `dlnm` package"* (§"Model ladder and fitting"; RCoreTeam2026 = "Version 4.6.0", Gasparrini2011 = dlnm JSS). S5 Table caption lists **R 4.6.0, `dlnm` 2.4.10, `mgcv` 1.9.4, `tsModel` 0.6-2** — versions ADEQUATE for the R stack.
- **Python:** named as the environment for the penalized logistic models but **versions NOT preserved** and explicitly flagged: *"versions of the Python modeling stack were not preserved in the reproducibility record and are marked as such"* (§"Model ladder and fitting"; repeated in S5 Table caption).
- **Gap:** the Python interpreter version and specific library versions (e.g., scikit-learn / numpy / statsmodels) are absent — a genuine reproducibility gap, transparently disclosed rather than concealed.

## 15. Multiplicity
**Adequate.** §"Uncertainty…": *"Threshold, horizon, percentile, and regime analyses were secondary or exploratory, with pointwise intervals and no multiplicity adjustment."* Restated at each secondary result. No adjustment is made, but the absence is disclosed consistently.

## 16. Effect measures and CIs
**Adequate.** Primary decision metric = net benefit at p*=0.30 (formula given, §"Decision-curve analysis…"); discrimination (AUC, PR-AUC), calibration (CITL, slope, Brier) reported. All key contrasts carry 95% CIs (percentile cluster-bootstrap), with sign/zero-crossing interpretation.

## 17. Estimand / prespecification status
**Adequate.** Table `tab:analysisstatus` classifies every contrast (prespecified? matched? role). Design-lock provenance dated (commit 1d8e268, 2026-06-14 13:24 before results report 02f986e). Matched contrasts explicitly post hoc. *"No prospective public registration is claimed."*

---

## Top statistical-reporting gaps (submission-relevant)

1. **Python software versions not preserved.** The primary penalized-logistic models (all M0–M5 net-benefit/calibration results) were fit in Python, but no interpreter or library versions are recorded — only the secondary R `dlnm` comparator is fully versioned (R 4.6.0, dlnm 2.4.10, mgcv 1.9.4, tsModel 0.6-2). This is transparently flagged but remains a reproducibility limitation reviewers will note; a pinned environment (or at least captured versions) should accompany the code release.

2. **Funding, competing interests, and data/code-availability specifics are placeholders.** Declarations read "Pending author confirmation," and the OpenDengue v1.3 version-specific record identifier + acquisition date and the repository URL/DOI/license are unresolved. SAMPL/journal reporting requires these before submission.

3. **Uncertainty intervals are conditional and multiplicity-unadjusted, with a small/fragile cluster base.** Primary CIs condition on frozen fitted predictions (omit model-development uncertainty except for the one Colombia development-inclusive refit); the Sri Lanka matched increment separates from zero only after recalibration and rests on 26 RDHS clusters (regime analyses on 8 clusters are non-interpretable); no multiplicity control across the threshold/horizon/percentile grids. All are disclosed, but the effective evidential strength for the climate increment is correspondingly weak and should not be over-read.

*(Secondary, minor:)* per-variable missing-data counts and a descriptive Table 1 of exposure distributions are deferred to Supporting Information rather than shown in-text; per-model mean predicted probabilities were not retained in the Colombia reproducibility record (disclosed in Table `tab:colombia`).
