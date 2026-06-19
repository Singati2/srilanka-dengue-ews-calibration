# E1 — Decision-Threshold / ΔNB Robustness Report (COMPLETED — sensitivity; reuses stored predictions, NO refit)
*Recomputed NB/ΔNB across p\*=0.10–0.50 and GID_2 cluster-bootstrap CIs from **stored per-test-row predictions** per `docs/decision_threshold_dnb_robustness_spec.md`. **No models refit; no predictions regenerated; no labels/thresholds recomputed; committed h=4 and horizon dirs unmodified. Colombia only (Sri Lanka deferred).** Outputs in a new versioned quarantine dir; only this report + script are committed. p\*=0.30 remains the registered primary threshold; this is sensitivity/supporting evidence.*

**Date:** 2026-06-19 · **Status:** completed · **Base commit:** 643f039 · **Script:** `scripts/decision_threshold_dnb_robustness_v1.py`.

## 1. Input prediction files + SHA256 (16-char)
- h=4: `…/model_ladder_h4_75pct_v1/colombia_model_predictions_h4_75pct_v1.csv` — `a938a138d9ef65e3…`
- horizons: `…/horizon_sensitivity_v1/colombia_horizon_predictions_v1.csv` — `ce365991c43ad9da…`
- **Both unchanged after the run** (verified) — reused read-only, not modified.

## 2. Output files (quarantine, read-only; NOT committed) + SHA256 (16-char)/size
- `decision_threshold_dnb_metrics_v1.csv` — `c93f2c28ca39ce0a…` — 7,494 B (point NB/ΔNB per dataset×horizon×threshold)
- `decision_threshold_dnb_ci_v1.csv` — `9e2601d6c1df1a50…` — 12,014 B (bootstrap ΔNB CIs)
- `decision_threshold_dnb_curves_v1.csv` — `de7e481160c6d8ac…` — 1,083 B (full p=0.05–0.50 NB curves)
- `decision_threshold_dnb_robustness_v1.meta.json` — `4a3bbe333f2fdd9a…` — 1,315 B
- Dir `~/data_quarantine/colombia_model_pilots/decision_threshold_dnb_robustness_v1/`, chmod 444.

## 3. Threshold grid
Reporting/CI grid p\* = 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50; curve grid p=0.05–0.50 (figures).

## 4. h=4 p\*=0.30 reproducibility check — PASS
| | committed h=4 | this run (from stored preds) |
|---|---|---|
| M1 NB@0.30 | 0.117 | 0.1171 |
| M4 NB@0.30 | 0.129 | 0.1293 |
| M5 NB@0.30 | 0.136 | 0.1358 |
| ΔNB(M5−M1)@0.30 | +0.018 [0.012,0.026] | +0.0188 [0.012,0.026] |
| ΔNB(M4−M1)@0.30 | +0.012 | +0.0122 |
- Matches within rounding; **no material difference**; computed by reusing stored predictions (no refit).

## 5. h=4 ΔNB(M5 − M1) across thresholds (GID_2 cluster bootstrap, B=1000, 0 failures)
| p\* | ΔNB(M5−M1) | 95% CI | CI excl 0 |
|---|---|---|---|
| 0.10 | −0.0001 | [−0.0002, +0.0000] | no |
| 0.15 | +0.0001 | [−0.0005, +0.0006] | no |
| 0.20 | +0.0022 | [+0.0007, +0.0039] | **yes** |
| 0.25 | +0.0098 | [+0.0060, +0.0138] | **yes** |
| **0.30** | **+0.0188** | **[+0.0117, +0.0260]** | **yes** |
| 0.35 | +0.0225 | [+0.0128, +0.0329] | **yes** |
| 0.40 | +0.0251 | [+0.0123, +0.0388] | **yes** (peak) |
| 0.45 | +0.0217 | [+0.0055, +0.0378] | **yes** |
| 0.50 | +0.0174 | [+0.0024, +0.0338] | **yes** |
- **Pointwise 95% bootstrap intervals excluded zero at 7/9 evaluated thresholds, covering p\*=0.20–0.50.** The hybrid advantage was therefore **not confined to the registered p\*=0.30 threshold**, and was largest near **p\*=0.40**. (Pointwise, not simultaneous — see §9.1.)
- At **very low thresholds (0.10–0.15) ΔNB ≈ 0** (CI includes 0): when the action threshold is well below outbreak prevalence (0.375), **treat-all dominates and all models converge** — a standard decision-curve boundary, not a model weakness.

