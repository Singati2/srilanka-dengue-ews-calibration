# Table 6 (M5_no-climate row) + Fig 4 rebuild: M5 vs M5_no-climate decision curves under
# raw and past-only recalibration, with the matched increment and 95% cluster-bootstrap bands.
# Reproduce-first gate: frozen M1/M4/M5 to <1e-6 before any output.
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd, numpy as np, json, sys
from patsy import dmatrix, build_design_matrices
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
import statsmodels.api as sm
V2="/home/mpcrlab/data_quarantine/analysis_tables/dengue_climate_population_linked_2018_2025_v2_date_aligned.csv"
HYB="/home/mpcrlab/data_quarantine/model_pilots/hybrid_model_extension_v1/hybrid_model_predictions_v1.csv"
FIGDIR="/home/mpcrlab/srilanka-dengue-ews-calibration/manuscript/paper1_validity_corrected_candidate/submission_figs"
CLIMVARS=['t2m_mean_c','precip_sum_mm','rh_mean_percent']; LAGS=list(range(0,9)); SEED=20260612; CGRID=[0.1,1.0,10.0]
EPS=1e-6; clip=lambda p:np.clip(p,EPS,1-EPS); logit=lambda p:np.log(clip(p)/(1-clip(p))); sig=lambda z:1/(1+np.exp(-z))
m=pd.read_csv(V2,parse_dates=['week_start','week_end'])
f=m[(m.outcome_missing_flag==0)&(m.exposure_missing_flag==0)&(m.population_missing_flag==0)&
    (m.epi_year>=2018)&(m.epi_year<=2025)].copy().sort_values(['geometry_id','week_start']).reset_index(drop=True)
fut=f[['geometry_id','week_start','dengue_incidence_per_100k']].rename(columns={'dengue_incidence_per_100k':'inc_future'})
fut['week_start']=fut['week_start']-pd.Timedelta(days=28)
f=f.merge(fut,on=['geometry_id','week_start'],how='left'); f=f[f.inc_future.notna()].copy()
f['split']=np.where(f.epi_year<=2022,'train','test')
gq=f[f.split=='train'].groupby('geometry_id')['dengue_incidence_per_100k']
f=f.merge(gq.quantile(0.75).rename('thr75').reset_index(),on='geometry_id',how='left')
f['y']=(f['inc_future']>f['thr75']).astype(int)
for L in [1,2,4]:
    t=f[['geometry_id','week_start','dengue_incidence_per_100k']].rename(columns={'dengue_incidence_per_100k':f'inc_lag{L}'}).copy()
    t['week_start']=t['week_start']+pd.Timedelta(days=7*L); f=f.merge(t,on=['geometry_id','week_start'],how='left')
f['inc_t']=f['dengue_incidence_per_100k']
for v in CLIMVARS:
    for L in LAGS:
        t=f[['geometry_id','week_start',v]].rename(columns={v:f'{v}__L{L}'}).copy()
        t['week_start']=t['week_start']+pd.Timedelta(days=7*L); f=f.merge(t,on=['geometry_id','week_start'],how='left')
w=2*np.pi*f['epi_week']/52.18
f['sin1'],f['cos1'],f['sin2'],f['cos2']=np.sin(w),np.cos(w),np.sin(2*w),np.cos(2*w)
rd=pd.get_dummies(f['geometry_id'],prefix='rd',drop_first=True).astype(float); f=pd.concat([f,rd],axis=1); RD=list(rd.columns)
tr0=f[f.split=='train']
for c in ['inc_lag1','inc_lag2','inc_lag4']+[f'{v}__L{L}' for v in CLIMVARS for L in LAGS]:
    f[c]=f[c].fillna(tr0[c].mean())
f['target_week']=f['week_start']+pd.Timedelta(days=28); f=f.reset_index(drop=True)
AR=['inc_t','inc_lag1','inc_lag2','inc_lag4']; VDF=LDF=3
DIs={v:dmatrix(f"cr(x, df={VDF}) - 1",{"x":f.loc[f.split=='train',f'{v}__L0'].values},return_type='dataframe').design_info for v in CLIMVARS}
BLAG=np.asarray(dmatrix(f"cr(x, df={LDF}) - 1",{"x":np.array(LAGS,float)},return_type='dataframe'))
def cb_all(v):
    n=len(f); Vb=np.empty((n,len(LAGS),VDF))
    for i,L in enumerate(LAGS): Vb[:,i,:]=np.asarray(build_design_matrices([DIs[v]],{"x":f[f'{v}__L{L}'].values})[0])
    return np.einsum('nlj,lk->njk',Vb,BLAG).reshape(n,VDF*LDF)
