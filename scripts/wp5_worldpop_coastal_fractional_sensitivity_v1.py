"""WP5 §17 — WorldPop centre-in-polygon vs fractional/boundary-aware assignment.

instruction_m6.md §17 makes this mandatory: the centre-in-polygon rule drops population near
coastlines, and within-unit normalisation must NOT be assumed to make that harmless. For each
unit and exposure it asks for  Delta X_i = X_fractional_i - X_centre_i,  with median and maximum
absolute difference, relative difference, rank correlation, the most affected RDHS units, and
whether downstream results change.

Method
------
centre-in-polygon : a 100 m pixel is assigned WHOLE to the district containing its centre.
                    (rasterio rasterize, all_touched=False — what notebook 03 and wp5_00 do.)
fractional        : a pixel contributes value * coverage_fraction to each district it overlaps.
                    Coverage fraction is computed by rasterizing each district at OVERSAMPLE x
                    the native grid inside the district's own window and block-averaging, which
                    is exact to 1/OVERSAMPLE^2 of a pixel. Assumes uniform density within a
                    100 m pixel — the standard assumption, and what "boundary-aware" means here.

Population is a COUNT per pixel, so fractional assignment splits the count by area overlap.

Outputs (quarantined): data_quarantine/wp5_exposure/wp5_worldpop_fractional_sensitivity_*.csv
"""
import json
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
import rasterio
from rasterio.features import rasterize
from rasterio.windows import Window, from_bounds
from scipy.stats import spearmanr

REPO = Path("/Users/mpcr/aj/Dengue/srilanka-dengue-ews-calibration")
QUAR = REPO / "data_quarantine"
OUT = QUAR / "wp5_exposure"
GEOM = Path("/Users/mpcr/aj/Dengue/dengue_map_workpack/geometry/rdhs_26_v1.gpkg")

OVERSAMPLE = 8  # 12.5 m subpixels; exact to 1/64 of a 100 m pixel
RASTERS = {
    "ppp_2020_UNadj": QUAR / "m6_geomatics" / "worldpop" / "lka_ppp_2020_UNadj.tif",
    "R2025A_2020_CN": QUAR / "population_r2025a" / "lka_pop_2020_CN_100m_R2025A_v1.tif",
}


def coverage_fraction(geom, src, window, transform):
    """Exact-to-1/OVERSAMPLE^2 fraction of each native pixel covered by geom."""
    h, w = int(window.height), int(window.width)
    fine = rasterize(
        [(geom, 1)],
        out_shape=(h * OVERSAMPLE, w * OVERSAMPLE),
        transform=transform * rasterio.Affine.scale(1 / OVERSAMPLE, 1 / OVERSAMPLE),
        fill=0, dtype="uint8", all_touched=False,
    )
    return fine.reshape(h, OVERSAMPLE, w, OVERSAMPLE).mean(axis=(1, 3))


def centre_mask(geom, window, transform):
    """all_touched=False rasterize == pixel-centre-in-polygon."""
    h, w = int(window.height), int(window.width)
    return rasterize([(geom, 1)], out_shape=(h, w), transform=transform,
                     fill=0, dtype="uint8", all_touched=False).astype(bool)


def run_raster(name, path, units):
    with rasterio.open(path) as src:
        nodata = src.nodata
        national = 0.0
        for _, win in src.block_windows(1):
            b = src.read(1, window=win)
            national += float(b[b != nodata].sum())

        rows = []
        for _, u in units.iterrows():
            geom = u.geometry
            w0 = from_bounds(*geom.bounds, transform=src.transform).round_offsets().round_lengths()
            # pad one pixel so boundary pixels are fully represented, then clamp to the
            # raster: read() clips silently at the edge, which would desync the masks.
            c0 = max(int(w0.col_off) - 1, 0)
            r0 = max(int(w0.row_off) - 1, 0)
            c1 = min(int(w0.col_off) + int(w0.width) + 1, src.width)
            r1 = min(int(w0.row_off) + int(w0.height) + 1, src.height)
            win = Window(c0, r0, c1 - c0, r1 - r0)
            arr = src.read(1, window=win).astype("float64")
            arr[arr == nodata] = 0.0
            tr = src.window_transform(win)

            frac = coverage_fraction(geom, src, win, tr)
            cen = centre_mask(geom, win, tr)

            rows.append({
                "geometry_id": u.geometry_id,
                "rdhs_name": u.rdhs_name,
                "pop_centre": float(arr[cen].sum()),
                "pop_fractional": float((arr * frac).sum()),
                "boundary_pixels": int(((frac > 0) & (frac < 1)).sum()),
            })
    d = pd.DataFrame(rows)
    d["delta"] = d.pop_fractional - d.pop_centre
    d["rel_delta_pct"] = 100 * d.delta / d.pop_centre
    d["raster"] = name
    return d, national


