# Colombia Boundary / Climate-Linkage Feasibility Report (feasibility only — build NOT run)
*Checks whether OpenDengue Colombia weekly Admin2 units can be reliably matched to municipality polygons and climate grids before building the external-replication arm. **No outbreak labels created; no models fit; no AUC/PR-AUC/calibration/DCA/net-benefit/ΔNB computed; no prediction tables; no external validation.** Only descriptive crosswalk/coverage checks. Downloaded boundary metadata is quarantined and read-only; no data files committed.*

**Date:** 2026-06-14 · **Status:** feasibility only · **Base commit:** 72ea8a8 · **Builds on:** `docs/colombia_external_replication_build_spec.md`.

## A. OpenDengue Colombia municipality metadata (from the quarantined extract, in-memory read)
- Working tier: `adm_0_name=='COLOMBIA' ∧ S_res=='Admin2' ∧ T_res=='Week'` → **199,458 weekly observations**, 2006–2022.
- **Unit count correction (important):** **1,071 distinct (department, municipality) units** — *not* 989. 989 is the number of distinct `adm_2_name` strings, but **62 municipality names recur across departments**, so the unit key **must be department+municipality**. (33 departments, consistent with the verified clean list.)
- **`FAO_GAUL_code` is not a safe join key:** present on 100% of rows but **not unique per municipality** (e.g., GAUL 13337 maps to two different Amazonas corregimientos). Crosswalk therefore uses **name + department**, not GAUL.
- Per-unit metadata (rows, first/last year, years-present) written to quarantine: `colombia_admin2_metadata_v1.csv` (1,071 rows). Median years-present per unit = 14 (unbalanced panel, as documented).
- A handful of units are **corregimientos departamentales `(CD)`** (special non-municipal districts in Amazonas/Vaupés/Guainía) — low observation counts.

## B. Boundary source inspected/downloaded
- **GADM v4.1 Colombia, Admin2 (level-2) GeoJSON** — chosen as the **minimal** source after a HEAD-only size check: GADM level-2 GeoJSON zip **1.13 MB** vs full GeoPackage 64 MB vs shapefile 38 MB. Only the 1.13 MB file was downloaded.
- Contains **1,119 Admin2 polygons**, 33 departments; attribute fields `NAME_1, NAME_2, VARNAME_2, GID_2, CC_2, TYPE_2, …`.
- **`CC_2` is empty (all NA)** in GADM v4.1 Colombia → GADM does **not** provide DIVIPOLA municipality codes here (see H).

## C. Boundary file provenance / size / SHA
- URL: `https://geodata.ucdavis.edu/gadm/gadm4.1/json/gadm41_COL_2.json.zip`
- Quarantine: `~/data_quarantine/colombia_external_replication_feasibility_v1/gadm41_COL_2.json.zip` (read-only, chmod 444)
- Size: **1,133,733 bytes** · inner `gadm41_COL_2.json` 4,224,604 bytes
- **SHA256:** `557aa8699b9b6f3928bc3cfa87371ccc618677304322386ca7d7b9e954a55dc0`

## D. Match strategy
1. **Key = department + municipality** (62 duplicate names force this), accent/case/space-insensitive (`unicodedata` NFKD + nbsp `\xa0` fix).
2. Department-name harmonization OpenDengue→GADM (e.g., `VALLE`→`VALLE DEL CAUCA`, `NORTE SANTANDER`→`NORTE DE SANTANDER`, `GUAJIRA`→`LA GUAJIRA`, `SAN ANDRES`→`SAN ANDRES Y PROVIDENCIA`, `BOGOTA`→`BOGOTA D.C.`).
3. Municipality candidates per polygon = **`NAME_2` ∪ `VARNAME_2`** (split on `|`), plus parenthetical aliases and `… DE X`→`X` reductions (GADM stores long official names: `Santiago de Cali`, `San José de Cúcuta`, `Cartagena de Indias`).
4. Tiers: **exact** (variant-set intersection) → **alias/containment** (short common name contained in long official name) → **fuzzy** (`difflib` ≥0.90).
- Tooling: `geopandas`+`pyogrio`+`shapely` (present); stdlib `unicodedata`/`difflib` for matching (no external fuzzy libs needed). **No geometry/zonal computation performed** — attribute-table matching only.

## E. Exact / alias / unmatched rates
*(Two reported figures: the saved crosswalk artifact uses exact+alias tiers; adding the `difflib` fuzzy tier lifts the match a little further. Both decisively pass the gate.)*
| Tier set | Units matched | Weekly obs matched | Unmatched obs |
|---|---|---|---|
| exact + alias (saved crosswalk) | 1,057 / 1,071 (**98.7%**) | **98.70%** | **1.30%** (14 units) |
| + difflib fuzzy (≥0.90) | 1,061 / 1,071 (**99.1%**) | **99.31%** | **0.69%** (10 units) |
- Exact-tier alone: **1,047 units (97.8%) / 97.9% of obs** — the bulk match cleanly on `NAME_2`/`VARNAME_2`.

