# Phase 5 — NB and matched climate increment across p* thresholds, from the VALIDATED
# frozen Sri Lanka reconstruction. Re-derives from frozen predictions only (no frozen
# result is altered); exits without reporting if reconstruction does not reproduce frozen <1e-6.
import pandas as pd, numpy as np, json, sys, csv
from patsy import dmatrix, build_design_matrices
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
V2="/home/mpcrlab/data_quarantine/analysis_tables/dengue_climate_population_linked_2018_2025_v2_date_aligned.csv"
PRIM="/home/mpcrlab/data_quarantine/model_pilots/pilot_h4_75pct_v1/predictions_h4_75pct_v1.csv"
HYB="/home/mpcrlab/data_quarantine/model_pilots/hybrid_model_extension_v1/hybrid_model_predictions_v1.csv"
CLIMVARS=['t2m_mean_c','precip_sum_mm','rh_mean_percent']; LAGS=list(range(0,9)); SEED=20260612; CGRID=[0.1,1.0,10.0]
EPS=1e-6; clip=lambda p:np.clip(p,EPS,1-EPS)
m=pd.read_csv(V2,parse_dates=['week_start','week_end'])
f=m[(m.outcome_missing_flag==0)&(m.exposure_missing_flag==0)&(m.population_missing_flag==0)&
    (m.epi_year>=2018)&(m.epi_year<=2025)].copy().sort_values(['geometry_id','week_start']).reset_index(drop=True)
fut=f[['geometry_id','week_start','dengue_incidence_per_100k']].rename(columns={'dengue_incidence_per_100k':'inc_future'})
fut['week_start']=fut['week_start']-pd.Timedelta(days=28)
f=f.merge(fut,on=['geometry_id','week_start'],how='left'); f=f[f.inc_future.notna()].copy()
f['split']=np.where(f.epi_year<=2022,'train','test')
g=f[f.split=='train'].groupby('geometry_id')['dengue_incidence_per_100k']
f=f.merge(g.quantile(0.75).rename('thr75').reset_index(),on='geometry_id',how='left')
f['y']=(f['inc_future']>f['thr75']).astype(int)
for L in [1,2,4]:
    t=f[['geometry_id','week_start','dengue_incidence_per_100k']].rename(columns={'dengue_incidence_per_100k':f'inc_lag{L}'}).copy()
    t['week_start']=t['week_start']+pd.Timedelta(days=7*L); f=f.merge(t,on=['geometry_id','week_start'],how='left')
f['inc_t']=f['dengue_incidence_per_100k']
for v in CLIMVARS:
    for L in LAGS:
        t=f[['geometry_id','week_start',v]].rename(columns={v:f'{v}__L{L}'}).copy()
        t['week_start']=t['week_start']+pd.Timedelta(days=7*L); f=f.merge(t,on=['geometry_id','week_start'],how='left')
w=2*np.pi*f['epi_week']/52.18
f['sin1'],f['cos1'],f['sin2'],f['cos2']=np.sin(w),np.cos(w),np.sin(2*w),np.cos(2*w)
rd=pd.get_dummies(f['geometry_id'],prefix='rd',drop_first=True).astype(float); f=pd.concat([f,rd],axis=1); RD=list(rd.columns)
tr0=f[f.split=='train']
for c in ['inc_lag1','inc_lag2','inc_lag4']+[f'{v}__L{L}' for v in CLIMVARS for L in LAGS]:
    f[c]=f[c].fillna(tr0[c].mean())
tr=f[f.split=='train'].copy(); te=f[f.split=='test'].copy(); ytr=tr['y'].values; yte=te['y'].values
AR=['inc_t','inc_lag1','inc_lag2','inc_lag4']; VDF=LDF=3
DIs={v:dmatrix(f"cr(x, df={VDF}) - 1",{"x":tr[f'{v}__L0'].values},return_type='dataframe').design_info for v in CLIMVARS}
BLAG=np.asarray(dmatrix(f"cr(x, df={LDF}) - 1",{"x":np.array(LAGS,float)},return_type='dataframe'))
def crossbasis(rows,v):
    n=len(rows); Vb=np.empty((n,len(LAGS),VDF))
    for i,L in enumerate(LAGS): Vb[:,i,:]=np.asarray(build_design_matrices([DIs[v]],{"x":rows[f'{v}__L{L}'].values})[0])
    return np.einsum('nlj,lk->njk',Vb,BLAG).reshape(n,VDF*LDF)
def climate_block(rows): return np.concatenate([crossbasis(rows,v) for v in CLIMVARS],axis=1)
def design(rows,kind):
    cb=climate_block(rows) if kind in ('M4','M5') else None
    if kind=='cases':   return rows[AR].values
    if kind=='matched': return np.concatenate([rows[AR].values, rows[['sin1','cos1','sin2','cos2']+RD].values],axis=1)
    if kind=='M4':      return np.concatenate([rows[AR].values, cb],axis=1)
    if kind=='M5':      return np.concatenate([rows[AR].values, cb, rows[['sin1','cos1','sin2','cos2']+RD].values],axis=1)
def time_blocks(rows):
    yrs=sorted(rows['epi_year'].unique()); folds=[]
    for i in range(1,len(yrs)):
        tri=rows.index[rows['epi_year']<=yrs[i-1]]; vai=rows.index[rows['epi_year']==yrs[i]]
        if len(vai)>0 and rows.loc[tri,'y'].nunique()>1 and rows.loc[vai,'y'].nunique()>1: folds.append((tri,vai))
    return folds
