# WP5 — WorldPop coastal sensitivity: fractional vs centre-in-polygon

**Instruction:** `instruction_m6.md` §17 (mandatory) · **Date:** 2026-08-07 · **Scope:** Sri Lanka
**Scripts:** `scripts/wp5_worldpop_coastal_fractional_sensitivity_v1.py` ·
`scripts/wp5_worldpop_coastal_snap_and_exposure_v1.py`
**Outputs (quarantined):** `data_quarantine/wp5_exposure/wp5_worldpop_fractional_sensitivity_*` ·
`wp5_worldpop_coastal_snap_*`

---

## Headline

**§17's premise conflates two different problems, and only one of them is real.**

- **The assignment rule is not the issue.** Fractional/boundary-aware weighting differs from
  centre-in-polygon by a median of **0.007%** of a district's population (max 0.073%), with
  Spearman rank correlation **1.000000** and **zero rank changes**. Boundary-aware weighting is
  not worth adopting for this purpose.
- **The coastline mismatch *is* the issue, and fractional weighting does not fix it.** The
  national shortfall is **1.37%**, and fractional assignment recovers **200 of 292,461 people** —
  0.07% of the gap. The missing population is not partially-covered boundary pixels; it lies
  **wholly outside** every RDHS polygon.
- **It matters for denominators, not for exposure.** Snapping the orphaned population to the
  nearest district adds up to **9.2% to a single district's denominator** (Batticaloa), but moves
  population-weighted temperature exposure by at most **0.0115 °C**.

So: **for WP5's exposure question the coastal shortfall is negligible and may now be described as
such** — §17's condition is met. **For population denominators it is not negligible** and needs a
fix, which is a different remedy than §17 anticipated.

## Method

`centre-in-polygon` assigns each 100 m pixel whole to the district containing its centre — what
notebook 03 and `wp5_00` do. `fractional` splits each pixel's count by its area overlap with each
district; coverage fractions were computed by rasterizing each district at **8×** the native grid
inside its own window and block-averaging, exact to 1/64 of a pixel. Both were run on two products:
the UN-adjusted `ppp` series that feeds WP5's weight field, and the R2025A series used to recover
the M6 thresholds.

## 1. Fractional vs centre-in-polygon — negligible

| | `ppp_2020_UNadj` | `R2025A_2020_CN` |
|---|---|---|
| national raster total | 21,413,250 | 22,481,947 |
| captured, centre-in-polygon | 98.63% | 99.90% |
| captured, fractional | 98.64% | 99.84% |
| per-unit \|Δ\|, median | 58 people (0.007%) | 106 people (0.019%) |
| per-unit \|Δ\|, max | 787 (Batticaloa, 0.073%) | 2,159 (Batticaloa, 0.241%) |
| Spearman rank correlation | 1.000000 | 1.000000 |
| rank changes | 0 | 0 |

Two things follow. First, the difference is far below any plausible effect on a decision threshold.
Second — and more usefully — **fractional assignment does not close the national gap**: 98.63% →
98.64%. Whatever is missing is not a boundary-pixel apportionment problem.

Note also that the R2025A series aligns far better with the RDHS boundaries (0.10% shortfall vs
1.37%). Since R2025A is already the series used for the M6 thresholds, the denominator problem
below is **13× smaller** in the artifact that actually consumes it.

## 2. Where the missing population is

Of `ppp_2020`, **292,461 people (1.37%) in 31,480 pixels fall outside every RDHS polygon.** They sit
a **median 107 m** from the nearest district boundary (max 2,105 m) — one to three pixels. This is a
**land-mask mismatch**: WorldPop's coastline extends slightly seaward of the RDHS polygon coastline,
so entire pixels — centre and area alike — land in the sea as far as the geometry is concerned.
Fractional overlap cannot recover them because their overlap is genuinely zero.

Reassigning each orphaned pixel to its nearest district restores national capture to
**100.0000%**.

