#!/usr/bin/env python3
"""Path B Stage 2 — matched fixed-effects decomposition in the EXACT original Colombia pipeline.
Reuses the original design/fit_select/platt/nb logic verbatim; adds ONLY M5_no_climate_matched=['cases','season','dept']
(= M5 minus the 18 climate columns). Reproduces M5-M1 (Gate A), then decomposes +0.0188 via a paired GID_2
cluster bootstrap (seed 20260612, B=1000). Read-only inputs; writes only under this run/ dir. No manuscript touched."""
import pandas as pd, numpy as np, json, hashlib, os, warnings
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, brier_score_loss, log_loss
import statsmodels.api as sm
warnings.filterwarnings('ignore'); np.random.seed(20260612)
LF='/home/mpcrlab/data_quarantine/colombia_label_features_v1'
OUT=os.path.dirname(os.path.abspath(__file__))
SRC=f'{LF}/colombia_modeling_table_h4_75pct_v1.csv'
PSTAR=0.30; CGRID=[0.001,0.003,0.01,0.03,0.1,0.3,1,3,10]; SEED=20260612; B=1000
d=pd.read_csv(SRC,dtype={'week_start':str})
d['dept']=d.GID_2.str.split('.').str[1]
PRE=[f'precip_lag{k}' for k in range(9)]; TMP=[f'temp_lag{k}' for k in range(9)]
CAS=['cases_lag0','cases_lag1','cases_lag2','cases_lag4']; SEA=['sin_woy_1','cos_woy_1','sin_woy_2','cos_woy_2']

def design(df, feats, scaler=None, dept_cats=None):     # verbatim from original
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

# ONLY addition: the matched baseline (M5 minus climate)
MODELS={'M1':['cases'],'M4':['cases','climate'],'M5':['cases','climate','season','dept'],
        'M5_no_climate_matched':['cases','season','dept']}

def fit_select(tr,va,feats):
    Xtr,sc,dc=design(tr,feats); Xva,_,_=design(va,feats,sc,dc)
    ytr=tr.label_h4.values; yva=va.label_h4.values; best=None
    for C in CGRID:
        m=LogisticRegression(C=C,penalty='l2',solver='lbfgs',max_iter=5000).fit(Xtr,ytr)
        p=np.clip(m.predict_proba(Xva)[:,1],1e-6,1-1e-6); ll=log_loss(yva,p,labels=[0,1])
        if best is None or ll<best[0]: best=(ll,C,m)
    return best[2],best[1],best[0],sc,dc,list(Xtr.columns)
def logit(p): p=np.clip(p,1e-6,1-1e-6); return np.log(p/(1-p))
def platt(p_va,y_va):
    lr=LogisticRegression(C=1e6,solver='lbfgs',max_iter=1000); lr.fit(logit(p_va).reshape(-1,1),y_va); return lr
def apply_platt(lr,p): return lr.predict_proba(logit(p).reshape(-1,1))[:,1]
def nb(y,p,t):
    pos=p>=t; n=len(y); tp=np.sum(pos&(y==1)); fp=np.sum(pos&(y==0)); return tp/n-(fp/n)*(t/(1-t))
def citl_slope(y,p):
    lp=logit(p)
    try: citl=float(sm.Logit(y,np.ones_like(lp),offset=lp).fit(disp=0).params[0])
    except Exception: citl=np.nan
    try: slope=float(sm.Logit(y,sm.add_constant(lp)).fit(disp=0).params[1])
    except Exception: slope=np.nan
    return citl,slope

