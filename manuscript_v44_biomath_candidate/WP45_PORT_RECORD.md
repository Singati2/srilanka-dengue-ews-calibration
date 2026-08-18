# WP4/WP5 port into the v44 biomath candidate

**Date:** 2026-08-17 · **Branch:** `wp45-into-v44` · **By:** Geospatial Lead
**Source:** `manuscript/wp4_wp5_sections/wp4_wp5_methods_results_v1.tex` (v2, 2026-08-16)

**Ported, not copied.** The fragment was written in v18's voice against a manuscript whose Methods
carried no incremental-estimand formalism. What changed, and why.

---

## What was inserted

| Location | Content |
|---|---|
| Methods, after *Settings, spatial units, and data sources* | `\subsection{Exposure construction as an analyst degree of freedom}` (`sec:methods-wp5`) and `\subsection{Spatially-honest cross-validation}` (`sec:methods-wp4`) |
| Results, after Q3–Q5, before Discussion | `\subsection{Q7. Is the increment robust to how climate information is operationalized, and to spatially-honest validation?}` (`sec:wp45`) |
| Results | 5 tables: `tab:wp5-ladder`, `tab:wp5-flips`, `tab:wp5-product`, `tab:wp4-power`, `tab:wp4-fold` |
| Results | 4 figures: `fig:wp5f2`, `fig:wp5f7`, `fig:wp5f8`, `fig:wp4f` |
| Discussion, before *Limitations* | `\subsection*{Exposure construction and spatially-honest validation}` |
| Preamble | `\providecommand{\REGBLOCK}` |
| Bibliography | 11 new `\bibitem` entries, converted from BibTeX to the candidate's inline Vancouver style |

File: 112,096 → 156,064 bytes.

## Voice and notation changes

**Framed against the estimand.** v44 defines $\Delta V_{C,k}=V_k(\mathcal I^{SC})-V_k(\mathcal I^{S})$.
Exposure construction is an operationalisation choice *inside* $\mathcal I^{C}$, so WP5 is now posed
as whether $\Delta V_{C,k}$ is sensitive to how $\mathcal I^{C}$ is realized numerically — not as a
free-standing MAUP analysis. The single most useful consequence: the fragment's "climate block
removed (ceiling)" **is** the estimand's own contrast, $\mathcal I^{SC}\to\mathcal I^{S}$, and is now
named that way in the text, the flips table and the F7 caption. The transfer coefficient is likewise
written on $\mathrm{logit}(p_{\text{M5}})-\mathrm{logit}(p_{\text{M5-no-climate}})$ rather than on
generic "full minus no-climate".

**Results recast as Q7.** v44's Results are question-headed (Q1, Q2, Q6, Q3–Q5). The fragment's four
free-standing Results subsections were merged into one question-headed subsection with paragraph
heads, matching the house structure.

**Redundancy removed.** v44's *Settings* subsection already documents CHIRPS v2, ERA5-Land, the
Alduchov–Eskridge derivation and the ISO-week linkage. The ported Methods reference these rather
than restating them, which is most of the length reduction.

## Two factual corrections the fragment predates

**1. The Colombia companion no longer exists.** The fragment said the well-powered spatial claim
"rests on the Colombia block cross-validation … outside the scope of the Sri Lanka analysis reported
here", which reads as *deferred*. Per the 2026-08-17 decision, §4.3 is **withdrawn**, not deferred.
The ported text now says a Colombia block CV "was scoped and is not part of this study's evidence",
and states plainly that the Sri Lanka spatial result therefore **stands alone as a characterised
limitation rather than a certified claim**. This is asserted in Methods, in Results (bolded) and in
the Discussion, because it is the single most load-bearing caveat in the port.

**2. The `\REGBLOCK` justification was wrong.** The fragment said the registered re-runs are blocked
because "the frozen analysis archive does not contain [design matrices] (it holds predictions)".
That is **false**: `analysis/v12_referee_response/run/sl_matched_and_recal.py` contains both the
design-matrix builder and the cross-basis builder, and reproduces the frozen M1/M4/M5 to <1e-6. The
analyses are not *impossible*, they are *not yet run*. All three `\REGBLOCK` sites now say "has not
been run". Zero occurrences of the old claim remain.

## Deliberately not claimed

Unchanged from the fragment: that the headline comparison survives spatial CV (not refitted under
the folds); that exposure construction changes $\Delta$AUC or calibration (same); anything about
Colombia; any absolute performance figure for the geomatics-only model.

## Verification

No TeX toolchain on this machine, so the port was checked structurally instead of compiled:

- environments balanced · **pass**
- 58 `\cite` keys all resolve to `\bibitem` · **pass**
- 20 `\ref` all resolve to `\label`, no duplicate labels · **pass**
- braces balanced (978/978) · **pass**
- **all 15 `tabular` column counts consistent with their specs** · **pass**
- `\REGBLOCK` defined before first use · **pass**

**A compile has not been run.** That is the first thing to do on a machine with LaTeX.

## Outstanding

1. **PI ratification.** This port overrides `FINAL_CANONICAL_DECISION.md` line 8, which places
   M6/WP4/WP5 outside Paper 1 evidence. That file is annotated, not rewritten. Nothing is pushed.
2. **Figures.** The four PDFs exist at `Manuscript_Figures/wp{4,5}/` and are referenced as
   `submission_figs/…` per the candidate's convention (gitignored; `\safeincludegraphics` renders a
   placeholder). They must be copied into `submission_figs/` at build time.
3. ~~**Number verification.**~~ **DONE 2026-08-18.** 137 WP4/WP5 numbers are now recomputed by
   `scripts/verify_numbers_v44.py` (46 checks -> 183). Three defects were found and fixed in this
   candidate: Table `wp4-fold` 50 km gap `-0.018`->`-0.019`, 100 km gap `-0.068`->`-0.070`, and the
   flipped-row event rate at `p*=0.10` `0.087`->`0.088`. The 100 km cell mattered most: the Gap
   column had been mixing bootstrap point estimates (0/75/100 km) with direct buffered-minus-control
   gaps (25/50 km), so the row read `0.502`, `0.573`, `-0.068` and a reader subtracting got `-0.071`.
   The column is now the direct gap throughout with the bootstrap CI around it. No conclusion moves.
4. **Compile and re-read.** Both PDFs, then a read-through for flow at the two seams.
