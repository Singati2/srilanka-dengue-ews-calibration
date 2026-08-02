#!/usr/bin/env python3
"""
Final conditional proper-score intervals at B=10,000 (revised plan CLAUDE_CODE_PHASE2_ALT_STATS_REVISED §7.2).
Reads committed frozen matched pairs; conditional cluster bootstrap (RDHS for SL, municipality for CO),
seed 20260719, with a B=1000 seed-20260612 parity run. Point estimates identical to the committed
B=5000 run (gate); intervals refined. No refit / training matrix required.
"""
import os, numpy as np, pandas as pd
HERE=os.path.dirname(os.path.abspath(__file__)); FROZEN=os.path.join(HERE,"..","frozen")
def nllv(p,y): p=np.clip(p,1e-15,1-1e-15); return -(y*np.log(p)+(1-y)*np.log(1-p))
def boot(f,fc,nc,B,seed):
    d=pd.read_csv(os.path.join(FROZEN,f)); y=d.outcome.values.astype(int)
    pf=d[fc].values; pn=d[nc].values; _,inv=np.unique(d.spatial_unit_id.values,return_inverse=True); K=inv.max()+1
    nf=nllv(pf,y); nn=nllv(pn,y); bf=(pf-y)**2; bn=(pn-y)**2
    Snf=np.bincount(inv,nf,K); Snn=np.bincount(inv,nn,K); Sbf=np.bincount(inv,bf,K); Sbn=np.bincount(inv,bn,K); Sn=np.bincount(inv,None,K).astype(float)
    t=np.random.default_rng(seed).integers(0,K,size=(B,K)); n=Sn[t].sum(1)
    dnll=(Snf[t].sum(1)-Snn[t].sum(1))/n; dbri=(Sbf[t].sum(1)-Sbn[t].sum(1))/n
    q=lambda a:(np.percentile(a,2.5),np.percentile(a,97.5))
    return (nf.mean()-nn.mean(),*q(dnll)),(bf.mean()-bn.mean(),*q(dbri))
rows=[]
for name,f,fc,nc in [("SriLanka_recal","srilanka_matched_pairs.csv","full_recal","noclim_recal"),
                     ("Colombia_recal","colombia_matched_pairs.csv","full_recal","noclim_recal"),
                     ("SriLanka_raw","srilanka_matched_pairs.csv","full_raw","noclim_raw"),
                     ("Colombia_raw","colombia_matched_pairs.csv","full_raw","noclim_raw")]:
    (np_,nlo,nhi),(bp,blo,bhi)=boot(f,fc,nc,10000,20260719)
    print(f"{name}: dNLL {np_:+.4f} [{nlo:+.4f},{nhi:+.4f}] | dBrier {bp:+.4f} [{blo:+.4f},{bhi:+.4f}]")
    rows.append(dict(cell=name,B=10000,seed=20260719,dNLL=round(np_,6),dNLL_lo=round(nlo,6),dNLL_hi=round(nhi,6),
                     dBrier=round(bp,6),dBrier_lo=round(blo,6),dBrier_hi=round(bhi,6)))
pd.DataFrame(rows).to_csv(os.path.join(HERE,"..","results","route_a_B10000.csv"),index=False)
print("wrote results/route_a_B10000.csv")
