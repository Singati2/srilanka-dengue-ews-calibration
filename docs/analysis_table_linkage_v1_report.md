# Analysis Table Linkage v1 — Build & QC Report
*First outcome↔exposure↔population join for the Sri Lanka dengue EWS calibration project. Performed **locally**; the linked CSV and all inputs stay git-ignored in quarantine and are **NOT committed**. This is a **join/QC artifact only** — no models were run, and no calibration, AUC, decision-curve, or regression quantities were computed. Preregistration, frozen outcome, and frozen exposure are unchanged and not overwritten.*

**Date:** 2026-06-12

## Purpose
Create the first linked RDHS × epidemiological-week analysis table by joining the three frozen layers — dengue outcome, climate exposure, and population denominators — on verified spatial/temporal keys, with full provenance and missingness flags, in preparation for the (separate, approval-gated) existing-models calibration/decision-curve pilot.

## Frozen inputs — checksums re-verified at build
| Layer | File | Recorded SHA256 | Re-verify |
|---|---|---|---|
| Outcome | `wer_dengue_currentweek_rdhs_2018_2025_v2.0-frozen.csv` | `99f0b9b1…2626af3e99` | ✅ exact match |
| Exposure | `rdhs_weekly_climate_exposure_2018_2025_v2_boundary_resolved.csv` | `3900082b…8d572d81ee5d` | ✅ exact match |
| Population | `rdhs_population_worldpop_district_rescaled_2018_2025.csv` | `e4585741…0ba37d5d3a` | ✅ match (meta) |

No frozen file was modified or overwritten.

## Join keys (documented — no silent guessing)
- Outcome carries **no `geometry_id`**; it keys on `rdhs` name + `year` + `week`. The 26 RDHS **name sets are identical** across outcome, exposure, and population (exact spelling), and exposure's `rdhs_name → geometry_id` map is strictly 1:1 — so outcome names were mapped to `geometry_id` directly via that authoritative map (**0 unmapped**; no crosswalk-template fallback required).
- `geometry_id` sets are identical between exposure and population (26 = 26).
- **Backbone = frozen exposure grid** (417 ISO weeks × 26 RDHS = 10,842). Outcome joined on (`geometry_id`, year, week); population joined on (`geometry_id`, year). **No week-number remapping was applied.**

## ⚠ New finding: WER-vs-ISO 2021 week-numbering anomaly (held for decision)
While linking, the build surfaced a calendar discrepancy **not previously catalogued**:
- WER's 2021 weekly **issue labels run 1–42 then 44–53** (it skips a "43" and carries a "53"); ISO-2021 has only 52 weeks.
- Under a strict literal-key join this means:
  - **2021-W43** (present in the ISO/exposure calendar) has **no WER issue** → flagged `outcome_missing_flag=1`.
  - **2021-W53** — a real WER issue (`Vol_48_no_53.pdf`, **771 current-week cases**, all 26 RDHS, non-NA) — has **no matching exposure week**.
- To **lose nothing and remap nothing**, the linked table uses a **full outer join on literal keys**: the 26 WER-2021-W53 rows are **retained** with `exposure_missing_flag=1` and climate fields NA (visible and flagged, but excluded from climate-based modeling until aligned). This anomaly is **not resolved here by design** — choosing an alignment (e.g. WER-W53 ↔ ISO-W52) is a modeling-frame decision and is held for your explicit instruction.

The other issue-absent weeks are expected: **2020-W53** (ISO genuinely has 53 weeks; WER published no W53 issue) and **2022-W44** (WER issue genuinely absent from the public archive).

## Linked table (quarantined, NOT committed)
- `~/data_quarantine/analysis_tables/dengue_climate_population_linked_2018_2025_v1.csv`
- **SHA256:** `d892f62f2a8b24903b8e1fccd7c51342d3786ced25474f360ff32e36aab9a70a` · 3,018,109 bytes · **10,868 rows** · 32 cols · read-only.
- Row accounting: 10,842 exposure-backbone rows (climate complete) + 26 outcome-only rows (2021-W53).
- Sidecar metadata: `dengue_climate_population_linked_2018_2025_v1.meta.md`.

## Variables preserved
- **IDs:** rdhs_name, geometry_id, epi_year, epi_week, week_start, week_end
- **Outcome:** dengue_current_week_cases; dengue_cumulative_cases (QC only, **not for modeling**); wer_vol, source_pdf, extraction_flag, extraction_method
- **Climate:** t2m_mean_c, t2m_min_c, t2m_max_c, d2m_mean_c, rh_mean_percent, precip_sum_mm, precip_mean_daily_mm (+ provenance n_era5_hours, n_chirps_days, era5_qc_flag, chirps_qc_flag, source_version)
- **Population:** population_rescaled, population_worldpop_raw, rescale_method
- **Derived QC-only:** dengue_incidence_per_100k, outcome_missing_flag, outcome_issue_absent, exposure_missing_flag, population_missing_flag
- **No outbreak/label/model columns** — preregistration does not yet define an outbreak threshold, so none was created.

## QC results
| Check | Result |
|---|---|
| Rows | 10,868 (10,842 backbone + 26 outcome-only) ✅ |
| Distinct RDHS | 26 ✅ |
| Years | 2018–2025 ✅ |
| Duplicate (geometry_id, epi_year, epi_week) | 0 ✅ |
| **Exposure match rate** | 99.761% (10,842 climate-complete rows; 26 outcome-only NA per 2021 anomaly) ✅ |
| **Outcome match rate** | 98.979% (111 missing) ✅ |
| **Population match rate** | 100.000% ✅ |
| Incidence nonnegative where outcome observed | ✅ (range 0–809.2 /100k) |
| Incidence NA where outcome missing | ✅ |
| population_rescaled > 0 (all) | ✅ |
| Climate nulls on backbone | 0 ✅ |
| n_era5_hours = 168 / n_chirps_days = 7 on backbone | ✅ |
| RH 0–100 / dewpoint ≤ temperature | ✅ |
| Fully-modelable rows (all three flags = 0) | 10,731 |
| Model-derived columns present | **NONE** ✅ |

### Missingness summary (111 outcome-missing rows)
- **78 issue-absent** = 3 weeks × 26 RDHS: 2020-W53, 2021-W43, 2022-W44.
- **33 present-but-NA cells** (verified, flagged not dropped): Gampaha 2018 wk23–52 (30); Puttalam 2019 wk23, 2021 wk45, 2021 wk50 (3).
- **26 outcome-only rows** retained for WER-2021-W53 (771 cases) pending the alignment decision above.
- Exposure: 0 unexpected missing on the backbone. Population: 0 missing.

## Confirmations
- **No models were run**; no AUC, calibration, decision-curve, or regression quantities computed. `dengue_incidence_per_100k` is a descriptive QC field only.
- **No outbreak labels** created (none defined in preregistration yet).
- Frozen outcome, frozen exposure, and population denominators were **read-only, unmodified, and not overwritten**; checksums re-verified.
- The linked CSV and all inputs remain **quarantined under `~/data_quarantine/`**; only this markdown report is proposed for commit.
- Preregistration unchanged.

## Next step (separate, approval-gated)
1. **Resolve the WER-2021 week-numbering anomaly** (alignment decision) before any modeling that uses 2021.
2. Then the **existing-models calibration / decision-curve pilot** per `preregistration_analysis_plan_v1.md` (calibration, recalibration, net-benefit/DCA, spatial decision-support) on the fully-modelable rows. Nothing models until directed.
