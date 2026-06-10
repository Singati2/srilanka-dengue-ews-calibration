# WER Dengue Extraction QC v2 (Quarantined)

Primary outcome field: **dengue_current_week**. Cumulative = QC-only.

- Issues extracted: **415**
- Rows total: **10790** (= 415 x 26, structural)
- Issues with structural 26 rows: **415/415**
- Issues with COMPLETE current-week (no NA): **382/415**
- Real current-week cells: **10757**
- NA cells (absent_in_text_layer): **33**
- Invalid current-week values (negative/non-int): **0**
- Cumulative week1-2 carryover decreases (NON-fatal): **209**
- Cumulative mid-year decreases (flagged, non-blocking): **68**
- Missing issues (no PDF in archive): **[(2022, 44)]**
- Manual double-entry sample: **33 issues**

## CURRENT-WEEK OUTCOME QC: **PASS (pending manual sample confirmation)**
## CUMULATIVE FIELD QC: **QC-only, NOT freeze-ready** (68 mid-year anomalies)

## NA cells (source-PDF text-layer loss; need OCR or institutional data)

- **Gampaha** (30): 2018w23, 2018w24, 2018w25, 2018w26, 2018w27, 2018w28, 2018w29, 2018w30, 2018w31, 2018w32, 2018w33, 2018w34, 2018w35, 2018w36, 2018w37, 2018w38, 2018w39, 2018w40, 2018w41, 2018w42, 2018w43, 2018w44, 2018w45, 2018w46, 2018w47, 2018w48, 2018w49, 2018w50, 2018w51, 2018w52
- **Puttalam** (3): 2019w23, 2021w45, 2021w50

## Cumulative mid-year decreases (top 15; cumulative-field QC only)

| Year | RDHS | wk->wk | cum->cum | drop |
|---|---|---|---|---|
| 2023 | Kalutara | 44->45 | 24394->4365 | 20029 |
| 2023 | Kalutara | 42->43 | 23793->4276 | 19517 |
| 2024 | Colombo | 45->46 | 10034->1018 | 9016 |
| 2025 | Ratnapura | 37->38 | 3863->685 | 3178 |
| 2025 | Kegalle | 38->39 | 3930->1207 | 2723 |
| 2023 | Anuradhapura | 46->47 | 2999->726 | 2273 |
| 2023 | Ratnapura | 51->52 | 2436->842 | 1594 |
| 2024 | Ratnapura | 37->38 | 2220->671 | 1549 |
| 2024 | Ratnapura | 34->35 | 2044->618 | 1426 |
| 2023 | Ratnapura | 42->43 | 1988->658 | 1330 |
| 2023 | Kalmunai | 46->47 | 2927->1713 | 1214 |
| 2023 | Badulla | 51->52 | 1740->656 | 1084 |
| 2024 | Kalmunai | 38->39 | 1690->671 | 1019 |
| 2023 | Kurunegala | 42->43 | 2694->1705 | 989 |
| 2023 | Polonnaruwa | 17->18 | 1197->243 | 954 |

## Notes
- Every issue is structurally 26 rows; absent source rows are NA-flagged, not dropped.
- NA current-week cells are documented MISSING DATA, not extraction errors; recover via OCR/institutional feed or accept as missing.
- Cumulative anomalies do NOT block the current-week outcome dataset (per analysis plan).
- Dataset remains in QUARANTINE; promotion requires manual-sample confirmation + a decision on NA cells.
