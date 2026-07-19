# A2 — differential-shrinkage sensitivity: refit SL M5 and M5_no-climate with a FIXED, identical
# penalty (no independent C-selection), to bound how much of the +0.0087 matched increment is
# climate vs differential regularization of the shared case/season/RDHS terms. Gate: reproduce frozen M5.
import pandas as pd, numpy as np
from patsy import dmatrix, build_design_matrices
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
V2="/home/mpcrlab/data_quarantine/analysis_tables/dengue_climate_population_linked_2018_2025_v2_date_aligned.csv"
HYB="/home/mpcrlab/data_quarantine/model_pilots/hybrid_model_extension_v1/hybrid_model_predictions_v1.csv"
CLIMVARS=['t2m_mean_c','precip_sum_mm','rh_mean_percent']; LAGS=list(range(0,9)); clip=lambda p:np.clip(p,1e-6,1-1e-6)
m=pd.read_csv(V2,parse_dates=['week_start','week_end'])
f=m[(m.outcome_missing_flag==0)&(m.exposure_missing_flag==0)&(m.population_missing_flag==0)&(m.epi_year>=2018)&(m.epi_year<=2025)].copy().sort_values(['geometry_id','week_start']).reset_index(drop=True)
fut=f[['geometry_id','week_start','dengue_incidence_per_100k']].rename(columns={'dengue_incidence_per_100k':'inc_future'}); fut['week_start']=fut['week_start']-pd.Timedelta(days=28)
f=f.merge(fut,on=['geometry_id','week_start'],how='left'); f=f[f.inc_future.notna()].copy()
f['split']=np.where(f.epi_year<=2022,'train','test'); g=f[f.split=='train'].groupby('geometry_id')['dengue_incidence_per_100k']
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
tr=f[f.split=='train'].copy(); te=f[f.split=='test'].copy(); ytr=tr['y'].values; yte=te['y'].values
AR=['inc_t','inc_lag1','inc_lag2','inc_lag4']; VDF=LDF=3
DIs={v:dmatrix(f"cr(x, df={VDF}) - 1",{"x":tr[f'{v}__L0'].values},return_type='dataframe').design_info for v in CLIMVARS}
BLAG=np.asarray(dmatrix(f"cr(x, df={LDF}) - 1",{"x":np.array(LAGS,float)},return_type='dataframe'))
def cb(rows,v):
    n=len(rows); Vb=np.empty((n,len(LAGS),VDF))
    for i,L in enumerate(LAGS): Vb[:,i,:]=np.asarray(build_design_matrices([DIs[v]],{"x":rows[f'{v}__L{L}'].values})[0])
    return np.einsum('nlj,lk->njk',Vb,BLAG).reshape(n,VDF*LDF)
def clim(rows): return np.concatenate([cb(rows,v) for v in CLIMVARS],axis=1)
def design(rows,kind):
    if kind=='matched': return np.concatenate([rows[AR].values,rows[['sin1','cos1','sin2','cos2']+RD].values],axis=1)
    if kind=='M5': return np.concatenate([rows[AR].values,clim(rows),rows[['sin1','cos1','sin2','cos2']+RD].values],axis=1)
def fitpred(kind,C):
    X=design(tr,kind); mu=X.mean(0); sd=X.std(0); sd[sd==0]=1
    clf=LogisticRegression(penalty='l2',C=C,solver='lbfgs',max_iter=8000).fit((X-mu)/sd,ytr)
    return clip(clf.predict_proba((design(te,kind)-mu)/sd)[:,1])
def nb(y,p,t=0.30): a=p>=t;n=len(y);return (a&(y==1)).sum()/n-(a&(y==0)).sum()/n*(t/(1-t))
print("Fixed-penalty matched increment DeltaNB(M5 - M5_no-climate) at p*=0.30, by shared C:")
for C in [0.1,1.0,10.0]:
    inc=nb(yte,fitpred('M5',C))-nb(yte,fitpred('matched',C))
    print(f"  C={C:>5}: matched increment = {inc:+.5f}")
print("(independent-penalty reference: +0.0087)")
