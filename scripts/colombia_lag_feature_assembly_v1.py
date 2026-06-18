#!/usr/bin/env python3
"""Colombia lag-feature value assembly (per docs/colombia_lag_feature_assembly_spec.md).
Assembles feature values + modelable flags ONLY. No models, no metrics, no label/threshold recompute.
Climate lags from the full gap-free climate grid; recent-case lags from the observed OpenDengue panel
(absent = missing, NOT zero). Outputs to quarantine only."""
import pandas as pd, numpy as np, hashlib, json, os
LF='/home/mpcrlab/data_quarantine/colombia_label_features_v1'
GRID='/home/mpcrlab/data_quarantine/colombia_climate_linkage_full_v1/colombia_weekly_climate_precip_temp_gid2_v1.csv'
LAB=f'{LF}/colombia_labels_h1_h2_h4_h8_h12_v1.csv'

lab=pd.read_csv(LAB,dtype={'week_start':str}); lab['wk']=pd.to_datetime(lab.week_start)
grid=pd.read_csv(GRID,dtype={'week_start':str})
clim={(g,w):(p,t) for g,w,p,t in zip(grid.GID_2,grid.week_start,grid.precip_mm_week,grid.temp_C_week)}
cases={(g,w):c for g,w,c in zip(lab.GID_2,lab.week_start,lab.dengue_total)}   # observed outcome panel

df=lab[['GID_2','week_start','split','dengue_total','label_h1','label_h2','label_h4','label_h8','label_h12']].copy()
def shifted(k): return (lab.wk-pd.Timedelta(weeks=k)).dt.date.astype(str)
# climate lags from full grid (no imputation; absent -> NaN)
for k in range(9):
    sh=shifted(k); vals=[clim.get((g,w),(np.nan,np.nan)) for g,w in zip(lab.GID_2,sh)]
    df[f'precip_lag{k}']=[v[0] for v in vals]; df[f'temp_lag{k}']=[v[1] for v in vals]
P=lambda a,b:[f'precip_lag{k}' for k in range(a,b+1)]; T=lambda a,b:[f'temp_lag{k}' for k in range(a,b+1)]
df['precip_mean_lag0_2']=df[P(0,2)].mean(axis=1); df['precip_mean_lag0_4']=df[P(0,4)].mean(axis=1); df['precip_mean_lag0_8']=df[P(0,8)].mean(axis=1)
df['precip_sum_lag0_2']=df[P(0,2)].sum(axis=1,min_count=3); df['precip_sum_lag0_4']=df[P(0,4)].sum(axis=1,min_count=5); df['precip_sum_lag0_8']=df[P(0,8)].sum(axis=1,min_count=9)
df['temp_mean_lag0_2']=df[T(0,2)].mean(axis=1); df['temp_mean_lag0_4']=df[T(0,4)].mean(axis=1); df['temp_mean_lag0_8']=df[T(0,8)].mean(axis=1)
df['temp_min_lag0_8']=df[T(0,8)].min(axis=1); df['temp_max_lag0_8']=df[T(0,8)].max(axis=1)
# recent-case lags from observed panel (absent = missing, flagged; NOT zero)
df['cases_lag0']=df.dengue_total
for j in [1,2,4]:
    sh=shifted(j); df[f'cases_lag{j}']=[cases.get((g,w),np.nan) for g,w in zip(lab.GID_2,sh)]
    df[f'cases_lag{j}_missing']=df[f'cases_lag{j}'].isna()
# seasonal (deterministic calendar)
woy=lab.wk.dt.isocalendar().week.astype(int).values; df['week_of_year']=woy
ang=2*np.pi*woy/52.1775
df['sin_woy_1']=np.sin(ang); df['cos_woy_1']=np.cos(ang); df['sin_woy_2']=np.sin(2*ang); df['cos_woy_2']=np.cos(2*ang)
# modelability flags (h4)
clim_ok=df[[f'precip_lag{k}' for k in range(9)]+[f'temp_lag{k}' for k in range(9)]].notna().all(axis=1)
cases_ok=df[['cases_lag0','cases_lag1','cases_lag2','cases_lag4']].notna().all(axis=1)
h4=df.label_h4.notna()
df['modelable_M2_M3_h4']=h4&clim_ok
df['modelable_M1_h4']=h4&cases_ok
df['modelable_M4_M5_h4']=h4&clim_ok&cases_ok
df['common_complete_M1_to_M5_h4']=h4&clim_ok&cases_ok

