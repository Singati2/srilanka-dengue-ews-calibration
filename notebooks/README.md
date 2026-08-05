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
| 01 | `01_terrain_batchA.ipynb` — elevation, slope, TWI, HAND | geometry + internet | ✅ executed |
| 02 | dynamic layers — MODIS LST, NDVI, surface water | internet | planned |
| 03 | feature assembly + QC | 01, 02 | planned |
| 04 | label + row mask | **outcome table (unstaged)** | blocked |
| 05 | M6 fit + calibration | 04 | blocked |
| 06 | evaluation — AUC, calibration, net benefit, bootstrap | 05 | blocked |
| 07 | results figures and infographics | 06 | blocked |

Notebooks 05–06 will **port the fitting, Platt recalibration, net-benefit and cluster-bootstrap
code verbatim** from `scripts/colombia_model_ladder_h4_75pct_M6_v1.py` rather than
reimplementing it — that is how M6 stays scored by identical machinery.

## Data sources — all free, no account, no API key

Deliberately avoids Google Earth Engine. Pinned granule IDs plus checksummed local rasters are
more reproducible than an Earth Engine run, whose collections can be revised underneath you.

| Layer | Source | Auth |
|---|---|---|
| Elevation → slope, TWI, HAND | Copernicus GLO-30 (AWS Open Data) | none |
| Land cover, built-up, cropland | ESA WorldCover 10 m (AWS) | none |
| Surface water | JRC Global Surface Water | none |
| Forest cover | Hansen GFC | none |
| Population | WorldPop | none |
| Wealth / SES | Meta Relative Wealth Index (HDX) | none |
| Healthcare access | OSM via Geofabrik | none |
| LST, NDVI/EVI | MODIS via Microsoft Planetary Computer STAC | none |

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
