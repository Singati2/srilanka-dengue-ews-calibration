#!/usr/bin/env python3
"""ALT_STATS Step 0.1/0.2 — regenerate + reproduce-gate + FREEZE the matched-pair
per-observation predictions for both settings. Pipelines copied VERBATIM from the frozen
V6 code (SL: sl_matched_and_recal.py; Colombia: co_devincl_full_refit.py). No V6 artifact
is modified. Writes frozen per-obs CSVs + records SHA-256. Reproduce-gates:
  SL: reconstructed M1/M4/M5 must match committed frozen preds to <1e-6.
  Colombia: matched point dNB(M5-M5noclim)@0.30 must reproduce +0.00786 to <1e-3, and
            regenerated M5_recal must match committed frozen M5_recal to <1e-6.
Outputs: ALT_STATS/frozen/{srilanka,colombia}_matched_pairs.csv
"""
import pandas as pd, numpy as np, json, hashlib, os, sys, time
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, log_loss
import warnings; warnings.filterwarnings('ignore')
ROOT="/home/mpcrlab/srilanka-dengue-ews-calibration/ALT_STATS"
FROZEN=f"{ROOT}/frozen"; os.makedirs(FROZEN,exist_ok=True)
def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as fh:
        for b in iter(lambda: fh.read(1<<20), b''): h.update(b)
    return h.hexdigest()
log=[]
def L(m): print(m,flush=True); log.append(m)

# ============================ COLOMBIA (verbatim from co_devincl_full_refit.py) ==========
L("=== COLOMBIA: regenerate matched pair (verbatim co_devincl pipeline) ===")
LF='/home/mpcrlab/data_quarantine/colombia_label_features_v1'
SRC=f'{LF}/colombia_modeling_table_h4_75pct_v1.csv'
PSTAR=0.30; CGRID=[0.001,0.003,0.01,0.03,0.1,0.3,1,3,10]
d=pd.read_csv(SRC,dtype={'week_start':str}); d['dept']=d.GID_2.str.split('.').str[1]
PRE=[f'precip_lag{k}' for k in range(9)]; TMP=[f'temp_lag{k}' for k in range(9)]
CAS=['cases_lag0','cases_lag1','cases_lag2','cases_lag4']; SEA=['sin_woy_1','cos_woy_1','sin_woy_2','cos_woy_2']
def design(df,feats,scaler=None,dept_cats=None):
    X=pd.DataFrame(index=df.index); cont=[]
    if 'cases' in feats:
        for c in CAS: X[c]=np.log1p(df[c]); cont.append(c)
    if 'climate' in feats:
        for c in PRE: X[c]=np.log1p(df[c]); cont.append(c)
        for c in TMP: X[c]=df[c]; cont.append(c)
    if 'season' in feats:
        for c in SEA: X[c]=df[c]
    if scaler is None: scaler={c:(X[c].mean(),X[c].std(ddof=0) or 1.0) for c in cont}
    for c in cont: mn,s=scaler[c]; X[c]=(X[c]-mn)/(s if s else 1.0)
    if 'dept' in feats:
        if dept_cats is None: dept_cats=sorted(df['dept'].unique())
        for dc in dept_cats: X[f'dept_{dc}']=(df['dept']==dc).astype(float)
    return X,scaler,dept_cats
MODELS={'M5':['cases','climate','season','dept'],'M5_no_climate_matched':['cases','season','dept']}
def logit(p): p=np.clip(p,1e-6,1-1e-6); return np.log(p/(1-p))
def platt(p_va,y_va):
    lr=LogisticRegression(C=1e6,solver='lbfgs',max_iter=1000); lr.fit(logit(p_va).reshape(-1,1),y_va); return lr
def apply_platt(lr,p): return lr.predict_proba(logit(p).reshape(-1,1))[:,1]
def fit_eval(tr,va,te,feats,dept_cats):
    Xtr,sc,_=design(tr,feats,None,dept_cats); Xva,_,_=design(va,feats,sc,dept_cats); Xte,_,_=design(te,feats,sc,dept_cats)
    ytr=tr.label_h4.values; yva=va.label_h4.values; best=None
    for C in CGRID:
        m=LogisticRegression(C=C,penalty='l2',solver='lbfgs',max_iter=5000).fit(Xtr,ytr)
        p=np.clip(m.predict_proba(Xva)[:,1],1e-6,1-1e-6); ll=log_loss(yva,p,labels=[0,1])
        if best is None or ll<best[0]: best=(ll,C,m)
    _,C,m=best
    praw_te=np.clip(m.predict_proba(Xte)[:,1],1e-6,1-1e-6)
    praw_va=np.clip(m.predict_proba(Xva)[:,1],1e-6,1-1e-6)
    prec_te=apply_platt(platt(praw_va,yva),praw_te)
    return praw_te, prec_te
