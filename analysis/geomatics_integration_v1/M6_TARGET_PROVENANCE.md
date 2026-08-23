# M6-core target provenance — how the labels were made, and what that costs

**Instruction:** `instruction_m6.md` §3 (+ §24 item 3) · **Date:** 2026-08-07 · **Scope:** Sri Lanka
**Verdict:** **`EXPLORATORY_RECONSTRUCTED_TARGET`** — Route C applies until Route A or B is supplied.
**Artifacts:** `M6_CORE_FROZEN_MANIFEST.yaml` · `scripts/m6_threshold_recovery_v1.py`

---

## 1. The claim being examined

The M6 label is *elevated activity*: for district `d` and week `t`,

```
label(d, t) = 1  iff  cases(d, t + 28 days) > thr(d, y)
```

where `thr` is the per-district 75th percentile of **training** incidence, expressed in count space.
The original threshold table for Sri Lanka was not available, so it was **reconstructed**. The
reconstruction reproduces the frozen test outcomes **3,926 / 3,926 = 1.000000**.

The 2026-08-07 PI note described that as sidestepping the threshold problem. **On §3's framing it
does not, and that wording was too strong.** This report sets out what the reconstruction actually
establishes and what it does not.

## 2. How the thresholds were derived

The threshold is a fixed *incidence*, so in count space it scales with population:

```
thr_count(d, y) = K(d) × WP(d, y)
```

with `WP` the WorldPop G2 R2025A constrained annual series (public download; the 2024 national total
computes to 23,008,641 against the original build report's 23,008,642 — one person apart, confirming
the same release). `K(d)` is the district's threshold incidence, and is the only free parameter.

`K(d)` was set in two steps:

1. **A feasible interval from the frozen TEST outcomes.** Each test row constrains `K`:
   `outcome = 1` implies `K < cases/WP`; `outcome = 0` implies `K ≥ cases/WP`. Intersecting these
   gives `K ∈ [max over 0-rows, min over 1-rows)`. All 26 districts admit a non-empty interval —
   78 constraints satisfied by 26 free parameters, which is not trivially satisfiable and is a
   genuine validation of the *rule*.
2. **A value inside it.** `K` is the empirical 75th percentile of **train** `cases/WP` where that
   lands inside the interval (21 districts), and **clamped to the interval's lower bound** where it
   does not (5 districts).

## 3. The dependency §3 identifies — quantified

Step 1 uses test labels. For the 21 districts where step 2's train quantile already fell inside the
interval, the interval merely *confirmed* a train-only quantity. For the 5 clamped districts it
**determined** it. The chain

```
test labels → feasible interval → selected threshold → training labels → M6 fit
```

is therefore live for the clamped subset. This is not predictor leakage; it is **test-dependent
target reconstruction**, and its size is:

| | count | share |
|---|---|---|
| threshold district-years, total | 208 | — |
| ...set by the empirical train q75 (train-only) | 168 | 80.8% |
| ...**clamped to the frozen-outcome interval** | **40** | **19.2%** |
| districts with any clamped year | **5 of 26** | Killinochchi, Matara, Polonnaruwa, Puttalam, Ratnapura |
| **test rows resting on a clamped threshold** | **755 of 3,926** | **19.2%** |
| test events on a clamped threshold | 200 of 1,321 | 15.1% |

All 5 clamped districts are clamped in **all 8 years** — clamping is a district-level property, not
a year-level accident, because `K` is a single per-district parameter.

**Reading:** about one fifth of the evaluation rests on thresholds informed by the test outcomes,
concentrated in one fifth of the districts. Four fifths is train-only. The `1.000000` acceptance
figure is a genuine verification of *internal consistency* but is **not** evidence of independence
from the test labels, and must not be quoted as if it were.

## 4. The generator is not in version control

