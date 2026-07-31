# Reviewer-Critique Classification Memo (Paper 1)

**Status:** Response-classification only. The external reviewer-style critique is treated as a *critical appraisal*, **not** as authorization to reopen the frozen analysis. No manuscript edit, no analysis, no data change, no commit/push was made in producing this memo.

**Manuscript under review:** `manuscript/plos_ntd_revision_v5_final_scientific_audit/dengue_ews_plos_ntd_v5.tex` (PLOS NTD revision v5).

**Source of the critique.** No standalone reviewer-critique document was supplied. The file pointed to (`~/Downloads/Dengue (5).pdf`, sha256 `5a74e694…`, 21 pp) was checked and found to be **the v5 manuscript itself** (text-identical to `dengue_ews_plos_ntd_v5.pdf`; it contains no reviewer/recommendation/critique text). Accordingly, the recommendations classified here are the ones enumerated in the author's instruction (the critique content), and the manuscript is unchanged since this memo was first written, so every quote below remains current.

**Evidence basis:** all manuscript quotes below were extracted and then independently **verified verbatim** against the v5 source (13/13 confirmed). Feasibility and appraisal points are grounded in the frozen committed reports under `docs/`. No number was recomputed.

**Categories used**
1. Mandatory writing/reporting correction for Paper 1
2. Already addressed in the current manuscript
3. Reviewer-contingent additional analysis (record only; do **not** run now)
4. Separate Paper 2 / future-project work

---

## 1. Master classification table

| # | Recommendation (from critique) | Category | Current manuscript status | Proposed response | New analysis required? |
|---|---|---|---|---|---|
| R1 | Keep finalized-vs-real-time surveillance limitation prominent | 1 + 2 | **Already stated** (Methods line ~154 & Limitations line ~404) | Keep verbatim; no change | No |
| R2 | Keep single Sri Lanka temporal-holdout limitation prominent | 1 + 2 | **Already stated** (Methods ~154 & Limitations ~404) | Keep verbatim | No |
| R3 | Keep COVID-era Colombia limitation prominent | 1 + 2 | **Already stated** (Results ~312 & Limitations ~404) | Keep verbatim | No |
| R4 | State climate feature implementations differed between settings | 1 + 2 | **Already stated** (Methods ~139; caption ~380; Limitations ~404) | Keep verbatim | No |
| R5 | State alert outcome was percentile exceedance, not official outbreak | 1 + 2 | **Already stated** (Methods ~130; Author Summary ~103; Limitations ~404) | Keep verbatim | No |
| R6 | State p\*=0.30 was a reference threshold, not a stakeholder-derived operating threshold | **1 (only genuine gap)** | **Partly** — substance present ("not an empirically established public-health threshold … not an empirically chosen operational tolerance"); the word/idea "stakeholder-derived/elicited" is **not explicit** | Add one half-clause making the non-stakeholder origin explicit (writing only) | No |
| R7 | Complete reproducibility archive, references, SI, declarations | 1 | **Partly** — references now Vancouver & verified; SI are drafts; declarations are neutral placeholders | Finish per `submission_blockers_v5.md` (author metadata, repo/DOI, completed checklists) | No (assembly, not analysis) |
| R8 | Preserve cautious cross-setting interpretation; no tested-heterogeneity claim | 1 + 2 | **Already stated** (Results "Cross-setting synthesis" ~376; caption ~380) | Keep verbatim | No |
| R9 | (Check) no reporting-delay simulation | 2 | **Already stated** (Limitations ~404) | Keep | No |
| R10 | (Check) no real-time deployment claim | 2 | **Already stated** (Limitations ~404) | Keep | No |
| R11 | (Check) no cross-country heterogeneity claim | 2 | **Already stated** (~376) | Keep | No |
| R12 | (Check) Colombia as framework replication, not transported-model validation | 2 | **Already stated** (Intro ~107; Methods ~118; Limitations ~404) | Keep | No |
| R13 | (Check) pointwise, multiplicity-unadjusted sensitivity intervals | 2 | **Already stated** (Methods ~154) | Keep | No |
| R14 | (Check) finalized rather than real-time surveillance | 2 | **Already stated** (Methods ~154; Limitations ~404) | Keep | No |
| R15 | (Check) differing climate implementations | 2 | **Already stated** (Methods ~139) | Keep | No |
| R16 | (Check) official-outbreak vs percentile-label distinction | 2 | **Already stated** (Methods ~130; Author Summary ~103) | Keep | No |
| R17 | (Check) change-of-support / MAUP limitation | 2 | **Already stated** (Limitations ~404) | Keep | No |
| R18 | (Check) no cost-effectiveness or cases-averted claim | 2 | **Already stated** (Discussion ~400; Limitations ~404) | Keep | No |
| R19 | Colombia pandemic-period (2020–2021) exclusion | 3 | Limitation already disclosed; analysis not performed | Decline now; record as contingent (test window *is* 2020–2022) | Yes (deferred) |
| R20 | Limited climate-feature harmonization sensitivity | 3 | Gap disclosed verbatim | Decline now; rebut with frozen disclosures | Yes (deferred; needs new Colombia humidity build) |
| R21 | Additional rolling-origin validation (one-off robustness) | 3 | Single-holdout limitation disclosed | Contingent; defer unless a reviewer requires | Yes (deferred refit) |
| R22 | Spatial-block validation | 3 | Limitation disclosed | Decline for this revision; defend design | Yes (deferred refit) |
| R23 | Formal two-country heterogeneity test | 3 | Explicitly not done; correctly refrained | Decline; only after a valid harmonized estimand is defined | Yes (deferred; requires redesign) |
| R24 | Reporting-delay simulation | 4 | — | Paper 2 (real-time robustness) | Yes (Paper 2) |
| R25 | Provisional undercount & backfill | 4 | — | Paper 2 | Yes (Paper 2) |
| R26 | Nowcasting | 4 | — | Paper 2 | Yes (Paper 2) |
| R27 | Delayed-vs-finalized M1 and M5 comparison | 4 | — | Paper 2 | Yes (Paper 2) |
| R28 | Weekly rolling-origin refitting (operational) | 4 | — | Paper 2 (distinct from the one-off R21) | Yes (Paper 2) |
| R29 | Adaptive recalibration | 4 | — | Paper 2 | Yes (Paper 2) |
| R30 | Stakeholder-grounded thresholds | 4 | — | Paper 2 | Yes (Paper 2) |
| R31 | Official operational alert outcomes | 4 | — | Paper 2 | Yes (Paper 2) |
| R32 | Prospective deployment | 4 | — | Paper 2 | Yes (Paper 2) |

