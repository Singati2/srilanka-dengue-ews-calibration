# E3 — Colombia Outbreak-Threshold Sensitivity Report (COMPLETED; secondary sensitivity)
*Tested whether the modest hybrid-over-surveillance advantage survives a rarer outbreak definition (train-only 75th → 80th → 90th percentile), per `docs/colombia_outbreak_threshold_sensitivity_spec.md`. Same M0–M5 ladder/features/preprocessing/recalibration as the committed h=4 run; only the outbreak percentile changes. **75th percentile h=4 remains the registered primary result.** No label/threshold files modified; outputs in a new versioned dir; only this report + script committed.*

**Date:** 2026-06-19 · **Status:** completed · **Base commit:** 643f039 · **Script:** `scripts/colombia_outbreak_threshold_sensitivity_v1.py`.

## 1. Inputs + SHA256 (16-char) — unchanged after run
- `colombia_modeling_table_all_horizons_v1.csv` — `d7512eeffd29ebda…`; `colombia_label_thresholds_train_only_v1.csv` — `23710e8cf82a1472…` (both unchanged; committed h=4 predictions `a938a138…` unchanged).

## 2. Outputs (quarantine, read-only; NOT committed) + SHA256 (16-char)/size
- `colombia_outbreak_thresholds_v1.csv` — `d27c726b8aab8d0b…` — 31,229 B
- `colombia_outbreak_threshold_labels_v1.csv` — `79209d410eca4477…` — 3,194,525 B
- `colombia_outbreak_threshold_predictions_v1.csv` — `1506534bf3f61da5…` — 5,743,032 B
- `colombia_outbreak_threshold_metrics_v1.csv` — `925459d1e2e6587f…` — 5,483 B
- `colombia_outbreak_threshold_dca_v1.csv` — `ab6477862b7ff1ba…` — 6,564 B
- `colombia_outbreak_threshold_bootstrap_ci_v1.csv` — `3e5d2f44d5d659e9…` — 1,073 B
- `colombia_outbreak_threshold_sensitivity_v1.meta.json` — `477b4e9b1c342041…` — 1,496 B
- Dir `~/data_quarantine/colombia_model_pilots/outbreak_threshold_sensitivity_v1/`, chmod 444.

## 3. Threshold provenance & label reproduction (verification)
- Train-only per-GID_2 thresholds recomputed from the panel train rows **reproduce the committed table**: **thr75 max|Δ| = 0.0**, **thr90 max|Δ| = 1.8e-15**. **thr80 newly computed** train-only (1,051 units), saved as a new versioned file; the committed threshold file was **not modified**.
- The reconstructed **75th-pct label reproduces the committed `label_h4` exactly** (79,785/79,785; 0 mismatches).
- **No validation/test outcomes used** in any threshold.

## 4. Common-complete rows & sparsity (same rows across percentiles)
Because h=4 labelability depends only on whether the **t+4 outcome row exists** (not on the threshold), the common-complete set is **identical (79,785 rows) for all three percentiles** — train 53,711 / val 12,713 / test 13,361 — so 75/80/90 are compared on **identical rows** (a strength). Only label values/prevalence differ:
| pct | test prevalence | test events | test units | test zero-event units |
|---|---|---|---|---|
| 75th | 0.375 | 5,015 | 475 | 104 |
| 80th | 0.331 | 4,416 | 475 | 117 |
| 90th | 0.235 | 3,136 | 475 | 170 |
- **Sparsity decision:** all three **adequate** (≥3,136 test events; prevalence ≥0.235) → **no 90th-pct downgrade**.
- **Honest caveat:** even the 90th-pct label is ~23.5% prevalent in test — train-only thresholds + upward temporal drift mean it captures "above the *train* 90th pct," not a rare epidemic. So this is a moderate-rarity sensitivity, not a true epidemic-threshold test.

## 5. Model ladder, preprocessing, tuning
Identical to the committed h=4 run: M0–M5; regularized L2 logistic; train-only log1p+standardize, department one-hot; C tuned by validation log loss; validation-only Platt recalibration; test scored once. Only the outcome label (75/80/90) changes.

