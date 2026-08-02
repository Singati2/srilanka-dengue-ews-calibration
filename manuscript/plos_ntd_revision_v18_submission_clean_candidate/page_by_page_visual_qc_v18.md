# Page-by-page visual QC — v18

> **Candidate-completion update.** After the candidate-completion pass (Author Summary replaced
> with the 186-word version; Supporting-Information opener changed to "are planned to accompany";
> documentation/gate corrections), both PDFs were **rebuilt and re-rendered at 200 dpi** to
> `/tmp/v18qc3/`. The shorter Author Summary reflowed page breaks, so **pages 2–24 all changed**
> versus the pre-correction render (only page 1, the title page, was unchanged). Every changed page
> was re-inspected directly; all render cleanly (no clipping, overflow, broken glyphs, orphan
> fragments, internal filenames, or false-completion claims). The internal-vs-clean pixel-identity
> still holds: pages 2–24 are identical between the two builds; only page 1 differs (gated notice).
> The build-check summary table at the end reflects the post-correction state (Author Summary now
> 186 words — within the PLOS 150–200 limit; the earlier overage flag is resolved).

Both final PDFs were rendered at 200 dpi (`pdftoppm -r 200`) to `/tmp/v18qc/{clean,internal}/`.
Every page was visually inspected. Reduced-size viewing copies (~1061×1500 px) were used for the
image reads because the many-image request path rejects renders whose larger dimension exceeds
2000 px; the 200 dpi masters were retained and the reduced copies preserve all glyphs and layout.

**Pixel-identity finding.** `cmp` on the 200 dpi renders shows pages **2–24 are byte-for-byte
pixel-identical** between `dengue_ews_v18_internal_author_completion.pdf` and
`dengue_ews_v18_scientifically_clean_not_submission_ready.pdf`. The two builds differ **only on
page 1** (the gated first-page notice). Internal-build pages 2–24 were therefore verified by
pixel-identity to the clean-build pages inspected below, in addition to page-1 direct inspection.

Legend: OK = renders correctly, no clipping/overlap/missing glyphs, running header present.

## dengue_ews_v18_scientifically_clean_not_submission_ready.pdf (24 pp)

