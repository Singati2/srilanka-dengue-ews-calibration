# B=1000 development-inclusive rerun (headline gate)

Identical procedure to `SL_development_inclusive.md`, changing **only** B (300→1000) and the output path (diff of the two scripts, excluding those two lines, = 0). Same seed 20260612, same 26-RDHS resampling, same within-replicate refit of M5 and M5_no-climate, same past-only rolling-52 recalibration, same evaluation rows, same percentile method. Runtime 4747 s (79 min). **Reproduce-first gate PASSED** (max|Δ| M5 vs frozen = 1.1e-16; conditional matched recal reproduced at +0.01565).

## B=300 vs B=1000, side by side (both contrasts)

| Contrast | Point | Conditional CI | Dev-inclusive **B=300** | Dev-inclusive **B=1000** | Zero (B=1000) |
|---|---|---|---|---|---|
| Raw matched | +0.0087 | [−0.0015, +0.0188] | [−0.0074, +0.0223] | **[−0.0079, +0.0245]** (median +0.0078) | includes |
| Recalibrated matched | +0.0157 | [+0.0066, +0.0257] | [+0.0015, +0.0284] | **[−0.0002, +0.0302]** (median +0.0139) | **includes** |

- Point estimates and conditional CIs are **unchanged** (as required).
- Failures/degenerate replicates: **0 / 1000**.
- **The recalibrated development-inclusive interval crosses zero at B=1000** (lower bound +0.0015 at B=300 → −0.00015 at B=1000). The B=300 exclusion was an artifact of the shallow bootstrap, exactly as suspected. Even the B=1000 interval rests on **26 clusters** and is therefore still finite-cluster-limited.

## Branch: **INCLUDES zero at B=1000 → symmetric-null**
Once model-development uncertainty is included at the paper's standard resampling depth, the Sri Lanka recalibrated matched increment **includes zero**, as the raw increment already did and as Colombia's matched increment does. No matched exclusion is robust across both raw evaluation and model refitting in either setting.
