# Computation / code / output / dataset verification — v9 (corrected)

## Scope and corrected verdict
This was a **read-only traceability and code-inspection audit**. It did **not** re-run preprocessing, model fitting, calibration, recalibration, bootstrapping, or output generation.

> The manuscript values examined were consistent, after rounding, with the committed result files. The inspected scripts implemented the documented train/test separation, train-defined alert labels, validation-period recalibration, decision-curve formula, and spatial-unit resampling logic. No obvious discrepancy was identified in the inspected files. Because the pipeline was not re-executed from source inputs, this audit establishes **traceability and internal consistency**, not independent computational reproduction.

The earlier ("v8") phrasing — "dataset is sound", "code is correct", "code is leakage-safe", "everything verified", and "ALL-MATCH" as proof of computational validity — is **withdrawn** and replaced by the categorized findings below. "Match" here means a committed-output value rounds to the manuscript value, not that the computation was independently reproduced.

## Provenance of the review (corrected)
> The verification used internal AI-assisted role-based review perspectives. These were not independent human experts or external peer reviewers.

It is **not** field-expert validation, independent expert consensus, or human-specialist verification.

## Evidence categories (kept distinct; not merged)
1. **Directly verified from committed output** — value read from a committed `*.csv`/`*.json`.
2. **Rounding match** — committed value rounds to the manuscript value at the stated precision.
3. **Verified by static code inspection** — logic read in source; not executed.
4. **Verified by deterministic arithmetic** — recomputed only non-model arithmetic from committed cells.
5. **Not independently verified without pipeline re-execution.**

---

## A. Dataset / analysis-table checks
Inspected: the analysis-ready Sri Lanka linked table and the Colombia committed prediction/meta files — **row counts, date ranges, unit counts, missingness summaries, metadata and checksums**. This is **not** verification of raw-source correctness: the original provider acquisition files were **not** independently re-checked against their providers (category 5).

| Claim | Location | Reported | Evidence type | Source path | Row/key | Source value | Rounding | Verdict | Limitation |
|---|---|---|---|---|---|---|---|---|---|
| SL linked rows = 10,868 | meta | 10,868 | 1 | `data_quarantine/analysis_tables/dengue_climate_population_linked_2018_2025_v1.csv` | `wc -l` − 1 | 10,868 | exact | match | row count only |
| 10,842 backbone + 26 outcome-only | meta | split | 1 | same | `awk exposure_missing_flag` | 10,842 / 26 | exact | match | flag-count only |
| 26 RDHS units | Methods | 26 | 1 | same | distinct `geometry_id` | 26 | exact | match | — |
| Period 2018–2025 | Methods | 2018–2025 | 1 | same | distinct `epi_year` | 2018..2025 | exact | match | — |
| Fully-modelable rows | meta | 10,731 | 1 | same | 3 flags == 0 | 10,731 | exact | match | — |
| Colombia test n = 13,361 | L313 | 13,361 | 1 | `colombia_model_ladder_h4_75pct_v1.meta.json` / predictions CSV | `primary_counts.test` | 13,361 | exact | match | — |
| Colombia test prevalence 0.375 | L313 | 0.375 | 4 | predictions CSV | mean(y) | 5015/13361 = 0.37535 | 3 dp | rounding match | descriptive count, not a model metric |
| Input checksums (outcome/exposure/pop) | meta | — | 1 | `.meta.md` | input rows | match (per meta) | — | not independently re-derived | category-5: provider files not re-checked |

## B. Output-to-manuscript traceability (headline metrics + intervals)
Evidence type 1/2 unless noted. Committed → manuscript.

**Colombia** (`colombia_model_pilots/model_ladder_h4_75pct_v1/`, `recal` rows):
- AUC M0–M5 0.51292/0.68519/0.55640/0.56411/0.69874/0.72548 → 0.513/0.685/0.556/0.564/0.699/0.726.
- CITL −0.5046/−0.4611/−0.4966/−0.5381/−0.4452/−0.5049 → −0.50/−0.46/−0.50/−0.54/−0.45/−0.50.
- slope 3.4330/1.0928/0.8531/1.2766/1.0450/1.1601 → 3.43/1.09/0.85/1.28/1.05/1.16.
- Brier 0.213–0.250 range; NB@0.30 0.10764/0.11706/0.10764/0.10764/0.12930/0.13583 → 0.108/0.117/0.108/0.108/0.129/0.136.
- ΔAUC(M5−M1) [0.023455,0.057508] → +0.040 [0.024,0.058]; ΔNB(M5−M1)@0.30 dNB 0.0187753, CI [0.0116685,0.0260056] → +0.0188 [0.0117,0.0260]; B=1000, failures=0.

