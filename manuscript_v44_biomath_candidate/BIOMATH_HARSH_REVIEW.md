# BIOMATH_HARSH_REVIEW

Four internal review passes over the biomath candidate. **These are self-critique passes, not independent external reviewers.**

## Reviewer A — Mathematical rigor
- **Notation consistency:** symbols in the framework match the notation table and are reused consistently ($\mathcal I^S/\mathcal I^C/\mathcal I^{SC}$, $p^{(m)}_{it}$, $\delta_{p^*}$, $\Delta V_C$, $\mathcal A_w$). ✓
- **Conditional-probability interpretation:** $p^{(m)}_{it}=P(Y\mid\mathcal I^{(m)}_{it})$ is correctly labeled predictive, not mechanistic. ✓
- **Nested sets:** correctly notes $\mathcal I^S\subseteq\mathcal I^{SC}$ holds for the matched pair but **not** for M4–M1 (non-nested) — this is the sharpest addition and is accurate. ✓
- **Net-benefit derivation / default identity:** $\mathrm{NB}_{\mathrm{all}}=\pi-(1-\pi)p^*/(1-p^*)$ and $=0\iff p^*=\pi$ are algebraically correct and correctly labeled a property, not a new estimate. ✓
- **Calibration:** monotone-recalibration-preserves-AUC statement is correct; intercept-only-does-not-fix-slope is correct. ✓
- **Spatial operator:** $\mathcal A_w$ definition is standard; correctly flagged pending. ✓
- **Concern (minor):** the filtration $\mathcal I_t=\sigma\{\cdot\}$ is heavier machinery than the analysis strictly uses (no martingale/measure-theoretic argument follows). *Mitigation:* it is presented as a clarifying condition, not a theorem; acceptable but a reviewer may call it ornamental. Keep it terse (it is one line).
- **Unsupported formalism:** none introduces an estimand not computed; $\Delta V_G$ and $\mathcal A_P$ are explicitly pending. ✓

## Reviewer B — Epidemiology
- **Outcome meaning:** elevated-activity threshold exceedance, not outbreak; preserved and emphasized. ✓
- **Horizon / surveillance / climate interpretation:** short-lead ($h=4$); recent-case autocorrelation dominance is well-motivated and literature-anchored. ✓
- **Causal overreach:** explicitly avoided ("predictive feature-block contrast, not a causal estimand"; "biological relevance ≠ incremental forecast value"). ✓
- **Concern:** "environmental information" in framing is slightly broader than the climate features used; ensure abstract/title do not imply remote sensing/geomatics were evaluated (they were not). *Mitigation:* claim boundary + notice box handle this; keep "climate" in the primary title.
- **Operational claims:** none beyond the net-benefit-scale rescaling, which is correctly disclaimed as not observed events. ✓

## Reviewer C — Prediction methodology
- **Estimand alignment:** the matched ablation is correctly elevated as the climate estimand; M4–M1 correctly demoted as non-nested. ✓
- **Comparator fairness:** matched (same case/season/geography/preprocessing/development); the shrinkage-under-matching argument is sound. ✓
- **Calibration / proper scoring / resampling:** conditional vs development-inclusive distinction is correct and is the paper's real methodological contribution; proper scores held to the same refit standard. ✓
- **External/spatial validation language:** Colombia framed as a *second case study*, not validation; selection to a higher-incidence subset stated. ✓
- **Temporal leakage:** admissibility formalization matches the WER→ISO and reporting-delay treatment; satellite latency correctly quarantined to pending M6. ✓
- **Concern:** development-inclusive Colombia interval holds department FE columns fixed — partial refit. The candidate preserves this caveat (framework paragraph + S10/S17). ✓

## Reviewer D — Hostile journal reviewer
1. **"Just old results with equations added?"** Partly — and the candidate says so plainly (it is a formalization layer; the empirical results are v44 verbatim). The defense is that the equations change what a reader can *state precisely* (the estimand, the non-nested caveat, the metric-agreement), not the numbers. A hostile reviewer may still prefer the plain v44; that is a legitimate editorial call, surfaced honestly in the rationale.
2. **Genuine mathematical contribution?** Formalization of the incremental-value estimand over nested information sets + value functionals; the default-strategy identity; the admissibility condition. Modest but real; not a theorem.
3. **Genuine empirical contribution?** The deflationary matched-comparator finding (unchanged from v44).
4. **Does the notation clarify a real estimand?** Yes — $\Delta V_C$ is exactly the matched ablation.
5. **Is "biomathematics" an overclaim?** For a core math-biology theory venue, **yes** — do not submit there. For applied decision-theory/methodology/geo-epi venues, the label "applied statistical decision theory / mathematical epidemiology" is defensible. (See framing-validity doc.)
6. **Novelty dependent on a false "first"?** No — one hedged "to our knowledge" sentence only; all other "first" claims are barred (novelty audit).
7. **Survives if the environmental increment is null?** Yes — the finding *is* essentially null/deflationary; the framework is designed so a null is a valid, interpretable result.
8. **Coherent without M6/WP4/WP5?** Yes — none is used; the geomatics estimand and exposure operator are pending framework only.

## Verdict
- **Major concerns:** (i) risk of "equations-as-decoration" perception — mitigate by keeping the framework terse and estimand-anchored (done); (ii) journal-fit — must not be pitched as mechanistic mathematical biology.
- **Minor concerns:** filtration notation could be trimmed; ensure "environmental" never implies geomatics were evaluated.
- **Desk-rejection risks:** submitting to a mechanistic math-biology journal (mismatch); any hardened "first"/heterogeneity/geomatics claim (barred).
- **Necessary repairs before author use:** none blocking in the candidate; author-owned submission items (ethics, ORCIDs, funding, COI, archival DOI/license) remain open, as flagged in Declarations.
- **Overall:** **Qualified accept as an internal candidate.** The reframe is faithful, compiles, changes no science, and clarifies the estimands. Whether to adopt it over the plain v44 is an author/editor decision about framing and venue, not a correctness question.
