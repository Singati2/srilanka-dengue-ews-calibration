# Study Decision Log

*A running, reverse-chronological record of the study's **new directions, approaches, and decisions** — what changed, why, and what it affects. Maintained by the Geospatial Lead.*

**Update discipline:** append a new dated entry (newest at top) whenever (a) a scope/method decision is settled, (b) the direction or approach changes, (c) a deliverable is produced/frozen, or (d) an open question is opened or closed. Keep it short; link to the spec/report that carries the detail. This log is the single place to answer "what's new and what did we decide?" without re-reading every doc.

**How to read the tags:** `DECISION` = a settled choice · `DIRECTION` = a change in approach/emphasis · `DELIVERABLE` = an artifact produced · `OPEN` = a question raised, not yet closed.

---

## 2026-08-20 — `wp5_05b` run: exposure construction moves the **decision**, not the score — and a recorded structural claim is corrected

**`DELIVERABLE` — the last unrun analysis in the plan is done.** `notebooks_wp45/wp5_05b_decision_
sensitivity_refit.ipynb`, 20/20 QC → `Manuscript_Figures/wp5/WP5_F7b_decision_sensitivity_refit.
{pdf,png}` + 8 quarantine tables + a full prediction panel. M5, M4 and M5's no-climate twin refitted
under **four** exposure arms, on the `sl_ladder` rebuild. **Independent-rebuild version — never to be
reported as the registered re-run.** Baseline reproduces `sl_04` to **exactly 0.0**. **Every notebook
in the plan has now been run.**

**`DECISION` — the ladder is run with four arms, not three.** Build C is two changes at once, and
the 2026-08-13 entry is explicit that only one is MAUP. So `C_frac` (lapse correction, area weights)
was added to isolate the **orography deficit** from **sub-grid population placement**. Without it the
headline number would have silently attributed the whole of Build C to MAUP — the exact error that
entry warned against.

**`DIRECTION` — THE finding, and it changes what a sensitivity analysis should report.** Exposure
construction does **not** move what the model *scores*: ΔAUC and ΔNB@0.30 span zero under every arm
and both models (AUC range across builds 0.0018; |ΔNB| ≤ 0.003). It **does** move what the model
*decides*: **72** alerts flip under population weighting, **64** under the orography correction,
**121** under both — against a measured swap-path noise floor of **3**. A sensitivity analysis
reading only ΔAUC and ΔNB would have reported a null. **Report the flip count alongside them.**

**`DIRECTION` — fourth independent appearance of ΔNB's blindness to threshold-local perturbations.**
121 alerts change sign and ΔNB moves **+0.0004 [−0.0022, +0.0031]**. Net benefit averages over the
panel a quantity in which flips in opposite directions cancel; it is the right decision-theoretic
summary and the wrong sensitivity statistic. Now demonstrated on the registered re-run itself, not
only on perturbations of frozen predictions.

**`DECISION` — the one thing that does move is calibration, and only in M5.** Δ calibration slope is
**+0.0234 / +0.0235 / +0.0345** under B / C-orography / C-full, and **all three intervals exclude
zero**; M4's do not, and change sign. Small in absolute terms and *away* from the ideal of 1
(1.0847 → 1.1192), so the honest reading is a detectable, clinically minor degradation — not a
finding to headline. It is the WP6 bridge again: miscalibration is where exposure construction shows
up.

**`DECISION` — a claim in the 2026-08-13 entry is CORRECTED, with the mechanism measured.** That
entry reads: Build C = Build B + a constant per-district offset, so *"district-relative models absorb
it exactly → Build C cannot flip any alert."* **The premise is confirmed** (within-district sd of the
B→C temperature offset, max over districts: **1.5e-6 °C**). **The conclusion is false for M5**, which
carries district fixed effects and flips **67** alerts B→C. Rather than argue it, the notebook breaks
the model in the one place the argument depends on: **refit M5 with the climate entered linearly and
the flips collapse to 10 (0.25%) — a 6.7× drop.** An additive district intercept absorbs a constant
shift in the **linear predictor**; Build C shifts **temperature**, which M5 reads through a natural-
cubic crossbasis, and a nonlinear function of a shifted input is not a shifted function of the input.
**The rule as it should now read: models *linear* in temperature with district fixed effects absorb
Build C; models with a nonlinear exposure–response do not.** The distinction matters because the
second description is the published model, and is the commoner design in this literature.

**`DIRECTION` — the transferable lesson: a structural argument is a hypothesis until something is
broken to test it.** The 2026-08-13 claim was correct algebra about the wrong object, and it survived
three months because it was *plausible and never executed*. It cost nothing to check — one refit with
the crossbasis swapped out. **Where a conclusion rests on "the model absorbs this", delete the
absorbing structure and count.**

**`DELIVERABLE` — `wp5_05`'s envelope is VALIDATED, and its stated bias had the stated sign.**
`wp5_05` bounded this answer without a refit and warned its transfer coefficient was *"attenuated by
the missing lag structure"*. Against the refit at p*=0.30: A′→B envelope **76** vs refit **72**;
A′→C envelope **104** vs refit **121**. It bracketed both rungs, was within four alerts at the first,
and **under-counted at the second — the direction it predicted**. Its 6.0% bound was never approached
(largest refit flip rate anywhere in the band **3.44%**). **A bound whose error direction is known in
advance earns its place in the record even when the refit is coming.**

**`DIRECTION` — the two rungs act differently, which is why they had to be separated.** Population
weighting flips **near-symmetrically** (35 on / 37 off); the orography correction is **directional**
(15 on / 49 off) — cooling the highlands turns alerts off. Flips concentrate where the Build C offset
is largest (**r = +0.66** across 26 districts; Nuwara Eliya 7.9%, Matale 7.3%, Badulla 6.6%), which
**independently corroborates `wp5_07`'s F8 result through a refit rather than an envelope**.

**`DECISION` — gates that carried the run.** (1) The **negative control**: M5's no-climate twin is
bit-identical (**exactly 0.0**) under all four arms — the 2026-08-18 diagnostic applied *before* the
fact rather than after. (2) The **swap-path null**: rebuilding Build A′ *through the swap machinery*
gives the noise floor (3 flips, max|Δp| 1.06e-3), so every flip count is read against the machinery's
own movement. (3) The **panel gate**: labels and split are byte-identical across arms. (4) **Knots
re-derived per arm**, with a fixed-knot variant showing the flips survive (72/64/121 → 74/65/119).

**`OPEN` — write-up integration is the outstanding item, not analysis.** `wp5_05b` is not yet in
`manuscript/wp4_wp5_sections/`, not in the v44 Results Q7 port, and its numbers are not in
`scripts/verify_numbers_v44.py`. The correction above also means the **2026-08-13 entry's structural
note must not be quoted as written** in any draft.

---

## 2026-08-18 (c) — The ladder rebuild's rainfall was mirrored north-to-south; corrected, and two conclusions change

**`DECISION` — a defect found in `sl_01_exposure.ipynb` and fixed; `notebooks_sl_ladder/` and
`wp4_02b` are both re-run.** `sl_01` indexed the staged CHIRPS window with
`ai = cell_row − min(cell_row)`. `cell_row` is **raster order (north-down)**; the staged array is
stored in the netCDF's **latitude-ascending (south-up)** order. Every district received its north–south
mirror image's rainfall — Galle got Killinochchi's, Colombo got Mannar's, Ratnapura got Mullaitivu's.
**Only 3 of 26 districts got their own.** The existing bbox assert could not catch it: a flipped index
range is identical, so the check passed on a completely wrong table.

**`DIRECTION` — this is the trap the study already recorded, and writing it down did not prevent it.**
The 2026-08-12 entry records exactly this hazard (`i = 1999 − row`) from building WP5's precipitation
twin. The rebuild hit it anyway three notebooks later, because the note was filed as a property of the
CHIRPS **reader** and `sl_01` is a CHIRPS **consumer**. **A trap recorded against one component does
not transfer to the next component that touches the same data.** The durable fix is a gate at the
point of use, not a note.

**`DELIVERABLE` — two gates now sit in `sl_01`, either of which would have caught it.** A
**geographic** one — the southwest wet zone must out-rain the northern dry zone, now reading Kalutara
3,821 mm against Killinochchi 996 mm — and a **cross-check against `wp5_01`'s independently-built
Build A′**, which now agrees to **4.2e-6 mm**. The second is the stronger and was available all along:
*the answer was already in the quarantine, computed by another notebook.*

**`DIRECTION` — the diagnostic that isolates a data defect from a modelling difference.** Every
climate-carrying model moved and no climate-free model did: M2 **0.6422 → 0.7034**, M3 0.6735 → 0.7204,
M4 0.7190 → 0.7604, M5 0.7570 → **0.7652**, while M0, M1 and M5-no-climate are unchanged to the digit.
**If a data error is real, the models that cannot see the data must not move.** Worth applying to any
future discrepancy before reaching for an explanation.

**`DECISION` — §4 of the rebuild report is withdrawn and rewritten; its argument was wrong.** It read
the full-model correlation with the frozen run (0.881) against the no-climate arm's (0.976) as the
**measured cost of ERA5 0.25° in place of ERA5-Land 0.1°**, and concluded a CDS key would buy most of
it back. Corrected, the full-model correlation is **0.9752** against **0.9758** — a gap of **0.0006**,
not 0.095. **Essentially all of it was the defect.** What a CDS key would buy is now *unmeasured, not
measured*.

**The transferable lesson, and it is not about CHIRPS: a defect was absorbed by the most plausible
explanation available.** An exposure substitution the team already knew was in play sat exactly where
the discrepancy appeared, so the reasoning looked sound — which is what made it dangerous. The check
that broke it was cheap and structural: **M5-full and M5-no-climate differ only in the climate block,
so their correlations with the frozen run cannot diverge by 0.095 unless the climate block itself is
wrong.** Ask what a discrepancy *cannot* be before accepting what it plausibly is.

**`OPEN` — the rebuild's headline moved and the earlier claim was too generous.** The matched increment
is now **+0.0166 [+0.0055, +0.0293]** (was +0.0071 [−0.0041, +0.0198]) against the frozen
**+0.0087 [−0.0079, +0.0245]**. So the rebuild's conditional interval now **excludes zero** and its
point estimate is roughly **twice** the frozen one. The 2026-08-17 entry's "the deflationary conclusion
survives the substitution — same qualitative reading, interval covers zero" **is corrected**: the sign
and order of magnitude replicate, the magnitude does not, and the rebuild is the more favourable of the
two. Two reasons not to read it as a challenge to the frozen result: the intervals are not comparable
(conditional vs development-inclusive), and the exposure is a different product. **The deflationary
conclusion is not overturned; the claim that it was independently confirmed at the same magnitude is.**

**`DIRECTION` — `wp4_02b`'s monotone trend did not survive, and the increment result got stronger.**
Corrected, the buffered-minus-control gap runs **+0.0379 / +0.0238 / +0.0030 / −0.0539 / −0.0274**
across 0–100 km: it **turns at 75 km and partially recovers at 100 km**, so the tidy "cost grows with
radius" reading in the 2026-08-18 (b) entry is withdrawn. **Exactly one radius reaches significance —
75 km, −0.0532 [−0.0916, −0.0157]** — and 100 km does not. Meanwhile the climate increment is now
**unchanged by spatial CV in the clean direction**: every change-vs-temporal interval spans zero with
every point estimate within 0.008 of the temporal split, where the mirrored run had put the buffered
arms awkwardly *above* temporal.

**`DECISION` — quote the cluster bootstrap, not the control-draw z.** The z compares a buffered fold to
the spread of ten control draws and ignores district-level sampling error. At 0 km it reads +2.57 with
all ten controls below while the bootstrap CI spans zero. The 2026-08-18 (b) entry leaned on the z;
that framing is corrected here.

---

## 2026-08-18 (b) — The cross-model fold contrast is measured on M5 itself, and M5's answer is not M6's

> **PARTLY SUPERSEDED by the 2026-08-18 (c) entry above.** This run used the mirrored rainfall column.
> The headline — M5's fold is not expensive at the operative radius, and the climate increment survives
> spatial CV — holds and strengthens. **Withdrawn: the monotone "cost grows with radius" reading** (the
> corrected series turns at 75 km) **and the reliance on the control-draw z-score.** Corrected numbers
> are in the (c) entry and in `notebooks_wp45/README.md`.

**`DELIVERABLE` — `notebooks_wp45/wp4_02b_fold_effect_within_m5.ipynb`, 17/17 QC, 2,912 fold-fits →
`Manuscript_Figures/wp4/WP4_F_fold_effect_within_m5.{pdf,png}` + 7 quarantine tables.** The contrast
`wp4_02` recorded as blocked — **M5 under buffered spatial CV versus M5 under the temporal split** —
now exists. M5 and its no-climate twin are refitted under every fold, each buffered fold matched to
**ten random-district controls of identical size**, exactly the design that made `wp4_02`
interpretable.

**`DIRECTION` — the price of a fold is a property of the MODEL, not of the geography alone.** M6 and
M5 disagree in **sign** at the operative radius and agree only at the far end:

| radius | M6 gap (`wp4_02`) | M5 gap (`wp4_02b`) |
|---|---|---|
| 0 km | −0.022 | **+0.023** (z = 2.09, 10/10 controls below) |
| 100 km | −0.070 | −0.053 (z = −2.54, 0/10 below) |

At the radius `wp4_01` selected and the study actually uses, **M5's buffered fold beats an
equally-sized random training set.** So `wp4_02`'s within-M6 result could never have substituted for
this one, and the 2026-08-14 (d) note that the two §5.1 asks "are not interchangeable" was right for
a reason stronger than the one given then: the models differ not in degree but in direction.

**`DECISION` — report the significance on the decision metric, not on AUC.** Every M5
buffered-minus-control **ΔAUC** interval spans zero, 100 km included (−0.0505 [−0.1107, +0.0064]).
On **ΔNB at p\*=0.30** the 75 km (−0.0216 [−0.0412, −0.0039]) and 100 km (−0.0353 [−0.0610, −0.0120])
intervals exclude it. The defensible claim is a **monotone, one-signed trend reaching conventional
significance only past 50 km and only on net benefit** — `wp4_00`'s power table is the citation for
why, at n = 26, that is the most the design can carry.

**`DELIVERABLE` — the referee's actual question is answered, and the answer is favourable.** The
paper claims an *increment*, not an AUC. Under buffered folds the climate block earns **+0.0218 (0 km),
+0.0200 (25), +0.0266 (50), +0.0152 (75), −0.0015 (100)** against **+0.0071** under the temporal split;
every change-vs-temporal interval spans zero. **Spatial CV does not deflate the increment** — if
anything the temporal split is the conservative choice. The point estimates sitting *above* temporal
are **not** claimed as a real gain; the honest reading is *unchanged*.

**`DIRECTION` — the long-radius dependence localises in the climate block.** The no-climate twin's
gap stays nearly flat (+0.0072 → −0.0154) while M5's falls to −0.0526. Coherent: climate fields are
spatially smooth over hundreds of km, so a neighbour's rainfall proxies yours in a way a neighbour's
case history does not.

**`DECISION` — this is the independent-rebuild version and is labelled as such everywhere.** Refitted
on `sl_linked_v2equiv.csv` (ERA5 0.25° + CHIRPS), not the frozen linked table. Fidelity measured:
3,926 test rows matched exactly, label agreement 0.988, M5 AUC 0.7570 vs the frozen 0.7715, ρ = 0.881.
The baseline arm reproduces `sl_04` to **exactly 0.0** through the generalised fitter, so every
contrast is within-rebuild and the offset is common to all arms. `registered_rerun: false` is stamped
in the provenance.

**`OPEN` — two traps recorded because either would have produced a confident wrong number.**
(1) A held-out district's RDHS fixed effect is **not estimable** — its dummy is all-zero in training,
so it is scored at the reference district's intercept. **Every temporal-versus-fold contrast therefore
conflates losing the neighbours with losing the fixed effect**; only buffered-minus-control separates
them, because the control carries the identical handicap. (2) **Pooled AUC and per-district AUC answer
different questions**: at 0 km the pooled gap is +0.0233 while **15 of 26 districts are individually
negative**. Pooling rewards the between-district ordering, which the per-district table cannot see.

**`OPEN` — `wp5_05b` is now the last unrun analysis in the plan**, and it is runnable on the same
substitute: the registered §3.3 re-run (ΔAUC / Δcalibration under Builds A′/B/C), with WP5's exposure
tables already sitting beside the linked table in the quarantine.

---

## 2026-08-18 — The WP4/WP5 port is in the v44 candidate and every number in it is machine-checked; the "§5.1 blocked" framing is retired

