# M6 feature-lock chronology — was the feature set fixed before the outcome was seen?

**Instruction:** `instruction_m6.md` §5 (Ganesh Shiwakoti, 2026-08-07) · §24 item 5 · **Executed:** 2026-08-11
**Scope:** Sri Lanka, `M6-core (A/B/C)` · **Source commit:** `ff6287d0e336ab4e3a3d178593d3bb28e3f33a21`
**Companions:** `M6_BATCH_D_AUDIT.md` · `M6_CORE_FROZEN_MANIFEST.yaml` · `M6_TARGET_PROVENANCE.md`

---

## Verdict

**No formal pre-outcome feature lock existed.** No `M6_CORE_FEATURE_LOCK.yaml` is created by this
document, and none should be created retroactively.

The wording required by §5 applies, and is adopted verbatim for manuscript and correspondence use:

> The feature set was developed before/alongside the outcome-stage workflow but was not formally
> cryptographically frozen before all outcome access; therefore M6 remains post-hoc exploratory.

Two facts are recorded alongside it, because they are commit-provable and they bound how post-hoc
the result actually is:

1. A **feature specification** — the A/B/C/D batch design, all 16 variables — was committed on
   **2026-07-17**, three weeks before the first outcome access and the first model fit. It is not a
   lock, but it is not a reconstruction either.
2. The **scope reduction to A/B/C** (Batch D not built) was recorded in the decision log on
   **2026-08-05**, one day *before* the first outcome access. The narrowing was not a response to
   seeing performance.

What is missing, and what makes this a specification rather than a lock: no hash-committed
statement of the **exact fitted column set** exists from before outcome access. The 92-column design
matrix is knowable only from artifacts produced on 2026-08-07, after the label was constructed.

---

## Timeline

Times are the commit author time (EDT) or the executed notebook's file mtime, as marked.

| # | Event | Evidence | When |
|---|---|---|---|
| 1 | **A/B/C/D feature specification first committed** — `docs/M6.md` §6 per-variable recipes, 16 variables in four batches | commit `baebaf7` | 2026-07-17 12:57 |
| 2 | Notebooks **00** (spatial frame) and **01** (Batch A terrain) first committed | commit `c0600d1` | 2026-08-05 14:16 |
| 3 | **Batch D recorded as not built**, and §9.5's A+B interim gate recorded as structurally unrunnable | `docs/study_decision_log.md`, entry 2026-08-05 | 2026-08-05 |
| 4 | Notebooks **02** (Batch C dynamic MODIS) and **03** (Batch B statics) first committed | commit `d815bd2` | 2026-08-05 23:50 |
| 5 | Only post-spec change to `docs/M6.md` — §12 handoff route. **No feature-definition change** | commit `c00d188` | 2026-08-05 23:54 |
| 6 | **Feature table frozen** — notebook 04 assembles the 101-column weekly table. Its provenance records **four inputs, all feature tables** (`batchA`, `batchB`, `lst`, `vi`); **no outcome input** | `nb04_provenance.json`; features `sha256_16 = 69033629d021dc39` | 2026-08-06 → mtime 2026-08-07 12:26 |
| 7 | **FIRST OUTCOME ACCESS** — notebook 05 reads the WER outcome table and the frozen test panel | `nb05_provenance.json` (`outcome_table.sha256_16 = 0ccde961edfc43e6`, `frozen_v20_sha256_16 = 99f0b9b122460c7d`) | 2026-08-06 → mtime 2026-08-07 12:26 |
| 8 | **FIRST MODEL FIT** — notebook 06 fits `M6-core` on the recovered label | `nb06_provenance.json`; mtime `notebooks/06_fit_m6.ipynb` | 2026-08-07 13:43 |
| 9 | Notebooks 04–08 first committed (all in one commit — see *Granularity limit* below) | commit `ff6287d` | 2026-08-07 14:40 |
| 10 | Artifact frozen — hashes, row counts, model config recorded. **After** the fit and **after** performance was seen | `M6_CORE_FROZEN_MANIFEST.yaml` | 2026-08-07 21:30 |
| 11 | Batch D audit — executed set established as 12/16, model renamed `M6-core (A/B/C)` | `M6_BATCH_D_AUDIT.md` | 2026-08-07 20:55 |

