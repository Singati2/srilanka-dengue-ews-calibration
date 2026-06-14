# Literature Landscape & Repositioning Memo (v1)
*Citation-verified positioning of the Sri Lanka dengue-EWS calibration/decision-evaluation study against the 2022–2026 literature. **No models run; no metrics computed; no data modified.** Documentation only. Citations in §2 were **independently verified this session by fetching the journal page / confirming the DOI**; anything not so verified is quarantined in §3 ("do not cite yet"). No claim of a forecasting win.*

**Date:** 2026-06-14 · **Verification method:** web retrieval of journal/DOI pages (Consensus academic search used for discovery only; DOIs confirmed separately).

## 1. Executive positioning (honest niche)
- **Not** a new winning climate EWS; **not** a full operational deployment trial; **not** an external-validation study (no second dataset analyzed yet).
- **What it is:** a reproducible, preregistered evaluation of *existing model classes* for dengue early warning in Sri Lanka (26 RDHS × epi-week, 2018–2025) that demonstrates **why date-aligned linkage, calibration, decision-curve/net-benefit analysis, and a strong recent-case baseline matter** — an evaluation lens that is standard in clinical prediction modelling but largely **absent in the dengue-EWS literature**.
- **On climate:** climate signal is real (a DLNM-style cross-basis significantly beats simple climate logistics; a hybrid M5 is a near-miss on net benefit), but **operational superiority over the recent-cases baseline is not confirmed** unless the strict ΔNB criteria are met — and in this pilot they were not.
- **Core transferable contributions:** (i) the WER issue-number↔ISO-week date-alignment pitfall + fix; (ii) a reproducible, checksummed RDHS-week dengue–climate–denominator resource; (iii) a calibration + decision-curve + recalibration + PROBAST/TRIPOD evaluation of dengue EWS model classes.

