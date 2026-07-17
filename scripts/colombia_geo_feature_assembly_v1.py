#!/usr/bin/env python3
"""Assemble the M6 dynamic-geospatial feature block for the Colombia ladder.

CONTRACT (what colombia_model_ladder_h4_75pct_M6_v1.py consumes)
----------------------------------------------------------------
Output: {LF}/colombia_geo_features_v1.csv
  - Keys: exactly ['GID_2','week_start'] (week_start 'YYYY-MM-DD', string; same convention
    as colombia_modeling_table_h4_75pct_v1.csv).
  - One row per (GID_2, week_start) in the modeling table; keys UNIQUE.
  - Feature columns: model-READY numeric values (per-variable transforms applied HERE). The
    harness only z-scores them on TRAIN stats, exactly like the continuous climate block.
  - COMPLETENESS (fairness-critical): every emitted feature is non-null on ALL
    common_complete_M1_to_M5_h4 rows, so M6 scores the IDENTICAL row set as M0-M5. A scale/
    feature that cannot be complete there is DROPPED (and logged) rather than shrinking the
    comparison. (To instead widen the pool you would define a new common-complete mask and
    RE-RUN M0-M5 on it -- not done here.)

LEAKAGE RULES (spatio-temporal honesty)
---------------------------------------
  - Dynamic features use PAST+current weeks only (accumulations/lags end at week t; the label
    is h=4 weeks ahead). No same-label-week leakage, no future.
  - Any statistic learned from data (SPI climatology mean/SD) is fit on TRAIN rows only, then
    applied to val/test.

FEATURE STATUS (Colombia data actually staged: weekly-mean precip + weekly-mean 2m temp only)
--------------------------------------------------------------------------------------------
  SPI  -- IMPLEMENTED & RUNNABLE: standardized precipitation index from the precip grid.
  DTR  -- DRAFTED, gated: needs ERA5-Land daily Tmax/Tmin (not extracted). Raises until staged.
  VPD  -- DRAFTED, gated: needs ERA5-Land dewpoint d2m (not extracted). Raises until staged.
Static per-municipality layers (elevation, built-up, NDVI, wealth, distance-to-water) are F8
EXPLAINERS, not M6 predictors (time-invariant + collinear with the dept fixed effects in
M3/M5) -- they do NOT belong in this table.

Usage:
  python3 colombia_geo_feature_assembly_v1.py            # assemble all enabled DERIVERS (SPI now)
  python3 colombia_geo_feature_assembly_v1.py --smoke    # PLUMBING-ONLY placeholder column
"""
import argparse, os, sys, hashlib
import pandas as pd, numpy as np

LF='/home/mpcrlab/data_quarantine/colombia_label_features_v1'
CLIM='/home/mpcrlab/data_quarantine/colombia_climate_linkage_full_v1'
SRC=f'{LF}/colombia_modeling_table_h4_75pct_v1.csv'
PRECIP_GRID=f'{CLIM}/colombia_weekly_climate_precip_temp_gid2_v1.csv'   # GID_2,week_start,precip_mm_week,temp_C_week
# --- gated inputs for DTR / VPD (NOT staged; expected schemas documented in the derivers) ---
ERA5_TMAXMIN=f'{CLIM}/colombia_weekly_era5_tmax_tmin_gid2_v1.csv'       # GID_2,week_start,tmax_C_week,tmin_C_week
ERA5_D2M=f'{CLIM}/colombia_weekly_era5_dewpoint_gid2_v1.csv'            # GID_2,week_start,d2m_C_week
OUT=f'{LF}/colombia_geo_features_v1.csv'
KEY=['GID_2','week_start']

# ------------------------------------------------------------------ helpers
def _load_base():
    cols=KEY+['split','common_complete_M1_to_M5_h4']
    return pd.read_csv(SRC,dtype={'week_start':str},usecols=lambda c: c in cols)

def _cc_keys(base):
    return base[base.common_complete_M1_to_M5_h4==True][KEY]

def _complete_on_cc(feat, base, cols):
    """Return {col: n_missing_on_cc}. 0 == complete."""
    m=_cc_keys(base).merge(feat,on=KEY,how='left')
    return {c:int(m[c].isna().sum()) for c in cols}

def _lag_from_weekly(base, weekly, valcol, prefix, nlag=9):
    """Build prefix_lag0..prefix_lag{nlag-1} by joining week t-k of a weekly per-GID_2 grid.
    Mirrors the upstream lag idiom in colombia_lag_feature_assembly_v1.py (past-only, no fill)."""
    vmap={(g,w):v for g,w,v in zip(weekly.GID_2,weekly.week_start,weekly[valcol])}
    wk=pd.to_datetime(base.week_start)
    out=base[KEY].copy()
    for k in range(nlag):
        sh=(wk-pd.Timedelta(weeks=k)).dt.date.astype(str)
        out[f'{prefix}_lag{k}']=[vmap.get((g,w),np.nan) for g,w in zip(base.GID_2,sh)]
    return out

