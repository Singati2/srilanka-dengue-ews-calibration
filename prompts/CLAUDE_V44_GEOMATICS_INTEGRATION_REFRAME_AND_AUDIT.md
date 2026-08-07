# Claude Code Execution Prompt — v44 Geomatics Integration, Experimental Reframe, and Scientific Audit Repair

## Mission

Work on the repository:

`Singati2/srilanka-dengue-ews-calibration`

The goal is **not** to cosmetically expand v43. The goal is to build a scientifically coherent **v44 integration candidate** that:

1. preserves the full history and evidence of v43;
2. repairs the false-PASS weaknesses in the Knowledge Graph + Agent Graph audit;
3. integrates the current geomatics/M6 work as a real experimental component rather than an unrelated appendix;
4. aligns the manuscript structure with the actual sequence of experiments and estimands;
5. keeps every claim bounded by what the data and code actually support;
6. never fabricates a result, reference, DOI, author declaration, data source, or successful reproduction;
7. never merges to `main` during this task.

The desired scientific reframe is broader and more coherent than a simple “climate helps / climate does not help” paper:

> **When does environmental information add useful predictive or decision value beyond recent surveillance in dengue early warning, and how do calibration, comparator structure, temporal information, spatial scale, and geomatics fidelity change that conclusion?**

This is an **incremental-information and validity-audit paper**, not a causal climate paper and not a leaderboard paper.

---

# 0. Repository state you must understand before changing anything

## 0.1 Important branches / PRs

### Main repository baseline
- Repository: `Singati2/srilanka-dengue-ews-calibration`
- Default branch: `main`
- Current relevant `main` base observed when this prompt was written: `5f203788f4259f46099a7e7617deb92e3afe43fc`

### Knowledge Graph + Agent Graph implementation
- PR #3: `KG + Agent audit: deterministic research-integrity system`
- Branch: `agent/kg-agent-implementation`
- Head observed when this prompt was written: `6c6f1b6e8f77c0b7ccf765cfdf5ae09356dd3fe4`
- This prompt branch was created **from that branch**, so the KG/Agent infrastructure should already be present here.

### Geomatics / M6 work
- PR #1: `M6 geomatics-only comparator: notebook workflow, feature extraction batches A/B/C`
- Branch: `m6-geomatics-notebooks`
- Head observed when this prompt was written: `13808979cf34719fc765f75b18ce623e5b760e59`
- Important changed files:
  - `docs/M6.md`
  - `docs/study_decision_log.md`
  - `notebooks/00_setup_and_geometry.ipynb`
  - `notebooks/01_terrain_batchA.ipynb`
  - `notebooks/02_dynamic_modis.ipynb`
  - `notebooks/03_batchB_statics.ipynb`
  - `notebooks/README.md`
  - `notebooks_requirements_lock.txt`

### Canonical pre-integration manuscript
- `manuscript_v43/revised_manuscript.tex`

**Do not overwrite or rename v43.** It is a historical evidence object.

---

# 1. Non-negotiable scientific and repository rules

## 1.1 No destructive history rewriting

- Do **not** edit `manuscript_v43/revised_manuscript.tex` in place.
- Create a new candidate directory such as:
  - `manuscript_v44/`
- Copy the v43 source into v44 and edit only the v44 copy.
- Preserve analysis chronology and labels such as:
  - internally design-locked;
  - post-result design-locked;
  - post-hoc exploratory;
  - sensitivity;
  - diagnostic;
  - reviewer-responsive.
- Do not relabel any post-hoc work as preregistered, prospective, confirmatory, primary, or externally validated.

## 1.2 No data leakage into Git

Never commit:
- raw rasters;
- surveillance row-level data;
- geomatics feature tables derived from private/quarantined data;
- model prediction rows if repository policy quarantines them;
- large binary raster products;
- tokens, credentials, API keys, personal paths, or secrets.

Use the repository’s existing quarantine discipline.

Commit only safe code, metadata, checksums where permitted, notebooks already approved for review, aggregate summaries, figures safe for publication, provenance manifests, and manuscript material.

## 1.3 No invented completion

If an experiment cannot be executed because data or an outcome table is not locally available:

- do not fabricate results;
- do not infer numeric results from prose;
- do not silently substitute a different sample;
- do not claim the experiment passed;
- write a precise blocker;
- continue all independent work that can still be completed.

