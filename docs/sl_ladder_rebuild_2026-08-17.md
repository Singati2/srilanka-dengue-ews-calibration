# Independent Sri Lanka M0–M5 rebuild — findings

**Date:** 2026-08-17 · **By:** Geospatial Lead · **Code:** `notebooks_sl_ladder/` (6 notebooks, all executed)
**Gate target:** `ALT_STATS/frozen/srilanka_matched_pairs.csv` (3,926 frozen test predictions)

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

| Model | mean \|Δp\| | max \|Δp\| | corr. with frozen |
|---|---|---|---|
| M5 no-climate | 0.0256 | 0.2607 | **0.9758** |
| M5 full | 0.0621 | 0.7773 | **0.8810** |

Cohort reconciliation:

| | Rebuild | Frozen | |
|---|---|---|---|
| Analysis rows | 10,490 | 10,516 | −26, fully explained |
| Test rows | **3,926** | **3,926** | exact |
| Test prevalence | 0.3372 | 0.3365 | |
| Label agreement | 0.9880 | — | 48 disagreements |
| Matched raw ΔNB | **+0.0071** | **+0.0087** | same sign, same order |

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
| M0 | 0.6220 | 0.2254 | 0.0652 | reimplementation |
| M1 | 0.7325 | 0.1993 | 0.1220 | **ported** |
| M2 | 0.6422 | 0.2174 | 0.0777 | reimplementation |
| M3 | 0.6735 | 0.2134 | 0.0839 | reimplementation |
| M4 | 0.7190 | 0.2011 | 0.1054 | **ported** |
| M5 | 0.7570 | 0.1943 | 0.1294 | **ported** |
| M5_no-climate | 0.7323 | 0.1994 | 0.1223 | **ported** |

Manuscript comparators: M1 AUC 0.752 / NB 0.137, M2 NB 0.069, M3 NB 0.078. The rebuilt ladder is
ordered identically and sits slightly low throughout, consistent with the coarser exposure.

Matched increment with district-cluster bootstrap (`sl_05`):

- **Rebuild:** +0.0071 [−0.0041, +0.0198], B=2000, conditional
- **Frozen:** +0.0087 [−0.0079, +0.0245], B=1000, development-inclusive

Same qualitative reading — small, positive, interval covers zero — reached through a different
reanalysis product. **The deflationary conclusion survives the substitution.** That is an independent
robustness result the study did not previously have.

Caveat: the intervals are not interchangeable. The rebuild's is conditional; the frozen study's is
development-inclusive and therefore wider and more honest.

---

## 4. What a CDS key would now buy

The gate localises the exposure cost precisely. M5-no-climate and M5-full are identical except for
the climate block, so the drop from 0.976 to 0.881 correlation is attributable to using ERA5 0.25°
in place of ERA5-Land 0.1° — not to anything else in the pipeline.

Pulling ERA5-Land would close most of that gap and change nothing else in the series. It is now an
optional fidelity upgrade with a known payoff, rather than a prerequisite.

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