`m6_label_thresholds_srilanka_v1.csv` defines the target, but **no committed code produces it**.
Notebook 06 only consumes it via `THRESHOLDS_CSV`; notebook 05 stopped before constructing a label.
The recovery ran as ad-hoc session code. Under §25 this is a stop condition in its own right:
provenance cannot establish which artifact produced the target.

**The port was attempted** — `scripts/m6_threshold_recovery_v1.py`, which verifies and deliberately
writes nothing, so no competing table can be mistaken for the frozen one. It half-succeeds:

| half of the procedure | reproduces? |
|---|---|
| feasible-interval solver + clamp rule | **exactly** — 26/26 non-empty intervals; all 26 frozen `K` inside their own interval; all 5 clamped districts on the lower bound to within 1e-12 |
| empirical train q75 | **no** — best **10 of 21** districts |

The failing half was searched across {2 year bases} × {6 train row-set definitions} × {5
interpolation modes} and halted there per §25, because the diagnostic is already conclusive about
*where* the discrepancy lives:

- `K` is an **exact observed train ratio in 21 of 21 districts**;
- at quantile level **0.733–0.765** (median 0.749) — so the method is confirmed as the empirical
  ~75th percentile of train `cases/WP`;
- but at a **varying rank, 187–195 of 255**, where a fixed quantile rule on a fixed series must
  give a fixed rank.

That combination means the **formula is right and the row set is wrong** — the original code used a
train set differing from any recoverable here by a few rows. Continuing to enumerate definitions
until one matched would manufacture a provenance rather than establish one.

**The asymmetry is worth stating plainly: the 19.2% that is test-informed reproduces exactly; the
80.8% that is train-only does not.** The half of the target with the provenance problem is the half
whose construction can be verified.

## 5. What this does and does not affect

**Does not affect:**
- the frozen thresholds themselves — unchanged, hashed in the freeze manifest;
- notebook 06's acceptance gate — still 3,926/3,926, asserted before fitting;
- the honest-null conclusion — §26's question 10 stays *yes*, and the interpretation does not turn
  on the target's provenance;
- the 80.8% of district-years whose thresholds are train-only.

**Does affect:**
- any claim of end-to-end reproducibility — currently false, and must not be written;
- any description of the reconstruction as an independent recovery of the original frozen target —
  it is not, and the PI note's wording is superseded by this report;
- the 5 clamped districts, whose training labels are partly determined by test outcomes.

## 6. Routes out, in order of preference

**Route A — the original threshold artifact.** Locate the table that produced the original Sri Lanka
labels; record path, hash, creation commit, threshold definition, and the row mask used. Then confirm
3,926/3,926 with no test-informed fitting anywhere in the chain. **Closes the issue outright.**

**Route B — the original frozen training panel.** If the threshold table is gone but the training
panel survives (with its outcome-, exposure- and population-missing masks and the 2018–2022 rows),
the quantile can be recomputed on the correct rows. Given §4's finding — right formula, wrong rows —
**Route B is very likely sufficient**, and would also resolve the 26-row training difference from the
2018 wk4 image-only PDF.

**Route C — neither is recoverable.** Keep the present reconstruction, tag it
`EXPLORATORY_RECONSTRUCTED_TARGET` wherever M6-core is reported, and state that the threshold
reconstruction was constrained by frozen test labels for 5 of 26 districts and 19.2% of test rows.
Do not describe it as an independent redevelopment, and do not restate the chronology to make it
look prespecified.

**Current status: Route C, provisionally.** Route A/B requested 2026-08-07
(`docs/m6_instruction_response_2026_08_07.md` §5.1). Route C's tag is applied in the interim rather
than after a failed recovery, so no artifact is ever unlabelled.

## 7. §22 checklist entry

| item | status |
|---|---|
| target-provenance issue | **REVIEW** — quantified, disclosed, tagged; resolvable only via Route A/B |
| result-to-artifact provenance (target) | **BLOCKED** — generator not reproducible from committed code |
