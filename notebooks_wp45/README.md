# WP5 (MAUP / exposure sensitivity) & WP4 (spatially-honest CV) · Python notebooks

Step-by-step build of `docs/maup_sensitivity_and_spatial_cv_plan.md`, in Jupyter so every
intermediate is inspectable. Sri Lanka first.

**Owner:** Geospatial Lead · **Status:** WP5's exposure ladder is **complete — A′, B and C, both
variables** (10,842 rows each, row-aligned), and so are **plan §3.2** (exposure contrast + Figure F2,
`wp5_03`) and **the exposure half of plan §3.5** (population-product sensitivity, `wp5_06`). WP4 fold
geometry and radius done — **evaluation under the folds is blocked**, see below. What remains in WP5
is the decision half (§3.3 / F7), blocked on the same §8 artifact as WP4.

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
| wp5_01 | `wp5_01_precipitation_exposure_twin.ipynb` — A′/B **precipitation** twin + contrast | CHIRPS (streamed, no account) | ✅ executed |
| wp5_02 | `wp5_02_temperature_exposure_twin.ipynb` — A′/B **temperature/RH** twin, ERA5 0.25° | ARCO-ERA5 (streamed, no account) | ✅ executed, **caveated** |
| wp5_02b | temperature twin rebuilt on ERA5-Land 0.1° | **needs a free CDS key** | blocked |
| wp5_03 | `wp5_03_exposure_contrast_and_F2.ipynb` — exposure contrast + **Figure F2** (plan §3.2) | the three frozen tables | ✅ executed |
| wp5_04 | `wp5_04_build_c_lapse_corrected_temperature.ipynb` — **Build C**, lapse-corrected | ERA5 orography (streamed, no account) | ✅ executed |
| wp5_05 | decision impact of exposure construction, Figure F7 (plan §3.3) | the fitted model (§8 blocker) | blocked |
| wp5_06 | `wp5_06_population_product_sensitivity.ipynb` — population-**product** sensitivity (plan §3.5, exposure half) | GHS-POP (streamed, no account) + staged climate | ✅ executed |
| wp4_00 | `wp4_00_loocv_folds_and_power.ipynb` — buffered-LOOCV folds + power cost | adjacency (present) | ✅ executed |
| wp4_01 | `wp4_01_autocorrelation_range.ipynb` — Moran's I / variogram, radius selection | M6 + frozen preds | ✅ executed |
| wp4_02 | models re-evaluated under the folds | **design matrices (§8 blocker)** | blocked |

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

CHIRPS daily p05 is streamed per year from `data.chc.ucsb.edu` and cached as the Sri Lanka window
only, under `data_quarantine/wp5_exposure/chirps_window/` (~6 MB per year).

Outputs go to `data_quarantine/wp5_exposure/` — gitignored. Weight tables, the predicted-shift
table, the precipitation twin `wp5_precip_exposure_twin_srilanka_v1.csv`, and the provenance JSONs.
**Never commit rasters, exposure tables or weights.**

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
  explicitly at build time or it enters the weighted mean as real rainfall. In this window 34.5% of
  cells are ocean; unmasked they enter as ~10 m of rain per day.
- **The weight table's `cell_row` and the CHIRPS netCDF latitude axis run in opposite directions.**
  `wp5_00` stored rows in raster order (row 0 at +50°, `lat = 50 − 0.05·(row+0.5)`); the netCDF
  `latitude` axis **ascends from −50°**. They are related by `i = 1999 − row`. Applying the raster
  index directly to the netCDF hands every district the rainfall of its mirror latitude in the
  southern hemisphere and produces a complete, plausible, entirely wrong table. wp5_01 §4.1 asserts
  the derived centres against the file's own axes; do not skip that check.
- **Do not trust a provenance sha as evidence a file was here.** `wp5_00_provenance.json` records
  Build A's sha256, but the value was transcribed from the build report — the file has never existed
  on this machine.

## Open

- **A CDS key is still the one thing that would improve every temperature number.** Not a blocker
  any more — the whole ladder is built at 0.25° (wp5_02, wp5_04) — but ERA5-Land 0.1° would raise
  Build B's reach from 65.3% to 91.7% and, more importantly, anchor Build C's lapse correction to a
  less-smoothed orography. Free, `~/.cdsapirc`, not on this machine. Every notebook rebuilds
  unchanged on 0.1°; `wp5_00`'s weight field is already on that grid.
