import pandas as pd, numpy as np, json
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler, SplineTransformer
from sklearn.metrics import log_loss
np.random.seed(20260612); Q="/home/mpcrlab/data_quarantine/"
d=pd.read_csv(Q+"colombia_label_features_v1/colombia_modeling_table_h4_75pct_v1.csv")
d['dept']=d.GID_2.str.split('.').str[1]; d['yr']=d['week_start'].astype(str).str[:4].astype(int)
cc=d[d.common_complete_M1_to_M5_h4==True].reset_index(drop=True); y=cc.label_h4.values.astype(int)
SEA=['sin_woy_1','cos_woy_1','sin_woy_2','cos_woy_2']
def nb(p,yy,t=0.30): a=p>=t; n=len(yy); return (a&(yy==1)).sum()/n-(a&(yy==0)).sum()/n*(t/(1-t))
_CB=None  # global cross-basis over ALL cc rows, value-spline fit on train (set after tr0 defined)
def build_global_cb(tr):
    global _CB
    mats=[]
    for var in ['temp','precip']:
        V=cc[[f'{var}_lag{l}' for l in range(9)]].values.astype(float)
        if var=='precip': V=np.log1p(V)
        vt=SplineTransformer(degree=3,n_knots=4,include_bias=False).fit(V[tr].reshape(-1,1))
        Blag=SplineTransformer(degree=2,n_knots=3,include_bias=False).fit_transform(np.arange(9).reshape(-1,1))
        kval=vt.transform(V[:1,:1]).shape[1]; klag=Blag.shape[1]; cb=np.zeros((len(cc),kval*klag))
        for l in range(9):
            Bv=vt.transform(V[:,l:l+1])
            for i in range(kval):
                for j in range(klag): cb[:,i*klag+j]+=Bv[:,i]*Blag[l,j]
        mats.append(cb)
    _CB=np.hstack(mats)
def Xmat(idx,parts,tr,case_cols,dlnm=False):
    M=[]
    if 'cases' in parts: M+=[np.log1p(cc.loc[idx,c].values) for c in case_cols]
    if 'clim' in parts:
        if dlnm:
            M+=[_CB[idx][:,k] for k in range(_CB.shape[1])]
        else:
            M+=[np.log1p(cc.loc[idx,f'precip_lag{l}'].values) for l in range(9)]+[cc.loc[idx,f'temp_lag{l}'].values for l in range(9)]
    if 'sea' in parts: M+=[cc.loc[idx,c].values for c in SEA]
    A=np.column_stack(M) if M else np.zeros((len(idx),1))
    if 'dept' in parts:
        depts=sorted(cc.loc[tr,'dept'].unique()); A=np.column_stack([A]+[(cc.loc[idx,'dept'].values==x).astype(float) for x in depts])
    return A
def predict(parts,tr,va,te,case_cols,dlnm=False,ctune=True):
    Xtr,Xva,Xte=Xmat(tr,parts,tr,case_cols,dlnm),Xmat(va,parts,tr,case_cols,dlnm),Xmat(te,parts,tr,case_cols,dlnm)
    sc=StandardScaler().fit(Xtr); Xtr,Xva,Xte=sc.transform(Xtr),sc.transform(Xva),sc.transform(Xte)
    best=None
    for C in ([0.01,0.1,1,3] if ctune else [1.0]):
        m=LogisticRegression(C=C,max_iter=2500).fit(Xtr,y[tr]); p=np.clip(m.predict_proba(Xva)[:,1],1e-6,1-1e-6)
        ll=log_loss(y[va],p,labels=[0,1]); best=(ll,m) if best is None or ll<best[0] else best
    m=best[1]; pva=np.clip(m.predict_proba(Xva)[:,1],1e-6,1-1e-6); pte=np.clip(m.predict_proba(Xte)[:,1],1e-6,1-1e-6)
    pl=LogisticRegression(C=1e6,max_iter=1000).fit(np.log(pva/(1-pva)).reshape(-1,1),y[va])
    return pl.predict_proba(np.log(pte/(1-pte)).reshape(-1,1))[:,1]
def bootci(pa,pb,te):
    dep=cc.loc[te,'dept'].values; uq=np.array(sorted(set(dep))); byd={u:np.where(dep==u)[0] for u in uq}
    rng=np.random.default_rng(20260612); yte=y[te]; ds=[]
    for _ in range(1000):
        ii=np.concatenate([byd[u] for u in rng.choice(uq,len(uq),replace=True)]); ds.append(nb(pa[ii],yte[ii])-nb(pb[ii],yte[ii]))
    return float(np.percentile(ds,2.5)),float(np.percentile(ds,97.5))
