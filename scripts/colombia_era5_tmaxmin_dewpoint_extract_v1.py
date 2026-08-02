#!/usr/bin/env python3
"""Colombia ERA5-Land daily Tmax / Tmin / dewpoint -> weekly per-GID_2 grids.

Companion to _build_temp_full2.py (daily-MEAN temperature). SAME polygons (GADM COL L2,
crosswalk-filtered, 1065), SAME all_touched rasterize + daily areal-mean zonal aggregation,
SAME weekly index (OpenDengue Colombia Admin2 weeks + 8 lead weeks), SAME Kelvin->C. Only the
requested ERA5 daily-statistic fields differ. Outputs are ROW-ALIGNED to
colombia_weekly_era5_temperature_gid2_v1.csv so they merge 1:1 on (GID_2, week_start).

Produces exactly the two files scripts/colombia_geo_feature_assembly_v1.py expects:
  colombia_weekly_era5_tmax_tmin_gid2_v1.csv  [GID_2,week_start,week_end,tmax_C_week,tmin_C_week,days_used]
  colombia_weekly_era5_dewpoint_gid2_v1.csv   [GID_2,week_start,week_end,d2m_C_week,days_used]
  -> unlock derive_dtr (DTR = weekly-mean(Tmax-Tmin)) and derive_vpd (VPD from Tmean+Tdew).

Requires: cdsapi + a configured ~/.cdsapirc (same CDS account used for the temp build),
xarray, geopandas, rasterio, netCDF4. Long-running (CDS queue + per-field download, order of
the temp build's ~60 h, x3 fields). Run detached; --only lets you fetch one field at a time.
"""
import cdsapi, xarray as xr, numpy as np, pandas as pd, geopandas as gpd, os, time, hashlib, zipfile, json, argparse
from rasterio.features import rasterize
from rasterio.transform import from_origin
log=lambda s: print(s,flush=True); t0=time.time(); OUT=os.getcwd()
CLIM='/home/mpcrlab/data_quarantine/colombia_climate_linkage_full_v1'
FEAS='/home/mpcrlab/data_quarantine/colombia_external_replication_feasibility_v1'

# ---- polygons: identical selection to _build_temp_full2.py ----
cx=pd.read_csv(f'{FEAS}/colombia_crosswalk_v1.csv')
al=pd.read_csv(f'{FEAS}/colombia_manual_alias_crosswalk_v1.csv')
gids=set(cx.loc[cx.match_type!='unmatched','gadm_gid2'])|set(al.loc[al.recommendation=='include','gadm_gid2'])
g=gpd.read_file(f'zip://{FEAS}/gadm41_COL_2.json.zip')
gp=g[g.GID_2.isin(gids)].reset_index(drop=True); GIDS=list(gp.GID_2); GI={k:i for i,k in enumerate(GIDS)}; NP=len(GIDS)

# ---- weekly index: identical to the temp build (OpenDengue COL Admin2 weeks + 8 lead weeks) ----
z=zipfile.ZipFile(f'/home/mpcrlab/data_quarantine/opendengue_extract_inspection_v1/Temporal_extract_V1_3.zip'); fn=z.namelist()[0]
ws=set()
for ch in pd.read_csv(z.open(fn),usecols=['adm_0_name','calendar_start_date','S_res','T_res'],chunksize=400000,low_memory=False):
    s=ch[(ch.adm_0_name=='COLOMBIA')&(ch.S_res=='Admin2')&(ch.T_res=='Week')]; ws|=set(pd.to_datetime(s.calendar_start_date))
weeks=sorted(ws); allweeks=[weeks[0]-pd.Timedelta(days=7*k) for k in range(8,0,-1)]+weeks
WI={}
for i,wk in enumerate(allweeks):
    for d in range(7): WI[(wk+pd.Timedelta(days=d)).date()]=i
NW=len(allweeks); years=list(range(allweeks[0].year,weeks[-1].year+1))
log(f"polys={NP} weeks={NW} years={years[0]}-{years[-1]}")

c=cdsapi.Client(); AREA=[13.6,-82.0,-4.4,-66.6]; state={'pairs':None}
def pick_var(ds,prefer):
    if prefer in ds.data_vars: return prefer
    cand=[v for v in ds.data_vars if v not in ('number','expver')]
    return cand[0]

