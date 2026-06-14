# Targeted Value of Climate — Stage 1A (h=4) Report
*Conditional ΔNB(M5 − M1) by train-defined regime at h=4 / 75th-pct, per the locked spec (`docs/novel_contribution_targeted_value_of_climate_spec.md`, commit 91ab128). **Existing predictions only — no refit, no new labels, no BYM2, no spatial smoothing, no exposure rebuild.** All computed artifacts are **quarantined and git-ignored**; only this markdown report is proposed for commit. No frozen outcome/exposure/population, no v1/v2 table, and no prior output was modified.*

**Date:** 2026-06-14 · **Scope:** Stage 1A only — h=4 only; multi-horizon (h=1,2,8,12), BYM2, and population-weighted exposure are **not** run.

## 1. Inputs & stop-gate (passed)
- M1 from committed primary (`predictions_h4_75pct_v1.csv`); M5 from `hybrid_model_predictions_v1.csv`.
- **Row/label match:** 3,926 test rows, labels identical to committed primary, **M1 byte-identical (max|Δ|=0)**. 26 RDHS, identifiers present.

## 2. Regime definitions (TRAIN-only, 2018–2022)
Computed from the v2 train period (read-only): per-RDHS **mean incidence** → median split = **13 low / 13 high**; per-RDHS **lag-1 incidence autocorrelation** → median split = **13 weak-AR / 13 strong-AR**. Combined = 4 cells (5–8 RDHS each). No test data used to define regimes.

## 3. Conditional ΔNB(M5 − M1) at p\*=0.30 — RDHS-cluster bootstrap 95% CI (B=1000, 0 failures)
| Regime | n | events | RDHS | ΔNB | 95% CI | excl 0? | prop boot >0 | powered? |
|---|---|---|---|---|---|---|---|---|
| ALL (reference) | 3,926 | 1,321 | 26 | +0.0081 | [−0.0012, 0.0181] | No | 0.96 | yes |
| incidence: low | 1,963 | 715 | 13 | +0.0034 | [−0.0100, 0.0181] | No | 0.66 | yes |
| incidence: high | 1,963 | 606 | 13 | +0.0128 | [−0.0009, 0.0264] | No | 0.97 | yes |
| AR: weak | 1,963 | 629 | 13 | +0.0079 | [−0.0039, 0.0213] | No | 0.90 | yes |
| AR: strong | 1,963 | 692 | 13 | +0.0083 | [−0.0071, 0.0234] | No | 0.85 | yes |
| low + weak-AR | 1,208 | 477 | 8 | +0.0122 | [−0.0032, 0.0295] | No | 0.94 | **under** |
| low + strong-AR | 755 | 238 | 5 | −0.0108 | [−0.0301, 0.0098] | No | 0.15 | **under** |
| high + weak-AR | 755 | 152 | 5 | +0.0010 | [−0.0142, 0.0170] | No | 0.52 | **under** |
| **high + strong-AR** | 1,208 | 454 | 8 | **+0.0202** | **[0.0038, 0.0370]** | **Yes** | 0.99 | **under (8 RDHS)** |

**At the registered p\*=0.30, no adequately-powered regime CI excludes 0.** The single CI-excluding regime (high-incidence + strong-AR) is **underpowered** (8 RDHS clusters < 10).

## 4. ΔNB at p\*=0.20 and 0.40 (powered single-axis regimes)
| Regime | p\*=0.20 ΔNB [CI] | excl 0? | p\*=0.40 ΔNB [CI] | excl 0? |
|---|---|---|---|---|
| ALL | +0.0096 [−0.0005, 0.0187] | No | +0.0241 [0.0090, 0.0399] | **Yes** |
| incidence: low | +0.0131 [0.0004, 0.0276] | **Yes** | +0.0236 [0.0049, 0.0436] | **Yes** |
| incidence: high | +0.0060 [−0.0079, 0.0200] | No | +0.0246 [0.0022, 0.0486] | **Yes** |
| AR: weak | +0.0186 [0.0080, 0.0302] | **Yes** | +0.0187 [−0.0026, 0.0408] | No |
| AR: strong | +0.0005 [−0.0131, 0.0153] | No | +0.0296 [0.0066, 0.0516] | **Yes** |