def main():
    units = gpd.read_file(GEOM).to_crs("EPSG:4326").sort_values("geometry_id").reset_index(drop=True)
    assert len(units) == 26

    summary, frames = {}, []
    for name, path in RASTERS.items():
        d, national = run_raster(name, path, units)
        frames.append(d)
        rho = spearmanr(d.pop_centre, d.pop_fractional).statistic
        worst = d.reindex(d.rel_delta_pct.abs().sort_values(ascending=False).index)
        summary[name] = {
            "national_raster_total": national,
            "captured_centre": float(d.pop_centre.sum()),
            "captured_fractional": float(d.pop_fractional.sum()),
            "capture_frac_centre": float(d.pop_centre.sum() / national),
            "capture_frac_fractional": float(d.pop_fractional.sum() / national),
            "national_shortfall_centre_pct": float(100 * (1 - d.pop_centre.sum() / national)),
            "national_shortfall_fractional_pct": float(100 * (1 - d.pop_fractional.sum() / national)),
            "median_abs_delta": float(d.delta.abs().median()),
            "max_abs_delta": float(d.delta.abs().max()),
            "max_abs_delta_unit": worst.iloc[0].rdhs_name,
            "median_abs_rel_delta_pct": float(d.rel_delta_pct.abs().median()),
            "max_abs_rel_delta_pct": float(d.rel_delta_pct.abs().max()),
            "spearman_rank_corr": float(rho),
            "rank_changes": int((d.pop_centre.rank() != d.pop_fractional.rank()).sum()),
            "most_affected": worst.head(5)[["rdhs_name", "delta", "rel_delta_pct"]].to_dict("records"),
        }
        print(f"\n=== {name} ===")
        print(f"national raster total      {national:,.0f}")
        print(f"captured, centre-in-poly   {d.pop_centre.sum():,.0f}  "
              f"({100 * d.pop_centre.sum() / national:.2f}%  shortfall "
              f"{100 * (1 - d.pop_centre.sum() / national):.2f}%)")
        print(f"captured, fractional       {d.pop_fractional.sum():,.0f}  "
              f"({100 * d.pop_fractional.sum() / national:.2f}%  shortfall "
              f"{100 * (1 - d.pop_fractional.sum() / national):.2f}%)")
        print(f"per-unit |delta|: median {d.delta.abs().median():,.0f}  max {d.delta.abs().max():,.0f}"
              f"  ({worst.iloc[0].rdhs_name})")
        print(f"per-unit |rel|:   median {d.rel_delta_pct.abs().median():.3f}%  "
              f"max {d.rel_delta_pct.abs().max():.3f}%")
        print(f"Spearman rank corr {rho:.6f}   rank changes {int((d.pop_centre.rank() != d.pop_fractional.rank()).sum())}")
        print(worst.head(5)[["rdhs_name", "pop_centre", "pop_fractional", "delta", "rel_delta_pct"]].to_string(index=False))

    OUT.mkdir(parents=True, exist_ok=True)
    pd.concat(frames).to_csv(OUT / "wp5_worldpop_fractional_sensitivity_srilanka_v1.csv", index=False)
    (OUT / "wp5_worldpop_fractional_sensitivity_provenance.json").write_text(
        json.dumps({"oversample": OVERSAMPLE, "geometry": str(GEOM.name),
                    "rasters": {k: str(v.name) for k, v in RASTERS.items()},
                    "summary": summary}, indent=2))
    print(f"\nwrote {OUT / 'wp5_worldpop_fractional_sensitivity_srilanka_v1.csv'}")


if __name__ == "__main__":
    main()
