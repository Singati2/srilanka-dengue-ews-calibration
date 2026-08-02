# Numeric fidelity check — v5 (transcription only; no recomputation)

Every displayed number is transcribed from a frozen committed report under `docs/` (prior fidelity audit: 200 checks / 0 mismatches; re-verified for v5 below). **No model, metric, bootstrap, CI, calibration, recalibration, sensitivity, threshold, heterogeneity, biomodel, or dataset transformation was run for v5.** Sources are listed per claim.

## Sri Lanka (sources: `pilot_h4_75pct_calibration_dca_report.md`, `decision_threshold_dnb_robustness_report.md`, `rolling_recalibration_extension_report.md`, `hybrid_model_extension_report.md`, `canonical_R_dlnm_report.md`, `targeted_value_climate_stage1a_h4_report.md`, `label_horizon_robustness_report.md`)

| Claim | Value | Frozen source |
|---|---|---|
| Test set / prevalence | n=3,926 RDHS-weeks, prevalence 0.336 | pilot DCA report; canonical_R_dlnm_report §line 11 |
| M0–M3 metrics (Table 1) | AUC 0.629/0.752/0.643/0.652; PR-AUC 0.459/0.652/0.460/0.476; Brier 0.222/0.191/0.220/0.220; CITL +0.530/+0.513/+0.479/+0.596; slope 0.664/1.246/1.027/0.738; mean pred 0.238/0.246/0.243/0.229; obs 0.336; NB@0.30 0.084/0.137/0.069/0.078 | pilot DCA report |
| Recalibration residual CITL | M0 +0.029, M1 +0.020, M2 +0.046, M3 +0.087 | rolling_recalibration_extension_report |
| Max recalibrated climate-only NB; M1 NB range | ≈0.085; 0.124–0.142 | rolling_recalibration_extension_report |
| Table 2 representative thresholds (alert-all/none/M0/M1/M2/M3) | 0.20, 0.30, 0.34, 0.40 rows | `pilot_h4_75pct_calibration_dca_report.md` §11 (exact: 0.34 row −0.005/0.000/0.059/0.111/0.032/0.060) |
| Canonical R DLNM vs M1 | ΔAUC −0.038 [−0.066,−0.008]; ΔNB@0.30 −0.025 [−0.041,−0.006]; M1 NB 0.137 vs 0.112 | canonical_R_dlnm_report §7 |
| Python-DLNM vs R-DLNM | ΔAUC +0.0003 [−0.005,0.007]; ΔNB +0.0008 [−0.005,0.007] | canonical_R_dlnm_report §39–40 |
| M4 (primary hybrid) | AUC 0.7643→0.764; NB band 0.20/0.30/0.40 = 0.1931/0.1284/0.0869 → 0.193/0.128/0.087 | hybrid_model_extension_report §3 (line 25), §7 band |
| ΔAUC(M4−M1); ΔNB(M4−M1)@0.30 | +0.013 [−0.020,0.046]; −0.008 [−0.028,0.013] | hybrid_model_extension_report §6 |
| M5 (steelman) | AUC 0.772 (0.7715), PR-AUC 0.667, Brier 0.180, NB@0.30 0.145 (0.1447); band 0.194/0.145/0.107 | hybrid_model_extension_report §3/§7 |
| ΔNB(M5−M1)@0.30 (primary, 4-dp) | +0.0081 (95% CI −0.0012 to +0.0181) | `targeted_value_climate_stage1a_h4_report.md` line 16 (verbatim) |
| p*=0.40 all-test ΔNB(M5−M1) | +0.0241 (95% CI +0.0090 to +0.0399) | `targeted_value_climate_stage1a_h4_report.md` §4 (line 31) |
| Largest regime estimate | +0.0202 (95% CI +0.0038 to +0.0370), 8 clusters | targeted_value report |
| M1 h=4 AUC display | 0.752 (raw 0.7515; rendered uniformly as 0.752) | label_horizon_robustness_report line 10 |
| Horizon AUC (h=1,2,4,8,12) | 0.843, 0.810, 0.752, 0.679, 0.646 | label_horizon_robustness_report |
| 26-RDHS coarse-CI caveat | "only 26 clusters → CIs coarse, may be anti-conservative" | `auc_dnb_confidence_interval_report.md` §3 |
| Bootstrap B, failures | B=1000, 0 failures | decision_threshold report §5; canonical_R_dlnm §48 (0/8000) |

