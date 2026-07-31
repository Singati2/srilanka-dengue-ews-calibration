#!/usr/bin/env python3
"""Sri Lanka DEVELOPMENT-INCLUSIVE proper-score intervals (removes the evidentiary asymmetry).
Faithful derivative of srilanka_matched_ablation_90pct_v1.py at the 75th-percentile PRIMARY label:
refit M5 and matched no-climate and re-apply the past-only rolling-52 recalibration within each RDHS
resample, recompute paired dNLL and dBrier (full - no-climate, recalibrated) per replicate, report
development-inclusive percentile intervals. Reproduce-first gate: full-data point dNLL matches the
reported conditional -0.0207 (dBrier -0.0079). Read-only inputs; writes only under OUT.
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
OUT="/home/mpcrlab/srilanka-dengue-ews-calibration/analysis/devincl_proper_scores_v1"; os.makedirs(OUT,exist_ok=True)
CLIMVARS=['t2m_mean_c','precip_sum_mm','rh_mean_percent']; LAGS=list(range(0,9)); SEED=20260612; CGRID=[0.1,1.0,10.0]
B=int(sys.argv[1]) if len(sys.argv)>1 else 1000
NPROC=int(sys.argv[2]) if len(sys.argv)>2 else 7
EPS=1e-6; SEPS=1e-15; clip=lambda p:np.clip(p,EPS,1-EPS); logit=lambda p:np.log(clip(p)/(1-clip(p))); sig=lambda z:1/(1+np.exp(-z))
t0=time.time()
m=pd.read_csv(V2,parse_dates=['week_start','week_end'])
f=m[(m.outcome_missing_flag==0)&(m.exposure_missing_flag==0)&(m.population_missing_flag==0)&(m.epi_year>=2018)&(m.epi_year<=2025)].copy().sort_values(['geometry_id','week_start']).reset_index(drop=True)
fut=f[['geometry_id','week_start','dengue_incidence_per_100k']].rename(columns={'dengue_incidence_per_100k':'inc_future'}); fut['week_start']=fut['week_start']-pd.Timedelta(days=28)
f=f.merge(fut,on=['geometry_id','week_start'],how='left'); f=f[f.inc_future.notna()].copy()
f['split']=np.where(f.epi_year<=2022,'train','test')
g=f[f.split=='train'].groupby('geometry_id')['dengue_incidence_per_100k']
f=f.merge(g.quantile(0.75).rename('thr75').reset_index(),on='geometry_id',how='left'); f['y']=(f['inc_future']>f['thr75']).astype(int)
for L in [1,2,4]:
    t=f[['geometry_id','week_start','dengue_incidence_per_100k']].rename(columns={'dengue_incidence_per_100k':f'inc_lag{L}'}).copy(); t['week_start']=t['week_start']+pd.Timedelta(days=7*L); f=f.merge(t,on=['geometry_id','week_start'],how='left')
f['inc_t']=f['dengue_incidence_per_100k']
for v in CLIMVARS:
    for L in LAGS:
        t=f[['geometry_id','week_start',v]].rename(columns={v:f'{v}__L{L}'}).copy(); t['week_start']=t['week_start']+pd.Timedelta(days=7*L); f=f.merge(t,on=['geometry_id','week_start'],how='left')
w=2*np.pi*f['epi_week']/52.18; f['sin1'],f['cos1'],f['sin2'],f['cos2']=np.sin(w),np.cos(w),np.sin(2*w),np.cos(2*w)
rd=pd.get_dummies(f['geometry_id'],prefix='rd',drop_first=True).astype(float); f=pd.concat([f,rd],axis=1); RD=list(rd.columns)
tr0=f[f.split=='train']
for c in ['inc_lag1','inc_lag2','inc_lag4']+[f'{v}__L{L}' for v in CLIMVARS for L in LAGS]: f[c]=f[c].fillna(tr0[c].mean())
f['target_week']=f['week_start']+pd.Timedelta(days=28); f=f.reset_index(drop=True)
AR=['inc_t','inc_lag1','inc_lag2','inc_lag4']; VDF=LDF=3
DIs={v:dmatrix(f"cr(x, df={VDF}) - 1",{"x":f.loc[f.split=='train',f'{v}__L0'].values},return_type='dataframe').design_info for v in CLIMVARS}
BLAG=np.asarray(dmatrix(f"cr(x, df={LDF}) - 1",{"x":np.array(LAGS,float)},return_type='dataframe'))
def crossbasis_all(v):
    n=len(f); Vb=np.empty((n,len(LAGS),VDF))
    for i,L in enumerate(LAGS): Vb[:,i,:]=np.asarray(build_design_matrices([DIs[v]],{"x":f[f'{v}__L{L}'].values})[0])
    return np.einsum('nlj,lk->njk',Vb,BLAG).reshape(n,VDF*LDF)
CB=np.concatenate([crossbasis_all(v) for v in CLIMVARS],axis=1); ARm=f[AR].values; SG=f[['sin1','cos1','sin2','cos2']+RD].values
X_M5=np.concatenate([ARm,CB,SG],axis=1); X_MA=np.concatenate([ARm,SG],axis=1)
Y=f['y'].values; yr=f['epi_year'].values; split=f['split'].values; tw=f['target_week'].values; ws=f['week_start'].values; geo=f['geometry_id'].values
tr_idx=np.where(split=='train')[0]; te_idx=np.where(split=='test')[0]; allrows=np.arange(len(f))
def fit_select(X,rows_tr):
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
    return clf,mu,sd
def predict(clf,mu,sd,X,rows): return clip(clf.predict_proba((X[rows]-mu)/sd)[:,1])
def past_only_recal(p_all,rows_all,test_rows,WIN=52):
    pos={r:i for i,r in enumerate(rows_all)}; tw_all=tw[rows_all]; y_all=Y[rows_all]; z_all=logit(p_all)
    test_ws=ws[test_rows]; tpos=np.array([pos[r] for r in test_rows]); rec=np.empty(len(test_rows))
    for wk in np.unique(test_ws):
        elig=(tw_all<wk)&(tw_all>=wk-np.timedelta64(7*WIN,'D')); ye=y_all[elig]; ze=z_all[elig]; a=0.0
        if ye.sum()>=1 and (len(ye)-ye.sum())>=1 and len(ye)>=20:
            try:
                r=sm.GLM(ye,np.ones((len(ye),1)),family=sm.families.Binomial(),offset=ze).fit()
                if abs(float(r.params[0]))<=15 and np.isfinite(r.params[0]): a=float(r.params[0])
            except Exception: a=0.0
        sel=np.where(test_ws==wk)[0]; rec[sel]=clip(sig(logit(p_all[tpos[sel]])+a))
    return rec
def nll(y,p): p=np.clip(p,SEPS,1-SEPS); return float(np.mean(-(y*np.log(p)+(1-y)*np.log(1-p))))
def brier(y,p): return float(np.mean((p-y)**2))
def recal_deltas(rows_tr,rows_te):
    c5=fit_select(X_M5,rows_tr); ca=fit_select(X_MA,rows_tr); rall=np.concatenate([rows_tr,rows_te])
    p5a=predict(*c5,X_M5,rall); paa=predict(*ca,X_MA,rall)
    r5=past_only_recal(p5a,rall,rows_te); ra=past_only_recal(paa,rall,rows_te); y=Y[rows_te]
    return nll(y,r5)-nll(y,ra), brier(y,r5)-brier(y,ra), c5, r5
# GATE
dNLL,dBrier,c5,r5=recal_deltas(tr_idx,te_idx)
hyb=pd.read_csv(HYB,parse_dates=['week_start']); key=['geometry_id','week_start']
p5_te=predict(*c5,X_M5,te_idx); tv=pd.DataFrame({'geometry_id':geo[te_idx],'week_start':ws[te_idx],'M5n':p5_te}).merge(hyb[key+['p_M5_hybrid_season_RDHS']],on=key)
d5=float(np.abs(tv['M5n']-tv['p_M5_hybrid_season_RDHS']).max())
gate=(d5<1e-6) and abs(dNLL-(-0.0207))<=0.003 and abs(dBrier-(-0.0079))<=0.003
print(f"GATE: M5vsfrozen={d5:.1e} dNLL={dNLL:+.5f} (target -0.0207) dBrier={dBrier:+.5f} (target -0.0079) -> {'PASS' if gate else 'FAIL'} [{time.time()-t0:.0f}s]",flush=True)
if not gate: raise SystemExit("*** GATE FAILED ***")
# DI RDHS bootstrap
rd_ids=sorted(np.unique(geo)); rng=np.random.default_rng(SEED); K=len(rd_ids)
tr_by={gg:tr_idx[geo[tr_idx]==gg] for gg in rd_ids}; te_by={gg:te_idx[geo[te_idx]==gg] for gg in rd_ids}
PICKS=[[rd_ids[i] for i in rng.integers(0,K,K)] for _ in range(B)]
def worker(pick):
    rtr=np.concatenate([tr_by[gg] for gg in pick]); rte=np.concatenate([te_by[gg] for gg in pick if len(te_by[gg])>0])
    if len(np.unique(Y[rtr]))<2 or len(np.unique(Y[rte]))<2: return None
    try:
        a,b,_,_=recal_deltas(rtr,rte); return (a,b)
    except Exception: return None
if __name__=='__main__':
    with Pool(NPROC) as pool: out=pool.map(worker,PICKS,chunksize=2)
    ok=[x for x in out if x is not None]; nllD=np.array([x[0] for x in ok]); brD=np.array([x[1] for x in ok]); fails=len(out)-len(ok)
    def ci(a): return [round(float(np.percentile(a,2.5)),5),round(float(np.percentile(a,97.5)),5)]
    res={"analysis":"srilanka_devincl_proper_scores","label":"75th-pct primary, recalibrated","B":B,"seed":SEED,
     "gate":{"M5_vs_frozen":d5},"point":{"dNLL":round(dNLL,5),"dBrier":round(dBrier,5)},
     "development_inclusive_RDHS":{"dNLL":{"point":round(dNLL,5),"ci":ci(nllD),"median":round(float(np.median(nllD)),5)},
        "dBrier":{"point":round(dBrier,5),"ci":ci(brD),"median":round(float(np.median(brD)),5)},"replicates_used":len(ok),"failures":fails},
     "conditional_reference_from_manuscript":{"dNLL":-0.0207,"dBrier":-0.0079},"seconds":round(time.time()-t0,1)}
    json.dump(res,open(f'{OUT}/srilanka_devincl_properscore_results.json','w'),indent=2)
    pd.DataFrame({"dNLL":pd.Series(nllD),"dBrier":pd.Series(brD)}).to_csv(f'{OUT}/srilanka_devincl_properscore_distribution.csv',index=False)
    print(json.dumps(res,indent=2),flush=True); print("DONE",flush=True)
