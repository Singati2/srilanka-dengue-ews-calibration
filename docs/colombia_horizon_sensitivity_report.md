# Colombia Horizon-Sensitivity Report (COMPLETED — secondary/supplementary; h=4 remains primary)
*Ran the M0–M5 ladder at h=1,2,4,8,12 per `docs/colombia_horizon_sensitivity_spec.md`, identical framework to the committed h=4 run. **Secondary/supplementary; the committed h=4 result is unchanged and was NOT overwritten.** No labels/thresholds recomputed; no Sri Lanka data touched. Outputs in a new quarantine dir; only this report + the script are committed.*

**Date:** 2026-06-18 · **Status:** completed · **Base commit:** 04346fa · **Script:** `scripts/colombia_horizon_sensitivity_v1.py`.

## 1. Input + SHA256 (16-char)
- `…/colombia_label_features_v1/colombia_modeling_table_all_horizons_v1.csv` — `d7512eeffd29ebda…`.

## 2. Outputs (quarantine, read-only; NOT committed) + SHA256 (16-char)/size
- dir `~/data_quarantine/colombia_model_pilots/horizon_sensitivity_v1/`
- `colombia_horizon_metrics_v1.csv` — `8fe52361ed5b9df3…` — 9,144 B
- `colombia_horizon_contrasts_v1.csv` — `85a95605331e3cb4…` — 1,093 B
- `colombia_horizon_dca_v1.csv` — `6b8cba36b0bd304e…` — 11,866 B
- `colombia_horizon_bootstrap_ci_v1.csv` — `275e7d4cff94860e…` — 7,396 B
- `colombia_horizon_predictions_v1.csv` — `ce365991c43ad9da…` — 9,240,490 B
- `colombia_horizon_sensitivity_v1.meta.json` — `334eb954cfd763f9…` — 1,858 B
- **Committed h=4 dir untouched** (`…model_metrics_h4_75pct_v1.csv` still `c2dd62f0…`, bootstrap still `319b35459…`).

## 3. Row counts by horizon × split (per-horizon common-complete, recomputed with label_h{h})
| h | train | val | test | total |
|---|---|---|---|---|
| 1 | 55,356 | 13,035 | 14,259 | 82,650 |
| 2 | 54,740 | 12,924 | 13,978 | 81,642 |
| **4** | **53,711** | **12,713** | **13,361** | **79,785** |
| 8 | 51,856 | 12,439 | 12,280 | 76,575 |
| 12 | 50,151 | 12,073 | 11,326 | 73,550 |
- Counts decrease with h (fewer t+h outcomes exist) — expected; no horizon collapsed; no one-class test split.

## 4. Test prevalence by horizon
h=1 0.404 · h=2 0.394 · **h=4 0.375** · h=8 0.332 · h=12 0.303 (declines with horizon).

## 5. Model definitions
Identical to h=4: M0 season · M1 recent cases · M2 climate-only · M3 climate+season+dept · M4 hybrid · M5 hybrid+season+dept.

## 6. Preprocessing & tuning
Train-only log1p(cases,precip)+standardize; department one-hot; **C tuned by validation log loss** per (horizon,model); validation-only Platt recalibration; test scored once. Same as committed h=4.

## 7. Validation-selected C (recal models)
| h | M0 | M1 | M2 | M3 | M4 | M5 |
|---|---|---|---|---|---|---|
|1|0.001|0.003|0.010|0.001|0.003|0.01|
|2|0.001|10|0.001|0.001|0.010|0.01|
|4|0.001|0.010|0.001|0.001|0.010|0.01|
|8|0.001|10|0.001|0.003|10|3.00|
|12|0.001|10|0.001|0.030|0.030|0.10|

## 8. Test metrics — M1 vs M5 by horizon (recalibrated)
| h | M1 AUC | M1 NB@0.30 | M5 AUC | M5 NB@0.30 |
|---|---|---|---|---|
| 1 | 0.701 | 0.165 | 0.740 | 0.180 |
| 2 | 0.697 | 0.149 | 0.738 | 0.165 |
| **4** | **0.685** | **0.117** | **0.725** | **0.136** |
| 8 | 0.661 | 0.052 | 0.690 | 0.071 |
| 12 | 0.628 | 0.005 | 0.652 | 0.019 |
- Both M1 and M5 **degrade monotonically with horizon**; at h=12 both approach treat-none (NB≈0–0.02).
- Climate-only (M2) is weak at **every** horizon (AUC 0.536–0.559).

## 9. Raw vs recalibrated
Full raw+recal metrics in `…metrics_v1.csv`; AUC/PR-AUC invariant to monotone recalibration; NB/DCA use recalibrated probabilities (matching the h=4 report). Same test-period over-prediction caveat as h=4 applies and grows at longer horizons (lower prevalence).

## 10. NB@0.30 by horizon (recal)
M1: 0.165 / 0.149 / 0.117 / 0.052 / 0.005 (h=1→12). M5: 0.180 / 0.165 / 0.136 / 0.071 / 0.019.