- **Four collaborator artifacts are absent, not three.** Add the frozen Build A exposure table (or
  the `~/data_quarantine/geomatics/` climate quarantine) to the §5.1 ask, alongside the threshold
  artifact, the M0/M1/M2 predictions and the design matrices.
- **The decision half of WP5 is blocked.** Exposure displacement is measured (`wp5_03`); whether it
  *flips an alert* needs the fitted model, which the repo does not hold. Same §8 blocker as WP4.
- **A second question belongs with the §5.1 ask: which model form do those artifacts use?**
  `wp5_03` §8.1 shows the answer decides in advance what §3.3 can find — a district-relative
  temperature model absorbs Build C exactly, so a null there would be a fact about the
  parameterisation, not about terrain. Worth knowing before the re-run, not after.
- **WorldPop UN-adj stops at 2020** against a window ending 2025, so the plan's vintage-matching
  requirement (§3.1) cannot be met as written. §11 measures the drift instead: the weight field
  moves ~1.1% of a typical weight over 2018→2020, so carrying 2020 forward is a bounded
  extrapolation — reported, not hidden.
- ~~**~1.4% of the population falls outside the 26 polygons**~~ — **CLOSED by `wp5_06` §4.** It is a
  WorldPop UN-adjusted 2020 coastline artifact, not a property of the geometry: the same polygons
  lose 0.23% of GHS-POP and 0.10% of WorldPop R2025A. Report it as a bounded product sensitivity;
  neither "accept 1.4%" nor "switch to fractional-coverage weighting" was the right framing.


## What wp5_01 establishes

**Population weighting moves precipitation exposure, so WP5's honest-null clause does not fire on
rainfall either** — the same verdict wp5_00 reached for temperature, now measured rather than
predicted. Over all 10,842 district-weeks the A′→B displacement averages **−0.75 mm/week**, but the
mean *absolute* displacement is **3.40 mm/week ≈ 7.9%** of mean weekly rainfall, and the largest
single district-week is **72.6 mm**. The two arms correlate 0.9935 — high, and beside the point: a
correlation near 1 across a table dominated by dry weeks says nothing about the wet weeks that
trigger alerts.

**In the tail, where alerts fire, the displacement grows in absolute terms and shrinks in relative
terms** — p90+ weeks 8.6 mm (5.4%), p99+ weeks 12.9 mm (4.9%). Both directions matter: a decision
analysis feels the millimetres, a bias argument feels the percentage.

**The sign is geographic, not noise.** Colombo loses 7.30 mm/week under population weighting and
Puttalam gains 4.37 — people cluster on the drier coastal strip in the first and away from it in the
second. Fifteen districts move down, eleven up.

**The mask is not the story; the weights are.** Splitting A→B into its two steps: swapping
`all_touched` for fractional area moves **1.8%** of mean rainfall, while re-weighting area→population
moves **7.9%**. The construction choice that matters is *what you weight by*, not *which cells you
admit*.

### The build had to rebuild Build A, and why that is better

**The frozen Build A table is not on this machine.**
`rdhs_weekly_climate_exposure_2018_2025_v2_boundary_resolved.csv` (sha `3900082b…`, 10,842 rows) and
the ~9.8 GB ERA5/CHIRPS quarantine behind it live under `~/data_quarantine/geomatics/`, which does
not exist here. `wp5_00`'s provenance records that sha, but it was **transcribed from the build
report, never computed locally** — worth knowing before trusting any provenance sha in this series.

So wp5_01 builds *both* arms from one freshly-staged CHIRPS stack. That is the stronger design: the
arms share their inputs by construction rather than by assumption. A third column, `a_alltouched`,
emulates the frozen build's mask so that (a) the A→B gap decomposes into mask and weight effects, and
(b) there is a validation target if the frozen table ever arrives.

### CHIRPS is far cheaper than the acquisition plan assumes

`docs/climate_bulk_acquisition_and_exposure_table_plan.md` §D specifies per-day global GeoTIFFs,
bbox-clipped on arrival — ~31 GB of transfer for this window, and the 2026-06 build pulled ~9.8 GB
that way. Unnecessary: the yearly netCDFs are **netCDF-4/HDF5, chunked `(20, 112, 400)`, gzipped**,
and Sri Lanka's bbox touches only 2×2 spatial chunks. An HTTP range read (`fsspec` + `h5netcdf`)
pulls a full year of the window in **8–19 s** and never materialises the global grid. The whole
2018–2025 stack is ~2 minutes and ~50 MB cached. No account, no bulk storage.

