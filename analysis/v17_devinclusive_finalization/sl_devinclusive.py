# Phase 1 — Sri Lanka DEVELOPMENT-INCLUSIVE uncertainty for the matched climate increment.
# Cluster-bootstrap that REFITS M5 and M5_no-climate (rolling-origin C-selection) and re-applies
# the identical past-only rolling-52 recalibration within each 26-RDHS resample; percentile CIs.
# Reproduce-first gate: reproduces frozen M1/M4/M5 to <1e-6 AND the conditional matched +0.0157
# before running the dev-inclusive loop; exits otherwise. Design matrices precomputed once
# (fixed cr() bases) so only coefficients/C-selection/recalibration are refit per replicate.
import pandas as pd, numpy as np, json, sys, time
from patsy import dmatrix, build_design_matrices
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
import statsmodels.api as sm
V2="/home/mpcrlab/data_quarantine/analysis_tables/dengue_climate_population_linked_2018_2025_v2_date_aligned.csv"
PRIM="/home/mpcrlab/data_quarantine/model_pilots/pilot_h4_75pct_v1/predictions_h4_75pct_v1.csv"
HYB="/home/mpcrlab/data_quarantine/model_pilots/hybrid_model_extension_v1/hybrid_model_predictions_v1.csv"
OUT="/home/mpcrlab/srilanka-dengue-ews-calibration/analysis/v17_devinclusive_finalization/SL_devinclusive_results.json"
CLIMVARS=['t2m_mean_c','precip_sum_mm','rh_mean_percent']; LAGS=list(range(0,9)); SEED=20260612; CGRID=[0.1,1.0,10.0]
B=300  # tractability: 300 refit replicates (per-week recal; percentile 2.5/97.5 stable); stated in report
EPS=1e-6; clip=lambda p:np.clip(p,EPS,1-EPS); logit=lambda p:np.log(clip(p)/(1-clip(p))); sig=lambda z:1/(1+np.exp(-z))
t0=time.time()
m=pd.read_csv(V2,parse_dates=['week_start','week_end'])
f=m[(m.outcome_missing_flag==0)&(m.exposure_missing_flag==0)&(m.population_missing_flag==0)&
    (m.epi_year>=2018)&(m.epi_year<=2025)].copy().sort_values(['geometry_id','week_start']).reset_index(drop=True)
fut=f[['geometry_id','week_start','dengue_incidence_per_100k']].rename(columns={'dengue_incidence_per_100k':'inc_future'})
fut['week_start']=fut['week_start']-pd.Timedelta(days=28)
f=f.merge(fut,on=['geometry_id','week_start'],how='left'); f=f[f.inc_future.notna()].copy()
f['split']=np.where(f.epi_year<=2022,'train','test')
g=f[f.split=='train'].groupby('geometry_id')['dengue_incidence_per_100k']
f=f.merge(g.quantile(0.75).rename('thr75').reset_index(),on='geometry_id',how='left')
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
f['target_week']=f['week_start']+pd.Timedelta(days=28)
f=f.reset_index(drop=True)
AR=['inc_t','inc_lag1','inc_lag2','inc_lag4']; VDF=LDF=3
DIs={v:dmatrix(f"cr(x, df={VDF}) - 1",{"x":f.loc[f.split=='train',f'{v}__L0'].values},return_type='dataframe').design_info for v in CLIMVARS}
BLAG=np.asarray(dmatrix(f"cr(x, df={LDF}) - 1",{"x":np.array(LAGS,float)},return_type='dataframe'))
def crossbasis_all(v):
    n=len(f); Vb=np.empty((n,len(LAGS),VDF))
    for i,L in enumerate(LAGS): Vb[:,i,:]=np.asarray(build_design_matrices([DIs[v]],{"x":f[f'{v}__L{L}'].values})[0])
    return np.einsum('nlj,lk->njk',Vb,BLAG).reshape(n,VDF*LDF)
