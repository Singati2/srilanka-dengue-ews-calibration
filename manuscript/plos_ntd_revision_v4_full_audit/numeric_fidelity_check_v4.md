# Numeric fidelity check — v4 (transcription only; no recomputation)

Every displayed number is transcribed from a frozen committed report (verified 200/0 in the prior fidelity audit; re-mapped in `claim_source_crosswalk_v4.md` and `v4_verified_evidence_ledger.md`). No model, metric, bootstrap, or sensitivity was run for v4. v4-added/changed figures re-verified against frozen reports in the v4 audit: Sri Lanka p\*=0.40 ΔNB +0.0241 [+0.0090, +0.0399] (`targeted_value_climate_stage1a_h4_report.md` §4); Figure 2 threshold 0.34 column (−0.005/0.059/0.111/0.032/0.060) (`pilot_h4_75pct_calibration_dca_report.md` §11); M1 h=4 AUC raw 0.7515 → displayed 0.752 consistently (`label_horizon_robustness_report.md`); 4-decimal Sri Lanka ΔNB(M5−M1) +0.0081 [−0.0012, 0.0181] printed verbatim in `targeted_value_climate_stage1a_h4_report.md` line 16; TP-equivalent interval 1.2–2.6 per 100 = 100×[0.0117, 0.0260] (deterministic rescaling of the frozen Colombia ΔNB CI).

## Sri Lanka (sources: `analysis_table_linkage_v2_date_aligned_report.md`, `pilot_h4_75pct_calibration_dca_report.md`, `decision_threshold_dnb_robustness_report.md`, `rolling_recalibration_extension_report.md`, `hybrid_model_extension_report.md`, `targeted_value_climate_stage1a_h4_report.md`)
| Claim | Value in v3 | Frozen source | Verified |
|---|---|---|---|
| Modelable rows | 10,705 | linkage report | ✓ |
| After target | 10,516 | linkage report | ✓ |
| Train obs / alerts | 6,590 / 1,593 | linkage report | ✓ |
| Test obs / alerts | 3,926 / 1,321 | linkage report | ✓ |
| Prevalence shift | 24.2% → 33.6% | linkage report | ✓ |
| M1 AUC / NB0.30 | 0.752 / 0.137 | pilot DCA report | ✓ |
| M5 AUC / NB0.30 | 0.772 / 0.145 | hybrid report (0.7715/0.1447) | ✓ |
| M5−M1 ΔNB / 95% CI | +0.0081 / −0.0012 to +0.0181 | targeted-value report | ✓ |
| Residual CITL (M0–M3) | +0.029/+0.020/+0.046/+0.087 | recalibration report | ✓ |
| Recalibration fallbacks | 0 | recalibration report §5 ("Zero fallbacks across all models and methods") | ✓ |

## Colombia (sources: `colombia_model_ladder_report.md`, `colombia_horizon_sensitivity_report.md`, `colombia_outbreak_threshold_sensitivity_report.md`)
| Claim | Value in v3 | Frozen source | Verified |
|---|---|---|---|
| n / prevalence | 13,361 / 0.375 | model-ladder report | ✓ |
| M0 AUC / NB | 0.513 / 0.108 | model-ladder report | ✓ |
| M1 AUC / NB | 0.685 / 0.117 | model-ladder report | ✓ |
| M2 AUC / NB | 0.556 / 0.108 | model-ladder report | ✓ |
| M3 AUC / NB | 0.564 / 0.108 | model-ladder report | ✓ |
| M4 AUC / NB | 0.699 / 0.129 | model-ladder report | ✓ |
| M5 AUC / NB | 0.726 / 0.136 | model-ladder report | ✓ |
| alert-all / alert-none NB | ≈0.107 / 0 | model-ladder report | ✓ |
| ΔAUC / 95% CI | +0.040 / +0.024 to +0.058 | model-ladder report | ✓ |
| ΔNB / 95% CI | +0.0188 / +0.0117 to +0.0260 | model-ladder report | ✓ |
| ΔNB translation | 1.9 TP-equiv/100; 4.4 fewer false-alert-equiv/100 (2.7–6.1) | arithmetic transform of ΔNB and p* (no new estimate) | ✓ |
| Secondary climate-only | M2 AUC ≈0.532, M3 ≈0.546, NB ≈0.001 | model-ladder report | ✓ |
| Horizon increments | ≈+0.015 to +0.019 (h1–8), ≈+0.014 (h12); ΔAUC +0.040→+0.024 | horizon report | ✓ |
| E3 75/80/90th ΔNB | +0.0188 / +0.0157 / +0.0092; 90th prev ≈23.5% | outbreak-threshold report | ✓ |

**Figures:** Fig 1 schematic (no data). Fig 2 (SL DCA) plots the four representative-threshold NB values from `decision_threshold_dnb_robustness_report.md` (caption labels them representative thresholds; a complete continuous grid was NOT recomputed). Fig 3 (Colombia) plots AUC for M1–M5 from the model-ladder report; net benefit is in Table 5. Fig 4 (horizon) from the horizon/label reports. All figure coordinates are transcriptions of frozen table values.

**No numerical transcription error found.** No value was changed in v3 except formatting/notation (e.g., 95% CI label, fixed-point axis ticks).