## What wp5_02 establishes — and why every number in it is a floor

**Build B now exists for both variables**, row-aligned with the precipitation twin: t2m mean/min/max,
dewpoint and RH, 10,842 rows, all QC green. RH is computed **per cell per hour** by Alduchov–Eskridge
Magnus before any averaging, as plan §E requires — deriving it from weekly-mean T and Td instead gives
a plausible-looking wrong answer.

**The temperature displacement is real but smaller than the DEM predicted**, because the grid is
coarser: mean |A′→B| **0.205 °C**, district range **−0.86 °C (Badulla) to +0.34 °C (Colombo)**, largest
single district-week **1.16 °C**. Two results are worth more attention than the mean:

- **Extremes move more than means.** Weekly `t2m_max` shifts by mean |0.387| °C and up to **2.76 °C**,
  nearly double the mean-temperature effect. For a transmission model driven by thermal limits rather
  than averages, that is the number that matters.
- **RH moves by mean |0.77| percentage points, up to 6.3.**

### The grid substitution, stated plainly

ERA5-Land 0.1° needs a CDS key that is not on this machine, so this is **ERA5 0.25°**. Measured before
building, from the DEM and WorldPop alone: Build B sees **65.3%** of the population-weighting
displacement at 0.25° against **91.7%** at 0.1°. Effective cells per district fall from 21.3/11.8
(area/pop) to **5.3/3.6**. So every figure above is a **conservative floor, biased toward the null** —
the safe direction for a claim that construction is *not* null, and useless for any claim about *which*
districts warm. **Ratnapura retains 6.7%** of its predicted shift (+0.83 → +0.06 °C).

### The prediction cross-check, read properly

`wp5_00` predicted these shifts from elevation and a lapse rate with no climate data; this is the first
measurement against a real temperature field. A bare "69% sign agreement" is the wrong summary — in a
flat district the prediction is ~0.01 °C and its sign is noise. Agreement rises with what the
prediction actually claims:

| threshold | districts | sign agreement | correlation |
|---|---|---|---|
| all | 26 | 69.2% | +0.71 |
| \|predicted\| > 0.2 °C | 7 | **85.7%** | **+0.79** |
| \|predicted\| > 0.3 °C | 5 | 80.0% | **+0.86** |

**Badulla is confirmed by measurement** (−0.86 °C observed against −1.75 °C predicted at 0.1°, close to
the ~65% this grid can see). **Kandy is a genuine disagreement** — predicted +0.58 °C, observed
−0.29 °C — the only one among districts with a substantial prediction, and most likely its steep
terrain being averaged away at 0.25°.

**A confounder tested and rejected.** Coastal districts draw much of their weight from cells that are
part ocean, where ERA5 (unlike ERA5-Land) blends in sea surface temperature — Mannar, Batticaloa and
Puttalam sit at ~0.56 population-weighted land fraction, island-wide 0.858. That was the obvious
suspect for the disagreements and it does **not** explain them: mean land fraction is 0.88 where signs
agree and 0.82 where they don't, both spanning the full range. The caveat is real; it is not the cause.

## What wp5_04 establishes — the ladder's last rung was never blocked, and it is not the smallest

**Build C needed no CDS key and no collaborator artifact.** ERA5's surface geopotential — the model's
own orography, the missing half of any lapse correction — sits in the same open ARCO-ERA5 store as
`t2m`, and `scripts/srilanka_era5_window_reader_v1.py` reads it unchanged. This table listed wp5_04 as
blocked behind a 0.1° rebuild; that was wrong, and the row is now corrected.

**On the grid we actually have, Build C moves exposure ~1.5× as far as Build B does:**

| step | mean \|ΔT\| across the 26 districts |
|---|---|
| A′ → B, population weighting | 0.205 °C |
| **B → C, lapse correction** | **0.306 °C** |

`wp5_00` ranked Build C last and set its acceptance target at "a few tenths of a degree." The target
was fine — 0.306 °C *is* a few tenths — but the **ranking inverts**, because that calculation was done
at 0.1°, where Build B already captured 91.7% of the elevation displacement. **What Build C recovers is
exactly what a coarse grid loses, so it grows as the grid coarsens.** It is the one rung that partly
repairs the missing CDS key instead of being degraded by it. Largest shifts: **Nuwara Eliya −1.92 °C**,
**Badulla −1.33 °C**, **Ratnapura +1.01 °C**.

