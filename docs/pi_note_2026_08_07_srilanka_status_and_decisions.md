# PI note — Sri Lanka geospatial workstream: results, and four decisions needed

**From:** Geospatial Lead (WP4 / WP5) · **Date:** 2026-08-07 · **Scope:** Sri Lanka only
**Detail:** `docs/study_decision_log.md`, entries 2026-08-06 and 2026-08-07
**Nothing here has been used in the manuscript.** Three results are finished and none can be
reported until the decisions in §5 are made.

---

## 1. Summary

| Workstream | State | Needs from you |
|---|---|---|
| **M6** geomatics-only model | **complete** — fitted, scored, plotted on the frozen test panel | framing sign-off; a ruling on §10's contrasts |
| **WP5** Build B (pop-weighted exposure) | weight field complete; exposure values await climate staging | a free CDS API key |
| **WP4** spatially-honest CV | fold geometry + autocorrelation range complete | design sign-off |

The headline: **M6 is a clean honest null**, and **exposure construction is not** — population-weighting
moves district temperature by up to 1.8 °C. Both are reportable results. The WP4 spatial check came
back showing no residual spatial autocorrelation, which makes that validation cheap rather than
expensive.

---

## 2. M6 — the honest null, on identical rows

Scored on the **identical 3,926 test rows** as the frozen comparators (26 RDHS × 151 weeks,
2023-01-02 → 2025-11-17), h = 4 weeks, 75th-percentile elevated-activity label, raw predictions,
RDHS cluster bootstrap B = 1000 at seed 20260612.

| model | AUC [95% CI] | PR-AUC | Brier | NB @ p*=0.30 [95% CI] |
|---|---|---|---|---|
| **M6 (geomatics only)** | **0.601 [0.568, 0.638]** | 0.442 | 0.223 | **0.058 [0.033, 0.085]** |
| M5 full hybrid | 0.771 [0.741, 0.804] | 0.667 | 0.180 | 0.145 [0.106, 0.184] |
| M5 no-climate | 0.751 [0.721, 0.782] | 0.652 | 0.191 | 0.135 [0.100, 0.176] |

- ΔNB (M6 − M5 full) **−0.087 [−0.112, −0.062]**; ΔNB (M6 − M5 no-climate) **−0.078 [−0.104, −0.054]**
- **0.000** of bootstrap replicates favour M6 in any contrast
- M6's net benefit (0.058) barely clears treat-all (0.052)

Per the pre-specified interpretation rules in `M6.md` §10 this is the **expected honest null**: a
purely spatial landscape model carries little standalone decision value. It strengthens the paper's
caution rather than contradicting it. **No headline changes, and none are proposed.**

**How the labels were verified.** The Sri Lanka label thresholds were not available, so they were
recovered from the frozen artifacts themselves: the label is a fixed incidence, so in count space it
scales with population, and solving the frozen outcomes for that scale gave all 26 districts a
feasible interval. The recovered labels reproduce the frozen test outcomes **3,926 / 3,926 =
1.000000**, with prevalence 0.3365 and 1,321 events matching `PAIRED_ROW_AUDIT.md` exactly. Notebook
06 asserts this before fitting, so the gate is permanent rather than a one-off check.

---

## 3. WP5 — exposure construction is not a null

Build A (area-weighted) and Build B (population-weighted) differ *only* in the weights, so the weight
field is the whole of Build B and was built before any climate data. Using the staged DEM and the
standard lapse rate:

**Population-weighting moves district temperature exposure by −1.75 °C to +0.83 °C.**

Badulla is the case: its population lives ~270 m *above* the district's areal mean elevation —
highland towns and tea estates, with the sparsely-settled Uva basin dragging the area-mean down — so
weighting by people **cools** its exposure. Ratnapura runs the other way.

For a model whose transmission terms move steeply over that range this is not a rounding correction,
and it means the plan's honest-null clause (§3.4) does **not** fire on temperature.

Two further findings:

- **Build C's target should come down.** Build B alone captures ~92% of the elevation displacement.
  The within-cell residual Build C would add tops out at ~0.36 °C, and is not reliably additive —
  in Badulla the two terms carry *opposite* signs. Build C stays in scope per 2026-07-07, but its
  acceptance target should be a few tenths of a degree, not something comparable to B.
- **Build A's `all_touched` mask misplaces ~31%** of a district's weight versus fractional overlap.
  Half of a typical ERA5-Land cell lies outside the district it is credited to.

