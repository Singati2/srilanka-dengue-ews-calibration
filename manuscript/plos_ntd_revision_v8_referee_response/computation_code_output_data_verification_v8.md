# Computation / code / output / dataset verification — v8 (read-only; no recomputation)

Multi-agent read-only audit (5 lenses + synthesis). **No script was executed, no model refit, no metric/bootstrap/CI recomputed.** Verification = compare already-committed outputs to the manuscript, read the code logic, and check deterministic arithmetic.

## Verdict per area
| Area | Verdict |
|---|---|
| Dataset integrity | **ALL-MATCH** |
| Colombia outputs → manuscript | **ALL-MATCH** |
| Sri Lanka outputs → manuscript | **ALL-MATCH** |
| Code correctness (logic) | **ALL-MATCH** |
| Computation consistency (arithmetic) | **ALL-MATCH** |
**No discrepancies found.** Every committed value rounds to the manuscript value at the stated precision.

## How each class was verified (method)
- **Dataset (Sri Lanka):** `wc -l`/`awk` on `dengue_climate_population_linked_2018_2025_v1.csv` for rows/flags/units/years, cross-read vs `.meta.md`. Confirmed 10,868 rows = 10,842 exposure backbone + 26 outcome-only (2021-W53, 771 cases, `Vol_48_no_53.pdf`); 26 RDHS; 2018–2025; 417×26 backbone; fully-modelable 10,731; outcome-missing 111 = 78 issue-absent + 33 NA.
- **Dataset (Colombia):** `meta.json` `primary_counts.test=13361`; `awk` mean(y)=5015/13361=0.3753→0.375 on the committed predictions CSV.
- **Outputs → manuscript:** read the `recal` rows of the committed `*_metrics.csv`, `*_dca.csv` (NB@0.3), and `*_bootstrap_ci.csv` (dAUC/dNB CI); compared rounded to Tables 1–5, Figure 3, and Results.
- **Code:** read (not ran) the NB function, label construction, `design()`/`fit_select()`, Platt, and cluster-bootstrap loops.
- **Computation:** deterministic arithmetic from two CSV cells each (odds 0.30/0.70=0.4286; ΔNB=NB_M5−NB_M1; ×100 translations).

## Representative confirmations (committed value → manuscript)
- Colombia M5 (recal): AUC 0.72548→0.726, CITL −0.5049→−0.50, slope 1.1601→1.16, NB@0.30 0.13583→0.136. ΔNB(M5−M1)=0.0187753→+0.0188; CI [0.011668,0.026006]→[0.0117,0.0260]; ΔAUC [0.023455,0.057508]→[0.024,0.058]; B=1000, failures=0.
- Sri Lanka M5 hybrid: brier 0.1801→0.180, AUC 0.7715→0.772, CITL 0.4398→0.440, slope 1.0774→1.077, NB@0.30 0.14471→0.145. ΔNB(M4−M1)=−0.00826 [−0.0278,0.01277]→−0.008 [−0.028,+0.013]; ΔNB(M5−M1)@0.30=0.00808 [−0.0012,0.01809]→+0.0081; @0.40=0.02411→+0.0241; regime 0.02022 [0.00378,0.03702], 8 clusters.
- Translations: 0.0188×100=1.88→1.9 (1.2–2.6); 4.39→4.4 (2.7–6.1).

## Code correctness (logic confirmed against the manuscript's claims)
- **Net-benefit formula** `tp/n − (fp/n)*(t/(1−t))` (ladder script) ≡ manuscript Eq. (NB).
- **Label = train-only percentile exceedance** (threshold from `split=='train'` rows only; strict `>`; future-absent = NaN) → **no test leakage**.
- **Preprocessing/penalty** scaler built from train, reused on val/test; penalty C selected on **validation** log-loss (disclosed) → leakage-safe.
- **Cluster bootstrap** resamples unique GID_2/RDHS with replacement, retains all weeks, skips one-class resamples, seed 20260612, B=1000, 0 failures.
- **Platt recalibration** fit on validation, applied to test (matches "Platt scaling fit on the validation period").
- **M4=M1+M2 linear lags; M5=M4+season+dept FE** (matches the per-country ladder). Note: Colombia M1 = cases-only lags (no harmonics) — the manuscript explicitly discloses per-country feature differences, so this is consistent, not a defect.

## Honest limits
- This is a **fidelity + code-logic audit**, not a re-execution. It proves the manuscript transcribes the committed outputs correctly and that the code implements the leakage-safe design claimed — it does **not** re-derive model fits or bootstrap distributions from raw data (that would break the freeze).
- Bootstrap CIs are checked as committed endpoints + B/seed/failure metadata, not re-resampled. The SL targeted-value seed is recorded as not retained (that one interval is checkable only as a committed value).
- Colombia n=13,361 / prevalence 0.375 are not stored in the metric/DCA/CI CSVs; verified from the predictions CSV + meta JSON instead.