---

## 2. Category 1 — Mandatory Paper 1 corrections

Most "mandatory" items are mandates to **keep** language that is already present and prominent (see Category 2 for verbatim quotes). Only two require any author action, and **neither requires analysis**:

- **R6 — make the non-stakeholder origin of p\*=0.30 explicit (the single genuine wording gap).**
  Current text (Methods, Decision-curve subsection): *"We used $p^*=0.30$ as the \\emph{primary reference threshold}. This is not an empirically established public-health threshold; it encodes a particular trade-off between the cost of an unnecessary alert and the loss from a missed alert …"* and *"This ratio is a mathematical implication of the selected reference threshold, not an empirically chosen operational tolerance."*
  Gap: the substance (not empirical, not an operational tolerance) is present, but the manuscript never explicitly says the threshold was **not stakeholder-elicited/derived**. Suggested minimal addition (writing only, author to insert): *"and was not elicited from operational stakeholders."*
- **R7 — complete the reproducibility archive, references, SI, and declarations.**
  References are already converted to verified Vancouver style. Outstanding items are assembly/metadata, not analysis: completed STROBE/TRIPOD+AI/PROBAST checklists, data/code repository URL + archival DOI + license, ethics/funding/competing-interests/CRediT, ORCIDs, second-author email, and the OpenDengue V1.3 version-specific DOI. All tracked in `submission_blockers_v5.md`.

The remaining Category-1 items (R1–R5, R8) are **already satisfied verbatim** and should simply be preserved.

---

## 3. Category 2 — Already addressed (verbatim quotes; all verified)

