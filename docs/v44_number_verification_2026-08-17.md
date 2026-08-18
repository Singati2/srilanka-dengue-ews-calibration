# v44 biomath candidate — number verification against analysis outputs

**Date:** 2026-08-17 · **Checked by:** Geospatial Lead · **Target:**
`manuscript_v44_biomath_candidate/revised_manuscript_biomath.tex`
(branch `upstream/agent/v44-hybrid-light-decision-framework` @ `26e1fb5`)

**Re-runnable check:** `scripts/verify_numbers_v44.py` — claimed values as literal dicts,
outputs read from disk, compared at the precision the manuscript uses. Exits non-zero while
any mismatch stands. **Adding a number to the manuscript means adding it to that script.**

**Result: 46 checks performed, 4 mismatches.** Plus one systematic LaTeX defect (8 cells)
found alongside.

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

## Caveat on the "superseded" defect class

Every file in this checkout carries its **checkout** mtime (2026-08-02 for repo files), so
mtime cannot establish whether text predates an output. That class was **not** audited. If it
needs auditing, compare git commit dates of each output against the `.tex`.
