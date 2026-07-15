# Colombia inverse-probability-weighted (IPW) selection-bias sensitivity for the matched
# climate increment. Model P(common-complete inclusion) from variables observed for BOTH
# included and excluded test-period municipality-weeks (department, year, seasonality),
# then recompute the matched contrast with stabilized IPW weights that reweight the
# analysed subset toward the full available test-period panel.
import pandas as pd, numpy as np, json
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import log_loss
np.random.seed(20260612); Q="/home/mpcrlab/data_quarantine/"
RUN="/home/mpcrlab/srilanka-dengue-ews-calibration/analysis/v12_referee_response/run/"
d=pd.read_csv(Q+"colombia_label_features_v1/colombia_modeling_table_h4_75pct_v1.csv")
d['dept']=d.GID_2.str.split('.').str[1]; d['yr']=d['week_start'].astype(str).str[:4].astype(int)
SEA=['sin_woy_1','cos_woy_1','sin_woy_2','cos_woy_2']; CAS=['cases_lag0','cases_lag1','cases_lag2','cases_lag4']
cc=d[d.common_complete_M1_to_M5_h4==True].reset_index(drop=True); y=cc.label_h4.values.astype(int)

# ---- 1) inclusion model on the FULL test-period panel (included + excluded) ----
tp=d[d.yr.isin([2020,2021,2022])].copy()
tp['incl']=tp.common_complete_M1_to_M5_h4.astype(int)
# covariates available for ALL rows: department dummies, year, seasonal harmonics
depts=sorted(tp['dept'].unique())
def Zmat(df):
    Z=[df['yr'].values.astype(float)]+[df[c].values for c in SEA]
    Z+=[(df['dept'].values==x).astype(float) for x in depts]
    return np.column_stack(Z)
Ztp=Zmat(tp); sc=StandardScaler().fit(Ztp[:,:5])
Ztp[:, :5]=sc.transform(Ztp[:,:5])
m_incl=LogisticRegression(C=1.0,max_iter=3000).fit(Ztp,tp['incl'].values)
tp['p_incl']=np.clip(m_incl.predict_proba(Ztp)[:,1],1e-3,1-1e-3)
print(f"[inclusion model] mean P(incl) among included={tp.loc[tp.incl==1,'p_incl'].mean():.3f}, excluded={tp.loc[tp.incl==0,'p_incl'].mean():.3f}; overall inclusion rate={tp.incl.mean():.3f}")

# ---- 2) map inclusion prob onto the common-complete rows (cc) ----
key=['GID_2','week_start']
pmap=tp.set_index(key)['p_incl']
cc_key=list(zip(cc.GID_2,cc.week_start))
p_incl_cc=np.array([pmap.get(k,np.nan) for k in cc_key])
# stabilized IPW weights, truncated at 1st/99th pct
pi=tp.incl.mean()
w=pi/p_incl_cc
w=np.clip(w,np.nanpercentile(w,1),np.nanpercentile(w,99)); w=w/np.nanmean(w)
print(f"[weights] range {np.nanmin(w):.2f}-{np.nanmax(w):.2f}, mean {np.nanmean(w):.2f}")

# ---- 3) frozen pipeline predictions for M5 and matched on cc test set ----
def X(idx,parts,tr):
    M=[np.log1p(cc.loc[idx,c].values) for c in CAS] if 'cases' in parts else []
    if 'clim' in parts: M+=[np.log1p(cc.loc[idx,f'precip_lag{l}'].values) for l in range(9)]+[cc.loc[idx,f'temp_lag{l}'].values for l in range(9)]
    if 'sea' in parts: M+=[cc.loc[idx,c].values for c in SEA]
    A=np.column_stack(M)
    if 'dept' in parts:
        dp=sorted(cc.loc[tr,'dept'].unique()); A=np.column_stack([A]+[(cc.loc[idx,'dept'].values==x).astype(float) for x in dp])
    return A
def predict(parts,tr,va,te):
    sc=StandardScaler().fit(X(tr,parts,tr)); best=None
    for C in [0.03,0.1,0.3,1,3]:
        mm=LogisticRegression(C=C,max_iter=2500).fit(sc.transform(X(tr,parts,tr)),y[tr])
        pp=np.clip(mm.predict_proba(sc.transform(X(va,parts,tr)))[:,1],1e-6,1-1e-6); ll=log_loss(y[va],pp,labels=[0,1])
        best=(ll,mm) if best is None or ll<best[0] else best
    mm=best[1]; pv=np.clip(mm.predict_proba(sc.transform(X(va,parts,tr)))[:,1],1e-6,1-1e-6); pt=np.clip(mm.predict_proba(sc.transform(X(te,parts,tr)))[:,1],1e-6,1-1e-6)
    pl=LogisticRegression(C=1e6,max_iter=1000).fit(np.log(pv/(1-pv)).reshape(-1,1),y[va]); return pl.predict_proba(np.log(pt/(1-pt)).reshape(-1,1))[:,1]
iy=lambda ys: cc.index[cc.yr.isin(ys)].values
tr0,va0,te0=iy(range(2006,2018)),iy([2018,2019]),iy([2020,2021,2022])
p5=predict({'cases','clim','sea','dept'},tr0,va0,te0); pm=predict({'cases','sea','dept'},tr0,va0,te0)
yte=y[te0]; wte=w  # cc is exactly te0 rows (all cc are... check: te0 subset of cc). map w to te0 rows:
# cc index==te0 positions: te0 are indices into cc for yr>=2020; align w (built over cc order) to te0
wte=w[te0]
def nb_w(p,yy,ww,t=0.30):
    a=p>=t; W=ww.sum()
    return (ww[a&(yy==1)].sum())/W - (ww[a&(yy==0)].sum())/W*(t/(1-t))
def nb(p,yy,t=0.30): a=p>=t;n=len(yy);return (a&(yy==1)).sum()/n-(a&(yy==0)).sum()/n*(t/(1-t))
unw=nb(p5,yte)-nb(pm,yte)
ipw=nb_w(p5,yte,wte)-nb_w(pm,yte,wte)
# cluster bootstrap (dept) for IPW estimate
dep=cc.loc[te0,'dept'].values; uq=np.array(sorted(set(dep))); byd={u:np.where(dep==u)[0] for u in uq}; rng=np.random.default_rng(20260612)
D=[]
for _ in range(1000):
    ii=np.concatenate([byd[u] for u in rng.choice(uq,len(uq),True)])
    D.append(nb_w(p5[ii],yte[ii],wte[ii])-nb_w(pm[ii],yte[ii],wte[ii]))
ci=[float(np.percentile(D,2.5)),float(np.percentile(D,97.5))]
res={'unweighted_matched':float(unw),'ipw_matched':float(ipw),'ipw_ci':ci,
     'inclusion_auc_note':'inclusion modeled from dept+year+seasonality (observed for all rows); reporting-density completeness not fully captured',
     'weight_range':[float(np.nanmin(w)),float(np.nanmax(w))]}
json.dump(res,open(RUN+"ipw_results.json","w"),indent=2)
print(f"\n[RESULT] matched increment: unweighted {unw:+.4f}  |  IPW-weighted {ipw:+.4f}  95% CI {ci}")
print("DONE")
