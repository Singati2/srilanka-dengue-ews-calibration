# Data Dictionary — WER Current-Week Dengue Outcome Dataset

**Describes (but does not contain):** `wer_dengue_currentweek_rdhs_2018_2025_v2.0-frozen.csv`
**Held locally only** (git-ignored). SHA256: `99f0b9b122460c7d24a6672bbc933176af250789c4b492b421852c2626af3e99`
**Grain:** one row per (WER issue × RDHS division). 415 issues × 26 RDHS = **10,790 rows**.

## Fields
| Column | Type | Description |
|---|---|---|
| `year` | int | Calendar/epi year of the WER issue (2018–2025). |
| `week` | int | Epidemiological week = WER issue number within the year (1–52/53). |
| `vol` | int | WER volume number (Vol 45 = 2018 … Vol 52 = 2025). |
| `rdhs` | string | RDHS division name (26 distinct; canonical spelling — see crosswalk for official/alias forms). |
| `dengue_current_week` | int / empty | **PRIMARY OUTCOME.** Dengue Fever cases reported during the current week for this RDHS (Table 1 column A). Empty = documented NA (see policy). |
| `dengue_cumulative` | int / empty | **QC-ONLY — NOT FOR ANALYSIS.** Year-cumulative dengue (Table 1 column B). Has year-1/2 prior-year carryover and ~68 mid-year extraction/revision anomalies; retained only for QC/support. |
| `source_pdf` | string | Filename of the source WER PDF the row was extracted from. |
| `extraction_flag` | string | `ok` (value extracted), `no_value`, or `absent_in_text_layer` (row physically missing from the source PDF text layer → NA). |
| `extraction_method` | string | `layout` (pdftotext -layout) or `layout+plain_fallback` (fallback used to recover rows). |

## Spatial / temporal unit
- **Spatial:** 26 RDHS divisions (Regional Director of Health Services areas). RDHS ≈ district except Ampara district is served by two RDHS (Ampara + Kalmunai). See `geomatics_templates/rdhs_crosswalk_template.csv`.
- **Temporal:** epidemiological week / WER issue, 2018–2025.

## Missingness policy
- The dataset is **structurally complete**: every issue emits exactly 26 RDHS rows. Genuinely-absent source rows are **NA-filled and flagged** (`extraction_flag = absent_in_text_layer`), never dropped.
- NA current-week cells are **documented missing data**, accepted as-is for the current frozen dataset (recoverable only via OCR or an institutional machine-readable feed).
- `dengue_current_week` has **0 invalid values** across the 10,757 real cells.

### Documented NA cells (33 total)
- **Gampaha — 2018 weeks 23–52** (30 cells): systematic source-PDF text-layer loss.
- **Puttalam — 2019 week 23, 2021 week 45, 2021 week 50** (3 cells): source-PDF text-layer loss.

### Missing full issue (1)
- **2022 week 44** (`Vol_49_no_44`): the entire WER issue is absent from the public archive (no PDF). Not represented in the dataset.

## Provenance & QC
- Source: Sri Lanka Epidemiology Unit, Weekly Epidemiological Report, Table 1.
- WER PDFs downloaded: 415 / 416.
- Manual / double-entry QC: 33 sampled issues, **0 mismatches** (control-total checksum + visual double-entry; ~624 cells independently verified). See `qc_summaries/wer_manual_qc_report.md` and `qc_summaries/wer_dengue_extraction_qc_v2.md`.
- Build/QC scripts: `scripts/wer_bulk_harvest.py`, `scripts/wer_bulk_extract_dengue_v2.py`, `scripts/wer_qc_report_v2.py`.

## Usage notes
- Use `dengue_current_week` as the outcome; treat empty as missing (NA).
- **Do not** use `dengue_cumulative` for analysis.
- Join to geometry/denominators via the RDHS crosswalk (apply aliases: `Killinochchi→Kilinochchi`, `Moneragala→Monaragala`, etc.).
