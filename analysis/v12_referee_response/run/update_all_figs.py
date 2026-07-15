# Regenerate all six data figures (Figs 4-8) with reviewer-requested improvements:
# uncertainty (CIs/error bars), prediction-distribution rug, CITL/slope/Brier annotations,
# raw+recalibrated SL panels, and per-horizon CIs + n + prevalence.
import pandas as pd, numpy as np, json
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import log_loss, brier_score_loss
from scipy.optimize import minimize_scalar
np.random.seed(20260612)
Q="/home/mpcrlab/data_quarantine/"
FIG="/home/mpcrlab/srilanka-dengue-ews-calibration/manuscript/paper1_validity_corrected_candidate/"
def nb(p,yy,t=0.30): a=p>=t; n=len(yy); return (a&(yy==1)).sum()/n-(a&(yy==0)).sum()/n*(t/(1-t))
def citl_slope(p,y):
    p=np.clip(p,1e-6,1-1e-6); lo=np.log(p/(1-p))
    m=LogisticRegression(C=1e9,max_iter=2000,fit_intercept=False).fit(np.column_stack([np.ones_like(lo),lo]),y); b=m.coef_[0][1]
    def nll(c): z=c+lo; pp=np.clip(1/(1+np.exp(-z)),1e-9,1-1e-9); return -np.sum(y*np.log(pp)+(1-y)*np.log(1-pp))
    a=minimize_scalar(nll,bounds=(-10,10),method='bounded').x; return float(a),float(b)
def wilson(k,n,z=1.96):
    if n==0: return (0,0)
    ph=k/n; d=1+z*z/n; c=(ph+z*z/(2*n))/d; h=z*np.sqrt(ph*(1-ph)/n+z*z/(4*n*n))/d; return (c-h,c+h)
def calplot(ax,P,y,models,styles,title):
    for m,st in zip(models,styles):
        p=np.clip(P[m],1e-6,1-1e-6); q=pd.qcut(p,10,duplicates='drop',labels=False)
        xs,ys,los,his=[],[],[],[]
        for b in np.unique(q):
            mask=q==b; k=int(y[mask].sum()); n=int(mask.sum())
            xs.append(p[mask].mean()); ys.append(k/n); lo,hi=wilson(k,n); los.append(k/n-lo); his.append(hi-k/n)
        a,s=citl_slope(P[m],y); br=brier_score_loss(y,np.clip(P[m],1e-6,1-1e-6))
        ax.errorbar(xs,ys,yerr=[los,his],fmt=st,ms=4,capsize=2,lw=1,label=f"{m} (CITL {a:+.2f}, slope {s:.2f}, Brier {br:.3f})")
    ax.plot([0,1],[0,1],'k--',lw=.8); ax.set_xlim(0,.8); ax.set_ylim(0,.8)
    # rug of predicted probs (first model)
    p0=np.clip(P[models[0]],1e-6,1-1e-6)
    ax.plot(np.clip(p0,0,.8),np.full(len(p0),0.005),'|',color='gray',alpha=0.08,ms=6)
    ax.set_xlabel('Mean predicted'); ax.set_ylabel('Observed frequency'); ax.set_title(title); ax.legend(fontsize=6.2,loc='upper left')

# ================= SRI LANKA =================
sl=pd.read_csv(Q+"model_pilots/hybrid_model_extension_v1/hybrid_model_predictions_v1.csv"); ysl=sl.y.values.astype(int)
SLm={'M1':'p_M1','M4':'p_M4_hybrid','M5':'p_M5_hybrid_season_RDHS'}
Praw={m:np.clip(sl[c].values,1e-6,1-1e-6) for m,c in SLm.items()}
fold=(pd.to_datetime(sl.week_start).dt.isocalendar().week.astype(int).values%2).astype(int)
def crossfit(p):
    out=np.zeros_like(p)
    for f in [0,1]:
        tr=fold!=f; te=fold==f; lo=np.log(p/(1-p))
        pl=LogisticRegression(C=1e6,max_iter=1000).fit(lo[tr].reshape(-1,1),ysl[tr]); out[te]=pl.predict_proba(lo[te].reshape(-1,1))[:,1]
    return np.clip(out,1e-6,1-1e-6)
