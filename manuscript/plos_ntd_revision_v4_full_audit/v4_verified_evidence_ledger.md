# V4 Verified Evidence Ledger

Purpose: single source of truth for the editor to apply v4 manuscript edits **without recomputation**.
Each entry gives the verified answer, a status flag, and the load-bearing source quote.
Status legend: **verified** (frozen record supports the prompt) · **partial** (some sub-claims confirmed, others not in committed record) · **not-found** (no committed evidence) · **contradicts-prompt** (frozen record differs from the prompt claim).

---

## Q1. Colombia E3 exceedance-threshold sensitivity — ΔNB(M5−M1)@p*=0.30, point estimates + 95% CIs (75th/80th/90th)

**Status: VERIFIED** — all three claims match the frozen report exactly.

| Percentile label | ΔNB(M5−M1)@0.30 | 95% CI | Notes |
|---|---|---|---|
| 75th (registered primary anchor) | +0.0188 | [+0.0117, +0.0260] | reproduced exactly in §15 integrity audit |
| 80th (secondary) | +0.0157 | [+0.0082, +0.0236] | |
| 90th (secondary) | +0.0092 | [+0.0003, +0.0183] | **borderline — CI lower bound +0.0003** |

- Source: GID_2 cluster bootstrap, B=1000, 0 failures; p*=0.30 is the registered confirmatory threshold; pointwise CIs, no multiplicity adjustment; CI excludes 0 at all three percentiles. Increment shrinks as outbreaks get rarer.
- File: `docs/colombia_outbreak_threshold_sensitivity_report.md` (Section 7 table; §15 audit).

Key quotes:
> `| **75th** | **+0.0188 [+0.0117, +0.0260]** | ...` (line 48)
> `| 90th | +0.0092 [+0.0003, +0.0183] | ...` (line 50)
> "the **90th-pct CI is borderline (lower bound +0.0003)**." (line 52)
> "ΔNB(M5−M1)@0.30 reproduced exactly (+0.0188 / +0.0157 / +0.0092)." (§15 audit, line 101)

---

## Q2. Colombia M4 feature set ("hybrid without full fixed effects")

**Status: VERIFIED.** M4 = M1 (recent-case lags) + M2 (climate lags), with **NO seasonality** and **NO department fixed effects**.

M4 exact predictors:
- **Recent-case lags:** `cases_lag0, cases_lag1, cases_lag2, cases_lag4` (lag3 intentionally absent); each log1p then standardized.
- **Climate lags:** `precip_lag0..precip_lag8` (9, log1p then standardized) and `temp_lag0..temp_lag8` (9, standardized but NOT log1p).
- **Seasonality:** NONE.
- **Fixed effects:** NONE.

Difference from M5: **M5 = M4 + seasonal sin/cos** (`sin_woy_1, cos_woy_1, sin_woy_2, cos_woy_2`) **+ department (Admin1, 33-level) one-hot fixed effects.**

- **Linear lags, NOT DLNM:** plain linear standardized lag columns entered into L2 logistic regression; no crossbasis/onebasis/spline basis anywhere in the code.
- **Humidity: NOT used.** Only climate inputs are precipitation and temperature.
- Caveat for editor: prompt phrases M4 as "without full fixed effects" — per committed code M4 has **no** fixed effects at all (not "partial"). State precisely.

- File: `scripts/colombia_model_ladder_h4_75pct_v1.py`; `docs/colombia_model_ladder_report.md`; `docs/colombia_model_ladder_spec.md`.

Key quotes:
> `'M4':['cases','climate'], 'M5':['cases','climate','season','dept']` (script lines 39-40)
> `CAS=['cases_lag0','cases_lag1','cases_lag2','cases_lag4']` (script line 19)
> `for c in PRE: X[c]=np.log1p(df[c]) ... for c in TMP: X[c]=df[c]` (script lines 26-28)
> `m=LogisticRegression(C=C,penalty='l2',solver='lbfgs',max_iter=5000)` (script line 47)
> "M4 M1+M2 · M5 M4+season+department FE." (report line 27)

