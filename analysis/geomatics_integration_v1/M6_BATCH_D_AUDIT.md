# M6 Batch D audit — is the executed model the full 16-variable M6?

**Instruction:** `instruction_m6.md` §2 (Ganesh Shiwakoti, 2026-08-07) · **Executed:** 2026-08-07
**Source commit:** `ff6287d0e336ab4e3a3d178593d3bb28e3f33a21` · **Scope:** Sri Lanka
**Machine-readable output:** `M6_CORE_FEATURE_MANIFEST.yaml` · **Generator:** `scripts/m6_batchD_feature_audit_v1.py`

---

## Verdict

**Batch D is absent. The executed model is `M6-core (A/B/C)`** and must not be described as the
complete originally planned 16-variable M6.

Three of the four Batch D variables were never built in any form. The fourth is half-present by
accident. Details below.

---

## What was audited

The fitted design matrix, taken from `m6_coefficients_srilanka_v1.csv` (the coefficient table is
the design matrix, one row per column actually entering the model).

- **92 features**, all fitted. Estimator is `LogisticRegression(penalty=l2, C=0.001)` with **no
  feature-selection step**, and **0 of 92 coefficients are zero** — so design matrix, candidate set
  and fitted set are the same object. There is no selection history to reconstruct.
- Cross-checked against the 101-column weekly feature table: the 9 non-fitted columns are 6 keys
  (`geometry_id`, `rdhs_id`, `rdhs_name`, `iso_year`, `iso_week`, `week_start`) and 3 QA/staleness
  diagnostics (`lst_age_days_lag0`, `vi_age_days_lag0`, `stale_flag`). **Nothing was built as a
  candidate feature and then left out.**

## Coverage against `docs/M6.md` §1

| Batch | Planned variables | Present | Features |
|---|---|---|---|
| **A** — DEM bundle | #1 elevation, #2 slope, #3 TWI, #4 HAND | **4 / 4** | 20 |
| **B** — open rasters | #5 built-up, #6 population, #7 nightlights, #8 fragmentation, #11 surface water, #12 forest | **6 / 6** | 14 |
| **C** — dynamic RS | #9 LST/UHI, #10 NDVI/EVI | **2 / 2** | 54 (6 base × lags 0–8) |
| **D** — harder layers | #13 mobility, #14 wealth, #15 healthcare access, #16 cropland | **0 fully / 1 partial** | 1 |

**12 of 16 planned variables are present.** Variables **#13, #14, #15 are fully absent** — no gravity
in-flow or centrality features, no Meta RWI or the nightlights+built-up SES fallback, no travel-time
or distance-to-facility surface. None of the corresponding rasters appear in
`data_quarantine/m6_geomatics/`.

## The one wrinkle: #16 is half-present, incidentally

`frac_crops` **is** in the design matrix, and cropland is a Batch D variable. It should not be read
as evidence that any part of Batch D was executed:

- It is one of **seven Impact Observatory `io-lulc-annual-v02` class fractions** co-extracted
  wholesale by notebook 03 (Batch B). It arrived as a byproduct of the land-cover extraction, not
  from a Batch D build step.
- §6.16 specifies **ESA WorldCover** cropland; the executed build used Impact Observatory.
- §6.16 pairs the static cropland share with an **EVI phenology amplitude** (seasonal max−min, the
  paddy-intensity proxy). That half was **never built** — the `evi_mean` lags in the matrix are
  Batch C #10, a different variable.

So the seasonal, mechanistically-motivated half of #16 is missing and the static half is present by
a different product than specified. Recorded as `partial`, not as a Batch D deliverable.

## Two further departures, recorded for the manifest

1. **Land-cover product substitution.** §1 names ESA WorldCover / GHSL for the land-cover-derived
   variables (#5, #8, #12, #16); the build used Impact Observatory `io-lulc-annual-v02` (10 m)
   throughout. One consequence worth naming: `frac_water` measures planned #11 via the LULC class
   vector rather than the JRC Global Surface Water layer §6.11 specifies. The JRC layer *is* also
   present (`water_occurrence_mean`, `permanent_water_frac`, `dist_permanent_water_km`), so #11 is
   covered as planned and `frac_water` is an additional same-concept measure.
2. **UHI variant not built.** §6.9's `unit LST − rural-ring LST` variant is absent; only direct LST
   statistics are present. §6.9 marks it *optional*, so this is not a departure from a requirement —
   noted because "UHI" appears in the variable name and could be over-read.

Three co-extracted LULC classes are in the matrix but are **not** among the planned 16:
`frac_bare`, `frac_flooded_veg`, `frac_rangeland`. They are unplanned additions, not substitutions
for anything.

## Consequences

- **Naming.** Use **M6-core (A/B/C)** in the manuscript, figures, and all downstream artifacts. If
  Batch D is ever added, that becomes **M6-extended**, versioned separately per §2. Historical M6
  is not redefined.
- **The null is narrower than "geomatics".** The honest null (AUC 0.601) is a null for *terrain,
  land cover and remotely-sensed dynamics*. It is **not** a test of mobility, wealth, or healthcare
  access — the three variables most plausibly related to dengue *reporting* and human exposure, and
  the three that are missing. §7's language constraint should extend to this: the result cannot
  support a claim about geomatics as a whole.
- **§9.5's interim gate is unaffected** by this audit — it was already unrunnable as written for the
  separate reason recorded 2026-08-05 (static A+B features cannot express *when* against a weekly
  label).

## Status

`instruction_m6.md` §22 checklist — **M6-core feature manifest: PASS.**
The manifest exists, is generated from the artifacts rather than transcribed, and asserts that every
one of the 92 fitted columns is assigned exactly once (the generator raises on an unassigned
column, so it cannot silently drift from a re-fit design matrix).
