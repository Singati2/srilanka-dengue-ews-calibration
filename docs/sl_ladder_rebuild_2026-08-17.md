# Independent Sri Lanka M0–M5 rebuild — findings

**Date:** 2026-08-17 · **By:** Geospatial Lead · **Code:** `notebooks_sl_ladder/` (6 notebooks, all executed)
**Gate target:** `ALT_STATS/frozen/srilanka_matched_pairs.csv` (3,926 frozen test predictions)

> ### CORRECTED 2026-08-18 — the first run's rainfall column was mirrored north-to-south
>
> `sl_01` indexed the staged CHIRPS window with `ai = cell_row − min(cell_row)`. `cell_row` is
> **raster order (north-down)**; the staged array is stored in the netCDF's **latitude-ascending
> (south-up)** order. Every district therefore received its north–south mirror image's rainfall —
> Galle got Killinochchi's, Colombo got Mannar's, Ratnapura got Mullaitivu's. **Only 3 of 26
> districts got their own.** The existing bbox assert could not see it: a flipped index range is
> identical, so the check passed on a completely wrong table.
>
> **This is the exact trap the study recorded on 2026-08-12** (`i = 1999 − row`) while building WP5's
> precipitation twin. The rebuild walked into it anyway, three notebooks later, because the trap was
> written down as a CHIRPS-*reader* note and this was a CHIRPS-*consumer*.
>
> Fixed in `sl_01`, which now carries two gates that would have caught it: a **geographic**
> one (the southwest wet zone must out-rain the northern dry zone — it now reads Kalutara 3,821 mm
> against Killinochchi 996 mm) and a **cross-check against `wp5_01`'s independently-built Build A′**,
> which now agrees to **4.2e-6 mm**. All numbers below are from the corrected re-run; the superseded
> values are shown alongside so the size of the error is on the record.

---

## What was asked, and what was actually possible

The ask was a Sri Lanka-only replication of the M0–M5 ladder, from scratch, in Jupyter, on this Mac —
with the expectation that a CDS API key would first be needed for ERA5-Land 0.1°.

**The key turned out not to be a prerequisite for building the pipeline.** WP5 had already cached an
ERA5 0.25° window, CHIRPS 0.05°, and — critically — the per-district **grid cell weight files**
(`w_area`, `w_pop`). Those weights are what normally requires the RDHS boundary polygons, which are
*not* on this machine. With them, the whole path runs today on a coarser reanalysis product.

So the series was built and executed end to end. What the key would buy is now a measured quantity
rather than an unknown (§4).

---

## Result: the gate

| Model | mean \|Δp\| | max \|Δp\| | corr. with frozen | *(superseded, mirrored)* |
|---|---|---|---|---|
| M5 no-climate | 0.0256 | 0.2607 | **0.9758** | 0.9758 — unaffected, it has no climate block |
| M5 full | 0.0335 | 0.2647 | **0.9752** | *was 0.8810* |

The two arms now agree to within 0.0006 of each other. That is the tell: M5-full and M5-no-climate
differ **only** in the climate block, so a full-model correlation far below the no-climate one was
never a product story — it was a defect. See §4, which the correction rewrites.

Cohort reconciliation:

| | Rebuild | Frozen | |
|---|---|---|---|
| Analysis rows | 10,490 | 10,516 | −26, fully explained |
| Test rows | **3,926** | **3,926** | exact |
| Test prevalence | 0.3372 | 0.3365 | |
| Label agreement | 0.9880 | — | 48 disagreements |
| Matched raw ΔNB | **+0.0166** | **+0.0087** | same sign; the rebuild now *overshoots* (was +0.0071 mirrored) |

The 26-row shortfall is one week: the recovered week offset (§2) pushes the first 2018 reporting week
to 2017-12-25, and the cached grids start 2018-01-01. Nothing else is unaccounted for.

---

## 1. Two undocumented conventions, recovered empirically

The frozen ladder script reads a linked table built on the Linux box. Two choices inside that build
appear in neither the code nor the Methods. Both were recovered by sweeping candidates against the
frozen labels (`sl_03`), not guessed.

**Week offset.** `week_start = ISO_Monday(y, w) − 7d`. The obvious mapping scores 0.820 label
agreement; the shifted one scores **0.988**, and the peak is sharp:

| shift | −2 | **−1** | 0 | +1 | +2 |
|---|---|---|---|---|---|
| agreement | 0.829 | **0.988** | 0.824 | 0.805 | 0.776 |

Reads as the WER bulletin labelled week *w* carrying the week that has just ended.

**Population denominator.** Time-invariant per district (0.988) rather than year-varying (0.986).
This also explains why only 2018–2020 WorldPop is staged locally: a constant denominator makes the
within-district quantile label scale-invariant, so the missing years never mattered.

**These are worth recording in the study's own documentation regardless of this rebuild.** Anyone
re-deriving the Sri Lanka table from the WER — a referee, or the group after the current data
custodian moves on — will hit exactly this and has nothing to guide them.

---

## 2. The residual 1.2% is boundary noise, not a hidden error

48 of 3,926 labels disagree. **All 48 sit within 15% of their district's threshold.** They are spread
across 2023–2025 and concentrate mildly in LK91 and LK32. That is the signature of rows sitting on
the threshold where any small difference in the case series flips the label — not of a systematic
construction error still unfound.

---

## 3. The ladder