**Why the highlands move so much, in one number:** ERA5's orography over Sri Lanka peaks at **1,219 m**
against the island's real 2,524 m. The reanalysis does not contain the central highlands, so it issues
2 m temperature for a mountain range about half the true height — and highland populations are the ones
nearest *Aedes*' lower thermal bound.

**Do not report B→C as a MAUP effect.** It is two things, and §6 separates them: mean |orography
deficit| **0.223 °C**, which would apply under area weighting too and belongs to the exposure-*quality*
argument, against **0.169 °C** of genuine sub-grid population placement, which is the only part that
belongs to WP5's exposure-*construction* argument. They can also oppose — in Nuwara Eliya, −2.26 and
+0.34 °C. Quoting the combined 0.306 °C as MAUP would overstate WP5's result by about half.

**The structural finding, available before the blocked refit.** For `t2m` and `d2m` the correction
carries no time index, so **Build C is Build B plus a constant per-district offset** (within-district
sd across 417 weeks < 2e-6 °C, asserted). That decides in advance what the §5.1-blocked decision re-run
*can* find: a model on district-relative temperature — anomalies, district fixed effects, per-district
standardisation — absorbs the offset exactly and **Build C cannot flip a single alert**; a model on
absolute temperature or a fixed thermal threshold sees the full ~2 °C. **So a Build C null must not be
read as "terrain doesn't matter"** — it may only mean the model was district-relative. Two things do
survive: **RH** (nonlinear in T and Td, within-district sd up to 0.71 pp) and threshold-crossing counts.
**DTR does not** — it is offset-invariant.

**Verification.** Zeroing the offsets rebuilds `wp5_02`'s frozen Build B through an independent code
path to **3.6e-15 °C** (RH 1.7e-05 pp), and the weight field reproduces the frozen file to 9.8e-17.

**Validated against station observations (2026-08-13).** GHCN-Daily carries six Sri Lankan stations
through 2025, including **Nuwara Eliya at 1,880 m** (`CE000434730`, GSN, record from 1869); free and
anonymous. Comparing like with like — ERA5 daily (max+min)/2 on **local** days (UTC+5:30):

| | station obs | ERA5 0.25° | ERA5 bias |
|---|---|---|---|
| Nuwara Eliya (1,880 m) | 16.40 °C | 21.17 °C | **+4.77 °C** |
| four lowland stations (1.8–116 m) | 27.9–28.7 °C | | **−0.36 to −0.42 °C** |

**ERA5 is accurate at sea level and ~5 °C too warm in the highlands** — elevation-dependent, exactly
what Build C models, not a global offset; present in every year 2018–2025 and in both TMAX and TMIN.
At the district level, regressing the five well-sampled stations on elevation (**6.40 °C/km**) and
interpolating to the district's population elevation of 1,260 m implies a true mean of 19.82 °C:
**Build B 21.89 °C (error +2.07), Build C 19.98 °C (error +0.15)** — Build C removes 93% of the error
where the correction is largest.

**The rate is well chosen; an earlier caveat here was wrong-signed and is withdrawn.** This section
previously read that §10's MODIS night-LST estimate (5.84 °C/km) put the 6.5 used *above* the local
rate, making Build C "not conservative", and advised scaling by ~0.90. MODIS LST was the weakest of
the three estimates — a *surface* temperature, regressed *between* districts, confounded by land
cover. Station **air** temperature gives **6.40 °C/km** and ERA5's own between-cell lapse over land
cells gives **6.31 °C/km**, both within ~2% of the 6.5 used. **No rescaling is warranted.**

**What still bounds every magnitude here.** The high end of the station regression rests on **one**
station — the other four sit below 120 m. The larger TMIN bias (+5.27) than TMAX (+4.27) is the
signature of **nocturnal cold-air pooling** in a highland basin, a local siting effect that must not
be extrapolated to a whole district's population, and the likely reason the raw station-vs-ERA5 gap
implies a steeper rate (~7.8 °C/km) than the clean regression. The correction is still anchored to
ERA5's *smoothed* orography, so a 0.1° rebuild would start from a better one. And the RH shift remains
bracketed by the dewpoint rate (−0.34 pp vapour-pressure-conserving, 0.00 pp RH-conserving) — report
the bracket, never the middle value alone.

## What wp5_03 establishes — plan §3.2 is done, and it was never blocked

