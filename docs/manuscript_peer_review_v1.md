# Multi-Expert Peer Review & Revision Plan

**Manuscript:** *Benchmarking Climate-Informed Dengue Early Warning Against Recent Surveillance: Calibration and Decision-Curve Evidence from Sri Lanka and Colombia* (Shiwakoti & Khadka, 23 pp).

**Review process:** 6 field-expert reviewers (biostatistics/DCA, dengue epidemiology, prediction-model methodology/TRIPOD-PROBAST, geospatial/data-engineering, decision-analytic/health-economics, editor/scope) — all independently returned *major revision*. 53 raw issues → consolidated to 24 → adversarially stress-tested against the manuscript text → **20 survived as real**; 4 thrown out as overstated/already-addressed.

---

## 1. Verdict — Major revision

Methodologically disciplined and honestly reported; the core design choices are correct and under-used in dengue EWS (surveillance baseline M1, not climatology/alert-all; net benefit + calibration as primary endpoints, not AUC; no over-claiming). The panel was unanimous that the science is sound and the conclusions are calibrated to the evidence. The load-bearing gaps reduce to a small set, **none of which overturn the headline** (the model ordering — M1 best — is stable under adjudication):

- an unjustified *"registered"* threshold p\*=0.30 with no cost ratio and no locatable preregistration object;
- **no Data/Code Availability section** in a paper whose stated contribution is a reusable framework;
- net-benefit values reported as bare decimals, never translated into operational units;
- the one *confirmed* climate result (Colombia) resting on a COVID-era window never given the anomaly-exclusion already run for Sri Lanka;
- a synthesis that dichotomizes two statistically **indistinguishable** hybrid increments into "confirmed" vs "not confirmed."

## 2. Strengths (preserve)

1. **Recent-case surveillance baseline M1** as the operational comparator — every reviewer named this the single most important decision.
2. **DCA net benefit + calibration as primary endpoints**, correct cost-loss attribution; DCA arithmetic checks out (alert-all NB at 0.20/0.30/0.40 reproduces from prevalence 0.336).
3. **WER-issue → ISO-week date-alignment audit** with the naive-linkage sensitivity (S1).
4. **Leakage-aware controls**: train-only scaling/thresholds, date-based target join, rolling-52-week recalibration using only pre-prediction pairs.
5. **Honest reporting**: SL hybrid explicitly unconfirmed, underpowered cells flagged not spun, 2021 anomaly handled.

Do not over-correct into a paper that oversells climate. The honesty is an asset.

## 3. Blocking & major issues — "where to update" (prioritized)

### 3.1 Justify or de-"register" p\*=0.30 — MAJOR
- **Location:** §2.12 (p.7); Abstract, §3.2/3.3; Tables 1/2; Figs 2/4/5.
- **Problem:** p\*=0.30 is called "registered" but justified only as a vague trade-off — no cost ratio, no DOI. It implies a ~0.43:1 false-alert-to-missed-outbreak cost ratio (implausible for dengue). Threshold-sensitive: alert-all NB goes negative by 0.34; Colombia ΔNB rises +0.018 (0.30) → +0.0241 (0.40).
- **Fix:** Justify 0.30 via its implied cost ratio with a concrete Tozan (2023) citation, or elicit a range; report the threshold range over which conclusions hold (M1 best across 0.20–0.40). **Either cite the preregistration object by DOI everywhere "registered" appears, or delete the word throughout.** Ordering is stable — justification/reporting, not reanalysis.

### 3.2 Add a Data and Code Availability section — MAJOR
- **Location:** Whole manuscript (jumps from §4.12 to References).
- **Problem:** No data/code statement, repo link, or DOI in 23 pages, in a paper whose contribution is a reusable framework. Load-bearing artifacts exist only as prose (WER→ISO map, Ampara–Kalmunai dissolve, 26-node queen graph, 208-record denominator table, M0–M5 ladder). TRIPOD+AI item 26 requires this.
- **Fix:** Add a "Data and Code Availability" section before References. Deposit code (M0–M5 ladder, WER→ISO linkage, recalibration, DCA) in a versioned public repo + license + Zenodo DOI. Release/fetch-script the derived artifacts (crosswalk, WER→ISO map with returns-cutoff dates incl. 2021 anomaly, 26-polygon geometry + queen adjacency, 208-record denominator table, date-aligned analysis table). Cite the OSF preregistration / registered-threshold object by DOI.

