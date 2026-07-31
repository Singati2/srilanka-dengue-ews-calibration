# Colombia 2022 week-eligibility — date evidence (v16)

Purpose: give the exact, verified explanation of why the Colombia 2022-only secondary sensitivity contained **48 eligible prediction-origin weeks, not 52**, separating the prediction-origin date, the target/outcome date, and the underlying-source coverage. No model or metric was recomputed; only the frozen prediction file's date column was inspected.

## Source inspected (frozen, read-only)
- File: `~/data_quarantine/colombia_model_pilots/model_ladder_h4_75pct_v1/colombia_model_predictions_h4_75pct_v1.csv`
- sha256: `a938a138d9ef65e302f5521acfaeb9c89468a92092a503fcf461960714206add`
- Rows: 13,361 (full test set 2020–2022). Columns: `GID_2`, `week_start`, `y`, `M0..M5_{raw,recal}`.
- `week_start` = the **prediction-origin** week (Monday). Weekly cadence verified (all consecutive gaps = 7 days).

## Prediction-origin week (week_start)
- Minimum origin (full file): **2020-01-05**
- Maximum origin (full file): **2022-11-27**
- 2022 origins: **48 distinct weeks**, from **2022-01-02** to **2022-11-27**.

## Target / outcome week
- There is **no separate stored target/outcome-date column**. Under the four-week horizon (h=4) the target for an origin at week *t* is the alert at week *t*+4 (origin + 28 days); `y` is that four-week-ahead label. The target date is therefore implied by construction, not preserved as its own column.
- The latest target actually used corresponds to the maximum origin: **2022-11-27 origin → 2022-12-25 target**.

## Underlying eligible-outcome source
- The maximum date of the underlying OpenDengue outcome series is **not independently documented** in the frozen prediction file. **This document does not claim the OpenDengue series ended in late November 2022.** What is verified is that the assembled prediction file's origins end 2022-11-27 and its latest four-week-ahead target is 2022-12-25.

## The four excluded December-2022 origin weeks and the targets they would require
| Excluded origin week | Required h=4 target (origin + 28 days) |
|---|---|
| 2022-12-04 | 2023-01-01 |
| 2022-12-11 | 2023-01-08 |
| 2022-12-18 | 2023-01-15 |
| 2022-12-25 | 2023-01-22 |

All four required targets fall in **January 2023**, beyond the available target period (the last target used is 2022-12-25). Hence 48 = 52 − 4.

## Verified explanation (as used in the manuscript and S9)
> The 2022 sensitivity contained 48 eligible prediction-origin weeks, ending November 27, 2022. The four December 2022 origin weeks would require four-week-ahead outcomes in January 2023, beyond the available target period.
