# Visual style guide v1 (colorblind-safe; grayscale-legible)

## Palette (Okabe–Ito; defined in the .tex preamble)
| Role | Color | RGB |
|---|---|---|
| Data sources | okBlue | 0,114,178 |
| Preprocessing | okOrange | 230,159,0 |
| Integrated analytic table | okGray | 120,120,120 |
| Model families | okGreen | 0,158,115 |
| Evaluation | okPurple | 204,121,167 |
| Synthesis/output | okVermillion | 213,94,0 |
| (reserve) | okSky / okYellow | 86,180,233 / 240,228,66 |

## Rules
- **No red–green-only distinctions.** Encode every series by **color + line style + marker shape** (redundant encoding) so it reads in grayscale.
- **Consistent model-family encoding across all figures:** M0 = orange/triangle; M1 = blue/filled-circle (thickest); M2 = green/diamond; M3 = purple/pentagon; M5 = vermillion/square. Alert-all = gray/open-circle; alert-none = black/square.
- Flowchart uses category fills (table above) and **no decorative causal arrows** — arrows denote data flow only.
- Minimum readable font: figure body text ≥ \footnotesize at final size; axis labels ≥ \small.
- **All quantitative figures generated only from frozen result tables** (TikZ/pgfplots coordinates transcribed from `docs/*_report.md`); **no screenshot-derived numeric plots**.
- Editable source for every figure: native TikZ/pgfplots in the `.tex` (and standalone copies in `figures/`).
- Check each figure in **color and grayscale** before submission.