So M5's net-benefit advantage **does** reach significance in some powered regimes/thresholds — but **at p\*=0.20 (low-incidence, weak-AR) and especially at p\*=0.40 (overall + several regimes), not at the registered p\*=0.30.**

## 5. Per-RDHS descriptive ΔNB@0.30 (no bootstrap, no smoothing — descriptive only)
- **16/26 RDHS** have ΔNB@0.30 > 0; 2 RDHS flagged unstable (low events).
- Most positive: Nuwara Eliya +0.061, Gampaha +0.056, Trincomalee +0.047, Kandy +0.046, Ratnapura +0.032 (several are high-incidence/strong-AR, consistent with §3).
- Most negative: Matale −0.038, Badulla −0.028, Mannar −0.023, Colombo −0.019, Hambantota −0.018.
- This is per-division description only — **not** a smoothed surface and **not** BYM2 (those are deferred to Stage 2).

## 6. Underpowered flags
Single-axis regimes (13 RDHS, ~1,963 rows, ~600–715 events): **adequately powered**. Combined regimes (5–8 RDHS): **underpowered** on RDHS-cluster count (<10) regardless of row/event counts — bootstrap CIs reported but treated as descriptive/hypothesis-generating.

## 7. Whether any regime met the targeted value-of-climate criteria
**No (at the registered p\*=0.30).** Per the pre-committed rules:
- No **adequately-powered** regime's ΔNB@0.30 CI excludes 0 → no confirmed targeted value-of-climate signal.
- The only CI-excluding regime (high-incidence+strong-AR, +0.020 [0.004, 0.037]) is **underpowered** → "positive only in a tiny/underpowered regime → do not claim evidence" → **hypothesis-generating only.**
- M5's broader pattern is positive (16/26 RDHS; prop-boot>0 0.85–0.97) and reaches significance at p\*=0.40 / in low-incidence/weak-AR at p\*=0.20 — but these are **not** the registered primary threshold.

## 8. Scientific conclusion (honest, rules-bound)
- **The h=4 Stage 1A pilot did NOT find confirmed targeted operational value of climate at the registered p\*=0.30 in any adequately-powered regime**, despite the hybrid M5 near-miss overall.
- It **did** generate a specific, testable hypothesis for a confirmatory, better-powered study: climate appears most valuable in **high-incidence + strong-autocorrelation** divisions and at **higher decision thresholds (p\*≈0.40)** — directions consistent across regimes and per-RDHS descriptives.
- **No manuscript headline change** (per rules): the study's framing stands — recent-cases surveillance is hard to beat operationally at the registered threshold; targeted climate value is a power-limited, hypothesis-generating signal, not confirmed evidence.

## 9. Output files (quarantined, read-only, NOT committed) + SHA256
- `conditional_dnb_h4_v1.csv` — `9359608724…1d6465ad`
- `conditional_dnb_bootstrap_ci_h4_v1.csv` — `ce80b0ce03…854f1ad78`
- `rdhs_descriptive_dnb_h4_v1.csv` — `0e153e26e5…57c1644bae`
- `stage1a_h4_diagnostics_v1.csv` — `01c700873c…1f9ebfe653`
- Metadata: `targeted_value_stage1a_h4.meta.md`; runner `_run_targeted_value_stage1a_h4.py` (all under `~/data_quarantine/model_pilots/targeted_value_climate_stage1a_h4_v1/`).

## 10. Confirmations
- Stage 1A / **h=4 only**; no refit of M1 or M5; no R DLNM rerun; **no new labels; no BYM2; no spatial smoothing; no exposure rebuild; no multi-horizon.**
- No frozen data/v1/v2 modified; no prior pilot/sensitivity/recalibration/CI/DLNM/hybrid output overwritten (new directory; row/label match verified).
- **No data files committed** — only this markdown report is proposed for commit. Preregistration unchanged; headline unchanged pending team review.

## 11. Next steps (separate, approval-gated)
Stage 2 (per-RDHS BYM2 value surface) and Stage 3 (population-weighted exposure) only on approval; a confirmatory/better-powered evaluation of the high-incidence+strong-AR hypothesis. Nothing runs until directed.
