# PREANALYSIS_ALT_STATS.md — locked specification (no results appear in this file)

**Framing.** A prospectively locked secondary reanalysis, specified after the Version 6
findings were known but before any alternative-statistics results were computed. The lock
reduces analytic flexibility in this secondary analysis; it does not eliminate all concern
about metric shopping, and it does not convert the post-hoc matched ablation into a
prospectively prespecified estimand.

## 1. Estimands (setting-specific; settings not pooled; no heterogeneity test)
- **Primary:** ΔNLL = mean_NLL(full climate) − mean_NLL(matched no-climate), per setting.
  NLL_i = −[y_i log p_i + (1−y_i) log(1−p_i)]. Orientation: ΔNLL<0 favors climate.
  Signed information gain IG_nats = −ΔNLL; IG_bits = −ΔNLL/log2. Reported separately as
  ΔNLL_SriLanka, ΔNLL_Colombia. No pooled estimate.
- **Key secondary:** ΔBS = BS(full) − BS(no-climate), BS = mean (p−y)^2. Orientation ΔBS<0
  favors climate. BSS = 1 − BS_full/BS_noclim reported descriptively only; flagged unstable
  if reference Brier is very small. |ΔBS| is the key secondary quantity, not BSS.
- **Calibration (descriptive/diagnostic, not a primary outcome):** CITL (α with logit-p
  offset), calibration intercept+slope (α,β), ICI via logistic recalibration with a
  restricted cubic spline of logit(p*) at 4 knots (quantiles 0.05,0.35,0.65,0.95),
  observed prevalence, mean predicted probability, flexible calibration curve.
- **Discrimination (secondary):** AUC, PR-AUC, ΔAUC, ΔPR-AUC (whole-sample per replicate;
  no pseudo per-observation AUC differences).

## 2. Prohibited headline replacements
Accuracy, single-threshold sensitivity/specificity, F1, balanced accuracy, NRI, IDI, any
metric chosen after viewing results, any test-data-selected threshold. Not used as primary.

## 3. Prediction states (Route A; refits no prediction model for scoring)
- Sri Lanka primary: past-only rolling-52 recalibrated M5 vs recalibrated M5-no-climate;
  secondary: raw M5 vs raw M5-no-climate.
- Colombia primary: validation-fit Platt-recalibrated M5 vs recalibrated M5-no-climate;
  secondary: raw vs raw.
- Inputs are the checksum-frozen files in `ALT_STATS/frozen/` (see FROZEN_INPUTS_MANIFEST).

## 4. Numerical handling
- Clip p to [ε, 1−ε] with ε = **1e-15** (primary). Report counts clipped at each boundary,
  min/max original p, max individual NLL, and whether source p appear rounded.
- Locked sensitivity: ε = **1e-12**. "Materially changes" ≡ |Δ(ΔNLL)| > max(1e-4,
  5% of |primary ΔNLL|). Report only whether it materially changes ΔNLL. No post-hoc
  clipping variants.

## 5. Calibration procedure
Logistic calibration with restricted cubic spline of clipped logit(p*), 4 knots at the
listed quantiles, fit per setting×model×state; ICI = mean|p − P̂(Y=1|p)|. CITL and
intercept/slope via statsmodels GLM. Cluster-bootstrap uncertainty for the curve, CITL,
intercept, slope, ICI, decile-bin observed proportions (NOT Wilson intervals, because
observations are clustered). Record all fit failures/warnings; no silent fallback.

## 6. Conditional cluster bootstrap
- Paired cluster resampling (both models on identical resampled observations).
- **B = 5000** primary percentile intervals (2.5th/97.5th); seed **20260612**; numpy PCG64
  `default_rng`. Also **B = 1000**, seed 20260612, as a Version-6 parity analysis only. The
  5000-replicate result is primary; do not choose by favorability.
- Sri Lanka unit: 26 RDHS. Colombia primary unit: municipality (475); prespecified
  dependence sensitivity: department (31), reported separately (not selected by
  favorability). Repeated cluster selections retained as distinct copies; units not
  collapsed. Store full-precision replicate values.
- Per replicate compute mean NLL, ΔNLL, mean Brier, ΔBS, AUC/ΔAUC, PR-AUC/ΔPR-AUC.
- Sign frequency (1/B)Σ I(Δ_b<0): labeled "fraction of bootstrap replicates favoring the
  climate model." Never "probability climate helps / probability of benefit / posterior."
- Failure rule: if >2% of replicates fail for a primary metric, stop and diagnose (no
  method substitution without a recorded post-lock deviation); if ≤2%, report the rate and
  the locked handling (single-outcome-class AUC replicates excluded from AUC/PR-AUC only,
  counted and reported).

## 7. Development-inclusive proper-score intervals
GATED. Per `PHASE1_GATE.md`, the refit-both-models bootstrap was NOT re-executed this
session → development-inclusive proper-score intervals are **NOT computed**; conditional
intervals only. This is stated in every report. No substitute refit pipeline is built.

## 8. Interpretation rules (locked before results)
Report ΔNLL exactly as obtained; do not reframe an unfavorable result. Do not organize
interpretation solely around whether an interval includes zero; interpret jointly
(magnitude, width, direction, conditional uncertainty, calibration, concordance with the
V6 decision-curve analysis, sample selection, operational-data limits). No
operational-importance claim (no elicited minimum worthwhile ΔNLL/ΔBS/IG): use "The
analysis quantifies predictive-score differences but does not establish an operationally
worthwhile increment." Concordance categories per Section 5.4 of the prompt. Post-hoc
statement required in every report: the matched ablation remained post hoc relative to V6;
the scoring rules were locked before their computation but after the V6 findings were known.
Cross-setting language: "two complementary, differently constructed case studies"; never
replicated/transported/pooled/universal/geographically-validated. Multiplicity: primary is
ΔNLL per setting; all else secondary/descriptive, no multiplicity adjustment claimed.

## 9. Software / figures
Engine: `src/score_route_a.py` (verifies checksums, deterministic seed, full precision,
loud failure, no source modification). Figures: A paired proper-score forest (ΔNLL, ΔBS;
SL raw+recal, Colombia raw+recal; conditional intervals; DI only if audited=none here);
B calibration curves (both models, both settings, identity line, cluster-bootstrap bands,
prediction density, decile points); C compact NLL/Brier/ICI/AUC/PR-AUC summary. Murphy
diagram optional/secondary, not a primary replacement.
