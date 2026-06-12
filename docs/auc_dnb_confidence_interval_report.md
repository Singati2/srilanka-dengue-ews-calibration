# ΔAUC / ΔNB Confidence Intervals — Report
*Executed exactly per the locked spec (`docs/auc_dnb_confidence_interval_spec.md`, commit 1d8a5da). Predictions were **held fixed** (reused from the committed primary pilot); no models were rerun or refit, no labels created, no DLNM added. All computed artifacts are **quarantined and git-ignored**; only this markdown report is proposed for commit. This is reporting-quality hardening (uncertainty quantification), not model selection or threshold optimization.*

**Date:** 2026-06-12

## 1. Input file & checksum
- `~/data_quarantine/model_pilots/pilot_h4_75pct_v1/predictions_h4_75pct_v1.csv`, SHA256 **`07f5916a…`** ✅ (read-only, unaltered). Primary h=4 / 75th-pct test set: n = 3,926 RDHS-weeks, 26 RDHS, prevalence 0.336.

## 2. Point-estimate reproduction check (stop-gate, passed)
Recomputed from the saved predictions vs the committed primary report — all match to <1e-4:
| Model | AUC (recomputed / committed) | NB@0.30 (recomputed / committed) |
|---|---|---|
| M0 | 0.6291 / 0.6291 | 0.08376 / 0.08376 |
| M1 | 0.7515 / 0.7515 | 0.13663 / 0.13663 |
| M2 | 0.6429 / 0.6429 | 0.06870 / 0.06870 |
| M3 | 0.6519 / 0.6519 | 0.07798 / 0.07798 |
No conflict with committed point estimates.

## 3. Bootstrap design
- **RDHS cluster (block) bootstrap:** resample the 26 RDHS with replacement; each drawn RDHS contributes its **entire** 2023–2025 test series (respects within-RDHS spatial + temporal autocorrelation).
- **Seed 20260612** (fixed); **percentile 95% CI**.
- Predictions fixed; only evaluation metrics recomputed per resample.
- **Caveat:** only 26 clusters → CIs are coarse and may be wide/slightly anti-conservative; borderline intervals should not be over-interpreted.

## 4. B=200 pilot → B=1000 final
- **B=200 pilot:** effective B = 200, **0 failures (0.00%)** → ≤5% gate passed, runtime trivial.
- **B=1000 final:** effective B = 1000, **0 failures (0.00%)**. CIs below use B=1000.

## 5. AUC and ΔAUC (95% percentile CI)
| Quantity | Point | 95% CI | Excludes 0? |
|---|---|---|---|
| AUC M0 | 0.629 | [0.594, 0.667] | — |
| AUC M1 | 0.752 | [0.721, 0.781] | — |
| AUC M2 | 0.643 | [0.589, 0.688] | — |
| AUC M3 | 0.652 | [0.624, 0.681] | — |
| **ΔAUC M1−M2** | **0.109** | **[0.064, 0.158]** | **Yes** |
| **ΔAUC M1−M3** | **0.100** | **[0.067, 0.128]** | **Yes** |
| ΔAUC M1−M0 (optional) | 0.122 | [0.093, 0.146] | Yes |

→ M1's discrimination advantage over **both** climate models is **statistically supported** (CIs exclude 0).

## 6. Net benefit and ΔNB at p\*=0.30 (95% CI)
| Model | NB@0.30 | 95% CI |
|---|---|---|
| M0 | 0.084 | [0.052, 0.118] |
| M1 | 0.137 | [0.101, 0.176] |
| M2 | 0.069 | [0.044, 0.097] |
| M3 | 0.078 | [0.052, 0.108] |

| ΔNB@0.30 | Point | 95% CI | Excludes 0? |
|---|---|---|---|
| **M1−M2** | **0.068** | **[0.047, 0.092]** | **Yes** |
| **M1−M3** | **0.059** | **[0.042, 0.077]** | **Yes** |

