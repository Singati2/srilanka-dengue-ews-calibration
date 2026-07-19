#!/usr/bin/env python3
"""ALT_STATS Route A scoring — post-lock. Verifies frozen checksums, then computes
NLL, Brier, calibration (CITL/intercept/slope/ICI), discrimination (AUC/PR-AUC), and
paired conditional cluster-bootstrap intervals (B=5000 primary, B=1000 parity) for both
settings × {raw, recal}. Development-inclusive intervals NOT computed (Phase 1 gate).
Deterministic seed 20260612. Full precision. Loud failure. No source modification.
"""
import pandas as pd, numpy as np, json, hashlib, os, sys
from sklearn.metrics import roc_auc_score, average_precision_score
import statsmodels.api as sm
from patsy import dmatrix
import warnings; warnings.filterwarnings('ignore')
ROOT="/home/mpcrlab/srilanka-dengue-ews-calibration/ALT_STATS"
FR=f"{ROOT}/frozen"; RES=f"{ROOT}/results"; os.makedirs(f"{RES}/bootstrap_replicates",exist_ok=True)
SEED=20260612; EPS=1e-15; EPS_SENS=1e-12
def sha256(p):
    h=hashlib.sha256()
    with open(p,'rb') as fh:
        for b in iter(lambda: fh.read(1<<20), b''): h.update(b)
    return h.hexdigest()
# ---- lock verification ----
locked={}
for line in open(f"{ROOT}/FROZEN_INPUTS.sha256"):
    cs,name=line.split(); locked[name.strip()]=cs
for name in locked:
    got=sha256(f"{FR}/{name}")
    assert got==locked[name], f"CHECKSUM MISMATCH {name}: {got} != {locked[name]}"
print(f"LOCK VERIFY: {len(locked)} frozen checksums OK",flush=True)

def clipp(p,eps=EPS): return np.minimum(1-eps,np.maximum(eps,p))
def nll(y,p,eps=EPS):
    p=clipp(p,eps); return float(np.mean(-(y*np.log(p)+(1-y)*np.log(1-p))))
def brier(y,p): return float(np.mean((p-y)**2))
def logit(p): p=clipp(p,1e-15); return np.log(p/(1-p))
def calib(y,p):
    lp=logit(p)
    citl=float(sm.GLM(y,np.ones((len(y),1)),family=sm.families.Binomial(),offset=lp).fit().params[0])
    r=sm.GLM(y,sm.add_constant(lp),family=sm.families.Binomial()).fit()
    a,b=float(r.params[0]),float(r.params[1])
    # ICI via restricted cubic spline of logit(p) at quantile knots
    kn=np.quantile(lp,[0.05,0.35,0.65,0.95])
    try:
        X=dmatrix("cr(lp, knots=kn[1:-1], lower_bound=kn[0], upper_bound=kn[-1])",{"lp":lp,"kn":kn},return_type='dataframe')
        fit=sm.GLM(y,X,family=sm.families.Binomial()).fit()
        phat=np.asarray(fit.predict(X)); ici=float(np.mean(np.abs(p-phat)))
    except Exception:
        ici=float('nan')
    return citl,a,b,ici

def score_all(y,p,eps=EPS):
    citl,a,b,ici=calib(y,p)
    return dict(nll=nll(y,p,eps),brier=brier(y,p),auc=float(roc_auc_score(y,p)),
                prauc=float(average_precision_score(y,p)),citl=citl,cal_int=a,cal_slope=b,ici=ici,
                meanp=float(np.mean(p)),prev=float(np.mean(y)))

def boot(y,pf,pn,units,B,seed):
    rng=np.random.default_rng(seed); uids=np.array(sorted(set(units)))
    idxby={u:np.where(units==u)[0] for u in uids}
    dnll=[];dbs=[];dauc=[];dpr=[];fail=0;single=0
    for _ in range(B):
        pick=uids[rng.integers(0,len(uids),len(uids))]
        idx=np.concatenate([idxby[u] for u in pick]); yy=y[idx]
        if yy.min()==yy.max(): single+=1; fail+=1; continue
        pfi=pf[idx]; pni=pn[idx]
        dnll.append(nll(yy,pfi)-nll(yy,pni)); dbs.append(brier(yy,pfi)-brier(yy,pni))
        try: dauc.append(roc_auc_score(yy,pf[idx])-roc_auc_score(yy,pn[idx])); dpr.append(average_precision_score(yy,pf[idx])-average_precision_score(yy,pn[idx]))
        except Exception: pass
    def ci(v): return [float(np.percentile(v,2.5)),float(np.percentile(v,97.5))] if len(v) else [float('nan')]*2
    def sf(v): return float(np.mean(np.array(v)<0)) if len(v) else float('nan')
    return dict(B=B,valid=len(dnll),failed=fail,single_class=single,
                dNLL_ci=ci(dnll),dBS_ci=ci(dbs),dAUC_ci=ci(dauc),dPRAUC_ci=ci(dpr),
                signfreq_dNLL=sf(dnll),signfreq_dBS=sf(dbs)), np.array(dnll),np.array(dbs)