Prec={m:crossfit(Praw[m]) for m in SLm}
rd=sl.geometry_id.values; uq=np.array(sorted(set(rd))); byd={u:np.where(rd==u)[0] for u in uq}; rng=np.random.default_rng(20260612)
def band(P,models,grid):
    out={}
    for m in models:
        reps=[]
        for _ in range(300):
            ii=np.concatenate([byd[u] for u in rng.choice(uq,len(uq),True)])
            reps.append([nb(P[m][ii],ysl[ii],t) for t in grid])
        reps=np.array(reps); out[m]=(np.percentile(reps,2.5,0),np.percentile(reps,97.5,0))
    return out
# Fig 4: SL calibration raw+recal
fig,axs=plt.subplots(1,2,figsize=(9,4))
calplot(axs[0],Praw,ysl,['M1','M4','M5'],['-o','-s','-^'],'Sri Lanka: raw predictions')
calplot(axs[1],Prec,ysl,['M1','M4','M5'],['-o','-s','-^'],'Sri Lanka: cross-fit recalibrated')
plt.tight_layout(); plt.savefig(FIG+"fig_sl_calibration.pdf"); plt.close()
# Fig 5: SL decision curves raw+recal, with bootstrap bands
grid=np.linspace(0.05,0.5,19); prev=ysl.mean()
fig,axs=plt.subplots(1,2,figsize=(9,4),sharey=True)
for ax,P,tag in [(axs[0],Praw,'raw'),(axs[1],Prec,'recalibrated')]:
    bd=band(P,['M1','M4','M5'],grid)
    for m,c in zip(['M1','M4','M5'],['C0','C1','C2']):
        ax.plot(grid,[nb(P[m],ysl,t) for t in grid],'-',color=c,label=m); ax.fill_between(grid,bd[m][0],bd[m][1],color=c,alpha=0.15)
    ax.plot(grid,[prev-(1-prev)*(t/(1-t)) for t in grid],color='gray',lw=.8,label='alert-all'); ax.axhline(0,color='k',lw=.6)
    ax.axvline(0.30,color='r',lw=.5,ls=':'); ax.set_xlabel('Threshold $p^*$'); ax.set_title(f'Sri Lanka DCA ({tag})'); ax.legend(fontsize=7)
axs[0].set_ylabel('Net benefit'); plt.tight_layout(); plt.savefig(FIG+"fig_sl_dca.pdf"); plt.close()
print("SL figs done")

# ================= COLOMBIA =================
d=pd.read_csv(Q+"colombia_label_features_v1/colombia_modeling_table_h4_75pct_v1.csv")
d['dept']=d.GID_2.str.split('.').str[1]; d['yr']=d['week_start'].astype(str).str[:4].astype(int)
cc=d[d.common_complete_M1_to_M5_h4==True].reset_index(drop=True); y=cc.label_h4.values.astype(int)
SEA=['sin_woy_1','cos_woy_1','sin_woy_2','cos_woy_2']; CAS=['cases_lag0','cases_lag1','cases_lag2','cases_lag4']
def Xb(idx,parts,tr,ccols=CAS):
    M=[np.log1p(cc.loc[idx,c].values) for c in ccols] if 'cases' in parts else []
    if 'clim' in parts: M+=[np.log1p(cc.loc[idx,f'precip_lag{l}'].values) for l in range(9)]+[cc.loc[idx,f'temp_lag{l}'].values for l in range(9)]
    if 'sea' in parts: M+=[cc.loc[idx,c].values for c in SEA]
    A=np.column_stack(M)
    if 'dept' in parts:
        dp=sorted(cc.loc[tr,'dept'].unique()); A=np.column_stack([A]+[(cc.loc[idx,'dept'].values==x).astype(float) for x in dp])
    return A
