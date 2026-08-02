# Colombia model ladder M0–M7 — comparison (geo/SPI pilot)

> **STATUS: PILOT — NOT A QUOTABLE RESULT.** Quarantine-derived, pipeline-debugging run.
> `analysis_plan_v2.md` Part I is **not yet frozen/preregistered**. Do not cite these numbers
> in the manuscript until the confirmatory run under the frozen plan. See "Caveats" below.

All eight models were fit and scored in a **single run on one identical row set** (the
M6-inclusive shared mask), so every metric is directly comparable across the ladder.

## Design (identical for all models)

| Element | Value |
|---|---|
| Setting / unit | Colombia, municipality (GID_2) × epi-week |
| Label | elevated activity, 75th-pct level, **h = 4 weeks** |
| Rows (shared mask) | **79,128** — train 53,108 / val 12,700 / test 13,320 |
| Estimator | L2 logistic regression; `C` tuned on validation log-loss |
| Preprocessing | continuous features standardized on **train stats only** |
| Recalibration | Platt on validation; **test scored once** |
| Reference threshold | p\* = 0.30 (net benefit) |
| Uncertainty | GID_2 cluster bootstrap, **seed 20260612, B = 1000** |

**Shared mask** = `common_complete_M1_to_M5_h4` ∧ SPI-features-present (657 cc rows dropped for
short precip history, 0.82%, applied uniformly to all eight models). Frozen full-`cc` M0–M5
artifacts are untouched; here M0–M5 are re-fit on the shared mask so the 8-way comparison is fair.

## Results — TEST set, recalibrated

| Model | Features | AUC [95% CI] | PR-AUC | Brier | CITL | slope | NB@0.30 [95% CI] | ΔNB vs M1 [95% CI] |
|---|---|---|---|---|---|---|---|---|
| M0 | season (Fourier) | 0.514 [0.486, 0.540] | 0.384 | 0.250 | −0.50 | 79.1* | 0.107 [0.059, 0.163] | — |
| **M1** | recent cases (lags 0,1,2,4) | 0.686 [0.644, 0.722] | 0.566 | 0.222 | −0.46 | 1.10 | 0.119 [0.071, 0.175] | reference |
| M2 | climate (precip+temp lags) | 0.554 [0.529, 0.577] | 0.409 | 0.248 | −0.50 | 0.88 | 0.107 | −0.012 [−0.015, −0.008] |
| M3 | climate + season + dept FE | 0.562 [0.534, 0.590] | 0.414 | 0.249 | −0.54 | 1.30 | 0.107 | −0.012 [−0.015, −0.008] |
| M4 | cases + climate | 0.699 [0.658, 0.733] | 0.584 | 0.217 | −0.45 | 1.05 | 0.129 [0.083, 0.184] | +0.010 [+0.005, +0.015] |
| **M5** | cases + climate + season + dept FE | **0.726 [0.686, 0.757]** | **0.607** | **0.213** | −0.51 | 1.16 | **0.136 [0.090, 0.188]** | +0.017 [+0.010, +0.024] |
| M6 | cases + SPI (8/13/26 wk) | 0.645 [0.606, 0.680] | 0.531 | 0.229 | −0.39 | 0.76 | 0.113 [0.068, 0.165] | −0.006 [−0.013, +0.0004] |
| M7 | cases + climate + season + dept FE + SPI | 0.688 [0.652, 0.720] | 0.575 | 0.219 | −0.43 | 0.91 | 0.132 [0.088, 0.182] | +0.012 [+0.003, +0.021] |

\* M0's calibration slope is a degenerate artifact of a near-constant season-only predictor
(present in the frozen ladder too); ignore it.

## Reading

- **M5 is best on every metric.** M1 (recent surveillance) is the strong baseline.
- **Adding the SPI geospatial block does not help.** M6 (cases + SPI) sits *below* M1;
  M7 (M5 + SPI) sits *below* M5. The ΔNB(M6−M1) CI straddles 0.
- Ruled out as causes (see `diagnostics`): not a code bug (M0–M5 reproduce the frozen ladder
  bit-identically; sizes/events/variances sound), and **not multicollinearity** — every single
  SPI scale, fit alone (no SPI–SPI collinearity), still underperforms M1. The signal is weakly
  associated with outbreaks in-sample and does not generalize to the 2020–2022 test era.
- This is a clean **honest-null**, consistent with the paper's thesis (recent surveillance is
  hard to beat) and with `analysis_plan_v2.md` §10.

## Caveats (scope of this comparison)

1. **SPI-only slice.** The intended dynamic geo pool also includes **DTR** and **VPD**, which
   could not be built — Colombia's ERA5 extraction has only daily-mean temperature (no Tmax/Tmin,
   no dewpoint). `derive_dtr`/`derive_vpd` are implemented and gated, awaiting those grids. Read
   M6/M7 as "(+full model) **+ drought index**," not "the full geospatial hybrid."
2. **Use this rowset only.** The generating run also emits a `secondary_climate_full` M2/M3 block
   on a larger row set — that block is **not** comparable to the models here.
3. **Pilot / not frozen.** Governance per `analysis_plan_v2.md`: freeze Part I (repo tag
   `plan_v2_frozen` + OSF) before the confirmatory run. These numbers are for method development.

## Reproduce

```
python3 scripts/colombia_geo_feature_assembly_v1.py      # builds SPI geo block (quarantine)
python3 scripts/colombia_model_ladder_h4_75pct_M6_v1.py  # fits M0–M7, writes artifacts (quarantine)
# then regenerate this table from the artifacts
```

Provenance (seed, C-grid selections, row counts, input checksums): `_provenance.json`.
Raw artifacts (git-ignored, quarantine): `data_quarantine/colombia_model_pilots/model_ladder_h4_75pct_M6_v1/`.
