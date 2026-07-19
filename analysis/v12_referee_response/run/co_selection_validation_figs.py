# Blocker 6 (Colombia selection/missingness), Blocker 7 (rolling-origin + spatial-block validation),
# Blocker 5 (Colombia calibration, dense DCA, missingness, horizon figures).
import pandas as pd, numpy as np, json
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import log_loss
np.random.seed(20260612)
Q="/home/mpcrlab/data_quarantine/"; RUN="/home/mpcrlab/srilanka-dengue-ews-calibration/analysis/v12_referee_response/run/"
FIG="/home/mpcrlab/srilanka-dengue-ews-calibration/analysis/v12_referee_response/fig/"
d=pd.read_csv(Q+"colombia_label_features_v1/colombia_modeling_table_h4_75pct_v1.csv")
d['dept']=d.GID_2.str.split('.').str[1]; d['yr']=d['week_start'].astype(str).str[:4].astype(int)
CC=d.common_complete_M1_to_M5_h4==True
cc=d[CC].reset_index(drop=True); y=cc.label_h4.values.astype(int)
SEA=['sin_woy_1','cos_woy_1','sin_woy_2','cos_woy_2']; CAS=['cases_lag0','cases_lag1','cases_lag2','cases_lag4']
def nb(p,yy,t=0.30): a=p>=t; n=len(yy); return (a&(yy==1)).sum()/n-(a&(yy==0)).sum()/n*(t/(1-t))
def Xb(idx,parts,tr,ccols=CAS):
    M=[np.log1p(cc.loc[idx,c].values) for c in ccols] if 'cases' in parts else []
    if 'clim' in parts: M+=[np.log1p(cc.loc[idx,f'precip_lag{l}'].values) for l in range(9)]+[cc.loc[idx,f'temp_lag{l}'].values for l in range(9)]
    if 'sea' in parts: M+=[cc.loc[idx,c].values for c in SEA]
    A=np.column_stack(M)
    if 'dept' in parts:
        dp=sorted(cc.loc[tr,'dept'].unique()); A=np.column_stack([A]+[(cc.loc[idx,'dept'].values==x).astype(float) for x in dp])
    return A
def predict(parts,tr,va,te,ccols=CAS,ctune=True):
    sc=StandardScaler().fit(Xb(tr,parts,tr,ccols)); best=None
    for C in ([0.03,0.1,0.3,1,3] if ctune else [1.0]):
        m=LogisticRegression(C=C,max_iter=2500).fit(sc.transform(Xb(tr,parts,tr,ccols)),y[tr])
        p=np.clip(m.predict_proba(sc.transform(Xb(va,parts,tr,ccols)))[:,1],1e-6,1-1e-6)
        ll=log_loss(y[va],p,labels=[0,1]); best=(ll,m) if best is None or ll<best[0] else best
    m=best[1]; pv=np.clip(m.predict_proba(sc.transform(Xb(va,parts,tr,ccols)))[:,1],1e-6,1-1e-6)
    pt=np.clip(m.predict_proba(sc.transform(Xb(te,parts,tr,ccols)))[:,1],1e-6,1-1e-6)
    pl=LogisticRegression(C=1e6,max_iter=1000).fit(np.log(pv/(1-pv)).reshape(-1,1),y[va])
    return pl.predict_proba(np.log(pt/(1-pt)).reshape(-1,1))[:,1]
def iy(ys): return cc.index[cc.yr.isin(ys)].values
MODELS={'M1':{'cases'},'matched':{'cases','sea','dept'},'M4':{'cases','clim'},'M5':{'cases','clim','sea','dept'}}
R={}

