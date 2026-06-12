# Specification — ΔAUC / ΔNB Confidence Intervals (design-lock)
*Pre-computation design lock for adding uncertainty intervals to the primary model comparison. **No bootstrap run; no CIs computed; no models rerun; no DLNM added; no data modified.** Documentation only. This hardens reporting quality on the already-committed primary pilot; it does **not** re-select models, re-tune thresholds, or refit anything.*

**Date:** 2026-06-12 · **Status:** specification only — locks the resampling design **before** any computation.

## Why this hardening is needed
- The harsh review and the committed self-assessment (`probast_tripod_self_assessment_v1.md`) flagged that the primary comparison reports **point estimates with no uncertainty** — a likely desk-reject for a comparative claim at a methods journal (TRIPOD R9/R11).
- Confidence intervals will **either strengthen** the M1-over-climate claim (ΔAUC/ΔNB CIs exclude 0) **or appropriately weaken it** (CIs include 0 → "no significant difference detected"). Both outcomes are acceptable and must be reported as-is.
- This is **reporting-quality hardening, not post-hoc model selection**: model predictions are held **fixed** (reused from the committed predictions file), no refitting, no threshold re-optimization, no headline change without team review.

## 1. Scope & input (fixed predictions, no refit)
- **Set:** primary pilot **h=4 / 75th-pct test set**, 2023–2025 (n = 3,926 RDHS-weeks, prevalence 0.336).
- **Input:** committed quarantined `~/data_quarantine/model_pilots/pilot_h4_75pct_v1/predictions_h4_75pct_v1.csv` (sha256 `07f5916a…`), columns `geometry_id, y, p_M1_lagged_AR, p_M2_climate_only, p_M3_climate_season_RDHS` (raw predictions). **Verify checksum before running.**
- **Comparisons:** **M1 vs M2** and **M1 vs M3** (raw predictions; recalibrated-prediction CIs are an optional later add, out of scope here).
- No model is refit; only evaluation metrics are recomputed on resamples.

## 2. Primary estimands (with 95% CI)
- **AUC** for M1, M2, M3.
- **ΔAUC** = AUC(M1) − AUC(M2); AUC(M1) − AUC(M3).
- **Net benefit at p\*=0.30** for M1, M2, M3 (NB = TP/n − FP/n · p\*/(1−p\*)).
- **ΔNB@0.30** = NB(M1) − NB(M2); NB(M1) − NB(M3).
- **Optional:** PR-AUC and ΔPR-AUC for the same pairs (event rate ~0.34 is moderate; report if cheap).
- **Threshold-band reporting (to defuse p\*=0.30 cherry-picking):** also report ΔNB and its 95% CI at **p\* ∈ {0.10, 0.20, 0.30, 0.40}**, so the conclusion is shown across the plausible band, not at one point. (Full DCA curve already committed.)

## 3. Bootstrap design
- **Primary: RDHS cluster (block) bootstrap.** Resample the **26 RDHS with replacement**; each drawn RDHS contributes its **entire** 2023–2025 test time series (all its weeks, with duplication). This respects within-RDHS spatial **and** temporal autocorrelation — the structure the self-assessment flagged. Metrics recomputed on each resampled pooled set.
- **Resamples:** **B = 200 (pilot)** first; **B = 1000 (final)** if pilot runtime is reasonable (extrapolate from pilot wall-clock). Report which B the published CIs use.
- **CI method:** **percentile 95%** (2.5th/97.5th of the bootstrap distribution) as primary; **BCa** as an optional robustness add if straightforward.
- **Reproducibility:** **fixed seed = 20260612** (passed explicitly; not `Math.random`/time-based). Record seed, B, and effective-B in outputs.
- **Caveat to state:** only 26 clusters → the cluster bootstrap is coarse and CIs may be wide/slightly anti-conservative; report this limitation rather than over-interpreting borderline intervals.
- **Sensitivity (optional, not required):** a moving-block bootstrap over weeks (block length ≈ within-RDHS autocorrelation span) as a secondary check on the RDHS-cluster CIs; only if cheap.

## 4. Stop / failure rules
- A resample is **degenerate** if its pooled `y` has a single class (all events or all non-events) → AUC/PR-AUC undefined. With 26 clusters at ~34% prevalence this should be near-impossible; if it occurs, **skip that replicate, count it as a failure**, and continue.
- **Report the bootstrap failure rate** (failed / B) per metric. If failure rate **> 5%**, **stop and report** rather than silently dropping — investigate (e.g., degenerate clustering) before trusting CIs.
- NB is defined for any resample (no failure mode); still report effective B.
- If pilot B=200 wall-clock implies B=1000 would be impractically long, **stop at B=200**, report it, and do not force B=1000.

## 5. Interpretation rules (pre-committed)
- **ΔAUC / ΔNB 95% CI excludes 0** → the M1 advantage is statistically supported at that metric/threshold → **strengthens** the claim.
- **CI includes 0** → report as **"no significant difference detected"** at that metric/threshold; **do not spin** as either a win or a refutation.
- Report **all** pairs, both metrics, and the full p\* band — **no selective reporting** of the most favorable interval.
- **Do not change the study headline based on the CIs without explicit team review** (per instruction). CIs are added to the existing committed numbers; they do not retroactively alter point estimates.

## 6. p\*=0.30 justification / threshold-range reporting
- The current p\*=0.30 is **not externally anchored** (reviewer-flagged). Two actions:
  1. **Threshold-band CI reporting** (§2) — report ΔNB(95% CI) at p\* ∈ {0.10,0.20,0.30,0.40} so no single threshold is privileged.
  2. **Justification narrative (team-written, placeholder here):** at p\*, acting is worthwhile when the benefit-to-harm ratio of an alert exceeds (1−p\*)/p\* ; p\*=0.30 ⇒ ratio ≈ 2.33 (i.e., one averted/managed outbreak-week is judged worth ~2.3 unnecessary-alert-weeks). The **team should anchor p\* to real Sri Lanka vector-control response cost/capacity** (or present the band and decline a single anchor). This spec does not invent a cost figure.

## 7. Outputs to be generated later (NOT now) — quarantined only
Directory: `~/data_quarantine/model_pilots/ci_bootstrap_v1/`
- `ci_auc_dnb_v1.csv` (per metric/pair: point estimate, 95% CI lo/hi, B, effective-B, failure rate)
- `ci_bootstrap_replicates_v1.csv` (optional: per-replicate metrics, for audit)
- `ci_bootstrap.meta.md`
CSVs read-only with SHA256; **none committed**. Safe repo report later: `docs/auc_dnb_confidence_interval_report.md`.

## 8. Confirmation
- This memo is **documentation only**; no bootstrap, CIs, model runs, or DLNM were executed.
- **No data modified; no data files created; nothing committed.** Predictions remain fixed and read-only.
- DLNM climate comparator remains **deferred** until after this CI step and only on explicit approval.

## Next step (separate, approval-gated)
On approval: verify the predictions checksum, run the RDHS cluster bootstrap (B=200 pilot → B=1000 if feasible, seed 20260612), write quarantined CI outputs + a safe markdown report, apply §5 interpretation rules. Nothing runs until directed.
