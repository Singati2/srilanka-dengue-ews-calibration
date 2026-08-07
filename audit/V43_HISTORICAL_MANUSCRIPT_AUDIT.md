# V43 historical manuscript audit (immutable record — R2 §2.5, §18.7)

**File:** `manuscript_v43/revised_manuscript.tex` · **sha256[:16]:** `60fa9b3632ad5c0d`

## Finding: v43 CONTAINS an internal proper-score contradiction (confirmed)
- **Methods (§ secondary reanalysis):** "...because the refit-both-models pipeline was not
  re-executed, **development-inclusive proper-score intervals were gated and not computed**."
- **Results/S18:** nonetheless **reports** development-inclusive proper-score intervals, e.g.
  Sri Lanka ΔNLL `-0.0403 to +0.0040`, Colombia ΔNLL `-0.0224 to -0.0002`.

These two statements are mutually inconsistent. The LaTeX-tolerant detector
(`detect_proper_score_contradiction`) flags it: **contradiction = True**.

## Why round 1 missed it
The round-1 detector matched intervals on raw text; v43 writes them inside `$...$` math
(`$-0.0403$ to $+0.0040$`), so `reports_DI` was False and the contradiction was not raised —
a genuine false PASS. R2 §2.2 LaTeX normalization fixes this.

## Disposition (do NOT rewrite history — R2 §2.1, §18.7)
v43 is preserved as-is. The repair belongs in a **new v44 manuscript** (retire the "gated and
not computed" Methods clause, since the intervals were in fact computed). This file is the
permanent historical record; the regression test `test_1b_real_v43_file_is_detected` will keep
failing-open (detecting) against the real v43 file until a separate v44 is created and audited.
