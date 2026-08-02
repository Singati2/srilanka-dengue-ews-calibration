# Matched Climate Ablation at the 90th-Percentile Outbreak Label — Specification (memo only — NO run)

*Pre-registers the **climate-specific matched ablation** ΔNB(M5 − M5_no-climate) at the 90th-percentile outcome definition, in both settings, in response to expert-panel review finding #1 (PLOS GPH readiness review, 2026-07-26). **Specification only: no models fit, no predictions or metrics produced, no labels or thresholds created, no quarantine/data outputs modified, nothing committed.** The 75th-percentile h=4 matched ablation remains the reference analysis; the 90th-percentile matched ablation is a post-hoc, exploratory, reviewer-responsive sensitivity.*

**Date:** 2026-07-26 · **Status:** specification only · **Builds on:** the frozen matched-ablation pipeline (`phase2_analysis/src/freeze_matched_predictions.py`, `score_route_a.py`), the locked E3 outbreak-threshold spec (`docs/colombia_outbreak_threshold_sensitivity_spec.md`), and `docs/colombia_model_ladder_spec.md`.

## 0. Why this analysis (motivation, verified)
The panel's single MAJOR-revision item: the paper's **primary climate-specific estimand** — the matched ablation ΔNB(M5 − M5_no-climate), which independently refits an otherwise-identical model with the 18-column climate feature block removed — is evaluated **only at the 75th-percentile label**. Verified against the quarantine:

- E3 (`colombia_model_pilots/outbreak_threshold_sensitivity_v1`) fit the ladder **M0–M5** at the 75/80/90th percentiles and reproduces the manuscript's **compound** ΔNB(M5−M1) exactly (75th +0.0188, 80th +0.0157, 90th +0.0092; Colombia 90th test prevalence 0.2347).
- E3 did **not** fit `M5_no-climate` at any threshold. The matched (climate-specific) comparator exists only in `freeze_matched_predictions.py`, which is hard-wired to the 75th-percentile label file (`colombia_modeling_table_h4_75pct_v1.csv`). **The climate-specific increment therefore exists only at 75th.** The finding is correct; this spec closes the gap.

## 1. Estimand (locked)
Primary quantity, per setting, at the 90th-percentile label:
**ΔNB(M5 − M5_no-climate) at p\*=0.30, h=4**, where M5_no-climate is M5 with **only** the 18 climate columns removed and **independently refit** under the identical development protocol (same rows, model family, C-grid, recalibration). This is a **predictive feature-block contrast, not a causal climate effect** — identical framing to the 75th-percentile matched ablation. No new predictors, lags, DLNM variants, horizons, or geographic splits are introduced.

## 2. Analysis status & hierarchy (no headline substitution)
- **75th-percentile h=4 remains the reference** matched ablation throughout the manuscript.
- The 90th-percentile matched ablation is **post-hoc, exploratory, reviewer-responsive sensitivity** — never relabelled primary, confirmatory, or prospectively registered.
- **Report the result regardless of sign or significance**, including if it is smaller, zero-spanning, or unstable. No percentile is selected as a new headline. The 80th-percentile matched ablation may be computed in the same run for completeness but is secondary to 90th.

## 3. Settings & primary inferential target
- **Sri Lanka (primary arm):** RDHS division-week; 90th-percentile label; conditional **and** development-inclusive RDHS-cluster bootstrap.
- **Colombia (secondary arm):** municipality-week complete-case subset; 90th-percentile label; conditional **and** development-inclusive **department**-cluster bootstrap.
- **Primary inferential target = the development-inclusive interval** (both models refit within each cluster resample), consistent with the manuscript's stated primary basis for robustness. The conditional (frozen-prediction) interval is secondary.