Precipitation remains open — CHIRPS is patchy and convective and has no elevation shortcut, so it
must wait for the data.

---

## 4. WP4 — the spatial check is cheap, and here is what it costs

**The autocorrelation range is effectively zero.** Moran's I on model residuals, computed per week
across 151 weeks and tested by permutation (999 shuffles), is indistinguishable from its null at
**every** distance band for all three models — permutation p ranges 0.53 to 0.99, and the empirical
variogram is flat from 25 km to 400 km.

That finding is more robust than it first looks. M5 carries **district fixed effects**, which absorb
time-invariant spatial structure, so a near-zero residual Moran's I could be an artifact of the model
rather than of the data. **M6 carries no fixed effects at all** and shows the same result
(I = 0.001 among adjacent districts, p = 0.99). The absence is therefore not an FE artifact.

Stated honestly: at n = 26 with weekly replication, the permutation null has sd ≈ 0.02, so this rules
out residual spatial correlation above roughly |I| = 0.04. It does not prove zero.

**Consequence:** the buffered scheme costs almost nothing. Adopting the minimum buffer (drop
immediately-adjacent districts) retains **21 of 25** training districts in the median fold and 16 in
the worst. The reviewer concern that motivated WP4 is answered directly rather than by an expensive
scheme.

For context, had the range been large the cost would have been severe — Sri Lanka is ~430 km end to
end, so at a 100 km buffer the median fold trains on 9 of 25 districts and at 150 km the scheme
collapses (12 of 26 folds keep fewer than 5 training districts). That table is frozen and available
if you would prefer a more conservative radius than the data requires.

Per §4.6 Sri Lanka remains the **compact-country sensitivity companion** regardless; the well-powered
external-validation claim still rests on Colombia's block CV, which is out of scope while this work
is Sri Lanka-only.

---

## 5. Decisions needed

**5.1 — M6 framing sign-off (blocking).** `M6.md` §0 requires it before M6 appears anywhere. The
proposal is to report it exactly as §10 prescribes for this outcome: an exploratory sensitivity
comparator returning a null, supporting the paper's thesis that recent surveillance is hard to beat.
Not a headline model, no figure caption calling it "best".

**5.2 — §10's contrast set cannot be answered as registered.** §10 asks whether M6 beats **M0**
(season) and **M2** (climate-only). The frozen artifact carries only **M5-full** and
**M5-no-climate** predictions on these rows. So the answerable question is *"does landscape add
against the full hybrid, and against it stripped of climate"*. Either M0/M1/M2 test predictions are
supplied on the identical rows, or §10 is restated. **A ruling is needed before write-up.**

**5.3 — WP4 buffer radius.** The data support the minimum buffer (adjacency only, 21/25 districts
retained). Confirm that, or nominate a more conservative radius from the frozen power table.

**5.4 — a free CDS API key**, so ERA5-Land can be staged and Build B's exposure table built. This is
the only item where the workstream is waiting on an external credential; CHIRPS is open.

---

## 6. Two limitations recorded, neither blocking

- **The 2025 MODIS gap.** Both MODIS products are absent 2025-07-04 → 2025-11-17 in the Planetary
  Computer catalogue (source-side, not cloud; Aqua is absent too). 11.3% of M6's test rows therefore
  carry forward-filled features. They cannot be dropped without breaking identical-rows
  comparability. The fresh-MODIS subset gives AUC 0.612 / NB 0.065 — the same conclusion — so this is
  a methods-section caveat, not a threat to the result. NASA's archive has the granules if we want
  the backfill for completeness.
- **The outcome table was restaged from source** on this machine (415 of 416 WER issues, QC passed).
  It is *not* byte-identical to the 2026-06-10 freeze: the 2018 week 4 PDF is now served as an
  image-only scan with no text layer, costing 26 district-weeks in the **training** period. The
  manuscript's frozen v2.0 is untouched; this is a parallel artifact, and M6 inherits that small gap.

---

## 7. Sequencing note, for the record

M6 is Phase **4** of `maup_sensitivity_and_spatial_cv_plan.md` §7 — the rung tagged *optional*. It
was built first because it was the only work runnable while Phase 0 staging stalled. Phases 1–3,
which carry the two *mandated* deliverables (WP5 Build B population-weighted exposure, a designated
primary result; and WP4 spatial CV), are now underway and are where effort should stay. WP4 is
complete but for a sign-off; WP5 needs only the climate acquisition in §5.4.
