# Page-by-page visual QC — v10 (full, both PDFs, color + grayscale)

**Method.** Every page of both review PDFs was rendered and **visually inspected** (not inferred): internal copy color at 200 dpi (Poppler `pdftoppm`), line-numbered copy color at 150 dpi, line-numbered grayscale at 150 dpi. PDFium CLI was not available on this system; Poppler (`pdftoppm`/`pdftocairo`) was used. A 5-agent panel inspected page batches; a separate harsh final read cross-checked numbers, labels, and wording. Initial inspection was on the 23-page build; after the references-page fix below the document is **22 pages** (per-page content unchanged; only the last reference and the SI page moved up).

## Overall verdict
Clean. **0 clipping/overflow, 0 line-number collisions, 0 broken orphans/widows, 0 undefined references, 0 mislabeled/truncated figures.** Line numbers are continuous in the line-numbered build and absent in the internal build (as intended); grayscale is legible on every page. The "Internal review copy — not for submission" notice appears **only** in the title-page box (not repeated per page); the running header is the normal short title.

## Harsh final read — no red flags
- M4/M5 labeling consistent everywhere (M4 = planned primary hybrid; M5 = pre-computation expanded-sensitivity hybrid) — Methods, Results, Tables 4/5/6, SI.
- Numbers reconcile across Abstract/body/tables: SL ΔNB(M4−M1) −0.008 [−0.028,+0.013]; SL ΔNB(M5−M1) +0.0081 [−0.0012,+0.0181]; Colombia ΔNB(M5−M1) +0.0188 [+0.0117,+0.0260]; Colombia ΔAUC +0.040 (= Table 5 M5−M1 0.726−0.685≈0.041). Table 1 vs Table 2 NB₀.₃₀ agree (M0 0.084/M1 0.137/M2 0.069/M3 0.078).
- Net-benefit equation (p8) consistent with the 0.429 / 2.33 interpretation; line numbers do not collide with the display equation.
- Figure 3 (p15): both panels correctly labeled (dot-plot AUC with no-skill line at 0.5; zero-based net benefit with alert-all≈0.107); no truncation/mislabel.
- No "post-hoc/steelman/confirmatory/registered" or significance-dichotomized wording; hedging appropriate ("exploratory/hypothesis-generating", "no prospective public registration is claimed", pointwise/multiplicity-unadjusted intervals).

## Per-page summary (issues only; all other pages clean)
| Page | Section | Line# | Issue | Severity | Action |
|---|---|---|---|---|---|
| 1 | Title / three-author block | continuous | Title-page "not for submission" box + pending admin metadata | minor (expected) | Expected internal-review content; tracked in `submission_blockers_v10.md`/`authorship_confirmation_v10.md` |
| 10 | Figure 1 (pipeline) + Table 1 | continuous | Figure 1 node fills (blue/orange/green) flatten in grayscale; outlines + labels remain legible so meaning preserved | cosmetic | Acknowledged; the caption no longer claims a redundant grayscale encoding (corrected earlier), so no false claim. Optional future: add shape/border cues. |
| ~19 | End of Discussion + Declarations | continuous | Declarations read "Pending author confirmation" (ethics, funding, COI, contributions, data/code, acknowledgments) | minor (expected) | Administrative, not a typesetting defect; tracked as submission blockers |
| (was 22) | References continuation | continuous | Reference [35] was alone on a ~95% empty page | cosmetic | **Fixed**: tightened bibliography `\itemsep`/`\parskip` → [35] now on p21; document is 22 pp; no near-empty page |
| 22 | Supporting information (S1–S10) | continuous | S1–S3 "draft", S10 "partial", items "not submission-final" | administrative (expected; the agent rated it "major") | Correctly disclosed draft status; these are **submission blockers**, not typesetting errors; page is well-filled (21 lines), not an orphan |

Pages with no issues: 2,3,4,5,6,7,8,9,11,12,13,14,15,16,17,18,20,21 (and post-fix 22 SI page is clean).

## Line-number / spacing / grayscale status
- Continuous line numbers verified in the line-numbered build (e.g., title page 1–11; no restart per page); absent in the internal build (author standing preference).
- Double spacing active in both prose builds.
- Grayscale: every page legible; only Figure 1's categorical fills lose color separation (cosmetic, meaning preserved).
- Final page (22, SI) is a proper page, not a near-empty continuation.
