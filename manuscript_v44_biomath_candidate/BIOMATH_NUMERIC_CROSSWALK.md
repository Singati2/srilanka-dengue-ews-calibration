# BIOMATH_NUMERIC_CROSSWALK

**Every number in the biomath candidate traces to the canonical source** `manuscript_v44/revised_manuscript.tex` (branch `agent/v44-round4-geomatics-execution` @ `4b3287c`, SHA256 `08fad12b9188b98faa7566d21769ac71fc3356248afeff91868cebfb07e46915`). The candidate was produced by **copying that file byte-for-byte** and inserting only framing/formalization text; therefore every results number is preserved *by construction*.

**Machine verification performed** (see final report §T): (a) `diff` of non-comment lines shows the only removed lines are the title, one abstract sentence (extended, not renumbered), five subsection headings, and eight `\includegraphics`→`\safeincludegraphics` swaps — **no numeric results line removed**; (b) a result-grade numeric-token census (regex `[+-]?\d\.\d{3,}`) found **all 241 distinct numbers preserved**; the one flagged token (`+0.0008`/`+0.0209`) was a single occurrence inside the *rewritten header comment*, with all 10/7 body (math-mode) occurrences intact. **Status legend:** `VERIFIED` = identical to canonical source and traceable to a frozen artifact cited in the manuscript; `SOURCE_ONLY` = identical to source, artifact cited but not independently re-opened here.

No number was changed for prose convenience. No new number was introduced except symbolic constants of the framework (e.g. the identity $p^*/(1-p^*)$), which are definitional, not empirical.

## Sample sizes / cohort
| Quantity | Value | Canonical location | Status |
|---|---|---|---|
| SL modelable RDHS-week rows after target | 10,516 | Results Q1 (Cohort) | VERIFIED |
| SL training obs / events (2018–2022) | 6,590 / 1,593 | Results Q1 | VERIFIED |
| SL test obs / events (2023–2025) | 3,926 / 1,321 | Results Q1; S18 | VERIFIED |
| CO common-complete test $n$ | 13,361 | Results Q2-CO; S4; Fig1 caption | VERIFIED |
| CO test events / municipalities / departments | 5,015 / 475 / 31 (28 both-class) | Uncertainty; S18; Fig1 | VERIFIED |
| CO municipalities partition | 475 analyzed / 167 excluded / 477 no-usable (=1,119) | Fig1 caption | VERIFIED |
| CO 2022-only subset | 4,802 muni-weeks, 274 munis, 2,202 events | S14 (via source); Results Q6 | SOURCE_ONLY |
| SL 90th-pct events / CO 90th-pct events | 417 / 3,136 | S14 | VERIFIED |

## Dates / periods / horizons / thresholds
| Quantity | Value | Location | Status |
|---|---|---|---|
| SL train / test period | 2018–2022 / 2023–2025 | Methods ladder; spec table | VERIFIED |
| CO train / val / test | 2006–2017 / 2018–2019 / 2020–2022 | Methods ladder; spec table | VERIFIED |
| Primary horizon; sensitivities | $h=4$; $h=1,2,8,12$ | Methods; spec table | VERIFIED |
| Alert label; stricter | training 75th pct; 90th pct | Methods ladder | VERIFIED |
| Reference threshold; grid | $p^*=0.30$; 0.20/0.30/0.34/0.40 | Methods DCA; S1 | VERIFIED |
| Climate lag window ($h=4$) | 4–12 weeks; lags 0–8 | Methods ladder | VERIFIED |

## Prevalence
| Quantity | Value | Location | Status |
|---|---|---|---|
| SL train → test prevalence | 24.2% → 33.6% (0.336) | Results Q1 | VERIFIED |
| CO test prevalence (common-complete) | 0.375 | Results Q2-CO; S4 | VERIFIED |
| CO 2022-subset prevalence | 0.4586 | Results Q6 (via source) | SOURCE_ONLY |
| CO included vs excluded prevalence | 0.375 vs 0.180 | Fig1; Results Q6; Discussion | VERIFIED |
| 90th-pct test prevalence SL / CO | 0.106 / 0.235 | S14 | VERIFIED |