## 4. Frozen inputs & threshold provenance (verify before any run)
- **Colombia label:** use the **already-computed train-only `thr90`** in `colombia_label_features_v1/colombia_label_thresholds_train_only_v1.csv` (verified present; GID_2-specific; train-only), or E3's committed `outbreak_threshold_sensitivity_v1/colombia_outbreak_threshold_labels_v1.csv`. **Do not recompute or modify** any committed threshold/label file. Verify checksum and train-only provenance first; **stop** if provenance is unclear or keys duplicate/missing.
- **Sri Lanka label:** derive the 90th-percentile RDHS label with the **identical train-only construction** used for the 75th (the matched pipeline currently computes the per-unit `quantile(0.75)` inline; change to `0.90` on the **training split only** — no validation/test information in the threshold). Save as a **new versioned** output.
- **Features/rows:** identical feature matrices and common-complete row rules as the 75th-percentile matched ablation; climate lags 0–8 and case lags complete; same train/val/test periods; **test used once**.
- **Model fitting:** same L2 C-grid selected on validation only; same past-only (rolling) recalibration; same seeds — **development-inclusive bootstrap seed 20260612, B=1000**; proper-score/parity seed 20260719 where applicable. M5 and M5_no-climate **both refit** per resample in the DI bootstrap.

## 5. Common-complete row-set & reporting (per setting, at 90th)
Report: total n; #clusters (RDHS units / departments); #events; **event prevalence**; min & median events per cluster; #clusters with zero test events. Make explicit any row-set difference from the 75th-percentile matched ablation (label availability may differ). Do **not** force identical rows across percentiles.

## 6. Sparsity & stop rules (pre-specified, objective)
Downgrade the 90th-percentile matched ablation to **descriptive/exploratory (or stop)** if, in either setting: the test outcome is one-class; too few test events for stable calibration/DCA; a large fraction of clusters have zero test events; **cluster-bootstrap failure rate > 5%**; recalibration parameters non-identifiable; or CIs are unreliable from sparse cluster-level events. Report **actual event counts** and the reason for any downgrade — never hide an attempted-but-unstable 90th result. If 90th is unstable but 80th is adequate, report the 80th matched ablation as the sensitivity and the attempted 90th with its instability.

## 7. Metrics (per setting, at 90th)
Per model (M5, M5_no-climate) and their contrast: AUC; PR-AUC; Brier; CITL; calibration slope; ICI; **NB at p\*=0.30**; DCA across p\*=0.10–0.50; ΔNB(M5 − M5_no-climate) with conditional and development-inclusive 95% cluster-bootstrap intervals. Because prevalence falls substantially at 90th (Colombia ~0.235), **emphasize calibration, PR-AUC, decision-curve net benefit, and event counts — AUC alone must not drive the conclusion.**

## 8. Pre-registered interpretation guardrails
- The 90th-percentile label is a **train-only percentile of a drifting series**, so it is **not epidemic-rare** (Colombia test prevalence ≈ 23.5%); state this explicitly and do not describe 90th as a true outbreak/epidemic threshold.
- A **smaller or zero-spanning** 90th-percentile matched increment is a legitimate, publishable outcome — it either strengthens the near-null or honestly bounds where any climate signal concentrates. It must not be spun as a positive.
- The compound already shrinks 75th→90th (+0.0188 → +0.0092); the climate-specific matched increment is expected to be **smaller still**. Pre-committing to report it regardless prevents outcome-dependent framing.

## 9. Deliverables (later run, gated & committed only on approval)
1. New **versioned quarantine outputs** (predictions, metrics, DCA, bootstrap CIs) under a new `*_matched_ablation_90pct_v1` directory — existing frozen files untouched.
2. A **report memo** (`docs/matched_ablation_90th_percentile_report.md`) tabulating both settings at 75th (reference) and 90th (and 80th if run), with all counts, prevalences, and intervals.
3. A **manuscript S14 update** replacing the current concession ("was not recomputed at the 80th or 90th definitions… open limitation") with the computed matched-ablation result, retaining honest caveats.

## 10. Stop conditions (any → halt, do not proceed to run)
Threshold file/checksum unverifiable; threshold appears to use validation/test outcomes; GID_2 / RDHS keys duplicated or missing; 90th-pct provenance unclear; frozen 75th-percentile predictions cannot be reproduced to prior tolerance (<1e-6 SL, <1e-15 Colombia) before extension; or any attempt would modify a committed frozen file.

---
*Workflow discipline: heavy data stays under `~/data_quarantine/` (read-only + SHA256); forbidden-file guard before any commit; separate gated spec → run → report cycles; user approves each commit; the pilot never sets the threshold or primary interval (both inherited from this locked spec).*