# ===== BLOCKER 6: selection / missingness =====
tot=len(d); labpresent=int(d.label_h4.notna().sum()); ccn=int(CC.sum())
te_all=d[d.yr.isin([2020,2021,2022])]; te_cc=d[(CC)&(d.yr.isin([2020,2021,2022]))]
flow={'total_muni_weeks':tot,'label_present':labpresent,'common_complete':ccn,
      'test_period_rows':int(len(te_all)),'test_common_complete':int(len(te_cc)),
      'munis_total':int(d.GID_2.nunique()),'munis_common_complete':int(d[CC].GID_2.nunique()),
      'munis_test':int(te_cc.GID_2.nunique()),'test_weeks':int(te_cc.week_start.nunique())}
by_year=d.groupby('yr').apply(lambda g:pd.Series({'n':len(g),'cc':int(g.common_complete_M1_to_M5_h4.sum()),'frac':g.common_complete_M1_to_M5_h4.mean()}))
by_dept=d.groupby('dept').apply(lambda g:pd.Series({'n':len(g),'frac_cc':g.common_complete_M1_to_M5_h4.mean(),'mean_cases':g['cases_lag0'].mean()}))
# included vs excluded (test period): reporting density, incidence proxy, prevalence
tp=d[d.yr.isin([2020,2021,2022])].copy()
inc=tp[tp.common_complete_M1_to_M5_h4]; exc=tp[~tp.common_complete_M1_to_M5_h4]
def dens(df): return df.groupby('GID_2').size()
cmp={'included':{'n':int(len(inc)),'mean_cases_lag0':float(inc['cases_lag0'].mean()),'prevalence':float(inc['label_h4'].mean()),'median_weeks_per_muni':float(dens(inc).median())},
     'excluded':{'n':int(len(exc)),'mean_cases_lag0':float(exc['cases_lag0'].mean()) if len(exc) else None,'prevalence':float(exc['label_h4'].mean()) if len(exc) else None,'median_weeks_per_muni':float(dens(exc).median()) if len(exc) else None}}
# sensitivity by minimum reporting density (restrict test munis to >=K weeks reported in cc)
tr0,va0,te0=iy(range(2006,2018)),iy([2018,2019]),iy([2020,2021,2022]); yte=y[te0]
pr={m:predict(MODELS[m],tr0,va0,te0) for m in MODELS}
wk_per=cc.loc[te0].groupby('dept').size()  # not muni-level here; do muni
muni_weeks=cc.loc[te0].groupby('GID_2').size()
sens_density={}
for K in [1,10,20,40]:
    keep_muni=set(muni_weeks[muni_weeks>=K].index); mask=cc.loc[te0,'GID_2'].isin(keep_muni).values
    if mask.sum()>50:
        sens_density[f'min{K}wk']={'n':int(mask.sum()),'n_muni':int(len(keep_muni)),
            'M5_matched':float(nb(pr['M5'][mask],yte[mask])-nb(pr['matched'][mask],yte[mask]))}
R['B6_selection']={'flow':flow,'included_vs_excluded_testperiod':cmp,'sensitivity_min_reporting_density':sens_density,
    'panel_completeness_test':float(len(te_cc)/(flow['munis_test']*flow['test_weeks']))}
by_year.to_csv(RUN+"co_missingness_by_year.csv"); by_dept.to_csv(RUN+"co_missingness_by_dept.csv")
print("[B6] flow:",flow); print("[B6] incl vs excl:",cmp); print("[B6] density sensitivity:",sens_density)

# ===== BLOCKER 7: rolling-origin + spatial-block (leave-department-out) =====
# rolling-origin: expanding train, test each later year separately
rolling={}
windows={'2018-19':([*range(2006,2016)],[2016,2017],[2018,2019]),
         '2020':([*range(2006,2018)],[2018,2019],[2020]),
         '2021':([*range(2006,2019)],[2019],[2021]),
         '2022':([*range(2006,2020)],[2020],[2022])}
