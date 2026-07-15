#!/usr/bin/env python3
"""GEO_FIXED_PARTIAL_REFIT diagnostic (Colombia matched climate increment).

Verdict spec: "Freeze ONLY the geographic (department) coefficients and refit ALL remaining terms in
both models." This isolates whether the development-inclusive interval's width is inflated by ill-posed
re-estimation of the 32 department fixed effects when ~1/3 of the 31 departments drop out of a resample.

Method: a custom L2-penalized logistic solver (validated to reproduce sklearn's matched increment) with
OFFSET support (sklearn lacks offsets). Department coefficients are frozen at their full-train values and
enter as a fixed offset; cases+climate+season coefficients (and the intercept, Platt) are refit on each
department resample. Per replicate we compute BOTH:
  (a) FREE-dept increment  (dept refit as free columns)  -> internal control; should match the full-refit width
  (b) FROZEN-dept increment (dept frozen via offset)      -> the diagnostic
Fixed penalty C (full-train-selected) is used for both so the ONLY difference is dept freezing.
Same department resamples / seed (20260612) as co_devincl_full_refit.py. Reproduce-gate on the point estimate.
Read-only inputs; writes only under this dir.
"""
import pandas as pd, numpy as np, json, os, time, warnings
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import log_loss
from scipy.optimize import minimize
warnings.filterwarnings('ignore'); np.random.seed(20260612)
LF='/home/mpcrlab/data_quarantine/colombia_label_features_v1'
OUT=os.path.dirname(os.path.abspath(__file__)); os.makedirs(OUT,exist_ok=True)
SRC=f'{LF}/colombia_modeling_table_h4_75pct_v1.csv'
PSTAR=0.30; CGRID=[0.001,0.003,0.01,0.03,0.1,0.3,1,3,10]; SEED=20260612; B=1000
d=pd.read_csv(SRC,dtype={'week_start':str}); d['dept']=d.GID_2.str.split('.').str[1]
PRE=[f'precip_lag{k}' for k in range(9)]; TMP=[f'temp_lag{k}' for k in range(9)]
CAS=['cases_lag0','cases_lag1','cases_lag2','cases_lag4']; SEA=['sin_woy_1','cos_woy_1','sin_woy_2','cos_woy_2']

def design(df, feats, scaler=None, dept_cats=None):
    """Same feature construction as path_b; returns X, scaler, dept_cats, and list of dept column names."""
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
    dept_cols=[]
    if 'dept' in feats:
        if dept_cats is None: dept_cats=sorted(df['dept'].unique())
        for dc in dept_cats: X[f'dept_{dc}']=(df['dept']==dc).astype(float); dept_cols.append(f'dept_{dc}')
    return X, scaler, dept_cats, dept_cols

def solve(X,y,C,offset=None,init=None):
    """L2 logistic matching sklearn objective: C*sum softplus(-yt*(Xw+b+o)) + 0.5||w||^2 (b unpenalized)."""
    X=np.asarray(X,float); n,k=X.shape; o=np.zeros(n) if offset is None else offset
    y=np.asarray(y,float); yt=2*y-1
    def f(th):
        w=th[:k]; b=th[k]; z=X@w+b+o
        loss=np.sum(np.logaddexp(0,-yt*z)); pr=1/(1+np.exp(-z)); g=pr-y
        return C*loss+0.5*np.sum(w*w), np.concatenate([C*(X.T@g)+w,[C*np.sum(g)]])
    th0=np.zeros(k+1) if init is None else init
    r=minimize(f,th0,jac=True,method='L-BFGS-B',options={'maxiter':100000,'maxfun':100000,'ftol':1e-15,'gtol':1e-9,'maxcor':50})
    return r.x[:k], r.x[k]
def logit(p): p=np.clip(p,1e-6,1-1e-6); return np.log(p/(1-p))
def platt(pva,yva): return LogisticRegression(C=1e6,solver='lbfgs',max_iter=1000).fit(logit(pva).reshape(-1,1),yva)
def apply_platt(lr,p): return lr.predict_proba(logit(p).reshape(-1,1))[:,1]
def nb(y,p,t=PSTAR): a=p>=t; n=len(y); return (a&(y==1)).sum()/n-(a&(y==0)).sum()/n*(t/(1-t))