# outputs
feat_cols=['GID_2','week_start','split']+[f'precip_lag{k}' for k in range(9)]+[f'temp_lag{k}' for k in range(9)]+\
 ['precip_mean_lag0_2','precip_mean_lag0_4','precip_mean_lag0_8','precip_sum_lag0_2','precip_sum_lag0_4','precip_sum_lag0_8',
  'temp_mean_lag0_2','temp_mean_lag0_4','temp_mean_lag0_8','temp_min_lag0_8','temp_max_lag0_8',
  'cases_lag0','cases_lag1','cases_lag2','cases_lag4','cases_lag1_missing','cases_lag2_missing','cases_lag4_missing',
  'week_of_year','sin_woy_1','cos_woy_1','sin_woy_2','cos_woy_2']
flagcols=['modelable_M2_M3_h4','modelable_M1_h4','modelable_M4_M5_h4','common_complete_M1_to_M5_h4']
df[feat_cols].to_csv(f'{LF}/colombia_lag_feature_values_v1.csv',index=False)
allh=df[feat_cols+['dengue_total','label_h1','label_h2','label_h4','label_h8','label_h12']+flagcols]
allh.to_csv(f'{LF}/colombia_modeling_table_all_horizons_v1.csv',index=False)
df[df.label_h4.notna()][feat_cols+['dengue_total','label_h4']+flagcols].to_csv(f'{LF}/colombia_modeling_table_h4_75pct_v1.csv',index=False)

# diagnostics
diag=[]
for sp in ['train','val','test','ALL']:
    s=df if sp=='ALL' else df[df.split==sp]
    diag.append(('rows',sp,'count',len(s)))
    for fl in flagcols: diag.append((fl,sp,'count',int(s[fl].sum())))
    diag.append(('clim_lag0_8_complete',sp,'count',int((s[[f'precip_lag{k}' for k in range(9)]+[f'temp_lag{k}' for k in range(9)]].notna().all(axis=1)).sum())))
    for j in [1,2,4]: diag.append((f'cases_lag{j}_present',sp,'count',int(s[f'cases_lag{j}'].notna().sum())))
diag.append(('dup_gid2_week','ALL','count',int(df.duplicated(['GID_2','week_start']).sum())))
pd.DataFrame(diag,columns=['metric','split','stat','value']).to_csv(f'{LF}/colombia_feature_assembly_diagnostics_v1.csv',index=False)

# meta
def sh(p): return hashlib.sha256(open(p,'rb').read()).hexdigest()
outs=['colombia_lag_feature_values_v1.csv','colombia_modeling_table_all_horizons_v1.csv','colombia_modeling_table_h4_75pct_v1.csv','colombia_feature_assembly_diagnostics_v1.csv']
meta=dict(spec='docs/colombia_lag_feature_assembly_spec.md (commit 84ad43f)',
  inputs={os.path.basename(GRID):sh(GRID),os.path.basename(LAB):sh(LAB)},
  base_rows=len(df),split_counts=df.split.value_counts().to_dict(),
  climate_lags='precip_lag0..8,temp_lag0..8 from full climate grid (no imputation, no future)',
  recent_case_lags='cases_lag0/1/2/4 from observed OpenDengue panel; absent=missing (flagged), NOT zero',
  modelable_h4={fl:int(df[fl].sum()) for fl in flagcols},
  modelable_h4_by_split={fl:df.groupby('split')[fl].sum().astype(int).to_dict() for fl in flagcols},
  labels_thresholds_recomputed=False,models_run=False,metrics_run=False,external_validation=False,no_leakage=True,
  output_sha256={o:sh(f'{LF}/{o}') for o in outs})
json.dump(meta,open(f'{LF}/colombia_feature_assembly_v1.meta.json','w'),indent=2)
print('base rows',len(df))
print('modelable h4:',{fl:int(df[fl].sum()) for fl in flagcols})
print('modelable h4 by split:',{fl:df.groupby('split')[fl].sum().astype(int).to_dict() for fl in flagcols})
print('clim_lag0_8 complete (all rows):',int(clim_ok.sum()),f'({100*clim_ok.mean():.1f}%)')
print('cases present:',{f'lag{j}':int(df[f'cases_lag{j}'].notna().sum()) for j in [0,1,2,4]})
print('dup keys:',int(df.duplicated(['GID_2','week_start']).sum()))
for o in outs+['colombia_feature_assembly_v1.meta.json']:
    print(' ',sh(f'{LF}/{o}')[:16],'…',os.path.getsize(f'{LF}/{o}'),'B',o)
