# audit_v42 / 01 — Colombia climate specification resolution (§5.1)

**Date:** 2026-07-27 · **Evidence hierarchy applied:** executable code + frozen outputs first.

## Verdict: RESOLVED — no residual contradiction in the current `.tex`

The v42 PDF's apparent contradiction (headline Colombia climate described as DLNM cross-basis vs. linear lags) is **not present** in the current manuscript source; Table 1, §Methods, S9 Table, and the Results robustness paragraph now agree, and all match the code.

## What the code actually does (source of truth)
`ALT_STATS/src/freeze_matched_predictions.py` (verbatim from the frozen `co_devincl_full_refit.py` pipeline), Colombia design:
```python
PRE=[f'precip_lag{k}' for k in range(9)]   # 9 precipitation lag columns (log1p)
TMP=[f'temp_lag{k}'   for k in range(9)]   # 9 temperature lag columns (linear)
# 'climate' block = PRE + TMP  = 18 columns
MODELS={'M5':['cases','climate','season','dept'], 'M5_no_climate_matched':['cases','season','dept']}
```
- **Primary Colombia matched-ablation climate block = 18 LINEAR lag columns** (9 precipitation + 9 temperature; log1p on precipitation; **no humidity; no DLNM basis**).
- `M5_no_climate_matched` removes exactly these 18 columns; the "18 climate columns" in S9 Table = these linear lag features. Confirmed by S9 Table: M5 (58) − M5_no-climate (40) = 18.

## What the manuscript now says (all consistent, code-matched)
- **Table 1, line 145:** Sri Lanka = "DLNM-style cross-basis: temperature, precipitation, humidity (lags 0–8)"; Colombia = "Linear temperature and precipitation lags 0–8 (no humidity)". ✅ correct per-setting.
- **Results (robustness):** "Refitting the climate terms as a distributed-lag nonlinear cross-basis moved the point increment to +0.0122 … so the estimate is sensitive to the climate-block specification." ✅ DLNM is a **sensitivity**, not the primary.
- **Results (Colombia):** climate-only M2/M3 used the linear lag spec. ✅

## Exact quantities and their sources
| Quantity | Value | Source |
|---|---|---|
| Colombia primary matched ablation ΔNB(M5−M5_no-climate), linear 18-col block | **+0.0078** | `co_devincl_full_refit.py`; frozen `colombia_matched_pairs.csv` |
| Colombia DLNM functional-form **sensitivity** | **+0.0122** (point only, no interval) | DLNM comparator run (distinct estimand) |
| Climate columns removed in matched no-climate model | **18 linear lags** | `freeze_matched_predictions.py` L31, design() |

## Action
- **No manuscript wording change required** for §5.1 in the current source — the contradiction was already repaired this session. This file documents the resolution and the code evidence.
- Retain the DLNM result strictly as a functional-form sensitivity; do **not** relabel it the primary Colombia climate block.