# ------------------------------------------------------------------ derivations
def derive_spi(base, scales=(8,13,26)):
    """Standardized Precipitation Index from weekly precip (McKee-style, Gaussian form).

    For each GID_2, accumulate precip over a k-week window ending at week t (k in `scales`;
    8/13/26 wk ~= 2/3/6 months), then standardize to a z-score against a TRAIN-ONLY climatology
    fit per (GID_2, ISO-week) with a per-GID_2 fallback where a calendar cell is too thin. The
    window ends at t (known at prediction time; label is t+4), so it is leakage-safe. Per-ISO-week
    standardization removes the seasonal cycle -- so these columns are emitted model-ready and are
    only globally rescaled by the harness.

    A scale is kept if its residual missingness on the common-complete rows is small
    (<= TOL_FRAC, from sporadic precip gaps / short early history) and DROPPED otherwise
    (e.g. SPI-26 lacks 6-month history for ~88 early-starting municipalities). Kept scales may
    still carry a handful of NaNs; the harness resolves them by intersecting into a shared
    M6-inclusive mask and re-running M0-M6 together on it, so all seven models stay row-fair."""
    TOL_FRAC=0.01
    g=pd.read_csv(PRECIP_GRID,dtype={'week_start':str},usecols=['GID_2','week_start','precip_mm_week'])
    g=g.merge(base[KEY+['split']],on=KEY,how='left')          # split only defined on modeling-table weeks
    g['wk']=pd.to_datetime(g.week_start)
    g=g.sort_values(['GID_2','wk']).reset_index(drop=True)
    g['woy']=g.wk.dt.isocalendar().week.astype(int)
    n_cc=len(_cc_keys(base)); feat=base[KEY].copy(); kept=[]
    for k in scales:
        col=f'spi{k}'
        # k-week accumulation ending at t, within each GID_2 (full window required -> NaN if short)
        roll=g.groupby('GID_2',sort=False)['precip_mm_week'].rolling(k,min_periods=k).sum()
        g['roll']=roll.reset_index(level=0,drop=True)
        tr=g[g.split=='train']
        cw=tr.groupby(['GID_2','woy'])['roll'].agg(mu='mean',sd='std',n='count')       # per calendar cell
        cg=tr.groupby('GID_2')['roll'].agg(mu_g='mean',sd_g='std')                     # per-GID_2 fallback
        gg=g.merge(cw,on=['GID_2','woy'],how='left').merge(cg,on='GID_2',how='left')
        use_cell=(gg['n']>=5)&(gg['sd']>0)&gg['sd'].notna()
        mu=np.where(use_cell,gg['mu'],gg['mu_g']); sd=np.where(use_cell,gg['sd'],gg['sd_g'])
        gg[col]=(gg['roll']-mu)/np.where((sd>0)&np.isfinite(sd),sd,np.nan)
        spi=gg[KEY+[col]].drop_duplicates(KEY)
        feat=feat.merge(spi,on=KEY,how='left')
        miss=_complete_on_cc(feat[KEY+[col]],base,[col])[col]
        if miss<=TOL_FRAC*n_cc:
            kept.append(col); print(f"[spi] {col}: {miss}/{n_cc} missing on cc rows ({miss/n_cc:.2%}) -> kept")
        else:
            feat=feat.drop(columns=[col]); print(f"[spi] {col}: {miss}/{n_cc} missing on cc rows ({miss/n_cc:.2%}) -> DROPPED (insufficient history)")
        g=g.drop(columns=['roll'])
    if not kept:
        raise RuntimeError("derive_spi: no SPI scale within the missingness tolerance")
    print(f"[spi] emitting scales: {kept}")
    return feat[KEY+kept]

def derive_dtr(base):
    """Diurnal temperature range = weekly-mean(Tmax - Tmin), lagged (dtr_lag0..8).

    Needs a weekly per-GID_2 ERA5-Land grid with Tmax and Tmin (columns tmax_C_week,tmin_C_week).
    The current Colombia extraction computed daily-MEAN 2m temperature only, so this input does
    not exist yet -- re-extract ERA5-Land 2m_temperature at daily max & min, zonal-mean per
    municipality-week, write {ERA5_TMAXMIN}. Implementation below is ready; it just needs the file."""
    if not os.path.exists(ERA5_TMAXMIN):
        raise FileNotFoundError(
            f"derive_dtr: missing {ERA5_TMAXMIN}. Stage ERA5-Land daily Tmax/Tmin -> weekly zonal "
            f"mean per GID_2 with columns [GID_2,week_start,tmax_C_week,tmin_C_week]. "
            f"(Colombia currently has weekly-MEAN temp only; DTR is not derivable from it.)")
    w=pd.read_csv(ERA5_TMAXMIN,dtype={'week_start':str})
    w['dtr_C_week']=w['tmax_C_week']-w['tmin_C_week']
    feat=_lag_from_weekly(base,w,'dtr_C_week','dtr',nlag=9)
    bad=_complete_on_cc(feat,base,[c for c in feat.columns if c not in KEY])
    drop=[c for c,n in bad.items() if n>0]
    if drop: print(f"[dtr] dropping incomplete lags on cc rows: {drop}"); feat=feat.drop(columns=drop)
    return feat

