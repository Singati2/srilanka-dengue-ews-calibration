#!/usr/bin/env python3
"""Colombia horizon sensitivity h=1,2,4,8,12 (per docs/colombia_horizon_sensitivity_spec.md).
Same M0-M5 regularized L2 logistic ladder, train-only preprocessing, validation-tuned C,
validation Platt recalibration, GID_2 cluster bootstrap (seed 20260612, B=1000) as the committed h=4 run.
Per-horizon common-complete recomputed with label_h{h}. h=4 = reproducibility anchor (does NOT overwrite committed h=4 dir).
SECONDARY/supplementary; h=4 remains the primary Colombia result. Outputs to a NEW quarantine dir only."""
import pandas as pd, numpy as np, json, hashlib, os, warnings
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, average_precision_score, brier_score_loss, log_loss
import statsmodels.api as sm
warnings.filterwarnings('ignore')
LF='/home/mpcrlab/data_quarantine/colombia_label_features_v1'
SRC=f'{LF}/colombia_modeling_table_all_horizons_v1.csv'
OUT='/home/mpcrlab/data_quarantine/colombia_model_pilots/horizon_sensitivity_v1'; os.makedirs(OUT,exist_ok=True)
PSTAR=0.30; CGRID=[0.001,0.003,0.01,0.03,0.1,0.3,1,3,10]; SEED=20260612; B=1000; HZ=[1,2,4,8,12]
d=pd.read_csv(SRC,dtype={'week_start':str}); d['dept']=d.GID_2.str.split('.').str[1]
PRE=[f'precip_lag{k}' for k in range(9)]; TMP=[f'temp_lag{k}' for k in range(9)]
CAS=['cases_lag0','cases_lag1','cases_lag2','cases_lag4']; SEA=['sin_woy_1','cos_woy_1','sin_woy_2','cos_woy_2']
MODELS={'M0':['season'],'M1':['cases'],'M2':['climate'],'M3':['climate','season','dept'],'M4':['cases','climate'],'M5':['cases','climate','season','dept']}
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
    for c in cont: m,s=scaler[c]; X[c]=(X[c]-m)/(s if s else 1.0)
    if 'dept' in feats:
        if dept_cats is None: dept_cats=sorted(df['dept'].unique())
        for dc in dept_cats: X[f'dept_{dc}']=(df['dept']==dc).astype(float)
    return X,scaler,dept_cats
def logit(p): p=np.clip(p,1e-6,1-1e-6); return np.log(p/(1-p))
def nb(y,p,t):
    pos=p>=t; n=len(y); tp=np.sum(pos&(y==1)); fp=np.sum(pos&(y==0)); return tp/n-(fp/n)*(t/(1-t))
def citl_slope(y,p):
    lp=logit(p)
    try: c=float(sm.Logit(y,np.ones_like(lp),offset=lp).fit(disp=0).params[0])
    except Exception: c=np.nan
    try: s=float(sm.Logit(y,sm.add_constant(lp)).fit(disp=0).params[1])
    except Exception: s=np.nan
    return c,s
clim_ok=d[PRE+TMP].notna().all(axis=1); cas_ok=d[CAS].notna().all(axis=1)

