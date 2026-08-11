# Response to `instruction_m6.md` — audit executed, artifact frozen, one finding you'll want

**From:** Geospatial Lead (WP4 / WP5) · **To:** Ganesh Shiwakoti · **Date:** 2026-08-07
**Re:** `instruction_m6.md` (commit `8de3018`, branch `agent/instruction-m6-next-actions`)
**Detail:** `docs/study_decision_log.md` entry 2026-08-07 (e)

Instructions received and accepted in full. §24 items 1 and 2 are done. Nothing has moved toward
v44, and nothing will until §22's checklist is resolved item by item.

One process note: the instruction branch is not on `main` and not on PR #1, and it is `ff6287d`
plus that single file. It was found only by sweeping the branch list. If future instructions land
the same way, a note on the PR would stop them sitting unread.

---

## 1. §2 — Batch D audit: the model is **M6-core (A/B/C)**

Executed. **12 of 16 planned variables are present.** Batches A (4/4), B (6/6) and C (2/2) are
complete. **#13 mobility, #14 wealth and #15 healthcare access are fully absent** — no gravity
in-flow or centrality features, no Meta RWI or its nightlights+built-up fallback, no travel-time or
distance-to-facility surface, and no corresponding rasters in quarantine.

The audit was unambiguous because there is no selection history to reconstruct: 92 features, L2
only, **no feature-selection step, 0 of 92 coefficients zero**, so candidate set, design matrix and
fitted set are one object. Cross-checked against the 101-column weekly table — the 9 unfitted
columns are 6 keys and 3 staleness diagnostics. Nothing was built as a candidate and dropped.

**One wrinkle, flagged rather than buried.** `frac_crops` *is* in the matrix and cropland is #16. It
is not evidence that Batch D ran: it is one of seven Impact Observatory `io-lulc-annual-v02` class
fractions co-extracted wholesale by notebook 03 (Batch B); §6.16 specifies ESA WorldCover, not
Impact Observatory; and §6.16's **EVI phenology amplitude** — the seasonal max−min paddy-intensity
proxy, the mechanistically motivated half — was never built. Recorded as `partial`, not as a
deliverable. Two further departures are in the manifest: the land-cover product substitution
throughout, and §6.9's optional UHI rural-ring variant not being built.

**Naming adopted:** `M6-core (A/B/C)` everywhere downstream. If Batch D is added it becomes
`M6-extended`, versioned separately. Historical M6 is not redefined.

- `analysis/geomatics_integration_v1/M6_BATCH_D_AUDIT.md`
- `analysis/geomatics_integration_v1/M6_CORE_FEATURE_MANIFEST.yaml`
- `scripts/m6_batchD_feature_audit_v1.py` — generated from the artifacts, not transcribed; raises on
  any unassigned column, so it cannot drift from a re-fit design matrix.

### One addition proposed to §7

§7 rightly forbids *"geomatics adds no value beyond surveillance."* The audit makes a second
constraint necessary: **the three absent variables are mobility, wealth and healthcare access** —
precisely the ones most plausibly tied to human exposure and to *reporting* behaviour. AUC 0.601 is
therefore a null for **terrain, land cover and remotely-sensed dynamics**, not for geomatics as a
category. Suggested for the not-allowed list: *"geomatics carries little decision value"* without
the A/B/C qualifier.

---

## 2. §6 — M6-core frozen

`analysis/geomatics_integration_v1/M6_CORE_FROZEN_MANIFEST.yaml`, generator
`scripts/m6_core_freeze_manifest_v1.py`. Carries notebook blob hashes at `ff6287d` (committed blobs,
not the working tree), row counts, test row-key hash `9db1c932d37a63be`, model config and selected
`C`, both calibration schemes with the Platt coefficients, bootstrap seed and B, the MODIS gap rule
with its sensitivity, and input / output / figure hashes. Headline numbers are recorded there so
they are never restated from a second source.

---

## 3. §3 — your target-provenance concern is correct, and here is its size

