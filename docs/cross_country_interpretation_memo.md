# Sri Lanka – Colombia Cross-Country Interpretation, Figures/Tables Plan & Sensitivity Recommendation (planning only — NO new analyses)
*Integrates the committed Sri Lanka and Colombia results, proposes manuscript figures/tables, and recommends the single most important remaining sensitivity. **No models run, no metrics computed, no labels/thresholds recomputed, no data modified, no new output files. Interpretation/planning only.** All result numbers are quoted from prior committed reports; literature claims are grounded in a documented Consensus search (§10.1), not asserted.*

**Date:** 2026-06-18 · **Status:** interpretation/planning memo · **Base commit:** 802fbb4 · **Supersedes:** the earlier un-committed cross-country draft.

## 1. Purpose
- Integrate Sri Lanka (primary arm) and Colombia (external framework-replication arm).
- Define the **safe manuscript claim** (supported vs not supported vs cautious).
- Convert the older recommendation list into a **current post-Colombia roadmap**, propose figures/tables, and pick **one** next sensitivity.

## 2. Current evidence status
| Component | Status |
|---|---|
| Sri Lanka primary analysis | ✅ completed |
| Sri Lanka calibration / DCA / uncertainty | ✅ completed |
| Colombia climate linkage (CHIRPS + ERA5-Land) | ✅ completed |
| Colombia labels (h=4 75th-pct, train-only) | ✅ completed |
| Colombia lag-feature assembly | ✅ completed |
| Colombia M0–M5 model ladder | ✅ completed & committed |
| More countries | ✗ not recommended now |
| Additional sensitivity analyses | ◐ optional/gated (one selected, §10) |

## 3. Sri Lanka interpretation (honest)
- Recent-cases / autoregressive baseline (M1) is **hard to beat** operationally.
- Climate-only does **not** clearly dominate; canonical R DLNM was statistically indistinguishable from the Python approximation and still below M1.
- Hybrid gains are **limited, threshold-/regime-dependent** (Stage-1A: no confirmed targeted value at registered p\*=0.30 in a powered regime; underpowered high-incidence+strong-AR signal only).
- **Decision-curve / net benefit matters more than AUC alone.**
- A broad **h=4 operational climate win at p\*=0.30 was not confirmed as universal**.

## 4. Colombia interpretation
- **External framework replication** (local re-fit; no Sri Lanka coefficients). Primary = common-complete M1–M5 h=4 test **n=13,361**, prevalence **0.375**; GID_2 cluster bootstrap seed 20260612, **B=1000, 0 failures**.
- **Climate-only (M2/M3) worse than M1** (M2 AUC 0.556, M3 0.564 vs M1 0.685; ΔAUC CIs exclude 0; ≈ treat-all at p\*=0.30).
- **Hybrid improves over M1:** M4 AUC 0.699 / NB 0.129; **M5 AUC 0.726 / NB 0.136** vs M1 AUC 0.685 / NB 0.117.
- **M5 vs M1: ΔAUC +0.040 [0.024, 0.058]; ΔNB@0.30 +0.018 [0.012, 0.026]** (both CIs exclude 0). M4 vs M1 also CI-excludes-0.
- **Caveat retained:** test-period over-prediction (CITL ≈ −0.5; COVID-era 2020–2022, though reporting did not collapse). ΔNB (within-test) is the robust contrast. **Not global validation.**

## 5. Cross-country conclusion
- **Recent surveillance is a strong benchmark in both settings.**
- **Climate-only dengue EWS is weak/insufficient relative to recent surveillance.**
- **Climate is most useful as an add-on to recent surveillance, not a standalone replacement.**
- **Colombia supports hybrid incremental value** (confirmed ΔAUC and ΔNB).
- **Sri Lanka shows climate value is not guaranteed** — it depends on setting, baseline surveillance strength, horizon, and decision threshold. The arms are **complementary, not contradictory** (same framework; different settings/labels/denominators).

## 6. Recommended manuscript headline (3 options)
- **A (conservative):** *"Recent-case surveillance is a hard-to-beat benchmark for dengue early warning; climate's contribution is incremental, hybrid-only, and setting-dependent under decision-curve evaluation."*
- **B (balanced — preferred):** *"Decision-curve evaluation of dengue early warning shows recent surveillance dominates climate-only models, while hybrid climate–surveillance models can add setting-dependent value."*
- **C (slightly stronger):** *"Climate alone is not enough: decision-curve external replication shows climate adds value to dengue early warning only when integrated with recent surveillance."*
- **Avoid:** "Climate predicts dengue", "Climate model outperforms surveillance", "Global validation", "Deployment-ready dengue early warning".

