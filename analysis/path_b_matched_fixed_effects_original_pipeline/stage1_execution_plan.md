# Stage 1 — Stage 2 Execution Plan (to run only after `APPROVE PATH B`)

Minimal, faithful reuse of the original pipeline. No change to outcome, horizon, threshold, rows, split, model family, penalty/tuning, recalibration, or bootstrap.

## Approach
1. **Preserve sources.** Copy `scripts/colombia_model_ladder_h4_75pct_v1.py` into `analysis/path_b_matched_fixed_effects_original_pipeline/run/` unmodified; record before/after hashes. Never edit the frozen original or its quarantine outputs.
2. **Single surgical change.** Add one entry to the `MODELS` dict:
   ```python
   'M5_no_climate_matched': ['cases','season','dept']
   ```
   (M5 minus the `'climate'` token — reuses the exact `design()`, `fit_select()`, `platt()`, `nb()`, and bootstrap code unchanged.) Everything else in the harness is reused verbatim, so M1/M5 are re-derived identically.
3. **Gate A first.** Reproduce frozen M5−M1 = +0.018775 (±0.001) and the bootstrap CI before touching the matched contrast. If it fails, stop and write `path_b_reproduction_check.md` only.
4. **Decomposition.** On the identical 13,361 test rows, compute NB(M1), NB(M5_no_climate_matched), NB(M5); the three paired contrasts; verify `ΔNB_nonclimate + ΔNB_climate ≈ ΔNB_original`.
5. **Uncertainty.** Reuse the original GID_2 (municipality) cluster bootstrap (seed 20260612, B=1000, resample municipalities w/ replacement, retain all weeks, skip degenerate) to get the **paired** 95% CI for `ΔNB_climate` and `ΔNB_nonclimate`. Do not change B or the interval method after seeing results.
6. **Only pre-existing metrics.** Also report AUC, Brier, CITL, slope, prevalence, alert-all/alert-none for the matched baseline — the same columns the frozen pipeline already emits. No new metric types.
7. **Column proof.** Save the retained vs removed design-matrix column lists to prove M5 vs matched differ only in the 18 climate columns (Gate B).
8. **Do NOT** rerun Sri Lanka, LODO spatial CV, Moran's I, horizon/threshold grids, 2022-only, WP4/WP5, or any geospatial work.

## Outputs (into this analysis dir / `run/`)
`path_b_protocol_final.md`, `path_b_environment.txt`, `path_b_source_hashes.sha256`, `path_b_run_log.txt`, `path_b_model_specification_crosswalk.csv`, `path_b_design_matrix_columns.txt`, `path_b_row_audit.csv`, `path_b_predictions_checksums.sha256`, `path_b_point_estimates.csv`, `path_b_bootstrap_distribution.csv`, `path_b_bootstrap_summary.csv`, `path_b_reproduction_check.md`, `path_b_matched_fixed_effects_report.md`, `path_b_decision_memo.md`, `path_b_manifest.md` (+ optional `path_b_nb_decomposition.png`, `path_b_bootstrap_contrasts.png`).

## Estimated cost
One ladder fit (6 models incl. the added baseline) over the common-complete set + one B=1000 municipality bootstrap. Comparable to the original run: **≈ 2–5 minutes wall-clock**, single core, no new data, no rasters. Outputs written under the analysis dir (and/or quarantine mirror), never committed.

## Guardrails
No manuscript edit. No frozen-original edit. No staging/commit/push/tag/release/upload/submit. Results interpreted strictly through the pre-committed `stage1_decision_rule.md`; the approximation is never substituted for the original-pipeline result.
