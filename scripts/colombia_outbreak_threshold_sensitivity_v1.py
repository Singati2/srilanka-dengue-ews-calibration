#!/usr/bin/env python3
"""E3 outbreak-threshold sensitivity (per docs/colombia_outbreak_threshold_sensitivity_spec.md).
Same M0-M5 ladder/features/preprocessing/recalibration as the committed h=4 run; only the outbreak
percentile (75/80/90, train-only per-GID_2) changes. Common-complete rows identical across percentiles
(h=4 labelability depends only on t+4 existence). 75th = registered primary anchor. GID_2 cluster
bootstrap seed 20260612 B=1000. NO label/threshold file modified; outputs to a new versioned dir only."""
import pandas as pd, numpy as np, json, hashlib, os, warnings
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, average_precision_score, brier_score_loss, log_loss
import statsmodels.api as sm
warnings.filterwarnings('ignore')
LF='/home/mpcrlab/data_quarantine/colombia_label_features_v1'
OUT='/home/mpcrlab/data_quarantine/colombia_model_pilots/outbreak_threshold_sensitivity_v1'; os.makedirs(OUT,exist_ok=True)
SRC=f'{LF}/colombia_modeling_table_all_horizons_v1.csv'; THRC=f'{LF}/colombia_label_thresholds_train_only_v1.csv'
PSTAR=0.30; CGRID=[0.001,0.003,0.01,0.03,0.1,0.3,1,3,10]; SEED=20260612; B=1000; DGRID=[round(x,2) for x in np.arange(0.10,0.51,0.05)]
d=pd.read_csv(SRC,dtype={'week_start':str}); d['dept']=d.GID_2.str.split('.').str[1]; d['wk']=pd.to_datetime(d.week_start)
# train-only thresholds (verify thr75/thr90 vs committed)
tr_all=d[d.split=='train']
rec=tr_all.groupby('GID_2').dengue_total.agg(thr75=lambda s:np.percentile(s,75),thr80=lambda s:np.percentile(s,80),thr90=lambda s:np.percentile(s,90),train_weeks='size').reset_index()
cm=pd.read_csv(THRC)[['GID_2','thr75','thr90']]; v=rec.merge(cm,on='GID_2',suffixes=('_rec','_cm'))
thr75_ok=float((v.thr75_rec-v.thr75_cm).abs().max()); thr90_ok=float((v.thr90_rec-v.thr90_cm).abs().max())
rec.to_csv(f'{OUT}/colombia_outbreak_thresholds_v1.csv',index=False)
# common-complete rows + t+4 outcome + labels
out={(g,w):c for g,w,c in zip(d.GID_2,d.week_start,d.dengue_total)}
cc=d[d.common_complete_M1_to_M5_h4==True].copy(); cc['t4']=(cc.wk+pd.Timedelta(weeks=4)).dt.date.astype(str)
cc['out_t4']=[out.get((g,w),np.nan) for g,w in zip(cc.GID_2,cc.t4)]
Tt=rec.set_index('GID_2')
for pct,col in [(75,'thr75'),(80,'thr80'),(90,'thr90')]:
    lab=(cc.out_t4>cc.GID_2.map(Tt[col].to_dict())).astype(float); lab[cc.out_t4.isna()]=np.nan; cc[f'label_{pct}']=lab
lab75_match=int((cc.label_75==cc.label_h4).sum())==len(cc)
cc[['GID_2','week_start','split','label_75','label_80','label_90']].to_csv(f'{OUT}/colombia_outbreak_threshold_labels_v1.csv',index=False)
PRE=[f'precip_lag{k}' for k in range(9)]; TMP=[f'temp_lag{k}' for k in range(9)]; CAS=['cases_lag0','cases_lag1','cases_lag2','cases_lag4']; SEA=['sin_woy_1','cos_woy_1','sin_woy_2','cos_woy_2']
MODELS={'M0':['season'],'M1':['cases'],'M2':['climate'],'M3':['climate','season','dept'],'M4':['cases','climate'],'M5':['cases','climate','season','dept']}
def design(df,feats,scaler=None,dc=None):
    X=pd.DataFrame(index=df.index); cont=[]
    if 'cases' in feats:
        for c in CAS: X[c]=np.log1p(df[c]); cont.append(c)
    if 'climate' in feats:
        for c in PRE: X[c]=np.log1p(df[c]); cont.append(c)
        for c in TMP: X[c]=df[c]; cont.append(c)
    if 'season' in feats:
        for c in SEA: X[c]=df[c]
    if scaler is None: scaler={c:(X[c].mean(),X[c].std(ddof=0) or 1.0) for c in cont}
    for c in cont: m,s=scaler[c]; X[c]=(X[c]-m)/(s if s else 1.0)
    if 'dept' in feats:
        if dc is None: dc=sorted(df['dept'].unique())
        for x in dc: X[f'dept_{x}']=(df['dept']==x).astype(float)
    return X,scaler,dc
