# Analysis Table Linkage v2 — Date-Aligned (Primary) — Build & QC Report
*Primary date-aligned outcome↔exposure↔population join, built **locally**. The linked CSV, the issue-date alignment table, and all inputs stay git-ignored in quarantine and are **NOT committed**. This is a **join/QC artifact only** — no models were run, and no outbreak labels, AUC, calibration, decision-curve, regression, or forecast quantities were computed. Frozen outcome, exposure, population, and the v1 linked table are unchanged and not overwritten. Preregistration unchanged.*

**Date:** 2026-06-12

## Why v2 supersedes v1 for primary modeling
The calendar decision memo (`docs/wer_2021_calendar_anomaly_decision_memo.md`) established that the frozen outcome's stored `week` is the **WER issue number**, which is offset from the true ISO climate week by a **year-varying** amount (+1 in most years, +2 in 2021). The v1 literal-week join (`outcome.week == exposure.epi_week`) therefore pairs each dengue observation with climate from 1–2 ISO weeks later — invalid for a climate-lag EWS. **v2 joins on the date-derived ISO week**, so dengue and climate refer to the same calendar week. v1 is retained only as a sensitivity/audit artifact (S1).

## Date-alignment method
For all 415 WER issues (2018–2025) we extracted, from the PDF text layer (`pdftotext -layout`; **no OCR**): the **returns-cutoff date** ("returns received on or before …"), the **surveillance-range end date** ("… reported (dd–dd Mon yyyy)"), and the **stated epi-week** ("(Nth Week)"). The robust derivation of ISO (year, week):
1. returns-cutoff and surveillance-end **agree** → use that date's ISO week (`date_consensus`).
2. a present date's week **matches** the spine `iso_week = epiweek − c[year]` → use that date, giving the correct boundary year (`date_confirmed`).
3. dates disagree or share a month typo → trust the **date-calibrated epiweek spine** (`epiweek_spine_typo_recovered`).
4. year-boundary first issues → date-based prior-year assignment (`BOUNDARY_TYPO_REVIEW` / `date_only_no_epiweek`; all manually verified).

`c[year]` = mode over typo-free issues of (epiweek − ISO week) = **0 for every year except 2021 (= +1)**. Failure mode handled: several WER PDFs contain **month typos** in their date lines (e.g. 2024 no_06 prints "02 Jan" for the "(05th Week)"; 2024 no_41 "Sep" vs the correct "Oct"); the clean "(Nth Week)" integer plus the per-year offset recover these. The derived mapping is **strictly monotonic (0 bad steps)** and **collision-free (0 ISO weeks claimed by >1 issue)**.

### Input checksums (re-verified at build; read-only, unmodified)
| Layer | SHA256 | Verify |
|---|---|---|
| Outcome | `99f0b9b1…2626af3e99` | ✅ |
| Exposure | `3900082b…8d572d81ee5d` | ✅ |
| Population | `e4585741…0ba37d5d3a` | ✅ |

### Issue-date extraction summary
- 415 issues processed; **returns-cutoff date 410/415 (98.8%)**, stated epi-week **415/415 (100%)**, **date-derived ISO 415/415 (100%)**.
- Flags: `date_consensus` 358, `date_confirmed` 48 (→ 406/415 = 97.8% date-direct), `epiweek_spine_typo_recovered` 5, `BOUNDARY_TYPO_REVIEW` 3, `date_only_no_epiweek` 1. 0 unresolved, 0 collisions.
- Issue-level alignment table (quarantined): `wer_issue_date_alignment_2018_2025_v1.csv`, sha256 `7c06bbff…`.

## Duplicate 2021 no_53 handling
**Excluded from the primary table** — 26 rows, **771 current-week cases**. Reason: `Vol_48_no_53.pdf` is a verbatim re-issue of no_52 (identical returns-cutoff 17 Dec 2021, byte-identical 26-RDHS counts, identical cumulative 25,084). It contains no new dengue data; its nominal ISO week (2021-W51) is therefore documented missing.

## Missing-issue handling (no imputation)
Four backbone ISO weeks have no outcome after date alignment, all documented:
- **2021-W41** — skipped issue no_43 (publication gap; genuinely unreported).
- **2021-W51** — only the dropped duplicate no_53 mapped here; genuinely unreported.
- **2022-W43** — missing issue no_44 (genuinely absent from the public archive; the v1/stored-week "2022-W44").
- **2025-W52** — boundary: the surveillance week whose issue is published in early Jan 2026 (outside the data window).

## Row count & checksum
- **10,868 rows** (10,842 exposure backbone + 26 outcome-only pre-study rows: 2018 issue no_01 → ISO **2017-W52**, flagged `exposure_missing_flag=1`).
- **SHA256:** `3a197d610fde721ffdf2be6388df88fea675a5b49bf131a0919fd89ec2518e91` · 37 cols · read-only.
- Sidecar metadata: `dengue_climate_population_linked_2018_2025_v2_date_aligned.meta.md`.

## QC summary
| Check | Result |
|---|---|
| Rows | 10,868 ✅ |
| Distinct RDHS | 26 ✅ |
| Years | 2018–2025 backbone (+26 pre-study 2017-W52 rows) ✅ |
| Duplicate (geometry_id, epi_year, epi_week) | 0 ✅ |
| Exposure match rate | 99.761% ✅ |
| Outcome match rate | 98.739% (137 missing = 104 issue-absent [4 wks×26] + 33 documented NA cells) ✅ |
| Population match rate | 99.761% (only the 26 pre-study 2017 rows lack a denominator) ✅ |
| 2021 no_53 counted as a new week | **No** — excluded ✅ |
| 2021 missing issue no_43 | documented missing (2021-W41) ✅ |
| 2022 missing issue no_44 | documented missing (2022-W43) ✅ |
| Known present-but-NA cells preserved | 33 (Gampaha 2018 →ISO wk22–51; Puttalam 2019-W22, 2021-W43, 2021-W48) ✅ |
| Incidence nonnegative where observed | ✅ (0–812.7 /100k; NaN where outcome/pop absent) |
| Climate nulls on exposure backbone | 0; n_era5=168 & n_chirps=7 all ✅ |
| population_rescaled > 0 and complete (backbone) | ✅ |
| Fully-modelable rows (all three flags 0) | 10,705 |
| Model-derived columns | **NONE** ✅ |

The 33 NA cells move to their date-derived ISO weeks (e.g. Gampaha 2018 stored wk23–52 → ISO wk22–51) and remain NA and flagged — not imputed.

## Confirmations
- **No models were run**; no outbreak labels, AUC, calibration, decision curves, regressions, or forecasts. `dengue_incidence_per_100k` is a descriptive QC field only.
- Frozen outcome, exposure, population, and the v1 linked table were **read-only, unmodified, not overwritten**; input checksums re-verified.
- The v2 linked CSV, the issue-date alignment table, and all inputs remain **quarantined under `~/data_quarantine/`**; only this markdown report is proposed for commit.
- Preregistration unchanged.

## Next steps (separate, approval-gated)
1. Fold the primary date-aligned rule + sensitivity analyses (**S1** naive week-number = v1; **S2** climate-lag sweep 0–8 wk; **S3** drop 2021 tail) into `preregistration_analysis_plan_v1.md`.
2. Existing-models calibration / decision-curve pilot on the 10,705 fully-modelable rows. Nothing models until directed.
