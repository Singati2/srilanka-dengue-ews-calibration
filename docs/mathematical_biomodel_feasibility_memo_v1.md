# Mathematical / Mechanistic Biological Dengue Model — Primary-Literature Feasibility Assessment

> **Correction addendum (2026-06-27).** Conclusion retained: **no biomodel is added** to the current manuscript. Two clarifications affirmed: (1) the trait-based temperature-suitability / R0(T) curves are **imported from published laboratory thermal-response studies and are not locally validated biology** for Sri Lankan or Colombian *Aedes*; this memo does not claim local entomological validation. (2) The only scope-compatible option (a mechanistic-statistical suitability covariate) is **explicitly reviewer-contingent or Paper-2 only** and is not implemented here. The manuscript includes a single concise Future Work sentence to this effect and builds no results section around it.

**Re:** Could a mathematical/mechanistic biological dengue transmission model be *credibly supported by THIS project's data*, and does it belong in this frozen evaluation paper?
**Date:** 2026-06-26
**Project state:** Analysis frozen (evaluation/decision-curve paper); locked decision **not** to pivot to mechanistic or forecasting model development.
**Method:** Primary-literature feasibility review. No model implemented, fit, or run. References below were checked against source venues; DOIs are verified except where explicitly labeled "(recollection)".
**Relationship to prior memo:** This is the fuller, citation-grounded successor to `docs/biomodel_feasibility_memo_v1.md`. It preserves that memo's verdict and extends it to the full six-candidate set (A–F) the task specifies, with a per-criterion decision-rule verdict for each.

---

## 0. The decision rule (applied explicitly to every candidate)

A mathematical biomodel is recommended for **this** manuscript **only if it satisfies all five**:

1. **Answers the existing question** — speaks to the surveillance-benchmark / decision-curve net-benefit comparison the paper is built on.
2. **Identifiable** — its parameters/states are estimable from the available data (not merely importable from literature, and not absorbed by a free reporting term).
3. **Validatable** — can be checked temporally (held-out weeks) **and** geographically (held-out units), in the way the paper already validates.
4. **Preserves the frozen endpoint** — does not change the binary, 4-week-ahead, train-period-75th-percentile alert outcome, the recalibration step, or the ΔNB scoring.
5. **Distinct test** — provides genuinely new evidence, not "a more flexible climate model" that re-expresses the DLNM/logistic climate signal already evaluated.

A candidate that fails any one of these is **not** added to this paper. The table in §3 records the verdict on each criterion.

---

## 1. Data reality (the binding constraint)

**Available:** weekly reported dengue case counts (Sri Lanka, 26 RDHS units, 2018–2025, ~10,500 unit-weeks; Colombia, ~1,100 municipalities via OpenDengue, **finalized — not real-time** counts); ERA5-Land weekly temperature (mean/min/max) + relative humidity; CHIRPS weekly precipitation; annual WorldPop denominators. Outcome = **binary 4-week-ahead alert** (incidence > train-period 75th percentile). Current models: L2 logistic ladder M0–M5 + a canonical R DLNM; scored by calibration + decision-curve net benefit vs a recent-case surveillance baseline.

**Absent (decisive):** serotype-resolved counts; seroprevalence / immunity / force-of-infection; entomological / vector indices (abundance, ovitrap/BG, biting rate, field mortality, field EIP); human mobility; vector-control / intervention records; observed reporting fraction.

This inventory produces one clean asymmetry that governs every verdict below:

- **Temperature-forced *rates* are importable.** Published *Aedes* thermal-trait curves (biting rate, parasite/virus development rate ≈ 1/EIP, adult mortality, fecundity, egg-to-adult survival) are mature enough to compute a relative R0(T)/vectorial-capacity transform from ERA5-Land temperature alone — *Mordecai 2017* (PLoS NTD 11(4):e0005568, doi:10.1371/journal.pntd.0005568) and *Huber 2018* (PLoS NTD 12(5):e0006451, doi:10.1371/journal.pntd.0006451).
- **Unobserved *states* are not recoverable.** The susceptible reservoir (no immunity/serotype), the entire vector limb (no entomology), and the reporting fraction (unobserved) trade off against one another — the classic dengue equifinality — and the binary alert outcome discards the magnitude/timing signal a dynamical estimator would need.