## 6. Test metrics (recalibrated) — M1 vs M5 by percentile
| pct | M1 AUC | M1 PR-AUC | M1 NB@0.30 | M5 AUC | M5 PR-AUC | M5 NB@0.30 |
|---|---|---|---|---|---|---|
| 75th | 0.685 | 0.566 | 0.117 | 0.725 | 0.608 | 0.136 |
| 80th | 0.689 | 0.525 | 0.081 | 0.726 | 0.563 | 0.096 |
| 90th | 0.703 | 0.444 | 0.031 | 0.734 | 0.473 | 0.041 |
- AUC is stable/slightly higher for rarer labels; **PR-AUC and absolute NB fall with rarity** (expected at lower prevalence) — so the decision-analytic view (NB), not AUC, governs interpretation.

## 7. ΔNB(M5−M1)@0.30, ΔNB(M4−M1)@0.30, ΔAUC(M5−M1) — GID_2 cluster bootstrap (B=1000, 0 failures)
| pct | ΔNB(M5−M1)@0.30 [95% CI] | ΔNB(M4−M1)@0.30 [95% CI] | ΔAUC(M5−M1) [95% CI] |
|---|---|---|---|
| **75th** | **+0.0188 [+0.0117, +0.0260]** | +0.0122 [+0.0073, +0.0171] | +0.0403 [+0.0235, +0.0575] |
| 80th | +0.0157 [+0.0082, +0.0236] | +0.0093 [+0.0038, +0.0147] | +0.0373 [+0.0203, +0.0538] |
| 90th | +0.0092 [+0.0003, +0.0183] | +0.0091 [+0.0038, +0.0147] | +0.0314 [+0.0155, +0.0464] |
- **Pointwise CI excludes 0 at all three percentiles for ΔNB(M5−M1), ΔNB(M4−M1), and ΔAUC.** (Pointwise bootstrap intervals; p\*=0.30 is the registered confirmatory threshold — same inference caveat as E1.)
- **The increment shrinks as outbreaks get rarer:** ΔNB(M5−M1) +0.0188 → +0.0157 → +0.0092; the **90th-pct CI is borderline (lower bound +0.0003)**.
- **75th-pct anchor reproduces the committed primary** exactly (+0.0188 [0.0117, 0.026]).

## 8. Net-benefit translation (decision-analytic equivalents)
At p\*=0.30, ΔNB(M5−M1):
- **75th (primary):** +0.0188 → ≈ **1.9 net true-positive equivalents per 100 municipality-weeks**, or equivalently **≈4.4 fewer false alerts per 100** at fixed true positives (false-alert-equiv CI ≈ **2.7–6.1**).
- **80th:** +0.0157 → ≈ 1.6 net TP-equiv / ≈ 3.7 fewer false alerts per 100 (CI ≈ 1.9–5.5).
- **90th:** +0.0092 → ≈ 0.9 net TP-equiv / ≈ 2.1 fewer false alerts per 100 (CI ≈ 0.07–4.3; borderline).
- **Caveat:** these are **decision-analytic equivalents conditional on the p\*=0.30 harm–benefit trade-off, not directly observed counts of alerts prevented or outbreaks detected.** Equivalents are **not** compared across percentiles as like-for-like (prevalence and outcome definitions differ).

