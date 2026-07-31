#!/usr/bin/env python3
"""Colombia DEVELOPMENT-INCLUSIVE proper-score intervals (removes the evidentiary asymmetry:
proper scores were previously conditional-only while decision curves got the refit stress test).

Faithful derivative of colombia_matched_ablation_90pct_v1.py at the 75th-percentile PRIMARY label:
refit M5 and M5_no-climate (scaling, penalty, Platt recalibration) within each department resample,
recompute the paired dNLL and dBrier (full - no-climate, recalibrated state) per replicate, and report
development-inclusive percentile intervals. Reproduce-first gate: full-data point dNLL must match the
reported conditional -0.0089 (dBrier -0.0043) within tolerance. Read-only inputs; writes only under OUT.
"""
import os
os.environ.setdefault('OMP_NUM_THREADS','1'); os.environ.setdefault('OPENBLAS_NUM_THREADS','1'); os.environ.setdefault('MKL_NUM_THREADS','1')
import sys, numpy as np, pandas as pd, json, time, warnings
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import log_loss
from multiprocessing import Pool
warnings.filterwarnings('ignore')
LF='/home/mpcrlab/data_quarantine/colombia_label_features_v1'
OUT='/home/mpcrlab/srilanka-dengue-ews-calibration/analysis/devincl_proper_scores_v1'; os.makedirs(OUT,exist_ok=True)
SRC=f'{LF}/colombia_modeling_table_h4_75pct_v1.csv'
CGRID=[0.001,0.003,0.01,0.03,0.1,0.3,1,3,10]; SEED=20260612
B=int(sys.argv[1]) if len(sys.argv)>1 else 1000
NPROC=int(sys.argv[2]) if len(sys.argv)>2 else 7
EPS=1e-15; t0=time.time()
d=pd.read_csv(SRC,dtype={'week_start':str}); d['dept']=d.GID_2.str.split('.').str[1]
prim=d[d.common_complete_M1_to_M5_h4==True].copy().reset_index(drop=True)
PRE=[f'precip_lag{k}' for k in range(9)]; TMP=[f'temp_lag{k}' for k in range(9)]
CAS=['cases_lag0','cases_lag1','cases_lag2','cases_lag4']; SEA=['sin_woy_1','cos_woy_1','sin_woy_2','cos_woy_2']
DEPT_CATS=sorted(prim.query("split=='train'")['dept'].unique())
casesX=np.column_stack([np.log1p(prim[c].values) for c in CAS])
preX=np.column_stack([np.log1p(prim[c].values) for c in PRE]); tmpX=np.column_stack([prim[c].values.astype(float) for c in TMP])
seaX=np.column_stack([prim[c].values.astype(float) for c in SEA]); deptX=np.column_stack([(prim['dept'].values==dc).astype(float) for dc in DEPT_CATS])
XM5=np.hstack([casesX,preX,tmpX,seaX,deptX]); CONT_M5=np.arange(0,22)
XNC=np.hstack([casesX,seaX,deptX]); CONT_NC=np.arange(0,4)
Y=prim['label_h4'].values.astype(int); dept=prim['dept'].values; split=prim['split'].values
tr_pos=np.where(split=='train')[0]; va_pos=np.where(split=='val')[0]; te_pos=np.where(split=='test')[0]
def fit_eval(Xm,cont,tr,va,te):
    Xt=Xm[tr]; mu=Xt[:,cont].mean(0); sd=Xt[:,cont].std(0,ddof=0); sd[sd==0]=1.0
    def std(rows):
        Z=Xm[rows].copy(); Z[:,cont]=(Z[:,cont]-mu)/sd; return Z
    Xtr,Xva,Xte=std(tr),std(va),std(te); ytr=Y[tr]; yva=Y[va]; best=None
    for C in CGRID:
        m=LogisticRegression(C=C,penalty='l2',solver='lbfgs',max_iter=5000).fit(Xtr,ytr)
        p=np.clip(m.predict_proba(Xva)[:,1],1e-6,1-1e-6); ll=log_loss(yva,p,labels=[0,1])
        if best is None or ll<best[0]: best=(ll,C,m)
    _,C,m=best
    praw_va=np.clip(m.predict_proba(Xva)[:,1],1e-6,1-1e-6); praw_te=np.clip(m.predict_proba(Xte)[:,1],1e-6,1-1e-6)
    lr=LogisticRegression(C=1e6,solver='lbfgs',max_iter=1000).fit(np.log(praw_va/(1-praw_va)).reshape(-1,1),yva)
    return lr.predict_proba(np.log(praw_te/(1-praw_te)).reshape(-1,1))[:,1]
