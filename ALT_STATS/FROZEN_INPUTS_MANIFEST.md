# FROZEN_INPUTS_MANIFEST.md

**Provenance note (read first).** The Version 6 pipelines do **not** store the matched
no-climate per-observation probabilities as standalone files. They are **regenerated** here
by the *verbatim* frozen V6 code (SL: `sl_matched_and_recal.py`; Colombia:
`co_devincl_full_refit.py`), **reproduce-gated**, and frozen into `ALT_STATS/frozen/`.
No V6 artifact was modified. This is a documented provenance choice (see `deviations.md`),
not a stored-file read.

## Reproduce-gate results (from `logs/freeze_gates.json`)
```json
{
  "colombia_gate_point": 0.007826616912763151,
  "colombia_fidelity_M5recal": 1.1102230246251565e-16,
  "srilanka_gate_M1": 8.881784197001252e-16,
  "srilanka_gate_M4": 1.1102230246251565e-16,
  "srilanka_gate_M5": 1.1102230246251565e-16,
  "srilanka_matched_recal_dNB": 0.015646605050578577,
  "colombia_prevalence": 0.37534615672479604,
  "srilanka_prevalence": 0.33647478349465104
}
```
- Colombia matched dNB(recal)@0.30 = **+0.00783** vs frozen **+0.00786** (gate <1e-3): PASS.
- Colombia fidelity: regenerated **M5_recal** vs committed frozen `colombia_model_predictions_h4_75pct_v1.csv:M5_recal` = **1.11e-16** (n=13,361): faithful to the stored V6 file.
- Sri Lanka reproduce-gate: reconstructed M1/M4/M5 vs committed frozen preds max|Δ| **<1e-6** (8.9e-16 / 1.1e-16 / 1.1e-16): PASS.
- Sri Lanka matched dNB(recal)@0.30 = **+0.01565** ≈ manuscript **+0.0157**.

## Frozen input files (checksums in `FROZEN_INPUTS.sha256`)
| File | Setting | Rows | Prev | Clusters | Columns |
|---|---|---|---|---|---|
| `frozen/srilanka_matched_pairs.csv` | Sri Lanka | 3,926 | 0.3365 | 26 RDHS | setting, spatial_unit_id, predictor_week, target_week, outcome, full_raw, noclim_raw, full_recal, noclim_recal |
| `frozen/colombia_matched_pairs.csv` | Colombia | 13,361 | 0.3753 | 31 dept / 475 muni | setting, spatial_unit_id, department_id, predictor_week, outcome, full_raw, noclim_raw, full_recal, noclim_recal |

## Upstream V6 source files (read-only, unmodified)
- SL: `data_quarantine/analysis_tables/dengue_climate_population_linked_2018_2025_v2_date_aligned.csv`; `model_pilots/pilot_h4_75pct_v1/predictions_h4_75pct_v1.csv`; `model_pilots/hybrid_model_extension_v1/hybrid_model_predictions_v1.csv`.
- Colombia: `data_quarantine/colombia_label_features_v1/colombia_modeling_table_h4_75pct_v1.csv`; frozen ladder `colombia_model_pilots/model_ladder_h4_75pct_v1/colombia_model_predictions_h4_75pct_v1.csv`.
- Generators (verbatim source): `analysis/v12_referee_response/run/sl_matched_and_recal.py`; `analysis/geo_effect_decomposition/co_devincl_full_refit.py`.

model_pair labels: full = M5 (cases+climate+season+geo FE); no-climate = M5 minus the climate block.
prediction states: raw; recalibrated (SL past-only rolling-52 intercept; Colombia validation-fit Platt).
