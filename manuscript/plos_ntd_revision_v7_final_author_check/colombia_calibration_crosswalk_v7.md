# Colombia calibration crosswalk (v7) — every reported value traced to frozen source

**Single source:** `docs/colombia_model_ladder_report.md` §8 ("Test metrics (recalibrated; common-complete, n=13,361)") and §9 ("Raw vs recalibrated"). All values are **post-Platt** (validation-fit Platt scaling), on the **same common-complete test rows** (n=13,361; M0–M5 all evaluated on this set; §3 row counts: train 53,711 / val 12,713 / test 13,361). No value was recomputed.

| Metric | Model | Value | Pre/Post recalibration | Source (file · section · row) |
|---|---|---|---|---|
| CITL | M0 | −0.50 | post-Platt | colombia_model_ladder_report.md · §8 · M0 |
| CITL | M1 | −0.46 | post-Platt | §8 · M1 |
| CITL | M2 | −0.50 | post-Platt | §8 · M2 |
| CITL | M3 | −0.54 | post-Platt | §8 · M3 |
| CITL | M4 | −0.45 | post-Platt | §8 · M4 |
| CITL | M5 | −0.50 | post-Platt | §8 · M5 |
| Brier (range) | M0–M5 | 0.250 / 0.222 / 0.248 / 0.249 / 0.217 / 0.213 → range 0.213–0.250 | post-Platt | §8 (per-model column) |
| Calibration slope (range) | M0–M5 | 3.43 / 1.09 / 0.85 / 1.28 / 1.05 / 1.16 → range 0.85–3.43 | post-Platt | §8 (per-model column) |
| Recalibration method | all | Platt scaling fit on the validation period | — | §1, §3, §9 |
| "metrics above are recalibrated" | all | confirms §8 table is post-Platt; AUC/PR-AUC unchanged by monotone recal | post-Platt | §9 |
| Test prevalence | common-complete set | 0.375 (shared by M0–M5) | — | §3 ("Test prevalence 0.375"), §8 header |
| alert-all reference NB@0.30 | — | ≈0.107 | — | §8 (line 46) |

## Same-rows verification (M0–M5)
The §8 metrics table is explicitly labeled "common-complete, n=13,361" and **includes M0** alongside M1–M5; the complete-case intersection is defined by the M1–M5 predictors (M0 = intercept+season has no missing predictors and is available on all rows). Therefore observed prevalence (0.375) is shared and known for all six models; only per-model **mean predicted probability** is not retained in the committed record.

## Manuscript statements supported
- CITL negative for every model (over-prediction persists post-Platt) — supported.
- Brier 0.213–0.250; slopes 0.85–3.43 — supported (the extremes 3.43 and 0.85 are the M0 and M2 baselines; no per-model dispersion label is asserted in the manuscript).
- "interpreted alongside imperfect test-period calibration rather than as evidence that absolute risks were fully calibrated" — supported by the persistent negative CITL and slope spread.

**No value lacked a frozen trace; none was removed. No recomputation.**