## F. >5% unmatched stop-gate
- **PASS.** Unmatched weekly-observation share = **1.30%** (conservative) to **0.69%** (with fuzzy) — both well under the 5% stop-gate.

## G. Unmatched units (characterized — all small or newly-created)
- **10–14 unmatched units**, median ~100–130 weekly obs each; **none are major cities** (CALI, CÚCUTA, CARTAGENA, BUGA, etc. all resolved via `VARNAME_2`/alias).
- Residuals are **newly-created municipalities** (Tuchín, Norosí, Guachené, San José de Uré — all incorporated 2006–2007, post-dating some GADM geometry) and **minor spellings** (Itsmina↔Istmina, Darién↔Calima). All resolvable with a **~14-row manual alias/code table** built train-side.
- List saved (read-only): `colombia_unmatched_units_v1.csv`. Full crosswalk (with `match_type`, `GID_2`): `colombia_crosswalk_v1.csv`.

## H. Climate data availability (assessment only — NO rasters downloaded)
- **ERA5-Land** (Copernicus C3S): hourly, ~9 km (0.1°), **1950–present, global land** → fully covers Colombia and **2006–2022**. Variables: **2 m temperature** (temp), **2 m dewpoint** → derive **relative humidity** (temp + dewpoint), total precipitation.
- **CHIRPS** (UCSB CHC): daily/pentad, 0.05°, **1981–present, 50°S–50°N** → Colombia (≈12°N–4°S) **fully within band**; preferred for tropical **precipitation**.
- **Weekly aggregation:** aggregate daily→ISO week aligned to OpenDengue `calendar_start_date`/`calendar_end_date` (direct alignment — no WER-style offset). **Lags 0–8 weeks feasible** because climate series are continuous (no panel gaps, unlike cases).
- **Aggregation to municipality:** area-weighted zonal statistics over the matched GADM Admin2 polygons (geometry is present in the downloaded file). No zonal computation done in this feasibility step.
- **Verdict:** climate linkage is **feasible**; the only real work is the (separately gated) raster download + zonal aggregation.

## I. Denominator (DANE) feasibility (assessment only — NO download)
- DANE municipal **population projections** (post-2005 census) are publicly available by **DIVIPOLA** code for 2005–2022 → an incidence label is feasible in principle.
- **Caveat (verified here):** GADM v4.1 `CC_2` is **empty**, and `GID_2` is GADM's own ID — **neither carries DIVIPOLA**. So DANE linkage needs an **additional name/DIVIPOLA crosswalk**, not a free code join. **Non-blocking:** the **count-based 75th-pct label remains primary** (denominator-free); the incidence label stays an **optional pre-registered sensitivity**.

## J. Feasibility decision
- **PROCEED to the Colombia external build, after a small manual crosswalk fix.** Boundary matching is essentially solved automatically (99.3% of weekly observations); the residual ≤14 small/new municipalities need a one-time ~14-row alias table. Climate linkage (ERA5-Land + CHIRPS) is feasible for Colombia 2006–2022 with weekly aggregation and lags 0–8. Denominators are optional and non-blocking.
- **Stop-gate:** PASS (unmatched obs 0.69–1.30% ≪ 5%).

## K. Recommended next step (separately gated)
1. Finalize the **~14-row manual alias/DIVIPOLA crosswalk** for the unmatched/new municipalities (train-side, documented).
2. **Gated download** of ERA5-Land + CHIRPS for Colombia 2006–2022 (to quarantine, read-only) and area-weighted zonal aggregation to the matched Admin2 polygons.
3. Then — separately approved — the build per `colombia_external_replication_build_spec.md`. **None of this is run now.**

## L. Quarantined outputs (read-only; NOT committed) + SHA256 (16-char prefix) / size
- `gadm41_COL_2.json.zip` — `557aa8699b9b6f39…` — 1,133,733 B (full SHA in §C)
- `colombia_admin2_metadata_v1.csv` — `9199e1cb70b9f2c4…` — 78,145 B
- `colombia_crosswalk_v1.csv` — `776aa57ccb155286…` — 59,157 B
- `colombia_match_summary_v1.json` — `709ce3b9367f7f58…` — 259 B
- `colombia_unmatched_units_v1.csv` — `a0aad08443b0ada8…` — 257 B
- All under `~/data_quarantine/colombia_external_replication_feasibility_v1/`, chmod 444.

## M. Confirmations
- **Feasibility check only:** no outbreak labels, no models, no AUC/PR-AUC/calibration/DCA/net-benefit/ΔNB, no prediction tables, no external validation.
- **Downloads:** one boundary file (GADM Admin2 GeoJSON, 1.13 MB) + the already-quarantined OpenDengue extract (read in-memory, not re-extracted). **No ERA5/CHIRPS/DANE data downloaded.** All downloaded/derived files quarantined and read-only.
- **No Sri Lanka frozen data or prior outputs read for modeling, modified, or overwritten.**
- **No data files committed** — only this markdown report is proposed for commit (pending your approval).