The Cambodia synthesis is the decisive empirical precedent for the "states-not-recoverable" half: *Brook et al. 2024* (PNAS 121(35):e2318704121, doi:10.1073/pnas.2318704121) show, on a 19-year serotyped + demographic dataset, that **climate-driven transmission alone is insufficient** to reproduce the observed epidemics — demography, serotype-specific immunity, and immune evasion are required. Our project has *none* of the data Brook et al. found necessary. Any climate-and-cases-only mechanistic dengue model is therefore building on a foundation the strongest recent primary literature has shown to be inadequate for the mechanistic claim.

---

## 2. Candidate-by-candidate assessment

### (A) Vector–host SEI–SEIR compartmental model

- **States/parameters:** Host S/E/I/R; vector S/E/I; bidirectional transmission probabilities (b·c), biting rate a(T), EIP/PDR(T), vector mortality μ(T), emergence/carrying capacity, host recovery/waning, S(0) immune fraction, and a reporting fraction ρ. Multi-serotype dengue additionally needs 4× serotype structure + ADE / cross-immunity.
- **Data needed for identification:** entomological time series (to break vector-abundance × force-of-infection × reporting confound), seroprevalence/serotype (to constrain S(0), waning, cross-immunity), and a reporting-fraction anchor. **All three are absent.**
- **Estimated vs imported:** the large majority of parameters would be *imported* from literature priors; the data (one noisy reported-case channel) constrain at most a reporting scale and one or two transmission multipliers.
- **Identifiability/equifinality:** structurally non-identifiable. R0 trades off against final attack size with no immunity data; the latent vector limb is confounded with ρ; flat profile-likelihood ridges; prior-dominated posteriors. *Reiner & Perkins 2013* (J R Soc Interface 10(81):20120921, doi:10.1098/rsif.2012.0921) catalog exactly this proliferation of under-identified Ross–Macdonald-family structures.
- **Validation:** would require a *continuous* incidence/timing target with reporting-delay correction; cannot be honestly validated against the binary alert without a re-thresholding pipeline the freeze forbids.
- **Answers the surveillance-benchmark question?** No — it asks a different (mechanistic-attribution) question.
- **This paper or separate project?** Separate project, and only with new data.
- **Post-hoc model-shopping risk:** **High** — many free structural choices, each with priors, invite tuning.
- **Burden:** Very high (hierarchical state-space/particle-MCMC build + identifiability diagnostics + new validation target).

### (B) Climate-dependent vectorial-capacity / temperature-dependent R0 (trait-based, Mordecai-style)

- **States/parameters:** No dynamical states — a deterministic transform R0(T) (or vectorial capacity VC(T)) assembled from thermal-trait response curves: a(T), PDR(T)=1/EIP, μ(T), EFD, pEA, etc.
- **Data needed:** temperature only — **fully present.** Trait curves come fixed from published Bayesian posteriors (*Mordecai 2017*; *Huber 2018*; Tesla/Ryan-family work).
- **Estimated vs imported:** **entirely imported.** Nothing in our data constrains a single trait parameter. The only quantity ever "estimated" is the index's regression coefficient *after* it enters the logistic ladder — which is candidate (E), not a mechanistic fit.
- **Identifiability/equifinality:** as a *suitability index* it is well-defined (closed-form); as a *transmission model* it is unidentified — absolute scale is meaningless, only relative/temporal shape is usable, and there is zero local entomological validation. Documented local *Aedes* thermal adaptation means imported curves could be locally miscalibrated with no way to detect it here.
- **Utility caveat specific to our sites:** Sri Lanka (~20–31 °C) and tropical Colombia sit near the **flat top** of R0(T) (optimum ≈ 29 °C in Mordecai 2017; Huber 2018 notes peak epidemic potential at 24–25 °C onset). The index is therefore near-saturated and **collinear with the lagged temperature already in M2–M5 and spanned by the DLNM cross-basis.** Areal-mean temperature input also incurs Jensen's-inequality aggregation bias on a nonlinear curve; precipitation/humidity have no thermal-trait analog and would enter as ad hoc multipliers.
- **Answers the surveillance-benchmark question?** Only if injected as a covariate — i.e. it *becomes* (E).
- **This paper or separate project?** As a standalone object it adds no identified evidence; as a feature it is (E). Paper-2 framing.
- **Post-hoc model-shopping risk:** Moderate (choice of which traits, which precip/humidity multipliers, which lags).
- **Burden:** Low to *compute*; but low-value here because of plateau collinearity.

