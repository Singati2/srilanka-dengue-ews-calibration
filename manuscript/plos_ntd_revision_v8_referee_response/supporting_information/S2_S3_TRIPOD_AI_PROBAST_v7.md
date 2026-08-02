# PROBAST / TRIPOD+AI internal assessment — DRAFT (prediction-model reporting & risk of bias)

> This is the **prediction-model** reporting and risk-of-bias self-assessment (S2/S3), clearly distinguished from the journal-facing **STROBE** observational checklist (S1). Internal draft for author review.

## TRIPOD+AI reporting (selected items; locators to be finalized)
| Item (abridged) | Addressed? | Location |
|---|---|---|
| Title/abstract identify a prediction-model study | Yes | Title; Abstract |
| Source of data; eligibility; outcome; predictors | Yes | Methods |
| Sample size; missing data | Partial | Results cohort; Methods missingness (EPV in S5 Table — transcribe, no recompute) |
| Model: type, predictors, penalty, tuning | Partial | Methods (L2/ridge; selection on training only) + S5 `[confirm exact penalty/C grid/versions]` |
| Performance: discrimination, calibration, net benefit | Yes | Results Tables; calibration; DCA |
| Model updating/recalibration | Yes | Methods/Results recalibration |
| Uncertainty (bootstrap) | Yes | Methods: B, seed (20260612), cluster unit, percentile CI, one-class handling |
| Interpretation/limitations | Yes | Discussion |
| Data/code availability | Draft | Declarations + DAS draft |
| AI use in development | Yes | AI-assistance disclosure |

## PROBAST risk-of-bias domains (signalling summary; author to finalize judgments)
| Domain | Provisional judgment | Basis |
|---|---|---|
| Participants/units | Low–unclear | RDHS-/municipality-week, complete-case, public surveillance; percentile labels not official outbreak declarations (limitation) |
| Predictors | Low | Defined from data available at/before predictor week; train-only scaling |
| Outcome | Unclear | Percentile-threshold alert, not an official outbreak definition (stated limitation) |
| Analysis | Unclear–high | Single temporal holdout (not rolling-origin/spatial-block); pointwise CIs, no multiplicity adjustment; some components documented extensions (stated) |

**Note:** these provisional judgments are for author review; finalize after confirming model-spec/EPV details. Imported thermal-suitability curves (biomodel) are **not** used here and are not claimed as locally validated biology.

---
## v7 transparency note (TRIPOD+AI graphical calibration item)
Flexible graphical calibration curves were **not generated** in the frozen analysis. Calibration is reported by calibration-in-the-large, calibration slope, mean predicted probability (where preserved), observed prevalence, and Brier score. This is disclosed in the manuscript Methods and recorded here for the TRIPOD+AI calibration item. No new curve was produced.
