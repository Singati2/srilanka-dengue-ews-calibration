# Number provenance — WP4 / WP5 manuscript sections v3

Every numeric claim in `wp4_wp5_methods_results_v1.tex`, mapped to the artifact it came from.
Verified by direct recomputation from the quarantined tables on **2026-08-15**; F8 rows added **2026-08-16**; the refit
(`wp5_05b`) and within-M5 fold (`wp4_02b`) rows added **2026-08-20** (not transcribed from
notebook prose). Where a number is quoted in the text, the value in this table is the recomputed one.

**Two provenance classes now coexist in the fragment, and they must not be mixed.** Rows tagged
`FROZEN` come from the study's committed predictions. Rows tagged `REBUILD` come from models
refitted on `data_quarantine/sl_ladder/sl_linked_v2equiv.csv`, an independent reconstruction of the
linked analysis table built here because the committed builder reads Linux-host paths. Every
`REBUILD` claim carries `\REBUILD` in the text and is worded as a sensitivity analysis. The
registered re-runs have **not** been performed.

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
| `SCREEN` | `wp5_f8_modifier_screen_srilanka_v1.csv` (60) + `wp5_miscalibration_structure_srilanka_v1.csv` (26) | " |
| `FLIPSUM` | `wp5_decision_flip_summary_srilanka_v1.csv` (2 rungs × 4 specs × 4 p*) | " |
| `POWER` | `wp4_power_cost_srilanka_v1.csv` | `data_quarantine/wp4_cv/` |
| `MORAN` | `wp4_morans_i_srilanka_v1.csv`, `wp4_variogram_srilanka_v1.csv` | " |
| `FOLD` | `wp4_fold_effect_gap_srilanka_v1.csv`, `..._metrics_...csv` | " |
| `NB-CELL` | a numbered cell output in the named notebook (bootstrap CIs only) | `notebooks_wp45/` |
| `REFIT` | `wp5_05b_refit_metrics_...csv`, `..._refit_flips_...csv`, `..._refit_deltas_bootstrap_...csv`, `..._refit_netbenefit_band_...csv`, `..._knot_sensitivity_...csv`, `..._envelope_vs_refit_...csv`, `..._per_district_flips_...csv`, `..._climate_increment_by_build_...csv` (`REBUILD`) | `data_quarantine/wp5_exposure/` |
| `REFIT-P` | `wp5_05b_refit_predictions_srilanka_v1.csv` — 3,926 rows × 12 prediction columns (4 arms × 3 models) (`REBUILD`) | " |
| `FOLD-M5` | `wp4_02b_fold_effect_m5_gap_...csv`, `..._metrics_...csv`, `..._bootstrap_...csv`, `..._increment_...csv`, `..._per_district_...csv` (`REBUILD`) | `data_quarantine/wp4_cv/` |
| `PROV` | `wp5_05b_provenance.json`, `wp4_02b_provenance.json` — gates, design, seeds | both quarantine dirs |

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

## Results — refit under each build (§ results-wp5-refit) — `REBUILD`

Source: `wp5_05b_decision_sensitivity_refit.ipynb`, 20/20 QC, seed 20260612, env
`/Users/mpcr/aj/Dengue/.venv` (Python 3.14.7, sklearn 1.9.0 — the only environment here that
reproduces the ladder baseline `sl_04` to 0.0). M5 = published specification (district FE +
harmonics + nonlinear cross-basis); M4 = no district FE, no harmonics; `matched` = M5's climate-free
twin. Arms: `A_frac` (fractional area), `B_pop` (population), `C_frac` (lapse correction under area
weights = orography only), `C_pop` (lapse correction under population weights = full Build C).

