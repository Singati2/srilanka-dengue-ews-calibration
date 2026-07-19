# CLOSEOUT VERDICT: **C2-CONFIRMED**

Provenance **CONFIRMED**, matched pair **VALID**, hygiene **applied**. The Sri Lanka M1 REFRAME stands as previously implemented; "design-locked / pre-specified" is defensible **for the spec-defined ladder and structured M1**. Author sign-off recommended, not blocking.

## Basis
- **Task 1 — PROVENANCE-CONFIRMED.** Spec L17 (`docs/hybrid_model_extension_spec.md`, commit `1d8e268`, 2026-06-14 13:24:14, never edited) predates the frozen SL results by: DAG ancestry on `main` (`1d8e268` is an ancestor of the results-report `02f986e` and of HEAD); no history-rewrite fingerprint (1/83 commits with ad≠cd, no mass-cd reset, original repo with a coherent 87-entry reflog, no bulk root import); and independent external corroboration — filesystem mtimes (spec written 13:15 < predictions generated 13:32) and the hash-pinned contemporaneous report ("Executed per the locked spec, commit 1d8e268 … exact row match"). See `provenance_report.md`.
- **Task 2 — matched pair VALID.** `M5_no-climate` is fit from scratch (`fit_eval('matched')` → new `LogisticRegression().fit`), same train rows, same C-grid protocol, same test set, differing from M5 only by removal of the DLNM climate cross-basis block. The +0.0006 gap vs M5−M1_frozen is explained by the independent refit (different penalty/standardization than the C=1e6 frozen M1) — the signature of a genuine refit, not coefficient-zeroing or relabeling. See `matched_pair_confirmation.md`.

## Qualification that survives CONFIRMED (do not overclaim)
CONFIRMED covers the **ladder and structured M1**. It does **not** make the featured interpretable estimand pre-specified: **M5 − M5_no-climate is post hoc** (absent from the frozen pipeline; M5 was specced as "a sensitivity, not primary"; no no-climate model was specced). Two honesty items therefore remain and are drafted for PI sign-off (they are not dissolved by provenance): describe the matched estimand as exploratory, and state plainly that the pre-specified primary (M4−M1) is the demoted non-nested contrast while the interpretable one is post hoc. See `manuscript_hygiene.md` §3c.

## What changed in the manuscript (v14, factual-precision only)
Three "comparable/similar size" phrasings → "consistently-signed, of uncertain magnitude" (SL +0.015 recal ≈ 2× CO +0.0078). Applied in `paper1_plos_gph_v14.tex` (39 pp, clean). v13 source preserved. No scientific-framing change was finalized; 3c drafts await PI.

## Not HALT, not POST-HOC
Not HALT (provenance not contradicted, matched pair valid). Not POST-HOC-routing (provenance is verifiable and confirmed, so "pre-specified/design-locked" language for the ladder need not be retired) — but the paper must not extend that pre-specified status to the post-hoc matched estimand, hence the 3c drafts.
