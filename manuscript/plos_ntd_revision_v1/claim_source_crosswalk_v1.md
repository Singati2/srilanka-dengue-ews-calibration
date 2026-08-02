# Claim-source crosswalk — revision v1 (numbers → frozen sources)

All figures verbatim from frozen committed reports (prior fidelity audit: 200 checks / 0 mismatches). No recomputation.

| Manuscript value | Frozen source |
|---|---|
| SL frame: 10,705 modelable rows; 10,516 after target; train 6,590/1,593; test 3,926/1,321; prev 24.2%→33.6% | `analysis_table_linkage_v2_date_aligned_report.md` |
| WER offset (≈1 wk; 2 wk in 2021; issue 43 missing; 53 dup of 52) | `analysis_table_linkage_v2_date_aligned_report.md`, `wer_2021_calendar_anomaly_decision_memo.md` |
| 26 RDHS / 60 edges; 208 denom records; rescaled-denominator census agreement (A20) | `rdhs_geometry_build_report.md`, `rdhs_adjacency_graph_build_report.md`, `population_denominator_rescaled_build_report.md` |
| SL Table 1 (M0–M3 AUC/PR-AUC/Brier/CITL/Slope/NB0.30) | `pilot_h4_75pct_calibration_dca_report.md` |
| SL Table NB grid (0.20/0.30/0.34/0.40) | `decision_threshold_dnb_robustness_report.md` |
| SL recalibration CITL (raw / rolling-52 / -104 / expanding) | `rolling_recalibration_extension_report.md` |
| SL S1–S3 sensitivities | `pilot_h4_75pct_sensitivity_report.md` |
| SL DLNM (Python/canonical R) + ΔAUC −0.038 / ΔNB −0.025 | `dlnm_climate_comparator_report.md`, `canonical_R_dlnm_report.md` |
| SL hybrid M4/M5 (AUC/PR-AUC/Brier/CITL/Slope/NB0.30) | `hybrid_model_extension_report.md` |
| SL targeted value (all-test +0.0081 [−0.0012,0.0181]; regimes; high×strongAR +0.0202 [0.0038,0.0370], 8 clusters; p*0.40 +0.0241) | `targeted_value_climate_stage1a_h4_report.md`, `novel_contribution_targeted_value_of_climate_spec.md` |
| SL horizon AUC/NB (75th/90th) | `label_horizon_robustness_report.md` |
| Colombia n=13,361; prev 0.375; M1–M5 AUC/NB0.30; ΔAUC +0.040 [0.024,0.058]; ΔNB +0.0188 [0.012,0.026] | `colombia_model_ladder_report.md` |
| Colombia horizon-flat (+0.015–0.019 h1–8; +0.014 h12; ΔAUC +0.040→+0.024) | `colombia_horizon_sensitivity_report.md` |
| Colombia E3 75/80/90th ΔNB +0.0188/+0.0157/+0.0092; 90th prev ≈23.5% | `colombia_outbreak_threshold_sensitivity_report.md` |
| Convergence/integrity audit (reproducibility note only) | `colombia_outbreak_threshold_sensitivity_report.md` §15, `scripts/audit_colombia_outbreak_threshold_sensitivity_v1.py` |
| ΔNB→units: +0.0188 ≈ 1.9 net TP-equiv/100; ≈4.4 fewer false-alert-equiv/100 (≈2.7–6.1) | derived from ΔNB and p*/(1−p*)=0.30/0.70; CI from [0.012,0.026] |

**Decision-analytic translation is a transform of the frozen ΔNB and p\*; it introduces no new estimate and required no computation.**
