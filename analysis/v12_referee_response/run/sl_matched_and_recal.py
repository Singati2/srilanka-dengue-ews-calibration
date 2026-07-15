# Reconstruct the EXACT frozen Sri Lanka pipeline, VALIDATE against committed frozen
# predictions, then run the two headline analyses the reviewers asked for:
#  (A) SL specification-matched decomposition (M5 vs M5_no-climate = AR+season+RDHS),
#      analogous to Colombia's Table 7, with RDHS-cluster bootstrap CIs.
#  (B) Past-only rolling-52 recalibration applied to M1, M4, M5 (same procedure the
#      frozen run applied to M0-M3), with recalibrated calibration + net benefit.
# Nothing is reported unless the reconstruction reproduces the frozen M1/M4/M5 to <1e-6.
import pandas as pd, numpy as np, json, sys
from patsy import dmatrix, build_design_matrices
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, brier_score_loss
import statsmodels.api as sm
V2="/home/mpcrlab/data_quarantine/analysis_tables/dengue_climate_population_linked_2018_2025_v2_date_aligned.csv"
PRIM="/home/mpcrlab/data_quarantine/model_pilots/pilot_h4_75pct_v1/predictions_h4_75pct_v1.csv"
HYB="/home/mpcrlab/data_quarantine/model_pilots/hybrid_model_extension_v1/hybrid_model_predictions_v1.csv"
RUN="/home/mpcrlab/srilanka-dengue-ews-calibration/analysis/v12_referee_response/run/"
CLIMVARS=['t2m_mean_c','precip_sum_mm','rh_mean_percent']; LAGS=list(range(0,9)); SEED=20260612; CGRID=[0.1,1.0,10.0]
EPS=1e-6; clip=lambda p:np.clip(p,EPS,1-EPS); logit=lambda p:np.log(clip(p)/(1-clip(p))); sig=lambda z:1/(1+np.exp(-z))

# ---- reconstruct frame (verbatim from _run_hybrid_model_extension.py) ----
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
f['target_week']=f['week_start']+pd.Timedelta(days=28)
tr=f[f.split=='train'].copy(); te=f[f.split=='test'].copy(); ytr=tr['y'].values; yte=te['y'].values
AR=['inc_t','inc_lag1','inc_lag2','inc_lag4']
VDF=LDF=3
DIs={v:dmatrix(f"cr(x, df={VDF}) - 1",{"x":tr[f'{v}__L0'].values},return_type='dataframe').design_info for v in CLIMVARS}
BLAG=np.asarray(dmatrix(f"cr(x, df={LDF}) - 1",{"x":np.array(LAGS,float)},return_type='dataframe'))
def crossbasis(rows,v):
    n=len(rows); Vb=np.empty((n,len(LAGS),VDF))
    for i,L in enumerate(LAGS): Vb[:,i,:]=np.asarray(build_design_matrices([DIs[v]],{"x":rows[f'{v}__L{L}'].values})[0])
    return np.einsum('nlj,lk->njk',Vb,BLAG).reshape(n,VDF*LDF)
def climate_block(rows): return np.concatenate([crossbasis(rows,v) for v in CLIMVARS],axis=1)
def design(rows,kind):
    cb=climate_block(rows) if kind in ('M4','M5','clim_only') else None
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
        ms=float(np.mean(sc));
        if ms>bestS: bestS,bestC=ms,C
    Xtr=(Xtr_full-mu)/sd; Xtes=(Xte-mu)/sd
    clf=LogisticRegression(penalty='l2',C=bestC,solver='lbfgs',max_iter=8000).fit(Xtr,ytr)
    if np.abs(clf.coef_).max()>15: clf=LogisticRegression(penalty='l2',C=0.1,solver='lbfgs',max_iter=8000).fit(Xtr,ytr)
    return clip(clf.predict_proba(Xtes)[:,1]), clip(clf.predict_proba((design(f,kind)-mu)/sd)[:,1])
# M1 exactly as frozen (fit_score AR+season+RDHS, C=1e6)
def fit_score_M1():
    cont=AR; mu=tr[cont].mean(); sd=tr[cont].std(ddof=0).replace(0,1)
    Xtr=np.concatenate([((tr[cont]-mu)/sd).values, tr[['sin1','cos1','sin2','cos2']+RD].values],axis=1)
    Xall=np.concatenate([((f[cont]-mu)/sd).values, f[['sin1','cos1','sin2','cos2']+RD].values],axis=1)
    clf=LogisticRegression(penalty='l2',C=1e6,solver='lbfgs',max_iter=5000).fit(Xtr,ytr)
    p_all=clip(clf.predict_proba(Xall)[:,1]); return p_all[te.index.map({ix:i for i,ix in enumerate(f.index)}).values]  if False else p_all