def predict(parts,tr,va,te,ccols=CAS,ct=True):
    sc=StandardScaler().fit(Xb(tr,parts,tr,ccols)); best=None
    for C in ([0.03,0.1,0.3,1,3] if ct else [1.0]):
        m=LogisticRegression(C=C,max_iter=2500).fit(sc.transform(Xb(tr,parts,tr,ccols)),y[tr])
        p=np.clip(m.predict_proba(sc.transform(Xb(va,parts,tr,ccols)))[:,1],1e-6,1-1e-6); ll=log_loss(y[va],p,labels=[0,1]); best=(ll,m) if best is None or ll<best[0] else best
    m=best[1]; pv=np.clip(m.predict_proba(sc.transform(Xb(va,parts,tr,ccols)))[:,1],1e-6,1-1e-6); pt=np.clip(m.predict_proba(sc.transform(Xb(te,parts,tr,ccols)))[:,1],1e-6,1-1e-6)
    pl=LogisticRegression(C=1e6,max_iter=1000).fit(np.log(pv/(1-pv)).reshape(-1,1),y[va]); return pl.predict_proba(np.log(pt/(1-pt)).reshape(-1,1))[:,1]
def iy(ys): return cc.index[cc.yr.isin(ys)].values
MOD={'M1':{'cases'},'matched':{'cases','sea','dept'},'M4':{'cases','clim'},'M5':{'cases','clim','sea','dept'}}
tr0,va0,te0=iy(range(2006,2018)),iy([2018,2019]),iy([2020,2021,2022]); yte=y[te0]
pr={m:predict(MOD[m],tr0,va0,te0) for m in MOD}
dep=cc.loc[te0,'dept'].values; uqc=np.array(sorted(set(dep))); bydc={u:np.where(dep==u)[0] for u in uqc}; rngc=np.random.default_rng(20260612)
def bootci(pa,pb,B=1000):
    D=[]
    for _ in range(B):
        ii=np.concatenate([bydc[u] for u in rngc.choice(uqc,len(uqc),True)])
        D.append(nb(pa[ii],yte[ii])-nb(pb[ii],yte[ii]))
    return np.percentile(D,2.5),np.percentile(D,97.5)
# Fig 7: Colombia calibration + DCA (with bands)
fig,axs=plt.subplots(1,2,figsize=(9,4))
calplot(axs[0],pr,yte,['M1','matched','M4','M5'],['-o','-s','-^','-d'],'Colombia calibration (test)')
grid=np.linspace(0.05,0.5,19); prevc=yte.mean()
bdc={}
for m in ['M1','matched','M4','M5']:
    reps=[]
    for _ in range(300):
        ii=np.concatenate([bydc[u] for u in rngc.choice(uqc,len(uqc),True)])
        reps.append([nb(pr[m][ii],yte[ii],t) for t in grid])
    reps=np.array(reps); bdc[m]=(np.percentile(reps,2.5,0),np.percentile(reps,97.5,0))
for m,c in zip(['M1','matched','M4','M5'],['C0','C3','C1','C2']):
    axs[1].plot(grid,[nb(pr[m],yte,t) for t in grid],'-',color=c,label=m); axs[1].fill_between(grid,bdc[m][0],bdc[m][1],color=c,alpha=0.12)
axs[1].plot(grid,[prevc-(1-prevc)*(t/(1-t)) for t in grid],color='gray',lw=.8,label='alert-all'); axs[1].axhline(0,color='k',lw=.6)
axs[1].axvline(0.30,color='r',lw=.5,ls=':'); axs[1].set_xlabel('Threshold $p^*$'); axs[1].set_ylabel('Net benefit'); axs[1].set_title('Colombia DCA (test)'); axs[1].legend(fontsize=7)
plt.tight_layout(); plt.savefig(FIG+"fig_co_calibration.pdf"); plt.close()
# keep fig_co_dca as a forest plot of contrasts with CIs (matched model included)
contrasts=[('M5$-$M1 (compound)',pr['M5'],pr['M1']),('M5$-$matched (climate)',pr['M5'],pr['matched']),
           ('matched$-$M1 (structure)',pr['matched'],pr['M1']),('M4$-$M1 (cases+climate)',pr['M4'],pr['M1'])]
