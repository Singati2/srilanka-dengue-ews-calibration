# DLNM-style Climate Comparator — Report
*Executed per the locked spec (`docs/dlnm_climate_comparator_spec.md`, commit 155412d). All computed artifacts are **quarantined and git-ignored**; only this markdown report is proposed for commit. No frozen outcome/exposure/population, no v1/v2 table, and no prior pilot/sensitivity/recalibration/CI output was modified. No R installed; no packages installed.*

**Date:** 2026-06-12

## ⚠ Implementation disclosure (read first)
This comparator is a **Python DLNM-style cross-basis approximation**, **not canonical R `dlnm`** (R/`dlnm`/`mgcv` are not available in this environment). It builds a Gasparrini-style cross-basis as a tensor of **natural cubic splines on the climate value × natural cubic splines on the lag dimension** (patsy `cr`), summed over lags 0–8 weeks, fit by logistic regression. The manuscript must describe it as a cross-basis approximation, not claim the canonical `dlnm` implementation.

## 1. Setup & row matching
- Same registered cell: 75th-pct label, h=4, train 2018–2022 / test 2023–2025, same filter.
- **Exact primary-row match (stop-gate passed):** train 6,590, **test 3,926 — identical rows to the committed primary predictions** (`07f5916a…`); M1/M2/M3 reused on those rows, DLNM scored on the same rows. Labels matched.

## 2. Model & fit diagnostics
Climate cross-basis over lags 0–8 wk for **temperature, precipitation, relative humidity**; value-spline knots, imputation, and scaling **train-only**; lagged features past-only (leakage-safe). All converged, **no separation**, no L2 fallback needed.
| Model | features | max|coef| | converged | role |
|---|---|---|---|---|
| DLNM_clim_df3 | 27 | 0.37 | yes | **primary** |
| DLNM_clim_df4 | 48 | 0.27 | yes | pre-specified sensitivity |
| DLNM_clim_season_RDHS_df3 | 56 | 0.95 | yes | steelman sensitivity (+season +RDHS FE) |

## 3. Metrics vs M1 / M2 / M3 (test, prevalence 0.336)
| Model | AUC | PR-AUC | Brier | CITL | slope | NB@0.30 |
|---|---|---|---|---|---|---|
| **M1 lagged-AR** | **0.752** | **0.652** | **0.191** | +0.513 | 1.246 | **0.137** |
| M2 climate-only | 0.643 | 0.460 | 0.220 | +0.479 | 1.027 | 0.069 |
| M3 climate+season+RDHS | 0.652 | 0.476 | 0.220 | +0.596 | 0.738 | 0.078 |
| **DLNM_clim_df3 (primary)** | 0.714 | 0.545 | 0.203 | +0.438 | 0.944 | 0.111 |
| DLNM_clim_df4 | 0.713 | 0.540 | 0.203 | +0.434 | 0.897 | 0.111 |
| DLNM_clim_season_RDHS_df3 | 0.695 | 0.556 | 0.202 | +0.348 | 0.687 | 0.115 |

Two clear movements:
- **The DLNM-style model substantially improves on the simple M2/M3 climate logistics** (AUC 0.714 vs 0.643/0.652; PR-AUC 0.545 vs 0.46/0.48; NB@.30 0.111 vs 0.069/0.078). The richer lagged-nonlinear climate structure **does** capture more signal — confirming M2/M3 were a weak floor.
- **DLNM still falls short of M1** on every primary metric (AUC 0.714 < 0.752; NB@.30 0.111 < 0.137). The steelman (DLNM + season + RDHS FE) does **not** close the gap (AUC 0.695, NB 0.115).

## 4. Decision-curve / net benefit (test)
| p\* | DLNM_df3 | DLNM_df4 | DLNM+season+FE | M1 | M2 | M3 |
|---|---|---|---|---|---|---|
| 0.10 | 0.264 | 0.262 | 0.250 | 0.259 | 0.262 | 0.248 |
| 0.20 | 0.179 | 0.182 | 0.163 | 0.185 | 0.164 | 0.147 |
| 0.30 | 0.111 | 0.111 | 0.115 | **0.137** | 0.069 | 0.078 |
| 0.40 | 0.057 | 0.052 | 0.070 | **0.083** | 0.012 | 0.039 |