## 1.4 No automatic scientific PASS from shallow presence checks

The current KG/Agent system is useful infrastructure but its PASS semantics are too strong.

A gate may be marked `PASS` only when the code actually verifies the intended property.

If the tool merely checks for the **presence of a lockfile, checksum, keyword, DOI-shaped string, manuscript sentence, or coding pattern**, the appropriate status is generally one of:

- `REVIEW`
- `PARTIAL`
- `NOT_VERIFIED`

not `PASS`.

Do not write “no scientific defect” unless the repository evidence supports that statement after the deeper checks below.

---

# 2. First action — establish an integration branch and import geomatics work safely

Start from the branch containing this prompt.

Before changes:

```bash
git status -sb
git remote -v
git branch --show-current
git log --oneline --decorate -8
```

Fetch all relevant refs:

```bash
git fetch --all --prune
```

Verify that the KG/Agent implementation and geomatics heads resolve.

Create a new implementation branch, for example:

```bash
git checkout -b agent/v44-geomatics-integration
```

Do **not** merge to `main`.

Import the PR #1 geomatics files from commit `13808979cf34719fc765f75b18ce623e5b760e59` or the current verified head of `m6-geomatics-notebooks`.

Because PR #1 may conflict with files already changed elsewhere, do not blindly merge and resolve by accepting one side wholesale. Inspect conflicts. The scientific decision log must retain both histories.

After import, run:

```bash
git status --short
git diff --check
```

Confirm that no quarantined data, raster, credential, `.pyc`, temporary file, or machine-specific artifact was newly added.

---

# 3. Repair the Knowledge Graph + Agent Graph before trusting it

The current implementation has already demonstrated a false PASS.

## 3.1 Known contradiction that must become a regression test

The current v43 manuscript contains an internal contradiction around development-inclusive proper-score intervals.

One Methods passage says, in substance, that development-inclusive proper-score intervals were **“gated and not computed.”**

A later Results passage reports development-inclusive proper-score intervals, including approximately:

- Sri Lanka ΔNLL: `-0.0403 to +0.0040`
- Sri Lanka ΔBrier: `-0.0153 to +0.0013`
- Colombia ΔNLL: `-0.0224 to -0.0002`
- Colombia ΔBrier: `-0.0102 to -0.0004`

The existing contradiction detector missed this because it searched for one exact literal sentence rather than the semantic contradiction.

### Required fix

Implement a robust deterministic rule that detects variants such as:

- “not computed”
- “were gated and not computed”
- “not available”
- “not re-executed”

when the same manuscript/repository contains a corresponding reported result set.

Add a regression test that fails on the v43 contradiction and passes only after the v44 text is internally consistent.

Do not simply hard-code one line number.

## 3.2 Status semantics

Extend the agent status vocabulary if necessary. Suggested statuses:

- `PASS`
- `REVIEW`
- `FAIL`
- `NOT_VERIFIED`

Use `PASS` only for properties that are actually demonstrated.

Examples:

### Reproducibility
A lockfile + checksum existence check is **not** enough for `REPRODUCIBILITY = PASS`.

A strong PASS should require, where feasible:
- a clean checkout or controlled environment;
- executable reproduction commands;
- successful command exit status;
- expected artifact/hash/value checks;
- explicit handling of unavailable private/quarantined inputs;
- documented exact-head evidence.

If full recomputation is impossible because data are quarantined, report `PARTIAL`/`NOT_VERIFIED` rather than PASS.

### Reference integrity
Undefined LaTeX keys are not the same as scientific reference verification.

Separate:
- citation-key integrity;
- DOI/metadata verification;
- claim-support verification.

If network access is available, verify high-stakes references against primary or authoritative metadata sources. If network access is unavailable, mark scientific support as `NOT_VERIFIED`; never infer that a citation supports a claim merely because the key exists.

### Temporal leakage
Do not equate absence of `.interpolate()` or `bfill` with absence of leakage.

A strong leakage audit must inspect:
- target horizon construction;
- train/validation/test date boundaries;
- threshold construction;
- scaling/tuning fit windows;
- climate/remote-sensing composite availability dates;
- lag construction;
- recalibration windows;
- imputation direction;
- outcome availability relative to forecast origin.

### Numerical traceability
A value match based only on a decimal token appearing somewhere in a file is insufficient.