fig,ax=plt.subplots(figsize=(6,3.2)); ys=range(len(contrasts))
for i,(lab,pa,pb) in enumerate(contrasts):
    pt=nb(pa,yte)-nb(pb,yte); lo,hi=bootci(pa,pb)
    ax.errorbar(pt,i,xerr=[[pt-lo],[hi-pt]],fmt='o',capsize=3,color='C0')
    ax.text(hi+0.001,i,f"{pt:+.4f} [{lo:+.3f}, {hi:+.3f}]",va='center',fontsize=7)
ax.axvline(0,color='k',lw=.6); ax.set_yticks(list(ys)); ax.set_yticklabels([c[0] for c in contrasts],fontsize=8)
ax.set_xlabel('$\\Delta$NB at $p^*=0.30$ (95\\% conditional CI)'); ax.set_title('Colombia paired contrasts'); ax.set_xlim(-0.005,0.035)
plt.tight_layout(); plt.savefig(FIG+"fig_co_dca.pdf"); plt.close()
print("CO calibration + forest done")

# Fig 6: completeness — year bars (integer) + included-vs-excluded
by=d.groupby('yr')['common_complete_M1_to_M5_h4'].mean()
tp=d[d.yr.isin([2020,2021,2022])]; inc=tp[tp.common_complete_M1_to_M5_h4]; exc=tp[~tp.common_complete_M1_to_M5_h4]
fig,axs=plt.subplots(1,2,figsize=(9,3.2))
axs[0].bar(by.index.astype(int),by.values,color='steelblue'); axs[0].set_xticks(range(int(by.index.min()),int(by.index.max())+1,2))
axs[0].set_xlabel('Year'); axs[0].set_ylabel('Fraction of observed muni-weeks\nthat are common-complete'); axs[0].set_title('Completeness by year')
metrics=['mean cases','prevalence','median wks/muni']
ivals=[inc['cases_lag0'].mean(),inc['label_h4'].mean(),inc.groupby('GID_2').size().median()]
evals=[exc['cases_lag0'].mean(),exc['label_h4'].mean(),exc.groupby('GID_2').size().median()]
x=np.arange(3); w=0.38
axs[1].bar(x-w/2,ivals,w,label='included',color='C0'); axs[1].bar(x+w/2,evals,w,label='excluded',color='C3')
axs[1].set_xticks(x); axs[1].set_xticklabels(metrics,fontsize=8); axs[1].set_title('Included vs excluded (test period)'); axs[1].legend(fontsize=7)
for i,(a,b) in enumerate(zip(ivals,evals)): axs[1].text(i-w/2,a,f"{a:.2f}",ha='center',va='bottom',fontsize=6); axs[1].text(i+w/2,b,f"{b:.2f}",ha='center',va='bottom',fontsize=6)
plt.tight_layout(); plt.savefig(FIG+"fig_co_missingness.pdf"); plt.close()
print("completeness done")