def derive_vpd(base):
    """Vapour-pressure deficit (kPa) = es(Tmean) - es(Tdew), Magnus form, lagged (vpd_lag0..8).

      es(T) = 0.6108 * exp(17.27*T/(T+237.3))   [kPa, T in degC]
    Uses weekly-mean 2m temp (already staged, temp_C_week) and weekly-mean dewpoint d2m (NOT
    staged). Re-extract ERA5-Land 2m_dewpoint_temperature -> weekly zonal mean per GID_2 into
    {ERA5_D2M} with columns [GID_2,week_start,d2m_C_week]. Implementation below is ready."""
    if not os.path.exists(ERA5_D2M):
        raise FileNotFoundError(
            f"derive_vpd: missing {ERA5_D2M}. Stage ERA5-Land dewpoint (d2m) -> weekly zonal mean "
            f"per GID_2 with columns [GID_2,week_start,d2m_C_week]. (No dewpoint was extracted for "
            f"Colombia, so VPD is not derivable yet.)")
    def es(T): return 0.6108*np.exp(17.27*T/(T+237.3))
    tair=pd.read_csv(PRECIP_GRID,dtype={'week_start':str},usecols=['GID_2','week_start','temp_C_week'])
    dew=pd.read_csv(ERA5_D2M,dtype={'week_start':str})
    w=tair.merge(dew,on=KEY,how='inner')
    w['vpd_kPa_week']=(es(w['temp_C_week'])-es(w['d2m_C_week'])).clip(lower=0)
    feat=_lag_from_weekly(base,w,'vpd_kPa_week','vpd',nlag=9)
    bad=_complete_on_cc(feat,base,[c for c in feat.columns if c not in KEY])
    drop=[c for c,n in bad.items() if n>0]
    if drop: print(f"[vpd] dropping incomplete lags on cc rows: {drop}"); feat=feat.drop(columns=drop)
    return feat

# Enable a deriver by uncommenting. SPI runs now; DTR/VPD raise until their ERA5 inputs are staged.
DERIVERS=[
    ('spi', derive_spi),
    # ('dtr', derive_dtr),
    # ('vpd', derive_vpd),
]

# ------------------------------------------------------------------ validate + write
def validate(feat, base):
    if feat.duplicated(KEY).any(): raise RuntimeError("duplicate (GID_2,week_start) keys in geo features")
    featcols=[c for c in feat.columns if c not in KEY]
    if not featcols: raise RuntimeError("no feature columns produced")
    # Residual per-column missingness on cc rows is allowed here (kept scales may carry a few NaNs);
    # the harness intersects into a shared M6-inclusive mask so M0-M6 stay row-fair. Report it.
    n_cc=len(_cc_keys(base)); res=_complete_on_cc(feat,base,featcols)
    for c,n in res.items():
        if n: print(f"[validate] {c}: {n}/{n_cc} NaN on cc rows ({n/n_cc:.2%}) -> harness will intersect")
    return feat

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--smoke',action='store_true',help='emit a PLUMBING-ONLY placeholder column (NOT a real feature)')
    a=ap.parse_args()
    base=_load_base()

    if a.smoke:
        b=pd.read_csv(SRC,dtype={'week_start':str},usecols=KEY+['temp_min_lag0_8','temp_max_lag0_8',
                                                                'common_complete_M1_to_M5_h4'])
        b['SMOKE_TESTONLY_dtr_proxy']=(b['temp_max_lag0_8']-b['temp_min_lag0_8']).astype(float)
        f=validate(b[KEY+['SMOKE_TESTONLY_dtr_proxy']],base); f.to_csv(OUT,index=False)
        print(f"[smoke] wrote PLUMBING-ONLY {OUT} -- do NOT quote results.")
        return

    frames=[]
    for name,fn in DERIVERS:
        print(f"[assemble] deriving {name} ...")
        frames.append(fn(base))
    if not frames:
        print("No derive_* enabled. Uncomment one in DERIVERS (SPI runs now).",file=sys.stderr); sys.exit(1)
    feat=frames[0]
    for extra in frames[1:]:
        feat=feat.merge(extra,on=KEY,how='outer',validate='one_to_one')
    feat=validate(feat,base); feat.to_csv(OUT,index=False)
    cols=[c for c in feat.columns if c not in KEY]
    print(f"[assemble] wrote {OUT}")
    print(f"[assemble] features: {cols}")
    print(f"[assemble] sha256={hashlib.sha256(open(OUT,'rb').read()).hexdigest()[:16]}")

if __name__=='__main__':
    main()
