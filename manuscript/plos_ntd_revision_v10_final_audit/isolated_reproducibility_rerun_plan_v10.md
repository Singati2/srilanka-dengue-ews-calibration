# Isolated reproducibility rerun plan (v9) — SPECIFICATION ONLY (NOT EXECUTED)

**Status: NOT RUN.** This documents how an independent rerun would be performed. Nothing here was executed; no frozen output was overwritten.

## Feasibility flag
**A fully isolated, bit-exact rerun is NOT currently feasible.** The historical Python modeling-stack versions were not preserved; only a best-effort tolerance-based rerun is currently feasible. For the canonical R-DLNM comparator, the analysis record preserves the reported R and package versions (R 4.6.0, dlnm 2.4.10, mgcv 1.9.4, tsModel 0.6-2). However, no complete historical environment lock, package-source archive or container record was identified, so exact environment reconstruction and bit-level reproduction are not guaranteed. Bit-exact reproduction may also depend on the operating system, compiler, BLAS/LAPACK implementation, package build artifacts, hardware, and randomness/parallel execution. The R component therefore has the strongest version record but is not established as bit-exactly reproducible.

## 1. Isolated location & commit
- Separate git worktree, e.g. `git worktree add ../dengue-rerun a32afd73897eeb1f5574747180535e3289813370` (current HEAD `a32afd7`).
- Run entirely inside that worktree + a scratch output dir **outside** `~/data_quarantine` (e.g. `~/dengue_rerun_outputs/`). **Never write into the frozen quarantine.**

## 2. Immutable inputs (verify checksums before running)
- Sri Lanka analysis table: `data_quarantine/analysis_tables/dengue_climate_population_linked_2018_2025_v1.csv` (sha256 in its `.meta.md`).
- Colombia linked table: `data_quarantine/colombia_climate_linkage_full_v1/*.csv` (sha256 in its `.meta.json`).
- Frozen inputs (WER outcome, ERA5-Land/CHIRPS exposure, WorldPop population) — checksums in the analysis-table `.meta.md`.
- Abort if any input checksum differs.

## 3. Required environment
- R: 4.6.0; dlnm 2.4.10; mgcv 1.9.4; tsModel 0.6-2 (reported versions preserved in the analysis record; no complete environment lock/container — pin to these as a best-effort starting point, not a guarantee of bit-level reproduction).
- Python: 3.x with NumPy/pandas/scikit-learn/SciPy/statsmodels — **exact versions unknown**. Plan: (a) attempt to infer from any `__pycache__` magic numbers / saved logs; (b) otherwise pin a documented best-effort set and **record** it; treat results as tolerance-reproduction, not exact.

## 4. Script order (committed scripts)
1. `colombia_label_construction_v1.py` → labels.
2. `colombia_lag_feature_assembly_v1.py` → features.
3. `colombia_model_ladder_h4_75pct_v1.py` → Colombia M0–M5 metrics/dca/bootstrap/predictions.
4. `colombia_outbreak_threshold_sensitivity_v1.py`, `colombia_horizon_sensitivity_v1.py`, `decision_threshold_dnb_robustness_v1.py` → Colombia sensitivities.
5. Sri Lanka pilot / hybrid / targeted-value / recalibration / CI scripts (locate the SL generators; some are referenced in `docs/*` but confirm presence before running).
6. R `dlnm` comparator (separate R environment).

## 5. Seeds
- Primary bootstrap seed **20260612**, B=1000 (recorded in diagnostics CSVs).
- **Sri Lanka targeted-value bootstrap seed: NOT retained** → its interval cannot be reproduced exactly; rerun would generate a *new* seed and compare distributionally, not exactly.

## 6. Expected outputs (compare to frozen)
- `colombia_model_metrics/dca/bootstrap_ci/predictions_h4_75pct_v1.csv`; `hybrid_model_metrics/dca_v1.csv`; pilot M0–M3 metrics/DCA; `conditional_dnb*_h4_v1.csv`; canonical R dlnm metrics/dca.

## 7. Comparison rules (exact vs tolerance)
- **Deterministic (exact):** row counts, label prevalence, NB at a threshold given identical predictions, arithmetic translations.
- **Tolerance:** AUC/Brier/CITL/slope to ±0.005 (abs) given environment drift; ΔNB point ±0.001; CI endpoints ±0.003 (bootstrap is seed/version sensitive). Flag any difference beyond tolerance for investigation.
- Predictions: compare per-row predicted probabilities; report max |Δp| (the canonical R-vs-Python DLNM check already reports 0.150 max |Δp| as precedent).

## 8. Runtime / storage estimates (rough)
- Colombia ladder + sensitivities: minutes–tens of minutes on a workstation; B=1000 cluster bootstrap dominates.
- R dlnm comparator: minutes.
- Storage: <1–2 GB scratch (predictions + bootstrap draws).

## 9. Stop conditions
- Input checksum mismatch.
- Missing committed generator script for any frozen output.
- Inability to construct any required environment.
- Any attempt to write inside `~/data_quarantine` (hard stop).

## 10. Prohibitions
- Do not overwrite, move, or delete any frozen output or input.
- Do not modify v1–v9 manuscript files.
- Do not stage/commit/push/release/upload.

**This plan is not executed in v9. Execution requires explicit author authorization (it would constitute reopening the analysis).**
