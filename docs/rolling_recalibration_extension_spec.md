# Specification — Time-Updated / Rolling Recalibration Extension (design-lock)
*Pre-computation design lock for the rolling-recalibration extension to the h=4 / RDHS-75th-pct pilot. **No recalibration was run; no models fit; no labels created; no AUC/calibration/DCA/regression/net-benefit computed.** No frozen outcome/exposure/population, no v1/v2 linked table, and no existing pilot output file is modified — this memo is documentation only. It extends, and does not replace, the committed primary pilot (`docs/pilot_h4_75pct_calibration_dca_report.md`) and S1–S3 sensitivities (`docs/pilot_h4_75pct_sensitivity_report.md`).*

**Date:** 2026-06-12 · **Status:** specification only — locks choices **before** any computation to prevent post-hoc window/method selection.

## 1. Purpose
The primary pilot and S1–S3 showed a robust **under-prediction (positive calibration-in-the-large) on the 2023–2025 test period** that training-only Platt recalibration did **not** fix. This extension tests whether an **operationally realistic, time-updated recalibration** — one that re-estimates the calibration map as new completed outcomes arrive — can correct that drift.
- This targets **calibration drift, not discrimination** (monotone recalibration leaves AUC/PR-AUC essentially unchanged).
- It is an **extension after** the primary and S1–S3 results, not a replacement; the primary conclusions stand regardless of the outcome here.

## 2. Primary input
- Primary prediction table (quarantined, read-only, **not altered**): `~/data_quarantine/model_pilots/pilot_h4_75pct_v1/predictions_h4_75pct_v1.csv` (test-period M0–M3 predictions; sha256 `07f5916a…`).
- Same h=4 target, RDHS-75th-pct label (train-2018–2022 thresholds), train/test split (2018–2022 / 2023–2025), and M0–M3 model definitions as the primary pilot.
- **Required full-span prediction stream:** rolling/expanding windows for an early-2023 test week need model predictions on *completed-target* weeks **before** that week (i.e. into 2022 and earlier), but the primary CSV stores only test-period predictions. The extension will therefore **deterministically re-fit M0–M3 on the identical training set (2018–2022)** — reproducing the original models and their test predictions **byte-identically** (the pipeline was verified deterministic) — and **score** the full 2018–2025 span to obtain the prediction stream. This is scoring, not a new model search; the original prediction CSV is **not modified**. No new model classes are introduced.

## 3. Recalibration ladder (pre-specified)
A logistic (Platt-style) calibration map on the linear predictor `z = logit(p_raw)`, refit over a moving information set:
- **R0 — Raw** prediction (already reported; reference).
- **R1 — Rolling intercept-only:** `logit(p_cal) = z + a_t`, `a_t` refit each week on the rolling window. Corrects calibration-in-the-large only.
- **R2 — Rolling intercept + slope:** `logit(p_cal) = b_t·z + a_t`, both refit each week on the rolling window.
- **R3 — Expanding-window intercept-only:** `a_t` refit on all prior completed weeks since 2018.
- **R4 — (Optional) Expanding-window intercept + slope:** `b_t, a_t` on all prior completed weeks; run **only if** window event counts are adequate (§6).
All maps are **pooled across the 26 RDHS** (a single central recalibration updated over time), applied to that week's forecasts for all divisions.

## 4. Time-updated information rule (leakage prevention)
The forecast made at prediction week *t* targets week *t+4*; its outcome is observed only at *t+4*. Therefore, at prediction week *t*, the recalibration map may be fit **only on forecast–outcome pairs whose target week is strictly before *t*** (target week ≤ *t−1*), i.e. forecasts issued at prediction week *s* with *s ≤ t−5* (since target = *s+4*). No outcome at or after *t* — and in particular not the current forecast's own t+4 outcome — may enter the map. This mirrors real-time deployment: only fully-completed targets inform recalibration.

## 5. Window definitions
Measured in **completed-target weeks** ending at *t−1*:
- **Primary rolling window:** previous **52** completed weeks.
- **Sensitivity rolling window:** previous **104** completed weeks (applied to R1/R2).
- **Expanding window:** **all** completed weeks since 2018 up to *t−1* (R3/R4).
- Windows pool all 26 RDHS, so a 52-week window contains up to ~26×52 forecast–outcome pairs.
- Full curve over all pre-specified windows is reported; **no single window is selected post hoc as the headline.**

## 6. Minimum-sample / stop rules
Per recalibration fit at week *t*:
- **Intercept+slope (R2/R4):** require **≥50 events and ≥50 non-events** in the window; otherwise **fall back to intercept-only**.
- **Intercept-only (R1/R3):** require **≥1 event and ≥1 non-event** (and ≥ a small minimum total, e.g. 20); if too sparse, **fall back to raw (R0)** and flag the week.
- **Stability:** if a refit fails to converge, or produces extreme recalibrated probabilities (e.g. any |coefficient| absurdly large, or recalibrated p pinned at 0/1 for a large share of rows), **fall back to the next-simpler method** and flag.
- The fraction of test weeks served by each fallback level is reported (no silent fallback).
- Global stop: if the extension cannot be run without leakage or adequate windows for the bulk of the test period, **stop and report** rather than force it.

## 7. Models to recalibrate
Apply the ladder to **M0, M1, M2, M3**. Primary interpretive focus: **M1 (recent-cases AR) versus M2/M3 (climate)**. No new model classes.

## 8. Evaluation (test period 2023–2025)
Per model × recalibration method, compare raw (R0) vs time-updated:
- **Calibration-in-the-large** (intercept, offset model), **calibration slope**, **Brier score**, **mean predicted vs observed**.
- **AUC / PR-AUC** (expected ~unchanged under monotone recalibration; reported to confirm).
- **DCA** on p\* = 0.05–0.50 (alert-all / alert-none comparators); **net benefit at p\*=0.30** highlighted.
- Evaluation is on the same fully-modelable test rows as the primary pilot, restricted to weeks where a valid recalibration window exists (others flagged).

## 9. Interpretation rules (pre-committed)
- **If rolling recalibration fixes CITL but M1 still dominates DCA** → "calibration drift is operationally correctable, **but the climate EWS still does not outperform the recent-case baseline**."
- **If rolling recalibration lifts M2/M3 enough to beat M1** on calibration *and* net benefit → report as a **major robustness finding** (would revise the lean).
- **If rolling recalibration fails to fix the drift** → "calibration drift is a **deployment limitation not solved by simple time-updating**."
- Report **all** pre-specified windows/methods; do not promote the best-performing window to the headline.

## 10. Outputs to be generated later (NOT now) — quarantined only
Directory: `~/data_quarantine/model_pilots/rolling_recalibration_v1/`
- `rolling_recalibration_predictions_v1.csv`
- `rolling_recalibration_metrics_v1.csv`
- `rolling_recalibration_dca_v1.csv`
- `rolling_recalibration.meta.md`
CSVs made read-only with SHA256 recorded; **none committed**. Safe repo report later: `docs/rolling_recalibration_extension_report.md` (the only artifact proposed for commit).

## 11. Confirmation
- This memo is **documentation only**; no recalibration or models were run; no new labels/metrics computed.
- **No data files modified**; **no frozen files modified**; the primary pilot prediction CSV and directory are untouched.
- **No outputs committed.** Preregistration unchanged.

## Next step (separate, approval-gated)
On approval, run the ladder R0–R4 with the leakage rule and windows above, write the quarantined outputs + a safe markdown report, and apply the §9 interpretation rules. Nothing runs until directed.
