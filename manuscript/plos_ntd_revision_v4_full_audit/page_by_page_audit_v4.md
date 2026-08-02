# Page-by-page audit — v4 (source: ~/Downloads/Dengue (2).pdf, 21 pp; corrections in v4)

Rendered before (`/tmp/dengue_v4_before`) and after (`/tmp/dengue_v4_after`) at 150–200 dpi. All numeric corrections transcribed from frozen reports via `v4_verified_evidence_ledger.md` (no recomputation).

| Page/region | Problem found | Correction | Evidence |
|---|---|---|---|
| 1 — title | "Administrative metadata pending — not for submission" as title-page content | moved to a running footer "INTERNAL REVIEW — ADMINISTRATIVE METADATA PENDING"; details → `submission_blockers_v4.md` | — |
| 1 — Abstract | informal "weak baselines", "hard to beat"; "or, equivalently … 4.4"; CI-overlap reliance | "less demanding comparators"; "the recent-surveillance benchmark outperformed…"; §3 translation phrasing; "No cross-country … heterogeneity test was performed; therefore, the study does not establish a difference" | model-ladder/E3 reports |
| 2 — Author Summary | "may be setting-dependent" invites heterogeneity reading | "The study did not formally test whether the hybrid estimates differed between settings, so each result needs local interpretation"; 200 words | — |
| 2–3 — Introduction | self-characterizing "honest"; CI-overlap | "comparative operational evaluation"; no CI-overlap-as-test | — |
| 4 — checklist contradiction | "provided as Supporting Information" vs SI drafts | "draft … prepared for author completion and are not yet submission-ready"; TRIPOD+AI/PROBAST framed as internal aids | `supporting_information_status_v4.md` |
| 4–7 — Methods | software line cites R for Python; R year 2024 vs R 4.6.0; recalibration leakage wording | Python fit logistic models, R 4.6.0 + `dlnm` comparator; R citation → 2026; leakage-safe wording retained (verified s≤t−5) | recalibration report; evidence Q4,Q6 |
| 4–7 — model defs | Colombia M4 "without full fixed effects" (it has none); humidity | M4 = recent cases + linear precip/temp lags, no seasonality, no FE; humidity not used in Colombia | `colombia_model_ladder_h4_75pct_v1.py` |
| 7 — fallbacks | (verified) | "No recalibration fallbacks occurred" | recalibration report §5 |
| 8 — Figure 1 | diagonal arrow crossed the "Key correction" annotation | removed the floating annotation node (info moved to a concise caption); category labels in boxes = redundant grayscale encoding | — |
| 9 — Table 1 | abbreviations undefined | defined AUC, PR-AUC, Brier, CITL, Slope, Mean pred.=mean predicted probability, Obs.=observed prevalence, NB₀.₃₀, FE=fixed effects; "M1 highest among M0–M3" scoped to the initial comparison | pilot report |
| 10 — orphan | single-word "workflow." stranded | shortened "in the evaluated rolling-recalibration workflow" → "occurred." (reflow) | — |
| 10 — Figure 2 | titled "decision-curve analysis" but only 4 thresholds; SI-grid claim | plot retitled "net benefit at representative thresholds"; caption states points are 4 reported thresholds, not a recomputed curve; removed unverified "full grid in SI" claim | decision-threshold report |
| 10–11 — §3.4 | two contrast orientations merged | separated: Python≈R-DLNM (CIs span zero) vs both < M1; R-DLNM−M1 ΔAUC −0.038 [−0.066,−0.008], ΔNB −0.025 [−0.041,−0.006] favoring M1 | canonical_R_dlnm/hybrid reports |
| 11 — Table 4 (DLNM/hybrid) | M5 present, M4 absent; thresholds | M4's per-threshold NB at 0.20/0.40 not in frozen comparison; table retained as a selected comparison (M4 AUC 0.764/NB 0.128 summarized in text) | hybrid report |
| 11–12 — Colombia | repetition; "dept. FE"; M4 vague | consolidated; "department fixed effects"; M4 exact description | model-ladder report/script |
| 11–12 — Colombia calibration (§17) | only "predictions exceeded prevalence" | added per-model CITL (all negative/over-prediction), Brier 0.213–0.250, slopes 0.85–3.43, Platt recal on validation; noted per-model obs-prev/mean-pred not retained | model-ladder report |
| 12 — Figure 3 | omitted M0; "0.69/0.7/0.73" precision; AUC only while caption discussed NB | **two-panel figure (A AUC, B NB) for M0–M5, 3-decimal labels, alert-all ≈0.107 line, hatch patterns for grayscale** | model-ladder report (frozen values) |
| 13 — sensitivity | full 1.9/4.4 translation repeated; "lower limit near zero" | de-duplicated (pointer to primary Results); exact 80th/90th CIs added (+0.0157 [0.0082,0.0236]; +0.0092 [0.0003,0.0183]); pointwise/multiplicity-unadjusted | E3 report |
| 13–14 — cross-setting | "intervals overlap" as evidence | replaced everywhere with "no heterogeneity test … does not establish a difference" | — |
| 14–16 — Discussion | "principal lesson is methodological"; "Climate-only weakness"; "operational meaning … small"; "two-country panel is imbalanced" | "principal evaluation lesson"; "the limited decision value of the climate-only models"; "the magnitude … was modest"; precise design-difference limitation | — |
| 16 — Declarations | placeholders | neutral "Pending author confirmation"; AI disclosure substance intact | `submission_blockers_v4.md` |
| 16–20 — References | R year/cites-Python; OpenDengue dataset year | fixed (see `reference_integrity_report_v4.md`); 0 `[?]`, populated | evidence Q6–Q7 |
| 20–21 — SI | drafts described accurately; order after References | `supporting_information_status_v4.md` | — |
| whole doc | line numbers absent (PLOS requires) | continuous line numbers restored; American English; black links | evidence (PLOS pages) |

