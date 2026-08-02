# Handoff — ERA5 Tmax/Tmin/Dewpoint extraction → complete the M6/M7 geo hybrid

> **For the incoming session.** This is a self-contained handoff. Everything is on the same
> machine (`/home/mpcrlab`). Repo: `Singati2/srilanka-dengue-ews-calibration`, branch `main`.
> **Current blocker: CDS returns `403 Forbidden` — needs interactive Terms-of-Use re-acceptance
> before the extraction can run (see §3).** Code is drafted, wired, and verified; only the data
> download is blocked.

---

## 1. Objective

Stage three ERA5-Land daily fields for Colombia municipalities — **daily Tmax, daily Tmin,
daily mean dewpoint (d2m)** — and reduce them to weekly per-`GID_2` grids, so we can derive:

- **DTR** = weekly-mean(Tmax − Tmin)  → `derive_dtr`
- **VPD** = es(Tmean) − es(Tdew), Magnus → `derive_vpd`  (uses new dewpoint + existing `temp_C_week`)

These two features complete the **M6/M7 geospatial hybrid**, which is currently an **SPI-only
slice** (precipitation drought index) because Colombia's ERA5 extraction only ever produced
daily-*mean* temperature (no Tmax/Tmin, no dewpoint).

**Where they are used:** DTR and VPD are dynamic *predictors* that enter only two models —
`M6 = cases + geo` and `M7 = M5 + geo`. They do **not** touch M0–M5, and they are **not** the
static F8 explainers (elevation/built-up/wealth), which stay out of the ladder.

---

## 2. Current state (what's done)

**In the repo (`main`, pushed):**
- `scripts/colombia_model_ladder_h4_75pct_M6_v1.py` — M0–M7 ladder. M0–M5 reproduce the frozen
  ladder bit-identically; M6/M7 add the geo block on a shared common-complete∧geo-present mask
  (all 8 models row-fair). Same estimator / Platt recal / GID_2 cluster bootstrap (seed
  20260612, B=1000) as the frozen ladder.
- `scripts/colombia_geo_feature_assembly_v1.py` — builds `colombia_geo_features_v1.csv`.
  `derive_spi` implemented (runnable); **`derive_dtr` / `derive_vpd` implemented but GATED** on
  the files this handoff produces.
- `scripts/colombia_era5_tmaxmin_dewpoint_extract_v1.py` — **the extraction script** (this
  handoff's Step 1). Identical working copy at
  `/home/mpcrlab/data_quarantine/colombia_climate_linkage_full_v1/_build_tmaxmin_dewpoint_full_v1.py`.
- `analysis/m6_geo_pilot/m0_m7_comparison.md` + `_provenance.json` — the current PILOT comparison
  (commit `430e5d6`).

**Current result (SPI-only, PILOT — not quotable):** adding the geo/SPI block does **not** beat
recent surveillance. M6 AUC 0.645 / NB 0.113 (< M1 0.686 / 0.119); M7 0.688 / 0.132 (< M5 0.726
/ 0.136). Verified this is **not a bug** (M0–M5 reproduce frozen exactly; sizes/events/variances
sound) and **not multicollinearity** (each SPI scale fit alone still underperforms M1). It is a
weak, non-generalizing drought signal (train 2007–2017 → test 2020–2022 shift). Honest-null,
consistent with `analysis_plan_v2.md` §10. **DTR/VPD may behave differently — that's why we're
staging them.**

---

## 3. THE BLOCKER — CDS `403 Forbidden` (needs a human on the CDS website)

The extraction was launched and immediately got `403 Forbidden` on every request:
```
[tmax] single-call failed (403 Client Error: Forbidden for url:
  https://cds.climate.copernicus.eu/api/retrieve/v1/processes/der...)
```
Config is correct — `~/.cdsapirc` points at the current endpoint (`https://cds.climate.copernicus.eu/api`),
and the **same key + same dataset** built the mean-temp grid on 2026-06-18. "Worked before, now
403" ⇒ account-side, almost certainly **pending CDS Terms-of-Use re-acceptance** (CDS blanket-403s
until you re-accept) or a **regenerated access token**.

