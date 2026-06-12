# Label / Horizon Robustness — Extension Report
*Executed exactly per the locked spec (`docs/label_horizon_robustness_spec.md`, commit 9ab8b36). All computed artifacts are **quarantined and git-ignored**; only this markdown report is proposed for commit. No frozen outcome/exposure/population, no v1/v2 linked table, and no existing pilot / sensitivity / recalibration output was modified.*

**Date:** 2026-06-12

## 1. Input & integrity
- v2 date-aligned table, SHA256 `3a197d61…` ✅ (read-only). Models, filter, split, and pipeline identical to the primary pilot; per-horizon target by calendar date (`week_start + 7·h days`, gap-safe).

## 2. Reproducibility (reference cell)
The 75th-pct × h=4 cell reproduces the committed primary raw AUC **exactly**: M0 0.6291, M1 0.7515, M2 0.6429, M3 0.6519 (match to <1e-4).

## 3. Grid run (10 cells, all stop-rules PASS)
75th & 90th pct × h = 1, 2, 4, 8, 12. Every cell passed all stop rules; all GLMs converged with no separation. The 90th-pct cells are **not sparse** (test prevalence ~10.6%, 399–426 test events ≥ 50), so they carry adequate power.

| Cell | n test | test prev | test events | M0 AUC | M1 AUC | M2 AUC | M3 AUC |
|---|---|---|---|---|---|---|---|
| 75pct h=1 | 4,004 | 0.346 | 1,384 | 0.615 | **0.843** | 0.601 | 0.636 |
| 75pct h=2 | 3,978 | 0.343 | 1,363 | 0.616 | **0.810** | 0.601 | 0.637 |
| 75pct h=4 | 3,926 | 0.336 | 1,321 | 0.629 | **0.751** | 0.643 | 0.652 |
| 75pct h=8 | 3,822 | 0.333 | 1,272 | 0.645 | **0.679** | 0.667 | 0.659 |
| 75pct h=12 | 3,718 | 0.333 | 1,238 | 0.653 | 0.646 | 0.622 | **0.659** |
| 90pct h=1 | 4,004 | 0.106 | 426 | 0.582 | **0.825** | 0.599 | 0.637 |
| 90pct h=2 | 3,978 | 0.106 | 421 | 0.580 | **0.794** | 0.612 | 0.644 |
| 90pct h=4 | 3,926 | 0.106 | 417 | 0.561 | **0.729** | 0.659 | 0.665 |
| 90pct h=8 | 3,822 | 0.105 | 403 | 0.566 | 0.644 | **0.663** | 0.656 |
| 90pct h=12 | 3,718 | 0.107 | 399 | 0.551 | 0.610 | 0.579 | **0.624** |

## 4. Raw model comparison — net benefit @ p\*=0.30 (the registered decision metric)
| Cell | M1 NB | best-climate NB | NB winner |
|---|---|---|---|
| 75pct h=1 | **+0.182** | +0.084 | M1 |
| 75pct h=2 | **+0.163** | +0.080 | M1 |
| 75pct h=4 | **+0.137** | +0.078 | M1 |
| 75pct h=8 | **+0.109** | +0.089 | M1 |
| 75pct h=12 | **+0.089** | +0.081 | M1 |
| 90pct h=1 | **+0.022** | +0.002 | M1 |
| 90pct h=2 | **+0.020** | +0.003 | M1 |
| 90pct h=4 | **+0.009** | +0.005 | M1 |
| 90pct h=8 | **+0.001** | −0.002 | M1 |
| 90pct h=12 | **−0.000** | −0.001 | M1 |

**M1 wins net benefit @ p\*=0.30 in all 10 cells.** (At 90th-pct × long horizons the event is rare and the absolute net benefit at p\*=0.30 collapses toward 0 for every model — decision value is negligible there for all.)

## 5. Rolling-52 recalibrated comparison
Rolling-52 intercept-only recalibration **corrects calibration-in-the-large toward ≈0 in every cell** (no fallbacks needed):
| | 75pct raw→recal (M1 / M3) | 90pct raw→recal (M1 / M3) |
|---|---|---|
| h=1 | +0.50→+0.05 / +0.63→+0.09 | +0.20→−0.00 / +0.07→+0.01 |
| h=4 | +0.51→+0.02 / +0.60→+0.09 | +0.20→−0.02 / +0.06→−0.02 |
| h=12 | +0.51→−0.01 / +0.53→+0.04 | +0.11→−0.05 / +0.07→−0.04 |

