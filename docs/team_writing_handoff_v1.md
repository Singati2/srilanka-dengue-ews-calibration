# Team Writing Handoff — Evidence-to-Writing Packet (v1)
*Purpose: help the human team write the manuscript **accurately in their own words**. This is a structured handoff of facts and numbers from the already-committed reports — **not** manuscript prose, **not** an abstract, **not** final wording. All numbers below trace to committed `docs/*` reports; no new computation was done. The team writes all narrative text.*

**Date:** 2026-06-12 · **Source commits:** afbb52e, 86f9015, 0034932, 35793e2 (+ specs/addendum 6720a58, ee41b46, 6d423b4, 9ab8b36).

---

## 1. One-sentence study message (plain language, for paraphrasing — not final wording)
In a Sri Lanka RDHS × epi-week dengue early-warning evaluation, existing climate-driven models did not beat a simple recent-cases baseline on operational decision value, and the calibration drift they all showed in 2023–2025 was correctable by simple time-updated recalibration.

---

## 2. Claim map
| # | Claim | Evidence source (committed) | Exact numbers to cite | Strength | Caution / wording guardrail |
|---|---|---|---|---|---|
| C1 | Recent-cases AR (M1) dominates at short-to-medium operational horizons | `pilot_h4_75pct_calibration_dca_report.md`, `label_horizon_robustness_report.md` | M1 AUC 0.843 (h=1), 0.810 (h=2), 0.751 (h=4); climate (M2/M3) ≤0.665 at those h; M1 wins NB@p*0.30 all 10 cells | **strong** | Say "at h ≤ 4 / operational leads," not "always." |
| C2 | Climate models do not beat M1 on registered net benefit at p\*=0.30 | `label_horizon_robustness_report.md` | M1 NB@0.30 wins all 10/10 cells; primary h=4: M1 0.137 vs M3 0.078, M2 0.069, alert-all 0.052 | **strong** | Tie to the *registered* decision metric; don't generalize to all thresholds. |
| C3 | Climate becomes competitive on AUC only at long horizons (h=8–12) | `label_horizon_robustness_report.md` | AUC crossover: 75pct h=12 M3 0.659 > M1 0.646; 90pct h=8 M2 0.663 > M1 0.644; 90pct h=12 M3 0.624 > M1 0.610 | **moderate** | Discrimination-only and conditional; does NOT flip net benefit at p*0.30. |
| C4 | A real calibration drift (under-prediction) exists in 2023–2025 | `pilot_h4_75pct_calibration_dca_report.md` | Raw CITL all positive: M0 +0.530, M1 +0.513, M2 +0.479, M3 +0.596; mean pred ~0.23–0.25 vs observed 0.336 | **strong** | Frame as temporal/base-rate drift (train 24.2% → test 33.6%), not model failure. |
| C5 | Rolling-52 recalibration corrects calibration-in-the-large | `rolling_recalibration_extension_report.md`, `label_horizon_robustness_report.md` | Rolling-52 CITL → ≈0 (M0 +0.029, M1 +0.020, M2 +0.046, M3 +0.087); expanding under-corrects (+0.31…+0.39); corrected in all 10 label/horizon cells | **strong** | "Operationally correctable"; note window choice matters (short rolling > expanding). |
| C6 | S1–S3 sensitivities support the main conclusion | `pilot_h4_75pct_sensitivity_report.md` | S1 v1: M1 0.753 vs climate ≤0.646; S2 max climate AUC 0.660 (lag 4) ≪ M1 0.752; S3 M1 0.753, conclusion unchanged; all stop rules PASS | **strong** | Report S2 as full lag curve; don't headline the best lag. |
| C7 | Date-aligned linkage matters but doesn't change the conclusion | `analysis_table_linkage_v2_date_aligned_report.md`, sensitivity S1 | Naive v1 vs date-aligned v2: M2 0.622→0.643, M3 0.646→0.652; M1 ~unchanged | **moderate** | Alignment is a methods-quality point, not a results-changing one. |

---

## 3. Key numbers table (the essential figures only)
| Item | Value(s) | Source |
|---|---|---|
| Primary modelable rows (h=4, 75pct) | 10,705 filtered → 10,516 after target → train 6,590 / test 3,926 | primary pilot |
| Event prevalence | overall 27.7%, train 24.2%, test 33.6% (test events 1,321) | primary pilot |
| Test AUC (raw) M0/M1/M2/M3 | 0.629 / **0.752** / 0.643 / 0.652 | primary pilot |
| Test PR-AUC (raw) | 0.459 / **0.652** / 0.460 / 0.476 | primary pilot |
| Test Brier (raw) | 0.222 / **0.191** / 0.220 / 0.220 | primary pilot |
| Test CITL (raw) | +0.530 / +0.513 / +0.479 / +0.596 | primary pilot |
| DCA net benefit @ p\*=0.30 (raw) | M1 0.137 > M0 0.084 > M3 0.078 > M2 0.069 > alert-all 0.052 > none 0 | primary pilot |
| S1 (v1 literal-week) AUC | M1 0.753; M2 0.622; M3 0.646 | sensitivity |
| S2 lag sweep (climate best) | M2 AUC 0.660 @lag4 (0.643 @lag0); M3 0.658 @lag2; max climate NB@0.30 0.088 ≪ M1 0.137 | sensitivity |
| S3 (drop late-2021) AUC | M1 0.753; climate 0.63–0.65; CITL +0.39…+0.47 | sensitivity |
| Rolling recal CITL before→after (roll-52) | M0 +0.530→+0.029; M1 +0.513→+0.020; M2 +0.479→+0.046; M3 +0.596→+0.087 | rolling recal |
| Rolling recal: M1 vs climate after recal | M1 AUC 0.707–0.752; climate 0.536–0.652; M1 NB@0.30 0.124–0.142; climate 0.055–0.085 (no climate beats M1) | rolling recal |
| Label/horizon: M1 AUC by horizon (75pct) | h1 0.843 → h4 0.751 → h8 0.679 → h12 0.646 | label/horizon |
| Label/horizon: NB@0.30 winner | M1 in all 10/10 cells | label/horizon |
| 90th-pct cells | test prev ~10.6%, events 399–426 (not sparse) | label/horizon |