Accepted without qualification. The recovery was described in the PI note as sidestepping the
threshold problem; on your framing it does not, and the earlier wording was too strong. The chain
you set out —

`test labels → feasible interval → selected threshold → training labels → M6 fit`

— applies to the subset where the empirical train quantile fell **outside** the feasible interval
and was clamped to it. Quantified:

| | count | share |
|---|---|---|
| threshold district-years total | 208 | — |
| ...set by empirical train q75 (unaffected) | 168 | 80.8% |
| ...**clamped to the frozen-outcome interval** | **40** | **19.2%** |
| districts with any clamped year | **5** | Killinochchi, Matara, Polonnaruwa, Puttalam, Ratnapura |
| **test rows resting on a clamped threshold** | **755 of 3,926** | **19.2%** |
| test events on a clamped threshold | 200 of 1,321 | 15.1% |

So roughly a fifth of the evaluation rests on thresholds informed by the test outcomes, concentrated
in 5 of 26 districts across all 8 years. The remaining four fifths are train-only. Status is recorded
as **`EXPLORATORY_RECONSTRUCTED_TARGET`** in the frozen manifest pending Route A or B, and the result
will not be described as an independent recovery of the frozen target.

**Route A is the ask (§5 below).** If the original threshold artifact exists on the original build
machine, this closes outright and the tag is removed.

---

## 4. A provenance gap found while freezing — not previously recorded

**The threshold generator is not committed.** `m6_label_thresholds_srilanka_v1.csv` defines the
model target, but **no committed code produces it**: notebook 06 only consumes it via
`THRESHOLDS_CSV`, and notebook 05 stopped before constructing a label. The WorldPop year-ratio
recovery ran as ad-hoc session code and was never written to `scripts/` or a notebook.

By §25 this is a stop condition — provenance cannot establish which artifact produced the target.
Related and minor: `nb05_provenance.json` still reads *"STOPPED … label NOT constructed"*,
predating the recovery, though its rowset hash is still correct.

### The port was attempted, and it is BLOCKED

`scripts/m6_threshold_recovery_v1.py`. It verifies and writes nothing, so no competing threshold
table can be mistaken for the frozen one. The outcome splits cleanly:

| half of the procedure | reproduces? |
|---|---|
| feasible-interval solver + clamp rule | **exactly** — 26/26 non-empty intervals, all 26 frozen `K` inside their own interval, all **5 clamped districts on the lower bound to 1e-12** |
| empirical train q75 | **no** — best **10 of 21** districts |

The 10/21 is across {2 year bases} × {6 train row-set definitions} × {5 interpolation modes}. I
stopped there deliberately. The diagnostic says the method is right and the row set is wrong:
`K` is an **exact observed train ratio in 21 of 21 districts**, at quantile level **0.733–0.765** —
so it *is* the empirical ~75th percentile of train `cases/WorldPop`. But `K` sits at a **varying
rank (187–195 of 255)**, where a fixed quantile rule on this series must give a fixed rank. That
implies the original train row set differed from anything recoverable here by a few rows. Enumerating
definitions until one matched would be the improvisation §25 forbids, and would manufacture a
provenance rather than establish one.

**Worth naming plainly:** the **19.2% of the target that is test-informed reproduces exactly; the
80.8% that is train-only does not.** The half with the provenance problem is the half we can verify.

This does not disturb the result — the frozen thresholds are unchanged and notebook 06's acceptance
test still passes 3,926/3,926. What is lost is the ability to regenerate the target from committed
code, which makes **Route A the only clean resolution** and raises the priority of §5.1 below.

---

## 5. What I need from you

1. **The original Sri Lanka threshold artifact, and the v2.0 frozen training panel** (§3 Route A,
   §4). **Now the only clean resolution**, since the port established that the train-only half of
   the target cannot be regenerated from committed artifacts. Either the threshold table itself, or
   the original training panel — the latter would let Route B recompute the quantile on the correct
   rows and would also resolve the 26-row difference from the 2018 wk4 image-only PDF. If neither
   exists, saying so is equally useful: Route C then applies permanently, and I would rather carry
   that tag early than discover it at submission.
