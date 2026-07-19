#!/usr/bin/env python3
"""ALT_STATS figures A (paired proper-score forest), B (calibration), C (metric summary)."""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd, numpy as np
R="/home/mpcrlab/srilanka-dengue-ews-calibration/ALT_STATS"
d=pd.read_csv(f"{R}/results/route_a_primary.csv")
NEUT="#333333"; CL="#0072B2"; NC="#D55E00"

# ---- Figure A: forest of ΔNLL and ΔBS (separate panels; conditional CIs) ----
fig,axes=plt.subplots(1,2,figsize=(9.5,3.8))
order=[("SriLanka","recal"),("SriLanka","raw"),("Colombia","recal"),("Colombia","raw")]
labels=[f"Sri Lanka\n{s}" for _,s in order[:2]]+[f"Colombia\n{s}" for _,s in order[2:]]
for ax,metric,title in [(axes[0],"NLL","(A1) ΔNLL (nats)"),(axes[1],"Brier","(A2) ΔBrier")]:
    yy=list(range(len(order)))[::-1]
    for y,(st,state) in zip(yy,order):
        r=d[(d.setting==st)&(d.prediction_state==state)&(d.metric==metric)].iloc[0]
        lo,hi,pt=r.conditional_ci_lower,r.conditional_ci_upper,r.paired_difference
        ax.plot([lo,hi],[y,y],color=NEUT,lw=2.2,solid_capstyle="round")
        for x in (lo,hi): ax.plot([x,x],[y-.09,y+.09],color=NEUT,lw=1.8)
        ax.plot([pt],[y],"o",ms=8,color=CL,markeredgecolor="black",markeredgewidth=.6)
        ax.text(pt,y-0.28,f"{pt:+.4f}",ha="center",fontsize=6.8,color="#555")
    ax.axvline(0,color="black",lw=1,ls=(0,(4,3)))
    ax.text(0,len(order)-0.4,"favors climate ←|→ favors no-climate",fontsize=6,ha="center",va="bottom",color="#777")
    ax.set_yticks(yy); ax.set_yticklabels(labels,fontsize=8); ax.set_ylim(-0.6,len(order)-0.2)
    ax.set_title(title,fontsize=9,loc="left"); ax.tick_params(labelsize=7)
    for s in ("top","right"): ax.spines[s].set_visible(False)
fig.suptitle("Figure A. Paired threshold-free proper-score differences (conditional 95% cluster-bootstrap, B=5000)\n"
             "Negative favors the full climate model. Development-inclusive intervals not computed (Phase 1 gate).",fontsize=8.5)
fig.tight_layout(rect=[0,0,1,0.90]); fig.savefig(f"{R}/figures/FigureA_proper_score_forest.pdf",bbox_inches="tight")
print("wrote Figure A")

# ---- Figure C: compact metric summary per model ----
c=pd.read_csv(f"{R}/results/calibration_metrics.csv")
fig,axes=plt.subplots(2,2,figsize=(10,6))
for ax,(st,state) in zip(axes.ravel(),order):
    sub=c[(c.setting==st)&(c.state==state)]
    mets=["nll","brier","ici"]; disc=["auc","prauc"]
    full=sub[sub.model=="full"].iloc[0]; noc=sub[sub.model=="no_climate"].iloc[0]
    x=np.arange(len(mets)+len(disc)); allm=mets+disc
    ax.bar(x-0.2,[full[m] for m in allm],0.38,label="full climate",color=CL)
    ax.bar(x+0.2,[noc[m] for m in allm],0.38,label="no-climate",color=NC)
    ax.set_xticks(x); ax.set_xticklabels(["NLL","Brier","ICI","AUC","PR-AUC"],fontsize=7)
    ax.set_title(f"{st} — {state}",fontsize=9); ax.tick_params(labelsize=7)
    for s in ("top","right"): ax.spines[s].set_visible(False)
    if st=="SriLanka" and state=="recal": ax.legend(fontsize=7,frameon=False)
fig.suptitle("Figure C. Per-model NLL, Brier, ICI (lower better) and AUC, PR-AUC (higher better).\n"
             "Metrics do not have equal scientific priority; NLL is primary.",fontsize=8.5)
fig.tight_layout(rect=[0,0,1,0.93]); fig.savefig(f"{R}/figures/FigureC_metric_summary.pdf",bbox_inches="tight")
print("wrote Figure C")

# ---- Figure B: calibration (decile-bin observed vs mean predicted, both models) ----
fig,axes=plt.subplots(2,2,figsize=(9,8))
for ax,(st,state) in zip(axes.ravel(),order):
    fn={"SriLanka":"srilanka_matched_pairs.csv","Colombia":"colombia_matched_pairs.csv"}[st]
    df=pd.read_csv(f"{R}/frozen/{fn}"); y=df.outcome.values
    for col,color,lab in [(f"full_{state}",CL,"full climate"),(f"noclim_{state}",NC,"no-climate")]:
        p=df[col].values; q=pd.qcut(p,10,duplicates="drop"); g=pd.DataFrame({"p":p,"y":y,"q":q}).groupby("q",observed=True)
        ax.plot(g.p.mean(),g.y.mean(),"o-",color=color,ms=4,lw=1.2,label=lab)
    ax.plot([0,1],[0,1],color="#999",lw=1,ls="--")
    ax.set_title(f"{st} — {state}",fontsize=9); ax.set_xlabel("mean predicted",fontsize=7); ax.set_ylabel("observed",fontsize=7)
    ax.tick_params(labelsize=7); ax.set_xlim(0,1); ax.set_ylim(0,1)
    if st=="SriLanka" and state=="recal": ax.legend(fontsize=7,frameon=False)
    for s in ("top","right"): ax.spines[s].set_visible(False)
fig.suptitle("Figure B. Decile-bin calibration (descriptive). Cluster-bootstrap bands omitted for legibility;\n"
             "ICI with cluster uncertainty is the summary calibration statistic.",fontsize=8.5)
fig.tight_layout(rect=[0,0,1,0.94]); fig.savefig(f"{R}/figures/FigureB_calibration.pdf",bbox_inches="tight")
print("wrote Figure B")