**`DELIVERABLE` — Results Q7 exists in the v44 biomath candidate** (`wp45-into-v44` @ `e08f2ee`,
worktree branch, three commits ahead of `upstream/agent/v44-hybrid-light-decision-framework`,
**unpushed**). Ported, not copied: the fragment was written in v18's voice against a Methods section
with no incremental-estimand formalism, so it is reframed against $\Delta V_{C,k}$ — exposure
construction is an operationalisation choice inside $I^C$, and the fragment's "climate block removed
(ceiling)" **is** the estimand's own $I^{SC} \to I^S$ contrast and is named that way throughout.
Two Methods subsections, one Results question, five tables, four figures, its own Discussion
subsection, 11 new bibitems. `FINAL_CANONICAL_DECISION.md` line 8 is **annotated, not rewritten** —
the override is still unratified, and the original wording is preserved beneath it. **No TeX
toolchain here: verified structurally (58/58 cites, 20/20 refs, 15/15 tabular column counts,
balanced environments) — A COMPILE HAS NOT BEEN RUN.**

**`DELIVERABLE` — `scripts/verify_numbers_v44.py` now carries 183 checks, up from 46**, and
`docs/v44_number_verification_2026-08-17.md` records both passes. The first pass found **4
mismatches inherited from v44** — none introduced by the biomath rewrite — plus a 16-occurrence
stray-comma table defect; 3 of 4 and the whole LaTeX defect are fixed. The second pass added the
port's **137 WP4/WP5 numbers, recomputed from the quarantine tables rather than transcribed**, and
that recomputation surfaced **three more defects** in the freshly-ported text (50 km gap −0.018 →
−0.019, 100 km gap −0.068 → −0.070, flipped-row event rate 0.087 → 0.088), all fixed.

**`DIRECTION` — the crosswalk-versus-recompute distinction is the reusable lesson.**
`BIOMATH_NUMERIC_CROSSWALK.md`'s "no candidate number differs from the canonical manuscript" is true
and is *not* this check: it compares the candidate to the **previous `.tex`**, where numbers are
preserved by construction, and never opens an analysis output. It therefore cannot see an error
**inherited from** v44 — which is where all four mismatches lived. Same shape as 2026-08-15's README
defect: **the summary layer is the layer nobody re-derives.**

**`DECISION` — a skipped check is now an assertion, not a silent pass.** The first draft of the
WP4/WP5 section guarded its modifier-screen lookups with `if key in fi:` and **silently skipped six
checks** on a wrong key (the screen's flip response is `flip_AC_pct`, not `flip_AB_pct`; the same
wrong-rung error had been applied to the three top-flip districts). A silently skipped check is
precisely the untraceable class the script exists to prevent. Both aggregation hazards the
provenance doc warns about were also live and are handled explicitly: **district-week vs
district-mean** (0.205 °C vs 0.171) and **raw vs recalibrated** (flips 35–76 raw vs 46–83 recal; the
441 ceiling holds raw-to-raw only, recal-vs-raw gives 759).

**`DIRECTION` — "blocked by §5.1" is retired as a description of the two registered re-runs; the
correct statement is "has not been run."** The old justification was that the archive holds
predictions and not design matrices. It does not survive inspection:
`analysis/v12_referee_response/run/sl_matched_and_recal.py` contains **both** the design-matrix and
cross-basis builders (`design()`, `crossbasis()`, `climate_block()`, `fit_eval()`) and reproduces
frozen M1/M4/M5 to <1e-6. All three `\REGBLOCK` sites now say so. **Sixth recovery by the
does-the-blocker-cover-all-of-it test** — and this one had been load-bearing for a year of scope
decisions.

**`OPEN` — what actually remains is an *input*, and a local substitute for it exists.** The
builder's declared inputs are `/home/mpcrlab/…` paths (the frozen v2 linked table, the two pilot
prediction files) that are not on this Mac. But the 2026-08-17 ladder rebuild produced
`data_quarantine/sl_ladder/sl_linked_v2equiv.csv` — same schema, 10,764 rows, carrying
`t2m_mean_c` / `precip_sum_mm` / `rh_mean_percent` and the three missing-flags — and WP5's A′/B/C
exposure tables sit beside it in `data_quarantine/wp5_exposure/`. **So both re-runs are runnable
here today**, conditionally: on a rebuilt table whose fidelity is *measured* (test set exact at
3,926, label agreement 0.988, matched raw ΔNB **+0.0071** against the frozen **+0.0087**,
no-climate correlation 0.976 and full 0.881). A result from it is an **independent-rebuild version**
of the registered re-run, not the registered re-run — it must never be reported as the latter.

**`OPEN` — the `+0.0049` three-week reporting-delay increment still stands against the archived
`0.005079`.** Unfixable by retyping: a stable claim tracing through `v15_final`,
`v16_recalibrated_matched_integration`, `v17_plos_gph_submission` and `v20_round3`, resting on a run
that is not the archived JSON. It is the highest-risk open number in the manuscript — v15's own peer
review calls it the most policy-relevant result and v20 promoted it to the abstract. **A referee who
recomputes it lands on 0.0051.** Needs the run reconciled, most likely on the Linux box.

**Unpushed as of this entry:** four commits on `m6-geomatics-notebooks` (`b4240fa` PI-ask draft,
`dc0a062` ladder rebuild, `4ca6a51`, `20b16e6` verifier) and three on `wp45-into-v44`. The
consolidated PI ask (`docs/pi_ask_v1_geomatics_open_questions.md`, five items) is still **DRAFT and
unsent**.

---

## 2026-08-17 — An independent Sri Lanka M0–M5 rebuild runs end to end on this Mac; two undocumented conventions recovered

**`DELIVERABLE` — `notebooks_sl_ladder/` (6 notebooks, all executed) + `docs/sl_ladder_rebuild_2026-08-17.md`.**
A Sri Lanka-only reconstruction of the ladder from raw inputs, gated against the frozen run's own
3,926 test predictions. Test set matches **exactly at 3,926**; label agreement **0.988**; matched raw
ΔNB **+0.0071** against the frozen **+0.0087**. Analysis rows 10,490 vs 10,516 — the 26-row gap is one
week and fully explained. Outputs go to git-ignored `data_quarantine/sl_ladder/`, per the standing
code-and-reports-only guardrail.

**`DIRECTION` — the CDS key was not the prerequisite it looked like.** The blocker was assumed to be
ERA5-Land 0.1° behind a CDS key, plus RDHS polygons to build cell masks. But WP5 had already cached
an ERA5 0.25° window, CHIRPS 0.05°, **and the per-district grid weight files** (`w_area`/`w_pop`) —
and those weights are precisely what the polygons would have been needed to produce. The whole path
therefore runs today on a coarser product. The key is now an **optional fidelity upgrade with a
measured payoff**, not a gate.

**`DELIVERABLE` — the exposure substitution's cost is localised, not merely asserted.** M5-no-climate
and M5-full are identical except for the climate block, so comparing them against frozen isolates the
product swap: correlation **0.976** (no-climate) vs **0.881** (full). Everything except the exposure
reconstructs near-exactly; the gap lives where it should.

**`DECISION` — two conventions in the frozen linked-table build are recorded here because they exist
nowhere else.** Neither appears in the code or the Methods; both were recovered by sweeping against
the frozen labels rather than guessed (`sl_03`):
1. **Week offset** — `week_start = ISO_Monday(y, w) − 7d`, not `ISO_Monday(y, w)`. Worth 17 points of
   label agreement (0.820 → **0.988**), with a sharp peak. Reads as the WER bulletin labelled week *w*
   carrying the week that just ended.
2. **Population denominator** — time-invariant per district, not year-varying. This also explains why
   only 2018–2020 WorldPop was ever staged: a constant denominator makes the within-district quantile
   label scale-invariant.
Residual disagreement is 48/3,926, and **all 48 sit within 15% of their district's threshold** —
boundary noise, not a systematic error still hiding. **These belong in the study's own documentation
regardless of this rebuild**: anyone re-deriving the Sri Lanka table from the WER hits exactly this
and currently has nothing to guide them.

**`DIRECTION` — this is an independent robustness result the study did not previously have.** The
deflationary conclusion (small, positive, interval covering zero) survives being rebuilt on a
different reanalysis product. Stated with its limits: the rebuild's interval is **conditional**
(+0.0071 [−0.0041, +0.0198], B=2000, district clusters) while the frozen headline is
development-inclusive and therefore wider and more honest — the two are not interchangeable. M0/M2/M3
are **reimplementations** from the Methods spec (no in-repo Sri Lanka reference) and carry weaker
provenance than the ported M1/M4/M5.

**`OPEN` — publication of a competing analysis of the upstream models goes to the PI first.** The
rebuild lives in the fork and is internal. Also open: whether to apply the pinned fidelity environment
(Python 3.10 / numpy 1.26.4 / pandas 2.1.3 / sklearn 1.7.2) — this ran under Python 3.12 / sklearn
1.9.0, so some residual gap may live in library drift rather than in the exposure.

---

## 2026-08-17 — Colombia is closed to new work, WP4/WP5 is folded into the v44 candidate, and the target is submission

**`DECISION` — no new Colombia analysis. Colombia's existing role in the manuscript is untouched.**
The plan's remaining Colombia deliverables (§4.3 block CV, cross-setting F2, the both-settings
leakage memo) are **withdrawn from scope**, not deferred. This is a decision about *new* work only:
the two readings were separated explicitly before settling, because they are not the same job.
Colombia is load-bearing in v44 — 88 mentions, one of two case studies, in the abstract, and the
sole external validation — so **removing it would weaken the paper**, and the paper is already
Sri Lanka–primary ("Sri Lanka (primary; RDHS division-week, 2018 to 2025) and a selected
complete-case Colombian municipality-week subset"). Nothing in the manuscript changes.

**`DIRECTION` — the cost of this is that WP4 loses its powered companion, and the write-up must say
so.** `wp4_02`'s fold effect was designed as the compact-country sensitivity companion to Colombia's
~1,000-municipality block CV (2026-07-07 D1). With §4.3 withdrawn there is no powered counterpart,
so the n=26 result stands alone: point estimates one-signed at every radius, CI spanning zero at the
operative radius (**−0.022 [−0.055, +0.011]**) and excluding it only at 75–100 km. It goes into the
paper as a **characterised limitation with the power caveat stated plainly**, never as a certified
claim. `wp4_00`'s power table is the citation for why.

**`DECISION` — WP4/WP5 (Sri Lanka) is folded into the v44 hybrid-light candidate.** This **overrides
`FINAL_CANONICAL_DECISION.md` line 8**, which holds M6/WP4/WP5 "outside Paper 1 evidence … only as
pending Discussion notes". Author's call, made knowing that position. Rationale is referee-facing,
not volume: the completed work answers the two most predictable objections to a spatial EWS paper —
*"your CV ignores spatial autocorrelation"* (`wp4_02`, measured against a size-matched control rather
than argued) and *"your conclusions depend on how exposure was built"* (the three-build ladder + F7)
— and WP5's ΔNB-blindness result qualifies sensitivity analyses **elsewhere in this same paper**.
**`OPEN`: this contradicts a canonical decision doc and therefore needs PI ratification**, which is
now a fifth item for `docs/pi_ask_v1_geomatics_open_questions.md`.

**`DIRECTION` — submission is not blocked by §5.1, and the earlier framing of Q1 was measured against
the wrong target.** `V44_VS_BIOMATH_DECISION_MEMO.md`: "No further analysis is required to submit
either way; the open blockers are author-owned (ethics, ORCIDs, funding, COI, Zenodo DOI/license,
OpenDengue v1.3 record id)" — all administrative. Q1/Q2 remain the critical path to *completing*
§3.3 (`wp5_05b`) and the cross-model contrast (`wp4_02b`), but **not** to submitting. Both blocked
analyses are refinements of results that already stand.

**`DIRECTION` — the integration target is v44 on `upstream/agent/v44-hybrid-light-decision-framework`,
not this branch.** `manuscript/wp4_wp5_sections/*.tex` was drafted in **v18's** voice and section
conventions; v44 is a different document with a different estimand notation
($\Delta V_{C,k}$). The fragments must be **ported, not copied**. Working branch `wp45-into-v44`.

---

## 2026-08-16 (b) — The four open questions are consolidated into one document; both drafts await sign-off

**`DELIVERABLE` — `docs/pi_ask_v1_geomatics_open_questions.md`, DRAFT, not sent.** The four questions
have accumulated across separate PR #1 memos, where they are easy to lose. Each is stated with **the
smallest artifact that would unblock it**, so answering is cheap and a partial answer is still useful.

**`DECISION` — Q1 and Q2 need DIFFERENT artifacts, and this is the sharpest reason not to bundle
them.** Previously they were separated only by *urgency* (wp4_02 raised one, wp5_05 lowered the
other). They are also separated by *substance*: **WP4 re-fits the same columns on different rows, so a
static design matrix suffices; WP5 §3.3 re-fits on different exposure values, so the columns must be
regenerated and what it needs is the cross-basis BUILDER, not its output.** Sending the matrix does
not unblock WP5; sending the builder does not unblock WP4 as cheaply. If only one can be answered it
should be Q1.

**`DECISION` — the v44 positions are quoted verbatim rather than characterised.** Verified against the
branch: `FINAL_CANONICAL_DECISION.md` says M6/WP4/WP5 "appear only as **pending** Discussion notes",
which supports the gate-consequence reading rather than a rejection; `V44_VS_BIOMATH_DECISION_MEMO.md`
says "no further analysis is required to submit either way; the open blockers are author-owned."
Both quotes checked against the files, not recalled.

**`DELIVERABLE` — `docs/pr1_memo_draft_2026-08-16.md`, DRAFT, not posted.** Covers `9085b3f` and
`9f4789e`, in the register of the existing memos, and points at the ask document rather than
restating the four questions a fifth time.

**`OPEN` — neither has been sent.** Posting is a communication to collaborators and is held for
explicit sign-off.

---

## 2026-08-16 — Plan §3.6 and Figure F8: the fifth recovery, and the loudest signal in the screen is a decoy

**`DIRECTION` — the blocker-coverage test recovers work for the fifth time, and F8 is the last figure
in the plan's checklist.** §3.6 was recorded as downstream of the §5.1-blocked refit. It is not:
per-district calibration slope/intercept, per-district ΔNB and per-district flip counts are all
reductions of the **frozen predictions**, and every modifier the plan names was already staged by M6
batches A/B. `notebooks_wp45/wp5_07_miscalibration_structure_and_F8.ipynb`, **16/16 QC**.

**`DELIVERABLE` — `WP5_F8_miscalibration_structure.{pdf,png}`** (6 panels, double column; PNG
committed, PDF gitignored) + `wp5_miscalibration_structure_srilanka_v1.csv` and
`wp5_f8_modifier_screen_srilanka_v1.csv`. With F2 and F7 this completes the plan's figure set.

**`DECISION` — the screen is run under §3.6's own guardrails, treated as hard requirements.** 4
responses × **15 pre-specified** modifiers = **60 tests**, Benjamini–Hochberg across the entire grid;
**19 reach raw p<0.05, 6 survive**. All 60 are plotted in panel (e) so the figure cannot be read as a
selected subset. Stamped `EXPLORATORY_EXPLANATORY`: nothing here may re-enter the ladder as an
accuracy predictor.

**`DECISION` — carry a non-geospatial decoy through any screen of this shape.** The single strongest
association of all 60 is calibration **intercept** against the district's own **alert prevalence**
(ρ=0.85, q<0.001) — near-tautological, since an intercept absorbs a base rate. `prev` was put in the
panel deliberately for exactly this reason. Had it been left out, the tautology would not have gone
away; it would have been **inherited silently** by whichever geospatial modifier happens to correlate
with outbreak burden. This is the transferable methodological point, above any specific association.

**`DELIVERABLE`/`OPEN` — miscalibration has real spatial structure; the flip concentration does not
resolve.** Calibration slope spans **0.67–2.23** across districts and tracks cropland fraction
(ρ=0.61, q=0.031) and land-cover diversity (0.59, q=0.032) up and population density (−0.50) down,
**all surviving adjustment for prevalence** (partial ρ 0.50 / 0.49 / −0.44). That is the WP6 bridge.
By contrast, flips concentrate in the highlands (Badulla 9.9%, Nuwara Eliya 9.3%, Ratnapura 6.0%;
ρ≈0.55 on slope/elevation/HAND) but **elevation and the measured B→C displacement are collinear at
ρ=0.74 and neither survives controlling for the other** (0.27, p=0.18; 0.05, p=0.82). **Recorded as
unidentified at n=26 — do not let a later revision upgrade it to "terrain drives the flips".**

**`DECISION` — ΔNB's blindness now has a third independent demonstration.** No modifier explains
per-district ΔNB (strongest: population density, ρ=0.40, **q=0.15**). Given `wp5_05`'s structural
result this is the *expected* outcome, not an additional null: the same threshold-local insensitivity
that flattens ΔNB nationally flattens it district by district.

**`DELIVERABLE` — the write-up is updated to v2** (`wp4_wp5_methods_results_v1.tex`): a Methods
paragraph for the screen, a Results subsection, the F8 figure block and caption, provenance rows, and
the Benjamini–Hochberg citation. Structural check re-run and extended: all `\cite` keys now resolve
against the two `.bib` files, all four `\includegraphics` targets exist, no dangling `\ref`.

---

## 2026-08-15 — Plan Phase 6: the WP4/WP5 write-up is drafted, and one README number was wrong

**`DELIVERABLE` — `manuscript/wp4_wp5_sections/`, three files.**
`wp4_wp5_methods_results_v1.tex` carries two Methods subsections (the three-build exposure ladder;
spatially-honest CV) and four Results subsections (exposure displacement; decisions; population
product; spatial CV), plus five tables, three figure blocks with captions, and a commented block of
Discussion material. `wp4_wp5_number_provenance_v1.md` maps every number to the artifact it was
recomputed from. `wp4_wp5_references_add_v1.bib` adds the 10 citations the sections need and that the
manuscript `.bib` does not already carry (MAUP, spatial CV, ERA5/ARCO, Magnus, GLO-30, GHCN, GHS-POP).
Written in the v18 candidate's voice and section conventions; structural check passes (no LaTeX
toolchain on this machine, so it is **not** compile-verified — flagged, not hidden).

