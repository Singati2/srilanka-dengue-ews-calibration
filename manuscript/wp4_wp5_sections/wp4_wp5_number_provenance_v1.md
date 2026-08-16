# Number provenance — WP4 / WP5 manuscript sections v1

Every numeric claim in `wp4_wp5_methods_results_v1.tex`, mapped to the artifact it came from.
Verified by direct recomputation from the quarantined tables on **2026-08-15** (not transcribed from
notebook prose). Where a number is quoted in the text, the value in this table is the recomputed one.

**Why this file exists.** The study has been bitten twice by numbers that drifted between an analysis
and the prose describing it. Everything below is recomputable in one pass; the recomputation script
is recorded at the bottom.

**Aggregation level is the main hazard here.** The same displacement has two legitimate values
depending on whether it is averaged over 10,842 district-weeks or over 26 district means. Example:
population weighting moves weekly mean temperature **0.205 °C** per district-week but **0.171 °C**
as a mean of district means. The manuscript sections quote **district-week** values throughout,
except where a per-district figure is explicitly named (e.g. "Nuwara Eliya −1.92 °C"). The
per-district table `wp5_exposure_contrast_srilanka_v1.csv` must not be used to check a district-week
claim.

---

## Sources

| Tag | Artifact | Location |
|---|---|---|
| `PRECIP` | `wp5_precip_exposure_twin_srilanka_v1.csv` (10,842 × 16) | `data_quarantine/wp5_exposure/` |
| `TEMP` | `wp5_temp_exposure_twin_srilanka_v1.csv` (10,842 × 31) | " |
| `BUILDC` | `wp5_buildC_temp_exposure_srilanka_v1.csv` (10,842) | " |
| `CONTRAST` | `wp5_exposure_contrast_srilanka_v1.csv` (26 districts) | " |
| `PRODUCT` | `wp5_population_product_contrast_srilanka_v1.csv` + `..._sensitivity_...csv` | " |
| `STATION` | `wp5_04_station_validation_srilanka.csv` (6 stations) | " |
| `ENVELOPE` | `wp5_decision_flip_envelope_srilanka_v1.csv` (3,926 rows) | " |
| `FLIPSUM` | `wp5_decision_flip_summary_srilanka_v1.csv` (2 rungs × 4 specs × 4 p*) | " |
| `POWER` | `wp4_power_cost_srilanka_v1.csv` | `data_quarantine/wp4_cv/` |
| `MORAN` | `wp4_morans_i_srilanka_v1.csv`, `wp4_variogram_srilanka_v1.csv` | " |
| `FOLD` | `wp4_fold_effect_gap_srilanka_v1.csv`, `..._metrics_...csv` | " |
| `NB-CELL` | a numbered cell output in the named notebook (bootstrap CIs only) | `notebooks_wp45/` |

All quarantine files are gitignored by policy; the notebooks that produce them are committed and
executed with outputs.

---

## Methods section

| Claim in text | Value | Source |
|---|---|---|
| Table dimensions, all builds | 10,842 rows = 26 × 417 ISO weeks | `PRECIP`, `TEMP`, `BUILDC` row counts |
| Exposure window | 2018-01-01 → 2025-12-28 | `PRECIP.week_start/week_end` min/max |
| Grid attenuation, 0.25° vs 0.1° | 65.3% vs 91.7% | `wp5_02` §3 (pre-build calculation from DEM + WorldPop) |
| Effective cells per district | 21.3 / 11.8 → 5.3 / 3.6 | `wp5_02` §3 |
| Ratnapura retains 6.7% of predicted shift | 6.7% | `wp5_02` §8 |
| WorldPop 2020→ drift in weight field | ~1.1% of a typical weight | `wp5_00` §11 |
| ERA5 orography peak vs true | 1,219 m vs 2,524 m | `STATION.z_orog` max; DEM max |
| Lapse rates applied | 6.5 °C/km (T), 1.5 °C/km (Td) | `wp5_04` §4 |
| Bootstrap protocol | 2,000 replicates, RDHS clusters, seed 20260612 | `wp5_05`/`wp4_02` provenance JSON |
| Transfer-coefficient specs | 4 specs, R² 0.27–0.38 | `wp5_05` §6 |

## Results — exposure displacement (§ results-wp5-exposure)

All values are **mean absolute displacement over 10,842 district-weeks** unless noted.

