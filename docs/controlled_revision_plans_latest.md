# Controlled Revision Plans (latest) — Audit §6, §7, §9, §10, §11

Read-only. **No new computation was authorized or performed. No manuscript edits; nothing staged/committed.** All feasibility statements rest on the repository's saved artifacts (per-row predictions live in `~/data_quarantine/`, gitignored — *not* in the repo).

---

## A. Proposed-analysis audit (§6)

For each proposed analysis: question answered · data/predictions exist? · changes the estimand? · prespecified? · computation required · scope-expansion risk · likely reviewer value · recommendation.

| Analysis | Question | Saved preds/data present? | Changes estimand? | Prespecified? | Computation | Scope risk | Reviewer value | Recommendation |
|---|---|---|---|---|---|---|---|---|
| Rolling-origin validation | Is the single-split ranking stable across origins? | No (quarantine only) — needs **model refit** at each origin | No (same estimand, more folds) | No | High (refit M0–M3/M1 per origin) | Medium | **High** — answers the "single holdout" criticism | **Plan B candidate #1** if a reviewer insists; else disclose single-split limitation |
| Spatial-block validation | Spatial generalization | No — **refit**, not implemented (`probast…:26`) | Partial | No | High | Medium | Medium (temporal is the more relevant threat) | Optional; lower priority than rolling-origin |
| Rolling-origin + spatial-block combined | Both at once | No — refit | Partial | No | Very high | High | Medium | Not recommended for Paper 1 (scope) |
| Flexible (loess) calibration curves | Local mis-calibration near p\*=0.30 | Per-row preds in quarantine → **no refit** to plot | No | No | Low (re-plot saved preds) | Low | High (directly answers §3.8) | **Plan B candidate #2** — cheapest high-value add |
| Harmonized climate features | Same features both settings | No — rebuild from quarantined/raw climate | Yes (new comparison) | No | High | High | Medium | **Study-level extension**, not a Paper 1 fix |
| Harmonized recalibration | Same recalibration both settings | Partial | Partial | No | Medium | Low–Medium | Low | One disclosing sentence suffices |
| Formal setting×model interaction | Do settings differ? | Fittable on saved preds (no refit) | **Yes** — new cross-country estimand | No | Medium | Medium | Medium | Only with a **defensible common estimand**; otherwise keep "no test performed" |
| 2022-only Colombia → primary | Pandemic-free effect | Exists (secondary) | Yes (redefines primary) | No (post-hoc, seed 20260630) | None | High | Low | **Keep secondary** — promotion = post-hoc redefinition (see hierarchy doc §3) |
| Dense threshold-grid DCA | NB across a fine grid | Point NB computed; recompute CIs from stored preds, **no refit** | No | No | Low | Low | Low–Medium | Optional presentational upgrade |
| Weighted AUNBC | Threshold-integrated NB summary | Integrable from stored preds | **Yes** — new estimand needing threshold weights | No | Low–Medium | Low | Medium | Optional sensitivity only, with **pre-stated weights** (Talluri & Shete 2016 = *weighted*) |
| Standardized net benefit | NB/prevalence, comparability | Arithmetic from existing numbers | No | No | Trivial | None | Medium | **Do it** (writing fix; also SL per-100 translation) |
| Stakeholder-derived threshold range | Operationally grounded p\* | No (no elicitation done) | No | None (report a range) | Low | Low | Medium | Report a range + implied cost ratios; full elicitation = future |
| 3–6-month horizons | Seasonal lead value | Not run (1–12 wk only) | Yes | No | High | Medium | **Paper 2** |
| Reporting-delay simulation | Real-time performance | Not run | Yes | No | High | High | **Paper 2** |
| Nowcasting | Backfill-aware alerting | Not run | Yes | No | Very high | Very high | **Paper 2** |

**Guardrails honored:** reporting-delay & nowcasting → Paper 2; harmonizing both countries → study extension; a heterogeneity test requires a defensible common estimand; AUNBC is a new estimand needing justified weights; 2022-only stays a sensitivity absent dated evidence otherwise; **no new computation authorized here.**

