import geopandas as gpd, itertools, json
g=gpd.read_file("cod/lka_admin2.shp").to_crs(32644)   # metric CRS (report used EPSG:32644)
g["pcode"]=g["adm2_pcode"].str.strip()
print("districts:", len(g), "| pcodes:", sorted(g.pcode.tolist()))
name={r.pcode:r.adm2_name for r in g.itertuples()}
# 25-district adjacency: shared boundary length > 100 m (report: rook, 0 edges <100m)
geom=dict(zip(g.pcode,g.geometry))
adj={p:set() for p in geom}
for a,b in itertools.combinations(geom,2):
    inter=geom[a].boundary.intersection(geom[b].boundary)
    if inter.length>100:  # metres
        adj[a].add(b); adj[b].add(a)
E25=sum(len(v) for v in adj.values())//2
print(f"25-district graph: {E25} edges")
print(f"Ampara (LK52) neighbours in 25-district graph: {sorted((p,name[p]) for p in adj['LK52'])}")

# --- split LK52 (Ampara) into LK52A + LK52K using the committed build-report neighbour lists ---
# report: Ampara(LK52A): Batticaloa LK51, Polonnaruwa LK72, Badulla LK81, Moneragala LK82, Matale LK22, Hambantota LK33, + Kalmunai
#         Kalmunai(LK52K): Batticaloa LK51, + Ampara
A_nb={"LK51","LK72","LK81","LK82","LK22","LK33"}; K_nb={"LK51"}
for p in list(adj): adj[p].discard("LK52")
del adj["LK52"]
adj["LK52A"]=set(A_nb)|{"LK52K"}; adj["LK52K"]=set(K_nb)|{"LK52A"}
for p in A_nb: adj[p].add("LK52A")
for p in K_nb: adj[p].add("LK52K")
name["LK52A"]="Ampara"; name["LK52K"]="Kalmunai"

nodes=sorted(adj); E26=sum(len(v) for v in adj.values())//2
degs=sorted(len(v) for v in adj.values())
print(f"\n=== VERIFY reconstructed 26-node graph vs committed build report ===")
print(f"  nodes: {len(nodes)}  (report: 26)  {'OK' if len(nodes)==26 else 'FAIL'}")
print(f"  edges: {E26}  (report: 60)  {'OK' if E26==60 else 'FAIL'}")
print(f"  degree min/med/max: {degs[0]}/{degs[len(degs)//2]}/{degs[-1]}  (report: 2/4/9)")
print(f"  Kalmunai (LK52K) degree: {len(adj['LK52K'])}  (report: 2)  {'OK' if len(adj['LK52K'])==2 else 'FAIL'}")
def has(a,b): return b in adj[a]
print(f"  edge Ampara-Matale: {has('LK52A','LK22')} (report: genuine)")
print(f"  edge Ampara-Hambantota: {has('LK52A','LK33')} (report: genuine)")
print(f"  edge Jaffna(LK41)-Mullaitivu(LK44): {has('LK41','LK44')} (report: shortest, real)")
import networkx as nx
G=nx.Graph()
for p in adj:
    for q in adj[p]: G.add_edge(p,q)
print(f"  connected components: {nx.number_connected_components(G)} (report: 1)")
json.dump({p:sorted(adj[p]) for p in adj}, open("adj26.json","w"), indent=0)
print("wrote adj26.json")
