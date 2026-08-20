# Four open questions for the PI — geomatics (WP4 / WP5)

> **SUPERSEDED 2026-08-20 by `docs/pi_ask_v2_geomatics_open_questions.md`. Do not send this
> version.** Q1 and Q2 rest on the claim that the frozen archive holds predictions rather than
> design matrices, so the re-runs could not be executed here. That claim is false — the builders are
> in `analysis/v12_referee_response/run/sl_matched_and_recal.py` — and Q3's structural argument
> ("a district-relative model absorbs Build C exactly, so it cannot flip an alert") was disproved by
> measurement: it flips 67. Kept unedited as the record of what was believed on 2026-08-16.

**Status: DRAFT, never sent, SUPERSEDED.** Prepared by the Geospatial Lead, 2026-08-16.
Companion to `docs/study_decision_log.md` and `docs/maup_sensitivity_and_spatial_cv_plan.md`.

---

## Why this document exists

Every WP4/WP5 analysis that can be run without collaborator artifacts is now done — the exposure
ladder (A′/B/C), plan §3.2 (F2), §3.3's runnable half (F7), §3.5's exposure half, §3.6 (F8), the fold
geometry and power table, and the fold effect measured within M6. The write-up is drafted.

What remains is not work I can do. It rests on four questions that have accumulated across separate
memos on PR #1, where they are easy to lose. This is all four in one place, each with **the smallest
artifact that would unblock it** — so that answering is cheap, and so a partial answer is still
useful.

**These four are deliberately not bundled.** Q1 and Q2 look like the same request and are not: they
need *different artifacts*, and the evidence for their urgency points in *opposite directions*. If
only one can be answered, it should be Q1.

| # | Question | What it unblocks | Urgency |
|---|---|---|---|
| **1** | Can I have **M5's design matrix** (and M0/M1/M2's, if they exist)? | WP4's cross-model fold re-run — the reviewer's actual concern | **Raised** by `wp4_02` |
| **2** | Can I have **the code that builds** that design matrix from an exposure table? | WP5 §3.3's registered re-run (ΔAUC, Δcalibration); §8's matched ablation; §4's threshold generator | **Lowered** by `wp5_05` |
| **3** | **Which model form** do those artifacts use — absolute or district-relative temperature, and do they carry dewpoint/humidity? | Decides *in advance* what §3.3 can possibly find | Answerable in one sentence |
| **4** | **Paper 1 or Paper 2** for the geomatics work? | Everything's priority, including whether the frozen-target recovery still matters | Blocking planning, not analysis |

---

## Q1 — M5's design matrix. This is the one that matters most.

**The ask:** the feature matrix M5 was fitted on — training rows (2018–2022) and test rows
(2023–2025), with column names — plus the penalty type and the selected regularisation strength.
`ALT_STATS/frozen/srilanka_matched_pairs.csv` carries **predictions only**, which is not enough to
re-fit.

**Why it got more urgent, not less.** `wp4_02` measured what spatial folds cost, inside M6, against a
size-matched random-district control so that the loss of training data is held fixed. The folds are
**not** cheap: at adjacency buffering the geography-attributable gap is −0.022 AUC, and at 100 km the
blocked estimate is 0.502 — chance — while an equally sized random training set still reaches 0.573.
Calibration slope falls from 0.875 to 0.018 across the same range.

M5's external-validation claim rests on a temporal split. **If M5 depends on spatial proximity the way
M6 does, spatial cross-validation moves it too** — which is precisely the reviewer concern WP4 exists
to answer. It cannot be tested without this matrix.

I also withdrew my own earlier inference here: `wp4_01` found residual Moran's I indistinguishable
from null at every band, and I concluded the buffered scheme was cheap. Direct measurement does not
support that. Residual autocorrelation and dependence on proximate training data are different
quantities and they disagree in this data. **So we cannot answer the reviewer from the residual
analysis alone — and I cannot answer it for M5 at all without the matrix.**

**Smallest sufficient version:** one CSV of the fitted feature matrix with the row keys
(district × predictor week) and column names, plus a line stating the penalty and its strength. If
M0/M1/M2 matrices exist too, they close §10's contrast, which is currently unanswerable because the
frozen artifact holds M5-full and M5-no-climate rather than M0/M1/M2.

---

## Q2 — The code that builds the design matrix. Different artifact, lower urgency.

**The ask:** the script that turns an exposure table into M5's climate columns — the DLNM-style
cross-basis construction (temperature, precipitation, humidity; lags 0–8; df=3), not the resulting
matrix.

**Why it is a different ask from Q1, concretely.** WP4 re-fits the *same columns* on *different rows*,
so a static matrix suffices. WP5 §3.3 re-fits on *different exposure values*, so the columns have to
be regenerated from Build B and Build C — which needs the builder, not its output. Sending me the
matrix does not unblock this, and sending me the builder does not unblock Q1 as cheaply. **Answering
one does not answer the other.**

**Why it is less urgent than I previously said.** `wp5_05` answered *does the decision move?* without
it, by bounding the answer three ways: an exact model-free flip curve, an observed ceiling from
deleting the whole climate block, and a transfer coefficient estimated from the frozen predictions.
Exposure construction changes **0.9–1.9%** of alerts under population weighting and **1.6–2.6%** with
the lapse correction, against **11.2%** for deleting climate altogether — 14–24% of the climate
block's entire decision leverage. The transfer coefficient's norm varies 2.3× across specifications
while the flip count varies far less, so the qualitative answer is robust to what this artifact would
supply.

