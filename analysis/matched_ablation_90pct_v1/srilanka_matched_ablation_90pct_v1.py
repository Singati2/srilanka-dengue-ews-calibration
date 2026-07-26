#!/usr/bin/env python3
"""Sri Lanka matched climate ablation at the 90th-percentile outbreak label (SPEED-OPTIMIZED).
Pre-registered in docs/matched_ablation_90th_percentile_spec.md (reviewer finding #1).

Numerically identical to the verbatim sl_devinclusive_B1000.py pipeline (feature build, cross-basis,
fit_select rolling-origin C-selection, past-only rolling-52 recalibration, nb) but the
development-inclusive RDHS-refit bootstrap replicates run in PARALLEL across cores over
PRE-GENERATED (seeded, deterministic) RDHS resample picks — identical picks & fits, just concurrent.
ONLY the per-unit outcome quantile changes (0.75 -> 0.90) on the TRAINING split.
Reproduce-first gate at 75th (point only): M5 vs frozen <1e-6 AND conditional recal matched +0.0157.
Read-only inputs; writes only under OUT. Nothing committed.
"""
import os
os.environ.setdefault('OMP_NUM_THREADS','1'); os.environ.setdefault('OPENBLAS_NUM_THREADS','1'); os.environ.setdefault('MKL_NUM_THREADS','1')
import sys, pandas as pd, numpy as np, json, time, warnings
from patsy import dmatrix, build_design_matrices
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
import statsmodels.api as sm
from multiprocessing import Pool
warnings.filterwarnings('ignore')
V2="/home/mpcrlab/data_quarantine/analysis_tables/dengue_climate_population_linked_2018_2025_v2_date_aligned.csv"
HYB="/home/mpcrlab/data_quarantine/model_pilots/hybrid_model_extension_v1/hybrid_model_predictions_v1.csv"
OUT="/home/mpcrlab/srilanka-dengue-ews-calibration/analysis/matched_ablation_90pct_v1"; os.makedirs(OUT,exist_ok=True)
CLIMVARS=['t2m_mean_c','precip_sum_mm','rh_mean_percent']; LAGS=list(range(0,9)); SEED=20260612; CGRID=[0.1,1.0,10.0]
B=int(sys.argv[1]) if len(sys.argv)>1 else 1000
NPROC=int(sys.argv[2]) if len(sys.argv)>2 else 14
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
f=f.merge(g.quantile(0.90).rename('thr90').reset_index(),on='geometry_id',how='left')   # NEW: 90th train-only threshold
f['y75']=(f['inc_future']>f['thr75']).astype(int); f['y90']=(f['inc_future']>f['thr90']).astype(int)
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
def crossbasis_all(v):
    n=len(f); Vb=np.empty((n,len(LAGS),VDF))
    for i,L in enumerate(LAGS): Vb[:,i,:]=np.asarray(build_design_matrices([DIs[v]],{"x":f[f'{v}__L{L}'].values})[0])
    return np.einsum('nlj,lk->njk',Vb,BLAG).reshape(n,VDF*LDF)
CB=np.concatenate([crossbasis_all(v) for v in CLIMVARS],axis=1)
ARm=f[AR].values; SG=f[['sin1','cos1','sin2','cos2']+RD].values
X_M5=np.concatenate([ARm,CB,SG],axis=1); X_MA=np.concatenate([ARm,SG],axis=1)
yr=f['epi_year'].values; split=f['split'].values; tw=f['target_week'].values; ws=f['week_start'].values; geo=f['geometry_id'].values
tr_idx=np.where(split=='train')[0]; te_idx=np.where(split=='test')[0]; allrows=np.arange(len(f))

def fit_select(X,rows_tr,Y):
    Xt=X[rows_tr]; yt=Y[rows_tr]; yrt=yr[rows_tr]; mu=Xt.mean(0); sd=Xt.std(0); sd[sd==0]=1
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
    if np.abs(clf.coef_).max()>15: clf=LogisticRegression(penalty='l2',C=0.1,solver='lbfgs',max_iter=6000).fit((Xt-mu)/sd,yt)
    return clf,mu,sd,bestC
