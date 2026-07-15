# CONSISTENCY_CROSSCHECK — v17 development-inclusive

Manuscript `paper1_plos_gph_v17_devinclusive_final.tex` (40 pp, exit 0, 0 undefined, 0 errors). All values identical across abstract, results, discussion, Table 1, and the new Sri Lanka matched table.

| Quantity | Value | Abstract | Results | Discussion/cross-tier | SL matched table |
|---|---|---|---|---|---|
| SL raw matched | +0.0087 | ✓ | ✓ | ✓ | ✓ |
| SL raw matched, **conditional** CI | −0.0015,+0.0188 | ✓ | ✓ | — | ✓ |
| SL raw matched, **development-inclusive** CI | −0.0074,+0.0223 | (implied "included zero throughout") | ✓ | — | ✓ |
| SL **recalibrated** matched | +0.0157 | ✓ | ✓ | ✓ | ✓ |
| SL recal matched, **conditional** CI | +0.0066,+0.0257 | ✓ | ✓ | ✓ | ✓ |
| SL recal matched, **development-inclusive** CI | +0.0015,+0.0284 | ✓ (5 loci total) | ✓ | ✓ | ✓ |
| CO matched, conditional / dev-inclusive | +0.0078 / [−0.0001,+0.0244] | ✓ | ✓ | ✓ | — |
| Structure (matched−cases) | +0.0462 [+0.0199,+0.0741] | — | ✓ | ✓ | ✓ |

Framing checks:
- **Symmetric-and-correct evidence tier:** SL recalibrated exclusion **survives** development-inclusive uncertainty (marginally); Colombia's does **not**; raw excludes zero in neither. The stale v16 claim "under development-inclusive uncertainty, neither setting shows a robust exclusion" is **removed** (grep = 0), replaced by the corrected cross-tier statement.
- "raw-scale calibration (Sri Lanka)" weaker-caveat substitute **removed** (grep = 0); Sri Lanka now carries the same model-development caveat as Colombia.
- No "excludes zero" headline rests on conditional-only for Sri Lanka (the dev-inclusive interval is reported in parallel everywhere).
- Abstract 397 words (≤500). No matched/unmatched mixing; M5−M1 still "not specification-matched"; post-hoc labels intact.
- Recalibration statement scoped (C1): "not recalibrated in the original frozen analysis … addressed by the post-hoc recalibration."

**PASS.**
