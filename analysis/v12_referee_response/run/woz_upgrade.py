# Wozniak-review rigor upgrades (Colombia data on disk):
#  (A) Horizon recomputed with the SAME tuned pipeline as the frozen +0.0188 reproduction,
#      so Figure 8 and the text agree (fixes the two-disagreeing-measurements problem at source),
#      with conditional cluster-bootstrap CIs.
#  (B) Development-inclusive ("nested") bootstrap for the matched increment DNB(M5 - matched):
#      refit models inside each cluster-resampled replicate -> interval that includes
#      training/refit uncertainty, not just conditional test-set sampling.
import pandas as pd, numpy as np, json
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import log_loss
np.random.seed(20260612)
Q="/home/mpcrlab/data_quarantine/"; FIG="/home/mpcrlab/srilanka-dengue-ews-calibration/manuscript/paper1_validity_corrected_candidate/"
RUN="/home/mpcrlab/srilanka-dengue-ews-calibration/analysis/v12_referee_response/run/"
SEA=['sin_woy_1','cos_woy_1','sin_woy_2','cos_woy_2']; CAS=['cases_lag0','cases_lag1','cases_lag2','cases_lag4']
MOD={'M1':{'cases'},'matched':{'cases','sea','dept'},'M4':{'cases','clim'},'M5':{'cases','clim','sea','dept'}}
def nb(p,yy,t=0.30): a=p>=t; n=len(yy); return (a&(yy==1)).sum()/n-(a&(yy==0)).sum()/n*(t/(1-t))

def build_X(df,idx,parts,tr_idx):
    M=[np.log1p(df.loc[idx,c].values) for c in CAS] if 'cases' in parts else []
    if 'clim' in parts: M+=[np.log1p(df.loc[idx,f'precip_lag{l}'].values) for l in range(9)]+[df.loc[idx,f'temp_lag{l}'].values for l in range(9)]
    if 'sea' in parts: M+=[df.loc[idx,c].values for c in SEA]
    A=np.column_stack(M)
    if 'dept' in parts:
        dp=sorted(df.loc[tr_idx,'dept'].unique()); A=np.column_stack([A]+[(df.loc[idx,'dept'].values==x).astype(float) for x in dp])
    return A
def fitpred(df,y,parts,tr,va,te,ct=True):
    sc=StandardScaler().fit(build_X(df,tr,parts,tr)); best=None
    for C in ([0.03,0.1,0.3,1,3] if ct else [1.0]):
        m=LogisticRegression(C=C,max_iter=2500).fit(sc.transform(build_X(df,tr,parts,tr)),y[tr])
        p=np.clip(m.predict_proba(sc.transform(build_X(df,va,parts,tr)))[:,1],1e-6,1-1e-6)
        ll=log_loss(y[va],p,labels=[0,1]); best=(ll,m) if best is None or ll<best[0] else best
    m=best[1]; pv=np.clip(m.predict_proba(sc.transform(build_X(df,va,parts,tr)))[:,1],1e-6,1-1e-6)
    pt=np.clip(m.predict_proba(sc.transform(build_X(df,te,parts,tr)))[:,1],1e-6,1-1e-6)
    pl=LogisticRegression(C=1e6,max_iter=1000).fit(np.log(pv/(1-pv)).reshape(-1,1),y[va])
    return pl.predict_proba(np.log(pt/(1-pt)).reshape(-1,1))[:,1]

# ---------- (A) tuned horizon ----------
dh=pd.read_csv(Q+"colombia_label_features_v1/colombia_modeling_table_all_horizons_v1.csv")
dh['dept']=dh.GID_2.str.split('.').str[1]; dh['yr']=dh['week_start'].astype(str).str[:4].astype(int)
H=[1,2,4,8,12]; hor={}
for h in H:
    lab=f'label_h{h}'; sub=dh[(dh['common_complete_M1_to_M5_h4']==True)&(dh[lab].notna())].reset_index(drop=True)
    y=sub[lab].values.astype(int); tr=sub.index[sub.yr<=2017].values; va=sub.index[sub.yr.isin([2018,2019])].values; te=sub.index[sub.yr>=2020].values
    if len(te)<200 or len(np.unique(y[te]))<2: continue
    p5=fitpred(sub,y,MOD['M5'],tr,va,te,ct=True); pm=fitpred(sub,y,MOD['matched'],tr,va,te,ct=True); p1=fitpred(sub,y,MOD['M1'],tr,va,te,ct=True)
    yt=y[te]; dep=sub.loc[te,'dept'].values; uq=np.array(sorted(set(dep))); byd={u:np.where(dep==u)[0] for u in uq}; rng=np.random.default_rng(20260612)
    def ci(pa,pb):
        D=[]
        for _ in range(500):
            ii=np.concatenate([byd[u] for u in rng.choice(uq,len(uq),True)]); D.append(nb(pa[ii],yt[ii])-nb(pb[ii],yt[ii]))
        return [float(np.percentile(D,2.5)),float(np.percentile(D,97.5))]
    hor[h]={'matched':nb(p5,yt)-nb(pm,yt),'matched_ci':ci(p5,pm),'compound':nb(p5,yt)-nb(p1,yt),'compound_ci':ci(p5,p1),'n':int(len(te)),'prev':float(yt.mean())}
    print(f"[A tuned horizon h={h}] matched {hor[h]['matched']:+.4f} {hor[h]['matched_ci']} | compound {hor[h]['compound']:+.4f} {hor[h]['compound_ci']}")