---

## Q3. Colombia per-model calibration metrics M0–M5; drift direction

**Status: PARTIAL.** CITL / slope / Brier are committed per model; **per-model observed prevalence and per-model mean predicted probability are NOT in any committed file** (only quarantined, uncommitted CSV).

Frozen primary run: h=4 weeks, 75th-pct outbreak label, **recalibrated**, common-complete test n=13,361, overall test prevalence **0.375** (base commit 37221a6). File: `docs/colombia_model_ladder_report.md`.

| Model | Brier | CITL | Slope |
|---|---|---|---|
| M0 (climatology) | 0.250 | −0.50 | 3.43 |
| M1 (recent cases) | 0.222 | −0.46 | 1.09 |
| M2 (climate-only) | 0.248 | −0.50 | 0.85 |
| M3 (climate+season+dept) | 0.249 | −0.54 | 1.28 |
| M4 (hybrid) | 0.217 | −0.45 | 1.05 |
| M5 (hybrid+season+dept) | 0.213 | −0.50 | 1.16 |

- **Recalibration method:** Platt fit on the **validation** set (not test); table values are post-recalibration; C tuned by validation log loss; test scored once. Recalibration "improved Brier/calibration modestly"; AUC/PR-AUC unchanged by monotone recalibration. **No numeric before/after recalibration values committed.**
- **Drift direction: OVER-prediction.** CITL ≈ −0.45 to −0.54 (all negative) across all models → systematic over-prediction on the test period, attributed to train/val→test temporal shift (COVID-era caveat), not fully removed by validation-fit recalibration.
- **NOT FOUND (committed):** per-model observed prevalence; per-model mean predicted probability. These exist only in quarantined `colombia_model_calibration_h4_75pct_v1.csv` (881 B, SHA256 6e89bb38f2920f3f…), which is read-only/uncommitted. Only the **overall** test prevalence 0.375 is committed.

Key quotes:
> `| M0 (climatology) | 0.513 | 0.384 | 0.250 | −0.50 | 3.43 | 0.108 |`
> "CITL ≈ −0.45 to −0.54 across all models → systematic over-prediction on the test period not fully removed by validation-fit recalibration."
> "Recalibration (Platt on validation) was applied; metrics above are recalibrated."
> "Test prevalence 0.375." (overall only; no per-model prevalence)

---

## Q4. Time-updated recalibration: leakage-safe rule + zero fallbacks

**Status: VERIFIED** (both facts).

1. **Leakage-safe:** at prediction week *t* (target *t+4*), only forecast–outcome pairs whose **target week is strictly before *t*** are eligible (prediction week *s ≤ t−5*); the row's own *t+4* outcome and any outcome at/after *t* are excluded; enforced **by dates, not row position**.
2. **Zero fallbacks:** "Zero fallbacks across all models and methods." Every eligible window had ≥50 events and ≥50 non-events; all intercept+slope (R2/R4/R2_104) and intercept-only (R1/R3/R1_104) methods ran at 100%; no raw fallback, no convergence failure, no extreme/pinned probabilities.

- Wording caveat for editor: the prompt phrase "No fallback was required under the prespecified recalibration rules" is **not verbatim** in the report; the committed equivalent is "Zero fallbacks across all models and methods." Substantive claim fully supported.
- File: `rolling_recalibration_extension_report.md` (§3 information rule; §5 fallback/stop-rule). Computed CSVs quarantined/git-ignored; markdown report is the committed record.

Key quotes:
> "only forecast–outcome pairs whose **target week is strictly before *t*** are eligible (i.e. prediction week *s ≤ t−5*). ... Enforced by dates, not row position." (§3)
> "**Zero fallbacks across all models and methods.**" (§5)

---

## Q5. Sri Lanka M5 frozen values + canonical R-DLNM contrasts