DEPT_CATS=sorted(d[d.common_complete_M1_to_M5_h4==True].query("split=='train'")['dept'].unique())
prim=d[d.common_complete_M1_to_M5_h4==True].copy()
tr0=prim[prim.split=='train']; va0=prim[prim.split=='val']; te0=prim[prim.split=='test'].copy()
raw5,rec5=fit_eval(tr0,va0,te0,MODELS['M5'],DEPT_CATS)
rawN,recN=fit_eval(tr0,va0,te0,MODELS['M5_no_climate_matched'],DEPT_CATS)
def nb(y,p,t=PSTAR):
    a=p>=t;n=len(y);return (a&(y==1)).sum()/n-(a&(y==0)).sum()/n*(t/(1-t))
y=te0.label_h4.values.astype(int)
gate_pt=nb(y,rec5)-nb(y,recN)
L(f"COLOMBIA reproduce-gate: matched dNB(recal)@0.30 = {gate_pt:+.5f} (target +0.00786)  -> {'PASS' if abs(gate_pt-0.00786)<1e-3 else 'FAIL'}")
# fidelity cross-check: regenerated M5_recal vs committed frozen M5_recal
FR="/home/mpcrlab/data_quarantine/colombia_model_pilots/model_ladder_h4_75pct_v1/colombia_model_predictions_h4_75pct_v1.csv"
fr=pd.read_csv(FR,dtype={'week_start':str})
mg=te0[['GID_2','week_start']].copy(); mg['rec5']=rec5
mg=mg.merge(fr[['GID_2','week_start','M5_recal']],on=['GID_2','week_start'],how='left')
d5=float(np.nanmax(np.abs(mg['rec5']-mg['M5_recal'])))
L(f"COLOMBIA fidelity: max|regen M5_recal - frozen M5_recal| = {d5:.2e}  (n={mg['M5_recal'].notna().sum()})")
co=pd.DataFrame({'setting':'Colombia','spatial_unit_id':te0['GID_2'].values,'department_id':te0['dept'].values,
    'predictor_week':te0['week_start'].values,'target_week':'', 'outcome':y,
    'full_raw':raw5,'noclim_raw':rawN,'full_recal':rec5,'noclim_recal':recN})
co.to_csv(f"{FROZEN}/colombia_matched_pairs.csv",index=False)
if abs(gate_pt-0.00786)>=1e-3 or d5>=1e-6:
    L("*** COLOMBIA GATE/FIDELITY FAILED — see STOP conditions ***")
L(f"COLOMBIA frozen: {len(co)} rows, prevalence {y.mean():.4f}, {te0['dept'].nunique()} depts, {te0['GID_2'].nunique()} munis")

# ============================ SRI LANKA (verbatim from sl_matched_and_recal.py) ==========
L("\n=== SRI LANKA: regenerate matched pair (verbatim sl pipeline) ===")
from patsy import dmatrix, build_design_matrices
import statsmodels.api as sm
V2="/home/mpcrlab/data_quarantine/analysis_tables/dengue_climate_population_linked_2018_2025_v2_date_aligned.csv"
PRIM="/home/mpcrlab/data_quarantine/model_pilots/pilot_h4_75pct_v1/predictions_h4_75pct_v1.csv"
HYB="/home/mpcrlab/data_quarantine/model_pilots/hybrid_model_extension_v1/hybrid_model_predictions_v1.csv"
CLIMVARS=['t2m_mean_c','precip_sum_mm','rh_mean_percent']; LAGS=list(range(0,9)); SEED=20260612; CGRID2=[0.1,1.0,10.0]
EPS=1e-6; clip=lambda p:np.clip(p,EPS,1-EPS); lg=lambda p:np.log(clip(p)/(1-clip(p))); sig=lambda z:1/(1+np.exp(-z))
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
for Lg in [1,2,4]:
    t=f[['geometry_id','week_start','dengue_incidence_per_100k']].rename(columns={'dengue_incidence_per_100k':f'inc_lag{Lg}'}).copy()
    t['week_start']=t['week_start']+pd.Timedelta(days=7*Lg); f=f.merge(t,on=['geometry_id','week_start'],how='left')
f['inc_t']=f['dengue_incidence_per_100k']
for v in CLIMVARS:
    for Lg in LAGS:
        t=f[['geometry_id','week_start',v]].rename(columns={v:f'{v}__L{Lg}'}).copy()
        t['week_start']=t['week_start']+pd.Timedelta(days=7*Lg); f=f.merge(t,on=['geometry_id','week_start'],how='left')