---

## B. Questionable methodological statements (§7)

1. **"MAUP attenuation makes the result conservative."** Not accepted automatically. Spatial aggregation (the modifiable areal unit problem) can **attenuate, amplify, or reverse** associations depending on spatial covariance, exposure heterogeneity, measurement error, and population distribution. **Recommend cautious language only** (e.g., "aggregation may bias associations in an unknown direction") + an optional within-RDHS change-of-support check; do **not** claim a conservative direction.
2. **"Continuous decision curves are definitionally required."** Distinguish: (a) computing NB across a grid — already done; (b) displaying selected thresholds — current figure; (c) visually connecting selected points — presentational; (d) computing a new dense grid — a re-plot from stored predictions, **no refit**. The current figure is transparent; a denser display is **presentational**, not definitionally required.
3. **"AUNBC is a proper crossing-robust test."** Threshold weighting is **not** prespecified here; the measure is **not** established for this exact design; it **changes the primary estimand**; added public-health interpretability is marginal. Talluri & Shete (2016) propose the **weighted** AUNBC (weights **required**). Treat as an optional sensitivity with pre-stated weights, not a confirmatory test.
4. **"Python versions must be recovered by rerunning."** Do **not** treat a freshly rerun environment as proof of the historical one. Repository search found: **no committed environment/requirements/lockfile**; **R stack recorded** (R 4.6.0 / dlnm 2.4.10 / mgcv 1.9.4 / tsModel 0.6-2, sessionInfo in quarantine); **primary Python modeling-stack versions not preserved** (only Python 3.10 inferable from `scripts/__pycache__/*.cpython-310.pyc`); the two secondary bootstrap sensitivities are pinned (Python 3.10.12 + wildboottest 0.3.2 etc., in the sensitivity workspace, not committed). **Recommend transparent disclosure** of exactly what is preserved vs not — not reconstruction-as-truth.
5. **"2022-only should become primary."** Assess as a **potential post-hoc redefinition**, not a correction: seed 20260630 postdates the 2026-06-19 analysis freeze; smaller sample (48 origins); different prevalence (0.4586 vs 0.375); different alert-all benchmark (0.2265). **Keep secondary.**

---

## C. Practitioner "so what" (§9) — supported implications only

Using only existing evidence, the defensible practical implications are:
- **Benchmark any climate-informed system against recent surveillance** (M1), not against climatology or alert-all.
- **Evaluate probability calibration**, not just discrimination/AUC.
- **Monitor temporal calibration drift** (e.g., the Colombia test-period over-prediction, CITL ≈ −0.5) and recalibrate on recent data.
- **Use decision thresholds tied to operational trade-offs**, and report NB across a threshold range rather than a single point.
- **Audit reporting-date ↔ climate-calendar alignment** (WER-issue → ISO-week), a real and often-ignored error source.
- **Interpret climate as a possible local *supplement* to recent surveillance**, not an assumed replacement.
- **Evaluate locally** — increments varied in magnitude and precision across settings, and no cross-setting difference was tested.

**Not inferable (do not state):** cases prevented, lives saved, costs saved, operational readiness, performance under delayed/real-time reporting, or stakeholder acceptance.

### Proposed "Implications for dengue programs" box (DRAFT — NOT inserted)
> *Before adopting a climate-informed dengue alerting model, benchmark it against a recent-case surveillance baseline and judge it by calibration and decision-curve net benefit at operationally relevant thresholds — not by discrimination against climatology. Re-check calibration on recent data and watch for drift. Verify that surveillance-report dates and climate calendars are aligned. In these two retrospective evaluations, recent surveillance was a strong benchmark and climate added at most a modest, locally variable increment; treat climate as a candidate local supplement, to be re-evaluated in each setting, not a drop-in replacement. These are decision-analytic evaluations on finalized data, not estimates of outbreaks detected, cases prevented, or deployment readiness.*

---

## D. Submission blockers (§10)