## Model hierarchy / definitions (UNCHANGED — firewall)
| Item | Value | Location | Status |
|---|---|---|---|
| Ladder M0–M5 + M5$_{\text{no-climate}}$ | as defined | Methods ladder; framework §info-sets | VERIFIED |
| Planned primary SL contrast | $\Delta$NB(M4$-$M1) @ $p^*{=}0.30$, $h{=}4$, 75th | Uncertainty; matched-ablation status | VERIFIED |
| Principal climate estimand | matched ablation $\Delta$NB(M5$-$M5$_{\text{no-climate}}$), **post-hoc/exploratory** | Matched-ablation subsection | VERIFIED |
| M4$-$M1 non-nested (not climate-specific) | stated | Matched-ablation; Discussion | VERIFIED |
| CO feature counts M1/M4/M5$_{\text{no-climate}}$/M5 | 4 / 22 / 40 / 58 (58−40=18 climate) | S4; S9 | VERIFIED |

## Discrimination (AUC / PR-AUC / Brier)
| Model / setting | Value | Location | Status |
|---|---|---|---|
| SL M0/M1/M2/M3 AUC | 0.629 / 0.752 / 0.643 / 0.652 | S1; S3 | VERIFIED |
| SL M1 PR-AUC / Brier | 0.652 / 0.191 | S1 | VERIFIED |
| SL Python-DLNM / R-DLNM AUC | 0.714 / 0.714 | S3 | VERIFIED |
| SL M4 / M5 / M5$_{\text{no-climate}}$ AUC | 0.764 / 0.772 / 0.751 | S3 | VERIFIED |
| CO M0..M5 AUC | 0.513/0.685/0.556/0.564/0.699/0.726 | S4 | VERIFIED |
| CO M2/M3 (larger climate-only set) AUC | ≈0.532 / 0.546 | S4 note; Results Q2-CO | VERIFIED |

## Net benefit @ p*=0.30 (levels)
| Model / setting | Value | Location | Status |
|---|---|---|---|
| SL M1 / M2 / M3 NB | 0.137 / 0.069 / 0.078 | Results Q1; S1; S3 | VERIFIED |
| SL alert-all NB @0.20/0.30/0.34/0.40 | 0.171 / 0.052 / −0.005 / −0.106 | S1 | VERIFIED |
| SL M1 NB @0.20/0.34/0.40 | 0.185 / 0.111 / 0.083 | S1; S3 | VERIFIED |
| SL M5 / M5$_{\text{no-climate}}$ NB@0.30 | 0.145 / 0.136 | S3 | VERIFIED |
| CO M1 / M5 NB@0.30 | 0.117 / 0.136 (0.1171 / 0.1358 full-prec) | S4 | VERIFIED |
| CO alert-all NB@0.30 | ≈0.107 | Results Q2-CO; S4 | VERIFIED |
| CO 2022-subset alert-all NB | ≈0.227 | Results Q6 | VERIFIED |