**Sri Lanka** (`model_pilots/pilot_h4_75pct_v1/`, `hybrid_model_extension_v1/`, `targeted_value_climate_stage1a_h4_v1/`):
- M1 0.7515/0.6517/0.1907/+0.5129/1.2457/0.13663 → 0.752/0.652/0.191/+0.513/1.246/0.137.
- M4 0.7643/+0.449/1.225/0.12837 → 0.764/+0.449/1.225/0.128; M5 0.7715/0.6674/0.1801/+0.4398/1.0774/0.14471 → 0.772/0.667/0.180/+0.440/1.077/0.145.
- ΔNB(M4−M1)@0.30 −0.00826 [−0.0278,0.01277] → −0.008 [−0.028,+0.013]; ΔNB(M5−M1)@0.30 0.00808 [−0.0012,0.01809] → +0.0081 [−0.0012,+0.0181]; @0.40 0.02411 [0.00899,0.03991] → +0.0241 [+0.0090,+0.0399]; @0.20 0.00955 [−0.00045,0.01873] → +0.0096; regime (high-incidence×strong-AR) 0.02022 [0.00378,0.03702], 8 clusters → +0.0202.
- Tables 1–3 (M0–M3 metrics; representative thresholds 0.20/0.30/0.34/0.40) traced to `metrics_h4_75pct_v1.csv` and the pilot DCA CSV.

## C. Static code inspection (category 3 — read, not run)
Scripts read: `colombia_model_ladder_h4_75pct_v1.py`, `colombia_label_construction_v1.py`, `colombia_lag_feature_assembly_v1.py`, `decision_threshold_dnb_robustness_v1.py`.
Properties checked by reading the source:
- Net-benefit function computes `tp/n − (fp/n)*(t/(1−t))`.
- Alert label = exceedance of a **train-split-only** percentile (`split=='train'`), strict `>`, future-absent → NaN.
- Scaler built from train and reused on val/test; penalty C selected on validation log-loss.
- Cluster bootstrap resamples the spatial unit (GID_2 / RDHS) with replacement, retains all weeks, skips one-class resamples; seed/B recorded.
- Platt recalibration fit on validation, applied to test; M4=M1+M2 lags, M5=M4+season+dept FE.
> No obvious inconsistency was identified during static inspection.
This does **not** prove the absence of leakage or bugs; it confirms the inspected code matches the documented design.

## D. Deterministic arithmetic (category 4)
- Threshold odds 0.30/0.70 = 0.42857 → 0.429; reciprocal 0.70/0.30 = 2.333 → 2.33.
- Colombia ΔNB = NB_M5 − NB_M1 = 0.1358324 − 0.1170571 = 0.0187753 → +0.0188.
- Per-100 translations: 0.0188×100 = 1.88 → 1.9 (interval 1.2–2.6); false-alert 4.39 → 4.4 (2.7–6.1).
- SL prevalence shift 1593/6590 = 0.2417 → 24.2%; 1321/3926 = 0.3365 → 33.6%.
- SL 0.34 threshold row (alert-all/none/M0/M1/M2/M3) and 0.30 row match the pilot DCA CSV.

## E. Not independently verified without pipeline re-execution (category 5)
- Preprocessing reproducibility (linkage, scaling, feature assembly from raw inputs).
- Model-fitting reproducibility (penalized logistic fits; coefficients).
- Optimizer convergence under a recreated environment.
- Bootstrap reproducibility (resampling distributions; CI endpoints re-derived).
- Random-seed reproducibility — note the Sri Lanka **targeted-value bootstrap seed was not retained** (that interval is checkable only as a committed value).
- Dependence on **unavailable historical Python package versions** (no environment/requirements/lock file committed; not reconstructable in writing).
- Raw-source-to-analysis-table fidelity where original acquisition files are unavailable.

These are addressed by the (not-yet-run) plan in `isolated_reproducibility_rerun_plan_v9.md`.