**Status: VERIFIED.**

M5 (`hybrid_model_extension_report.md` §5): AUC **0.7715** (≈0.772), PR-AUC **0.667**, Brier **0.180**, NB@0.30 **0.1447** (≈0.145). M5 is a reference/near-miss, not a declared win.

ΔNB(M5−M1)@0.30 (§6): point **+0.008**, 95% CI **[−0.001, 0.018]** — CI just touches/includes 0.
- Editor note (corrected 2026-06-28): `hybrid_model_extension_report.md` §6 prints 3-decimal forms, but the companion report `targeted_value_climate_stage1a_h4_report.md` line 16 **does print the 4-decimal forms verbatim** (`+0.0081 [−0.0012, 0.0181]`). The manuscript's 4-decimal figures are therefore directly sourced and correct. (An earlier draft of this ledger erroneously said the 4-decimal forms were not printed and instructed using only 3-decimal forms; that instruction was wrong and is rescinded.)

Canonical R-DLNM vs M1 (`canonical_R_dlnm_report.md` §7): ΔAUC **−0.038** [−0.066, −0.008]; ΔNB@0.30 **−0.025** [−0.041, −0.006] — both favor **M1**, both CIs exclude 0.

R-DLNM vs Python-DLNM (§7): ΔAUC **+0.0003** [−0.005, 0.007]; ΔNB@0.30 **+0.0008** [−0.005, 0.007] — both ~0, CIs span zero, "indistinguishable."

Test set: 3,926 rows, prevalence 0.336 (both reports).

Key quotes:
> `| M5 hybrid + season + RDHS | **0.7715** | **0.667** | **0.180** | ... | **0.1447** |`
> `| M5 − M1 | ΔNB@0.30 | +0.008 | [−0.001, 0.018] | No (just touches 0) |`
> `| **R-DLNM − M1** | ΔAUC | **−0.038** | [−0.066, −0.008] | Yes | M1 |`
> `| **R-DLNM − Python-DLNM** | ΔAUC | +0.0003 | [−0.005, 0.007] | No | (indistinguishable) |`

---

## Q6. Software versions, R citation year, "Python and R [RCoreTeam]" defect

**Status: VERIFIED** (with two flagged defects).

Recorded versions (committed):
- **R 4.6.0 (2026-04-24)**; **dlnm 2.4.10**; **mgcv 1.9.4**; **tsModel 0.6-2** (`canonical_R_dlnm_report.md` §1).
- **geopandas 1.1.3**, **pyogrio 0.12.1**, **pyproj 3.7.1**, **shapely 2.1.2** (`rdhs_geometry_build_report.md`).
- **geopandas 1.1.3**, **rasterio 1.4.4**, **rasterstats 0.21.0** (`worldpop_population_denominator_build_report.md`).

**NOT preserved anywhere committed:** explicit versions for **Python, NumPy, pandas, scikit-learn, SciPy, statsmodels**. sessionInfo recorded only for R (`R_sessionInfo_v1.txt`), not the Python environment.

**DEFECT 1 — R citation YEAR mismatch (CONTRADICTS PROMPT/BIB):** correct R Core Team citation year for R 4.6.0 = **2026** (released 2026-04-24, "Because it was There"). Committed bib key `RCoreTeam2024` (and a 2024 year) is **WRONG → must be 2026**. `reference_audit_v1.md` §5 already flags the version/year as unverified; now resolved to 2026.

**DEFECT 2 — "Analyses used Python and R [RCoreTeam]":** confirmed defect. There is **no Python software citation** in the bibliography at all (audit lists only `RCoreTeam2024` as software); a single `[RCoreTeam]` cite attached to "Python and R" wrongly attributes Python to the R Core Team reference.

Key quotes:
> "**R 4.6.0** (2026-04-24); **dlnm 2.4.10** ...; **mgcv 1.9.4**; tsModel 0.6-2."
> "`RCoreTeam2024` exact R version ... specific minor version/year not verified ... Match to the R version actually used."
> "R 4.6.0 was released on April 24, 2026 ... release name 'Because it was There'" (WebSearch / r-bloggers).

