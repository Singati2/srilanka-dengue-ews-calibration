#!/usr/bin/env python3
"""Colombia matched climate ablation at the 90th-percentile outbreak label (SPEED-OPTIMIZED).
Pre-registered in docs/matched_ablation_90th_percentile_spec.md (reviewer finding #1).

Numerically identical to the verbatim co_devincl_full_refit.py pipeline, but:
  (1) the raw (pre-standardization) design is PRECOMPUTED once as numpy arrays and row-indexed,
      instead of rebuilt with pandas per fit — same numbers, no pandas overhead;
  (2) the per-replicate standardization (train mu/sd, ddof=0), C-grid log-loss selection, and
      Platt recalibration are unchanged (development-inclusive: scaling+tuning+recal refit per resample);
  (3) bootstrap replicates run in parallel across cores over PRE-GENERATED (seeded, deterministic)
      department resample picks — identical picks & fits as sequential, just concurrent.
Reproduce-first gate at 75th (matched +0.00786, compound +0.018775) before the 90th run.
Read-only inputs; writes only under OUT. Nothing committed.
"""
import os
os.environ.setdefault('OMP_NUM_THREADS','1'); os.environ.setdefault('OPENBLAS_NUM_THREADS','1'); os.environ.setdefault('MKL_NUM_THREADS','1')
import sys, numpy as np, pandas as pd, json, time, warnings
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import log_loss
from multiprocessing import Pool
warnings.filterwarnings('ignore')
LF='/home/mpcrlab/data_quarantine/colombia_label_features_v1'
E3='/home/mpcrlab/data_quarantine/colombia_model_pilots/outbreak_threshold_sensitivity_v1/colombia_outbreak_threshold_labels_v1.csv'
OUT='/home/mpcrlab/srilanka-dengue-ews-calibration/analysis/matched_ablation_90pct_v1'; os.makedirs(OUT,exist_ok=True)
SRC=f'{LF}/colombia_modeling_table_h4_75pct_v1.csv'
PSTAR=0.30; CGRID=[0.001,0.003,0.01,0.03,0.1,0.3,1,3,10]; SEED=20260612
B=int(sys.argv[1]) if len(sys.argv)>1 else 1000
NPROC=int(sys.argv[2]) if len(sys.argv)>2 else 14
t0=time.time()
d=pd.read_csv(SRC,dtype={'week_start':str}); d['dept']=d.GID_2.str.split('.').str[1]
e=pd.read_csv(E3,dtype={'week_start':str})
d=d.merge(e[['GID_2','week_start','label_90']],on=['GID_2','week_start'],how='left')
prim=d[d.common_complete_M1_to_M5_h4==True].copy().reset_index(drop=True)
assert prim['label_90'].notna().all(), "label_90 merge incomplete — STOP"
PRE=[f'precip_lag{k}' for k in range(9)]; TMP=[f'temp_lag{k}' for k in range(9)]
CAS=['cases_lag0','cases_lag1','cases_lag2','cases_lag4']; SEA=['sin_woy_1','cos_woy_1','sin_woy_2','cos_woy_2']
DEPT_CATS=sorted(prim.query("split=='train'")['dept'].unique())

# ---- precompute RAW (pre-standardization) design, M5 column order ----
# [ cases_log(4) | precip_log(9) | temp(9) | season(4) | dept(32) ]  (cont = first 22)
casesX=np.column_stack([np.log1p(prim[c].values) for c in CAS])
preX  =np.column_stack([np.log1p(prim[c].values) for c in PRE])
tmpX  =np.column_stack([prim[c].values.astype(float) for c in TMP])
seaX  =np.column_stack([prim[c].values.astype(float) for c in SEA])
deptX =np.column_stack([(prim['dept'].values==dc).astype(float) for dc in DEPT_CATS])
XM5=np.hstack([casesX,preX,tmpX,seaX,deptX]);  CONT_M5=np.arange(0,22)
XNC=np.hstack([casesX,seaX,deptX]);            CONT_NC=np.arange(0,4)   # cases+season+dept (no climate)
XM1=casesX.copy();                             CONT_M1=np.arange(0,4)
Y75=prim['label_h4'].values.astype(int); Y90=prim['label_90'].values.astype(int)
dept=prim['dept'].values; split=prim['split'].values
tr_pos=np.where(split=='train')[0]; va_pos=np.where(split=='val')[0]; te_pos=np.where(split=='test')[0]

def fit_eval(Xm,cont,tr,va,te,Y):
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
    prec_te=lr.predict_proba(np.log(praw_te/(1-praw_te)).reshape(-1,1))[:,1]
    return prec_te
def nb(y,p,t=PSTAR):
    pos=p>=t; n=len(y); return np.sum(pos&(y==1))/n-np.sum(pos&(y==0))/n*(t/(1-t))
def point(Y):
    p5 =fit_eval(XM5,CONT_M5,tr_pos,va_pos,te_pos,Y)
    pnc=fit_eval(XNC,CONT_NC,tr_pos,va_pos,te_pos,Y)
    p1 =fit_eval(XM1,CONT_M1,tr_pos,va_pos,te_pos,Y)
    yte=Y[te_pos]
    return yte,p5,pnc,nb(yte,p5)-nb(yte,pnc),nb(yte,p5)-nb(yte,p1)

