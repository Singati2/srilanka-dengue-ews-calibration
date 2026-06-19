#!/usr/bin/env python3
"""E1 decision-threshold / ΔNB robustness (per docs/decision_threshold_dnb_robustness_spec.md).
Recomputes NB/ΔNB across p*=0.10-0.50 and GID_2 cluster-bootstrap CIs from STORED per-test-row predictions.
NO model refit; NO prediction regeneration; NO label/threshold recompute. Colombia only (Sri Lanka deferred).
Does NOT modify the committed h4 or horizon dirs. Outputs to a new versioned dir only."""
import pandas as pd, numpy as np, json, hashlib, os
H4='/home/mpcrlab/data_quarantine/colombia_model_pilots/model_ladder_h4_75pct_v1/colombia_model_predictions_h4_75pct_v1.csv'
HZ='/home/mpcrlab/data_quarantine/colombia_model_pilots/horizon_sensitivity_v1/colombia_horizon_predictions_v1.csv'
OUT='/home/mpcrlab/data_quarantine/colombia_model_pilots/decision_threshold_dnb_robustness_v1'; os.makedirs(OUT,exist_ok=True)
GRID=[round(x,2) for x in np.arange(0.10,0.51,0.05)]; CURVE=[round(x,2) for x in np.arange(0.05,0.51,0.05)]
B=1000; SEED=20260612
def nb(y,p,t):
    pos=p>=t; n=len(y); tp=np.sum(pos&(y==1)); fp=np.sum(pos&(y==0)); return tp/n-(fp/n)*(t/(1-t))
def boot_dnb(y,pa,pb,units,thr):
    """ΔNB(a-b) bootstrap over GID_2 clusters; returns {t:(lo,med,hi)} + fail_rate."""
    uniq=np.array(sorted(set(units))); idx={u:np.where(units==u)[0] for u in uniq}
    rng=np.random.default_rng(SEED); acc={t:[] for t in thr}; fails=0
    for b in range(B):
        samp=rng.choice(uniq,size=len(uniq),replace=True); bi=np.concatenate([idx[u] for u in samp]); yb=y[bi]
        if len(np.unique(yb))<2: fails+=1; continue
        for t in thr: acc[t].append(nb(yb,pa[bi],t)-nb(yb,pb[bi],t))
    out={t:(float(np.percentile(acc[t],2.5)),float(np.percentile(acc[t],50)),float(np.percentile(acc[t],97.5))) for t in thr}
    return out,fails

metrics=[]; cis=[]; curves=[]
# ---- h4 primary ----
h4=pd.read_csv(H4); y=h4.y.values.astype(int); U=h4.GID_2.values
prev=y.mean()
for t in GRID:
    row=dict(dataset='h4_primary',horizon=4,threshold=t,
        NB_M1=nb(y,h4.M1_recal.values,t),NB_M4=nb(y,h4.M4_recal.values,t),NB_M5=nb(y,h4.M5_recal.values,t),
        NB_treat_all=prev-(1-prev)*(t/(1-t)),NB_treat_none=0.0,
        dNB_M4_M1=nb(y,h4.M4_recal.values,t)-nb(y,h4.M1_recal.values,t),
        dNB_M5_M1=nb(y,h4.M5_recal.values,t)-nb(y,h4.M1_recal.values,t)); metrics.append(row)
for t in CURVE:
    curves.append(dict(dataset='h4_primary',horizon=4,threshold=t,
        NB_M1=nb(y,h4.M1_recal.values,t),NB_M4=nb(y,h4.M4_recal.values,t),NB_M5=nb(y,h4.M5_recal.values,t),
        NB_treat_all=prev-(1-prev)*(t/(1-t)),NB_treat_none=0.0))
b5,f5=boot_dnb(y,h4.M5_recal.values,h4.M1_recal.values,U,GRID)
b4,f4=boot_dnb(y,h4.M4_recal.values,h4.M1_recal.values,U,GRID)
for t in GRID:
    cis.append(dict(dataset='h4_primary',horizon=4,threshold=t,contrast='M5_vs_M1',
        dNB_point=nb(y,h4.M5_recal.values,t)-nb(y,h4.M1_recal.values,t),dNB_lo=b5[t][0],dNB_med=b5[t][1],dNB_hi=b5[t][2],B=B,failures=f5,fail_rate=f5/B))
    cis.append(dict(dataset='h4_primary',horizon=4,threshold=t,contrast='M4_vs_M1',
        dNB_point=nb(y,h4.M4_recal.values,t)-nb(y,h4.M1_recal.values,t),dNB_lo=b4[t][0],dNB_med=b4[t][1],dNB_hi=b4[t][2],B=B,failures=f4,fail_rate=f4/B))