### 3.3 Translate ΔNB / NB into operational units — MAJOR
- **Location:** §3.11/Table 8; Abstract; §4.4; Figs 2/4b/5b; Tables 1/2/5/6/8.
- **Problem:** Every NB/ΔNB is a bare decimal; figure axes argue the third decimal. "0.018" is rhetorically indistinguishable from negligible.
- **Fix (cost-free; needs only N and prevalence):** Colombia ΔNB +0.018 ≈ ~1.8 net true-positive-equivalent alerts per 100 unit-weeks (N=13,361, prevalence 0.375); also per 1,000 and as false-alert-equivalents; same for SL M1 NB₀.₃₀=0.137 and the M5 near-miss. Report standardized NB (NB/prevalence) in Tables 1/2/5/6/8; annotate figure axes + table footnote with the per-observation denominator; add one Abstract sentence. Keep explicit cost/loss translation as future work.

### 3.4 COVID-era confound on the only confirmed result — MAJOR
- **Location:** §3.11 (p.16).
- **Problem:** Colombia M5>M1 (ΔNB +0.018; ΔAUC +0.040) comes from a test window including 2020–2021 with acknowledged over-prediction, handled by a single "Nevertheless" clause. The analogous calendar-anomaly drop was run only for Sri Lanka (S3), where nothing hinges on it. Pandemic reporting disruption degrades the M1 AR comparator specifically.
- **Fix:** Refit the Colombia M1–M5 ladder excluding 2020–2021 (and/or add a pandemic indicator); report whether ΔNB(M5−M1)@0.30 still excludes zero with the municipality-cluster bootstrap CI. State the exact Colombia test date range and per-year case counts / alert prevalence. Elevate from a clause to a named threat in Limitations and the §4.4 sentence; soften "statistically supported improvement" if it does not survive exclusion. (Thesis survives even if Colombia is fully discounted — SL drives it.)

### 3.5 Reframe the two-setting discordance honestly — MAJOR
- **Location:** Abstract; §2.2; §3.11; §3.13/Fig 6.
- **Problem:** SL +0.0081 [−0.0012, 0.0181] "not confirmed" vs Colombia +0.018 [0.012, 0.026] "confirmed" — overlapping CIs, close point estimates, narrated as harmonious replication with no pooling/heterogeneity test. Classic "difference between significant and non-significant is not itself significant."
- **Fix:** (1) Present both hybrid ΔNB estimates with CIs side by side in one quantitative row; (2) state explicitly they are not statistically distinguishable and the "confirmed vs not-confirmed" labeling reflects which side of zero each noisy CI fell on, not a demonstrated difference; (3) add that the design is not powered for a cross-country heterogeneity/interaction test and none was performed. Replace near-miss/confirmed dichotomy with estimates+intervals. Keep the existing cautionary framing (the "headline leans on Colombia" charge was adjudicated *overstated*).

### 3.6 Specify the bootstrap protocol — MAJOR
- **Location:** §2.13; Table 7; §3.11.
- **Problem:** The cluster bootstrap is the sole inferential engine, yet B is never stated, the resampling procedure is named not described, the CI construction method (percentile/BCa/bootstrap-t) is unspecified, and there is no rule for degenerate one-class resamples. Confirmatory cells are sparse (8 and 5 clusters), where percentile CIs are unstable.
- **Fix:** Add to §2.13: B (+ Monte-Carlo error on endpoints); the resampling unit/procedure (resample clusters with replacement, retain all within-cluster rows); the CI construction method actually used; the degenerate-resample handling rule (with rejection fraction). Prefer cluster bootstrap-t or BCa over percentile for sparse ΔNB cells, or explicitly acknowledge percentile-CI fragility and lean on the underpowered caveat.

