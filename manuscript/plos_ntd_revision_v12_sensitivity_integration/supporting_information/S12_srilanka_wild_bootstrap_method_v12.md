# S12 Text — Sri Lanka wild-cluster-bootstrap-t: method, implementation, and reproducibility record (secondary)

This secondary few-cluster sensitivity provides an alternative uncertainty interval for the two frozen Sri Lanka net-benefit contrasts (M4−M1, the planned primary hybrid; M5−M1, the expanded sensitivity hybrid) at the reference threshold p\*=0.30. It did not refit any model, regenerate any prediction, or recompute any point estimate.

## Method
For a secondary few-cluster sensitivity, the row-level difference in net-benefit contribution was analyzed as an intercept-only clustered mean, with RDHS as the cluster. A restricted studentized wild-cluster-bootstrap-t procedure used Webb six-point weights, 9,999 draws and test inversion for confidence intervals. The analysis used a Python implementation of published wild-cluster-bootstrap algorithms. Webb and Rademacher weights produced similar two-sided p-values. A second complete software implementation was not available in the preserved environment.

The confidence limits were obtained by Monte Carlo test inversion and are therefore reported at a precision appropriate to the number of bootstrap draws.

There are 26 RDHS clusters, balanced at 151 rows each. The point estimates equal the frozen reconstructed ΔNB (+0.0081 for M5−M1; −0.0083 for M4−M1). The studentized statistics were 1.564 (M5−M1) and −0.762 (M4−M1).

## Weight-sensitivity results (reported here, not in the headline table)
- M5−M1: Webb p ≈ 0.131; Rademacher p ≈ 0.129.
- M4−M1: Webb p ≈ 0.457; Rademacher p ≈ 0.452.

The inference was not materially sensitive to the two evaluated wild-weight distributions. Neither weight scheme was selected because it was more favorable; both are reported. The test-inverted acceptance set was contiguous for both contrasts (no interior gaps).

## Single-implementation limitation
The bootstrap p-values and inverted intervals were generated using a single Python implementation. The studentized statistics and cluster-robust standard errors were independently reproduced using statsmodels, but a second full wild-bootstrap implementation was not available. We do not claim independent computational reproduction of the entire procedure.

## Synthetic check
A synthetic software smoke test was performed to detect obvious implementation failure; it was not a finite-sample coverage study.

## Reproducibility record (isolated environment)
- Python 3.10.12.
- `wildboottest` 0.3.2 (wheel sha256 `886762642098358ddeb190656fc05c17e26d5c024ccff9f8863627ce3392902f`).
- `statsmodels` 0.14.6, `numpy` 1.26.4, `pandas` 2.1.3, `scipy` 1.11.4, `numba` 0.58.1, `packaging` 26.0; full `pip freeze` (490 packages) preserved in the sensitivity workspace.
- Seed 20260631; B = 9,999. Reruns with the same seed reproduce the p-values.
- Input: frozen `hybrid_model_predictions_v1.csv` (sha256 `0f505fed…`); recalibrated predictions; no refit.

## Precision note
Full-precision test-inverted bounds (M5−M1: −0.00254 to +0.01869; M4−M1: −0.03076 to +0.01407) are preserved in the machine-readable file `S11_srilanka_wild_cluster_bootstrap_t_results.csv`. These are numerical, single-implementation, Monte-Carlo-limited bounds and are not exact confidence limits; the manuscript-facing S11 table reports rounded intervals accordingly.