(90th-pct raw drift is smaller to begin with because the rarer tail event has a smaller train→test prevalence shift.) Recalibration is monotone within week, so the AUC/net-benefit ordering of §4 is essentially preserved; M1 still wins net benefit @ p\*=0.30 after recalibration in every cell.

## 6. Does M1 dominate M2/M3?
- **In the operational regime (h = 1, 2, 4), at BOTH thresholds: yes, decisively** — M1 leads on AUC *and* net benefit, and **climate never beats M1 at any mid-high threshold (p\* 0.20–0.50): 0/62 cells** for every h≤4 cell.
- **On the registered decision metric (net benefit @ p\*=0.30): M1 wins all 10 cells** (every horizon, both thresholds).

## 7. Does any climate model beat M1, and under what condition?
**Only at long horizons (h ≥ 8), and mostly on discrimination, not the registered decision metric:**
- **AUC crossover:** 75pct h=12 (M3 0.659 > M1 0.646), 90pct h=8 (M2 0.663 > M1 0.644), 90pct h=12 (M3 0.624 > M1 0.610). M1's AUC decays with horizon (~0.84 at h=1 → ~0.61–0.65 at h=12) as recent-case autocorrelation fades, while climate models are flatter — a sensible epidemiological signal (climate is a *longer-lead* driver).
- **Mid-high net benefit:** climate exceeds M1 at *some* thresholds only at h=8 (3/62 at 75pct, 15/62 at 90pct) and h=12 (24/62 at 75pct, 16/62 at 90pct) — never at h≤4.
- **Reported as conditional, not a headline:** climate's edge appears only at long leads, is largely discrimination-only, and **does not overturn M1 on the registered net-benefit metric (p\*=0.30) in any cell**. Per the pre-committed interpretation rule, this is reported as a conditional horizon effect, not generalized.

## 8. Does rolling-52 recalibration correct calibration drift across cells?
**Yes — uniformly.** Raw calibration-in-the-large (+0.06 to +0.63) is driven to ≈0 (−0.10 to +0.09) in every cell and at every horizon/threshold, confirming the committed extension's finding generalizes across labels and horizons. The under-prediction is an **operationally correctable** deployment issue throughout.

## 9. Interpretation (pre-committed rules applied)
- **Main conclusion is robust where it matters:** in the operational short-to-medium horizon regime and on the registered decision metric, the recent-case AR baseline (M1) is not beaten by the existing climate-driven EWS forms.
- **New, honest nuance:** at long horizons (8–12 weeks) climate information becomes competitive on *discrimination* — consistent with climate as a longer-lead driver — but this does not translate into a net-benefit advantage at the registered threshold. Reported as conditional.
- Calibration drift remains real but **operationally correctable** across all labels/horizons via rolling-52 recalibration.
- This continues to support a **calibration-reporting / decision-evaluation / data-resource contribution** (prereg §O) rather than a "climate EWS beats surveillance" headline; no favorable cell is promoted to a new headline.

## 10. Output files (quarantined, read-only, NOT committed) + SHA256
- `label_horizon_metrics_v1.csv` — `c89fd55f852e7af90201e759c645249d60daa45140dfeaf53ba4cc38480d6e01`
- `label_horizon_dca_v1.csv` — `1170f4abfeb4eab868977a4d70425108ed29ec24a1bd573330b8decdd2ff288e`
- `label_horizon_stop_rules_v1.csv` — `06c5cc619c4d2acb6efd753c18b1638bf55d89b17b054074299af75441da1292`
- Metadata: `label_horizon.meta.md` (all under `~/data_quarantine/model_pilots/label_horizon_robustness_v1/`).

## 11. Confirmations
- Only the pre-specified grid was run (75/90 pct × h=1,2,4,8,12); raw + rolling-52 only; no new model classes, feature search, or test tuning.
- **No frozen outcome/exposure/population or linked-analysis CSV (v1/v2) was modified**; input checksum re-verified. No prior pilot/sensitivity/recalibration directory was overwritten.
- **No data files committed** — all outputs quarantined/git-ignored; only this markdown report is proposed for commit.
- Preregistration unchanged.

## 12. Next steps (separate, approval-gated)
Manuscript results-synthesis document; PROBAST/TRIPOD-AI self-assessment of the pilot. Nothing runs until directed.