### (C) Ross–Macdonald extension

- **States/parameters:** the classical a, m (vectors per host), b, c, μ (vector mortality), n (EIP), r (host recovery) → R0 = m a² b c e^(−μn) / (μ r). Extensions add seasonality, immunity, or stochasticity.
- **Data needed:** crucially **m** (vector-to-host ratio) and μ, n — i.e. entomology and field EIP. **Absent.** *Reiner & Perkins 2013* document that the m a² product and μ/n terms are jointly weakly identified even *with* entomological data; without it they are free.
- **Estimated vs imported:** vector terms imported or assumed; only a coarse transmission scale could be touched by the data, and it would be confounded with ρ.
- **Identifiability/equifinality:** the squared-biting-rate / vector-density degeneracy is textbook equifinality; no local entomology to break it.
- **Validation:** same continuous-target problem as (A); binary alert is the wrong target.
- **Answers the surveillance-benchmark question?** No.
- **This paper or separate project?** Separate; arguably weaker than (A) because R-M collapses dengue's multiserotype/immunity dynamics it cannot represent.
- **Post-hoc model-shopping risk:** Moderate–high.
- **Burden:** High (and low scientific yield given absent m).

### (D) Renewal-equation / state-space transmission model (EpiEstim / EpiNow2-style Rt; or particle-MCMC state-space)

- **States/parameters:** time-varying reproduction number Rt; a generation-interval / serial-interval distribution; (state-space variants add latent infections + an observation model with reporting delay).
- **Data needed:** an incidence series + a generation-interval prior — runnable **without** entomology or immunity. *Cori et al. 2013* (Am J Epidemiol 178(9):1505–1512, doi:10.1093/aje/kwt133); branching/renewal lineage from *Wallinga & Teunis 2004* (Am J Epidemiol 160(6):509–516, doi:10.1093/aje/kwh255).
- **Estimated vs imported:** Rt is estimated; the generation interval is imported (and a *temperature-dependent* GI would just re-import candidate-B thermal priors).
- **Identifiability/equifinality:** Rt itself is reasonably identified, **but two structural mismatches dominate.** (i) EpiEstim's instantaneous-Rt validity assumes reasonably timely incidence and a known reporting process; our Colombia counts are **finalized/non-real-time** and the reporting fraction is unobserved, so a real-time-style Rt nowcast is misaligned with the data-generating process and with the paper's *prospective-alert* framing. (ii) A climate-forced Rt is structurally an autoregression on recent cases (candidate M1) fused with a climate GLM on log-Rt (M2–M5) — it re-derives the paper's own thesis ("surveillance is hard to beat") through more expensive machinery.
- **Validation:** natively produces a *continuous* incidence/Rt nowcast, **not** the binary h=4 75th-percentile alert; converting requires a new re-thresholding pipeline the freeze forbids.
- **Answers the surveillance-benchmark question?** Only by re-expressing M1 + climate — not a *distinct* test.
- **This paper or separate project?** Separate (forecasting paper), or Paper-2.
- **Post-hoc model-shopping risk:** Moderate (GI choice, window length, threshold conversion).
- **Burden:** Moderate–high (new continuous target + delay handling).

