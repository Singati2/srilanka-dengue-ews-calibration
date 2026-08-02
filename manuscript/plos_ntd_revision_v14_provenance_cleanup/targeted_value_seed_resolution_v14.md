# Targeted-value bootstrap seed resolution (v14)

Purpose: resolve whether the Sri Lanka targeted-value regime bootstrap seed was preserved. The v12 manuscript and S6/S8 stated the seed "was not retained." Inspection of the frozen artifacts shows the seed **was** preserved: **20260612**. This document records, per workflow, which output each seed governs, and warns against assuming one seed applies to every Sri Lanka bootstrap. No analysis was recomputed.

## Per-workflow record

| Analysis | Script | Result file(s) | Diagnostic file | B | Seed | Seed applies to that exact output? |
|---|---|---|---|---|---|---|
| Sri Lanka **targeted-value regime** (Stage 1A, h=4) — ΔNB(M5−M1) all-test + threshold grid + train-defined regimes | `_run_targeted_value_stage1a_h4.py` (`SEED=20260612; B=1000`, line 8; `rng=np.random.default_rng(SEED)`, line 58) | `conditional_dnb_bootstrap_ci_h4_v1.csv` (sha256 `ce80b0ce034089942caf…`), `conditional_dnb_h4_v1.csv` | `stage1a_h4_diagnostics_v1.csv` (seed column = 20260612; B = 1000) | 1000 | **20260612** | **Yes** — the runner sets the seed, `default_rng(SEED)` seeds the resampler, and the diagnostics CSV records `seed=20260612`; the CI file sha256 matches the manuscript's targeted-value/threshold-grid numbers. |
| Sri Lanka primary hybrid contrast (M4−M1, M5−M1 all-test) | `hybrid_model_extension` runner | `hybrid_model_predictions_v1.csv` / hybrid report | (hybrid report) | 1000 | 20260612 (as recorded in S6 row 1 from the hybrid report) | Applies to that analysis per S6 row 1; **not assumed** from the targeted-value run. |

## What changed in v13
- Manuscript Methods: "targeted-value bootstrap seed was not retained" → "the Sri Lanka targeted-value regime bootstrap used seed 20260612 (B=1000), verified in the frozen runner script and diagnostics record."
- S6 row 2 (targeted-value regimes): seed placeholder → **20260612**, source = runner script + diagnostics CSV.
- S8: "seed was not retained" → seed 20260612 (B=1000, 0 failures), with the M5−M1 secondary/exploratory framing.

## Caution (explicit)
Seed 20260612 is verified for the **targeted-value Stage 1A** outputs above (and is listed in S6 for other analyses from their own committed records). It is **not** assumed to apply to every Sri Lanka bootstrap; each S6 row cites its own verification source.
