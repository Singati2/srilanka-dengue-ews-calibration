<!--
DRAFT PR #1 comment — not yet posted. Covers 9085b3f (write-up) and 9f4789e (F8).
Prepared 2026-08-16 by the Geospatial Lead. Post with:
  gh pr comment 1 --repo Singati2/srilanka-dengue-ews-calibration --body-file docs/pr1_memo_draft_2026-08-16.md
(strip this comment block first)
-->

## Figure F8 lands, the WP4/WP5 write-up is drafted — and the strongest signal in the F8 screen is a decoy I put there on purpose

Pushed as `9085b3f` and `9f4789e`: `notebooks_wp45/wp5_07_miscalibration_structure_and_F8.ipynb`, **16/16 QC**, plus `Manuscript_Figures/wp5/WP5_F8_miscalibration_structure.png`, two quarantine tables, and drop-in manuscript sections under `manuscript/wp4_wp5_sections/`.

**With F8, the plan's figure set is complete: F2, F7, F8.** Every WP4/WP5 analysis that can be run without collaborator artifacts is now done, and written up.

### Why §3.6 was runnable

The README had it as downstream of the §5.1-blocked refit. It isn't — **fifth time the same check has recovered work I'd recorded as blocked**, after §3.2, §3.5, §3.3 and WP4's evaluation half. Ask whether the blocker covers *all* of it:

- per-district **calibration slope and intercept** are a within-district fit of the outcome on `logit(p)` — that needs predictions, not a design matrix;
- per-district **ΔNB** is the full-vs-noclim difference on identical rows — predictions again;
- per-district **flip counts** were already computed in `wp5_05`;
- every **modifier** the plan names — elevation, built-up, NDVI, distance-to-water, plus the optional set — was already staged by M6 notebooks 01 and 03.

All four left-hand sides and all fifteen right-hand sides were on this machine.

### The guardrails, because §3.6 is the plan's most dangerous section

A 4 × 15 screen on **26 units** will produce something publishable-looking whether or not anything is there. So the plan's own rules were treated as hard requirements: the covariate panel was **fixed before looking** and not revisited; **Benjamini–Hochberg across the whole 60-test grid** at once, not per response; **all 60 tests are plotted** in panel (e) so the figure cannot be read as a selected subset; and the whole thing is stamped `EXPLORATORY_EXPLANATORY` — no modifier here may re-enter the ladder as an accuracy predictor.

60 tests, **19 reach raw p < 0.05, 6 survive FDR**.

| response | modifier | ρ | q |
|---|---|---|---|
| calibration **intercept** | **alert prevalence (not geospatial)** | **0.854** | <0.001 |
| calibration slope | cropland fraction | 0.606 | 0.031 |
| calibration slope | land-cover diversity | 0.588 | 0.032 |
| A′→C flip rate | slope | 0.560 | 0.035 |
| A′→C flip rate | elevation | 0.560 | 0.035 |
| A′→C flip rate | HAND (flood proneness) | 0.548 | 0.038 |

### The top row is the point, and it is a warning rather than a finding

The strongest association in the entire screen is calibration **intercept against the district's own alert prevalence** — near-tautological, since an intercept absorbs a base rate. **I put `prev` in the modifier panel deliberately, as a non-geospatial decoy.**

That decision is the transferable part. Leaving it out would not have removed the tautology; it would have **hidden** it, and whichever geospatial modifier happens to correlate with outbreak burden would have inherited the association silently and been written up as an explanation of miscalibration. **Any screen of this shape should carry the obvious non-spatial confounder through it rather than excluding it up front.**

### What survives once prevalence is accounted for

**Miscalibration has real spatial structure** — the WP6 bridge §3.6 was written to build. Per-district calibration slope spans **0.67 to 2.23**, so the model is not uniformly calibrated in space, and it tracks cropland fraction and land-cover diversity up and population density down. All three **survive adjustment for prevalence** (partial ρ = 0.50 / 0.49 / −0.44), so they are not the tautology in disguise. Predictions are too widely spread in the dense built-up districts and too compressed in the agricultural, land-cover-heterogeneous ones.

### Where I stopped, and why

**Decision flips concentrate in the highlands** — Badulla 9.9% of weeks, Nuwara Eliya 9.3%, Ratnapura 6.0% — which is coherent with those being where the lapse correction moves exposure most. It is tempting to write that terrain drives the flips. **It is not identified, and I have not written it.**