| Claim | Value | Source |
|---|---|---|
| Held-out panel | 3,926 rows (26 × 151) | `REFIT-P` row count |
| AUC, M5, four arms | 0.76532 / 0.76679 / 0.76586 / 0.76498 | `REFIT` metrics |
| AUC total span across arms | **0.0018** | max − min of the above |
| ΔAUC vs A′, M5 | +0.00147 [−0.00078, +0.00375] · +0.00054 [−0.00180, +0.00278] · −0.00033 [−0.00402, +0.00357] | `REFIT` deltas bootstrap |
| ΔNB@0.30 vs A′, M5 | +0.00131 [−0.00149, +0.00433] · −0.00247 [−0.00630, +0.00091] · +0.00040 [−0.00222, +0.00309] | " |
| Δcal. slope vs A′, M5 | **+0.02337 [+0.00521, +0.04237]** · **+0.02354 [+0.00972, +0.03739]** · **+0.03452 [+0.01008, +0.06178]** | " — the only three intervals excluding 0 |
| Δcal. slope vs A′, M4 | +0.00288 · −0.00892 · −0.01944, all spanning 0 | " |
| Cal. slope, M5, four arms | 1.0847 / 1.1081 / 1.1083 / 1.1192 | `REFIT` metrics |
| Flips at p\*=0.30, M5 | **72 (1.83%) · 64 (1.63%) · 121 (3.08%)** | `REFIT` flips |
| Flip direction, M5, p\*=0.30 | B 35 on / 37 off · C-orog 15 on / 49 off · C-full 42 on / 79 off | " |
| Flips at p\*=0.40, M5 | 60 · 67 · 93 (**B and C-orography swap order here**) | " |
| Largest M5 flip rate, any arm/threshold | **3.44%** (C-full, p\*=0.10) | " |
| Swap-path noise floor | **3** flips at p\*=0.30 (1 / 0 / 3 / 1 at 0.10/0.20/0.30/0.40); max |Δp| 1.06e-3 | `PROV` `gates.swap_path_noise_floor_*` |
| Climate-block-removal ceiling, same refit | **427 flips (10.88%)** at p\*=0.30 | **derived** — see recipe below |
| Exposure share of that ceiling | **15.0% – 28.3%** (64/427, 121/427) | derived from the two rows above |
| Climate increment ΔAUC / ΔNB, A′ arm | 0.0330 / 0.01634 | `REFIT` climate-increment table |
| Envelope vs refit, A′→B | 76 est. vs **72** measured (−4) | `REFIT` envelope-vs-refit |
| Envelope vs refit, A′→C | 104 est. vs **121** measured (+17, envelope under-counts) | " |
| Knot sensitivity (per-arm vs fixed at A′) | 72→74 · 64→65 · 121→119 | `REFIT` knot sensitivity |
| B→C flips, cross-basis vs linear temperature | **67 vs 10** (both keep district FE) | `PROV` `results.mechanism` |
| Within-district sd of the B→C offset | 1.5e-6 °C | `wp5_05b` §8 (the premise of the corrected claim) |
| Top flip districts (C-full) | Nuwara Eliya 7.95% · Matale 7.28% · Badulla 6.62% · Matara 5.96% · Ratnapura 5.30% | `REFIT` per-district |
| corr(flips, \|Build C offset\|) | **r = +0.66** (Pearson, n = 26) | " |
| Matale's rank on offset magnitude | **7th** (0.212 °C) while 2nd on flips | " |
| Baseline gate | M5 and twin reproduce `sl_04` to **0.0** | `PROV` `gates` |
| No-climate invariance across arms | **0.0** (bit-identical, all four arms) | " |
| Build A′ agreement with WP5's independent build | 1.8e-5 °C (T), 4.2e-6 mm (precip), 3.2e-4 pp (RH) | " |

> **The 427 is the only number in this file computed in the write-up rather than in a notebook.**
> Recipe, one pass over `REFIT-P`: `sum((p_A_frac_M5 >= 0.30) != (p_A_frac_matched >= 0.30))` = 427
> of 3,926 = 10.88%. It exists because the fragment's earlier "14–24% of the climate block's decision
> leverage" divides envelope flip counts by the **frozen** ceiling of 441; quoting refit flips against
> a frozen ceiling would mix the two provenance classes. At p\* = 0.10/0.20/0.40 the same rule gives
> 688 / 545 / 400.

> **Do not quote M4's flip counts as a robustness result.** M4 flips *more* (95 / 84 / 140 at
> p\*=0.30), not less, and its calibration deltas reverse sign. M4 is in the design to show that the
> calibration movement is specific to the published specification, not to establish a range.

