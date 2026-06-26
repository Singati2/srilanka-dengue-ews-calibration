# Memo: Is a mechanistic/mathematical biological dengue model implementable — and does it belong in this paper?

**Re:** Feasibility of a mathematical/biological transmission model from this project's data, and scope placement
**Date:** 2026-06-26
**Project state:** Analysis frozen at f1ace05; locked no-scope-expansion decision (evaluation paper, no mechanistic/forecasting pivot)
**Method:** Expert panel (mechanistic transmission modeler, vector/thermal-biology ecologist, data-and-identifiability statistician, literature-precedent researcher) → per-class adversarial verification → synthesis.

---

## 1. Bottom line

**Do not add a mechanistic transmission model to this paper.** A genuine, data-identified dengue transmission model is **not implementable** from this project's data — and the one mechanistic ingredient that *is* computable (a literature-parameterized temperature-suitability index) is not actually an identified model, sits in a temperature range where it is near-flat, and is already largely spanned by the DLNM cross-basis you tested. The single defensible move, if any, is to note a Mordecai-style temperature-suitability index as a **Paper-2 mechanistic extension** in Future Work, or to run it — clearly secondary — as a one-paragraph triangulation/robustness arm only if a reviewer demands a mechanistic comparator.

The honest one-sentence answer: **a derived climate-suitability covariate is implementable; an identified mechanistic transmission model is not, and neither belongs in this frozen evaluation paper.**

---

## 2. The data reality

Available: weekly reported case counts per administrative unit (RDHS / GID_2), ERA5-Land temperature (mean everywhere; min/max + RH for Sri Lanka), CHIRPS precipitation, WorldPop denominators — 2018–2025 with COVID-disrupted 2020–2021. The evaluation target is a **binary 4-week-ahead alert** keyed to the train-period 75th percentile.

Decisively absent: **no entomology** (no Aedes abundance, ovitrap/BG counts, biting rate, field mortality, field EIP), **no serotype data**, **no seroprevalence/immunity data**, **no observed reporting fraction**.

That inventory rules mechanistic ingredients in or out cleanly:

- **Rules IN** a temperature-forced *rate* index — published Aedes thermal-trait curves (biting a(T), EIP/PDR, adult mortality μ(T), egg-to-adult survival, fecundity) are mature enough to compute a relative-R₀(T)/vectorial-capacity transform from temperature alone. Nothing missing is needed to *compute* it.
- **Rules OUT** every *state* you would need to estimate dynamics: the susceptible reservoir (no immunity/serotype data), the vector limb (no entomology), and the reporting fraction (unobserved). These trade off against each other — the classic dengue equifinality — and the binary alert outcome discards the magnitude/timing signal a mechanism would need anyway.

The asymmetry is the whole story: **forced rates are importable; unobserved states are not recoverable.** Mechanism here belongs in a *feature*, not an *estimator*.

---

## 3. Candidate classes A–D

| Class | Implementable | Binding obstacle | Identifiable? | Effort | Scope fit |
|---|---|---|---|---|---|
| **A** — Trait-based R₀(T)/vectorial-capacity suitability index | **Partial** | Computable but equifinal as dynamics; collapses into D | Computable yes; identified no | Low | Paper 2 only |
| **B** — Climate-forced SEIR-host / SEI-vector | **No** | Latent vector + susceptible states confounded with unknown reporting; no serotype/immunity | Structurally non-identifiable | Very high | Paper 2 only (at best) |
| **C** — Semi-mechanistic time series (TSIR / renewal-Rt) | **Partial** | TSIR breaks on multi-serotype; Rt is AR-on-cases + climate GLM, needs continuous target | TSIR no; Rt partial | High | Paper 2 only |
| **D** — Mechanistic suitability index as a covariate in the existing logistic/calibration/DCA ladder | **Yes** | None for feasibility — redundancy is the real issue | Yes (one free logistic weight) | Low | Paper 2 only |

