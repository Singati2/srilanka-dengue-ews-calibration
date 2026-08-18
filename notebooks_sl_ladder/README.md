# Sri Lanka M0–M5 ladder — independent rebuild

A Sri Lanka-only reconstruction of the model ladder, built from raw inputs on this Mac and gated
against the frozen run's own 3,926 test-set predictions.

Run in order. Each notebook writes to `data_quarantine/sl_ladder/` and reads only what the previous
ones wrote.

| Notebook | Does | Key result |
|---|---|---|
| `sl_00_inputs` | Inventory and check every input | grid window is over Sri Lanka; both WER extractions agree |
| `sl_01_exposure` | ERA5/CHIRPS grids → district-week climate | 10,842 district-weeks, 26 districts |
| `sl_02_linked_table` | Join outcome + population + exposure | all 3,926 frozen keys present |
| `sl_03_conventions_and_label` | Recover two undocumented conventions | week offset −1 (0.820 → 0.988) |
| `sl_04_ladder_and_gate` | Fit M0–M5, gate against frozen | test set **exactly 3,926**; ΔNB +0.0071 vs frozen +0.0087 |
| `sl_05_evaluation` | Calibration, decision curves, cluster bootstrap | ΔNB +0.0071 [−0.0041, +0.0198] |

## What is reconstruction and what is reimplementation

M1, M4, M5 and M5_no-climate port their design and fit **verbatim** from
`analysis/v12_referee_response/run/sl_matched_and_recal.py`. Only the input path changes, so any
difference from the frozen run is a data difference rather than a modelling one.

M0, M2 and M3 have no in-repo Sri Lanka implementation and are built from the Methods spec. They
carry weaker provenance and are labelled as such wherever they appear.

## The one substantive deviation

The frozen study built exposure from **ERA5-Land at 0.1°**, which needs a CDS key and is not on this
machine. This rebuild substitutes the cached **ERA5 0.25°** window and keeps CHIRPS 0.05° for rainfall.

`sl_04`'s gate measures what that costs, and the measurement is unusually clean:

| Model | corr. with frozen predictions |
|---|---|
| M5 no-climate (uses no climate at all) | **0.976** |
| M5 full (identical, plus the climate block) | **0.881** |

Two models that differ only by the climate block, so the drop is attributable to the exposure
substitution and not to anything else in the pipeline. A CDS key and an ERA5-Land pull would close
most of that gap; nothing else in the series would change.

## Two conventions recovered, not documented anywhere

`sl_03` sweeps both against the frozen labels rather than guessing:

1. **Week offset.** `week_start = ISO_Monday(y, w) − 7d`, not `ISO_Monday(y, w)`. Worth 17 points of
   label agreement (0.820 → 0.988). Reads as the WER bulletin labelled week *w* carrying the week
   that just ended.
2. **Population denominator.** Time-invariant per district, not year-varying.

With both applied, label agreement is 98.8%, and **all 48 residual disagreements sit within 15% of
their district's threshold** — boundary noise, not a systematic error still hiding.

## Row reconciliation

10,490 rows against the manuscript's 10,516. The 26-row gap is one week: the −1 shift pushes the
first 2018 reporting week to 2017-12-25, and the cached climate grids start 2018-01-01. The **test
set matches exactly at 3,926**, which is what the gate depends on.

## Known limitations

- Three districts have CHIRPS area coverage below 25%; **LK52K (Kalmunai)** has no valid CHIRPS cell
  at all and falls back to the nearest valid one. Narrow coastal units are poorly served by a 0.05°
  land mask.
- The bootstrap in `sl_05` is **conditional** (models fixed, evaluation set resampled). The frozen
  study's headline interval is development-inclusive and therefore wider and more honest; the two are
  not interchangeable.
- M0/M2/M3 are reimplementations. Their levels are plausible and correctly ordered but should not be
  quoted as reproductions of the frozen ladder.