# Fig 8: horizon with 95% CIs + n + prevalence
dh=pd.read_csv(Q+"colombia_label_features_v1/colombia_modeling_table_all_horizons_v1.csv")
dh['dept']=dh.GID_2.str.split('.').str[1]; dh['yr']=dh['week_start'].astype(str).str[:4].astype(int)
H=[1,2,4,8,12]; hm={};hc={};hn={};hp={}
for h in H:
    lab=f'label_h{h}'; sub=dh[(dh['common_complete_M1_to_M5_h4']==True)&(dh[lab].notna())].reset_index(drop=True)
    yy=sub[lab].values.astype(int); tr=sub.index[sub.yr<=2017].values; va=sub.index[sub.yr.isin([2018,2019])].values; te=sub.index[sub.yr>=2020].values
    if len(te)<200 or len(np.unique(yy[te]))<2: continue
    def Xh(idx,parts,trr):
        M=[np.log1p(sub.loc[idx,c].values) for c in CAS] if 'cases' in parts else []
        if 'clim' in parts: M+=[np.log1p(sub.loc[idx,f'precip_lag{l}'].values) for l in range(9)]+[sub.loc[idx,f'temp_lag{l}'].values for l in range(9)]
        if 'sea' in parts: M+=[sub.loc[idx,c].values for c in SEA]
        A=np.column_stack(M)
        if 'dept' in parts:
            dp=sorted(sub.loc[trr,'dept'].unique()); A=np.column_stack([A]+[(sub.loc[idx,'dept'].values==x).astype(float) for x in dp])
        return A
    def ph(parts):
        sc=StandardScaler().fit(Xh(tr,parts,tr)); m=LogisticRegression(C=1.0,max_iter=2000).fit(sc.transform(Xh(tr,parts,tr)),yy[tr])
        pv=np.clip(m.predict_proba(sc.transform(Xh(va,parts,tr)))[:,1],1e-6,1-1e-6); pt=np.clip(m.predict_proba(sc.transform(Xh(te,parts,tr)))[:,1],1e-6,1-1e-6)
        pl=LogisticRegression(C=1e6,max_iter=1000).fit(np.log(pv/(1-pv)).reshape(-1,1),yy[va]); return pl.predict_proba(np.log(pt/(1-pt)).reshape(-1,1))[:,1]
    p5=ph(MOD['M5']); pm=ph(MOD['matched']); p1=ph(MOD['M1']); yt=yy[te]
    dh_dep=sub.loc[te,'dept'].values; uh=np.array(sorted(set(dh_dep))); bh={u:np.where(dh_dep==u)[0] for u in uh}; rh=np.random.default_rng(20260612)
    def ci(pa,pb):
        D=[]
        for _ in range(500):
            jj=np.concatenate([bh[u] for u in rh.choice(uh,len(uh),True)])
            D.append(nb(pa[jj],yt[jj])-nb(pb[jj],yt[jj]))
        return np.percentile(D,2.5),np.percentile(D,97.5)
    hm[h]=(nb(p5,yt)-nb(pm,yt),ci(p5,pm)); hc[h]=(nb(p5,yt)-nb(p1,yt),ci(p5,p1)); hn[h]=len(te); hp[h]=float(yt.mean())
hs=sorted(hm)
fig,ax=plt.subplots(figsize=(6,3.6))
ax.errorbar(hs,[hm[h][0] for h in hs],yerr=[[hm[h][0]-hm[h][1][0] for h in hs],[hm[h][1][1]-hm[h][0] for h in hs]],fmt='-o',capsize=3,label='M5$-$matched (climate)')
ax.errorbar([h+0.15 for h in hs],[hc[h][0] for h in hs],yerr=[[hc[h][0]-hc[h][1][0] for h in hs],[hc[h][1][1]-hc[h][0] for h in hs]],fmt='-s',capsize=3,label='M5$-$M1 (compound)')
ax.axhline(0,color='k',lw=.6); ax.set_xlabel('Horizon (weeks)'); ax.set_ylabel('$\\Delta$NB at $p^*=0.30$ (95\\% CI)'); ax.set_title('Colombia increment vs horizon'); ax.legend(fontsize=7)
for h in hs: ax.annotate(f"n={hn[h]}\nprev {hp[h]:.2f}",(h,ax.get_ylim()[0]),fontsize=5.5,ha='center',va='bottom',color='gray')
plt.tight_layout(); plt.savefig(FIG+"fig_co_horizon.pdf"); plt.close()
print("horizon done"); print("DONE")