**Only A and D are scope-compatible in principle, and they are the same object viewed two ways. D *is* A used honestly.**

**Class A — partial.** The R₀(T) index is a closed-form deterministic transform of ERA5-Land temperature with all trait parameters fixed from published lab posteriors (Mordecai 2017/2019, Huber, Ryan, Tesla). No missing entomology, serotype, or seroprevalence is smuggled in to *compute* it — that claim survives adversarial check. But as a transmission model it is fully unidentified and equifinal: every trait is fixed from literature priors unconstrained by your data, absolute scale is meaningless (only relative/temporal shape is usable), and there is zero local entomological validation — documented local thermal adaptation means the imported curves could be locally miscalibrated with no way to detect it here. The only thing that ever gets "identified" is the index's regression coefficient *after* it enters the logistic ladder — which is literally Class D. Worse for utility: Sri Lanka (~20–31 °C) and tropical Colombia sit near the flat top of R₀(T) (peak ~29 °C), so the index is near-saturated and collinear with the raw lagged temperature already in M2–M5; areal-mean input incurs Jensen's-inequality aggregation bias; precipitation/humidity enter only as ad hoc multipliers with no thermal-trait analog.

**Class B — no.** A climate-forced SEIR-SEI carries host S/E/I/R, vector S/E/I, bidirectional transmission rates, EIP, vector mortality/emergence/carrying-capacity, reporting fraction, and initial immune fraction — and your data expose exactly one noisy, partially-observed channel: reported cases. Three fatal observability gaps: (1) no entomology, so the entire vector limb is latent and confounded with reporting and force of infection; (2) no seroprevalence/serotype, so S(0) and waning are free and R₀ trades off against final attack size without constraint, and the 4-serotype/ADE structure cannot even be represented; (3) reporting fraction absorbs whatever the optimizer needs. The literature precedent is decisive: climate-driven transmission alone cannot reproduce epidemics without demography + serotype + waning immunity — none of which exist here. Any fit would fix the large majority of parameters from priors and recover at most a reporting scale plus a couple of transmission multipliers, with flat profile-likelihood ridges and prior-dominated posteriors. Feeding such a fragile, prior-dominated fit into your locked calibration/NB comparison would inject unconstrained-prior dependence into the paper's central, carefully-bounded claim — weakening it, not strengthening it. This is the most data-hungry and worst-matched candidate.

**Class C — partial, but half-rejected and half-redundant.** TSIR is non-identifiable here: its susceptible reconstruction assumes a single fully-immunizing pathogen with known reporting — dengue violates every premise (4 serotypes, no immunity data, low/unknown reporting, short series). Decline it outright. The renewal/Rt branch is technically runnable without entomology or immunity data, but it is structurally a regularized autoregression on recent cases with a climate GLM on log-Rt — i.e., M1 (recent-case surveillance) fused with M2–M5 (climate). It re-derives your own thesis (surveillance is hard to beat) through more expensive machinery, and it natively produces a continuous incidence nowcast, not the binary h=4 75th-percentile alert — converting it requires a new re-thresholding pipeline the freeze forbids. Its one novel artifact, a temperature-dependent generation interval, just re-imports Class-A thermal priors.

**Class D — yes.** This is the only unambiguously implementable and identifiable option, precisely because it estimates *no* dynamical system. The mechanism lives entirely in a fixed deterministic feature (the Class-A index); the downstream penalized-logistic layer absorbs scale, baseline reporting, and sign, so there is no equifinality and no dependence on the absent data. The one honest caveat — the index's *value* depends on the literature priors being roughly right for local Aedes — degrades gracefully: even a mis-scaled index is just "an extra nonlinear temperature feature," not a misidentified mechanistic claim. The binding issue is **redundancy, not feasibility**: M2–M5 already enter temp_lag0..8 linearly, and your DLNM comparator already fits a natural-cubic-spline cross-basis (ns df=3 on value and lag) over temp × lag 0–8 on the identical evaluation rows. The single-peaked, plateaued suitability index sits largely *within* that already-tested span. So non-redundancy (collinearity/VIF vs the existing temp terms; incremental ΔNB over M4/M5 *and* the DLNM arm) is the empirical question that must be reported — and the expected result is null-to-flat.