2. **M0 / M1 / M2 test predictions on the identical 3,926 rows**, or your confirmation to write the
   §9 Option B deviation note. Either is workable; the choice is yours.
3. **§7 addition** above — confirm or reject the A/B/C qualifier.
4. **Still outstanding from the 2026-08-07 PI note §5.4: a free CDS API key.** `instruction_m6.md`
   does not mention it. I am treating it as self-service and registering, since §24 item 11 (WP5
   climate staging) cannot start without it and the download queue is long. Flag if you would rather
   it went through an institutional account.

---

## 6. §24 status

*(updated 2026-08-11 — see the addendum below)*

| item | state |
|---|---|
| 1 · freeze `ff6287d` outputs and hashes | **done** |
| 2 · feature audit; label M6-core if Batch D absent | **done** — Batch D absent |
| 3 · target-provenance report | **done** — `M6_TARGET_PROVENANCE.md` |
| 4 · recover original threshold / training artifact | **blocked on §5.1** |
| 5 · feature-lock chronology | **done** — `M6_FEATURE_CHRONOLOGY.md`; no lock existed, none manufactured |
| 6 · nomenclature registry | **done** — `docs/MODEL_NOMENCLATURE_REGISTRY_v44.md` |
| 7 · M0/M1/M2 recovery or deviation note | **blocked on §5.2** |
| 8 · define/freeze matched geomatics base | **`MATCHED_GEOMATICS_ABLATION = BLOCKED`** — no base design matrix exists in the repo |
| 9 · run the matched comparison | blocked by item 8 |
| 10 · WP4 buffered-LOOCV performance | blocked — needs the registered reference model |
| 11 · WP5 climate exposure staging | blocked on a CDS key (§5.4) |
| 12 · fractional WorldPop/boundary sensitivity | **done** — `wp5_worldpop_coastal_sensitivity_report_v1.md` |
| 13 · MODIS-backfill sensitivity | blocked on a NASA Earthdata login (self-service, being obtained) |
| 14 · claim-to-artifact provenance table | queued — needs 4, 7, 10, 11 |
| 15 · integrate into v44 | gated on all of the above |

The threshold-generator port was attempted ahead of item 3 and is **BLOCKED** (§4 above);
`scripts/m6_threshold_recovery_v1.py` carries what recovered, with the interval and clamp
reproduction asserted as a permanent regression test. Item 3's report was written against that
outcome rather than against an assumed-clean port.

---

# Addendum — 2026-08-11

Delayed delivery: this memo was written on 2026-08-07 and, through an oversight on my side, was not
committed or posted until today. Four items have advanced since, and one question has appeared that
did not exist when it was drafted.

## A. §24 item 5 — feature-lock chronology: **no lock existed, and I have not manufactured one**

`analysis/geomatics_integration_v1/M6_FEATURE_CHRONOLOGY.md`. §5's prescribed sentence is adopted
verbatim and `M6_CORE_FEATURE_LOCK.yaml` is deliberately **not** created.

Two facts are recorded next to it because they are commit-provable and they bound how post-hoc the
result is:

- the **A/B/C/D feature specification was committed 2026-07-17** (`baebaf7`, `docs/M6.md` §6), three
  weeks before first outcome access and first fit;