w=2*np.pi*f['epi_week']/52.18
f['sin1'],f['cos1'],f['sin2'],f['cos2']=np.sin(w),np.cos(w),np.sin(2*w),np.cos(2*w)
rd=pd.get_dummies(f['geometry_id'],prefix='rd',drop_first=True).astype(float); f=pd.concat([f,rd],axis=1); RD=list(rd.columns)
tr0s=f[f.split=='train']
for c in ['inc_lag1','inc_lag2','inc_lag4']+[f'{v}__L{Lg}' for v in CLIMVARS for Lg in LAGS]:
    f[c]=f[c].fillna(tr0s[c].mean())
f['target_week']=f['week_start']+pd.Timedelta(days=28)
tr=f[f.split=='train'].copy(); te=f[f.split=='test'].copy(); ytr=tr['y'].values; yte=te['y'].values
AR=['inc_t','inc_lag1','inc_lag2','inc_lag4']; VDF=LDF=3
DIs={v:dmatrix(f"cr(x, df={VDF}) - 1",{"x":tr[f'{v}__L0'].values},return_type='dataframe').design_info for v in CLIMVARS}
BLAG=np.asarray(dmatrix(f"cr(x, df={LDF}) - 1",{"x":np.array(LAGS,float)},return_type='dataframe'))
def crossbasis(rows,v):
    n=len(rows); Vb=np.empty((n,len(LAGS),VDF))
    for i,Lg in enumerate(LAGS): Vb[:,i,:]=np.asarray(build_design_matrices([DIs[v]],{"x":rows[f'{v}__L{Lg}'].values})[0])
    return np.einsum('nlj,lk->njk',Vb,BLAG).reshape(n,VDF*LDF)
def climate_block(rows): return np.concatenate([crossbasis(rows,v) for v in CLIMVARS],axis=1)
def designS(rows,kind):
    cb=climate_block(rows) if kind in ('M4','M5') else None
    if kind=='matched': return np.concatenate([rows[AR].values, rows[['sin1','cos1','sin2','cos2']+RD].values],axis=1)
    if kind=='M4':      return np.concatenate([rows[AR].values, cb],axis=1)
    if kind=='M5':      return np.concatenate([rows[AR].values, cb, rows[['sin1','cos1','sin2','cos2']+RD].values],axis=1)
def time_blocks(rows):
    yrs=sorted(rows['epi_year'].unique()); folds=[]
    for i in range(1,len(yrs)):
        tri=rows.index[rows['epi_year']<=yrs[i-1]]; vai=rows.index[rows['epi_year']==yrs[i]]
        if len(vai)>0 and rows.loc[tri,'y'].nunique()>1 and rows.loc[vai,'y'].nunique()>1: folds.append((tri,vai))
    return folds
def fit_evalS(kind):
    Xtr_full=designS(tr,kind); Xte=designS(te,kind); mu=Xtr_full.mean(0); sd=Xtr_full.std(0); sd[sd==0]=1
    folds=time_blocks(tr); bestC,bestS=None,-1
    for C in CGRID2:
        sc=[]
        for tri,vai in folds:
            Xt=(designS(tr.loc[tri],kind)-mu)/sd; Xv=(designS(tr.loc[vai],kind)-mu)/sd
            clf=LogisticRegression(penalty='l2',C=C,solver='lbfgs',max_iter=8000).fit(Xt,tr.loc[tri,'y'].values)
            sc.append(roc_auc_score(tr.loc[vai,'y'].values,clf.predict_proba(Xv)[:,1]))
        ms=float(np.mean(sc))
        if ms>bestS: bestS,bestC=ms,C
    Xtr=(Xtr_full-mu)/sd; Xtes=(Xte-mu)/sd
    clf=LogisticRegression(penalty='l2',C=bestC,solver='lbfgs',max_iter=8000).fit(Xtr,ytr)
    if np.abs(clf.coef_).max()>15: clf=LogisticRegression(penalty='l2',C=0.1,solver='lbfgs',max_iter=8000).fit(Xtr,ytr)
    return clip(clf.predict_proba(Xtes)[:,1]), clip(clf.predict_proba((designS(f,kind)-mu)/sd)[:,1])
def fit_score_M1():
    cont=AR; mu=tr[cont].mean(); sd=tr[cont].std(ddof=0).replace(0,1)
    Xtr=np.concatenate([((tr[cont]-mu)/sd).values, tr[['sin1','cos1','sin2','cos2']+RD].values],axis=1)
    Xall=np.concatenate([((f[cont]-mu)/sd).values, f[['sin1','cos1','sin2','cos2']+RD].values],axis=1)
    clf=LogisticRegression(penalty='l2',C=1e6,solver='lbfgs',max_iter=5000).fit(Xtr,ytr)
    return clip(clf.predict_proba(Xall)[:,1])
