# Page-by-page visual QC — v12 (sensitivity integration)

**Method.** All 24 pages of the line-numbered review build were rendered at 100 dpi in color (Poppler `pdftoppm`) and every page visually inspected; the grayscale build was rendered and the three figure pages (Fig 1 pipeline p10, Fig 2 Sri Lanka DCA p11, Fig 3 Colombia p15) inspected for grayscale legibility. Text of every inserted/edited passage was additionally verified against the extracted PDF text (`pdftotext`). Build guards (fail-fast) reported 0 overfull/underfull boxes and 0 undefined citations/references across both builds.

## Overall verdict
Clean. 24 pages (up from 22 in v10 because of the added Colombia 2022-only paragraph, the Discussion M4/M5 additions, and two new SI items S11/S12). **0 overfull/underfull boxes, 0 undefined references/citations, 0 clipping/overflow, 0 broken figures, 0 literal [?].** Continuous line numbers present in the line-numbered build (1–590) and absent in the internal build; double spacing active in both prose builds; the "Internal review copy — not for submission" notice appears only in the title-page box and now points to `submission_blockers_v12.md`.

## Per-page notes (issues only; all other pages clean)
| Page | Content | Note | Severity |
|---|---|---|---|
| 1 | Title / authors / internal-review box | Title-page box + pending admin metadata (expected internal-review content); box now cites `submission_blockers_v12.md` | minor (expected) |
| 10 | Figure 1 (pipeline) | Node fills (blue/orange/green) flatten in grayscale; outlines + labels remain legible, meaning preserved | cosmetic (unchanged from v10) |
| 16 | Colombia robustness Results | New 2022-only paragraph typesets cleanly within margins; no overflow | none |
| 19–20 | Declarations / references start | "Pending author confirmation" declarations (administrative, expected) | minor (expected) |
| 23 | References tail ([34] doi + [35]) | Reference [35] and the tail of [34] sit on an otherwise sparse page; the SI `\clearpage` starts Supporting Information fresh on p24. Cosmetic references-continuation sparseness (same class as the v10 note); not an orphan/overflow defect | cosmetic |
| 24 | Supporting information (S1–S12) | S1–S12 captions present and correctly numbered; S9 caption now names the 2022-only subset; S11 Table and S12 Text added | none |

Pages with no issues: 2–9, 11–15, 17, 18, 21, 22 (and the substantive content pages 16, 24 above are clean apart from the expected/cosmetic notes).

## Grayscale
Figure 1 categorical node fills flatten (cosmetic; outlines/labels preserve meaning). Figure 2 (Sri Lanka DCA) remains legible in grayscale: distinct markers (circle/square/triangle/filled-circle/diamond/pentagon) and solid/dashed line styles distinguish the six series; M1 (darkest filled circles) is visibly highest across the mid-to-high range. Figure 3 (Colombia) uses a crosshatch pattern on the net-benefit bars and filled circular markers on the AUC panel, both legible in grayscale.

## Inserted/edited text verified in the compiled PDF
- Colombia 2022-only paragraph (+0.0150 [+0.0067,+0.0249] vs +0.0188; 4,802/274/48 weeks/2,202/0.4586; not pandemic-free) — present.
- Sri Lanka wild-cluster-bootstrap-t main-text sentence (26 RDHS clusters; intervals similar to percentile; SI S11/S12) — present; no p-values in Abstract or headline Results.
- Principal (planned primary) estimand now M4−M1 (NB_M4 − NB_M1); "the M5−M1 contrast is not the principal Sri Lanka estimand" — present.
- Signed canonical R-DLNM contrasts ΔAUC = −0.038 and ΔNB = −0.025 — present.
- Threshold-grid traceability-record reference removed from the body (0 occurrences).
- Discussion reports both M4 (planned primary) and M5 (expanded sensitivity), plus the "support rather than replace" interpretation sentence — present.
- OpenDengue reported at the acquisition-verified level ("Temporal extract version 1.3; the file recorded in the acquisition log") — present.
