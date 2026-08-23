# Open questions for the PI — geomatics (WP4 / WP5), v2

**Status: DRAFT, not yet sent.** Prepared by the Geospatial Lead, 2026-08-20.
Supersedes `docs/pi_ask_v1_geomatics_open_questions.md` (2026-08-16), which was never sent and
**should not be**: two of its four questions rested on a premise I have since disproved.
Companion to `docs/study_decision_log.md`.

---

## What changed since v1, in one paragraph

v1 asked for two artifacts — M5's design matrix and the code that builds it — on the stated grounds
that the frozen archive holds predictions only and the re-runs therefore could not be executed here.
**That was wrong, and it was wrong in the repository the whole time.**
`analysis/v12_referee_response/run/sl_matched_and_recal.py` carries the design-matrix builder, the
cross-basis builder, the climate block and the fitting code, and reproduces the frozen M1/M4/M5 to
<1e-6. What is actually missing is an *input*: the linked analysis table, whose committed builder
reads paths that exist only on the study's Linux host. I substituted an independent rebuild of that
input, ran both re-runs, and they are now written up as sensitivity analyses. **So v1's Q2 is
withdrawn, v1's Q1 changes into a request for a different artifact, and one genuinely new decision
has appeared: whether rebuild-based results may be reported at all.**

| # | Question | What it decides | Urgency |
|---|---|---|---|
| **1** | May the **rebuild-based results be reported**, and under what label? | Whether Results Q7 stands as drafted | **Blocking the write-up** |
| **2** | Can I have the **linked analysis table** the committed builder reads? | Turns both sensitivity analyses into the registered re-runs | High, no longer blocking |
| **3** | **Paper 1 or Paper 2** for the geomatics work? | Everything's priority, and whether `FINAL_CANONICAL_DECISION.md` line 8 stands | Blocking planning |
| **4** | One sentence confirming **M5's published form** | Nothing now; closes a loop | Low — ask last |

Each is separable. A partial answer is still useful, and if only one can be answered it should be Q1.

---

## Q1 — May I report results refitted on a rebuilt input? This is the new one.

**The decision:** both registered re-runs have now been executed, but on an **independent rebuild**
of the linked analysis table (`data_quarantine/sl_ladder/sl_linked_v2equiv.csv`), not on the
registered input. Everything drafted from them is labelled a sensitivity analysis and marked
`\REBUILD` in the text. **Do you want them reported at all, and if so under what label?**

**What the rebuild is.** Same weather windows and same per-district weights as WP5's own build;
ERA5 0.25° in place of the registered ERA5-Land 0.1° for temperature and humidity; CHIRPS at native
resolution for rainfall, unchanged. Two undocumented conventions had to be recovered by sweeping
against the frozen labels — `week_start = ISO_Monday − 7d`, and a time-invariant population
denominator — and both are worth writing into the study's own documentation regardless of this
decision.

**How closely it reproduces the frozen run, measured rather than asserted.** Refitted on the
rebuild, M5 agrees with the frozen model's alert labels on **98.8%** of the 3,926 held-out rows and
its held-out predictions correlate **0.975** with the frozen ones (0.976 for the climate-free twin).
Within the rebuild, the baseline arm of each notebook reproduces the rebuild's own committed
predictions to **exactly 0.0**, so every contrast reported is the exposure or the fold and not the
refit.

**Why I think it is worth reporting, and where I could be wrong.** It answers the reviewer's actual
question in the favourable direction (below), and the alternative is reporting nothing on the two
questions the referee raised. Against that: it is a competing analysis of a collaborator's models
run on a reconstruction of their input, and that is a judgement about the collaboration as much as
about the statistics. **That judgement is yours, not mine, which is why this is Q1 and not a
footnote.** If the answer is no, the drafted sections come out and Q2 becomes the critical path.

**The three findings that stand or fall with this decision.**

1. **Spatial cross-validation does not deflate the climate increment.** Under buffered folds the
   climate block earns +0.009 to +0.016 in net benefit against +0.017 under the temporal split;
   every change-versus-temporal interval spans zero. Stated as *unchanged*, not as a gain.
2. **Exposure construction moves the decision but not the score.** Across four exposure builds every
   ΔAUC and ΔNB interval spans zero, while 72 / 64 / 121 alert decisions flip against a measured
   noise floor of 3. A sensitivity analysis reading only ΔAUC and ΔNB would have reported a null.
3. **The price of a spatial fold is a property of the model, not only of the geography.** At the
   operative radius M5 and the geomatics-only model disagree in *sign* (+0.038 against −0.022), so
   the within-M6 result in the earlier draft could never have substituted for it.

---

## Q2 — The linked analysis table. Different artifact from v1's ask, and the only thing still missing.

**The ask:** the linked analysis table M5 was fitted on — district × week rows, 2018–2025, with the
outcome column and the climate exposure columns as the study built them. One CSV. Not the design
matrix, not the builder: I have both.

**Why the earlier ask was wrong.** v1 said the archive "holds predictions, not design matrices", and
concluded the re-runs were impossible here. The builders were in the repo. I record this rather than
quietly correcting it because the claim had been load-bearing for three months and shaped two memos:
**a blocker that is never re-tested becomes a fact.**

**What this artifact would change.** It would convert both sensitivity analyses into the registered
re-runs, and remove the one substitution that biases a reported number: ERA5 0.25° in place of
ERA5-Land 0.1° attenuates the very effect WP5 measures — the population-weighted construction
recovers 65.3% of the elevation displacement at 0.25° against 91.7% at 0.1° — so every temperature
displacement reported is a conservative floor. The direction of that bias is known and stated; its
size on the *decision* counts is not.

