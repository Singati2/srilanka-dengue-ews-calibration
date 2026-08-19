# WP5 (MAUP / exposure sensitivity) & WP4 (spatially-honest CV) · Python notebooks

Step-by-step build of `docs/maup_sensitivity_and_spatial_cv_plan.md`, in Jupyter so every
intermediate is inspectable. Sri Lanka first.

**Owner:** Geospatial Lead · **Status:** WP5's exposure ladder is **complete — A′, B and C, both
variables** (10,842 rows each, row-aligned), and so are **plan §3.2** (exposure contrast + Figure F2,
`wp5_03`), **the exposure half of plan §3.5** (population-product sensitivity, `wp5_06`) and now
**the runnable half of plan §3.3** (decision-flip envelope + Figure F7, `wp5_05`) and **plan §3.6**
(spatial structure of miscalibration + Figure F8, `wp5_07`). WP4 fold geometry
and radius done, the fold effect measured inside M6 (`wp4_02`), and **the cross-model contrast now
measured on M5 itself** (`wp4_02b`) — the §5.1 blocker turned out to cover the *input table*, not the
builders, and the `sl_ladder` rebuild supplies a substitute of measured fidelity. What remains is the
*registered* §3.3 re-run (ΔAUC / Δcalibration under each build, `wp5_05b`), which is runnable on the
same substitute and has not been run.

**Plan Phase 6 (write-up) is drafted** as of 2026-08-15:
`manuscript/wp4_wp5_sections/wp4_wp5_methods_results_v1.tex` holds drop-in Methods and Results
subsections for both work packages, with `wp4_wp5_number_provenance_v1.md` mapping every number to
the table it was recomputed from and `wp4_wp5_references_add_v1.bib` supplying the new citations.
It is held **outside** the manuscript tree until the PI settles Paper 1 vs Paper 2 and
`instruction_m6.md` §22.

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
| wp5_05 | `wp5_05_decision_flip_envelope.ipynb` — decision-flip envelope + **Figure F7** (plan §3.3, runnable half) | frozen predictions + the three exposure tables | ✅ executed |
| wp5_05b | ΔAUC / Δcalibration under Builds B and C (plan §3.3, registered re-run) | **design matrices (§5.1 blocker)** | blocked |
| wp5_06 | `wp5_06_population_product_sensitivity.ipynb` — population-**product** sensitivity (plan §3.5, exposure half) | GHS-POP (streamed, no account) + staged climate | ✅ executed |
| wp5_07 | `wp5_07_miscalibration_structure_and_F8.ipynb` — spatial structure of miscalibration + **Figure F8** (plan §3.6) | frozen predictions + M6 statics | ✅ executed |
| wp4_00 | `wp4_00_loocv_folds_and_power.ipynb` — buffered-LOOCV folds + power cost | adjacency (present) | ✅ executed |
| wp4_01 | `wp4_01_autocorrelation_range.ipynb` — Moran's I / variogram, radius selection | M6 + frozen preds | ✅ executed |
| wp4_02 | `wp4_02_fold_effect_within_m6.ipynb` — fold effect measured **within M6**, against a size-matched control | M6 features + labels (ours) + `wp4_00` folds | ✅ executed |
| wp4_02b | `wp4_02b_fold_effect_within_m5.ipynb` — **M5 and its no-climate twin** under the same folds (the cross-model contrast) | `sl_ladder` rebuilt linked table + `wp4_00` folds | ✅ executed (independent-rebuild version) |

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
- ~~**The decision half of WP5 is blocked.**~~ — **PARTLY RECOVERED by `wp5_05`.** Whether exposure
  construction *flips an alert* is answerable from the frozen predictions alone, to within a bounded
  envelope: exposure construction moves **1–3%** of alerts against **10–14%** for deleting the whole
  climate block. What still needs the design matrices is ΔAUC and Δcalibration under each build.
  **Third time the check-whether-the-blocker-covers-all-of-it test recovered work recorded as
  blocked** (after §3.2 and §3.5) — it is now standard practice, not a one-off.
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
second. **Seventeen districts move down, nine up** (corrected 2026-08-15 from "fifteen / eleven",
which was introduced in this README and never appeared in `wp5_01`; recomputed from the twin table,
identical under either baseline arm — see `manuscript/wp4_wp5_sections/wp4_wp5_number_provenance_v1.md`).

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


## What wp5_05 establishes — exposure construction changes alerts, and ΔNB cannot see it