---

## Q7. Reference-integrity check (dataset/article citations)

**Status: VERIFIED.** All eight target citations reached a primary source; **none UNVERIFIED.** Files: `references_v4.bib`, `docs/reference_audit_v1.md`.

| Citation | Primary-source result | Correction needed? |
|---|---|---|
| OpenDengue paper (Clarke2024OpenDengue) | Crossref 10.1038/s41597-024-03120-7; Sci Data 2024;11:296; authors Clarke, Lim, Gupte, Pigott, van Panhuis, Brady | **None** |
| OpenDengue V1.3 figshare (OpenDengue2024) | DOI 10.6084/m9.figshare.24259573 resolves; versioned concept DOI, V1.3 published under same DOI in 2025 | **YES** — bib year 2024 → **2025**; title differs from official figshare title "OpenDengue: data from the OpenDengue database" |
| WorldPop R2025A (WorldPop2025) | "Global 2015-2030, R2025A v1," 100m, release Sept 2025 (no DOI). Methods paper Tatem2017 = Sci Data 2017;4:170004 (10.1038/sdata.2017.4) | **None** (grey-lit OK) |
| Sri Lanka 2024 Census (SriLankaCensus2025) | DCS Census 2024; reference moment 18 Dec 2024; district totals released 30 Oct 2025; national total 21,781,800; bib year 2025 correct | **None** |
| ERA5-Land CDS (ERA5LandCDS) | DOI 10.24381/cds.e2161bac resolves to Copernicus CDS "ERA5-Land hourly data from 1950 to present" (ECMWF/C3S) | **None** |
| CHIRPS (Funk2015) | Crossref 10.1038/sdata.2015.66; Sci Data 2015;2:150066; 11 authors (Funk…Michaelsen) | **None** |
| HDX Sri Lanka COD-AB (HDXCODABSriLanka) | data.humdata.org/dataset/cod-ab-lka; Survey Department of Sri Lanka (OCHA/ITOS); reviewed Oct 2024 | None substantive — recommend adding URL + access date |
| Sri Lanka WER (SriLankaWER) | Epidemiology Unit, MoH (epid.gov.lk/weekly-epidemiological-report) | None substantive — recommend adding URL + date range |

Only substantive correction: the **OpenDengue figshare DATASET entry** (year 2024→2025; align title to official figshare title).

---

# SAFE TO STATE (facts confirmed by the frozen record)

1. Colombia ΔNB(M5−M1)@0.30: 75th **+0.0188 [+0.0117, +0.0260]**; 80th **+0.0157 [+0.0082, +0.0236]**; 90th **+0.0092 [+0.0003, +0.0183]** (90th borderline; GID_2 cluster bootstrap B=1000). 75th is the registered primary anchor and reproduces exactly.
2. Colombia M4 = recent-case lags (cases_lag0/1/2/4) + climate lags (precip_lag0–8 log1p, temp_lag0–8) only — **no seasonality, no fixed effects**; M5 adds seasonal sin/cos + 33-level department FE. **Linear lags, no DLNM; no humidity.**
3. Colombia per-model **CITL / slope / Brier** (M0–M5) as tabulated; overall test prevalence **0.375**; test n=13,361.
4. Colombia drift = systematic **OVER-prediction** (CITL ≈ −0.45 to −0.54, all negative), train/val→test temporal/COVID-era shift, recalibration via Platt-on-validation, AUC/PR-AUC unchanged.
5. Time-updated recalibration is **leakage-safe** (date-enforced, *s ≤ t−5*) with **zero fallbacks** (all methods ran at 100%).
6. Sri Lanka M5: AUC **0.772** (0.7715), PR-AUC **0.667**, Brier **0.180**, NB@0.30 **0.145** (0.1447); ΔNB(M5−M1)@0.30 **+0.008 [−0.001, 0.018]** (just includes 0). Test n=3,926, prevalence 0.336.
7. Canonical R-DLNM − M1: ΔAUC **−0.038 [−0.066, −0.008]**, ΔNB@0.30 **−0.025 [−0.041, −0.006]** (both favor M1). R-DLNM ≈ Python-DLNM (ΔAUC +0.0003, ΔNB +0.0008; indistinguishable).
8. Recorded versions: R 4.6.0 (2026-04-24), dlnm 2.4.10, mgcv 1.9.4, tsModel 0.6-2, geopandas 1.1.3, pyogrio 0.12.1, pyproj 3.7.1, shapely 2.1.2, rasterio 1.4.4, rasterstats 0.21.0.
9. Correct R Core Team citation year for R 4.6.0 = **2026** (fix bib key/year from 2024).
10. Reference set verified against primary sources: OpenDengue paper, WorldPop (incl. Tatem2017), Sri Lanka 2024 Census, ERA5-Land DOI, CHIRPS/Funk2015, HDX COD-AB, Sri Lanka WER — all clean except the OpenDengue figshare dataset entry.
11. PLOS NTD requires **continuous line numbering** (do not restart per page), **double spacing**, and **page numbers** in the manuscript file. **Restore continuous line numbers for the review version.**