**`DECISION` — the write-up is held OUTSIDE the manuscript tree, deliberately.** PR #8 places
M6/WP4/WP5 outside Paper 1 evidence pending PI direction, and Paper 1 vs Paper 2 is still unanswered.
Drop-in fragments cost nothing to move once the PI decides; editing a live manuscript before that
decision would have to be undone. The two §5.1-blocked analyses are marked inline with `\REGBLOCK` so
the revisit points are mechanical to find.

**`DIRECTION` — every number was recomputed from the quarantined tables, not transcribed.** That is
what caught the error below, and it is now the standard for any prose that quotes a result.

**`OPEN` → `DECISION` — a README number was wrong and is corrected.** `notebooks_wp45/README.md` said
population weighting makes **"fifteen districts drier, eleven wetter"**; recomputation gives
**17 down / 9 up**, identical under either baseline arm. The figure never appeared in `wp5_01` — it
was introduced in the README summary. No notebook, table, figure or PR memo is affected. **The
transferable lesson is where it came from:** the wrong number was in the *summary layer*, which is
exactly the layer nobody re-derives. Summaries need the same provenance discipline as results.

**`DECISION` — aggregation level is now stated explicitly wherever a displacement is quoted.** The
same quantity has two legitimate values: population weighting moves weekly mean temperature
**0.205 °C** per district-week but **0.171 °C** as a mean of district means. The sections quote
district-week throughout except where a district is named. Checking a district-week claim against
`wp5_exposure_contrast_srilanka_v1.csv` will disagree and is not an error.

**`DIRECTION` — the methodological finding leads the Results, not the MAUP magnitudes.** The
structural blindness of ΔNB to threshold-local perturbations qualifies *every* sensitivity analysis in
this literature that reads a small ΔNB as "no decision effect" — including analyses reported elsewhere
in this paper. It is written to travel beyond WP5, with the concrete recommendation (report a
decision-flip count alongside ΔNB) stated in the Results and again in the Discussion material.

---

## 2026-08-14 (c) — WP4's evaluation half, measured inside M6: the folds are not cheap, and wp4_01's inference does not survive

**`DIRECTION` — the blocker-coverage test recovers WP4's evaluation half too (fourth time).** The
README blocked `wp4_02` because re-fitting M5 under spatial folds needs its design matrix. True — but
that bars only the **cross-model** contrast. **M6 under spatial folds vs M6 under the temporal split**
is a within-model contrast we fully own, and it is a *better* instrument for WP4's question because
nothing but the validation scheme moves. `notebooks_wp45/wp4_02_fold_effect_within_m6.ipynb`,
**14/14 QC**, 1,456 fold-fits.

**`DELIVERABLE` — `WP4_F_fold_effect_within_m6.{pdf,png}` + three quarantine tables.** Gate first:
**the baseline arm reproduces the committed M6 to 8.6e-15** and the rebuilt label reproduces the
frozen outcomes 3,926/3,926, so every difference is the folds. Selected `C` is effectively constant
across arms (§9.1), so it is not a shrinkage artifact.

**`DECISION` — the confound is controlled, and that is what makes the result usable.** Buffering
removes leakage *and* training data. Every buffered fold is therefore matched against a
**random-district control of identical size**; the buffered-minus-matched gap is the part
attributable to geography.

| buffer | train districts | buffered AUC | matched control | gap |
|---|---|---|---|---|
| 0 km (`wp4_01`'s selected radius) | 21 | 0.5649 | 0.5873 | **−0.022** |
| 50 km | 15 | 0.5582 | 0.5767 | −0.018 |
| 100 km | 9 | **0.5024** | 0.5726 | **−0.070** |

Temporal split 0.6008; LOOCV without buffer 0.5923. **At 100 km the spatially-blocked estimate is
chance (0.502) while an equally-sized random training set still reaches 0.573** — a gap that cannot
be sample size, because size is held fixed by construction. In 0 of 10 control draws at 0, 75 and
100 km did a random subset score below the buffered fold.

**`OPEN` — how far it is resolvable with 26 units.** Cluster-bootstrap CIs (2,000 replicates,
control ensemble averaged inside each replicate): the gap spans zero at 0 km
(**−0.022 [−0.055, +0.011]**) and excludes zero only at 75 km (−0.061 [−0.119, −0.008]) and 100 km
(−0.068 [−0.143, −0.001]). The point estimates are consistent and one-signed at every radius; the
*power* to certify them is what `wp4_00`'s table already warned about.

**`DIRECTION` — `wp4_01`'s "the buffered scheme is cheap" is withdrawn as an inference.** Residual
Moran's I and dependence on spatially proximate training data are **different quantities**, and here
they disagree: residuals of a model fitted with all districts present show no spatial structure, yet
removing the neighbours from training still costs more than removing an equal number of random
districts. Moran's I asks *"having fitted on everyone, is the remainder clustered?"*; a buffered fold
asks *"can this generalise to a region it has never seen?"* **Plan §4.1's design — pick the operative
radius from a residual-range analysis — therefore cannot price the folds.** The price must be
measured. This is the transferable lesson, not the M6-specific number.

**`DIRECTION` — the §5.1 ask gets MORE urgent, in the opposite direction to `wp5_05`.** M5's
external-validation claim rests on a temporal split. If M5 depends on spatial proximity the way M6
does, spatial CV moves it too — exactly the reviewer concern WP4 exists to answer — and that cannot
be tested without M5's design matrix. Same day, `wp5_05` found §5.1 matters *less* than assumed for
§3.3. **The two asks are not interchangeable and must be put to the PI separately rather than
bundled.**

**`DECISION` — scope stamped in the provenance.** `cross_model_rerun: false`. M6's label keeps the
`EXPLORATORY_RECONSTRUCTED_TARGET` caveat (19.2% of test rows) — identical across arms, so it cannot
manufacture a between-arm difference, but it bars quoting any single AUC here as M6's performance.
Nothing here speaks to Colombia, where §4.3's ~1,000-municipality block CV carries the well-powered
claim.

**`DECISION` — environment split recorded.** `wp4_02` runs on the **`freight-eda`** kernel
(Python 3.9.6, sklearn 1.6.1) because **`pywmp-mac` carries no scikit-learn**. The `wp5_*` series
stays on `pywmp-mac`. No overlap in dependencies, so the two are not reconciled.

---

## 2026-08-14 (b) — Plan §3.3 (runnable half): exposure construction changes alerts, and ΔNB is structurally unable to show it

**`DIRECTION` — the blocker-coverage test recovers work for the third time, and it is now standard
practice.** Plan §3.3 pairs a *registered re-run* (ΔAUC, Δcalibration, ΔNB under a refit — genuinely
blocked on the §5.1 design matrices) with the question *does the decision move?*, which is answerable
from the frozen predictions alone. `notebooks_wp45/wp5_05_decision_flip_envelope.ipynb` is executed,
**16/16 QC**. After §3.2 and §3.5, this is the third blocked line with a runnable half; the test is
applied to every remaining blocked item from here, not treated as a lucky find.

**`DELIVERABLE` — a bracket, built from three pieces, only one of which is modelled.**
`Manuscript_Figures/wp5/WP5_F7_decision_flip_envelope.{pdf,png}` (6 panels, double column) plus
`wp5_decision_flip_envelope_srilanka_v1.csv` and `wp5_decision_flip_summary_srilanka_v1.csv`.

1. **An exact, model-free flip curve.** A row flips only if `|p − p*|` is smaller than the movement
   applied to it, so `#{|p − p*| ≤ δ}` upper-bounds the flips from *any* perturbation bounded by δ.
   At p\* = 0.30 a movement of 0.02 in predicted risk cannot flip more than ~6.4% of alerts.
2. **An observed ceiling.** `full` and `noclim` sit on identical rows, so deleting the whole climate
   block is measurable: **441 alerts (11.2%)** at p\* = 0.30.
3. **An estimated transfer coefficient.** `logit(full) − logit(noclim)` isolates the climate-
   attributable prediction; regressed on exposure it gives the model's effective sensitivity without
   the design matrix.

**`DECISION` — exposure construction is not a decision null.** At p\* = 0.30, across four
specifications: **A′→B 35–76 alerts (0.9–1.9%)**, **A′→C 64–104 (1.6–2.6%)** — i.e. **14–24% of the
climate block's entire decision leverage**. District-clustered bootstrap: A′→B 1.94% [1.27, 2.65],
A′→C 2.45% [1.50, 3.57]. WP5's honest-null clause fires on the decision no more than it did on the
exposure.

**`DIRECTION` — the most consequential finding is methodological and belongs in the manuscript.**
`ΔNB` stays within **±0.002** while flip counts are unambiguously non-zero. This is **not** flips
cancelling by direction — they are strongly asymmetric (A′→B adds 67 alerts, removes 9). It is
structural: **a row can only flip if it sits near p\*; threshold-adjacent rows have an event rate
≈ p\*; and p\* is by definition the break-even rate.** Measured, the flipped-row event rate tracks
p\* across both rungs and all four thresholds (0.087 / 0.160 / 0.289 / 0.431 against 0.10 / 0.20 /
0.30 / 0.40; r = 0.96), and the arithmetic closes exactly:
`ΔNB = (+14 − 44 × 0.4286)/3926 = −0.0012`. **Every flip is worth ≈ 0 net benefit either way.**
Therefore `ΔNB` is *structurally insensitive* to any perturbation acting near the threshold, and a
near-zero `ΔNB` must not be reported as "exposure construction does not affect decisions" — the flip
count answers that question, `ΔNB` answers a different one. This bears on how every DCA-based
sensitivity result in the study is worded, not only WP5's.

**`OPEN` → `DECISION` — how much the missing artifact would actually change.** The transfer
coefficient's norm spans **2.3×** across four specifications (R² 0.27–0.38, signs stable), but the
flip count spans far less, because the flip curve is locally near-linear. β would have to be
understated several-fold before exposure construction reached the ceiling. **What §5.1 would add is
the ΔAUC / Δcalibration table, not a reversal of the qualitative answer** — which lowers the urgency
of that ask for §3.3 specifically, though not for §4, §8 or WP4.

**`OPEN` — a defect in the frozen artifact the team must resolve.** `full_recal` is **not** a
monotone recalibration of `full_raw`: 49% of adjacent pairs invert, and AUC differs (**0.7715 raw vs
0.7512 recalibrated**), which a monotone recalibration cannot do. Cause identified in
`analysis/v12_referee_response/run/sl_matched_and_recal.py` §(B): a **past-only rolling-52-week
intercept update refitted every test week**, so the map is time-varying and re-ranks across weeks
while being an exact constant shift *within* a week (147 of 151 weeks; zero within-week inversions).
It is a defensible design, but **every reported AUC must state which column it came from**, and any
sentence of the form "recalibration does not affect discrimination" is false here. Flagged to the PI.

**`DECISION` — this is not the registered §3.3 deliverable and is stamped so.** The provenance
carries `registered_rerun: false`, so the envelope cannot later be mistaken for the re-run.

---

## 2026-08-14 — Plan §3.5 (exposure half): WP5's result is not a WorldPop artifact; one open item closes

**`DIRECTION` — the §3.2/§3.3 split repeats at §3.5, and the same half is runnable.** Plan §3.5 pairs
*"rebuild Build B weights under an alternative population product"* with *"recompute ΔNB at p\* under
each layer."* Only the second needs the fitted model. `notebooks_wp45/wp5_06_population_product_sensitivity.ipynb`
is executed, **17/17 QC**, and delivers the first. This is the second time the "check whether the
blocker applies to all of it" test has recovered work recorded as blocked — it is now worth applying
to every remaining blocked line rather than treating it as a one-off.

**`DELIVERABLE` — three population products at one epoch (2020), all free and anonymous.** WorldPop
UN-adjusted (incumbent), WorldPop R2025A constrained (same producer, newer release), GHS-POP R2023A
(JRC; different institution, built-up-surface dasymetric rather than random forest). Outputs
`wp5_population_product_sensitivity_srilanka_v1.csv` and `wp5_population_product_contrast_srilanka_v1.csv`.
Because Build B normalises weights within district, a product's national total cancels exactly; only
the shape of the surface inside a district can move exposure.

**`DECISION` — the reviewer's obvious attack is answered with a number.** "Your MAUP result is a
WorldPop artifact" fails:

| contrast | mean displacement |
|---|---|
| weight moved, area → population (A′→B, ERA5 grid) | **27.5%** of a district |
| weight moved, WorldPop unadj → GHS-POP | 1.6% |
| exposure, A′→B, weekly mean t2m | **0.205 °C** vs product swap **0.006 °C** |
| exposure, A′→B, rainfall | **3.40 mm/wk** vs product swap **0.161 mm/wk** |

Ratios run **16.7×–32×** at the mean and do **not** narrow in the tails where alerts fire (19.5× in
the wettest 1% of district-weeks; 35.8× in the hottest 1%). In **0 of 26** districts does the product
effect reach the weighting effect, and the ranking of movers survives (ρ = 0.985 / 0.990, identical
top-fives, complete sign agreement) — so `wp5_03`'s per-district statements are not statements about
WorldPop either.

**`DECISION` — version drift inside one producer exceeds the gap between producers.** WorldPop
UN-adjusted vs WorldPop's own R2025A: mean TV **0.0201**. WorldPop vs GHS-POP: **0.0157**. The
instinct that "same producer, newer release" is the conservative substitution is backwards here, and
it bears on any future re-run that upgrades a population vintage without re-testing.

**`OPEN` → `DECISION` — the ~1.4% coastal shortfall is CLOSED, and it was never a methods choice.**
It is specific to WorldPop UN-adjusted 2020: the same 26 polygons lose **0.23%** of GHS-POP and
**0.10%** of WorldPop R2025A. The standing choice between "accept and report" and "switch to
fractional-coverage weighting at the boundary" was a choice between two ways of absorbing another
product's coastline error. Report it as a bounded product sensitivity instead.

**`DECISION` — §3.5's fourth arm is degenerate and should not be built.** Census district totals
carry no within-district spatial information, so distributing them uniformly makes the climate-cell
weight proportional to in-district area — Build A exactly (verified to 0.0) — and the totals
themselves cancel in the within-district normalisation. Not an empirical null; the arithmetic of the
weighting. The plan's §3.5 checklist should be amended to say so.

**`OPEN` — nothing here touches net benefit.** A small *exposure* displacement does not imply a small
*decision* displacement; that inference is what WP5 exists to test and it needs the §5.1 artifacts.
Colombia's §3.5 arm is also unrun. And all three products are **modelled** surfaces over much of the
same census input, so their agreement bounds *method* sensitivity, not the truth of where people are.

**Three traps worth carrying forward.** (1) `rasterio.merge.merge(srcs, bounds=…)` derives its
transform from the requested bounds and resamples — on population **counts** a 0.54-px offset moves
people; paste tiles at integer offsets instead. (2) The staged CHIRPS window was cut to WorldPop's
*clipped* extent, so unclipped products index three columns west of it and NumPy wraps the negative
index — Jaffna silently gets east-coast rainfall. Asserted, dropped, renormalised, error bounded at
4.3e-4 mm/wk. (3) **RH is the only column that is not bit-reproducible across environments** — 1.65e-5
pp (2.2 float32 ULP) against the frozen twin, because it alone passes through `exp()` in float32,
while the three temperature columns reproduce to 1e-14. Immaterial, but a re-run on a different
NumPy/libm build will not match byte-for-byte and the acceptance test must encode that rather than
fail mysteriously.

---

## 2026-08-13 (c) — Plan §3.2 and Figure F2 are done; they were never blocked, and one memo claim narrows

**`DIRECTION` — half of a "blocked" item was not blocked.** `notebooks_wp45/README.md` listed
`wp5_03` as waiting on the fitted model. That conflated the plan's **§3.2** (*how far does the
exposure move when only its construction changes?*) with its **§3.3** (*does the decision move?*).
Only the second needs a model. §3.2 needs the three frozen exposure tables, which are on this
machine. `notebooks_wp45/wp5_03_exposure_contrast_and_F2.ipynb` is executed, 15/15 QC, and produces
**`Manuscript_Figures/wp5/WP5_F2_exposure_contrast.{pdf,png}`** and the per-district deliverable
`wp5_exposure_contrast_srilanka_v1.csv`. The remaining WP5 half is renamed `wp5_05` and stays blocked
on the §5.1 artifacts. **Worth generalising: before recording an item as blocked, check whether the
blocker applies to all of it.**