### 3.7 Report model specification, EPV, exact penalty — MAJOR
- **Location:** §2.8 (p.6); §2.9 (p.6); §2.11.
- **Problem:** Predictors only in prose; no feature list, parameter count, DLNM cross-basis df, or EPV against 1,593 events. "Large-penalty approximation to maximum likelihood" names neither penalty type, strength, nor tuning — and sits oddly against M1's slope 1.246. The §2.11 promised fallback fraction is never reported.
- **Fix:** Add a model-specification table (per M0–M5: every term, lag/harmonic counts, 26 FE levels, DLNM cross-basis df, total params; EPV vs 1,593 events). Replace "large-penalty approximation" with the exact method (L2/ridge with λ and how chosen — fixed vs CV on training folds only — or Firth) + software/package/version + convergence/separation criteria. Report the recalibration fallback fraction, or state it was zero.

### 3.8 Calibration uncertainty and flexible curves — MAJOR
- **Location:** Tables 1/3/6; §2.10–2.11; §3.4.
- **Problem:** CITL/slope are point estimates only (M1 slope 1.246, M3 0.738), no CIs, no clustered calibration regression, yet "overfitting"/"insufficient spread" interpretations are drawn. Intercept-plus-slope recalibration "considered" but never reported. No flexible (loess) calibration curve (Fig 3 is a CITL bar chart). M1's 1.246 never interpreted.
- **Fix:** Add RDHS-cluster-bootstrap CIs for CITL/slope in Tables 1/3/6; fit the calibration model with clustering; interpret slope only where the CI excludes 1. Add ≥1 loess calibration curve with CIs per model in the test period, focused near p\*=0.30. Report intercept-plus-slope recalibrated CITL/slope/NB@0.30 alongside intercept-only in Table 3, or state why it fell back. Interpret M1's slope 1.246 (mild insufficient spread by the paper's own rubric).

### 3.9 Real-time vs finalized counts — MAJOR
- **Location:** §2.3 (p.3), §2.6 (p.5); §4.10 (p.21).
- **Problem:** M1 uses finalized, retrospectively-completed WER counts, not the provisional real-time counts an operational EWS sees at week t; climate (ERA5-Land/CHIRPS) is genuinely near-real-time. The AR benchmark is handed cleaner-than-reality information; reporting delay is only generic future work.
- **Fix:** Either (a) impose realistic reporting-delay/right-truncation (nowcast-style censoring of the most recent 1–4 weeks) on the recent-case features and refit M1, or (b) qualify the central claim to "**finalized** recent surveillance is hard to beat retrospectively" and foreground reporting delay as the key unresolved threat. Add a censoring sensitivity if feasible.

### 3.10 Complete the TRIPOD/PROBAST self-assessment artifact — MAJOR
- **Location:** §2.15 (p.8).
- **Problem:** §2.15 claims a "structured PROBAST/TRIPOD-style self-assessment" in two narrative sentences — no completed checklist with page locators, no PROBAST domain table, no signalling-question judgments.
- **Fix:** Either (a) add the completed instruments as SI and cite from §2.15 (TRIPOD+AI checklist with page locators; PROBAST table with low/high/unclear judgments for all four domains, per setting), or (b) soften to a "narrative risk-of-bias discussion mapped to PROBAST/TRIPOD domains." Option (a) preferred given the framing.

## 4. Minor issues (targeted edits, no restructuring)

