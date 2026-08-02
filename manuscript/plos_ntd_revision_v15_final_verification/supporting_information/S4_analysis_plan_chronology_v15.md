# S4 Text — Analysis-plan and addendum chronology (transcribed from dated records; no recomputation)

This item documents the prespecified-versus-documented-extension chronology and, in particular, the M4/M5 hybrid designation. Facts are transcribed from dated committed records; no analysis was rerun.

## M4/M5 hybrid designation (from the dated design-lock)
- **Design-lock document:** `docs/hybrid_model_extension_spec.md`, sha256 `a396fd29cc747d25a047f6eabc88a4e4ea62892c00fcb16393706bf6c8b3acb2`, dated **2026-06-14**, status "specification only — locks models, evaluation, and strict winning criteria **before any computation**."
- **M4 = planned primary hybrid:** M1's lagged dengue features plus the DLNM-style climate cross-basis; "M4 is the locked primary regardless of which scores higher." The planned primary Sri Lanka hybrid estimand is **ΔNB(M4−M1) on the full test set at p\*=0.30 under the h=4, 75th-percentile outcome definition.**
- **M5 = pre-computation expanded-hybrid sensitivity:** M4 plus annual/semiannual harmonics and RDHS fixed effects; specified in the same dated plan, before computation, "reported as a sensitivity, not the primary."
- **Execution report:** `docs/hybrid_model_extension_report.md`, sha256 `da085e6de30cd5afc29ccc6f0330a6842bd4d7d722298d09c92712b5b99b071c`, dated 2026-06-14: ΔNB(M4−M1) = −0.008; ΔNB(M5−M1) = +0.0081.
- **Consequence for secondary analyses:** the Sri Lanka **threshold, horizon, and train-defined regime** analyses were computed on the **M5−M1** contrast and are **secondary or exploratory**; they were **not** part of the planned primary M4 estimand, and M4 was not evaluated across those regimes. "post-hoc" is not used for M5 (it was specified before computation).

## Prespecified vs documented-extension status
- Prespecified core: model ladder M0–M5; recent-surveillance benchmark; calibration/recalibration; decision-curve net benefit at the reference threshold p\*=0.30; primary h=4, 75th-percentile label.
- Documented extensions (secondary/exploratory, pointwise, multiplicity-unadjusted): threshold grid (p\*=0.20/0.30/0.40), horizons h=1/2/8/12, stricter 90th-percentile label, train-defined regimes, and the two author-authorized v2 sensitivities (Colombia 2022-only; Sri Lanka wild-cluster-bootstrap-t).
- No prospective public registration is claimed.

## Current Supporting-Information map (this manuscript, S1–S12)
S1 STROBE (draft) · S2/S3 TRIPOD+AI / PROBAST (draft internal aids) · S4 this chronology · S5 per-country M0–M5 specification · S6 per-analysis bootstrap protocol · S7 Sri Lanka linkage/climate-lag/2021-anomaly grid · S8 Sri Lanka targeted-value regime analysis (M5−M1) · S9 Colombia threshold/horizon/2022-only · S10 reproducibility inventory (draft) · S11 Sri Lanka wild-cluster-bootstrap-t table (+ machine-readable results) · S12 Sri Lanka wild-bootstrap method/reproducibility.
