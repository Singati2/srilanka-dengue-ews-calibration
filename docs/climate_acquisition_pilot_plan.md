# Climate Acquisition Pilot Plan (Geomatics WP2 prep)
*Planning + tooling/auth check only. **No climate data downloaded.** No bulk download, no outcome↔exposure linkage, no models, frozen outcome dataset unchanged, preregistration unchanged. Any pilot files will stay git-ignored in quarantine.*

**Date:** 2026-06-11

## A. Purpose
Validate the climate-exposure pipeline on **one pilot month** (ERA5-Land + CHIRPS over a Sri Lanka bounding box) before committing to the 2018–2025 bulk download — confirming access, tooling, CRS/units/bounds, and the ability to aggregate to RDHS × epi-week. **No modeling, no linkage** at this stage.

## B. Chosen access route
- **ERA5-Land:** **CDS-local** via the `cdsapi` Python client → NetCDF into quarantine.
- **CHIRPS:** **direct download** of daily GeoTIFFs, **subset to the Sri Lanka bbox** (no API key; public domain). Readable with `rasterio` (already installed).

## C. Required packages
Installed: `rasterio` ✅, `rasterstats` ✅.
**Missing** (needed for the ERA5-Land/NetCDF route): `cdsapi`, `xarray`, `netCDF4`.
**Exact user-local install command (not run yet — needs approval):**
```bash
python3 -m pip install --user cdsapi xarray netCDF4
```
(Optional: `cfgrib` if GRIB is ever used; `exactextract` for fractional-cell weighting. CHIRPS needs none of these.)

## D. CDS credential status
**`~/.cdsapirc`: ABSENT** · `CDSAPI_KEY` env var: not set → **ERA5-Land cannot be downloaded yet.** Setup (user action; **do not paste the token into the repo or GitHub**):
1. Create a free **Copernicus Climate Data Store** account: https://cds.climate.copernicus.eu/
2. On the **ERA5-Land** dataset page, **accept the licence/terms** (required once per dataset).
3. Get your **Personal Access Token** from your CDS profile and create `~/.cdsapirc` per the official guide (https://cds.climate.copernicus.eu/how-to-api):
   ```
   url: https://cds.climate.copernicus.eu/api
   key: <your-personal-access-token>
   ```
4. `chmod 600 ~/.cdsapirc`. **Never commit `~/.cdsapirc`** (the `.gitignore` blocks `credential*`/`token`/`.env`; `~/.cdsapirc` is outside the repo anyway).

## E. ERA5-Land pilot request spec (one month only)
- **Dataset:** `reanalysis-era5-land` (hourly).
- **Variables:** `2m_temperature`, `2m_dewpoint_temperature` (relative humidity derived from T and Td).
- **Period:** pilot month **2019-06** (a representative June dengue-season peak in a clean data year), all days, all 24 hours.
- **Area (N, W, S, E):** **[10.0, 79.5, 5.8, 82.0]** — Sri Lanka bbox with margin.
- **Format:** NetCDF.
- **Output (quarantined):** `~/data_quarantine/geomatics/climate_pilot/era5land/era5land_lka_2019_06.nc`.
- Expected size: small (SL bbox, 2 vars, 1 month hourly ≈ tens of MB).

## F. CHIRPS pilot request spec (one month only)
- **Product:** CHIRPS daily v2.0 Final, global p05 daily GeoTIFFs.
- **Variable:** daily precipitation (mm/day).
- **Period:** **2019-06** (match ERA5-Land pilot month), 30 daily files.
- **Source pattern:** `https://data.chc.ucsb.edu/products/CHIRPS-2.0/global_daily/tifs/p05/2019/chirps-v2.0.2019.06.DD.tif.gz` → gunzip → **clip to SL bbox** [79.5, 5.8, 82.0, 10.0] with `rasterio`.
- **Format:** GeoTIFF (clipped). **Output (quarantined):** `~/data_quarantine/geomatics/climate_pilot/chirps/`.
- Expected size: small after SL clip (MBs).

## G. Pilot QC checks
On the pilot files (before any bulk):
- **CRS:** both EPSG:4326 (matches `rdhs_26_v1.gpkg`).
- **Bounds:** cover the full RDHS extent (no clipping inside Sri Lanka); CHIRPS clip window correct.
- **Time coverage:** ERA5-Land = 24 × 30 = **720 hourly steps**; CHIRPS = **30 daily** files.
- **Missing values:** ERA5-Land `_FillValue`/NaN handled; CHIRPS nodata **−9999** masked.
- **Units:** ERA5-Land temperature/dewpoint in **Kelvin** (convert to °C); CHIRPS precip in **mm/day**. Confirm RH derivation from T & Td is sane (0–100%).
- **Aggregation test:** zonal-aggregate one week to the 26 RDHS polygons (fractional/area-weighted; population-weighting via WorldPop), confirm coarse-grid handling works for small RDHS (e.g., Kalmunai) and produces plausible weekly T/RH/precip.

## H. Stop conditions before bulk download
- **CDS credentials absent or install not approved** → ERA5-Land download blocked (current state). Stop.
- **Pilot QC fails** (wrong CRS/bounds/units, nodata mishandled, or RDHS aggregation implausible) → fix before bulk; do not proceed.
- **Download size unexpectedly large** (e.g., accidental global CHIRPS pull) → stop and reassess (must bbox-subset).
- **ERA5-Land latency** leaves recent 2025 weeks unavailable → note and decide window handling before bulk.

## I. Exact next step
1. **User:** set up CDS account + accept ERA5-Land terms + create `~/.cdsapirc` (Section D).
2. **Approve the install:** `python3 -m pip install --user cdsapi xarray netCDF4`.
3. **Run the one-month pilot** (ERA5-Land 2019-06 + CHIRPS 2019-06) into quarantine; run Section G QC; write a pilot QC report (doc only).
4. **Only after pilot QC passes + explicit approval** → bulk 2018–2025 acquisition, then build & freeze the RDHS × epi-week exposure table. **No modeling until the exposure table is frozen.**

## Note
No climate data was downloaded in this step. Pilot/bulk climate files remain git-ignored in quarantine (`.nc/.tif/.grib/.h5/.zip` blocked); only documentation/templates are committed.
