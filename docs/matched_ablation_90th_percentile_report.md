# Matched Climate Ablation at the 90th-Percentile Outbreak Label — Report

*Executes the pre-registered spec `docs/matched_ablation_90th_percentile_spec.md` (reviewer finding #1). Closes the open limitation that the specification-matched, climate-specific ablation $\Delta$NB(M5$-$M5_no-climate) had been evaluated only at the 75th-percentile label.*

**Date:** 2026-07-26 · **Status:** run complete · **Seed:** 20260612 · **B:** 1000 (development-inclusive refit bootstrap; 0 failures both settings)
**Scripts:** `analysis/matched_ablation_90pct_v1/{colombia,srilanka}_matched_ablation_90pct_v1.py`
**Outputs:** `analysis/matched_ablation_90pct_v1/*_results.json`, `*_distribution.csv`

## Method (faithful derivatives; only the outcome definition changed)
Verbatim design/fit/recalibration/net-benefit logic from the frozen 75th-percentile pipelines
(`geo_effect_decomposition/co_devincl_full_refit.py`; `v18_bootstrap_b1000/sl_devinclusive_B1000.py`).
Colombia relabels via the committed train-only E3 labels (`colombia_outbreak_threshold_labels_v1.csv`,
`label_90`, verified 1.000000 row-for-row agreement of `label_75` vs the frozen modeling table's
`label_h4`); Sri Lanka recomputes the per-unit training-split `quantile(0.90)` inline. Colombia design
was precomputed to numpy and both bootstraps parallelized across cores over pre-generated seeded picks
(identical numerics to sequential). Primary target = development-inclusive interval (both models refit +
recalibrated per cluster resample); conditional (frozen-prediction) interval secondary.

## Reproduce-first gate (75th) — PASSED both settings
- Colombia: matched $+0.00783$ (target $+0.00786$), compound M5$-$M1 $+0.01878$ (target $+0.018775$).
- Sri Lanka: M5 vs frozen $\max|\Delta|=2.1\times10^{-13}$; conditional recal matched $+0.01565$ (target $+0.0157$).
- Colombia 90th compound M5$-$M1 reproduced E3 exactly: $+0.00923$ (E3 $+0.0092$).

## Results — matched climate-specific increment $\Delta$NB(M5$-$M5_no-climate) at $p^*=0.30$

| Setting | Threshold | Test prev (events) | Matched $\Delta$NB | Conditional 95% CI | Dev.-inclusive 95% CI |
|---|---|---|---|---|---|
| Sri Lanka | 75th (recal) | 0.336 | +0.0157 | +0.0066 to +0.0257 | −0.0002 to +0.0302 |
| Sri Lanka | **90th** (recal) | 0.106 (417) | **+0.0034** | −0.0070 to +0.0138 | −0.0105 to +0.0185 |
| Colombia | 75th | 0.375 | +0.0078 | +0.0039 to +0.0119 | +0.0008 to +0.0209 |
| Colombia | **90th** | 0.235 (3,136) | **+0.0081** | +0.0029 to +0.0138 | +0.0009 to +0.0188 |

## Interpretation (pre-committed to report regardless of sign; corrected after adversarial harsh review)
At the stricter 90th-percentile label the recalibrated increment was **+0.0034 in Sri Lanka** (both
intervals span zero) and **+0.0081 in Colombia** (DI lower bound +0.0009). **This is NOT a setting
effect.** A 4-agent publishability council initially framed it as "Sri Lanka collapses / Colombia holds,"
but a unanimous 3-reviewer harsh peer-review panel (2026-07-26) rejected that as a **difference-in-
significance (Gelman–Stern) fallacy**: the two development-inclusive intervals ([-0.0105,+0.0185] vs
[+0.0009,+0.0188]) overlap heavily, each point lies inside the other's interval, no heterogeneity test
was run, and the apparent contrast is confounded with (a) event count (417 vs 3,136 positive weeks →
wider SL intervals), (b) prevalence-dependence of net benefit at fixed p*=0.30 (SL prevalence fell
0.336→0.106, below p*; Colombia 0.375→0.235), and (c) the settings differing on every axis. Colombia's
+0.0009 is inferentially identical to the 75th's +0.0008, which S17 already declares not a firm
exclusion of zero. **Honest conclusion: at the stricter threshold the matched climate increment is small
and compatible with zero in BOTH settings**; the numerical difference is hypothesis-generating at most.
The 90th label is a train-only percentile of a drifting series (Colombia test prevalence still ~23.5%),
so it is
not epidemic-rare.

## Manuscript integration
`revised_manuscript.tex`: S14 matched-ablation sub-table added and the "not recomputed at 80th/90th …
open limitation" concession replaced with the result; abstract's "matched ablation was not repeated at
the stricter 90th-percentile outcome" corrected to the actual finding for both settings. Compiles
33 pp, 0 undefined refs, abstract 270 words. No frozen file modified; nothing committed pending review.

## Caveats / non-claims
Post-hoc reviewer-responsive sensitivity; 75th $h=4$ remains the reference. Pointwise, multiplicity-
unadjusted. Development-inclusive intervals only (no wild-cluster-t / jackknife re-run at 90th).
