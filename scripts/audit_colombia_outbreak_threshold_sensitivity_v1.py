#!/usr/bin/env python3
"""Convergence & integrity audit for the FROZEN E3 outbreak-threshold sensitivity (commit f1ace05).
Re-runs the E3 fits with explicit convergence capture and compares against the frozen outputs.
READ-ONLY w.r.t. the frozen E3 directory: writes nothing there; regenerates nothing; overwrites nothing.
Use SAME frozen inputs / labels / models / C-grid / split / preprocessing / Platt recal / seed as the
committed generator (scripts/colombia_outbreak_threshold_sensitivity_v1.py), which remains UNCHANGED.
Hard-fails on any convergence or integrity-gate violation. Prints a summary; optionally writes a small
audit-summary JSON to a SEPARATE audit dir (never the frozen E3 dir)."""
import pandas as pd, numpy as np, warnings, json, os
from sklearn.linear_model import LogisticRegression
from sklearn.exceptions import ConvergenceWarning
from sklearn.metrics import log_loss, roc_auc_score
LF='/home/mpcrlab/data_quarantine/colombia_label_features_v1'
FROZEN='/home/mpcrlab/data_quarantine/colombia_model_pilots/outbreak_threshold_sensitivity_v1'   # READ-ONLY
AUDIT='/home/mpcrlab/data_quarantine/colombia_model_pilots/outbreak_threshold_sensitivity_audit_v1'  # separate
SRC=f'{LF}/colombia_modeling_table_all_horizons_v1.csv'; THRC=f'{LF}/colombia_label_thresholds_train_only_v1.csv'
CGRID=[0.001,0.003,0.01,0.03,0.1,0.3,1,3,10]; MAXIT=5000; PMAXIT=1000; PSTAR=0.30
PRE=[f'precip_lag{k}' for k in range(9)]; TMP=[f'temp_lag{k}' for k in range(9)]
CAS=['cases_lag0','cases_lag1','cases_lag2','cases_lag4']; SEA=['sin_woy_1','cos_woy_1','sin_woy_2','cos_woy_2']
MODELS={'M0':['season'],'M1':['cases'],'M2':['climate'],'M3':['climate','season','dept'],'M4':['cases','climate'],'M5':['cases','climate','season','dept']}
def design(df,feats,sc=None,dc=None):
    X=pd.DataFrame(index=df.index); cont=[]
    if 'cases' in feats:
        for c in CAS: X[c]=np.log1p(df[c]); cont.append(c)
    if 'climate' in feats:
        for c in PRE: X[c]=np.log1p(df[c]); cont.append(c)
        for c in TMP: X[c]=df[c]; cont.append(c)
    if 'season' in feats:
        for c in SEA: X[c]=df[c]
    if sc is None: sc={c:(X[c].mean(),X[c].std(ddof=0) or 1.0) for c in cont}
    for c in cont: m,s=sc[c]; X[c]=(X[c]-m)/(s if s else 1.0)
    if 'dept' in feats:
        if dc is None: dc=sorted(df['dept'].unique())
        for x in dc: X[f'dept_{x}']=(df['dept']==x).astype(float)
    return X,sc,dc
def logit(p): p=np.clip(p,1e-6,1-1e-6); return np.log(p/(1-p))
def nb(y,p,t): pos=p>=t; n=len(y); return np.sum(pos&(y==1))/n-(np.sum(pos&(y==0))/n)*(t/(1-t))
def fit_cap(X,y,C,maxit):
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter('always')
        m=LogisticRegression(C=C,penalty='l2',solver='lbfgs',max_iter=maxit).fit(X,y)
        cw=any(issubclass(x.category,ConvergenceWarning) for x in w)
    ni=int(np.max(m.n_iter_)); return m,ni,((not cw) and ni<maxit)

