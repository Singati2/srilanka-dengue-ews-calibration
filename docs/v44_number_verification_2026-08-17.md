# v44 biomath candidate — number verification against analysis outputs

**Date:** 2026-08-17 · **Checked by:** Geospatial Lead · **Target:**
`manuscript_v44_biomath_candidate/revised_manuscript_biomath.tex`
(branch `upstream/agent/v44-hybrid-light-decision-framework` @ `26e1fb5`)

**Re-runnable check:** `scripts/verify_numbers_v44.py` — claimed values as literal dicts,
outputs read from disk, compared at the precision the manuscript uses. Exits non-zero while
any mismatch stands. **Adding a number to the manuscript means adding it to that script.**

**Result: 46 checks performed, 4 mismatches.** Plus one systematic LaTeX defect found alongside.

> **RESOLVED 2026-08-17 (same day).** Three of the four mismatches and the whole LaTeX defect are
> fixed on branch `wp45-into-v44`; the verifier now reports **46 checks, 1 mismatch** and exits 1.
> See [§ Resolution](#resolution) at the foot of this document. The one that remains — the
> `+0.0049` reporting-delay increment — **cannot be fixed by retyping** and is the outstanding item.

---

## Why this check was run at all

`BIOMATH_NUMERIC_CROSSWALK.md` already reports "**No candidate number differs from the
canonical manuscript**" over 241 numeric tokens. That statement is true and it is *not* the
check performed here. The crosswalk verifies the candidate against the **previous `.tex`** —
line 3: numbers are "preserved *by construction*" because the file was copied byte-for-byte —
and its own legend concedes the limit: `SOURCE_ONLY` = "artifact cited but **not independently
re-opened** here."

So the crosswalk proves the candidate did not *corrupt* v44. It cannot detect an error
**inherited from** v44, because it never opens an analysis output. That is the gap this pass
covers, and it is where all four mismatches live — every one of them is inherited, none was
introduced by the biomath rewrite.

This is the same lesson the study already recorded on 2026-08-15: *the wrong number was in the
summary layer, which is exactly the layer nobody re-derives.*

---

## Source-of-truth hierarchy (established before comparing anything)

**Authoritative** — frozen, checksum-locked, cited in the manuscript:

| Output | Carries |
|---|---|
| `ALT_STATS/results/route_a_primary.csv` | proper scores, discrimination, conditional CIs |
| `ALT_STATS/results/calibration_metrics.csv` | CITL, slope, ICI, mean predicted, prevalence |
| `analysis/v18_bootstrap_b1000/SL_devinclusive_B1000.json` | SL development-inclusive, B=1000 |
| `analysis/geo_effect_decomposition/co_devincl_full_refit_results.json` | CO development-inclusive, B=1000 |
| `analysis/path_b_matched_fixed_effects_original_pipeline/run/*.json` | CO NB levels, compound, robustness |

**Superseded — must not be used:** `analysis/v17_devinclusive_finalization/SL_devinclusive_results.json`
is the **B=300** pilot. Its recalibrated DI interval is `[+0.00152, +0.02839]` — it **excludes
zero**, where the authoritative B=1000 gives `[−0.00015, +0.03017]`, which **includes** zero.
The manuscript correctly uses B=1000. Flagged because quoting the wrong file here would flip a
headline conclusion.

**Not on this machine** (see the script's closing block): 90th-percentile matched-ablation
outputs, development-inclusive proper-score outputs, and the S1/S3 ladder tables all ship only
`.py`, no results. Those numbers are **unchecked, which is not the same as correct.**

---

## Mismatches — worklist, ordered

| # | Location | Label | Manuscript says | Output gives | Class |
|---|---|---|---|---|---|
| 1 | line 295 (Results Q2-CO prose) | Colombia M5 AUC | **0.726** | `0.7254819772649461` → **0.725** | Stale / inconsistent |
| 2 | line 573 (ladder table) | Colombia M5 AUC | **0.726** | `0.7254819772649461` → **0.725** | Stale / inconsistent |
| 3 | line 316 (Results Q6) | CO matched @ 3-week delay censor | **+0.0049** | `0.005078747` → **+0.0051** | Stale |
| 4 | line 318 (Results Q6) | CO matched, unweighted arm of IPW contrast | **+0.0078** | `0.007858693` → **+0.0079** | Inconsistent (precision) |

### 1–2. Colombia M5 AUC is 0.725, not 0.726 — and the paper already says so once

Two independent outputs agree to 16 digits: `route_a_primary.csv` (both `raw` and `recal`
rows — AUC is invariant to monotone recalibration, so there is no state ambiguity here) and
`recompute_three_results.json` (`A2_dlnm_no_humidity.AUC.M5lin`). Both give
`0.7254819772649461`, which is **0.725** at three decimals.

The manuscript states 0.726 twice (prose line 295, ladder table line 573) — and states the
same quantity **correctly** as `0.7255` at line 746 in the S19 table. **The document
contradicts itself on one number.**

**Why it survived:** the S19 table reports Colombia AUC at *four* decimals while the same
column reports Sri Lanka at *three* (`0.751`, `0.724`). Inconsistent precision inside one
column is what let `0.726` and `0.7255` coexist without looking odd. Worth normalising the
column regardless of this fix.

**Fix:** `0.726` → `0.725` at lines 295 and 573. Nothing downstream moves: no delta, CI, or
conclusion depends on the third decimal here.

### 3. The 3-week reporting-delay increment does not reproduce

`matched_robustness_results.json → A3_matched_delaycurve.drop0_1_2["M5-matched"]` is
`0.005078747`, i.e. **+0.0051**. The manuscript says **+0.0049** (with CI `+0.0001` to
`+0.0097`). The 2-week arm shows the same pattern: output `0.007516546`
(CI `[0.002854, 0.013347]`) against a manuscript-era `+0.0077` (CI `+0.0034` to `+0.0132`).

This is **not** a rounding-convention artifact — 0.0049 and 0.0051 differ in the second
significant figure. The value traces consistently through many internal audit docs
(`v15_final`, `v16_recalibrated_matched_integration`, `v17_plos_gph_submission`,
`v20_round3`), so it is a **stable claim resting on a run that is not the archived JSON**.
Either a superseding run exists off this machine, or the text is stale.

**This one cannot be fixed by retyping** — it needs the run reconciled. It matters more than
its size suggests: `v15_final/harsh_peer_review_final.md` §2.1 flags this exact number as the
paper's most policy-relevant result ("the regime an EWS actually operates in"), and
`v20_round3` promoted it to the abstract. A referee who recomputes it will land on 0.0051.

### 4. The IPW-vs-unweighted contrast is finer than the pipeline can resolve

Line 318 reads "IPW $+0.0079$ versus unweighted $+0.0078$." But the same matched increment
appears in the archive as **three** values: frozen committed `0.00786`, reconstructed
`0.00783` (S17, disclosed, Δ 0.00003), and `0.007859` in the robustness JSON. That spread
**straddles the 0.0078/0.0079 boundary**.

So the quoted difference between the IPW and unweighted arms is plausibly an artifact of which
reconstruction each arm came from, not an effect of weighting. The manuscript's *conclusion*
("essentially unchanged") is safe — arguably safer than stated. The two differing digits imply
a resolution the pipeline does not have.

**Fix:** quote both arms at the precision that is stable, or state them as equal to within
reconstruction tolerance.

---

## Systematic LaTeX defect: 8 cells contain a literal comma

`&, &` appears at lines **539, 540, 639, 641, 642, 645, 745, 748** — four different tables,
including both Δ rows of the S19 table and both raw-state rows of the calibration table. Each
renders a stray `,` in a cell that should be empty or an em-dash. Present in the compiled
28-page PDFs.

Mechanical fix (`&, &` → `& &`), but it should be done in one pass, not per-table, since it is
one defect with eight sites.

---

## What verified cleanly (42 of 46)

- **The entire S19 proper-score table — all 16 level cells and all 6 deltas.** Deltas were
  **recomputed from their operands**, not read from the `paired_difference` column, so a stale
  delta with current operands would have been caught.
- **Every headline Sri Lanka matched-ablation number**: `+0.0087` raw, `+0.0157` recalibrated
  (from `0.01565`), and both development-inclusive intervals — including the recalibrated lower
  bound `−0.0002`, which is a correct round-half-away-from-zero of `−0.00015`. (Python's
  built-in `round()` is banker's rounding and mis-flags this; the script uses `Decimal` with
  `ROUND_HALF_UP` for exactly this reason.)
- **Every headline Colombia number**: `+0.0078` point, DI interval `+0.0008` to `+0.0209`
  (from `[0.00075, 0.02089]`), compound `+0.0188`, NB levels `0.117` / `0.136`, DLNM refit
  `+0.0122`, and the disclosed `0.00783` vs `0.00786` fidelity gap.
- **All four ICI values**, prevalences (`0.336`, `0.375`), CO mean predicted `0.485`, and the
  M1/M4 Colombia AUCs (`0.685`, `0.699`).
- The S19 note explaining that recalibrated full-model AUC `0.751` coincides with raw
  no-climate AUC `0.751` is **correct and self-aware** — both check out independently.

**No headline conclusion is affected by any of the four mismatches.** The deflationary result
stands exactly as written.

---

## Resolution

Applied to `manuscript_v44_biomath_candidate/revised_manuscript_biomath.tex` on branch
`wp45-into-v44`. **17 lines changed.** Verifier re-run: **46 checks, 1 mismatch, exit 1.**

| # | Fix | Status |
|---|---|---|
| 1–2 | CO M5 AUC `0.726` → `0.725` at lines 295 and 573 | **done** |
| 3 | CO 3-week reporting-delay increment `+0.0049` | **open — needs the run reconciled** |
| 4 | Line 318 IPW/unweighted restated as both `+0.008` | **done** |
| — | S19 AUC column normalised to 3 dp (`0.7255`→`0.725`, `0.7134`→`0.713`) | **done** |
| — | Stray literal commas in empty table cells | **done — 16 occurrences over 12 lines** |

Three notes on what changed beyond the original worklist:

**The comma defect was larger than first characterised.** The initial pass caught the `&, &`
pattern (8 sites). The actual defect is `&,` anywhere — which also occurs as `&, \\` at line ends —
giving **16 occurrences across 12 lines**, including a table at line 677 that the first pass missed
entirely. Fixed as one pass. Ampersand counts were verified unchanged on every touched line, so no
table's column structure moved.

**The S19 precision normalisation was not in the original worklist but removes the mechanism.**
Colombia was reported at 4 dp in the same column where Sri Lanka was reported at 3 dp, and that
inconsistency is precisely what let `0.726` and `0.7255` coexist without looking odd. Normalising to
3 dp leaves the printed Δ unchanged (`0.725 − 0.713 = 0.012`, as already stated).

**Line 318 now claims less than it did, on purpose.** The same matched increment exists in the
archive as `0.00786` (frozen), `0.00783` (reconstructed) and `0.007859` (robustness JSON) — a spread
that straddles the `0.0078`/`0.0079` boundary. Quoting two arms that differ in the fourth decimal
implied a resolution the pipeline does not have. Both arms are now stated as `+0.008`; the
conclusion ("essentially unchanged") is unaffected and better supported.

### The one that stands

`+0.0049` versus the archived `0.005079`. This is a **stable claim resting on a run that is not the
archived JSON** — it traces consistently through `v15_final`, `v16_recalibrated_matched_integration`,
`v17_plos_gph_submission` and `v20_round3`. Either a superseding run exists off this machine, or the
text is stale. It needs the run reconciled, most likely on the Linux box, and it is the highest-risk
open item in the manuscript: `v15_final/harsh_peer_review_final.md` §2.1 calls it the paper's most
policy-relevant result, and v20 promoted it to the abstract. **A referee who recomputes it lands on
0.0051.**

---

## Caveat on the "superseded" defect class

Every file in this checkout carries its **checkout** mtime (2026-08-02 for repo files), so
mtime cannot establish whether text predates an output. That class was **not** audited. If it
needs auditing, compare git commit dates of each output against the `.tex`.

---

## Addendum 2026-08-18 — WP4/WP5 numbers added to the verifier

The WP4/WP5 port introduced ~130 numbers into Results Q7. Per the study's own discipline (*adding a
number to the manuscript means adding it to the script*), they are now in `verify_numbers_v44.py`.

**Verifier: 46 checks → 183 checks. 137 WP4/WP5 numbers recomputed** from the quarantine tables —
never transcribed. Still exits 1 while any mismatch stands.

Because the quarantine tables are gitignored by study policy, the section **skips cleanly** on a
machine without them and says so, rather than failing or silently passing.

### Two aggregation hazards, handled explicitly

The provenance doc warns that the same displacement has two legitimate values. Both traps were live:

- **district-week vs district-mean.** Temperature A′→B is `0.205 °C` per district-week but `0.171`
  as a mean of 26 district means. The checks use the 10,842-row tables for table/prose claims and
  the 26-row table only where a district is named.
- **raw vs recalibrated.** The flip analysis is quoted in the **raw** state throughout (recal gives
  46–83 where raw gives 35–76), except the exact bound, which the text labels as recalibrated. The
  climate-removal ceiling is 441 only when compared raw-to-raw; recal-vs-raw gives 759.

### Three defects found, all fixed

| Location | Was | Recomputed | Class |
|---|---|---|---|
| Table `wp4-fold`, 50 km gap | `−0.018` | `−0.019` | Stale/rounding |
| Table `wp4-fold`, 100 km gap | `−0.068` | `−0.070` | Inconsistent |
| Results Q7, flipped-row event rate at `p*=0.10` | `0.087` | `0.088` | Rounding |

The 100 km cell is the interesting one. The **Gap** column was not self-consistent in its sourcing:
at 0, 75 and 100 km it quoted the cluster-bootstrap point estimate, and at 25 and 50 km — where no
bootstrap was recorded — it quoted buffered-minus-control directly. At 100 km that showed on the face
of the table: the row read `0.502`, `0.573`, `−0.068`, and a reader subtracting the two columns gets
`−0.071`. The column is now the direct gap throughout, with the bootstrap CI around it, so the point
estimate is the quantity its neighbours imply. Only two cells moved and no conclusion changes.

### One defect in the checker itself

The first draft guarded its modifier-screen lookups with `if key in fi:`, which **silently skipped six
checks** when the key was wrong — the screen's flip response is `flip_AC_pct`, not `flip_AB_pct`.
A silently skipped check is the untraceable class this script exists to prevent, so the guard is now
an assertion. The same wrong-rung error had been applied to the three top-flip districts
(Badulla 9.9%, Nuwara Eliya 9.3%, Ratnapura 6.0% are the A′→C rung).

### What the new section does not cover

Reported at the foot of every run. The largest gap: **the population-product columns of Table
`wp5-product`**. The local product table is per-district (t2m `0.0070`) while the manuscript quotes
per-district-week (`0.0088`); the district-week product table is not on this machine, so checking one
against the other would be wrong rather than merely lax. Also unchecked: every cluster-bootstrap
interval (notebook cell outputs, not tables), the grid-attenuation figures, the transfer-coefficient
spread, the station lapse-rate interpolation, the partial correlations, and the WP4 reproduce gates.
