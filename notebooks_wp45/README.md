# WP5 (MAUP / exposure sensitivity) & WP4 (spatially-honest CV) · Python notebooks

Step-by-step build of `docs/maup_sensitivity_and_spatial_cv_plan.md`, in Jupyter so every
intermediate is inspectable. Sri Lanka first.

**Owner:** Geospatial Lead · **Status:** WP5 Build B weight field done (exposure values await climate
staging); WP4 fold geometry done (operative radius awaits §4.1).

Separate from `notebooks/`, which is the **M6 geomatics-only model** (an *optional* Phase 4 rung).
These two work packages carry the plan's *mandated* deliverables. Different question, different
series, deliberately not renumbered into the M6 sequence.

---

## Why these two

Everything downstream of exposure currently consumes the **area-weighted** Build A table. There is
no population-weighted table and no spatial-block CV. WP5 asks whether the *construction* of
exposure changes the decision; WP4 asks whether the external-validation claim survives a test that
respects spatial autocorrelation.

## Notebooks

| # | Notebook | Needs | Status |
|---|---|---|---|
| wp5_00 | `wp5_00_population_weight_field.ipynb` — Build B weight field, A→B prediction | WorldPop + DEM (staged) | ✅ executed |
| wp5_01 | Build B exposure table — apply weights to ERA5-Land + CHIRPS | **climate grids (unstaged)** | blocked |
| wp5_02 | exposure contrast, Figure F2 | wp5_01 | blocked |
| wp5_03 | Build C — lapse-rate corrected temperature | wp5_01 | blocked |
| wp4_00 | `wp4_00_loocv_folds_and_power.ipynb` — buffered-LOOCV folds + power cost | adjacency (present) | ✅ executed |
| wp4_01 | `wp4_01_autocorrelation_range.ipynb` — Moran's I / variogram, radius selection | M6 + frozen preds | ✅ executed |

## What wp5_00 establishes

Build A and Build B differ **only in the weights** — the climate fields are identical — so the
weight field is the whole of Build B and can be frozen before any climate data is downloaded. Once
ERA5-Land and CHIRPS are staged, the exposure table is a join against these weights and a weighted
sum, row-aligned to Build A's 10,842 keys (417 ISO weeks × 26 RDHS).

Headline numbers, all computed from locally staged inputs:

- **Population-weighting moves temperature by −1.75 °C to +0.83 °C** across districts, estimated
  from the staged DEM and the standard lapse rate. Badulla's population lives ~270 m *above* its
  district's areal mean elevation (highland towns and tea estates; the sparsely-settled Uva basin
  drags the area-mean down), so weighting by people **cools** its exposure. Ratnapura runs the
  other way. This pre-empts the plan's honest-null clause (§3.4) with a number: on temperature,
  exposure construction is not a null.
- **Build B reaches ~92%** of that displacement at ERA5-Land resolution. The within-cell residual —
  what Build C's lapse correction would add — tops out at ~56 m ≈ 0.36 °C, and is *not* reliably
  additive: `corr(|between|,|within|) = 0.33`, same sign in only 65% of districts, and in Badulla
  the two carry opposite signs. Build C's acceptance target should be set at a few tenths of a
  degree, not assumed comparable to B.
- **`all_touched` misplaces ~31% of a district's weight** (median, ERA5-Land) against fractional
  overlap. Half of a typical ERA5-Land cell lies outside the district it is credited to
  (median `cell_frac` 0.51); for Colombo and Jaffna it is under a third.
- **Population-weighting halves the effective spatial support** — a median district's exposure is
  drawn from ~12 effective ERA5-Land cells instead of ~21. That is the correct answer to "what
  weather did these *people* experience", but it is the cost side of the trade.

## Data

Inputs are already local, staged by the M6 notebooks: WorldPop UN-adjusted 100 m (2018–2020) and
Copernicus GLO-30 DEM tiles, both under `data_quarantine/m6_geomatics/`. One CHIRPS granule is
downloaded to pin that product's grid exactly (open, no account).

Outputs go to `data_quarantine/wp5_exposure/` — gitignored. Weight tables, the predicted-shift
table, and `wp5_00_provenance.json`. **Never commit rasters, exposure tables or weights.**

## Traps

- **The two climate grids do not share a cell alignment.** CHIRPS ships a GeoTIFF whose transform
  states the upper-left *edge*; ERA5-Land is distributed on grid *points* at exact multiples of
  0.1°, which are cell *centres*, so its edges fall on 0.05°, 0.15°, … Treating them the same way
  moves every person up to ~5.5 km into the wrong cell, raises nothing, and produces weights that
  look entirely reasonable. §3 verifies CHIRPS against a real granule and leaves ERA5-Land declared
  but flagged `verified=False` — **assert it against the first staged granule.**
