# S6 Table — Per-analysis bootstrap protocol (DRAFT)

Verified separately per analysis from the committed scripts/reports. The main text states only the common verified principles; analysis-specific parameters are below. Do **not** infer a shared seed; values absent from the committed record are marked.

| # | Analysis | Resampling unit | B | Seed | CI method | Degenerate/one-class handling | Failure count | Pointwise vs simultaneous | Multiplicity adjustment |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Sri Lanka hybrid (M4−M1 planned primary; M5−M1 expanded) | RDHS cluster | 1000 | 20260612 | percentile 95% | one-class resamples excluded from discrimination | 0 | pointwise | none |
| 2 | Sri Lanka targeted-value regimes (M5−M1; secondary/exploratory) | RDHS cluster | 1000 | 20260612 (verified: runner script `_run_targeted_value_stage1a_h4.py` `SEED=20260612` + `stage1a_h4_diagnostics_v1.csv` seed column) | percentile 95% | excluded one-class | 0 | pointwise | none (descriptive/hypothesis-generating; underpowered cells flagged) |
| 3 | Colombia primary model ladder | GID_2 (municipality) cluster | 1000 | 20260612 | percentile (2.5/97.5) | excluded one-class | 0 | pointwise | none |
| 4 | Colombia E1 threshold sensitivity | GID_2 cluster | 1000 | 20260612 | percentile (2.5/97.5) | excluded one-class | 0 | **pointwise (explicitly not simultaneous bands)** | none |
| 5 | Colombia horizon sensitivity | GID_2 cluster | 1000 | 20260612 | percentile 95% | excluded one-class | 0 | pointwise | none |
| 6 | Colombia E3 exceedance-definition sensitivity | GID_2 cluster | 1000 | 20260612 | percentile 95% | excluded one-class; failure rate recorded | 0 | pointwise | none (across 75/80/90 definitions) |

**Common verified principles (main text):** resample the spatial unit with replacement, retain all weeks within a sampled unit; percentile intervals; one-class resamples excluded from discrimination summaries; failure counts recorded; intervals pointwise and unadjusted for multiplicity across threshold/horizon/percentile/regime grids.

**Verification sources:** `hybrid_model_extension_report.md` (1), `targeted_value_climate_stage1a_h4_report.md` (2), `colombia_model_ladder_report.md` + `scripts/colombia_model_ladder_h4_75pct_v1.py` (3), `decision_threshold_dnb_robustness_report.md` + script (4), `colombia_horizon_sensitivity_report.md` + script (5), `colombia_outbreak_threshold_sensitivity_report.md` + `scripts/colombia_outbreak_threshold_sensitivity_v1.py` (6).