Where possible, link each manuscript result to:
- metric name;
- model/comparator;
- setting;
- state (raw/recalibrated);
- horizon;
- threshold;
- point estimate;
- uncertainty interval;
- generating script;
- result artifact;
- commit/tag/checksum.

## 3.3 New tests

Add tests for at least:

1. the v43 proper-score contradiction;
2. a fabricated manuscript sentence with a valid citation key but unsupported/unknown scientific verification status;
3. a lockfile/checksum-only reproducibility case that must not receive a strong PASS;
4. a MODIS composite whose start date is before forecast week but end date extends past forecast origin — this must be flagged as leakage if joined by start date;
5. traceability collisions where the same four-decimal number appears in unrelated results;
6. one clean fully supported result lineage that does receive PASS.

The tests should verify scientific gate meaning, not only that functions return legal strings.

---

# 4. Author decision granted by this prompt

The author is explicitly deciding to **include the geomatics work in the paper**, subject to scientific completion and honest labeling.

Therefore:

- M6/geomatics is no longer merely an ignored optional side project.
- It should be integrated into the v44 scientific architecture.
- It remains **exploratory** unless the repository contains evidence justifying a stronger status.
- The paper must not imply that geomatics was part of the original frozen primary model ladder.
- The addition must be described in the analysis chronology.

This author decision resolves the “do we include M6?” framing question.

It does **not** authorize fabrication, outcome-driven feature selection, or retrospective relabeling.

---

# 5. Scientific reframe for v44

## 5.1 Core thesis

Reframe the paper around the following hierarchy:

> Dengue early-warning models can appear to benefit from environmental information depending on the comparator, calibration state, threshold, uncertainty target, temporal information content, and spatial aggregation. We evaluate environmental information as a set of bounded feature blocks rather than as a single causal construct, using recent surveillance as the operational benchmark, matched climate ablation to isolate incremental climate information, and geomatics/spatial experiments to test whether landscape and remotely sensed context add independent signal or expose spatial-scale limitations.

Do not copy that sentence mechanically if the evidence suggests better wording, but preserve its scientific logic.

## 5.2 Strong contribution that v44 may support

The paper should aim to make the following contribution, only to the extent verified:

1. **Comparator discipline** — separate a non-nested “hybrid versus surveillance” comparison from a matched feature-block ablation that more cleanly isolates incremental climate information.
2. **Calibration-aware evaluation** — show that discrimination alone is not enough; proper scores and decision value depend on calibration and the uncertainty target.
3. **Environmental-information decomposition** — distinguish reanalysis weather/climate features from geomatics/remote-sensing landscape information rather than treating “environment” as one block.
4. **Spatial-scale audit** — use geomatics findings, WP4 spatial validation, and WP5/MAUP work to show how administrative aggregation and exposure construction affect what environmental signals can be observed.
5. **Honest near-null / modest-effect interpretation** — do not force a positive story. Small or unstable environmental increments are scientifically meaningful when they are demonstrated under matched comparisons.

## 5.3 What v44 must NOT become

Do not frame the paper as:

- “AI predicts dengue using satellite data”;
- “climate causes dengue outbreaks”;
- “geomatics improves dengue prediction” before the experiment proves it;
- “external validation across Sri Lanka and Colombia”;
- “national generalizability”;
- “operational deployment”;
- “quantified public-health impact / cases prevented”;
- “first ever” unless independently verified by literature review.

---

# 6. Organize the manuscript around experiments

The manuscript should map every major claim to an explicit experiment.

Create:

`manuscript_v44/EXPERIMENT_CLAIM_MATRIX.md`

with columns such as:

| Experiment | Scientific question | Models/features | Setting | Rows | Horizon | Threshold | Calibration state | Metric | Uncertainty | Analysis status | Result source | Allowed claim |

At minimum define:

## Experiment 1 — Existing model ladder / operational benchmark

Question:
- How do recent-surveillance, climate-only, structured-climate, and hybrid models compare under the existing frozen evaluation?

Preserve existing model labels and country-specific differences.

The role of Experiment 1 is context and benchmark performance, not proof that climate itself is beneficial.

## Experiment 2 — Matched climate feature-block ablation

Question:
- What is the incremental contribution associated with adding the climate block when non-climate structure and development protocol are matched?