**The old row above was wrong.** This table used to list `wp5_03` as blocked behind the fitted model.
That conflated the plan's §3.2 (*how far does the exposure move?*) with its §3.3 (*does the decision
move?*). Only the second needs a model. §3.2 needs the three frozen tables, which are on this machine,
and it is now complete: `Manuscript_Figures/wp5/WP5_F2_exposure_contrast.{pdf,png}` plus the
per-district table `wp5_exposure_contrast_srilanka_v1.csv`. 15/15 QC.

- **Exposure construction moves exposure on every variable measured**, so §3.4's honest-null clause
  fires on neither. Rainfall 3.40 mm/wk (7.9% of its mean), weekly mean temperature 0.205 °C, weekly
  **maximum** temperature 0.387 °C, the lapse correction a further 0.306 °C.
- **The mask is a footnote; the weights are the result** — 1.8% against 7.9%.
- **Exposure construction is not a property of a district.** Ranked by displacement, rainfall and
  temperature share **one** district in their top fives, and the rank correlation of the absolute
  displacements is indistinguishable from zero (ρ = 0.24, p = 0.23). A single-variable sensitivity
  check will misidentify which districts are exposed to the choice.
- **The two rungs act on different parts of the distribution.** Population weighting moves the weekly
  maximum ~2× the mean (it re-weights a field whose cells disagree most in the tails); the lapse
  correction moves min, mean and max identically because it is one number per district.
- **Only 0.169 of B→C's 0.306 °C is attributable to MAUP.** The rest is ERA5's orography deficit,
  which applies under area weighting too. Reporting the sum as a MAUP effect overstates WP5 by ~half.
- **In the weeks that would trigger an alert the rainfall contrast grows in millimetres and shrinks
  in percent** — 12.9 mm / 4.9% in the wettest 1% of district-weeks.

**Correction it forces to the Build C memo.** PR #1 said Build C is a constant per-district offset
"for `t2m` and `d2m`". Tested against the exact −Γ·Δz prediction rather than against zero variance:
`t2m` holds to **6×10⁻⁷ °C**, `d2m` **does not** — it departs by up to **0.46 °C** (Nuwara Eliya) and
varies week to week, because the physically necessary saturation guard
`td = min(td − Γ_td·Δz, t − Γ_t·Δz)` binds in some hours and not others, in three highland districts.
`wp5_04` §9 is amended accordingly. The consequence runs the useful way: a model on district-relative
*temperature* still absorbs Build C exactly, but a model carrying **dewpoint or humidity** sees a
residual no district effect can absorb — so §3.3 has more to find there than the memo implied.

**Why precipitation has no Build C rung.** CHIRPS is observational — cold-cloud duration calibrated
to gauges — not a reanalysis with an internal orography that disagrees with the real one. There is no
"elevation CHIRPS believes" to correct against. The physical analogue would be an orographic
enhancement *model*, which the study's no-new-model rule bars. A property of the data, not a gap.

**Greyscale, stated rather than claimed.** The two bar panels carry hatch as a second identity
channel and pass. The three maps do **not**: a diverging ramp is symmetric in luminance, so ±1.9 °C
print as the same grey. Mitigated by labelling the largest movers numerically on the map face; the
notebook measures it rather than asserting it.


## What wp5_06 establishes — WP5's result is not a WorldPop artifact

Plan §3.5 splits the same way §3.2 did: *"rebuild Build B weights under an alternative population
product"* is runnable, *"recompute ΔNB at p\* under each layer"* is not. This is the first half.

Three products at the same 2020 epoch — **WorldPop UN-adjusted** (the incumbent), **WorldPop R2025A
constrained** (a newer release from the same producer), and **GHS-POP R2023A** (JRC; a different
institution and a different dasymetric method, built-up-surface rather than random forest). All free,
all anonymous. Because Build B normalises weights *within* district, a product's national total
cancels exactly; only the shape of the surface inside a district can matter.

**The construction step is roughly an order of magnitude taller than the product uncertainty.**

| contrast | mean displacement |
|---|---|
| weight moved, area → population (ERA5 grid) | **27.5%** of a district |
| weight moved, WorldPop unadj → GHS-POP | 1.6% |
| weight moved, WorldPop unadj → R2025A | 2.0% |
| exposure, A′→B, weekly mean t2m | **0.205 °C** |
| exposure, product swap, weekly mean t2m | 0.006 °C |
| exposure, A′→B, rainfall | **3.40 mm/wk** |
| exposure, product swap, rainfall | 0.161 mm/wk |

