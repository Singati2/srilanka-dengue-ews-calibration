# Literature Positioning Memo v2 — Targeted Value of Climate Information for Dengue EWS (2020–2026)
*An **expanded 2020–2026 scoping review of directly relevant literature** (not a PRISMA systematic review; no formal screening/eligibility protocol followed) to decide exactly how this paper should land **before any further analysis**. **No models run; no metrics computed; no data modified.** Supersedes `docs/literature_landscape_repositioning_v1.md` (commit ecbf0d8). Verified citations carry DOIs (independently confirmed this session); unverified retrievals are quarantined in §2b ("do not cite yet").*

**Date:** 2026-06-14 · **Verification:** journal/DOI pages fetched for the §2a anchors. Discovery via academic search (Semantic Scholar/PubMed/Scopus/ArXiv); ~60 papers screened, 10 anchors DOI-verified.

## 1. Final landing statement (one paragraph)
This paper is **not** a winning climate-forecasting-model paper, **not** a deployment trial, and **not** an external-validation study. It is a **2026-aligned decision-analytic framework for estimating the *targeted value of climate information*** — when and where adding climate to a strong recent-dengue-surveillance baseline yields operational **net benefit** — in a reproducible Sri Lanka RDHS × epi-week setting (2018–2025). Its spine is **conditional net benefit** (by lead time, incidence regime, local autocorrelation regime, and **spatial heterogeneity**), built on a **date-aligned WER linkage** (correcting an undocumented issue-number↔ISO-week pitfall), with **calibration/recalibration** and **reproducibility** treated as first-class, rather than the field's usual forecast-accuracy/alarm-performance lens.