> **The aggregation hazard that dominates the exposure tables does not bite here.** Every district
> contributes exactly 151 held-out weeks, so the national flip percentage and the mean of the 26
> per-district percentages coincide at 3.08%. That is a property of this balanced panel, not a general
> licence: it stops holding the moment a district is dropped or the panel is re-cut.

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

## Results — where miscalibration concentrates (§ results-wp5-f8)

Source: `wp5_07_miscalibration_structure_and_F8.ipynb`, 16/16 QC. Responses computed per district
from `ENVELOPE` (26 × 151); modifiers from `M6` batch A/B; screen written to
`wp5_f8_modifier_screen_srilanka_v1.csv` (60 rows) and the joined design to
`wp5_miscalibration_structure_srilanka_v1.csv` (26 rows).

| Claim | Value | Source |
|---|---|---|
| Tests run / raw p<0.05 / survive FDR | **60 / 19 / 6** | screen CSV |
| Calibration slope range across districts | **0.67 – 2.23** | `wp5_07` §2 |
| cal. intercept ~ alert prevalence | ρ = **0.854**, q < 0.001 | screen CSV |
| cal. slope ~ cropland fraction | ρ = **0.606**, q = 0.031 | " |
| cal. slope ~ land-cover diversity | ρ = **0.588**, q = 0.032 | " |
| cal. slope ~ population density | ρ = **−0.495**, q = 0.066 (raw p = 0.010) | " |
| flip rate ~ slope | ρ = **0.560**, q = 0.035 | " |
| flip rate ~ elevation | ρ = **0.560**, q = 0.035 | " |
| flip rate ~ HAND | ρ = **0.548**, q = 0.038 | " |
| Partial, cal. slope ~ cropland \| prevalence | ρ = **0.497**, p = 0.010 | `wp5_07` §5a |
| Partial, cal. slope ~ diversity \| prevalence | ρ = 0.492, p = 0.011 | " |
| Partial, cal. slope ~ pop. density \| prevalence | ρ = −0.439, p = 0.025 | " |
| corr(elevation, \|B→C\| displacement) | ρ = **0.744** | `wp5_07` §5b |
| Partial, flips ~ elevation \| displacement | ρ = 0.269, **p = 0.184** | " |
| Partial, flips ~ displacement \| elevation | ρ = 0.047, **p = 0.820** | " |
| Top flip districts | Badulla 9.9%, Nuwara Eliya 9.3%, Ratnapura 6.0% | `wp5_07` §7 |
| ΔNB strongest of 15 modifiers | population density, ρ = **0.402**, q = **0.150** | screen CSV |