prim=d[d.common_complete_M1_to_M5_h4==True].copy()
tr0=prim[prim.split=='train']; va0=prim[prim.split=='val']; te0=prim[prim.split=='test']
yte0=te0.label_h4.values.astype(float)
DEPT_CATS=sorted(tr0['dept'].unique())            # fixed 32-department column set
FEATS_FULL=['cases','climate','season','dept']; FEATS_MA=['cases','season','dept']
FEATS_FULL_ND=['cases','climate','season']; FEATS_MA_ND=['cases','season']   # non-dept versions

# ---------- full-train fit (custom solver): select C, extract frozen dept betas ----------
def fulltrain_fit(feats):
    Xtr,sc,dc,dcol=design(tr0,feats,None,DEPT_CATS); Xva,_,_,_=design(va0,feats,sc,dc)
    ytr=tr0.label_h4.values.astype(float); yva=va0.label_h4.values.astype(float)
    best=None
    for C in CGRID:
        w,b=solve(Xtr.values,ytr,C)
        pv=np.clip(1/(1+np.exp(-(Xva.values@w+b))),1e-6,1-1e-6); ll=log_loss(yva,pv,labels=[0,1])
        if best is None or ll<best[0]: best=(ll,C,w,b,list(Xtr.columns),sc)
    ll,C,w,b,cols,sc=best
    beta_dept={c.replace('dept_',''):w[cols.index(c)] for c in cols if c.startswith('dept_')}
    return C,beta_dept
t0=time.time()
C_M5,bdept_M5=fulltrain_fit(FEATS_FULL); C_MA,bdept_MA=fulltrain_fit(FEATS_MA)
print(f"full-train selected C: M5={C_M5} matched={C_MA}  [{time.time()-t0:.0f}s]",flush=True)

def fit_free(tr,va,te,feats,C):
    Xtr,sc,dc,_=design(tr,feats,None,DEPT_CATS); Xva,_,_,_=design(va,feats,sc,dc); Xte,_,_,_=design(te,feats,sc,dc)
    w,b=solve(Xtr.values,tr.label_h4.values.astype(float),C)
    pv=np.clip(1/(1+np.exp(-(Xva.values@w+b))),1e-6,1-1e-6); pt=np.clip(1/(1+np.exp(-(Xte.values@w+b))),1e-6,1-1e-6)
    return apply_platt(platt(pv,va.label_h4.values.astype(float)),pt)
def fit_frozen(tr,va,te,feats_nd,beta_dept,C):
    """Refit non-dept terms with department contribution held fixed as an offset."""
    Xtr,sc,_,_=design(tr,feats_nd,None,None); Xva,_,_,_=design(va,feats_nd,sc,None); Xte,_,_,_=design(te,feats_nd,sc,None)
    otr=tr['dept'].map(beta_dept).fillna(0.0).values; ova=va['dept'].map(beta_dept).fillna(0.0).values; ote=te['dept'].map(beta_dept).fillna(0.0).values
    w,b=solve(Xtr.values,tr.label_h4.values.astype(float),C,offset=otr)
    pv=np.clip(1/(1+np.exp(-(Xva.values@w+b+ova))),1e-6,1-1e-6); pt=np.clip(1/(1+np.exp(-(Xte.values@w+b+ote))),1e-6,1-1e-6)
    return apply_platt(platt(pv,va.label_h4.values.astype(float)),pt)

# ---------- point estimate + reproduce gate (free-dept custom solver) ----------
p5=fit_free(tr0,va0,te0,FEATS_FULL,C_M5); pm=fit_free(tr0,va0,te0,FEATS_MA,C_MA)
pt_free=nb(yte0,p5)-nb(yte0,pm)
p5f=fit_frozen(tr0,va0,te0,FEATS_FULL_ND,bdept_M5,C_M5); pmf=fit_frozen(tr0,va0,te0,FEATS_MA_ND,bdept_MA,C_MA)
pt_frozen=nb(yte0,p5f)-nb(yte0,pmf)
gate = abs(pt_free-0.00786)<=0.0015
print(f"GATE: free-dept point={pt_free:+.5f} (target +0.00786, tol 0.0015) -> {'PASS' if gate else 'FAIL'} | frozen-dept point={pt_frozen:+.5f}  [{time.time()-t0:.0f}s]",flush=True)
if not gate: print("*** GATE FAILED ***"); raise SystemExit(1)

