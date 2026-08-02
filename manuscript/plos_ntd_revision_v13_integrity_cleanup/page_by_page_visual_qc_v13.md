# Page-by-page visual QC — v13 (integrity cleanup)

**Method.** All 23 pages of each of the three PDFs — internal author-review (line numbers off), line-numbered review (line numbers on), and grayscale line-numbered — were rendered at **200 dpi** (Poppler `pdftoppm`) and inspected. Every page was checked, not only figure pages. Build guards (fail-fast) reported 0 overfull/underfull boxes and 0 undefined citations/references for both LaTeX builds.

**Overall verdict.** Clean. **24 pages** in the final build. (An intermediate build before the post-review fixes was 23 pages; adding a two-line clarifying note to the Colombia Table~5 caption — see the addendum below — returned the document to 24 pages, shifting content from the Colombia table page onward by at most one page.) 0 clipping/overflow, 0 line-number collisions, 0 unreadable tables/figures, 0 misplaced captions, 0 undefined references, 0 literal `[?]`, 0 literal placeholder tokens. Continuous line numbers present in the line-numbered build and absent in the internal build; double spacing active in both prose builds. Figures are legible in grayscale.

**Post-harsh-review fixes (re-rendered and re-inspected; all clean).** After a multi-agent field-expert + harsh-peer-review pass (GO, 0 blockers), three presentation/consistency items were corrected and the affected pages re-inspected: (1) the Abstract (p2) now names Colombia's figure as the M5−M1 estimate (+0.0188) instead of "the corresponding estimate," removing a model-tier conflation with Sri Lanka's M4−M1; (2) the Colombia primary Table~5 caption (Colombia results page) now states that all six ladder models are shown for completeness and that the reported primary Colombia contrast is M5−M1 with the M4−M1 contrast in S9, resolving an orphaned M4 row; (3) the Sri Lanka wild-bootstrap full-precision bounds were removed from S11 and S12 text so they are preserved only in the machine-readable CSV (removing an internal self-contradiction). The per-page table below reflects the page content and is unchanged in substance; only pagination from the Colombia table page onward shifts by at most one page.

| Page | Content | Clipping | Line-number collision | Table/figure readability | Caption placement | Grayscale | Admin placeholders | Action |
|---|---|---|---|---|---|---|---|---|
| 1 | Title, authors, corrected internal-review box | none | none | n/a | n/a | text only, legible | Internal-review box (expected); cites `submission_blockers_v13.md` | none |
| 2 | Abstract (271 words) | none | none | n/a | n/a | text only | none | none |
| 3 | Author Summary (191 words) + Introduction | none | none | n/a | n/a | text only | none | none |
| 4 | Introduction | none | none | n/a | n/a | text only | none | none |
| 5 | Methods 2.2–2.3 (OpenDengue version corrected) | none | none | n/a | n/a | text only | none | none |
| 6 | Methods 2.4–2.6 | none | none | n/a | n/a | text only | none | none |
| 7 | Methods 2.7 calibration | none | none | n/a | n/a | text only | none | none |
| 8 | Methods 2.8–2.9 (DCA eqn; uncertainty) | none | none | equation clean | n/a | text only | none | none |
| 9 | Methods 2.9 tail (corrected M4/M5 estimand + seed 20260612) | none | none | n/a | n/a | text only | none | none |
| 10 | Figure 1 (pipeline) + Table 1 | none | none | readable | below/above content | fills flatten; outlines + labels + arrows legible | none | none (cosmetic, meaning preserved) |
| 11 | Table 2 + Figure 2 (Sri Lanka DCA) | none | none | readable | below plot | 6 series distinguishable by marker + line style | none | none |
| 12 | Table 3 (recalibration) + 3.4 hybrid (signed R-DLNM) | none | none | readable | above table | text/table legible | none | none |
| 13 | Table 4 + M5−M1 result + wild-bootstrap sentence | none | none | readable | above table | legible | none | none |
| 14 | Colombia replication + Table 5 | none | none | readable | above table | legible | none | none |
| 15 | Figure 3 (Colombia AUC + NB) + 3.6 Horizon | none | none | readable | below panels | crosshatch bars + filled markers legible | none | none |
| 16 | 3.7 Threshold/stricter-outcome + Colombia 2022-only paragraph (corrected 48-week explanation) | none | none | n/a | n/a | text only | none | none |
| 17 | Cross-setting synthesis + Table 6 (corrected title) | none | none | readable | above table | legible | none | none |
| 18 | Discussion (M4/M5; no Colombia M4; no zero-crossing verdict) | none | none | n/a | n/a | text only | none | none |
| 19 | Discussion/Limitations (2022-subset limitation) | none | none | n/a | n/a | text only | none | none |
| 20 | Declarations (Ethics/Funding/COI/… pending) + AI-use statement | none | none | n/a | n/a | text only | "Pending author confirmation" (expected) | none |
| 21 | References [1]–[16] | none | none | n/a | n/a | text only | none | none |
| 22 | References [17]–[35] | none | none | n/a | n/a | text only | none | none |
| 23 | Supporting information S1–S12 | none | none | n/a | n/a | text only | draft-status note (expected) | none |

**Notes.**
- The v12 sparse references-continuation page is resolved: references now end on p22 and the Supporting Information fills p23.
- Grayscale differs from color only on the three figure pages (10, 11, 15); all other pages are black text on white and are identical in grayscale. Figure 1's categorical node fills flatten to gray (cosmetic; outlines and labels preserve meaning) — the only grayscale-specific note, unchanged from prior audits.
- The internal author-review build was confirmed to carry no line numbers; content is identical to the line-numbered build.
