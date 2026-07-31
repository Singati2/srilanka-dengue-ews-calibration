# Threshold-grid traceability (v9) — Sri Lanka ΔNB(M5−M1), all-test (26 RDHS, reference)

Complete evaluated grid transcribed from the frozen committed output. No threshold was selected or optimized; values are transcribed, not recomputed.

- **Source file:** `~/data_quarantine/model_pilots/targeted_value_climate_stage1a_h4_v1/conditional_dnb_bootstrap_ci_h4_v1.csv`
- **SHA256:** `ce80b0ce034089942cafb91ff94e52a0b7d626930c1b5090240787f854f1ad78`
- **Row key:** `regime == "ALL (26 RDHS, reference)"`; B=1000, failures=0, seed 20260612 (per the diagnostics file).

| threshold p\* | ΔNB(M5−M1) | 95% CI | pointwise status | multiplicity adjustment | source row |
|---|---|---|---|---|---|
| 0.20 | +0.00955 | [−0.00045, +0.01873] | pointwise | none | ALL, threshold=0.2 |
| 0.30 | +0.00808 | [−0.0012, +0.01809] | pointwise | none | ALL, threshold=0.3 |
| 0.40 | +0.02411 | [+0.00899, +0.03991] | pointwise | none | ALL, threshold=0.4 |

(The point estimates also appear in `conditional_dnb_h4_v1.csv`: NB_M1/NB_M5/dNB at each threshold, e.g. 0.30 → 0.13663/0.14471/0.00808.)

## Pattern statement supported by these values
- The three estimates were not monotonic: +0.00955 at p\*=0.20, +0.00808 at p\*=0.30 and +0.02411 at p\*=0.40.
- This is **not** a consistent trend across a grid. The manuscript states only that incremental net benefit was larger at the higher evaluated threshold (p\*=0.40) than at p\*=0.30 or p\*=0.20, and that all three are pointwise, multiplicity-unadjusted secondary estimates.

## Note on a separate (Colombia) threshold grid
A fuller 9-point ΔNB(M5−M1) grid (p\*=0.10–0.50) exists in `docs/decision_threshold_dnb_robustness_report.md` for the **Colombia** (GID_2) arm and is not the Sri Lanka all-test grid above; it is not used to characterize the Sri Lanka threshold dependence.
