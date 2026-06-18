import pandas as pd, numpy as np, hashlib, json, os
SRC='/home/mpcrlab/data_quarantine/colombia_climate_linkage_full_v1/colombia_opendengue_climate_linked_with_temp_v1.csv'
OUT=os.getcwd()
d=pd.read_csv(SRC,dtype={'week_start':str})
prim=d[d.gadm_gid2.notna()&d.precip_mm_week.notna()&d.temp_C_week.notna()&(~d.excluded_newly_created)].copy()
prim['wk']=pd.to_datetime(prim.week_start)
# OPTION 1 aggregation: sum dengue_total onto shared polygon; climate identical within polygon
agg_before=len(prim)
panel=prim.groupby(['gadm_gid2','wk'],as_index=False).agg(dengue_total=('dengue_total','sum'),
        precip_mm_week=('precip_mm_week','first'),temp_C_week=('temp_C_week','first'))
panel=panel.rename(columns={'gadm_gid2':'GID_2'})
panel['week_start']=panel.wk.dt.date.astype(str); panel['week_end']=(panel.wk+pd.Timedelta(days=6)).dt.date.astype(str)
n_aggregated=agg_before-len(panel)
TR1=pd.Timestamp('2017-12-31'); VA1=pd.Timestamp('2019-12-31')
panel['split']=np.where(panel.wk<=TR1,'train',np.where(panel.wk<=VA1,'val','test'))
keyset=set(zip(panel.GID_2,panel.wk))

# thresholds from TRAIN only
tr=panel[panel.split=='train']
th=tr.groupby('GID_2').dengue_total.agg(train_weeks='size',nonzero_train_weeks=lambda s:int((s>0).sum()),
     thr75=lambda s:float(np.percentile(s,75)),thr90=lambda s:float(np.percentile(s,90))).reset_index()
th['flag_lt52_train_weeks']=th.train_weeks<52
th['flag_lt10_nonzero']=th.nonzero_train_weeks<10
th['flag_thr75_zero']=th.thr75==0
panel=panel.merge(th[['GID_2','thr75']],on='GID_2',how='left')

# labels via shifted self-merge
HZ=[1,2,4,8,12]
out=panel[['GID_2','week_start','week_end','split','dengue_total','thr75']].copy()
prev={}; labelable={}
for h in HZ:
    fut=panel[['GID_2','wk','dengue_total']].copy(); fut['wk']=fut.wk-pd.Timedelta(weeks=h)
    mm=panel[['GID_2','wk','thr75']].merge(fut.rename(columns={'dengue_total':'df'}),on=['GID_2','wk'],how='left')
    lab=np.where(mm.df.notna(),(mm.df>mm.thr75).astype('float'),np.nan)
    out[f'label_h{h}']=lab
    labelable[h]=int(mm.df.notna().sum())
    L=pd.DataFrame({'split':panel.split.values,'lab':lab}).dropna()
    prev[h]=L.groupby('split').lab.mean().to_dict()
out.to_csv(f'{OUT}/colombia_labels_h1_h2_h4_h8_h12_v1.csv',index=False)

# per-unit h4 prevalence + flags into thresholds file
h4=pd.DataFrame({'GID_2':panel.GID_2,'split':panel.split,'lab':out['label_h4']})
h4p=h4.dropna(subset=['lab']).groupby('GID_2').lab.mean().rename('h4_prevalence').reset_index()
th=th.merge(h4p,on='GID_2',how='left')
th['flag_h4_prev_lt1pct']=th.h4_prevalence<0.01
th['flag_h4_prev_gt80pct']=th.h4_prevalence>0.80
th.to_csv(f'{OUT}/colombia_label_thresholds_train_only_v1.csv',index=False)

# lag availability — CLIMATE-GRID keyset (NOT the OpenDengue observed panel).
# A climate lag k at week t is available iff the full gap-free climate grid has (GID_2, t-k);
# it does NOT require an OpenDengue outcome row at t-k. (Corrected 2026-06-18.)
GRID='/home/mpcrlab/data_quarantine/colombia_climate_linkage_full_v1/colombia_weekly_climate_precip_temp_gid2_v1.csv'
_grid=pd.read_csv(GRID,dtype={'week_start':str})
_cok=_grid[_grid.precip_mm_week.notna()&_grid.temp_C_week.notna()]
ckey=set(zip(_cok.GID_2,_cok.week_start))
la=panel[['GID_2','week_start','split','wk']].copy()
for k in range(9):
    sh=(panel.wk-pd.Timedelta(weeks=k)).dt.date.astype(str)
    avail=[ (g,w) in ckey for g,w in zip(panel.GID_2,sh)]
    la[f'precip_lag{k}_avail']=avail; la[f'temp_lag{k}_avail']=avail
