#!/usr/bin/env python3
"""
Calibration-robustness sensitivity of the matched climate ablation (reviewer I7).

Reads the committed frozen matched-pair predictions (ALT_STATS/frozen/*.csv), reproduces the
published conditional point estimates and interval as gates, then computes the intercept-shift
sensitivity: shift BOTH models' predictions by delta logits and recompute the matched dNB at
p*=0.30. This tests whether the Colombia increment is an artifact of the shared ~0.5-logit
over-prediction. CONDITIONAL on the frozen predictions only (does not address development-inclusive
robustness). Env: numpy 1.26.4, pandas 2.1.3 (reconstruction lockfile). Seed 20260612.
NB definition matches analysis/v12_referee_response/run/co_selection_validation_figs.py.
"""
import os, numpy as np, pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
FROZEN = os.path.join(HERE, "..", "frozen")
OUT = os.path.join(HERE, "..", "results", "calibration_sensitivity.csv")
SEED = 20260612
SHIFTS = [-1.0, -0.5, -0.25, 0.0, 0.25, 0.5, 1.0]

def sig(x): return 1.0 / (1.0 + np.exp(-x))
def logit(p):
    p = np.clip(p, 1e-15, 1 - 1e-15); return np.log(p / (1 - p))
def nb(p, y, t=0.30):
    a = p >= t; n = len(y)
    return (a & (y == 1)).sum() / n - (a & (y == 0)).sum() / n * (t / (1 - t))
def nll(p, y):
    p = np.clip(p, 1e-15, 1 - 1e-15); return -(y * np.log(p) + (1 - y) * np.log(1 - p)).mean()
def brier(p, y): return ((p - y) ** 2).mean()

GATES = {  # committed targets (route_a_primary.csv / path_b / sl_matched_and_recal)
    "Colombia": dict(nb_recal=0.0078, nll_recal=-0.0089, brier_recal=-0.0043, cond_ci=(0.0039, 0.0119)),
    "SriLanka": dict(nb_recal=0.0157, nb_raw=0.0087, nll_recal=-0.0207, brier_recal=-0.0079),
}

rows = []
for name, fname in [("Colombia", "colombia_matched_pairs.csv"), ("SriLanka", "srilanka_matched_pairs.csv")]:
    d = pd.read_csv(os.path.join(FROZEN, fname))
    y = d.outcome.values.astype(int)
    fr, nr = d.full_recal.values, d.noclim_recal.values
    fw, nw = d.full_raw.values, d.noclim_raw.values
    g = GATES[name]
    print(f"\n== {name} (n={len(y)}, events={y.sum()}) ==")
    def gate(lbl, got, exp):
        ok = "PASS" if (exp is None or abs(got - exp) < 6e-4) else "FAIL"
        print(f"  GATE {lbl}: {got:+.4f} vs {exp}  {ok}")
    gate("matched dNB recal", nb(fr, y) - nb(nr, y), g["nb_recal"])
    gate("dNLL recal", nll(fr, y) - nll(nr, y), g["nll_recal"])
    gate("dBrier recal", brier(fr, y) - brier(nr, y), g.get("brier_recal"))
    if "nb_raw" in g: gate("matched dNB raw", nb(fw, y) - nb(nw, y), g["nb_raw"])

    # conditional cluster bootstrap (municipality = spatial_unit_id) for gate + shifted CI
    clusters = d.spatial_unit_id.values
    uniq = np.unique(clusters)
    idx_by = {c: np.where(clusters == c)[0] for c in uniq}
    def matched_dnb(rowsel, delta):
        yy = y[rowsel]
        return nb(sig(logit(fr[rowsel]) + delta), yy) - nb(sig(logit(nr[rowsel]) + delta), yy)
    def boot_ci(delta, B=1000):
        rng = np.random.default_rng(SEED); est = []
        for _ in range(B):
            samp = rng.choice(uniq, size=len(uniq), replace=True)
            est.append(matched_dnb(np.concatenate([idx_by[c] for c in samp]), delta))
        e = np.array(est); return float(np.percentile(e, 2.5)), float(np.percentile(e, 97.5))
    full = np.arange(len(y))
    if name == "Colombia":
        lo0, hi0 = boot_ci(0.0)
        gate("conditional 95% CI (delta=0)", lo0, g["cond_ci"][0]); gate("  upper", hi0, g["cond_ci"][1])
    print("  I7 intercept-shift (both models; matched dNB @ p*=0.30, recal):")
    for delta in SHIFTS:
        pt = matched_dnb(full, delta)
        lo, hi = boot_ci(delta)
        print(f"     delta={delta:+.2f}: dNB={pt:+.4f}  cond95%[{lo:+.4f},{hi:+.4f}]")
        rows.append(dict(setting=name, delta_logit=delta, matched_dNB=round(pt, 6),
                         cond_ci_lo=round(lo, 6), cond_ci_hi=round(hi, 6), threshold=0.30,
                         state="recal", B=1000, seed=SEED))

pd.DataFrame(rows).to_csv(OUT, index=False)
print(f"\nwrote {os.path.relpath(OUT, os.path.join(HERE, '..', '..'))}")