prim=d[d.common_complete_M1_to_M5_h4==True].copy()
assert prim['split'].value_counts().to_dict()=={'train':53711,'val':12713,'test':13361}, "row-count drift"
tr=prim[prim.split=='train']; va=prim[prim.split=='val']; te=prim[prim.split=='test']
yte=te.label_h4.values; res={}; cols_by={}
for name,feats in MODELS.items():
    m,C,vll,sc,dc,cols=fit_select(tr,va,feats)
    praw_va=np.clip(m.predict_proba(design(va,feats,sc,dc)[0])[:,1],1e-6,1-1e-6)
    praw=np.clip(m.predict_proba(design(te,feats,sc,dc)[0])[:,1],1e-6,1-1e-6)
    prec=apply_platt(platt(praw_va,va.label_h4.values),praw)
    ci,sl=citl_slope(yte,prec)
    res[name]=dict(praw=praw,prec=prec,C=C,AUC=roc_auc_score(yte,praw),NB=nb(yte,prec,PSTAR),
                   Brier=brier_score_loss(yte,prec),CITL=ci,slope=sl,nfeat=len(cols)); cols_by[name]=cols

# Gate B: matched differs from M5 only by the 18 climate columns
climate_cols=set(PRE+TMP)
removed=sorted(set(cols_by['M5'])-set(cols_by['M5_no_climate_matched']))
extra=sorted(set(cols_by['M5_no_climate_matched'])-set(cols_by['M5']))
gateB = (set(removed)==climate_cols) and (len(extra)==0)
open(f'{OUT}/path_b_design_matrix_columns.txt','w').write(
    "M5 cols:\n"+"\n".join(cols_by['M5'])+"\n\nMATCHED cols:\n"+"\n".join(cols_by['M5_no_climate_matched'])+
    f"\n\nREMOVED (M5 - matched): {removed}\nEXTRA: {extra}\nGATE_B_only_climate_differs={gateB}\n")

# point estimates & decomposition
def dnb(a,b): return res[a]['NB']-res[b]['NB']
pt={'NB_M1':res['M1']['NB'],'NB_matched':res['M5_no_climate_matched']['NB'],'NB_M5':res['M5']['NB'],'NB_M4':res['M4']['NB'],
    'dNB_M5_M1':dnb('M5','M1'),'dNB_M4_M1':dnb('M4','M1'),
    'dNB_nonclimate_matched_M1':dnb('M5_no_climate_matched','M1'),
    'dNB_climate_M5_matched':dnb('M5','M5_no_climate_matched'),
    'dAUC_M5_M1':res['M5']['AUC']-res['M1']['AUC']}
pt['decomp_sum_check']=pt['dNB_nonclimate_matched_M1']+pt['dNB_climate_M5_matched']-pt['dNB_M5_M1']

# paired GID_2 cluster bootstrap (seed, B, method identical to original)
units=te.GID_2.values; uniq=np.array(sorted(set(units))); idx_by={u:np.where(units==u)[0] for u in uniq}
rng=np.random.default_rng(SEED)
dist={k:[] for k in ['dNB_M5_M1','dNB_M4_M1','dNB_nonclimate_matched_M1','dNB_climate_M5_matched','dAUC_M5_M1']}
fails=0
for b in range(B):
    samp=rng.choice(uniq,size=len(uniq),replace=True); bi=np.concatenate([idx_by[u] for u in samp]); yb=yte[bi]
    if len(np.unique(yb))<2: fails+=1; continue
    N={n:nb(yb,res[n]['prec'][bi],PSTAR) for n in MODELS}
    dist['dNB_M5_M1'].append(N['M5']-N['M1']); dist['dNB_M4_M1'].append(N['M4']-N['M1'])
    dist['dNB_nonclimate_matched_M1'].append(N['M5_no_climate_matched']-N['M1'])
    dist['dNB_climate_M5_matched'].append(N['M5']-N['M5_no_climate_matched'])
    dist['dAUC_M5_M1'].append(roc_auc_score(yb,res['M5']['praw'][bi])-roc_auc_score(yb,res['M1']['praw'][bi]))
def ci(a): a=np.array(a); return float(np.percentile(a,2.5)),float(np.median(a)),float(np.percentile(a,97.5))
boot={k:ci(v) for k,v in dist.items()}
pd.DataFrame(dist).to_csv(f'{OUT}/path_b_bootstrap_distribution.csv',index=False)

