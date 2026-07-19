import pandas as pd, numpy as np, json
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
np.random.seed(20260612)
Q="/home/mpcrlab/data_quarantine/"; FIG="/home/mpcrlab/srilanka-dengue-ews-calibration/manuscript/paper1_validity_corrected_candidate/"
RUN="/home/mpcrlab/srilanka-dengue-ews-calibration/analysis/v12_referee_response/run/"
SEA=['sin_woy_1','cos_woy_1','sin_woy_2','cos_woy_2']; CAS=['cases_lag0','cases_lag1','cases_lag2','cases_lag4']
MOD={'M1':{'cases'},'matched':{'cases','sea','dept'},'M5':{'cases','clim','sea','dept'}}
def nb(p,yy,t=0.30): a=p>=t;n=len(yy);return (a&(yy==1)).sum()/n-(a&(yy==0)).sum()/n*(t/(1-t))
def X(df,idx,parts,tr):
    M=[np.log1p(df.loc[idx,c].values) for c in CAS] if 'cases' in parts else []
    if 'clim' in parts: M+=[np.log1p(df.loc[idx,f'precip_lag{l}'].values) for l in range(9)]+[df.loc[idx,f'temp_lag{l}'].values for l in range(9)]
    if 'sea' in parts: M+=[df.loc[idx,c].values for c in SEA]
    A=np.column_stack(M)
    if 'dept' in parts:
        dp=sorted(df.loc[tr,'dept'].unique()); A=np.column_stack([A]+[(df.loc[idx,'dept'].values==x).astype(float) for x in dp])
    return A
def fp(df,y,parts,tr,va,te):
    sc=StandardScaler().fit(X(df,tr,parts,tr)); m=LogisticRegression(C=1.0,max_iter=1500).fit(sc.transform(X(df,tr,parts,tr)),y[tr])
    pv=np.clip(m.predict_proba(sc.transform(X(df,va,parts,tr)))[:,1],1e-6,1-1e-6); pt=np.clip(m.predict_proba(sc.transform(X(df,te,parts,tr)))[:,1],1e-6,1-1e-6)
    pl=LogisticRegression(C=1e6,max_iter=800).fit(np.log(pv/(1-pv)).reshape(-1,1),y[va]); return pl.predict_proba(np.log(pt/(1-pt)).reshape(-1,1))[:,1]
dh=pd.read_csv(Q+"colombia_label_features_v1/colombia_modeling_table_all_horizons_v1.csv")
dh['dept']=dh.GID_2.str.split('.').str[1]; dh['yr']=dh['week_start'].astype(str).str[:4].astype(int)
hor={}
for h in [1,2,4,8,12]:
    lab=f'label_h{h}'; sub=dh[(dh['common_complete_M1_to_M5_h4']==True)&(dh[lab].notna())].reset_index(drop=True)
    y=sub[lab].values.astype(int); tr=sub.index[sub.yr<=2017].values; va=sub.index[sub.yr.isin([2018,2019])].values; te=sub.index[sub.yr>=2020].values
    if len(te)<200 or len(np.unique(y[te]))<2: continue
    p5=fp(sub,y,MOD['M5'],tr,va,te); pm=fp(sub,y,MOD['matched'],tr,va,te); yt=y[te]
    dep=sub.loc[te,'dept'].values; uq=np.array(sorted(set(dep))); byd={u:np.where(dep==u)[0] for u in uq}; rng=np.random.default_rng(20260612)
    D=[]
    for _ in range(400):
        ii=np.concatenate([byd[u] for u in rng.choice(uq,len(uq),True)]); D.append(nb(p5[ii],yt[ii])-nb(pm[ii],yt[ii]))
    hor[h]={'matched':float(nb(p5,yt)-nb(pm,yt)),'ci':[float(np.percentile(D,2.5)),float(np.percentile(D,97.5))],'n':int(len(te)),'prev':float(yt.mean())}
    print(f"h={h} matched {hor[h]['matched']:+.4f} {hor[h]['ci']}",flush=True)
hs=sorted(hor); fig,ax=plt.subplots(figsize=(5.6,3.6))
ax.errorbar(hs,[hor[h]['matched'] for h in hs],yerr=[[hor[h]['matched']-hor[h]['ci'][0] for h in hs],[hor[h]['ci'][1]-hor[h]['matched'] for h in hs]],fmt='-o',capsize=3,color='C0',label='M5$-$matched (climate-specific)')
ax.axhline(0,color='k',lw=.6); ax.set_xlabel('Horizon (weeks)'); ax.set_ylabel('$\\Delta$NB(M5$-$matched) at $p^*=0.30$'); ax.set_title('Colombia matched climate increment vs horizon'); ax.legend(fontsize=7)
for h in hs: ax.annotate(f"n={hor[h]['n']}\nprev {hor[h]['prev']:.2f}",(h,ax.get_ylim()[0]),fontsize=6,ha='center',va='bottom',color='gray')
plt.tight_layout(); plt.savefig(FIG+"fig_co_horizon.pdf"); plt.close(); print("Fig 8 regenerated",flush=True)
d=pd.read_csv(Q+"colombia_label_features_v1/colombia_modeling_table_h4_75pct_v1.csv")
d['dept']=d.GID_2.str.split('.').str[1]; d['yr']=d['week_start'].astype(str).str[:4].astype(int)
cc=d[d.common_complete_M1_to_M5_h4==True].reset_index(drop=True); y=cc.label_h4.values.astype(int)
tr0=cc.index[cc.yr<=2017].values; va0=cc.index[cc.yr.isin([2018,2019])].values; te0=cc.index[cc.yr>=2020].values
pt=nb(fp(cc,y,MOD['M5'],tr0,va0,te0),y[te0])-nb(fp(cc,y,MOD['matched'],tr0,va0,te0),y[te0])
depts=np.array(sorted(cc['dept'].unique())); rng=np.random.default_rng(20260612); nest=[]
for _ in range(200):
    rows=np.concatenate([cc.index[cc['dept']==dp].values for dp in rng.choice(depts,len(depts),True)])
    bd=cc.loc[rows].reset_index(drop=True); yb=bd.label_h4.values.astype(int)
    trb=bd.index[bd.yr<=2017].values; vab=bd.index[bd.yr.isin([2018,2019])].values; teb=bd.index[bd.yr>=2020].values
    if len(teb)<100 or len(np.unique(yb[teb]))<2 or len(np.unique(yb[vab]))<2: continue
    try: nest.append(nb(fp(bd,yb,MOD['M5'],trb,vab,teb),yb[teb])-nb(fp(bd,yb,MOD['matched'],trb,vab,teb),yb[teb]))
    except Exception: pass
nest=np.array(nest)
json.dump({'horizon_matched':hor,'nested':{'point':float(pt),'n':int(len(nest)),'ci':[float(np.percentile(nest,2.5)),float(np.percentile(nest,97.5))]}},open(RUN+"woz_results.json","w"),indent=2)
print(f"NESTED matched point {pt:+.4f}; refit-inclusive 95% CI [{np.percentile(nest,2.5):+.4f},{np.percentile(nest,97.5):+.4f}] over {len(nest)} reps (conditional +0.0039 to +0.0119)",flush=True)
print("DONE")
