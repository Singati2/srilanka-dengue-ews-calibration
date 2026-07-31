# Threshold-grid traceability (v9) — Sri Lanka ΔNB(M5−M1), all-test (26 RDHS, reference)

Complete evaluated grid transcribed from the frozen committed output. No threshold was selected or optimized; values are transcribed, not recomputed.

- **Source file:** `~/data_quarantine/model_pilots/targeted_value_climate_stage1a_h4_v1/conditional_dnb_bootstrap_ci_h4_v1.csv`
- **SHA256:** `ce80b0ce034089942cafb91ff94e52a0b7d626930c1b5090240787f854f1ad78`
- **Row key:** `regime == "ALL (26 RDHS, reference)"`; B=1000, failures=0, seed 20260612 (per the diagnostics file).

| p\* | ΔNB(M5−M1) | 95% CI | excludes_zero | pointwise | multiplicity | source row |
|---|---|---|---|---|---|---|
| 0.20 | +0.00955 | [−0.00045, +0.01873] | No | yes | unadjusted | ALL, threshold=0.2 |
| 0.30 | +0.00808 | [−0.0012, +0.01809] | No | yes | unadjusted | ALL, threshold=0.3 |
| 0.40 | +0.02411 | [+0.00899, +0.03991] | Yes | yes | unadjusted | ALL, threshold=0.4 |

(The point estimates also appear in `conditional_dnb_h4_v1.csv`: NB_M1/NB_M5/dNB at each threshold, e.g. 0.30 → 0.13663/0.14471/0.00808.)

## Pattern statement supported by these values
- The evaluated all-test grid has **three thresholds** (0.20, 0.30, 0.40). The estimate is **not monotonic**: it is +0.0096 at 0.20, **dips** to +0.0081 at 0.30, then **rises** to +0.0241 at 0.40.
- Therefore the manuscript does **not** claim a "consistent" or monotonic across-grid pattern. It states only that incremental net benefit was **larger at the higher evaluated threshold (p\*=0.40)** than at 0.30 or 0.20, and that all three are pointwise, multiplicity-unadjusted secondary estimates.
- Only the p\*=0.40 interval excludes zero; 0.20 and 0.30 include zero.

## Note on a separate (Colombia) threshold grid
A fuller 9-point ΔNB(M5−M1) grid (p\*=0.10–0.50) exists in `docs/decision_threshold_dnb_robustness_report.md` for the **Colombia** (GID_2) arm and is not the Sri Lanka all-test grid above; it is not used to characterize the Sri Lanka threshold dependence.