Elevation and the measured B→C displacement are collinear across 26 districts at **ρ = 0.74**, and *neither survives controlling for the other*: elevation given displacement ρ = 0.27 (p = 0.18), displacement given elevation ρ = 0.05 (p = 0.82). At this sample size the design cannot separate them. The map reports a concentration; the attribution is left open, and the provenance file carries an explicit note so a later revision does not quietly upgrade it.

### ΔNB, for the third time

**No modifier explains per-district ΔNB** — the strongest of fifteen is population density at ρ = 0.40, **q = 0.15**. Given `wp5_05`, that is the *expected* result rather than a second null: the same structural blindness that flattens ΔNB nationally flattens it district by district. **A decision-flip count and ΔNB are not substitutes**, and this work now demonstrates that three independent ways — nationally (§3.3), across population products (§3.5), and spatially (§3.6).

### The write-up (`9085b3f`), and why it is not in the manuscript tree

`manuscript/wp4_wp5_sections/` holds three files: drop-in Methods and Results subsections in the v18 candidate's voice and section conventions, with five tables and four figure blocks; a number-provenance file mapping every figure quoted to the artifact it was recomputed from; and the 11 bibliography entries the sections need that the manuscript `.bib` does not already carry.

**They are held outside the manuscript tree on purpose.** PR #8 places M6/WP4/WP5 outside Paper 1 evidence pending direction, and Paper 1 vs Paper 2 is unanswered. Drop-in fragments cost nothing to move once that is settled; edits to a live manuscript would have to be undone. The two §5.1-blocked analyses are marked inline with `\REGBLOCK` so the revisit points are mechanical to find.

**Caveat stated rather than buried:** there is no LaTeX toolchain on this machine, so the fragment passed a structural check — braces, environments, table cell counts against column specs, every `\cite` key resolving against both `.bib` files, every `\includegraphics` target existing, no dangling `\ref` — but it has **not been compiled**.

### A correction to my own README

Every number in the write-up was recomputed from the quarantined tables rather than transcribed, and that caught one error. The `notebooks_wp45/README.md` summary said population weighting makes **"fifteen districts drier, eleven wetter"**. It is **17 down, 9 up**, under either baseline arm. The figure never appeared in `wp5_01` — I introduced it in the README summary. Corrected; no notebook, table, figure or earlier memo is affected.

The lesson is where it came from: the wrong number lived in the **summary layer**, which is the layer nobody re-derives. Summaries need the same provenance discipline as results.

One more trap worth recording for anyone checking these numbers: the same displacement has two legitimate values depending on aggregation. Population weighting moves weekly mean temperature **0.205 °C per district-week** but **0.171 °C as a mean of district means**. The sections quote district-week throughout; checking one against the per-district contrast table will disagree, and that disagreement is not an error.

### Scope

Nothing here is causal — 26 units, 60 tests, exploratory-explanatory by the plan's own rule. Nothing here speaks to the study's headline comparison. Nothing about **Colombia**, where ~1,000 municipalities would give this screen real power and where the analogue of F8 is worth considerably more than it is here. And F8 uses the **frozen** predictions, so it maps where the *existing* model is miscalibrated — not how each exposure build would change that, which remains the §5.1-blocked re-run.

### The four open questions, now in one place

They have accumulated across separate memos and are easy to lose, so they are collected in **`docs/pi_ask_v1_geomatics_open_questions.md`**, each with the smallest artifact that would unblock it:

1. **M5's design matrix** — for WP4's cross-model fold re-run. `wp4_02` *raised* this one's urgency.
2. **The code that builds that matrix from an exposure table** — for WP5 §3.3's registered re-run. `wp5_05` *lowered* this one's urgency.
3. **Which model form** the artifacts use — absolute or district-relative temperature, and whether they carry dewpoint/humidity.
4. **Paper 1 or Paper 2** for the geomatics work.

**Q1 and Q2 are not the same request.** WP4 re-fits the same columns on different rows, so a static matrix suffices. WP5 re-fits on different exposure values, so the columns must be regenerated and the *builder* is what's needed. Answering either does not answer the other, and if only one can be answered it should be Q1. Q3 is a one-sentence answer that decides in advance what the re-run can possibly find — a district-relative temperature model absorbs Build C exactly, so a null there would be a fact about the parameterisation and not about terrain.