DLNM is competitive with M1 at low thresholds (p\*=0.10–0.20) but **M1 leads clearly at the registered p\*=0.30 and at 0.40** — the same threshold-dependent pattern seen throughout, now with a credible climate model.

## 5. ΔAUC / ΔNB vs comparators (RDHS cluster bootstrap, seed 20260612, B=1000, 0 failures)
| Comparison | metric | point | 95% CI | excludes 0? |
|---|---|---|---|---|
| **DLNM_df3 − M1** | ΔAUC | **−0.038** | **[−0.065, −0.010]** | **Yes (M1 better)** |
| **DLNM_df3 − M1** | ΔNB@0.30 | **−0.025** | **[−0.042, −0.005]** | **Yes (M1 better)** |
| DLNM_df3 − M2 | ΔAUC | +0.071 | [0.032, 0.111] | Yes (DLNM better) |
| DLNM_df3 − M2 | ΔNB@0.30 | +0.042 | [0.016, 0.071] | Yes (DLNM better) |
| DLNM_df3 − M3 | ΔAUC | +0.062 | [0.033, 0.085] | Yes (DLNM better) |
| DLNM_df3 − M3 | ΔNB@0.30 | +0.033 | [0.016, 0.053] | Yes (DLNM better) |

→ **Statistically supported both ways:** the DLNM-style climate model **significantly beats the simple climate logistics** (M2/M3) *and* is **significantly beaten by the recent-cases baseline M1** — on both discrimination and registered net benefit.

## 6. Interpretation (locked rules applied)
- The pre-committed branch is realized: **"even a more credible lagged-nonlinear climate comparator did not outperform the recent-case baseline operationally"** — and now this is **statistically supported** (ΔAUC and ΔNB vs M1 exclude 0). **This strengthens the paper.**
- It also **defuses the strawman objection directly**: a fair, recognizable climate model was built; it materially beats the simple M2/M3 logistics (so the earlier climate models were a floor, not a ceiling) — yet the surveillance baseline still wins where it matters operationally.
- DLNM beats M1 only at low thresholds (p\*≤~0.20), not at the registered p\*=0.30 — consistent with the decision-value framing (discrimination/low-threshold competitiveness ≠ operational decision advantage). **Keep the existing decision-value framing.**
- **No automatic headline change** (DLNM did not beat M1 on net benefit). Caveat reported: this is a cross-basis **approximation**, not R `dlnm`; 26-cluster bootstrap → CIs coarse. **Do not claim climate has no value** (it clearly carries signal, just less operational value than recent cases here) **and do not claim DLNM represents the whole EWS literature.**

## 7. Output files (quarantined, read-only, NOT committed) + SHA256
- `dlnm_comparator_metrics_v1.csv` — `dc57afd78554a1e542538de258f2687ff0828d2cd932ed350a07a4ff41a0f97d`
- `dlnm_comparator_dca_v1.csv` — `037dca4994acd04b195f466c074302ca2734d961f8e8ec2ed6471367301813ca`
- `dlnm_comparator_predictions_v1.csv` — `3c0f4bf2be08cb75de8fb30304b56fadb4d2596dfd98113a7d5a0dfac36029cb`
- `dlnm_comparator_diagnostics_v1.csv` — `a15b3f6f36fdece7be47982a88a39ae778947cd9e12cfb519407cc53c7769f6c`
- `dlnm_comparator_ci_v1.csv` — `925aa97c5e4acba8016ee1a7ba1ee993e84975a70bbcfb5defcee37d5d6c2a80`
- Metadata: `dlnm_comparator.meta.md` (all under `~/data_quarantine/model_pilots/dlnm_comparator_v1/`).

## 8. Confirmations
- **Python cross-basis approximation, not canonical R `dlnm`** (stated above and in metadata).
- One locked model + two pre-specified sensitivities; no post-hoc test-based selection; bootstrap CIs computed on fixed predictions.
- **No R/packages installed; no frozen files modified; no prior pilot/sensitivity/recalibration/CI output overwritten** (new directory only; input checksums re-verified; exact row match).
- **No data files committed** — only this markdown report is proposed for commit. Preregistration unchanged.

## 9. Next steps (separate, approval-gated)
Optional: rolling-52 recalibration of DLNM (drift expected, correctable as before); team-written p\* cost anchor; canonical R `dlnm` only if R is installed (approval required). Nothing runs until directed.