**`DELIVERABLE` — Figure F2, six panels, double column.** Three choropleths (precipitation A′→B,
temperature A′→B, temperature B→C) over the shape of the effect (which temperature statistic each
rung moves), the wet-week tail, and the B→C decomposition. Style block ported verbatim from
`notebooks/08_figures.ipynb` so the figure set cannot drift.

**`DELIVERABLE` — what §3.2 establishes.** Over 10,842 district-weeks:

| contrast | mean \|Δ\| |
|---|---|
| precipitation, mask step (`all_touched` → fractional) | 0.76 mm/wk (**1.8%**) |
| precipitation, **A′→B population weighting** | 3.40 mm/wk (**7.9%**) |
| temperature A′→B, weekly **mean** | 0.205 °C |
| temperature A′→B, weekly **maximum** | **0.387 °C** |
| temperature **B→C**, all three statistics | 0.306 °C |

- **The honest-null clause (§3.4) fires on neither variable.**
- **Exposure construction is not a property of a district.** Rainfall and temperature share **one**
  district in their top-five movers, and the rank correlation of absolute displacements is
  indistinguishable from zero (ρ = 0.24, p = 0.23). **A single-variable sensitivity check will
  misidentify which districts are exposed to the choice** — this is new, and it constrains how the
  paper is allowed to summarise WP5.
- **The two rungs act on different parts of the distribution.** Population weighting moves the weekly
  maximum ~2× the mean; the lapse correction moves min/mean/max identically, being one offset.
- **Only 0.169 of B→C's 0.306 °C is MAUP-attributable**; the rest is the orography deficit, which
  applies under area weighting too. Restated here because it is the easiest number in WP5 to overclaim.
- **In the wettest 1% of district-weeks the rainfall contrast is 12.9 mm (4.9%)** — it grows in
  millimetres and shrinks in percent as weeks get wetter.

**`DECISION` — the Build C memo's "constant offset" claim is narrowed to temperature.** PR #1 comment
`5287452143` stated Build C is a constant per-district offset for `t2m` **and** `d2m`. Tested against
the exact −Γ·Δz prediction rather than against zero variance: `t2m` holds to **6×10⁻⁷ °C**; `d2m`
departs by up to **0.46 °C** (Nuwara Eliya) and varies week to week, because the physically necessary
saturation guard `td = min(td − Γ_td·Δz, t − Γ_t·Δz)` binds in some hours and not others, in three
highland districts. `wp5_04` §9 is amended (markdown only; the cell below it only ever tested `t2m`).
**The consequence runs the useful way:** a district-relative *temperature* model still absorbs Build C
exactly, but a model carrying **dewpoint or humidity** sees a residual no district effect can absorb.
**Lesson worth keeping: the assertion that travelled furthest was the half that was never tested.**

**`OPEN` — a second question belongs with the §5.1 ask: which model form do those artifacts use?**
The answer decides in advance what §3.3 can find. If the reference model is district-relative, Build C
can only return a null there, and that null would be a property of the parameterisation rather than of
terrain. Better established before the re-run than explained after it.

**`DECISION` — precipitation gets no Build C rung, and that is a property of the data.** CHIRPS is
observational (cold-cloud duration calibrated to gauges), not a reanalysis carrying an internal
orography that disagrees with the real one, so there is no "elevation the product believes" to correct
against. The physical analogue would be an orographic-enhancement *model*, which the no-new-model rule
bars. Recorded so it is not later read as an unfinished rung.

---

## 2026-08-13 (b) — Build C validated against station observations; the §10 rate caveat was wrong-signed

**`DELIVERABLE` — the Build C correction is confirmed by independent ground truth.** GHCN-Daily has
six Sri Lankan stations reporting TMAX/TMIN through 2025, one of them **Nuwara Eliya at 1,880 m**
(`CE000434730`, GSN, record from 1869), the rest at 1.8–116 m. Free, anonymous, no account. Compared
like with like — ERA5 daily (max+min)/2 on **local** days (UTC+5:30), QC-flagged station values
dropped:

| | station obs | ERA5 0.25° | ERA5 bias |
|---|---|---|---|
| Nuwara Eliya (1,880 m) | 16.40 °C | 21.17 °C | **+4.77 °C** |
| four lowland stations (1.8–116 m) | 27.9–28.7 °C | | **−0.36 to −0.42 °C** |

**ERA5 is accurate at sea level and ~5 °C too warm in the highlands** — an elevation-dependent error,
exactly the thing Build C models, not a global offset. The highland bias is present in **every year
2018–2025** (+4.34 to +4.99) and in **both TMAX (+4.27) and TMIN (+5.27)**.

**`DELIVERABLE` — the district-level number lands within 0.15 °C of ground truth.** Regressing the
five well-sampled stations' observed temperature on elevation gives **6.40 °C/km**, and interpolating
to Nuwara Eliya district's population-weighted elevation (1,260 m, so interpolation, not
extrapolation) implies a true mean of **19.82 °C**:

- **Build B: 21.89 °C — error +2.07 °C**
- **Build C: 19.98 °C — error +0.15 °C**

**Build C removes 93% of Build B's error at the district where the correction is largest.** The
−1.92 °C shift is real and, if anything, slightly conservative.

**`DECISION` — the 2026-08-13 §10 caveat "this bias does not run toward the null; scale by ~0.90" is
withdrawn.** It rested on the MODIS night-LST estimate (5.84 °C/km), which was the weakest of the
available estimates — a *surface* temperature, regressed *between* districts, confounded by land
cover. Two better estimates now bracket it: station **air** temperature vs elevation **6.40 °C/km**,
and ERA5's own between-cell lapse over land cells **6.31 °C/km** (internal to the reanalysis, no
station involved). **The 6.5 °C/km used is well chosen — within ~2% of both — so no rescaling is
warranted**, and Build C's magnitudes should not be discounted. A correction has been posted to PR #1,
where the withdrawn version was sent.

**`OPEN` — what the station check does *not* license.** The high end of the station regression rests
on **one** station: the other four sit below 120 m. And the larger TMIN bias (+5.27) than TMAX
(+4.27) is the signature of **nocturnal cold-air pooling** in a highland basin — a local siting effect
that must *not* be extrapolated to the district's whole population, and the likely reason the raw
station-versus-ERA5 gap implies a steeper rate (~7.8 °C/km) than the clean regression does. So: the
rate stays at 6.5, the sign and magnitude of Build C are confirmed, and no *finer-grained* claim
about individual highland districts rests on this. It also remains true that a 0.1° rebuild would
anchor the correction to a less-smoothed orography.

---

## 2026-08-13 — Build C is built; WP5's exposure ladder is complete, and the plan's ranking of its rungs inverts

**`DELIVERABLE` — `notebooks_wp45/wp5_04_build_c_lapse_corrected_temperature.ipynb`, executed.**
Lapse-rate–corrected temperature exposure on the v2 schema — 10,842 rows, four arms (`a_frac`,
`b_pop`, `c_frac`, `c_pop`), row-aligned to Builds A′/B, all QC green. Quarantined as
`wp5_buildC_temp_exposure_srilanka_v1.csv` (sha `b7bf6ac8e99274ca`). **With this, WP5's A→B→C ladder
locked on 2026-07-07 is complete for Sri Lanka**, and the remaining WP5 work is the decision half,
blocked on the same §8 artifact as WP4.

**`DECISION` — Build C was never actually blocked, and the README said it was.** The missing half of
any lapse correction is the elevation the *model* believes, and ERA5's surface geopotential sits in
the same open ARCO-ERA5 store as `t2m`/`d2m` — `scripts/srilanka_era5_window_reader_v1.py` reads it
unchanged, no CDS key, invariant asserted at 0.0 across hours and across 2018 vs 2023. Correcting to
a DEM *without* it would have been the natural error: it silently assumes ERA5 sits at the true mean
elevation, which is precisely the assumption that fails in the highlands.

**`DIRECTION` — the rung the plan ranked last moves exposure ~1.5× as far as the rung it ranked
first.** Measured: mean |A′→B| **0.205 °C**, mean |B→C| **0.306 °C**; largest **Nuwara Eliya
−1.92 °C**, **Badulla −1.33 °C**, **Ratnapura +1.01 °C**. `wp5_00`'s "Build C worth ≤0.36 °C, lowest
rung, set its acceptance target at a few tenths of a degree" was computed at **0.1°**, where Build B
already captured 91.7% of the elevation displacement. The target was right; the *ranking* was not.
**What Build C recovers is exactly what a coarse grid loses, so its value grows as the grid coarsens**
— at 0.25° Build B reaches only 65.3%. Build C is therefore the one rung that partially repairs the
missing CDS key rather than being degraded by it. The physical statement is one number: ERA5's
orography over Sri Lanka peaks at **1,219 m** against a real 2,524 m, so the reanalysis issues 2 m
temperature for a mountain range roughly half the true height — over exactly the populations sitting
nearest *Aedes*' lower thermal bound.

**`DECISION` — B→C must not be reported as a MAUP effect; the notebook decomposes it.** Mean
|orography deficit| **0.223 °C** (present under area weighting too — an exposure-*quality* correction)
against **0.169 °C** of genuine sub-grid population placement, the only part belonging to WP5's
exposure-*construction* argument. The two can oppose: Nuwara Eliya is −2.26 and +0.34 °C, so almost
none of its headline −1.9 °C is MAUP. Quoting the combined figure as MAUP would overstate WP5 by
about half.

**`OPEN` — a structural result that constrains the blocked decision re-run before it happens.** For
`t2m` and `d2m` the correction carries no time index, so **Build C is Build B plus a constant
per-district offset** (within-district sd across 417 weeks < 2e-6 °C, asserted). A model on
district-relative temperature — anomalies, district fixed effects, per-district standardisation —
absorbs it exactly and **Build C cannot flip a single alert**; a model on absolute temperature or a
fixed thermal threshold sees the full ~2 °C. **A Build C null must therefore not be read as "terrain
does not matter"**; it may only mean the model was district-relative. RH survives (nonlinear,
within-district sd up to 0.71 pp) and so do threshold-crossing counts; **DTR does not** — it is
offset-invariant. Which model form the §5.1 artifacts use is now a question worth asking the PI
*with* the ask, not after it.

**`OPEN` — unlike `wp5_02`'s grid substitution, this notebook's bias does not run toward the null.**
The MODIS-anchored sensitivity the plan §3.1b asked for puts Sri Lanka's night-LST lapse rate at
**5.84 °C/km [5.03, 7.70]**, *below* the 6.5 used, so Build C magnitudes should be scaled by ~0.90
for the locally-anchored version (a between-district surface-temperature regression, so a bracket,
not a measurement). The RH shift is likewise bounded by the dewpoint lapse rate, not measured
independently of it: −0.34 pp at vapour-pressure-conserving, −0.23 at the 1.5 °C/km used, 0.00 at
RH-conserving. Report the bracket, never the middle value alone. And every magnitude is anchored to
ERA5's *smoothed* orography — the highland numbers are simultaneously the most striking and the least
trustworthy here, which is the dangerous combination.

**`DELIVERABLE` — the pipeline is verified end to end.** Zeroing the offsets reproduces `wp5_02`'s
frozen Build B twin to **3.6e-15 °C** (RH 1.7e-05 pp) through an independent code path, and the
rebuilt weight field matches the frozen file to 9.8e-17. Also recorded in the notebook: because the
lapse correction is affine in elevation, per-pair correction of the weighted-*mean* elevation is
**exactly** equal to correcting every 100 m pixel and then aggregating — so plan §3.1b's "fine grid
before aggregation" requirement is met at zero cost. RH is the exception and is recomputed per pair
per hour, never patched onto the aggregate.

---

## 2026-08-12 (b) — WP5 Build B is complete for both variables; the temperature arm is a measured floor

**`DELIVERABLE` — `notebooks_wp45/wp5_02_temperature_exposure_twin.ipynb`, executed.** t2m mean/min/max,
dewpoint and RH on the v2 schema, 10,842 rows, row-aligned with the precipitation twin, all QC green.
RH computed **per cell per hour** (Alduchov–Eskridge Magnus) before any averaging, per plan §E.
Written to quarantine as `wp5_temp_exposure_twin_srilanka_v1.csv` (sha `3dc97795984dda1d`), together
with a **new 0.25° weight field** — `wp5_00` froze 0.05° and 0.1° only.

**`DIRECTION` — with this, WP5's Build B exists for both variables, and the honest-null clause fires
on neither.** Temperature: mean |A′→B| **0.205 °C**, district range **−0.86 °C (Badulla) to +0.34 °C
(Colombo)**, max district-week **1.16 °C**; RH mean |0.77| pp, max 6.3. **Extremes move roughly twice
as much as means** — weekly `t2m_max` shifts by mean |0.387| °C and up to **2.76 °C** — which matters
more than the mean for any transmission model driven by thermal limits.

**`DECISION` — the temperature arm is built on ERA5 0.25° (ARCO-ERA5, anonymous), not ERA5-Land 0.1°,
and every number in it is a floor.** No CDS key is available on this machine. The cost was *measured
before building*, from the DEM and WorldPop alone: Build B sees **65.3%** of the displacement at 0.25°
versus **91.7%** at 0.1°; effective cells per district fall from 21.3/11.8 to 5.3/3.6. The bias runs
**toward the null**, so a non-null result is a conservative lower bound — but no claim about *which*
districts warm can rest on it: **Ratnapura retains 6.7%** of its predicted shift. Tagged as a
substitution in `wp5_02_provenance.json`; the notebook rebuilds unchanged on 0.1° if a key arrives.

**`DELIVERABLE` — the first measurement of `wp5_00`'s DEM prediction against a real temperature
field.** Read at face value it looks weak (69% sign agreement); read properly it is strong, because in
a flat district the prediction is ~0.01 °C and its sign is noise. Restricting to districts where the
prediction claims something: **85.7% sign agreement and r = +0.79 above 0.2 °C**, r = **+0.86** above
0.3 °C. **Badulla is confirmed by measurement** (−0.86 observed vs −1.75 predicted at 0.1°). **Kandy
is a genuine disagreement** (+0.58 predicted, −0.29 observed) — the only one among districts with a
substantial prediction, most likely steep terrain averaged away at 0.25°, and recorded rather than
smoothed over.

**`OPEN` — a confounder tested and rejected, and a caveat that survives.** At 0.25° many cells are
part ocean and ERA5 blends in SST where ERA5-Land would not: Mannar, Batticaloa and Puttalam draw
~44% of their population-weighted exposure from such cells (island-wide land fraction 0.858). That was
the obvious explanation for the sign disagreements and it is **not** — 0.88 mean land fraction where
signs agree, 0.82 where they don't, both spanning the full range. The blending caveat stands on its
own as a second reason to prefer the 0.1° rebuild; it is not the cause of the disagreement.

**`DECISION` — ERA5 acquisition, like CHIRPS, needs no account.** ARCO-ERA5's `raw/` single-level
files are classic netCDF-3, contiguous int16, so the Sri Lanka rows form one contiguous byte span per
timestep: 24 range requests per file instead of a 50 MB download. The full window — 70,128 hours × 2
variables — staged in ~40 minutes and ~8 MB/year. The reader and stager are committed at
`scripts/srilanka_era5_window_reader_v1.py` and `scripts/srilanka_era5_stage_window_v1.py`; the
header parser is validated to **0.0 difference** against xarray. Also recorded: ERA5 packs t2m and d2m with
*independent* scale factors, so at saturation dewpoint can exceed temperature by ~0.004 K in 0.018% of
cell-hours — quantisation, not a decoding fault; bounded, clipped and documented rather than asserted
away.

---

## 2026-08-12 — WP5's precipitation twin is built; WP4 is blocked for the §8 reason; Build A is not here

**`DELIVERABLE` — `notebooks_wp45/wp5_01_precipitation_exposure_twin.ipynb`, executed.** A
population-weighted (Build B) precipitation exposure table for Sri Lanka, 2018–2025, on the v2
boundary-resolved schema — **10,842 rows = 417 ISO weeks × 26 RDHS**, all full 7-day spans including
the six that cross a year boundary, all QC green. Written to gitignored quarantine as
`wp5_precip_exposure_twin_srilanka_v1.csv` (sha `fe46af09328ccaba`).