## Colombia (sources: `colombia_model_ladder_report.md`, `colombia_horizon_sensitivity_report.md`, `colombia_outbreak_threshold_sensitivity_report.md`, `decision_threshold_dnb_robustness_report.md`)

| Claim | Value | Frozen source |
|---|---|---|
| Common-complete split / test n / prevalence | train 53,711 / val 12,713 / test 13,361; prevalence 0.375 | colombia_model_ladder_report §3 (line 20–21) |
| M0–M5 evaluated on n=13,361 (incl. M0) | yes (test-metrics table labeled common-complete, n=13,361, includes M0) | colombia_model_ladder_report §8 |
| AUC M0–M5 | 0.513/0.685/0.556/0.564/0.699/0.726 | §8 table |
| NB@0.30 M0–M5 | 0.108/0.117/0.108/0.108/0.129/0.136 | §8/§10 |
| CITL M0–M5 (post-Platt) | −0.50/−0.46/−0.50/−0.54/−0.45/−0.50 | §8 table |
| Brier range; slope range | 0.213–0.250; 0.85–3.43 | §8 table |
| Metrics are post-Platt (recalibrated) | yes; Platt fit on validation; AUC unchanged by monotone recal | §8 header, §9 |
| Observed prevalence retained? | yes — 0.375 for the common-complete test set (shared by all models) | §3/§8 |
| Per-model mean predicted probability retained? | NO (not in committed record) | v4 evidence ledger item 1 |
| treat-all (alert-all) NB; alert-none | ≈0.107; 0 | §8 (line 46) |
| ΔAUC(M5−M1); ΔNB(M5−M1)@0.30 | +0.040 (95% CI +0.024 to +0.058); +0.0188 (95% CI +0.0117 to +0.0260) | colombia model-ladder / decision_threshold §4 |
| Operational translation | 1.9 TP-equiv (≈1.2–2.6) / 100; 4.4 fewer false-alert equiv (2.7–6.1) / 100 — monotone rescalings of the same ΔNB CI (100×[0.0117,0.0260]) | deterministic transform of frozen ΔNB CI |
| Secondary climate-only (larger set) | M2/M3 NB ≈0.001; AUC ≈0.532/0.546 | colombia_model_ladder_report §... (full-set) |
| Horizon ΔNB(M5−M1) | ≈+0.015 to +0.019 across h=1–8; ≈+0.014 at h=12; ΔAUC +0.040 (h≤4) → +0.024 (h=12) | colombia_horizon_sensitivity_report |
| Stricter-threshold ΔNB(M5−M1)@0.30 (75/80/90th) | +0.0188 [+0.0117,+0.0260]; +0.0157 [+0.0082,+0.0236]; +0.0092 [+0.0003,+0.0183]; 90th-pct prevalence ≈23.5% | colombia_outbreak_threshold_sensitivity_report |

## v5-specific changes verified
- Sri Lanka M4 row newly displayed in Table 4 — all four cells trace to the frozen hybrid report (above). No recomputation.
- p*=0.30 decision-threshold interpretation corrected to 0.429 TP-equivalents per false alert and 2.33 false alerts per true alert: deterministic arithmetic (0.30/0.70=0.4286; 0.70/0.30=2.333).
- Colombia observed prevalence (0.375) restored as known for the common-complete set; only per-model mean predicted probability remains unretained.
- All calibration metrics labeled as post-Platt (recalibrated), matching the frozen §8 table header.

**No value in the manuscript is unsupported by a frozen source.**