def nll(y,p): p=np.clip(p,EPS,1-EPS); return float(np.mean(-(y*np.log(p)+(1-y)*np.log(1-p))))
def brier(y,p): return float(np.mean((p-y)**2))
def deltas(tr,va,te):
    p5=fit_eval(XM5,CONT_M5,tr,va,te); pnc=fit_eval(XNC,CONT_NC,tr,va,te); y=Y[te]
    return nll(y,p5)-nll(y,pnc), brier(y,p5)-brier(y,pnc)
# GATE (full-data point)
dNLL,dBrier=deltas(tr_pos,va_pos,te_pos)
gate=abs(dNLL-(-0.0089))<=0.002 and abs(dBrier-(-0.0043))<=0.002
print(f"GATE: dNLL={dNLL:+.5f} (target -0.0089) dBrier={dBrier:+.5f} (target -0.0043) -> {'PASS' if gate else 'FAIL'} [{time.time()-t0:.0f}s]",flush=True)
if not gate: raise SystemExit("*** GATE FAILED ***")
# DI department bootstrap
test_depts=sorted(np.unique(dept[te_pos]))
tr_by={g:tr_pos[dept[tr_pos]==g] for g in DEPT_CATS}; va_by={g:va_pos[dept[va_pos]==g] for g in DEPT_CATS}; te_by={g:te_pos[dept[te_pos]==g] for g in test_depts}
rng=np.random.default_rng(SEED); K=len(test_depts)
PICKS=[[test_depts[i] for i in rng.integers(0,K,K)] for _ in range(B)]
def worker(pick):
    rtr=np.concatenate([tr_by[g] for g in pick if len(tr_by[g])]); rva=np.concatenate([va_by[g] for g in pick if len(va_by[g])]); rte=np.concatenate([te_by[g] for g in pick if len(te_by[g])])
    if len(np.unique(Y[rte]))<2 or len(np.unique(Y[rva]))<2 or len(np.unique(Y[rtr]))<2: return None
    try: return deltas(rtr,rva,rte)
    except Exception: return None
if __name__=='__main__':
    with Pool(NPROC) as pool: out=pool.map(worker,PICKS,chunksize=4)
    ok=[x for x in out if x is not None]; nllD=np.array([x[0] for x in ok]); brD=np.array([x[1] for x in ok]); fails=len(out)-len(ok)
    def ci(a): return [round(float(np.percentile(a,2.5)),5),round(float(np.percentile(a,97.5)),5)]
    res={"analysis":"colombia_devincl_proper_scores","label":"75th-pct primary, recalibrated","B":B,"seed":SEED,
     "point":{"dNLL":round(dNLL,5),"dBrier":round(dBrier,5)},
     "development_inclusive_department":{"dNLL":{"point":round(dNLL,5),"ci":ci(nllD),"median":round(float(np.median(nllD)),5)},
        "dBrier":{"point":round(dBrier,5),"ci":ci(brD),"median":round(float(np.median(brD)),5)},"replicates_used":len(ok),"failures":fails},
     "conditional_reference_from_manuscript":{"dNLL":-0.0089,"dBrier":-0.0043},"seconds":round(time.time()-t0,1)}
    json.dump(res,open(f'{OUT}/colombia_devincl_properscore_results.json','w'),indent=2)
    pd.DataFrame({"dNLL":pd.Series(nllD),"dBrier":pd.Series(brD)}).to_csv(f'{OUT}/colombia_devincl_properscore_distribution.csv',index=False)
    print(json.dumps(res,indent=2),flush=True); print("DONE",flush=True)