Every quote below was confirmed as an exact substring of `dengue_ews_plos_ntd_v5.tex`.

| Item | Verbatim current wording | Location | Genuinely missing? |
|---|---|---|---|
| No reporting-delay simulation | "The study was retrospective, used finalized rather than real-time surveillance counts, and did not simulate reporting delay; under real-time conditions the recent-case signal that M1 depends on could be degraded, and the direction and magnitude of any change in the relative net benefit of the models cannot be determined from these data." | Limitations (~404) | none |
| No real-time deployment claim | "we make no claim of deployment readiness, transportability, causal climate effects, cost-effectiveness, rare-epidemic prediction, or universal hybrid benefit." | Limitations (~404) | none |
| Finalized (not real-time) surveillance | "surveillance counts are finalized rather than real-time, so results reflect retrospective performance on completed counts." | Methods (~154) | none |
| No cost-effectiveness / cases-averted | "decision-analytic representations of the same net-benefit difference, not observed public-health outcomes." (+ explicit "cost-effectiveness" disclaimer at ~404) | Discussion (~400) / Limitations (~404) | none |
| No cross-country heterogeneity claim | "No cross-country interaction or heterogeneity test was designed or performed; therefore, the study does not establish that the setting-specific estimates differ." | Cross-setting synthesis (~376) | none |
| Colombia = framework replication | "Colombia is external framework replication, not external model validation, so the findings do not establish that coefficients or thresholds transport to other settings …" | Limitations (~404) | none |
| Pointwise, multiplicity-unadjusted intervals | "Threshold, horizon, percentile, and regime analyses were secondary or exploratory, with pointwise intervals and no multiplicity adjustment." | Methods (~154) | none |
| Climate implementations differ | "the implementations differed: in Sri Lanka the hybrid climate component was a Python DLNM-style cross-basis approximation (temperature, precipitation, humidity; lags 0--8 weeks; df=3), whereas in Colombia the climate component used linear weekly precipitation and temperature lags … humidity was not used in Colombia." | Methods (~139) | none |
| Outbreak vs percentile label | "Alert labels were percentile (exceedance) thresholds rather than official outbreak declarations" | Limitations (~404); Author Summary (~103) | none |
| p\*=0.30 reference threshold | "We used $p^*=0.30$ as the \\emph{primary reference threshold}. This is not an empirically established public-health threshold …" | Methods (~151) | **partial** — see R6 (no explicit "not stakeholder-derived") |
| Change-of-support / MAUP | "climate exposures were aggregated to administrative units (raising change-of-support and modifiable-areal-unit concerns)" | Limitations (~404) | none |
| Single SL temporal holdout | "the primary Sri Lanka design used a single temporal holdout rather than a rolling-origin and spatial-block design" | Limitations (~404); Methods (~154) | none |
| COVID-era Colombia | "The Colombia test period was 2020--2022 and therefore includes the COVID-19-era years 2020--2021 … a pandemic-period exclusion analysis was not performed in the current study, so its effect on the M5$-$M1 contrast cannot be inferred." | Limitations (~404); Results (~312) | none |

**Conclusion:** 12 of 13 checklist items are fully addressed verbatim; only the p\*=0.30 "not stakeholder-derived" nuance is genuinely (and minimally) missing.

---

## 4. Category 3 — Reviewer-contingent analyses (record only; do NOT run now)

All five would require reopening the freeze (recomputation/refit) and are therefore **deferred** unless a reviewer explicitly requires them.

