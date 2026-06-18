# Colombia Outbreak-Label Specification (memo only — NO labels created)
*Defines the outbreak labels and temporal split for the Colombia external framework-replication arm. **Specification only: no labels, no lag features, no models, no metrics, no external validation, no data files created or committed.** Mirrors the Sri Lanka evaluation framework while respecting Colombia's OpenDengue data structure.*

**Date:** 2026-06-18 · **Status:** specification only · **Base commit:** 0802942 · **Builds on:** `docs/colombia_chirps_full_precipitation_report.md`, `docs/colombia_era5_full_temperature_report.md`, `docs/colombia_manual_alias_crosswalk_report.md`.

## 1. Purpose
- Define outbreak labels for the Colombia external **framework-replication** arm (replication of the decision-evaluation framework, not transfer of Sri Lanka coefficients).
- Preserve a **strict no-leakage** design: all thresholds estimated on training weeks only.
- Match the Sri Lanka framework where possible (per-unit 75th-pct train-only label, h=4 primary) while respecting Colombia's unbalanced weekly Admin2 panel.
- **This is a specification only; no labels are created in this step.**

## 2. Analysis population
- **Primary spatial unit:** OpenDengue Colombia Admin2 (department+municipality) mapped to **GADM `GID_2`** via the finalized crosswalk (1,065 primary polygons).
- **Primary rows must have:** valid weekly `dengue_total`; valid `GID_2`; linked CHIRPS precipitation; linked ERA5-Land temperature.
- **Primary climate-linked rows (from prior reports):** **198,266** OpenDengue rows linked to **both** CHIRPS + ERA5 (99.4%).
- **Excluded from primary (audited, not silently dropped):**
  - **5 newly-created municipalities** absent from GADM v4.1 (Tuchín, Albania–La Guajira, Norosí, Guachené, San José de Uré) — 763 rows, flagged `excluded_newly_created`.
  - **Island rows without climate linkage** — San Andrés (`COL.27.2_2`) and Providencia (`COL.27.3_2`), 429 rows, land-masked out of CHIRPS/ERA5.
- All exclusions recorded with counts in the later construction report.

### 2a. **Outcome-grid decision (MUST resolve before labels) — absent municipality-weeks**
OpenDengue is an **unbalanced panel** (98–415 reporting municipalities/week of 1,065). A horizon-*h* label needs the outcome at week *t+h* to exist, but many *t* rows have no *t+h* row.
- **Primary rule (pre-specified here):** **do NOT assume an absent municipality-week = 0 cases.** Define `label_h` only where the *t+h* outcome row **genuinely exists** in OpenDengue; rows whose *t+h* outcome is absent have **undefined `label_h`** and are excluded from that horizon's labelable set (counted, not silently dropped).
- **Sensitivity (pre-registered, not primary):** "panel completion" — treat absent municipality-weeks as 0 reported cases, yielding a balanced grid; report how prevalence/label counts change. Justification: absent ≠ confirmed zero (could be non-reporting), so panel completion is a sensitivity, not the primary.
- The later construction report must state, per horizon, the **labelable-row count** after this rule (expected < 198,266).

## 3. Time span and split
- **Span (from prior reports):** weekly Admin2 **2006-12-31 → 2022-12-25** (835 weeks; +8 warm-up weeks already in the climate table).
- **Honest temporal split (pre-specified):**
  - **Train:** 2006-12-31 → 2017-12-31
  - **Validation/tuning (if needed):** 2018-01-01 → 2019-12-31
  - **Test:** 2020-01-01 → 2022-12-25
- All outbreak thresholds estimated on **training weeks only**.
- **If the distribution makes the split problematic, report it — do not change the split without approval.**

### 3a. **Flagged validity threat — COVID-era test window (report, do not change split unapproved)**
The test window **2020–2022 overlaps the COVID-19 pandemic**, which disrupted dengue surveillance/reporting and dynamics, and follows Colombia's **large 2019 epidemic** (in the validation block). Risk: test-period net-benefit/calibration could reflect **pandemic reporting artifacts**, not climate-EWS value.
- **Required in the construction step:** a **2020–2022 reporting-continuity check** (municipalities reporting/week, total weekly cases vs 2014–2019 baseline) to quantify disruption.
- **Gated options (await approval; do NOT auto-apply):** (i) keep the split and report COVID as an explicit caveat; (ii) use a pre-COVID test window (e.g., test 2017–2019, train earlier); (iii) report both. **No split change without your sign-off.**