# ---- GATE (75th) ----
y75,p5_75,pnc_75,m75,c75=point(Y75)
gate=abs(m75-0.00786)<=0.001 and abs(c75-0.018775)<=0.001
print(f"GATE 75th: matched={m75:+.5f} (t +0.00786) compound={c75:+.5f} (t +0.018775) -> {'PASS' if gate else 'FAIL'}  [{time.time()-t0:.0f}s]",flush=True)
if not gate: raise SystemExit("*** GATE FAILED — aborting ***")

# ---- 90th POINT ----
y90,p5_90,pnc_90,m90,c90=point(Y90)
print(f"90th POINT: prev={y90.mean():.4f} events={int(y90.sum())} n={len(y90)} matched={m90:+.5f} compound={c90:+.5f} (E3 compound +0.0092)  [{time.time()-t0:.0f}s]",flush=True)

# ---- DI department-refit bootstrap at 90th (PRIMARY, parallel over pre-generated picks) ----
test_depts=sorted(np.unique(dept[te_pos]))
tr_by={g:tr_pos[dept[tr_pos]==g] for g in DEPT_CATS}
va_by={g:va_pos[dept[va_pos]==g] for g in DEPT_CATS}
te_by={g:te_pos[dept[te_pos]==g] for g in test_depts}
rng=np.random.default_rng(SEED); K=len(test_depts)
PICKS=[[test_depts[i] for i in rng.integers(0,K,K)] for _ in range(B)]
def di_worker(pick):
    rtr=np.concatenate([tr_by[g] for g in pick if len(tr_by[g])])
    rva=np.concatenate([va_by[g] for g in pick if len(va_by[g])])
    rte=np.concatenate([te_by[g] for g in pick if len(te_by[g])])
    yb=Y90[rte]
    if len(np.unique(yb))<2 or len(np.unique(Y90[rva]))<2 or len(np.unique(Y90[rtr]))<2: return None
    try:
        p5 =fit_eval(XM5,CONT_M5,rtr,rva,rte,Y90); pnc=fit_eval(XNC,CONT_NC,rtr,rva,rte,Y90)
        return float(nb(yb,p5)-nb(yb,pnc))
    except Exception: return None
if __name__=='__main__':
    with Pool(NPROC) as pool:
        out=pool.map(di_worker,PICKS,chunksize=4)
    matched_D=np.array([x for x in out if x is not None]); fails=int(sum(x is None for x in out))
    uniq=[len(set(p)) for p in PICKS]
    print(f"DI done: used={len(matched_D)} fails={fails} meanUniqDept={np.mean(uniq):.1f}  [{time.time()-t0:.0f}s]",flush=True)

    # ---- conditional municipality bootstrap at 90th (secondary, frozen full-fit preds) ----
    munis=prim['GID_2'].values[te_pos]; mids=sorted(set(munis)); idx_by={mm:np.where(munis==mm)[0] for mm in mids}
    rng2=np.random.default_rng(SEED); cond_D=[]
    for _ in range(B):
        pick=[mids[i] for i in rng2.integers(0,len(mids),len(mids))]; ii=np.concatenate([idx_by[mm] for mm in pick]); yb=y90[ii]
        if len(np.unique(yb))<2: continue
        cond_D.append(nb(yb,p5_90[ii])-nb(yb,pnc_90[ii]))
    cond_D=np.array(cond_D)
    def ci(a): return [round(float(np.percentile(a,2.5)),5),round(float(np.percentile(a,97.5)),5)]
    res={"analysis":"colombia_matched_ablation_90pct","B":B,"seed":SEED,
     "gate_75th":{"matched":round(m75,5),"compound":round(c75,5),"passed":bool(gate)},
     "point_90th":{"prevalence":round(float(y90.mean()),4),"events":int(y90.sum()),"n":int(len(y90)),
                   "matched_dNB":round(m90,5),"compound_dNB_M5_M1":round(c90,5)},
     "development_inclusive_department":{"point":round(m90,5),"ci":ci(matched_D),"median":round(float(np.median(matched_D)),5),
                   "replicates_used":int(len(matched_D)),"failures":fails,
                   "mean_unique_depts":round(float(np.mean(uniq)),2),"total_test_depts":K},
     "conditional_municipality":{"point":round(m90,5),"ci":ci(cond_D),"replicates_used":int(len(cond_D))},
     "reference_75th_from_manuscript":{"matched":0.0078,"conditional":[0.0039,0.0119],"development_inclusive":[0.0008,0.0209]},
     "seconds":round(time.time()-t0,1)}
    json.dump(res,open(f'{OUT}/colombia_matched_ablation_90pct_results.json','w'),indent=2)
    pd.DataFrame({"matched_DI":pd.Series(matched_D),"matched_cond":pd.Series(cond_D)}).to_csv(f'{OUT}/colombia_matched_ablation_90pct_distribution.csv',index=False)
    print(json.dumps(res,indent=2),flush=True); print("DONE",flush=True)