**`DIRECTION` — WP5's honest-null clause (§3.4) does not fire on precipitation either.** wp5_00
pre-empted it for temperature by prediction; this measures it for rainfall. The A′→B displacement
averages **−0.75 mm/week**, mean absolute **3.40 mm/week ≈ 7.9% of mean weekly rainfall**, largest
single district-week **72.6 mm**. In the wet tail where alerts fire it grows absolutely and shrinks
relatively: p90+ 8.6 mm (5.4%), p99+ 12.9 mm (4.9%). The A′/B correlation is 0.9935 and is *not*
reassurance — the table is dominated by dry weeks. The sign is geographic: **Colombo −7.30 mm/week,
Puttalam +4.37**, 15 districts down and 11 up. Splitting the gap into its two steps,
`all_touched`→fractional-area moves **1.8%** and area→population moves **7.9%** — **the construction
choice that matters is what you weight by, not which cells you admit.**

**`DECISION` — both arms rebuilt from one staged stack, because the frozen Build A is not on this
machine.** `rdhs_weekly_climate_exposure_2018_2025_v2_boundary_resolved.csv` (sha `3900082b…`) and
the ~9.8 GB ERA5/CHIRPS quarantine behind it live under `~/data_quarantine/geomatics/`, which does
not exist here; `wp5_00`'s provenance records that sha but **transcribed it from the build report**
rather than computing it. Rebuilding both arms is the stronger design anyway — they then share
inputs by construction, not by assumption — and a third column `a_alltouched` emulates the frozen
mask so the gap decomposes and a validation target exists if the frozen table arrives. **This is a
fourth absent collaborator artifact and belongs in the §5.1 ask.**

**`DECISION` — CHIRPS acquisition supersedes plan §D.** The plan specifies per-day global GeoTIFFs
(~31 GB for this window; the 2026-06 build pulled ~9.8 GB). The yearly netCDFs are netCDF-4/HDF5
chunked `(20, 112, 400)`, and Sri Lanka touches only 2×2 spatial chunks, so an HTTP range read pulls
a year of the window in 8–19 s. Whole stack ≈ 2 minutes, ~50 MB cached, no account. Adopted; §D's
bulk route is retained only as the description of how the frozen table was built.

**`DIRECTION` — WP4 cannot be completed either, and for the §8 reason.** `instruction_m6.md`
corrected "WP4 complete" to *fold design complete until models are evaluated under the folds*.
Evaluating under folds requires each model's **design matrix**; the repo holds **predictions only**
(`ALT_STATS/frozen/srilanka_matched_pairs.csv`). M6 alone could be re-fit — we own its features and
labels — but a spatially-CV'd M6 against a temporally-split M5 is an artifact, not a comparison, and
publishing it would oblige the same treatment for M0/M1/M2/M5. Recorded as blocked rather than
worked around. **Consequence: the §5.1 ask now unblocks three items — §4, §8 and WP4 — not two.**

**`OPEN` — the temperature arm is where the larger effect was predicted** (−1.75 °C to +0.83 °C) and
it needs a free CDS API key that is not on this machine. The decision half of WP5 — whether the
measured displacement *flips an alert* — remains blocked on the same missing model.

---

## 2026-08-11 — Paper 1 is being finalised without geomatics; §24 items 5 and 6 delivered

**`DIRECTION` — M6/WP4/WP5 are firewalled out of Paper 1, and that is a gate consequence, not a
rejection.** PR **#8** (`agent/v44-hybrid-light-decision-framework`, `26e1fb5`, 2026-08-10) proposes
a hybrid-light decision-theoretic v44 candidate whose `FINAL_CANONICAL_DECISION.md` states that
M6/WP4/WP5 *"remain separate and outside Paper 1 evidence."* Read against
`SOURCE_MANUSCRIPT_RESOLUTION.md` (§9: a token scan of `manuscript_v44/revised_manuscript.tex`
finds `M6`=0, `WP4`=0, `WP5`=0) and the pass's own restrictions (*"no M6/WP4/WP5 promotion"*), the
firewall is a **scope restriction of a formalisation-only task**, applied because
`instruction_m6.md` §22's gates are unresolved — not a scientific decision to drop the workstream.
It does **not** contradict the PI's 2026-08-07 comment on PR #1 approving geomatics inclusion in
the v44 reframe; the PI approved inclusion in principle, and §24 item 15 admits it only after the
gates pass. In the candidate, $\Delta V_G$ (incremental geomatics value) and the spatial-exposure
operator $\mathcal A_w$ survive as **framework notation marked PENDING / NOT ESTIMATED**, which is
the correct placeholder.

**`OPEN` — the real risk is timing, not exclusion.** `V44_VS_BIOMATH_DECISION_MEMO.md` states *"no
further analysis is required to submit either way; the open blockers are author-owned"* (ethics,
ORCIDs, DOI, OpenDengue record id). Paper 1 can therefore be submitted at any time. Whether the
geomatics work lands in Paper 1 or becomes Paper 2 is decided by whether the §22 gates close before
that submission — and three of them are blocked on inputs the Geospatial Lead cannot supply
(original threshold artifact, M0/M1/M2 predictions, a CDS key). Raised to the PI, not assumed.