rows=[];calibrows=[];runman={"seed":SEED,"eps_primary":EPS,"eps_sensitivity":EPS_SENS}
for f,setting,primunit,secunit in [("srilanka_matched_pairs.csv","SriLanka","spatial_unit_id",None),
                                    ("colombia_matched_pairs.csv","Colombia","spatial_unit_id","department_id")]:
    df=pd.read_csv(f"{FR}/{f}"); y=df.outcome.values.astype(float)
    for state in ["recal","raw"]:  # recal = primary, raw = secondary
        pf=df[f"full_{state}"].values; pn=df[f"noclim_{state}"].values
        Sf=score_all(y,pf); Sn=score_all(y,pn)
        dNLL=Sf['nll']-Sn['nll']; dBS=Sf['brier']-Sn['brier']
        # clipping sensitivity
        dNLL_sens=nll(y,pf,EPS_SENS)-nll(y,pn,EPS_SENS)
        material=abs(dNLL_sens-dNLL) > max(1e-4, 0.05*abs(dNLL))
        units=df[primunit].values.astype(str)
        b5,r5n,r5b=boot(y,pf,pn,units,5000,SEED)
        b1,_,_=boot(y,pf,pn,units,1000,SEED)  # parity
        np.savez(f"{RES}/bootstrap_replicates/{setting}_{state}_B5000.npz",dNLL=r5n,dBS=r5b)
        base=dict(setting=setting,prediction_state=state,sample_size=len(y),event_count=int(y.sum()),
                  cluster_count=int(pd.Series(units).nunique()),bootstrap_replicates=5000,
                  bootstrap_failure_count=b5['failed'],development_inclusive_status="NOT_COMPUTED (Phase1 gate)",
                  analysis_commit="",input_checksum_set=locked[f])
        for metric,fe,ne,pd_,orient,ci5,sf5 in [
            ("NLL",Sf['nll'],Sn['nll'],dNLL,"lower_favors_climate",b5['dNLL_ci'],b5['signfreq_dNLL']),
            ("Brier",Sf['brier'],Sn['brier'],dBS,"lower_favors_climate",b5['dBS_ci'],b5['signfreq_dBS']),
            ("AUC",Sf['auc'],Sn['auc'],Sf['auc']-Sn['auc'],"higher_favors_climate",b5['dAUC_ci'],float('nan')),
            ("PR_AUC",Sf['prauc'],Sn['prauc'],Sf['prauc']-Sn['prauc'],"higher_favors_climate",b5['dPRAUC_ci'],float('nan'))]:
            rows.append({**base,"metric":metric,"full_model_estimate":fe,"no_climate_estimate":ne,
                "paired_difference":pd_,"orientation":orient,"conditional_ci_lower":ci5[0],"conditional_ci_upper":ci5[1],
                "development_inclusive_ci_lower":"","development_inclusive_ci_upper":"",
                "bootstrap_fraction_favoring_climate":sf5,
                "IG_nats": (-pd_ if metric=="NLL" else ""),"IG_bits": (-pd_/np.log(2) if metric=="NLL" else ""),
                "BSS": (1-fe/ne if metric=="Brier" else ""),
                "clip_sensitivity_material": (bool(material) if metric=="NLL" else ""),
                "B1000_parity_ci": (b1['dNLL_ci'] if metric=="NLL" else b1['dBS_ci'] if metric=="Brier" else "")})
        for mdl,S in [("full",Sf),("no_climate",Sn)]:
            calibrows.append(dict(setting=setting,state=state,model=mdl,**{k:S[k] for k in ['citl','cal_int','cal_slope','ici','meanp','prev','auc','prauc','nll','brier']}))
        print(f"{setting} {state}: ΔNLL={dNLL:+.5f} (IG_bits={-dNLL/np.log(2):+.5f}) CI{b5['dNLL_ci']}  ΔBS={dBS:+.6f} CI{b5['dBS_ci']}  signfreq_NLL={b5['signfreq_dNLL']:.3f}  bootfail={b5['failed']}/5000",flush=True)

pd.DataFrame(rows).to_csv(f"{RES}/route_a_primary.csv",index=False)
pd.DataFrame(calibrows).to_csv(f"{RES}/calibration_metrics.csv",index=False)
runman["failure_rates"]={f"{r['setting']}_{r['prediction_state']}":r['bootstrap_failure_count']/5000 for r in rows if r['metric']=='NLL'}
json.dump(runman,open(f"{RES}/run_manifest.json","w"),indent=2,default=float)
print("\nROUTE A COMPLETE ->",RES)
