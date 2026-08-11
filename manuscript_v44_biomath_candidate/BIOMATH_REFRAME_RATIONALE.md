# BIOMATH_REFRAME_RATIONALE

## What this candidate is
A **formalization/framing layer** over the frozen canonical v44 manuscript. It adds a decision-theoretic vocabulary (nested information sets, an incremental value functional, a threshold decision rule, calibration and admissibility conditions, a spatial-exposure operator) that makes the study's *existing* estimands explicit, without changing any datum, model, metric, interval, threshold, horizon, split, or hierarchy.

## Why it qualifies as applied biomathematics (qualified)
The paper's central object is genuinely decision-theoretic: it scores probabilistic forecasts by a utility functional (net benefit) and strictly proper scoring rules, and estimates the *incremental* value of an information block against a structurally matched comparator, with an explicit conditional-vs-development-inclusive uncertainty distinction. Formalizing these is honest because the equations map one-to-one onto what was computed — the matched ablation *is* $\Delta V_C=V(\mathcal I^{SC})-V(\mathcal I^{S})$, and the paper's key insight ("value attributed to climate depends on how much structure the comparator already carries") *is* a statement about nested sets. See `../analysis/v44_biomath_gap_analysis/BIOMATH_FRAMING_VALIDITY.md`. Most accurate label: **applied statistical decision theory / mathematical epidemiology (forecasting–decision sub-branch)**.

## Why it is NOT a mechanistic transmission model
No SIR/SEIR, Ross–Macdonald, vector–host ODE/PDE, reproduction number, or force-of-infection parameter appears or is fitted. Climate enters as predictive features, not rate modifiers. The manuscript states mechanistic modeling is reserved for separate work; the candidate preserves that and adds an explicit disclaimer ("this is a decision-theoretic evaluation, not a mechanistic transmission model").

## The mathematical contribution
1. **Nested information sets** $\mathcal I^S\subseteq\mathcal I^{SC}$ make the estimand precise and expose why **M4−M1 is non-nested** (differs beyond climate) while the **matched ablation** (M5 vs M5$_{\text{no-climate}}$) isolates the climate block.
2. **A single incremental value functional** $\Delta V_C=V(\mathcal I^{SC})-V(\mathcal I^{S})$ unifies the decision-curve (NB), proper-score (−NLL, −Brier), and discrimination (AUC) results as *different value functionals over the same contrast* — explaining why they differ in emphasis but agree in conclusion.
3. **The default-strategy identity** $\mathrm{NB}_{\mathrm{all}}(p^*)=0\iff p^*=\pi$ turns an observed pattern (alert-all near zero at $p^*\approx0.34$, SL prevalence 0.336) into a stated mathematical property.
4. **Forecast-origin admissibility** $\mathcal I_t=\sigma\{X_j:\tau_{\mathrm{avail}}(X_j)\le t\}$ formalizes the WER→ISO date-alignment and lag-window rules as validity conditions, not incidental cleaning.
5. **A spatial-exposure operator** $\mathcal A_w[X]$ frames the area-mean-vs-population-weighting question (pending WP5) precisely, without claiming a result.

## The empirical contribution (unchanged)
A deflationary, matched-comparator finding across two settings: recent surveillance is a demanding short-lead benchmark; climate improves average probability accuracy modestly but adds small, calibration- and comparator-sensitive, not-robust decision value, with no formal cross-setting claim. Every number is the canonical v44 result.

## Limitations of the biomath framing
- The mathematics **clarifies estimands; it proves nothing** — no optimality theorem, no identification result. Overselling it as "mathematical biology" would be an overclaim (see framing-validity doc).
- Two framework elements (spatial-exposure operator; the geomatics incremental estimand $\Delta V_G$) are **pending/not estimated** and must stay labeled as such; importing M6/WP4/WP5 numbers is firewalled off.
- Adding notation to a post-hoc, exploratory analysis does not make it confirmatory; the exploratory status is preserved verbatim.

## What additional theory a stronger math-biology identity would need
(Not done here.) A mechanistic climate-forced transmission model fit to the same data; or a formal decision-theoretic optimality/value-of-information result with proof; or an estimable spatial change-of-support error model tied to WP5. Each is a separate project.

## Bottom line
The reframe succeeds by the task's own standard — it makes the estimands **clearer** ("what additional decision-relevant information does environment contribute once recent surveillance is known, and under what validity conditions?") without changing the science. If a reader wanted only the empirical result, the canonical v44 already delivers it; the value added here is precision of statement and journal-framing optionality, not new findings.