## 3. Effect on denominators — material, and concentrated

| RDHS | population (centre) | added by snap | % |
|---|---|---|---|
| **Batticaloa** | 484,852 | 44,470 | **+9.17%** |
| **Puttalam** | 770,447 | 37,005 | **+4.80%** |
| **Jaffna** | 586,565 | 20,958 | **+3.57%** |
| **Galle** | 1,076,314 | 38,131 | **+3.54%** |
| Trincomalee | 403,927 | 10,049 | +2.49% |

Median across all 26 units: **+0.015%**. The effect is entirely coastal and entirely concentrated —
five districts carry essentially all of it.

**This is the part §17 is right to insist on.** A 9% denominator error is not absorbed by within-unit
normalisation, because incidence denominators do not normalise within unit — they scale the whole
series. It propagates anywhere a per-capita rate is formed, including the M6 threshold work, where
the threshold is a fixed *incidence*.

## 4. Effect on exposure — negligible

Propagating the snap through the population-weighted mean elevation and the standard lapse rate —
the same proxy `wp5_00` used, so the numbers are directly comparable:

| RDHS | Δ elevation | Δ temperature |
|---|---|---|
| Matara | −1.77 m | **+0.0115 °C** |
| Galle | −0.93 m | +0.0061 °C |
| Puttalam | −0.78 m | +0.0050 °C |
| Batticaloa | −0.60 m | +0.0039 °C |

Median |ΔT| across units is **0.0000 °C**; the maximum is **0.0115 °C**. For scale, Build B's
population-weighting displacement is **−1.75 to +0.83 °C** — roughly **150× larger** than the worst
coastal artifact.

The reason is straightforward: the orphaned population sits at the same near-sea-level elevation as
the coastal population already inside the polygon, so recovering it barely moves the weighted mean.
The weight field shifts seaward, but seaward is where the retained coastal weight already was.

## 5. Answers to §17's specific questions

| §17 asks | answer |
|---|---|
| median absolute difference | 58 people / 0.007% (fractional vs centre) |
| maximum absolute difference | 787 people / 0.073% (Batticaloa) |
| relative difference | median 0.007%, max 0.073% |
| rank correlation | **1.000000**, zero rank changes |
| most affected RDHS units | Batticaloa, Puttalam, Jaffna, Galle, Trincomalee — all coastal |
| do downstream model results change? | **exposure: no** (≤0.0115 °C). **denominators: yes** for 5 coastal districts, up to +9.2% |

**§17's gate — "only after this analysis may the coastal shortfall be described as negligible, if
supported" — is met for exposure and not met for denominators.**

## 6. Recommendations

1. **Do not adopt fractional weighting for population.** It costs compute and changes nothing
   (rank correlation 1.0). This is a genuine negative result, and it also means `wp5_00`'s weight
   field needs no rebuild on this account.
2. **Do adopt a nearest-district snap for orphaned populated pixels** wherever a population
   *denominator* is formed. It is a two-line change, restores 100.0000% capture, and is defensible
   on validity grounds rather than performance grounds (§18's standard).
3. **Prefer the R2025A series** where a choice exists — its shortfall is 0.10% against `ppp`'s
   1.37%. The M6 threshold work already uses it.
4. **Check the denominator provenance of the frozen incidence series.** The 9.2% Batticaloa figure
   is material for a per-capita rate. If the frozen denominators were built with centre-in-polygon
   on `ppp`, the affected districts' incidence is biased high by up to ~9%, which would shift their
   thresholds. This is worth a targeted check and is **not** something this report can settle — it
   needs the original denominator build.

## 7. Distinct from §18

§18 concerns `all_touched` versus fractional overlap for **coarse climate grids** (ERA5-Land
0.1°), where `wp5_00` measured ~31% of a district's weight misplaced. That is a much larger effect
at a much coarser support and remains open. Nothing here supersedes it: this report is about the
**100 m population layer**, where the same comparison turns out to be negligible.
