import pandas as pd, numpy as np, json, warnings
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import SplineTransformer
from sklearn.metrics import roc_auc_score
warnings.filterwarnings('ignore'); np.random.seed(20260612)
Q="/home/mpcrlab/data_quarantine/"; PSTAR=0.30; CGRID=[0.001,0.003,0.01,0.03,0.1,0.3,1,3,10]; B=1000
d=pd.read_csv(Q+"colombia_label_features_v1/colombia_modeling_table_h4_75pct_v1.csv")
d['dept']=d.GID_2.str.split('.').str[1]; d['yr']=d['week_start'].astype(str).str[:4].astype(int)
cc=d[d.common_complete_M1_to_M5_h4==True].reset_index(drop=True); y=cc.label_h4.values.astype(int)
PRE=[f'precip_lag{k}' for k in range(9)]; TMP=[f'temp_lag{k}' for k in range(9)]
CAS=['cases_lag0','cases_lag1','cases_lag2','cases_lag4']; SEA=['sin_woy_1','cos_woy_1','sin_woy_2','cos_woy_2']

def nb(p,yy,t=PSTAR):
    a=p>=t; n=len(yy); return (a&(yy==1)).sum()/n-(a&(yy==0)).sum()/n*(t/(1-t))
def crossbasis(idx_all, tr_mask, var, nval=4, nlag=3):
    """DLNM-style cross-basis for one variable over lags 0-8; value basis fit on TRAIN lag values."""
    cols=[f'{var}_lag{l}' for l in range(9)]; Xl=cc.loc[idx_all,cols].values
    vt=SplineTransformer(degree=3,n_knots=nval,include_bias=False).fit(Xl[tr_mask].reshape(-1,1))
    lt=SplineTransformer(degree=2,n_knots=nlag,include_bias=False)
    Blag=lt.fit_transform(np.arange(9).reshape(-1,1))            # 9 x klag
    kval=vt.transform(Xl[:1,:1]).shape[1]; klag=Blag.shape[1]
    cb=np.zeros((len(idx_all),kval*klag))
    for l in range(9):
        Bv=vt.transform(Xl[:,l:l+1])                            # n x kval
        for i in range(kval):
            for j in range(klag):
                cb[:,i*klag+j]+=Bv[:,i]*Blag[l,j]
    return cb

def build(feats, idx, tr_mask, extra_cb=None):
    X=pd.DataFrame(index=range(len(idx))); cont=[]
    sub=cc.loc[idx]
    if 'cases' in feats:
        for c in feats['cases']: X[c]=np.log1p(sub[c].values); cont.append(c)
    if 'climate' in feats:
        for c in PRE: X[c]=np.log1p(sub[c].values); cont.append(c)
        for c in TMP: X[c]=sub[c].values; cont.append(c)
    if 'season' in feats:
        for c in SEA: X[c]=sub[c].values
    if extra_cb is not None:
        for k in range(extra_cb.shape[1]): X[f'cb{k}']=extra_cb[:,k]; cont.append(f'cb{k}')
    Xv=X.values.astype(float)
    # standardize continuous on train
    mu=Xv[tr_mask].mean(0); sd=Xv[tr_mask].std(0); sd[sd==0]=1
    isc=[X.columns.get_loc(c) for c in cont]
    Xv[:,isc]=(Xv[:,isc]-mu[isc])/sd[isc]
    if 'dept' in feats:
        for dc in sorted(sub.loc[tr_mask,'dept'].unique() if False else cc.loc[idx][tr_mask]['dept'].unique()):
            pass
    return Xv, X.columns.tolist()

def fitpred(Xtr,ytr,Xva,yva,Xte):
    best=None
    for C in CGRID:
        m=LogisticRegression(C=C,penalty='l2',solver='lbfgs',max_iter=3000).fit(Xtr,ytr)
        from sklearn.metrics import log_loss
        p=np.clip(m.predict_proba(Xva)[:,1],1e-6,1-1e-6); ll=log_loss(yva,p,labels=[0,1])
        if best is None or ll<best[0]: best=(ll,m)
    m=best[1]
    pva=np.clip(m.predict_proba(Xva)[:,1],1e-6,1-1e-6); pte=np.clip(m.predict_proba(Xte)[:,1],1e-6,1-1e-6)
    pl=LogisticRegression(C=1e6,max_iter=1000).fit(np.log(pva/(1-pva)).reshape(-1,1),yva)
    return pl.predict_proba(np.log(pte/(1-pte)).reshape(-1,1))[:,1]

