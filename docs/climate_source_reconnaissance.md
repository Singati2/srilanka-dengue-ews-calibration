# Climate-Source Reconnaissance — Exposure Pipeline (Geomatics WP2 prep)
*Reconnaissance only — web metadata inspection; **no climate data downloaded**. No ERA5/CHIRPS processing, no outcome↔exposure linkage, no models, frozen outcome dataset unchanged, preregistration unchanged (this is a documentation note).*

**Date:** 2026-06-11
**Goal:** identify the climate sources, access route, tooling, and download footprint for building the RDHS × epi-week exposure table (per `preregistration_analysis_plan_v1.md` §H).
**Companion inventory:** `geomatics_templates/climate_source_inventory_template.csv`

## Primary candidates
### ERA5-Land (temperature + humidity)
- **Source:** ECMWF / Copernicus Climate Data Store. https://cds.climate.copernicus.eu/datasets/reanalysis-era5-land
- **Variables:** **2m temperature**, **2m dewpoint temperature** (→ relative humidity); precipitation also available. ~50 land variables.
- **Temporal:** hourly (1950–present) → aggregate to daily → weekly. Covers **2018–2025** (reanalysis; recent weeks have ~2–3-month latency).
- **Spatial:** **0.1° (~9 km)**, lapse-rate-corrected for altitude.
- **Format:** NetCDF / GRIB. **License:** Copernicus Licence (free, open, attribution).
- **Access:** `cdsapi` Python client (free CDS account + API **token** required) for local NetCDF; OR Google Earth Engine (`ECMWF/ERA5_LAND/HOURLY`, server-side, GEE auth).
- **Size:** Sri Lanka bbox (~5.5–10°N, 79–82°E ≈ a small grid) hourly, 2 variables, 8 years ≈ **low-single-digit GB** (far smaller if daily-aggregated at source or via GEE).
- **Weekly RDHS aggregation feasible?** **Yes** — gridded, EPSG:4326; reproject/align to RDHS polygons and zonal-aggregate.

### CHIRPS (precipitation)
- **Source:** UCSB Climate Hazards Center. https://www.chc.ucsb.edu/data/chirps
- **Variable:** precipitation. **Temporal:** **daily** (also pentad/monthly), 1981–near-present, covers 2018–2025. **Spatial:** **0.05° (~5.5 km)**.
- **Format:** GeoTIFF / NetCDF. **License:** **public domain** (no API key).
- **Access:** direct download (chc.ucsb.edu), Google Earth Engine (`UCSB-CHG/CHIRPS/DAILY`), or NOAA ERDDAP.
- **Size:** Sri Lanka bbox subset is **small (MBs)**; the **global** daily archive is large (~tens of GB) → **must subset to the SL bbox or use GEE**.
- **Weekly RDHS aggregation feasible?** **Yes** — gridded, finer than ERA5-Land; same zonal-aggregation approach.

## Optional / sensitivity sources (not primary)
- **ERA5 (0.25°)** — coarser sibling of ERA5-Land; **sensitivity** for temperature/humidity only.
- **GPM IMERG (0.1°)** — independent satellite precipitation; **validation/sensitivity** vs CHIRPS (needs Earthdata login).
- **MODIS LST MOD11 (1 km, 8-day)** — land-surface temperature cross-check; note LST ≠ air temperature; **sensitivity**.
- **MODIS NDVI MOD13 (250 m–1 km, 16-day)** — larval-habitat **covariate** for the spatial decision-support (not a climate forcing).
- **TerraClimate (monthly, ~4 km)** — VPD/PET water-balance variables; **monthly only → reject for the weekly primary** (sensitivity at most).

## Strict recommendation
- **A. Primary temperature/humidity source:** **ERA5-Land** (2m temperature + 2m dewpoint → RH), 0.1°, hourly→weekly. Matches the EWS literature and the prereg.
- **B. Primary precipitation source:** **CHIRPS daily v2.0 Final**, 0.05°, public domain.
- **C. Is ERA5-Land + CHIRPS sufficient?** **Yes** — together they cover temperature, humidity, and precipitation at the resolution/coverage the DLNM/mechanistic models need; both are standard, open, EWS-designed inputs. The optional sources are for sensitivity/validation only.
- **D. Population-weighted aggregation feasible?** **Yes** — both are gridded in EPSG:4326 (the RDHS geometry CRS); WorldPop (already in quarantine) provides the weights. **Caveat:** ERA5-Land 0.1° (~9 km) cells are coarse relative to the smallest RDHS (e.g., Sainthamaruthu/Kalmunai); use **fractional-cell (area- and population-weighted) aggregation** (exactextract-style) — not centroid sampling — to avoid coarse-grid bias. Retain a naive area-weighted version for the MAUP sensitivity.
- **E. New packages / API keys needed?**
  - **ERA5-Land via CDS:** a **free CDS account + API token** (user action) and an **install** — `cdsapi` + a NetCDF/GRIB reader (`xarray` + `netCDF4` or `cfgrib`). Alternatively, the **Google Earth Engine** route needs a GEE account/auth instead.
  - **CHIRPS:** **no key**; GeoTIFFs read with `rasterio` (already installed).
  - **Zonal aggregation:** `rasterio` + `rasterstats` already installed; `exactextract` optional for fractional weighting.
  - → An install + a CDS key are required **only** for the ERA5-Land local route. **Not installed yet — requires approval.**
- **F. Is download size manageable?** **Yes, if subset to the Sri Lanka bounding box** (small country): ERA5-Land SL ≈ low-GB, CHIRPS SL ≈ MBs. The risk is accidentally pulling **global** CHIRPS daily (tens of GB) — avoided by bbox-subsetting or GEE.
- **G. Exact next step before any download:**
  1. **Choose the access route:** (i) **CDS API local** (NetCDF; needs CDS key + `cdsapi`/`xarray` install — ASK) or (ii) **Google Earth Engine** (server-side zonal stats; needs GEE auth). Recommendation: **CDS-local for ERA5-Land + direct bbox CHIRPS GeoTIFFs**, keeping everything reproducible in quarantine.
  2. **Obtain the CDS API token** (user action) if route (i).
  3. **Approve the install** (`cdsapi xarray netCDF4` [+ optional `cfgrib`/`exactextract`]).
  4. **Freeze the request spec** in a doc: SL bounding box, variable list (2m T, 2m Td; CHIRPS precip), period 2018–2025, hourly→daily→weekly aggregation, RH derivation, and the **DLNM lag windows** — before any bulk pull.
  5. **Pilot download** (1 month / 1 year) to validate the pipeline, then bulk. **No modeling until the exposure table is built, QC'd, and frozen** (per prereg §H/§Q).

## Note
No climate data was downloaded. Any future climate download stays under git-ignored quarantine (`.nc/.tif/.grib/.h5/.zip` blocked); only documentation/templates are committed.