This remains the principal interpretable climate-specific contrast.

Label it post-hoc/exploratory if that is the true chronology.

## Experiment 3 — Calibration / proper-score / decision-value robustness

Question:
- Does the apparent increment persist across calibration state, threshold-free proper scores, conditional uncertainty, and development-inclusive uncertainty?

Resolve all contradictions between Methods and Results before release.

## Experiment 4 — Geomatics-only environmental comparator (M6)

Question:
- Does a pre-specified set of spatial and remotely sensed environmental variables carry standalone predictive or decision information at the chosen administrative/time scale, and how does that compare with season/climate/surveillance baselines?

This is exploratory.

## Experiment 5 — Spatial validity / MAUP / exposure construction

Question:
- How sensitive are environmental associations/predictions to spatial aggregation, population weighting, spatial holdout, and known geomatics fidelity limitations?

WP4/WP5 results belong here if actually executed.

If WP4/WP5 remain incomplete, include only verified geomatics diagnostics and state the missing experiment explicitly.

---

# 7. Integrate and complete M6 without outcome-driven redesign

## 7.1 Read the geomatics evidence before modeling

Read completely:

- `docs/M6.md`
- `docs/study_decision_log.md`
- all four existing M6 notebooks
- `notebooks/README.md`
- `notebooks_requirements_lock.txt`

The following decisions/findings are already part of the project history and must be preserved unless disproven by code:

### Static features cannot express “when”
Terrain, built environment, population, fragmentation, static water, and similar features may vary between areas but not between weeks.

Therefore a weekly static-only M6 cannot be interpreted as a fair temporal early-warning model.

Do **not** report a static-only near-chance weekly result as evidence that geomatics has no signal.

If a static-only diagnostic is retained, use an explicitly cross-sectional/spatial target or describe it only as a “where” diagnostic.

### MODIS leakage rule
For an 8-day or 16-day composite, use the **composite end date**, not the start date, to determine availability at forecast origin.

Only composites fully available by the forecast origin may enter a predictor.

Past-only gap filling is mandatory.

### Land-cover vintage
The notebooks found implausible year-to-year class relabeling relative to net change.

Do not feed annual land-cover classification noise into the weekly model as if it were real urbanization.

Use the already documented single-epoch strategy unless a pre-outcome methodological reason and new validation justify changing it.

### UHI / MAUP finding
At the 26-RDHS scale, built-up versus daytime-LST correlation is approximately near zero while other cross-product relationships remain strong.

Interpret this as a **scale/aggregation result**, not evidence that urban heat islands do not exist.

Never convert “not visible at this areal unit” into “no urban effect.”

### WorldPop coastline shortfall
The current center-in-polygon aggregation loses roughly 3.5% of national population and disproportionately affects coastal units.

Before WP5 uses this denominator, compare at least:
- existing center-based assignment;
- a defensible fractional-coverage / area-weighted alternative or other principled coastal correction.

Choose the primary denominator on methodological grounds **before inspecting downstream predictive performance**. Preserve the other as sensitivity.

### Data vintages
Document the actual coverage:
- land cover through ~2023;
- population through ~2020 in the current source;
- HREA/nightlights through ~2019;
- surface water effectively a fixed epoch.

Do not pretend these layers are contemporaneous through 2025.

## 7.2 Freeze the M6 feature specification before outcome access

This is essential.

Before joining any dengue outcome/prediction table, create a machine-readable and human-readable feature specification, e.g.:

- `analysis/geomatics_integration_v1/M6_FEATURE_LOCK.json`
- `analysis/geomatics_integration_v1/M6_FEATURE_LOCK.md`

The lock must contain:

- feature names;
- source product;
- static/dynamic status;
- spatial aggregation rule;
- temporal availability rule;
- lag rule;
- missingness rule;
- transformation/standardization rule;
- whether the feature is included or excluded and why;
- checksum of the frozen feature manifest;
- timestamp and git commit.

Do not select features based on test-set performance.

If Batch D is incomplete, do **not** silently redefine the original full M6 after seeing outcomes.

Instead, define a clearly named pre-outcome subset such as:

- `M6-core (validated A+B+C feature set)`

and record that Batch D was not yet available.

The subset must be locked before outcomes are joined.

If Batch D later becomes available, call the expanded model `M6-extended` and treat it as a separate exploratory sensitivity.