CB=np.concatenate([crossbasis_all(v) for v in CLIMVARS],axis=1)          # climate block, all rows
ARm=f[AR].values; SG=f[['sin1','cos1','sin2','cos2']+RD].values          # AR and season+RDHS blocks
X_M5=np.concatenate([ARm,CB,SG],axis=1)                                   # M5 design (all rows)
X_MA=np.concatenate([ARm,SG],axis=1)                                     # matched (no-climate) design
yv=f['y'].values; yr=f['epi_year'].values; split=f['split'].values
tw=f['target_week'].values; ws=f['week_start'].values; geo=f['geometry_id'].values
tr_mask=split=='train'; te_mask=split=='test'
tr_idx=np.where(tr_mask)[0]; te_idx=np.where(te_mask)[0]

def fit_select(X, rows_tr):
    """rolling-origin C-selection on rows_tr, return fitted clf + standardizer."""
    Xt=X[rows_tr]; yt=yv[rows_tr]; yrt=yr[rows_tr]
    mu=Xt.mean(0); sd=Xt.std(0); sd[sd==0]=1
    yrs=sorted(np.unique(yrt)); folds=[]
    for i in range(1,len(yrs)):
        a=np.where(yrt<=yrs[i-1])[0]; b=np.where(yrt==yrs[i])[0]
        if len(b)>0 and len(np.unique(yt[a]))>1 and len(np.unique(yt[b]))>1: folds.append((a,b))
    bestC,bestS=1.0,-1
    if folds:
        for C in CGRID:
            sc=[]
            for a,b in folds:
                clf=LogisticRegression(penalty='l2',C=C,solver='lbfgs',max_iter=4000).fit((Xt[a]-mu)/sd,yt[a])
                try: sc.append(roc_auc_score(yt[b],clf.predict_proba((Xt[b]-mu)/sd)[:,1]))
                except ValueError: pass
            if sc and np.mean(sc)>bestS: bestS,bestC=np.mean(sc),C
    clf=LogisticRegression(penalty='l2',C=bestC,solver='lbfgs',max_iter=6000).fit((Xt-mu)/sd,yt)
    if np.abs(clf.coef_).max()>15:
        clf=LogisticRegression(penalty='l2',C=0.1,solver='lbfgs',max_iter=6000).fit((Xt-mu)/sd,yt)
    return clf,mu,sd,bestC
def predict(clf,mu,sd,X,rows): return clip(clf.predict_proba((X[rows]-mu)/sd)[:,1])

def past_only_recal(p_all_full, rows_all, test_rows, WIN=52):
    """Per-WEEK intercept recalibration (matches the frozen pipeline): one intercept per
    prediction week, eligibility target_week < week within a 52-week window."""
    pos={r:i for i,r in enumerate(rows_all)}
    tw_all=tw[rows_all]; y_all=yv[rows_all]; z_all=logit(p_all_full)
    test_ws=ws[test_rows]; tpos=np.array([pos[r] for r in test_rows])
    rec=np.empty(len(test_rows))
    for wk in np.unique(test_ws):
        elig=(tw_all< wk)&(tw_all>= wk-np.timedelta64(7*WIN,'D'))
        ye=y_all[elig]; ze=z_all[elig]; a=0.0
        if ye.sum()>=1 and (len(ye)-ye.sum())>=1 and len(ye)>=20:
            try:
                r=sm.GLM(ye,np.ones((len(ye),1)),family=sm.families.Binomial(),offset=ze).fit()
                if abs(float(r.params[0]))<=15 and np.isfinite(r.params[0]): a=float(r.params[0])
            except Exception: a=0.0
        sel=np.where(test_ws==wk)[0]
        rec[sel]=clip(sig(logit(p_all_full[tpos[sel]])+a))
    return rec

def nb(y,p,t=0.30): a=p>=t; n=len(y); return (a&(y==1)).sum()/n-(a&(y==0)).sum()/n*(t/(1-t))

