# Dengue Manuscript — Final Publication Verdict (post C2-CONFIRMED finalization)

*Consolidated finalization of `paper1_plos_gph_C2_final.tex` (40 pp; compiles exit 0, 0 undefined references, 0 errors). Nothing committed or pushed; HEAD `05f235e`; v13 and v14 sources preserved.*

---

## Final verdict: **NOT READY — MAJOR REVISIONS REMAIN**

…but the remaining work is **author-owned and administrative, not scientific.** The scientific content — estimand definitions, numbers, provenance, and interpretation — is resolved and reviewer-resistant. Submission is blocked only by declarations and reproducibility artifacts that **you** must supply (§8), plus a coauthor attestation (§5). Once those are in, the science does not require further revision.

If the journal's declaration blockers were already satisfied, this manuscript would be **READY WITH MINOR AUTHOR CHECKS**.

---

## 1. What changed in this finalization

**The substantive scientific fix (Phase 4 estimand correction).** The prior draft repeatedly called Sri Lanka **M5 − M1** "the matched climate increment." That is wrong: the frozen M1 was fit under different penalization/standardization (near-unpenalized C=1e6, AR-only standardization) than M5, so M5 − M1 conflates climate with fitting differences. Corrected at four Sri Lanka loci (results, recalibration, and two discussion passages) plus the abstract:
- The **only** specification-matched climate estimand is now consistently **M5 − M5_no-climate** (+0.0087).
- **M5 − M1** (+0.0081) is labeled the *frozen-pipeline, non-matched* contrast, with the §D.3 reconciliation of the ≈0.0006 gap.
- Inserted the approved §D.1 "Estimand hierarchy" methods block verbatim; added the Sri Lanka matched row to the analysis-status table.

**Recalibration attribution fix.** The past-only recalibration value (+0.015, CI excludes zero) is now correctly attributed to the frozen **M5 − M1** contrast, not to the matched estimand — so the only zero-excluding result is explicitly recalibration-dependent *and* specific to a non-matched contrast.

**Magnitude honesty (Phase 3b).** All "same/similar/comparable magnitude" wording removed; replaced with "consistently-signed … of uncertain, setting-varying magnitude" (Sri Lanka ~+0.015 under recalibration ≈ 2× Colombia +0.0078).

**Post-hoc disclosure.** M5 − M5_no-climate is designated primary **and** flagged post hoc/exploratory in both settings; "prespecified/design-locked" now applies only to the model ladder and the structured Sri Lanka M1, never to the matched estimand.

---

## 2. Primary scientific result

A small, **consistently-signed** matched climate increment appears in **both** settings, of **uncertain, setting-varying magnitude**, not robustly distinguishable from zero:

| Setting | ΔNB(M5 − M5_no-climate) @ p*=0.30 | 95% CI | Note |
|---|---|---|---|
| Sri Lanka | **+0.0087** | [−0.0015, +0.0188] | includes zero (raw) |
| Colombia | **+0.0078** | [+0.0039, +0.0119] | conditional interval; **development-inclusive interval includes zero** |

- Sri Lanka non-climate structure contributes far more than climate: matched − cases = **+0.0462** [+0.0199, +0.0741].
- Prespecified secondary **M4 − M1** (non-nested): raw −0.008 → recalibrated +0.010, CI [−0.011, +0.030] (includes zero).
- **Threshold consistency (recomputed from the validated reconstruction):** the matched increment is **positive at every** p*∈{0.10, 0.20, 0.30, 0.40, 0.50}; CI excludes zero at p*∈{0.20, 0.40, 0.50}. Consistent in **sign**; magnitude/precision vary with threshold.

Interpretation: predictive / decision-analytic, **not causal**, **not transportable**, **not** proof of operational utility.

---

## 3. What is no longer claimed

