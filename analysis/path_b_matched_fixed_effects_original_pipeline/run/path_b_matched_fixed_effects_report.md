# Path B — Matched Fixed-Effects Report (Stage 2 results)
Original Colombia pipeline; only addition = `M5_no_climate_matched=['cases','season','dept']` (M5 minus 18 climate cols).
Gate A PASS (reproduced +0.01878). Gate B PASS (M5 vs matched differ only by precip_lag0–8, temp_lag0–8).

## Test-set net benefit (p*=0.30, recalibrated, n=13,361)
| Model | features | AUC | NB@0.30 |
|---|---|---|---|
| M1 (cases) | 4 | 0.685 | +0.1171 |
| matched (cases+season+deptFE) | 40 | — | +0.1280 |
| M5 (cases+climate+season+deptFE) | 58 | 0.726 | +0.1358 |
| M4 (cases+climate) | 22 | 0.699 | +0.1293 |

## Decomposition of ΔNB(M5−M1)=+0.01878  (paired GID_2 bootstrap 95% CI)
| Component | ΔNB | 95% CI | share |
|---|---|---|---|
| non-climate (matched − M1): season + department FE | **+0.01095** | [+0.0060, +0.0164] | ~58% |
| **climate (M5 − matched), net of season+deptFE** | **+0.00783** | **[+0.0039, +0.0119]** | ~42% |
| M4 − M1 (climate on cases, NO FE) — separate | +0.01224 | [+0.0073, +0.0171] | — |
| sum check (nonclimate+climate−original) | +0.000000 | — | — |

## Reading (per approved rules)
- Matched climate increment +0.0078: point > +0.005 and 95% CI [+0.0039,+0.0119] excludes 0 and extends past the ±0.005 reference band → **small but non-negligible; not a strong negligible-effect result.**
- ~58% of the headline +0.0188 is unmatched non-climate structure (season + dept FE M1 lacked) → +0.0188 **overstates** the climate contribution.
- Cross-reference: earlier leave-one-department-out spatial CV gave ΔNB(M5−M1) = −0.0007 [−0.0104,+0.0098] → the increment does **not transport** across departments; the small matched climate effect may proxy seasonal/geographic structure.
