# FINAL VERDICT

## Verdict: **C2 — REFRAME, qualified**

## Basis (the two gates, together)
- **Phase 3 reproduction gate: PASS.** Reconstructed SL M1/M4/M5 reproduce the committed frozen predictions to max|Δ| ≤ 1.1e-16 with verified row identity (all 3,926 test rows aligned by stable identifiers; none dropped/duplicated). < 1e-6 gate met.
- **Phase 4 design-intent finding: INTENDED-STRUCTURED.** The dated design-lock spec (`hybrid_model_extension_spec.md` L17) explicitly defines SL M1 as "incidence lags + harmonics + RDHS FE"; Colombia's spec defines its M1 as cases-only. The two baselines are deliberately different by design. The manuscript methods prose ("M1 = lags only") is the error, not the code.

Reproduction PASS **and** INTENDED-STRUCTURED ⇒ REFRAME (not REPAIR, not STOP). Qualified to **C2** because material inferential limitations remain (below), so the reframe is implemented **with explicit disclosure** rather than as a clean C1.

## Why C2 and not C1
1. **Cross-country baseline asymmetry.** SL M1 = cases+harmonics+RDHS; Colombia M1 = cases-only. M1-level benchmark comparisons (M0/M2/M3 − M1, and M4 − M1) are therefore **not comparable across countries**. Cross-setting claims must be confined to the **specification-matched climate estimand** (M5 − M5_no-climate), which *is* comparable, and this is disclosed.
2. **Evaluation-only (conditional) bootstrap.** The primary intervals resample spatial clusters on frozen predictions and omit model-development uncertainty; disclosed, and a development-inclusive interval is shown for the Colombia matched increment.
3. **Few clusters.** 26 RDHS clusters — modest for percentile cluster bootstrap; the finite-cluster caution applies to the primary intervals, not only the 8-cluster regime analyses.
4. **Recalibration dependence.** The SL matched increment (M5−M1) includes zero on raw predictions and excludes zero only under past-only recalibration; the estimand's separation from zero depends on the recalibration procedure.
5. **Predictive, not causal.** The matched contrast is a specification-matched *incremental predictive value of climate information*, not a causal/attributable/transportable effect.

## What the reframe entails (per Phase 11, Mode REFRAME)
- The **specification-matched contrast (M5 − M5_no-climate)** is the primary climate estimand in both countries; **M4 − M1** is retained as a design-locked, secondary, **non-nested / structurally mismatched** diagnostic (NOT called "confounding").
- SL M1 methods description corrected to reflect its non-climate structure (country-specific ladder).
- Cross-setting claims confined to the matched estimand; the M1-level baseline asymmetry disclosed (Colombia comparability, option (b): state and justify the asymmetry).
- The past-only rolling recalibration (verified leakage-free: eligibility uses target_week < prediction week) is reported alongside the optimistic cross-fit.

## M1-level benchmark quantities (Table 3, Table 4, Fig 2, M0/M2/M3 − M1)
Because the finding is INTENDED-STRUCTURED (not a bug), these **do not need to be regenerated** — the frozen M1 is the intended model. The only requirement is that their prose no longer describe M1 as cases-only for Sri Lanka, and that cross-country comparisons at the M1 level are not asserted.

## Status of the manuscript
The reframe was already implemented (prior turns) in the correct direction; this audit (a) confirms the direction is correct via the design-lock spec, (b) corrects the Rule-9 language ("confounded" → "non-nested / structurally mismatched"), and (c) records the C2 qualifications and the Colombia-comparability disclosure. No numbers were changed; no earlier version overwritten; nothing committed or pushed.

## Author sign-off still required
The scientific reframing (matched contrast primary; M4−M1 demoted) is a PI-level decision. This verdict authorizes it on the documentary evidence, but Khadka/Thapa/Shiwakoti should confirm the SL M1 specification and approve the reframe before submission.
