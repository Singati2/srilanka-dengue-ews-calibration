# Specification — DLNM Climate Comparator (design-lock)
*Pre-computation design lock for adding **one** credible lagged-nonlinear climate comparator. **No DLNM fit; no models run; no labels created; no metrics computed; no data modified.** Documentation only. This is a hardening / robustness comparator on the already-committed primary evaluation cell; it does **not** change the primary analysis, re-tune thresholds, or alter the headline.*

**Date:** 2026-06-12 · **Status:** specification only — locks the model and evaluation **before** any computation, to prevent post-hoc model shopping.

## 1. Purpose
- Address the reviewer concern that M2/M3 (six raw climate variables in a logistic regression) are **not a mature climate-EWS comparator** — i.e., a strawman.
- Add **one** credible climate comparator (a distributed-lag nonlinear model, DLNM-style) **without** changing the primary analysis or headline.
- Treated explicitly as a **pre-specified robustness comparator**, not model shopping: a single locked specification, evaluated once on the registered cell.

## 2. Scientific scope
- **Not** a new forecasting project; **not** a survey of the dengue-EWS literature.
- **One** additional climate-focused comparator that answers: *"Does a more credible lagged, nonlinear climate model outperform the recent-cases AR baseline (M1) on the same registered decision metrics?"*
- It raises the climate comparator from "raw-variable logistic" to "lagged nonlinear cross-basis" — a fair, recognizable climate-EWS form — while staying within the project's existing data and evaluation frame.

## 3. Primary target (same registered cell)
Identical to the primary pilot — no changes:
- Label: **RDHS-specific 75th percentile** (train-only thresholds).
- Horizon: **h = 4 weeks**; target by calendar date (+28 d, gap-safe).
- Split: **train 2018–2022 / test 2023–2025**; same primary filter; **same modelable rows** as the primary pilot (so DLNM, M1, M2/M3 are compared on the identical test rows).
- Metrics: **AUC, PR-AUC, Brier, calibration-in-the-large, calibration slope, DCA p\*=0.05–0.50 (highlight p\*=0.30 + band {0.10,0.20,0.30,0.40})** — exactly as the primary.

## 4. Candidate DLNM design (conservative, locked)
A **cross-basis distributed-lag logistic** model for the binary alert at t+4:
- **Outcome:** future dengue alert label (same as primary).
- **Predictors:** a Gasparrini-style **cross-basis** of climate over lags — i.e. a tensor of (basis over the climate value) × (basis over the lag dimension), summed over lags.
- **Climate variables:** **temperature (t2m_mean_c)**, **precipitation (precip_sum_mm)**, **relative humidity (rh_mean_percent)** — one cross-basis per variable.
- **Lag window:** **0–8 weeks** (fixed, consistent with the committed S2 lag-sweep range). Lagged values built by the same date-based gap-safe join used throughout.
- **Basis functions:** natural cubic splines (or B-splines), **df ≈ 3–4 per dimension** (value and lag), knots at quantiles **of the training data only**. This keeps the cross-basis modest (~9–16 terms per variable).
- **Implementation note (honest):** if R `dlnm`/`mgcv` are available they are preferred; **otherwise (default, Python)** the cross-basis is **approximated** with spline-expanded lagged climate features (patsy/scipy natural-spline bases on value and lag) fit by logistic regression — a documented approximation to a true cross-basis, **not** claimed as the canonical `dlnm` implementation. The report must state which path was used.
- **Regularization:** mild L2 (as in the primary M0–M3) for numerical stability given 26 RDHS × limited years; report the penalty.

## 5. Model comparison set
- **M1** recent-cases AR baseline (reference; from committed predictions / identical refit).
- **Best existing simple climate model** (M2 climate-only and/or M3 climate+season+RDHS) from the committed reports.
- **DLNM climate-only comparator** (the new model).
- **Optional, separately pre-specified:** a **DLNM + recent-cases** combined model — only if explicitly approved later; **not** in this first pass.

