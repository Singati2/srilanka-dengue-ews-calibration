# Dengue EWS — Cartography Work Pack (Set 1 + Set 2)

**Purpose:** self-contained handoff to build the study-area (Set 1) and data-availability
(Set 2) map figures on a second machine. Everything the maps need is in this bundle:
public boundary geometry + *aggregate* coverage tables (no raw surveillance data) + the
current figure scripts + this plan. Generated 2026-07-15.

Repo: `github.com/Singati2/srilanka-dengue-ews-calibration` (PRIVATE). This pack ships as
`dengue_map_workpack.zip`, force-added past `.gitignore`.

---

## 0. Project in one paragraph

Retrospective **decision-analytic** evaluation of climate-driven dengue early warning,
benchmarked against recent-case surveillance, in two settings: **Sri Lanka** (primary; 26
RDHS divisions, weekly, 2018–2025) and **Colombia** (second case study; a *selected*
municipality-week subset, 2020–2022). Honest headline: *recent surveillance is hard to
beat; climate adds at most a modest, setting-dependent increment, visible only under
matched specifications, calibration, and decision-curve net benefit.* The paper's whole
credibility rests on **not overclaiming** — this governs every map below.

Manuscript state: `paper1_plos_gph_v31` (`~/Downloads/revision_v31/`). Nine figures, none
spatial yet. These maps are a writing-phase deliverable, **not** new analysis or scope
expansion.

---

## 1. The three map sets (program)

Building **Set 1 then Set 2** now. Set 3 is documented but **deferred** (see §5 — it is
scientifically dangerous and must not be built casually).

### SET 1 — Study area with geographic context
Two figures (or a 2-panel), each a main map + an equal-area locator inset.

- **Sri Lanka:** main = 26 RDHS divisions (`geometry/rdhs_26_v1.gpkg`, EPSG:32644).
  Locator = Asia, Sri Lanka highlighted.
- **Colombia:** main = municipalities (`geometry/gadm41_COL_2.json.zip`, admin-2, EPSG:3116).
  Locator = South America, Colombia highlighted.

**Cartographic rules (state CRS in every caption — referees check):**
- Mains keep their national projected CRS (SL 32644 / CO 3116).
- **Locators must be equal-area, not Web Mercator:** Asia → Lambert Azimuthal Equal Area
  (~80°E/20°N); South America → Albers Equal Area Conic (ESRI:102033). Desaturated grey
  land, study country in one accent, neighbour labels only where they orient.
- Scale bar on each main; light graticule (does the north-arrow job — omit the arrow);
  no drop shadows; no rainbow.
- **Ampara/Kalmunai:** Sri Lanka has 25 admin districts but 26 RDHS units because Ampara
  splits into Ampara + Kalmunai. Show this as a **boundary annotation with a leader line**,
  NOT by spending the panel's fill colour on it (the current script wastes fill on it).

**Signature innovation — true-relative-scale inset.** SL = 65,610 km²; CO = 1,141,748 km²
(**17.4×** larger). Printed equal-size, the reader silently equates them. In the Colombia
panel, drop Sri Lanka's outline **drawn at Colombia's scale** in a corner. One glance = 26
units on a small island vs 1,119 municipalities across a subcontinent. That asymmetry is a
real premise of the paper and no current figure states it.

### SET 2 — Data availability & the analysis subset
This is where the paper's *setting-dependent* thesis becomes visible.

- **One shared sequential ramp across BOTH countries:** *percent of test weeks contributed*,
  0–100%. Same scale, same legend, so the contrast is unarguable.
  - Sri Lanka renders **uniformly saturated** — all 26 units at 151/151 = **100%**.
  - Colombia renders **mostly pale** — median 14/152, **18.5%** overall fill.
- **Missing must NEVER read as a low value** (the classic choropleth lie — and exactly the
  bug in the current Fig1B, see §4). Keep two absence classes OFF the sequential ramp:
  - **grey hatch** = "Observed but excluded" (n=167 munis)
  - **white** = "No usable test-period data" (n=477 munis = all GADM admin-2 not in the
    coverage table)

**Signature innovation — space-time availability raster.** Companion panel: units on y
(sorted by total weeks), the ~152 test weeks on x, one mark per observed cell. Sri Lanka =
a solid black rectangle; Colombia = confetti. Shows what no choropleth can — *which* weeks,
and whether they are contiguous or scattered. This matters directly: the lag features need
**consecutive** weeks, so scattered availability ≠ a short continuous run.

### SET 3 — Results dissemination (DEFERRED — read §5 before building)

---

## 2. Data in this bundle

### `geometry/` — public boundaries (safe to share; these are the only geometry needed)
| file | what | CRS | source |
|---|---|---|---|
| `rdhs_26_v1.gpkg` | Sri Lanka 26 RDHS analytic units (+ `.meta.md`) | EPSG:4326 → reproject 32644 | HDX COD-AB (Survey Dept. of Sri Lanka), Ampara split into Ampara+Kalmunai |
| `gadm41_COL_2.json.zip` | Colombia admin-2 (municipalities), `GID_2` key | reproject 3116 | GADM v4.1 |
| `lka_admin2.{shp,dbf,shx,prj,cpg}` | Sri Lanka admin-2 districts (context/base) | EPSG:4326 | HDX COD-AB |

Load GADM directly from the zip: `geopandas.read_file("zip://gadm41_COL_2.json.zip")`.

### `coverage/` — DERIVED AGGREGATES ONLY (no case counts, no climate values)
- **`srilanka_rdhs_coverage_v1.csv`** — 26 rows.
  `geometry_id, rdhs_name, train_weeks_contributed, test_weeks_contributed,
   test_weeks_available(=151), pct_test_coverage(=100.0 all), coverage_class(=Included)`.
  Join to gpkg on `geometry_id`.