| Page | Content | Visual result |
|---|---|---|
| 1 | Title, authors, affiliations, corresponding email; first-page notice box | OK — notice reads "Scientifically cleaned author-review copy. Submission metadata and declarations remain incomplete." No internal-workflow language. |
| 2 | Abstract; Author Summary (start) | OK — clean render. Abstract 291 words. Author Summary begins with the corrected 186-word text. |
| 3 | Author Summary (cont.); §1 Introduction (start) | OK — corrected Author Summary (186 words) reads cleanly; de-duplicated ("That increment did not increase across the evaluated lead times…"); no significance language; no broken "did not while an expanded" fragment. |
| 4 | §1 Introduction (cont.); §2 Methods / §2.1 | OK |
| 5 | §2.2 Settings and spatial units; §2.3 Surveillance outcomes and alert labels | OK |
| 6 | §2.4 Population denominators; §2.5 Climate exposures; §2.6 Model ladder and fitting | OK |
| 7 | §2.6 (cont.); §2.7 Calibration and time-updated recalibration | OK |
| 8 | §2.7 (cont.); §2.8 Decision-curve analysis and reference threshold; §2.9 Uncertainty, multiplicity, and analysis status | OK — NB(p*) formula renders; "no prospective public registration claimed" phrasing present. |
| 9 | §2.9 (cont.); §3 Results; §3.1 Cohort and data alignment | OK — M4 planned-primary / M5 pre-computation expanded-sensitivity framing intact. |
| 10 | §3.1 (cont.); §3.2 Sri Lanka primary comparison; Figure 1 (study pipeline schematic) | OK — Figure 1 renders fully, no clipping. |
| 11 | Table 1; Table 2; Figure 2 (Sri Lanka net benefit vs threshold) | OK — tables and plot legible; frozen numbers unchanged. |
| 12 | §3.3 Calibration and recalibration; Table 3; §3.4 Sri Lanka structured climate+hybrid results | OK |
| 13 | §3.4 (cont.); §3.5 Colombia external framework replication | OK — SL M4−M1 and M5−M1 frozen estimates/CIs present. |
| 14 | §3.5 (cont.); Table 4 (Colombia) | OK — Colombia M5−M1 +0.0188 (CI +0.0117 to +0.0260) intact. |
| 15 | §3.5 (cont.); Figure 3 (Colombia AUC and net benefit panels); §3.6 Horizon result | OK — two-panel figure renders. |
| 16 | §3.6 (cont.); §3.7 Threshold and stricter-outcome robustness | OK — Colombia 2022-only +0.0150 (percentile interval +0.0067 to +0.0249) intact. |
| 17 | §3.7 (cont.); §3.8 Cross-setting synthesis; Table 5; §4 Discussion (start) | OK — no cross-setting interaction/heterogeneity/equivalence conclusion; explicitly framed as not a formal comparative test. |
| 18 | §4 Discussion (cont.) | OK |
| 19 | §4 Discussion (cont.) | OK — "Two secondary sensitivity analyses … were consistent with the overall interpretation" phrasing present (WCB-t single-implementation concordant). |
| 20 | §4 Discussion (end); Declarations (Ethics, Data and code availability start) | OK — Declarations are honest placeholders ("pending author confirmation"); no self-certified ethics/funding. |
| 21 | Declarations (Funding, Competing interests, Author contributions, Acknowledgments, Use of AI assistance); References (start) | OK — AI-assistance disclosure reflects §5 refinement ("reviewed the code, outputs, reported results and citations"; no "independently checked"). |
| 22 | References (cont.) | OK |
| 23 | References (cont.) | OK — 35 numbered entries, none undefined. |
| 24 | Supporting information (S1–S12 captions) | OK — opener now reads "are **planned to** accompany the manuscript"; retained secondary-sensitivity note (S9/S11/S12 pointwise, multiplicity-unadjusted); 12 SI items listed; no status/"draft"/internal-workflow phrasing; S1–S3/S10 not described as completed. |

## dengue_ews_v18_internal_author_completion.pdf (24 pp)

| Page | Content | Visual result |
|---|---|---|
| 1 | Title page; internal author-completion notice box | OK — notice reads "Internal author-completion copy. Author metadata and declarations … remain to be confirmed by the authors before submission." Enumerates the unresolved items; no external-facing claim. |
| 2–24 | Identical body to the clean build | OK — verified pixel-identical (`cmp`, 0 bytes differ) to clean-build pages 2–24; all page rows above apply unchanged. |

## Build-check summary (both PDFs, §11)

| Check | Value | Status |
|---|---|---|
| Page count | 24 | OK (matches v17) |
| Abstract word count | 291 | OK (≤300) |
| Author Summary word count | 186 | OK — within PLOS 150–200 (candidate-completion replacement; earlier 221-word overage resolved) |
| Bibliography entries (\bibitem) | 35 | OK |
| Undefined citations/references | 0 | OK |
| Overfull \hbox | 1 (max 3.999 pt) | OK — cosmetic, below 10 pt; not fixed per instruction |
| Underfull \hbox | 1 | OK — cosmetic; not fixed |
| Overfull/Underfull \vbox | 0 / 0 | OK |
| Supporting Information items | 12 (S1–S12) | OK |
| Line numbers | OFF (gated behind `\linenumberedcopy`, not defined in these builds) | OK (reading-copy preference) |
| Double spacing | Active (`\doublespacing`; local `\setstretch{1.0}` only for dense table/SI blocks) | OK |
| Literal `[?]` in text | none | OK |

No page shows clipping, overlapping text, missing glyphs, or a broken figure/table. After the
candidate-completion pass the Author Summary is 186 words (within the PLOS 150–200 limit), so the
earlier length overage is resolved. The remaining open items are author-owned submission metadata
and declarations tracked in `submission_metadata_gate_v18.md` (gate still FAILED); no visual-QC
defect remains.