**`DELIVERABLE` — §24 item 5, `analysis/geomatics_integration_v1/M6_FEATURE_CHRONOLOGY.md`.**
Verdict: **no formal pre-outcome feature lock existed**, and none is manufactured — §5's prescribed
wording is adopted verbatim and `M6_CORE_FEATURE_LOCK.yaml` is deliberately **not** created. Two
commit-provable facts bound how post-hoc the result is: the **A/B/C/D feature specification was
committed 2026-07-17** (`baebaf7`), three weeks before first outcome access; and the **reduction to
A/B/C was logged 2026-08-05**, one day *before* first outcome access — so the narrowing was not a
response to performance. First outcome access = notebook 05; first fit = notebook 06 (2026-08-07
13:43); the freeze manifest was written at 21:30, *after* performance was seen. All four deviations
from the spec (Batch D absent, #16 partial, land-cover product substitution, §9.5 gate abandoned)
predate outcome access. **Feature definitions changed after outcome access: none** — verified
cell-by-cell against the `ff6287d` blobs, not asserted. Three limits keep it short of a lock:
notebooks 04–08 entered git in one post-fit commit, so the separation rests on notebook-written
provenance rather than commit boundaries; the analyst had prior access to the study's own outcomes
throughout; and 19.2% of the target is itself test-informed.

**`DECISION` — post-freeze working-tree edits to notebooks 00–03 discarded.** The only difference
from the frozen blobs was output noise plus one added `pip install pystac_client` cell in notebook
02 — no code, no feature definition. Kept, they would have silently invalidated the notebook blob
hashes recorded in `M6_CORE_FROZEN_MANIFEST.yaml`. Backed up outside the repo before discarding.

**`DELIVERABLE` — §24 item 6, `docs/MODEL_NOMENCLATURE_REGISTRY_v44.md`** (also satisfies round-3
prompt §5.1). The collision is worse than a name clash: Colombia's pilot **M6 = cases + SPI** is a
*hybrid*, Sri Lanka's **M6 = geomatics-only** is a *standalone with no case history* — opposite in
kind. Rule adopted: **bare `M6`/`M7` must not appear in v44**; nothing historical is renamed;
descriptive names only. Two further traps recorded — `M5-no-climate` (frozen, exists) versus
`M5_NO_GEO` (BLOCKED, does not exist), and Sri Lanka's M1 carrying seasonal harmonics + RDHS fixed
effects where Colombia's M1 does not, so any cross-country "M1" sentence is false without the
qualifier.

**`OPEN` — §24 items 8/9 (matched geomatics estimand) are `BLOCKED`, and the reason is now
established.** `instruction_m6.md` §8 requires `BASE + GEOMATICS` versus `BASE WITHOUT GEOMATICS`
on identical rows with identical machinery. The repo holds only M5 **predictions**
(`ALT_STATS/frozen/srilanka_matched_pairs.csv`: `full_raw`, `noclim_raw`, `full_recal`,
`noclim_recal`) — **no base design matrix**, so the base cannot be refit with a geomatics block
added. Recorded as `MATCHED_GEOMATICS_ABLATION = BLOCKED`, resolvable only by the same Route A ask.

---

## 2026-08-07 (g) — §17 coastal sensitivity: the premise was wrong, and the real problem is elsewhere

**`DELIVERABLE` — `docs/wp5_worldpop_coastal_sensitivity_report_v1.md`**, from
`scripts/wp5_worldpop_coastal_fractional_sensitivity_v1.py` and
`…_coastal_snap_and_exposure_v1.py`. §17's mandatory analysis, executed. Also **`M6_TARGET_PROVENANCE.md`**
(§24 item 3) written, consolidating entries (e) and (f).

**`DECISION` — do NOT adopt fractional weighting for the population layer.** Fractional vs
centre-in-polygon differs by a median **0.007%** of a district's population (max 0.073%), Spearman
rank correlation **1.000000**, **zero rank changes**. A genuine negative result: `wp5_00`'s weight
field needs no rebuild on this account.

**`DIRECTION` — §17 conflates two problems and fractional weighting fixes neither.** The national
shortfall is **1.37%** (`ppp_2020`) and fractional assignment recovers **200 of 292,461 people**.
The missing population is not partially-covered boundary pixels — it lies **wholly outside** every
RDHS polygon, a **median 107 m** beyond the nearest boundary (max 2.1 km). It is a **land-mask
mismatch**: WorldPop's coastline runs seaward of the RDHS coastline. The remedy is a
**nearest-district snap**, which restores capture to **100.0000%**, not area weighting.

**`DECISION` — the §17 gate is met for exposure, NOT met for denominators.**
- **Exposure: negligible.** Snapping moves population-weighted temperature by at most **0.0115 °C**
  (Matara), median 0.0000 °C — about **150× smaller** than Build B's −1.75/+0.83 °C displacement.
  The orphaned population sits at the same near-sea-level elevation as the coastal population
  already inside the polygon. The coastal shortfall **may now be described as negligible for WP5
  exposure**, which is what §17 required before that wording could be used.
- **Denominators: material and concentrated.** Snapping adds **+9.17% to Batticaloa**, +4.80%
  Puttalam, +3.57% Jaffna, +3.54% Galle (median across 26 units: +0.015%). Within-unit
  normalisation does **not** absorb this, because a denominator scales the whole series.

**`OPEN` — a cross-link to the label work.** The M6 threshold is a fixed *incidence*, so a 9%
denominator error would shift the affected districts' thresholds. The threshold recovery used
**R2025A**, whose shortfall is **0.10%** against `ppp`'s 1.37% — 13× smaller — so the exposure is
limited. But if the **frozen** incidence denominators were built centre-in-polygon on `ppp`, up to
5 coastal districts carry incidence biased high by several percent. Needs the original denominator
build to settle; raised as a targeted question, not a claim.

**Note:** §18 (`all_touched` vs fractional on the coarse ERA5-Land grid, ~31% of weight misplaced)
is a **different** finding at a different support and remains open. Nothing here supersedes it.

---

## 2026-08-07 (e) — governance instructions received; M6 renamed M6-core and frozen

**`DIRECTION` — `instruction_m6.md` arrived from Ganesh Shiwakoti** (26 sections, commit `8de3018`,
2026-08-07 16:58 EDT). It sits on `upstream/agent/instruction-m6-next-actions` — **not on `main`,
not on PR #1** — and that branch is `ff6287d` plus this one file. Governing instruction: *"The goal
is not to make M6 look successful. The goal is to make every geomatics conclusion defensible."*
**Nothing goes into manuscript v44 until §22's checklist is resolved item by item.**

**Three of the PI note's four asks are answered.** §5.1 M6 framing — signed off as an exploratory
null, with §23 supplying the conclusion wording. §5.2 §10 contrasts — ruled: recover M0/M1/M2 on
the identical rows, or file a formal deviation; *"do not silently rewrite the original question
after seeing M6 performance."* §5.3 WP4 radius — ratify **before** viewing performance under
competing radii, then freeze. **§5.4 (CDS key) is unanswered** — treat as self-service.

**`DIRECTION` — three entries below this one are now overstated.**
- **WP4 is not complete** (§14). It is *fold design and spatial-range analysis* complete until models
  are trained and evaluated under the held-out folds. Supersedes the 08-07 (c)/(d) framing.
- **WP5 is not only waiting on climate** (§17). The WorldPop coastal fractional-overlap sensitivity
  is **mandatory** — per-unit `ΔX_i = X_frac − X_centre`, medians, maxima, rank correlation, most
  affected units — before the 3.5% shortfall may be called negligible.
- **The threshold recovery is not the clean close** that 08-07 (b) claims. See below.

**`DECISION` — the executed model is `M6-core (A/B/C)`, not the 16-variable M6** (§2 audit executed).
12 of 16 planned variables are present; **#13 mobility, #14 wealth, #15 healthcare access are fully
absent**. #16 cropland is *partial and incidental*: `frac_crops` is one of seven Impact Observatory
`io-lulc-annual-v02` class fractions co-extracted wholesale by notebook 03 (Batch B), the product
differs from §6.16's ESA WorldCover, and the EVI **phenology amplitude** half was never built. The
design matrix is 92 features, L2 only, **no selection step, 0 zero coefficients**, so candidate set =
design matrix = fitted set. Detail: `analysis/geomatics_integration_v1/M6_BATCH_D_AUDIT.md`,
manifest `M6_CORE_FEATURE_MANIFEST.yaml`, generator `scripts/m6_batchD_feature_audit_v1.py`.

**`OPEN` — the null is narrower than "geomatics", and §7's language rule should say so.** The three
missing variables are mobility, wealth and healthcare access — the ones most plausibly tied to human
exposure and to *reporting* behaviour. AUC 0.601 is a null for terrain, land cover and RS dynamics.
Proposed as an addition to §7's allowed/not-allowed list.

**`DELIVERABLE` — M6-core frozen** (§6): `M6_CORE_FROZEN_MANIFEST.yaml`, generator
`scripts/m6_core_freeze_manifest_v1.py`. Notebook blob hashes at `ff6287d`, row counts, test
row-key hash `9db1c932d37a63be`, model config, calibration, bootstrap seed/B, MODIS gap rule,
input/output/figure hashes, headline numbers. No future result may overwrite it.

**`OPEN` — two provenance gaps found while freezing, both previously unrecorded.**
1. **The threshold generator is not committed.** `m6_label_thresholds_srilanka_v1.csv` defines the
   model *target*, but no committed code produces it — notebook 06 only consumes it via
   `THRESHOLDS_CSV`, and notebook 05 stopped before constructing a label. The WorldPop year-ratio
   recovery ran as ad-hoc session code. This trips §25's stop condition on establishing which
   artifact produced a number, for the target itself. **Fix: port it into 05 or `scripts/` and
   confirm the hash.**
2. `nb05_provenance.json` still reads *"STOPPED … label NOT constructed"*, predating the recovery.
   Its rowset hash is still correct.

**`OPEN` — §3's target-provenance concern is real, and now has a number.** The chain
`test labels → feasible interval → selected threshold → training labels → M6 fit` applies to the
**40 of 208 district-years clamped to the frozen-outcome interval** — 5 districts (Killinochchi,
Matara, Polonnaruwa, Puttalam, Ratnapura), all 8 years each. That is **755 of 3,926 test rows
(19.2%) and 200 of 1,321 events** resting on a threshold chosen using the test outcomes. The other
168 district-years are the empirical train q75 and are unaffected. Status recorded as
`EXPLORATORY_RECONSTRUCTED_TARGET` pending Route A/B recovery.

**Next:** §24 items 3–4 (target-provenance report + attempt recovery of the original frozen
threshold/training artifact). Two external asks issued in parallel: the original threshold table
and v2.0 training artifact from the team, and self-service CDS registration.

---

## 2026-08-07 (f) — the threshold generator port is BLOCKED: half of it will not reproduce

**`DELIVERABLE` — `scripts/m6_threshold_recovery_v1.py`**, the port attempted in (e). It verifies
and **writes nothing** — the frozen CSV stays the sole source of the target, so no competing
threshold table can be mistaken for it.

**`DECISION` — reported BLOCKED per §25 rather than searched further.** The result splits cleanly:

- **The feasible-interval solver and clamp rule RECOVER EXACTLY.** 26/26 districts admit a
  non-empty interval; all 26 frozen `K` lie inside the interval their own labels imply; all **5
  clamped districts sit on the lower bound to within 1e-12**. Asserted in the script, so it is a
  permanent regression test.
- **The empirical q75 half does NOT recover.** Best **10 of 21** districts across
  {2 year bases} × {6 train row-set definitions} × {5 interpolation modes}.

**Why the search was halted.** The diagnostic is decisive, not merely negative: `K` is an **exact
observed train ratio in 21/21 districts**, at quantile level **0.733–0.765** — so the method is
confirmed to be the empirical ~75th percentile of train `cases/WorldPop`. But `K` sits at a
**varying rank (187–195 of 255)** where a fixed quantile rule on this series must give a fixed
rank. That points to a train row set differing from any recoverable here by a few rows, not to a
different formula. Continuing to enumerate definitions until one matched is precisely the
improvisation §25 forbids, and would manufacture a false provenance.

**`OPEN` — the irony is worth stating to the PI.** The **19.2% of test rows that are test-informed
are fully reproducible**; the **80.8% that are train-only are not**. The half of the target with a
provenance problem is the half whose construction we can verify.

**Consequence:** **Route A is now the only clean resolution** — the original threshold artifact, or
the original frozen training panel that would let Route B recompute the quantile on the right rows.
Until one arrives, `EXPLORATORY_RECONSTRUCTED_TARGET` stands and M6-core cannot be described as
reproducible end-to-end. This does **not** disturb the M6 result itself: the frozen thresholds are
unchanged, and notebook 06's acceptance test still passes 3,926/3,926. What is lost is the ability
to regenerate the target from committed code.

---

## 2026-08-07 (d) — WP4 §4.1: no residual spatial autocorrelation; PI note issued

**`DELIVERABLE` — `notebooks_wp45/wp4_01_autocorrelation_range.ipynb`, executed.** Moran's I per week
across the 151 test weeks (26 districts each), permutation-tested (999 shuffles, seed 20260612), plus
an empirical variogram, on raw residuals of M5-full, M5-no-climate and M6.

**`DECISION` — the range is effectively zero, so the buffered scheme is cheap.** Moran's I is
indistinguishable from its null at **every** distance band for all three models (permutation
p 0.53–0.99); the variogram is flat 25–400 km. Selected radius: the **minimum buffer** (drop
immediately-adjacent districts), retaining **21 of 25** training districts in the median fold and 16
in the worst — against 9 and 5 at 100 km. The reviewer concern motivating WP4 is answered directly
rather than by an expensive scheme.

**Why this is not an artifact.** M5 carries district fixed effects, which absorb time-invariant
spatial structure, so a near-zero residual Moran's I could be a property of the model. **M6 carries
no fixed effects** (`M6.md` §0) and returns the same answer — I = 0.001 among adjacent districts,
p = 0.99. Honest bound: with 26 units the permutation null has sd ≈ 0.02, so this rules out residual
correlation above roughly |I| = 0.04; it does not prove zero.

**`OPEN` — first estimate only.** §4.1 specifies the *reference* model's residuals; M5-full as frozen
is the closest available here. Re-run if the registered reference model differs — only the residual
column changes.

**`DELIVERABLE` — PI note issued:** `docs/pi_note_2026_08_07_srilanka_status_and_decisions.md`.
Carries the M6 honest null, the WP5 1.8 °C exposure finding, this WP4 result, and **four decisions
requested**: (1) M6 framing sign-off; (2) a ruling on §10's contrast set, which cannot be answered as
registered because M0/M1/M2 predictions do not exist on these rows; (3) confirmation of the WP4
buffer radius; (4) a free CDS API key so ERA5-Land can be staged for Build B.

---

## 2026-08-07 (c) — WP4 fold geometry built: the power caveat is now a curve

**`DELIVERABLE` — `notebooks_wp45/wp4_00_loocv_folds_and_power.ipynb`, executed.** §4.2's buffered
LOOCV built as a **function of buffer radius**, so when §4.1 returns the autocorrelation range it
selects a row from a table that already exists. Adjacency re-derived and checked against notebook
00 (26 nodes / 60 edges, connected). 260 fold definitions frozen to `data_quarantine/wp4_cv/`.

**`DECISION` — distance is boundary-to-boundary, not centroid-to-centroid.** Adjacent districts here
sit **28–119 km** apart by centroid while sharing a border, so a centroid buffer would be wildly
uneven across the island. Boundary distance in the equal-area CRS is the primary; centroids reported
for visibility only.

**`DELIVERABLE` — §4.6's power caveat is quantified.** Training districts available, of 25:

| buffer | median fold | worst fold | median train district-weeks | degenerate folds |
|---|---|---|---|---|
| adjacency only | 21 | 16 | 5,481 | 0 |
| 25 km | 19 | 14 | 4,959 | 0 |
| 50 km | 15 | 10 | 4,045 | 0 |
| 75 km | 12 | 6 | 3,132 | 0 |
| 100 km | 9 | 5 | 2,349 | 0 |
| 150 km | 5 | 0 | 1,435 | **12** |

Sri Lanka is ~430 km end to end, so a buffer is a large fraction of the country by construction. At
100 km the median fold trains on 9 of 25 districts, the worst on 5; at 150 km the scheme collapses.
**This is the number to put to the PI** — §4.6's "low-powered even with LOOCV" was previously an
assertion.

**`DECISION` — hop and kilometre buffers are NOT interchangeable.** One hop removes 2–7 districts
depending on position, so it applies an uneven buffer while looking uniform. Kilometre buffers are
the defensible primary; hops reported because the plan mentions them.

**`DELIVERABLE` — §4.4 spatial leakage audit passes.** Zero train/test pairs within the buffer, every
radius, every fold, asserted rather than assumed. Temporal leakage is enforced upstream in M6
notebook 04; the two constraints are orthogonal and together make the scheme spatio-temporal.

**`OPEN` — the operative radius (§4.1).** Needs an empirical variogram or Moran's I decay on model
residuals. M6's predictions now exist on the 3,926 test rows so a first estimate is available
immediately; the registered version should use the reference model's residuals. Per §4.6 this stays
the **compact-country companion** — the well-powered claim rests on Colombia's block CV (§4.3), out
of scope while the work is Sri Lanka-only.

---

## 2026-08-07 (b) — M6 is FITTED AND SCORED: thresholds recovered exactly, honest null confirmed

**`DELIVERABLE` — the label thresholds are recovered to the last row.** Route 3 of the 08-07 entry,
executed. WorldPop **G2 R2025A constrained** 2018–2025 pulled (public, no account) and zonal-summed
per RDHS. Confirmation the release is identical to the frozen build's: computed 2024 national
**23,008,641** against the build report's *"raw WorldPop was 23,008,642"* — one person apart.

Method: the threshold is a fixed incidence, so in count space it scales with population,
`thr_count(d,y) = K(d) × WP(d,y)`. Solving the frozen test outcomes for a feasible `K(d)` gives
**26 of 26 districts a non-empty interval** — 78 constraints satisfied by 26 free parameters, which
is not trivially satisfiable and is itself the validation. `K` is set to the empirical 75th
percentile of train `cases/WP` where that lands inside the interval (21 of 26) and clamped to the
interval otherwise (5 of 26, where this repo's train rows differ slightly — the lost 2018 wk4 plus
their `exposure_missing_flag` filter). **This sidesteps the 08-07 open item entirely: the recovered
thresholds are the values actually used, not a re-execution of the procedure.**

Frozen to `m6_label_thresholds_srilanka_v1.csv` (208 rows = 26 × 8 years) and
`m6_worldpop_r2025a_by_district_year.csv`.

**`DECISION` — acceptance test passes exactly: 3,926 / 3,926 = 1.000000** against the frozen
outcomes; reconstructed test prevalence **0.3365** with **1,321** events, matching
`PAIRED_ROW_AUDIT.md` exactly. Notebook 06 asserts this before fitting, so the gate is permanent.

**`DELIVERABLE` — notebooks 06, 07, 08 re-run non-provisionally.** `quotable: true`. Superseded
`_PROVISIONAL` artifacts deleted so a stale figure cannot be picked up later.

**`RESULT` — the honest null, on identical rows.** M6 (geomatics-only) on the 3,926 frozen test rows,
raw predictions, RDHS cluster bootstrap B=1000 seed 20260612:

| model | AUC [95% CI] | PR-AUC | Brier | NB@0.30 [95% CI] |
|---|---|---|---|---|
| **M6 (geomatics only)** | **0.601 [0.568, 0.638]** | 0.442 | 0.223 | **0.058 [0.033, 0.085]** |
| M5 full hybrid | 0.771 [0.741, 0.804] | 0.667 | 0.180 | 0.145 [0.106, 0.184] |
| M5 no-climate | 0.751 [0.721, 0.782] | 0.652 | 0.191 | 0.135 [0.100, 0.176] |

- ΔAUC(M6 − M5full) **−0.170 [−0.203, −0.135]**; ΔNB **−0.087 [−0.112, −0.062]**
- ΔAUC(M6 − M5noclim) **−0.150 [−0.182, −0.115]**; ΔNB **−0.078 [−0.104, −0.054]**
- Fraction of bootstrap replicates favouring M6: **0.000** in all four contrasts.

M6's NB (0.058) barely exceeds treat-all (0.052). Per the pre-specified §10 rules this is the
**expected honest null**: a purely spatial landscape model carries little standalone decision value,
which strengthens the paper's caution rather than contradicting it. **No headline changes.**

**`OPEN` — caveats that stand.** (1) Contrasts are against M5-full and M5-no-climate; M0/M1/M2 are
absent, so §10's "beats season / climate-only" remains unanswerable. (2) 11.3% of test rows carry
forward-filled MODIS features from the 2025 gap; the fresh-MODIS subset moves M6 to AUC 0.612 /
NB 0.065 — same conclusion, reported as sensitivity only. (3) M6 is Platt-recalibrated while the
comparators are rolling-52, so the **raw** columns are the primary comparison. (4) Result is
EXPLORATORY per §0 and needs PI framing sign-off before any use.

---

## 2026-08-07 — The M6 label definition is recovered from a committed artifact; the blocker changes shape

**Context.** Searched the repo for any frozen artifact carrying the Sri Lanka label thresholds. Found
something better: the label *construction* itself.

**`DECISION` — the 2026-08-06(d) statement that "the SL analogue of
`colombia_label_construction_v1.py` is not in this repo" was WRONG, and is corrected.** It is
committed at **`analysis/v12_referee_response/run/sl_matched_and_recal.py`** — inside an analysis run
directory rather than `scripts/`, which is why it was missed. Lines 26–30 are the definition:

```python
fut['week_start'] = fut['week_start'] - pd.Timedelta(days=28)          # h = 4 weeks
f['split'] = np.where(f.epi_year <= 2022, 'train', 'test')
g = f[f.split=='train'].groupby('geometry_id')['dengue_incidence_per_100k']
f = f.merge(g.quantile(0.75).rename('thr75').reset_index(), ...)
f['y'] = (f['inc_future'] > f['thr75']).astype(int)
```

**`DECISION` — the 1.7% residual in notebook 05 is fully explained: the label is on INCIDENCE, not
case counts.** `dengue_incidence_per_100k`, thresholded at the per-district 75th percentile of
**train** (`epi_year ≤ 2022`) incidence, strict `>`. Notebook 05 reconstructed on raw counts. Within
a district the population factor nearly cancels — hence 98.3% agreement — but it varies by *year*,
so no single count threshold exists, which is exactly why 3 of 26 districts came back
`CONTRADICTION` under a one-threshold-per-district model.

**`DELIVERABLE` — empirical confirmation.** Re-solving the implied thresholds **per (district,
target-year)** instead of per district takes consistency from **23/26 districts to 75/78
district-years**. The implied year-on-year threshold ratios are **~1.01** (2024/2023 median 1.0115,
2025/2023 median 1.0061) — i.e. plausible population growth, exactly as a count threshold scaling
with the denominator should behave. The rule is confirmed to the last detail.

**`DIRECTION` — the outstanding ask is no longer "26 numbers we cannot derive".** The threshold is a
fixed incidence per district, so `thr_count(d,y) = thr75(d) × pop(d,y) / 1e5` — linear in
population. And the rescale formula `pop_adj(d,y) = Census2024(d) × WP(d,y)/WP(d,2024)`
(`docs/population_denominator_rescaled_build_report.md`) means **the census anchor cancels in year
ratios**. So exact labels need only *one* of:

1. the 208-row denominator table (`…population_denominator_district_rescaled_2018_2025.csv`), or
2. the frozen `dengue_climate_population_linked_2018_2025_v2_date_aligned.csv`, or
3. **the WorldPop G2 R2025A constrained annual series 2018–2025 — a public download**, combined with
   the thresholds already recovered from the frozen outcomes for 2023–2025.

Route 3 needs nothing from a collaborator. That is a materially better position than 08-06(d).

**`OPEN` — one subtlety before claiming exactness.** The train quantile is computed over rows
surviving `outcome_missing_flag==0 & exposure_missing_flag==0 & population_missing_flag==0`. The
**exposure** flag drops district-weeks lacking climate, so the quantile is taken over a row set this
repo cannot fully reconstruct without the climate table. Effect is likely small but must be measured,
not assumed — the acceptance intervals in `m6_implied_thresholds_srilanka_v1.csv` (now extensible to
per-district-year) remain the test.

---

## 2026-08-06 (d) — M6 pushed to its stop rule: outcome restaged, time axis resolved, blocker reduced to 26 numbers

**Context.** Instruction was to complete M6. It cannot be completed here, and the reason is a rule
this project wrote for itself — but the attempt moved the blocker a long way and closed two open
items.

**`DELIVERABLE` — the WER outcome table is restaged from source on this machine.** 415 of 416 issues
harvested (2022 wk44 absent from the archive, as documented), extracted and QC'd: 10,790 rows,
415/415 issues structurally complete at 26 rows, 0 invalid current-week values. Frozen as
**`wer_dengue_currentweek_rdhs_2018_2025_v2.1-refresh.csv`**, SHA256 `0ccde961…`.

**`DECISION` — v2.1 does NOT supersede the v2.0 freeze, and the delta is fully explained.** It is
not byte-identical (59 NA cells vs the documented 33). The 26 extra are one whole issue: **2018
week 4 (`Vol_45_no_04.pdf`) is now served as an image-only PDF with a zero-length text layer**,
where it had extractable text at the 2026-06-10 harvest. OCR is out of scope by standing policy, so
those district-weeks are NA-flagged. They fall in the **training** period, not the test set. The
manuscript's v2.0 freeze (`99f0b9b1…`) is untouched; this is a parallel artifact.

**`DECISION` — `wer_bulk_harvest.py` repaired (bitrot, not logic).** `epid.gov.lk` now returns HTTP
403 to curl's default user-agent and 200 to a browser one, so the harvester silently retrieved an
empty listing and reported "0 downloads" rather than failing. A browser agent is now sent; same
URLs, same parsing, same logic.

**`OPEN` → `DECISION` — the WER issue-number ↔ ISO-week question is settled, empirically.** Logged
open on 2026-08-05 and again in 08-06(b). Measured against the 3,926 frozen labels by sweeping
candidate offsets: **WER issue *N* covers the epidemiological week beginning ISO-Monday(*N*) − 7
days.** Agreement is **98.3%** at that offset against **82.4%** at the nominal one. The horizon is
unchanged at 4 weeks; it is the outcome table's own time axis that is shifted one week from ISO —
the publication lag showing up in the data. **Joining WER to an ISO-Monday spine without this shift
trains every model one week off, and still yields entirely plausible metrics.**

**`DIRECTION` — the panel blocker recorded in 08-06(b) was too pessimistic and is corrected.**
`ALT_STATS/frozen/srilanka_matched_pairs.csv` is committed in this repo and **is** the complete Sri
Lanka test panel: 26 districts × 151 consecutive weeks = 3,926 rows, no subsetting, carrying the
outcome *and* frozen comparator predictions. "Matched pairs" refers to the two *models* being paired
on identical rows, not to observation matching. All 3,926 rows have complete M6 features from
notebook 04 (0 nulls).

**`DELIVERABLE` — `notebooks/05_label_and_row_mask.ipynb`, executed, ending at a STOP.** The label
*rule* is confirmed in form: **23 of 26 districts admit a single threshold that reproduces every
frozen label**, and all 68 residual disagreements sit within a case or two of the threshold (median
gap 1 vs 12 on agreements). So the rule, the join and the case series are right; only the threshold
*values* are unknown. Their per-district acceptance intervals are recovered from the frozen outputs
and frozen to `m6_implied_thresholds_srilanka_v1.csv`.

**`DECISION` — STOP per `M6.md` §11 ("labels/thresholds get recomputed").** No training window ×
percentile-method combination reproduces the thresholds (best 14 of 23). Fitting M6 against a label
that is 98.3% the frozen one, then comparing it to predictions made under the real one, would look
rigorous and would not be — precisely what §0's comparability rule exists to prevent. **The
outstanding ask is now 26 numbers:** the Sri Lanka label/threshold table, or the SL analogue of
`scripts/colombia_label_construction_v1.py`, which is not in this repo. The recovered intervals are
a one-look acceptance test for whoever holds it.

**`OPEN` — §10's contrasts must be restated or supplemented.** The frozen artifact carries **M5-full**
and **M5-no-climate** predictions on the test rows — not M0, M1 or M2 separately. So "does landscape
beat season (M0) or climate-only (M2)" is unanswerable from this repo; "does landscape add against
the full hybrid, and against it stripped of climate" is answerable. Goes to the PI with the framing
sign-off already outstanding.

**`OPEN` — a validation-split decision is owed.** §9.4 says tune `C` on the committed validation
split, but Sri Lanka's design is train/test with past-only rolling-52 recalibration
(`ALT_STATS/PREANALYSIS_ALT_STATS.md` §3), not Colombia's train/val/test with Platt-on-validation.
Carving a validation slice from the tail of training preserves the committed train/test boundary and
is the least-worst option — but it is a documented deviation, not a free choice.

**`DIRECTION` — the 2025 MODIS backfill is now on the critical path, not optional.** The frozen test
panel runs to 2025-11-17, so **442 test rows (11.3%)** fall inside the MODIS gap and carry
forward-filled features. They **cannot be dropped** without breaking identical-rows comparability
(§11). The LP DAAC backfill from 08-06's entry is therefore required for a defensible evaluation.

---

## 2026-08-06 (c) — WP5 Build B started: the weight field is built, and A→B is not a null

**Context.** Deliberate move off M6 (Phase 4, *optional*) onto the plan's **mandated** rungs. M6 is
now blocked on the M1/M2/M5 panel spine, which is someone else's to supply; Phases 1–3 are blocked
on nobody and still had zero code. Sri Lanka only.

**`DIRECTION` — Build B's weight field can be built before any climate data exists.** Builds A and B
differ *only* in `w` — the climate fields are identical — so the weight field is the whole of Build
B. WorldPop and the DEM were already staged locally by M6 notebooks 01/03, so the work is runnable
today and the exposure table becomes a join plus a weighted sum once ERA5-Land and CHIRPS land.
New series `notebooks_wp45/`, kept separate from the M6 `notebooks/` sequence.

**`DELIVERABLE` — `notebooks_wp45/wp5_00_population_weight_field.ipynb`, executed.** Weight tables
for both climate grids (ERA5-Land 965 and CHIRPS 3,044 (district, cell) pairs), plus displacement
and predicted-shift tables, in gitignored `data_quarantine/wp5_exposure/`.

**`DECISION` — the honest-null clause (§3.4) can be pre-empted, and it does not fire.** Using the
staged DEM and the standard lapse rate, population-weighting alone moves district temperature
exposure by **−1.75 °C (Badulla) to +0.83 °C (Ratnapura)**. Badulla's population lives ~270 m
*above* its areal mean elevation — highland towns and tea estates, with the sparsely-settled Uva
basin dragging the area-mean down — so weighting by people *cools* its exposure. For a model whose
transmission terms move steeply over this range, that is not a rounding correction. Precipitation
remains open: CHIRPS is patchy and convective and has no elevation shortcut, so it must wait.

**`DIRECTION` — Build C's acceptance target should be lowered, on evidence.** Build B alone reaches
**92%** of the total elevation displacement at ERA5-Land resolution. The within-cell residual that
Build C's lapse correction would add tops out at ~56 m ≈ **0.36 °C** (Matale), and is not reliably
additive — `corr(|between|,|within|) = 0.33`, same sign in only 65% of districts, and in Badulla the
two carry *opposite* signs, so the residual partly offsets rather than compounds. Build C stays in
scope per 2026-07-07, but its target is a few tenths of a degree, not something comparable to B.
Re-check in Colombia, which spans far more relief.

**`DECISION` — Build A's `all_touched` mask is quantified, without an arbitrary threshold.** Against
fractional overlap, a uniform (`all_touched`) weighting misplaces a median **31%** of a district's
weight (total-variation distance, ERA5-Land). Half of a typical ERA5-Land cell lies outside the
district it is credited to (median `cell_frac` 0.51); for Colombo and Jaffna it is under a third.
This is the mechanism behind whatever A→B divergence the exposure table eventually shows.

**`OPEN` — population-weighting halves the effective spatial support.** A median district's exposure
is drawn from ~12 effective ERA5-Land cells under population weighting against ~21 under area
weighting. This is the *correct* answer to "what weather did these people experience", but it is the
cost side of the trade and belongs in the Methods rather than being discovered at review.

**`DECISION` — a trap recorded before it bites: the two climate grids are not co-aligned.** CHIRPS
ships a GeoTIFF stating its upper-left *edge*; ERA5-Land is distributed on grid *points* at exact
multiples of 0.1°, which are cell *centres*, so its edges sit at 0.05°, 0.15°, … Treating them alike
displaces every person by up to ~5.5 km into the wrong cell, raises nothing, and yields entirely
plausible weights. CHIRPS is verified against a real granule; **ERA5-Land's convention is declared
and flagged `verified=False` — assert it against the first staged granule.** Also confirmed on that
granule: CHIRPS carries **no nodata tag**, so −9999 must be masked explicitly or it enters the
weighted mean as rainfall.

**`OPEN` — the vintage requirement cannot be met, so it is sized instead.** §3.1 requires the
population vintage to match the exposure year; WorldPop UN-adj stops at **2020** against a window
ending 2025. Measured: the weight field moves ~**1.1%** of a typical weight over 2018→2020, so
carrying 2020 forward is a bounded extrapolation. Same resolution as notebook 03's carry-forward
table — report it, don't hide it.

**Still blocked for WP5:** ERA5-Land (free CDS API key) and CHIRPS (open HTTP) acquisition, per
`docs/climate_bulk_acquisition_and_exposure_table_plan.md`. **Next unblocked rung:** WP4 §4.2 fold
geometry — buffered-LOOCV folds and their power cost can be characterised across candidate buffer
radii from the adjacency graph alone; only the *autocorrelation range* that picks the radius needs
model residuals. That is precisely what §4.6 asks be flagged to the PI.

---

## 2026-08-06 (b) — Notebook 04: the epi-week join is built, and the leakage rule is enforced mechanically

**Context.** Sri Lanka only, by request. Batches A, B and C sit on three clocks (one row per
district; 8-day; 16-day) and the model needs one district × epi-week matrix. This is the step where
a leakage bug gets in, so it is the subject of the notebook rather than a line inside it.

**`DELIVERABLE` — `notebooks/04_feature_assembly.ipynb`, executed.** Output
`m6_features_weekly_srilanka_v1.csv` (quarantined): **10,868 rows** (26 districts × 418 weeks,
2018-01-01 → 2025-12-29) × 101 columns — 6 keys, 38 static predictors, 54 dynamic (6 layers ×
lags 0–8), 3 QC. Carries `geometry_id` (`LK11`…) beside `rdhs_id` so notebook 05 can join the
frozen panel.

**`DECISION` — the join keys on `composite_end`, strictly.** A composite is admissible for week *W*
only if it ended **before** *W* began; lag *k* takes the last admissible composite ending before
*W* − 7*k* days (`merge_asof`, `allow_exact_matches=False`). Closes the 2026-08-05 `OPEN` item.
Measured cost of the alternative: the naive start-date join puts future observations inside
**91.4%** of district-weeks, a median of 3 days each. Gap-fill is past-only by construction —
nulls are dropped before the merge, so the search walks further back instead of interpolating
forward. Lags are 0–8 weeks to match M2, so the contrast M6 exists to make stays like-for-like.

**`DECISION` — week key is the Monday start date,** verified rather than assumed: every week in
`ALT_STATS/frozen/srilanka_matched_pairs.csv` is a Monday and falls inside this spine.

**`OPEN` — the WER issue-number ↔ ISO-week mapping is unresolved.** The outcome is keyed
`(year, week)` where `week` is the *WER issue number*; the spine is keyed by date. The two can
differ by one at year boundaries, which would misalign the label by a week precisely at the
December–January transition when dengue peaks. Notebook 05 must reconcile against the outcome
table, not against an assumption.

**`OPEN` — both MODIS products are absent 2025-07-04 → 2025-11-17, and the fix is a backfill, not a
truncation.** ~4.5 months missing from LST *and* VI. Flagged in notebook 04 as `stale_flag` (4.78%
of rows; 34.6% of 2025) rather than filled quietly. Four checks, run 2026-08-06, settle what to do:

1. **Not a notebook-02 search bug.** Re-querying Planetary Computer today returns the same hole —
   Terra composites stop at 2025-06-26 and resume 2025-11-25 (LST) / 2025-11-17 (VI).
2. **Aqua is not a fallback.** MYD11A2/MYD13Q1 are absent over the same window, so the gap is in
   the collection, not the platform. This retires the "add Aqua as a sensitivity" option for 2025.
3. **Truncating the window is not available.** 520 rows — **13.2%** — of
   `ALT_STATS/frozen/srilanka_matched_pairs.csv` have predictor weeks inside the gap (the frozen
   artifact runs to 2025-11-17). Ending M6's window at 2025-06-26 would drop rows M1/M2/M5 are
   scored on, which is `M6.md` §11's first **STOP** condition, not a judgement call.
4. **The data exists at the authoritative source.** NASA CMR returns **76 MOD11A2.061 granules**
   over Sri Lanka for 2025-07-01→11-20. Planetary Computer simply has not ingested mid-2025.

**`DIRECTION` — backfill batch C for 2025-07 → 2025-11 from LP DAAC, then re-run notebook 04.**
This is not a substitution under the 2026-08-05 rule — it is the *same* product (MOD11A2.061 /
MOD13Q1.061) from its primary archive, so the pinned-granule provenance model is unchanged. It
needs a free NASA Earthdata login, which is a registration, not a paywall; weighed against 13.2%
of scored rows resting on a five-month forward-fill, registering is clearly the cheaper cost. If
the backfill is refused, the only remaining option is to keep the rows and report `stale_flag` as
a covariate-quality limitation — the honest version of a result that is weaker than it looks.

**`DECISION` — a trap worth the repo's memory: `pandas.merge_asof` does not preserve the left
index.** It returns a fresh `RangeIndex` in join-key order, so `df[col] = joined[col].values`
scrambles every value across districts and weeks. The first run of notebook 04 did exactly that.
Nothing caught it: the column stayed full, seasonal and correctly ranged, and *every* leakage and
monotonicity check passed, because each re-derives its own frame and is self-consistent within it.
What caught it was the cross-check against notebook 02 §15 — scrambling destroys between-district
variance, so NDVI's within-district share read **93%** against 29% at source, i.e. the error moved
the number in the direction that flatters the argument. Notebook 04 now joins on the keys, asserts
alignment against the spine, and re-derives a stored column to compare. The corrected weekly splits
reproduce §15 to within **1.5 pp** on all six layers, which is the evidence the join is sound.

**`DIRECTION` — `M6.md` §9.5's interim A+B gate needs restating, for a second reason.** Beyond
being unable to express *when* (2026-08-05), the static block is **38 features measured on 26
districts**: its correlation matrix has rank **25**, the districts−1 ceiling, and 7 components
carry 95% of its variance. 135 of 703 pairs exceed |r| > 0.8. A 38-predictor fit on A+B is
saturated before it starts; the honest gate is cross-sectional.

**Scope note.** The row set remains provisional and this is still the binding constraint. `M6.md`
§8 defines M6's rows as the M1/M2/M5 panel spine with its committed split flags; those artifacts
are not on this machine and `scripts/` holds no Sri Lanka ladder, only the Colombia one. §11 makes
a locally-constructed split a **stop** condition, so notebook 05 cannot proceed past the join
without them. Separately, the frozen WER outcome CSV is regenerable here from public PDFs
(`data/README.md`; SHA256 `99f0b9b1…`) — that half of the block is a job, not a dependency.

---

## 2026-08-06 — Correctness pass over the M6 notebooks: one real defect, two stale statements

**Context.** Audited the four executed notebooks for silent defects. All four already ran clean —
74 cells, zero exceptions — so nothing here was visible as a failure; each of these returns
plausible numbers either way. Fixes kept deliberately small, and **no feature value changed**:
notebook 03's `output_sha256_16` is byte-identical before and after (`716844d268e349f9`), which is
the evidence that the corrections touched reporting only.

**`DECISION` — the vintage carry-forward number in notebook 03 §11 was wrong by 25×, and is
corrected.** The audit loop used `years` as its loop variable, clobbering the land-cover year
array set in §4. After the loop it held HREA's `[2018, 2019]`, so the drift was measured over
2018→2019 rather than 2018→2023. The cell reported *"+1.01 pp over 1 years"* and *"carrying 2019
forward to 2025 (6 yr) implies a bias of order 6.08 pp"*. Correct values: **+0.61 pp over 5
years, carrying 2023 forward 2 years, bias of order 0.24 pp.** The printed conclusion was also
self-contradicting — it selected *"larger than"* and then asserted *"so it is not the dominant
uncertainty"*. Both now follow from the same quantity, and the corrected reading is that the
carry-forward bias (0.24 pp) is genuinely **smaller** than the product's own year-to-year noise
(0.76 pp). This strengthens the §11 carry-forward argument rather than weakening it; the
2026-08-05 `DIRECTION` on single-epoch land cover is unaffected, as it rests on §4, not §11.

**`DECISION` — the leakage rule is now stated one way only.** Notebook 02 §2 said the epi-week
join would key on the composite's **start** date, while §16 and the design notes said **end**.
Start-date keying *is* the leak — an 8-day composite starting 2020-06-01 still contains
observations through 06-08. §2 corrected to match. Recorded because notebook 04 is next and this
is the rule it has to implement.

**`DECISION` — fragmentation's vintage was misreported in notebook 03 §2** as 2020 (it had been
given the surface-water epoch as a placeholder) while §11 correctly showed 2023. §2 now derives
it from the land-cover years, so the two tables agree.

