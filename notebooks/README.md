# M6 — Geomatics-only model · Python notebooks

Step-by-step build of the **M6 geomatics-only model** (`docs/M6.md`), in Jupyter so every
intermediate is visible and verifiable rather than hidden behind a script.

**Owner:** Geospatial Lead · **Status:** complete — M6 fitted, scored and plotted on the frozen test
panel. Result is an **exploratory honest null**, pending PI framing sign-off (`docs/M6.md` §0).

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
| 04 | `04_feature_assembly.ipynb` — epi-week join, lags 0–8, leakage + QC | 01, 02, 03 | ✅ executed |
| 05 | `05_label_and_row_mask.ipynb` — outcome, time axis, label, row set | 04 + WER outcome | ⚠️ executed → **STOP** |
| 06 | `06_fit_m6.ipynb` — fit + Platt calibration | 05 + thresholds | ✅ executed |
| 07 | `07_evaluation.ipynb` — AUC, calibration, net benefit, bootstrap | 06 | ✅ executed |
| 08 | `08_figures.ipynb` — manuscript figure set | 07 | ✅ executed |

### Notebooks 06–08 now run on recovered labels

The label thresholds were **recovered exactly** (2026-08-07, decision log). `QUOTABLE == True`,
outputs carry no `_PROVISIONAL` suffix, and notebook 06 asserts the acceptance test —
**3,926 / 3,926 = 1.000000** against the frozen outcomes — before it fits anything, so the gate is
permanent rather than a one-off check.

How the thresholds were recovered, since it is not obvious: the label is a fixed **incidence**
threshold, so in count space it scales with population, `thr_count(d,y) = K(d) × WP(d,y)`. Solving
the frozen test outcomes for a feasible `K(d)` gave all 26 districts a non-empty interval — 78
constraints met by 26 free parameters, which is the validation. WorldPop **G2 R2025A constrained**
supplies the year ratios (the census anchor cancels in ratios); the computed 2024 national total of
23,008,641 matches the denominator build report's "raw WorldPop was 23,008,642" to one person,
confirming the release. This recovers the values *actually used* rather than re-executing the
procedure, which sidesteps the `exposure_missing_flag` subtlety entirely.

All three transcribe their machinery from `scripts/colombia_model_ladder_h4_75pct_M6_v1.py` rather
than reimplementing it (`design`, `fit_select`, `platt`, `nb`, `citl_slope`, the RDHS cluster
bootstrap at seed 20260612 / B=1000). That is what makes M6 comparable to the ladder at all.

### The result

M6 on the 3,926 frozen test rows, raw predictions, RDHS cluster bootstrap B=1000:

| model | AUC [95% CI] | PR-AUC | Brier | NB@0.30 [95% CI] |
|---|---|---|---|---|
| **M6 (geomatics only)** | **0.601 [0.568, 0.638]** | 0.442 | 0.223 | **0.058 [0.033, 0.085]** |
| M5 full hybrid | 0.771 [0.741, 0.804] | 0.667 | 0.180 | 0.145 [0.106, 0.184] |
| M5 no-climate | 0.751 [0.721, 0.782] | 0.652 | 0.191 | 0.135 [0.100, 0.176] |

ΔNB(M6 − M5full) **−0.087 [−0.112, −0.062]**; ΔNB(M6 − M5noclim) **−0.078 [−0.104, −0.054]**;
0.000 of bootstrap replicates favour M6 in any contrast. M6's net benefit (0.058) barely clears
treat-all (0.052).