CB=np.concatenate([cb_all(v) for v in CLIMVARS],axis=1)
X_M5=np.concatenate([f[AR].values,CB,f[['sin1','cos1','sin2','cos2']+RD].values],axis=1)
X_MA=np.concatenate([f[AR].values,f[['sin1','cos1','sin2','cos2']+RD].values],axis=1)
yv=f['y'].values; yr=f['epi_year'].values; split=f['split'].values
tw=f['target_week'].values; ws=f['week_start'].values; geo=f['geometry_id'].values
tr_idx=np.where(split=='train')[0]; te_idx=np.where(split=='test')[0]; allrows=np.arange(len(f)); yte=yv[te_idx]
def fit_sel(X,rows):
    Xt=X[rows]; yt=yv[rows]; yrt=yr[rows]; mu=Xt.mean(0); sd=Xt.std(0); sd[sd==0]=1
    yrs=sorted(np.unique(yrt)); folds=[]
    for i in range(1,len(yrs)):
        a=np.where(yrt<=yrs[i-1])[0]; b=np.where(yrt==yrs[i])[0]
        if len(b)>0 and len(np.unique(yt[a]))>1 and len(np.unique(yt[b]))>1: folds.append((a,b))
    bestC,bestS=1.0,-1
    for C in CGRID:
        sc=[]
        for a,b in folds:
            clf=LogisticRegression(penalty='l2',C=C,solver='lbfgs',max_iter=6000).fit((Xt[a]-mu)/sd,yt[a])
            sc.append(roc_auc_score(yt[b],clf.predict_proba((Xt[b]-mu)/sd)[:,1]))
        if sc and np.mean(sc)>bestS: bestS,bestC=np.mean(sc),C
    clf=LogisticRegression(penalty='l2',C=bestC,solver='lbfgs',max_iter=8000).fit((Xt-mu)/sd,yt)
    if np.abs(clf.coef_).max()>15: clf=LogisticRegression(penalty='l2',C=0.1,solver='lbfgs',max_iter=8000).fit((Xt-mu)/sd,yt)
    return clf,mu,sd
def pr(c,mu,sd,X,rows): return clip(c.predict_proba((X[rows]-mu)/sd)[:,1])
def recal_pastonly(p_all,test_rows,WIN=52):
    z=logit(p_all); rec=np.empty(len(test_rows)); tws=ws[test_rows]
    for wk in np.unique(tws):
        elig=(tw<wk)&(tw>=wk-np.timedelta64(7*WIN,'D')); ye=yv[elig]; ze=z[elig]; a=0.0
        if ye.sum()>=1 and (len(ye)-ye.sum())>=1 and len(ye)>=20:
            try:
                r=sm.GLM(ye,np.ones((len(ye),1)),family=sm.families.Binomial(),offset=ze).fit()
                if abs(float(r.params[0]))<=15 and np.isfinite(r.params[0]): a=float(r.params[0])
            except Exception: a=0.0
        sel=np.where(tws==wk)[0]; rec[sel]=clip(sig(logit(p_all[test_rows[sel]])+a))
    return rec
c5=fit_sel(X_M5,tr_idx); ca=fit_sel(X_MA,tr_idx)
pM5=pr(*c5,X_M5,te_idx); pMA=pr(*ca,X_MA,te_idx)
# GATE
hyb=pd.read_csv(HYB,parse_dates=['week_start']); key=['geometry_id','week_start']
tv=pd.DataFrame({'geometry_id':geo[te_idx],'week_start':ws[te_idx],'M5n':pM5}).merge(hyb[key+['p_M5_hybrid_season_RDHS']],on=key)
d5=np.abs(tv['M5n']-tv['p_M5_hybrid_season_RDHS']).max()
if d5>=1e-6: print(f"GATE FAILED d5={d5:.1e}"); sys.exit(1)
pM5_all=pr(*c5,X_M5,allrows); pMA_all=pr(*ca,X_MA,allrows)
rM5=recal_pastonly(pM5_all,te_idx); rMA=recal_pastonly(pMA_all,te_idx)
def nb(y,p,t): a=p>=t; n=len(y); return (a&(y==1)).sum()/n-(a&(y==0)).sum()/n*(t/(1-t))
def nb_allt(p,grid): return np.array([nb(yte,p,t) for t in grid])
# ---- Table 6 numbers: matched (raw) AUC + NB at 0.20/0.30/0.40 ----
auc_MA=roc_auc_score(yte,pMA); auc_M5=roc_auc_score(yte,pM5)
t6={"AUC_matched":round(float(auc_MA),3),"AUC_M5":round(float(auc_M5),3),
    "NB020":round(float(nb(yte,pMA,0.20)),3),"NB030":round(float(nb(yte,pMA,0.30)),3),"NB040":round(float(nb(yte,pMA,0.40)),3)}