def iy(years): return cc.index[cc.yr.isin(years)].values
CAS=['cases_lag0','cases_lag1','cases_lag2','cases_lag4']
tr0,va0,te0=iy(range(2006,2018)),iy([2018,2019]),iy([2020,2021,2022]); yte0=y[te0]
build_global_cb(tr0)
R={}
# sanity
pM1=predict({'cases'},tr0,va0,te0,CAS); pM5=predict({'cases','clim','sea','dept'},tr0,va0,te0,CAS)
print("SANITY M5-M1=%+.4f"%(nb(pM5,yte0)-nb(pM1,yte0)))
pMatch=predict({'cases','sea','dept'},tr0,va0,te0,CAS)
print("frozen-split matched climate M5-matched=%+.4f"%(nb(pM5,yte0)-nb(pMatch,yte0)))
# ---- A2 matched under DLNM ----
pM5d=predict({'cases','clim','sea','dept'},tr0,va0,te0,CAS,dlnm=True)
a2=nb(pM5d,yte0)-nb(pMatch,yte0); a2ci=bootci(pM5d,pMatch,te0)
R['A2_matched_dlnm']={'M5dlnm_minus_matched':a2,'ci':a2ci,'NB_M5dlnm':nb(pM5d,yte0),'NB_matched':nb(pMatch,yte0)}
print("[A2 matched, DLNM] M5dlnm-matched = %+.4f %s (linear matched was +0.0078)"%(a2,a2ci))
# ---- A3 matched under reporting delay, depth curve ----
depths={'full':['cases_lag0','cases_lag1','cases_lag2','cases_lag4'],'drop0':['cases_lag1','cases_lag2','cases_lag4'],
        'drop0_1':['cases_lag2','cases_lag4'],'drop0_1_2':['cases_lag4']}
a3={}
for name,cols in depths.items():
    pm1=predict({'cases'},tr0,va0,te0,cols); pmat=predict({'cases','sea','dept'},tr0,va0,te0,cols); pm5=predict({'cases','clim','sea','dept'},tr0,va0,te0,cols)
    a3[name]={'NB_M1':nb(pm1,yte0),'M5-M1':nb(pm5,yte0)-nb(pm1,yte0),'M5-matched':nb(pm5,yte0)-nb(pmat,yte0)}
    if name=='drop0_1': a3[name]['M5-matched_ci']=bootci(pm5,pmat,te0)
R['A3_matched_delaycurve']=a3
print("[A3 matched delay curve]")
for k,v in a3.items(): print("   %-9s NB_M1=%.4f  M5-M1=%+.4f  M5-matched=%+.4f %s"%(k,v['NB_M1'],v['M5-M1'],v['M5-matched'],v.get('M5-matched_ci','')))
# ---- A1 single pre-specified split: train<=2015, val 2016-17, test 2018-19; matched contrast + CI ----
trA,vaA,teA=iy(range(2006,2016)),iy([2016,2017]),iy([2018,2019]); yteA=y[teA]
pm5A=predict({'cases','clim','sea','dept'},trA,vaA,teA,CAS); pmatA=predict({'cases','sea','dept'},trA,vaA,teA,CAS); pm1A=predict({'cases'},trA,vaA,teA,CAS)
a1=nb(pm5A,yteA)-nb(pmatA,yteA); a1ci=bootci(pm5A,pmatA,teA)
R['A1_matched_prepandemic_single']={'split':'train<=2015/val2016-17/test2018-19','M5-matched':a1,'ci':a1ci,'M5-M1':nb(pm5A,yteA)-nb(pm1A,yteA),'test_prev':float(yteA.mean())}
print("[A1 matched, single pre-pandemic split] M5-matched = %+.4f %s  (M5-M1 %+.4f; test prev %.3f)"%(a1,a1ci,nb(pm5A,yteA)-nb(pm1A,yteA),yteA.mean()))
json.dump(R,open("/home/mpcrlab/srilanka-dengue-ews-calibration/analysis/path_b_matched_fixed_effects_original_pipeline/run/matched_robustness_results.json","w"),indent=2)
print("DONE")