**`DECISION` — land-cover fractions keep their existing denominator; the definition is documented
instead.** The class fractions divide by *all* district pixels, so nodata/snow/cloud leave them
summing to 0.979–1.000 rather than 1. Measured before deciding: the unclassified share is
**flat across years** (0.234 / 0.224 / 0.226 / 0.235 / 0.237 / 0.261 % for 2018–2023), and the
per-district maximum (~2.06%) is the same district every year — a granule-edge effect, not
weather. Renormalising would shift every year by a near-uniform +0.03 pp, leave the 0.76 pp
year-to-year movement untouched, change no conclusion, and cost a re-stream plus a new checksum on
a frozen table. So the raw definition is kept and stated in §4 with the measured share.

**`DECISION` — notebook 00's forward-reference was stale and is corrected.** It named
`01_static_geomatics_gee.ipynb` and **Google Earth Engine** as the derivation environment,
superseded by the 2026-08-05 no-GEE decision, and described nightlights and surface water as
dynamic layers in notebook 02 when both ended up static in notebook 03.

**Scope boundary held.** This pass covered the M6 notebooks only — new work. `scripts/` and
`analysis/` carry the frozen v6 pipeline the manuscript's reproducibility claim rests on and were
deliberately not touched.

---

## 2026-08-05 (b) — M6 notebooks handed off for review; PI sign-off formally requested

**`DELIVERABLE` — the four executed notebooks are pushed and under review.** Branch
`m6-geomatics-notebooks` pushed to **both** remotes (spatial-py `origin`, Singati2 `upstream`),
and **PR #1** opened in Singati2:
<https://github.com/Singati2/srilanka-dengue-ews-calibration/pull/1>. Seven files, code + docs
only, no data. The PR body carries the four plan-changing findings and the two plan corrections
(spec conflict, CRS) so they are reviewed as decisions rather than buried in notebook prose.

**`OPEN` — three asks put to the PI in writing,** which starts the clock on items that had been
open without an owner since 2026-07-07: (1) sign-off on the M6 framing, given extraction is ~60%
done and §7 marks the rung optional pending ratification; (2) outcome-table staging, the single
hard blocker on notebooks 05–08; (3) a decision on the WorldPop coastal shortfall *before* WP5's
Build B is founded on the same denominator.

**`DECISION` — collaboration topology corrected in `M6.md` §12.** The documented handoff
(`gh pr create --head spatial-py:<branch>`) **cannot work**: spatial-py's repo is *not* a GitHub
fork of Singati2's (`isFork: false`, no parent), just an independent repo sharing the history, and
GitHub restricts cross-repo PRs to a single fork network. The spatial-py account holds WRITE on
Singati2, so the working route — now written into §12 — is to push the branch to `upstream` as a
**review branch** (never to its `main`) and open a same-repo PR. Recorded because the failure mode
is confusing: the error reads *"No commits between…"* even when the branch is pushed and ahead.

