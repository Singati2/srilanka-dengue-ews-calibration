# Colombia Outbreak-Label Construction Report (COMPLETED — labels built; NO models)
*Executed per `docs/colombia_label_specification.md`. The one triggered stop-rule (duplicate `GID_2 × week_start`) was resolved by **approved Option 1 (aggregate-sum onto the shared polygon `COL.28.78_2`)**; all other checks passed and the full label set was built. **No models, no metrics (AUC/PR-AUC/calibration/DCA/net-benefit/ΔNB), no external validation.** Generated label/diagnostic data are quarantined; only this report + the construction script are committed.*

**Date:** 2026-06-18 · **Status:** completed · **Base commit:** 9fdbbbe · **Spec:** `docs/colombia_label_specification.md`.

## 1. Input (read-only) + checksum
- `~/data_quarantine/colombia_climate_linkage_full_v1/colombia_opendengue_climate_linked_with_temp_v1.csv` — SHA256 `248bb73a11e8e433e3ce45e8d5e3e535f6864c6b5198eb1e02aad080f6e5ee5a` (199,458 OD rows).
- Reproducible script (committed): `scripts/colombia_label_construction_v1.py`.

## 2. Crosswalk-resolution applied (approved Option 1)
- **Issue:** GID_2 `COL.28.78_2` (Socorro, Santander) carried two OpenDengue municipalities — `SOCORRO` and `PALMAS SOCORRO` (Palmas del Socorro, split from Socorro in 1996; GADM has a separate polygon `COL.28.59_2` that is not in the climate panel).
- **Resolution (approved):** **aggregate-sum** `dengue_total` for both onto the shared polygon `COL.28.78_2` (climate identical within the polygon). **71 rows folded**; all 87 Palmas del Socorro cases retained. This is a **crosswalk-resolution step, not a label-definition change**, documented here and in `colombia_label_specification_v1.meta.json`.
- Effect: unique `(GID_2, week)` panel of **198,195 rows across 1,063 units** (Palmas del Socorro folded into Socorro's polygon).

## 3. Analysis population & exclusions (audited)
- Primary climate-linked rows: **198,266** → unique-keyed panel **198,195** (after the 71-row Option-1 fold).
- Excluded (recorded, not silently dropped): 763 newly-created-municipality rows; 429 island rows (San Andrés/Providencia, land-masked from CHIRPS/ERA5).

## 4. Train/validation/test split (as committed)
- Train 2006-12-31→2017-12-31: **135,468** rows · Val 2018-01-01→2019-12-31: **27,224** · Test 2020-01-01→2022-12-25: **35,503**. Split applied cleanly.

## 5. Thresholds (train-only)
- Per-GID_2 75th + 90th percentile of weekly `dengue_total`, **training weeks only** (no validation/test, no full-period distribution).
- **threshold-75 == 0: 0 of 1,051 units (0.0%)** — non-degenerate.
- **Sparse flags (reported, not dropped):** <52 training weeks: **435 units (41%)**; <10 nonzero training weeks: **187 units**. (Reflects the unbalanced panel; these units' thresholds are less stable — flagged per-unit in the thresholds file.)

## 6. Labels (strictly-greater; absent t+h → undefined, per §2a)
| h | labelable rows | % of panel | prev train | prev val | prev test |
|---|---|---|---|---|---|
| 1 | 132,303 | 66.8% | 0.265 | 0.407 | 0.313 |
| 2 | 130,500 | 65.8% | 0.263 | 0.409 | 0.310 |
| **4 (primary)** | **127,703** | **64.4%** | **0.259** | **0.414** | **0.300** |
| 8 | 123,189 | 62.2% | 0.250 | 0.418 | 0.279 |
| 12 | 119,085 | 60.1% | 0.242 | 0.418 | 0.264 |
- ~35% of rows lack a t+h outcome (unbalanced panel) — excluded from that horizon's labelable set per the no-assume-zero rule; **not** imputed. h=4 prevalence ~0.26–0.41 (not rare).

## 7. COVID-era continuity (2020–2022) — no collapse
| Year | rows | reporting units | total cases |
|---|---|---|---|
| 2018 | 9,698 | 708 | 44,574 |
| 2019 | 17,526 | 836 | 125,409 (epidemic) |
| 2020 | 13,328 | 781 | 73,823 |
| 2021 | 9,801 | 730 | 49,889 |
| 2022 | 12,374 | 744 | 66,391 |
- Reporting **continued** through 2020–2022 (730–781 units vs 708–836 in 2018–2019) — normal post-epidemic cyclicity, not a reporting outage. COVID concern **mitigated**; remains a test-period interpretation caveat. **Split unchanged** (no approval to change it).

## 8. Lag 0–8 availability (diagnostics only — no feature values created)
- A lag-k value at week t requires a panel row at `(GID_2, t−k)`; panel rows carry both precip+temp, so precip- and temp-lag availability are identical.
- **Full lag-0–8 (both vars) available: 63,055 rows (31.8%)** — train 42,096 / val 9,837 / test 11,122.
- **Modelable h=4 (label defined AND full lag-0–8): 58,128 rows** — train 39,063 / val 9,255 / test 9,810.
- **Key constraint for modeling:** the unbalanced panel limits the lag-rich modelable set to ~58k municipality-weeks (still substantial: 1,063 units, ~39k train). Rows without full lag history are **flagged, not imputed.**

## 9. Stop-rule assessment (final)
| Stop rule | Status |
|---|---|
| Duplicate `GID_2 × week_start` | **RESOLVED** (approved Option 1 aggregation) |
| >10% rows lack climate linkage | PASS (0.6%) |
| Many threshold-75 == 0 | PASS (0.0%) |
| h=4 prevalence too rare | PASS (test 0.30) |
| Labelable-row collapse | PASS (h4 64.4%) |
| Split not cleanly applicable | PASS |
| COVID reporting severely disrupted | PASS (no collapse) |

## 10. Output files (quarantine, read-only; NOT committed) + SHA256 (16-char) / size
- `colombia_label_thresholds_train_only_v1.csv` — `23710e8cf82a1472…` — 74,722 B (per-GID_2 thresholds + flags + h4 prevalence)
- `colombia_labels_h1_h2_h4_h8_h12_v1.csv` — `bd37e68ab37eeabb…` — 12,270,801 B (198,195 rows; labels h1/h2/h4/h8/h12)
- `colombia_lag_feature_availability_v1.csv` — `8ead2e7c1ae4a9af…` — 33,569,059 B (lag0–8 availability + modelable flags)
- `colombia_label_construction_diagnostics_v1.csv` — `6be7f414211de462…` — 2,473 B (by-year/horizon/split tidy diagnostics)
- `colombia_label_specification_v1.meta.json` — `559513435525a428…` — 2,371 B (spec, aggregation note, split, thresholds, checksums)
- All under `~/data_quarantine/colombia_label_features_v1/`, chmod 444.

## 11. Confirmations
- **No models, no metrics, no external validation** — labels + diagnostics only.
- **No-leakage:** thresholds from training weeks only; never the full 2006–2022 distribution; t+h used only as the label.
- No Sri Lanka data or prior climate-linkage outputs modified (input read-only).
- **Generated label/diagnostic data kept out of git** (quarantine only); only this report + `scripts/colombia_label_construction_v1.py` are committed.

## 12. Next gate (separate)
Lag-feature assembly (values, not just availability) → then model fitting + calibration/DCA/net-benefit evaluation — **all gated and not started.** The modelable h=4 set (~58k rows, 1,063 units) is the basis for the eventual evaluation.
