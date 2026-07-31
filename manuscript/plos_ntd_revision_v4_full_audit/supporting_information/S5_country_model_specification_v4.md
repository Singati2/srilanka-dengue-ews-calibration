# S5 Table — Per-country M0–M5 model specification, penalty/tuning, and software versions (DRAFT)

Verified from the committed generator scripts/reports. The conceptual M0–M5 labels do **not** imply identical feature implementation across countries.

## Per-country model implementation
| Conceptual model | Sri Lanka implementation | Colombia implementation |
|---|---|---|
| Predictor families | M0 season; M1 recent cases; M2 climate; M3 climate+season+RDHS FE; M4 cases+climate (DLNM cross-basis); M5 M4+season+RDHS FE | M0 season; M1 recent cases; M2 climate; M3 climate+season+dept FE; M4 cases+climate (linear lags); M5 M4+season+dept FE |
| Recent-case lags | recent incidence lags `[REPRODUCIBILITY RECORD INCOMPLETE — confirm exact SL lag set from the pilot spec]` | `cases_lag0, cases_lag1, cases_lag2, cases_lag4` (verified, Colombia script) |
| Climate variables / lags | **DLNM-style cross-basis** over temperature, precipitation, humidity; lags 0–8 wk; df≈3 (M4 = 31 features; M5 = 60 features) | **linear** weekly lags `precip_lag0–8` and `temp_lag0–8` (verified, Colombia script) |
| Seasonality | seasonal harmonic terms | `sin_woy_1, cos_woy_1, sin_woy_2, cos_woy_2` (verified) |
| Geographic fixed effects | RDHS division | department (`dept`) one-hot (verified) |
| Penalty | L2 (ridge) logistic | L2 (ridge) logistic |
| C / tuning | rolling-origin internal validation on training years; criterion mean validation AUC; grid C∈{0.1,1,10}; selected **M4 C=0.1, M5 C=10** (verified, hybrid report) | single validation split; criterion validation log-loss; grid C∈{0.001…10}; selected **M0 0.001, M1 0.01, M2 0.001, M3 0.001, M4 0.01, M5 0.01** (verified, ladder report) |
| Recalibration | rolling 52-week intercept-only, time-updated (no fallbacks) | Platt (logistic) recalibration fit on validation (verified, ladder report) |
| Events-per-variable | `[REPRODUCIBILITY RECORD INCOMPLETE — transcribe parameter counts vs events; no recomputation]` | `[REPRODUCIBILITY RECORD INCOMPLETE]` |

> Sri Lanka M4/M5 used a Python DLNM-style cross-basis (not canonical R `dlnm`, which was a separate comparator). Colombia did **not** use a DLNM cross-basis.

## Software / reproducibility versions
| Component | Version | Status |
|---|---|---|
| Python | — | Version not preserved in the current reproducibility record |
| NumPy, pandas, scikit-learn, statsmodels, SciPy | — | Versions not preserved in the current reproducibility record (no environment/requirements file committed) |
| R | 4.6.0 (2026-04-24) | Verified (`canonical_R_dlnm_report.md`) |
| dlnm | 2.4.10 | Verified |
| mgcv | 1.9.4 | Verified |
| tsModel | 0.6-2 | Verified |
| geopandas / pyogrio / pyproj / shapely | 1.1.3 / 0.12.1 / 3.7.1 / 2.1.2 | Verified (geometry build report) |
| rasterio / rasterstats | 1.4.4 / 0.21.0 | Verified (denominator build report) |
| LaTeX / build | TeX Live 2022 (pdfTeX 3.141592653-2.6-1.40.22), BibTeX 0.99d | Verified (build environment) |

Do not guess unrecorded versions; the Python modeling stack versions must be supplied by the authors before submission.