**Smallest sufficient version:** the CSV, or the four or five input files the committed builder's
`/home/mpcrlab/…` paths point at. Either closes it.

---

## Q3 — Paper 1 or Paper 2? Unchanged in substance, sharper in consequence.

**The ask:** where does the geomatics work land?

PR #8's `FINAL_CANONICAL_DECISION.md` places M6/WP4/WP5 *"separate and outside Paper 1 evidence"* as
**pending Discussion notes**. I read "pending" as the operative word — a gate consequence, not a
rejection, and not a contradiction of the 2026-08-07 PR #1 comment approving geomatics inclusion.
I have not treated it as a rejection, but I would rather be told than keep inferring.

**What has changed since v1 is that the inference now has a commit behind it.** WP4/WP5 are ported
into the v44 biomath candidate as Results Q7, on the branch `wp45-into-v44`. That port **overrides
line 8 of `FINAL_CANONICAL_DECISION.md`**, which I have annotated rather than rewritten, because
overriding a ratified decision is not mine to do. The branch is pushed so you can read it, but
nothing is merged and no pull request is open against it: pushing a branch is not a claim that the
override stands. If the answer is Paper 2, the port is reverted and the Colombia arm — where the well-powered spatial claim would have lived — is
the question to revisit; note that the Colombia block CV was withdrawn from the study on 2026-08-17,
so **the n=26 limitation currently has no companion analysis coming and is written as permanent.**

**A note either way.** One result here is not really about WP5 and would strengthen Paper 1 wherever
the geomatics lands: **net benefit is structurally blind to perturbations acting near the decision
threshold.** A row can only flip if it sits near p\*; rows near p\* have an event rate ≈ p\*; and p\*
is by definition the break-even rate, so every flip is worth ≈ 0 net benefit either way. It now has
**four** independent demonstrations in this work, the newest on a refit rather than on perturbed
frozen predictions: 121 alert decisions change sign while ΔNB moves +0.0004 [−0.0022, +0.0031].
**A near-zero ΔNB must not be reported as "no decision effect"** — a critique that applies to
sensitivity analyses reported elsewhere in the current manuscript.

---

## Q4 — One sentence on M5's published form. Ask last; I no longer need it to proceed.

**The ask:** confirmation that the published SL hybrid is the form
`sl_matched_and_recal.py` builds — district fixed effects, seasonal harmonics, and temperature
entering through a nonlinear DLNM-style cross-basis rather than linearly.

**Why it is now a confirmation rather than a question.** v1 argued that a district-relative model
would absorb Build C's per-district offset exactly, so Build C could flip no alert, and that a null
would therefore be a fact about the parameterisation rather than about terrain. **The premise is
right and the conclusion is wrong, and I only found that by breaking the model to test it.** Build C
flips **67** decisions in M5. An additive intercept absorbs a shift in the *linear predictor*; Build
C shifts *temperature*, read through a nonlinear cross-basis, and a nonlinear function of a shifted
input is not a shifted function of the input. Refitting with temperature entered linearly collapses
the flips to **10**. The rule that survives is narrower than the one I sent you in v1: *a model
linear in temperature absorbs a uniform exposure offset; a model with a nonlinear exposure–response
does not.* **If any draft still quotes v1's version of that argument, it is wrong.**

---

## Withdrawn from v1

- **v1's Q2 (the design-matrix builder).** The artifact is in the repository. Withdrawn entirely.
- **v1's Q1 as phrased (the fitted design matrix).** Superseded by Q2 above, which asks for the
  input instead. If the design matrices exist as artifacts they are still welcome, but they are no
  longer the binding constraint and should not be prioritised over the linked table.
- **v1's Q3 as a question.** Reduced to the confirmation in Q4.
- **v1's claim that "Build C cannot flip a single alert" under a district-relative model.** Disproved
  by measurement. See Q4.

---

## For information — no reply needed

**A defect in the frozen artifact, unchanged from v1 and still live.** `full_recal` is not a monotone
recalibration of `full_raw`: sorting by the raw prediction, 49% of adjacent recalibrated pairs
invert, and AUC is **0.7715 raw against 0.7512 recalibrated**, which a monotone map cannot do. The
cause is in the repo: `sl_matched_and_recal.py` §(B) applies a past-only rolling 52-week intercept
update refitted at every test week, so the map is time-varying and re-ranks *across* weeks; *within*
a week it is an exact constant logit shift. Consequence: **every reported AUC needs to state which
column it came from** — the manuscript's 0.771 is the raw one — and "recalibration does not affect
discrimination" is false for this artifact.

**A defect I introduced and fixed, recorded because it bears on how the rebuild should be read.** The
first version of the rebuild carried rainfall mirrored north-to-south: an index built from raster row
order was applied to a latitude-ascending array, so all but three districts received their mirror
image's rainfall. It was caught because a correlation gap of 0.095 between two models differing
*only* in the climate block is not something an exposure substitution can produce. Fixed, everything
downstream re-run, and **no manuscript number ever depended on it**. The gap after the fix is 0.0006.

**Not a PI item.** A free Copernicus CDS key would rebuild the temperature ladder at 0.1° instead of
0.25°, raising Build B's reach from 65.3% to 91.7% and anchoring Build C to a less-smoothed
orography. Not a blocker — every number is a conservative floor biased toward the null — and it is on
my side to obtain, not yours.

**Verification state, for the record.** 324 numbers in the v44 candidate are recomputed from their
source outputs by `scripts/verify_numbers_v44.py`; one mismatch stands, the +0.0049 three-week
reporting-delay increment, which needs the Linux box. The WP4/WP5 fragment passes 51 structural
checks. **Neither document has been compiled — there is no LaTeX toolchain on this machine.**