---

## 4. Figure & table checklist (team to construct — no figures drawn here)
| ID | Title (working) | Data/report | x-axis | y-axis | Main message | Placement |
|---|---|---|---|---|---|---|
| F1 | Decision curve, primary pilot | `dca_h4_75pct_v1.csv` (primary report) | threshold prob p\* (0.05–0.50) | net benefit | M1 > climate > alert-all in mid-high band | Main |
| F2 | Calibration before vs after recalibration | `rolling_recalibration_*` report | predicted prob (decile) | observed freq | raw under-predicts; rolling-52 restores diagonal | Main |
| F3 | AUC vs forecast horizon, M1 vs M2/M3 | `label_horizon_metrics_v1.csv` (report) | horizon h (1–12) | AUC | M1 decays, climate flat → crossover at h≥8 | Main |
| F4 | NB@p\*=0.30 vs horizon by model | `label_horizon_*` report | horizon h | net benefit @0.30 | M1 wins all horizons on decision value | Main or Supp |
| F5 | S2 climate-lag sweep | `sensitivity_lag_sweep_*` (S1–S3 report) | climate lag L (0–8) | AUC / NB@0.30 | climate best at L≈2–4, still ≪ M1 | Supplement |
| T1 | Primary metrics table (M0–M3 × raw/recal) | primary + rolling recal reports | — | — | discrimination/calibration/DCA summary | Main |
| T2 | Stop-rule / prevalence by cell | `*_stop_rules_*` CSVs (reports) | — | — | all cells valid, 90pct not sparse | Supplement |
| T3 | Sensitivity summary (S1–S3) | S1–S3 report | — | — | conclusion robust to linkage/lag/anomaly | Main or Supp |

---

## 5. Results section bullet outline (bullets only — team writes prose)
**A. Analysis frame**
- Unit: 26 RDHS × ISO epi-week, 2018–2025; outcome = WER current-week dengue; denominators = census-rescaled WorldPop.
- Date-aligned linkage v2 used (WER issue number ≠ ISO week; offset +1 typical, +2 in 2021).
- Primary filter → 10,705 modelable rows; train 2018–2022 / test 2023–2025.
- *Caution:* state linkage is date-derived, not week-number; cite the calendar-anomaly memo.

**B. Primary pilot (h=4, 75th-pct)**
- Target 10,516 rows; test prevalence 33.6% vs train 24.2%.
- AUC: M1 0.752 ≫ M2 0.643 / M3 0.652 / M0 0.629; Brier M1 0.191.
- NB@p\*0.30: M1 0.137 > M0 0.084 > M3 0.078 > M2 0.069 > alert-all 0.052.
- *Caution:* discrimination is secondary; lead with calibration + decision value.

**C. Calibration drift**
- All models under-predict on test: CITL +0.48…+0.60; mean predicted ~0.23–0.25 vs observed 0.336.
- Driven by train→test prevalence rise (24.2%→33.6%).
- Training-only Platt recalibration did NOT fix it.
- *Caution:* describe as temporal/base-rate drift, not "models are wrong."

**D. Rolling recalibration**
- Time-updated, leakage-safe (only completed targets before week t), pooled across RDHS.
- Rolling-52 intercept-only drives CITL to ≈0 (+0.02…+0.09); zero fallbacks; expanding under-corrects (+0.31…+0.39).
- M1 still dominates after every method (AUC 0.707–0.752; NB@0.30 0.124–0.142 vs climate ≤0.085).
- *Caution:* note AUC shifts slightly because the map is time-varying (not globally monotone).

**E. S1–S3 sensitivities**
- S1 naive v1 linkage slightly lowers climate AUC (M2 0.622, M3 0.646); M1 unchanged.
- S2 lag sweep: climate best at lag 2–4 (M2 0.660) but ≪ M1 (0.752); full curve reported.
- S3 drop late-2021: conclusion unchanged (M1 0.753).
- *Caution:* do not headline the best S2 lag.