**Fix (interactive, cannot be done from the shell):**
1. Log in at https://cds.climate.copernicus.eu and accept any pending **Terms of Use** banner.
2. Dataset page **"ERA5-Land post-processed daily statistics"** → **Terms of use** → **Accept**.
3. **Your profile → Personal Access Token** must match the `key:` line in `~/.cdsapirc`
   (regenerate + update the file if not).

**Verify the fix (fast, one call):**
```bash
python3 -c "import cdsapi; cdsapi.Client().retrieve('derived-era5-land-daily-statistics', {'variable':['2m_temperature'],'year':'2022','month':'01','day':'01','daily_statistic':'daily_maximum','time_zone':'utc+00:00','frequency':'1_hourly','area':[13.6,-82,-4.4,-66.6]}, '/tmp/cds_test.nc')"
```
Returns a file → fixed. Still 403 → Terms/token still not right.

---

## 4. Pipeline to execute (once auth is fixed)

```
STEP 1  Extract (LONG — CDS queue + download; temp mean-build logged ~60 h, ×3 fields. Run detached.)
  cd /home/mpcrlab/data_quarantine/colombia_climate_linkage_full_v1
  nohup python3 -u colombia_era5_tmaxmin_dewpoint_extract_v1.py \
      > _build_tmaxmin_dewpoint_run.log 2>&1 &      # or run the repo copy from scripts/
  #   --only tmax|tmin|d2m  to fetch one field at a time (resume-friendly)
  # RECOMMEND first: add/run a single-year smoke before the full multi-day pull (see §7).
     → writes, row-aligned to colombia_weekly_era5_temperature_gid2_v1.csv:
        colombia_weekly_era5_tmax_tmin_gid2_v1.csv   [GID_2,week_start,week_end,tmax_C_week,tmin_C_week,days_used]
        colombia_weekly_era5_dewpoint_gid2_v1.csv    [GID_2,week_start,week_end,d2m_C_week,days_used]
     (the script self-checks 1:1 row-alignment against the temp grid and logs matched/unmatched)

STEP 2  Turn on the derivations — edit scripts/colombia_geo_feature_assembly_v1.py:
  DERIVERS = [('spi', derive_spi), ('dtr', derive_dtr), ('vpd', derive_vpd)]   # uncomment DTR/VPD

STEP 3  Rebuild the geo block
  python3 scripts/colombia_geo_feature_assembly_v1.py
     → colombia_geo_features_v1.csv now carries SPI + DTR + VPD (completeness-checked on cc rows)

STEP 4  Re-run the ladder (NO code change)
  python3 scripts/colombia_model_ladder_h4_75pct_M6_v1.py
     → M6 = cases + {SPI,DTR,VPD};  M7 = M5 + {SPI,DTR,VPD}  ← full geo hybrid
     → shared mask re-intersects; M0–M7 stay row-fair automatically

STEP 5  Regenerate + push the comparison (same as analysis/m6_geo_pilot/, keep the PILOT label)
```

Steps 2–5 need **zero new code** — the derivations and harness already consume those exact file
paths (`ERA5_TMAXMIN`, `ERA5_D2M` in the assembly script). Only Step 1 is new work.

---

## 5. Feature → model map (what consumes the new data)

| ERA5 field (new) | Combines with | Derived feature | Columns | Used in |
|---|---|---|---|---|
| Tmax + Tmin | each other | **DTR** = wk-mean(Tmax−Tmin) | `dtr_lag0..8` | geo block → M6, M7 |
| Dewpoint (d2m) | existing `temp_C_week` | **VPD** (Magnus) | `vpd_lag0..8` | geo block → M6, M7 |

