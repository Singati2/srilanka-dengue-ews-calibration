# Pilot Specification — Existing-Model Calibration / Decision-Curve Evaluation
*Pre-modeling design lock for the first calibration + decision-curve pilot. **No models have been run; no outbreak/alert labels created; no AUC, calibration, decision-curve, regression, net-benefit, or forecast quantities computed.** No frozen or quarantined data file is modified or committed — this memo is documentation only. It operationalizes, without changing, the registered plan (`preregistration_analysis_plan_v1.md` and its 2026-06-12 analysis-frame addendum).*

**Date:** 2026-06-12 · **Status:** specification only — locks choices **before** any computation to prevent post-hoc tuning.

## 1. Primary analysis table
- **Table:** `~/data_quarantine/analysis_tables/dengue_climate_population_linked_2018_2025_v2_date_aligned.csv` (quarantined, read-only, not committed).
- **SHA256:** `3a197d610fde721ffdf2be6388df88fea675a5b49bf131a0919fd89ec2518e91`.
- **Primary modeling filter:** `outcome_missing_flag==0 ∧ exposure_missing_flag==0 ∧ population_missing_flag==0 ∧ 2018 ≤ epi_year ≤ 2025` → **10,705 RDHS × epi-week rows**.
- Unit of analysis: one RDHS × ISO epi-week. Outcome basis: `dengue_current_week_cases`; denominator: `population_rescaled` → incidence per 100k (already present as the QC field `dengue_incidence_per_100k`).

## 2. Prediction target / forecast horizon
- **Primary horizon: h = 4 weeks ahead.** Features observed through week *t* (RDHS *i*) predict the alert state at week *t+4*. Justification: (a) operationally actionable lead time for RDHS-level vector control (source reduction, larviciding, risk messaging) — a 1-week horizon is too short to mobilize; (b) consistent with the climate→*Aedes*→transmission lag structure (egg/larval development + extrinsic incubation), which concentrates climate signal at ~4–12-week lags; (c) keeps a large usable sample (only the last 4 weeks per RDHS-year drop out).
- **Sensitivity horizons (if feasible after the primary pass):** h = 1, 2, 8, 12 weeks. Horizon is fixed *before* fitting; not selected on performance.

## 3. Alert / outbreak label definition (PROPOSED — not created yet)
A binary alert label `y_{i,t} = 1` if RDHS-*i* incidence in week *t* exceeds an RDHS-specific threshold. **All thresholds are estimated on the TRAINING period only (2018–2022) and frozen before touching the test period** — no leakage, no post-hoc tuning.
- **PRIMARY rule (recommended): RDHS-specific historical 75th percentile** of weekly incidence over 2018–2022. Rationale: yields a non-rare, non-saturating event (~20–25% training base rate by construction) → stable calibration/DCA estimation and a meaningful net-benefit comparison; an "above-usual transmission" signal that is interpretable per division.
- **SENSITIVITY rule: RDHS-specific historical 90th percentile** (2018–2022) — higher-specificity "elevated-outbreak" definition; expect a rarer event (~10%) and will trigger the PR-AUC and rare-event stop checks (§11).
- **Tertiary (only if a defensible source exists): a fixed national incidence threshold per 100k** — included *only* if the Epidemiology Unit publishes an operational cutoff; otherwise omitted (we will not invent one).
- Labels are derived from the frozen outcome/denominators at evaluation time; **none are created in this memo.** The endemic-channel centile here is consistent with the threshold language in prereg §N.

## 4. Candidate model classes (hardened first-pass ladder)
All models output a **predicted alert probability** `P(y_{i,t+4}=1 | info ≤ t)`; count models (NB) are mapped to alert probability via the same RDHS threshold. Each model is a single, pre-specified, hardened fit (no feature/grid search in the pilot).
- **M0 — Seasonal climatological baseline (reference):** empirical alert frequency for (RDHS × ISO-epi-week-of-year) estimated on training; the "same-week historical risk" null any climate model must beat.
- **M1 — Lagged dengue autoregressive baseline:** adds recent observed incidence (lags of `dengue_current_week_cases`, e.g. *t*, *t−1*, *t−4*) — the surveillance-only benchmark (no climate). Uses only past cases (no future leakage).
- **M2 — Climate-only GLM:** logistic (primary) or negative-binomial on **lagged** `t2m_mean_c` (and t2m_min/max), `rh_mean_percent`, `precip_sum_mm`, via distributed lags (DLNM or discrete lag features, lag span per §9-S2). No autoregressive term — isolates climate's standalone predictive/decision value.
- **M3 — Climate + seasonality + RDHS fixed effects:** M2 plus harmonic seasonality (annual + semiannual sin/cos of ISO week) and RDHS fixed effects — the primary "existing climate-driven EWS" form for the calibration/DCA contribution.
- **M4 — (Deferred) BYM2 spatial extension:** uses the existing 26-RDHS adjacency graph. **Not in the first pilot** unless the spatial machinery is already implemented and validated; added only as a later, separately-gated step.

