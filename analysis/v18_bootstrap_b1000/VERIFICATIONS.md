# VERIFICATIONS (Task 3)

## 3.1 — C2 disclosure: **GAP FOUND → one SI sentence to add**
The raw M5−M1 contrast has two slightly different percentile intervals in the repository — committed [−0.0012, +0.0181] (used in the manuscript, 5 loci) vs reconstruction [−0.0025, +0.0180] (recal_matched_results.json) — same point estimate (+0.0081), both include zero. This reconciliation currently lives **only** in `NUMBER_PROVENANCE_TABLE.csv`; a grep of the manuscript found **no** mention (the only "implementations differed" hit is about the climate cross-basis, not the bootstrap). **Action:** add one sentence to the SI reproducibility note (S14 Text) so a reader who finds both numbers finds the reconciliation. Proposed:
> "The committed and reconstruction bootstraps yield marginally different percentile intervals for the raw M5$-$M1 contrast ($-0.0012$ to $+0.0181$ vs $-0.0025$ to $+0.0180$; identical point estimate $+0.0081$, both including zero), a bootstrap-implementation difference that does not affect any conclusion; the committed interval is reported in the main text."
(Applied in the v18 manuscript.)

## 3.2 — Table 6 M5_no-climate row: **GENUINELY COMPUTED (not a copy of M1)**
Source: independent reconstruction (`/tmp scratch prov_check.py`, same feature pipeline; gate validated elsewhere to ≤1.1e-16). Full-precision test-set values (n=3,926):

| Model | AUC | NB(0.20) | NB(0.30) | NB(0.40) |
|---|---|---|---|---|
| M1 (frozen: C=1e6, AR-standardized) | 0.751480 | 0.184857 | 0.136635 | 0.082527 |
| M5_no-climate (matched: whole-design standardized, C-selected) | 0.751293 | 0.184794 | 0.136016 | 0.082781 |

- The two rows **differ at every metric** (4th decimal or closer); NB(0.30) even **rounds differently** (M1 0.137 vs matched 0.136) and AUC rounds differently (0.752 vs 0.751).
- Per-row prediction difference: **max|p_M1 − p_matched| = 2.9×10⁻³**, correlation 0.999997 — very similar (both carry cases+season+RDHS) but an independent fit, **not a copy**.
- The rounded Table row (matched: AUC 0.751, NB 0.185/0.136/0.083) is a faithful 3-dp rounding of the computed values.