## 6. h=4 ΔNB(M4 − M1) across thresholds
- CI-excludes-0 at **p\*=0.25–0.50 (6/9)**; ≈0 at 0.10–0.20. Same pattern as M5 (smaller magnitude); peak near p\*=0.40 (+0.019).

## 7. Horizon × threshold ΔNB(M5 − M1) — # thresholds (of 9) with CI excluding 0
| horizon | thresholds CI-excl-0 |
|---|---|
| h=1 | 7/9 |
| h=2 | 6/9 |
| h=4 | 7/9 |
| h=8 | 5/9 |
| h=12 | 5/9 |
- The hybrid advantage is **consistent at every horizon** — pointwise CI excluded zero at most evaluated thresholds — with slightly fewer such thresholds at longer horizons (consistent with the overall degradation already reported). Full grid in `…ci_v1.csv`.

## 8. Thresholds where ΔNB(M5−M1) CI excludes 0
- **h=4 primary:** p\*=0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50 (7/9). Pointwise CI included zero only at p\*=0.10, 0.15.

## 9. Interpretation (per spec §11)
- **Threshold-robust (descriptive).** Pointwise 95% bootstrap intervals excluded zero at **7/9 evaluated thresholds (p\*=0.20–0.50)** at h=4, and at most evaluated thresholds at every horizon (5–7/9). The hybrid advantage was therefore **not confined to the registered p\*=0.30 threshold** and was largest near p\*=0.40 — addressing the concern that p\*=0.30 was selected post hoc.
- **Boundary:** at very low thresholds (0.10–0.15) the advantage is indistinguishable from zero because treat-all dominates there (threshold ≪ prevalence). This is expected DCA behavior; the supporting evidence is scoped to **the evaluated mid-to-high threshold range (≳0.20)**.
- The increment remains **modest in magnitude** (peak ΔNB ≈ +0.025 at p\*=0.40) — consistent with the paper's "modest but robust" framing; no over-claim.
- **h=4 primary conclusion unchanged;** this strengthens, not replaces, it.

### 9.1 Statistical-inference note (pointwise CIs; multiplicity)
- The percentile 95% intervals reported at each threshold are **pointwise** GID_2 cluster-bootstrap intervals; they are **not simultaneous confidence bands** across the threshold grid.
- **No multiplicity adjustment** was applied across the nine evaluated thresholds.
- Accordingly, the threshold-grid results are **supporting sensitivity/descriptive evidence on whether the registered p\*=0.30 finding is threshold-confined — not nine separate confirmatory hypothesis tests.** "Excluded zero at 7/9 thresholds" should be read descriptively (consistent with how decision-curve analysis is conventionally reported across thresholds), not as 7 independent significant results. The single registered confirmatory contrast remains ΔNB(M5−M1) at p\*=0.30.

## 10. Stop-rule assessment (final)
| Stop rule | Status |
|---|---|
| Prediction files present / columns ok | PASS |
| h=4 p\*=0.30 reproducible from stored preds | PASS (matches committed) |
| Row sets differ across compared models | PASS (same per-row predictions) |
| Bootstrap failure rate | PASS (0% all settings) |
| Overwrite without versioning | PASS (new dir) |
| Any model refit / prediction regeneration | PASS (none — point estimates and CIs both from stored preds) |
| Existing h=4/horizon dirs modified | PASS (SHAs unchanged) |

## 11–14. Confirmations
- **No models refit.** **No predictions regenerated.** **No labels/thresholds recomputed.** **No data or existing quarantine outputs modified** (committed h=4 `a938a138…` and horizon `ce365991…` prediction files unchanged; no Sri Lanka outputs touched).
- **Sri Lanka deferred:** SL h=4 predictions exist, but SL hybrid (M4/M5) predictions are in a different-schema/recalibration file; a separate SL-consistent E1 is needed (not forced here).
- **h=4 p\*=0.30 remains the registered primary threshold;** E1 is sensitivity/supporting evidence.
- **No data files committed** — only this report + `scripts/decision_threshold_dnb_robustness_v1.py` proposed for commit.

## 15. Manuscript use
- Supplementary figure: **ΔNB(M5−M1) vs threshold with 95% CI** (h=4) — shows robustness across p\*≈0.20–0.50, peak ~0.40, convergence to treat-all at low thresholds.
- Supplementary heatmap: **horizon × threshold ΔNB(M5−M1)**.
- Text: the hybrid's net-benefit advantage is **robust across the evaluated mid-to-high threshold range (not confined to p\*=0.30)** but **modest** and **null at thresholds far below prevalence** (pointwise intervals; see §9.1).