## 7. Claims supported
- Recent-case surveillance is a **hard-to-beat operational benchmark**.
- Climate EWS models **should not be evaluated only against weak/null baselines**.
- **Hybrid climate + surveillance improves discrimination AND net benefit in Colombia**.
- **Net benefit and calibration are essential** (AUC alone can mislead).
- **External framework replication is feasible** with OpenDengue + CHIRPS + ERA5-Land.
- **Temporal and spatial data alignment** (WER ISO-week alignment; GID_2 crosswalk; gap-free climate grid) are substantive **methodological contributions**.

## 8. Claims NOT supported (explicit)
- Climate-only outperforms recent surveillance.
- Universal climate value across settings.
- Global validation · deployment readiness · causal effect of climate · cost-effectiveness.
- That Colombia erases the Sri Lanka caution.
- That AUC improvement alone proves operational utility.

## 9. Main figures / tables plan (implementation-ready)
**Main figures**
- **Fig 1 — Study design & decision-evaluation framework:** data → labels → model ladder → calibration/DCA/net-benefit → cluster bootstrap; Sri Lanka primary + Colombia replication arms.
- **Fig 2 — Sri Lanka WER date-alignment schematic:** v1 vs v2 linkage (ISO-week ↔ WER issue offset) and its impact — the methodological-lesson figure.
- **Fig 3 — Sri Lanka decision curves / ΔNB:** net benefit vs threshold for M0–M5; ΔNB(hybrid − M1) with CIs.
- **Fig 4 — Colombia M0–M5 test panel:** (a) AUC with bootstrap CIs; (b) calibration plots (raw vs recalibrated); (c) decision curve p=0.05–0.50; (d) ΔNB@0.30 vs M1 forest plot.
- **Fig 5 — Cross-country summary:** climate-only vs recent-surveillance vs hybrid, side-by-side (AUC + NB@0.30), both settings — the one-glance headline figure.

**Main tables**
- **Table 1 — Data sources & cohorts:** Sri Lanka vs Colombia (source, unit, period, n, prevalence, climate inputs, label rule).
- **Table 2 — Model ladder M0–M5 definitions** (features per model; identical structure both arms).
- **Table 3 — Primary test metrics:** AUC / PR-AUC / Brier / CITL / slope / NB@0.30 + ΔAUC/ΔNB vs M1, both settings.
- **Table 4 — Supported vs unsupported claims / operational interpretation.**

**Supplement candidates**
- Full DCA threshold curves; bootstrap-CI tables; horizon/label sensitivity; calibration belts; data-quality/crosswalk details (incl. Socorro/Palmas-del-Socorro fold, island exclusions); TRIPOD/PROBAST + WHO-aligned reporting checklist.

## 10. Single most important remaining sensitivity — RECOMMENDED: **Colombia horizon sensitivity (h = 1, 2, 4, 8, 12)**

### 10.1 Evidence basis (documented Consensus search, 2026-06-18)
- **Beal et al. 2025, *GeoHealth*** — *Colombia cities (Cali, Cúcuta, Medellín, Leticia)*: hydroclimate-based models are **particularly skillful at 3- and 6-month lead times, where autoregressive models often fail**, and climate is **most beneficial when recent-case autoregressive relationships are weak**. (Near-direct prior for this arm.)
- **Johansson et al. 2016, *Scientific Reports* (Mexico):** climate did not improve seasonal AR overall; **short-term autocorrelation drives short-lead skill, seasonal structure drives long-lead skill** → skill is horizon-structured.
- **Colón-González et al. 2021, *PLoS Medicine* (Vietnam)** and EWARS reviews: climate/lagged-case ensembles add value at **1–6 month** leads; case-only models excel at ≤1 week.
- *Verify DOIs at manuscript stage; titles/journals/years are from the Consensus index.*

### 10.2 Why horizon is the right single choice
- It tests the **mechanistic, falsifiable prediction**: recent cases dominate at short leads (strong autocorrelation), but their advantage **decays at longer leads where climate's leading-indicator value emerges**. Our committed result is **h=4 (short)**; extending to **h=8/12** directly asks whether the hybrid/climate increment **grows** at operationally useful longer lead times.
- It is **directly anchored in Colombia evidence** (Beal 2025) and sharpens the paper's core narrative (climate is conditionally useful, lead-time dependent).
- It is **low-risk and assumption-free for us:** labels h=1/2/8/12 are **already constructed and committed**, and the feature/model pipeline is identical — no new data, no new modeling decisions, no delay-distribution assumptions.