## 11. ΔAUC and ΔNB vs M1 by horizon (bootstrap 95% CI; B=1000, 0 failures)
| h | M5 ΔAUC [CI] | M5 ΔNB@0.30 [CI] | M4 ΔNB | M2/M3 ΔNB |
|---|---|---|---|---|
| 1 | +0.039 [+0.021,+0.056] | +0.015 [+0.008,+0.023] | +0.012 | −0.016 |
| 2 | +0.041 [+0.024,+0.057] | +0.017 [+0.009,+0.024] | +0.008 | −0.014 |
| **4** | **+0.040 [+0.023,+0.058]** | **+0.019 [+0.012,+0.026]** | +0.012 | −0.009 |
| 8 | +0.029 [+0.009,+0.047] | +0.019 [+0.013,+0.026] | +0.011 | −0.005 |
| 12 | +0.024 [+0.002,+0.046] | +0.014 [+0.010,+0.019] | +0.006 | −0.001 |
- **M5 vs M1 ΔNB CI excludes 0 at every horizon** (and ΔAUC too). **Climate-only (M2/M3) is worse than M1 at every horizon** (negative ΔNB, trending to 0 as everything collapses at long h).

## 12. Bootstrap failure rates
**0.0% at every horizon** (0/1000 each).

## 13. h=4 reproducibility check (anchor) — PASS
| Metric | Committed h=4 | This run (h=4 anchor) |
|---|---|---|
| M1 AUC / NB | 0.685 / 0.117 | 0.685 / 0.117 |
| M4 AUC | 0.699 | 0.699 |
| M5 AUC / NB | 0.726 / 0.136 | 0.725 / 0.136 |
| M5 vs M1 ΔAUC | +0.040 [0.024,0.058] | +0.040 [+0.023,+0.058] |
| M5 vs M1 ΔNB | +0.018 [0.012,0.026] | +0.019 [+0.012,+0.026] |
- Matches within rounding (M5 AUC 0.725 vs 0.726; ΔNB point 0.019 vs report's 0.018 — same value, rounding). The committed h=4 dir was **not** modified. **No material difference.**

## 14. Interpretation (per committed spec §14) — HONEST, partly null
- **Primary sensitivity question — "does ΔNB(M5−M1) increase at longer horizons (h=8/12)?" → NO.** ΔNB(M5−M1) is **roughly flat** across h=1–8 (+0.015 to +0.019) and **slightly lower at h=12 (+0.014)**; **ΔAUC(M5−M1) actually decreases** at longer horizons (+0.040 at h≤4 → +0.024 at h=12). The leading-indicator "climate-grows-with-lead" hypothesis is **not supported within the 1–12-week range.**
- **What IS supported (robustness):** the hybrid's incremental value over recent-cases is **consistent and CI-confirmed at every horizon** (M5 ΔNB CI excludes 0 for h=1,2,4,8,12) — so the committed h=4 hybrid finding **generalizes across horizons**, it is not a single-horizon artifact.
- **Climate-only stays weak at all horizons** (M2/M3 worse than M1 throughout) — consistent with h=4 and the cross-country conclusion.
- **Absolute predictability falls with horizon:** by h=12 both M1 and M5 are near treat-none (NB≈0–0.02); the 75th-pct outbreak is hard to anticipate 12 weeks out with these features.
- **Important scope caveat:** the Colombia lead-time evidence motivating this sensitivity (Beal 2025, GeoHealth) found hydroclimate dominance at **3–6-month (≈12–26-week) leads**, **beyond our maximum h=12 weeks**. Our weekly horizons do not reach that seasonal-lead regime where autoregression fully decays, so we **cannot confirm or refute** a long-lead climate-dominant regime; within 1–12 weeks the hybrid edge is stable but not increasing.
- **Primary h=4 conclusion is unchanged.** The cross-country memo's mechanistic framing ("climate more useful at longer leads") should be **softened**: in Colombia at 1–12 weeks the hybrid increment is *robust but flat*, not lead-time-increasing (flagged for the cross-country memo / discussion).

## 15. Stop-rule assessment (final)
| Stop rule | Status |
|---|---|
| Input/label columns present | PASS |
| Any horizon low n / one-class test | PASS (test n 11,326–14,259; both classes) |
| Labels/thresholds recomputed | PASS (no; SHAs unchanged) |
| Split changed / test leakage | PASS (none) |
| Model convergence | PASS |
| h=4 anchor differs materially | PASS (matches within rounding) |
| Inconsistent row-set rules across horizons | PASS (same rule per h) |
| h=4 committed dir overwritten | PASS (separate `horizon_sensitivity_v1/`) |
| Bootstrap failure rate | PASS (0%) |

## 16. Confirmation — h=4 primary, horizon secondary
The committed **h=4 model ladder remains the primary Colombia result**; this horizon sweep is **secondary/supplementary** and does not replace it. The committed h=4 output directory is unchanged.

## 17. Confirmation — labels/thresholds/Sri Lanka unchanged
Labels `bd37e68a…`, thresholds `23710e8c…`, input `d7512eef…` unchanged; committed h=4 outputs unchanged; no Sri Lanka data used.

## 18. Confirmation — no data files committed
All 6 horizon outputs remain read-only in quarantine; **only this report + `scripts/colombia_horizon_sensitivity_v1.py`** are proposed for commit. No models/metrics beyond this sensitivity; no external validation.

## 19. Manuscript use
Supplementary: heatmap (horizon × model ΔNB) and line plot ΔNB(M5−M1) across horizons. Headline for the supplement: **the hybrid's incremental net benefit over recent-case surveillance is robust across 1–12-week horizons but does not increase with lead time in this range** (the long-lead climate-dominant regime, if any, lies beyond 12 weeks).
