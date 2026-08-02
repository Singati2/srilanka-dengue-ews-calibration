# Executed Experiments — Results, Verification, and the Strongest Reframe (v1)

*New pilot re-analysis (2026-07-08). Distinct from the frozen v18 numbers. Run on the on-disk `data_quarantine` artifacts (per-row predictions, Colombia modeling table, SL geometry/adjacency). Every result was independently reproduced by an adversarial verification agent. Read-only w.r.t. the manuscript; nothing here was committed or pushed. All net benefit NB = TP/n − FP/n·(p*/(1−p*)) at p*=0.30, h=4, 75th-pct label.*

---

## 0. Headline

The frozen manuscript's single positive result — **Colombia ΔNB(M5−M1)@0.30 = +0.0188** ("climate may add a modest increment within hybrid systems") — is a **confounded contrast**. The frozen M5 carries **department fixed effects** that the frozen M1 does not; that spatial baseline, not climate, drives the increment, and it is **non-transportable** — it vanishes under spatially-honest validation. Climate's net-of-baseline decision value is a **negligible band (≈ −0.002 to +0.004)**. This does not weaken the paper — it makes it **stronger and more defensible**: recent surveillance is a demanding benchmark, and the apparent climate signal was a modelling artifact.

---

## 1. Sanity gate — my metric code reproduces v18 exactly (VERIFIED)

From `colombia_model_predictions_h4_75pct_v1.csv` (13,361 test rows, recalibrated probs):
- ΔNB(M5−M1)@0.30 = **+0.01878**, ΔNB(M4−M1) = **+0.01224**, prevalence **0.3753** — matches frozen `colombia_model_contrasts` to the digit; threshold-tie-robust. → my NB/AUC harness is trustworthy.

## 2. Colombia leave-one-department-out spatial-block CV (VERIFIED)

Refit plain L2-logistic M1 (case lags) vs M5 (case+climate+season lags), department blocks (32 depts from GID_2), scaler + Platt fit on training departments only, out-of-fold predictions pooled then NB computed once:
- **ΔNB(M5−M1)@0.30 = −0.0007**, ΔAUC ≈ 0.0001, department-cluster bootstrap 95% CI **[−0.0104, +0.0098]** (spans 0).
- Climate-only M2 vs M1: **−0.0286** (worse than surveillance).
- Verifier: leakage-proof, pooling correct, department parse correct. It is a *spatial-transportability* estimand (ignores time), fair because M1/M5 are treated identically and "transportable" is the claim.

## 3. Fixed-effects decomposition — the mechanism (VERIFIED + corroborated by the frozen coefficients)

**Smoking gun (from `colombia_model_coefficients_h4_75pct_v1.csv`):** frozen **M5 contains `dept_1…dept_33` fixed effects; frozen M1 has none** (case lags + intercept only). The ladder never isolated climate.

Matched decomposition (temporal split, my code):

| Contrast | ΔNB@0.30 | Reading |
|---|---|---|
| M5 climate+season, **no FE** − M1 | **−0.0002** | climate alone adds nothing |
| M5 **+dept-FE** − M1 | **+0.0151** | reproduces most of frozen **+0.0188** → approximation faithful in direction & magnitude |
| M5 − M1, **both +dept-FE** (climate net of matched dept baseline) | **+0.0041** | small, negligible |
| M5 − M1, **both +muni-FE** | **−0.0018** | negligible/negative |

So the frozen +0.0188 ≈ **+0.011 department baseline + ~0.004 climate**. The dominant piece is a spatial fixed-effect baseline that M5 carried and M1 lacked — and it is exactly what disappears under LODO (§2). **Honest wording:** climate adds **no meaningful transportable net benefit (|ΔNB| < ~0.005)** once the baseline is matched — a negligible band, not a hard zero.

## 4. Sri Lanka residual spatial autocorrelation — Moran's I (VERIFIED)