## Incremental net benefit ΔNB (matched ablation and compound)
| Contrast | Point | Conditional 95% CI | Development-inclusive 95% CI | Location | Status |
|---|---|---|---|---|---|
| SL matched, raw | +0.0087 | −0.0015 to +0.0188 | −0.0079 to +0.0245 | Headline table; S3 | VERIFIED |
| SL matched, recalibrated | +0.0157 | +0.0066 to +0.0257 | −0.0002 to +0.0302 | Headline; Results Q2-SL | VERIFIED |
| SL 90th matched (recal) | +0.0034 | −0.0070 to +0.0138 | −0.0105 to +0.0185 | S14 | VERIFIED |
| SL non-climate structure (M5$_{\text{nc}}$−cases) | +0.0462 | +0.0199 to +0.0741 | — | Results Q2-SL; S3 | VERIFIED |
| SL single-penalty refit range | +0.0087 to +0.0099 | — | — | Results Q2-SL | VERIFIED |
| CO matched, recalibrated | +0.0078 | +0.0039 to +0.0119 | +0.0008 to +0.0209 | Headline; Results Q2-CO; S17 | VERIFIED |
| CO 90th matched | +0.0081 | +0.0029 to +0.0138 | +0.0009 to +0.0188 | S14; Results Q6 | VERIFIED |
| CO matched, −0.5 logit intercept shift | +0.0042 | −0.0015 to +0.0099 | — | Results Q2-CO | VERIFIED |
| CO matched, DLNM cross-basis refit | +0.0122 | (no interval) | — | Results Q6 | VERIFIED |
| CO matched, 3-wk reporting-delay censor | +0.0049 | — | — | Results Q6 | VERIFIED |
| CO matched, rolling-origin median | +0.0052 (positive in 75% of 28 depts) | — | — | Results Q6 | VERIFIED |
| CO matched, IPW sensitivity | +0.0079 (vs +0.0078) | — | — | Results Q6 | VERIFIED |
| CO matched, spatial-block conditional | — | +0.0018 to +0.0119 | — | Discussion Limitations | VERIFIED |
| CO matched, wild-cluster-t / LODO jackknife (dept) | — | +0.0036 to +0.0124 / +0.0036 to +0.0120 | — | S15/S16 | VERIFIED |
| CO matched, reconstructed point (fidelity) | +0.00783 vs frozen +0.00786 (Δ 0.00003) | — | — | S17 | VERIFIED |
| CO compound M5−M1 | +0.0188 | +0.0117 to +0.0260 | — | Results Q2-CO; S4; S14 | VERIFIED |
| CO compound ΔAUC(M5−M1) | +0.040 | +0.024 to +0.058 | — | S4 | VERIFIED |
| CO compound 2022-only | +0.0150 | +0.0067 to +0.0249 | — | Results Q6 | VERIFIED |
| CO compound 80th / 90th / h≤8 / h=12 | +0.0157 / +0.0092 / ≈+0.008 / +0.002 | — | S14 | VERIFIED |
| SL M4−M1 (planned primary; non-matched) | −0.008 | −0.028 to +0.013 | — | Results Q2-SL; Discussion | VERIFIED |
| SL M5−M1 (non-matched) | +0.0081 | −0.0012 to +0.0181 | — | Results Q2-SL | VERIFIED |
| SL R-DLNM−M1 ΔAUC / ΔNB | −0.038 / −0.025 | −0.066 to −0.008 / −0.041 to −0.006 | — | S3 | VERIFIED |
| CO operational rescaling @0.30 | ≈0.78 TP-equiv / 100 obs | — | — | Results Q2-CO | VERIFIED |

## Calibration
| Quantity | Value | Location | Status |
|---|---|---|---|
| SL raw CITL M0..M3 | +0.530/+0.513/+0.479/+0.596 | S1; S2 | VERIFIED |
| SL rolling-52 residual CITL M0..M3 | +0.029/+0.020/+0.046/+0.087 | S2 | VERIFIED |
| SL rolling-104 / expanding CITL | per S2 table | S2 | VERIFIED |
| SL M4 / M5 raw CITL; slopes | +0.449 / +0.440; 1.225 / 1.077 | S2; Results | VERIFIED |
| SL M1 slope | 1.246 | S1 | VERIFIED |
| CO CITL M0..M5 | −0.50/−0.46/−0.50/−0.54/−0.45/−0.50 | Results Q2-CO | VERIFIED |
| CO slopes (M0/M2 extremes; M1/M4/M5) | 3.43 / 0.85; 1.09/1.05/1.16 | Results Q2-CO | VERIFIED |
| CO mean predicted vs observed | 0.485 vs 0.375 (→0.376 at −0.5 logit) | Results Q2-CO | VERIFIED |
| ICI full vs matched (SL / CO) | 0.027 vs 0.045 / 0.109 vs 0.113 | Results proper-score; S19 | VERIFIED |