Plan §3.3 splits like §3.2 and §3.5 did. The *registered re-run* (ΔAUC, Δcalibration, ΔNB under a
refit) needs the design matrices. Three other things do not, and together they bracket the answer:
an **exact, model-free flip curve**; an observed **ceiling** (`full` vs `noclim` on identical rows);
and a **transfer coefficient estimated** from `logit(full) − logit(noclim)` regressed on exposure.
16/16 QC → `Manuscript_Figures/wp5/WP5_F7_decision_flip_envelope.{pdf,png}` (6 panels, double
column) + `wp5_decision_flip_envelope_srilanka_v1.csv`.

**Exposure construction moves real alert decisions.** At p\* = 0.30, across four regression
specifications: **A′→B 35–76 alerts (0.9–1.9%)**, **A′→C 64–104 (1.6–2.6%)**. Deleting the entire
climate block moves **441 (11.2%)**. So the construction choice carries **14–24%** of the climate
block's decision leverage — far from nothing, far from everything. Cluster-bootstrap CI at the
district level, p\* = 0.30: A′→B 1.94% [1.27, 2.65], A′→C 2.45% [1.50, 3.57].

**The headline result is methodological, and it should reach the manuscript.** `ΔNB` stays within
**±0.002** while the flip count is unambiguously non-zero. That is *not* flips cancelling by
direction — they are strongly asymmetric (A′→B adds 67 alerts, removes 9). It is structural: **a row
can only flip if it sits near p\*, and threshold-adjacent rows have an event rate ≈ p\*, which is by
definition the break-even rate.** Measured, the flipped-row event rate tracks p\* across both rungs
and all four thresholds (0.087 / 0.160 / 0.289 / 0.431 against 0.10 / 0.20 / 0.30 / 0.40; r = 0.96).
**Every flip is worth ≈ 0 net benefit in either direction.** Therefore `ΔNB` is *structurally*
insensitive to any perturbation acting near the threshold, and a near-zero `ΔNB` must **not** be read
as "exposure construction does not affect decisions". The flip count answers that question; `ΔNB`
answers a different one.

**The exact half survives any objection to the estimated half.** The flip curve is a property of the
frozen predictions: a perturbation of 0.02 in predicted risk cannot flip more than ~6.4% of alerts at
p\* = 0.30, whatever generates it. Every estimate is asserted against that bound in the notebook.

**Flips need a displacement *and* a prediction near the threshold.** Across the 26 districts the flip
count correlates with the induced prediction shift but not with displacement alone — so, one step on
from `wp5_03`'s finding, naming "exposure-sensitive districts" from the exposure contrast names the
wrong set for decisions too.

**Sensitivity to the missing artifact is measured, not asserted.** The transfer coefficient's norm
spans **2.3×** across four specifications (R² 0.27–0.38, signs stable throughout), but the flip count
spans much less — the flip curve is locally near-linear. β would have to be understated several-fold
before exposure construction reached the ceiling, so the *qualitative* answer is robust to what §5.1
would supply.

### What wp5_05 found about the frozen artifact itself

**`full_recal` is not a monotone recalibration of `full_raw`, and the team needs to know.** Sorting
by `full_raw`, **49%** of adjacent `full_recal` pairs are inverted, and the AUCs differ: **0.7715 raw
vs 0.7512 recalibrated**. A monotone recalibration cannot change AUC. The cause is in the repo —
`analysis/v12_referee_response/run/sl_matched_and_recal.py` §(B) applies a **past-only rolling-52-week
intercept update refitted at every test week**, so the map is time-varying and re-ranks *across*
weeks. **Within** a week it is an exact constant shift in logit space (147 of 151 weeks; the four
exceptions are consecutive Jan–Feb 2024 weeks that fall back to the intercept-slope variant), with
**zero inversions inside any week**. Consequences: every reported AUC must say which column it came
from, and "recalibration does not affect discrimination" is false for this artifact.

### Traps this notebook adds

- **`WK.shift` is a DataFrame method.** A column named `shift` is shadowed by `DataFrame.shift`, so
  attribute access returns the method and fails with an `AttributeError` about a *function* — the
  same failure mode already recorded here for `d.pop` / `pop_sum`.
- **A near-zero ΔNB is the expected result of a threshold-local perturbation, not evidence of a
  null.** See above; this is the notebook's main finding and the easiest number in it to misread.

## What wp5_07 establishes — F8 exists, and the biggest signal in it is a warning

Plan §3.6 was recorded here as downstream of the blocked refit. **It was not** — per-district
calibration slope/intercept, per-district ΔNB and per-district flip counts are all reductions of the
*frozen predictions*, and every modifier is already staged by M6 batches A/B. **Fifth recovery by the
does-the-blocker-cover-all-of-it test.** 16/16 QC →
`Manuscript_Figures/wp5/WP5_F8_miscalibration_structure.{pdf,png}` + two quarantine tables.