def predict(clf,mu,sd,X,rows): return clip(clf.predict_proba((X[rows]-mu)/sd)[:,1])
def past_only_recal(p_all_full,rows_all,test_rows,Y,WIN=52):
    pos={r:i for i,r in enumerate(rows_all)}; tw_all=tw[rows_all]; y_all=Y[rows_all]; z_all=logit(p_all_full)
    test_ws=ws[test_rows]; tpos=np.array([pos[r] for r in test_rows]); rec=np.empty(len(test_rows))
    for wk in np.unique(test_ws):
        elig=(tw_all<wk)&(tw_all>=wk-np.timedelta64(7*WIN,'D')); ye=y_all[elig]; ze=z_all[elig]; a=0.0
        if ye.sum()>=1 and (len(ye)-ye.sum())>=1 and len(ye)>=20:
            try:
                r=sm.GLM(ye,np.ones((len(ye),1)),family=sm.families.Binomial(),offset=ze).fit()
                if abs(float(r.params[0]))<=15 and np.isfinite(r.params[0]): a=float(r.params[0])
            except Exception: a=0.0
        sel=np.where(test_ws==wk)[0]; rec[sel]=clip(sig(logit(p_all_full[tpos[sel]])+a))
    return rec
def nb(y,p,t=0.30): a=p>=t; n=len(y); return (a&(y==1)).sum()/n-(a&(y==0)).sum()/n*(t/(1-t))
def point(Y):
    c5=fit_select(X_M5,tr_idx,Y); ca=fit_select(X_MA,tr_idx,Y)
    p5_all=predict(*c5[:3],X_M5,allrows); pa_all=predict(*ca[:3],X_MA,allrows)
    r5=past_only_recal(p5_all,allrows,te_idx,Y); ra=past_only_recal(pa_all,allrows,te_idx,Y)
    p5_te=predict(*c5[:3],X_M5,te_idx); pa_te=predict(*ca[:3],X_MA,te_idx)
    return p5_te,pa_te,r5,ra,c5,ca

# ---- GATE (75th, point only) ----
Y75=f['y75'].values; p5_te,pa_te,r5,ra,c5,_=point(Y75)
hyb=pd.read_csv(HYB,parse_dates=['week_start']); key=['geometry_id','week_start']
tv=pd.DataFrame({'geometry_id':geo[te_idx],'week_start':ws[te_idx],'M5n':p5_te}).merge(hyb[key+['p_M5_hybrid_season_RDHS']],on=key)
d5=float(np.abs(tv['M5n']-tv['p_M5_hybrid_season_RDHS']).max())
raw75=round(float(nb(Y75[te_idx],p5_te)-nb(Y75[te_idx],pa_te)),5); rec75=round(float(nb(Y75[te_idx],r5)-nb(Y75[te_idx],ra)),5)
gate=(d5<1e-6) and abs(rec75-0.0157)<=0.0015
print(f"GATE 75th: max|Δ|M5 vs frozen={d5:.2e} | raw={raw75} recal={rec75} (t +0.0157) -> {'PASS' if gate else 'FAIL'} [{time.time()-t0:.0f}s]",flush=True)
if not gate: raise SystemExit("*** GATE FAILED — aborting ***")

# ---- 90th POINT ----
Y90=f['y90'].values
p5_te,pa_te,r5_90,ra_90,c5,ca=point(Y90)
raw90=round(float(nb(Y90[te_idx],p5_te)-nb(Y90[te_idx],pa_te)),5); rec90=round(float(nb(Y90[te_idx],r5_90)-nb(Y90[te_idx],ra_90)),5)
prev90=float(Y90[te_idx].mean())
print(f"90th POINT: prev={prev90:.4f} events={int(Y90[te_idx].sum())} n={len(te_idx)} raw={raw90} recal={rec90} [{time.time()-t0:.0f}s]",flush=True)

