# Path B — Decision Memo (Stage 2)

*Run 2026-07-08 in the exact original Colombia pipeline (`scripts/colombia_model_ladder_h4_75pct_v1.py`, sha256 `0d88ea02…`), reusing its design/fit/recalibration/bootstrap verbatim and adding only `M5_no_climate_matched=['cases','season','dept']`. Read-only inputs; outputs under this `run/` dir. **No manuscript edited; nothing staged/committed/pushed.** For author + PI review.*

Interpretation rules applied as approved: ±0.005 is an **internal descriptive reference band, not a validated equivalence margin**; a *strong* negligible-effect conclusion requires the **full 95% CI** inside [−0.005, +0.005]; M4−M1 reported separately; climate is not declared to "have no predictive value."

## Answers to the ten required questions

1. **Did the original pipeline reproduce +0.0188?** **Yes (Gate A PASS).** ΔNB(M5−M1)@0.30 = **+0.01878** (frozen +0.018775; |Δ| = 5e-6 ≤ 0.001), ΔAUC +0.0403, bootstrap 95% CI **[+0.0117, +0.0260]** (frozen [+0.0117, +0.0260]).

2. **Were original M1 and M5 structurally unmatched?** **Yes.** M1 = 4 features (cases only). M5 = 58 (4 cases + 18 climate + 4 season + **32 department fixed effects**). M5 carries season and department fixed effects that M1 entirely lacks — the M5−M1 contrast is **not baseline-matched**.

3. **Did the matched baseline remove only climate terms?** **Yes (Gate B PASS).** `M5_no_climate_matched` (40 features) = M5 minus exactly the 18 climate columns (`precip_lag0–8`, `temp_lag0–8`); all cases, season, and 32 department fixed effects, plus rows/scaling/penalty/recalibration, identical.

4. **What is `M5 − matched baseline` (climate net of matched structure)?** **+0.00783.**

5. **Its 95% interval?** **[+0.0039, +0.0119]** (paired GID_2 cluster bootstrap, seed 20260612, B=1000, 0 failures). The interval **excludes 0** and its point estimate and upper half lie **outside** the ±0.005 reference band.

6. **How much of +0.0188 is non-climate structure?** ΔNB(matched − M1) = **+0.01095 [+0.0060, +0.0164]** ≈ **58%** of the +0.0188 is season + department fixed effects; the remaining **≈42% (+0.00783)** is climate net of that structure. (NB levels: M1 +0.1171, matched +0.1280, M5 +0.1358.)

7. **Is the matched climate increment inside the approved negligible band?** **No.** Point +0.00783 > +0.005, and the full CI [+0.0039, +0.0119] extends above +0.005. → **not** a strong negligible-effect conclusion; classify as **small but non-negligible, and estimated with modest precision.**

8. **Does the original climate-hybrid interpretation remain defensible?** **Partially, but the headline overstates climate.** Climate does retain a small increment (+0.0078, CI excludes 0) net of matched fixed effects, so it is **not** pure spatial-baseline confounding. However, the reported **+0.0188 conflates climate with unmatched season + department fixed effects** (~58% of it), so presenting +0.0188 as "the climate-hybrid increment" **overstates the climate contribution by ~2.4×** and should be corrected to the matched value.

9. **Is Path A authorized?** **NO — not as a pure null reframe.** Gate D outcome (2) applies (matched climate increment materially positive). Do **not** reframe the paper to "climate adds no value." A **nuanced partial correction** is warranted (see Q10), subject to author + PI review.

10. **What manuscript sentences would need revision?** (Proposed language only — NOT applied.)
   - Where the abstract/results state climate "may add a modest increment" of **+0.0188**: revise to *"After matching the surveillance baseline for seasonality and department fixed effects, the climate increment was ΔNB = +0.0078 (95% CI +0.0039 to +0.0119); roughly 58% of the unadjusted +0.0188 M5−M1 difference was attributable to non-climate structure (seasonality and department fixed effects) that the recent-case baseline lacked."*
   - Add a limitation: *"The primary M5−M1 comparison was not baseline-matched (M5 carried department fixed effects absent from M1); the matched climate increment is smaller."*
   - Cross-reference the spatial-transportability result (below).

## Reconciliation with the spatial-CV result (both true, not contradictory)
- **This (Path B, temporal holdout):** climate net of matched fixed effects = **+0.0078 [+0.0039, +0.0119]** — small, positive, in-sample/temporal.
- **Earlier leave-one-department-out spatial CV:** ΔNB(M5−M1) = **−0.0007 [−0.0104, +0.0098]** — the advantage does **not transport** across departments.
- Honest synthesis: on the temporal holdout climate retains a small real increment, **but** it (and the larger fixed-effect component) does **not generalize to unseen departments**. Following the approval note (Q from rule 5), the small matched climate increment may reflect climate **proxying seasonal/geographic structure** rather than a transportable causal signal — not proof climate is worthless.

## Verdict
The prior +0.0188 is **specification-confounded, not fraudulent**: ~58% non-climate structure, ~42% a genuine but small climate increment (CI excludes 0). **Path A (null reframe) is NOT authorized.** Recommended: a **corrected, matched framing** (climate ≈ +0.008 net of fixed effects; +0.0188 overstates it) plus the non-transportability caveat — **for author + PI decision.** No manuscript change made. **STOP for review.**
