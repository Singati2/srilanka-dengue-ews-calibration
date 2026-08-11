# NOVELTY_CLAIM_AUDIT

*Classification of novelty statements for the biomath reframe. Assessed against the manuscript's own cited literature and its existing hedges; no broad web search performed (task §20 forbids it unless required). Where a claim needs external confirmation it is marked NEEDS_LITERATURE_VERIFICATION. No source changed.*

Legend: **SUPPORTED** (safe as written) · **NLV** NEEDS_LITERATURE_VERIFICATION · **TOO_STRONG** (weaken) · **REMOVE**.

## What the canonical manuscript already claims (and how it hedges)
The v44 manuscript makes **one** scoped novelty claim: *"To our knowledge this is the first application of decision-curve net benefit to population-level dengue elevated-activity forecasting, distinct from its recent use in individual dengue clinical prognosis [Sangkaew2026], paired with a matched climate-block ablation."* It immediately disclaims the stronger versions: *"We do not claim a validated or transportable instrument: no simulation, formal theory, prospective testing, external validation, independent replication, or standardized software release supports that stronger claim."* This is a well-hedged posture the biomath candidate must preserve.

## Unsafe claims — must NOT appear
| Claim | Class | Reason |
|---|---|---|
| First climate dengue forecast | **REMOVE** | Vast prior literature (Lowe 2013/2021, EWARS-csd, Colón-González 2021, etc., all cited). |
| First remote-sensing / geomatics dengue forecast | **REMOVE** | Untrue and also M6-pending; outside canonical scope. |
| First comparison against surveillance | **REMOVE** | Manuscript itself cites Lowe 2013 (surveillance-mirroring baseline), Johansson 2016, Benedum 2020 as prior surveillance-benchmark work. |
| First demonstration that spatial representativeness matters | **REMOVE** | MAUP/change-of-support is long-established; WP5 not even done. |
| "Climate adds no incremental value" / $\Delta V_G=0$ / climate is irrelevant to transmission | **REMOVE** | The paper's finding is *"no robust evidence of operationally meaningful incremental value,"* explicitly **not** proof of zero. Never restate as a null-proven claim. |
| Validated, transportable, or deployment-ready instrument | **REMOVE** | Explicitly disclaimed in-manuscript. |
| A formal Sri Lanka–Colombia difference/heterogeneity | **REMOVE** | "No formal between-setting comparison was performed." |

## Potentially defensible claims — allowed with the existing hedge
| Claim | Class | Handling |
|---|---|---|
| First application of decision-curve **net benefit** to population-level dengue elevated-activity forecasting, paired with a matched climate-block ablation (distinct from clinical-prognosis DCA) | **`VERIFIED_SUPPORTED_WITH_HEDGE`** (DCA_DENGUE_NOVELTY_VERIFICATION.md, 2026-08-10; no conflicting prior work found, Scopus/WoS not searched) — softened in the .tex to "we did not identify a prior…"; do NOT strengthen to "first-ever" (a `% NOVELTY CLAIM REQUIRES TARGETED LITERATURE VERIFICATION` marker is placed next to the sentence in the candidate .tex) | Carry verbatim from v44 with its hedge. The DCA-in-dengue-EWS gap is corroborated by the manuscript's own reviews (Leung 2022: decision-analytic evaluation "essentially absent"; Hussain-Alkhateeb 2021). Do not upgrade "to our knowledge" to an absolute "first." |
| Integration of a structurally matched environmental-information ablation with calibration, proper scores, decision-curve net benefit, and development-inclusive uncertainty | **SUPPORTED** | This is the true methodological contribution; state as an *integration/combination* claim, not a component-invention claim. |
| Formal treatment of environmental inputs as **nested information sets** in dengue early warning | **SUPPORTED (framing)** | New to *this literature's framing*; the concept itself (nested models / incremental value) is standard in prediction methodology (Steyerberg, Vickers), so frame as "we make explicit," not "we introduce." |
| Explicit linkage between **forecast-origin information admissibility** and environmental early-warning evaluation | **SUPPORTED (framing) / NLV (priority)** | Availability/vintage reasoning exists in nowcasting literature; claim only the *explicit formal linkage in this evaluation*, not first-ever. |
| Joint framing of comparator strength + calibration + temporal availability + spatial support as **validity conditions** for incremental environmental value | **SUPPORTED** | This synthesis is a fair, modest conceptual contribution. |
| Development-inclusive (refit-both-models) vs conditional uncertainty distinction applied to a climate ablation | **SUPPORTED** | Already the paper's signature; safe as a methodological emphasis, not "first invention of the bootstrap." |

## Component-novelty disclaimers to keep (do NOT claim novelty for)
Logistic regression; DLNM (Gasparrini); calibration/recalibration; decision-curve analysis (Vickers); proper scoring rules; cluster bootstrap (Cameron–Gelbach–Miller). The contribution is their **integration into a surveillance-benchmarked, matched-ablation dengue-alerting evaluation**, not any single method.

## Net guidance for the candidate
- Keep exactly one "to our knowledge, first…" sentence — the DCA-net-benefit-for-population-dengue-EWS-with-matched-ablation claim, with its hedge — and no other "first."
- Frame all mathematical additions as **"we make explicit / we formalize,"** never "we introduce" or "for the first time."
- Preserve every existing negative-scope disclaimer verbatim.
- If the authors later want to harden the "first DCA net benefit in population dengue EWS" claim, that is the **one** statement worth a targeted literature verification (search terms: "decision curve analysis" OR "net benefit" AND dengue AND (outbreak OR "early warning" OR forecast) — excluding individual clinical prognosis). Flagged **NLV**; not performed here per task scope.