# ---------- bootstrap: same department resamples as full-refit script ----------
test_depts=sorted(te0['dept'].unique())
tr_by={g:tr0[tr0.dept==g] for g in DEPT_CATS}; va_by={g:va0[va0.dept==g] for g in DEPT_CATS}; te_by={g:te0[te0.dept==g] for g in test_depts}
rng=np.random.default_rng(SEED)
free_D=[]; frozen_D=[]; uniq=[]; fails=0
for b in range(B):
    pick=[test_depts[i] for i in rng.integers(0,len(test_depts),len(test_depts))]; uniq.append(len(set(pick)))
    rtr=pd.concat([tr_by[g] for g in pick if len(tr_by[g])]); rva=pd.concat([va_by[g] for g in pick if len(va_by[g])]); rte=pd.concat([te_by[g] for g in pick if len(te_by[g])])
    yb=rte.label_h4.values.astype(float)
    if len(np.unique(yb))<2 or len(np.unique(rva.label_h4.values))<2 or len(np.unique(rtr.label_h4.values))<2: fails+=1; continue
    try:
        a5=fit_free(rtr,rva,rte,FEATS_FULL,C_M5); am=fit_free(rtr,rva,rte,FEATS_MA,C_MA); free_D.append(nb(yb,a5)-nb(yb,am))
        f5=fit_frozen(rtr,rva,rte,FEATS_FULL_ND,bdept_M5,C_M5); fm=fit_frozen(rtr,rva,rte,FEATS_MA_ND,bdept_MA,C_MA); frozen_D.append(nb(yb,f5)-nb(yb,fm))
    except Exception: fails+=1; continue
    if (b+1)%50==0: print(f"  rep {b+1}/{B} free_med={np.median(free_D):+.4f} frozen_med={np.median(frozen_D):+.4f} used={len(free_D)} [{time.time()-t0:.0f}s]",flush=True)

free_D=np.array(free_D); frozen_D=np.array(frozen_D)
def ci(a): return [round(float(np.percentile(a,2.5)),5),round(float(np.percentile(a,97.5)),5)]
def width(a): c=ci(a); return round(c[1]-c[0],5)
res={"analysis":"colombia_GEO_FIXED_PARTIAL_REFIT_diagnostic","B":B,"seed":SEED,
     "replicates_used":int(len(free_D)),"failures":int(fails),"fixed_C":{"M5":C_M5,"matched":C_MA},
     "reproduce_gate":{"free_point":round(float(pt_free),5),"target":0.00786,"passed":bool(gate)},
     "free_refit_dept":{"point":round(float(pt_free),5),"ci":ci(free_D),"width":width(free_D),"median":round(float(np.median(free_D)),5)},
     "frozen_dept_partial_refit":{"point":round(float(pt_frozen),5),"ci":ci(frozen_D),"width":width(frozen_D),"median":round(float(np.median(frozen_D)),5)},
     "width_reduction_frozen_vs_free":round(float(width(free_D)-width(frozen_D)),5),
     "width_ratio_frozen_over_free":round(float(width(frozen_D)/width(free_D)),3) if width(free_D)>0 else None,
     "dept_dropout":{"mean_unique_depts_per_resample":round(float(np.mean(uniq)),2),"min":int(np.min(uniq)),"max":int(np.max(uniq)),"total_test_depts":len(test_depts)},
     "seconds":round(time.time()-t0,1)}
json.dump(res,open(f'{OUT}/co_geo_partial_refit_results.json','w'),indent=2)
pd.DataFrame({"free":free_D,"frozen":frozen_D}).to_csv(f'{OUT}/co_geo_partial_refit_distribution.csv',index=False)
print("\n=== GEO_FIXED_PARTIAL_REFIT diagnostic ===")
print(f"  FREE-dept   (dept refit) : point {pt_free:+.5f}  95% CI [{res['free_refit_dept']['ci'][0]:+.4f}, {res['free_refit_dept']['ci'][1]:+.4f}]  width {res['free_refit_dept']['width']:.4f}")
print(f"  FROZEN-dept (dept frozen): point {pt_frozen:+.5f}  95% CI [{res['frozen_dept_partial_refit']['ci'][0]:+.4f}, {res['frozen_dept_partial_refit']['ci'][1]:+.4f}]  width {res['frozen_dept_partial_refit']['width']:.4f}")
print(f"  width ratio frozen/free = {res['width_ratio_frozen_over_free']}  (small ratio => full width is largely an ill-posed-FE-refit artifact)")
print(f"  mean unique depts/resample = {res['dept_dropout']['mean_unique_depts_per_resample']} of {len(test_depts)}")
print("DONE")