Four responses × 15 pre-specified modifiers = **60 tests, BH-FDR across the whole grid**; 19 reach
raw p<0.05, **6 survive**. All 60 are plotted in panel (e) — the figure cannot be read as a selected
subset.

- **The strongest association in the screen is not geospatial and is near-tautological.** Calibration
  *intercept* tracks the district's own alert prevalence at **ρ=0.85, q<0.001**, because an intercept
  absorbs a base rate. `prev` was carried through the panel **as a deliberate decoy**; without it,
  any modifier correlated with outbreak burden would have inherited that association silently. **Keep
  the decoy in any screen of this shape.**
- **Miscalibration has real spatial structure.** Calibration slope spans **0.67–2.23** and tracks
  cropland fraction (**ρ=0.61, q=0.031**) and land-cover diversity (0.59, q=0.032) up, population
  density down (−0.50). All survive adjustment for prevalence (partial ρ 0.50 / 0.49 / −0.44).
  Predictions are too spread out in dense built-up districts, too compressed in agricultural ones.
- **Flips concentrate in the highlands — and the attribution is NOT identified.** Badulla 9.9%,
  Nuwara Eliya 9.3%, Ratnapura 6.0%; flip rate tracks slope/elevation/HAND (ρ≈0.55, q≈0.035). But
  **elevation and the measured B→C displacement are collinear at ρ=0.74** and *neither survives
  controlling for the other* (0.27 p=0.18; 0.05 p=0.82). Reported as a concentration, not as
  "terrain drives the flips". n=26 cannot separate them.
- **ΔNB has no spatial structure at all** — strongest of 15 is population density at ρ=0.40, **q=0.15**.
  Given `wp5_05` this is expected, not a second null: **the same threshold-local blindness that
  flattens ΔNB nationally flattens it district by district. Third independent appearance.**
- **Explanatory only.** Nothing here may re-enter the ladder as an accuracy predictor; stamped
  `EXPLORATORY_EXPLANATORY` in the provenance.
- **Environment:** `freight-eda` (needs `statsmodels` for the per-district logits) — same kernel as
  `wp4_02`, not `pywmp-mac`.

## Why WP4 is half-finished, and which half

`instruction_m6.md` corrected "WP4 complete" to *fold design complete until models are evaluated
under the folds*. The **cross-model** evaluation is genuinely blocked: re-fitting M5/M0/M1/M2 under
spatial folds needs each model's **design matrix**, and `ALT_STATS/frozen/srilanka_matched_pairs.csv`
carries **predictions only**. A spatially-CV'd M6 set against a temporally-split M5 would be an
artifact, not a comparison.

**But that argument only bars the cross-model contrast.** M6 under spatial folds against M6 under the
temporal split is a *within-model* contrast — same features, same labels, same test rows, only the
validation scheme moving — and it is a **better** instrument for WP4's question than the cross-model
version would be, because nothing else varies. `wp4_02` does exactly that; see below.

**Consequence for the §5.1 ask: it still unblocks three items** — §4 (threshold generator), §8
(matched geomatics ablation) and WP4's *cross-model* re-run. `wp4_02` **raises** the priority of the
third rather than lowering it (see below).


## What wp4_02 establishes — the folds are NOT cheap, and wp4_01's inference does not survive

M6 re-fitted **1,456 times** across four arms on the same 3,926 frozen test rows, 14/14 QC →
`Manuscript_Figures/wp4/WP4_F_fold_effect_within_m6.{pdf,png}` (6 panels) plus three tables in the
quarantine. **The baseline arm reproduces the committed M6 to 8.6e-15**, so every difference below is
the validation scheme and nothing else; §9.1 shows the selected `C` is effectively constant across
arms, so it is not a shrinkage effect either.

**The design point that makes it mean anything.** Removing a district's neighbours from training
removes spatial leakage *and* training data, and both push performance down. So every buffered fold
is matched against a **random-district control trained on the same number of districts**. The
buffered-minus-matched gap is the part attributable to geography; the rest is the price of a smaller
training set. Without that control this would have measured sample size and called it leakage.