| Analysis | Feasibility | Data requirements | Scientific value | Scope risk | Recommended response |
|---|---|---|---|---|---|
| **Colombia pandemic-period (2020–2021) exclusion** | Infeasible without redesign | The Colombia test window *is* 2020–2022 (OpenDengue V1.3 Admin-2 tier ends 2022); excluding 2020–2021 leaves only 2022 (~1/3 of 13,361 rows). No non-pandemic test years exist. | Low/confounded — would yield an underpowered 2022-only re-estimate; the project's own continuity check (S7 label report) shows reporting did not collapse in 2020–2022 | **High** | Decline; explain transparently that no clean non-pandemic Colombia test window exists, rather than produce a confounded re-estimate |
| **Climate-feature harmonization sensitivity** | Infeasible without redesign | Harmonizing "up" needs Colombia ERA5-Land dewpoint→RH (not built; ~60h CDS retrieval) plus full refit of Colombia M2–M5 with a DLNM-style cross-basis | Moderate concept, low increment here — the difference is already fully disclosed and no claim rests on a harmonized comparison | **High** | Decline; rebut in the response letter using the already-frozen disclosures (Methods ~139, caption ~380) |
| **Additional rolling-origin validation (one-off)** | Feasible with refit (inputs exist; would recompute) | Frozen SL panel + committed M0–M5 scripts already present; no new external data | Moderate, well-targeted — directly tests the single-holdout concern | Moderate | Contingent; defer unless required. First defense: the manuscript already concedes the single-holdout limitation explicitly |
| **Spatial-block cross-validation** | Feasible with refit | Frozen SL exposure panel + 26-RDHS queen adjacency (26 nodes/60 edges) + scripts exist | Moderate, mostly defensive (not result-changing); SL arm already self-labeled exploratory | **High** | Decline for this revision; defend the pre-specified design and reaffirm the freeze |
| **Formal two-country heterogeneity / interaction test** | Infeasible without redesign | Requires a shared label, units, period, features — none harmonized (RDHS 26 vs ~475 GID_2; 2023–2025 vs 2020–2022; DLNM+RH vs linear lags; rolling vs Platt recalibration) | Low-to-negative — a test on two non-harmonized estimates would be statistically vacuous and could invite over-interpretation | **High** | Decline; point to existing language; only consider after defining a valid harmonized estimand (a redesign, i.e., Paper 2 territory) |

---

## 5. Category 4 — Separate Paper 2 (real-time robustness paper)

Assigned wholesale to the future real-time robustness project; **out of scope for Paper 1**:
reporting-delay simulation; provisional undercount & backfill; nowcasting; delayed-vs-finalized M1 and M5 comparison; weekly rolling-origin refitting (operational pipeline, distinct from the one-off robustness check R21); adaptive recalibration; stakeholder-grounded thresholds; official operational alert outcomes; prospective deployment.

Rationale: each requires either real-time/provisional data the project does not hold, a deployment context, or stakeholder elicitation — none of which is needed to support Paper 1's actual claim (a retrospective, surveillance-benchmarked, calibration- and decision-curve evaluation on finalized counts).

---

## 6. Critical appraisal of the critique itself

(Substantiated against the manuscript and repo; verdicts abbreviated — full evidence retained in the workflow record.)

1. **Reporting delay duplicated (weaknesses 1 and 7).** *Valid as a redundancy point.* The real-time-count threat and the reporting-delay threat reduce to one right-truncation mechanism, which the manuscript already names once (Limitations ~404). The on-file review (`docs/manuscript_peer_review_v1.md`) raises it as a single item and uses no "weakness 1/7" numbering, so the duplication refers to an external/paraphrased critique and holds only at the concept level.
2. **30–70% underreporting range.** *Correct — unsupported.* A repo-wide search finds no project-specific quantified underreporting fraction; the manuscript frames the real-time concern mechanistically with no number. A 30–70% figure would be an imported external prior and **must not enter the manuscript** without an applicable cited source (and would violate the freeze discipline).
3. **Formal two-country heterogeneity test may be invalid.** *Strongly substantiated and already honored.* The settings differ in period, units, sample size, climate-feature implementation, and recalibration; the manuscript already declines the test and says the estimates "should not be interpreted as establishing a between-setting difference."
4. **2022-only COVID exclusion may be underpowered.** *Largely valid (inference, not computed).* Excluding 2020–2021 leaves only 2022 (~1/3 of 13,361 test rows; full-set confirmatory ΔNB +0.0188 [+0.0117, +0.0260]); a one-third window would widen the bootstrap CI and could drag the lower limit toward zero. Exact per-year event counts are not in the frozen record, so this is an informed inference and cannot be computed under the freeze.
5. **Locally refitted framework replication is not a design error.** *Correct.* The manuscript consistently frames Colombia as "external framework replication, not external model validation … refitting all models locally rather than transporting coefficients." Local refitting is the intended design; criticizing it as a flaw misreads the stated estimand.
6. **"Landmark paper" is speculative.** *Correct.* The phrase appears nowhere in the manuscript or repo; the project's stated positioning is deliberately modest ("we do not … claim methodological novelty"). It should not drive scope (e.g., adding countries or claims).

