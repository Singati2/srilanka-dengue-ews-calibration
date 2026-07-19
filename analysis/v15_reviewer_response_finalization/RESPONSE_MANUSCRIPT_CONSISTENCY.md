# Task 3 — Response ↔ manuscript ↔ abstract consistency cross-check

Manuscript = `paper1_plos_gph_C2_final.tex` (rebuilt, 40 pp, 0 undefined/errors). All values agree to the digit.

| Quantity | Abstract | Results | Discussion | Reviewer response v2 | Consistent? |
|---|---|---|---|---|---|
| SL matched raw ΔNB(M5−M5_no-climate) | +0.0087 (CI incl. 0) | +0.0087 [−0.0015,+0.0188] | +0.0087 (incl. 0) | +0.0087 | ✅ |
| **SL matched RECALIBRATED** recal(M5)−recal(M5_no-climate) | +0.0157 [+0.0066,+0.0257] (excl. 0) | +0.0157 [+0.0066,+0.0257] | +0.0157 | +0.0157 [+0.0066,+0.0257] | ✅ |
| SL frozen M5−M1 recal (operational sensitivity, NOT matched) | not in abstract | +0.0154 (labeled operational sensitivity) / M5−M1 +0.008→+0.015 | — | labeled operational sensitivity | ✅ |
| SL M4−M1 (secondary, non-nested) | −0.008 → +0.009/+0.010 | −0.008 raw → +0.010 [−0.011,+0.030] | −0.008 | −0.008 → +0.010 | ✅ |
| CO matched | +0.0078 [+0.0039,+0.0119] | +0.0078 | +0.0078 | +0.0078 | ✅ |
| Cross-setting magnitude | "consistently-signed … not equal size" | — | "magnitudes not established equal" | "same sign, not magnitude" | ✅ |

Checks:
- "matched" is never attached to M5−M1 or M4−M1 (grep clean; both explicitly non-matched / non-nested).
- No "same/similar/comparable/equivalent magnitude" phrasing remains (grep = 0).
- No "matched recalibrated value was not computed" text remains (grep = 0) — replaced by the computed +0.0157.
- The only remaining "+0.015" strings are Colombia's horizon M5−M1 profile and the frozen SL M5−M1 operational sensitivity, both explicitly labeled M5−M1.

**Status: response, abstract, results, and discussion are numerically identical. No estimand mixing.**
