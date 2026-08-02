# S11 Table — Sri Lanka wild-cluster-bootstrap-t sensitivity (secondary; transcribed, no recomputation)

Secondary few-cluster robustness check for the two planned Sri Lanka net-benefit contrasts at the reference threshold p\*=0.30 (h=4, 75th-percentile label), using the frozen row-level predictions `hybrid_model_predictions_v1.csv` (sha256 `0f505fed…`). No model refit and no new estimation of the point estimates; the wild-cluster-bootstrap-t provides an alternative uncertainty interval for the same frozen ΔNB point estimates. Values transcribed from the audited v2 output (`sri_lanka_wild_cluster_bootstrap_t_v2_results.csv`). Method, weight-sensitivity p-values, single-implementation disclosure, and reproducibility record are in S12 Text.

| Contrast | ΔNB | Original percentile-bootstrap 95% interval | Wild-cluster-bootstrap-t 95% interval | Clusters | Weights | Replications |
| -------- | ------: | -----------------------------------------: | ------------------------------------: | -------: | -------------- | -----------: |
| M4−M1    | −0.0083 |                           −0.028 to +0.013 |                      −0.031 to +0.014 |       26 | Webb six-point |        9,999 |
| M5−M1    | +0.0081 |                         −0.0012 to +0.0181 |                      −0.003 to +0.019 |       26 | Webb six-point |        9,999 |

M4−M1 is the planned primary hybrid contrast; M5−M1 is the expanded-hybrid sensitivity contrast. The wild-cluster-bootstrap-t intervals are similar to the original percentile cluster-bootstrap intervals for both contrasts, and both intervals contain zero.

**Rounded versus machine-readable.** The intervals in this table are intentionally rounded because Monte Carlo uncertainty in the test-inverted bounds (≈±0.002 in the bootstrap p near 0.05, at B=9,999) exceeds the numerical bisection tolerance (≤0.0001 in ΔNB); reporting more digits would imply a precision the procedure does not have. Full-precision test-inverted bounds are preserved only in the attached machine-readable file `S11_srilanka_wild_cluster_bootstrap_t_results.csv`:

- M5−M1: −0.00254 to +0.01869
- M4−M1: −0.03076 to +0.01407

These refined boundaries are numerical, single-implementation, and Monte-Carlo-limited; they are **not** exact confidence limits.
