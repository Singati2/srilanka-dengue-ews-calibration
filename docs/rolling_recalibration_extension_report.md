# Rolling / Time-Updated Recalibration — Extension Report
*Executed exactly per the locked spec (`docs/rolling_recalibration_extension_spec.md`, commit 6d423b4). All computed artifacts are **quarantined and git-ignored**; only this markdown report is proposed for commit. No frozen outcome/exposure/population, no v1/v2 linked table, and no existing pilot output file was modified. This extends — does not replace — the primary pilot and S1–S3.*

**Date:** 2026-06-12

## 1. Input & integrity
- Primary table v2: SHA256 `3a197d61…` ✅ (read-only). Primary pilot predictions `07f5916a…`, metrics `a5366123…` (read-only, unaltered).

## 2. Full prediction-stream reconstruction & reproducibility check
Rolling windows for early-2023 test weeks need model predictions on completed pre-test weeks, but the primary pilot saved only test predictions. The M0–M3 models were therefore **deterministically re-fit on the identical 2018–2022 training set** and scored over the full 2018–2025 span (scoring, not a new model search). The reconstructed **test predictions reproduce the committed primary to numerical precision**: max |Δ| ≤ **8.9 × 10⁻¹⁶** across all four models → reproducible (<1e-9). The original prediction CSV was not altered.

## 3. Recalibration information rule (leakage prevention, date-enforced)
Time-updated Platt map on `z = logit(p_raw)`, pooled across the 26 RDHS. At prediction week *t* (target *t+4*), only forecast–outcome pairs whose **target week is strictly before *t*** are eligible (i.e. prediction week *s ≤ t−5*). The current row's own *t+4* outcome and any outcome at/after *t* are excluded. Enforced by dates, not row position.

## 4. Window / method ladder
- **R0** raw (reference) · **R1** rolling-52 intercept-only · **R2** rolling-52 intercept+slope · **R3** expanding intercept-only · **R4** expanding intercept+slope · **R1_104 / R2_104** rolling-104 variants. All pre-specified; full table reported (no post-hoc window selected as headline).

## 5. Fallback / stop-rule results
**Zero fallbacks across all models and methods.** Every eligible window contained ≥50 events and ≥50 non-events, so intercept+slope methods (R2/R4/R2_104) ran at full level (100%) and intercept-only methods (R1/R3/R1_104) ran at full level (100%); no raw fallback, no convergence failure, no extreme/pinned probabilities. (Windows are well-populated because the pooled 26-RDHS stream and the 2018–2022 history feed even the earliest 2023 test weeks.)

## 6. Calibration: raw vs time-updated (test 2023–2025, prevalence 0.336)
**Calibration-in-the-large (CITL; target 0):**
| Model | R0 raw | R1 roll-52 | R1_104 | R3 expand |
|---|---|---|---|---|
| M0 | +0.530 | **+0.029** | +0.137 | +0.338 |
| M1 | +0.513 | **+0.020** | +0.111 | +0.325 |
| M2 | +0.479 | **+0.046** | +0.155 | +0.314 |
| M3 | +0.596 | **+0.087** | +0.204 | +0.394 |

**Finding:** the **rolling 52-week intercept-only recalibration drives CITL to ≈0** (+0.02 to +0.09) for every model — the 2023–2025 under-prediction is **operationally correctable**. The shorter window corrects best because it tracks the rising prevalence; the **expanding window under-corrects** (CITL +0.31 to +0.39) by averaging in the lower-prevalence early years; the 104-week window is intermediate. Brier improves slightly for the better-calibrated M1 (0.191→0.186 under R1) and is roughly flat elsewhere.

## 7. Discrimination: raw vs recalibrated
| Model | R0 AUC | AUC range across R1–R4 | R0 PR-AUC |
|---|---|---|---|
| M0 | 0.629 | 0.560–0.596 | 0.459 |
| **M1** | **0.752** | **0.707–0.741** | 0.652 |
| M2 | 0.643 | 0.536–0.627 | 0.460 |
| M3 | 0.652 | 0.581–0.638 | 0.476 |

AUC is **not exactly preserved** under time-updated recalibration — because the map is **time-varying** (a different intercept/slope each week), it is monotone *within* each week but not globally across the pooled test set, so pooled ranking shifts modestly. The shifts are small and **M1 remains clearly highest at every method** (0.707–0.752 vs climate 0.536–0.652).

## 8. Decision-curve / net benefit (test), net benefit @ p\*=0.30
| Model | R0 | R1 roll-52 | R3 expand | R4 expand |
|---|---|---|---|---|
| M0 | 0.084 | 0.068 | 0.085 | 0.085 |
| **M1** | **0.137** | 0.124 | **0.141** | **0.142** |
| M2 | 0.069 | 0.063 | 0.082 | 0.082 |
| M3 | 0.078 | 0.085 | 0.083 | 0.082 |

Across **all method × threshold cells**, M1 net benefit (range 0.124–0.142 @ p\*=0.30) exceeds every climate value (0.055–0.085); climate beats M1 at only 92/644 method×threshold×climate cells — all in the low-p\* (≤~0.16) band where alert-all is itself competitive, never in the operational mid-high range.

## 9. Does recalibration change the M1-vs-climate conclusion?
**No.** Under **every** recalibration method:
- No climate model beats M1 on **AUC** (max climate 0.652 < min M1 0.707).
- No climate model beats M1 on **net benefit @ p\*=0.30** (max climate 0.085 < min M1 0.124).
- No climate model is materially better-calibrated than M1.

## 10. Interpretation (pre-committed rule applied)
Matching the spec's pre-committed branch: **calibration drift is operationally correctable** (rolling-52 recalibration removes the under-prediction), **but the climate-driven EWS still does not outperform the recent-case AR baseline (M1)** on discrimination or net benefit. The alternative branch ("recalibration lifts M2/M3 past M1") did **not** occur. This **strengthens** the calibration-reporting / data-resource framing (prereg §O): the calibration story is a deployable lesson (drift is fixable with simple time-updating, and the right window matters — short rolling beats expanding), while the headline "climate EWS beats surveillance" remains unsupported.

## 11. Output files (quarantined, read-only, NOT committed) + SHA256
- `rolling_recalibration_predictions_v1.csv` — `c2490ae4811506fa288ed1ec8018941d4ce7644d82b139b7fcf8152e0a68f005`
- `rolling_recalibration_metrics_v1.csv` — `084ea264ccb1314132455c28208cd73310ae232d3182e21b618b8d876452c60c`
- `rolling_recalibration_dca_v1.csv` — `e7727264f1ec7c17ca2797d5659ccfe6bb6dad6942d8d6febcee451f6530db6b`
- `rolling_recalibration_fallbacks_v1.csv` — `165323612f3f49c936d66011cb2888d6bf17e7cf3549ae22c748dea0814c8f2d`
- Metadata: `rolling_recalibration.meta.md` (all under `~/data_quarantine/model_pilots/rolling_recalibration_v1/`).

## 12. Confirmations
- Only the spec'd R0–R4 (+104-week) ladder was run; no new labels/horizons/model classes; no post-hoc window promoted to headline (full table reported).
- **No frozen outcome/exposure/population or linked-analysis CSV (v1/v2) was modified**; input checksums re-verified. The primary pilot directory and its prediction CSV were not overwritten.
- **No data files committed** — all outputs quarantined/git-ignored; only this markdown report is proposed for commit.
- Preregistration unchanged.

## 13. Next steps (separate, approval-gated)
90th-pct label and h = 1/2/8/12 horizon variants; results synthesis toward the manuscript framing. Nothing runs until directed.