| buffer | train districts | buffered AUC | matched control | gap | controls below |
|---|---|---|---|---|---|
| 0 km (adjacency, `wp4_01`'s pick) | 21 | 0.5649 | 0.5873 | **−0.022** | 0 of 10 |
| 25 km | 19 | 0.5714 | 0.5897 | −0.018 | 1 of 10 |
| 50 km | 15 | 0.5582 | 0.5767 | −0.018 | 2 of 10 |
| 75 km | 12 | 0.5162 | 0.5777 | **−0.062** | 0 of 10 |
| 100 km | 9 | 0.5024 | 0.5726 | **−0.070** | 0 of 10 |

Reference points: temporal split **0.6008**, LOOCV with no buffer **0.5923**. At 100 km the
spatially-blocked estimate is **0.502 — chance** — while a random training set of the *same size*
still reaches 0.573. **M6's apparent skill depends materially on having geographically nearby
districts in training.**

**Where it is resolvable and where it is not.** Cluster-bootstrap CIs (2,000 replicates, districts
resampled, control ensemble averaged inside each replicate): buffered − control mean is
**−0.022 [−0.055, +0.011]** at 0 km — spans zero — and only excludes zero at **75 km
(−0.061 [−0.119, −0.008])** and **100 km (−0.068 [−0.143, −0.001])**. With 26 districts the bootstrap
has little to work with; that is `wp4_00`'s power finding arriving from the other direction.

### This qualifies wp4_01, and the qualification is the transferable part

`wp4_01` found residual Moran's I indistinguishable from its null at every distance band and
concluded **"the buffered scheme is cheap"**. Direct measurement does not support that.
**Residual spatial autocorrelation and dependence on spatially proximate training data are different
quantities**, and here they disagree. Moran's I on residuals asks *"having fitted on everyone, is
what is left over spatially clustered?"*; a buffered fold asks *"can this model generalise to a
region it has never seen?"* A model can pass the first and fail the second — M6 does.

**So plan §4.1's design — select the operative radius from a residual-range analysis — cannot be
relied on to price the folds.** The price has to be measured. `wp4_00`'s power table bounds how well
it can be measured with 26 units.

**This raises the stakes on §5.1.** M5's external-validation claim rests on a temporal split. If M5
depends on spatial proximity the way M6 does, spatial CV would move it too — which is precisely the
reviewer concern WP4 exists to answer, and it cannot be tested without M5's design matrix. Note this
cuts the **opposite** way from `wp5_05`, where §5.1 turned out to matter less than assumed: the two
asks are not interchangeable and should not be bundled when they are put to the PI.

**Not one district's doing.** 17 of 26 districts lose AUC under adjacency buffering and 9 gain
(§12); Batticaloa, Kurunegala and Puttalam lose most, Ratnapura gains most. No single fold drives the
pooled result.

**What it does not establish.** Nothing about the study's headline comparison — M5 cannot be re-fitted
(`cross_model_rerun: false` in the provenance). Nothing about M6's absolute performance: the label
carries the `EXPLORATORY_RECONSTRUCTED_TARGET` caveat (19.2% of test rows), identical across arms so
it cannot manufacture a difference, but enough to bar quoting any single AUC. And nothing about
**Colombia**, where §4.3's block CV over ~1,000 municipalities is where the well-powered claim
actually rests.

### Environment

`wp4_02` runs on the **`freight-eda`** kernel (`/Users/mpcr/aj/Rhee/0_EDA/.venv`, Python 3.9.6,
sklearn 1.6.1) because **`pywmp-mac` has no scikit-learn**. The `wp5_*` notebooks stay on
`pywmp-mac`. Nothing in `wp4_02` touches the raster stack, so the two environments never need
reconciling.

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

## What wp4_02b establishes — M5's folds are cheap where the study uses them and expensive beyond, and the climate increment survives

`wp4_02` measured the fold effect inside M6 because the cross-model contrast was recorded as blocked:
the archive holds M5's *predictions*, not its design matrix. **That justification does not survive
inspection.** `analysis/v12_referee_response/run/sl_matched_and_recal.py` carries the design-matrix and
cross-basis builders in full, and `notebooks_sl_ladder/` rebuilt the linked table they read. **Sixth
recovery by the does-the-blocker-cover-all-of-it test** — and the one that had been shaping scope longest.

**What it is not.** The frozen linked table has never been on this machine, so M5 is refitted on the
rebuild (ERA5 0.25° + CHIRPS). Fidelity is measured, not assumed: 3,926 test rows matched exactly,
label agreement **0.988**, M5 AUC **0.7570** here against the frozen **0.7715**, no-climate **0.7323**
against **0.7513**, ρ = 0.881 full and 0.976 no-climate. **This is an independent-rebuild version of
the registered re-run and must never be reported as the registered one.** Every contrast below is
within-rebuild, so the offset is common to all arms and cannot manufacture a fold effect.

### The result: M5's answer is not M6's

| radius | buffered | size-matched control | gap | ΔNB gap | controls below |
|---|---|---|---|---|---|
| 0 km | 0.7411 | 0.7177 | **+0.0233** | +0.0110 | 10/10 |
| 25 km | 0.7344 | 0.7212 | +0.0132 | +0.0071 | 9/10 |
| 50 km | 0.7078 | 0.7171 | −0.0092 | −0.0014 | 2/10 |
| 75 km | 0.6842 | 0.7171 | −0.0329 | −0.0217 | 1/10 |
| 100 km | 0.6500 | 0.7026 | **−0.0526** | −0.0355 | 0/10 |

**At the operative radius the folds are not merely cheap — the buffered fold BEATS an equally-sized
random training set** (+0.0233, z = 2.09, every one of ten controls below it). M6 lost 0.022 at the
same radius. The two models disagree in **sign** at 0 km and agree at 100 km, which is why
`wp4_02`'s within-M6 result could never have stood in for this one: *the price of a fold is a
property of the model, not of the geography alone.*

**Read the significance honestly.** On AUC, **every** buffered-minus-control interval spans zero,
100 km included (−0.0505 [−0.1107, +0.0064]). On net benefit at p\* = 0.30 the 75 km
(−0.0216 [−0.0412, −0.0039]) and 100 km (−0.0353 [−0.0610, −0.0120]) intervals exclude it. So the
defensible claim is **a monotone, one-signed trend that reaches conventional significance only on
the decision metric and only past 50 km** — n = 26 is the binding constraint, exactly as `wp4_00`
priced it.

### The climate increment is what the paper claims, and it survives

| arm | ΔNB (M5 − no-climate) | change vs temporal |
|---|---|---|
| temporal split | +0.0071 | — |
| LOOCV, no buffer | +0.0057 | — |
| buffered 0 km | +0.0218 | +0.0148 [−0.0095, +0.0420] |
| buffered 25 km | +0.0200 | +0.0130 [−0.0086, +0.0370] |
| buffered 50 km | +0.0266 | +0.0192 [−0.0053, +0.0437] |
| buffered 75 km | +0.0152 | +0.0078 [−0.0189, +0.0344] |
| buffered 100 km | −0.0015 | −0.0088 [−0.0325, +0.0162] |

**Under spatial CV the climate block earns at least as much as it does under the temporal split**, at
every radius up to 75 km, and every change-vs-temporal interval spans zero. This is the direct answer
to *"your CV ignores spatial autocorrelation, so your increment is inflated"*: it is **not** inflated
by the temporal split — if anything the temporal split is the conservative choice. The point estimates
running *above* temporal are not claimed as a real gain; the intervals cover zero and the honest
reading is *unchanged*.

### Where the spatial dependence lives, and where it does not

Panel (e). The no-climate twin's gap is nearly flat (+0.0072 → −0.0154 across the radii) while M5's
falls to −0.0526. **Most of what long-radius blocking removes is in the climate block** — which is
coherent: climate fields are spatially smooth over hundreds of km, so a neighbour's rainfall is a
usable proxy for yours in a way a neighbour's case history is not.

### Traps this notebook adds

- **A held-out district's fixed effect is not estimable.** M5 carries an RDHS dummy per district; hold
  one out and its column is all-zero in training, so it is scored at the reference district's
  intercept (`LK11`, dropped by `drop_first`). **Therefore every temporal-versus-fold contrast
  conflates losing the neighbours with losing the fixed effect** — only buffered-minus-control
  separates them, because the control carries the identical handicap. This is the M5 analogue of
  `wp4_02`'s sample-size confound and it needs the same matched-control cure.
- **Pooled AUC and per-district AUC answer different questions.** At 0 km the pooled gap is
  **+0.0233** while **15 of 26 districts are individually negative**. Pooling rewards getting the
  between-district ordering right; the per-district table does not see that at all. Quote the one you
  mean. (At 100 km the two agree: 17 of 26 negative.)
- **The frozen pipeline imputes missing lags with a train-set mean over all districts**, which is a
  cross-district touch under a spatial fold. It is bounded here rather than waved past: 182 rows
  (1.73%) have an incomplete lag window, **0 of them in the test split**, so no imputed row is ever
  predicted on.
- **`pd.concat` keeps both frames' indices**, and `pd.crosstab` then reindexes — duplicate labels
  raise `cannot reindex on an axis with duplicate labels`. Reset the index after concatenating.
- **Environment: a third one.** `wp4_02b` runs on the **`python3` kernel → `/Users/mpcr/aj/Dengue/.venv`**
  (3.14.6, sklearn 1.9.0) — the only env here with sklearn + patsy + statsmodels that reproduces
  `sl_04` to **exactly 0.0**. `wp5_*` stays on `pywmp-mac`, `wp4_02` on `freight-eda`.
