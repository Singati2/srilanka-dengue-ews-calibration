# M4/M5 chronology evidence (v9)

Purpose: justify the manuscript's M4/M5 designation strictly from dated records, and document why "post-hoc" is **not** used for M5.

## Evidence 1 — design lock (pre-computation)
- **File:** `docs/hybrid_model_extension_spec.md`
- **SHA256:** `a396fd29cc747d25a047f6eabc88a4e4ea62892c00fcb16393706bf6c8b3acb2`
- **Date in file:** **2026-06-14** · **Status:** "specification only --- locks models, evaluation, and strict winning criteria **before any computation**, to prevent post-hoc model shopping or threshold tuning."
- **Quoted text:**
  - "**M4 --- hybrid (primary new model):** M1's lagged dengue features + the DLNM-style climate cross-basis ... all preprocessing train-only."
  - "**M5 --- hybrid + season + RDHS FE (steelman sensitivity):** M4 plus annual/semiannual harmonics and RDHS fixed effects; penalized logistic; **reported as a sensitivity, not the primary**."
  - "M4 vs M5 are both reported; neither is chosen on test performance. **M4 is the locked primary regardless of which scores higher.**"
- **Date relative to analysis execution:** this is the design-lock document; it predates computation ("before any computation"). The execution report (Evidence 2) carries the same date.
- **Conclusion justified:** **M4 was the initially planned (locked primary) hybrid.** **M5 was specified in the same dated plan, before computation, as a documented expanded model (a "sensitivity"), not the primary.** Therefore M5 is a *documented expanded* hybrid, **not** a post-hoc model.

## Evidence 2 — execution report
- **File:** `docs/hybrid_model_extension_report.md`
- **SHA256:** `da085e6de30cd5afc29ccc6f0330a6842bd4d7d722298d09c92712b5b99b071c`
- **Date in file:** **2026-06-14**
- **Quoted text:** "M4 (primary hybrid) ...", "M5 (steelman sensitivity) ...", "**M4 (primary hybrid) does not beat M1** --- its net benefit at p\*=0.30 is slightly lower"; "M5 ... ΔNB@0.30 95% CI just includes 0 ... explicitly not a model-winning result."
- **Conclusion justified:** the numbers reported for M4 (ΔNB(M4−M1) −0.008) and M5 (ΔNB(M5−M1) +0.0081) are from this dated execution of the locked plan.

## Resulting terminology (used consistently in v9)
- **M4 = initially planned hybrid** (the dated plan's locked primary).
- **M5 = documented expanded hybrid** (specified in the same dated plan as a sensitivity; more fully specified by adding seasonal harmonics and fixed effects).
- **Not used:** "post-hoc" / "post hoc" for M5 (the dated evidence shows M5 was specified before computation, not after examining results). "steelman" is avoided in the manuscript as informal, though it is the spec's internal label.
- The manuscript states the M5−M1 contrast is the main reported expanded-hybrid contrast and **not** a prospectively designated primary contrast; the prospectively designated primary hybrid was M4 (Evidence 1).

## What the dates do NOT support
- They do not support calling M5 "post-hoc" or "selected after seeing results."
- They do not support calling M5−M1 a registered/confirmatory primary contrast (M4−M1 was the planned primary hybrid contrast).