ALLm=[]; ALLc=[]; ALLdca=[]; ALLpred=[]; ALLboot=[]; counts={}
for h in HZ:
    lab=f'label_h{h}'; cc=d[clim_ok&cas_ok&d[lab].notna()].copy()
    counts[h]=cc.split.value_counts().to_dict()
    tr=cc[cc.split=='train']; va=cc[cc.split=='val']; te=cc[cc.split=='test']
    if te[lab].nunique()<2: raise SystemExit(f"STOP: horizon h={h} test has one class")
    res={}; yte=te[lab].values.astype(int)
    for name,feats in MODELS.items():
        Xtr,sc,dc=design(tr,feats); ytr=tr[lab].values.astype(int); yva=va[lab].values.astype(int)
        best=None
        for C in CGRID:
            m=LogisticRegression(C=C,penalty='l2',solver='lbfgs',max_iter=5000); m.fit(Xtr,ytr)
            p=np.clip(m.predict_proba(design(va,feats,sc,dc)[0])[:,1],1e-6,1-1e-6); ll=log_loss(yva,p,labels=[0,1])
            if best is None or ll<best[0]: best=(ll,C,m)
        vll,C,m=best
        praw_va=np.clip(m.predict_proba(design(va,feats,sc,dc)[0])[:,1],1e-6,1-1e-6)
        praw=np.clip(m.predict_proba(design(te,feats,sc,dc)[0])[:,1],1e-6,1-1e-6)
        pl=LogisticRegression(C=1e6,max_iter=1000).fit(logit(praw_va).reshape(-1,1),yva)
        prec=pl.predict_proba(logit(praw).reshape(-1,1))[:,1]
        res[name]=dict(praw=praw,prec=prec,C=C,vll=vll)
        for tag,p in [('raw',praw),('recal',prec)]:
            ci,sl=citl_slope(yte,p)
            ALLm.append(dict(horizon=h,model=name,calib=tag,C=C,val_logloss=vll,AUC=roc_auc_score(yte,p),
                PR_AUC=average_precision_score(yte,p),Brier=brier_score_loss(yte,p),CITL=ci,slope=sl,NB_p30=nb(yte,p,PSTAR)))
        for t in np.round(np.arange(0.05,0.51,0.05),2): ALLdca.append(dict(horizon=h,model=name,threshold=t,NB_recal=nb(yte,prec,t)))
    prev=yte.mean()
    for t in np.round(np.arange(0.05,0.51,0.05),2):
        ALLdca.append(dict(horizon=h,model='treat_all',threshold=t,NB_recal=prev-(1-prev)*(t/(1-t))))
        ALLdca.append(dict(horizon=h,model='treat_none',threshold=t,NB_recal=0.0))
    # contrasts vs M1 (recal NB, raw-equiv AUC)
    a=lambda p: roc_auc_score(yte,p)
    for name in ['M2','M3','M4','M5']:
        ALLc.append(dict(horizon=h,contrast=f'{name}_vs_M1',dAUC=a(res[name]['praw'])-a(res['M1']['praw']),
            dNB_p30=nb(yte,res[name]['prec'],PSTAR)-nb(yte,res['M1']['prec'],PSTAR)))
    # predictions (test)
    pr={'horizon':h,'GID_2':te.GID_2.values,'week_start':te.week_start.values,'y':yte}
    for name in MODELS: pr[f'{name}_recal']=res[name]['prec']
    ALLpred.append(pd.DataFrame(pr))
    # bootstrap
    units=te.GID_2.values; uniq=np.array(sorted(set(units))); idx={u:np.where(units==u)[0] for u in uniq}
    rng=np.random.default_rng(SEED); fails=0; bd={f'{n}_vs_M1':{'dAUC':[],'dNB':[]} for n in ['M2','M3','M4','M5']}
    bm={n:{'AUC':[],'NB':[]} for n in MODELS}
    for b in range(B):
        samp=rng.choice(uniq,size=len(uniq),replace=True); bi=np.concatenate([idx[u] for u in samp]); yb=yte[bi]
        if len(np.unique(yb))<2: fails+=1; continue
        au={}; nbs={}
        for n in MODELS: au[n]=roc_auc_score(yb,res[n]['praw'][bi]); nbs[n]=nb(yb,res[n]['prec'][bi],PSTAR); bm[n]['AUC'].append(au[n]); bm[n]['NB'].append(nbs[n])
        for n in ['M2','M3','M4','M5']: bd[f'{n}_vs_M1']['dAUC'].append(au[n]-au['M1']); bd[f'{n}_vs_M1']['dNB'].append(nbs[n]-nbs['M1'])
    pc=lambda arr,q: float(np.percentile(arr,q)) if len(arr) else np.nan
    for n in MODELS:
        ALLboot.append(dict(horizon=h,model=n,AUC_lo=pc(bm[n]['AUC'],2.5),AUC_med=pc(bm[n]['AUC'],50),AUC_hi=pc(bm[n]['AUC'],97.5),
            NB_lo=pc(bm[n]['NB'],2.5),NB_med=pc(bm[n]['NB'],50),NB_hi=pc(bm[n]['NB'],97.5),B=B,failures=fails,fail_rate=fails/B))
    for c in bd:
        ALLboot.append(dict(horizon=h,model=c,dAUC_lo=pc(bd[c]['dAUC'],2.5),dAUC_med=pc(bd[c]['dAUC'],50),dAUC_hi=pc(bd[c]['dAUC'],97.5),
            dNB_lo=pc(bd[c]['dNB'],2.5),dNB_med=pc(bd[c]['dNB'],50),dNB_hi=pc(bd[c]['dNB'],97.5),B=B,failures=fails,fail_rate=fails/B))
