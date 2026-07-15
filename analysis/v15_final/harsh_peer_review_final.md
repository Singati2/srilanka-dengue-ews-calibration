# Adversarial peer review — PLOS Global Public Health

**Manuscript:** "Standard evaluation can overstate climate's added value for dengue alerting: a matched-baseline, decision-curve reanalysis in Sri Lanka and Colombia" (Shiwakoti, Khadka, Thapa).
**File reviewed:** `paper1_plos_gph_C2_final.tex` (read end to end, incl. abstract, methods, results, discussion, declarations, references, SI captions).
**Reviewer stance:** hostile, inclined to reject; the settled-context items (direction/precision of the two matched estimands, demotion of M4−M1, provenance-to-1.1e-16, known author-action blockers) are accepted as given and stress-tested, not re-litigated.

Severity scale: **fatal** (invalidates a central claim) / **major** (threatens a conclusion, needs substantive work) / **moderate** / **minor** / **presentation**.
Status: resolved / partially-resolved / unresolved-but-disclosed / unresolved-submission-blocking.

---

## 0. One-paragraph orientation

This is, on its own text, a **null-to-negligible empirical result wrapped around a methodological cautionary tale**. The prespecified primary contrast (Sri Lanka M4−M1) is null and is demoted for being non-nested. Every positive/interpretive statement in the paper now rests on a **post-hoc, specification-matched decomposition (M5−M5_no-climate)** whose most-appropriate confidence intervals **include zero in both settings** (Sri Lanka raw CI [−0.0015, +0.0188]; Colombia development-inclusive CI [−0.0001, +0.0244]). The single interval that excludes zero for a quasi-climate contrast (Sri Lanka frozen M5−M1, +0.015 under past-only recalibration) is simultaneously **not specification-matched** and **recalibration-dependent** — i.e., it is exactly the contrast the authors themselves disqualify from interpretation. The paper is unusually, even self-flagellatingly, honest about all of this. The central editorial question is therefore not "is the science fraudulent or broken" (it is neither, and it reproduces to machine precision) but "does a post-hoc, zero-including, recalibration-fragile increment, plus a standard incremental-value decomposition, clear the bar for a research article, and are the residual handling/comparability defects and hard submission blockers resolved." My judgment: not yet.

---

## 1. Novelty