> **The prevalence decoy is load-bearing.** `prev` is in the modifier panel deliberately and is not a
> geospatial variable. It produced the largest association in the screen, which is near-tautological
> (a district's calibration intercept absorbs its base rate). Removing it would not have removed the
> problem — it would have hidden it, and any modifier correlated with outbreak burden would have
> inherited the association silently.

> **The flip concentration is not attributed.** Elevation and the measured B→C displacement are
> collinear at ρ = 0.74 across 26 districts, and neither partial correlation survives. The prose says
> flips concentrate in high, steep districts and stops there. Do not let a later revision upgrade this
> to "terrain drives the flips".

> **Ranked-by vs labelled-with, panel (b).** The map labels the three districts with the largest
> |slope − 1| but prints the slope itself (Puttalam 2.23, Killinochchi 1.95, Kurunegala 1.89). Checking
> the labels against a ranking of raw `cal_slope` will agree here, but the ranking column is the
> deviation.

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

### The same measurement on the published specification — `REBUILD`

Source: `wp4_02b_fold_effect_within_m5.ipynb`, 17/17 QC, seed 20260612, same `.venv` as `wp5_05b`,
2,912 fold-fits (M5 and its climate-free twin, 4 arms × 5 radii × 26 folds + 10 control draws).
150 km is excluded: `wp4_00` records 12 degenerate folds there.

| Claim | Value | Source |
|---|---|---|
| Temporal-split AUC, M5 | 0.7652 | `FOLD-M5` metrics |
| LOOCV unbuffered AUC, M5 | 0.7201 (**below** buffered 0 km — unexplained, see note) | " |
| Buffered AUC, 0/25/50/75/100 km | 0.7430 / 0.7355 / 0.7095 / 0.6624 / 0.6672 | " |
| Matched-control mean AUC | 0.7051 / 0.7116 / 0.7065 / 0.7163 / 0.6946 | `FOLD-M5` gap |
| Train units (median over folds) | 21 / 19 / 15 / 12 / 9 | `FOLD-M5` gap — **not** the metrics file's mean |
| Gap (buffered − control) | **+0.0379 / +0.0238 / +0.0030 / −0.0539 / −0.0274** | " |
| Controls scoring below buffered | 10/10 · 9/10 · 6/10 · 0/10 · 2/10 | `FOLD-M5.pct_controls_below` |
| Control-draw z at 0 km | +2.57 (yet the bootstrap CI spans zero) | " |
| Bootstrap gap ΔAUC, 75 km | **−0.0532 [−0.0916, −0.0157]** — the only radius excluding 0 | `FOLD-M5` bootstrap |
| Bootstrap gap ΔAUC, 0 / 25 / 50 / 100 km | +0.0370 [−0.0116,+0.1107] · +0.0229 [−0.0214,+0.0800] · +0.0024 [−0.0386,+0.0535] · −0.0277 [−0.0868,+0.0287] | " |
| Bootstrap gap ΔNB@0.30, 75 km | **−0.0296 [−0.0489, −0.0129]** | " |
| Bootstrap gap ΔNB@0.30, 100 km | −0.0197 [−0.0436, **+0.0037**] — spans zero | " |
| Calibration slope gradient, M5 | 1.084 (temporal) → 0.721 (0 km) → 0.230 (100 km) | `FOLD-M5` metrics |
| Climate increment ΔNB@0.30, temporal | +0.0166 | `FOLD-M5` increment |
| Climate increment under buffering | +0.0091 / +0.0148 / +0.0155 / +0.0091 / +0.0159 | " |
| Change vs temporal, all radii | −0.0071 · −0.0015 · −0.0008 · −0.0075 · −0.0007, **every CI spans 0** | `FOLD-M5` increment bootstrap |
| Twin's gap across radii (flat) | +0.0072 / +0.0166 / +0.0005 / −0.0040 / −0.0154 | `FOLD-M5` gap, `matched` rows |
| Districts with negative gap | 15/26 (0 km) · 17 · 20 · 20 · 20/26 (100 km) | `FOLD-M5` per-district |
| Gates | label agreement 0.9880 vs frozen; corr 0.9752 (full) / 0.9758 (twin); baseline vs `sl_04` **0.0** | `PROV` |

> **Train units come from the gap file, not the metrics file.** The gap file reports the *median*
> training-set size over the 26 folds (50 km: 15); the metrics file reports the *mean* (15.5). Table
> `wp4-fold` quotes the median, so `wp4-fold-m5` must too --- the two tables are printed to be read
> against each other. The verifier caught this after the first draft of the table used 15.5.

> **Two point estimates exist for each gap and the fragment quotes the direct one.** The gap table's
> `auc_gap` is the full-sample buffered − control-mean difference (75 km: −0.0539); the bootstrap's
> `dAUC` is the mean over 2,000 replicates with the control ensemble averaged inside each replicate
> (−0.0532). The tables and prose quote the **full-sample** point with the bootstrap percentile
> interval — the standard pairing, and the same convention as Table `wp4-fold` — so the printed gaps
> are +0.038 / +0.024 / +0.003 / −0.054 / −0.027. Checked against the bootstrap `point` column
> instead they disagree in the third decimal at four of the five radii (+0.037 / +0.023 / +0.002 /
> −0.053 / −0.028). That is a difference between two estimators of the same quantity, not a defect;
> recompute against the `FOLD-M5` **gap** file, not the bootstrap file.

> **The LOOCV inversion is unexplained and is flagged, not smoothed.** M5 scores 0.720 under
> unbuffered leave-one-out and 0.743 under adjacency buffering, despite the latter training on four
> fewer districts. The estimand is unaffected — the matched control holds training size fixed by
> construction — but the fragment says so in the text rather than omitting the LOOCV row. Do not let a
> revision quietly drop it.

> **Never quote the control-draw z as the test.** At 0 km all ten controls fall below the buffered
> fold (z = +2.57) while the bootstrap interval spans zero. The draws sample the control set with the
> 26 districts fixed; the bootstrap resamples the districts, which is the inference the claim needs.

---

## Not in these sections, and why

| Quantity | Status |
|---|---|
| The **registered** re-runs, either of them | **Still outstanding.** The "blocked on the §5.1 design matrices" framing was withdrawn on 2026-08-18: the builders are in `analysis/v12_referee_response/run/sl_matched_and_recal.py` and reproduce frozen M1/M4/M5 to <1e-6. What is missing is the linked analysis table, whose builder reads Linux-host paths. Both analyses are reported here on a **rebuilt** input, marked `\REBUILD`, and must never be described as the registered re-run. |
| ΔAUC, Δcalibration under Builds B/C on the **frozen** input | Not available here — see the row above. The `REFIT` rows are the rebuild version. |
| M0/M1/M2 under spatial folds | Not run. `wp4_02` covers the geomatics-only model and `wp4_02b` the published specification; the intermediate ladder rungs were not refitted under the folds. |
| ΔNB under each population product | Not run. `wp5_05b` varies the **construction**, not the population product. The fragment says so and offers an inference from the exposure ratios instead, explicitly labelled as not a measurement. |
| Any Colombia figure | Out of scope, and now permanently: the Colombia block CV was **withdrawn from the study** on 2026-08-17, not deferred. The n=26 limitation has no companion analysis coming and is written as a limitation, not as future work. |
| Any absolute AUC for the geomatics-only model | Barred by the reconstructed-target caveat (19.2% of test rows). Only *between-arm* contrasts are quoted. |
| Which districts warm under A′→B temperature | Barred by grid attenuation (Ratnapura retains 6.7%). Per-district temperature claims are made only for B→C, which is not attenuated the same way. |
| ΔAUC / Δcalibration **per district** under Builds B/C | Not estimated. F8 uses the *frozen* predictions, so it maps where the existing model is miscalibrated, not how each build changes that; the refit reports per-district **flips** but not per-district discrimination or calibration deltas, which 151 rows per district will not support. |

## Recomputation

```bash
# district-week displacements, flips, AUCs, fold gaps
/Users/mpcr/aj/WMP/pywmp/pywmp-main/.venv/bin/python   # wp5_* tables (no sklearn)
/Users/mpcr/aj/Rhee/0_EDA/.venv/bin/python             # anything needing roc_auc_score
/Users/mpcr/aj/Dengue/.venv/bin/python                 # wp4_02b and wp5_05b (refits)

# the one number derived in the write-up rather than in a notebook
python3 - <<'PY'
import csv
rows = list(csv.DictReader(open(
    'data_quarantine/wp5_exposure/wp5_05b_refit_predictions_srilanka_v1.csv')))
flips = sum((float(r['p_A_frac_M5']) >= 0.30) != (float(r['p_A_frac_matched']) >= 0.30)
            for r in rows)
print(flips, len(rows), 100 * flips / len(rows))     # 427 3926 10.876...
PY

# structural check on the fragment (no LaTeX toolchain here)
python3 scripts/check_wp45_fragment.py
```

The three-kernel split is not incidental: `pywmp-mac` has no scikit-learn, `freight-eda` has no
raster stack, and only `/Users/mpcr/aj/Dengue/.venv` has the sklearn/patsy/statsmodels combination
that reproduces the ladder baseline to 0.0. `wp5_*` runs on the first, `wp4_02` and any AUC
recomputation on the second, both refit notebooks on the third.

**Known non-reproducible column:** relative humidity is the only variable computed through `exp()` in
float32 and reproduces to 1.65e-5 pp (2.2 float32 ULP) rather than bit-exactly across NumPy builds.
The temperature columns reproduce to 1e-14. This is 2,000× below the smallest effect reported; an
acceptance test must encode the tolerance rather than fail mysteriously.
