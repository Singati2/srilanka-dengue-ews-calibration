# Phase 5 — Threshold consistency of the Sri Lanka matched climate increment

Computed from the VALIDATED frozen reconstruction (`threshold_sweep.py`; reproduces frozen M1/M4/M5 to ≤1.1e-16 before reporting). Net benefit NB(p*) = TP/N − (FP/N)·p*/(1−p*). Matched increment = ΔNB(M5 − M5_no-climate).

| p* | prop. flagged | NB M1 | NB M5 | NB matched | ΔNB matched climate | 95% CI | sign |
|---|---|---|---|---|---|---|---|
| 0.10 | 0.79 | 0.2586 | 0.2616 | 0.2586 | **+0.0030** | [−0.0072, +0.0112] | + |
| 0.20 | 0.52 | 0.1849 | 0.1944 | 0.1848 | **+0.0096** | [+0.0005, +0.0200] | + |
| 0.30 | 0.34 | 0.1366 | 0.1447 | 0.1360 | **+0.0087** | [−0.0010, +0.0189] | + |
| 0.40 | 0.21 | 0.0825 | 0.1066 | 0.0828 | **+0.0239** | [+0.0095, +0.0391] | + |
| 0.50 | 0.12 | 0.0489 | 0.0741 | 0.0487 | **+0.0255** | [+0.0148, +0.0357] | + |

**Sign of the matched increment is stable (positive) across the entire threshold grid.** The interval excludes zero at p*∈{0.20, 0.40, 0.50} and includes zero at p*∈{0.10, 0.30}. The p*=0.30 point (+0.0087) reproduces the authoritative value exactly. Reported honestly: the finding is consistent in **sign**, and its magnitude/precision vary with threshold; separation from zero at the reference p*=0.30 is not established on raw predictions. No significance is manufactured — the reference-threshold raw interval still includes zero. `dNB_M4_M1` (secondary, non-nested) is smaller and crosses zero at p*=0.30 (−0.008).