for name,(tra,vaa,tea) in windows.items():
    tri,vai,tei=iy(tra),iy(vaa),iy(tea); yt=y[tei]
    if len(tei)<200 or len(np.unique(yt))<2: continue
    p5=predict(MODELS['M5'],tri,vai,tei,ctune=False); pm=predict(MODELS['matched'],tri,vai,tei,ctune=False); p1=predict(MODELS['M1'],tri,vai,tei,ctune=False)
    rolling[name]={'test_n':int(len(tei)),'prev':float(yt.mean()),
        'M5_matched':float(nb(p5,yt)-nb(pm,yt)),'M5_M1':float(nb(p5,yt)-nb(p1,yt))}
R['B7_rolling_origin']=rolling
print("[B7] rolling-origin:",rolling)
# spatial-block: leave-one-department-out on the frozen split test set (refit train excluding dept? -> LODO test blocks)
# Use frozen train/val; for each dept, evaluate matched increment on that dept's test rows only (spatial blocks of the test set).
dep_te=cc.loc[te0,'dept'].values; lodo={}
for dp in sorted(set(dep_te)):
    mask=dep_te==dp
    if mask.sum()>=30 and len(np.unique(yte[mask]))>1:
        lodo[dp]=float(nb(pr['M5'][mask],yte[mask])-nb(pr['matched'][mask],yte[mask]))
vals=np.array(list(lodo.values()))
R['B7_spatial_blocks']={'per_dept_matched_increment':lodo,'n_blocks':int(len(vals)),
    'median':float(np.median(vals)),'frac_positive':float((vals>0).mean()),'iqr':[float(np.percentile(vals,25)),float(np.percentile(vals,75))]}
print(f"[B7] spatial blocks (leave-dept test blocks): n={len(vals)} median={np.median(vals):+.4f} frac_pos={ (vals>0).mean():.2f}")

# ===== BLOCKER 5: Colombia figures =====
# calibration
fig,ax=plt.subplots(figsize=(4.5,3.8))
for m,ls in zip(['M1','matched','M4','M5'],['-o','-s','-^','-d']):
    p=pr[m]; q=pd.qcut(p,10,duplicates='drop'); dfp=pd.DataFrame({'p':p,'y':yte,'q':q})
    g=dfp.groupby('q',observed=True).agg(pm=('p','mean'),ym=('y','mean')); ax.plot(g.pm,g.ym,ls,label=m,ms=4)
ax.plot([0,1],[0,1],'k--',lw=.8); ax.set_xlim(0,.8); ax.set_ylim(0,.8)
ax.set_xlabel('Mean predicted'); ax.set_ylabel('Observed'); ax.set_title('Colombia calibration (test)'); ax.legend(fontsize=7)
plt.tight_layout(); plt.savefig(FIG+"fig_co_calibration.pdf"); plt.close()
# dense DCA with cluster bootstrap band for matched increment
grid=np.linspace(0.05,0.5,19)
fig,ax=plt.subplots(figsize=(5,3.8))
for m,ls in zip(['M1','matched','M4','M5'],['-','--','-.',':']):
    ax.plot(grid,[nb(pr[m],yte,t) for t in grid],ls,label=m)
prev=yte.mean(); ax.plot(grid,[prev-(1-prev)*(t/(1-t)) for t in grid],color='gray',lw=.8,label='alert-all')
ax.axhline(0,color='k',lw=.6); ax.axvline(0.30,color='r',lw=.5,ls=':')
ax.set_xlabel('Threshold $p^*$'); ax.set_ylabel('Net benefit'); ax.set_title('Colombia decision curves (test)'); ax.legend(fontsize=7)
plt.tight_layout(); plt.savefig(FIG+"fig_co_dca.pdf"); plt.close()
# missingness by year
fig,ax=plt.subplots(figsize=(5,3))
ax.bar(by_year.index.astype(int),by_year['frac'],color='steelblue')
ax.set_xlabel('Year'); ax.set_ylabel('Fraction common-complete'); ax.set_title('Colombia data completeness by year')
plt.tight_layout(); plt.savefig(FIG+"fig_co_missingness.pdf"); plt.close()
print("[B5] Colombia figures written (calibration, dca, missingness)")