print("TABLE6 matched row:",json.dumps(t6))
# ---- Fig 4 data: NB grids + matched increment bands ----
grid=np.round(np.arange(0.05,0.505,0.025),3)
NB={"M5_raw":nb_allt(pM5,grid),"MA_raw":nb_allt(pMA,grid),"M5_recal":nb_allt(rM5,grid),"MA_recal":nb_allt(rMA,grid)}
alert_all=np.array([ (yte.mean()) - (1-yte.mean())*(t/(1-t)) for t in grid])
rd_ids=sorted(np.unique(geo[te_idx])); groups={g:np.where(geo[te_idx]==g)[0] for g in rd_ids}; rng=np.random.default_rng(SEED)
def diff_band(pa_raw,pb_raw):
    lo=[];hi=[];mid=[]
    D=np.zeros((1000,len(grid)))
    for k in range(1000):
        idx=np.concatenate([groups[rd_ids[i]] for i in rng.integers(0,len(rd_ids),len(rd_ids))]); yy=yte[idx]
        if yy.min()==yy.max(): D[k]=np.nan; continue
        D[k]=[ (nb(yy,pa_raw[idx],t)-nb(yy,pb_raw[idx],t)) for t in grid]
    lo=np.nanpercentile(D,2.5,axis=0); hi=np.nanpercentile(D,97.5,axis=0); mid=np.nanmean(D,axis=0)
    return lo,hi
inc_raw=NB["M5_raw"]-NB["MA_raw"]; inc_recal=NB["M5_recal"]-NB["MA_recal"]
lo_r,hi_r=diff_band(pM5,pMA); lo_c,hi_c=diff_band(rM5,rMA)
# ---- PLOT ----
fig,(axA,axB)=plt.subplots(1,2,figsize=(9.2,3.7))
# Panel A: NB curves
axA.plot(grid,NB["M5_raw"],'-',color='#1f77b4',lw=1.6,label='M5 (raw)')
axA.plot(grid,NB["MA_raw"],'--',color='#1f77b4',lw=1.4,label='M5$_{no-climate}$ (raw)')
axA.plot(grid,NB["M5_recal"],'-',color='#d62728',lw=1.6,label='M5 (recal.)')
axA.plot(grid,NB["MA_recal"],'--',color='#d62728',lw=1.4,label='M5$_{no-climate}$ (recal.)')
axA.plot(grid,alert_all,':',color='0.4',lw=1.2,label='Alert-all')
axA.axhline(0,color='0.7',lw=0.8); axA.axvline(0.30,color='0.75',lw=0.8,ls=':')
axA.set_xlabel('Threshold $p^*$'); axA.set_ylabel('Net benefit'); axA.set_title('(A) Decision curves: M5 vs M5$_{no-climate}$',fontsize=10)
axA.legend(fontsize=7,frameon=False,loc='upper right'); axA.set_xlim(0.05,0.50)
# Panel B: matched increment with bands
axB.fill_between(grid,lo_r,hi_r,color='#1f77b4',alpha=0.18)
axB.fill_between(grid,lo_c,hi_c,color='#d62728',alpha=0.18)
axB.plot(grid,inc_raw,'-',color='#1f77b4',lw=1.7,label='Matched increment (raw)')
axB.plot(grid,inc_recal,'-',color='#d62728',lw=1.7,label='Matched increment (past-only recal.)')
axB.axhline(0,color='0.5',lw=1.0); axB.axvline(0.30,color='0.75',lw=0.8,ls=':')
axB.set_xlabel('Threshold $p^*$'); axB.set_ylabel('$\\Delta$NB (M5 $-$ M5$_{no-climate}$)')
axB.set_title('(B) Specification-matched climate increment',fontsize=10)
axB.legend(fontsize=7,frameon=False,loc='upper left'); axB.set_xlim(0.05,0.50)
plt.tight_layout()
plt.savefig(FIGDIR+"/Fig4.pdf",bbox_inches='tight'); plt.savefig(FIGDIR+"/../Fig4_new_preview.pdf",bbox_inches='tight')
print("Fig4.pdf written to",FIGDIR)
print("increment@0.30 raw=%.4f recal=%.4f"%(inc_raw[list(grid).index(0.30)],inc_recal[list(grid).index(0.30)]))
json.dump({"table6_matched":t6,"gate_maxabsdiff":float(d5)},open("/home/mpcrlab/srilanka-dengue-ews-calibration/analysis/v17_devinclusive_finalization/fig4_table6_results.json","w"),indent=2)