- **Contemporaneous (lag-0) primary climate feature** (§2.5; §3.6/Table 4): do **not** restructure to DLNM-primary (that comparator already loses with CIs excluding zero). Instead report the cross-basis lag span (confirm it reaches ~12–16 wk), add 12/16-week points to the simple sweep (or justify the 8-week cap), note the week-t feature predicts a t+4 target (4-week effective lead), and foreground that Table 4 climate numbers are **best-lag**.
- **Multiplicity** (Table 7; §3.11): state the total contrast count (regimes × thresholds × horizons × labels × settings); frame all cells as exploratory/not multiplicity-protected with per-setting ΔNB(M5−M1)@0.30 as the single confirmatory contrast; note Colombia [0.012, 0.026] is a nominal unadjusted bootstrap interval.
- **Single temporal holdout** (§2.9/2.15/4.10): add a rolling-origin refit of M0–M3 (AUC/Brier/NB₀.₃₀ across origins, median/IQR) or at minimum cluster-bootstrap CIs on Table 1 headline metrics.
- **Clustered CIs on Tables 1–3** (§2.13): attach RDHS-cluster CIs to headline cells (AUC, Brier, CITL, NB₀.₃₀) and Table 3 CITL.
- **Percentile label vs outbreak definition** (§2.7/4.10): strengthen the caveat; add ≥1 operationally grounded label (endemic channel / mean+2SD, or absolute trigger) as secondary; report whether surveillance-beats-climate holds at rare onset events; at minimum report the climate-vs-surveillance ranking at the existing 90th-pct label.
- **Climate-vs-AR horizon fairness** (§3.9/Fig 4; §4.2–4.3): add climate-vs-M1 ΔNB with CIs in AUC-crossover cells (75th h=12; 90th h=8/12); note both models' NB is near zero there.
- **Prevalence vs threshold fairness** (§3.3–3.4): *overstated* — no new analysis; add 1–2 sentences that p\*=0.30 sits just below realized prevalence (0.336 SL; 0.375 Colombia) and the M1 ranking holds/widens at 0.34/0.40.
- **MAUP / climate aggregation** (§2.5/4.10): specify zonal weighting (pop vs area), ERA5-Land/CHIRPS regridding onto the 26-polygon frame, coastal masking; add a within-RDHS CV change-of-support check.
- **Denominator circularity/trend** (§2.4): brief sensitivity (alt Ampara/Kalmunai split; ±2%/yr or dual-anchor 2012+2024); one Limitations sentence that denominators are single-anchored to 2024 and the intra-Ampara split is WorldPop-derived/unvalidated.
- **Queen graph unused** (§2.2/2.4): report Moran's I on test residuals, add a BYM2 robustness check, or trim the "BYM2-compatible backbone" claim to one sentence.
- **WER→ISO correction not validated** (§2.6/3.6): add the per-year offset distribution (rows shifted 0/1/2 wk), validate against a sample of WER PDF returns-cutoff dates (agreement rate), state how many pairs differ between v1 and v2.
- **Missingness reporting** (§2.3/2.9/3.1): state the training-period imputation rule + fraction imputed; split the 10,705→10,516 accounting by missing-outcome vs missing-climate; missingness by train vs test; one complete-case-vs-imputed robustness check.
- **Cost-effectiveness "overreach"** (§4.8/4.10): *already addressed* — optional illustrative one-way break-even; optionally soften "Hybrid systems are more plausible."

## 5. Reference audit

**Consistency:** reconcile the **24-vs-23** entry count; harmonize "Epidemiology Unit (2025)" vs "(2018–2025)"; enumerate the "Hussain-Alkhateeb et al." authors in the list itself; TRIPOD 2015 is cited but **TRIPOD+AI (2024)** — the current standard — is absent; DCA referencing is thin (only Vickers & Elkin 2006).

**Suspect / placeholder (add DOIs/versions, de-duplicate):** Climate Hazards Center (2026) vs Funk 2015; WorldPop (2025, "2015–2030") vs Tatem 2017 — state these are projected denominators; Copernicus C3S (2019, "accessed 2026") — add the CDS DOI; verify the **2024 Sri Lanka census** published district totals in time to anchor 2018–2025 (prior census was 2012); if preliminary, label as such.