**First outcome access = event 7. First model fit = event 8.** Events 1–6 all precede both.

---

## Feature changes after outcome access

**None to any feature definition.** Verified rather than asserted:

- **Definitions.** The four extraction notebooks (00–03) were compared cell-by-cell against their
  committed blobs at `ff6287d`. Notebooks 00, 01 and 03 are source-identical. Notebook 02's only
  difference was one added `pip install pystac_client` cell at position 2 (an environment
  convenience from a later re-run), with every other cell unchanged and merely shifted by one index.
  Those working-tree edits were **discarded on 2026-08-11** so the blob hashes recorded in
  `M6_CORE_FROZEN_MANIFEST.yaml` remain the hashes of the files on disk. Backup retained outside the
  repo for the session.
- **Additions or removals after viewing M6 performance: none.** The design matrix is 92 features,
  L2 only, **no selection step, 0 of 92 coefficients zero** (`M6_BATCH_D_AUDIT.md`), so candidate
  set, design matrix and fitted set are one object. There is no selection history in which a
  post-hoc removal could hide. The 9 columns of the 101-column table that do not enter the model are
  6 keys and 3 staleness diagnostics — never candidate features.

---

## Deviations from the specification, and when each was decided

All four predate first outcome access (event 7). None is a response to observed M6 performance.

| Deviation | Decided | Before outcome access? |
|---|---|---|
| **Batch D not built** — #13 mobility, #14 wealth, #15 healthcare access absent | decision log 2026-08-05 | **Yes** |
| **#16 cropland partial** — `frac_crops` present incidentally via Impact Observatory class fractions; the EVI phenology-amplitude half never built | notebook 03, commit `d815bd2`, 2026-08-05 | **Yes** |
| **Land-cover product substitution** — Impact Observatory `io-lulc-annual-v02` used throughout in place of §6.16's ESA WorldCover | notebook 03, commit `d815bd2`, 2026-08-05 | **Yes** |
| **§9.5 interim gate abandoned** — "fit on A+B first" is unrunnable against a weekly label because A+B are static per district | decision log 2026-08-05 (evidence: notebook 02 §15 variance split) | **Yes** |

---

## Why this is still not a lock — the three limits

1. **Granularity limit.** Notebooks 04–08 entered git in a single commit, `ff6287d`, on 2026-08-07,
   *after* the fit. Git history alone cannot separate "assembled features" from "constructed label"
   from "fitted model" inside that commit. The separation above rests on the notebook provenance
   JSONs and file mtimes, which are weaker evidence than a commit boundary — they are written by the
   notebooks themselves and are not independently attested.
2. **Prior exposure to the study's outcomes.** The analyst had full access to the frozen matched-pair
   panel, the M5 results and the v43 manuscript throughout, from long before 2026-07-17. Independence
   from the *M6 label* is demonstrable; independence from the *study's* outcome data is not, and no
   chronology can establish it.
3. **The target itself is partly outcome-informed.** 40 of 208 district-year thresholds were clamped
   to the frozen-**test**-outcome interval, so **755 of 3,926 test rows (19.2%)** rest on
   test-informed thresholds (`M6_TARGET_PROVENANCE.md`, tagged `EXPLORATORY_RECONSTRUCTED_TARGET`).
   A feature-side lock would not repair a target-side dependency, and no claim here should be read
   as doing so.

---

## Answer to §26's first question

> *Was the feature set fixed before the outcome influenced model design?*

**Partially, and not provably.** The specification and the A/B/C scope reduction are commit-dated
before first outcome access; the exact fitted column set is not. Combined with limit 3 above,
**`M6-core` remains post-hoc exploratory** and must be reported as such.