### (E) Mechanistic-statistical hybrid — mechanistic index as a covariate in the existing framework

- **States/parameters:** none new — a *fixed* deterministic candidate-B index (relative R0(T)/VC(T)) enters the existing penalized-logistic ladder as one feature (with its 0–8 wk lags), all trait parameters frozen from literature.
- **Data needed:** temperature only — **present.** The downstream logistic layer absorbs scale, baseline reporting, and sign.
- **Estimated vs imported:** trait parameters imported; **one** free logistic coefficient estimated — fully identified, no dynamical system, no dependence on the absent data.
- **Identifiability/equifinality:** none, by construction. Honest caveat: the index's *value* still rests on the imported curves being roughly right for local *Aedes*; but a mis-scaled index degrades gracefully to "an extra nonlinear temperature feature," not a misidentified mechanism.
- **Validation:** **uses the identical frozen protocol** — same recalibration, same decision-curve ΔNB, same RDHS/GID_2 cluster-bootstrap, temporal + geographic.
- **Answers the surveillance-benchmark question?** **Yes** — directly, on the same evaluation rows.
- **Distinct test?** Marginally: it tests whether a *physiologically-shaped* climate feature beats surveillance where empirical splines did not. But the binding issue is **redundancy** — M2–M5 already carry temp_lag0..8 and the DLNM comparator already fits an ns(df=3) cross-basis over temp × lag 0–8 on the same rows. The single-peaked, plateaued index sits largely *within* that already-tested span. Non-redundancy (VIF/collinearity vs existing temp terms; incremental ΔNB over M4/M5 **and** the DLNM arm) is the empirical question, and the expected result is **null-to-flat** (consistent with the modest, plateaued climate increment already observed; Colombia ΔNB@p\*=0.30 ≈ +0.018 in prior runs).
- **This paper or separate project?** The *only* candidate that is scope-compatible at all — and even so its honest contribution is **interpretive/triangulation, not a metric gain**. Best as Paper-2 lead extension or a reviewer-contingent one-paragraph robustness arm.
- **Post-hoc model-shopping risk:** **Low-to-moderate, only if pre-specified** (one fixed index, fixed lags, the frozen pipeline). Unconstrained, the trait/lag/precip-multiplier choices reintroduce shopping risk — hence pre-registration is essential.
- **Burden:** Low (one deterministic feature reusing the exact frozen pipeline).

### (F) Climate-forced endemic–epidemic model (Held/Meyer `hhh4`, R `surveillance`)

- **States/parameters:** additive decomposition of conditional mean into **endemic** (covariate-driven, incl. climate + seasonality), **autoregressive** (within-unit, prior-week cases), and **neighbourhood/spatial** components; negative-binomial overdispersion; optional random effects. *Paul & Held 2011* (Stat Med 30(10):1118–1136, doi:10.1002/sim.4177); *Meyer & Held 2014* (Ann Appl Stat 8(3):1612–1639, doi:10.1214/14-AOAS743); `surveillance`/`hhh4` vignette (Meyer, Held & Höhle, J Stat Softw 2017, doi:10.18637/jss.v077.i11).
- **Data needed:** multivariate count time series + covariates + (optionally) an adjacency/neighbourhood matrix — **all present** (counts, climate, unit geography). No entomology/immunity required.
- **Estimated vs imported:** all components **estimated from our data** (this is the one mechanistically-flavored candidate that is genuinely identifiable here) — but "mechanistic" only in the loose branching-process-with-immigration sense; it is **not** a vector-host biological model. Its autoregressive term *is* essentially the recent-case surveillance signal, formalized.
- **Identifiability/equifinality:** well-behaved statistically (NB-GLM machinery). Risk is **conceptual, not numerical**: the endemic-climate vs autoregressive-case split is exactly the M2–M5-vs-M1 contrast the paper already runs, now with a spatial term.
- **Validation:** supports proper temporal one-step-ahead scoring and geographic/neighbourhood structure — compatible *in principle* — **but** it natively targets the *count* series, not the frozen binary 4-week-ahead 75th-percentile alert; scoring it on the frozen endpoint needs a thresholded-forecast conversion the freeze forbids, and `hhh4`'s native one-step-ahead horizon differs from h=4.
- **Answers the surveillance-benchmark question?** Partially and indirectly — it is closest of B–F to "a better surveillance+climate model," which is precisely why it is *not a distinct test*: it is a more flexible re-expression of the autoregressive-vs-climate decomposition already evaluated.
- **This paper or separate project?** Separate (a spatiotemporal-forecasting paper), or Paper-2. Note the project's existing DLNM comparator already represents the Lowe-style Bayesian spatiotemporal climate-lag approach (*Lowe et al. 2021*, Lancet Planet Health 5(4):e209–e219, doi:10.1016/S2542-5196(20)30292-8) at the level this evaluation needs.
- **Post-hoc model-shopping risk:** **High** — component on/off, lag/seasonality bases, neighbourhood weights, random effects = a large model space, with horizon/threshold conversions inviting tuning toward the frozen metric.
- **Burden:** Moderate–high (new model family, horizon alignment, endpoint conversion, new validation).