The headline contribution is calibration + net-benefit of M2/M3 vs the M0/M1 baselines — not chasing discrimination.

## 5. Calibration assessment (primary axis)
Reported per model on the test period (and after recalibration): **calibration intercept** (calibration-in-the-large), **calibration slope**, **flexible calibration curve** (loess) plus a **decile/grouped reliability plot**, **Brier score** (+ Brier skill score vs M0), and **Expected Calibration Error (ECE)**. Recalibration (intercept-only and intercept+slope / Platt) is **fit on training only** and its effect on the calibration metrics and on the decision conclusions is reported (per the go/no-go "survives recalibration" criterion).

## 6. Discrimination (secondary)
**AUC/ROC** and, because the event is moderately-to-low prevalence, **PR-AUC** (with the base rate stated). Explicitly framed as **secondary to calibration and decision value** — a model may discriminate equally yet differ materially in net benefit; that gap is the paper's point.

## 7. Decision-curve analysis / net benefit
- **Threshold-probability grid: p\* = 0.05 → 0.50** (step 0.01; reported at 0.05 increments), spanning plausible alert cost ratios.
- Comparators: **alert-all** and **alert-none**.
- Report **net benefit** NB(p\*) and **standardized net benefit** for each model across the grid; highlight the cost-anchored `p*` band from prereg §M.
- **No post-hoc threshold optimization** — the full curve is reported; no single "best" threshold is selected from the data.

## 8. Validation design
- **PRIMARY (first pilot): temporal holdout.** Train = **2018–2022**, Test = **2023–2025**. Respects time ordering (no look-ahead), is simple and hardened, and matches the registered frame. **All** label thresholds, baseline climatologies, model coefficients, and recalibration parameters are estimated on train only; the test period is untouched until the single final evaluation.
- **SECONDARY (if simple enough): rolling-origin** (expanding-window) validation as a robustness check on the temporal split. Not primary for the first pass.

## 9. Sensitivity analyses (carried from the preregistration addendum)
- **S1 — Naive literal-week linkage (v1):** repeat the pilot on the v1 `week==epi_week` table (`d892f62f…`) to quantify the impact of the 1–2-week misalignment on calibration/DCA.
- **S2 — Climate-lag sweep 0–8 weeks:** vary the climate distributed-lag span; lag is a primary robustness axis given the year-varying offset finding.
- **S3 — Drop late-2021 anomaly window:** exclude the late-2021 calendar-anomaly weeks (around ISO 2021-W41/W51) and confirm conclusions are unchanged.

## 10. Outputs to be produced later (NOT now)
When the pilot is approved and run, all heavy outputs stay **quarantined and git-ignored**:
- quarantined prediction table (per RDHS × week: predicted probability, label, fold);
- quarantined metrics CSV (calibration/discrimination/DCA per model × horizon × sensitivity);
- a **safe markdown pilot report** (the only committed artifact), with checksums of the quarantined outputs.
- **No raw or model-output CSV is committed.** No outbreak label file is committed.

## 11. Stop rules / go-no-go (pre-specified)
Halt and report (do not tune to rescue) if:
- **Event too rare/common:** primary-label base rate <5% or >50% in *either* train or test → re-examine the label (escalate to the 90th-pct or fixed-threshold variant) before proceeding; document, don't silently retune.
- **Unstable event counts:** test-period positive events too few for stable estimation (e.g. <~50 pooled, or RDHS-strata with 0 events) → report instability; pool or widen rather than over-interpret.
- **Convergence/separation:** any GLM shows non-convergence or quasi-/complete separation (notably M3 with RDHS FE) → flag; use penalized estimation (Firth/ridge) or drop the offending term, documented.
- **DCA dominated:** if, across the *entire* plausible p\* band, every candidate is dominated by alert-all or alert-none → there is no decision value; **downgrade to a methods/data note** per prereg §O (do not escalate model search).
- Tie-in to prereg §O GO/NO-GO: a publishable pilot requires a material, **recalibration-robust** net-benefit difference at `p*` with spatially coherent flips; otherwise report the null honestly.

## 12. Confirmation
- **No models were run.**
- **No outbreak/alert labels were created** (label rules are proposed only, to be derived from frozen data on training at run time).
- **No AUC, calibration, decision-curve, regression, net-benefit, or forecast quantities were computed.**
- **No frozen outcome/exposure/population or linked-analysis CSV was modified**; none was committed.
- This memo is the sole artifact; only safe markdown is proposed for commit.

## Next step (separate, approval-gated)
On approval of this specification, run the **single hardened first pass**: derive the primary 75th-pct labels on 2018–2022, fit M0–M3, evaluate calibration → discrimination → DCA on 2023–2025 at h=4, apply the §11 stop rules, write the quarantined outputs + a safe markdown pilot report for review. Nothing runs until directed.
