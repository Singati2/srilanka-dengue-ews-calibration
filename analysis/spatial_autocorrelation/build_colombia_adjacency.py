import geopandas as gpd, itertools, numpy as np, pandas as pd, json
g=gpd.read_file("gadm41_COL_1.json").to_crs(3116)   # MAGNA-SIRGAS metric (paper's CRS)
# GID_1 like 'COL.10_1' -> department index 10 (matches analysis department_id, which came from these GIDs)
g["dept"]=g["GID_1"].str.extract(r"COL\.(\d+)_").astype(int)
print("GADM departments:", len(g), "| dept ids:", sorted(g.dept.tolist()))
geom=dict(zip(g.dept,g.geometry))
adj={d:set() for d in geom}
for a,b in itertools.combinations(geom,2):
    if geom[a].boundary.intersection(geom[b].boundary).length>100:  # metres
        adj[a].add(b); adj[b].add(a)
# residuals per department (mean outcome - prediction) over frozen test data
d=pd.read_csv("co_pairs.csv"); d["dept"]=d["department_id"].astype(int)
test_depts=sorted(d.dept.unique())
print(f"test departments in frozen data: {len(test_depts)}  -> {test_depts}")
# subgraph on test departments; report isolates
iso=[t for t in test_depts if len(adj.get(t,set())&set(test_depts))==0]
print(f"isolated (no neighbour among test depts): {iso}  ({[g.set_index('dept').loc[i,'NAME_1'] for i in iso]})")
use=[t for t in test_depts if t not in iso]
idx={t:i for i,t in enumerate(use)}; n=len(use)
Wm=np.zeros((n,n))
for t in use:
    for q in adj[t]:
        if q in idx: Wm[idx[t],idx[q]]=1.0
Wm=Wm/Wm.sum(1,keepdims=True); S0=Wm.sum()
def moran(x):
    z=x-x.mean(); return (n/S0)*((z@Wm@z)/((z*z).sum()))
def perm_p(x,I,K=9999,seed=20260612):
    rng=np.random.default_rng(seed); c=sum(abs(moran(rng.permutation(x)))>=abs(I) for _ in range(K)); return (c+1)/(K+1)
print(f"\nMoran's I over {n} connected test departments (dropped {len(iso)} isolate):")
for col,lab in [("full_recal","M5 (full, recal)"),("noclim_recal","M5 no-climate (recal)")]:
    r=d.groupby("dept").apply(lambda gg:(gg.outcome-gg[col]).mean()).reindex(use).values
    I=moran(r); EI=-1/(n-1); p=perm_p(r,I)
    print(f"  {lab:24}: Moran's I = {I:+.4f}  (E[I]={EI:+.4f})  perm p = {p:.4f}  {'significant' if p<0.05 else 'no significant residual autocorrelation'}")
json.dump({str(t):sorted(adj[t]) for t in use}, open("co_adj.json","w"))