## 4. Primary label
- **Outcome:** future outbreak indicator from a **train-only, municipality-specific count threshold**.
- **Threshold:** the **75th percentile of weekly `dengue_total` within each `GID_2`, computed on training weeks only**.
- **Definition (horizon h):** `label_h = 1` if `dengue_total` at week **t+h** is **strictly greater than** that `GID_2`'s train-only 75th-percentile threshold; else `label_h = 0`. (Undefined where the t+h outcome is absent, per §2a.)
- **Primary horizon:** **h = 4 weeks** (matches Sri Lanka).
- **Secondary horizons:** h = 1, 2, 8, 12 weeks.
- **Note (base rate):** a 75th-pct threshold labels ~25% of a unit's threshold-period weeks as outbreaks — a high base rate by construction (kept for SL comparability; the 90th-pct sensitivity addresses rarer events).
- **No labels are computed in this memo.**

## 5. Sensitivity labels (not implemented now)
- **90th-percentile** train-only municipality-specific count threshold (rarer-event variant).
- **Pooled department-level (Admin1) threshold** — only if many municipalities have too few nonzero training weeks for a stable per-unit threshold.
- **Incidence-based threshold** (per-100k) — only if reliable **DANE** municipal denominators are later linked (count-based remains primary; incidence stays optional, consistent with prior reports).
- **Panel-completion (absent=0)** variant, per §2a.

## 6. No-leakage rules
- Percentile thresholds computed **only on training-period weeks**; no validation/test outcome can influence any threshold.
- **Do NOT use the full 2006–2022 distribution** to define thresholds.
- Climate **lags use only information at or before the prediction week t**; the future outcome at t+h is used **only** as the label.
- Any rolling recalibration or threshold tuning uses **only pre-test** information.
- Train/validation/test boundaries are by `week_start` date; a row belongs to the period containing week **t** (the prediction week), and thresholds derive from train **t+h** outcomes only within the train period.

## 7. Handling sparse / low-incidence municipalities
- Per `GID_2`, report: training weeks, nonzero training weeks, threshold value, and event prevalence (train and by split).
- **Predefined flags:**
  - `< 52` training weeks
  - `< 10` nonzero training weeks
  - 75th-pct threshold `== 0` (degenerate: any case ≥ 1 becomes an "outbreak")
  - event prevalence `< 1%` or `> 80%`
- If **many** municipalities hit threshold=0 or unstable flags, **recommend review before construction** (do not silently exclude).
- Low-incidence units are **reported**, not silently dropped.

## 8. Climate lag / feature-readiness rules
- Climate panel is **lag-ready**; **no modeling features created in this step.**
- Future feature table to support **lags 0–8 weeks** for: weekly **CHIRPS precipitation sum** and weekly **ERA5-Land temperature mean**.
- **Lag k at prediction week t uses climate from week t−k.**
- Rows lacking full lag history are **flagged by lag availability**, never silently imputed.
- The 8 warm-up weeks already in the climate table (grid start 2006-11-05) support lag-8 from the first study week.

## 9. Output files to create later (NOT now)
Future quarantine outputs (dir `~/data_quarantine/colombia_label_features_v1/`):
- `colombia_label_thresholds_train_only_v1.csv`
- `colombia_labels_h1_h2_h4_h8_h12_v1.csv`
- `colombia_lag_feature_availability_v1.csv`
- `colombia_label_specification_v1.meta.json`

Future safe repo report: `docs/colombia_label_construction_report.md`.

## 10. Quality checks required later
- Threshold distribution by municipality.
- Event prevalence by horizon.
- Event prevalence by year (incl. the COVID 2020–2022 check, §3a).
- Missingness / exclusion counts (incl. labelable-row count after §2a).
- Lag-availability counts.
- Train vs validation vs test event-rate comparison.
- Explicit confirmation of **no leakage**.
- Explicit confirmation that **no labels were created from full-period percentiles**.

## 11. Stop rules for the later label-construction step
Stop and report (await approval) if:
- The required climate-linked table is missing.
- `GID_2` × `week_start` keys are unexpectedly duplicated.
- **> 10%** of primary rows lack climate linkage.
- **Many** municipalities have degenerate threshold=0 labels.
- Event prevalence at the primary **h=4 / 75th-pct** label is **too rare** for evaluation (e.g., overall positive rate near 0).
- The temporal split cannot be applied cleanly (e.g., a period has near-zero usable rows).
- The §2a labelable-row count collapses (e.g., the unbalanced panel leaves too few defined h=4 labels).
- **Report and ask for approval before changing any label definition.**

## 12. Confirmation
- **No labels created.**
- **No lag features created.**
- **No models run.**
- **No metrics computed** (no AUC/PR-AUC/calibration/DCA/net-benefit/ΔNB/regression/forecast).
- **No external validation performed.**
- **No data files created or committed.**
- No Sri Lanka frozen data or prior outputs modified.
- **This is a specification-only markdown commit candidate** (pending your approval).