- **`pop` is a DataFrame method.** `d.pop` returns the method, not the column, and fails with an
  unhelpful `AttributeError` well downstream. The population column is named `pop_sum`.
- **CHIRPS carries no nodata tag** (confirmed on the probe granule) — `-9999` must be masked
  explicitly at build time or it enters the weighted mean as real rainfall.

## Open

- **ERA5-Land and CHIRPS are the only missing inputs.** ERA5-Land needs a free CDS API key; CHIRPS
  is open HTTP. Acquisition is specified in `docs/climate_bulk_acquisition_and_exposure_table_plan.md`.
- **WorldPop UN-adj stops at 2020** against a window ending 2025, so the plan's vintage-matching
  requirement (§3.1) cannot be met as written. §11 measures the drift instead: the weight field
  moves ~1.1% of a typical weight over 2018→2020, so carrying 2020 forward is a bounded
  extrapolation — reported, not hidden.
- **~1.4% of the population falls outside the 26 polygons** (centre-in-polygon on an island
  coastline). Same quantity as notebook 03 §7 and the same open WP5 decision: accept and report, or
  switch to fractional-coverage weighting at the boundary.


## What wp4_00 establishes

§4.2's buffered LOOCV built as a **function of buffer radius**, so when §4.1 returns the
autocorrelation range it selects a row from a table that already exists. Distance is
**boundary-to-boundary** in the equal-area CRS, not centroid-to-centroid: adjacent districts here sit
28–119 km apart by centroid while sharing a border, so a centroid buffer would be wildly uneven.

**The power cost — the number §4.6 requires be put to the PI.** Training districts available, of 25:

| buffer | median fold | worst fold | median train district-weeks | degenerate folds |
|---|---|---|---|---|
| adjacency only (0 km) | 21 | 16 | 5,481 | 0 |
| 25 km | 19 | 14 | 4,959 | 0 |
| 50 km | 15 | 10 | 4,045 | 0 |
| 75 km | 12 | 6 | 3,132 | 0 |
| 100 km | 9 | 5 | 2,349 | 0 |
| 150 km | 5 | 0 | 1,435 | **12** |

Sri Lanka is ~430 km end to end, so a buffer is a large fraction of the country by construction. At
100 km the median fold trains on 9 of 25 districts and the worst on 5; at 150 km the scheme collapses
(12 of 26 folds keep fewer than 5 training districts). §4.6's "low-powered even with LOOCV" is now
quantified rather than asserted.

**Leakage audit (§4.4, spatial half):** zero train/test pairs within the buffer, for every radius and
every fold, asserted rather than assumed. Temporal leakage is enforced upstream in M6 notebook 04
(composites ending strictly before the predicted week, verified over 195,624 cells); the two
constraints are orthogonal and together make the scheme spatio-temporal.

**Still needed:** the operative radius from §4.1 — an empirical variogram or Moran's I decay on model
residuals. M6's predictions now exist on the 3,926 test rows, so a first estimate could be taken
immediately; the registered version should use the reference model's residuals.

**Caveats.** Hop and kilometre buffers are *not* interchangeable — one hop removes 2 to 7 districts
depending on where you are, so it applies an uneven buffer while looking uniform; the kilometre
buffers are the defensible primary. And per §4.6 this remains the **compact-country companion**: the
well-powered external-validation claim rests on Colombia's block CV (§4.3), out of scope while the
work is Sri Lanka-only.


## What wp4_01 establishes

**The residual autocorrelation range is effectively zero.** Moran's I computed per week across the
151 test weeks and tested by permutation (999 shuffles, seed 20260612) is indistinguishable from its
null at **every** distance band for all three models — permutation p from 0.53 to 0.99 — and the
empirical variogram is flat from 25 km to 400 km.

That is more robust than it first appears. M5 carries **district fixed effects**, which absorb
time-invariant spatial structure, so a near-zero residual Moran's I could be an artifact of the
model. **M6 carries no fixed effects at all** (`M6.md` §0) and returns the same answer — I = 0.001
among adjacent districts, p = 0.99. The absence is not an FE artifact.

Stated honestly: with 26 units the permutation null has sd ≈ 0.02, so this rules out residual spatial
correlation above roughly |I| = 0.04. It does not prove zero.

**Consequence:** the buffered scheme is cheap. The minimum buffer (drop immediately-adjacent
districts) retains 21 of 25 training districts in the median fold, 16 in the worst — against 9 and 5
at 100 km. The reviewer concern motivating WP4 is answered directly rather than by an expensive
scheme, and the power table remains frozen if a more conservative radius is preferred.

This is a **first estimate**: §4.1 specifies the reference model's residuals and M5-full as frozen is
the closest available. If the registered reference model differs, re-run — only the residual column
changes.