## 9. Interpretation (per spec §11)
- **The modest hybrid advantage is robust to a rarer outbreak definition (in direction and pointwise significance):** ΔNB(M5−M1)@0.30 remains positive with CI excluding 0 at 80th **and** 90th — so the result is **not an artifact of the high-prevalence 75th-pct label**.
- **But the increment is smaller for rarer outbreaks** (+0.019 → +0.009) and the **90th-pct evidence is weak** (CI nearly touches zero; absolute NB and PR-AUC fall). Combined with §4's caveat (the 90th label is still ~23.5% prevalent), the honest reading is: **robust for moderately rarer outbreaks; suggestive but borderline for the rarest definition tested.**
- AUC rises slightly with rarity while net benefit falls → **discrimination ≠ operational value** (the paper's core point); the decision-curve view is the informative one.
- **Summary sentence (for manuscript):** *the hybrid increment persisted under increasingly stringent training-referenced percentile definitions but diminished as the percentile increased; the 90th-percentile estimate was small and borderline and the test prevalence remained 23.5%, so this is **not** evidence for performance on rare epidemics.*
- **Multiplicity / inference caveat:** percentile-specific intervals are **pointwise** GID_2 cluster-bootstrap intervals; **no multiplicity adjustment was applied across the three percentile definitions**; **E3 is secondary sensitivity evidence**, and the **75th-percentile h=4 analysis remains the registered primary** (the sole confirmatory contrast).
- **Primary 75th-pct h=4 conclusion is unchanged;** E3 strengthens its robustness, does not replace it.

## 10. Reporting-delay limitation (verbatim)
> "OpenDengue contains finalized rather than real-time surveillance counts. Under operational reporting delays, both the recent-surveillance and hybrid models may perform differently. The direction and magnitude of any change in their relative net benefit cannot be determined from the present data."
- No reporting-delay analysis added; **no lower-bound claim**; deferred (real-time vintages / separately pre-specified simulation); belongs in the manuscript Discussion.

## 11. Stop-rule assessment (final)
| Rule | Status |
|---|---|
| Threshold file verifiable / train-only | PASS (thr75/thr90 reproduce; train-only) |
| GID_2 keys duplicated/missing | PASS (none) |
| 90th-pct one-class / too sparse | PASS (3,136 test events; prev 0.235) — no downgrade |
| Bootstrap failure rate >5% | PASS (0% all percentiles) |
| Inconsistent row-set across percentiles | PASS (identical 79,785 rows; differences = label values only) |
| Labels/thresholds files modified | PASS (no; SHAs unchanged) |
| 75th anchor differs from committed | PASS (reproduces +0.0188 [0.0117, 0.026]) |
| Existing dirs overwritten | PASS (new versioned dir) |

## 12. Confirmations
- **No label/threshold files modified** (committed `23710e8c…` unchanged); thr80 saved as a new versioned output only.
- **75th remains the registered primary;** 80th/90th are secondary sensitivity, fully reported including the borderline 90th.
- No Sri Lanka data used; committed h=4/horizon/E1 outputs untouched. **No data files committed** — only this report + `scripts/colombia_outbreak_threshold_sensitivity_v1.py`.

## 13. Analysis freeze
Per the project decision, **E3 closes the analysis phase.** Do **not** run E2 (longer horizons), E4 (leave-department-out), or E5 (richer climate) before the manuscript draft; reserve them for documented reviewer requests or a separate paper. Next step is **manuscript preparation** around the agreed thesis.

## 14. Manuscript use
Supplementary table/figure: **ΔNB(M5−M1)@0.30 by outbreak percentile (75/80/90) with bootstrap CI**, shown on identical rows; text: *the hybrid increment is robust to a moderately rarer outbreak definition but shrinks and becomes borderline at the rarest threshold tested, and absolute net benefit falls with rarity*. Pair with the E1 threshold-robustness and the horizon-flat results as the sensitivity suite supporting the modest-but-robust primary finding.

## 15. Implementation/convergence audit (2026-06-19)
A narrow integrity audit re-ran the E3 fits **without modifying the committed quarantine outputs**, prompted by the original generator's blanket `warnings.filterwarnings('ignore')` possibly hiding logistic-regression convergence failures. The audit was performed by a **separate** script, `scripts/audit_colombia_outbreak_threshold_sensitivity_v1.py`, which reads the same frozen inputs, captures convergence explicitly, re-checks the integrity gates, and numerically compares regenerated probabilities against the frozen predictions. It writes only an audit summary to a separate audit directory and regenerates/overwrites nothing in the frozen E3 quarantine directory. The original generator, `scripts/colombia_outbreak_threshold_sensitivity_v1.py`, is **unchanged** and remains the exact historical code that produced the frozen E3 outputs (commit f1ace05).
- **Convergence (explicitly captured via `catch_warnings(record=True)` + `n_iter_` vs `max_iter`):** **0** non-converged selected models, **0** candidate C-grid fits with a `ConvergenceWarning`, **0** non-converged Platt recalibration fits, across all 3 percentiles × 6 models. The blanket suppression therefore **hid nothing** — there were no convergence failures to detect.
- **Integrity gates re-verified:** thr75 max|Δ| = 0.0; thr90 max|Δ| = 1.8e-15; 75th-pct label reproduces committed `label_h4` exactly; rows 53,711 / 12,713 / 13,361.
- **Reproduction:** re-run recalibrated predictions match the committed predictions to **max|Δ| ≈ 1.1e-16** across all models/percentiles; ΔNB(M5−M1)@0.30 reproduced exactly (+0.0188 / +0.0157 / +0.0092).
- **Outcome:** **no scientific result changed; no quarantine output modified.** The frozen E3 results stand. The audit reproduced recalibrated probabilities to max absolute difference approximately 1.1×10⁻¹⁶ and reproduced the reported key estimates. Full output-file byte identity was not tested because the frozen quarantine outputs were not regenerated or overwritten. The original generator was not modified; the separate audit script (above) carries the explicit convergence capture and integrity hard-checks.