**Missing — most consequential first:**
1. **Colombia data source — the single most serious omission.** The 13,361-obs Colombia replication has **no provenance citation**. Add **OpenDengue (Clarke et al. 2024, *Scientific Data*)** and/or SIVIGILA (INS Colombia).
2. **Lowe et al.** dengue-EWS benchmark work (e.g. *Lancet Planetary Health* 2021).
3. **WHO/TDR EWARS / PAHO EWAR** operational framework.
4. **DCA standards** beyond Vickers-Elkin 2006: Vickers, Van Calster & Steyerberg (2016, *BMJ* 352:i6) + the step-by-step guide (2019, *Diagnostic and Prognostic Research* 3:18).
5. **Cameron, Gelbach & Miller (2008)** for cluster-bootstrap inference (+ a spatial/Moran anchor).
6. **Steyerberg & Vergouwe (2014)** + a flexible (loess) calibration-curve reference.
7. **TRIPOD+AI (Collins et al. 2024, *BMJ* 385:e078378)**.
8. **Saito & Rehmsmeier (2015)** for PR-AUC under imbalance.

Nothing appears fabricated, but the list is under-referenced on methodology/EWS benchmarks, over-weighted toward data-source/reporting-tool citations, and carries an **unsourced Colombia dataset** that must be fixed before submission.

## 6. Target journal — PLOS Neglected Tropical Diseases (primary, with conviction)

Most-cited venue in the manuscript's own reference list (Hussain-Alkhateeb, Mordecai, Huber); its editors/reviewers already publish dengue EWS and climate-suitability work; it explicitly values cautionary/negative/replication results judged on rigor not novelty — exactly suited to this message. Acceptance risk moderate (expect pushback on the single holdout, percentile labels, and the Colombia/8-cluster lean — all on the fix list).

**Alternatives:**
1. **Diagnostic and Prognostic Research (BMC)** — strongest methods fit and safest acceptance (its core refs are literally cited here); smaller, methods-focused readership.
2. **BMC Infectious Diseases / BMC Public Health** — high-reach, methodologically tolerant fallback.
3. **PLOS Climate** — only if foregrounding the climate angle; higher risk of reading as under-selling climate.

**Biggest framing change:** pivot from a negative finding to a **positive methodological prescription with an empirical demonstration** — *"the first surveillance-benchmarked, calibration-aware, decision-curve evaluation of climate-informed dengue EWS."* Converts the novelty disclaimer from weakness into a scoped first-of-its-kind claim and pre-empts the "just a negative result" desk-reject reflex.

## 7. Restructuring plan for PLOS NTDs

Target ~5,000–6,000-word main text, IMRaD, heavy SI use; surface the framework + two-country evidence, move provenance/engineering machinery to SI.

- **Title/Abstract (rewrite first):** framework-forward title, e.g. *"Surveillance-benchmarked, calibration-aware, decision-curve evaluation of climate-informed dengue early warning: evidence from Sri Lanka and Colombia."* Structured ~250–300-word abstract: the evaluation gap; the framework as contribution; the two-setting design with Colombia named exploratory; the headline **with operational translation**; the prescriptive takeaway. Drop any implication of symmetric two-country validation.
- **Author summary** (PLOS NTDs requires one, ~150–200 words, plain language): the prescription + modest/setting-dependent finding.
- **Introduction (~600–800 w):** lead with the operational question and the evaluation-standard gap; keep the §4.2 framing that recent surveillance summarizes upstream climate effects; end with the scoped novelty claim.
- **Methods (main ~1,800–2,200 w):** keep settings, outcome/labels (+ new operational label), M0–M5 *with spec table*, DCA/p\* *with justification*, calibration, *fully-specified* bootstrap, 1-paragraph RoB → SI. **Move to SI:** full WER→ISO audit + offset distribution, Ampara–Kalmunai dissolve + denominator formula/208-record table, queen adjacency, climate aggregation/regridding, completed TRIPOD+AI/PROBAST instruments.
- **Results (~1,600–2,000 w):** economize to ~4–5 display items — Table 1 *with CIs + standardized NB*; DCA figure (Fig 2) *with annotated axes*; condensed horizon/label panel (Fig 4); cross-setting comparison *as a quantitative estimates+CIs table* (replacing qualitative Fig 6). Move Tables 2/3/5/6/7 and Figs 1/3/5 to SI or merge. Lead with M1-beats-climate + operational translation; present Colombia with COVID-exclusion sensitivity and the discordance reframing.
- **Discussion (~1,200–1,500 w):** lead with the evaluation prescription; then the modest/setting-dependent finding; tighten Limitations to *name* reporting-delay, single holdout, percentile labels, MAUP, Colombia COVID window; split implications into (a) well-supported methodology recommendations vs (b) substantive climate claims capped at "one modest confirmed increment in one external setting, not cost-justified or transportable."
- **Data and Code Availability (new, mandatory):** repo + Zenodo DOI + artifact list/fetch script + OSF preregistration DOI.
- **Figure/table economy:** ~4–5 main display items, rest to SI. Cut the "BYM2 spatial backbone" prominence unless a Moran's I / BYM2 check is added.