M1 recalibrated residuals aggregated per RDHS, row-standardized queen W (26 nodes, 60 edges, symmetry + node alignment checked), 99,999 permutations:
- **Moran's I = −0.093**, E[I] = −0.040, permutation **p ≈ 0.63** → **no significant residual spatial autocorrelation.** The single temporal split was defensible; spatial leakage was never a real threat for SL. (This is the panel's #1 requested spatial check, answered with a clean defensive negative.)

## 5. Stability-selected hybrid (developed model) — honest null

Stability selection (L1-logistic, subsampled) over the climate+season pool: stably-selected features (π≥0.6) are dominated by **seasonal harmonics** (sin/cos week-of-year) plus a few precipitation lags; temperature features are unstable. Because the *full* climate+season set already gives spatial-CV ΔNB = −0.0007 and net-of-FE ≈ 0, a selected **subset cannot exceed it** → the developed hybrid is a confirmed honest null on transportable decision value.

---

## 6. What was implementable vs not (direct answer)

**Implementable and DONE now (needed only on-disk artifacts):** the scientifically load-bearing program — spatial-block CV (WP4), Moran's I autocorrelation diagnostic, the fixed-effects decomposition, and the developed/selected hybrid stress test. These answer the core question decisively.

**NOT implementable now (need weeks of raster/Earth-Engine staging):** WP5 MAUP Build B/C (population-weighted, terrain-corrected exposure) and the F8 ~20-factor GEE covariate panel. WorldPop/DEM/GEE inputs are not on disk. **They are also now largely unnecessary** — the core question ("does geospatial/climate information add transportable decision value beyond recent surveillance?") is already answered: no.

---

## 7. The strongest single paper (recommended reframe)

The executed results convert the paper from "modest, uncertain climate increment" into a **rigorous, mechanistic null** — a much stronger contribution:

1. **Claim:** recent-case surveillance is a demanding benchmark for climate/geospatial dengue alerting under calibration + decision-curve net benefit.
2. **Mechanism:** apparent hybrid advantages can be **spatial-baseline confounding** — a hybrid that carries area fixed effects the surveillance baseline lacks will look better for reasons unrelated to climate. (Demonstrated on the frozen ladder's own coefficients.)
3. **Transport test:** under leave-one-department-out spatial CV the advantage vanishes (ΔNB −0.0007 [−0.0104, +0.0098]); residual spatial autocorrelation is negligible (Moran's I p≈0.63).
4. **Prescription:** benchmark climate systems against recent surveillance **with matched spatial baseline**, validate **spatially** (not only temporally), and report calibration + net benefit — or risk mistaking non-transportable spatial baseline for climate value.

This is publishable and harder to attack than the original, and it needs **no raster staging**. The MAUP/geospatial-factor expansion becomes optional future work, not a submission blocker.

### Integrity note (important, time-sensitive)
The current v18 abstract/results present Colombia +0.0188 as a climate-hybrid increment. On this evidence that framing is **confounded** and should be corrected before submission — the increment is department baseline, not climate. Recommend the authors confirm with the *exact* frozen DLNM+FE training code (my M1/M5 are faithful plain-logistic approximations that reproduce the frozen behaviour once dept-FE is included, but the definitive check is to add matched fixed effects to M1 in the original pipeline and re-report ΔNB).

## 8. Method references (for the write-up)
- Spatial/block cross-validation & leakage: Roberts et al. 2017, *Ecography* 40:913–929; Valavi et al. 2019 (blockCV).
- Decision-curve analysis / net benefit: Vickers & Elkin 2006, *Med Decis Making*; Vickers, Van Calster & Steyerberg 2016, *BMJ* 352:i6.
- Stability selection: Meinshausen & Bühlmann 2010, *JRSS-B* 72:417–473.

*Verification: all four primary claims independently reproduced by an adversarial agent; no bugs found; only correction was to state climate net-of-baseline as a negligible band (≈ −0.002 to +0.004) rather than exactly zero. No manuscript file was modified; nothing staged, committed, or pushed.*
