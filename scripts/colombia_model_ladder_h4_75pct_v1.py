#!/usr/bin/env python3
"""Colombia M0-M5 model-ladder evaluation (per docs/colombia_model_ladder_spec.md).
Regularized L2 logistic regression; train-only preprocessing; C tuned on validation log loss;
Platt recalibration on validation; test evaluated once; GID_2 cluster bootstrap (seed 20260612, B=1000).
Colombia data only; no coefficient transfer; no label/threshold recompute. Outputs to quarantine only."""
import pandas as pd, numpy as np, json, hashlib, os, warnings
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, average_precision_score, brier_score_loss, log_loss
import statsmodels.api as sm
warnings.filterwarnings('ignore')
np.random.seed(20260612)
LF='/home/mpcrlab/data_quarantine/colombia_label_features_v1'
OUT='/home/mpcrlab/data_quarantine/colombia_model_pilots/model_ladder_h4_75pct_v1'; os.makedirs(OUT,exist_ok=True)
SRC=f'{LF}/colombia_modeling_table_h4_75pct_v1.csv'
PSTAR=0.30; CGRID=[0.001,0.003,0.01,0.03,0.1,0.3,1,3,10]; SEED=20260612; B=1000
d=pd.read_csv(SRC,dtype={'week_start':str})
d['dept']=d.GID_2.str.split('.').str[1]
PRE=[f'precip_lag{k}' for k in range(9)]; TMP=[f'temp_lag{k}' for k in range(9)]
CAS=['cases_lag0','cases_lag1','cases_lag2','cases_lag4']; SEA=['sin_woy_1','cos_woy_1','sin_woy_2','cos_woy_2']

def design(df, feats, scaler=None, dept_cats=None):
    X=pd.DataFrame(index=df.index)
    cont=[]
    if 'cases' in feats:
        for c in CAS: X[c]=np.log1p(df[c]); cont.append(c)
    if 'climate' in feats:
        for c in PRE: X[c]=np.log1p(df[c]); cont.append(c)
        for c in TMP: X[c]=df[c]; cont.append(c)
    if 'season' in feats:
        for c in SEA: X[c]=df[c]
    # standardize continuous only (train stats)
    if scaler is None: scaler={c:(X[c].mean(),X[c].std(ddof=0) or 1.0) for c in cont}
    for c in cont: m,s=scaler[c]; X[c]=(X[c]-m)/(s if s else 1.0)
    if 'dept' in feats:
        if dept_cats is None: dept_cats=sorted(df['dept'].unique())
        for dc in dept_cats: X[f'dept_{dc}']=(df['dept']==dc).astype(float)
    return X, scaler, dept_cats

MODELS={'M0':['season'],'M1':['cases'],'M2':['climate'],'M3':['climate','season','dept'],
        'M4':['cases','climate'],'M5':['cases','climate','season','dept']}

def fit_select(tr,va,feats):
    Xtr,sc,dc=design(tr,feats); Xva,_,_=design(va,feats,sc,dc)
    ytr=tr.label_h4.values; yva=va.label_h4.values
    best=None
    for C in CGRID:
        m=LogisticRegression(C=C,penalty='l2',solver='lbfgs',max_iter=5000)
        m.fit(Xtr,ytr); p=np.clip(m.predict_proba(Xva)[:,1],1e-6,1-1e-6)
        ll=log_loss(yva,p,labels=[0,1])
        if best is None or ll<best[0]: best=(ll,C,m)
    return best[2],best[1],best[0],sc,dc,list(Xtr.columns)

def logit(p): p=np.clip(p,1e-6,1-1e-6); return np.log(p/(1-p))
def platt(p_va,y_va):
    lr=LogisticRegression(C=1e6,solver='lbfgs',max_iter=1000); lr.fit(logit(p_va).reshape(-1,1),y_va)
    return lr
def apply_platt(lr,p): return lr.predict_proba(logit(p).reshape(-1,1))[:,1]
def nb(y,p,t):
    pos=p>=t; n=len(y); tp=np.sum(pos&(y==1)); fp=np.sum(pos&(y==0))
    return tp/n - (fp/n)*(t/(1-t))
def citl_slope(y,p):
    lp=logit(p)
    try:
        citl=float(sm.Logit(y,np.ones_like(lp),offset=lp).fit(disp=0).params[0])
    except Exception: citl=np.nan
    try:
        m=sm.Logit(y,sm.add_constant(lp)).fit(disp=0); slope=float(m.params[1])
    except Exception: slope=np.nan
    return citl,slope

