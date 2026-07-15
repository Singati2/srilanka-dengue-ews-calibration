# Phase 6 — Recalibration & uncertainty language audit: PASS

## Three recalibration regimes distinguished in the manuscript
1. **Raw** (frozen hybrids were not recalibrated; M0–M3 were). Primary contrasts reported raw first.
2. **Cross-fitted (ISO-week-parity two-fold)** — leakage-controlled but **internal and optimistic** (uses concurrent, temporally adjacent test weeks); explicitly labeled an optimistic upper bound; **not** presented as operationally deployable.
3. **Past-only rolling-52-week** (operational emphasis) — at each test week an intercept recalibration fit only on forecast–outcome pairs observable **before** that week (leakage-free; eligibility target_week < prediction week). Given operational primacy in the recalibration subsection.

Verified: the cross-fit is never described as deployable; the past-only procedure carries the operational reading. Both are reported for M4−M1 (raw −0.008 → recal +0.010, CI incl. 0) and the frozen M5−M1 (raw +0.008 → recal +0.015, CI excl. 0). **The +0.015 is now correctly attributed to the frozen (non-matched) M5−M1 contrast, not to the matched estimand** (Phase 4 fix); the matched estimand's separation from zero is stated as recalibration-dependent and specific to the frozen contrast.

## Bootstrap / uncertainty language
- Intervals are **cluster-bootstrap percentile intervals conditional on the fitted prediction models** — resample the spatial unit on frozen test predictions; do **not** refit models, repeat penalty selection, or refit recalibration. Explicitly stated to omit model-development/feature-selection/tuning/training-sample uncertainty.
- **26-RDHS finite-cluster limitation** stated; cautioned further for 8-cluster regime analyses.
- Colombia matched increment additionally reports a **development-inclusive refit-bootstrap** interval that includes zero — the honest contrast to the conditional interval.

No overstatement found; language is consistent with §C/§D and Rules 5–6.
