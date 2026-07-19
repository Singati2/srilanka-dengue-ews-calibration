# Path B — Final Protocol (as executed)
- Pipeline: exact `scripts/colombia_model_ladder_h4_75pct_v1.py` logic (design/fit_select/platt/nb/citl_slope) reused verbatim.
- Only change: added `M5_no_climate_matched=['cases','season','dept']` to MODELS.
- Rows: common_complete_M1_to_M5_h4 (train 53,711/val 12,713/test 13,361); label_h4; h=4; 75th-pct; p*=0.30.
- Fit: L2 logistic, lbfgs, max_iter 5000; C∈[0.001..10] tuned on validation log loss; train-only scaling; Platt recalibration on validation.
- Uncertainty: GID_2 (municipality) cluster bootstrap, seed 20260612, B=1000, resample units w/ replacement, retain all weeks, skip degenerate, percentile; PAIRED (all contrasts on identical resampled rows).
- Gates: A (reproduce +0.0188 ≤0.001) PASS; B (only 18 climate cols differ) PASS; C (report point+CI, no significant/not) done; D (outcome logic) → matched climate materially positive → Path A NOT authorized as null.
- Not run: Sri Lanka, LODO/Moran's I (prior), horizon/threshold grids, 2022-only, WP4/WP5. No new recalibration method. No manuscript edit.