## 7.3 Outcome-table staging

The M6 experiment must use the **identical evaluable rows** required by the original comparison.

Before fitting, produce a row-key audit showing:

- expected row count;
- actual M6 feature row count;
- matched outcome row count;
- unmatched keys on each side;
- duplicate keys;
- date range;
- 26 RDHS units;
- train/test split;
- target prevalence.

Use exact keys, not positional joins.

If row identity cannot be guaranteed, stop the M6 performance experiment and record the blocker.

## 7.4 Model family and tuning

Use a model family that keeps interpretation of the comparator clear and avoids creating a new deep-learning contest.

Preferred default:
- penalized logistic regression / the same broad family used by the relevant existing ladder;
- standardization fit only on development data;
- regularization selected only within training/validation data;
- no test-set tuning;
- no test-driven feature elimination.

Because the terrain/static block is collinear, use regularization and report coefficient instability as a limitation. Do not interpret coefficients causally.

## 7.5 M6 evaluation

Use the same held-out period and compatible evaluation machinery.

Report at least, where already used elsewhere:

- AUC;
- PR-AUC;
- Brier score;
- NLL/log loss;
- CITL;
- calibration slope;
- ICI if available;
- decision-curve net benefit across the existing threshold grid;
- the existing illustrative reference threshold, clearly labeled as illustrative;
- comparison with alert-all / alert-none;
- conditional cluster bootstrap;
- development-inclusive refit uncertainty if computationally feasible and scientifically aligned.

At minimum compare M6 against:

- M0 / season or climatological baseline;
- M2 / climate-only where rows are comparable;
- M1 / recent surveillance as the operational benchmark;
- do not claim M6 is “better” solely from a higher AUC if calibration or decision value disagrees.

## 7.6 Static-versus-dynamic geomatics decomposition

Because static features answer “where” and dynamic remote sensing can answer “when,” predefine a diagnostic decomposition:

- `M6-core`: all locked validated geomatics features;
- `M6-dynamic`: dynamic remotely sensed features only, if scientifically coherent;
- `M6-static`: **not** treated as a weekly early-warning competitor unless the target/evaluation is explicitly cross-sectional.

This decomposition is explanatory, not a post-hoc model shopping exercise.

## 7.7 No mechanistic feature-importance claims

Do not write:
- “built-up causes…”;
- “NDVI protects…”;
- “nightlights drive…”;
- “terrain is a mechanism…”

Feature coefficients/importances in this design are predictive descriptors and are highly scale-dependent.

---

# 8. WP4/WP5 integration

Read the existing spatial/MAUP plan and related documentation before writing new code.

The v44 paper should distinguish:

- **M6**: an exploratory geomatics-only predictive comparator;
- **WP4**: spatial validation / spatial generalization stress test;
- **WP5**: MAUP / population-weighted exposure construction sensitivity.

Do not collapse these into one experiment.

## 8.1 WP4 spatial validation

If required data are available, implement the planned spatial CV/holdout protocol using the repository’s designated unit definitions.

The purpose is not to maximize performance; it is to test whether results depend on spatial information leakage or memorization of unit structure.

Report:
- exact folds/holdouts;
- number of units/events per fold;
- whether unit fixed effects are usable in a truly held-out unit;
- any required model specification changes;
- performance/calibration degradation relative to temporal holdout;
- limitations from only 26 Sri Lanka RDHS units.

Do not compare spatial CV values directly with temporal holdout values without explaining the different estimand.

## 8.2 WP5 MAUP / population-weighted exposure

If executed, WP5 should be presented as a **measurement/fidelity sensitivity**, not an accuracy booster.

Explicitly evaluate:
- areal aggregation choice;
- population weighting;
- coastline assignment sensitivity;
- any Ampara/Kalmunai split implications;
- whether environmental relationships change materially with aggregation.

The UHI-at-RDHS finding can become an important illustration of MAUP if the result is independently reproduced and framed correctly.

---

# 9. v44 manuscript structure

Create:

`manuscript_v44/revised_manuscript.tex`

and a separate:

`manuscript_v44/REFRAME_DECISION.md`

The reframe decision document must explain:

