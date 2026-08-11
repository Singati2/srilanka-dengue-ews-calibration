# BIOMATH_HARSH_REVIEW_V2

Four self-critique passes over the **tightened** candidate (post decision-theoretic tightening pass). **Not independent external reviewers.** Supersedes `BIOMATH_HARSH_REVIEW.md`; the V1 decoration/ornament concerns are now addressed.

## What changed since V1
- Value functional is now **metric-oriented**: $V_k$, larger-is-better, with $V_{\mathrm{Brier}}=-\mathrm{Brier}$, $V_{\mathrm{NLL}}=-\mathrm{NLL}$; estimand $\Delta V_{C,k}=V_k(\mathcal I^{SC})-V_k(\mathcal I^{S})$.
- **Removed from main Methods:** σ-algebra filtration (→ plain admissibility iff), spatial-exposure operator $\mathcal A_w$ (→ one Discussion sentence), geomatics estimand $\Delta V_G$ (→ one Discussion sentence), textbook Brier/NLL formulas (→ S18 pointer).
- **Added:** `MATCHED_COMPARATOR_STRUCTURE.md` (feature-block proof of nesting).
- Framework displayed equations reduced (outcome, predictive prob, $\Delta V_{C,k}$, calibration, decision rule, NB = 6 in the framework subsection; Methods total ~7 incl. the pre-existing DCA net-benefit display).
- Title changed to a decision-analytic (not "nested information sets") default; "biomathematics" absent from title/abstract.

## Reviewer A — Mathematical rigor
- **Metric orientation:** explicit and consistent (larger-is-better; Brier/NLL negated). ✓ Fixes the V1 sloppiness of an unoriented $V$.
- **$V_k$ definition:** family indexed by $k$, each mapped to a reported quantity. ✓
- **Nested-set legitimacy:** now backed by S9 feature counts (58−40=18 climate) in `MATCHED_COMPARATOR_STRUCTURE.md`; PASS on information nesting, PARTIAL on penalty identity (disclosed, shown not to drive result). ✓
- **Unnecessary notation:** filtration/σ-algebra removed; admissibility is a one-line iff. ✓
- **Calibration formalism:** kept separate (not forced into $V_k$), one recalibration equation retained (matches procedure). ✓
- **Net-benefit interpretation:** NB displayed once in framework; default-strategy identity kept inline because it earns its space (explains alert-all at $p^*\approx0.34$). ✓
- **Residual concern (minor):** NB formula now appears in both the framework subsection and the pre-existing DCA subsection (canonical). Duplication is harmless and numerically identical; could be de-duplicated later.

## Reviewer B — Epidemiology
- Outcome wording (elevated-activity, not outbreak), horizon, no causal overreach: preserved. ✓
- No environmental/geomatics inflation: $\Delta V_G$ and $\mathcal A_w$ are explicitly pending, not results; "climate" (not "environmental") leads the title. ✓
- No deployment claim: preserved. ✓

## Reviewer C — Prediction methodology
- Matched comparator: now documented at feature-block level; same row universe/estimator/evaluation; penalty-selection difference disclosed and bounded. ✓
- Proper-score orientation and metric-role separation explicit. ✓
- Conditional vs development-inclusive: retained, Colombia fixed-FE caveat preserved. ✓
- Difference-in-significance fallacy: avoided (no formal heterogeneity claim; "no between-setting comparison"). ✓

## Reviewer D — Hostile editor
1. **Still old results + equations?** Less so — the framework is now shorter and each equation maps to a reported quantity; the estimand $\Delta V_{C,k}$ is identifiable at a glance.
2. **Indispensable equations?** Outcome; predictive probability; $\Delta V_{C,k}$; net benefit; decision rule. (Calibration map is near-essential.)
3. **Could half be removed?** The ornamental half already was (filtration, spatial operator, $\Delta V_G$, textbook scores).
4. **Does $\Delta V_{C,k}$ match reported results?** Yes — it *is* the matched ablation reported per metric.
5. **Matched comparator nested?** Yes (PASS), with a disclosed PARTIAL on penalty identity shown not to drive the result.
6. **"Biomathematics" oversold?** No — removed from title/abstract; framed as decision-analytic / prediction-methodology / math-epidemiology.
7. **Coherent without M6/WP4/WP5?** Yes.
8. **Novelty still hinges on the unverified "first DCA" sentence?** It remains one hedged sentence, now marked `NEEDS_EXTERNAL_VERIFICATION`; the contribution is framed as the joint architecture, so the paper survives if that sentence is softened.
9. **Would a PLOS/GeoHealth/methodology editor get it fast?** Yes — title and estimand are decision-analytic and concrete.
10. **Stronger than plain v44?** For estimand/metric clarity, yes; the empirical content is identical.

## Verdict
**`ADOPT_HYBRID_LIGHT_FORMALIZATION`.** The tightened candidate keeps the genuinely clarifying formalism (metric-oriented incremental estimand; matched-comparator nesting; conditional vs development-inclusive uncertainty; the association ≠ prediction ≠ decision distinction) and sheds the ornamental machinery. It is stronger than plain v44 on estimand/metric clarity at near-zero risk (no science changed). It is **not** a full "biomath" rebrand and should not be marketed as mechanistic mathematical biology. Recommended path: fold this light formalization into the submission line, or carry both and let the target journal's framing decide (see `V44_VS_BIOMATH_DECISION_MEMO.md`).
