#!/usr/bin/env python3
"""
Spatial-block bootstrap sensitivity for the Colombia matched increment (reviewer M10 follow-up).

Tests whether the borderline residual spatial autocorrelation inflates the Colombia conditional
interval. Resamples CONTIGUOUS department blocks (greedy-modularity communities of the committed
department adjacency) instead of independent departments, preserving spatial correlation, and
compares to the standard department bootstrap. Conditional (frozen predictions) only; the
development-inclusive interval needs model refitting (training matrix not archived). Seed 20260612.
"""
import os, json, numpy as np, pandas as pd, networkx as nx
HERE=os.path.dirname(os.path.abspath(__file__)); FROZEN=os.path.join(HERE,"..","..","ALT_STATS","frozen")
d=pd.read_csv(os.path.join(FROZEN,"colombia_matched_pairs.csv")); d["dept"]=d.department_id.astype(int)
adj={int(k):[int(x) for x in v] for k,v in json.load(open(os.path.join(HERE,"colombia_dept_adjacency_reconstructed.json"))).items()}
depts=sorted(adj); dset=set(depts); rows_by={dp:d[d.dept==dp] for dp in depts}
def nb(p,y,t=0.30):
    a=p>=t; n=len(y); return (a&(y==1)).sum()/n-(a&(y==0)).sum()/n*(t/(1-t))
def dnb(sel):
    s=pd.concat([rows_by[dp] for dp in sel]); y=s.outcome.values
    return nb(s.full_recal.values,y)-nb(s.noclim_recal.values,y)
def ci(draws,B=2000,seed=20260612):
    rng=np.random.default_rng(seed); e=[]
    for _ in range(B):
        sel=[]; 
        for u in rng.choice(len(draws),size=len(draws),replace=True): sel+=draws[u]
        e.append(dnb(sel))
    e=np.array(e); return np.percentile(e,2.5),np.percentile(e,97.5)
print(f"point matched dNB (recal): {dnb(depts):+.4f}  (committed +0.0078)")
lo,hi=ci([[x] for x in depts]); print(f"standard dept bootstrap:  [{lo:+.4f}, {hi:+.4f}]  width {hi-lo:.4f}  (GATE vs committed +0.0038..+0.0115)")
G=nx.Graph(); G.add_nodes_from(depts)
for a in depts:
    for b in adj[a]:
        if b in dset: G.add_edge(a,b)
blk=[sorted(c) for c in nx.algorithms.community.greedy_modularity_communities(G)]
lo2,hi2=ci(blk)
print(f"spatial-block ({len(blk)} blocks, sizes {sorted(len(b) for b in blk)}): [{lo2:+.4f}, {hi2:+.4f}]  width {hi2-lo2:.4f}")
print(f"widening {(hi2-lo2)/(hi-lo):.2f}x; lower bound {lo:+.4f}->{lo2:+.4f} (>0: {lo2>0})")