- what changed from v43;
- why the old narrative was too climate-centric or too disconnected from the actual experiments;
- what the new central question is;
- which analyses are original versus added later;
- what geomatics adds scientifically;
- what geomatics does **not** establish;
- whether the evidence is sufficient for one integrated paper or whether some geomatics material should remain Supporting Information.

## 9.1 Candidate title logic

Generate 3–5 title candidates, but do not choose a sensational title.

The preferred style should emphasize:
- dengue early warning;
- incremental environmental information;
- calibration/decision value;
- spatial scale or geomatics where warranted.

Avoid “causal,” “AI breakthrough,” “precision public health,” and “external validation.”

A reasonable conceptual direction is:

> **Environmental information beyond recent surveillance in dengue early warning: calibration, matched feature-block ablation, and spatial-scale sensitivity**

Treat that only as a direction, not mandatory final wording.

## 9.2 Abstract

The abstract must mirror the experiment hierarchy.

It should not lead with a single favorable number.

It should report:
- settings and retrospective design;
- recent-surveillance benchmark;
- matched climate ablation;
- calibration/proper-score robustness;
- geomatics experiment if completed;
- spatial/MAUP result if completed;
- bounded conclusion.

If M6 performance is incomplete, do not insert placeholders that look like results. State that the predictive geomatics comparison is not yet complete in the internal draft, and do not call the manuscript submission-ready.

## 9.3 Introduction

Rebuild the Introduction around the actual methodological gap:

1. dengue forecasting often combines recent incidence, climate, seasonality, and spatial/environmental context;
2. apparent value of an environmental block depends heavily on the comparator;
3. discrimination can mislead when calibration and decision thresholds are ignored;
4. spatial aggregation and geomatics measurement can erase or distort environmental signal;
5. therefore the scientific question is not simply whether climate correlates with dengue, but whether environmental information contributes incremental, robust, decision-relevant information beyond surveillance under realistic spatial/temporal constraints.

Do not write the Introduction as if M6 was prespecified from the beginning.

## 9.4 Methods

Organize Methods by experiments or clearly cross-reference them.

The reader should be able to answer:

- What was frozen originally?
- What was added later?
- What exactly was compared?
- What rows were used?
- What information was available at forecast origin?
- What was the calibration protocol?
- What was the uncertainty target?
- What changed for geomatics?

## 9.5 Results

Use the same experiment order as Methods.

Do not mix descriptive geomatics QC findings with predictive M6 results without signaling the difference.

A good order is:

1. dataset/sample and operational benchmark;
2. matched climate ablation;
3. calibration/proper-score robustness;
4. geomatics data-fidelity and scale findings;
5. M6 predictive results, if completed;
6. WP4/WP5 spatial robustness, if completed;
7. integrated interpretation.

## 9.6 Discussion

The Discussion should synthesize rather than defend a predetermined positive result.

Potential interpretation if supported:

- recent surveillance remains a strong benchmark;
- climate can contain modest incremental probability information under matched comparison;
- decision value is calibration- and threshold-sensitive;
- under redevelopment uncertainty, some increments weaken or become boundary-adjacent;
- geomatics contains spatial/environmental information, but whether it helps weekly warning depends on dynamic content and spatial resolution;
- coarse administrative aggregation can erase physically plausible local relationships;
- adding more environmental features is not automatically equivalent to adding operational value.

This is a stronger and more general contribution than either “climate failed” or “satellite variables improved AUC.”

---

# 10. Figures and tables for v44

Do not preserve v43 figures merely because they already exist.

Build a figure/table plan that matches the experiment hierarchy.

Potential structure, only if supported by completed results:

### Main Figure 1 — Study + experiment architecture
Show:
- Sri Lanka and Colombia;
- training/test windows;
- model ladder;
- matched climate ablation;
- geomatics branch;
- calibration/decision evaluation;
- spatial validity branch.

### Main Figure 2 — Existing benchmark / matched climate increment
Use the cleanest visualization of the primary matched climate feature-block result.

### Main Figure 3 — Calibration / proper-score / uncertainty target
Show why conditional versus development-inclusive interpretation matters.

### Main Figure 4 — Geomatics and spatial-scale result
Possible panels:
- feature groups and temporal availability;
- cross-product validation correlations;
- UHI visibility/MAUP illustration;
- M6 performance if completed.

### Main Figure 5 — Spatial/MAUP sensitivity
Only if WP4/WP5 is completed strongly enough.