# ---- load frozen inputs (read-only) ----
d=pd.read_csv(SRC,dtype={'week_start':str}); d['dept']=d.GID_2.str.split('.').str[1]; d['wk']=pd.to_datetime(d.week_start)
rec=d[d.split=='train'].groupby('GID_2').dengue_total.agg(thr75=lambda s:np.percentile(s,75),thr80=lambda s:np.percentile(s,80),thr90=lambda s:np.percentile(s,90)).reset_index()
cm=pd.read_csv(THRC)[['GID_2','thr75','thr90']]; v=rec.merge(cm,on='GID_2',suffixes=('_r','_c'))
thr75_d=float((v.thr75_r-v.thr75_c).abs().max()); thr90_d=float((v.thr90_r-v.thr90_c).abs().max())
assert thr75_d<=1e-9 and thr90_d<=1e-6, f"threshold provenance FAIL thr75={thr75_d} thr90={thr90_d}"
out={(g,w):c for g,w,c in zip(d.GID_2,d.week_start,d.dengue_total)}
cc=d[d.common_complete_M1_to_M5_h4==True].copy(); cc['t4']=(cc.wk+pd.Timedelta(weeks=4)).dt.date.astype(str)
cc['o4']=[out.get((g,w),np.nan) for g,w in zip(cc.GID_2,cc.t4)]; Tt=rec.set_index('GID_2')
for p,c in [(75,'thr75'),(80,'thr80'),(90,'thr90')]:
    l=(cc.o4>cc.GID_2.map(Tt[c].to_dict())).astype(float); l[cc.o4.isna()]=np.nan; cc[f'label_{p}']=l
lab75_match=int((cc.label_75==cc.label_h4).sum())==len(cc); assert lab75_match,"75th label != committed label_h4"
ccn=cc.split.value_counts().to_dict(); assert (ccn.get('train'),ccn.get('val'),ccn.get('test'))==(53711,12713,13361),f"row counts {ccn}"

frozen_pred=pd.read_csv(f'{FROZEN}/colombia_outbreak_threshold_predictions_v1.csv')
sel_noncv=[]; cand_warn=0; platt_noncv=[]; maxabs=0.0; dnb={}
for pct in [75,80,90]:
    lab=f'label_{pct}'; g=cc.dropna(subset=[lab]); trn,va,te=g[g.split=='train'],g[g.split=='val'],g[g.split=='test']
    yva=va[lab].values.astype(int); rr={}
    for name,feats in MODELS.items():
        Xtr,sc,dc=design(trn,feats); ytr=trn[lab].values.astype(int); best=None
        for C in CGRID:
            m,ni,ok=fit_cap(Xtr,ytr,C,MAXIT)
            if not ok: cand_warn+=1
            p=np.clip(m.predict_proba(design(va,feats,sc,dc)[0])[:,1],1e-6,1-1e-6); ll=log_loss(yva,p,labels=[0,1])
            if best is None or ll<best[0]: best=(ll,C,m,ok,ni)
        ll,C,m,ok,ni=best
        if not ok: sel_noncv.append((pct,name,C,ni))
        pv=np.clip(m.predict_proba(design(va,feats,sc,dc)[0])[:,1],1e-6,1-1e-6)
        pr=np.clip(m.predict_proba(design(te,feats,sc,dc)[0])[:,1],1e-6,1-1e-6)
        plm,pni,pok=fit_cap(logit(pv).reshape(-1,1),yva,1e6,PMAXIT)
        if not pok: platt_noncv.append((pct,name,pni))
        prec=plm.predict_proba(logit(pr).reshape(-1,1))[:,1]; rr[name]=prec
        sub=frozen_pred[frozen_pred.percentile==pct]
        mg=pd.DataFrame({'GID_2':te.GID_2.values,'week_start':te.week_start.values,'rr':prec}).merge(sub[['GID_2','week_start',f'{name}_recal']],on=['GID_2','week_start'])
        maxabs=max(maxabs,float((mg.rr-mg[f'{name}_recal']).abs().max()))
    sub=frozen_pred[frozen_pred.percentile==pct]; y=sub.y.values
    dnb[pct]=round(nb(y,sub.M5_recal.values,PSTAR)-nb(y,sub.M1_recal.values,PSTAR),4)

summary=dict(audited_commit='f1ace05',frozen_dir=FROZEN,
    convergence=dict(selected_nonconverged=sel_noncv,candidate_convergence_warnings=cand_warn,platt_nonconverged=platt_noncv),
    integrity=dict(thr75_maxabs=thr75_d,thr90_maxabs=thr90_d,label75_reproduces_committed=bool(lab75_match),row_counts=ccn),
    reproduction=dict(predictions_max_abs_diff_recal=maxabs,dNB_M5_M1_p30_from_frozen=dnb),
    note='Frozen E3 outputs NOT regenerated/overwritten; full output-file byte identity NOT tested.')
os.makedirs(AUDIT,exist_ok=True); json.dump(summary,open(f'{AUDIT}/e3_audit_summary_v1.json','w'),indent=2)
print(json.dumps(summary,indent=2))
print('\nAUDIT VERDICT:', 'PASS — no convergence/integrity issue; results unchanged' if not(sel_noncv or platt_noncv) else 'FAIL — see above')