CDS request (per field, in the script): dataset `derived-era5-land-daily-statistics`,
`daily_statistic` ∈ {`daily_maximum`,`daily_minimum`,`daily_mean`}, `frequency:1_hourly`,
`time_zone:utc+00:00`, `area:[13.6,-82.0,-4.4,-66.6]`, Kelvin→°C. Method mirrors
`_build_temp_full2.py` exactly (1065 GADM polygons, `all_touched` rasterize, daily areal mean →
weekly mean).

---

## 6. Key paths (all quarantine dirs are git-ignored — data stays local)

| What | Path |
|---|---|
| Modeling table (M0–M5 features + labels) | `data_quarantine/colombia_label_features_v1/colombia_modeling_table_h4_75pct_v1.csv` |
| Geo features (currently SPI only) | `data_quarantine/colombia_label_features_v1/colombia_geo_features_v1.csv` |
| Precip + mean-temp grid | `data_quarantine/colombia_climate_linkage_full_v1/colombia_weekly_climate_precip_temp_gid2_v1.csv` |
| Existing mean-temp grid (row-align ref) | `data_quarantine/colombia_climate_linkage_full_v1/colombia_weekly_era5_temperature_gid2_v1.csv` |
| **NEW Tmax/Tmin grid (to create)** | `data_quarantine/colombia_climate_linkage_full_v1/colombia_weekly_era5_tmax_tmin_gid2_v1.csv` |
| **NEW dewpoint grid (to create)** | `data_quarantine/colombia_climate_linkage_full_v1/colombia_weekly_era5_dewpoint_gid2_v1.csv` |
| GADM boundaries | `data_quarantine/colombia_external_replication_feasibility_v1/gadm41_COL_2.json.zip` |
| OpenDengue weeks (for weekly index) | `data_quarantine/opendengue_extract_inspection_v1/Temporal_extract_V1_3.zip` |
| Ladder outputs | `data_quarantine/colombia_model_pilots/model_ladder_h4_75pct_M6_v1/` |

---

## 7. Prerequisites & guardrails

- **Verified present:** `cdsapi`, `xarray`, `geopandas`, `rasterio`, `netCDF4` all import;
  `~/.cdsapirc` exists (new endpoint); GADM + OpenDengue inputs present. Only the CDS **auth**
  is blocked (§3).
- **Recommended before the full pull:** add a single-year smoke to the extractor (e.g. a
  `--test-year 2022` that limits `years=[2022]` and writes `*_SMOKE.csv`) so plumbing is
  validated in minutes, not days. Not yet implemented.
- **Fairness contract (do not break):** M6/M7 must score the *same rows* as M0–M5. DTR/VPD must
  be complete on the `common_complete_M1_to_M5_h4` rows; the harness intersects into the shared
  mask and re-runs all models on it. If a field is short on early rows it is logged and
  intersected (as SPI-26 was, 0.82%).
- **No leakage:** features are past-only lags; any learned stat (e.g. SPI climatology) is fit on
  TRAIN rows only.
- **Governance (PILOT):** these runs are quarantine-only method development. `analysis_plan_v2.md`
  Part I is **not frozen**. Do not quote in the manuscript until: freeze Part I (repo tag
  `plan_v2_frozen` + OSF), then run the confirmatory version. Do not let pilot results reshape
  the preregistered feature pool (§10 no-fishing rule).

---

## 8. TL;DR for the incoming session

1. Get CDS auth working (§3) — human step on the website.
2. (Recommended) validate with a one-year smoke, then run `colombia_era5_tmaxmin_dewpoint_extract_v1.py` detached.
3. Uncomment DTR/VPD in `DERIVERS`, rebuild geo block, re-run the ladder — no other code changes.
4. Regenerate `analysis/m6_geo_pilot/` comparison; keep the PILOT label; push.
5. Then hand back for the freeze/preregistration decision.