def fetch(variable,daily_statistic,yrs,tag):
    nc=OUT+f"/_{tag}.nc"
    c.retrieve('derived-era5-land-daily-statistics',{'variable':[variable],
      'year':[str(y) for y in yrs],'month':[f"{m:02d}" for m in range(1,13)],'day':[f"{d:02d}" for d in range(1,32)],
      'daily_statistic':daily_statistic,'time_zone':'utc+00:00','frequency':'1_hourly','area':AREA},nc)
    return nc

def ingest(nc,prefer,acc,dcnt,man):
    sz=os.path.getsize(nc); sha=hashlib.sha256(open(nc,'rb').read()).hexdigest(); man.append((os.path.basename(nc),sz,sha))
    ds=xr.open_dataset(nc); tc='valid_time' if 'valid_time' in ds.coords else 'time'
    latn='latitude' if 'latitude' in ds.coords else 'lat'; lonn='longitude' if 'longitude' in ds.coords else 'lon'
    lat=ds[latn].values; lon=ds[lonn].values; flip=lat[1]>lat[0]
    if state['pairs'] is None:                       # build rasterize pairs ONCE; ERA5-Land grid identical across fields
        la=lat[::-1] if flip else lat; res=abs(round(float(la[0]-la[1]),4)); wt=from_origin(lon.min()-res/2,la.max()+res/2,res,res)
        H,W=len(lat),len(lon); cids=[]; pids=[]
        for r in gp.itertuples():
            cc=np.flatnonzero(rasterize([(r.geometry,1)],out_shape=(H,W),transform=wt,all_touched=True,fill=0,dtype='uint8'))
            cids.append(cc); pids.append(np.full(len(cc),GI[r.GID_2]))
        state['pairs']=(np.concatenate(cids),np.concatenate(pids)); log(f"  grid {H}x{W} pairs {len(state['pairs'][0])}")
    cids,pids=state['pairs']; times=pd.to_datetime(ds[tc].values); da=ds[pick_var(ds,prefer)]
    for ti,tt in enumerate(times):                   # daily areal MEAN per polygon -> accumulate per week
        wk=WI.get(pd.Timestamp(tt).date())
        if wk is None: continue
        layer=da.isel({tc:ti}).values-273.15         # Kelvin -> C (temperature AND dewpoint)
        if flip: layer=layer[::-1,:]
        vals=layer.ravel()[cids]; okm=~np.isnan(vals)
        s=np.bincount(pids[okm],weights=vals[okm],minlength=NP); cc=np.bincount(pids[okm],minlength=NP)
        dm=np.divide(s,cc,out=np.full(NP,np.nan),where=cc>0); has=cc>0
        acc[wk][has]+=dm[has]; dcnt[wk][has]+=1
    ds.close(); os.remove(nc)

def build_field(variable,daily_statistic,tag,prefer):
    """Fetch one daily-statistic field for the full span and reduce to a weekly per-GID_2 mean."""
    acc=np.zeros((NW,NP)); dcnt=np.zeros((NW,NP),dtype=int); man=[]
    try:
        log(f"[{tag}] requesting full span in ONE call ..."); nc=fetch(variable,daily_statistic,years,f'{tag}_all')
        log(f"  [{tag}] single OK {(time.time()-t0)/60:.1f}min"); ingest(nc,prefer,acc,dcnt,man)
    except Exception as e:
        log(f"[{tag}] single-call failed ({str(e)[:100]}); falling back to 3 chunks")
        for ci,yr in enumerate([years[0:6],years[6:12],years[12:]]):
            for att in range(3):
                try: nc=fetch(variable,daily_statistic,yr,f'{tag}_c{ci}'); break
                except Exception as e2: log(f"  [{tag}] chunk{ci} attempt{att+1} fail {str(e2)[:80]}"); time.sleep(15)
            ingest(nc,prefer,acc,dcnt,man); log(f"  [{tag}] chunk {ci+1}/3 done {(time.time()-t0)/60:.1f}min")
    week=np.divide(acc,dcnt,out=np.full((NW,NP),np.nan),where=dcnt>0)   # weekly MEAN of daily statistic
    rows=[(gid,allweeks[wk].date(),(allweeks[wk]+pd.Timedelta(days=6)).date(),
           (week[wk,pi] if dcnt[wk,pi]>0 else ''),int(dcnt[wk,pi])) for wk in range(NW) for pi,gid in enumerate(GIDS)]
    df=pd.DataFrame(rows,columns=['GID_2','week_start','week_end','value','days_used'])
    return df,man

