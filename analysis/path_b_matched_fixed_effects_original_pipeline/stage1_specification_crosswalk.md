# Stage 1 — Model-Specification Crosswalk

All from `scripts/colombia_model_ladder_h4_75pct_v1.py` (line refs) + frozen `colombia_model_coefficients_h4_75pct_v1.csv` (feature counts). Read-only; no fitting.

Feature-set definitions (script:39–40):
`M1=['cases']` · `M4=['cases','climate']` · `M5=['cases','climate','season','dept']`.

| Component | Original M1 | Original M5 | **M5_no_climate_matched** | Evidence |
|---|---|---|---|---|
| Recent-case terms | `cases_lag0,1,2,4`, `log1p`, standardized | same | **same** | script:19,24–25,32–33 |
| Seasonal terms | none | `sin/cos_woy_1,2` (raw) | **same as M5** (present) | script:19,29 |
| Department fixed effects | **none** | **32 dept dummies** (`dept_*`, all levels) | **same as M5** (present) | script:34–36; coef file: M5 dept_FE=32, M1=0 |
| Climate variables | none | `precip_lag0–8` (`log1p`), `temp_lag0–8` (raw) — 18 cols | **REMOVED (the only difference)** | script:18,26–28 |
| Climate lags / basis | n/a | raw lags 0–8; **no DLNM cross-basis** | removed | script:18,26–28 |
| Other non-climate | intercept | intercept | intercept | script:93 |
| Scaling | standardize continuous (cases) on **train** stats | standardize cases+climate on train | standardize cases on train | script:31–33 |
| Missing-data handling | uses `cases_lag0,1,2,4` via `log1p`; `*_missing` flags **not** entered | same | same | script:24–25 (CAS list) |
| Penalty & tuning | L2; `C` tuned on **validation log loss** over `[0.001…10]` | same | same | script:15,42–51 |
| Solver | `lbfgs`, `max_iter=5000` | same | same | script:47 |
| Train/val/test rows | common-complete 53,711 / 12,713 / 13,361 | same | same | script:102–106 |
| Recalibration | **Platt on validation** predictions, applied to test | same | same | script:54–57,80 |
| Feature count (frozen) | 4 | 58 (4 cases + 18 climate + 4 season + 32 dept) | **40 (4 cases + 4 season + 32 dept)** | coef file |

## Matched baseline definition (locked)
```
M5_no_climate_matched = ['cases','season','dept']
```
Constructed by cloning **M5** and removing **only** the 18 climate columns (`precip_lag0–8`, `temp_lag0–8`). It **retains** all M5 non-climate structure: recent-case terms, seasonality, all 32 department fixed effects, the identical common-complete row set, train-only scaling, L2 penalty with validation-tuned `C`, and Platt-on-validation recalibration. It is **not** M1 (M1 lacks season and department fixed effects), so it must not be labeled M1.

## Locked contrasts
- **Primary diagnostic:** `ΔNB_climate = NB(M5) − NB(M5_no_climate_matched)` at p*=0.30, h=4, 75th-pct, common-complete test rows, recalibrated (frozen recalibration status).
- **Decomposition (must sum to the original within tolerance):**
  - `ΔNB_original   = NB(M5) − NB(M1)`  (frozen +0.018775)
  - `ΔNB_nonclimate = NB(M5_no_climate_matched) − NB(M1)`
  - `ΔNB_climate    = NB(M5) − NB(M5_no_climate_matched)`
  - Check: `ΔNB_nonclimate + ΔNB_climate ≈ ΔNB_original`.

## Fairness / leakage pre-checks (to verify at run time, Stage 2)
Identical test rows/outcomes across M1, M5, matched; identical h=4 and p*=0.30; no test data in fit/scale/tune/recalibration (all train- or validation-fit per script); no duplicated municipality-week rows; lags use only pre-prediction information (built upstream in the modeling table); **M5 and matched differ only in the 18 climate columns** (verify retained/removed column lists explicitly).