---

# DO NOT STATE / NEEDS AUTHOR (unverified or not in committed record)

1. **Colombia per-model observed prevalence** and **per-model mean predicted probability** (M0–M5): NOT in any committed file — only in quarantined, uncommitted `colombia_model_calibration_h4_75pct_v1.csv`. Do not cite per-model prevalence/mean-pred; only the overall 0.375 is committed. **NEEDS AUTHOR** if per-model figures are wanted in the manuscript.
2. **Numeric before/after recalibration values** for Colombia: not committed (only qualitative "improved modestly"). Do not quote specific deltas.
3. ~~**4-decimal Sri Lanka ΔNB figures** (+0.0081 / −0.0012 / +0.0181): NOT printed in the committed report; use the 3-decimal forms.~~ **CORRECTED 2026-06-28 — this item was an error.** The 4-decimal forms `+0.0081 [−0.0012, 0.0181]` ARE printed verbatim in `targeted_value_climate_stage1a_h4_report.md` line 16; the manuscript's 4-decimal usage is verified and correct. (Item retained, struck through, for audit trail.)
4. **Python / NumPy / pandas / scikit-learn / SciPy / statsmodels versions:** not preserved in any committed report. Do not state specific versions; **NEEDS AUTHOR** to record the Python environment before submission.
5. **A Python software citation** is missing from the bibliography. Do not write "Python and R [RCoreTeam]"; **NEEDS AUTHOR** to add a proper Python (and key library) citation and split the cite.
6. **Specific PLOS NTD body font point size** (e.g., 11pt/12pt): NOT specified by the journal — only "a standard font size." Do not assert a numeric requirement.
7. **The verbatim phrase** "No fallback was required under the prespecified recalibration rules" is not in the report; use the committed wording "Zero fallbacks across all models and methods."

---

## Prompt claims that the frozen record does NOT support (explicit flags)

- **80th/90th CI:** prompt values all match — **no discrepancy** (90th CI is genuinely borderline at +0.0003, not a mismatch).
- **Colombia per-model calibration metric that does not exist:** per-model **observed prevalence** and **mean predicted probability** do **not exist** in the committed record (quarantined only). FLAGGED.
- **R citation-year mismatch:** bib key `RCoreTeam2024` / year 2024 **CONTRADICTS** the installed R 4.6.0 → must be **2026**. FLAGGED.
- **"Python and R [RCoreTeam]":** wrongly cites only R for Python; no Python citation exists in the bib. FLAGGED.
- **OpenDengue figshare dataset entry:** year 2024 should be **2025**; title differs from official figshare title. FLAGGED.