Ratios run **16.7× to 32×** at the mean, hold in the tails where alerts fire (19.5× in the wettest 1%
of district-weeks, 35.8× in the hottest 1%), and in **0 of 26 districts** does the product effect
reach the weighting effect. The per-district reading survives too: ρ = 0.985 / 0.990 on the ranking
of movers, identical top-five sets, complete sign agreement. So `wp5_03`'s statements about *which*
districts are exposure-sensitive are not statements about WorldPop.

**Version drift inside one producer exceeds the gap between producers.** WorldPop UN-adjusted and
WorldPop's own R2025A differ *more* (mean TV 0.0201) than WorldPop and GHS-POP do (0.0157). "Same
producer, newer release" is not the safer substitution it sounds like.

**The coastal shortfall was a product defect, and this closes that open item.** The ~1.4% of
population falling outside the 26 polygons is specific to WorldPop UN-adjusted 2020: on the same
boundaries GHS-POP loses **0.23%** and WorldPop R2025A **0.10%**. The README's open choice between
"accept and report" and "switch to fractional-coverage weighting at the boundary" was a choice
between two ways of absorbing someone else's coastline error, and §6 bounds what it can do to the
weights regardless.

**The fourth arm §3.5 names is degenerate by construction.** Census district totals carry no
within-district spatial information, so distributing them uniformly makes the climate-cell weight
proportional to in-district area — Build A exactly (verified to 0.0). And because weights are
normalised within district, the totals themselves cancel: the district could hold one person or ten
million. Not a null result about population data; the arithmetic of the weighting.

### Traps this notebook adds

- **`rasterio.merge.merge(srcs, bounds=…)` does not snap to the source grid.** It derives the output
  transform from the *requested bounds* and resamples into it (nearest by default). On population
  **counts** a sub-pixel shift duplicates some 100 m cells and drops others — it moves people. Here
  it produced a 0.54-pixel offset. §3.2 pastes tiles at integer offsets instead, with no resampling.
- **GHS-POP needs all four tiles.** Sri Lanka straddles both the 80 °E and the 10 °N tile seams;
  taking only the two southern tiles silently truncates Jaffna, Kilinochchi and Mullaitivu.
- **The staged CHIRPS window was cut to WorldPop's clipped extent.** WorldPop UN-adj stops at
  79.648 °E; GHS-POP and R2025A do not, so their weight tables reach three columns further west and
  `j = col − J0` goes negative — NumPy wraps it and Jaffna quietly receives east-coast rainfall.
  Asserted, dropped, renormalised, and the induced error bounded at **4.3e-4 mm/week**.
- **RH is the one column that is not bit-reproducible across environments.** The three temperature
  columns reproduce the frozen twin to 1e-14; RH reproduces to 1.65e-5 pp (**2.2 float32 ULP**),
  because it is the only variable computed through `exp()` in float32 and `np.exp` is accurate to
  ~1 ULP but not bit-identical across NumPy/libm builds. Immaterial — 2,000× below the smallest
  effect reported — but a re-run under a different build will not match byte-for-byte, and the
  acceptance test must say so rather than fail mysteriously.

**What it does not establish.** Nothing about net benefit or decisions — that is §3.5's second half,
blocked with `wp5_05` and `wp4_02`. A small *exposure* displacement does not mechanically imply a
small *decision* displacement; testing that inference is what WP5 is for. Nothing about **Colombia**,
where smaller and more heterogeneous municipalities give the products more room to disagree. And all
three products are **modelled** surfaces sharing much of their input census, so their agreement
bounds method sensitivity, not the truth of where people are.


## Why WP4 cannot be finished either

`instruction_m6.md` corrected "WP4 complete" to *fold design complete until models are evaluated
under the folds*. That evaluation is **blocked for the same reason §8 is**: re-fitting under spatial
folds needs each model's **design matrix**, and `ALT_STATS/frozen/srilanka_matched_pairs.csv` carries
**predictions only**. M6 could be re-fit alone — we own its features and labels end-to-end — but a
spatially-CV'd M6 set against a temporally-split M5 is not a comparison, it is an artifact, and it
would oblige the same treatment for M0/M1/M2/M5 that the artifacts do not permit.

**Consequence for the §5.1 ask: it now unblocks three items, not two** — §4 (threshold generator),
§8 (matched geomatics ablation) and WP4's evaluation half.

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