# ---- horizon sweep ----
hz=pd.read_csv(HZ)
for h in sorted(hz.horizon.unique()):
    g=hz[hz.horizon==h]; yh=g.y.values.astype(int); Uh=g.GID_2.values; pv=yh.mean()
    for t in GRID:
        metrics.append(dict(dataset='horizon',horizon=int(h),threshold=t,
            NB_M1=nb(yh,g.M1_recal.values,t),NB_M4=nb(yh,g.M4_recal.values,t),NB_M5=nb(yh,g.M5_recal.values,t),
            NB_treat_all=pv-(1-pv)*(t/(1-t)),NB_treat_none=0.0,
            dNB_M4_M1=nb(yh,g.M4_recal.values,t)-nb(yh,g.M1_recal.values,t),
            dNB_M5_M1=nb(yh,g.M5_recal.values,t)-nb(yh,g.M1_recal.values,t)))
    b5h,f5h=boot_dnb(yh,g.M5_recal.values,g.M1_recal.values,Uh,GRID)
    b4h,f4h=boot_dnb(yh,g.M4_recal.values,g.M1_recal.values,Uh,GRID)
    for t in GRID:
        cis.append(dict(dataset='horizon',horizon=int(h),threshold=t,contrast='M5_vs_M1',
            dNB_point=nb(yh,g.M5_recal.values,t)-nb(yh,g.M1_recal.values,t),dNB_lo=b5h[t][0],dNB_med=b5h[t][1],dNB_hi=b5h[t][2],B=B,failures=f5h,fail_rate=f5h/B))
        cis.append(dict(dataset='horizon',horizon=int(h),threshold=t,contrast='M4_vs_M1',
            dNB_point=nb(yh,g.M4_recal.values,t)-nb(yh,g.M1_recal.values,t),dNB_lo=b4h[t][0],dNB_med=b4h[t][1],dNB_hi=b4h[t][2],B=B,failures=f4h,fail_rate=f4h/B))

M=pd.DataFrame(metrics); C=pd.DataFrame(cis); CV=pd.DataFrame(curves)
M.to_csv(f'{OUT}/decision_threshold_dnb_metrics_v1.csv',index=False)
C.to_csv(f'{OUT}/decision_threshold_dnb_ci_v1.csv',index=False)
CV.to_csv(f'{OUT}/decision_threshold_dnb_curves_v1.csv',index=False)
def sh(p): return hashlib.sha256(open(p,'rb').read()).hexdigest()
# reproducibility anchor
h4c=C[(C.dataset=='h4_primary')&(C.threshold==0.30)]
repro=dict(M1_NB30=round(float(nb(y,h4.M1_recal.values,0.30)),4),M4_NB30=round(float(nb(y,h4.M4_recal.values,0.30)),4),
    M5_NB30=round(float(nb(y,h4.M5_recal.values,0.30)),4),
    dNB_M5_M1_30=round(float(h4c[h4c.contrast=='M5_vs_M1'].dNB_point.iloc[0]),4),
    dNB_M5_M1_30_CI=[round(float(h4c[h4c.contrast=='M5_vs_M1'].dNB_lo.iloc[0]),3),round(float(h4c[h4c.contrast=='M5_vs_M1'].dNB_hi.iloc[0]),3)],
    dNB_M4_M1_30=round(float(h4c[h4c.contrast=='M4_vs_M1'].dNB_point.iloc[0]),4))
outs=['decision_threshold_dnb_metrics_v1.csv','decision_threshold_dnb_ci_v1.csv','decision_threshold_dnb_curves_v1.csv']
meta=dict(spec='docs/decision_threshold_dnb_robustness_spec.md (643f039)',
    inputs={'h4_predictions':sh(H4),'horizon_predictions':sh(HZ)},grid=GRID,curve_grid=CURVE,B=B,seed=SEED,
    sri_lanka='DEFERRED (hybrid predictions in different-schema/recal file; separate SL-consistent E1 needed)',
    models_refit=False,predictions_regenerated=False,labels_thresholds_recomputed=False,
    h4_p30_reproducibility=repro,output_sha256={o:sh(f'{OUT}/{o}') for o in outs})
json.dump(meta,open(f'{OUT}/decision_threshold_dnb_robustness_v1.meta.json','w'),indent=2)
# console summary
print('h4 p*=0.30 reproducibility:',repro)
print('\nh4 ΔNB(M5-M1) across thresholds [point | 95% CI] (CI-excl-0?):')
for t in GRID:
    r=h4c if False else C[(C.dataset=='h4_primary')&(C.threshold==t)&(C.contrast=='M5_vs_M1')].iloc[0]
    excl='YES' if (r.dNB_lo>0 or r.dNB_hi<0) else 'no'
    print(f"  p*={t:.2f}: {r.dNB_point:+.4f} [{r.dNB_lo:+.4f},{r.dNB_hi:+.4f}] excl0={excl}")
print('\nhorizon M5-M1 ΔNB: # thresholds (of 9) with CI excluding 0, by horizon:')
for h in sorted(hz.horizon.unique()):
    sub=C[(C.dataset=='horizon')&(C.horizon==h)&(C.contrast=='M5_vs_M1')]
    nexcl=int(((sub.dNB_lo>0)|(sub.dNB_hi<0)).sum()); print(f"  h={h}: {nexcl}/9 thresholds CI-excl-0")
print('\nbootstrap fail rates: h4',f5,f4,'| max horizon fail', max([int(C[(C.dataset=='horizon')].failures.max())]))