**Primary comparisons:** DLNM-climate vs **M1**; DLNM-climate vs **M2/M3**.

## 6. Leakage rules
- **All** spline knots, standardization, imputation, and any df choice are learned/fixed on **train (2018–2022) only**.
- **No** test outcomes used in fitting or tuning; **no** threshold optimization on test.
- Lagged climate features use **past data only** (date-based; no future leakage into a week).
- If df is selected from a grid, selection uses **train-only** criteria (e.g., train cross-validated likelihood) **or** is fixed a priori; the chosen value is reported.
- **Stop** if leakage cannot be avoided (report rather than force).

## 7. Complexity control (pre-specified, small)
- Lag window **fixed at 0–8 weeks**; climate variables **fixed** (temp, precip, RH).
- Spline **df limited (3–4)** per dimension; **no** large hyperparameter search.
- **No** post-hoc selection based on test AUC or DCA.
- At most a **small, pre-listed** set of DLNM variants (e.g., df ∈ {3,4}); if more than one is run, **all** are reported and clearly **labelled exploratory**, with **no headline change without team review**.
- RDHS handling: a single pooled cross-basis (optionally + RDHS fixed effects, matching M3) — fixed before fitting; report which.

## 8. Metrics
Same as primary: AUC, PR-AUC, Brier, calibration-in-the-large, calibration slope, net benefit at p\*=0.30, threshold-band DCA. **ΔAUC and ΔNB vs M1** computed on the identical test rows. **Bootstrap CIs** (RDHS cluster, seed 20260612, as in the CI step) added **only after** point estimates are validated against the primary rows — not required in the first pass unless runtime is trivial.

## 9. Stop rules
- **Stop** if the DLNM package dependency (R `dlnm`/`mgcv`, or the Python spline path) is unavailable.
- **Stop** if model fitting fails to converge or shows separation (report; try the mild-L2 fallback once, then stop if still failing).
- **Stop** if predictions cannot be generated for **all** primary test rows (DLNM must score the same rows as M1).
- **Stop** if point estimates cannot be compared on the **same rows** as M1.
- **Stop** if any output would require modifying a frozen/committed table.
- Every stop is **reported honestly**, not worked around.

## 10. Interpretation rules (pre-committed)
- **DLNM still does not beat M1 on net benefit** → the paper gets **stronger**: "even a more credible lagged nonlinear climate comparator did not outperform the recent-case baseline on the registered decision metric." (Most likely outcome given S2.)
- **DLNM beats M1 on AUC but not net benefit** → keep the existing decision-value framing (discrimination ≠ decision value).
- **DLNM beats M1 on net benefit (ΔNB CI excludes 0)** → **do not change the headline automatically**; report as a **major new finding requiring team review** and possibly revised manuscript framing.
- **Do not** claim climate has no value; **do not** claim DLNM represents the entire dengue-EWS literature; report the full comparison without selective emphasis.

## 11. Outputs (LATER, not now) — quarantined only
Future directory: `~/data_quarantine/model_pilots/dlnm_comparator_v1/`
- `dlnm_predictions_v1.csv`, `dlnm_metrics_v1.csv`, `dlnm_dca_v1.csv`, (optional `dlnm_ci_v1.csv`), `dlnm_comparator.meta.md`.
CSVs read-only with SHA256; **none committed**. Future safe report: `docs/dlnm_climate_comparator_report.md`. The prior pilot/sensitivity/recalibration/CI directories are **not** overwritten.

## 12. Confirmation
- **No DLNM fit; no models run; no labels created; no metrics computed; no data modified.**
- **Only this markdown spec was created.** Nothing committed. Preregistration unchanged.

## Next step (separate, approval-gated)
On approval: verify dependencies and the primary test-row set; fit the single locked DLNM (df fixed/train-selected); score the identical test rows; compute the primary metrics + ΔAUC/ΔNB vs M1; write quarantined outputs + a safe markdown report; apply §10 rules. Nothing runs until directed.