# write
pd.DataFrame(ALLm).to_csv(f'{OUT}/colombia_horizon_metrics_v1.csv',index=False)
pd.DataFrame(ALLc).to_csv(f'{OUT}/colombia_horizon_contrasts_v1.csv',index=False)
pd.DataFrame(ALLdca).to_csv(f'{OUT}/colombia_horizon_dca_v1.csv',index=False)
pd.DataFrame(ALLboot).to_csv(f'{OUT}/colombia_horizon_bootstrap_ci_v1.csv',index=False)
pd.concat(ALLpred,ignore_index=True).to_csv(f'{OUT}/colombia_horizon_predictions_v1.csv',index=False)
def sh(p): return hashlib.sha256(open(p,'rb').read()).hexdigest()
outs=['colombia_horizon_metrics_v1.csv','colombia_horizon_contrasts_v1.csv','colombia_horizon_dca_v1.csv','colombia_horizon_bootstrap_ci_v1.csv','colombia_horizon_predictions_v1.csv']
# h=4 reproducibility check
m=pd.DataFrame(ALLm); mr=m[m.calib=='recal']
def gv(h,model,col): return float(mr[(mr.horizon==h)&(mr.model==model)][col].iloc[0])
cdf=pd.DataFrame(ALLc);
def gc(h,contrast,col): return float(cdf[(cdf.horizon==h)&(cdf.contrast==contrast)][col].iloc[0])
repro=dict(M1_AUC=round(gv(4,'M1','AUC'),3),M1_NB=round(gv(4,'M1','NB_p30'),3),M4_AUC=round(gv(4,'M4','AUC'),3),
    M5_AUC=round(gv(4,'M5','AUC'),3),M5_NB=round(gv(4,'M5','NB_p30'),3),M5vM1_dAUC=round(gc(4,'M5_vs_M1','dAUC'),3),M5vM1_dNB=round(gc(4,'M5_vs_M1','dNB_p30'),3))
meta=dict(spec='docs/colombia_horizon_sensitivity_spec.md (04346fa)',input=SRC,input_sha256=sh(SRC),
    horizons=HZ,common_complete_counts=counts,pstar=PSTAR,C_grid=CGRID,seed=SEED,B=B,
    role='SECONDARY/supplementary; h=4 remains primary committed result; this run does NOT overwrite model_ladder_h4_75pct_v1',
    h4_reproducibility=repro,labels_thresholds_recomputed=False,sri_lanka_data_used=False,output_sha256={o:sh(f'{OUT}/{o}') for o in outs})
json.dump(meta,open(f'{OUT}/colombia_horizon_sensitivity_v1.meta.json','w'),indent=2)
print('common-complete counts:',counts)
print('\nh=4 reproducibility (recal):',repro)
print('\nM5 vs M1 by horizon (ΔAUC, ΔNB@0.30) + bootstrap CI:')
bdf=pd.DataFrame(ALLboot)
for h in HZ:
    r=bdf[(bdf.horizon==h)&(bdf.model=='M5_vs_M1')].iloc[0]
    print(f"  h={h}: ΔAUC {gc(h,'M5_vs_M1','dAUC'):+.3f} [{r.dAUC_lo:+.3f},{r.dAUC_hi:+.3f}] | ΔNB {gc(h,'M5_vs_M1','dNB_p30'):+.3f} [{r.dNB_lo:+.3f},{r.dNB_hi:+.3f}]")
print('\nM1 & M5 AUC/NB by horizon (recal):')
for h in HZ: print(f"  h={h}: M1 AUC {gv(h,'M1','AUC'):.3f} NB {gv(h,'M1','NB_p30'):.3f} | M5 AUC {gv(h,'M5','AUC'):.3f} NB {gv(h,'M5','NB_p30'):.3f}")
print('\nfail rates:',{h:float(bdf[bdf.horizon==h].fail_rate.iloc[0]) for h in HZ})