| Claim | Value | Source |
|---|---|---|
| Rainfall A′→B | **3.399 mm/wk** | `PRECIP`: mean\|b_pop − a_frac\| |
| Rainfall, % of mean | **7.91%** (mean weekly rainfall 42.94 mm) | `PRECIP` |
| Rainfall, max single district-week | **72.6 mm** | `PRECIP` |
| Rainfall, signed mean | −0.748 mm/wk | `PRECIP` |
| Mask step A→A′ | **0.763 mm = 1.78%** | `PRECIP`: mean\|a_frac − a_alltouched\| |
| Wettest decile (n=1,085) | 8.56 mm, 5.40% of 158.6 mm | `PRECIP`, p90 cut on `a_frac` |
| Wettest percentile (n=109) | 12.89 mm, 4.90% of 263.0 mm | `PRECIP`, p99 cut |
| A′/B correlation, rainfall | 0.9935 | `PRECIP` |
| t2m mean A′→B | **0.2049 °C** (max 1.164) | `TEMP` |
| t2m max A′→B | **0.3874 °C** (max 2.764) | `TEMP` |
| t2m min A′→B | 0.3158 °C (max 2.337) | `TEMP` |
| RH A′→B | **0.769 pp** (max 6.286) | `TEMP` |
| t2m mean B→C | **0.3060 °C** (max 1.917) | `BUILDC` |
| B→C orography component | 0.2232 °C | `CONTRAST.temp_b2c_orography_c` (per-district) |
| B→C sub-grid component | 0.1692 °C | `CONTRAST.temp_b2c_subgrid_c` (per-district) |
| Nuwara Eliya B→C | −1.917 °C | `CONTRAST` |
| Badulla B→C | −1.333 °C | `CONTRAST` |
| Ratnapura B→C | +1.008 °C | `CONTRAST` |
| Nuwara Eliya orography vs sub-grid oppose | −2.26 / +0.34 °C | `wp5_04` §6 |
| Badulla A′→B (largest negative) | −0.856 °C | `CONTRAST` |
| Colombo A′→B (largest positive) | +0.336 °C | `CONTRAST` |
| Colombo rainfall A′→B | −7.30 mm/wk | `CONTRAST` |
| Puttalam rainfall A′→B | +4.37 mm/wk | `CONTRAST` |
| Districts drier / wetter under weighting | **17 down / 9 up** | `PRECIP`, per-district signed mean |
| ρ between \|rainfall\| and \|temp\| displacement | 0.243, p = 0.231 | `CONTRAST`, Spearman |
| Top-five overlap, rainfall vs temperature | 1 district | `CONTRAST` |

> **Correction to the repo README.** `notebooks_wp45/README.md` states "Fifteen districts move down,
> eleven up" for rainfall. The correct count is **17 down, 9 up**, under either baseline arm
> (`a_frac` or `a_alltouched`). The figure does not appear in `wp5_01` itself — it was introduced in
> the README summary. The README has been corrected; no notebook, table or figure is affected.

### Station validation

| Claim | Value | Source |
|---|---|---|
| Nuwara Eliya station elevation / obs / ERA5 / bias | 1,880 m · 16.40 · 21.17 · **+4.77 °C** | `STATION` |
| Four lowland stations (1.8–116 m), bias | −0.36 to −0.42 °C | `STATION` (Kurunegala, Colombo, Puttalam, China Bay) |
| Hambantota excluded from regression | n = 121 days only | `STATION.n_days` |
| Station lapse rate (5 well-sampled) | 6.40 °C/km | `wp5_04` §10 |
| ERA5 between-cell lapse over land | 6.31 °C/km | `wp5_04` §10 |
| Nuwara Eliya population elevation | 1,260 m | `wp5_04` §11 |
| Implied true district mean | 19.82 °C | `wp5_04` §11 |
| Build B / Build C district value and error | 21.89 (+2.07) / 19.98 (+0.15) | `wp5_04` §11 |
| Error removed by Build C | 93% | derived: 1 − 0.15/2.07 |
| TMIN vs TMAX bias | +5.27 / +4.27 °C | `wp5_04` §10 |

## Results — decisions (§ results-wp5-decision)

Held-out panel: 3,926 rows, 26 districts × 151 weeks, 2023-01-02 → 2025-12-15, 1,321 events
(prevalence 0.3365). Verified against `ENVELOPE`.