## 8. Revision checklist (ordered)

1. Execute the **framing pivot** (title/abstract/author summary/intro): framework as contribution; Colombia explicitly exploratory; disclaimer → scoped first-of-its-kind claim.
2. Resolve **"registered"**: cite the OSF/registered-threshold object by DOI everywhere, or delete the word; justify p\*=0.30 via its ~0.43:1 cost ratio (Tozan 2023) or an elicited range; report the threshold range over which conclusions hold.
3. Add the **Data and Code Availability** section (repo + Zenodo DOI + license + artifact release/fetch script + OSF DOI).
4. Add the **Colombia data-source citation** (OpenDengue/SIVIGILA) — non-negotiable.
5. Run the **Colombia COVID-exclusion sensitivity**; report whether ΔNB₀.₃₀ still excludes zero; state date range + per-year counts; foreground as a named threat; soften the Abstract if it does not survive.
6. **Translate every headline NB/ΔNB** into operational units; annotate axes + footnotes; add the per-100 Abstract sentence.
7. **Reframe the two-setting discordance** (side-by-side ΔNB + CIs; not-distinguishable statement; no-heterogeneity-test caveat; estimates+intervals language).
8. **Fully specify the bootstrap** (B, unit/procedure, CI method, degenerate-resample rule; prefer BCa/bootstrap-t for sparse cells).
9. **Add the model-specification table + EPV + exact penalty/tuning + recalibration fallback fraction.**
10. **Add calibration CIs (cluster-bootstrap), a loess calibration curve, intercept-plus-slope recalibration results, and the M1 slope=1.246 interpretation.**
11. **Address real-time vs finalized counts**: censoring sensitivity or qualify the headline; foreground reporting delay.
12. **Complete and attach the TRIPOD+AI checklist + PROBAST domain table as SI** (or soften §2.15).
13. **Minor analytics bundle** (§4): cluster-bootstrap CIs on Tables 1–3; operational outbreak label; climate-vs-M1 ΔNB CIs in crossover cells; rolling-origin refit or CIs; DLNM lag span + extend sweep to 12/16 wk; multiplicity count + Colombia nominal-CI caveat; prevalence-vs-threshold sentences; MAUP spec + CV check; denominator sensitivity; queen-graph Moran's I or trim; WER→ISO offset distribution + agreement rate; missingness flow.
14. **Fix references** (§5): reconcile 24-vs-23; harmonize the Epidemiology Unit year; add DOIs/versions; de-duplicate CHIRPS/WorldPop/ERA5 placeholders; enumerate Hussain-Alkhateeb authors; add Lowe et al., WHO/PAHO EWARS, DCA standards, Cameron-Gelbach-Miller, Steyerberg & Vergouwe, TRIPOD+AI 2024, Saito & Rehmsmeier.
15. **Restructure to PLOS NTDs** (§7): tighten main text, ~4–5 display items, machinery + instruments to SI, add author summary, split Discussion implications.
16. **Final consistency pass**: every "confirmed/near-miss" claim, every threshold reference, and every NB figure axis consistent with the revised translations and the de-registered/justified p\*.

---

*Generated 2026-06-26 via a multi-agent expert panel (6 reviewers + reference auditor + journal-fit analyst → chair consolidation → per-issue adversarial verification → editor synthesis). Manuscript locations cited inline by section/table/figure and page.*