**F. Label/horizon robustness**
- 10 cells (75/90 pct × h=1,2,4,8,12), all stop-rules pass; 90pct not sparse (events 399–426).
- M1 AUC decays with horizon (0.843→0.646); climate flatter → AUC crossover at h≥8.
- NB@p\*0.30: M1 wins all 10 cells; climate beats M1 at mid-high thresholds only at h=8/12 (never h≤4).
- *Caution:* report long-horizon climate edge as conditional and discrimination-only.

**G. Final interpretation**
- Operational regime (h≤4, registered p\*0.30): M1 not beaten by existing climate EWS forms.
- Calibration drift real but operationally correctable.
- Long-lead (8–12 wk) climate competitiveness on AUC is a credible, conditional nuance.
- *Caution:* frame as calibration-reporting / decision-evaluation / data-resource contribution, not "climate EWS fails/wins."

---

## 6. Discussion talking points (bullets only)
- **Recent cases beat climate at short horizons:** dengue autocorrelation makes last weeks' counts highly predictive of next weeks' alerts; climate's signal is indirect/lagged.
- **Climate competitive at long horizons:** climate is a *longer-lead* driver (vector dynamics), so its relative value rises as autocorrelation fades (h≥8).
- **AUC alone is insufficient:** equal/decent AUC coexisted with material calibration drift and threshold-dependent decision value; ranking ≠ usefulness.
- **Why DCA matters:** net benefit at a clinically/operationally anchored threshold reflects deployment value better than discrimination; comparators (alert-all/none) ground the comparison.
- **Why rolling recalibration matters:** drift is a deployment reality; simple time-updated recalibration fixes calibration-in-the-large, and window length is a real operational choice (short > expanding).
- **Limitations:** single country/period; existing models only (no new forecaster); region-specific labels; not externally validated; not prospectively deployed.
- **Public-health relevance:** argues for calibration + decision-curve reporting standards in dengue EWS, and a reusable RDHS-week linked data resource; cautions against AUC-only model claims.

---

## 7. Claims to AVOID (hard guardrails)
- ❌ Do **not** claim climate EWS "fails" in general — it is competitive at long horizons on discrimination.
- ❌ Do **not** claim climate has "no value."
- ❌ Do **not** claim M1 is "universally best" — it decays with horizon; climate edges AUC at h≥8.
- ❌ Do **not** claim any **causal** effect of climate on dengue.
- ❌ Do **not** claim **external validity** beyond this Sri Lanka 2018–2025 dataset.
- ❌ Do **not** claim **deployment readiness** — no prospective/real-time test was done.
- ❌ Do **not** present the most favorable horizon/threshold/lag as the headline.

---

## 8. Recommended headline options (SUGGESTIONS ONLY — team decides)
- S1: "Calibration and decision-curve evaluation of climate-driven dengue early-warning models in Sri Lanka: a recent-case baseline is hard to beat, and calibration drift is correctable."
- S2: "Discrimination is not enough: a decision-analytic re-evaluation of climate-based dengue early warning in Sri Lanka."
- S3: "When does climate help? Horizon-dependent value of climate vs surveillance signals for dengue alerts in Sri Lanka."
*(All three are drafts for the team to rewrite; do not treat as final titles.)*

---

## 9. Suggested writing assignments
- **Methods — data & linkage:** outcome harvest/freeze, geometry, denominators, date-aligned linkage, calendar-anomaly handling. (Sources: linkage v2 report, calendar memo, exposure freeze.)
- **Methods — modeling/evaluation:** M0–M3 ladder, labels, splits, calibration/DCA definitions, recalibration. (Sources: pilot spec, recalibration spec.)
- **Results:** primary pilot + robustness numbers per §5 outline. (Sources: 4 committed reports.)
- **Calibration/DCA interpretation:** §6 talking points 3–5. 
- **Discussion/limitations:** §6 + §7 guardrails.
- **Figures/tables:** §4 checklist; pull from quarantined CSVs (kept local, not committed).

---

## 10. Reproducibility note — committed evidence chain (latest relevant commits)
- Primary pilot report — `docs/pilot_h4_75pct_calibration_dca_report.md` (commit 35793e2)
- S1–S3 sensitivity report — `docs/pilot_h4_75pct_sensitivity_report.md` (commit 0034932)
- Rolling recalibration report — `docs/rolling_recalibration_extension_report.md` (commit 86f9015)
- Label/horizon robustness report — `docs/label_horizon_robustness_report.md` (commit afbb52e)
- Supporting specs/addendum: pilot spec (ee41b46), preregistration addendum (6720a58), recalibration spec (6d423b4), label/horizon spec (9ab8b36), exposure freeze (8495401), linkage v2 (482f4a2), calendar memo (2b07d46).
- All numeric artifacts are **quarantined** (`~/data_quarantine/model_pilots/...`), read-only, checksummed in each report; not committed.

---

## Confirmation
- **No models were run; no metrics computed.** All numbers are transcribed from already-committed reports.
- **No data modified; no data files created.** Only this markdown handoff document was created.
- This document contains **no manuscript paragraphs, no abstract, and no final prose** — only structured facts, tables, and bullets for the human team to write from.