## 2. Verified literature table (DOI-confirmed this session)
| Citation | Year | Setting | Model class | Data | Eval metrics | Calibration? | DCA / net benefit? | Relevance to us | DOI / URL |
|---|---|---|---|---|---|---|---|---|---|
| Clarke et al., *Scientific Data* (OpenDengue) | 2024 | Global, 102 countries | Data resource (no model) | Dengue case counts, weekly/monthly; subnational for 40 countries; 1924–2023 | n/a | n/a | n/a | The realistic **external-validation data source** for a multi-country transportability arm (note: **no Sri Lanka subnational**) | [10.1038/s41597-024-03120-7](https://www.nature.com/articles/s41597-024-03120-7) · [opendengue.org](https://opendengue.org/) |
| Schlesinger et al., *Front. Public Health* (EWARS-csd) | 2024 | Colombia (11 municipalities) | **DLNM + INLA Bayesian** | Climate (temp, rain) + weekly hospitalizations | Sensitivity/specificity/PPV/NPV | Operational alarm-threshold tuning (not probabilistic calibration) | No | The **canonical operational climate EWS** = the benchmark a reviewer will demand vs our Python DLNM approximation | [10.3389/fpubh.2024.1323618](https://doi.org/10.3389/fpubh.2024.1323618) · PMID 38314090 |
| Khamthong & Phramrung, *PLoS NTD* | 2026 | Thailand (Kanchanaburi) | Bayesian negative-binomial dynamic regression, lagged climate | Monthly DHF + max temp, RH | LOO-CV, posterior predictive checks | Posterior predictive checks | No | **Spatial representativeness of climate inputs > marginal association; explanatory ≠ predictive** — directly supports the geomatics exposure/MAUP work | [10.1371/journal.pntd.0014270](https://journals.plos.org/plosntds/article?id=10.1371/journal.pntd.0014270) |
| Beal et al., *GeoHealth* | 2025 | Colombia (4 cities) | Hydroclimate statistical forecast vs autoregressive | Monthly dengue + hydroclimate, SST | Forecast skill at 1/3/6-mo lead | No | No | **Key corroboration:** hydroclimate skillful at 3–6-mo lead *when AR models fail*; most useful when incidence low / autocorrelation weak — independently confirms our horizon-dependence result | [10.1029/2024GH001325](https://doi.org/10.1029/2024GH001325) · PMID 40901247 |
| Gulati et al., *Circ. Cardiovasc. Qual. Outcomes* | 2022 | Multi (CVD trial cohorts) | 104 clinical prediction models | Trial data | Discrimination + calibration + **net benefit** | Yes | **Yes** | **Methods anchor:** external validation degrades performance; 91% of models risk net harm at some threshold; **recalibration (intercept/slope) mitigates** — mirrors our calibration-drift + rolling-recalibration finding | [10.1161/CIRCOUTCOMES.121.008487](https://www.ahajournals.org/doi/10.1161/CIRCOUTCOMES.121.008487) · PMID 35354282 |
| Benitez-Aurioles et al., *Diagn. Progn. Res.* | 2026 (arXiv 2024) | Methods (CVD examples) | Prediction-model evaluation methodology | n/a | **Continuous net benefit** (area under decision curve over thresholds) | n/a | **Yes (extends DCA)** | Formal basis for our **threshold-band (p\*=0.20–0.40) DCA reporting** | [10.1186/s41512-026-00224-z](https://doi.org/10.1186/s41512-026-00224-z) |

**Verified count: 6.** These cover the user's "at minimum verify" set (OpenDengue, EWARS-csd, Khamthong, continuous net benefit) plus the two strongest corroborations (Beal, Gulati).

## 3. Unverified / do not cite yet (retrieved via academic search; DOI NOT independently confirmed this session)
*These came from a peer-reviewed academic search engine (Consensus over Semantic Scholar/PubMed/Scopus/ArXiv) and are very likely real, but were **not** independently DOI-verified here. **Verify each DOI before citing in the manuscript.***
| Label | Claimed finding (as retrieved) | Status |
|---|---|---|
| Finch et al., *Nat. Commun.* 2024 — Singapore serotype + climate | Serotype/immunity raises skill beyond climate (54%→60% vs seasonal baseline) | Verify DOI before citing |
| Fletcher et al., *Lancet Planet. Health* 2025 — Barbados compound extremes | Long/short-lag climate interactions; real deployment; TPR 81% vs 68% baseline | Verify DOI before citing |
| Hu et al., *BMC Med. Res. Methodol.* 2026 — PROBAST/TRIPOD-AI review | Of 14 prediction-model studies, 1 used DCA, none assessed fairness | Verify DOI before citing |
| Cox et al., *Crit. Care Med.* 2022 | "Preserved discrimination but poor calibration; improved after recalibration" | Verify DOI before citing |
| Naderalvojoud et al., *JAMIA Open* 2025 | Base-rate shift (14.7%→34.3%) degrades net benefit; retraining fixes | Verify DOI before citing |
| Baharom et al. 2022; Sutriyawan et al. 2025; da Costa et al. 2026 — dengue EWS reviews | Climate (temp/rain) most-used; ML (RF/LSTM) > ARIMA/Poisson; data-quality & TRIPOD gaps | Verify DOI before citing |
| Nguyen 2022; Chen 2025; Lu 2024; Tuan 2024/2025; others — DL/mobility dengue | LSTM/XGBoost/mobility-augmented forecasting; external validation uncommon | Verify DOI before citing |
*Also: any citation referenced in the earlier chat "council" response that is not in §2 is, by definition, **unverified** and lives here until DOI-checked.*

## 4. How the literature changes our framing (bullets)
**Aligned with the field:**
- Our horizon-dependence (AR strong at short lead; climate's value at longer lead / low incidence) matches Beal 2025 (verified).
- Our calibration-drift-correctable-by-recalibration result matches Gulati 2022 (verified) and (unverified) Cox 2022 / Naderalvojoud 2025.
- Our exposure/representativeness concern matches Khamthong & Phramrung 2026 (verified).

**Weaker than the field:**
- Climate comparator is a **Python cross-basis approximation, not DLNM+INLA / EWARS-csd** (Schlesinger 2024, verified).
- No serotype/immunity (Finch 2024, unverified) and no human-mobility signal.
- Single country, single period, retrospective; **no external validation** yet.

**Novel relative to the field:**
- DCA / net benefit is essentially **absent** in dengue EWS (which reports RMSE/sens/spec/AUC); we import it. Continuous net benefit (Benitez-Aurioles, verified) formalizes our band reporting.
- The WER date-alignment pitfall + fix appears undocumented in this literature.
- A fully reproducible, checksummed, preregistered pipeline with PROBAST/TRIPOD self-assessment — rare in this field.

**Likely reviewer attacks:**
- "Your climate model is not a real EWS (not DLNM+INLA)." → add EWARS-style comparator or scope explicitly.
- "Single country / no external validation." → OpenDengue transportability arm.
- "Finding is unsurprising (AR wins short-term)." → reframe as decision-evaluation + corroboration, cite Beal.
- "Exposure is area-averaged, not population-weighted." → Khamthong-motivated MAUP sensitivity.

**Safest claims:** see §5.

## 5. Strongest defensible claims (supported by our committed evidence + verified literature)
- **Date alignment matters** — WER issue number ≠ ISO week (year-varying 1–2-wk offset); naive joins misalign climate and outcome (our committed linkage/anomaly reports).
- **Recent surveillance is a hard baseline to beat at short lead** — M1 dominates climate classes on AUC and net benefit at h≤4 (our committed CI report; corroborated by Beal 2025).
- **Climate signal exists but needs fair evaluation** — DLNM-style cross-basis significantly beats simple climate logistics; hybrid M5 is a near-miss (our committed DLNM/hybrid reports).
- **Calibration drift and recalibration matter** — under-prediction across 2023–2025 corrected by rolling-52 recalibration (our committed recalibration report; method anchored by Gulati 2022).
- **DCA / net benefit adds value beyond AUC** — discrimination and decision value diverge across thresholds (our committed pilot; method anchored by Benitez-Aurioles 2026, Gulati 2022).
- **Exposure / spatial representativeness is important** — motivates population-weighted exposure + MAUP sensitivity (Khamthong & Phramrung 2026, verified).

## 6. Claims to avoid
- ❌ Do **not** claim climate has no value (it carries signal; DLNM beats simple climate models).
- ❌ Do **not** claim "climate EWS generally fails" (operational climate EWS like EWARS-csd perform well elsewhere; we did not test them).
- ❌ Do **not** call it "DLNM" / "canonical R dlnm" — it is a **Python cross-basis approximation**.
- ❌ Do **not** claim a model-winning result unless the strict ΔNB criteria (CI excludes 0, band-robust) are met — they were not.
- ❌ Do **not** claim external validation unless OpenDengue (or another dataset) is actually analyzed.
- ❌ Do **not** claim deployment readiness (no prospective/real-time test).

## 7. Upgrade decision table
| Upgrade | Reviewer problem addressed | Effort | Risk | Likely payoff | Needed before 1st submission? |
|---|---|---|---|---|---|
| **A. DLNM+INLA / EWARS-style comparator** | "Strawman climate model" (Schlesinger 2024) | High (needs R install + INLA) | Medium (env setup; may still lose to M1) | High (kills the main attack) | **Strongly recommended** — or scope claim explicitly |
| **B. Population-weighted / MAUP geomatics exposure sensitivity** | "Area-averaged exposure unrepresentative" (Khamthong 2026) | Medium (geomatics engineer; already-quarantined rasters) | Low | Medium-High (real methods result, your geomatics deliverable) | **Recommended** |
| **C. OpenDengue external-validation arm** | "Single country / no external validation" | Medium-High (new data ingest, national-level) | Medium (OpenDengue lacks SL subnational; transportability of *evaluation finding* only) | High (addresses field's #1 gap) | Recommended; could be a strong supplement |
| **D. p\* cost-anchoring narrative** | "p\*=0.30 arbitrary" | Low (team-written + a cited cost rationale) | Low | Medium | **Yes — cheap, do it** |
| **E. Continuous net benefit across band** | "Single-threshold cherry-pick" (Benitez-Aurioles 2026) | Low (compute on existing predictions) | Low | Medium | **Yes — cheap, do it** |

## 8. Recommended next action
- **Before manuscript writing (do now):** D (p\* anchoring narrative) and E (continuous net benefit) — cheap, low-risk, directly close two reviewer attacks; B (population-weighted exposure + MAUP) as the geomatics engineer's headline methods contribution.
- **Strongly consider before first submission:** A (EWARS-style DLNM+INLA comparator) — the single highest-value upgrade for credibility; requires a gated R/INLA install decision. If declined, the manuscript must scope every climate claim to "model classes including a DLNM-style cross-basis approximation."
- **Can wait for supplement / future study:** C (OpenDengue external-validation arm) — valuable but larger; can be a supplement or the seed of the confirmatory study justified by the M5 near-miss.
- **Do not do now:** chase a forecasting "win"; add serotype/mobility (out of current data scope); claim deployment readiness.

## 9. Confirmation
- **No models run; no metrics computed; no data modified.**
- **No files created except this markdown memo.** No data committed.
- All §2 citations were DOI-verified this session; all unconfirmed items are quarantined in §3. No forecasting-win claim is made. Preregistration unchanged.
