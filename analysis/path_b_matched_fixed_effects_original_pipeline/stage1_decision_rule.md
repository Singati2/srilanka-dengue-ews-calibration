# Stage 1 — Pre-committed Decision Rule

Written **before** any Stage-2 fitting. This rule is frozen once you reply `APPROVE PATH B`; it is not to be changed after seeing results.

## Gate A — reproduce the original result (prerequisite)
Re-running the exact original pipeline must reproduce the frozen `M5−M1` point estimate within **absolute tolerance ≤ 0.001** (target dNB@0.30 = +0.018775; dAUC +0.04029) and reproduce the bootstrap interval [+0.0117, +0.0260] to stored precision (seed 20260612, B=1000). **If Gate A fails, STOP** — do not interpret the matched comparison; produce a reproduction-failure report.

## Gate B — isolate climate
`M5` and `M5_no_climate_matched` must differ **only** in the 18 climate-derived columns (`precip_lag0–8`, `temp_lag0–8`). The retained/removed column lists must be saved and checked programmatically. Everything else (cases, season, 32 dept fixed effects, rows, scaling, penalty/tuning, recalibration) identical.

## Gate C — evaluate magnitude and uncertainty
Report the **full point estimate and 95% interval** for `ΔNB_climate = NB(M5) − NB(M5_no_climate_matched)`, plus the decomposition (`ΔNB_nonclimate`, `ΔNB_climate`, and their sum vs `ΔNB_original`). **Do not** reduce the conclusion to "significant"/"not significant."

**Proposed operationally-negligible band (AWAITING AUTHOR APPROVAL — not used until approved):**
```
-0.005 <= ΔNB_climate <= +0.005
```
(≈ at most 0.5 net true-positive equivalents per 100 municipality-weeks in either direction.)

## Gate D — outcome logic
1. Gate A reproduces **and** `ΔNB_climate` is inside the approved negligible band → conclude the prior **+0.0188 was primarily attributable to unmatched non-climate structure (season + department fixed effects)**; Path A authorized.
2. `ΔNB_climate` remains **materially positive** (above the band) → **do not** auto-reframe; report that climate retains net-benefit value on top of the matched baseline; reassess with author/PI.
3. `ΔNB_climate` **materially negative** → report climate reduced net benefit vs the matched baseline.
4. Reconstruction incomplete / Gate A fails → **unresolved verdict**; do not reframe; do not propagate +0.0188 externally until resolved.
5. **Never** substitute the approximate plain-logistic result for the original-pipeline result.

## Explicit caveat carried from Stage 1
The earlier plain-logistic approximation gave a *no-FE* climate hybrid ≈ 0, but the **frozen M4−M1 = +0.0122** (climate on cases, no FE) is materially non-zero. The approximation therefore **cannot** stand in for this pipeline, and the matched contrast `ΔNB_climate` (climate net of cases+season+dept) is genuinely unknown until Gate A/C are executed. This is the whole reason for Path B.

## Fallback if Gate A cannot run cheaply
If the original pipeline cannot be executed within the estimated budget, the fallback is **"unresolved verdict; escalate to author/PI"** — it is **explicitly NOT** "let the approximation carry the correction." (This closes the back-door risk flagged in the go/no-go review.)
