# BIOMATH_FRAMING_VALIDITY

*Is it honest to describe the canonical v44 manuscript as an applied-biomathematics / mathematical-epidemiology / decision-theory paper? A critical assessment. No source changed.*

## The honest one-line answer
**Qualified yes for "applied statistical decision theory / quantitative epidemiological forecasting," and defensibly "mathematical epidemiology"; NO for "mathematical biology" in the mechanistic sense.** A few equations do not make a paper biomathematics; what earns the label here is that the *estimand itself* is a decision-theoretic object (incremental value of an information set under a threshold utility), not that the prose contains symbols.

## What the paper genuinely is
The study is a **decision-analytic evaluation of information value**: it defines an alert as a thresholded probabilistic forecast, scores forecasts by a decision-utility functional (net benefit) plus strictly proper scoring rules, and estimates the *incremental* value of the climate information block against a structurally matched comparator, with an explicit conditional-vs-development-inclusive uncertainty distinction. Those are bona fide topics in:
- **statistical decision theory** (loss/utility, threshold rules, proper scoring rules);
- **prediction-model methodology** (calibration, recalibration, discrimination, DCA);
- **quantitative / mathematical epidemiology** (population-level infectious-disease forecasting and early-warning evaluation).

The matched-ablation estimand and the conditional/development-inclusive uncertainty split are the parts with real methodological content; formalizing them (information sets, a value functional $V(\cdot)$, admissibility of the origin-week filtration) sharpens rather than decorates.

## What the paper is NOT — and must not be dressed up as
- **Not a mechanistic transmission model.** There is no SIR/SEIR, no vector–host coupled dynamical system, no compartmental flow, no basic reproduction number, no force-of-infection parameter estimation. Climate enters as *predictive features*, not as rate modifiers in a transmission process.
- **Not a vector–host dynamical system / epidemic-compartment model.** None is fitted or simulated; the manuscript states mechanistic modeling "would require additional serotype, immunity, entomological, mobility, intervention, and reporting-process data and is reserved for separate work."
- **Not a causal mechanistic analysis.** The matched ablation is explicitly "a predictive feature-block contrast, not a causal climate-effect estimand, because climate overlaps with seasonal and geographic structure." No causal identification strategy is claimed.
- **Not a theorem paper.** The mathematics clarifies estimands and validity conditions; it proves nothing. Adding theorem/lemma apparatus would be cosmetic overclaim.

## Why "a few equations" would NOT suffice
The net-benefit formula is already in the manuscript, and simply pasting more standard formulas (Brier, NLL, a filtration) would be decoration. The framing is honest **only because** the equations map onto the actual estimand: the matched ablation genuinely is $V(\mathcal I^{SC})-V(\mathcal I^{S})$, and the paper's central intellectual move — "value attributed to climate depends on how much structure the comparator already carries" — *is* a statement about nested information sets. If those equations were removed, the science would be unchanged; if the estimand were different, the equations would be wrong. That correspondence is what licenses the framing.

## What additional mathematics a stronger mathematical-biology identity would require
(For transparency; **not** recommended for this task, which forbids new science.)
1. A mechanistic climate-forced transmission model (e.g., temperature-dependent Ross–Macdonald or SEIR-SEI) with identifiable biological parameters, fit to the same data, and compared to the statistical models — a different paper.
2. A formal decision-theoretic optimality result (e.g., Bayes-optimal alert policy under an explicit loss, or a value-of-information theorem) with proof — would move it toward decision theory proper.
3. A spatial stochastic-process treatment of the exposure operator and change-of-support with estimable error, tied to WP5 — pending and empirical, not yet done.
None of these is present, and none should be added here.

## Recommended disciplinary label (most accurate first)
1. **Applied statistical decision theory for infectious-disease early warning** (most accurate).
2. **Quantitative / methodological epidemiology (prediction-model evaluation).**
3. **Mathematical epidemiology (forecasting/decision sub-branch)** — defensible for an applied-math-biology venue *if* the framing foregrounds decision theory and disclaims mechanism.
4. **Mathematical biology (mechanistic)** — **inaccurate; do not use.**

## Journal-fit implication (summary; full treatment in final report §S)
The math strengthens fit for methodology/decision venues (BMC Medical Research Methodology, Diagnostic & Prognostic Research) and geo/epi venues (PLOS Global Public Health — the current header target — GeoHealth, PLOS NTD). It is **not** substantive enough for a core mathematical-biology theory journal (e.g., *Bull. Math. Biol.*, *J. Math. Biol.*), and submitting there would risk desk rejection for lack of mechanistic or theoretical novelty. Choose a venue on the strength of the *decision-analytic methodology and the deflationary empirical finding*, not on the presence of equations.
