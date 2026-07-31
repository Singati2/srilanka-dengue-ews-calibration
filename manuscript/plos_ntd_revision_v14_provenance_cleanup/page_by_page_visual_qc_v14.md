# Page-by-page visual QC — v14 (provenance cleanup)

**Method.** All 23 pages of each of the three final v14 PDFs — internal author-review (line numbers off), line-numbered review (line numbers on), and grayscale line-numbered — were rendered at **200 dpi** (Poppler `pdftoppm`) and inspected. Every page was inspected, not only figure pages. Build guards (fail-fast) reported 0 undefined citations/references and no overfull hbox ≥10 pt for both LaTeX builds.

**Overall verdict.** Clean. **23 pages.** 0 clipping/overflow, 0 line-number collisions, 0 unreadable tables/figures, 0 misplaced captions, 0 undefined references, 0 literal `[?]`, 0 literal placeholder tokens. One sub-threshold typographic overfull hbox (3.99 pt, in the Sri Lanka primary-comparison paragraph) and one underfull hbox (a reference line) — neither is visible and both are below the build's 10 pt fail threshold; page renders show no margin overflow. Continuous line numbers present in the line-numbered build and absent in the internal build; double spacing active in both prose builds. Figures are legible in grayscale.

| Page | Content inspected | Result |
|---|---|---|
| 1 | Title, authors, internal-review box (cites `submission_blockers_v14.md`) | clean; box is expected internal-review content |
| 2 | Abstract (272 words; no p-values; Colombia figure named as M5−M1) | clean |
| 3 | Author Summary (191 words) + Introduction | clean |
| 4 | Introduction / Methods 2.1 | clean |
| 5 | Methods 2.2–2.3 — OpenDengue provenance (locally analyzed file, verified V1.3, generic DOI, pending reconciliation/acquisition date) | clean; §2 distinction present |
| 6 | Methods 2.4–2.6 | clean |
| 7 | Methods 2.7 calibration | clean |
| 8 | Methods 2.8 (DCA equation) – 2.9 | clean; equation renders correctly |
| 9 | Methods 2.9 tail — corrected M4/M5 estimand + targeted-value seed 20260612 | clean |
| 10 | Figure 1 (pipeline) + cohort text | clean; grayscale outlines/labels legible |
| 11 | Table 1 + Table 2 + Figure 2 (Sri Lanka DCA) | clean; 6 series distinguishable in grayscale |
| 12 | Table 3 (recalibration) + 3.4 hybrid (signed R-DLNM) | clean |
| 13 | Table 4 + M5−M1 result + wild-bootstrap sentence + Colombia start | clean |
| 14 | Colombia + Table 5 (caption: ladder shown for completeness; primary contrast M5−M1; M4−M1 in S9) | clean |
| 15 | Figure 3 (Colombia AUC + NB) + 3.6 Horizon | clean; crosshatch + markers legible in grayscale |
| 16 | 3.7 Threshold/stricter-outcome + Colombia 2022-only paragraph (origin/target 48-week explanation) | clean |
| 17 | Cross-setting synthesis + Table 6 (corrected descriptive title) | clean |
| 18 | Discussion — Sri Lanka estimate-only wording (M4−M1 point estimate −0.008; M5−M1 +0.0081 with substantial uncertainty; no verdict) | clean |
| 19 | Discussion / Limitations | clean |
| 20 | Declarations — Data & code availability carries OpenDengue version/DOI distinction; AI-use statement (no agent count/panel claim) | clean; "Pending author confirmation" items expected |
| 21 | References [1]–[16] | clean |
| 22 | References [17]–[35] — OpenDengue [22] has no internal filename | clean |
| 23 | Supporting information S1–S12 (cites `submission_blockers_v14.md`) | clean |

**Notes.**
- Grayscale differs from color only on the three figure pages (10, 11, 15); all other pages are black text on white and are identical in grayscale. Figure 1's categorical node fills flatten to gray (cosmetic; outlines and labels preserve meaning) — the only grayscale-specific note, unchanged from prior revisions.
- The internal author-review build carries no line numbers; content is identical to the line-numbered build.
- The review that preceded these v14 edits was an internal AI-assisted role-based adversarial review, not external human peer review or independent expert validation (see `sensitivity_review_provenance_v14.md`).