| Claim | Value | Source |
|---|---|---|
| A′→B flips at p*=0.30, across 4 specs | **35–76 (0.89–1.94%)** | `FLIPSUM` |
| A′→C flips at p*=0.30 | **64–104 (1.63–2.65%)** | `FLIPSUM` |
| Climate block removed, p*=0.30 | **441 (11.23%)** | `ENVELOPE`, recomputed |
| Share of climate-block leverage | 14–24% | derived: (35…104)/441 |
| Bootstrap, A′→B p*=0.30 | 1.936% [1.274, 2.649] | `wp5_05` cell 40 |
| Bootstrap, A′→C p*=0.30 | 2.445% [1.503, 3.566] | " |
| Bootstrap, climate removed | 11.233% [9.398, 13.169] | " |
| Operational translation | ≈26 vs ≈152 alert changes/yr | derived: pct × 26 × 52 |
| Exact flip bound, \|p−p*\|≤0.02 | **6.44% recal (253 rows)**; 6.01% raw (236) | `ENVELOPE`, recomputed |
| \|ΔNB\| across all rungs/specs/thresholds | ≤ **0.00212** raw, ≤ **0.00229** recal | `FLIPSUM` min/max |
| \|ΔNB\| A′→B at p*=0.30 | ≤ 0.00124 | `FLIPSUM` |
| \|ΔNB\| A′→C at p*=0.30 | ≤ 0.00087 | `FLIPSUM` |
| Flip direction, A′→B p*=0.30 | +67 / −9 | `ENVELOPE`, recomputed |
| Flip direction, A′→C p*=0.30 | +70 / −26 | `ENVELOPE`, recomputed |
| Flipped-row event rates (A′→B) | 0.087 / 0.160 / 0.289 / 0.431 | `ENVELOPE`, recomputed |
| corr(flipped-row event rate, p*) | **r = 0.959** (both rungs × 4 thresholds) | `ENVELOPE`, recomputed |
| Transfer coefficient norm spread | 2.3×, R² 0.27–0.38 | `wp5_05` §6 |

> **The `flip_*` columns in `ENVELOPE` are the district-fixed-effects specification.** At p*=0.30
> they give 76 (A′→B) and 96 (A′→C), matching `FLIPSUM`'s `+ district FE` row. A check against the
> `exposure only` row (35 / 64) will disagree and is not an error.

> **Every AUC must name its column.** Recomputed on `ENVELOPE`: **raw 0.7715**, **recalibrated
> 0.7512**, climate-free 0.7513. These differ because the frozen recalibration is a past-only rolling
> 52-week intercept update refitted at each test week, so it is time-varying and re-ranks *across*
> weeks (49.1% of adjacent pairs invert when sorted by the raw prediction) while remaining an exact
> constant logit shift *within* a week. The manuscript's 0.771 is the **raw** column. Flagged to the
> team separately; the sections above avoid quoting a bare AUC for the frozen model.

## Results — population product (§ results-wp5-product)

| Claim | Value | Source |
|---|---|---|
| Weight moved, area→population (ERA5 grid) | **27.50%** mean TV | `wp5_06` cell 21/51 |
| Weight moved, unadj→R2025A | 2.007% | " |
| Weight moved, unadj→GHS-POP | 1.570% | " |
| t2m mean: A′→B vs products | 0.2049 vs 0.0088 / 0.0064 °C | `PRODUCT` |
| t2m max: A′→B vs products | 0.3874 vs 0.0231 / 0.0187 °C | `PRODUCT` |
| RH: A′→B vs products | 0.769 vs 0.0416 / 0.0319 pp | `PRODUCT` |
| Rainfall: A′→B vs products | 3.399 vs 0.2032 / 0.1612 mm | `PRODUCT` |
| Ratio range across variables | **16.7× – 32.1×** | `PRODUCT` |
| Tail ratios | 19.5× wettest 1%, 35.8× hottest 1% | `wp5_06` §7 |
| Districts where product beats weighting | **0 of 26** | `wp5_06` cell 51 |
| Mover rank correlation | 0.985 (R2025A), 0.990 (GHS-POP) | " |
| Version drift vs producer gap | TV 0.0201 vs 0.0157 | `wp5_06` cell 21 |
| Population outside polygons | 1.37% unadj · 0.23% GHS-POP · 0.10% R2025A | `wp5_06` cell 51 |