---

## Review-pass addendum (2026-06-28) — eleven-perspective harsh review applied

Verdict from the 11-reviewer panel (epi, stats, DCA, calibration, reporting, bibliography, PLOS structure, writing, layout, provenance, metadata): **MINOR REVISION** — BLOCKING-SCIENCE **empty**, NEEDS-NEW-COMPUTATION **empty**, hard-stops **9 PASS / 1 CONDITIONAL PASS (OpenDengue V1.3 DOI) / 0 FAIL**. The following writing/layout edits were applied (all transcription or deterministic arithmetic from frozen reports; no recomputation; two reviewer-supplied numbers were re-verified and corrected before use):

| Tag | Edit | Evidence / note |
|---|---|---|
| W1 | §2.6 "Python distributed-lag nonlinear cross-basis" → "Python DLNM-style cross-basis approximation" (consistency with §3.4/§3.8) | `dlnm_climate_comparator_report.md` |
| W2 | Methods: distinguished Sri Lanka rolling time-updated recalibration from Colombia Platt-on-validation; "same logic" = framework, not identical procedure | colombia results |
| W3 | Abstract: split climate-only claim from the M5−M1 hybrid increment | — |
| W4 | Abstract: attributed horizon-flatness explicitly to Colombia | — |
| W5 | Results + Discussion: symmetric CI for the operational translation (TP-equiv 1.2–2.6; false-alert 2.7–6.1 per 100); noted both are monotone transforms of the same ΔNB CI | 1.2–2.6 = 100×[0.0117,0.0260] |
| W6 | Results: added Sri Lanka p\*=0.40 ΔNB CI **+0.0090 to +0.0399** (excludes zero; pointwise, secondary). Reviewer's quoted CI verified against `targeted_value...report.md` §4; the +0.0251 Colombia value was kept separate. | `targeted_value_climate_stage1a_h4_report.md:31` |
| W7 | Results: scoped 0.085 max NB as "recalibrated climate-only (M2/M3)" | recal report |
| W8 | Methods: M5−M1 labeled "primary reference contrast for the hybrid increment," distinct from confirmatory M1-vs-climate | — |
| W9 | Methods: surfaced B=1000 cluster bootstrap, 0 failures; disclosed unretained Sri Lanka targeted-value seed | S6 |
| W10 | Methods: OpenDengue coverage made level-explicit (release through 2023; Admin-2 tier through 2022) | — |
| W11 | Cross-setting table caption: must-not-compare-for-overlap clause | — |
| W12 | Figure 2 caption: explained 0.34 (alert-all zero-crossing, NB −0.005, near prevalence 0.336) | `pilot_h4_75pct_calibration_dca_report.md` §11 |
| W13 | DCA Methods: stated threshold odds / cost-loss exchange rate (~0.43 false per true alert at p\*=0.30) | 0.30/0.70 |
| W14 | Methods: fixed SIVIGILA comma splice (→ SIVIGILA/INS, and) | — |
| W16 | §3.9 M1 h=4 AUC 0.751 → 0.752 to match tables (raw 0.7515; display-only) | `label_horizon_robustness_report.md:10` |
| W18 | Colombia Table 5 caption: note that per-model mean-pred/observed prevalence omitted (not retained) | ledger item 1 |
| C1 | OpenDengue bib: added note that the record DOI resolves to V1.2; V1.3 version-specific DOI + access date are author-to-confirm (not asserted) | `reference_audit_v1.md:46` |
| L1 | Abstract trimmed for headroom (rendered ≈276 words ≤300) | — |
| G1 | Internal `v4_verified_evidence_ledger.md` item #3 corrected (4-decimal SL ΔNB **is** printed verbatim in `targeted_value...report.md` line 16); stale "v3"/"v1" titles in fidelity-check and crosswalk updated to v4 | review-flagged ledger error |

**Reviewer errors caught by verification (not propagated):** (a) the review quoted the Sri Lanka p\*=0.40 CI as `[+0.0090,+0.0399]` — this matched the frozen report and was used; but the adjacent claim conflated it with Colombia's `+0.0251` value, which was kept distinct; (b) the review recommended expanding `EWARScsd` with a five-author list that actually belongs to the **2021 scoping review** (a different paper) — the 2024 EWARS-csd full author list is **not** in the committed record, so it was **not** invented and remains an author-to-confirm item.

**Not applied (cosmetic / out of scope):** W15 (denominator provenance pointer — already correct in body; traceability noted in crosswalk), W17 (descriptor harmonization — no stray "dept" found; descriptors already consistent), W19 (optional NB-vs-bootstrap-mean footnote — load-bearing values unaffected), C2 full author expansions and all S-table/metadata items (author-to-confirm, tracked in `submission_blockers_v4.md`).

**Post-edit build:** 22 pp (grew by 1 from the additions; page 22 is the full Supporting Information page, not an orphan), 0 undefined citations/refs, 0 `[?]`, 0 LaTeX errors, max overfull 3.99 pt (Figure 1 tikz box, < 10 pt). Abstract 276 rendered words; Author Summary 200. Visual QC: pages 1, 10 (Fig 2), 13 (Fig 3) re-rendered and confirmed.