→ At the registered threshold, M1's net-benefit advantage over both climate models **excludes 0** (statistically supported).

## 7. ΔNB threshold-band CIs (p\* ∈ {0.10, 0.20, 0.30, 0.40})
| p\* | M1−M2 ΔNB [95% CI] | excl 0 | M1−M3 ΔNB [95% CI] | excl 0 |
|---|---|---|---|---|
| 0.10 | −0.004 [−0.010, 0.003] | **No** | +0.010 [0.003, 0.018] | Yes |
| 0.20 | +0.020 [0.001, 0.041] | Yes | +0.038 [0.024, 0.054] | Yes |
| 0.30 | +0.068 [0.047, 0.092] | Yes | +0.059 [0.042, 0.077] | Yes |
| 0.40 | +0.070 [0.045, 0.096] | Yes | +0.043 [0.024, 0.067] | Yes |

→ M1 > climate on net benefit at the **operational band (p\* = 0.20–0.40)**, CIs exclude 0 for both comparisons. **The single interval crossing 0** is **M1−M2 at p\* = 0.10** (low threshold), where the difference is **not significant** — exactly the low-threshold region where the prior point estimates already showed M2 competitive (alert-all also competitive there). Reported as-is; not hidden.

## 8. Bootstrap diagnostics / failure rate
| B | effective B | failures | failure rate | seed | clusters | n_test |
|---|---|---|---|---|---|---|
| 200 (pilot) | 200 | 0 | 0.00% | 20260612 | 26 | 3,926 |
| 1000 (final) | 1000 | 0 | 0.00% | 20260612 | 26 | 3,926 |
No degenerate (single-class) resamples; percentile-95 CIs.

## 9. Interpretation (locked rules applied)
- **CI excludes 0 → supported:** ΔAUC (M1−M2, M1−M3) and ΔNB@0.30 (M1−M2, M1−M3) all exclude 0 → the M1-over-climate advantage on discrimination and on registered net benefit is **statistically supported**, not a point-estimate artifact.
- **CI crosses 0 → uncertain:** ΔNB M1−M2 at p\*=0.10 crosses 0 → **no significant difference** at that low threshold; reported plainly, **no spin**.
- **No selective reporting:** all pairs, both metrics, and the full p\* band are shown.
- **No headline change without team review:** these CIs *strengthen* the existing committed conclusion (they do not overturn any point estimate); the study headline is unchanged pending team review. Caveat: 26-cluster bootstrap → CIs coarse.

## 10. Output files (quarantined, read-only, NOT committed) + SHA256
- `auc_ci_primary_v1.csv` — `f6ebd575df5dcf3baf435abed1c65ef04cc65dbea7b49d65a472194c1b69067d`
- `dnb_ci_primary_v1.csv` — `0d2188031c59a62ac3f668ca3585c9777011687c54ca3be8a3965bbd7672c07f`
- `dca_threshold_band_ci_v1.csv` — `d3bf52da9708be6d0595f5be3d4846bdb9bb1df3301eff85dda74ca378faeb1a`
- `uncertainty_bootstrap_diagnostics_v1.csv` — `a0f08634aa5493d85813674af0a7c6252370a088f155f4545a556baef81a2497`
- Metadata: `uncertainty_intervals.meta.md` (all under `~/data_quarantine/model_pilots/ci_bootstrap_v1/`).

## 11. Confirmations
- **No models rerun or refit; no labels created; no DLNM added.** Predictions fixed and read-only.
- **No frozen files modified; no prior pilot/sensitivity/recalibration/label-horizon output overwritten** (input checksum re-verified; new directory only).
- **No data files committed** — all outputs quarantined/git-ignored; only this markdown report is proposed for commit.
- Preregistration unchanged.

## 12. Next steps (separate, approval-gated)
DLNM climate comparator (deferred, explicit approval only); team-written p\* cost-anchoring narrative; optional recalibrated-prediction CIs. Nothing runs until directed.
