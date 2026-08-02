# audit_v42 / 02 — Headline results matrix (§5.2)

**Date:** 2026-07-28 · **Status legend:** MATCH = reproduced from code/frozen outputs this session; NEW = computed this session, gate-reproduced; ROUNDING = differs only by rounding.
All decision-curve values at p\*=0.30, h=4, 75th-percentile label unless stated. Sources: `ALT_STATS/frozen/*_matched_pairs.csv`, `co_devincl_full_refit.py`, `sl_devinclusive_B1000.py`, `analysis/matched_ablation_90pct_v1/`, `analysis/devincl_proper_scores_v1/`, `score_route_a.py`.

## Sri Lanka
| Quantity | Value | Conditional 95% CI | Development-inclusive 95% CI | Source | Status |
|---|---|---|---|---|---|
| ΔNB(M4−M1) design-locked primary | −0.008 | −0.028 to +0.013 | — | S3 Table / frozen preds | MATCH |
| ΔNB(M5−M1) | +0.0081 | −0.0012 to +0.0181 | — | frozen preds | MATCH |
| Matched ablation, raw | +0.0087 | −0.0015 to +0.0188 | −0.0079 to +0.0245 | sl_devinclusive_B1000.py | MATCH |
| Matched ablation, recalibrated | +0.0157 | +0.0066 to +0.0257 | −0.0002 to +0.0302 | sl_devinclusive_B1000.py | MATCH |
| Matched ablation, 90th-pct (recal) | +0.0034 | −0.0070 to +0.0138 | −0.0105 to +0.0185 | srilanka_matched_ablation_90pct_v1.py | NEW |
| Proper score ΔNLL (recal) | −0.0207 | −0.0346 to −0.0067 | **−0.0403 to +0.0040** | devincl_proper_scores_v1 | NEW (DI) |
| Proper score ΔBrier (recal) | −0.0079 | (excl 0) | **−0.0153 to +0.0013** | devincl_proper_scores_v1 | NEW (DI) |
| Discrimination ΔAUC (recal) | +0.027 | excl 0 | — | score_route_a.py | MATCH |
| Calibration ICI (full vs matched) | 0.027 vs 0.045 | — | — | score_route_a.py | MATCH |

## Colombia
| Quantity | Value | Conditional 95% CI | (Partial) development-inclusive 95% CI | Source | Status |
|---|---|---|---|---|---|
| ΔNB(M5−M1) compound | +0.0188 | +0.0117 to +0.0260 | — | co_devincl_full_refit.py | MATCH |
| Matched ablation (primary, linear 18-col climate) | +0.0078 | +0.0039 to +0.0119 | +0.0008 to +0.0209 | co_devincl_full_refit.py | MATCH |
| Calibration-intercept (−0.5 logit) sensitivity | +0.0042 | −0.0015 to +0.0099 | — | calibration_sensitivity.py | MATCH |
| DLNM functional-form sensitivity | +0.0122 | (point only) | — | DLNM comparator | MATCH |
| Reporting-delay (3-wk censor) sensitivity | +0.0049 | — | — | reporting-delay emulation | MATCH |
| Matched ablation, 90th-pct | +0.0081 | +0.0029 to +0.0138 | +0.0009 to +0.0188 | colombia_matched_ablation_90pct_v1.py | NEW |
| Proper score ΔNLL (recal) | −0.0089 | −0.0165 to −0.0011 | **−0.0224 to −0.0002** | devincl_proper_scores_v1 | NEW (DI) |
| Proper score ΔBrier (recal) | −0.0043 | (excl 0) | **−0.0102 to −0.0004** | devincl_proper_scores_v1 | NEW (DI) |
| Discrimination ΔAUC (recal) | +0.012 | excl 0 | — | score_route_a.py | MATCH |
| Calibration ICI (full vs matched) | 0.109 vs 0.113 | — | — | score_route_a.py | MATCH |

## Adjudication
- No CONTRADICTION or UNVERIFIED cells among headline values.
- The two NEW analyses (90th-pct matched ablation; DI proper scores) each reproduced the corresponding frozen/conditional point estimate as a gate before their bootstraps ran.
- **Key consistency gained:** DI proper scores now match the DI decision-curve pattern within each setting (Sri Lanka both cross zero; Colombia both boundary-adjacent below zero), removing the prior conditional-only asymmetry.
