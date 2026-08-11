# SINGLE_PENALTY_0099_PROVENANCE (Gate A)

```
VALUE: +0.0099
STATUS: PRE_EXISTING_VERIFIED

ORIGINAL_ARTIFACT: canonical v44 manuscript line 171 (Sri Lanka matched-increment paragraph):
  "Refitting both matched models under a single identical penalty left the increment
   essentially unchanged (+0.0087 to +0.0099), so it is not an artifact of differential
   regularization." Underlying numbers committed with the V6 frozen analysis pipeline/outputs.
ORIGINAL_SCRIPT: Sri Lanka matched-ablation + recalibration pipeline under analysis/
  (family: analysis/v12_referee_response/run/sl_matched_and_recal.py — L2 LogisticRegression;
   the single-penalty variant fixes a common C across the matched pair). Frozen V6 pipeline.
ORIGINAL_COMMIT: 0b8bbff ("REPRO: commit V6 analysis pipelines and frozen outputs", 2026-07-15);
  carried forward in 4241971 (v43 sync, 2026-07-31) and 8573512 (v44 Methods, 2026-08-07).
ORIGINAL_DATE: 2026-07-15 (first git appearance of the "single identical penalty" sentence + value).
ORIGINAL_COMMAND: the committed V6 Sri Lanka matched-ablation runner (not re-executed here).
INPUT_HASHES: frozen V6 SL predictions (M1/M4/M5 reproduced to <1e-6 per manuscript); not re-hashed here.
OUTPUT_HASH: n/a (not regenerated in this task).
FIRST_GIT_APPEARANCE: commit 0b8bbff, 2026-07-15 18:41 -0400.
FIRST_LOCAL_APPEARANCE: quoted (not generated) in this task's MATCHED_COMPARATOR_STRUCTURE.md / BIOMATH_NUMERIC_CROSSWALK.md.
WAS_ANY_MODEL_REFIT_DURING_THE_BIOMATH_TASK?: NO
SAFE_TO_QUOTE_IN_MANUSCRIPT?: YES
```

## Verdict: **GATE A = PASS**
`+0.0099` is the upper end of the Sri Lanka matched-ablation single-penalty refit range reported in the **canonical v44 manuscript** (line 171), whose underlying result was computed and committed with the frozen V6 pipeline on **2026-07-15** — weeks before this formalization task. It is distinct from the identical numeral `+0.0099` that appears in the older `paper1_plos_gph_v20b.tex` lineage (there, the cross-fitted M5−M1 recalibration $+0.0081\to+0.0099$); the canonical v44 usage is unambiguously the matched-ablation single-penalty refit. No model was fit or refit during the biomath task; the number was quoted verbatim from the canonical source. Safe to retain.