**Note on sequencing, flagged for the PI.** This work is Phase **4** of
`maup_sensitivity_and_spatial_cv_plan.md` §7 — the rung tagged *optional*. Phases 1–3, which carry
the two *mandated* deliverables (WP5 Build B population-weighted exposure, a designated primary
result; and WP4 spatial CV), still have **no code written**. The order was forced rather than
chosen: M6 feature extraction needs only geometry and internet, so it was the only work runnable
while Phase 0 data staging stalled. It also de-risked Phase 1 in passing — WorldPop 2018–2020
rasters are now staged locally and the equal-area zonal pipeline works, which are Build B's two
main ingredients.

---

## 2026-08-05 — M6 moved from plan to build: Python notebook workflow, batches A and C extracted

**Context.** Started implementing the M6 geomatics-only model (`docs/M6.md`) as a step-by-step Jupyter workflow rather than a script, so every intermediate is inspectable. This is **new work only** — it does not touch, port or re-run the frozen v6 pipeline the manuscript's reproducibility claim rests on (`v6-analysis-frozen`, `alt-stats-results-v1/v2`, seed 20260612).

**`DECISION` — spec conflict resolved in favour of `M6.md`.** `M6.md` §0 defines M6 as geomatics-only with *no reanalysis climate*, while `maup_sensitivity_and_spatial_cv_plan.md` §4a lists temperature/precipitation/humidity among the geomatics factors. The notebooks follow **`M6.md`**: admitting reanalysis climate would collapse M6 into "M2 plus extras" and make the research question unanswerable. Dynamic *remotely-sensed* layers (LST, NDVI, surface water, nightlights) are in — they are satellite observations, not reanalysis.

**`DECISION` — no Google Earth Engine.** All layers come from anonymous public downloads: Copernicus GLO-30 via AWS Open Data, MODIS via Microsoft Planetary Computer STAC. Pinned granule IDs plus checksummed local rasters are more reproducible than a GEE run, whose collections can be revised underneath you. Supersedes the 2026-07-07 note adopting GEE as the derivation environment.

**`DECISION` — CRS correction to the plan.** `maup_sensitivity_and_spatial_cv_plan.md` §5 recommends SLD99 or UTM 44N for area weighting; **both are transverse Mercator — conformal, not equal-area.** The notebooks use a Lambert azimuthal equal-area projection centred on the island for all area-bearing computation. Measured effect for Sri Lanka is small (per-unit area error −0.044% to −0.080%) but it is the correct default and will matter more for Colombia, which spans far more latitude.

**`DECISION` — batch C (dynamic) built before batch B (static).** Most M6 variables are static per district, and a model built only from those emits one constant prediction per district for every week: against a weekly label it can express *which* districts differ but never *when*, so it scores near chance **by construction**. That null would be structural, not empirical, and must not be reported as "geomatics carries no signal". The dynamic layers decide whether M6 is answerable at all, so they were settled first.

**`DECISION` — MODIS extraction rules** (recorded because each alternative fails silently):
- **Terra only.** `modis-11A2-061` and `modis-13Q1-061` each contain *both* Terra (`MOD*`, ~10:30 overpass) and Aqua (`MYD*`, ~13:30). Selection is on the product id prefix — not the STAC `platform` field, which is empty for some items. Aqua is a legitimate later gap-filling sensitivity as a **separate column**, never merged into the Terra one.
- **Duplicate granules resolved to newest `created`** (21 LST, 12 VI reprocessing pairs), so selection is deterministic rather than arrival-ordered.
- **LST QA = mandatory QA ≤ 1 AND average error ≤ 2 K**, adopted after measuring the alternatives. Mandatory-QA-0-only retains 14–42% of land pixels and empties whole districts; worse, what it drops is the cloudy, wet weeks — biasing the series warm and dry in exactly the conditions a dengue model cares about.
- **No resampling of the data.** Zonal reduction happens on the native MODIS sinusoidal grid (itself equal-area); the geometry is reprojected to the data once instead of the data being warped 700 times.

**`DELIVERABLE` — three executed notebooks** (`notebooks/`, outputs committed; feature tables stay in gitignored `data_quarantine/m6_geomatics/`):
- **00 — spatial frame.** Independently reproduces the recorded 26-node/60-edge queen adjacency and the `rdhs_26_v1.gpkg` checksum (9e5e2c0a).
- **01 — batch A terrain.** Elevation, slope, TWI, HAND for all 26 RDHS from Copernicus GLO-30. Cross-checks: max elevation 2,514 m vs Pidurutalagala 2,524 m; raster land area 66,040 km² vs vector 66,041 km². **Finding: batch A is strongly collinear** — 19 of 28 pairs exceed |r| > 0.8, so eight terrain features span roughly two independent dimensions. Feature importance will be unstable; stability selection is required, as §4a anticipates.
- **02 — batch C dynamic.** MOD11A2 LST day/night (8-day, 1 km) and MOD13Q1 NDVI/EVI (16-day, 250 m), 2017-11 to 2025-12, with per-unit coverage carried alongside every mean. Window starts 2017-11 so an 8-week lag exists for the first 2018 epi-week.

**`OPEN` — leakage rule for the temporal join, to be enforced in assembly.** An 8-day composite dated 2020-06-01 summarises 2020-06-01 to 06-08; joining it to the epi-week beginning 06-01 puts post-week observations into a predictor. Assembly must use only composites whose **end** date precedes the week being predicted, then lag 0–8 weeks from there (mirroring M2). Relatedly, **cloud gaps must be filled with past data only** — `interpolate()` across a gap reaches into the future. Composite start *and* end dates are carried in the frozen tables so this can be enforced.

**`DELIVERABLE` — notebook 03, batch B statics** (executed same day). Land cover, fragmentation, surface water, population and nightlights for all 26 RDHS; 18 features. Sources: Impact Observatory `io-lulc-annual-v02` (10 m, annual 2018–2023), JRC GSW v1.4, WorldPop UN-adjusted, HREA.

**`DECISION` — two substitutions, both under the "genuine access barrier / document it" rule:**
- **`io-lulc-annual-v02` replaces ESA WorldCover** for built-up/forest/cropland. WorldCover has only 2020 and 2021 epochs; vintage is the binding constraint (below). One classification then supplies three variables consistently.
- **HREA replaces monthly VIIRS DNB** for nightlights. EOG's monthly composites need a registered account. HREA is the same sensor, hosted anonymously, but **annual** — so nightlights drops from a dynamic layer to a slow one. Moot in practice: HREA ends 2019.

**`OPEN` → `DECISION` — the vintage gate cannot be met, so it is reported instead.** `M6.md` §6 requires each layer's year to match the analysis window. **No batch-B source reaches the end of the 2018–2025 window**: land cover ends 2023, population 2020, nightlights 2019, surface water is a 2020 epoch. Resolution: build annually where possible, carry the last year forward, and **publish the carry-forward table** (notebook 03 §11) so a reader sees which district-weeks rest on extrapolation.

**`DIRECTION` — do NOT join land cover year-by-year; use a single epoch.** This reverses the plan's assumption. Measured in notebook 03 §4: island built-up runs 16.7% (2018) → 18.5% (2020) → 17.3% (2023), **0 of 26 districts move monotonically**, and median year-to-year movement (0.76 pp) is comparable to net change across the whole record (0.94 pp). Settlement does not un-build, so most of the annual variation is the classifier relabelling the same ground. A year-matched join would feed reclassification noise to the model as if it were urbanisation. Jaffna and Killinochchi are the genuine exceptions (~1.1 pp/yr, post-conflict resettlement). Per-year tables frozen anyway as the evidence, and to keep the call reversible.

**`DIRECTION` — the urban heat island is absent at 26-district resolution, and that is a MAUP result, not a data error.** Notebook 03 §10 cross-checks batch B against A and C; four relationships hold strongly between products sharing no inputs (trees~NDVI +0.87, NDVI~LST −0.79, nightlights~built-up +0.93, pop-density~built-up +0.91). Built-up~daytime-LST is ~**+0.05**. Elevation is *not* the confounder (corr(built-up, elevation) ≈ −0.03, partial correlation unchanged): district-mean LST is governed by moisture/vegetation, and the dry zone is hot with almost no built-up, cancelling Colombo. The UHI is a few-km phenomenon inside units averaging ~2,500 km². **This is the study's own MAUP thesis appearing in its covariates** — a real physical effect erased purely by the choice of areal unit. Consequence: an M6 null on built-up means "invisible at this unit", never "no urban effect", and M6 feature importances must not be read as mechanism.

**`OPEN` — population denominator loses ~3.5% at the coast.** WorldPop totals inside the 26 RDHS polygons are 20.9–21.1 M against ~21.4–21.9 M nationally; pixels are assigned whole to the unit containing their centre and Sri Lanka is all coastline. Quantified in notebook 03 §7 as a capture fraction. **This propagates directly into WP5's population-weighted exposure build**, whose denominator is the same quantity, and the affected districts are the dense coastal ones. Needs a decision in WP5: accept and report, or switch to fractional-coverage weighting at the boundary.

**`OPEN` — still outstanding for M6:** batch D (healthcare access, relative wealth, connectivity, rice-paddy phenology). Note that `M6.md` §9.5's interim gate — fit M6 on batch A + B before the full ladder — is now known to be **structurally unrunnable as written**: A + B are entirely static, so against a weekly label they cannot express *when* (notebook 02 §15). The honest version tests A + B against a cross-sectional baseline, not a weekly one. Modelling (notebooks 05–08) remains **blocked on outcome-table staging**, unchanged from 2026-07-07.

---

## 2026-07-07 — Scope for WP4/WP5 locked; plan promoted from draft to phased

**Context.** Resumed the geospatial work-stream (WP4 spatial cross-validation, WP5 MAUP/exposure sensitivity). The geospatial risk-factor literature review (`dengue_geospatial_risk_factors_review.html`, 59 sources, produced 2026-07-02) was in hand and informed the calls below.

**`DECISION` — four open scope questions settled** (detail + rationale in `maup_sensitivity_and_spatial_cv_plan.md` §1a):
- **D1 — Cross-validation setting: BOTH countries, scheme sized to n.** Sri Lanka (26 RDHS) → **buffered leave-one-out (LOOCV)** — hold out one district, drop its within-range neighbors from training to stop leakage. Colombia (~1,000 municipalities) → **spatial block CV** (leave-one-department-out). Colombia carries the well-powered external-validation claim; SL is the compact-country sensitivity companion. Temporal honesty (past-only lags) preserved inside every fold → spatio-temporal CV.
- **D2 — Three exposure builds**, a nested ladder each adding one refinement: **A** area-mean (exists) → **B** population-weighted → **C** elevation/lapse-rate–corrected temperature (Copernicus GLO-30 DEM, −6.5 °C/km start). Terrain correction promoted from "brainstorm/maybe" to in-scope because elevation is the top-ranked geospatial *modifier* in the lit review and should move temperature most in the central highlands.
- **D3 — Resolution stays at 26 RDHS / municipality.** No re-extraction to MOH-division (would require rebuilding the frozen outcome table).
- **D4 — All four extras IN this paper:** per-variable MAUP (precip vs temp) · spatial-structure-of-miscalibration map (WP6 bridge, F8) · cross-setting MAUP (repeat weather contrast in Colombia) · population-product sensitivity (WorldPop vs GHSL vs census; lowest priority, first to trim).

**`DIRECTION` — deliberately comprehensive paper.** D4 accepts the full extras set rather than deferring most to "Paper 2." Paper-2 backlog now: uncertainty propagation, human-mobility/connectivity, boundary-vintage sensitivity, rice-paddy/LULC phenology.

**`DELIVERABLE` — plan doc promoted.** `maup_sensitivity_and_spatial_cv_plan.md` moved from *DRAFT — for discussion* to *SCOPE LOCKED* with: a new §1a (locked decisions), three-build WP5 (§3.1/3.1b + per-variable/cross-setting/population-product/F8 subsections), a two-country WP4 (§4.2 SL buffered LOOCV, §4.3 Colombia block CV, §4.6 power caveat), an expanded deliverables checklist, and a new §7 phased execution sequence (Phase 0 data staging → Phase 5 write-up).

**`DELIVERABLE` — HTML implementation plan.** `wp4_wp5_implementation_plan.html` — self-contained, browser-friendly rendering of the plan in the project's house style (locked decisions, three-build ladder, two-country CV side-by-side, phased sequence, guardrails). Now also carries **plain-language "In plain language" notes** on the builds, the CV design, and each of the four extras. Markdown plan remains source of truth if the two ever disagree.

**`DIRECTION` — lit-review factors mapped to plan roles.** Reconciled the 23-factor geospatial review with the plan under the no-new-model rule (HTML §5; MD plan §3.7). A factor may enter **only** as (A) exposure construction [elevation→Build C, population→Build B] or (B) an F8 miscalibration explainer [urbanisation, elevation, NDVI, distance-to-surface-water]; the other 14 factors are logged for Paper 2.

**`DECISION` — all 23 lit-review factors screened against 4 tests (free data · district×week derivable · role A/B only · evidence-worth-it); include-then-prune.** Resolves the earlier "three candidates" open item. Detail + source-linked table + step-by-step recipes in HTML §5; MD plan §3.7.
- **Added to the exposure layer (weekly, free, transforms of held data):** DTR, absolute humidity/VPD, drought index SPI/SPEI. *(The three former candidates are now IN.)*
- **Added as F8 map covariates (static per district, free):** healthcare access (OSM/HDX distance-to-facility — reporting completeness drives miscalibration), Relative Wealth Index/SES (Meta RWI on HDX).
- **Optional — kept, freely downloadable, prune if flat (10):** nightlights (VIIRS), TWI/slope (DEM), flood-proneness HAND (DEM), static connectivity (WorldPop+OSM), land-surface temp/UHI (MODIS), land-cover fragmentation (WorldCover), cropland/rice (WorldCover), forest (Hansen/WorldCover), wind (ERA5-Land), + ENSO/IOD as a temporal-only stratifier.
- **Dropped → Paper 2 — ONLY 3, all for non-free data (reason stated):** mobility live weekly flows (gated Meta/telco), household water storage (DHS/JMP survey micro-data), housing/roof (DHS/paid VHR imagery).

**`DIRECTION` — geomatics stress test added to the plan (optional, PI sign-off).** User proposed a geomatics-only model → feature-importance → selected-geomatics hybrid. Reconciled with the no-new-model rule by framing it as a **value-of-geomatics stress test** of the existing conclusion (not a proposed predictor): 3 steps (broad geomatics-only model incl. dynamic + static factors → **stability feature-selection inside the WP4 spatial folds** → selected-geomatics hybrid with recent cases, judged by the M-ladder calibration + net-benefit lens). Key guardrails flagged: **no selection leakage** (nested CV via the spatial folds), **no lone winner** (importance unstable under collinearity → stability selection + ranges), honest-null accepted. If geomatics *materially* helps → that's a new finding = Paper 2, escalate to PI. Plain-language write-up: HTML §6; spec: MD plan §4a; new execution Phase 4. **`OPEN`: awaiting PI sign-off before this rung is run.**

**`DIRECTION` — max-inclusion of freely-downloadable factors (user directive, supersedes the earlier evidence-based drops).** Keep **every** factor whose data is free and easily downloadable (include-then-prune); drop **only** for a genuine access barrier, with the reason recorded. This moved 6 previously-dropped-but-free factors (land-surface temp, fragmentation, cropland, forest, wind, ENSO/IOD) back to OPTIONAL — now 20 of 23 kept, 3 dropped. Larger optional panel → mandatory pre-specification + FDR control (F8 stays exploratory-explanatory). Google Earth Engine adopted as the free derivation environment for the static covariates.

**`OPEN` / blocking before any implementation:**
1. **PI ratification** of the §1a scope.
2. **Data staging** — this checkout holds only code + docs; every input (frozen Build-A exposure CSV, WorldPop rasters, RDHS/Colombia geometries, OpenDengue outcome, DEM) lives outside the repo and must be staged before Phase 1.

**Guardrails reaffirmed:** no data committed (code + reports only); honest-null clause (SOW §N) — a well-characterized "exposure construction doesn't change the decision" is a publishable result, not a failure; geospatial modifiers stay *explanatory* (miscalibration), never new accuracy predictors (no-new-model rule).

---

## Prior context (pre-log, for continuity)

- **2026-07-02 — `DELIVERABLE`:** geospatial & remotely-sensed dengue risk-factor literature review (`dengue_geospatial_risk_factors_review.html`, 59 sources) — ranked catalogue of geomatics-derivable drivers/modifiers/confounders to guide the exposure-layer extension.
- **2026-07-01 — `DELIVERABLE`:** `study_guide.html` (plain-language onboarding) and the first draft of `maup_sensitivity_and_spatial_cv_plan.md`.
- **Standing study finding (from the manuscript, in major revision):** recent case counts (M1) beat climate-only early-warning models; climate adds only a small hybrid increment (M5) — confirmed in Colombia, not in Sri Lanka. Paper's headline: *two equally accurate warning systems can recommend different public-health actions* — evaluated via calibration + decision-curve / net-benefit. Target: PLOS NTDs.
