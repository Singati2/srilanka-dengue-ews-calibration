#!/usr/bin/env python3
"""Colombia matched climate increment — REPRODUCIBLE development-inclusive department-refit bootstrap.

Motivation: the manuscript's Colombia development-inclusive interval [-0.0001, +0.0244] is NOT
reproducible from any repo code (external/original-submission number; repo's own review said "disclose").
This script reproduces a development-inclusive interval from scratch using the EXACT original Colombia
pipeline (design/fit_select/platt/nb copied verbatim from path_b_stage2_runner.py), refitting ALL
coefficients (cases + climate + season + 32 department fixed effects) within each of B department resamples.

Resampling unit = the 31 test departments (the fixed-effect unit), matching the manuscript's statement
that the development-inclusive bootstrap "resamples departments." A FIXED 32-department column set is used,
so a resample that omits departments leaves those dept_* columns all-zero (the ill-posed-FE-refit regime).

Reproduce-first gate: matched point estimate dNB(M5 - M5_no_climate)@0.30 must reproduce +0.00786 (frozen)
and dNB(M5-M1) must reproduce +0.018775, both within 0.001, before the bootstrap runs.
Read-only inputs; writes only under this dir. No manuscript touched.
"""
import pandas as pd, numpy as np, json, os, time, warnings
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, log_loss
warnings.filterwarnings('ignore'); np.random.seed(20260612)
LF='/home/mpcrlab/data_quarantine/colombia_label_features_v1'
OUT=os.path.dirname(os.path.abspath(__file__)); os.makedirs(OUT,exist_ok=True)
SRC=f'{LF}/colombia_modeling_table_h4_75pct_v1.csv'
PSTAR=0.30; CGRID=[0.001,0.003,0.01,0.03,0.1,0.3,1,3,10]; SEED=20260612; B=1000
d=pd.read_csv(SRC,dtype={'week_start':str}); d['dept']=d.GID_2.str.split('.').str[1]
PRE=[f'precip_lag{k}' for k in range(9)]; TMP=[f'temp_lag{k}' for k in range(9)]
CAS=['cases_lag0','cases_lag1','cases_lag2','cases_lag4']; SEA=['sin_woy_1','cos_woy_1','sin_woy_2','cos_woy_2']

def design(df, feats, scaler=None, dept_cats=None):      # verbatim from path_b_stage2_runner.py
    X=pd.DataFrame(index=df.index); cont=[]
    if 'cases' in feats:
        for c in CAS: X[c]=np.log1p(df[c]); cont.append(c)
    if 'climate' in feats:
        for c in PRE: X[c]=np.log1p(df[c]); cont.append(c)
        for c in TMP: X[c]=df[c]; cont.append(c)
    if 'season' in feats:
        for c in SEA: X[c]=df[c]
    if scaler is None: scaler={c:(X[c].mean(),X[c].std(ddof=0) or 1.0) for c in cont}
    for c in cont: m,s=scaler[c]; X[c]=(X[c]-m)/(s if s else 1.0)
    if 'dept' in feats:
        if dept_cats is None: dept_cats=sorted(df['dept'].unique())
        for dc in dept_cats: X[f'dept_{dc}']=(df['dept']==dc).astype(float)
    return X, scaler, dept_cats

MODELS={'M1':['cases'],'M5':['cases','climate','season','dept'],
        'M5_no_climate_matched':['cases','season','dept']}

def logit(p): p=np.clip(p,1e-6,1-1e-6); return np.log(p/(1-p))
def platt(p_va,y_va):
    lr=LogisticRegression(C=1e6,solver='lbfgs',max_iter=1000); lr.fit(logit(p_va).reshape(-1,1),y_va); return lr
def apply_platt(lr,p): return lr.predict_proba(logit(p).reshape(-1,1))[:,1]
def nb(y,p,t=PSTAR):
    pos=p>=t; n=len(y); tp=np.sum(pos&(y==1)); fp=np.sum(pos&(y==0)); return tp/n-(fp/n)*(t/(1-t))

# FIXED 32-department column set (from full train) so the refit column set is invariant across resamples
DEPT_CATS=sorted(d[d.common_complete_M1_to_M5_h4==True].query("split=='train'")['dept'].unique())

def fit_eval(tr,va,te,feats,dept_cats):
    """Fit with C selected by validation log-loss (path_b method), Platt on val, return recalibrated test preds."""
    Xtr,sc,_=design(tr,feats,None,dept_cats); Xva,_,_=design(va,feats,sc,dept_cats); Xte,_,_=design(te,feats,sc,dept_cats)
    ytr=tr.label_h4.values; yva=va.label_h4.values; best=None
    for C in CGRID:
        m=LogisticRegression(C=C,penalty='l2',solver='lbfgs',max_iter=5000).fit(Xtr,ytr)
        p=np.clip(m.predict_proba(Xva)[:,1],1e-6,1-1e-6); ll=log_loss(yva,p,labels=[0,1])
        if best is None or ll<best[0]: best=(ll,C,m)
    _,C,m=best
    praw_va=np.clip(m.predict_proba(Xva)[:,1],1e-6,1-1e-6)
    praw_te=np.clip(m.predict_proba(Xte)[:,1],1e-6,1-1e-6)
    prec_te=apply_platt(platt(praw_va,yva),praw_te)
    return prec_te, praw_te, C

prim=d[d.common_complete_M1_to_M5_h4==True].copy()
tr0=prim[prim.split=='train']; va0=prim[prim.split=='val']; te0=prim[prim.split=='test']
yte0=te0.label_h4.values

