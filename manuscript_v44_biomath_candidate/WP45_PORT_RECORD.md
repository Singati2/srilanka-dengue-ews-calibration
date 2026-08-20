# WP4/WP5 port into the v44 biomath candidate

**Date:** 2026-08-17, extended 2026-08-20 · **Branch:** `wp45-into-v44` · **By:** Geospatial Lead
**Source:** `manuscript/wp4_wp5_sections/wp4_wp5_methods_results_v1.tex` (v3, 2026-08-20)

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

---

# Second pass, 2026-08-20: the two deferred analyses are in

The v2 port carried three `\REGBLOCK` sites saying the registered refits "have not been run". Both
have now been run --- on an **independent rebuild** of the linked analysis table, never on the
registered input --- so the marker changes meaning rather than disappearing.

## What changed

| Location | Change |
|---|---|
| Preamble | `\REGBLOCK` **retired**, replaced by `\REBUILD` (10 uses). Zero occurrences of `\REGBLOCK` remain. |
| Methods `sec:methods-wp5` | New paragraph *Decision sensitivity by refitting, and the fourth arm it requires* --- the substitution and its gates, the four-arm ladder, the swap-path null. Carries `\label{par:rebuild}`, which the WP4 methods `\pageref`s. |
| Methods `sec:methods-wp4` | *Measuring what the folds cost* rewritten for two models, plus the non-estimable held-out fixed effect and why only the matched control separates it from the loss of neighbours. |
| Results Q7 | New paragraphs: the refit under each build, and the corrected structural claim; the M5 fold contrast. |
| Results Q7 | `tab:wp5-refit` and `tab:wp4-fold-m5`; `fig:wp5f7b` and `fig:wp4fm5`. Five tables → 7, four figures → 6. |
| Results Q7 | "third independent appearance" of the $\Delta\mathrm{NB}$ mechanism → **fourth**; the population-product tail no longer defers to a blocked refit. |
| Discussion | 14--24% → **15--28%** of the climate block's decision leverage (the refit's own ceiling, 427 flips, not the frozen 441); the $\Delta\mathrm{NB}$ point now rests on a refit; the closing "has not been run" is replaced by what the refit measured. |

## The finding the port has to carry

Exposure construction moves the **decision** and not the **score**. Across four builds every
$\Delta$AUC and $\Delta\mathrm{NB}$ interval spans zero while 72 / 64 / 121 alert decisions flip
against a measured swap-path noise floor of 3. A sensitivity analysis reading only $\Delta$AUC and
$\Delta\mathrm{NB}$ would have reported a null. For this candidate specifically: **$\Delta V_{C,k}$
is not detectably sensitive to how $\mathcal I^{C}$ is realized numerically**, which is the
favourable answer to Q7 --- and it is only credible because the decision-level movement is reported
alongside it rather than suppressed by the same metrics.

## The claim this pass corrects

The v2 port inherited a structural argument holding that district fixed effects absorb Build C
exactly, so it could flip nothing. Measured, it flips 67; entering temperature linearly instead of
through the cross-basis collapses that to 10. The narrow rule survives (a model **linear** in
temperature absorbs a uniform offset) and the model in use is not that kind. Any draft quoting the
old claim as written is wrong.

## Verification

Re-checked structurally, same limits as before --- **a compile has still not been run**:

- 58 `\cite` keys all resolve to `\bibitem`, none uncited · **pass**
- 25 `\ref`/`\pageref` all resolve to `\label`, no duplicates · **pass**
- **all 17 `tabular` column counts consistent with their specs** · **pass**
- `\REBUILD` defined before first use; `\REGBLOCK` absent · **pass**

## Outstanding, restated

1. **PI ratification** --- unchanged, and now with a second item: publishing a competing refit of the
   upstream models on a rebuilt input is a decision for the PI, not a technical choice.
2. **Figures** --- now six PDFs to copy into `submission_figs/` at build time, adding
   `WP5_F7b_decision_sensitivity_refit.pdf` and `WP4_F_fold_effect_within_m5.pdf`.
3. **Number verification** --- **DONE 2026-08-20.** The new numbers are recomputed by
   `scripts/verify_numbers_v44.py`, which grows from 183 checks to **324** (278 of them WP4/WP5).
   One defect was surfaced and fixed in this candidate: Table `tab:wp4-fold-m5`'s 50 km train-units
   cell read `15.5`, the *mean* over folds from the metrics file, where Table `tab:wp4-fold` quotes
   the *median* from the gap file (`15`); the two tables were not comparable in that column. One
   pre-existing mismatch still stands, the `+0.0049` three-week reporting-delay increment, which
   needs the Linux box.
4. **Compile and re-read** --- unchanged, and now the first thing to do.
