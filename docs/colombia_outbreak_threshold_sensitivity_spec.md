# E3 — Colombia Outbreak-Threshold Sensitivity Specification (memo only — NO E3 run)
*Specifies whether the modest hybrid advantage over recent-case surveillance survives a **rarer, more epidemic-like** outbreak definition (75th → 80th/90th percentile). **Specification only: no models run, no predictions, no metrics, no labels created, no thresholds recomputed, no data/quarantine outputs modified, nothing committed.** 75th-percentile h=4 remains the registered primary analysis.*

**Date:** 2026-06-19 · **Status:** specification only · **Base commit:** 643f039 · **Builds on:** `docs/paper_strategy_reframe_memo.md` (E3), `docs/colombia_model_ladder_report.md`, `docs/colombia_label_construction_report.md`.
**E1 status (explicit):** the E1 report/script (`docs/decision_threshold_dnb_robustness_report.md`, `scripts/decision_threshold_dnb_robustness_v1.py`) are **present but uncommitted** (untracked); left untouched here.

## 1. Purpose
Test whether the modest hybrid advantage over recent-case surveillance holds when the outbreak definition becomes rarer/more epidemic-like. **Primary question:** does **ΔNB(M5−M1) at h=4 remain positive when the outcome threshold moves from the train-unit 75th percentile to the 80th and 90th percentiles?** This directly tests whether the existing result is an artifact of the relatively high-prevalence (~37.5%) 75th-percentile label.

## 2. Analysis status & hierarchy
- Colombia **h=4, 75th percentile** remains the **registered primary** analysis.
- 80th/90th-percentile analyses are **secondary sensitivity**.
- Do **not** replace, redefine, or silently update the primary result; do **not** select the most favorable percentile as a new headline; **report all attempted percentile definitions, including null/unstable**.

## 3. Outcome definitions (later run)
- **75th-pct:** existing committed reference outcome.
- **80th-pct:** derive **training-period data only** (per-GID_2); not currently in the threshold table — compute in the E3 run, save as a **new versioned output** (do not modify the existing threshold file).
- **90th-pct:** use the **already-computed train-only `thr90`** in `colombia_label_thresholds_train_only_v1.csv` **if verifiable**; otherwise **stop** rather than silently recomputing.
- All thresholds **municipality/GID_2-specific**, same construction as the committed 75th-pct analysis. **No full-sample or test-period information** in any threshold.

## 4. Threshold verification before any future run
Before label construction in the run: locate the committed threshold table; verify columns for 75th and 90th pct; verify the table **checksum**; verify **train-only** derivation; check whether 80th-pct thresholds exist; if not, compute them **only in the E3 run on the frozen training split** and save as a new versioned file; **do not modify the existing threshold file**.
*(Preflight already observed: `colombia_label_thresholds_train_only_v1.csv`, 1051 GID_2, columns include `thr75`,`thr90`; `thr80` absent; no duplicate GID_2.)*
**Stop if:** the threshold file cannot be verified; thresholds appear to use validation/test outcomes; GID_2 keys duplicated/missing; 90th-pct provenance unclear.

## 5. Forecast horizon & model comparison
- Primary E3 setting: **Colombia, h=4 weeks**, same train/val/test periods, same **M0–M5 ladder**, same feature definitions, same **train-only preprocessing**, **validation-only C selection**, **validation-only Platt recalibration**, **test used once**.
- **Primary comparison: M5 vs M1.** Secondary: M4 vs M1; M2/M3 vs M1; M0 reference if useful.
- **Do NOT add** new predictors, longer climate lags, DLNM features, alternative geographic splits, or new horizons in E3.

## 6. Common-complete row-set rule (per percentile, independently)
Per outbreak percentile: label defined; climate lags 0–8 complete; `cases_lag0/1/2/4` complete; valid split; **all compared models use the same test rows within that percentile**.
Report by percentile × split: total n; #GID_2 units; #events; event prevalence; min & median events per GID_2; #GID_2 with zero test events.
- Do **not** force 75/80/90 to use identical rows if label availability differs — **make row-set differences explicit**.
- Optional common-intersection row sensitivity **only if** it does not materially reduce sample size (not primary).

## 7. Sparsity & stop rules (pre-specified, objective)
**Downgrade the 90th-pct analysis to descriptive/exploratory (or stop) if:** test outcome one-class; event prevalence extremely low; too few test events for stable AUC/PR-AUC/calibration/DCA; a large fraction of GID_2 have no test events; **cluster bootstrap failure rate > 5%**; calibration parameters non-identifiable/unstable; CIs unreliable from sparse cluster-level events.
- **No arbitrary sample-size cutoff alone**; the report must give **actual event counts** and explain any stop/downgrade.
- If 90th unstable but 80th adequate: report **75th + 80th** as the primary sensitivity comparison; **report the attempted 90th and why** it was unstable; **do not hide it**.