---

## 3. Decision-rule verdict table

Legend: ✓ = satisfied; ✗ = fails; ~ = partial/contingent.

| Candidate | (1) Answers benchmark Q | (2) Identifiable from data | (3) Temporal+geo validatable | (4) Preserves frozen endpoint | (5) Distinct test | **Verdict** |
|---|---|---|---|---|---|---|
| **A** Vector–host SEI–SEIR | ✗ | ✗ | ✗ | ✗ | ✓ | **Reject** (not identifiable; separate project + new data) |
| **B** Trait-based R0(T)/VC suitability | ~ (only as a feature → E) | ✗ (imported, not estimated) | ~ | ✗ (standalone) | ~ | **Reject standalone** → only via E |
| **C** Ross–Macdonald extension | ✗ | ✗ (no m, μ, n) | ✗ | ✗ | ~ | **Reject** (equifinal; weakest yield) |
| **D** Renewal / state-space Rt | ~ (re-expresses M1+climate) | ~ (Rt yes; reporting/real-time no) | ✗ (continuous target ≠ binary alert) | ✗ | ✗ | **Reject for this paper** → Paper-2/forecasting |
| **E** Mechanistic-statistical hybrid (index covariate) | ✓ | ✓ (one logistic coef) | ✓ (frozen pipeline) | ✓ | ~ (expected null-to-flat; redundancy risk) | **Only scope-compatible option**; defer to Paper-2 / reviewer-contingent robustness arm |
| **F** Climate-forced endemic–epidemic `hhh4` | ~ | ✓ | ~ (count target ≠ binary h=4 alert) | ✗ | ✗ (re-expresses AR-vs-climate split) | **Reject for this paper** → Paper-2/spatiotemporal-forecasting |

**Only E passes criteria 1–4. It passes 5 only weakly (its honest contribution is interpretive triangulation, with an expected null-to-flat metric result), and it carries a real redundancy/model-shopping risk unless strictly pre-specified. That is not enough to break the analysis freeze.**

---

## 4. Bottom-line verdict

**Do not add a mathematical/mechanistic biomodel to this frozen paper.**

