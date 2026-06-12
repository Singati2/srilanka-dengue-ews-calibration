# Decision Memo — WER-vs-ISO 2021 Calendar Anomaly (and a study-wide alignment finding)
*Investigation and recommended modeling-frame rule. **No models were run; no outbreak labels, AUC, calibration, decision-curve, regression, or forecast were computed.** No frozen outcome/exposure/population/linked files were modified or overwritten. No data files (PDFs, CSVs, climate rasters, linked tables) are committed — only this markdown memo.*

**Date:** 2026-06-12 · **Status:** decision support only — **no remapping applied.**

## 1. Problem statement
The linkage v1 report flagged a 2021 week-numbering mismatch: WER 2021 issue labels run 1–42 then 44–53 (no "43"), while ISO-2021 has 52 weeks; 2021-W43 has climate exposure but no WER outcome, and WER-2021-W53 (771 cases) has outcome but no exposure. This memo investigates the WER PDFs to determine the cause and recommend a rule **before any modeling**. The investigation resolved the 2021 case **and** surfaced a larger, study-wide temporal-alignment issue.

## 2. Evidence from the frozen outcome table
- 2021 contains exactly **52 issues**: weeks **1–42 and 44–53** (issue "43" absent); `vol`=48 throughout.
- **2021-W52 and 2021-W53 are byte-identical across all 26 RDHS** in *both* `dengue_current_week` (771 each) **and** `dengue_cumulative` (25,084 each). A genuinely later week would raise the cumulative; identical cumulative ⇒ **no new data** in W53.
- 33 documented NA cells and the genuinely-missing 2022 issue are unrelated to this anomaly.

## 3. Evidence from WER PDF dates/metadata (text layer, `pdftotext -layout`; no OCR)
Every 2021 WER issue states its surveillance week explicitly: header publication range (top-right), a "Summary of … diseases reported (dd–dd Mon yyyy) (Nth Week)" line, and a "returns received on or before dd Mon yyyy" cutoff.

- **Issue number = WER epi-week + 1**, consistently (e.g. no_42 → "41st Week"; no_44 → "43rd Week"; no_53 → "52nd Week"). Verified for all 2021 issues 38–53 and spot-checked in 2019/2020/2022/2023/2024.
- **Issue 43 was never published.** no_42 closes returns 08 Oct (ISO wk 40); no_44 closes 22 Oct (ISO wk 42). The intervening week — returns ~15 Oct, **ISO wk 41** — has no issue. That single surveillance week's dengue data is **genuinely missing** (a publication gap, exactly like the 2022 missing issue).
- **Issue 53 duplicates issue 52.** no_53's "returns received on or before" date is **17 Dec 2021 — identical to no_52** (no_53's masthead claims 25–31 Dec, but its actual data cutoff equals no_52's). This confirms no_53 republished no_52's dengue table verbatim.

### 3.1 Study-wide finding: the stored `week` label ≠ the ISO climate week
The climate exposure is built on **ISO weeks** (real Monday–Sunday `week_start`/`week_end`). The outcome's stored `week` is the **WER issue number**. Because (a) issue N reports the week whose returns just closed (≈ −1) and (b) WER epi-weeks run **Saturday–Friday** vs ISO Monday–Sunday (another ≈ −1), the stored label sits **ahead of the true ISO surveillance week — by +1 ISO week in most years and +2 in 2021** (2021's issue stream is inflated by one earlier in the year). The current linkage v1 join (`outcome.week == exposure.epi_week`) therefore pairs each dengue observation with climate from **1–2 ISO weeks later**, and the offset is **not constant across years**. → **Week-number equality is an invalid join key for a climate-lag analysis; alignment must be by date.**

## 4. Alignment table (2021, issues 38–53)
"ISO week by date" = ISO week of the returns-cutoff / surveillance-end date extracted from the PDF.

| WER label (stored week) | source_pdf | returns cutoff | WER epi-week (stated) | ISO week by date | dengue current-week total | offset (stored − ISO) | alignment status |
|---|---|---|---|---|---|---|---|
| 38 | Vol_48_no_38 | 10 Sep | 37 | 36 | 162 | +2 | ok (re-align by date) |
| 39 | Vol_48_no_39 | 17 Sep | 38 | 37 | 203 | +2 | ok |
| 40 | Vol_48_no_40 | 24 Sep | 39 | 38 | 215 | +2 | ok |
| 41 | Vol_48_no_41 | 01 Oct | 40 | 39 | 190 | +2 | ok |
| 42 | Vol_48_no_42 | 08 Oct | 41 | 40 | 271 | +2 | ok |
| **43** | **— (never published)** | — | (42) | **41** | **— (missing)** | — | **genuinely missing week** |
| 44 | Vol_48_no_44 | 22 Oct | 43 | 42 | 241 | +2 | ok |
| 45 | Vol_48_no_45 | 29 Oct | 44 | 43 | 523 | +2 | ok |
| 46 | Vol_48_no_46 | 05 Nov | 45 | 44 | 261 | +2 | ok |
| 47 | Vol_48_no_47 | 12 Nov | 46 | 45 | 314 | +2 | ok |
| 48 | Vol_48_no_48 | 19 Nov | 47 | 46 | 369 | +2 | ok |
| 49 | Vol_48_no_49 | 26 Nov | 48 | 47 | 446 | +2 | ok |
| 50 | Vol_48_no_50 | 03 Dec | 49 | 48 | 982 | +2 | ok |
| 51 | Vol_48_no_51 | 10 Dec | 50 | 49 | 634 | +2 | ok |
| 52 | Vol_48_no_52 | 17 Dec | 51 | 50 | 771 | +2 | ok |
| **53** | **Vol_48_no_53** | **17 Dec (same as 52)** | 52 (masthead) | 51→**dup of 50** | 771 | +2 | **verbatim duplicate of issue 52** |

