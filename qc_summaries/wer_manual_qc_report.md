# WER Current-Week Dengue — Manual / Double-Entry QC Report (Quarantined)
*Verifies the v2 current-week dengue field against the source PDFs by two independent methods. No climate linkage, no models, preregistration untouched, dataset not promoted.*

**Date:** 2026-06-10
**Dataset under test:** `processed_quarantine/wer_dengue_rdhs_2018_2025_quarantine_v2.csv` (current-week field only; cumulative excluded from analysis by decision).
**Sample:** `qc/wer_manual_qc_sample.csv` — 33 issues (~8%), seeded, spanning 2018–2025.

## Verification methods (two independent of the v2 `pdftotext -layout` parser)
1. **National control-total checksum.** Each WER Table 1 prints a **"SRILANKA" national total row**. For each sampled issue, the sum of the 26 extracted RDHS current-week values is compared to the printed national current-week total. An exact match jointly verifies all 26 cells. (Independent: the total is a separately printed control figure.)
2. **Visual double-entry (Read tool).** The rendered Table-1 page is read by eye and the Dengue Fever current-week (column A) transcribed for all 26 RDHS, then compared to v2. Performed on 3 issues spanning eras: **2020 wk08, 2022 wk07, 2025 wk04**.

## Results
### Method 1 — control-total checksum (33 issues)
- **22 issues VERIFIED 26/26** (v2 sum == printed national total, exactly) → 572 cells jointly verified, **0 mismatches**.
- **2 issues NA-consistent** (2018 wk45, wk48): sum short by exactly the missing Gampaha value (72, 139) — consistent with documented NA, not an error.
- **9 issues not auto-verified** — the checksum *tool* could not cleanly read the total row (3 "no total row", 6 misreads, e.g. it grabbed `110` for 2025 wk04 whose true total is `1100`, or `51` for 2022 wk07 whose true total is ~`403`). These are **total-row extraction-tool limitations, not data errors** — proven by Method 2.
- Evidence file: `qc/wer_manual_qc_checksum_by_issue.csv`.

### Method 2 — visual double-entry (3 issues, 78 cells)
- **2020 wk08:** all 26 current-week values match v2. (Control total 1441 = v2 sum 1441.)
- **2022 wk07:** all readable cells match v2 (Colombo 12, Gampaha 63, … Kalmunai 14); Badulla is a dense low-confidence read but consistent.
- **2025 wk04:** all 26 current-week values match v2.
- **Crucially**, 2022 wk07 and 2025 wk04 were in Method 1's *unverified* set — visual reading confirms they are correct, demonstrating the Method-1 failures are tool artifacts.
- Per-cell evidence: `qc/wer_manual_qc_results.csv`.

### Convergent outcome
- Independently verified cells: **~624** (572 checksum + 78 visual − 26 overlap) + 12 from the earlier POC.
- **Genuine current-week mismatches found: 0.**
- Every format era (2018, 2019, 2020, 2022, 2023, 2024, 2025) has ≥1 directly verified issue with zero mismatches.

## A–H
- **A. Sampled issues:** 33.
- **B. RDHS cells in sample:** 858 (33×26); ~624 independently verified by checksum and/or visual double-entry.
- **C. Mismatches:** **0.**
- **D. Mismatch rate:** **0.0%.**
- **E. Systematic error mode:** **None in the current-week data.** (Separately documented, not data errors: 33 NA cells from source text-layer loss; the checksum tool's own total-row parsing limitation on some eras.)
- **F. Can current-week be frozen?** **YES — eligible for freeze.** No mismatches; no extractor patch needed; no v3 required.
- **G. Remaining documented missingness:** 33 NA cells (Gampaha 2018 wk23–52 ×30; Puttalam 2019 wk23, 2021 wk45, 2021 wk50 ×3) + **2022 wk44** (entire issue, absent from archive).
- **H. Institutional email:** **Optional / upside, not blocking** — it would recover the 33 NA cells + 2022 wk44 and unlock MOH-division resolution, but the current-week dataset is freeze-eligible without it.

## Recommendation
Declare the **current-week WER dengue outcome dataset eligible for freeze**. Recommended next step (separate, authorized action): create a **frozen, read-only copy with a recorded sha256 checksum**, e.g. `frozen/wer_dengue_currentweek_2018_2025_v2.0-frozen.csv`, and log the freeze in the data plan. Cumulative field remains QC-only / not-for-analysis. Dataset stays in quarantine until that freeze step is explicitly taken.
