# Analysis-Hierarchy Verification (latest) — M4/M5 and Colombia

**Audit type:** read-only evidence audit. No model, metric, bootstrap, calibration curve, DCA curve, or dataset was recomputed. No manuscript file was edited. Nothing was staged, committed, or pushed.
**Repository:** `/home/mpcrlab/srilanka-dengue-ews-calibration` · HEAD `a32afd7` == `origin/main` (clean; working tree has only untracked audit/manuscript files).
**Date of audit:** 2026-07-07.

---

## 0. Anchors (Audit §1)

**True latest manuscript revision:** `manuscript/plos_ntd_revision_v18_submission_clean_candidate/` — `dengue_ews_plos_ntd_v18.tex` (541 lines). Compiled PDFs present: `dengue_ews_v18_internal_author_completion.pdf`, `dengue_ews_v18_scientifically_clean_not_submission_ready.pdf`.
- Latest `.tex`: `dengue_ews_plos_ntd_v18.tex`.
- Latest bibliography: `references_v18.bib`.
- Latest Supporting Information: `supporting_information/S1…S12` (v18).
- Latest submission-gate file: `submission_metadata_gate_v18.md` (supersedes `internal_review_only/submission_blockers_v17.md`).
- Source revision it derives from: v17 (`plos_ntd_revision_v17_exact_wording_verification/`), pinned by `v17_state_at_v18_start.sha256` ("Recorded 2026-07-02T12:43:42Z before any v18 edits. v17 is NOT modified after this.").

**Provenance caveat (important):** the entire `manuscript/` tree is **untracked in git** (`git ls-files manuscript/` → 0 files). Only `docs/`, `scripts/`, `data/README`, etc. are committed (last commit 2026-06-26). Therefore:
- The **docs/ evidence base is genuinely git-dated** (commit timestamps are load-bearing).
- The **manuscript revisions are dated only by file mtime + internal sha256 pins + internal chronology docs**, not by git history. This is itself a reproducibility gap (the manuscript is not version-controlled/committed).

**Is the review's "v17" premise stale?** The review under audit (`docs/manuscript_peer_review_v1.md`, generated 2026-06-26) reviews an *earlier, 2-author (Shiwakoti & Khadka), 23-pp* manuscript — older than v17. The current manuscript is **v18** (3 authors incl. Thapa). The audit-prompt's own "manuscript is currently v17" premise is **stale**: v17 has been superseded by the v18 submission-clean candidate. Many of the review's demands were addressed in v16→v18 (see `multi_agent_review_response_matrix_latest.md`).

---

## 1. Model ladder M0–M5 (definitions)

Source: `manuscript/…/supporting_information/S5_country_model_specification_v18.md:8`; hybrid defs `docs/hybrid_model_extension_spec.md:17-19`.

| Model | Definition |
|---|---|
| M0 | Season only (seasonal harmonics) |
| M1 | Recent cases (autoregressive surveillance-only baseline) — the operational comparator |
| M2 | Climate only |
| M3 | Climate + season + RDHS fixed effects |
| M4 | Recent cases + climate (DLNM-style cross-basis) — **planned primary hybrid** (31 SL features) |
| M5 | M4 + seasonal harmonics + geographic fixed effects — **pre-computation expanded/steelman sensitivity hybrid** (60 SL features) |

---

## 2. Sri Lanka hybrid hierarchy (Audit §2)

All numbers verified first-hand and via cross-checked frozen sources; every figure below carries a `file:line` citation.

| Contrast | Estimate & 95% CI (p\*=0.30, h=4, 75th-pct, ALL-test) | Role claimed by the review/prompt | Role supported by dated evidence | Evidence predates computation? | Current manuscript (v18) wording correct? |
|---|---|---|---|---|---|
| **M4 − M1** (ΔNB) | **−0.008** [−0.028, +0.013]; precise −0.00826 [−0.0278, +0.01277] (`docs/hybrid_model_extension_report.md:32`; `hybrid_all_test_seed_evidence_v18.md:16`) | Prespecified **primary** SL hybrid | **Planned primary** — locked before computation (`docs/hybrid_model_extension_spec.md:12,18,31`) | **Yes** — design-lock spec committed `1d8e268` *before* results report `02f986e`, both 2026-06-14; spec states "before any computation" (`:4`) | **Correct.** v18 L103/L164/L299/L303 label M4 "planned primary hybrid"; reports −0.008 [−0.028, +0.013] |
| **M5 − M1** (ΔNB) | **+0.0081** [−0.0012, +0.0181]; precise +0.00808 [−0.00135, +0.01845] (`docs/targeted_value_climate_stage1a_h4_report.md:16`; `S8_srilanka_targeted_value_v18.md:6`) | Sensitivity / expanded-hybrid | **Pre-computation expanded-hybrid sensitivity** (`docs/hybrid_model_extension_spec.md:19,31`; `S4_analysis_plan_chronology_v18.md:8`) | **Yes** — specified in the same 2026-06-14 lock, before computation, "reported as a sensitivity, not the primary" | **Correct.** v18 L103/L164/L299 label M5 "expanded sensitivity hybrid"; CI includes 0 |

