# FIGURE_TABLE_AUDIT — v16

| Item | Content | Matched label correct? | +0.0154 shown as matched? | Notes |
|---|---|---|---|---|
| Table (analysis status) | lists SL M4−M1 (planned primary), SL M5−M1 (sensitivity), SL M5−M5_no-climate (post hoc matched), CO M5−M1, CO matched | ✅ SL & CO matched rows are M5−M5_no-climate | no | correct |
| Table (contrast questions, CO) | M4−M1, Matched−M1, M5−Matched, M5−M1 | ✅ "Matched" = M5_no-climate | no | correct |
| Table (matcheddecomp, CO) | CO decomposition numbers | ✅ | no | +0.0078 matched |
| Fig 2 (SL thresholds) | pgfplots NB vs threshold | n/a | no | 4-point series (noted as presentation limitation in verdict) |
| Fig 4/5 (SL calibration/DCA) | M1,M4,M5 raw vs recal | n/a (no matched label) | no | SL recal matched +0.0157 is text-only; no figure mislabels it |
| Fig 7 (CO calibration/DCA) | includes "structure-matched no-climate model" | ✅ | no | correct |
| Fig 8 (CO forest) | paired contrasts incl. M5−matched | ✅ | no | development-inclusive CI (incl. 0) shown for climate-specific |
| Fig 9 (CO horizon) | matched increment vs horizon | ✅ M5−M5_no-climate | no | correct |

- No figure calls M5−M1 "matched"; no caption presents +0.0154 as the matched recalibrated result.
- The recalibrated matched value +0.0157 appears in text only; raw and recalibrated states are separated; the finite-cluster/conditional caveat is in the text where the exclusion is claimed.
- No axis manipulation to exaggerate the small NB difference (decision curves use full grid with cluster-bootstrap bands).
- **Recommendation (author-action):** Fig 2 (SL) is a 4-point line series; consider a denser SL decision curve for readability. Not a validity issue.