# ---- DI RDHS-refit bootstrap at 90th (PRIMARY, parallel over pre-generated picks) ----
rd_ids=sorted(np.unique(geo)); rng=np.random.default_rng(SEED); K=len(rd_ids)
tr_by={gg:tr_idx[geo[tr_idx]==gg] for gg in rd_ids}; te_by={gg:te_idx[geo[te_idx]==gg] for gg in rd_ids}
PICKS=[[rd_ids[i] for i in rng.integers(0,K,K)] for _ in range(B)]
def di_worker(pick):
    rtr=np.concatenate([tr_by[gg] for gg in pick]); rte=np.concatenate([te_by[gg] for gg in pick if len(te_by[gg])>0])
    if len(np.unique(Y90[rtr]))<2 or len(np.unique(Y90[rte]))<2: return None
    try:
        c5b=fit_select(X_M5,rtr,Y90); cab=fit_select(X_MA,rtr,Y90); rall=np.concatenate([rtr,rte])
        p5a=predict(*c5b[:3],X_M5,rall); paa=predict(*cab[:3],X_MA,rall)
        r5b=past_only_recal(p5a,rall,rte,Y90); rab=past_only_recal(paa,rall,rte,Y90)
        p5t=predict(*c5b[:3],X_M5,rte); pat=predict(*cab[:3],X_MA,rte)
        return (float(nb(Y90[rte],p5t)-nb(Y90[rte],pat)), float(nb(Y90[rte],r5b)-nb(Y90[rte],rab)))
    except Exception: return None
if __name__=='__main__':
    with Pool(NPROC) as pool:
        out=pool.map(di_worker,PICKS,chunksize=2)
    raw_D=np.array([x[0] for x in out if x is not None]); rec_D=np.array([x[1] for x in out if x is not None]); fails=int(sum(x is None for x in out))
    print(f"DI done: used={len(rec_D)} fails={fails}  [{time.time()-t0:.0f}s]",flush=True)
    # conditional RDHS bootstrap (secondary, frozen recal preds)
    geo_te=geo[te_idx]; idx_by={gg:np.where(geo_te==gg)[0] for gg in rd_ids}; rng2=np.random.default_rng(SEED); cond_D=[]
    for _ in range(B):
        pick=[rd_ids[i] for i in rng2.integers(0,K,K)]; ii=np.concatenate([idx_by[gg] for gg in pick if len(idx_by[gg])>0]); yb=Y90[te_idx][ii]
        if len(np.unique(yb))<2: continue
        cond_D.append(nb(yb,r5_90[ii])-nb(yb,ra_90[ii]))
    cond_D=np.array(cond_D)
    def ci(a): return [round(float(np.percentile(a,2.5)),5),round(float(np.percentile(a,97.5)),5)]
    res={"analysis":"srilanka_matched_ablation_90pct","B":B,"seed":SEED,
     "gate_75th":{"maxabs_M5_vs_frozen":d5,"raw":raw75,"recal":rec75,"passed":bool(gate)},
     "point_90th":{"prevalence":round(prev90,4),"events":int(Y90[te_idx].sum()),"n":int(len(te_idx)),"raw_dNB":raw90,"recal_dNB":rec90,"C_M5":c5[3]},
     "development_inclusive_RDHS":{
        "raw_matched":{"point":raw90,"ci":ci(raw_D),"median":round(float(np.median(raw_D)),5)},
        "recal_matched":{"point":rec90,"ci":ci(rec_D),"median":round(float(np.median(rec_D)),5)},
        "replicates_used":int(len(rec_D)),"failures":fails},
     "conditional_RDHS":{"recal_matched":{"point":rec90,"ci":ci(cond_D),"replicates_used":int(len(cond_D))}},
     "reference_75th_from_manuscript":{"raw":0.0087,"recal":0.0157,"recal_conditional":[0.0066,0.0257],"recal_DI":[-0.0002,0.0302]},
     "seconds":round(time.time()-t0,1)}
    json.dump(res,open(f'{OUT}/srilanka_matched_ablation_90pct_results.json','w'),indent=2)
    pd.DataFrame({"raw_DI":pd.Series(raw_D),"recal_DI":pd.Series(rec_D),"recal_cond":pd.Series(cond_D)}).to_csv(f'{OUT}/srilanka_matched_ablation_90pct_distribution.csv',index=False)
    print(json.dumps(res,indent=2),flush=True); print("DONE",flush=True)
