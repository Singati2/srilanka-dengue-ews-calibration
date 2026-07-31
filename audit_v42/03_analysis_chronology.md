# audit_v42 / 03 — Analysis chronology (§5.3)

**Date:** 2026-07-28 · **Evidence:** git tags/commits (authoritative), design-lock docs, output metadata. Dates are commit-authored dates from `git log`.

| # | Analysis | Date / commit | Tag | Classification |
|---|---|---|---|---|
| 1 | Original design-locked model ladder + Sri Lanka M4−M1 primary contrast | (pre-tag ladder) → frozen `2026-07-16` `8d76cd6` | `v6-analysis-frozen` | **internally design-locked, not registered** |
| 2 | Recognition that M4 vs M1 is structurally non-nested (does not isolate climate) | during v6 finalization | — | interpretive; motivates (3) |
| 3 | Matched climate ablation ΔNB(M5−M5_no-climate) created | within `v6-analysis-frozen` | `v6-analysis-frozen` | **post-hoc, exploratory** |
| 4 | Threshold-free proper-score design lock (metric/state/clustering/seed/calibration choices committed *before* any score) | `2026-07-15 11:28` `28c0341` | `alt-stats-plan-v1` | **post-result design-locked secondary** |
| 5 | Proper-score execution (`score_route_a.py`, committed results) | `2026-07-15 18:41` `1f12181` | `alt-stats-results-v1` | post-result design-locked secondary (executed after lock #4) |
| 6 | Calibration-intercept (−0.5 logit) sensitivity (`calibration_sensitivity.py`) | `2026-07-16 18:39` `e14ae31` | `alt-stats-results-v2` | **sensitivity** |
| 7 | DLNM functional-form sensitivity (Colombia) | within v6 frozen pipelines | `v6-analysis-frozen` | **sensitivity** |
| 8 | Development-inclusive (refit-both-models) decision-curve bootstraps, both settings | `v6-analysis-frozen` + reconstruction | `v6-analysis-frozen` | **diagnostic / uncertainty target** (primary robustness basis) |
| 9 | 90th-percentile matched climate ablation, both settings (B=1000) | `2026-07-26` `c32884c` (branch `add-90th-matched-ablation`) | — | **post-hoc, reviewer-responsive sensitivity** |
| 10 | Development-inclusive proper-score intervals, both settings (B=1000) | `2026-07-28` (branch `manuscript-v43-repair`, `analysis/devincl_proper_scores_v1/`) | — | **post-hoc, reviewer-responsive** (closes the conditional-only asymmetry) |

## Key ordering fact (design-lock before computation)
The proper-score **plan** (`alt-stats-plan-v1`, 2026-07-15 11:28) is committed **before** the proper-score **results** (`alt-stats-results-v1`, 2026-07-15 18:41), supporting the manuscript's statement that metric/state/clustering/seed/calibration/interpretation choices were locked before any score was computed. It was locked *after* the primary findings were known, so it is **post-result design-locked secondary**, not prespecified/primary — the manuscript labels it correctly.

## Discrepancy noted (evidence-hierarchy resolution)
A prior project note recorded the analysis freeze as `2026-06-19 / f1ace05`; the authoritative git tag `v6-analysis-frozen` is dated `2026-07-16 / 8d76cd6`. Per the evidence hierarchy (tagged release > notes), the **2026-07-16** frozen date is used. No manuscript claim depends on the earlier note.

## Label discipline (no upgrades)
No analysis is labeled prespecified, primary, confirmatory, registered, validated, or prospective beyond what the tags/design-locks support. The matched ablation and both new bootstraps (90th-pct, DI proper scores) are consistently labeled post-hoc/exploratory or reviewer-responsive sensitivity.