**1.1 — Thin novelty; the paper concedes most of it away.** *Severity: major (for a journal that still expects a defined contribution) → moderate (given PLOS GPH's sound-science remit).* Location: Introduction ¶4–5 (lines 90). The authors explicitly disclaim novelty for (a) benchmarking against surveillance (Lowe2013, Benedum2020), (b) calibration/DCA in dengue (Sangkaew2026), and (c) the empirical "climate is weak beyond recent cases" claim (Johansson2016, "the empirical result is confirmatory"). The residual "genuinely novel piece" is the matched-baseline attribution. But a nested-model incremental-value decomposition (remove a feature block, refit, compare net benefit) is **textbook added-predictor / incremental-value analysis** (Vickers 2016, cited by the authors themselves). Applying a standard decomposition to two new datasets is a competent contribution, not a methodological innovation. Why it threatens the paper: the abstract and discussion lean on "the contribution is primarily methodological," yet the method is standard and the empirical payload is a disclosed null. Status: **unresolved-but-disclosed** — honestly scoped, but the editor must decide whether it suffices.

## 2. Epidemiologic / public-health relevance

**2.1 — The one operating regime that matters is where the signal vanishes.** *Severity: major.* Location: Colombia robustness (line 294), reporting-delay sensitivity: three-week matched increment falls to +0.0049 (95% CI +0.0001 to +0.0097), lower bound ≈ 0. The authors correctly note operational surveillance is delayed by weeks and even "final" climate products lag. So the climate-specific increment is largest under finalized, best-case, concurrent data and **decays toward zero under the delayed-surveillance regime in which an EWS actually operates**. This is disclosed ("we read this as a limitation, not as support") but it hollows out the public-health case: the paper cannot claim operational value in the regime it purports to inform. Status: **unresolved-but-disclosed.**

**2.2 — Magnitudes are explicitly un-costed and "ordinal."** *Severity: moderate.* Location: §2.8 (line 125), Discussion (line 395). p*=0.30 is "not an empirically established public-health threshold," "not elicited from stakeholders," "not derived from a documented response-cost analysis." The authors then say net-benefit magnitudes "should be read as ordinal until costed." A ΔNB of 0.008 at an admittedly arbitrary threshold, with intervals crossing zero, has no anchored operational interpretation. The "1.9 net TP / 4.4 fewer FP per 100 municipality-weeks" translations (line 286) are two monotone rescalings of one CI presented as if two results, and are explicitly "not observed outbreaks/alerts/lives." Status: **partially-resolved** (honestly hedged, but relevance remains unquantified).

**2.3 — Estimand is "elevated activity" (~1/3 of weeks), not outbreak.** *Severity: moderate.* Location: line 104, 389, 399. Even the 90th-percentile stricter label leaves ~23.5% prevalence. This is not rare-epidemic early warning, and the framing "dengue alerting" risks over-reading by readers who equate EWS with outbreak prediction. Disclosed. Status: **resolved (as disclosure).**

## 3. Validity of the predictive method

**3.1 — Single temporal holdout for the primary setting; authors concede "exploratory/hypothesis-generating."** *Severity: major.* Location: line 128, 399. Sri Lanka uses one train/test split (2018–2022 / 2023–2025), not rolling-origin or spatial-block. For a paper whose thesis is rigorous evaluation, the primary analysis does not meet the standard it advocates. Status: **unresolved-but-disclosed.**

**3.2 — Cross-country implementations differ so much the "same ladder" is nominal.** *Severity: major.* Location: line 101, 113. SL uses a DLNM-style cross-basis (temp, precip, humidity; lags 0–8; df=3); Colombia uses linear temp/precip lags, **no humidity**; penalty type and tuning differ. The paper leans on the matched contrast "having the same meaning in both countries" (line 351) — but the exposure sets themselves differ, so even the matched estimand is not like-for-like across settings. The "consistently-signed increment in both settings" headline therefore compares two differently-defined climate blocks. Status: **partially-resolved** (disclosed, reframed as "two case studies," but the cross-setting synthesis still exploits a comparability it disclaims).

## 4. Estimand clarity, post-hoc honesty, and sufficiency

**4.1 — The interpretive centerpiece is post hoc, and the prespecified primary is null.** *Severity: major — this is the manuscript's defining credibility problem.* Location: Table `analysisstatus` (line 130 ff.) still lists M4−M1 as "Planned primary"; §"Estimand hierarchy" (line 168–173) states "All cross-setting statements concerning the incremental predictive value of climate are therefore based exclusively on the specification-matched M5−M5_no-climate contrast," which line 169 confirms was "not part of the original design-locked model ladder in either setting … post hoc, exploratory." So the paper's entire positive content is carried by an analysis constructed after data inspection, while the one contrast fixed before the data (M4−M1) returned nothing. This is HARKing-adjacent (garden of forking paths). The mitigation is real and substantial — the authors do **not** relabel it "primary," retain and report M4−M1 as null, and repeatedly call the matched contrast a "diagnostic." But a hostile reader will still see a paper whose only forward-looking claim is a post-hoc estimand that **includes zero under the appropriate uncertainty in both settings**. Honesty of disclosure: high. Sufficiency of that honesty to license the interpretive weight placed on it: not established. Status: **partially-resolved.** *Direct answer to the editor's probe: yes, resting interpretation on a post-hoc estimand while the prespecified one is demoted is a credibility problem; it is defused as a transparency failure but not as an inferential one — the finding must be labeled hypothesis-generating throughout, including in the title and abstract, which currently assert a directional "added value … can be overstated" conclusion that reads as stronger than a zero-including post-hoc diagnostic supports.*

**4.2 — Over-disclosure obscures the estimand rather than clarifying it.** *Severity: presentation → moderate.* Location: abstract (line 74–76), which juxtaposes at least five different ΔNB numbers (M4−M1 raw/recalibrated, Colombia compound +0.0188, matched +0.0078, three-week +0.0049, SL matched +0.0087, SL frozen M5−M1 +0.015) with different recalibration states and uncertainty definitions in a single paragraph. A reader cannot extract one defensible headline number. Paradoxically the transparency becomes a comprehension barrier and signals the authors' own difficulty locating a robust result. Status: **unresolved (presentation).**

## 5. Model comparability

**5.1 — The frozen Sri Lanka M1 confounds regularization with features.** *Severity: major.* Location: line 263, 357. The frozen M1 is "near-unpenalized C=10^6, AR-only standardization," while M5 is penalized/tuned with whole-design standardization. So frozen M5−M1 mixes a feature difference with a **penalization-and-scaling difference**. The authors know this — it is why they built M5_no-climate. But then the single zero-excluding SL number they report (frozen M5−M1 = +0.015, past-only recalibration) is precisely this contaminated, non-matched contrast (line 357). Emphasizing the one "significant" figure that the paper's own methods section disqualifies is an internal contradiction the reviewer cannot let pass. Status: **partially-resolved** (contradiction disclosed but still foregrounded).

**5.2 — M1 differs between countries, so benchmark-level comparisons are non-comparable.** *Severity: moderate.* Location: line 113, 351. SL M1 = cases + harmonics + RDHS FE; Colombia M1 = cases only. Disclosed; cross-setting claims restricted to the matched estimand. Status: **resolved (as disclosure).**

## 6. Calibration handling

**6.1 — The primary hybrids were not recalibrated in the frozen pipeline; the frozen primary contrasts are raw-vs-raw, contradicting the paper's own thesis.** *Severity: major.* Location: line 243 (explicit: "the primary hybrid models M4 and M5 were therefore *not* recalibrated … a limitation"), line 356–357. A paper arguing "judge by calibrated decision-curve net benefit" computes its frozen primary hybrid contrasts on **uncalibrated** predictions, and the sign of the conclusion **flips** when calibration is applied (M4−M1: −0.008 raw → +0.009 cross-fit → +0.010 past-only). The corrective recalibrations are all post hoc, and the cross-fit variant is "optimistic" (concurrent test-period weeks). So the calibration handling in the confirmatory analysis is inconsistent with the manuscript's central methodological claim, and the direction of the primary result is calibration-contingent. Status: **unresolved-but-disclosed.**

**6.2 — Colombia calibration never actually achieves calibration.** *Severity: moderate.* Location: line 286. After validation-fit Platt, **every** model still over-predicts (CITL −0.45 to −0.54, Brier 0.213–0.250) across the pandemic regime shift; slopes range 0.85–3.43. Per-model mean predicted probabilities "not retained" (line 286, 314) — a reproducibility gap in a calibration-centric paper. The M5−M1 net-benefit contrast is thus drawn between two miscalibrated models. Status: **partially-resolved** (calibration limitation flagged; missing mean-predicted values are a provenance gap).

## 7. Decision-curve methodology

**7.1 — The primary Sri Lanka "decision curve" (Fig 2) is four points joined by straight lines.** *Severity: presentation → moderate.* Location: Fig 2 caption (line 238): "line segments connect them and do not represent a recomputed continuous grid." For the flagship setting, the DCA is four thresholds, not a curve; the dense grid exists only for Colombia. Status: **unresolved (presentation).**

**7.2 — Effect sizes sit near the numerical noise floor of DCA.** *Severity: moderate.* Location: throughout — ΔNB reported to the 4th decimal (e.g., +0.0078, +0.0087, difference of 0.0006 between M5−M1 and M5−M5_no-climate discussed at line 263). Distinguishing 0.0078 from 0.0087 is not epidemiologically meaningful and invites over-interpretation of decimal-place differences. Status: **unresolved-but-disclosed.**

## 8. Inference (conditional bootstrap; 26 / 8 clusters)

**8.1 — The bootstrap does not refit models; all "excludes zero" claims are conditional only.** *Severity: major.* Location: line 127–128 ("The intervals therefore reflect conditional test-set sampling uncertainty and do not capture model-development uncertainty"), line 291. Where development uncertainty *is* added (Colombia), the matched interval moves from [+0.0039, +0.0119] to [−0.0001, +0.0244] — **it now includes zero**. So the only matched interval that excludes zero does so **only because it omits model-development uncertainty**. Combined with §4.1, the honest synthesis is: **no matched, development-robust, zero-excluding climate result exists in either setting.** Status: **unresolved-but-disclosed** (and, in my view, decisive against the directional framing).

**8.2 — Few clusters; 8-cluster CIs conceded invalid; wild-bootstrap is not independent validation.** *Severity: moderate.* Location: line 128, 345 ("only eight clusters … not interpretable as a valid bootstrap confidence interval"), line 263/394 (wild-cluster-bootstrap-t is "a secondary, single-implementation sensitivity … not independent validation"). 26 clusters gives imperfect percentile coverage; the authors flag it. Status: **partially-resolved.**

## 9. Reproducibility / provenance

**9.1 — Python modeling-stack versions not preserved.** *Severity: major (reproducibility) / submission-blocking.* Location: line 115, 535 (only R 4.6.0 / dlnm etc. pinned; "Python modeling-stack versions not preserved"). The entire penalized-logistic ladder — i.e., the models carrying the result — runs in an unpinned Python environment. Reproduction "to ≤1.1e-16" (settled context) demonstrates internal determinism from frozen artifacts, **not** independent re-executability from source. Status: **unresolved-submission-blocking.**

**9.2 — Frozen prediction CSVs git-untracked; provenance rests on author attestation.** *Severity: moderate (per settled context, high but non-cryptographic).* The chain from raw data to frozen predictions is not cryptographically pinned. Acceptable if S10 checksums + attestation are provided; currently pending. Status: **unresolved-submission-blocking.**

**9.3 — OpenDengue v1.3 has no version-specific record identifier or acquisition date.** *Severity: moderate.* Location: line 104, 412. The analyzed archive cannot be uniquely re-retrieved. Status: **unresolved-submission-blocking.**

## 10. Transparency & interpretation restraint

**10.1 — Restraint is exemplary, arguably excessive.** *Severity: minor / strength.* The paper argues its own null more forcefully than a critic would (line 294, 351, 401, 405). This is a genuine strength and largely inoculates against over-claiming. The flip side (§4.2) is legibility and the question of whether a paper this hedged has a positive finding to report at all. Status: **resolved (strength).**

## 11. Colombia complete-case selection

**11.1 — Severe, incompletely-bounded selection toward high-incidence, well-reporting units.** *Severity: major.* Location: line 365–366, 401. Analyzed subset = 13,361 of 21,646 test municipality-weeks (62%), ≈19% of a full panel; included vs excluded differ starkly (mean recent cases 11.1 vs 1.9; prevalence 0.375 vs 0.180). The K-completeness sensitivity shows the estimate **grows** with completeness (+0.0078 at ≥1 wk → +0.0126 at ≥40 wk), which the authors correctly say "may reflect a further-shifted target population rather than removal of bias." The IPW sensitivity is weak: inclusion covariates barely discriminate (mean modeled inclusion prob 0.63 vs 0.60), so the reweighting is nearly inert and cannot adjust for unmodeled completeness drivers. Net direction of bias is declared uncertain and the estimand is restricted to the analyzed subset. Consequence: the Colombia "positive" is concentrated in exactly the best-reporting, highest-incidence municipalities — the least representative of the sparse-reporting settings where EWS value is most needed. *Direct answer to the editor's probe: the selection is thoroughly disclosed and one sensitivity (IPW) is attempted, but it is not adequately bounded — bias direction is unresolved, IPW is near-inert, and completeness-stratification points to target-population shift; the generalizability claim is therefore not secured, only honestly fenced.* Status: **unresolved-but-disclosed.**

**11.2 — COVID-era test window + static recalibration across a regime shift.** *Severity: major.* Location: line 286, 393. Colombia test = 2020–2022 (includes 2020–2021 pandemic disruption of both transmission and surveillance); recalibration is a static Platt fit on 2018–2019 (including the 2019 record epidemic) applied across the pandemic break. The only within-pandemic-free check (2022-only) is itself higher-prevalence and not "post-pandemic." The pre-pandemic window is confounded by the 2016 dengue–Zika co-circulation and 2019 epidemic (line 294) and explicitly "uninterpretable." So the Colombia increment is conditioned on a pandemic-era window with a mismatched recalibration and no clean out-of-pandemic confirmation. Status: **unresolved-but-disclosed.**

**11.3 — "Same logic" overstates cross-setting recalibration comparability.** *Severity: moderate.* Location: line 118. SL = rolling time-updated intercept recalibration; Colombia = static validation-fit Platt. The two headline increments therefore arise under **different** recalibration regimes, yet are juxtaposed as "consistently signed." Disclosed at line 118/393. Status: **partially-resolved.**

## 12. Journal fit (PLOS Global Public Health)

**12.1 — Fit is plausible but the "so-what for global public health" is thin.** *Severity: moderate.* PLOS GPH judges on soundness and valid conclusions rather than novelty/impact, which *helps* this paper (the methods are sound and conclusions are matched to evidence). But GPH still expects a global-health-relevant message; here the actionable message reduces to "don't benchmark climate EWS against weak comparators, and match structure before crediting climate" — a reasonable methods lesson, supported by an essentially null empirical core, in a regime (finalized counts, arbitrary threshold) that the authors admit is not operational. It reads closer to a methods/commentary contribution than an empirical advance. Status: **partially-resolved.**

---

## 13. Direct answers to the three editorial probes

1. **Post-hoc "primary" vs demoted prespecified — credibility problem?** Yes. It is HARKing-adjacent and is the manuscript's defining vulnerability. It is neutralized as a *transparency* failure (fully disclosed, prespecified null retained and reported) but **not** as an *inferential* one: the forward-looking claim rests entirely on a post-hoc estimand whose appropriate intervals include zero in both settings. The directional framing in the title/abstract exceeds what a zero-including post-hoc diagnostic licenses.

2. **Does recalibration-dependence of the only zero-excluding result undercut the headline?** Yes, substantially. The lone zero-excluding quasi-climate contrast (SL frozen M5−M1 +0.015) is *both* non-specification-matched *and* recalibration-dependent (past-only), and the Colombia matched result excludes zero only under conditional (development-omitting) bootstrap. The "small, consistently-signed climate increment" headline is thus an artifact of which recalibration and which uncertainty definition are foregrounded. This is disclosed but not resolved.

3. **Is the Colombia selection adequately bounded?** No. It is thoroughly *disclosed* and one (near-inert) IPW sensitivity is run, but the bias direction is unresolved, completeness-stratification indicates target-population shift, and inference is restricted to a high-incidence, well-reporting subset. Bounded honestly; not secured.

---

## 14. What would move this toward acceptance

- Reframe title/abstract to a **hypothesis-generating / methods-cautionary** register; remove any directional "added value" wording not supported by a zero-excluding, matched, development-robust interval (there is none).
- Compute the specification-matched estimand under (a) a *calibrated* frozen pipeline (recalibrate M4/M5 within the frozen run, not only post hoc) and (b) development-inclusive bootstrap in **both** settings; report those as the primary uncertainty. Stop foregrounding the non-matched, recalibration-dependent frozen M5−M1 +0.015.
- Add rolling-origin/spatial-block validation for Sri Lanka, or explicitly restrict all Sri Lanka claims to "single-holdout, exploratory."
- Resolve submission blockers: pin the Python environment; deposit frozen artifacts with checksums under a persistent identifier; supply the OpenDengue v1.3 version-specific identifier + acquisition date; complete ethics, funding, competing-interests, contributions; retain per-model mean predicted probabilities for Colombia.
- Consolidate the numeric thicket into a single estimand table (contrast × recalibration state × uncertainty definition) so a reader can locate one defensible number.

None of these is a validity repair — the analysis is sound and reproduces — but together they exceed "minor author checks."

---

## Verdict

**NOT READY — MAJOR REVISIONS REMAIN**
