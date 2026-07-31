# Final QC addendum — v17 (read-only completion)

Read-only final-QC completion. No manuscript TeX, bibliography, Supporting Information, PDF, analysis, or numerical result was created or modified in this pass (the only file created is this addendum). No rebuild was performed: all three PDFs were already present and non-corrupt (24 pages each).

## 1. Final PDF hashes and modification times
| PDF | SHA256 | bytes | mtime | pages |
|---|---|---|---|---|
| dengue_ews_v17_internal_author_review.pdf | `d87b18dba3121a026dba105452c72d0d8c9f8cebdadab677ffa756af501de702` | 416813 | 2026-07-01 19:19:48.609027388 -0400 | 24 |
| dengue_ews_v17_line_numbered_review.pdf | `910c3a3fb4e5c6d2005971e842ff51db1e1cd068a3bd7362909ebc4b04349930` | 435709 | 2026-07-01 19:20:03.521528953 -0400 | 24 |
| dengue_ews_v17_line_numbered_review_grayscale.pdf | `b5c00749faca3dfcca087fb8f8db166216ba7a59e82dcdc004f655932205789d` | 234375 | 2026-07-01 19:20:05.978611580 -0400 | 24 |

## 2. Rendering
Old temporary renders were deleted, and all three final PDFs above were re-rendered at 200 dpi. **All inspections in this addendum were performed from fresh renders generated from the final hashed PDFs listed in Section 1.** No pixel-identity claim is made from any single-page comparison; every reported page was opened and inspected directly.

## 3. Internal author-review PDF — all 24 pages inspected individually
For every page: content complete; **no line numbers present** (internal build); no clipping or margin overflow; tables and figures readable; captions and footnotes correctly placed; expected administrative wording present where applicable.

| Page | Content | Line numbers absent | Clipping/overflow | Tables/figures | Captions/footnotes | Admin wording | Result |
|---|---|---|---|---|---|---|---|
| 1 | Title/authors/internal-review notice | yes (none) | none | n/a | n/a | internal-review box (submission_blockers_v17.md) | PASS |
| 2 | Abstract + Author Summary start | yes | none | n/a | n/a | none | PASS |
| 3 | Author Summary + Introduction | yes | none | n/a | n/a | none | PASS |
| 4 | Introduction / Methods 2.1 | yes | none | n/a | n/a | none | PASS |
| 5 | Methods 2.2–2.3 (OpenDengue V1.3) | yes | none | n/a | n/a | none | PASS |
| 6 | Methods 2.4–2.6 | yes | none | n/a | population formula | none | PASS |
| 7 | Methods 2.6–2.7 | yes | none | n/a | n/a | none | PASS |
| 8 | Methods 2.8 (DCA equation)–2.9 | yes | none | n/a | equation clean | none | PASS |
| 9 | Methods 2.9 tail (seed; estimand) | yes | none | n/a | n/a | none | PASS |
| 10 | Figure 1 (pipeline) + cohort | yes | none | Fig 1 readable | caption below | none | PASS |
| 11 | Tables 1–2 + Figure 2 (DCA) | yes | none | rules crisp; Fig 2 legible | below | none | PASS |
| 12 | Table 3 + 3.4 hybrid (signed R-DLNM) | yes | none | rules crisp | above table | none | PASS |
| 13 | Table 4 + hybrid/WCB-t pointer | yes | none | rules crisp | above table | none | PASS |
| 14 | Colombia + Table 5 | yes | none | rules crisp | above table | none | PASS |
| 15 | Figure 3 (Colombia) + 3.6 Horizon | yes | none | markers/crosshatch legible | below panels | none | PASS |
| 16 | 3.7 Threshold + Colombia 2022 paragraph | yes | none | n/a | n/a | none | PASS |
| 17 | Cross-setting synthesis + Table 6 | yes | none | rules crisp | descriptive title | none | PASS |
| 18 | Discussion (M4/M5 estimates; WCB-t concordant; cross-setting) | yes | none | n/a | n/a | none | PASS |
| 19 | Limitations (elevated-activity; ~23.5%) | yes | none | n/a | n/a | none | PASS |
| 20 | Future-work + Declarations start | yes | none | n/a | n/a | "Pending author confirmation" (expected) | PASS |
| 21 | Author contributions/Acknowledgments + AI-use + References [1]–[11] | yes | none | n/a | n/a | pending items (expected) | PASS |
| 22 | References [12]–[30] | yes | none | n/a | n/a | none | PASS |
| 23 | References [31]–[35] | yes | none | n/a | n/a | none | PASS |
| 24 | Supporting information S1–S12 | yes | none | n/a | n/a | draft-status note (expected) | PASS |

Internal build: **24/24 PASS.** No line numbers on any page; no defects.

## 4. Line-numbered and grayscale builds — records tied to the final hashes
Both the line-numbered build and the grayscale line-numbered build were re-rendered from the final hashed PDFs (Section 1) and all 24 pages of each were opened and inspected in this pass.
- **Line-numbered build: 24/24 PASS.** Continuous line numbers on every page; no collisions with text, tables, or the decision-curve equation; content matches the internal build; all v17 wording edits present (cross-setting §2 p17; Discussion §3/§4/§5 p18; limitations §7 p19; future-work §6 p20).
- **Grayscale build: 24/24 PASS.** Every page legible; tables use booktabs rules with no shading and reproduce exactly; Figures 1–3 legible via redundant non-colour encodings (flow-diagram outlines/labels; distinct markers and solid/dashed lines; filled markers and crosshatch bars).

## 5. Totals and defects
- Internal author-review: **24/24 inspected.**
- Line-numbered review: **24/24 inspected.**
- Grayscale line-numbered review: **24/24 inspected.**
- **Total: 72/72 page inspections.**
- **Defects found: none.** 0 clipping/overflow, 0 line-number collisions, 0 unreadable tables/figures, 0 misplaced captions/footnotes, 0 unexpected administrative wording.

## 6. Change confirmation
No manuscript TeX, bibliography, Supporting Information, PDF, analysis, or frozen/numerical result was created or modified in this read-only pass (only this addendum file was created). No revision was created; no rebuild was performed. Revisions v1–v16 and the authorized-sensitivity workspace are unchanged.
