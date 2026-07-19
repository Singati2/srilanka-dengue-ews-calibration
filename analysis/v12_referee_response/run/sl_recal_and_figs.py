# Blocker 2 (SL recalibration sensitivity) + Blocker 5 (SL calibration & DCA figures)
# Uses frozen SL per-obs test predictions (raw, un-recalibrated) for M1/M4/M5.
import pandas as pd, numpy as np, json
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import brier_score_loss
np.random.seed(20260612)
RUN="/home/mpcrlab/srilanka-dengue-ews-calibration/analysis/v12_referee_response/run/"
FIG="/home/mpcrlab/srilanka-dengue-ews-calibration/analysis/v12_referee_response/fig/"
d=pd.read_csv("/home/mpcrlab/data_quarantine/model_pilots/hybrid_model_extension_v1/hybrid_model_predictions_v1.csv")
y=d.y.values.astype(int)
mods={'M1':'p_M1','M4':'p_M4_hybrid','M5':'p_M5_hybrid_season_RDHS'}
P={m:np.clip(d[c].values,1e-6,1-1e-6) for m,c in mods.items()}
def nb(p,yy,t=0.30): a=p>=t; n=len(yy); return (a&(yy==1)).sum()/n-(a&(yy==0)).sum()/n*(t/(1-t))
def citl(p,yy):
    lo=np.log(p/(1-p)); m=LogisticRegression(C=1e9,max_iter=1000).fit(np.zeros((len(yy),1)),yy) if False else None
    # CITL = intercept of logistic(y ~ offset=logit(p)); slope fit separately
    import statsmodels.api as sm
    return None
def cal_intercept_slope(p,yy):
    lo=np.log(p/(1-p))
    # slope: y ~ a + b*logit(p)
    X=np.column_stack([np.ones_like(lo),lo]);
    m=LogisticRegression(C=1e9,max_iter=2000,fit_intercept=False).fit(X,yy)
    a,b=m.coef_[0]
    # CITL: y ~ intercept + offset(logit p)  => fit intercept only with slope fixed 1
    from scipy.optimize import minimize_scalar
    def nll(c):
        z=c+lo; pp=1/(1+np.exp(-z)); pp=np.clip(pp,1e-9,1-1e-9); return -np.sum(yy*np.log(pp)+(1-yy)*np.log(1-pp))
    r=minimize_scalar(nll,bounds=(-10,10),method='bounded'); return float(r.x),float(b)

# ---------- Blocker 2: cross-fitted (leakage-free within test) Platt recalibration ----------
# 2-fold cross-fit by week parity so recalibration is never fit and applied on same rows.
wk=pd.to_datetime(d.week_start).view('int64').values
fold=(pd.to_datetime(d.week_start).dt.isocalendar().week.astype(int).values % 2).astype(int)
def crossfit_recal(p):
    out=np.zeros_like(p)
    for f in [0,1]:
        tr=fold!=f; te=fold==f
        lo=np.log(p/(1-p))
        pl=LogisticRegression(C=1e6,max_iter=1000).fit(lo[tr].reshape(-1,1),y[tr])
        out[te]=pl.predict_proba(lo[te].reshape(-1,1))[:,1]
    return np.clip(out,1e-6,1-1e-6)
Pr={m:crossfit_recal(P[m]) for m in mods}

res={'raw':{},'recal_crossfit':{}}
for m in mods:
    ai,sl=cal_intercept_slope(P[m],y); air,slr=cal_intercept_slope(Pr[m],y)
    res['raw'][m]={'NB30':nb(P[m],y),'CITL':ai,'slope':sl,'Brier':brier_score_loss(y,P[m])}
    res['recal_crossfit'][m]={'NB30':nb(Pr[m],y),'CITL':air,'slope':slr,'Brier':brier_score_loss(y,Pr[m])}
res['contrasts']={
 'raw_M4_M1':nb(P['M4'],y)-nb(P['M1'],y),'raw_M5_M1':nb(P['M5'],y)-nb(P['M1'],y),
 'recal_M4_M1':nb(Pr['M4'],y)-nb(Pr['M1'],y),'recal_M5_M1':nb(Pr['M5'],y)-nb(Pr['M1'],y)}