### 10.3 Why NOT delayed-surveillance (evaluated, as requested) — strong runner-up
- Delayed surveillance is genuinely manuscript-relevant: the reporting-delay/nowcasting literature (**Bastos 2017 *Stat Med*; McGough 2020 *PLoS Comp Biol* (NobBS); Sylvestre 2022 *PLoS NTD***) shows recent-case data are systematically **delayed/incomplete in real time**, so M1's advantage may be **optimistic** under realistic latency — a fair-baseline critique reviewers will raise.
- **But** OpenDengue provides *finalized* counts, not real-time **reporting-delay vintages** for Colombia, so a delayed-surveillance analysis would be a **hypothetical scenario** (e.g., drop `cases_lag0`/shift lags) resting on an **unmeasured delay assumption** — weaker and more speculative than horizon, which uses already-built labels.
- **Recommendation:** run **horizon (h=1/2/4/8/12)** as the single primary next sensitivity; keep **delayed-surveillance as a supplementary robustness scenario** (clearly framed as assumption-based), and the secondary climate-only full-row write-up (already computed) as supplement. **Do not run now.**

## 11. Abstract-style results paragraph (draft — cautious)
> Across two settings evaluated with a pre-specified decision-curve and calibration framework, a recent-case surveillance baseline was difficult to beat. In Sri Lanka, climate-only models did not clearly outperform surveillance and hybrid gains were limited and threshold/regime-dependent. In an external framework replication in Colombia (h=4 weeks; common-complete test n=13,361; outbreak prevalence 0.375), climate-only models underperformed surveillance, whereas a hybrid climate–surveillance model improved both discrimination and net benefit over surveillance alone (M5 vs surveillance: ΔAUC +0.040, 95% CI 0.024–0.058; Δ net benefit at p\*=0.30 +0.018, 95% CI 0.012–0.026; municipality-cluster bootstrap, 0/1000 failures). Improvements were incremental and hybrid-specific; climate alone added no operational value over a treat-all default. Test-period calibration drift (a COVID-era window) tempers absolute estimates but not the within-test contrasts. Climate appears to add value to dengue early warning conditionally — as a complement to recent surveillance, not a standalone replacement.

## 12. Discussion paragraph (draft — why mixed ≠ contradictory)
> The Sri Lanka and Colombia results are complementary rather than contradictory. Both deliver the same core lesson — recent-case surveillance is a strong benchmark and climate alone is insufficient — which is precisely the comparison under-tested in much of the climate-EWS literature. They differ in whether the *hybrid* increment reaches significance at the registered decision threshold: Sri Lanka's targeted-value signal was power-limited and regime-dependent, while Colombia's larger panel yielded a confirmed hybrid net-benefit gain. This is consistent with a setting-dependent picture in which climate information is partly **redundant** with recent cases where surveillance autocorrelation is strong, but **complementary** where it is weaker or at longer lead times — a pattern the broader literature attributes to climate acting as a *leading* indicator. The implication is incremental, integrative climate value under rigorous decision-analytic, calibration-aware, surveillance-benchmarked evaluation — not universal climate-model superiority.

## 13. Updated implementation roadmap
- **Phase 1 — completed:** Sri Lanka analysis; Colombia infrastructure (climate linkage, crosswalk, labels, features); Colombia M0–M5 model ladder.
- **Immediate next:** commit this cross-country memo; decide the one sensitivity (recommended: **horizon h=1/2/4/8/12**).
- **Before manuscript submission:** run the one selected sensitivity; draft main figures/tables; write the manuscript outline; reviewer-facing limitations paragraph.
- **Do NOT implement now:** more countries; SHAP; formal mediation; cost-effectiveness; serotype/entomology/socioeconomic predictors; top-tier-journal claim.

## 14. Confirmation
- **No new analyses run. No models run. No metrics computed. No labels/thresholds recomputed. No data modified. No quarantine outputs modified.**
- **Interpretation/planning memo only.** No global-validation/deployment/causal claim.
- **No data files committed** — only this markdown memo is proposed for commit (pending approval). Literature claims are grounded in the documented Consensus search; DOIs to be finalized at manuscript stage.
