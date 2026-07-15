# Task 3 — Manuscript hygiene

Operated on a NEW file `paper1_plos_gph_v14.tex` (built: 39 pp, 0 undefined, 0 errors). The v13 source `paper1_plos_gph.tex` is preserved unmodified. Diff: `manuscript_v13_to_v14.diff`.

## 3a — Residual M1-level cross-country comparisons: **NONE FOUND (clean)**
Swept abstract, results, cross-setting synthesis, discussion, conclusion for any SL-vs-CO claim anchored at the M1 / benchmark / M0–M3−M1 / M4−M1 level. Findings:
- **Every quantitative cross-setting claim is anchored on the specification-matched estimand** M5−M5_no-climate (SL +0.0087, CO +0.0078) — the comparable quantity. Locations: L74, L76, L343, L385, L393.
- L343 carries the explicit disclosure: *"M1-level benchmark comparisons are not comparable across settings; cross-setting statements are therefore confined to the specification-matched estimand … which has the same meaning in both countries."*
- "Recent surveillance was a strong benchmark in both settings" (L343, L381) is a **within-setting** qualitative parallel (surveillance is hard to beat in each), not a cross-setting comparison of the non-comparable M1 baselines, and sits in the same paragraph as the disclosure. Reviewed → acceptable, no change.
No fixes required for 3a.

## 3b — Factual-precision correction (APPLIED; 3 edits)
Rationale: "same size / comparable size" overclaims — under the paper's advocated recalibration the SL matched increment is +0.015 vs Colombia +0.0078 (~2×). The consistent finding is *sign*, not *magnitude*.

| # | Loc | Before | After |
|---|---|---|---|
| 1 | Abstract (L74) | "a **similar** small climate increment" | "a small climate increment **of the same sign** … of uncertain magnitude **and not of established equal size** in both settings" |
| 2 | Discussion (L385a) | "small and **of comparable size** in Sri Lanka ($+0.0087$ matched)" | "small in Sri Lanka ($+0.0087$ matched, **of uncertain magnitude**)" |
| 3 | Discussion (L385b) | "a small climate increment **of comparable sign and size** in both settings (SL $+0.0087$, CO $+0.0078$)" | "a small, **consistently-signed** climate increment **of uncertain magnitude** in both settings (SL $+0.0087$ raw / $+0.015$ under past-only recalibration, CO $+0.0078$; **the magnitudes are not established to be equal**)" |

Passages already using the safe framing (L76 "consistently-signed", L343 "of uncertain magnitude") were left unchanged — they were already correct.

## 3c — Framing-honesty items — DRAFT ONLY, **PENDING AUTHOR APPROVAL** (not applied)
Provenance came back CONFIRMED, so the *ladder and structured M1* are defensibly design-locked. Two honesty tensions remain that provenance does **not** dissolve:

1. **Exploratory framing for the featured estimand.** The interpretable primary now featured, **M5 − M5_no-climate**, is NOT in the frozen pipeline (frozen columns: `p_M1, p_M4_hybrid, p_M5_hybrid_season_RDHS`; no no-climate model) and the spec designates M5 as "a sensitivity, not the primary." It is a valid but **revision-stage, post-hoc analytic decomposition**. *Proposed methods/limitations sentence (PENDING AUTHOR APPROVAL):* "The specification-matched climate estimand (M5 − M5_no-climate) was constructed during revision to isolate the incremental value of climate information; it was not part of the pre-registered ladder and is therefore exploratory / hypothesis-generating rather than confirmatory."

2. **Do not let 'design-locked primary' launder the demotion.** The spec's pre-specified primary new model was **M4** and its pre-specified contrast **M4 − M1**, which the paper now correctly demotes to a non-nested diagnostic. *Proposed limitations sentence (PENDING AUTHOR APPROVAL):* "The pre-specified primary contrast (M4 − M1) is non-nested and does not isolate climate; the interpretable climate estimand is post hoc. We therefore do not rest the climate claim on pre-registration of the primary contrast."

3. **Rule-9 coverage — VERIFIED.** The non-nested / "does not isolate climate" caveat is present at both interpretive loci (L349, L381). All other M4−M1 mentions are definitional ("planned/design-locked primary," accurate). *Optional (PENDING AUTHOR APPROVAL):* add a five-word non-nested flag to the abstract's SL M4−M1 sentence (L74) for symmetry with the Colombia decomposition; abstract brevity currently omits it.