def design(sub_idx, feats, tr_idx, va_idx, te_idx, dlnm_vars=None, case_cols=CAS):
    """Return recalibrated test predictions for a model on given split."""
    allidx=np.concatenate([tr_idx,va_idx,te_idx]); pos={ix:i for i,ix in enumerate(allidx)}
    trm=np.array([True]*len(tr_idx)+[False]*len(va_idx)+[False]*len(te_idx))
    F={}
    if 'cases' in feats: F['cases']=case_cols
    if 'climate' in feats: F['climate']=True
    if 'season' in feats: F['season']=True
    cb=None
    if dlnm_vars:
        cbs=[crossbasis(allidx, trm, v) for v in dlnm_vars]; cb=np.hstack(cbs)
    Xv,cols=build(F, allidx, trm, extra_cb=cb)
    # dept dummies
    if 'dept' in feats:
        depts=sorted(cc.loc[tr_idx,'dept'].unique()); sub=cc.loc[allidx]
        D=np.column_stack([(sub['dept'].values==dc).astype(float) for dc in depts])
        Xv=np.hstack([Xv,D])
    ntr=len(tr_idx); nva=len(va_idx)
    ya=y[allidx]
    return fitpred(Xv[:ntr],ya[:ntr],Xv[ntr:ntr+nva],ya[ntr:ntr+nva],Xv[ntr+nva:])

def contrasts(preds, yte, teidx, pairs, boot_pairs=()):
    out={}
    for name,(a,b) in pairs.items():
        out[name]=nb(preds[a],yte)-nb(preds[b],yte)
    # dept bootstrap for selected pairs
    depts=cc.loc[teidx,'dept'].values; uniq=np.array(sorted(set(depts)))
    byd={u:np.where(depts==u)[0] for u in uniq}; rng=np.random.default_rng(20260612)
    ci={}
    for name in boot_pairs:
        a,b=pairs[name]; dist=[]
        for _ in range(B):
            ii=np.concatenate([byd[u] for u in rng.choice(uniq,len(uniq),replace=True)])
            dist.append(nb(preds[a][ii],yte[ii])-nb(preds[b][ii],yte[ii]))
        ci[name]=(float(np.percentile(dist,2.5)),float(np.percentile(dist,97.5)))
    return out,ci

def idx_years(years): return cc.index[cc.yr.isin(years)].values

# ================= SANITY: reproduce frozen +0.0188 on original split =================
tr0=idx_years(range(2006,2018)); te0=idx_years([2020,2021,2022]); va0=idx_years([2018,2019])
# NOTE frozen used train=2006-2017, val=2018-2019, test=2020-2022 (val is 2018-19)
pM1=design(None,{'cases':1},tr0,va0,te0); pM5=design(None,{'cases':1,'climate':1,'season':1,'dept':1},tr0,va0,te0)
yte0=y[te0]
print("SANITY ΔNB(M5-M1) on frozen split = %+.4f  (target +0.0188)  test n=%d prev=%.3f"%(nb(pM5,yte0)-nb(pM1,yte0),len(te0),yte0.mean()))

RES={}
# ================= A1: PRE-PANDEMIC holdout (train<=2016, val=2017, test 2018-2019) =================
trA=idx_years(range(2006,2017)); vaA=idx_years([2017]); teA=idx_years([2018,2019]); yteA=y[teA]
pr={}
pr['M1']=design(None,{'cases':1},trA,vaA,teA)
pr['matched']=design(None,{'cases':1,'season':1,'dept':1},trA,vaA,teA)
pr['M4']=design(None,{'cases':1,'climate':1},trA,vaA,teA)
pr['M5']=design(None,{'cases':1,'climate':1,'season':1,'dept':1},trA,vaA,teA)
pairs={'M5-M1':('M5','M1'),'M4-M1':('M4','M1'),'matched-M1':('matched','M1'),'M5-matched':('M5','matched')}
o,ci=contrasts(pr,yteA,teA,pairs,boot_pairs=['M5-M1','M5-matched'])
RES['A1_prepandemic']={'test_n':int(len(teA)),'prev':float(yteA.mean()),'NB':{k:float(nb(pr[k],yteA)) for k in pr},
    'contrasts':{k:float(v) for k,v in o.items()},'ci':ci}
