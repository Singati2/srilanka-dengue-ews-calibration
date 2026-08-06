# M6 — Geomatics-only model · Python notebooks

Step-by-step build of the **M6 geomatics-only model** (`docs/M6.md`), in Jupyter so every
intermediate is visible and verifiable rather than hidden behind a script.

**Owner:** Geospatial Lead · **Status:** in progress — feature extraction underway, modelling
blocked on data staging.

---

## Scope boundary — read this first

These notebooks build **new** geomatics work only. They do **not** touch, port, or re-run the
frozen analysis behind the manuscript.

The tags `v6-analysis-frozen`, `alt-stats-results-v1/v2` reproduce the published numbers under
seed 20260612, and the manuscript stakes its reproducibility claim on them. Nothing here
modifies that pipeline.

## What M6 is

A model whose predictors are spatial / remotely-sensed landscape layers **only** — no recent case
counts (that is M1), no ERA5/CHIRPS reanalysis climate lags (that is M2).

It is an **exploratory sensitivity comparator, not a headline model**. The question: *does a
purely spatial model carry standalone early-warning signal, and does it beat season (M0) or
climate-only (M2) on net benefit?* The expected honest answer is no or marginal, and that null
is a legitimate result.

**Comparability rule** (`docs/M6.md` §0): M6 must be scored on the **identical test rows** as
M1/M2/M5, with the same evaluation code, split, threshold and bootstrap seed. If it cannot score
the same rows — stop.

### A spec conflict, resolved

`docs/M6.md` §0 defines M6 as geomatics-only with *no reanalysis climate*, while
`docs/maup_sensitivity_and_spatial_cv_plan.md` §4a lists temperature, precipitation and humidity
among the geomatics factors. These notebooks follow **`M6.md`**: admitting reanalysis climate
would collapse M6 into "M2 plus extras" and make the research question unanswerable. Dynamic
*remotely-sensed* layers (LST, NDVI, surface water, nightlights) are in — they are satellite
observations, not reanalysis.

### Static predictors cannot produce a temporal signal

Most of the 16 M6 variables — elevation, slope, TWI, HAND, built-up, wealth, healthcare access —
are static per district. A model built only from these emits **one constant prediction per
district for every week**. Against a weekly elevated-activity label it can express *which*
districts differ but never *when*, so it scores near chance **by construction**.

That null would be structural, not empirical, and must not be reported as "geomatics carries no
signal". The dynamic layers in notebook 02 are what make M6 a real test.

---

## Notebooks

| # | Notebook | Needs | Status |
|---|---|---|---|
| 00 | `00_setup_and_geometry.ipynb` — frame, CRS, adjacency | geometry only | ✅ executed |
| 01 | `01_terrain_batchA.ipynb` — batch A: elevation, slope, TWI, HAND | geometry + internet | ✅ executed |
| 02 | `02_dynamic_modis.ipynb` — batch C: MODIS LST, NDVI/EVI | internet | ✅ executed |
| 03 | `03_batchB_statics.ipynb` — batch B: land cover, fragmentation, water, population, nightlights | internet | ✅ executed |
| 04 | feature assembly + QC — epi-week join, lags 0–8 | 01, 02, 03 | planned |
| 05 | label + row mask | **outcome table (unstaged)** | blocked |
| 06 | M6 fit + calibration | 05 | blocked |
| 07 | evaluation — AUC, calibration, net benefit, bootstrap | 06 | blocked |
| 08 | results figures and infographics | 07 | blocked |

Batch C (dynamic) was built before batch B (static) deliberately: the dynamic layers are the ones
that decide whether M6 is answerable at all (see *Static predictors* above), so they were worth
settling first. Notebook 02 §15 confirms they carry the temporal variance the static layers
cannot.

Notebooks 06–07 will **port the fitting, Platt recalibration, net-benefit and cluster-bootstrap
code verbatim** from `scripts/colombia_model_ladder_h4_75pct_M6_v1.py` rather than
reimplementing it — that is how M6 stays scored by identical machinery.

## Data sources — all free, no account, no API key

Deliberately avoids Google Earth Engine. Pinned granule IDs plus checksummed local rasters are
more reproducible than an Earth Engine run, whose collections can be revised underneath you.

| Layer | Source | Auth | Used in |
|---|---|---|---|
| Elevation → slope, TWI, HAND | Copernicus GLO-30 (AWS Open Data) | none | 01 |
| LST, NDVI/EVI | MODIS MOD11A2 / MOD13Q1 via Planetary Computer | none | 02 |
| Land cover → built-up, forest, cropland, fragmentation | Impact Observatory `io-lulc-annual-v02` 10 m, annual | none | 03 |
| Surface water | JRC Global Surface Water v1.4 | none | 03 |
| Population | WorldPop UN-adjusted 100 m | none | 03 |
| Nighttime lights | HREA (VIIRS-derived) — *substitute, see below* | none | 03 |
| Wealth / SES | Meta Relative Wealth Index (HDX) | none | batch D |
| Healthcare access | OSM via Geofabrik | none | batch D |

