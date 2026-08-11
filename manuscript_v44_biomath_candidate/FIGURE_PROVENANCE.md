# FIGURE_PROVENANCE

Status of the eight figures referenced by the candidate manuscript.

## Search performed (2026-08-10)
- `find ~ -type d -name submission_figs` → **none**.
- The referenced files (`submission_figs/Fig1.pdf, Fig4.pdf, Fig2.pdf, Fig1_pipeline.pdf, S1_Fig.pdf, S2_Fig.pdf, S3_Fig.pdf, S4_Fig.pdf`) are **gitignored** (`*.pdf` blocked) and are **not tracked on any branch** (checked `origin/main`, `origin/agent/v44-round4-geomatics-execution`, `origin/manuscript-v43-repair`).
- Other committed images exist but are **different figures**: `ALT_STATS/figures/FigureA_proper_score_forest.pdf`, `FigureB_calibration.pdf`, `FigureC_metric_summary.pdf`, and `Manuscript_Figures/study area maps/{SriLanka_Layout,Columbia_Layout1}.png`. These are **not** the manuscript's Fig1/Fig2/Fig4/S-figs and must **not** be substituted.
- Desktop `paper1_overleaf_bundle*` folders belong to a **different paper** (topological-index figures: octane heatmap, degeneracy bars) — not dengue.

## Per-figure status
| Figure | Source path | SHA256 | Source script | Regenerated? | Identical to prior submission figure? |
|---|---|---|---|---|---|
| Fig1 (study design) | `submission_figs/Fig1.pdf` | UNAVAILABLE | (author Overleaf) | No | NOT_VERIFIED (file absent) |
| Fig4 (SL matched DCA) | `submission_figs/Fig4.pdf` | UNAVAILABLE | (author Overleaf) | No | NOT_VERIFIED |
| Fig2 (CO ladder, S4 Fig) | `submission_figs/Fig2.pdf` | UNAVAILABLE | (author Overleaf) | No | NOT_VERIFIED |
| Fig1_pipeline (S6 Fig) | `submission_figs/Fig1_pipeline.pdf` | UNAVAILABLE | (author Overleaf) | No | NOT_VERIFIED |
| S1_Fig | `submission_figs/S1_Fig.pdf` | UNAVAILABLE | (author Overleaf) | No | NOT_VERIFIED |
| S2_Fig | `submission_figs/S2_Fig.pdf` | UNAVAILABLE | (author Overleaf) | No | NOT_VERIFIED |
| S3_Fig | `submission_figs/S3_Fig.pdf` | UNAVAILABLE | (author Overleaf) | No | NOT_VERIFIED |
| S4_Fig | `submission_figs/S4_Fig.pdf` | UNAVAILABLE | (author Overleaf) | No | NOT_VERIFIED |

## Decision
**`FIGURE_PROVENANCE = PASS_OR_EXPLICITLY_DOCUMENTED` (documented).** The frozen figure PDFs are not present on this machine and not recoverable from the repository. No figure was regenerated (regeneration would need the exact frozen scripts + inputs and risks altering results — out of scope for a formalization pass). The internal-review PDF therefore renders labeled placeholders via `\safeincludegraphics`; **no axis, label, threshold, color, panel, or result was altered**. To produce a submission render, the authors supply `submission_figs/` from their Overleaf/frozen bundle and recompile with `build.sh` — the placeholders resolve automatically. This is a review-only candidate, so missing frozen figures do **not** block the review-branch push, but they are a documented pre-submission item.
