# FIGURE_TABLE_PLAN — main vs supporting (Phase 6)

PLOS has no hard figure limit, but a concise 4–6 main-figure set reads better. Current: 9 figures.

## Recommended MAIN figures (5)
| Fig | Content | Keep as main? | Why |
|---|---|---|---|
| Fig1 | Study/pipeline schematic | Main | Orients the two-country evaluation design |
| Fig3 | Colombia AUC / net benefit | Main | Core decision-analytic result, secondary setting |
| Fig4 | Sri Lanka calibration (raw vs recalibrated) | Main | Central to the calibration-dependence message |
| Fig5 | Sri Lanka decision curves | Main | The primary decision-analytic display (SL) |
| Fig8 | Colombia matched-decomposition forest | Main | Shows matched vs unmatched contrasts and dev-inclusive CI |

## Recommended SUPPORTING figures (move 4 → S_ Figs)
| Fig | Content | Move to | Why |
|---|---|---|---|
| Fig2 | SL threshold curves (4-point series) | S1 Fig | Sparse; threshold sensitivity is secondary; also improve density |
| Fig6 | Colombia completeness/selection | S2 Fig | Selection diagnostic |
| Fig7 | Colombia calibration + dense DCA | S3 Fig | Diagnostic; overlaps Fig3 message |
| Fig9 | Colombia matched increment vs horizon | S4 Fig | Horizon sensitivity is secondary |

## Tables
- Keep MAIN: model specification / analysis-status table; Sri Lanka primary metrics; Colombia matched-decomposition table.
- Move to SI: full per-model metric tables, threshold grids, bootstrap details, provenance.

**Note:** moving figures is a recommendation only — not yet applied to the .tex (the current file keeps all 9 inline). If you approve, I will renumber to the reduced main set + S_ Figs and regenerate. No result needed to understand prespecified-vs-post-hoc, matched-vs-unmatched, raw-vs-recalibrated, or uncertainty is removed by this plan.

---

## APPLIED (in paper1_plos_gph_submission_ready.tex, rebuilt 39 pp, 0 undefined/errors)
Reduced to **5 main figures**; 4 moved to Supporting Information. Files in `manuscript/.../submission_figs/` (PLOS names).

| Main file | Content | Was |
|---|---|---|
| Fig1.pdf | Pipeline schematic | Fig1 |
| Fig2.pdf | Colombia AUC / net benefit | Fig3 |
| Fig3.pdf | Sri Lanka calibration (raw vs recalibrated) | Fig4 |
| Fig4.pdf | Sri Lanka decision curves | Fig5 |
| Fig5.pdf | Colombia matched-decomposition forest | Fig8 |

| SI file | Content | In-text ref | Was |
|---|---|---|---|
| S1_Fig.pdf | Sri Lanka threshold curves | "S1 Fig" | Fig2 |
| S2_Fig.pdf | Colombia data completeness | "S2 Fig" | Fig6 |
| S3_Fig.pdf | Colombia calibration + dense decision curves | "S3 Fig" | Fig7 |
| S4_Fig.pdf | Colombia matched increment vs horizon | "S4 Fig" | Fig9 |

**Numbering note:** the SI figures continue the manuscript's existing S1–S14 sequence (hence S15–S18 Fig), avoiding a collision with the existing S1 Checklist / S2 Checklist / S3 Table / S4 Text etc. If you prefer the figures to be S1–S4 Fig, the whole SI list (and its in-text S-refs) would need renumbering — say the word and I'll do it.