Authoritative gate: `submission_metadata_gate_v18.md` — **GATE FAILED** (VERIFIED 1 · PARTIAL 4 · OPEN 15). **All OPEN items are administrative or reproducibility; no scientific or formatting blockers** (manuscript is "scientifically clean"; PLOS format-free initial submission).

| Item | Class | Status |
|---|---|---|
| Ethics determination | administrative | **OPEN** — pending FAU determination; do **not** self-certify |
| Funding | administrative | OPEN |
| Competing interests | administrative | OPEN — do not assume "none" |
| CRediT roles | administrative | OPEN |
| Acknowledgments | administrative | OPEN |
| Author order & approval | administrative | order documented; **approval OPEN** |
| Author emails | administrative | corresponding VERIFIED; coauthors OPEN |
| ORCIDs | administrative | OPEN — register real iDs |
| Public repository URL | reproducibility | OPEN |
| License (code + derived data) | reproducibility | OPEN (repo `LICENSE` present, type unconfirmed) |
| Archival DOI (Zenodo) | reproducibility | OPEN — plan only, no DOI reserved |
| OpenDengue version ID | reproducibility | PARTIAL — V1.3 verified locally; version-specific DOI pending |
| OpenDengue access date | reproducibility | OPEN — not preserved |
| AI-disclosure approval | administrative | PARTIAL — text drafted; all-author approval OPEN |
| STROBE (S1) | reproducibility | OPEN — DRAFT |
| TRIPOD+AI (S2) | reproducibility | OPEN — DRAFT (note: not mandated by PLOS NTD by name; keep as internal aid) |
| PROBAST (S3) | reproducibility | OPEN — DRAFT (internal aid) |
| Software/package versions | reproducibility | PARTIAL — R verified; **primary Python stack not preserved** |
| Saved prediction outputs (repro) | reproducibility | PARTIAL/OPEN — inventory incomplete; preds in quarantine, not deposited |

None unresolved item may be marked complete. STROBE is the PLOS NTD-mandated observational checklist; TRIPOD+AI/PROBAST are advisable (EQUATOR) but **not** required by PLOS NTD by name (see `external_claim_verification_latest.md` #10).

---

## E. Three controlled plans (§11)

### Plan A — Freeze and submit Paper 1 (no new analyses)
Allowed scope: accurate M4/M5 hierarchy (already correct); framework-centered reframe (already largely done); writing corrections (SL-side operational units/standardized NB; MAUP cautious language; optional "not powered" clause; reference reconciliation and year fixes); literature context (add Lowe 2017/2021, Vietnam superensemble, Beal 2025 [= PMID 40901247, one source], Johansson 2016, EWARS); reproducibility closure (finalize S1–S3, deposit code + Zenodo DOI, transparent software-version disclosure); SI completion; declarations (ethics/funding/CoI/CRediT/ORCID/approval); layout and references. **No new modeling, no recomputation.** This plan is viable now — every remaining blocker is administrative/reproducibility, not scientific.

### Plan B — At most one strengthening analysis
Pick **exactly one**, by value/feasibility/low-scope-risk:
- **Preferred: a flexible (loess) calibration curve near p\*=0.30** for the primary models — highest value-to-cost; answers review §3.8; **re-plot from saved predictions, no model refit**; does not change the estimand.
- **Alternative (if a reviewer specifically challenges the single holdout): rolling-origin refit** of M0–M3/M1 (AUC/Brier/NB₀.₃₀ across origins, median/IQR) — higher value against the "single split" criticism, but requires refitting (scope/effort cost) and re-deriving predictions.
Do **not** perform both; do not perform either during this audit.

### Plan C — Paper 2 (reserve)
Reporting-delay simulation; provisional/backfilled real-time counts; nowcasting; rolling-origin **real-time** evaluation; adaptive/online (conformal) recalibration; stakeholder-elicited decision thresholds; 3–6-month seasonal horizons; full cross-country feature harmonization. These change the estimand and/or data requirements and should not expand Paper 1.

---

*No model, metric, bootstrap, calibration curve, DCA curve, or dataset was recomputed. No manuscript revision was modified. Nothing was staged, committed, or pushed.*