> On the finer CHIRPS 0.05° grid the same contrasts are 41.3% (area→pop) against 4.78% / 4.74%
> (products) — a ratio of ~8.6× rather than ~14×. The sections quote the ERA5-grid weight figures and
> the exposure-level ratios; if a reviewer asks for the weight ratio on the precipitation grid, it is
> smaller and should be given as such.

## Results — spatial CV (§ results-wp4)

| Claim | Value | Source |
|---|---|---|
| Power table (all radii) | as printed in Table `wp4-power` | `POWER` |
| Retained training district-weeks | 84% (0 km) → 36% (100 km) | `POWER.retained_pct` |
| Degenerate folds at 150 km | 12 of 26 | `POWER` |
| Leakage violations | 0, every radius, every fold | `wp4_00` §7 |
| Moran's I permutation p range | 0.528 – 0.993 | `MORAN` |
| M6 adjacency I | 0.0011, p = 0.993 | `MORAN` |
| Permutation null sd at adjacency | 0.019 – 0.023 | `MORAN.null_sd` |
| Variogram flat range | 0.149 – 0.164 semivariance, 0–400 km | `MORAN` (variogram file) |
| Temporal-split AUC | 0.6008 | `FOLD` metrics |
| LOOCV unbuffered AUC | 0.5923 | " |
| Buffered / control / gap, all radii | as printed in Table `wp4-fold` | `FOLD` gap file |
| Calibration slope gradient | 0.875 → 0.529 (0 km) → 0.018 (100 km) | `FOLD` metrics |
| Controls scoring below buffered | 0/10, 1/10, 2/10, 0/10, 0/10 | `FOLD.pct_controls_below` |
| Bootstrap gap, 0 km | −0.0217 [−0.0547, +0.0109] | `wp4_02` cell 32 |
| Bootstrap gap, 75 km | −0.0610 [−0.1186, −0.0081] | " |
| Bootstrap gap, 100 km | −0.0678 [−0.1433, −0.0010] | " |
| Districts losing / gaining AUC at 0 km | 17 / 9 | `wp4_02` §12 |
| Total model fits | 1,456 | `wp4_02` §8 |
| Baseline reproduces committed M6 | 8.6e-15 | `wp4_02` §3 |
| Label reproduces frozen outcomes | 3,926 / 3,926 | `wp4_02` §2 |
| Exploratory-target caveat coverage | 19.2% of test rows | `instruction_m6.md` §22 |

---

## Not in these sections, and why

| Quantity | Status |
|---|---|
| ΔAUC, Δcalibration under Builds B/C | **Blocked** — needs design matrices (§5.1). Marked `\REGBLOCK`. |
| M0/M1/M2/M5 under spatial folds | **Blocked** — same. Marked `\REGBLOCK`. |
| ΔNB under each population product | **Blocked** — same. |
| Any Colombia figure | Out of scope for the Sri Lanka analysis; the block CV over ~1,000 municipalities is where the well-powered spatial claim rests. |
| Any absolute AUC for the geomatics-only model | Barred by the reconstructed-target caveat (19.2% of test rows). Only *between-arm* contrasts are quoted. |
| Which districts warm under A′→B temperature | Barred by grid attenuation (Ratnapura retains 6.7%). Per-district temperature claims are made only for B→C, which is not attenuated the same way. |
| Figure F8 (miscalibration map) | Not built — plan §3.6, downstream of the blocked refit. |

## Recomputation

```bash
# district-week displacements, flips, AUCs, fold gaps
/Users/mpcr/aj/WMP/pywmp/pywmp-main/.venv/bin/python   # wp5_* tables (no sklearn)
/Users/mpcr/aj/Rhee/0_EDA/.venv/bin/python             # anything needing roc_auc_score
```

The two-kernel split is not incidental: `pywmp-mac` has no scikit-learn and `freight-eda` has no
raster stack. `wp5_*` runs on the first, `wp4_02` and any AUC recomputation on the second.

**Known non-reproducible column:** relative humidity is the only variable computed through `exp()` in
float32 and reproduces to 1.65e-5 pp (2.2 float32 ULP) rather than bit-exactly across NumPy builds.
The temperature columns reproduce to 1e-14. This is 2,000× below the smallest effect reported; an
acceptance test must encode the tolerance rather than fail mysteriously.