- ❌ "Sri Lanka M5 − M1 is the matched climate increment" → now the frozen, **non-matched** contrast.
- ❌ "Colombia positive, Sri Lanka null" → both show a small, consistently-signed increment.
- ❌ "same / similar / comparable magnitude across settings" → sign consistent, magnitude not equal.
- ❌ pre-specification of the interpretable estimand → the matched contrast is **post hoc**.
- ❌ M4 − M1 as "structurally confounded" → "non-nested, structurally mismatched; does not isolate climate."

---

## 4. Provenance status

**CONFIRMED to a high, non-cryptographic standard.** The design-lock spec commit `1d8e268` (2026-06-14 13:24) is a DAG ancestor of the results report `02f986e` (14:33) on `main`; the M1-defining line was never edited; filesystem mtimes corroborate spec-before-results (13:15 < 13:32); the report hash-pins the spec. **Qualification (disclosed in the paper):** the frozen prediction CSVs are git-untracked, so the ordering rests on timestamps + an author-produced report + attestation — strong evidence of no fabrication, **not** tamper-proof. Reproduction of frozen predictions: ≤1.1×10⁻¹⁶ over all 3,926 rows (re-confirmed this session by `threshold_sweep.py`).

---

## 5. Author attestation (required, not optional)

The provenance/pre-specification *framing* depends on the coauthors confirming the Sri Lanka M1 was structured **and fixed before the frozen results**. Sign-off sheet + verbatim cover-letter text: `analysis/v15_final/COAUTHOR_SIGNOFF.md`.

---

## 6. Reference audit

Clean: **45 bibitem entries, 45 cited keys, perfect 1:1 mapping** — 0 orphan citations, 0 uncited entries, 0 duplicate keys. Only cosmetic issues (three "single-author + et al." entries vs the stated six-author convention; two key-year vs printed-year mismatches — `Leung2022`, `OpenDengue2024`; one missing terminal period; PLoS/PLOS casing). DOI resolution and full bibliographic correctness are `NEEDS-EXTERNAL-CHECK` (no web access). Full report: `analysis/v15_final/reference_audit.{md,csv}`.

---

## 7. Remaining weaknesses (harsh, specific)

1. **The only zero-excluding result is doubly qualified** — it requires recalibration *and* is the non-matched M5 − M1 contrast; the matched estimand's reference-threshold raw interval includes zero. The headline rests on sign-consistency, not established magnitude.
2. **Primary estimand is post hoc** while the prespecified contrast (M4 − M1) is demoted — defensible and disclosed, but a reviewer may still read it as reframing toward a favorable estimand. The post-hoc disclosure is explicit and must stay.
3. **Provenance is not tamper-proof** (untracked frozen artifacts) — mitigated only by attestation until the checksummed archive exists (§8).
4. **Colombia selection** toward high-incidence, better-reporting municipalities; bounded by an IPW sensitivity but not eliminated.
5. **26 RDHS clusters / conditional bootstrap** — intervals omit model-development uncertainty; finite-cluster coverage caution stands.