# cluster bootstrap CI (RDHS) for recalibrated contrasts
rd=d.geometry_id.values; uq=np.array(sorted(set(rd))); byd={u:np.where(rd==u)[0] for u in uq}
rng=np.random.default_rng(20260612)
def bootci(pa,pb):
    D=[]
    for _ in range(1000):
        ii=np.concatenate([byd[u] for u in rng.choice(uq,len(uq),True)]); D.append(nb(pa[ii],y[ii])-nb(pb[ii],y[ii]))
    return [float(np.percentile(D,2.5)),float(np.percentile(D,97.5))]
res['recal_ci']={'M4_M1':bootci(Pr['M4'],Pr['M1']),'M5_M1':bootci(Pr['M5'],Pr['M1'])}
json.dump(res,open(RUN+"sl_recal_results.json","w"),indent=2)
print("SL recalibration sensitivity (cross-fitted Platt):")
for m in mods: print(f"  {m}: raw NB30={res['raw'][m]['NB30']:.4f} CITL={res['raw'][m]['CITL']:+.3f} slope={res['raw'][m]['slope']:.3f} | recal NB30={res['recal_crossfit'][m]['NB30']:.4f} CITL={res['recal_crossfit'][m]['CITL']:+.3f} slope={res['recal_crossfit'][m]['slope']:.3f}")
print(f"  ΔNB(M4-M1): raw {res['contrasts']['raw_M4_M1']:+.4f} -> recal {res['contrasts']['recal_M4_M1']:+.4f} CI {res['recal_ci']['M4_M1']}")
print(f"  ΔNB(M5-M1): raw {res['contrasts']['raw_M5_M1']:+.4f} -> recal {res['contrasts']['recal_M5_M1']:+.4f} CI {res['recal_ci']['M5_M1']}")

# ---------- Blocker 5: SL calibration + dense DCA figures ----------
def calplot(ax,Pd,tag):
    for m,ls in zip(mods,['-o','-s','-^']):
        p=Pd[m]; q=pd.qcut(p,10,duplicates='drop'); dfp=pd.DataFrame({'p':p,'y':y,'q':q})
        g=dfp.groupby('q',observed=True).agg(pm=('p','mean'),ym=('y','mean'))
        ax.plot(g.pm,g.ym,ls,label=m,ms=4)
    ax.plot([0,1],[0,1],'k--',lw=.8); ax.set_xlim(0,.8); ax.set_ylim(0,.8)
    ax.set_xlabel('Mean predicted'); ax.set_ylabel('Observed'); ax.set_title(tag); ax.legend(fontsize=7)
fig,axs=plt.subplots(1,2,figsize=(8,3.6))
calplot(axs[0],P,'Sri Lanka: raw'); calplot(axs[1],Pr,'Sri Lanka: cross-fit recalibrated')
plt.tight_layout(); plt.savefig(FIG+"fig_sl_calibration.pdf"); plt.close()

grid=np.linspace(0.05,0.5,19)
fig,ax=plt.subplots(figsize=(5,3.8))
for m,ls in zip(mods,['-','--','-.']):
    ax.plot(grid,[nb(Pr[m],y,t) for t in grid],ls,label=m)
prev=y.mean(); ax.plot(grid,[prev-(1-prev)*(t/(1-t)) for t in grid],':',color='gray',label='alert-all')
ax.axhline(0,color='k',lw=.6); ax.axvline(0.30,color='r',lw=.5,ls=':')
ax.set_xlabel('Threshold $p^*$'); ax.set_ylabel('Net benefit'); ax.set_title('Sri Lanka decision curves (recalibrated)'); ax.legend(fontsize=7)
plt.tight_layout(); plt.savefig(FIG+"fig_sl_dca.pdf"); plt.close()
print("SL figures written: fig_sl_calibration.pdf, fig_sl_dca.pdf")
print("DONE")
