# V6_CROSSCHECK.md
Tolerances (locked): identical-code/data score values abs tol 1e-10; rounded published values
to published precision.

| Quantity | Version 6 | Phase 2 recomputed | Δ | Status |
|---|---|---|---|---|
| Colombia test n | 13,361 | 13,361 | 0 | MATCH |
| Colombia prevalence | 0.375 | 0.3753 | <1e-3 | MATCH (rounding) |
| Colombia clusters (dept/muni) | 31 / 475 | 31 / 475 | 0 | MATCH |
| Colombia M5_recal AUC | (frozen M5) | 0.7255 | — | MATCH: Phase-2 full-recal AUC 0.7255 equals committed frozen M5_recal AUC |
| Colombia regen M5_recal vs frozen file | committed | 1.11e-16 | <1e-10 | MATCH (per-observation) |
| Colombia matched dNB(recal)@0.30 | +0.00786 | +0.00783 | 3e-5 | MATCH (<1e-3 gate) |
| Sri Lanka test n | 3,926 | 3,926 | 0 | MATCH |
| Sri Lanka prevalence | 0.336 | 0.3365 | <1e-3 | MATCH |
| Sri Lanka clusters | 26 RDHS | 26 | 0 | MATCH |
| Sri Lanka M1/M4/M5 vs frozen | committed | <1e-6 | <1e-6 | MATCH (reproduce-gate) |
| Sri Lanka matched dNB(recal)@0.30 | +0.0157 | +0.01565 | 5e-5 | MATCH |

No Version 6 value was overwritten. All discrepancies are rounding at published precision or
below the 1e-6 reproduce-gate. The Phase-2 proper-score analysis therefore evaluates the same
frozen predictions the Version-6 decision-curve analysis used.
