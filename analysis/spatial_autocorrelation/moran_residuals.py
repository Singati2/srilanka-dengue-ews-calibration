#!/usr/bin/env python3
"""
Residual spatial-autocorrelation diagnostic (reviewer M10).

Reads committed frozen matched predictions (ALT_STATS/frozen/*.csv) and the reconstructed,
verified adjacency graphs in this directory, then computes Moran's I on per-unit mean residuals
(outcome - prediction) with row-standardized weights and a 9999-permutation test. Seed 20260612.

Adjacency provenance (see build_adjacency.py): Sri Lanka = public HDX COD-AB ADM2 districts,
Ampara split into Ampara+Kalmunai, VERIFIED against the committed 26-node/60-edge build report
(degree 2/4/9, named edges). Colombia = public GADM v4.1 GID_1 departments (department_id parsed
from the GADM GIDs carried in the frozen data); no committed graph exists to cross-verify.
No refit and no training feature matrix required.
"""
import os, json, numpy as np, pandas as pd
HERE=os.path.dirname(os.path.abspath(__file__)); FROZEN=os.path.join(HERE,"..","..","ALT_STATS","frozen")
def moran(x,Wm,S0,n):
    z=x-x.mean(); return (n/S0)*((z@Wm@z)/((z*z).sum()))
def perm_p(x,I,Wm,S0,n,K=9999,seed=20260612):
    rng=np.random.default_rng(seed); c=sum(abs(moran(rng.permutation(x),Wm,S0,n))>=abs(I) for _ in range(K)); return (c+1)/(K+1)
def run(adjfile, pairs, unit_from):
    adj={k:set(v) for k,v in json.load(open(os.path.join(HERE,adjfile))).items()}
    d=pd.read_csv(os.path.join(FROZEN,pairs)); d["u"]=unit_from(d)
    use=[u for u in sorted(adj) if any(q in adj and str(q) in map(str,d.u.unique()) for q in adj[u])]
    use=[u for u in sorted(adj) if len(set(map(str,adj[u]))&set(map(str,d.u.unique())))>0]
    idx={u:i for i,u in enumerate(use)}; n=len(use); Wm=np.zeros((n,n))
    for u in use:
        for q in adj[u]:
            if str(q) in idx or q in idx:
                k=q if q in idx else str(q)
                if k in idx: Wm[idx[u],idx[k]]=1.0
    Wm=Wm/Wm.sum(1,keepdims=True); S0=Wm.sum()
    for col,lab in [("full_recal","M5 full recal"),("noclim_recal","M5 no-climate recal")]:
        r=d.groupby("u").apply(lambda gg:(gg.outcome-gg[col]).mean()).reindex(use).values
        I=moran(r,Wm,S0,n); print(f"    {lab:22}: I={I:+.4f}  E[I]={-1/(n-1):+.4f}  p={perm_p(r,I,Wm,S0,n):.4f}  (n={n})")
print("Sri Lanka (26 RDHS, adjacency VERIFIED vs committed graph):")
run("rdhs26_adjacency_reconstructed.json","srilanka_matched_pairs.csv",lambda d:d.spatial_unit_id.str.strip())
print("Colombia (31 test departments, adjacency from GADM GID_1):")
run("colombia_dept_adjacency_reconstructed.json","colombia_matched_pairs.csv",lambda d:d.department_id.astype(str))