If not, move incomplete material to Supporting Information.

Tables should separate:
- experimental status;
- comparator definitions;
- country-specific feature implementation;
- geomatics source/vintage/fidelity;
- main result estimates.

---

# 11. Claim discipline

For every headline sentence in Abstract, Results, Discussion, and Conclusion, create or update a claim lineage entry.

Each claim must have:

- claim text;
- analysis status;
- experiment ID;
- source script;
- source artifact;
- statistic;
- sample definition;
- uncertainty definition;
- allowed interpretation;
- forbidden stronger interpretation.

Examples:

### Allowed
“Under the matched development protocol, adding the climate block produced a small improvement in probability scoring in the selected Colombia subset.”

### Not automatically allowed
“Climate improves dengue forecasts in Colombia.”

### Allowed
“At the 26-RDHS aggregation, built-up fraction showed little correlation with district-mean daytime LST despite strong cross-product checks, consistent with a scale-dependent loss of local urban heat contrast.”

### Forbidden
“Sri Lanka has no urban heat island.”

### Allowed
“A geomatics-only model did not exceed recent surveillance on the prespecified decision metric.”

### Forbidden
“Geomatics is useless for dengue prediction.”

---

# 12. Reference verification

Do not trust existing references simply because they compile.

Create:

`audit/v44/reference_verification.md`

For every high-stakes claim, verify at least:

- citation exists;
- title/authors/year/journal are correct;
- DOI or authoritative identifier is correct where available;
- source actually supports the sentence;
- no causal claim is being sourced from an association paper;
- no “first”/novelty claim is unsupported.

If internet/network verification is unavailable, clearly mark the reference `NOT_VERIFIED_EXTERNAL` rather than PASS.

Do not invent DOI values.

---

# 13. Reproducibility and provenance for geomatics

Create a safe provenance layer that an external reviewer can understand without raw rasters.

At minimum include:

- source product IDs;
- source date/vintage;
- acquisition method;
- CRS;
- spatial aggregation method;
- QA filtering;
- temporal composite start/end handling;
- checksum for locally frozen source manifests where permitted;
- software versions;
- feature-lock hash;
- row-key audit hash;
- model config;
- seed;
- bootstrap B;
- output aggregate checksum.

Parameterize absolute paths.

The v44 audit should fail or review any new `/home/<user>/...` or `/Users/<user>/...` paths in runnable tracked code/configuration unless they occur only in clearly historical logs/examples.

---

# 14. Mandatory adversarial review council

After implementation, perform a structured review from at least these perspectives:

1. infectious-disease epidemiologist;
2. biostatistician / bootstrap and uncertainty expert;
3. calibration + decision-curve expert;
4. geomatics / remote-sensing expert;
5. spatial-statistics / MAUP expert;
6. ML reproducibility engineer;
7. scientific editor;
8. hostile skeptical reviewer looking for post-hoc reframing and overclaiming.

This narrative council does **not** replace deterministic tests.

For each reviewer, report:

- strongest contribution;
- most serious flaw;
- one claim that should be weakened;
- one missing check;
- accept / minor / major / reject recommendation;
- confidence.

Then produce a consensus section that distinguishes:

- fatal blocker;
- major revision;
- optional improvement.

Do not inflate scores.

---

# 15. Required deliverables

At the end, the branch should contain, as applicable:

## Audit repair
- updated `knowledge_graph/` code;
- updated `agent_graph/` code;
- stronger tests;
- regenerated current audit;
- explicit `NOT_VERIFIED`/`REVIEW` states where appropriate.

## Geomatics integration
- imported reviewed M6 notebooks/docs from PR #1;
- `analysis/geomatics_integration_v1/M6_FEATURE_LOCK.json`;
- `analysis/geomatics_integration_v1/M6_FEATURE_LOCK.md`;
- row-key comparability audit;
- leakage audit;
- model/evaluation code if the outcome table is available;
- safe aggregate result summaries;
- provenance manifest.

## Manuscript
- `manuscript_v44/revised_manuscript.tex`;
- `manuscript_v44/REFRAME_DECISION.md`;
- `manuscript_v44/EXPERIMENT_CLAIM_MATRIX.md`;
- updated figure/table plan;
- no destructive change to v43.