---

## 7. Author decision summary

- **No reopening of the frozen analysis is warranted by this critique.** Paper 1's claim is retrospective, surveillance-benchmarked, calibration/decision-curve evaluation on finalized counts; every limitation the critique raises is already disclosed verbatim (Category 2).
- **One genuine writing addition (R6):** make explicit that p\*=0.30 was not stakeholder-elicited. **One assembly task (R7):** finish the reproducibility archive / SI / declarations per `submission_blockers_v5.md`. Neither needs analysis.
- **Decline now, record as reviewer-contingent (Category 3):** pandemic-period exclusion, climate harmonization, one-off rolling-origin, spatial-block, and the formal heterogeneity test — all require reopening the freeze, and three are infeasible without redesign. Respond to any reviewer by pointing to the existing honest disclosures.
- **Defer to Paper 2 (Category 4):** the entire real-time/operational program (delay simulation, nowcasting, delayed-vs-finalized comparison, operational rolling refitting, adaptive recalibration, stakeholder thresholds, operational outcomes, deployment).
- **Reject two imported critique elements outright:** the unsourced 30–70% underreporting figure and the "landmark paper" framing.

**No recommendation was implemented. Stopping for author review.**

---

## 8. Expert-panel deep-research addendum

A seven-expert field panel (surveillance epidemiologist; biostatistician; decision-curve/net-benefit methodologist; calibration & TRIPOD+AI/PROBAST reporting expert; real-time/operational EWS expert; reproducibility/open-science expert; journal peer-review strategist) independently stress-tested the classification, grounded verbatim in the v5 manuscript. Every claimed manuscript "gap" was then **adversarially verified** against the `.tex`: of 40 candidate gaps, **32 were refuted as already covered** and **8 survived as genuinely missing** (all writing-only). All findings are read-only; nothing was applied to the manuscript.

### 8.1 Panel consensus
**Unanimous: do not reopen the freeze.** No model/bootstrap/CI/calibration/threshold/heterogeneity quantity needs recomputation. Every confirmed action is writing/reporting only and reuses already-frozen numbers. Genuine dissent existed but was entirely writing-level (sharpen the finite-cluster bootstrap caveat; widen R6's scope; interpret the Colombia slopes; split R7's OpenDengue-DOI correction from deferred assembly; flag rolling-origin as the most likely reviewer demand). None rose to refitting.

### 8.2 Confirmed mandatory Paper-1 writing additions (verified-real; proposed text only — NOT applied)

