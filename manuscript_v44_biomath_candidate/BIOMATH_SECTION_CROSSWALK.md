# BIOMATH_SECTION_CROSSWALK

Maps every change from the canonical source (`manuscript_v44/revised_manuscript.tex`, SHA256 `08fad12b…`) to the biomath candidate (`revised_manuscript_biomath.tex`). **All changes are additive/framing; no results paragraph, table, figure caption, number, or citation was altered.** Verified by `diff` (only the rows below differ) and by a result-grade numeric-token check (all 241 preserved; the single flagged token was a rewritten provenance *comment*).

| Canonical element | Candidate change | Type | Science touched? |
|---|---|---|---|
| Header comment (Version 25 provenance) | Rewritten to a biomath-candidate banner; original provenance note retained in prose | Comment | No |
| Preamble `\usepackage{graphicx}` | Added `\safeincludegraphics` (placeholder if figure absent); 6 fragile packages (`threeparttable, microtype, placeins, setspace, fancyhdr, lineno`) wrapped in `\IfFileExists` fallbacks; `\grayscalecopy` color-model flag after `xcolor` | Build robustness | No |
| Title | "Exploratory matched-comparator evaluation…" → "Nested information sets and the incremental decision value of climate information … an exploratory matched-comparator evaluation" | Framing | No |
| (after author block) | Added "internal biomath-reframe candidate — not for submission" notice box | New | No |
| Abstract, sentence 2 | Appended one sentence naming the estimand ("incremental value of a climate information block added to a recent-surveillance information set") | Framing | No (no number) |
| Introduction (before "The question is therefore not…") | Inserted one paragraph: the four-level distinction (association ≠ standalone ≠ incremental ≠ decision value) + pointer to the framework | New | No |
| Methods, first subsection | **Inserted** `\subsection{Mathematical and decision-analytic framework}` (outcome; information sets; probabilistic prediction; nested estimand $\Delta V_C$; calibration operator; threshold rule; net benefit + default-strategy identity; proper scores; conditional vs development-inclusive; forecast-origin admissibility; spatial-exposure operator [pending]) + notation table | New | No — restates existing objects; pending items carry no number |
| Results §"Cohort…" | Heading → "Q1. How strong is the recent-surveillance benchmark? (Cohort and data alignment)" | Heading | No |
| Results §"Sri Lanka: matched climate increment" | Heading → "Q2. What incremental decision value remains after adding climate? Sri Lanka" | Heading | No |
| Results §"Colombia: a second…" | Heading → "Q2, continued. Colombia…" | Heading | No |
| Results §"Robustness, selection, and horizon" | Heading → "Q6. Does the increment persist across robustness, selection, and horizon?" (label `sec:robustness` kept) | Heading | No |
| Results §"Threshold-free proper-score reanalysis" | Heading → "Q3–Q5. Does it persist under calibration, proper scoring, and development-inclusive refitting?…" | Heading | No |
| Discussion §"Principal findings" | Appended one paragraph tying results to $\Delta V_C=V(\mathcal I^{SC})-V(\mathcal I^{S})$ and the boxed "biological relevance ≠ incremental forecast value" | Framing | No |
| Materials/methods body subsections (design, settings, ladder, calibration, DCA, uncertainty, proper-score, matched-ablation, spec table) | **Unchanged** | — | No |
| All Results tables (headline, proper-score, spec) and figures | **Unchanged** (figures via `\safeincludegraphics`) | — | No |
| Declarations, References (thebibliography), Supporting Information (S1–S19) | **Unchanged** | — | No |

## Structure of the candidate (as compiled, 28 pp)
1. Title + candidate notice
2. Abstract (verbatim + 1 estimand sentence)
3. Introduction (verbatim + four-level paragraph)
4. Materials and methods
   - **Mathematical and decision-analytic framework (new)** + Notation table
   - Study design and identity; Settings/data; Alert labels & ladder; Calibration; DCA & threshold; Uncertainty; Proper-score reanalysis; Matched ablation & status; Spec table *(all verbatim)*
5. Results — Q1…Q6 headings over verbatim bodies/tables/figures
6. Discussion (verbatim + estimand/biological-relevance framing)
7. Declarations, References, Supporting Information *(verbatim)*

---

## Tightening-pass changes (decision-theoretic revision)
Additive/framing only; no results number changed (re-verified — see NUMERIC_CROSSWALK).
| Element | Change | Type |
|---|---|---|
| Title | → decision-analytic default ("The incremental decision value of climate information beyond recent surveillance…") | Framing |
| Framework: value functional | single unoriented $V(\cdot)$ → metric-oriented family $V_k$ (larger=better; Brier/NLL negated); estimand $\Delta V_{C,k}$ | Precision |
| Framework: information sets | inlined $\mathcal I^{SC}=\mathcal I^S\cup\mathcal I^C$; dropped $\mathcal I^G/\mathcal I^{SG}$ from Methods; added pointer to MATCHED_COMPARATOR_STRUCTURE.md | Trim |
| Framework: proper scores | textbook Brier/NLL formulas → S18 pointer + metric-role paragraph | Trim |
| Framework: admissibility | σ-algebra filtration $\mathcal I_t=\sigma\{\cdot\}$ → plain iff $X_j\in\mathcal I_t\iff\tau_{\mathrm{avail}}(X_j)\le t$ | De-ornament |
| Framework: spatial operator $\mathcal A_w$ | removed from Methods → one Discussion sentence | Trim |
| Framework: geomatics estimand $\Delta V_G$ | removed from Methods → one Discussion sentence (pending, not estimated) | Trim |
| Notation table | dropped $\mathcal A_w$/$\Delta V_G$/filtration from core rows; $V(\cdot)\to V_k$ oriented | Consistency |
| Discussion | box → three-way "biological relevance ≠ incremental predictive value ≠ incremental decision value"; added pending-extensions note | Framing |
| Intro | added `% NOVELTY CLAIM REQUIRES TARGETED LITERATURE VERIFICATION` marker | Traceability |
| Displayed equations in framework subsection | 8 → 6 (outcome, predictive prob, $\Delta V_{C,k}$, calibration, decision rule, NB) | Reduction |