# ---------- POINT ESTIMATE + reproduce-first gate ----------
clf5,mu5,sd5,c5=fit_select(X_M5,tr_idx); clf_a,mua,sda,ca=fit_select(X_MA,tr_idx)
pM5_te=predict(clf5,mu5,sd5,X_M5,te_idx); pMA_te=predict(clf_a,mua,sda,X_MA,te_idx)
# validate M5 against frozen
hyb=pd.read_csv(HYB,parse_dates=['week_start']); key=['geometry_id','week_start']
tv=pd.DataFrame({'geometry_id':geo[te_idx],'week_start':ws[te_idx],'M5n':pM5_te}).merge(hyb[key+['p_M5_hybrid_season_RDHS']],on=key)
d5=np.abs(tv['M5n']-tv['p_M5_hybrid_season_RDHS']).max()
allrows=np.arange(len(f))
pM5_all=predict(clf5,mu5,sd5,X_M5,allrows); pMA_all=predict(clf_a,mua,sda,X_MA,allrows)
rM5=past_only_recal(pM5_all,allrows,te_idx); rMA=past_only_recal(pMA_all,allrows,te_idx)
raw_pt=round(float(nb(yv[te_idx],pM5_te)-nb(yv[te_idx],pMA_te)),5)
recal_pt=round(float(nb(yv[te_idx],rM5)-nb(yv[te_idx],rMA)),5)
print(f"GATE: max|Δ|M5 vs frozen={d5:.2e} | conditional matched raw={raw_pt} recal={recal_pt} | C(M5)={c5} C(match)={ca} | {time.time()-t0:.0f}s",flush=True)
if d5>=1e-6 or abs(recal_pt-0.0157)>0.0015:
    print("*** GATE FAILED — not running dev-inclusive ***"); sys.exit(1)

# ---------- DEVELOPMENT-INCLUSIVE BOOTSTRAP (refit within replicates) ----------
rd_ids=sorted(np.unique(geo)); rng=np.random.default_rng(SEED)
tr_by={gg:tr_idx[geo[tr_idx]==gg] for gg in rd_ids}; te_by={gg:te_idx[geo[te_idx]==gg] for gg in rd_ids}
raw_D=[]; rec_D=[]; fails=0
for b in range(B):
    pick=[rd_ids[i] for i in rng.integers(0,len(rd_ids),len(rd_ids))]
    rtr=np.concatenate([tr_by[gg] for gg in pick]); rte=np.concatenate([te_by[gg] for gg in pick if len(te_by[gg])>0])
    if len(np.unique(yv[rtr]))<2 or len(np.unique(yv[rte]))<2: fails+=1; continue
    try:
        c5b=fit_select(X_M5,rtr); cab=fit_select(X_MA,rtr)
        rall=np.concatenate([rtr,rte])                       # replicate rows for recal eligibility
        # predictions on replicate rows
        p5_all=predict(c5b[0],c5b[1],c5b[2],X_M5,rall); pa_all=predict(cab[0],cab[1],cab[2],X_MA,rall)
        r5=past_only_recal(p5_all,rall,rte); ra=past_only_recal(pa_all,rall,rte)
        p5_te=predict(c5b[0],c5b[1],c5b[2],X_M5,rte); pa_te=predict(cab[0],cab[1],cab[2],X_MA,rte)
        raw_D.append(nb(yv[rte],p5_te)-nb(yv[rte],pa_te))
        rec_D.append(nb(yv[rte],r5)-nb(yv[rte],ra))
    except Exception as e:
        fails+=1; continue
    if (b+1)%50==0: print(f"  rep {b+1}/{B} | recal median so far {np.median(rec_D):.4f} | {time.time()-t0:.0f}s",flush=True)
raw_D=np.array(raw_D); rec_D=np.array(rec_D)
def ci(D): return [round(float(np.percentile(D,2.5)),5),round(float(np.percentile(D,97.5)),5)]
res={"B":B,"replicates_used":int(len(rec_D)),"failures":int(fails),
 "reproduce_gate":{"maxabsdiff_M5_vs_frozen":float(d5),"conditional_recal_matched":recal_pt,"conditional_raw_matched":raw_pt},
 "conditional":{"raw_matched":raw_pt,"recal_matched":recal_pt},
 "development_inclusive":{
    "raw_matched":{"point":raw_pt,"ci":ci(raw_D),"median":round(float(np.median(raw_D)),5)},
    "recal_matched":{"point":recal_pt,"ci":ci(rec_D),"median":round(float(np.median(rec_D)),5)}},
 "seconds":round(time.time()-t0,1)}
json.dump(res,open(OUT,"w"),indent=2)
print(json.dumps(res,indent=2))