Per the pre-specified §10 rules this is the **expected honest null** — a purely spatial landscape
model carries little standalone decision value — which strengthens the paper's caution. **No
headline changes.** Three caveats stand: contrasts are against M5-full and M5-no-climate only
(M0/M1/M2 absent, so §10's "beats season / climate-only" is still unanswerable); 11.3% of test rows
carry forward-filled MODIS features from the 2025 gap (fresh-MODIS subset: AUC 0.612, NB 0.065 —
same conclusion); and M6 is Platt-recalibrated while the comparators are rolling-52, which is why
the raw columns are primary.

Two design properties worth keeping in view: `C` selects at the **lower edge** of the ladder's grid
(not widened — that would diverge from the shared machinery — so reported instead), and
Platt-on-validation mis-centres M6 because validation prevalence sits well below test.

### The figure set (notebook 08)

Three figures, written to `Manuscript_Figures/m6/` as PDF (vector, TrueType embedded) **and** PNG at
600 dpi, sized to the journal column (89 / 183 mm) and never rescaled:

- **F1 — discrimination and decision value, side by side.** ROC in panel (a), decision curve in
  panel (b). They share a figure deliberately: "discrimination is not decision value" is the paper's
  central claim, and a model can look respectable in (a) while sitting under *treat all* in (b).
- **F2 — calibration.** Decile bins with **cluster-bootstrap** intervals over the 26 RDHS.
  `ALT_STATS/PREANALYSIS_ALT_STATS.md` §5 rules out Wilson intervals because observations are
  clustered within districts, so binomial bars would be far too narrow.
- **F3 — contrasts.** ΔAUC and ΔNB against each frozen comparator, with 95% percentile
  cluster-bootstrap intervals and zero drawn as the reference.

Style is defined in **one** block reused by all three — copy-pasting per figure is how a set drifts.
Colours are the Okabe–Ito subset, which passes all six checks of the `dataviz` validator (worst
adjacent pair ΔE 11.0 deutan, 25.8 normal vision); identity is *also* carried by dash pattern and
marker, so nothing depends on hue in greyscale. No titles are drawn inside the images — captions are
emitted as text for the manuscript. §8 asserts every figure is newer than the metrics that produced
it, since stale figures beside updated tables is the most common submission defect.

If a run is ever provisional again, each figure is **stamped `PROVISIONAL` across its face**, not
merely in its filename — a CSV rarely leaves the repo without its provenance, but a PNG does
constantly, and once it is in a slide only what is drawn on the image survives.

### Where notebook 05 stops, and why

`M6.md` §11 makes *"labels/thresholds get recomputed"* a **STOP** condition. Notebook 05 goes as far
as that rule allows and then halts rather than fitting against a label it reconstructed.

It resolves a lot on the way. The outcome table is restaged from source on this machine (415 of 416
WER issues, QC passed). The **time axis is settled empirically**: WER issue *N* covers the epi-week
beginning **ISO-Monday(*N*) − 7 days**, measured by testing candidate offsets against 3,926 frozen
labels (98.3% agreement at the correct offset, 82.4% at the nominal one). The label *rule* is
confirmed — 23 of 26 districts admit a single threshold reproducing every frozen label — and every
one of the 68 residual disagreements sits within a case or two of the threshold, so the rule, the
join and the case series are all right and only the threshold *values* are unknown.

No training window or percentile method reproduces those values (best: 14 of 23). So the ask is now
**26 numbers**: the Sri Lanka label/threshold table, or the SL analogue of
`scripts/colombia_label_construction_v1.py`, which is not in this repo.
`data_quarantine/m6_geomatics/m6_implied_thresholds_srilanka_v1.csv` holds the acceptance intervals
— correct thresholds must land inside them for all 23 recoverable districts, which is a one-look
check for whoever holds the file.

### The panel blocker was smaller than notebook 04 recorded

Notebook 04's design notes said M6 was blocked on the M1/M2/M5 panel spine. In fact
`ALT_STATS/frozen/srilanka_matched_pairs.csv` is committed here and **is** the complete Sri Lanka
test panel — 26 districts × 151 consecutive weeks = 3,926 rows, no subsetting, carrying the outcome
*and* frozen comparator predictions. "Matched pairs" means the two *models* are paired on identical
rows, not that observations were matched. All 3,926 rows have complete M6 features.

One caveat for §10: the frozen artifact carries **M5-full** and **M5-no-climate** predictions, not
M0 / M1 / M2 separately. So "does landscape beat season or climate-only" cannot be answered from
this repo; "does landscape add against the full hybrid, and against it stripped of climate" can.
Either obtain M0/M1/M2 test predictions on these rows, or restate §10's contrasts.

Notebook 04 produces `m6_features_weekly_srilanka_v1.csv` — 10,868 rows (26 districts × 418 weeks) ×
101 columns. It is deliberately **not** named `m6_model_matrix_…`: `M6.md` §8 reserves that name for
the table joined onto the M1/M2/M5 panel spine with its labels and split flags, and that panel is not
staged here. Notebook 04's spine is a candidate superset for notebook 05 to intersect, and carries
`geometry_id` (`LK11`…) alongside `rdhs_id` so that join is possible.

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
- **`pandas.merge_asof` does not preserve the left frame's index.** It needs the left sorted by the
  join key and returns a fresh `RangeIndex` in *that* order, so writing the result back with
  `df[col] = joined[col].values` assigns cut-date order into district-major order and scrambles
  every value across districts and weeks. The column stays full, seasonal and correctly ranged;
  notebook 04's leakage and monotonicity checks all still passed, because each re-derives its own
  frame and is self-consistent within it. What caught it was the variance cross-check — scrambling
  destroys between-district variance, so NDVI's within-district share read 93% against 29% at
  source. Notebook 04 §8 now joins on the keys and asserts alignment, and §12 re-derives a stored
  column and compares.
- **Both MODIS products are absent 2025-07-04 → 2025-11-17.** ~4.5 months missing from LST *and*
  VI, so it is source-side, not cloud. Forward-fill would hold a "dynamic" feature constant across
  a whole monsoon; notebook 04 §7 flags the 22 affected weeks rather than filling them quietly.
  Re-run notebook 02's search before treating it as permanent — the catalogue may have caught up.
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
