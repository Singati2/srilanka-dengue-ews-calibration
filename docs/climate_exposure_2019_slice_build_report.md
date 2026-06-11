# 2019 Climate Exposure Slice Build Report (Geomatics WP2)
*Documents the 2019 build slice performed **locally**. All climate inputs and the exposure CSV stay in git-ignored quarantine and are **NOT committed**. 2019 only. No outcome↔exposure linkage, no models, frozen outcome dataset unchanged, preregistration unchanged.*

**Date:** 2026-06-11

## Scope
First **full-year build slice (2019)** validating the bulk pipeline before extending to 2018 and 2020–2025 (per `climate_bulk_acquisition_and_exposure_table_plan.md` §L).

## Acquisition
- **ERA5-Land** hourly: the full-year single CDS request was **rejected (cost limit "request too large")** → fell back to **12 per-month requests** (the plan's contingency). Result: **12/12 months**, hour counts verified per month (24×ndays, 8760 total), 22 MB, quarantined.
- **CHIRPS** daily v2.0 Final: **365/365 days** downloaded + bbox-clipped, **0 failures**, raw gz 1.3 GB, clipped ~2.9 MB, quarantined.
- No redownloads of existing files; idempotent monthly script.

## Processing
- ERA5: K→°C; **RH via Alduchov–Eskridge Magnus** (computed per cell per hour, pre-average); hourly→ISO-week (t2m mean/min/max, d2m mean, RH mean).
- CHIRPS: **−9999 nodata masked explicitly**; daily→ISO-week (weekly sum, mean-daily).
- RDHS aggregation via **precomputed per-RDHS cell masks** (rasterized once per grid, `all_touched`, NaN-masked) — **no centroid sampling**, and not the slow per-call zonal approach (the first build attempts timed out on 312 rasterstats calls; precomputed masks fixed it).

## Output (quarantined, NOT committed)
- `~/data_quarantine/geomatics/climate_exposure/processed_slices/rdhs_weekly_climate_exposure_2019_slice.csv`
- **SHA256:** `6c1a2724ff72a06fa62409ef4926ab5af3be6ed932ecf3fd2811c79782752e1d` · 1352 rows.
- Columns: `rdhs_name, geometry_id, epi_year, epi_week, week_start, week_end, t2m_mean_c, t2m_min_c, t2m_max_c, d2m_mean_c, rh_mean_percent, precip_sum_mm, precip_mean_daily_mm, n_era5_hours, n_chirps_days, era5_qc_flag, chirps_qc_flag, aggregation_method, source_version, notes`.

## QC results
| Check | Result |
|---|---|
| Rows (26 RDHS × 52 ISO weeks) | **1352** ✅ |
| 26 RDHS present; weeks 1–52 | ✅ |
| Duplicate / missing RDHS-week | 0 / 0 ✅ |
| t2m plausible | mean 20.0–31.2 °C; min 15.2; max 37.5 ✅ |
| d2m plausible | 15.2–25.4 °C ✅ |
| Dewpoint ≤ temperature (all rows) | ✅ |
| RH within 0–100 | 56.0–92.1 % ✅ |
| Precip nonnegative; no empty cells | ✅ |
| ERA5 hour count | 168 (full) / **144 (W01 partial)** ✅ |
| CHIRPS day count | 7 (full) / **6 (W01 partial)** ✅ |
| Kalmunai aggregated | ✅ |
| Null values | 0 ✅ |

## Documented partial week (not imputed)
**ISO 2019-W01** spans 2018-12-31→2019-01-06; the 2019 download covers Jan 1–6 only (144 h / 6 d). All 26 W01 rows are flagged `partial_week_boundary` — **no imputation**; resolved when the 2018 slice supplies 2018-12-31. (Dec 30–31 2019 → ISO-2020-W01, excluded here.)

## Spatial plausibility (annual 2019)
Nuwara Eliya (highlands) coolest & very wet (21.9 °C, 2812 mm); Colombo (west) wettest (3696 mm); Kalmunai (east coast) drier (1657 mm); Anuradhapura (dry zone) driest (1482 mm). The cool-highland / wet-west / dry-east-and-north pattern is the correct monsoon climatology — and temperature/precip are cross-consistent (the pilots showed the same).

## Verdict & next step
The **2019 slice is clean and the bulk pipeline is validated end-to-end** (acquire → unit-convert → RH → epi-week → RDHS aggregation → QC). Ready, on approval, to extend to **2018 and 2020–2025**, then merge, QC, and **freeze** the full 2018–2025 exposure table.
- ERA5-Land bulk must use **per-month requests** (year requests exceed CDS cost limits).
- Boundary weeks (e.g., W01) resolve at multi-year merge.
- **No outcome↔exposure linkage and no modeling until the full exposure table is frozen.**