---

## 4. If pursued anyway — Paper 2 sketch

A *credible* mechanistic model (Class B, the only version that would add genuinely new evidence) would require, at minimum:

- **Entomological observation** — Aedes abundance / ovitrap or BG time series to break the vector-abundance × reporting × force-of-infection confound, plus local field EIP and mortality to anchor the trait curves instead of importing them.
- **Immunity/serotype structure** — seroprevalence and serotype-resolved case counts to constrain S(0), waning, and the 4-serotype/ADE cross-immunity that drives dengue's multiannual cycles.
- **Reporting-fraction information** — an external estimate or a hierarchical observation model to stop the optimizer from absorbing climate signal into reporting.
- **Inference machinery** — a hierarchical state-space / particle-MCMC build (not a logistic regression), evaluated against a *continuous* incidence/timing target with reporting-delay correction and a temperature-scaled generation interval as a deliberate design choice — with profile-likelihood/identifiability diagnostics reported, not assumed.

Even with all of that, climate-attribution claims remain fragile without the missing immunological data. For Class A/D in Paper 2: trait-posterior Monte Carlo and DTR/rate-summation sensitivity (Sri Lanka's min/max + RH would support a diurnal rate-summation correction), validated solely for non-redundancy against the existing temperature features.

---

## 5. Recommendation for THIS paper

**Do not add a biomodel. Note it as future work.** Every implementable option is model-development/feature-expansion that the locked f1ace05 scope explicitly forbids, and none changes the headline. Decline B and TSIR-C outright as non-identifiable from this data; defer the renewal/Rt branch and the suitability index to Paper 2.

The one low-effort, scope-compatible, decision-relevant thing worth *considering* — and only as a clearly secondary triangulation/robustness arm, never a confirmatory test or a model-development pivot — is **Class D**: a pre-specified Mordecai-style temperature-suitability index (all trait parameters fixed from literature) added with its 0–8 wk lags as an M6-type feature to the existing M4/M5 hybrid, scored under the *identical* frozen recalibration + decision-curve ΔNB-at-p\*=0.30 + GID_2/RDHS cluster-bootstrap protocol, with strict non-redundancy reporting against both M5 and the DLNM arm. Its honest contribution is **interpretive, not metric**: a clean negative/triangulation result — *"recent surveillance is hard to beat even against a biologically-shaped, physiologically-motivated mechanistic climate feature, not just empirical splines."* Given that climate-only signal is already weak, the hybrid increment is modest-and-flat (Colombia ΔNB@0.30 ≈ +0.018), these sites sit on the R₀ thermal plateau, and the DLNM ns-df=3 surface already failed to move the headline, the expected result is null. **Effort bound: low — one deterministic feature reusing the exact frozen pipeline; ~one short paragraph or a reviewer-rebuttal sensitivity arm.** That does *not* justify breaking the analysis freeze pre-draft. Default: pre-register it as the lead mechanistic extension for Paper 2; run it in *this* paper only if a referee explicitly demands a mechanistic comparator.

---

## 6. Draft sentence for Future Work

> A natural mechanistic extension is to replace the empirical climate terms with a trait-based temperature-suitability index — a relative R₀(T)/vectorial-capacity transform parameterized entirely from published *Aedes aegypti* thermal-response curves (Mordecai et al.) — and to test it as a single pre-specified covariate within the same calibration and decision-curve framework; we defer this, together with a fully climate-forced SEIR–SEI model (which is not identifiable from case-and-climate data absent local entomological, serotype, and seroprevalence observations), to future work.

---

*Generated 2026-06-26 via a multi-agent expert panel with per-class adversarial verification. This memo is advisory; it recommends no change to the frozen analysis and proposes the biomodel only as a Paper-2 / reviewer-contingent extension.*