- **`colombia_municipality_coverage_v1.csv`** — 642 rows (every municipality observed in the
  2020–22 test window). `GID_2, test_weeks_contributed, test_weeks_available(=152),
  pct_test_coverage, coverage_class, dept_GID_1`.
  `coverage_class ∈ {Included (n=475), Observed but excluded (n=167)}`.
  **The 477 "No usable test-period data" municipalities are NOT rows here** — derive them on
  the map side: any GADM `GID_2` absent from this table → white. (This is what
  `scripts/make_fig1_v31.py` already does in its `cls()` function.)

These tables are methodological metadata (week counts + a class label), not surveillance
data — that is why they are safe to commit even though raw project data never is.

### `scripts/` — starting points (both currently in `~/Downloads/revision_v31/`)
- `make_fig1_v31.py` — builds the current 4-panel Fig1 (A SL map, B CO coverage, C
  timelines, D flow). **Contains the two bugs in §4.** Best starting skeleton for Set 2.
- `make_map_fig1a.py` — standalone Sri Lanka RDHS map. Starting point for Set 1 panel A.

---

## 3. Key numbers (all reproduced from the bundled tables)

| quantity | Sri Lanka | Colombia |
|---|---|---|
| analytic units | 26 RDHS | 1,119 admin-2 (GADM) |
| units in TEST set | 26 | 642 observed → **475 included**, 167 excluded, 477 no-data |
| test weeks available | 151 | 152 |
| median weeks contributed / unit | **151 (100%)** | **14 (of 152)** |
| overall panel fill | **100.0%** | **18.5%** |
| area | 65,610 km² | 1,141,748 km² (**17.4×**) |
| test alert prevalence | 33.6% | 0.375 (common-complete set) |

The **completeness gulf** (100% vs 18.5%) *is* the setting-dependence result, drawn.

---

## 4. Two bugs in the current Fig1B to fix while building Set 2

1. **Membership coloured as completeness (the important one).** `make_fig1_v31.py` line ~34
   builds `inc` as a *set of GID_2 with ≥1 usable week*, then floods them solid blue under a
   legend that says "common-complete." But 51 of those municipalities contributed a **single
   week** and 196 contributed ≤10 — painted identically to the 3 with all 152. The panel
   makes Colombia look well-covered, which **argues against the paper's own caution.** Fix:
   colour Included by `pct_test_coverage` on the graded ramp (§SET 2).
2. **Hardcoded stray number.** Line ~48 annotation says "Included = 475 of **864**." The
   panel's own legend sums to 475+167+477 = **1,119**. 864 is not computed anywhere and is
   stale. Compute it or cut it (docstring promises "no fabrication").

---

## 5. SET 3 — why it is deferred, not forgotten

A per-district ΔNB choropleth is *available today* (`~/data_quarantine/model_pilots/
targeted_value_climate_stage1a_h4_v1/rdhs_descriptive_dnb_h4_v1.csv`, 26 rows), but **do not
map it naively:**
- Between-district spread (SD **±0.0263**, range −0.0378…+0.0615) is **3× the mean
  (+0.0081)**; the run's own metadata says *no adequately-powered regime CI excludes 0* at
  p*=0.30. A choropleth would render inferential noise as a vivid signal.
- It is the **M5−M1 compound** contrast, which the manuscript explicitly disowns ("does not
  estimate an independent climate effect"). The paper's headline is the **matched**
  contrast (M5 − M5_no-climate). Per-unit *matched* numbers do **not** exist yet — that is a
  new run, and it collides with the analysis freeze.
- Mapping a vivid-but-null effect, under this paper's own thesis that conventional
  evaluation overstates climate value, would be self-defeating.

**Planned honest Set 3 (when we get to it): a lineup / graphical inference plot** (Buja et
al. 2009; Wickham et al. 2010) — hide the real per-district map among 8 null maps; if the
reader cannot find it, the null *is* the finding. Needs per-district bootstrap replicates
(new computation). Fallback: map the pre-specified `incid_regime` / `ar_regime` strata
(train-only defined → no inference leak) and let the existing forest plot carry the numbers.

---

## 6. External dependency NOT in this bundle

**Country outlines for the Set 1 locator insets.** geopandas 1.1.3 removed its built-in
Natural Earth datasets, and no world/admin-0 layer exists locally. On the second machine,
fetch **Natural Earth 1:110m Admin 0 – Countries**:
`https://naturalearth.s3.amazonaws.com/110m_cultural/ne_110m_admin_0_countries.zip`
(or `pip install naturalearth` / cartopy). Use it only for the grey locator context; the
study geometry comes from this bundle. **No DEM/elevation layer** is bundled — noted for
Set 2 fairness (Colombia's white zones are partly high Andes / sparse Amazon where dengue
structurally does not transmit; if elevation masking is wanted later, source an SRTM/Copernicus DEM).

---

## 7. Provenance & hygiene (do not break on the other machine)
- Raw project data lives under `~/data_quarantine/` (read-only, SHA256-tracked) and is
  **never committed**. `.gitignore` blocks `*.csv/*.gpkg/*.geojson/*.shp/*.zip/data_quarantine/`.
- This pack ships as a single **force-added** zip precisely because of that guard. When you
  regenerate maps, commit **only** the scripts + output PDFs' captions/text — not the data.
- New figures for the paper are PDFs (`Fig*.pdf`), also gitignored; move them into the
  Overleaf/submission bundle as the existing figures are handled.