**Verification of the review/prompt's specific number:** ΔNB(M5−M1) = **+0.0081, 95% CI −0.0012 to +0.0181** is **VERIFIED** (four concordant sources agree to rounding: `hybrid_model_extension_report.md:34`; `targeted_value_climate_stage1a_h4_report.md:16`; `S8_srilanka_targeted_value_v18.md:6`; `hybrid_all_test_seed_evidence_v18.md:17`). Bootstrap: RDHS-cluster, **seed 20260612, B=1000, 0 failures** (`hybrid_all_test_seed_evidence_v18.md:14,21`).

**Was M4 truly the planned primary, before results?** Yes, on dated internal evidence:
- `docs/hybrid_model_extension_spec.md:4` — "specification only — locks models, evaluation, and strict winning criteria **before any computation**," dated 2026-06-14, sha256-pinned.
- `:18` "M4 — hybrid (primary new model)"; `:31` "M4 is the locked primary regardless of which scores higher"; `:14` win declared only if the ΔNB(M4−M1) cluster-bootstrap CI excludes 0.
- git commit **order** corroborates temporal separation *within* 2026-06-14: spec `1d8e268` committed before results `02f986e`.

**When was M5 introduced / was it prespecified?** M5 was in the **same 2026-06-14 lock**, explicitly as a "steelman sensitivity … reported as a sensitivity, not the primary" (`hybrid_model_extension_spec.md:19,31`). It is **not** post-hoc; it is a pre-computation *sensitivity*, subordinate to the M4−M1 estimand (`S4_analysis_plan_chronology_v18.md:8,10`).

**Registration status:** **Internal design-lock only; no public registration.** `S4_analysis_plan_chronology_v18.md:15` — "No prospective public registration is claimed." The `docs/osf_prereg_skeleton.md` (2026-06-10) is an unexecuted *intention* ("to be frozen on OSF before exposure data are linked"), with no OSF ID, DOI, or filing timestamp anywhere. The 2026-06-11 `preregistration_analysis_plan_v1.md` is an internal document ("Public data-release decision deferred," `:89`).

**Does dated evidence support "M4 = planned primary, M5 = expanded sensitivity"?** **Yes.** No dated document ever treats M5−M1 as the primary confirmatory contrast; the primary confirmatory contrast is consistently ΔNB(M4−M1) at p\*=0.30, h=4. **The review under audit (`manuscript_peer_review_v1.md`) predates and is unaware of this M4-primary lock** — it called "per-setting ΔNB(M5−M1)@0.30 … the single confirmatory contrast" (`manuscript_peer_review_v1.md:84`). That characterization is **superseded** by the current manuscript, which correctly designates M4−M1 as primary and M5−M1 as secondary. The audit-prompt's summary (M4 primary / M5 sensitivity) matches the **current manuscript**, not the older review.

**Honest caveat to flag to the author (not a defect, a communication risk):** although provenance is clean, the *operationally interesting* SL signal rests on the **M5−M1** contrast, which reaches a CI excluding 0 only at **p\*=0.40** and in an **8-cluster, high-incidence×strong-autocorrelation regime (+0.0202)** — not at the registered p\*=0.30 (`targeted_value_climate_stage1a_h4_report.md:16-24`). v18 handles this correctly by labeling every M5-based result secondary/exploratory and imprecise (`S8_…v18.md:10`).

---

## 3. Colombia hierarchy (Audit §3)

**Primary Colombia replication = full 2020–2022 test period** (never a pandemic-excluded subset). `dengue_ews_plos_ntd_v18.tex:414` — "the Colombia 2020–2022 analysis remains the primary replication, and neither sensitivity was treated as a primary analysis."