pM1_all=fit_score_M1(); pos={ix:i for i,ix in enumerate(f.index)}; te_pos=[pos[ix] for ix in te.index]
M1=pM1_all[te_pos]
pM4,_=fit_eval('M4'); pM5,_=fit_eval('M5')

# ---- VALIDATE against frozen ----
prim=pd.read_csv(PRIM,parse_dates=['week_start']); hyb=pd.read_csv(HYB,parse_dates=['week_start'])
key=['geometry_id','week_start']; tv=te[key].copy()
tv['M1n']=M1; tv['M4n']=pM4; tv['M5n']=pM5
mg=tv.merge(prim[key+['p_M1_lagged_AR']],on=key).merge(hyb[key+['p_M4_hybrid','p_M5_hybrid_season_RDHS']],on=key)
d1=np.abs(mg['M1n']-mg['p_M1_lagged_AR']).max(); d4=np.abs(mg['M4n']-mg['p_M4_hybrid']).max(); d5=np.abs(mg['M5n']-mg['p_M5_hybrid_season_RDHS']).max()
print(f"VALIDATION max|Δ|: M1={d1:.2e} M4={d4:.2e} M5={d5:.2e}  (n_test={len(mg)})")
if not (d1<1e-6 and d4<1e-6 and d5<1e-6):
    print("*** RECONSTRUCTION DID NOT REPRODUCE FROZEN PREDICTIONS — NOT REPORTING ***"); sys.exit(1)
print("RECONSTRUCTION VALIDATED (<1e-6). Proceeding.\n")

def nb(y,p,t=0.30): a=p>=t;n=len(y);return (a&(y==1)).sum()/n-(a&(y==0)).sum()/n*(t/(1-t))
def cal_is(y,p):
    lp=logit(p); r=sm.GLM(y,sm.add_constant(lp),family=sm.families.Binomial()).fit()
    r0=sm.GLM(y,np.ones((len(y),1)),family=sm.families.Binomial(),offset=lp).fit(); return float(r0.params[0]),float(r.params[1])

# ---- (A) SL matched decomposition ----
pcases,_=fit_eval('cases'); pmatch,_=fit_eval('matched')
rd_ids=sorted(te['geometry_id'].unique()); groups={g:np.where(te['geometry_id'].values==g)[0] for g in rd_ids}; rng=np.random.default_rng(SEED)
def bootci(pa,pb,B=1000):
    D=[]
    for _ in range(B):
        idx=np.concatenate([groups[rd_ids[i]] for i in rng.integers(0,len(rd_ids),len(rd_ids))]); yy=yte[idx]
        if yy.min()==yy.max(): continue
        D.append(nb(yy,pa[idx])-nb(yy,pb[idx]))
    return [round(float(np.percentile(D,2.5)),5),round(float(np.percentile(D,97.5)),5)]
NBv={'cases':nb(yte,pcases),'matched':nb(yte,pmatch),'M4':nb(yte,pM4),'M5':nb(yte,pM5),'M1_frozen':nb(yte,M1)}
decomp={'NB':{k:round(v,5) for k,v in NBv.items()},
 'M5_minus_matched(climate)':{'point':round(nb(yte,pM5)-nb(yte,pmatch),5),'ci':bootci(pM5,pmatch)},
 'matched_minus_cases(structure)':{'point':round(nb(yte,pmatch)-nb(yte,pcases),5),'ci':bootci(pmatch,pcases)},
 'M4_minus_cases':{'point':round(nb(yte,pM4)-nb(yte,pcases),5),'ci':bootci(pM4,pcases)},
 'M5_minus_cases(compound)':{'point':round(nb(yte,pM5)-nb(yte,pcases),5),'ci':bootci(pM5,pcases)},
 'M5_minus_M1frozen':{'point':round(nb(yte,pM5)-nb(yte,M1),5),'ci':bootci(pM5,M1)}}