## Review / release
- `audit/v44/reference_verification.md`;
- `audit/v44/SCIENTIFIC_GATE_REPORT.md`;
- `audit/v44/EXTERNAL_REVIEW_COUNCIL.md`;
- a machine-readable v44 gate result;
- exact list of unresolved author-only items.

---

# 16. Submission-readiness gate

Do not use a single binary `SUBMISSION READY` result unless the components below are exposed separately.

Required minimum gates:

| Gate | Meaning |
|---|---|
| Repository integrity | tracked files, portability, no quarantined leakage |
| Experimental comparability | same rows/splits/targets where comparisons require it |
| Temporal integrity | no future information at forecast origin |
| Spatial integrity | geometry/CRS/unit definitions and spatial validation understood |
| Model specification | model/tuning/preprocessing match documented estimand |
| Calibration | calibration procedure and states reproducible |
| Numerical traceability | headline values linked to generating artifacts |
| Reproducibility | actual runnable evidence, not just file presence |
| Reference metadata | citation keys + metadata |
| Reference support | cited source supports the claim |
| Manuscript consistency | no internal contradiction |
| Analysis chronology | post-hoc/design-locked distinctions correct |
| Submission declarations | author-supplied declarations resolved |

If any scientific gate is unverified, do not write:

> “only paperwork remains.”

Instead say exactly what remains scientifically unverified.

---

# 17. Stop rules

Stop the affected experiment and report the blocker if any of these occurs:

1. M6 cannot be joined to the identical intended outcome rows.
2. Dynamic MODIS features require information after forecast origin.
3. Training/tuning touches test-period information.
4. A geomatics data vintage is silently substituted without documentation.
5. Static-only weekly performance is being interpreted as a full test of geomatics.
6. WorldPop weighting produces a denominator artifact that materially changes the result and has not been resolved methodologically.
7. A v44 headline number cannot be traced to a reproducible or explicitly quarantined source.
8. A reference used for a high-stakes claim cannot be verified.
9. v43 history would have to be rewritten to make the narrative appear prespecified.
10. A new “best model” is selected after inspecting test performance without a pre-outcome lock.

A stop rule blocks that experiment; it does not block unrelated audit, writing, or provenance work.

---

# 18. Final report format

Create a concise but evidence-heavy final report with these headings:

1. **Branch / commits used**
2. **What was imported from geomatics PR #1**
3. **What changed in the KG/Agent audit**
4. **False-PASS bugs fixed**
5. **M6 feature-lock status**
6. **Outcome-row comparability status**
7. **Temporal leakage status**
8. **M6 experiment results or exact blocker**
9. **WP4/WP5 status**
10. **v43 → v44 reframe summary**
11. **Claims strengthened / weakened / removed**
12. **Figures/tables changed**
13. **Reference verification status**
14. **Tests and CI**
15. **Scientific gate table**
16. **Harsh reviewer council verdict**
17. **Remaining blockers**
18. **Exact next action for the author**

Use exact commit SHAs and command results.

---

# 19. What success looks like

Success is **not** a more impressive abstract.

Success is a repository and manuscript where an external reviewer can see:

- what the original frozen study tested;
- why the original non-nested comparison could not isolate climate;
- what the matched climate ablation actually estimates;
- how calibration and uncertainty alter interpretation;
- what geomatics adds as a distinct environmental-information experiment;
- why static landscape features answer “where” more naturally than “when”;
- whether dynamic remote sensing adds weekly early-warning information;
- how spatial aggregation/MAUP can hide real local environmental structure;
- what is reproducible;
- what is only partially reproducible because data remain quarantined;
- what is post-hoc;
- what remains unverified;
- and why no stronger claim is being made.

The target final interpretation should be something like the following **only if the completed experiments support it**:

> In retrospective dengue early-warning evaluations, recent surveillance is a strong operational benchmark. Environmental information can contribute modest incremental predictive information under matched comparison, but its apparent value depends on calibration, uncertainty target, temporal information content, and spatial scale. Geomatics and remote-sensing layers provide a complementary test of environmental signal, while coarse administrative aggregation and data-vintage constraints limit mechanistic interpretation and can erase local environmental structure. These findings support calibrated, comparator-matched, spatially explicit evaluation rather than simply adding more environmental predictors.

If the results do not support that synthesis, rewrite it to match the evidence.

**Evidence governs the narrative. The narrative never governs the evidence.**