## 5. Exact unmatched weeks, rows, and cases (linked table v1)
- **2021-W43 (stored):** exposure present, outcome absent → **26 rows** `outcome_missing_flag=1`. Cause: never-published issue 43 (true ISO-wk-41 gap).
- **2021-W53 (stored):** outcome present, exposure absent → **26 rows** `exposure_missing_flag=1`, **771 cases**. Cause: verbatim duplicate of issue 52 — **not a real epi-week**. Keeping it alongside W52 would **double-count 771 cases**.
- Net for 2021: the linked table already isolates these as flagged rows; no other 2021 week is affected.

## 6. Most likely explanation
**Option A + a duplicate** (not a simple typo, not unresolvable):
- **2021-W43** = a **true missing WER issue** (publication gap; one ISO surveillance week genuinely unreported) — same class as the 2022 missing issue.
- **2021-W53** = a **duplicate re-issue** of issue 52 (data-integrity artifact), confirmed by identical returns cutoff, byte-identical district counts, and identical cumulative.
- Incidentally established: the stored `week` is the WER **issue number**, which is offset from the ISO week by **+1 (typical) to +2 (2021)** — a study-wide alignment defect in the *join rule* (the frozen data themselves are correct).

## 7. Options considered
1. **Complete-case primary modeling, week-number join kept.** Drop the W53 duplicate, treat W43 as missing, keep `week==epi_week`. Simplest, but **inherits the 1–2-week, year-varying climate↔outcome misalignment** — unacceptable for a climate-*lag* EWS.
2. **Date-reconciled alignment (re-link by date).** Map each WER issue to the ISO climate week by `returns-cutoff`/`week_end` overlap, applied uniformly to all years. The PDF dates **clearly and unambiguously support this**. Resolves 2021 as a special case (W53 collapses onto issue 52's ISO week and is dropped; the W43 gap becomes ISO-wk-41 missing) and fixes the global offset.
3. **Exclude 2021 weeks 43–53 entirely.** Clean but discards ~10 real weeks during a high-incidence period (Dec 2021 totals 600–980/wk); use only as sensitivity, not primary.
4. **Treat as unresolved archive anomaly.** Not warranted — the dates resolve it.

## 8. Recommendation
**PRIMARY RULE — adopt date-based alignment as the canonical outcome↔exposure join for the whole study (Option 2).** Concretely, in a *separate, approval-gated* re-linkage (linked table **v2**):
1. Derive each WER issue's true ISO week from its **returns-cutoff date** (`week_end`/Friday), not its issue number.
2. **Drop issue no_53** as a confirmed duplicate of no_52 (prevents double-counting 771 cases).
3. Treat the **never-published issue 43 (ISO wk 41, 2021)** as documented missing outcome — no imputation, flagged like the 2022 gap.
4. Join on the date-derived ISO week, so dengue and climate refer to the **same calendar week** in every year; then **complete-case** modeling on weeks where both layers exist.
- The frozen outcome, exposure, and population tables are **correct and unchanged** — only the *join key* changes (issue-number → date-derived ISO week). This is a linkage-layer fix, not a re-freeze of inputs.

**SENSITIVITY ANALYSES (preregister alongside the primary):**
- **S1 — Naive week-number alignment:** re-run with `week==epi_week` to quantify how much the 1–2-week offset moves calibration/decision-curve results.
- **S2 — Lag sweep:** fit the date-aligned model at climate lags of 0–8 weeks; the offset finding makes the lag structure a primary robustness axis, not an afterthought.
- **S3 — Drop-2021-tail:** exclude 2021 ISO weeks 41–52 to confirm conclusions are not driven by the anomalous tail.

**ONE CHEAP VERIFICATION BEFORE EXECUTING v2 (recommended, not blocking this memo):** visually confirm on one PDF that the **front-page dengue district table** shares the issue's reporting week (this memo established the week from the communicable-disease returns line, which governs the whole issue; standard WER format ties the dengue table to the same week), and audit early-2021 issues to locate the source of the extra +1 numbering drift. Neither changes the recommendation; both increase confidence.

## 9. Statements
- **No models were run**; no outbreak labels, AUC, calibration, decision curves, regressions, or forecasts were computed.
- **No frozen files were modified or overwritten** (outcome `99f0b9b1…`, exposure `3900082b…`, population `e4585741…`, linked v1 `d892f62f…` all untouched and read-only).
- **No linked CSV, PDF, climate file, raster, or quarantined data was committed** — only this markdown memo is proposed for commit.
- **No remapping was applied.** This memo supports a decision; execution (linked table v2) is a separate, approval-gated step.
- Preregistration unchanged; the proposed primary rule and S1–S3 are offered for incorporation into the analysis plan **upon your decision**.