def logit(p): p=np.clip(p,1e-6,1-1e-6); return np.log(p/(1-p))
def nb(y,p,t):
    pos=p>=t; n=len(y); return np.sum(pos&(y==1))/n-(np.sum(pos&(y==0))/n)*(t/(1-t))
def citl_slope(y,p):
    lp=logit(p)
    try: c=float(sm.Logit(y,np.ones_like(lp),offset=lp).fit(disp=0).params[0])
    except Exception: c=np.nan
    try: s=float(sm.Logit(y,sm.add_constant(lp)).fit(disp=0).params[1])
    except Exception: s=np.nan
    return c,s
metrics=[]; dca=[]; preds=[]; boot=[]; anchor={}
for pct in [75,80,90]:
    lab=f'label_{pct}'; g=cc.dropna(subset=[lab]).copy()
    trn,va,te=g[g.split=='train'],g[g.split=='val'],g[g.split=='test']
    yte=te[lab].values.astype(int); res={}
    for name,feats in MODELS.items():
        Xtr,sc,dc=design(trn,feats); ytr=trn[lab].values.astype(int); yva=va[lab].values.astype(int)
        best=None
        for C in CGRID:
            m=LogisticRegression(C=C,penalty='l2',solver='lbfgs',max_iter=5000).fit(Xtr,ytr)
            p=np.clip(m.predict_proba(design(va,feats,sc,dc)[0])[:,1],1e-6,1-1e-6); ll=log_loss(yva,p,labels=[0,1])
            if best is None or ll<best[0]: best=(ll,C,m)
        vll,C,m=best
        pv=np.clip(m.predict_proba(design(va,feats,sc,dc)[0])[:,1],1e-6,1-1e-6)
        pr=np.clip(m.predict_proba(design(te,feats,sc,dc)[0])[:,1],1e-6,1-1e-6)
        pl=LogisticRegression(C=1e6,max_iter=1000).fit(logit(pv).reshape(-1,1),yva); prec=pl.predict_proba(logit(pr).reshape(-1,1))[:,1]
        res[name]=dict(praw=pr,prec=prec,C=C)
        for tag,p in [('raw',pr),('recal',prec)]:
            ci,sl=citl_slope(yte,p)
            metrics.append(dict(percentile=pct,model=name,calib=tag,C=C,n_test=len(te),events_test=int(yte.sum()),prev_test=round(float(yte.mean()),4),
                AUC=roc_auc_score(yte,p),PR_AUC=average_precision_score(yte,p),Brier=brier_score_loss(yte,p),CITL=ci,slope=sl,NB_p30=nb(yte,p,PSTAR)))
        for t in DGRID: dca.append(dict(percentile=pct,model=name,threshold=t,NB_recal=nb(yte,prec,t)))
    prev=yte.mean()
    for t in DGRID:
        dca.append(dict(percentile=pct,model='treat_all',threshold=t,NB_recal=prev-(1-prev)*(t/(1-t))))
        dca.append(dict(percentile=pct,model='treat_none',threshold=t,NB_recal=0.0))
    pp={'percentile':pct,'GID_2':te.GID_2.values,'week_start':te.week_start.values,'y':yte}
    for n in MODELS: pp[f'{n}_recal']=res[n]['prec']
    preds.append(pd.DataFrame(pp))
    # bootstrap @p*=0.30: ΔNB(M5-M1), ΔNB(M4-M1), ΔAUC(M5-M1)
    units=te.GID_2.values; uniq=np.array(sorted(set(units))); idx={u:np.where(units==u)[0] for u in uniq}
    rng=np.random.default_rng(SEED); d5n=[]; d4n=[]; d5a=[]; fails=0
    for b in range(B):
        bi=np.concatenate([idx[u] for u in rng.choice(uniq,len(uniq),replace=True)]); yb=yte[bi]
        if len(np.unique(yb))<2: fails+=1; continue
        d5n.append(nb(yb,res['M5']['prec'][bi],PSTAR)-nb(yb,res['M1']['prec'][bi],PSTAR))
        d4n.append(nb(yb,res['M4']['prec'][bi],PSTAR)-nb(yb,res['M1']['prec'][bi],PSTAR))
        d5a.append(roc_auc_score(yb,res['M5']['praw'][bi])-roc_auc_score(yb,res['M1']['praw'][bi]))
    pc=lambda a,q: float(np.percentile(a,q))
    point_d5n=nb(yte,res['M5']['prec'],PSTAR)-nb(yte,res['M1']['prec'],PSTAR)
    boot.append(dict(percentile=pct,contrast='M5_vs_M1_dNB_p30',point=point_d5n,lo=pc(d5n,2.5),med=pc(d5n,50),hi=pc(d5n,97.5),B=B,failures=fails,fail_rate=fails/B))
    boot.append(dict(percentile=pct,contrast='M4_vs_M1_dNB_p30',point=nb(yte,res['M4']['prec'],PSTAR)-nb(yte,res['M1']['prec'],PSTAR),lo=pc(d4n,2.5),med=pc(d4n,50),hi=pc(d4n,97.5),B=B,failures=fails,fail_rate=fails/B))
    boot.append(dict(percentile=pct,contrast='M5_vs_M1_dAUC',point=roc_auc_score(yte,res['M5']['praw'])-roc_auc_score(yte,res['M1']['praw']),lo=pc(d5a,2.5),med=pc(d5a,50),hi=pc(d5a,97.5),B=B,failures=fails,fail_rate=fails/B))
    if pct==75: anchor=dict(M5_M1_dNB30_point=round(point_d5n,4),CI=[round(pc(d5n,2.5),4),round(pc(d5n,97.5),4)])