## Proper scores (NLL / Brier / info gain)
| Quantity | Value | Location | Status |
|---|---|---|---|
| ΔNLL recal SL / CO | −0.0207 (−0.0346,−0.0067) / −0.0089 (−0.0165,−0.0011) | Table properscore; S19 | VERIFIED |
| ΔNLL raw SL / CO | −0.0256 / −0.0085 | Table properscore | VERIFIED |
| ΔBrier recal SL / CO | −0.0079 (−0.0129,−0.0030) / −0.0043 (−0.0076,−0.0009) | Table properscore | VERIFIED |
| ΔBrier raw SL / CO | −0.0107 / −0.0036 | Table properscore | VERIFIED |
| Info gain (bits) SL / CO | +0.030 / +0.013 (raw +0.037 / +0.012) | Table properscore | VERIFIED |
| ΔAUC recal SL / CO | +0.027 / +0.012 | Results proper-score; S19 | VERIFIED |
| ΔPR-AUC SL / CO | +0.016 (−0.002,+0.036) / +0.011 (−0.002,+0.026) | Results proper-score | VERIFIED |
| Dev-incl ΔNLL SL / CO | −0.0403 to +0.0040 / −0.0224 to −0.0002 | Results proper-score; S18 | VERIFIED |
| Dev-incl ΔBrier SL / CO | −0.0153 to +0.0013 / −0.0102 to −0.0004 | S18 | VERIFIED |
| Per-model NLL/Brier/ICI/AUC (S19) | SL 0.5406/0.1787/0.027/0.751 vs 0.5613/0.1865/0.045/0.724; CO 0.6162/0.2127/0.109/0.7255 vs 0.6251/0.2169/0.113/0.7134 | S19 | VERIFIED |

## Bootstrap protocol / seeds
| Quantity | Value | Location | Status |
|---|---|---|---|
| Primary DCA bootstrap | $B=1000$, seed 20260612, 0 failures | Uncertainty; S10 | VERIFIED |
| Wild-cluster-t | $B=1999$ (percentile-t) | Uncertainty; S10; S15 | VERIFIED |
| Proper-score bootstrap | $B=10{,}000$ seed 20260719 (parity $B=1000$ seed 20260612); AUC/PR-AUC $B=5000$ | Proper-score methods; S18 | VERIFIED |
| Dev-inclusive proper-score refit | $B=1000$ seed 20260612, 0 failures | S18; v43→v44 change | VERIFIED |
| Clusters | SL 26 RDHS; CO 475 muni / 31 dept (28 both-class); regime 8 | Uncertainty; S10 | VERIFIED |
| Moran's I (SL / CO; matched) | −0.12 (p=0.33) / +0.20 (p=0.10); matched −0.07 / +0.22 | Discussion Limitations | VERIFIED |
| Data table SHA-256 (CO climate-linked) | 5d4d646e…a9ad2a | Declarations | VERIFIED |

## Country-specific statements
- SL: recent surveillance hard to beat; matched climate increment small, development-inclusive intervals include zero (raw and recalibrated). — Results/Discussion — VERIFIED
- CO: matched increment small (+0.0078), selected higher-incidence subset, widens under refitting, boundary-adjacent DI lower bound (+0.0008) not a firm exclusion of zero. — Results Q2-CO; S17 — VERIFIED
- No formal between-setting heterogeneity test performed. — Abstract; Uncertainty; Discussion — VERIFIED

## Result
**No candidate number differs from the canonical manuscript.** No `NOT_TRACEABLE` entries. If any future edit changes a candidate number, stop and reconcile to the canonical source before proceeding.

---

## Tightening-pass re-verification
The decision-theoretic tightening pass changed only framing/notation (metric orientation, trims, title, Discussion). Re-ran the result-grade numeric census (`[+-]?\d\.\d{3,}`) candidate vs canonical: **all 241 numbers preserved**; the only reduced token remains the single `+0.0008 to +0.0209` occurrence inside the rewritten header *comment* (all 10/7 math-mode body occurrences intact). No results number was changed. Status of every entry above: unchanged (`VERIFIED`/`SOURCE_ONLY`).

---

## Final-verification pass re-check (2026-08-10)
Novelty sentence reworded (framing only), `+0.0099` provenance confirmed pre-existing (canonical line 171; commit 0b8bbff, 2026-07-15 — see SINGLE_PENALTY_0099_PROVENANCE.md). Re-ran the result-grade census: **241/241 preserved**; only the header-comment `+0.0008/+0.0209` token differs. No headline result untraceable. Candidate `.tex` SHA256 `69a00534…`; internal-review PDF `3c04367f…`, grayscale `899b3ea9…`.
