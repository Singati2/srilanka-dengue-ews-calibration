# Reviewer response (final) — point by point

We thank the reviewers. Their two headline requests — a Sri Lanka specification-matched decomposition and a past-only recalibration — prompted a reconstruction that uncovered and corrected an error in our own methods description. We summarize the changes; the manuscript is `paper1_plos_gph_C2_final.tex`.

**1. Sri Lanka M1 was described incompletely.** The frozen Sri Lanka M1 is recent incidence lags (t, t−1, t−2, t−4) **plus seasonal harmonics plus RDHS fixed effects** — a structured surveillance benchmark — not cases-only. Colombia's M1 is cases-only. The two baselines differ **by design**, each fixed in its own dated design-lock specification. We corrected the ladder description to be country-specific and no longer assert a universal M1 definition.

**2. Provenance / pre-specification.** The dated design-lock spec (commit 1d8e268, 2026-06-14 13:24) that defines the structured Sri Lanka M1 is a DAG ancestor of the results report (02f986e, same day 14:33) on `main`; the spec line defining M1 was never edited after introduction; filesystem timestamps corroborate that the spec was written (13:15) before the frozen predictions were generated (13:32); the report hash-pins the spec. This supports pre-specification of the **model ladder and the structured M1** to a high (non-cryptographic) standard. **Qualification we now disclose:** the frozen prediction files are archived outside version control, so this ordering rests on timestamps plus an author-produced report and our attestation, not tamper-proof evidence; we provide a coauthor attestation and will archive checksummed frozen artifacts to a tamper-evident repository. Pre-specification applies to the **ladder/M1 only**, not to the revision-stage matched estimand.

**3. Exact reproduction.** We reconstructed the frozen pipeline and reproduced the committed M1/M4/M5 test predictions to ≤1.1×10⁻¹⁶ over all 3,926 rows before reporting any new number; the gate refuses to report otherwise.

**4. Specification-matched decomposition (both settings, now primary but post hoc).** The only clean climate estimand is ΔNB(M5 − M5_no-climate), where M5_no-climate is M5 with only the climate block removed, independently refit under the same protocol. Sri Lanka +0.0087 (95% CI −0.0015 to +0.0188); Colombia +0.0078 (95% CI +0.0039 to +0.0119). We designate this the primary interpretable contrast **and disclose it as post hoc / exploratory** — it was reported for Colombia in the original submission and constructed analogously for Sri Lanka in this revision; it was **not** part of the design-locked ladder in either setting.

**5. M4 − M1 retained but demoted.** The prespecified M4 − M1 is kept for transparency as a design-locked secondary diagnostic. Because M4 and M1 are non-nested and differ structurally beyond climate, it does **not** isolate the incremental value of climate; we do not rest the climate interpretation on it, and we do not call it "confounded."

**6. M5 − M1 is not a matched contrast.** Although M5 and the Sri Lanka M1 share AR+season+RDHS terms, the frozen M1 was fit under different penalization/standardization (near-unpenalized C=1e6, AR-only standardization) than M5; so M5 − M1 (+0.0081) conflates climate with fitting differences and is reported only as the frozen-pipeline contrast, with an explicit reconciliation to the matched +0.0087 (≈0.0006 gap explained by the refit).

**7. Corrected Colombia timeline.** The Colombia matched decomposition was in the **original submission**; the Sri Lanka matched decomposition is **new to this revision**. We do not imply both are new.

**8. Cross-setting interpretation corrected.** M1-level benchmarks are not comparable across settings; all cross-setting statements are confined to the matched estimand. The earlier "Colombia positive / Sri Lanka null" reading does not hold — both show a small, consistently-signed increment. We now state the magnitudes are **not** equal (under recalibration Sri Lanka ~+0.015 is about twice Colombia's +0.0078); the finding is consistent in **sign, not magnitude**.

**9. Past-only recalibration added.** Reported alongside the optimistic cross-fit, with the cross-fit explicitly flagged as non-deployable.

**10. Uncertainty limits.** Intervals are conditional cluster-bootstrap (frozen predictions), omitting model-development uncertainty; 26-RDHS finite-cluster caution stated; Colombia development-inclusive interval (includes zero) shown.

**11. Threshold sensitivity.** The matched increment is positive at all thresholds p*∈{0.10–0.50}; the reference-threshold raw interval still includes zero (no significance manufactured).

This is a correction of **description and estimand interpretation**, not of the underlying fitted models, and not fabrication or data manipulation. Section-by-section edits are in `manuscript_final.diff`.