def run(df,label):
    tr=df[df.split=='train']; va=df[df.split=='val']; te=df[df.split=='test']
    res={}; preds={'GID_2':te.GID_2.values,'week_start':te.week_start.values,'y':te.label_h4.values}
    metrics=[]; calib=[]; coefs=[]; dca_rows=[]
    for name,feats in MODELS.items():
        m,C,vll,sc,dc,cols=fit_select(tr,va,feats)
        Xva,_,_=design(va,feats,sc,dc); Xte,_,_=design(te,feats,sc,dc)
        praw_va=np.clip(m.predict_proba(Xva)[:,1],1e-6,1-1e-6)
        praw=np.clip(m.predict_proba(Xte)[:,1],1e-6,1-1e-6)
        pl=platt(praw_va,va.label_h4.values); prec=apply_platt(pl,praw)
        yte=te.label_h4.values
        preds[f'{name}_raw']=praw; preds[f'{name}_recal']=prec
        res[name]=dict(praw=praw,prec=prec,C=C,vll=vll)
        for tag,p in [('raw',praw),('recal',prec)]:
            auc=roc_auc_score(yte,p); pr=average_precision_score(yte,p); br=brier_score_loss(yte,p)
            ci,sl=citl_slope(yte,p)
            metrics.append(dict(rowset=label,model=name,calib=tag,C=C,val_logloss=vll,
                AUC=auc,PR_AUC=pr,Brier=br,CITL=ci,slope=sl,NB_p30=nb(yte,p,PSTAR)))
            calib.append(dict(rowset=label,model=name,calib=tag,CITL=ci,slope=sl))
        for t in np.round(np.arange(0.05,0.51,0.05),2):
            dca_rows.append(dict(rowset=label,model=name,threshold=t,NB_recal=nb(yte,prec,t)))
        for fn,cf in zip(cols,m.coef_[0]): coefs.append(dict(rowset=label,model=name,feature=fn,coef=float(cf)))
        coefs.append(dict(rowset=label,model=name,feature='_intercept',coef=float(m.intercept_[0])))
    # treat-all / treat-none DCA reference
    yte=te.label_h4.values; prev=yte.mean()
    for t in np.round(np.arange(0.05,0.51,0.05),2):
        dca_rows.append(dict(rowset=label,model='treat_all',threshold=t,NB_recal=prev-(1-prev)*(t/(1-t))))
        dca_rows.append(dict(rowset=label,model='treat_none',threshold=t,NB_recal=0.0))
    return res,metrics,calib,coefs,dca_rows,preds,te

# ---- PRIMARY: common-complete ----
prim=d[d.common_complete_M1_to_M5_h4==True].copy()
expected={'train':53711,'val':12713,'test':13361}
observed=prim['split'].value_counts().to_dict()
if observed!=expected:
    raise RuntimeError(f"Primary common-complete row-count mismatch: expected {expected}, observed {observed}")
res,metrics,calib,coefs,dca_rows,preds,te=run(prim,'primary_common_complete')
pd.DataFrame(preds).to_csv(f'{OUT}/colombia_model_predictions_h4_75pct_v1.csv',index=False)

# ---- contrasts vs M1 (recal NB, raw-equiv AUC) on test ----
yte=te.label_h4.values
def auc(p): return roc_auc_score(yte,p)
contrasts=[]
for name in ['M2','M3','M4','M5']:
    contrasts.append(dict(contrast=f'{name}_vs_M1',dAUC=auc(res[name]['praw'])-auc(res['M1']['praw']),
        dNB_p30=nb(yte,res[name]['prec'],PSTAR)-nb(yte,res['M1']['prec'],PSTAR)))

# ---- GID_2 cluster bootstrap on test ----
units=te.GID_2.values; uniq=np.array(sorted(set(units)))
idx_by={u:np.where(units==u)[0] for u in uniq}
rng=np.random.default_rng(SEED)
boot={k:[] for k in ['M0','M1','M2','M3','M4','M5']}
bootd={f'{n}_vs_M1':{'dAUC':[],'dNB':[]} for n in ['M2','M3','M4','M5']}
fails=0
for b in range(B):
    samp=rng.choice(uniq,size=len(uniq),replace=True)
    bi=np.concatenate([idx_by[u] for u in samp])
    yb=yte[bi]
    if len(np.unique(yb))<2: fails+=1; continue
    aucs={}; nbs={}
    for n in MODELS:
        aucs[n]=roc_auc_score(yb,res[n]['praw'][bi]); nbs[n]=nb(yb,res[n]['prec'][bi],PSTAR)
        boot[n].append((aucs[n],nbs[n]))
    for n in ['M2','M3','M4','M5']:
        bootd[f'{n}_vs_M1']['dAUC'].append(aucs[n]-aucs['M1']); bootd[f'{n}_vs_M1']['dNB'].append(nbs[n]-nbs['M1'])
def ci(a): a=np.array(a); return (float(np.percentile(a,2.5)),float(np.percentile(a,97.5)),float(np.median(a)))
brows=[]
for n in MODELS:
    arr=np.array(boot[n]);
    if len(arr):
        al,ah,am=ci(arr[:,0]); nl,nh,nm=ci(arr[:,1])
        brows.append(dict(model=n,AUC_med=am,AUC_lo=al,AUC_hi=ah,NB_med=nm,NB_lo=nl,NB_hi=nh))
