# V44_MATHEMATICAL_GAP_ANALYSIS

*Comparison of the canonical manuscript (`manuscript_v44/revised_manuscript.tex` @ `4b3287c`, SHA256 `08fad12b…`) against the proposed decision-theoretic framework. No number recomputed; no source changed. Classifications use the task taxonomy.*

Legend: **AE** ALREADY_EXPLICIT · **INF** IMPLICIT_BUT_NOT_FORMALIZED · **MU** MISSING_AND_USEFUL · **MC** MISSING_BUT_COSMETIC · **NS** NOT_SUPPORTED_BY_CURRENT_SCIENCE · **DEF** DEFER_UNTIL_M6_WP4_WP5_VALIDATED

## Concept-by-concept classification

| # | Mathematical concept | Class | Evidence in v44 / justification |
|---|---|---|---|
| 1 | Elevated-activity outcome $Y_{i,t+h}$ as training-defined threshold exceedance | **AE** | §"Alert labels" : "a future week was flagged if its incidence exceeded the unit's training-period 75th percentile"; horizon $h=4$, date-based join. Formula not written but definition exact. |
| 2 | Nested information sets $\mathcal I^S,\mathcal I^C,\mathcal I^{SC}$ | **INF → MU** | The **matched climate ablation** ($\Delta$NB(M5$-$M5$_{\text{no-climate}}$)) *is* an $\mathcal I^{SC}$ vs $\mathcal I^{S+}$ contrast, and the paper explicitly reasons about "how much non-climate structure the comparator omits." But the set notation is never written, and the key subtlety (M4$-$M1 is **non-nested**; only the matched ablation isolates the climate block) is currently prose. Formalizing $\mathcal I^{S}\subseteq\mathcal I^{SC}$ makes the estimand and the M4$-$M1/matched distinction precise. |
| 3 | Probabilistic forecast $p^{(m)}_{it}=P(Y_{i,t+h}=1\mid\mathcal I^{(m)}_{it})$ | **INF** | Predicted probabilities and their conditioning on origin-week information are used throughout ("constructed only from information available at the forecast origin"), but never written as a conditional-probability object. Low-cost, clarifying. |
| 4 | Alert action as decision rule $a=\mathbf 1\{p\ge p^*\}$ | **INF → MU** | Net benefit is defined via TP/FP at $p^*$, which presupposes the rule, but the map $\mathcal I\to p\to a$ is not stated. Writing it is the bridge from prediction to action and is faithful. |
| 5 | Net benefit via decision utility / cost–loss weight $p^*/(1-p^*)$ | **AE** | §DCA: full NB formula present; cost–loss interpretation cited (Murphy 1985, Tozan 2023); Vickers 2023 caveat that CIs/tests on NB are contested is already incorporated. |
| 6 | Incremental value of climate $\Delta V_C=V(\mathcal I^{SC})-V(\mathcal I^{S})$ | **INF → MU** | This *is* the paper's central estimand (the matched ablation), but expressed only as a model-label difference. Writing $\Delta V_C$ generically over a value functional $V\in\{$NB, $-$NLL, $-$Brier, AUC$\}$ unifies the decision-curve and proper-score results under one estimand and clarifies that "value" is metric-dependent. |
| 7 | Conditional vs development-inclusive uncertainty | **AE** | §"Uncertainty": conditional = "recompute metrics on the frozen, already-fitted test-set predictions without refitting"; development-inclusive = "refit both models within each resample." This is a genuine, already-formalized contribution of v44. A compact $D^{(b)}\to\hat f^{(b)}\to\hat p^{(b)}\to\Delta^{(b)}$ schematic would only tidy it (**INF** at most for the notation). |
| 8 | Forecast-origin information admissibility $\tau_{\text{avail}}(X_j)\le t$ | **INF (partial) → MU / DEF** | The WER issue→ISO date-alignment and the "no future climate enters the predictors" / reporting-delay censoring are exactly availability reasoning, and are **AE** for the WER/climate lags. A general filtration $\mathcal I_t=\sigma(X_j:\tau_{\text{avail}}(X_j)\le t)$ is **MU** as a unifying principle. Its satellite-composite (measurement/composite-end/release) refinement is a leakage concern from the **M6 workstream** and must stay **DEF** — described as a general principle only, no M6 number imported. |
| 9 | Temporal availability of environmental data | **AE (WER/climate) / DEF (satellite)** | WER→ISO mapping and lag-window admissibility are in the canonical manuscript; satellite-composite latency is M6-pending. |
| 10 | Spatial exposure aggregation as an operator $\mathcal A_w[X]$ | **INF → DEF** | The manuscript states climate was summarized as "unweighted administrative-unit means; no population weighting" and names change-of-support/MAUP as a limitation — so the *area-mean* operator is used and its limitation acknowledged. The general $\mathcal A_w$ operator with $w=1$ vs $w=P(s)$ vs fractional support is **MU** *as motivation/limitation formalization*, but population-weighted/fractional comparison is empirically **WP5-pending** → keep as framework + pending, never as a result. |
| 11 | Area- vs population- vs fractional weighting distinction | **DEF** | Only area-mean was computed. Formalize the distinction conceptually; do **not** claim population weighting changes performance (WP5 not validated/integrated). |
| 12 | Why standalone M6 does not estimate incremental geomatics value | **MU (gap-docs) / DEF (manuscript)** | Not in the manuscript (M6 absent). The distinction $V(\mathcal I^{G})$ vs $V(\mathcal I^{SG})-V(\mathcal I^{S})$ is worth stating **as a formal estimand definition labelled PENDING/NOT ESTIMATED**; it must not import M6 numbers or reinterpret the M6 null as $\Delta V_G=0$. Belongs primarily in the gap docs and, if at all, only as a clearly-pending future-estimand paragraph. |
| 13 | Do the equations clarify estimands or only decorate? | — | **Clarify** for #2, #4, #6, #8(principle): they make the matched-ablation estimand, the non-nested M4$-$M1 caveat, and the availability condition precise. **Decorate** if pushed further (theorem apparatus, filtration formalism beyond one line). Recommendation: add the clarifying minimum; resist the rest. |
| 14 | Would applied-biomath framing improve journal fit without misrepresenting? | — | Qualified yes — see `BIOMATH_FRAMING_VALIDITY.md`. It is applied statistical decision theory / mathematical epidemiology, **not** mechanistic mathematical biology. |
| 15 | Equations that must NOT be added | — | (a) any mechanistic transmission/SEIR/Ross–Macdonald/force-of-infection model (NS, out of scope); (b) a monetary/health-utility function (NS — no cost elicitation); (c) a population-weighted exposure *result* (DEF — WP5); (d) a geomatics incremental *estimate* $\Delta V_G$ (DEF — M6); (e) any equation implying an estimand not actually computed (e.g. a formal Sri Lanka–Colombia heterogeneity parameter — the paper explicitly performed none). |