# regenerate Fig 8 (tuned)
hs=sorted(hor)
fig,ax=plt.subplots(figsize=(6,3.6))
ax.errorbar(hs,[hor[h]['matched'] for h in hs],yerr=[[hor[h]['matched']-hor[h]['matched_ci'][0] for h in hs],[hor[h]['matched_ci'][1]-hor[h]['matched'] for h in hs]],fmt='-o',capsize=3,label='M5$-$matched (climate)')
ax.errorbar([h+0.15 for h in hs],[hor[h]['compound'] for h in hs],yerr=[[hor[h]['compound']-hor[h]['compound_ci'][0] for h in hs],[hor[h]['compound_ci'][1]-hor[h]['compound'] for h in hs]],fmt='-s',capsize=3,label='M5$-$M1 (compound)')
ax.axhline(0,color='k',lw=.6); ax.set_xlabel('Horizon (weeks)'); ax.set_ylabel('$\\Delta$NB at $p^*=0.30$ (95\\% CI)'); ax.set_title('Colombia increment vs horizon (tuned pipeline)'); ax.legend(fontsize=7)
for h in hs: ax.annotate(f"n={hor[h]['n']}\nprev {hor[h]['prev']:.2f}",(h,ax.get_ylim()[0]),fontsize=5.5,ha='center',va='bottom',color='gray')
plt.tight_layout(); plt.savefig(FIG+"fig_co_horizon.pdf"); plt.close()

# ---------- (B) development-inclusive nested bootstrap for matched increment (h=4) ----------
d=pd.read_csv(Q+"colombia_label_features_v1/colombia_modeling_table_h4_75pct_v1.csv")
d['dept']=d.GID_2.str.split('.').str[1]; d['yr']=d['week_start'].astype(str).str[:4].astype(int)
cc=d[d.common_complete_M1_to_M5_h4==True].reset_index(drop=True); y=cc.label_h4.values.astype(int)
tr0=cc.index[cc.yr<=2017].values; va0=cc.index[cc.yr.isin([2018,2019])].values; te0=cc.index[cc.yr>=2020].values
# point estimate (tuned) for reference
p5=fitpred(cc,y,MOD['M5'],tr0,va0,te0); pm=fitpred(cc,y,MOD['matched'],tr0,va0,te0)
pt_point=nb(p5,y[te0])-nb(pm,y[te0])
depts_all=np.array(sorted(cc['dept'].unique()))
rng=np.random.default_rng(20260612); nested=[]
for b in range(300):
    samp=rng.choice(depts_all,len(depts_all),True)
    rows=np.concatenate([cc.index[cc['dept']==dp].values for dp in samp])
    bd=cc.loc[rows].reset_index(drop=True); yb=bd.label_h4.values.astype(int)
    trb=bd.index[bd.yr<=2017].values; vab=bd.index[bd.yr.isin([2018,2019])].values; teb=bd.index[bd.yr>=2020].values
    if len(teb)<100 or len(np.unique(yb[teb]))<2 or len(np.unique(yb[vab]))<2: continue
    try:
        p5b=fitpred(bd,yb,MOD['M5'],trb,vab,teb,ct=False); pmb=fitpred(bd,yb,MOD['matched'],trb,vab,teb,ct=False)
        nested.append(nb(p5b,yb[teb])-nb(pmb,yb[teb]))
    except Exception: pass
nested=np.array(nested)
res={'A_tuned_horizon':hor,
     'B_nested_bootstrap':{'point':float(pt_point),'n_reps':int(len(nested)),
        'ci95':[float(np.percentile(nested,2.5)),float(np.percentile(nested,97.5))],
        'note':'department cluster resample + refit (penalty not re-tuned); development-inclusive'}}
json.dump(res,open(RUN+"woz_results.json","w"),indent=2)
print(f"\n[B nested bootstrap] matched increment point {pt_point:+.4f}; nested 95% CI [{np.percentile(nested,2.5):+.4f}, {np.percentile(nested,97.5):+.4f}] over {len(nested)} refit replicates")
print("(compare conditional CI +0.0039 to +0.0119)")
print("DONE")