# ---------- POINT ESTIMATE + reproduce-first gate ----------
t0=time.time()
prec={}; praw={}
for name,feats in MODELS.items():
    prec[name],praw[name],_=fit_eval(tr0,va0,te0,feats,DEPT_CATS)
pt_matched=nb(yte0,prec['M5'])-nb(yte0,prec['M5_no_climate_matched'])
pt_m5m1=nb(yte0,prec['M5'])-nb(yte0,prec['M1'])
gateA = abs(pt_matched-0.00786)<=0.001 and abs(pt_m5m1-0.018775)<=0.001
print(f"GATE A: matched={pt_matched:+.5f} (target +0.00786)  M5-M1={pt_m5m1:+.5f} (target +0.018775)  -> {'PASS' if gateA else 'FAIL'}  [{time.time()-t0:.0f}s]",flush=True)
if not gateA:
    print("*** GATE A FAILED — aborting ***"); raise SystemExit(1)

# ---------- DEVELOPMENT-INCLUSIVE DEPARTMENT-REFIT BOOTSTRAP ----------
test_depts=sorted(te0['dept'].unique())            # 31 test departments = resampling unit
tr_by={g:tr0[tr0.dept==g] for g in DEPT_CATS}
va_by={g:va0[va0.dept==g] for g in DEPT_CATS}
te_by={g:te0[te0.dept==g] for g in test_depts}
rng=np.random.default_rng(SEED)
matched_D=[]; m5m1_D=[]; uniq_counts=[]; fails=0
for b in range(B):
    pick=[test_depts[i] for i in rng.integers(0,len(test_depts),len(test_depts))]
    uniq_counts.append(len(set(pick)))
    rtr=pd.concat([tr_by[g] for g in pick if len(tr_by[g])]) if any(len(tr_by[g]) for g in pick) else None
    rva=pd.concat([va_by[g] for g in pick if len(va_by[g])]) if any(len(va_by[g]) for g in pick) else None
    rte=pd.concat([te_by[g] for g in pick if len(te_by[g])])
    yb=rte.label_h4.values
    if rtr is None or rva is None or len(np.unique(yb))<2 or len(np.unique(rva.label_h4.values))<2 or len(np.unique(rtr.label_h4.values))<2:
        fails+=1; continue
    try:
        # matched increment only (M5 vs M5_no_climate) — both carry the 32 dept FE; this is the
        # quantity the external [-0.0001,+0.0244] constant refers to. M1 refit dropped for tractability.
        p_m5,_,_=fit_eval(rtr,rva,rte,MODELS['M5'],DEPT_CATS)
        p_ma,_,_=fit_eval(rtr,rva,rte,MODELS['M5_no_climate_matched'],DEPT_CATS)
        matched_D.append(nb(yb,p_m5)-nb(yb,p_ma))
    except Exception:
        fails+=1; continue
    if (b+1)%50==0:
        print(f"  rep {b+1}/{B}  matched median={np.median(matched_D):+.4f}  used={len(matched_D)}  meanUniqDept={np.mean(uniq_counts):.1f}  [{time.time()-t0:.0f}s]",flush=True)

matched_D=np.array(matched_D)
def ci(a): return [round(float(np.percentile(a,2.5)),5),round(float(np.percentile(a,97.5)),5)]
res={"analysis":"colombia_development_inclusive_department_refit_REPRODUCIBLE",
     "B":B,"replicates_used":int(len(matched_D)),"failures":int(fails),"seed":SEED,
     "resampling_unit":"department (31 test depts)","fixed_dept_columns":len(DEPT_CATS),
     "reproduce_gate":{"matched_point":round(float(pt_matched),5),"m5m1_point":round(float(pt_m5m1),5),
                       "matched_target":0.00786,"m5m1_target":0.018775,"passed":bool(gateA)},
     "point_estimates":{"matched":round(float(pt_matched),5),"m5m1":round(float(pt_m5m1),5)},
     "development_inclusive":{
         "matched":{"point":round(float(pt_matched),5),"ci":ci(matched_D),"median":round(float(np.median(matched_D)),5)}},
     "external_reported_matched_ci":[-0.0001,0.0244],
     "dept_dropout":{"mean_unique_depts_per_resample":round(float(np.mean(uniq_counts)),2),
                     "min":int(np.min(uniq_counts)),"max":int(np.max(uniq_counts)),"total_test_depts":len(test_depts)},
     "seconds":round(time.time()-t0,1)}
json.dump(res,open(f'{OUT}/co_devincl_full_refit_results.json','w'),indent=2)
pd.DataFrame({"matched":matched_D}).to_csv(f'{OUT}/co_devincl_full_refit_distribution.csv',index=False)
print("\n=== REPRODUCIBLE development-inclusive department-refit ===")
print(f"  matched dNB(M5-M5_noclim)@0.30 = {pt_matched:+.5f}  95% CI [{res['development_inclusive']['matched']['ci'][0]:+.4f}, {res['development_inclusive']['matched']['ci'][1]:+.4f}]")
print(f"  (external reported CI was [-0.0001, +0.0244])")
print(f"  mean unique depts / resample = {res['dept_dropout']['mean_unique_depts_per_resample']} of {len(test_depts)}  (dropout mechanism)")
print(f"  replicates_used={len(matched_D)} failures={fails}  {time.time()-t0:.0f}s")
print("DONE")