| Quantity | Full-period (2020–2022) | 2022-only subset (secondary) |
|---|---|---|
| Test years | 2020-01-01 → 2022-12-25 (`colombia_model_ladder_spec.md:30`) | 2022 only; **48** eligible prediction-origin weeks, Jan 2–Nov 27 2022 (`S9…v18.md:25`; `colombia_2022_week_eligibility_v18.md:14`) |
| Eligible obs | **13,361** municipality-weeks (475 GID_2 units) (`colombia_model_ladder_report.md:21`) | **4,802** municipality-weeks, 274 municipalities, 2,202 events (`S9…v18.md:27`) |
| Prevalence | **0.375** (`colombia_model_ladder_report.md:21`) | **0.4586** (`S9…v18.md:27`) |
| Alert-all NB @0.30 | (positive; full-period baseline) | **0.2265** (alert-none 0) (`S9…v18.md:27`) |
| **ΔNB(M4−M1)@0.30** | **+0.0122** [+0.0073, +0.0171] (`colombia_outbreak_threshold_sensitivity_report.md:48`) | **+0.0097** [+0.0048, +0.0150] (`S9…v18.md:44`) |
| **ΔNB(M5−M1)@0.30** | **+0.0188** [+0.0117, +0.0260] (`…report.md:48`; `.tex:322`) | **+0.0150** [+0.0067, +0.0249] (`S9…v18.md:43`; `.tex:387`) |
| ΔAUC(M5−M1) | **+0.040** [+0.024, +0.058] (precise +0.0403 [+0.0235,+0.0575]) (`.tex:322`) | +0.0546 [+0.0336, +0.0768] (`S9…v18.md:42`) |

**Verification of the review/prompt's number:** ΔNB(M5−M1)@0.30 full-period = **+0.0188 [+0.0117, +0.0260], ΔAUC +0.040** — **VERIFIED** (`colombia_outbreak_threshold_sensitivity_report.md:48`; `.tex:322`; `S9…v18.md:8`).

**Was the 2022-only analysis prespecified, documented later, or post-hoc?** **Post-hoc secondary sensitivity, created after the analysis freeze.** Dated evidence:
- Uses **seed 20260630** (`S9…v18.md:26`), i.e. generated ≈ 2026-06-30 — **after** the 2026-06-19 E3 report that closed the analysis phase (`colombia_outbreak_threshold_sensitivity_report.md:92` — "E3 closes the analysis phase … Next step is manuscript preparation").
- Classified in `S4_analysis_plan_chronology_v18.md:14` as one of "the two secondary v2 sensitivities (Colombia 2022-only; Sri Lanka wild-cluster-bootstrap-t)" — a documented extension, **not** in the prespecified core (`:13`).
- Absent from every pre-June-30 plan (model-ladder spec, cross-country memo roadmap, E3 freeze list).
- The word "post-hoc" is not used in-repo, but the dated record establishes it was created after the fact.

**Was pandemic-period exclusion ever designated primary?** **No — nowhere** (`.tex:414,418,387`; `S9…v18.md:22-23`; `colombia_model_ladder_spec.md:15-16`).

**Consequences if the 2022-only result were promoted to primary (Audit §3):** it would be (a) **post-hoc selection** (seed-dated after freeze); (b) a **smaller temporal sample** (48 origins vs full period); (c) at a **different prevalence** (0.4586 vs 0.375); (d) against a **different, far more competitive alert-all benchmark** (0.2265), so absolute NB levels are not comparable; (e) **less comparable** with the full-period estimate. The manuscript's own wording is correct: the 2022-only estimate "should not be read as post-pandemic validation" and is "not … a lower bound" (`.tex:387,418`). **Recommendation: keep 2022-only as a secondary sensitivity.**

**Horizon behavior (1–12 wk):** ΔNB(M5−M1) is **approximately flat** (h1 +0.015 / h2 +0.017 / h4 +0.019 / h8 +0.019 / h12 +0.014), and ΔAUC **declines** (+0.040 at h≤4 → +0.024 at h=12) (`colombia_horizon_sensitivity_report.md:67-71,88`). The "climate helps more at longer lead" expectation is **not supported**.

**Full-period COVID interpretation:** the 2020–2022 window is COVID-era; all models over-predict (CITL ≈ −0.5) (`.tex:322`; `colombia_model_ladder_report.md:49`). The manuscript relies on the **within-test ΔNB contrast under identical recalibration** as the robust quantity, and treats the pandemic as an absolute-calibration caveat, not a reason to switch the primary period (`cross_country_interpretation_memo.md:35`).

**Cross-setting asymmetry to note (consistency, not error):** Sri Lanka's *planned primary* hybrid is M4−M1, but the Colombia narrative foregrounds M5−M1 (M4−M1 relegated to S9). This is defensible because **both** Colombia contrasts exclude zero (M4−M1 +0.0122 [+0.0073, +0.0171]; M5−M1 +0.0188 [+0.0117, +0.0260]) — the Colombia positive is not an artifact of choosing M5 — but the manuscript could state the Colombia M4−M1 value in-text for symmetry with the SL primary estimand.

---

## Confirmation

- No model, metric, bootstrap, calibration curve, DCA curve, or dataset was recomputed; all numbers are transcribed from frozen committed/pinned records with `file:line` citations.
- No manuscript revision was modified. Nothing was staged, committed, or pushed.
