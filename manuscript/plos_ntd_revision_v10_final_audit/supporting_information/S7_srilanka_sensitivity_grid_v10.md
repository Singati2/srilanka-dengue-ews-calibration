# S7 Table — Sri Lanka linkage / climate-lag / late-2021 anomaly sensitivity (transcribed; no recomputation)
Source: `docs/pilot_h4_75pct_sensitivity_report.md` (frozen). h=4, 75th-pct label, test 2023–2025.

| Sensitivity | n test | events | prevalence | result vs primary |
|---|---|---|---|---|
| S1 naive v1 literal-week linkage | 3,926 | — | — | climate models slightly degrade (M2 AUC 0.622 vs 0.643; M3 0.646 vs 0.652); M1 unchanged (0.753) |
| S2 per-lag contemporaneous-climate (v2 primary) | 3,926 | 1,321 | 33.6% | PASS; conclusions unchanged |
| S3 drop late-2021 anomaly | 3,926 | 1,239 | 31.6% | PASS; conclusions unchanged |

Net benefit @ p*=0.30 under naive linkage: M1 0.136 ≫ M0 0.085 > M3 0.077 > M2 0.052. **Conclusion (all sensitivities): M1 recent-case baseline dominates; date-alignment helps climate marginally but does not overturn the ranking.** Values transcribed verbatim from the frozen report.