print("=== (A) SL MATCHED DECOMPOSITION (NB@0.30, RDHS cluster bootstrap) ===")
print("  NB:",decomp['NB'])
for k in ['M5_minus_matched(climate)','matched_minus_cases(structure)','M4_minus_cases','M5_minus_cases(compound)','M5_minus_M1frozen']:
    print(f"  {k}: {decomp[k]['point']:+.4f} CI {decomp[k]['ci']}")

# ---- (B) past-only rolling-52 recalibration (intercept-only + intercept-slope) applied to M1/M4/M5 ----
f2=f.copy(); f2['p_M1']=pM1_all; f2['p_M4']=fit_eval.__wrapped__ if False else None
# need full-series M4/M5 predictions for recal eligibility; recompute on all rows
_,pM4_all=fit_eval('M4'); _,pM5_all=fit_eval('M5'); f2['p_M4']=pM4_all; f2['p_M5']=pM5_all
def recal_intercept(z_e,y_e):
    if y_e.sum()>=1 and (len(y_e)-y_e.sum())>=1 and len(y_e)>=20:
        try:
            r=sm.GLM(y_e,np.ones((len(y_e),1)),family=sm.families.Binomial(),offset=z_e).fit(); a=float(r.params[0])
            if abs(a)<=15 and np.isfinite(a): return lambda z: sig(z+a)
        except Exception: pass
    return lambda z: sig(z)
test_weeks=sorted(f2[f2.split=='test'].week_start.unique()); WIN=52
recal={m:np.full(len(f2),np.nan) for m in ['p_M1','p_M4','p_M5']}
for t in test_weeks:
    rows_t=f2.index[(f2.split=='test')&(f2.week_start==t)]
    elig=f2[(f2.target_week<t)&(f2.target_week>=t-pd.Timedelta(days=7*WIN))]
    for mdl in ['p_M1','p_M4','p_M5']:
        fn=recal_intercept(logit(elig[mdl].values),elig['y'].values)
        recal[mdl][[pos[ix] for ix in rows_t]]=clip(fn(logit(f2.loc[rows_t,mdl].values)))
rM1=recal['p_M1'][te_pos]; rM4=recal['p_M4'][te_pos]; rM5=recal['p_M5'][te_pos]
recalres={}
for nm,raw,rec in [('M1',M1,rM1),('M4',pM4,rM4),('M5',pM5,rM5)]:
    ci_r,cs_r=cal_is(yte,rec)
    recalres[nm]={'raw_NB30':round(nb(yte,raw),5),'recal_NB30':round(nb(yte,rec),5),
                  'recal_CITL':round(ci_r,4),'recal_slope':round(cs_r,4),'recal_Brier':round(brier_score_loss(yte,rec),4)}
recalres['dNB_M4_M1_raw']=round(nb(yte,pM4)-nb(yte,M1),5); recalres['dNB_M4_M1_recal']=round(nb(yte,rM4)-nb(yte,rM1),5)
recalres['dNB_M5_M1_raw']=round(nb(yte,pM5)-nb(yte,M1),5); recalres['dNB_M5_M1_recal']=round(nb(yte,rM5)-nb(yte,rM1),5)
recalres['dNB_M4_M1_recal_ci']=bootci(rM4,rM1); recalres['dNB_M5_M1_recal_ci']=bootci(rM5,rM1)
print("\n=== (B) PAST-ONLY ROLLING-52 RECALIBRATION (SL M1/M4/M5) ===")
for nm in ['M1','M4','M5']: print(f"  {nm}: raw NB {recalres[nm]['raw_NB30']} -> recal NB {recalres[nm]['recal_NB30']} (CITL {recalres[nm]['recal_CITL']}, slope {recalres[nm]['recal_slope']})")
print(f"  dNB(M4-M1): raw {recalres['dNB_M4_M1_raw']:+.4f} -> past-only recal {recalres['dNB_M4_M1_recal']:+.4f} CI {recalres['dNB_M4_M1_recal_ci']}")
print(f"  dNB(M5-M1): raw {recalres['dNB_M5_M1_raw']:+.4f} -> past-only recal {recalres['dNB_M5_M1_recal']:+.4f} CI {recalres['dNB_M5_M1_recal_ci']}")
json.dump({'validation':{'M1':d1,'M4':d4,'M5':d5},'A_matched_decomp':decomp,'B_pastonly_recal':recalres},
          open(RUN+"sl_matched_recal_results.json","w"),indent=2,default=float)
print("\nDONE")