# Gate A: reproduce frozen M5-M1 = +0.018775 within 0.001
gateA = abs(pt['dNB_M5_M1']-0.018775)<=0.001
summary=dict(gateA_reproduced=bool(gateA), gateB_only_climate_differs=bool(gateB),
    point=pt, bootstrap_ci={k:{'lo':v[0],'med':v[1],'hi':v[2]} for k,v in boot.items()},
    boot_B=B, boot_failures=fails, selected_C={n:res[n]['C'] for n in MODELS},
    nfeat={n:res[n]['nfeat'] for n in MODELS}, test_prevalence=float(yte.mean()))
json.dump(summary,open(f'{OUT}/path_b_point_estimates.json','w'),indent=2,default=float)
pd.DataFrame([{'model':n,**{k:res[n][k] for k in ['C','nfeat','AUC','NB','Brier','CITL','slope']}} for n in MODELS]
    ).to_csv(f'{OUT}/path_b_model_summary.csv',index=False)
pd.DataFrame([{'contrast':k,'point':pt[k],'lo':boot.get(k,(np.nan,)*3)[0],'med':boot.get(k,(np.nan,)*3)[1],
    'hi':boot.get(k,(np.nan,)*3)[2]} for k in ['dNB_M5_M1','dNB_M4_M1','dNB_nonclimate_matched_M1','dNB_climate_M5_matched','dAUC_M5_M1']]
    ).to_csv(f'{OUT}/path_b_bootstrap_summary.csv',index=False)

print("=== GATE A (reproduce frozen M5-M1=+0.018775 ±0.001) ===")
print(f"  dNB(M5-M1)@.30 = {pt['dNB_M5_M1']:+.5f}   dAUC(M5-M1)={pt['dAUC_M5_M1']:+.4f}   -> GATE A {'PASS' if gateA else 'FAIL'}")
print(f"  bootstrap dNB(M5-M1) 95% CI = [{boot['dNB_M5_M1'][0]:+.4f}, {boot['dNB_M5_M1'][2]:+.4f}] (frozen [+0.0117,+0.0260])")
print("\n=== GATE B (M5 vs matched differ ONLY by 18 climate cols) ===")
print(f"  removed={removed[:3]}...({len(removed)})  only_climate={gateB}")
print("\n=== DECOMPOSITION of +0.0188 (point, and paired 95% CI) ===")
for k,lab in [('dNB_M5_M1','M5 - M1 (original)'),('dNB_nonclimate_matched_M1','matched - M1 (non-climate: season+deptFE)'),
              ('dNB_climate_M5_matched','M5 - matched (CLIMATE, net of season+deptFE)'),('dNB_M4_M1','M4 - M1 (climate on cases, NO FE) [separate]')]:
    lo,md,hi=boot[k]; print(f"  {lab:52s} {pt[k]:+.5f}  [{lo:+.4f}, {hi:+.4f}]")
print(f"\n  decomposition sum check (nonclimate+climate - original) = {pt['decomp_sum_check']:+.6f} (≈0)")
print(f"  NB: M1={res['M1']['NB']:+.4f}  matched={res['M5_no_climate_matched']['NB']:+.4f}  M5={res['M5']['NB']:+.4f}  M4={res['M4']['NB']:+.4f}")
print(f"  boot failures={fails}, test prevalence={yte.mean():.4f}")
# hash outputs
outs=['path_b_point_estimates.json','path_b_model_summary.csv','path_b_bootstrap_summary.csv','path_b_bootstrap_distribution.csv','path_b_design_matrix_columns.txt']
open(f'{OUT}/path_b_predictions_checksums.sha256','w').write("\n".join(f"{hashlib.sha256(open(f'{OUT}/{o}','rb').read()).hexdigest()}  {o}" for o in outs)+"\n")
print("\nDONE")