- A genuinely mechanistic, biologically-identified dengue transmission model (**A, B-standalone, C**) is **not identifiable** from this project's data — the necessary entomological, serotype, seroprevalence, and reporting-fraction observations are absent, and *Brook et al. 2024* (doi:10.1073/pnas.2318704121) is decisive primary evidence that climate-and-cases-only is insufficient for the mechanistic claim. These are *separate projects requiring new data*, not additions.
- The two estimable-from-data candidates that are *not* vector-host-biological (**D** renewal/Rt; **F** `hhh4`) fail the freeze on different grounds: they target a *continuous/count* series rather than the binary 4-week-ahead 75th-percentile alert (criterion 4), and they re-express the autoregressive-vs-climate decomposition the paper already evaluates rather than posing a *distinct* test (criterion 5). They are sound **Paper-2 / forecasting** directions.
- The single scope-compatible move is the **mechanistic-statistical hybrid (E)**: a pre-specified, literature-frozen Mordecai/Huber-style temperature-suitability index added as one covariate (+0–8 wk lags) inside the *identical* frozen recalibration + decision-curve ΔNB + cluster-bootstrap pipeline, reported strictly for **non-redundancy** against M5 and the DLNM arm. Because both sites sit on the R0(T) thermal plateau and the DLNM ns(df=3) surface already failed to move the headline, the **expected result is null-to-flat**. Its value is interpretive ("surveillance is hard to beat even against a physiologically-motivated mechanistic climate feature"), not a metric gain — so it does **not** justify breaking the freeze pre-draft.

**Recommended disposition:** Note A/B/C/D/F as Future Work (E as the lead mechanistic extension for Paper 2). Run **E only** in *this* paper if a referee explicitly demands a mechanistic comparator, executed exactly within the frozen protocol with pre-specified index/lags to control model-shopping risk.

---

## 5. References (DOIs verified unless noted)

- Mordecai EA et al. 2017. *Detecting the impact of temperature on transmission of Zika, dengue, and chikungunya using mechanistic models.* PLoS Negl Trop Dis 11(4):e0005568. doi:10.1371/journal.pntd.0005568
- Huber JH, Childs ML, Caldwell JM, Mordecai EA. 2018. *Seasonal temperature variation influences climate suitability for dengue, chikungunya, and Zika transmission.* PLoS Negl Trop Dis 12(5):e0006451. doi:10.1371/journal.pntd.0006451
- Brook CE et al. 2024. *Climate, demography, immunology, and virology combine to drive two decades of dengue virus dynamics in Cambodia.* PNAS 121(35):e2318704121. doi:10.1073/pnas.2318704121
- Reiner RC, Perkins TA et al. 2013. *A systematic review of mathematical models of mosquito-borne pathogen transmission: 1970–2010.* J R Soc Interface 10(81):20120921. doi:10.1098/rsif.2012.0921
- Cori A, Ferguson NM, Fraser C, Cauchemez S. 2013. *A new framework and software to estimate time-varying reproduction numbers during epidemics.* Am J Epidemiol 178(9):1505–1512. doi:10.1093/aje/kwt133
- Wallinga J, Teunis P. 2004. *Different epidemic curves for SARS reveal similar impacts of control measures.* Am J Epidemiol 160(6):509–516. doi:10.1093/aje/kwh255
- Lowe R et al. 2021. *Combined effects of hydrometeorological hazards and urbanisation on dengue risk in Brazil: a spatiotemporal modelling study.* Lancet Planet Health 5(4):e209–e219. doi:10.1016/S2542-5196(20)30292-8
- Paul M, Held L. 2011. *Predictive assessment of a non-linear random effects model for multivariate time series of infectious disease counts.* Stat Med 30(10):1118–1136. doi:10.1002/sim.4177
- Meyer S, Held L. 2014. *Power-law models for infectious disease spread.* Ann Appl Stat 8(3):1612–1639. doi:10.1214/14-AOAS743
- Meyer S, Held L, Höhle M. 2017. *Spatio-temporal analysis of epidemic phenomena using the R package surveillance (hhh4).* J Stat Softw 77(11). doi:10.18637/jss.v077.i11

*Not verified to a specific DOI in this pass (labeled recollection):* the precise R0(T) thermal-optimum value (~29 °C) is reported in Mordecai 2017/2019-family papers; the Sri Lanka/Colombia ambient-temperature ranges and the prior Colombia ΔNB@0.30 ≈ +0.018 figure are from this project's own materials, not external literature.

---

*Generated 2026-06-26. Primary-literature feasibility review only — no model implemented, fit, run, committed, or pushed; no other project files edited. Advisory: recommends no change to the frozen analysis; proposes a biomodel only as a Paper-2 / reviewer-contingent extension.*