for c in bootd:
    dl,dh,dm=ci(bootd[c]['dAUC']); nl,nh,nm=ci(bootd[c]['dNB'])
    brows.append(dict(model=c,AUC_med=np.nan,AUC_lo=np.nan,AUC_hi=np.nan,
        dAUC_med=dm,dAUC_lo=dl,dAUC_hi=dh,dNB_med=nm,dNB_lo=nl,dNB_hi=nh))
boot_df=pd.DataFrame(brows); boot_df['B']=B; boot_df['failures']=fails; boot_df['fail_rate']=fails/B

# ---- SECONDARY: M2/M3 on full climate-modelable set ----
sec=d[d.modelable_M2_M3_h4==True].copy()
sec_metrics=[]
trs=sec[sec.split=='train']; vas=sec[sec.split=='val']; tes=sec[sec.split=='test']
for name in ['M2','M3']:
    m,C,vll,sc,dc,cols=fit_select(trs,vas,MODELS[name])
    Xte,_,_=design(tes,MODELS[name],sc,dc); p=np.clip(m.predict_proba(Xte)[:,1],1e-6,1-1e-6)
    pl=platt(np.clip(m.predict_proba(design(vas,MODELS[name],sc,dc)[0])[:,1],1e-6,1-1e-6),vas.label_h4.values)
    prec=apply_platt(pl,p); y=tes.label_h4.values
    sec_metrics.append(dict(rowset='secondary_climate_full',model=name,C=C,n_test=len(tes),
        AUC=roc_auc_score(y,p),NB_p30_recal=nb(y,prec,PSTAR),Brier_recal=brier_score_loss(y,prec)))

# ---- write outputs ----
pd.DataFrame(metrics+sec_metrics).to_csv(f'{OUT}/colombia_model_metrics_h4_75pct_v1.csv',index=False)
pd.DataFrame(dca_rows).to_csv(f'{OUT}/colombia_model_dca_h4_75pct_v1.csv',index=False)
pd.DataFrame(calib).to_csv(f'{OUT}/colombia_model_calibration_h4_75pct_v1.csv',index=False)
pd.DataFrame(coefs).to_csv(f'{OUT}/colombia_model_coefficients_h4_75pct_v1.csv',index=False)
boot_df.to_csv(f'{OUT}/colombia_model_bootstrap_ci_h4_75pct_v1.csv',index=False)
pd.DataFrame(contrasts).to_csv(f'{OUT}/colombia_model_contrasts_h4_75pct_v1.csv',index=False)
def sh(p): return hashlib.sha256(open(p,'rb').read()).hexdigest()
outs=['colombia_model_predictions_h4_75pct_v1.csv','colombia_model_metrics_h4_75pct_v1.csv','colombia_model_dca_h4_75pct_v1.csv',
 'colombia_model_calibration_h4_75pct_v1.csv','colombia_model_coefficients_h4_75pct_v1.csv','colombia_model_bootstrap_ci_h4_75pct_v1.csv','colombia_model_contrasts_h4_75pct_v1.csv']
meta=dict(spec='docs/colombia_model_ladder_spec.md (37221a6)',input=SRC,input_sha256=sh(SRC),
  primary_rowset='common_complete_M1_to_M5_h4',primary_counts=prim.split.value_counts().to_dict(),
  secondary_rowset='modelable_M2_M3_h4',secondary_counts=sec.split.value_counts().to_dict(),
  pstar=PSTAR,C_grid=CGRID,selected_C={n:res[n]['C'] for n in MODELS},seed=SEED,B=B,boot_failures=fails,boot_fail_rate=fails/B,
  labels_thresholds_recomputed=False,sri_lanka_coeffs_used=False,output_sha256={o:sh(f'{OUT}/{o}') for o in outs})
json.dump(meta,open(f'{OUT}/colombia_model_ladder_h4_75pct_v1.meta.json','w'),indent=2)
# console summary
M=pd.DataFrame(metrics); Mt=M[(M.calib=='recal')]
print('selected C:',{n:res[n]['C'] for n in MODELS})
print('val logloss:',{n:round(res[n]['vll'],4) for n in MODELS})
print('\nTEST (recal):')
print(Mt[['model','AUC','PR_AUC','Brier','CITL','slope','NB_p30']].round(4).to_string(index=False))
print('\ncontrasts vs M1 (test):'); print(pd.DataFrame(contrasts).round(4).to_string(index=False))
print('\nbootstrap (B=%d, failures=%d):'%(B,fails)); print(boot_df.round(4).to_string(index=False))
print('\nsecondary M2/M3 climate-full:'); print(pd.DataFrame(sec_metrics).round(4).to_string(index=False))
print('\ntest prevalence:',round(yte.mean(),4))