## 8. Metrics for the future run
Per percentile × model: AUC; PR-AUC; Brier; calibration intercept/CITL; calibration slope; **NB at registered p\*=0.30**; **DCA across p\*=0.10–0.50**; ΔAUC vs M1; ΔNB vs M1.
- Because prevalence changes substantially, **emphasize PR-AUC, calibration, decision-curve net benefit, and event counts/prevalence**. **AUC alone must not determine the conclusion.**

## 9. Bootstrap uncertainty
GID_2 cluster bootstrap; **B=1000; seed 20260612**; resample GID_2 with replacement (all weeks of a unit together); **percentile 95% CI**; report failure rate.
- **Primary interval:** ΔNB(M5−M1) at p\*=0.30. Secondary: ΔAUC(M5−M1); ΔNB(M4−M1); PR-AUC differences if feasible/stable.
- One-class bootstrap replicate → mark that discrimination metric failed, exclude from that metric's denominator, **report failure count and rate**.

## 10. Net-benefit translation (statistically correct)
The future E3 report (and the E1 report + manuscript) must present, for the **registered 75th-pct h=4 primary** result at **p\*=0.30**:
- ΔNB(M5−M1) ≈ **+0.0188**;
- ≈ **1.9 additional net true-positive equivalents per 100 municipality-weeks**, under the harm–benefit trade-off encoded by p\*=0.30;
- equivalently, **holding true-positive detections fixed, ≈ 4.4 fewer false alerts per 100 municipality-weeks**;
- approximate **false-alert-equivalent CI: ≈ 2.7 to 6.1 fewer per 100**.
- **Required caveat:** *"These are decision-analytic equivalents conditional on the p\*=0.30 harm–benefit trade-off, not directly observed counts of alerts prevented or outbreaks detected."*
- These are **conditional on p\*/(1−p\*)**; **p\*=0.30 remains the registered primary threshold**; the translation belongs in the **E1 report and manuscript**, not only E3.
- For 80th/90th-pct outcomes, compute the same translation **only if** the corresponding ΔNB is stable; **do not compare transformed equivalents across percentiles without noting that event prevalence and outcome definitions differ**.

## 11. Interpretation rules
- ΔNB(M5−M1) positive with CI excluding 0 at 80th and/or 90th → **modest hybrid advantage robust to a rarer outbreak definition**.
- Positive at 80th but unstable/null at 90th → **robust for moderately rarer outbreaks, inconclusive for the rarest**.
- Advantage disappears → **gain applies mainly to above-usual activity, not rarer epidemic weeks**.
- AUC improves but ΔNB does not → **do not claim improved operational value**.
- PR-AUC/calibration deteriorate materially → **emphasize rarity-related limitations**.
- **Do not change the primary 75th-pct h=4 conclusion based on the sensitivity alone.**

## 12. Reporting-delay limitation (exact wording)
> "OpenDengue contains finalized rather than real-time surveillance counts. Under operational reporting delays, both the recent-surveillance and hybrid models may perform differently. The direction and magnitude of any change in their relative net benefit cannot be determined from the present data."
- **No reporting-delay analysis will be added now; no lower-bound claim will be made; this belongs in the manuscript Discussion; delay-vintage analysis is deferred** (requires real-time vintages or a separately pre-specified simulation).

## 13. Future quarantine outputs (NOT now)
Dir `~/data_quarantine/colombia_model_pilots/outbreak_threshold_sensitivity_v1/`:
- `colombia_outbreak_thresholds_v1.csv` · `colombia_outbreak_threshold_labels_v1.csv` · `colombia_outbreak_threshold_predictions_v1.csv` · `colombia_outbreak_threshold_metrics_v1.csv` · `colombia_outbreak_threshold_dca_v1.csv` · `colombia_outbreak_threshold_bootstrap_ci_v1.csv` · `colombia_outbreak_threshold_sensitivity_v1.meta.json`.
- **Do not overwrite** existing threshold, label, prediction, model-ladder, horizon, or E1 files.

## 14. Future safe repo files (after approval)
`scripts/colombia_outbreak_threshold_sensitivity_v1.py`, `docs/colombia_outbreak_threshold_sensitivity_report.md`.

## 15. Final analysis-freeze rule
After E3 is completed, reviewed, and committed: **freeze substantive analyses**; do **not** run E2, E4, or E5 before the initial manuscript draft; do **not** add new horizons, climate features, model classes, geographic validations, or outcome definitions; **begin manuscript preparation**; reserve further analyses for **documented reviewer requests or a separate paper**.

## 16. Confirmation
- **No E3 models run; no predictions generated; no metrics computed; no labels created in this step; no thresholds recomputed; no data modified; no quarantine outputs modified.**
- **Specification-only markdown memo; no data files staged or committed.**
