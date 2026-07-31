# M4/M5 chronology and terminology decision (v7)

## Decision: Scenario A
M4 was the **initially planned (locked primary) hybrid**; M5 was an **expanded hybrid extension** added as a more fully specified sensitivity model. Terminology is chosen from the dated record, **not** from which result is more favorable.

## Dated evidence (quoted verbatim)
From `docs/hybrid_model_extension_spec.md` — **Date: 2026-06-14**, "specification only — locks models, evaluation, and strict winning criteria before any computation, to prevent post-hoc model shopping" (commit 1d8e268):
- "**M4 — hybrid (primary new model):** M1's lagged dengue features + the DLNM-style climate cross-basis … in one penalized logistic regression."
- "**M5 — hybrid + season + RDHS FE (steelman sensitivity):** M4 plus annual/semiannual harmonics and RDHS fixed effects … **reported as a sensitivity, not the primary.**"
- "Primary hypothesis: **M4 (hybrid) improves over M1** …"
- "**M4 vs M5 are both reported; neither is chosen on test performance. M4 is the locked primary regardless of which scores higher.**"

From `docs/hybrid_model_extension_report.md` (**Date: 2026-06-14**): "M4 (primary hybrid)"; "M5 (steelman sensitivity)".

For Colombia (external framework replication), the dated planning memos report the headline hybrid contrast as **M5−M1** (`docs/cross_country_interpretation_memo.md`; `docs/paper_strategy_reframe_memo.md`: "Primary metric: ΔNB(M5−M1)"). This is why the manuscript ended up using M5−M1 as the cross-setting headline while the Sri Lanka spec locked M4 as primary.

## Consequence for the manuscript
- **M4 = initially planned hybrid** (the locked primary hybrid in the dated Sri Lanka spec).
- **M5 = expanded hybrid** (M4 + seasonal harmonics + geographic fixed effects).
- **M5−M1 = the main reported expanded-hybrid contrast** (used for the cross-setting comparison and as the Colombia headline). It is **not a prospectively registered or confirmatory contrast.** The prospectively planned Sri Lanka hybrid contrast was **M4−M1**, which did not exceed M1.

## Terminology applied consistently (Methods, Results, Table 4, captions, Abstract, Discussion, SI)
- "initially planned hybrid (M4)" / "expanded hybrid (M5)".
- "main reported expanded-hybrid contrast" for M5−M1; describe M4−M1 as the initially planned hybrid contrast.
- **Banned terms removed:** "steelman", "confirmatory", "primary reference contrast" (as applied to M5−M1), "hybrid reference", "registered/preregistered" (no public registration; the dated internal plan is described as "the dated analysis plan", and "no prospective public registration is claimed" is retained).

## Freeze note
No model was run; M4/M5 numbers are transcribed from the frozen `hybrid_model_extension_report.md`. This is a terminology/writing reconciliation only.
