# Fig8 (Colombia forest) from FROZEN manuscript values; show BOTH the conditional and the
# development-inclusive (refit) interval for the climate-specific matched contrast.
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
FIG="/home/mpcrlab/srilanka-dengue-ews-calibration/manuscript/paper1_validity_corrected_candidate/submission_figs/Fig5.pdf"
# (label, point, cond_lo, cond_hi, refit_lo, refit_hi or None)
rows=[("M4$-$M1 (cases+climate)", 0.0122, 0.0073, 0.0171, None, None),
      ("matched$-$M1 (structure)",0.0110, 0.0060, 0.0164, None, None),
      ("M5$-$matched (climate)",  0.0078, 0.0039, 0.0119, 0.0008, 0.0209),
      ("M5$-$M1 (compound)",      0.0188, 0.0117, 0.0260, None, None)]
fig,ax=plt.subplots(figsize=(6.4,3.4))
for i,(lab,pt,clo,chi,rlo,rhi) in enumerate(rows):
    if rlo is not None:  # development-inclusive interval (wider, light, drawn first/behind)
        ax.errorbar(pt,i+0.13,xerr=[[pt-rlo],[rhi-pt]],fmt='none',ecolor='C1',elinewidth=1.4,capsize=3,alpha=0.9)
        ax.text(rhi+0.001,i+0.13,f"refit [{rlo:+.3f}, {rhi:+.3f}]",va='center',fontsize=6.5,color='C1')
    ax.errorbar(pt,i-0.06 if rlo is not None else i,xerr=[[pt-clo],[chi-pt]],fmt='o',capsize=3,color='C0')
    ax.text(chi+0.001,i-0.06 if rlo is not None else i,f"{pt:+.4f} [{clo:+.3f}, {chi:+.3f}]",va='center',fontsize=6.5,color='C0')
ax.axvline(0,color='k',lw=.6); ax.set_yticks(range(len(rows))); ax.set_yticklabels([r[0] for r in rows],fontsize=8)
ax.set_xlabel(r"$\Delta$NB at $p^*=0.30$"); ax.set_title("Colombia paired contrasts (post hoc)"); ax.set_xlim(-0.006,0.040)
# legend
from matplotlib.lines import Line2D
ax.legend(handles=[Line2D([0],[0],color='C0',marker='o',lw=1.2,label='conditional frozen-prediction 95% CI'),
                   Line2D([0],[0],color='C1',lw=1.4,label='development-inclusive (reproducible dept-refit) 95% CI')],
          fontsize=6.5, loc='lower right')
plt.tight_layout(); plt.savefig(FIG); plt.close()
print("Fig8 redrawn with conditional + development-inclusive intervals for the climate contrast")