pd.DataFrame(metrics).to_csv(f'{OUT}/colombia_outbreak_threshold_metrics_v1.csv',index=False)
pd.DataFrame(dca).to_csv(f'{OUT}/colombia_outbreak_threshold_dca_v1.csv',index=False)
pd.concat(preds,ignore_index=True).to_csv(f'{OUT}/colombia_outbreak_threshold_predictions_v1.csv',index=False)
bdf=pd.DataFrame(boot); bdf.to_csv(f'{OUT}/colombia_outbreak_threshold_bootstrap_ci_v1.csv',index=False)
def sh(p): return hashlib.sha256(open(p,'rb').read()).hexdigest()
outs=['colombia_outbreak_thresholds_v1.csv','colombia_outbreak_threshold_labels_v1.csv','colombia_outbreak_threshold_predictions_v1.csv','colombia_outbreak_threshold_metrics_v1.csv','colombia_outbreak_threshold_dca_v1.csv','colombia_outbreak_threshold_bootstrap_ci_v1.csv']
meta=dict(spec='docs/colombia_outbreak_threshold_sensitivity_spec.md',horizon=4,common_complete_n=len(cc),
    thr75_reproduces_committed_maxabs=thr75_ok,thr90_reproduces_committed_maxabs=thr90_ok,thr80='computed train-only (new)',
    label75_reproduces_committed_label_h4=bool(lab75_match),
    test_prevalence={p:round(float(cc[cc.split=='test'][f'label_{p}'].mean()),4) for p in [75,80,90]},
    sparsity_decision='all percentiles adequate (test events 5015/4416/3136; no downgrade)',
    h4_75th_primary_anchor=anchor,pstar=PSTAR,seed=SEED,B=B,
    labels_thresholds_files_modified=False,models_refit='yes (new percentile labels; not the committed h4 run)',
    output_sha256={o:sh(f'{OUT}/{o}') for o in outs})
json.dump(meta,open(f'{OUT}/colombia_outbreak_threshold_sensitivity_v1.meta.json','w'),indent=2)
m=pd.DataFrame(metrics); mr=m[m.calib=='recal']
print('thr75 maxΔ',thr75_ok,'thr90 maxΔ',thr90_ok,'| label75==committed:',lab75_match)
print('75th anchor M5-M1 ΔNB@0.30:',anchor)
print('\nTEST (recal) by percentile — M1 vs M5 (AUC, PR-AUC, NB@0.30):')
for pct in [75,80,90]:
    for nm in ['M1','M5']:
        r=mr[(mr.percentile==pct)&(mr.model==nm)].iloc[0]
        print(f"  p{pct} {nm}: AUC {r.AUC:.3f} PRAUC {r.PR_AUC:.3f} NB@0.30 {r.NB_p30:.4f} (prev {r.prev_test})")
print('\nΔNB(M5-M1)@0.30 & ΔNB(M4-M1)@0.30 & ΔAUC by percentile [point | 95% CI]:')
for pct in [75,80,90]:
    for c in ['M5_vs_M1_dNB_p30','M4_vs_M1_dNB_p30','M5_vs_M1_dAUC']:
        r=bdf[(bdf.percentile==pct)&(bdf.contrast==c)].iloc[0]; excl='excl0' if (r.lo>0 or r.hi<0) else 'incl0'
        print(f"  p{pct} {c}: {r.point:+.4f} [{r.lo:+.4f},{r.hi:+.4f}] {excl} (fail {r.fail_rate})")