- the **reduction to A/B/C was logged 2026-08-05**, one day *before* first outcome access — so the
  narrowing was not a response to seeing performance. All four deviations from the spec (Batch D
  absent, #16 partial, land-cover product substitution, §9.5 gate abandoned) likewise predate it.

First outcome access is notebook 05; first fit is notebook 06 (2026-08-07 13:43); the freeze
manifest was written at 21:30, after performance was seen. **No feature definition changed after
outcome access** — verified cell-by-cell against the `ff6287d` blobs rather than asserted.

Three limits keep this a *specification*, not a *lock*, and they are stated in the document: (1)
notebooks 04–08 entered git in a single post-fit commit, so the ordering rests on notebook-written
provenance JSONs rather than commit boundaries; (2) I had access to the study's own outcome data
throughout, which no chronology can undo; (3) 19.2% of the target is itself test-informed (§3
above). **`M6-core` remains post-hoc exploratory.**

## B. §24 item 6 — nomenclature registry

`docs/MODEL_NOMENCLATURE_REGISTRY_v44.md`. The collision is sharper than a repeated letter:
Colombia's pilot **M6 = cases + SPI** is a *hybrid*; Sri Lanka's **M6 = geomatics-only** is a
*standalone with no case history*. Opposite in kind. Rule proposed: **bare `M6`/`M7` never appear in
v44**, nothing historical is renamed, descriptive names only. Two further traps are registered —
`M5-no-climate` (frozen, exists) versus `M5_NO_GEO` (blocked, does not exist); and Sri Lanka's M1
carries seasonal harmonics and RDHS fixed effects where Colombia's does not, so any cross-country
"M1" sentence is false without the country qualifier.

## C. §24 item 8 — `MATCHED_GEOMATICS_ABLATION = BLOCKED`, with the reason established

§8 requires `BASE + GEOMATICS` versus `BASE WITHOUT GEOMATICS` sharing rows, machinery and
protocol. The repository holds only M5 **predictions** — `ALT_STATS/frozen/srilanka_matched_pairs.csv`
carries `full_raw`, `noclim_raw`, `full_recal`, `noclim_recal` and no features. **There is no base
design matrix to add a geomatics block to.** Marked BLOCKED per §8 rather than substituted with
M6-vs-M5 renamed, which §8 explicitly forbids. It is resolved by the same artifact as §5.1 below —
one more reason that ask is the critical one.

## D. A question that did not exist on 2026-08-07 — is geomatics in Paper 1 or not?

PR **#8** (`agent/v44-hybrid-light-decision-framework`, 2026-08-10) states in
`FINAL_CANONICAL_DECISION.md` that M6/WP4/WP5 *"remain separate and outside Paper 1 evidence."* I
read that as a **consequence of the §22 gates being open**, not as a scientific rejection — the pass
was formalisation-only and carried an explicit "no M6/WP4/WP5 promotion" restriction, and
`SOURCE_MANUSCRIPT_RESOLUTION.md` §9 confirms the canonical v44 contains zero geomatics tokens
already. On that reading it is consistent with the PI's 2026-08-07 approval on PR #1, which admits
geomatics *in principle* while §24 item 15 admits it *after* the gates.

What makes it urgent is the schedule, not the wording: `V44_VS_BIOMATH_DECISION_MEMO.md` records
that **no further analysis is required to submit Paper 1** and that the remaining blockers are
author-owned. So Paper 1 can go out at any time, and three of the gates that would admit geomatics
are blocked on inputs I cannot supply.

**The question, plainly: should the geomatics workstream be planned as Paper 2?** If yes, that is a
clean answer and I will re-plan WP4/WP5 around it — and §5.1's ask stops being urgent, because a
separate paper can construct its own target rather than recovering the frozen one. If the intent is
still Paper 1, then items 4 and 7 need the artifacts below before Paper 1 submits, and it would help
to know the intended submission window. Either answer is workable; not knowing which is the only
thing that makes the ask urgent.

## E. Still outstanding, unchanged

§5.1 (original threshold artifact / v2.0 training panel — now also the only route to unblocking §8)
and §5.2 (M0/M1/M2 predictions on the identical 3,926 rows, or approval to write the Option B
deviation note). §5.4's CDS key is being handled self-service, along with a NASA Earthdata login for
the 2025 MODIS backfill (§11) — that gap covers 442 test rows, 11.3%, and cannot be dropped without
tripping §11's identical-rows STOP.