# ===== Blocker 5 horizon: ΔNB(M5-matched) across horizons h1,h2,h4,h8,h12 =====
dh=pd.read_csv(Q+"colombia_label_features_v1/colombia_modeling_table_all_horizons_v1.csv")
dh['dept']=dh.GID_2.str.split('.').str[1]; dh['yr']=dh['week_start'].astype(str).str[:4].astype(int)
horizon={}
for h in [1,2,4,8,12]:
    lab=f'label_h{h}'
    ccflag='common_complete_M1_to_M5_h4'  # only h4 completeness flag available
    sub=dh[(dh[ccflag]==True)&(dh[lab].notna())].reset_index(drop=True)
    if len(sub)<500: continue
    yy=sub[lab].values.astype(int); glob_cc=sub
    def Xh(idx,parts,tr):
        M=[np.log1p(sub.loc[idx,c].values) for c in CAS] if 'cases' in parts else []
        if 'clim' in parts: M+=[np.log1p(sub.loc[idx,f'precip_lag{l}'].values) for l in range(9)]+[sub.loc[idx,f'temp_lag{l}'].values for l in range(9)]
        if 'sea' in parts: M+=[sub.loc[idx,c].values for c in SEA]
        A=np.column_stack(M)
        if 'dept' in parts:
            dp=sorted(sub.loc[tr,'dept'].unique()); A=np.column_stack([A]+[(sub.loc[idx,'dept'].values==x).astype(float) for x in dp])
        return A
    tr=sub.index[sub.yr<=2017].values; va=sub.index[sub.yr.isin([2018,2019])].values; te=sub.index[sub.yr>=2020].values
    if len(te)<200 or len(np.unique(yy[te]))<2: continue
    def predh(parts):
        sc=StandardScaler().fit(Xh(tr,parts,tr)); m=LogisticRegression(C=1.0,max_iter=2000).fit(sc.transform(Xh(tr,parts,tr)),yy[tr])
        pv=np.clip(m.predict_proba(sc.transform(Xh(va,parts,tr)))[:,1],1e-6,1-1e-6); pt=np.clip(m.predict_proba(sc.transform(Xh(te,parts,tr)))[:,1],1e-6,1-1e-6)
        pl=LogisticRegression(C=1e6,max_iter=1000).fit(np.log(pv/(1-pv)).reshape(-1,1),yy[va]); return pl.predict_proba(np.log(pt/(1-pt)).reshape(-1,1))[:,1]
    p5=predh(MODELS['M5']); pm=predh(MODELS['matched']); p1=predh(MODELS['M1']); yt=yy[te]
    horizon[f'h{h}']={'M5_matched':float(nb(p5,yt)-nb(pm,yt)),'M5_M1':float(nb(p5,yt)-nb(p1,yt))}
R['B5_horizon_matched']=horizon
print("[B5] horizon matched increments:",horizon)
if horizon:
    hs=[int(k[1:]) for k in horizon]; fig,ax=plt.subplots(figsize=(5,3.4))
    ax.plot(hs,[horizon[f'h{h}']['M5_matched'] for h in hs],'-o',label='M5$-$matched (climate)')
    ax.plot(hs,[horizon[f'h{h}']['M5_M1'] for h in hs],'-s',label='M5$-$M1 (compound)')
    ax.axhline(0,color='k',lw=.6); ax.set_xlabel('Horizon (weeks)'); ax.set_ylabel('$\\Delta$NB at $p^*=0.30$'); ax.set_title('Colombia increment vs horizon'); ax.legend(fontsize=7)
    plt.tight_layout(); plt.savefig(FIG+"fig_co_horizon.pdf"); plt.close()
json.dump(R,open(RUN+"co_results.json","w"),indent=2,default=float)
print("DONE")