## 2a. Literature map 2020–2026 — DOI-verified anchors (10)
| Paper | Year | Setting | Data source | Model class | Horizon | Eval metrics | Calibration? | Net benefit / DCA? | External val.? | Relevance | DOI/URL | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Karasinghe et al. | 2024 | Sri Lanka (Colombo) | **WER** | ARIMA(2,1,0)+AR16 | 1-wk weekly | AIC/SBIC, fit error | No | **No** | No | **Direct Sri Lanka precedent on same WER source** — single district, time-series only; we extend to RDHS-wide climate linkage + decision value | [10.1371/journal.pone.0299953](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0299953) | ✓DOI |
| Wu et al. | 2025 | Global, 180+ locations | Multi-country surveillance | Mechanistic+stat+ML ensembles | 1–3 mo | CRPS/relative skill | Partial (probabilistic) | **No** | Yes (prospective) | "No single model wins"; **strong baselines** — corroborates M1-hard-to-beat; not conditional decision value | [10.1073/pnas.2422335122](https://www.pnas.org/doi/10.1073/pnas.2422335122) | ✓DOI |
| Beal et al. | 2025 | Colombia (4 cities) | Surveillance + hydroclimate/SST | Hydroclimate stat vs autoregressive | 1/3/6 mo | Forecast skill | No | **No** | No | **Key corroboration:** climate skillful at long lead / low incidence / weak AR — our horizon-dependence | [10.1029/2024GH001325](https://doi.org/10.1029/2024GH001325) | ✓DOI |
| Schlesinger et al. (EWARS-csd) | 2024 | Colombia (11 munic.) | Climate + hospitalizations | **DLNM + INLA Bayesian** | weeks ahead | Sens/spec/PPV/NPV | Alarm-threshold tuning | **No** | Validation study | **The operational climate-EWS benchmark** we must add or scope against | [10.3389/fpubh.2024.1323618](https://doi.org/10.3389/fpubh.2024.1323618) | ✓DOI |
| Khamthong & Phramrung | 2026 | Thailand | DHF + station climate | Bayesian NB dynamic regression | monthly | LOO-CV, PPC | PPC | **No** | No | **Spatial representativeness > marginal association; predictive ≠ explanatory** — grounds geomatics axis | [10.1371/journal.pntd.0014270](https://journals.plos.org/plosntds/article?id=10.1371/journal.pntd.0014270) | ✓DOI |
| Clarke et al. (OpenDengue) | 2024 | Global, 102 countries | Public case counts | Data resource | n/a | n/a | n/a | n/a | n/a | **External-validation data source** (no Sri Lanka subnational) | [10.1038/s41597-024-03120-7](https://www.nature.com/articles/s41597-024-03120-7) | ✓DOI |
| Leung et al. (systematic review) | **2023** | Global (64 studies, 99 models) | Mostly climate | Stat + ML | mixed | Accuracy/AUC/sens-spec | Rarely | **Rarely/none** | **5.2% only** | Field-wide evidence: climate-dominated, weak validation, poor reporting | [10.1371/journal.pntd.0010631](https://journals.plos.org/plosntds/article?id=10.1371/journal.pntd.0010631) | ✓DOI (note: 2023, not 2022) |
| Hussain-Alkhateeb et al. (scoping review) | 2021 | Global (37 studies) | Climate/entomology/epi | EWS tools | mixed | Prediction validity | Rarely | **No** | Rare | Gap: "transforming model outputs into local action"; spatial prediction limited | [10.1371/journal.pntd.0009686](https://journals.plos.org/plosntds/article?id=10.1371/journal.pntd.0009686) | ✓DOI |
| Gulati et al. | 2022 | Multi (CVD cohorts) | Trial data | 104 clinical prediction models | n/a | Discrimination+calibration+**net benefit** | Yes | **Yes** | 158 validations | Methods anchor: validation degrades performance; 91% risk net harm at some threshold; recalibration mitigates | [10.1161/CIRCOUTCOMES.121.008487](https://www.ahajournals.org/doi/10.1161/CIRCOUTCOMES.121.008487) | ✓DOI |
| Benitez-Aurioles et al. | 2026 | Methods (CVD) | n/a | Prediction-model evaluation | n/a | **Continuous net benefit** | n/a | **Yes** | n/a | Formal basis for our threshold-band (p\*=0.20–0.40) DCA | [10.1186/s41512-026-00224-z](https://doi.org/10.1186/s41512-026-00224-z) | ✓DOI |

## 2b. Unverified retrievals — DO NOT CITE YET (verify DOI before use)
Retrieved via academic search (real papers, URLs available) but **not independently DOI-verified** this session:
- **Sesay et al. 2026** (Freetown; BiLSTM-NB vs baselines; **lag-1 climate gains non-significant** — strong corroboration) — verify.
- **Evans et al. 2024** (dengue **label/prevalence-shift detection + recalibration** — strong calibration anchor) — verify.
- **Rumack et al. 2021** (recalibrating epidemic forecasts, FluSight) — verify.
- **Kiang et al. 2020** (Thailand mobility; "no single model wins") — verify.
- **Phung et al. 2025** (Nat Commun "3-U useful/usable/used" — operational decision-relevance gap) — verify.
- **Finch et al. 2024** (Nat Commun serotype+climate) — verify.
- **Bracher et al. 2020** (WIS interval scoring) — verify.
- **Colón-González 2021** (PLoS Med superensemble vs baseline), **Areed 2024**, **Liu 2026** (ST-GAT), **Thayer 2025** (Puerto Rico thresholds), **Baharom 2022**, **Sebastianelli 2024**, **Villanueva-Miranda 2025** — verify each before citing.
*Any citation not in §2a is unverified by definition.*

## 3. Are we scooped? (strict)
**No.**
- **Karasinghe 2024** overlaps on **Sri Lanka WER + autoregressive forecasting**, but is **Colombo-only, time-series ARIMA, forecast-accuracy only**. It does **not** address RDHS-wide climate linkage, the date-alignment pitfall, calibration/recalibration, decision-curve/net benefit, DLNM-style climate comparison, the hybrid near-miss, or targeted value-of-climate. It is a **precedent we extend and cite**, not a scoop (it even validates WER as a source and a recent-cases baseline).
- **Wu 2025 / global ensemble papers** focus on **average forecast performance and ensembling**, not the **conditional decision value of climate** over a surveillance baseline. Not a scoop; corroborates our baseline-strength point.
- **EWARS-csd (Schlesinger 2024)** is the operational **DLNM+INLA climate EWS**, but it is a **benchmark to add or explicitly scope against**, not a study of targeted value-of-climate in net-benefit terms. Not a scoop.

## 4. Gap statement (three levels)
- **A. Evaluation gap:** Dengue EWS overwhelmingly reports **forecast accuracy (CRPS/RMSE/MAE), discrimination (AUC), or alarm sensitivity/specificity/PPV** — **not** decision-curve net benefit or calibration/recalibration (verified anchors Leung 2023, Hussain-Alkhateeb 2021; a targeted search for DCA-in-dengue returned none). Clinical prediction has long adopted net benefit (Gulati 2022; Benitez-Aurioles 2026); dengue EWS has not.
- **B. Incremental-value gap:** The literature asks *whether climate helps forecasting*; it rarely asks *whether climate adds operational decision value beyond a strong recent-surveillance baseline* (Beal 2025 shows skill regime-dependence; Sesay 2026 [unverified] shows non-significant climate gains — but neither in net-benefit terms).
- **C. Targeting gap:** No conditional **"when and where is climate worth adding?"** framework exists, jointly using **lead time, local autocorrelation regime, incidence regime, and spatial heterogeneity**.

## 5. Our contribution (three legs)
1. **Data/resource:** a **date-aligned Sri Lanka WER RDHS-week dengue–climate–population panel**, with the documented **WER issue-number vs ISO-week pitfall** + fix (reproducible, checksummed; Karasinghe 2024 used the same source without this).
2. **Evaluation:** **calibration, recalibration (rolling), decision-curve / net benefit, continuous net benefit**, and **strict recent-case baseline comparisons with CIs** — imported, for the first time to our knowledge, into climate-dengue EWS.
3. **Novel estimand — targeted value of climate information:**
   **ΔNB_climate(p\*, z) = NB(surveillance + climate | p\*, z) − NB(surveillance only | p\*, z)**, conditional on **z = {lead time, incidence regime, AR regime, RDHS/spatial structure}**, with RDHS-cluster bootstrap CIs and a BYM2-smoothed per-division value surface.

## 6. Title & abstract positioning
**Three candidate titles:**
1. *Targeted value of climate information for dengue early warning: a decision-curve and calibration re-evaluation in Sri Lanka (2018–2025).*
2. *When and where is climate worth it? Conditional net benefit of climate information beyond recent dengue surveillance in Sri Lanka.*
3. *Beyond discrimination: decision-analytic evaluation of climate-driven dengue early warning and a date-aligned RDHS-week data resource.*

**Recommended:** **Title 1** (names the novel estimand + the evaluation lens + the setting; honest, not over-claiming).

**5-sentence abstract-positioning skeleton (intent per sentence — not finished prose):**
1. *Problem/field framing:* dengue EWS is evaluated on forecast accuracy/alarm performance; operational decision value and calibration are rarely assessed.
2. *What we do:* on a date-aligned Sri Lanka RDHS-week panel, we evaluate existing model classes with calibration, recalibration, and decision-curve net benefit, and define the targeted value of climate information.
3. *Key result 1 (honest):* a recent-case baseline is hard to beat at short lead; climate's incremental net benefit is conditional (regime/space), not an overall win; the hybrid is a near-miss.
4. *Key result 2:* calibration drift under base-rate shift is real but recalibration-correctable; date alignment materially changes the linkage.
5. *Contribution/scope:* we provide a reusable resource and a conditional value-of-climate framework; single-country, no external validation, climate component is a DLNM-style approximation.

## 7. Reviewer attack table
| Likely criticism | Why they'll say it | How we answer | More analysis needed? |
|---|---|---|---|
| Single-country, not generalizable | One setting, retrospective | Scope as Sri Lanka decision-analytic framework; OpenDengue external arm planned | Optional (external arm) |
| Python DLNM-style ≠ canonical R `dlnm`/EWARS | Operational benchmark is DLNM+INLA (Schlesinger 2024) | Add EWARS/INLA comparator **or** scope every climate claim as "DLNM-style approximation" | Recommended (INLA comparator) |
| M5 is a near-miss, not a win | ΔNB@0.30 CI just includes 0 | We **never** claim a win; report as discrimination gain without confirmed decision value | No (already done) |
| DCA is imported from clinical prediction | Method not new per se | Novelty is the **conditional value-of-climate estimand + regime map**, not DCA-as-method | No |
| No serotype/mobility | Finch 2024 (serotype), Kiang 2020 (mobility) add value | Acknowledge as scope/limitation; out of current data | No (future work) |
| Novelty overclaimed | "First" claims are risky | Hedge to "to our knowledge, per reviewed verified literature"; no absolute first | No |
| No external validation | Transportability unproven | State explicitly; OpenDengue arm as supplement/future | Optional |

## 8. Required vs optional before first submission
**Required before first submission:**
- **Stage 1A:** conditional ΔNB at **h=4** (on committed predictions; no refit).
- Clean manuscript positioning (this memo → Methods/Intro framing).
- **Cost-threshold / p\* justification** (anchor or band rationale).
- **Continuous net benefit over p\*=0.20–0.40** (Benitez-Aurioles 2026).
- **Explicit scope note** for the Python DLNM-style approximation.

**Strongly recommended (before submission if feasible):**
- **EWARS/INLA comparator** (requires gated R install decision).
- **Population-weighted / MAUP exposure sensitivity** (geomatics; Khamthong 2026).

**Future / supplement:**
- **OpenDengue external validation**; multi-country confirmatory study; serotype/mobility extensions.

## 9. Claims allowed vs forbidden
**Allowed:** climate signal exists; recent cases hard to beat at short lead; hybrid M5 is a near-miss (not a confirmed operational win); targeted value-of-climate is the novel estimand; date alignment materially matters; calibration/recalibration and net benefit change interpretation.
**Forbidden:** climate wins overall; M5 model-winning; "canonical R `dlnm`" (only Python approximation used); external validation without OpenDengue/another dataset analyzed; deployment-ready; absolute "first ever."

## 10. Final recommendation (strict go/no-go)
- **GO — worth continuing.** The direction is genuinely novel relative to the verified 2020–2026 literature, not scooped (Karasinghe 2024 differs in scope/question), and the two core findings are **independently corroborated** (Beal 2025; Wu 2025; Sesay 2026 [unverified]). Realistic landing: a solid PLoS NTD / PLOS Global Public Health / BMC Med Res Methodol-tier **decision-analytic + data-resource** paper — not Nature/Lancet, not a forecasting-win paper.
- **How it should land:** as **"targeted value of climate information"** (Title 1), carried by the conditional value-of-climate estimand + the calibration/decision-curve transfer + the WER date-alignment resource, with the EWARS comparator added or explicitly scoped.
- **Run next (after this memo, on approval):** **Stage 1A** — conditional ΔNB at h=4 on the committed predictions (cheapest, highest-signal; tells us if any regime shows positive CI-backed value-of-climate before investing in BYM2/geomatics).
- **Do NOT run now:** BYM2 spatial surface, population-weighted exposure rebuild, OpenDengue ingest, or any INLA install — all gated behind Stage 1A's result and your approval.

## Confirmation
- **No models run; no metrics computed; no labels created; no data modified; no Stage 1A/BYM2/spatial analysis run.**
- **Only this markdown memo was created.** Nothing committed. Preregistration unchanged. Novelty asserted relative to the reviewed verified literature, not as an absolute first.