| ID | Severity | Topic | Current wording (verbatim) | Proposed addition (author to insert) |
|---|---|---|---|---|
| M-1 | **Moderate** | No graphical calibration curve (TRIPOD+AI item) | NOT FOUND (no calibration plot in text or S1–S6 captions) | Either add an SI flexible (loess) calibration curve per model **if it already exists in a frozen report**, or state in Methods that graphical calibration was not produced and that calibration is summarized by CITL, slope, and Brier. Do **not** generate new curves. |
| M-2 | Minor | Colombia slopes 0.85–3.43 uninterpreted | "with Brier scores 0.213--0.250 and calibration slopes 0.85--3.43, consistent with the temporal prevalence shift not being fully removed by validation-fit recalibration" | "These slopes departed from 1 in both directions across the model ladder, indicating residual over- and under-dispersion that intercept-only and Platt recalibration do not correct; the M5--M1 contrast is therefore a decision-analytic comparison conditioned on imperfectly calibrated probabilities, not evidence of correctly-scaled absolute risks." (per-model attribution only if already frozen) |
| M-3 | Minor | p\*=0.30 not stakeholder-derived (R6, widened) | "This is not an empirically established public-health threshold; it encodes a particular trade-off…" | "…and was not elicited from operational stakeholders or derived from a documented response-cost analysis; it sits below the observed test-period prevalences (0.336 Sri Lanka, 0.375 Colombia), which is why alert-all remains competitive at lower thresholds and why we report net benefit across a threshold grid." |
| M-4 | Minor | Reporting-delay caveat applies to the alert LABEL too, not only M1 | "under real-time conditions the recent-case signal that M1 depends on could be degraded…" | "Because the alert label is itself defined from finalized counts, real-time reporting delay would affect both the recent-case predictor and the observed alert outcome at week $t+4$, not the M1 predictor alone; climate inputs are largely complete in near-real-time, so the asymmetry could move the M5--M1 contrast in either direction." |
| M-5 | Minor | Operational translation only for Colombia | "the $\Delta$NB of $+0.0188$ corresponds to approximately 1.9 additional net true-positive equivalents per 100 municipality-weeks" | Parallel Sri Lanka line: "the Sri Lanka $\Delta$NB of $+0.0081$ corresponds to approximately 0.8 net true-positive equivalents per 100 RDHS-weeks, with a confidence interval crossing zero — a decision-analytic representation, not an observed count." (0.8 = 0.0081×100; arithmetic restatement) |
| M-6 | Minor | OpenDengue V1.3-vs-record-DOI integrity (R7, split) | "OpenDengue. Global dengue data, Temporal extract, version 1.3 [dataset]. figshare; 2025. doi: 10.6084/m9.figshare.24259573." | Pin the version-specific V1.3 figshare identifier + access date; if unavailable, render "V1.3 Temporal extract (record DOI 10.6084/m9.figshare.24259573; version-specific identifier pending), accessed [date]." |
| M-7 | Minor | Data/code PID + forward commitment (R7 assembly) | Declarations placeholder "Pending author confirmation" | "Analysis code and derived artifacts will be archived at Zenodo with a DOI assigned upon acceptance; source datasets are redistributed by citation and documented fetch instructions," then insert repo URL/license once confirmed. |
| M-8 | Minor (opt.) | Finite-cluster bootstrap mechanism | "resampled only 26 RDHS clusters, so its percentile intervals are coarse and may be mildly anti-conservative…" | Optional one clause: "because cluster-bootstrap variance is downward-biased with few clusters, nominal coverage is not assured — most acutely for the eight-cluster regime estimate and for the primary contrast whose lower limit sits at zero." |
| M-9 | Minor (opt.) | Abstract "varied across settings" vs no-heterogeneity disclaimer | Abstract/Author-Summary "varied" + line 93 "No cross-country heterogeneity test was performed; therefore, the study does not establish a difference between settings." | Internal-consistency tightening only: keep each "varied" instance adjacent to the no-test disclaimer (already true in the abstract). No substantive change. |

All M-IDs reuse frozen numbers; **none requires analysis**. M-1 is the only one rising above "minor" and is a reporting-completeness (assembly) item, not a computation.

### 8.3 Reclassifications adopted from the panel
- **R6 → Category 1, widened** to include the prevalence-position clause (M-3), not only "not stakeholder-elicited."
- **R7 → Category 1, split:** (a) OpenDengue DOI/version mismatch = a reporting correction available now (M-6); (b) repo URL / archival DOI / ORCIDs / completed checklists = deferred pre-submission assembly (M-7).
- **R8/R11 (cross-setting) and R13 (cluster bootstrap):** remain Category 2 with optional Category-1 sharpening (M-8). The "overlapping CIs" addition is **declined** as a stand-alone claim — overlapping pointwise CIs is a weak heuristic; the procedural "no test designed or performed" framing is the stronger rebuttal and is kept.
- **R21 (rolling-origin):** remains Category 3 but flagged as the **most likely reviewer-mandated item and the weakest decline** — pre-authorize as the first concession (supplementary sensitivity on the existing frozen panel, not a change to the primary pre-specified estimand) if an editor presses.
- **Graphical calibration (M-1):** newly recognized Category-1 reporting-completeness item.