full=np.all([la[f'precip_lag{k}_avail'] for k in range(9)],axis=0)
la['full_lag0_8_precip']=full; la['full_lag0_8_temp']=full; la['full_lag0_8_both']=full
for h in HZ:
    la[f'modelable_h{h}']=full & out[f'label_h{h}'].notna().values
la.drop(columns=['wk']).to_csv(f'{OUT}/colombia_lag_feature_availability_v1.csv',index=False)

# diagnostics (tidy) : by-year continuity + horizon + split
panel['yr']=panel.wk.dt.year
diag=[]
for yr,g in panel.groupby('yr'):
    diag.append(('by_year',int(yr),'rows',len(g))); diag.append(('by_year',int(yr),'reporting_units',g.GID_2.nunique())); diag.append(('by_year',int(yr),'total_cases',float(g.dengue_total.sum())))
for h in HZ:
    diag.append(('horizon',h,'labelable_rows',labelable[h]))
    for sp in ['train','val','test']:
        diag.append(('prevalence',f'h{h}_{sp}',sp, round(prev[h].get(sp,float('nan')),4)))
for sp,c in panel.split.value_counts().items(): diag.append(('split',sp,'rows',int(c)))
diag.append(('flags','thr75_zero_units','count',int(th.flag_thr75_zero.sum())))
diag.append(('flags','lt52_train_units','count',int(th.flag_lt52_train_weeks.sum())))
diag.append(('flags','lt10_nonzero_units','count',int(th.flag_lt10_nonzero.sum())))
diag.append(('aggregation','rows_folded_option1','count',int(n_aggregated)))
pd.DataFrame(diag,columns=['category','key','metric','value']).to_csv(f'{OUT}/colombia_label_construction_diagnostics_v1.csv',index=False)

# meta + checksums
files=['colombia_label_thresholds_train_only_v1.csv','colombia_labels_h1_h2_h4_h8_h12_v1.csv',
       'colombia_lag_feature_availability_v1.csv','colombia_label_construction_diagnostics_v1.csv']
sha={f:hashlib.sha256(open(f'{OUT}/{f}','rb').read()).hexdigest() for f in files}
meta=dict(spec='docs/colombia_label_specification.md (commit 9fdbbbe)',input=SRC,
  input_sha256='248bb73a11e8e433e3ce45e8d5e3e535f6864c6b5198eb1e02aad080f6e5ee5a',
  option1_aggregation=dict(gid2='COL.28.78_2',od_units=['SOCORRO','PALMAS SOCORRO'],rule='sum dengue_total onto shared polygon; climate identical',rows_folded=int(n_aggregated)),
  panel_rows=len(panel),units=int(panel.GID_2.nunique()),
  split=dict(train='2006-12-31..2017-12-31',val='2018-01-01..2019-12-31',test='2020-01-01..2022-12-25',
             counts=panel.split.value_counts().to_dict()),
  threshold='train-only per-GID_2 75th pct (90th for sensitivity); strictly-greater label; absent t+h -> undefined (no assume-zero)',
  horizons=HZ,labelable=labelable,prevalence={h:prev[h] for h in HZ},
  flags=dict(thr75_zero=int(th.flag_thr75_zero.sum()),lt52_train=int(th.flag_lt52_train_weeks.sum()),lt10_nonzero=int(th.flag_lt10_nonzero.sum())),
  no_leakage=True,models_run=False,metrics_run=False,external_validation=False,output_sha256=sha)
json.dump(meta,open(f'{OUT}/colombia_label_specification_v1.meta.json','w'),indent=2)
print("panel rows",len(panel),"units",panel.GID_2.nunique(),"folded",n_aggregated)
print("h4 labelable",labelable[4],"prev",{k:round(v,3) for k,v in prev[4].items()})
print("thr75==0 units",int(th.flag_thr75_zero.sum()))
print("files written:",files+['colombia_label_specification_v1.meta.json'])
for f in files: print(" ",f,sha[f][:16],"…",os.path.getsize(f'{OUT}/{f}'),"B")
