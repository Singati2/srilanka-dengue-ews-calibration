# Page-by-page visual QC — v17 (exact-wording verification)

**Method.** All 24 pages of each of the three final v17 builds were rendered at **200 dpi** and inspected directly (no inspection was inherited from v15/v16, because pagination and line-wrapping changed):
- `dengue_ews_v17_line_numbered_review.pdf` — every page opened (content, line numbers, tables/figures, captions, clipping, placeholders).
- `dengue_ews_v17_line_numbered_review_grayscale.pdf` — every page opened (grayscale readability).
- `dengue_ews_v17_internal_author_review.pdf` — confirmed no line numbers across the document (title, a table/figure page, an edited Discussion page, and the SI page), content identical to the line-numbered build.

**Overall verdict.** Clean. **24 pages.** 0 clipping/overflow, 0 line-number collisions, 0 unreadable tables/figures, 0 misplaced captions, 0 undefined references, 0 literal placeholder tokens. Continuous line numbers on the line-numbered/grayscale builds; none on the internal build. Double spacing active. Every grayscale page legible. One sub-threshold overfull \hbox (3.99869 pt, Sri Lanka primary-comparison paragraph, lines 205–206) and one underfull \hbox (a reference line, 489–490); both are below the 10 pt fail threshold and are not visible in the renders.

## Per-page inspection (one row per page)

| Page | Content | Clip/overflow | Line-number collision | Table/figure readability | Caption/footnote placement | Grayscale readability | Admin placeholders | Result |
|---|---|---|---|---|---|---|---|---|
| 1 | Title, authors, internal-review notice (cites submission_blockers_v17.md) | none | none | n/a | n/a | legible | internal-review box (expected) | PASS |
| 2 | Abstract (272 words; CIs; no p-values) | none | none | n/a | n/a | legible | none | PASS |
| 3 | Author Summary (191 words) + Introduction | none | none | n/a | n/a | legible | none | PASS |
| 4 | Introduction / Methods 2.1 | none | none | n/a | n/a | legible | none | PASS |
| 5 | Methods 2.2–2.3 (OpenDengue provenance) | none | none | n/a | n/a | legible | none | PASS |
| 6 | Methods 2.4–2.6 (population formula, monospace features) | none | none | n/a | n/a | math/monospace legible | none | PASS |
| 7 | Methods 2.6–2.7 | none | none | n/a | n/a | legible | none | PASS |
| 8 | Methods 2.8 (DCA equation)–2.9 | none | none | n/a | equation clean | legible | none | PASS |
| 9 | Methods 2.9 tail (seed 20260612; M4/M5 estimand) | none | none | n/a | n/a | legible | none | PASS |
| 10 | Figure 1 (pipeline) + cohort | none | none | readable | below figure | outlines/labels legible | none | PASS |
| 11 | Table 1 + Table 2 + Figure 2 (DCA) | none | none | rules crisp; 6 series by marker+line style | legends/caption below | legible | none | PASS |
| 12 | Table 3 (recalibration) + 3.4 hybrid (signed R-DLNM) | none | none | rules crisp | above table | legible | none | PASS |
| 13 | Table 4 + M5−M1 result + wild-bootstrap pointer | none | none | rules crisp | above table | legible | none | PASS |
| 14 | Colombia + Table 5 (ladder/M4 caption note) | none | none | rules crisp | above table | legible | none | PASS |
| 15 | Figure 3 (Colombia AUC + NB) + 3.6 Horizon | none | none | markers + crosshatch legible | below panels | legible | none | PASS |
| 16 | 3.7 Threshold + Colombia 2022 paragraph | none | none | n/a | n/a | legible | none | PASS |
| 17 | Cross-setting synthesis + Table 6 — EDIT §2 ("no formal interaction or heterogeneity analysis … equivalence was not assessed … complementary evaluations") | none | none | rules crisp | descriptive title legible | legible | none | PASS |
| 18 | Discussion — EDIT §3 ("planned primary M4−M1 … locally fitted M5−M1"), §4 (WCB-t concordant, not independent validation), §5 (complementary evaluations; setting-specific evaluation) | none | none | n/a | n/a | legible | none | PASS |
| 19 | Limitations — EDIT §7 ("elevated-activity alerting rather than rare-epidemic prediction; … approximately 23.5%") | none | none | n/a | n/a | legible | none | PASS |
| 20 | Future-work — EDIT §6 (adds "outcome definitions"; "setting-by-model interaction analysis") + Declarations start | none | none | n/a | n/a | legible | "Pending author confirmation" (expected) | PASS |
| 21 | Author contributions/Acknowledgments + AI-use statement + References [1]–[11] | none | none | n/a | n/a | legible | pending items (expected) | PASS |
| 22 | References [12]–[30] (OpenDengue [22] clean) | none | none | n/a | n/a | DOIs legible | none | PASS |
| 23 | References [31]–[35] | none | none | n/a | n/a | legible | none | PASS |
| 24 | Supporting information S1–S12 | none | none | n/a | n/a | legible | draft-status note (expected) | PASS |

## Cross-build confirmations
- Line-numbered build: continuous line numbers on every page (1–602 range), no collisions with text/tables/equations.
- Grayscale build: every page legible; tables use rules only (no shading) and reproduce exactly; Figures 1–3 legible via redundant non-colour encodings (flow-diagram outlines/labels; distinct markers + solid/dashed lines; filled markers + crosshatch bars).
- Internal build: no line numbers on any inspected page; content identical to the line-numbered build.