### 8.4 Refuted "gaps" (already covered — use as reviewer rebuttals, not edits)
32 candidate gaps were adjudicated already-addressed against the verbatim text, including: the percentile label is relative-elevation (line 130); M1 lags and the t+4 label share the reporting process (lines 114/141); the hybrid clears alert-all/alert-none (M5 NB 0.145 > alert-all 0.052 > alert-none 0; line 289/Tables); the 4-point grid is captioned as representative thresholds, not a continuous curve (line 264); cross-setting estimates are on different prevalence/scales and the procedural no-test framing is stated (line 376); asymmetric recalibration is in the cross-setting caption (line 380); Python versions "not preserved" is disclosed (line 141); the common-not-rare prevalence caveat (~23.5%) is stated (line 373). These need no edit; they are ready-made response-letter points.

### 8.5 Consolidated reviewer response-letter draft (themes A–K)
A ready-to-adapt response letter, organized by theme, is retained for the author:
- **A. Finalized vs real-time / reporting delay** — one right-truncation mechanism, disclosed once; mechanism made explicit (M-4); no 30–70% figure imported; delay simulation deferred to Paper 2.
- **B. Percentile label vs official outbreak** — kept prominent; relative-elevation label distinguished from EWARS-csd alarm logic.
- **C. COVID-era Colombia / pandemic exclusion** — declined: V1.3 Admin-2 ends 2022, so a 2020–2021 exclusion leaves only ~1/3 of rows (underpowered/confounded); disclosed transparently.
- **D. Formal heterogeneity test** — declined as ill-posed across non-harmonized estimands; differences enumerated; valid only after a harmonized estimand (redesign).
- **E. Uncertainty (pointwise/multiplicity/finite clusters)** — primary CI is a single pointwise interval; 26-cluster coverage caveat sharpened (M-8); primary contrast treated as hypothesis-generating.
- **F. Threshold p\*=0.30** — origin made explicit (M-3); grid reported; cost-anchored thresholds deferred.
- **G. DCA default-strategy clearance** — M5 clears alert-all/alert-none in Sri Lanka; the demanding test is the M1 benchmark, which the +0.0081 increment addresses.
- **H. Operational translation** — magnitude-only; symmetric Sri Lanka translation added (M-5); no cost-effectiveness claim.
- **I. Calibration interpretation** — slopes interpreted (M-2); graphical calibration handled (M-1); asymmetric recalibration noted.
- **J. Single temporal holdout / rolling-origin** — limitation stated; rolling-origin offered as a supplementary sensitivity if required (R21).
- **K. Reproducibility/references/declarations** — OpenDengue version pinned (M-6); Zenodo/data-availability commitment (M-7); R version-pinned, Python "not preserved" disclosed.

(The full drafted prose for each theme is preserved in the deep-research record; insert verbatim into the response letter as needed.)

### 8.6 Strengthened critical appraisal of the critique (panel-reinforced)
1. **Reporting delay duplicated (weaknesses 1 & 7)** — one right-truncation mechanism, disclosed once (line 404); counting it twice double-penalizes a single disclosed limitation.
2. **30–70% underreporting** — unsourced imported prior; no applicable project-specific source; must not enter the manuscript; the real-time concern is framed mechanistically without a magnitude.
3. **Formal heterogeneity test** — statistically invalid without harmonized models/outcomes/periods/units; the "overlapping CIs" counter is deliberately not adopted (weak heuristic); the procedural no-test framing stands.
4. **2022-only exclusion** — underpowered and confounded (V1.3 Admin-2 ends 2022 → ~1/3 of test rows); transparent disclosure preferred.
5. **Local refit framework replication** — the intended estimand, not a design error; transportability is explicitly disclaimed.
6. **"Landmark paper"** — editorial speculation; appears nowhere in the project; must not drive scope.
7. **Most "mandatory" items mandate KEEPING already-present language** — the genuinely new writing is confined to M-1…M-9, none of which touches the frozen analysis.

**Deep-research provenance:** 7-expert panel + adversarial gap-verification + lead synthesis (48 sub-agents). All manuscript quotes verified verbatim. No manuscript edit, no analysis, no data change, no commit/push. Proposed text in §8.2 is for author decision only and has not been applied. Stopping for author review.