**Two deliberate substitutions**, both recorded in the notebooks and in `docs/M6.md`'s terms:

- **`io-lulc-annual-v02` instead of ESA WorldCover.** WorldCover exists only for 2020 and 2021;
  Impact Observatory's is annual, and vintage is the binding constraint (notebook 03 §2). It also
  supplies built-up, forest and cropland from one mutually consistent classification.
- **HREA instead of monthly VIIRS DNB.** The monthly composites require a registered Earth
  Observation Group account — a genuine access barrier, the one condition under which the
  2026-07-07 decision permits substitution. HREA is built from the same sensor and is anonymous,
  at the cost of being annual rather than monthly.

## Running them

```bash
uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python -r notebooks_requirements_lock.txt
.venv/bin/jupyter lab
```

Run in order — notebook 01 asserts against the provenance record notebook 00 writes, and will
stop if the geometry has changed underneath it.

Outputs are committed with the notebooks so results can be read without re-running.

## Data hygiene

Everything the notebooks download or derive goes to `data_quarantine/m6_geomatics/`, which is
gitignored. **Rasters, feature tables and predictions are never committed** — code and reports
only, per `docs/maup_sensitivity_and_spatial_cv_plan.md` §5.

Each notebook writes a `nbNN_provenance.json` with input checksums, parameters and the seed, so
any feature table can be traced to the exact bytes that produced it.

## Traps found along the way

Recorded because each one is silent — the code runs and returns plausible numbers either way.

- **`modis-11A2-061` and `modis-13Q1-061` each contain two platforms.** Terra (`MOD*`, ~10:30
  overpass) *and* Aqua (`MYD*`, ~13:30). Grouping granules by date and tile without checking gives
  you whichever the catalogue listed first, so a series can switch platform mid-record and the
  step change looks like climate. Notebook 02 selects on the **product id prefix** — not the STAC
  `platform` field, which is empty for some items.
- **A few (composite, tile) pairs appear twice** as reprocessing versions. Resolved to the newest
  `created`, so the selection is deterministic rather than arrival-ordered.
- **Mandatory-QA-0 only is not a usable LST filter here.** It retains 14–42% of land pixels on the
  composites measured and empties whole districts. Worse, the pixels it drops are the cloudy, wet
  weeks — exactly the ones a dengue model cares about, so the series would be biased warm and dry.
  Notebook 02 §8 measures the options and adopts mandatory QA ≤ 1 with LST error ≤ 2 K.
- **Uncovered mosaic pixels read as 0**, which is a legal NDVI DN (≈ bare ground) and a legal QC
  byte. Tiles are therefore placed by their true extent with an explicit coverage mask, not by a
  sentinel fill value.
- **A bbox search on `io-lulc-annual-v02` returns a UTM *zone 1* granule** (`01N`, the Pacific)
  alongside Sri Lanka's `44N`/`44P`. Because MGRS tiles share a local coordinate frame, `01N`'s
  bounds are *numerically identical* to `44N`'s — so any window computed from coordinates alone
  overlaps it and pastes ocean nodata over the island, silently. Notebook 03 keeps only granules
  whose real extent contains the island **in their own CRS**, then filters by that EPSG.
- **WorldPop totals inside the district mask fall ~3.5% short of the national raster.** Pixels go
  whole to the unit containing their centre, and Sri Lanka is all coastline. Notebook 03 reports
  the capture fraction rather than absorbing it, because WP5's population-weighted build divides
  by that same denominator.

## Known environment notes

- `pysheds` 0.5 calls `np.in1d`, **removed in NumPy 2.0**. Notebook 01 aliases it to `np.isin`
  (the rename; exactly equivalent for the 1-D arrays pysheds passes it). Shim is visible in the
  notebook, not hidden.
- `pysheds.view.ViewFinder` requires a real `pyproj.CRS`; passing `None` raises a bare
  `CRSError`.
- `Grid.compute_hand` needs its drainage mask as a `Raster` with boolean-representable nodata.

## A correction to the plan's CRS guidance

`maup_sensitivity_and_spatial_cv_plan.md` §5 recommends SLD99 or UTM 44N for area weighting.
**Both are transverse Mercator — conformal, not equal-area.** These notebooks use a Lambert
azimuthal equal-area projection centred on the island for all area-bearing computation.

In fairness, the measured effect for Sri Lanka is small: per-unit area error from using UTM 44N
is only −0.044% to −0.080% (quantified in notebook 00). It is the correct default on principle
and will matter more for Colombia, which spans far more latitude.