| Model | AUC | Brier | NB@0.30 | Provenance |
|---|---|---|---|---|
| Model | AUC | Brier | NB@0.30 | Provenance | *AUC when mirrored* |
|---|---|---|---|---|---|
| M0 | 0.6220 | 0.2254 | 0.0652 | reimplementation | 0.6220 (no climate) |
| M1 | 0.7325 | 0.1993 | 0.1220 | **ported** | 0.7325 (no climate) |
| M2 | 0.7034 | 0.2059 | 0.1022 | reimplementation | *0.6422* |
| M3 | 0.7204 | 0.2035 | 0.1107 | reimplementation | *0.6735* |
| M4 | 0.7604 | 0.1913 | 0.1290 | **ported** | *0.7190* |
| M5 | 0.7652 | 0.1870 | 0.1389 | **ported** | *0.7570* |
| M5_no-climate | 0.7323 | 0.1994 | 0.1223 | **ported** | 0.7323 (no climate) |

Manuscript comparators: M1 AUC 0.752 / NB 0.137, M2 NB 0.069, M3 NB 0.078. The rebuilt ladder is
ordered identically and sits slightly low throughout, consistent with the coarser exposure.

**Every climate-carrying model moved and no climate-free model did** — M2 by +0.061 AUC, M3 by
+0.047, M4 by +0.041 — which is the signature of the defect and a useful diagnostic in its own right:
*if a data error is real, the models that cannot see the data must not move.*

Matched increment with district-cluster bootstrap (`sl_05`):

- **Rebuild:** +0.0166 [+0.0055, +0.0293], B=2000, conditional *(mirrored run gave +0.0071 [−0.0041, +0.0198])*
- **Frozen:** +0.0087 [−0.0079, +0.0245], B=1000, development-inclusive

**The correction changes this reading and the earlier version of this document overstated the
agreement.** Corrected, the rebuild's increment is roughly **twice** the frozen one and its
conditional interval **excludes zero**, where the frozen development-inclusive interval covers it.
The honest summary is now: *the sign and the order of magnitude replicate; the magnitude does not
match, and the rebuild is the more favourable of the two.*

Two reasons not to read that as a challenge to the frozen result, and they are not interchangeable:

1. **The intervals are not comparable.** The rebuild's is conditional on one fitted pipeline; the
   frozen study's is development-inclusive, which folds in model-selection variability and is
   therefore wider and more honest. A conditional interval excluding zero is a weaker statement than
   it looks.
2. **The exposure is a different product**, ERA5 0.25° area-weighted against the frozen build's.
   A rebuild that lands *above* the original is no more evidence of an understated original than a
   rebuild landing below would have been evidence of an overstated one.

What can be said plainly: **the deflationary conclusion is not overturned, and the direction of the
climate block's contribution replicates through an independent path.**

---

## 4. What a CDS key would now buy

**This section's original argument was wrong, and the correction is the point.** It read the
0.976 → 0.881 correlation drop as the measured cost of ERA5 0.25° in place of ERA5-Land 0.1°, and
concluded a CDS key would buy back most of it. Corrected, the full-model correlation is **0.9752**
against the no-climate arm's **0.9758** — the gap is **0.0006**, not 0.095. **Essentially all of what
was attributed to the coarser product was the mirrored rainfall column.**

The transferable lesson is not about CHIRPS. *A defect was absorbed by the most plausible
explanation available* — an exposure substitution the team already knew was in play, sitting exactly
where the discrepancy appeared. The reasoning was sound; that is what made it dangerous. The check
that broke it was cheap and structural: **M5-full and M5-no-climate differ only in the climate block,
so their correlations with the frozen run cannot diverge by 0.095 unless something is wrong with the
climate block itself.** Ask what a discrepancy *cannot* be before accepting what it plausibly is.

What a CDS key would buy is therefore now **unmeasured, not measured**. The remaining gap to the
frozen run is small and no longer decomposed.

The other genuinely absent input is the **RDHS boundary polygons**, needed to build 0.1° cell masks
(the cached masks are 0.25°/0.05°-specific). HDX COD-AB serves these free, no account.

---

## 5. Known limitations

- **CHIRPS coastal coverage.** Three districts fall below 25% area coverage; **LK52K (Kalmunai)** has
  no valid CHIRPS cell at all and uses a nearest-valid-cell fallback. Narrow coastal units are poorly
  served by a 0.05° land mask. Per-district coverage is written to `sl_chirps_coverage.csv`.
- **M0/M2/M3 are reimplementations**, built from the Methods spec with no in-repo Sri Lanka reference.
  Plausible and correctly ordered, but not reproductions.
- **Library drift.** Run under Python 3.12 / numpy 2.4.6 / pandas 3.0.5 / sklearn 1.9.0, against a
  frozen run on Python 3.10 / numpy 1.26.4 / pandas 2.1.3 / sklearn 1.7.2. A pinned environment was
  offered as an option and is not yet applied; some of the residual gap may live here rather than in
  the exposure.

---

## 6. Standing constraints

Consistent with the project guardrail — **code and reports only, no data committed** — the notebooks
write to `data_quarantine/sl_ladder/`, which is git-ignored. Nothing in this rebuild has been shared
outside the fork.

**Publishing an independent analysis of the upstream models anywhere public should go to the PI
first.** This document and the notebooks are internal until that conversation happens.