print("\n[A1 PRE-PANDEMIC 2018-2019] test n=%d prev=%.3f"%(len(teA),yteA.mean()))
for k,v in o.items(): print("   %-11s %+.4f %s"%(k,v,ci.get(k,'')))

# ================= A2: DLNM cross-basis vs linear, original split, test 2020-2022 =================
pr2={'M1':pM1}
pr2['M4lin']=design(None,{'cases':1,'climate':1},tr0,va0,te0)
pr2['M5lin']=pM5
pr2['M4dlnm']=design(None,{'cases':1},tr0,va0,te0,dlnm_vars=['temp','precip'])  # cases + temp/precip cross-basis
pr2['M5dlnm']=design(None,{'cases':1,'season':1,'dept':1},tr0,va0,te0,dlnm_vars=['temp','precip'])
p2={'M4lin-M1':('M4lin','M1'),'M5lin-M1':('M5lin','M1'),'M4dlnm-M1':('M4dlnm','M1'),'M5dlnm-M1':('M5dlnm','M1')}
o2,ci2=contrasts(pr2,yte0,te0,p2,boot_pairs=['M5dlnm-M1','M4dlnm-M1'])
RES['A2_dlnm_no_humidity']={'note':'Colombia humidity unavailable; DLNM on temp+precip only (functional-form test)',
    'contrasts':{k:float(v) for k,v in o2.items()},'ci':ci2,'AUC':{k:float(roc_auc_score(yte0,pr2[k])) for k in pr2}}
print("\n[A2 DLNM vs LINEAR, test 2020-2022] (humidity unavailable -> temp+precip only)")
for k,v in o2.items(): print("   %-11s %+.4f %s"%(k,v,ci2.get(k,'')))

# ================= A3: reporting-delay (drop recent case lags), original split =================
pr3={'M5':pM5}
pr3['M1_full']=pM1
pr3['M1_delay1']=design(None,{'cases':1},tr0,va0,te0,case_cols=['cases_lag1','cases_lag2','cases_lag4'])   # drop lag0
pr3['M1_delay2']=design(None,{'cases':1},tr0,va0,te0,case_cols=['cases_lag2','cases_lag4'])                # drop lag0,1
p3={'M5-M1_full':('M5','M1_full'),'M5-M1_delay1':('M5','M1_delay1'),'M5-M1_delay2':('M5','M1_delay2')}
o3,ci3=contrasts(pr3,yte0,te0,p3,boot_pairs=['M5-M1_delay2'])
RES['A3_reporting_delay']={'NB_M1_full':float(nb(pM1,yte0)),'NB_M1_delay1':float(nb(pr3['M1_delay1'],yte0)),
    'NB_M1_delay2':float(nb(pr3['M1_delay2'],yte0)),'NB_M5':float(nb(pM5,yte0)),
    'contrasts':{k:float(v) for k,v in o3.items()},'ci':ci3}
print("\n[A3 REPORTING-DELAY] NB M1_full=%.4f M1_delay1(drop lag0)=%.4f M1_delay2(drop lag0,1)=%.4f  M5=%.4f"%(
    nb(pM1,yte0),nb(pr3['M1_delay1'],yte0),nb(pr3['M1_delay2'],yte0),nb(pM5,yte0)))
for k,v in o3.items(): print("   %-14s %+.4f %s"%(k,v,ci3.get(k,'')))

json.dump(RES,open("/home/mpcrlab/srilanka-dengue-ews-calibration/analysis/path_b_matched_fixed_effects_original_pipeline/run/recompute_three_results.json","w"),indent=2)
print("\nDONE")