FIELDS={  # tag -> (variable, daily_statistic, xarray var to prefer, output column)
 'tmax':('2m_temperature','daily_maximum','t2m','tmax_C_week'),
 'tmin':('2m_temperature','daily_minimum','t2m','tmin_C_week'),
 'd2m' :('2m_dewpoint_temperature','daily_mean','d2m','d2m_C_week'),
}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--only',choices=list(FIELDS),nargs='*',help='fetch only these fields (default: all)')
    a=ap.parse_args(); todo=a.only or list(FIELDS)
    built={}; manifest=[]
    for tag in todo:
        variable,stat,prefer,col=FIELDS[tag]
        log(f"=== FIELD {tag}: {variable}/{stat} -> {col} ===")
        df,man=build_field(variable,stat,tag,prefer); df=df.rename(columns={'value':col}); built[tag]=df; manifest+=man

    # tmax + tmin -> one row-aligned CSV (only when both were built)
    if 'tmax' in built and 'tmin' in built:
        m=built['tmax'].merge(built['tmin'][['GID_2','week_start','tmin_C_week']],on=['GID_2','week_start'],how='outer',validate='one_to_one')
        m=m[['GID_2','week_start','week_end','tmax_C_week','tmin_C_week','days_used']]
        m.to_csv(f'{CLIM}/colombia_weekly_era5_tmax_tmin_gid2_v1.csv',index=False)
        log(f"wrote colombia_weekly_era5_tmax_tmin_gid2_v1.csv rows={len(m)}")
    if 'd2m' in built:
        built['d2m'][['GID_2','week_start','week_end','d2m_C_week','days_used']].to_csv(
            f'{CLIM}/colombia_weekly_era5_dewpoint_gid2_v1.csv',index=False)
        log(f"wrote colombia_weekly_era5_dewpoint_gid2_v1.csv rows={len(built['d2m'])}")

    # row-alignment check against the daily-mean temperature grid (keys must match 1:1)
    ref=pd.read_csv(f'{CLIM}/colombia_weekly_era5_temperature_gid2_v1.csv',dtype={'week_start':str},usecols=['GID_2','week_start'])
    for tag,df in built.items():
        d=df.copy(); d['week_start']=d.week_start.astype(str)
        merged=ref.merge(d,on=['GID_2','week_start'],how='left',indicator=True)
        miss=int((merged['_merge']!='both').sum())
        log(f"  [{tag}] row-alignment vs temp grid: {len(ref)-miss}/{len(ref)} matched, {miss} unmatched")

    pd.DataFrame(manifest,columns=['file','bytes','sha256']).to_csv(f'{CLIM}/era5_tmaxmin_dewpoint_manifest_v1.csv',index=False)
    meta=dict(polygons=NP,weeks_total=NW,years=years,fields=todo,era5_files=len(manifest),
      era5_bytes=int(sum(x[1] for x in manifest)),
      variables={t:f"{FIELDS[t][0]}/{FIELDS[t][1]}->weekly_mean_C" for t in todo},
      note='row-aligned to colombia_weekly_era5_temperature_gid2_v1.csv; DTR=weekly-mean(Tmax-Tmin); VPD from Tmean+Tdew (Magnus)',
      runtime_min=round((time.time()-t0)/60,1))
    json.dump(meta,open(f'{CLIM}/colombia_era5_tmaxmin_dewpoint_v1.meta.json','w'),indent=2)
    log(f"DONE fields={todo} files={len(manifest)} MB={sum(x[1] for x in manifest)/1e6:.0f} runtime={(time.time()-t0)/60:.1f}min")

if __name__=='__main__':
    main()