## Answers to the 15 gap questions

1. **Nested information sets formalized?** No — implicit via the matched ablation; not written as sets.
2. **Distinguishes association / standalone / incremental / decision value?** Partially and in prose. The Discussion §"Probability accuracy versus decision value" and §"Why the comparator matters" separate standalone, incremental, and decision value well, and Intro separates biological association from incremental value ("not whether climate carries predictive signal beyond chance, but whether it adds value beyond recent cases"). The **four-level ladder is not stated as one explicit hierarchy** — MU.
3. **Probability forecast as conditional on available information?** Conceptually yes, notationally no — INF.
4. **Alert action as a decision rule?** Presupposed by NB; not written — INF/MU.
5. **Net benefit as decision utility / cost trade-off?** Yes — AE (with the Vickers-2023 inference caveat).
6. **Incremental value of climate defined mathematically?** As a model-label difference, yes; as a generic estimand over a value functional, no — MU.
7. **Conditional vs development-inclusive uncertainty distinguished mathematically?** Yes — AE (v44's signature methodological point).
8. **Forecast-origin admissibility formalized?** Applied (WER→ISO, lag windows, reporting-delay censoring) but not stated as a general condition — INF→MU; satellite refinement DEF.
9. **Temporal availability of environmental data formalized?** For WER/climate lags yes in substance; satellite composite latency is M6-pending — AE/DEF.
10. **Spatial exposure aggregation as an operator?** Area-mean used and its MAUP limitation acknowledged; operator not written — INF→DEF for weighting variants.
11. **Area/pop/fractional weighting distinguished mathematically?** No, and only area-mean computed — DEF.
12. **Shows why standalone M6 ≠ incremental geomatics value?** No (M6 absent) — belongs in gap docs; manuscript mention only as pending estimand.
13. **Clarify or decorate?** The minimal set (2,4,6,8-principle,10-framework) clarifies; more would decorate.
14. **Applied-biomath framing honest + better fit?** Qualified yes (decision theory / math epidemiology, not mechanistic biology).
15. **Equations NOT to add?** Mechanistic transmission models; monetary utility; population-weighted/geomatics *results*; any not-estimated estimand (esp. formal heterogeneity).

## Verdict: is the biomath candidate justified?

**Yes — as a thin formalization layer, not a rewrite.** The formalization genuinely clarifies three things the current prose leaves implicit:
1. that the **matched ablation is the nested-information estimand** $\Delta V_C=V(\mathcal I^{SC})-V(\mathcal I^{S})$, and that **M4$-$M1 is non-nested** and therefore not climate-specific;
2. that **net benefit, proper scores, AUC, and calibration are different value functionals $V$** answering different questions over the *same* nested contrast — which is exactly why the paper's metrics disagree in emphasis but agree in conclusion;
3. that **admissibility (availability by the forecast origin)** and **spatial support** are *validity conditions* on $\mathcal I$, not incidental data-cleaning.

Everything else the framework proposes is either already explicit (NB, conditional/dev-inclusive uncertainty), or must be deferred (population weighting, geomatics increment, satellite latency). **No equation implies an estimand the study did not compute.** The candidate must therefore be a formalization/notation layer over the exact v44 science, with a hard M6/WP4/WP5 firewall — which is what `manuscript_v44_biomath_candidate/` implements.