**Independent harsh-review agent: same verdict — NOT READY — MAJOR REVISIONS REMAIN** (no scientific-validity failure). Its sharpest additional points, worth heeding before submission:
- The **"consistently-signed increment" headline is partly an artifact of which uncertainty is foregrounded**: no matched, development-robust, zero-excluding climate result exists in *either* setting (Colombia's development-inclusive interval [−0.0001, +0.0244] includes zero; Sri Lanka's matched raw CI includes zero; the only zero-excluding number, SL frozen M5−M1 +0.015, is both non-matched and recalibration-dependent — the very contrast the paper's own methods disqualify). Consider softening any directional tone in the **title/abstract** to match a zero-including post-hoc diagnostic.
- The **frozen primary hybrids were never calibrated** (compared raw-vs-raw), yet the paper's thesis is calibration-centric, and the primary M4−M1 sign flips once recalibrated — foreground this tension rather than letting a reviewer find it.
- Presentation: **Fig 2 (SL) is four points joined by lines** (not a dense decision curve); the numeric density obscures a single locatable headline number; p*=0.30 is un-costed. These are presentation-level, not validity, issues.

**Manuscript claim-ledger: complete and clean.** 97 claims audited — **82 verified, 15 verified-with-qualification, 0 unsupported / inconsistent / outdated.** All six authoritative estimands match the frozen JSON exactly, and internal ratios (prevalences, rescalings, decomposition sums) reconcile. The 15 qualified items are all author-owned placeholders the manuscript itself flags as pending (declarations, OpenDengue ID, abbreviated reference author lists, the cosmetic `Leung2022` key/year mismatch) — none touch a reported estimand. The ledger's one wording flag (a lone "similar small increment" in the conclusion) has been **fixed** → "small increment of the same sign … of uncertain and setting-varying magnitude." No "same/similar/comparable magnitude" phrasing now remains (grep = 0). Files: `analysis/v15_final/manuscript_claim_ledger.{md,csv}`.

---

## 8. PLOS GPH compliance — Author-action-required (submission-blocking)

**10 resolved · 13 author-action · 6 external-confirmation.** The blocking items are all author-owned placeholders in the Declarations block:

1. Data Availability Statement (placeholder)
2. Code availability (repository/PID/license)
3. Ethics statement ("determination pending")
4. Funding ("pending")
5. Competing interests ("pending")
6. Author contributions / CRediT ("pending")
7. **OpenDengue v1.3 version-specific record ID + acquisition date**
8. **Pinned/reproducible Python environment** for the primary M0–M5 models

Plus: trim abstract (~500 → journal limit ~300 words); add corresponding-author ORCID; add S# in-text citations for S1/S2/S3/S4/S7/S8/S10/S13/S14; acknowledgments. **Recommended:** archive the frozen predictions + `source_checksums` to Zenodo/OSF — this simultaneously hardens provenance (removes the untracked-artifact caveat) and satisfies items 1–2. Full checklist: `analysis/v15_final/PLOS_GPH_compliance_checklist.md`.

---

## 9. Files created (`analysis/v15_final/`)

`FINAL_MANIFEST.md` · `primary_estimand_final_check.md` (PASS) · `final_model_specification_table.md` · `final_threshold_consistency_check.{md,csv}` · `threshold_sweep.py` · `recalibration_and_uncertainty_language_audit.md` · `reviewer_response_final.md` · `COAUTHOR_SIGNOFF.md` · `reference_audit.{md,csv}` · `PLOS_GPH_compliance_checklist.md` · `manuscript_final.diff` · `compile_log.txt` · (pending) `manuscript_claim_ledger.{md,csv}`, `harsh_peer_review_final.md`. Manuscript: `manuscript/paper1_validity_corrected_candidate/paper1_plos_gph_C2_final.tex`/`.pdf`. Delivered to `~/Downloads/`: `paper1_plos_gph_C2_final.tex`/`.pdf`, this verdict.

---

## 10. Git status

No commit, no push. HEAD unchanged at `05f235e`. v13 (`paper1_plos_gph.tex`) and v14 (`paper1_plos_gph_v14.tex`) preserved untouched; all edits in the new `paper1_plos_gph_C2_final.tex`.

---

## 11. Recommended author action (exact next step)

1. **Circulate `COAUTHOR_SIGNOFF.md`** to Shiwakoti/Khadka/Thapa and obtain the attestation (closes the provenance framing).
2. **Fill the 8 blocking declarations** (§8 items 1–8), especially the OpenDengue v1.3 record ID + date and a pinned Python environment.
3. **Archive frozen predictions + checksums to Zenodo/OSF**, mint the DOI, and drop it into the Data/Code Availability statements.
4. Trim the abstract to the GPH limit and add the S# in-text citations + ORCID.

After 1–4 the manuscript is submission-ready; the science needs no further revision.
