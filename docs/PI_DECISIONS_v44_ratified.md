# PI decisions — ratified (v44 track)

**Ratified by:** G. Shiwakoti (PI / first author) · **Date:** 2026-08-07 · **Scope:** unblocks the
geomatics build (notebooks 05–08) and WP5, and clears the manuscript's one internal contradiction.

---

## Decision 1 — WorldPop coastal shortfall (was blocking WP5 Build B)

**Context (co-author notebook 03 §7 / study_decision_log OPEN item):** whole-pixel-to-centroid
assignment under-captures ~3.5% of population inside the 26 RDHS polygons (20.9–21.1 M vs
~21.4–21.9 M national), concentrated in dense coastal districts; the same denominator feeds WP5's
population-weighted exposure.

**RATIFIED DECISION: accept-and-report as primary; fractional-coverage boundary weighting as the WP5 sensitivity.**
- Population weights are normalized *within each unit*, so a roughly-proportional coastal undercount
  largely cancels in the weighted-mean exposure; the absolute denominator is not used for per-capita rates.
- Report the per-district capture fraction. Run fractional-coverage boundary weighting as the WP5
  **population-product sensitivity** (already an accepted D4 extra) — not a blocker for Build B.
- **Action for co-author:** proceed with Build B on the WorldPop denominator; add the fractional-coverage
  sensitivity in WP5.

---

## Decision 2 — geomatics stress-test rung (was awaiting PI sign-off)

**Context (study_decision_log DIRECTION):** geomatics-only model → stability feature-selection inside
the WP4 spatial folds → selected-geomatics hybrid with recent cases, judged by calibration + net benefit,
framed as a *value-of-geomatics stress test of the existing null* (not a proposed predictor).

**RATIFIED DECISION: APPROVED — conditional on four hard guardrails, pre-registered before outcome access.**
1. Freeze/tag the feature + selection spec **before any outcome join** (no outcome-driven selection).
2. **Nested spatial-CV stability selection** (selection inside the WP4 folds → no selection leakage).
3. Report importance **ranges, not a lone winner** (collinearity makes single-feature claims unstable).
4. **Honest-null is the accepted outcome.** If geomatics *materially* helps beyond the matched
   comparator, it becomes **Paper 2** and escalates to the PI — it never becomes a new accuracy
   predictor in this paper (no-new-model rule preserved).
- **Action for co-author:** run the rung under these four conditions; pre-register (repo tag) first.

---

## Deliverable — v44 Methods correction (applied)

The v43 Methods clause "development-inclusive proper-score intervals were gated and not computed"
contradicted the Results, which report those intervals (from `analysis/devincl_proper_scores_v1`,
B=1000, seed 20260612, 0 failures). Corrected in **`manuscript_v44/revised_manuscript.tex`** (v43 is
preserved unchanged as historical evidence per the audit's immutability rule). The KG/agent audit
confirms: v43 MANUSCRIPT CONSISTENCY = FAIL (contradiction); v44 = REVIEW (contradiction resolved).

`manuscript_v44/` is a **DRAFT**: it carries only this Methods correction. Geomatics integration
(M6/WP4/WP5) and the full experimental reframe remain pending the co-author's build under the two
decisions above — this draft must not be treated as submission-final.
