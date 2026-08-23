"""WP5 §17, part 2 — where the missing coastal population is, and whether it moves exposure.

Part 1 (wp5_worldpop_coastal_fractional_sensitivity_v1.py) showed that fractional/boundary-aware
weighting is nearly identical to centre-in-polygon AND does not recover the national shortfall.
This script establishes why, and measures the consequence:

  1. locate the population that falls outside every RDHS polygon;
  2. reassign it to the nearest district (a coastline-mismatch remedy, not an area-weighting one);
  3. propagate to exposure via the population-weighted mean elevation and the standard lapse
     rate — the same proxy wp5_00 used to estimate Build B's displacement, so the two numbers
     are directly comparable.

Outputs (quarantined): data_quarantine/wp5_exposure/wp5_worldpop_coastal_snap_*.csv
"""
import glob
import json
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
import rasterio
from rasterio.features import rasterize
from rasterio.merge import merge
from rasterio.warp import Resampling, reproject
from shapely.geometry import Point

REPO = Path("/Users/mpcr/aj/Dengue/srilanka-dengue-ews-calibration")
QUAR = REPO / "data_quarantine"
OUT = QUAR / "wp5_exposure"
GEOM = Path("/Users/mpcr/aj/Dengue/dengue_map_workpack/geometry/rdhs_26_v1.gpkg")
POP = QUAR / "m6_geomatics" / "worldpop" / "lka_ppp_2020_UNadj.tif"
DEM_GLOB = str(QUAR / "m6_geomatics" / "dem" / "*.tif")
EQUAL_AREA = ("+proj=laea +lat_0=7.6221 +lon_0=80.6987 +x_0=0 +y_0=0 "
              "+datum=WGS84 +units=m +no_defs")
LAPSE_C_PER_M = 6.5e-3


def main():
    units = (gpd.read_file(GEOM).to_crs("EPSG:4326")
             .sort_values("geometry_id").reset_index(drop=True))

    with rasterio.open(POP) as src:
        pop = src.read(1).astype("float64")
        pop[pop == src.nodata] = 0.0
        shape, transform, crs = src.shape, src.transform, src.crs

    # district id per pixel by centre-in-polygon (0 = outside every district)
    owner = rasterize([(g, i + 1) for i, g in enumerate(units.geometry)],
                      out_shape=shape, transform=transform, fill=0,
                      dtype="int32", all_touched=False)

    # DEM mosaic resampled onto the population grid
    dem_src = [rasterio.open(p) for p in sorted(glob.glob(DEM_GLOB))]
    mosaic, mos_tr = merge(dem_src)
    dem = np.full(shape, np.nan, dtype="float32")
    reproject(mosaic[0], dem, src_transform=mos_tr, src_crs=dem_src[0].crs,
              dst_transform=transform, dst_crs=crs, resampling=Resampling.bilinear)

    # ---- 1. the population outside every district -----------------------------
    rr, cc = np.where((owner == 0) & (pop > 0))
    xs, ys = rasterio.transform.xy(transform, rr, cc)
    orphan = gpd.GeoDataFrame(
        {"pop": pop[rr, cc], "elev": dem[rr, cc]},
        geometry=[Point(x, y) for x, y in zip(xs, ys)], crs="EPSG:4326")
    national = float(pop.sum())
    print(f"national            {national:,.0f}")
    print(f"outside all 26 RDHS {orphan['pop'].sum():,.0f} "
          f"({100 * orphan['pop'].sum() / national:.2f}%) in {len(orphan):,} pixels")

    # ---- 2. snap to nearest district ------------------------------------------
    snapped = gpd.sjoin_nearest(orphan.to_crs(EQUAL_AREA),
                                units[["geometry_id", "geometry"]].to_crs(EQUAL_AREA),
                                how="left", distance_col="dist_m")
    print(f"snap distance: median {snapped.dist_m.median():.0f} m  max {snapped.dist_m.max():.0f} m")

    rows = []
    for i, r in units.iterrows():
        sel = owner == i + 1
        p, e = pop[sel], dem[sel]
        ok = np.isfinite(e)
        base_pop, base_elev = p[ok].sum(), np.average(e[ok], weights=p[ok])
        add = snapped[(snapped.geometry_id == r.geometry_id) & np.isfinite(snapped.elev)]
        tot = base_pop + add["pop"].sum()
        elev_snap = (base_elev * base_pop + (add.elev * add["pop"]).sum()) / tot
        rows.append({
            "geometry_id": r.geometry_id, "rdhs_name": r.rdhs_name,
            "pop_centre": base_pop, "pop_snapped": tot,
            "pop_added": add["pop"].sum(),
            "pop_added_pct": 100 * add["pop"].sum() / base_pop,
            "elev_centre_m": base_elev, "elev_snapped_m": elev_snap,
            "d_elev_m": elev_snap - base_elev,
            "dT_C": -LAPSE_C_PER_M * (elev_snap - base_elev),
        })
    d = pd.DataFrame(rows)

    print(f"\nnational capture after snap: {100 * d.pop_snapped.sum() / national:.4f}%")
    print("\nmost affected DENOMINATORS:")
    print(d.nlargest(5, "pop_added_pct")[
        ["rdhs_name", "pop_centre", "pop_added", "pop_added_pct"]].to_string(index=False))
    print(f"\npopulation added, per unit: median {d.pop_added_pct.median():.3f}%  "
          f"max {d.pop_added_pct.max():.3f}%")
    print("\nmost affected EXPOSURE (lapse-rate proxy):")
    print(d.reindex(d.dT_C.abs().nlargest(5).index)[
        ["rdhs_name", "d_elev_m", "dT_C"]].to_string(index=False))
    print(f"\n|dT|: median {d.dT_C.abs().median():.4f} C  max {d.dT_C.abs().max():.4f} C")
    print(f"for scale, Build B's population-weighting displacement is -1.75 to +0.83 C")

    OUT.mkdir(parents=True, exist_ok=True)
    d.to_csv(OUT / "wp5_worldpop_coastal_snap_srilanka_v1.csv", index=False)
    (OUT / "wp5_worldpop_coastal_snap_provenance.json").write_text(json.dumps({
        "population_raster": POP.name, "geometry": GEOM.name,
        "lapse_rate_C_per_m": LAPSE_C_PER_M,
        "national_total": national,
        "orphan_pop": float(orphan["pop"].sum()),
        "orphan_pct": float(100 * orphan["pop"].sum() / national),
        "orphan_pixels": int(len(orphan)),
        "snap_dist_m_median": float(snapped.dist_m.median()),
        "snap_dist_m_max": float(snapped.dist_m.max()),
        "capture_after_snap_pct": float(100 * d.pop_snapped.sum() / national),
        "max_pop_added_pct": float(d.pop_added_pct.max()),
        "max_abs_dT_C": float(d.dT_C.abs().max()),
    }, indent=2))
    print(f"\nwrote {OUT / 'wp5_worldpop_coastal_snap_srilanka_v1.csv'}")


if __name__ == "__main__":
    main()