**What is still missing without it:** ΔAUC and Δcalibration under each build — a table, not a
reversal. Also §8's matched geomatics ablation and §4's threshold generator.

---

## Q3 — Which model form? One sentence changes what §3.3 can find.

**The ask:** does the SL hybrid enter temperature in **absolute** terms or **district-relative** terms
(anomalies, district fixed effects, per-district standardisation)? And does it carry **dewpoint or
relative humidity** as well as temperature?

**Why it must be answered before the re-run, not after.** Build C's correction to `t2m` carries no
time index — it is Build B plus a constant per-district offset (within-district sd < 2×10⁻⁶ °C over
417 weeks). Therefore:

- A **district-relative** temperature model absorbs that offset **exactly**, and Build C cannot flip a
  single alert. A null would then be a fact about the parameterisation, **not about terrain**, and
  must not be written up as "terrain doesn't matter."
- An **absolute-temperature or fixed-threshold** model sees the full displacement — up to ~2 °C in the
  highlands.

And the humidity half runs the other way, which is why the second half of the question matters:
`d2m` is **not** a constant offset. It departs from the exact −Γ·Δz prediction by up to 0.46 °C and
varies week to week, because the physically necessary saturation guard binds in three highland
districts. **So a model carrying dewpoint or humidity sees a Build C residual that no district effect
can absorb** — §3.3 has more to find there than my earlier memo implied.

Knowing the answer now would let me state what the re-run can and cannot show *before* it is run,
rather than discovering it in the result.

---

## Q4 — Paper 1 or Paper 2?

**The ask:** where does the geomatics work land?

**Why I am asking rather than assuming.** PR #8's `FINAL_CANONICAL_DECISION.md` has M6/WP4/WP5
*"remain **separate and outside Paper 1 evidence**. No geomatics/spatial-CV/exposure-weighting result
is imported; the geomatics estimand and spatial-exposure operator appear only as **pending Discussion
notes**."* I read "pending" as the operative word: that is a **gate consequence, not a rejection** —
the pass was formalisation-only, carrying a "no M6/WP4/WP5 promotion" restriction — and it does not
contradict the 2026-08-07 PR #1 comment approving geomatics inclusion. I have not treated it as a
rejection, but I would rather be told than keep inferring.

**The real issue is timing.** `V44_VS_BIOMATH_DECISION_MEMO.md` states that *"no further analysis is
required to submit either way; the open blockers are author-owned."* If Paper 1 goes out without this
work, then:

- the frozen-target recovery stops being urgent (M6's label currently carries an
  `EXPLORATORY_RECONSTRUCTED_TARGET` caveat on 19.2% of test rows);
- Q1 and Q2 become Paper 2 dependencies rather than submission blockers;
- and the **Colombia arm** — ~1,000 municipalities, where the well-powered spatial claim and the
  cross-setting MAUP check actually live — becomes the right next investment rather than a stretch
  goal.

If instead any of this belongs in Paper 1, Q1 is on the critical path and I would want it first.

**A note either way.** One result in this work is not really about WP5 and would strengthen Paper 1
wherever the geomatics lands: **net benefit is structurally blind to perturbations acting near the
decision threshold.** A row can only flip if it sits near p\*; rows near p\* have an event rate ≈ p\*;
and p\* is by definition the break-even rate — so every flip is worth ≈ 0 net benefit either way.
Measured, flipped-row event rates track p\* across all four thresholds (r = 0.96), and ΔNB stays
within ±0.0023 while flip counts are unambiguously non-zero. **A near-zero ΔNB must not be reported
as "no decision effect."** That critique applies to sensitivity analyses reported elsewhere in the
current manuscript, and it now has three independent demonstrations in this work (§3.3 nationally,
§3.5 across population products, §3.6 district by district).

---

## For information — no reply needed

**A defect in the frozen artifact.** `full_recal` is not a monotone recalibration of `full_raw`:
sorting by the raw prediction, 49% of adjacent recalibrated pairs invert, and **AUC is 0.7715 raw
against 0.7512 recalibrated** — which a monotone map cannot do. The cause is in the repo:
`analysis/v12_referee_response/run/sl_matched_and_recal.py` §(B) applies a past-only rolling 52-week
intercept update refitted at every test week, so the map is time-varying and re-ranks *across* weeks.
*Within* a week it is an exact constant logit shift (147 of 151 weeks, zero within-week inversions).
Consequence: **every reported AUC needs to state which column it came from** — the manuscript's 0.771
is the raw one — and "recalibration does not affect discrimination" is false for this artifact.
(Already flagged in the `wp5_05` memo; repeated here because it bears on Q3 and on the manuscript.)

**Four collaborator artifacts are absent, not three.** The design matrices, the threshold artifact,
the M0/M1/M2 predictions, and — found later — **the frozen Build A exposure table itself**
(`rdhs_weekly_climate_exposure_2018_2025_v2_boundary_resolved.csv`). Its sha in `wp5_00`'s provenance
was transcribed from the build report, not computed locally; the file has never been on this machine.
WP5 therefore rebuilt both arms from one freshly staged CHIRPS stack, which is the stronger design
(the arms share inputs by construction rather than by assumption) — so this is **not** a request.
Recorded so that no one treats a provenance sha in that series as evidence a file existed.

**Not a PI item.** A free Copernicus CDS key would rebuild the temperature ladder at 0.1° instead of
0.25°, raising Build B's reach from 65.3% to 91.7% and anchoring Build C to a less-smoothed orography.
Not a blocker — the whole ladder is built and every number is a conservative floor biased toward the
null — and it is on my side to obtain, not the PI's.
