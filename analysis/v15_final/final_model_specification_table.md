# Phase 3 — Final model specification table (country-specific, from code + dated specs)

| Country | Model | Case history | Climate | Seasonality | Geography | Interpretation |
|---|---|---|---|---|---|---|
| Sri Lanka | M1 | inc_t, lag1, lag2, lag4 | — | sin1,cos1,sin2,cos2 | RDHS FE | Structured recent-surveillance benchmark (near-unpenalized C=1e6, AR-only standardization) |
| Sri Lanka | M4 (prespecified primary) | ✓ | DLNM cross-basis (temp, precip, RH; lags 0–8; cr df=3) | — | — | cases+climate; M4−M1 non-nested, does not isolate climate |
| Sri Lanka | M5 (expanded sensitivity) | ✓ | DLNM cross-basis | ✓ | RDHS FE | full hybrid; whole-design standardization, C-selected |
| Sri Lanka | M5_no-climate (matched) | ✓ | — | ✓ | RDHS FE | independently refit; M5−M5_no-climate = specification-matched climate estimand (post hoc) |
| Colombia | M1 | cases_lag0,1,2,4 | — | — | — | cases-only recent-surveillance benchmark |
| Colombia | M4 | ✓ | linear climate lags | — | — | cases+climate |
| Colombia | M5 | ✓ | climate | ✓ | 32 dept FE | full hybrid |
| Colombia | M5_no-climate (matched) | ✓ | — | ✓ | 32 dept FE | independently refit; matched climate estimand (post hoc, original submission) |

**Baselines are intentionally different by design** (SL M1 structured; CO M1 cases-only), each fixed in its own dated spec (`hybrid_model_extension_spec.md` L17; `colombia_model_ladder_spec.md` L35). No universal model-label equivalence is asserted; M1-level cross-country comparisons are not made; cross-setting synthesis is restricted to M5 − M5_no-climate.