def fit_eval(kind):
    Xtr_full=design(tr,kind); Xte=design(te,kind); mu=Xtr_full.mean(0); sd=Xtr_full.std(0); sd[sd==0]=1
    folds=time_blocks(tr); bestC,bestS=None,-1
    for C in CGRID:
        sc=[]
        for tri,vai in folds:
            Xt=(design(tr.loc[tri],kind)-mu)/sd; Xv=(design(tr.loc[vai],kind)-mu)/sd
            clf=LogisticRegression(penalty='l2',C=C,solver='lbfgs',max_iter=8000).fit(Xt,tr.loc[tri,'y'].values)
            sc.append(roc_auc_score(tr.loc[vai,'y'].values,clf.predict_proba(Xv)[:,1]))
        ms=float(np.mean(sc))
        if ms>bestS: bestS,bestC=ms,C
    Xtr=(Xtr_full-mu)/sd; Xtes=(Xte-mu)/sd
    clf=LogisticRegression(penalty='l2',C=bestC,solver='lbfgs',max_iter=8000).fit(Xtr,ytr)
    if np.abs(clf.coef_).max()>15: clf=LogisticRegression(penalty='l2',C=0.1,solver='lbfgs',max_iter=8000).fit(Xtr,ytr)
    return clip(clf.predict_proba(Xtes)[:,1])
def fit_score_M1():
    cont=AR; mu=tr[cont].mean(); sd=tr[cont].std(ddof=0).replace(0,1)
    Xtr=np.concatenate([((tr[cont]-mu)/sd).values, tr[['sin1','cos1','sin2','cos2']+RD].values],axis=1)
    Xte=np.concatenate([((te[cont]-mu)/sd).values, te[['sin1','cos1','sin2','cos2']+RD].values],axis=1)
    clf=LogisticRegression(penalty='l2',C=1e6,solver='lbfgs',max_iter=5000).fit(Xtr,ytr)
    return clip(clf.predict_proba(Xte)[:,1])
M1=fit_score_M1(); pM4=fit_eval('M4'); pM5=fit_eval('M5'); pmatch=fit_eval('matched'); pcases=fit_eval('cases')
# validate against frozen
prim=pd.read_csv(PRIM,parse_dates=['week_start']); hyb=pd.read_csv(HYB,parse_dates=['week_start'])
key=['geometry_id','week_start']; tv=te[key].copy(); tv['M1n']=M1; tv['M4n']=pM4; tv['M5n']=pM5
mg=tv.merge(prim[key+['p_M1_lagged_AR']],on=key).merge(hyb[key+['p_M4_hybrid','p_M5_hybrid_season_RDHS']],on=key)
d1=np.abs(mg['M1n']-mg['p_M1_lagged_AR']).max(); d4=np.abs(mg['M4n']-mg['p_M4_hybrid']).max(); d5=np.abs(mg['M5n']-mg['p_M5_hybrid_season_RDHS']).max()
if not (d1<1e-6 and d4<1e-6 and d5<1e-6):
    print(f"VALIDATION FAILED M1={d1:.1e} M4={d4:.1e} M5={d5:.1e} — NOT REPORTING"); sys.exit(1)
def nb(y,p,t): a=p>=t; n=len(y); return (a&(y==1)).sum()/n-(a&(y==0)).sum()/n*(t/(1-t))
rd_ids=sorted(te['geometry_id'].unique()); groups={g:np.where(te['geometry_id'].values==g)[0] for g in rd_ids}
rng=np.random.default_rng(SEED)
def bootci(pa,pb,t,B=1000):
    D=[]
    for _ in range(B):
        idx=np.concatenate([groups[rd_ids[i]] for i in rng.integers(0,len(rd_ids),len(rd_ids))]); yy=yte[idx]
        if yy.min()==yy.max(): continue
        D.append(nb(yy,pa[idx],t)-nb(yy,pb[idx],t))
    return [round(float(np.percentile(D,2.5)),5),round(float(np.percentile(D,97.5)),5)]
rows=[]
for t in [0.10,0.20,0.30,0.40,0.50]:
    inc=round(nb(yte,pM5,t)-nb(yte,pmatch,t),5); ci=bootci(pM5,pmatch,t)
    rows.append(dict(pstar=t, prop_flagged=round(float((pM5>=t).mean()),4),
        NB_M1=round(nb(yte,M1,t),5), NB_M4=round(nb(yte,pM4,t),5), NB_M5=round(nb(yte,pM5,t),5),
        NB_matched=round(nb(yte,pmatch,t),5), NB_cases=round(nb(yte,pcases,t),5),
        dNB_matched_climate=inc, matched_ci_lo=ci[0], matched_ci_hi=ci[1],
        dNB_M4_M1=round(nb(yte,pM4,t)-nb(yte,M1,t),5), dNB_M5_M1_frozen=round(nb(yte,pM5,t)-nb(yte,M1,t),5),
        sign_matched=("+" if inc>0 else ("0" if inc==0 else "-"))))
with open("/home/mpcrlab/srilanka-dengue-ews-calibration/analysis/v15_final/final_threshold_consistency_check.csv","w",newline="") as fh:
    wtr=csv.DictWriter(fh,fieldnames=list(rows[0].keys())); wtr.writeheader(); [wtr.writerow(r) for r in rows]
print(f"VALIDATED (max|Δ| M1={d1:.1e} M4={d4:.1e} M5={d5:.1e}); n_test={len(yte)}")
print(json.dumps(rows,indent=1))