pM1_all=fit_score_M1(); pos={ix:i for i,ix in enumerate(f.index)}; te_pos=[pos[ix] for ix in te.index]
M1=pM1_all[te_pos]
pM4,pM4_all=fit_evalS('M4'); pM5,pM5_all=fit_evalS('M5')
pmatch,pmatch_all=fit_evalS('matched')
# reproduce-gate: validate M1/M4/M5 vs committed frozen
prim=pd.read_csv(PRIM,parse_dates=['week_start']); hyb=pd.read_csv(HYB,parse_dates=['week_start'])
key=['geometry_id','week_start']; tv=te[key].copy(); tv['M1n']=M1; tv['M4n']=pM4; tv['M5n']=pM5
mg2=tv.merge(prim[key+['p_M1_lagged_AR']],on=key).merge(hyb[key+['p_M4_hybrid','p_M5_hybrid_season_RDHS']],on=key)
d1=float(np.abs(mg2['M1n']-mg2['p_M1_lagged_AR']).max()); d4=float(np.abs(mg2['M4n']-mg2['p_M4_hybrid']).max()); d5s=float(np.abs(mg2['M5n']-mg2['p_M5_hybrid_season_RDHS']).max())
L(f"SRI LANKA reproduce-gate max|Δ|: M1={d1:.2e} M4={d4:.2e} M5={d5s:.2e}  -> {'PASS' if max(d1,d4,d5s)<1e-6 else 'FAIL'}")
# past-only rolling-52 recalibration applied to full(M5) and matched(no-climate)
def recal_intercept(z_e,y_e):
    if y_e.sum()>=1 and (len(y_e)-y_e.sum())>=1 and len(y_e)>=20:
        try:
            r=sm.GLM(y_e,np.ones((len(y_e),1)),family=sm.families.Binomial(),offset=z_e).fit(); a=float(r.params[0])
            if abs(a)<=15 and np.isfinite(a): return lambda z: sig(z+a)
        except Exception: pass
    return lambda z: sig(z)
f2=f.copy(); f2['p_full']=pM5_all; f2['p_noclim']=pmatch_all
test_weeks=sorted(f2[f2.split=='test'].week_start.unique()); WIN=52
recal={mm:np.full(len(f2),np.nan) for mm in ['p_full','p_noclim']}
for t in test_weeks:
    rows_t=f2.index[(f2.split=='test')&(f2.week_start==t)]
    elig=f2[(f2.target_week<t)&(f2.target_week>=t-pd.Timedelta(days=7*WIN))]
    for mdl in ['p_full','p_noclim']:
        fn=recal_intercept(lg(elig[mdl].values),elig['y'].values)
        recal[mdl][[pos[ix] for ix in rows_t]]=clip(fn(lg(f2.loc[rows_t,mdl].values)))
rFull=recal['p_full'][te_pos]; rNo=recal['p_noclim'][te_pos]
# matched climate point (recal) reproduce check vs manuscript +0.0157
mp=nb(yte,rFull)-nb(yte,rNo)
L(f"SRI LANKA matched climate dNB(recal)@0.30 = {mp:+.5f} (manuscript +0.0157)")
sl=pd.DataFrame({'setting':'SriLanka','spatial_unit_id':te['geometry_id'].values,'department_id':'',
    'predictor_week':te['week_start'].values.astype('datetime64[D]').astype(str),
    'target_week':te['target_week'].values.astype('datetime64[D]').astype(str),'outcome':yte,
    'full_raw':pM5,'noclim_raw':pmatch,'full_recal':rFull,'noclim_recal':rNo})
sl.to_csv(f"{FROZEN}/srilanka_matched_pairs.csv",index=False)
L(f"SRI LANKA frozen: {len(sl)} rows, prevalence {yte.mean():.4f}, {te['geometry_id'].nunique()} RDHS units")
if max(d1,d4,d5s)>=1e-6: L("*** SRI LANKA GATE FAILED ***")

# ============================ checksums ============================
inputs={"colombia_matched_pairs.csv":f"{FROZEN}/colombia_matched_pairs.csv",
        "srilanka_matched_pairs.csv":f"{FROZEN}/srilanka_matched_pairs.csv"}
with open(f"{FROZEN}/../FROZEN_INPUTS.sha256","w") as fh:
    for name,p in inputs.items(): fh.write(f"{sha256(p)}  {name}\n")
gates={"colombia_gate_point":gate_pt,"colombia_fidelity_M5recal":d5,
       "srilanka_gate_M1":d1,"srilanka_gate_M4":d4,"srilanka_gate_M5":d5s,
       "srilanka_matched_recal_dNB":mp,"colombia_prevalence":float(y.mean()),"srilanka_prevalence":float(yte.mean())}
json.dump(gates,open(f"{FROZEN}/../logs/freeze_gates.json","w"),indent=2,default=float)
open(f"{FROZEN}/../logs/freeze_log.txt","w").write("\n".join(log))
L("\nFREEZE COMPLETE. Checksums -> FROZEN_INPUTS.sha256")
