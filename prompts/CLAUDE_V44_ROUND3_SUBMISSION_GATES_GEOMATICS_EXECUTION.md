# Claude Code Execution Prompt — v44 Round 3: Submission-Gate Semantics, Geomatics Import, M6/WP4/WP5 Execution, and v44 Build

## Mission

Continue work on:

`Singati2/srilanka-dengue-ews-calibration`

Start from the latest implementation branch:

`agent/v44-round2-impl`

Observed round-2 implementation commit:

`11d8ec1b300ec151918e2cf4f9bbd6a076d6e2eb`

Round 2 successfully fixed the real-LaTeX contradiction detector and added explicit manuscript targeting. The actual tracked `manuscript_v43/revised_manuscript.tex` is now correctly detected as internally inconsistent, and v43 is preserved as historical evidence.

This round must now move the project from **audit hardening** toward **real experimental integration**, but only through explicit scientific gates.

The scientific objective remains:

> **When does environmental information add useful predictive or decision value beyond recent dengue surveillance, and how do calibration, comparator structure, temporal information, spatial scale, and geomatics fidelity change that conclusion?**

This is an **incremental-information and validity-audit study**.

It is NOT:

- a causal climate-effect study;
- a forecasting leaderboard;
- a claim that geomatics must improve prediction;
- a claim of deployment readiness;
- a claim of national external validation;
- a justification for turning exploratory results into confirmatory results;
- an excuse to rewrite historical analysis status.

Do not merge to `main` during this task.

---

# 0. Non-negotiable rules

## 0.1 Preserve historical evidence

Do not modify historical artifacts merely to make tests pass.

In particular:

- preserve `manuscript_v43/revised_manuscript.tex` as the historical v43 record;
- preserve `audit/V43_HISTORICAL_MANUSCRIPT_AUDIT.md`;
- preserve frozen v6/alternative-statistics tags and outputs;
- preserve old M6/M7 scripts and commit history even if their naming conflicts with the new geomatics comparator;
- never silently rewrite analysis chronology.

Any correction to v43 belongs in a separately created v44 candidate.

## 0.2 Never fabricate completion

Do not invent:

- M6/geomatics performance;
- spatial-CV results;
- MAUP results;
- population-weighted exposure results;
- bootstrap intervals;
- calibration metrics;
- external-reference verification;
- author declarations;
- ethics statements;
- funding information;
- ORCID identifiers;
- repository accessibility checks;
- DOI values.

If an analysis cannot run because an input is unavailable, document the blocker precisely and stop that analysis path.

## 0.3 Do not use outcome information to select geomatics features

The geomatics feature specification must be frozen BEFORE model fitting on outcome data.

Feature inclusion/exclusion can be based on:

- source availability;
- temporal availability;
- physical interpretability;
- duplicate/near-duplicate variables;
- pre-outcome collinearity diagnostics;
- missingness/vintage feasibility;
- leakage rules;
- previously recorded study decisions.

Feature inclusion/exclusion must NOT be based on:

- test AUC;
- test net benefit;
- test NLL/Brier;
- test p-values;
- which feature makes the desired story look stronger.

## 0.4 Negative/null geomatics findings are scientifically acceptable

Do not tune until geomatics “wins.”

A result such as:

- static spatial features predict where risk differs but not when weekly alerts occur;
- dynamic remote-sensing features add little beyond recent surveillance;
- geomatics value disappears under spatial validation;
- geomatics signal is sensitive to MAUP;

is scientifically meaningful and may strengthen the manuscript.

---

# 1. First task: repair submission-readiness semantics

The current runner contains logic equivalent to:

```python
ready = not any(r["status"] == "FAIL" for r in results)
```

This is too permissive for a submission-readiness claim because `NOT_VERIFIED`, `PARTIAL`, and `REVIEW` can still represent unresolved scientific validity problems.

## 1.1 Separate two concepts

Implement two explicit top-level states.

### A. AUDIT SOFTWARE HEALTH

This answers:

> Did the audit software execute deterministically and complete its intended checks without crashing?

Possible output:

- `HEALTHY`
- `DEGRADED`
- `FAILED`

### B. MANUSCRIPT SUBMISSION READINESS

This answers:

> Are all mandatory scientific, reproducibility, provenance, reference, consistency, and declaration gates demonstrated strongly enough for submission?

Possible output:

- `READY`
- `NOT_READY`

Do not conflate these two.

## 1.2 Submission readiness rule

For the final manuscript submission gate, treat ALL of the following as blocking unless a gate is explicitly designated non-blocking:

- `FAIL`
- `REVIEW`
- `PARTIAL`
- `NOT_VERIFIED`

Only mandatory gates with `PASS` may count as resolved.

If you want optional/non-blocking gates, encode that explicitly in gate metadata, e.g.:

```python
{
  "name": "...",
  "mandatory_for_submission": True,
  "status": "NOT_VERIFIED"
}
```

Then compute readiness from mandatory gates only.

Do NOT hide unresolved gates merely because no critical error is present.

## 1.3 Required regression tests

Add tests proving that:

1. all mandatory PASS → `submission_ready == True`;
2. one mandatory FAIL → False;
3. one mandatory REVIEW → False;
4. one mandatory PARTIAL → False;
5. one mandatory NOT_VERIFIED → False;
6. an explicitly non-blocking optional gate may remain REVIEW without forcing False;
7. audit software health can still be HEALTHY while submission readiness is False.

The tests must exercise the real readiness function, not duplicate its logic locally.

---

# 2. Repair the remaining shallow PASS gates

Round 2 correctly downgraded temporal leakage, reproducibility, and reference integrity.

Several remaining PASS gates still imply more verification than the code demonstrates.

## 2.1 MODEL SPECIFICATION

Current broad wording/seed checks are insufficient for a strong PASS.

Until exact design matrices or equivalent structured model specifications are verified, return at most:

`PARTIAL`

A strong PASS should require evidence that the compared models differ only in the intended feature block where a matched ablation is claimed.

For a matched climate contrast, verify as far as artifacts permit:

```text
full model features
minus climate block
=
matched no-climate model features
```

while retaining:

- identical observation keys;
- identical train/validation/test partitions;
- same preprocessing family;
- same model family;
- same recalibration protocol;
- same evaluation rows;
- independently fitted coefficients/tuning where appropriate.

If exact matrices are quarantined and unavailable, state `PARTIAL` or `NOT_VERIFIED`.

## 2.2 CALIBRATION

Presence of words such as `CITL`, `slope`, `recalibration`, and `ICI` is not calibration verification.

Until the calibration implementation is re-executed or checked against date-indexed predictions, return at most:

`PARTIAL`

A strong PASS requires explicit evidence for:

- training/validation/test separation;
- what period fits calibration parameters;
- rolling Sri Lanka recalibration uses only prior observable forecast–outcome pairs;
- no concurrent/future test observations enter the primary past-only recalibration;
- Colombia Platt scaling uses validation data only;
- raw vs recalibrated predictions retain identical row keys;
- metric outputs reproduce frozen results within declared tolerance.

## 2.3 ADVERSARIAL REVIEW

The current automated term scanner is useful but should not be labeled as a full adversarial peer review.

Rename or clearly identify the deterministic gate as something like:

`OVERCLAIM LANGUAGE SCAN`

A later substantive reviewer stage must separately evaluate scientific design and inference.

Do not claim an LLM/multi-expert review occurred unless it actually runs and produces saved evidence.

## 2.4 SPATIAL CONSISTENCY

A strong PASS must not rely only on presence of unit counts.

Before strong PASS, verify what can be verified from committed artifacts:

- 26 Sri Lanka RDHS units;
- Ampara/Kalmunai split handling;
- geometry key uniqueness;
- adjacency graph count if available;
- Colombia municipality/department mapping consistency;
- explanation of 32 fixed-effect columns versus 31 analyzed test departments;
- spatial bootstrap cluster definitions;
- no silent geographic-key mismatches.

If only text-level checks are available, use `PARTIAL`.

---

# 3. Keep explicit manuscript targeting

Round 2 added `--manuscript`; preserve and expand it.

Every audit report must record:

- exact manuscript path;
- SHA-256 fingerprint;
- git commit/branch if available;
- whether the manuscript is historical or submission candidate.

Required commands should support:

```bash
python -m agent_graph.run_audit \
  --repo . \
  --manuscript manuscript_v43/revised_manuscript.tex
```

and later:

```bash
python -m agent_graph.run_audit \
  --repo . \
  --manuscript manuscript_v44/revised_manuscript.tex
```

v43 must continue to FAIL manuscript consistency because its contradiction is part of the historical record.

Do not edit v43 to turn that FAIL into PASS.

---

# 4. Import the real geomatics work from PR #1

Source PR:

`#1 — M6 geomatics-only comparator: notebook workflow, feature extraction batches A/B/C`

Source branch:

`m6-geomatics-notebooks`

Observed source work includes:

- `docs/M6.md`
- `docs/study_decision_log.md`
- `notebooks/00_setup_and_geometry.ipynb`
- `notebooks/01_terrain_batchA.ipynb`
- `notebooks/02_dynamic_modis.ipynb`
- `notebooks/03_batchB_statics.ipynb`
- `notebooks/README.md`
- `notebooks_requirements_lock.txt`

The current v44 round-2 branch contains the M6 plan but not all executed notebooks.

## 4.1 Import rules

Do a conflict-aware import.

Do NOT blindly merge all branch history.

Before import:

1. list every source file;
2. compare against current branch versions;
3. identify conflicts;
4. preserve newer audit changes;
5. preserve geomatics provenance/decision-log content;
6. record source branch and source commit SHA.

Create:

`audit/GEOMATICS_IMPORT_PROVENANCE.md`

with:

- PR number;
- source branch;
- source SHA;
- imported files;
- skipped files and reasons;
- conflicts and resolutions;
- checksums where practical.

## 4.2 Do not treat executed notebooks as proof of completed M6

Notebooks 00–03 demonstrate feature extraction/preprocessing stages only.

They do not prove:

- outcome-row comparability;
- M6 model fitting;
- M6 calibration;
- M6 DCA;
- M6 proper scores;
- spatial CV;
- MAUP sensitivity.

Keep these stages distinct.

---

# 5. Resolve model-name collisions BEFORE manuscript use

Historical code already uses M6/M7 labels in older exploratory Colombia geospatial/SPI pilots.

The newer geomatics work also uses “M6” for a geomatics-only comparator.

This is dangerous for manuscript provenance.

## 5.1 Build a model nomenclature registry

Create:

`docs/MODEL_NOMENCLATURE_REGISTRY.md`

Include every model label appearing in tracked code/manuscripts/docs.

At minimum record:

| historical label | implementation | feature blocks | country | analysis status | manuscript use? |
|---|---|---|---|---|---|

Do NOT rename historical scripts merely to clean appearance.

Instead create unambiguous v44 manuscript labels.

Recommended descriptive naming for new geomatics experiments:

- `GEO_ONLY` = geomatics-only environmental comparator;
- `M5_PLUS_GEO` = full matched model plus geomatics block;
- `M5_NO_GEO` or baseline M5 = matched comparator without geomatics;
- `DELTA_GEO` = matched incremental geomatics contribution.

Alternative names are acceptable if they are explicit and collision-free.

Avoid using bare “M6” in v44 unless the registry proves it is unambiguous.

---

# 6. Freeze the geomatics feature specification before outcome access

Create:

`analysis/geomatics_v44/GEOMATICS_FEATURE_SPEC_LOCK.md`

and a machine-readable companion:

`analysis/geomatics_v44/geomatics_feature_spec_lock.json`

The lock must be committed BEFORE fitting against outcome data.

## 6.1 Record each feature

For every proposed geomatics feature, record:

- canonical feature name;
- source/product;
- source version/vintage;
- static vs dynamic;
- spatial resolution;
- temporal resolution;
- spatial aggregation rule;
- temporal aggregation rule;
- lag rule;
- missingness rule;
- carry-forward rule;
- population-weighted vs area-weighted vs unweighted;
- expected availability period;
- leakage risk;
- final include/exclude decision;
- reason for decision;
- whether it can encode “where”, “when”, or both.

## 6.2 Preserve known geomatics findings/constraints

Explicitly incorporate already observed design constraints:

### Static variables cannot encode weekly timing

Terrain, built-up, fragmentation, and other static/slow features can identify spatial heterogeneity but cannot by themselves produce within-unit weekly timing variation.

Do not interpret weak weekly performance of a static-only model as “geomatics has no signal.”

### MODIS composite timing

For dynamic remote-sensing composites:

- do not join by composite start date if the composite extends beyond forecast origin;
- use only composites whose END date is known/complete by forecast origin;
- no interpolation using future observations;
- any gap filling must be past-only.

### MAUP/UHI finding

The observed weak built-up ↔ district-mean LST relationship at 26-RDHS resolution must be interpreted as a scale/aggregation finding, not evidence that urban heat-island effects do not exist.

### Land-cover vintages

Do not feed unstable year-to-year classifier relabeling into the model as if it were true urbanization without a documented decision.

### WorldPop coastal shortfall

The ~3.5% coastline capture shortfall must be resolved or explicitly propagated into WP5 uncertainty/limitations before population-weighted exposure claims are made.

---

# 7. Build an identical-row evaluation gate

M6/geomatics results are interpretable only if comparator rows are aligned.

Create a deterministic row-comparability gate.

For each country/experiment, require exact equality of intended observation keys across compared models.

Recommended key:

```text
country + spatial_unit_id + forecast_origin_date/week + target_horizon + target_definition
```

Verify:

- identical test rows;
- identical outcome labels;
- identical train/test split boundaries;
- identical 75th-percentile threshold definition where used;
- identical 90th-percentile sensitivity definition where used;
- identical horizon definition;
- no silent complete-case shrinkage favoring one model.

If a shared complete-case mask is necessary, recompute ALL compared model metrics on that shared mask and label them as a new row-matched analysis.

Do not compare a geomatics model on one row set with M1/M5 metrics from another row set.

Create:

`analysis/geomatics_v44/ROW_COMPARABILITY_REPORT.md`

and machine-readable hashes/manifests without exposing restricted/raw data.

---

# 8. Build a temporal-availability gate for dynamic geomatics

For every dynamic feature row, verify:

```text
feature_information_available_time <= forecast_origin_time
```

This must consider the END of satellite composites, not merely nominal start date.

Check:

- MOD11A2 composite windows;
- MOD13Q1 composite windows;
- weekly aggregation;
- lag generation;
- past-only gap filling;
- any rolling summaries;
- any standardization learned from training only;
- any target-threshold construction.

Write:

`analysis/geomatics_v44/TEMPORAL_AVAILABILITY_AUDIT.md`

The geomatics model must not be fit if this gate FAILs.

---

# 9. Distinguish two different geomatics scientific questions

Do not collapse these into one model.

## 9.1 Question A — standalone environmental/geomatics signal

> Can landscape + remotely sensed environmental information predict elevated dengue activity without recent case counts?

Use:

`GEO_ONLY`

This is conceptually analogous to the climate-only model and answers a bounded information-content question.

Interpretation rules:

- static variables mainly encode spatial susceptibility (“where”);
- dynamic remote sensing can encode temporal variation (“when”);
- weak performance is not proof of no biological relevance;
- do not interpret coefficients causally.

## 9.2 Question B — matched incremental geomatics value beyond existing surveillance/climate structure

> Does adding the frozen geomatics block improve predictive/decision performance beyond the otherwise identical matched model?

Use a matched pair such as:

```text
M5_PLUS_GEO
vs
M5
```

or equivalent collision-free names.

The only intended difference should be the geomatics block.

This is the geomatics analogue of the matched climate ablation.

Primary incremental estimands may include:

- ΔNLL;
- ΔBrier;
- ΔAUC / ΔPR-AUC as secondary discrimination measures;
- ΔNB across threshold grid;
- reference-threshold ΔNB at p*=0.30 only as illustrative;
- calibration changes.

All geomatics analyses remain post-hoc/exploratory unless historical documentation proves otherwise.

---

# 10. M6/geomatics modeling requirements

Only proceed after feature-lock, row-comparability, and temporal-availability gates pass.

## 10.1 Keep model family matched

Use the same or explicitly justified model family/preprocessing pipeline as the relevant comparator.

Do not introduce a new complex model solely to make geomatics appear better.

## 10.2 Scaling/tuning

- learn scaling on development data only;
- choose regularization/tuning without test-outcome access;
- independently fit matched models if the original matched-ablation protocol does so;
- preserve random seeds;
- record software versions.

## 10.3 Calibration

Apply country-appropriate calibration under the same temporal discipline as comparator models.

For Sri Lanka:

- primary recalibration must remain past-only;
- optimistic cross-fitted recalibration may be sensitivity only.

For Colombia:

- validation-based Platt calibration must not use test outcomes.

## 10.4 Required metrics

At minimum report:

- NLL;
- Brier;
- AUC;
- PR-AUC;
- CITL;
- calibration slope;
- ICI if already part of project protocol;
- DCA across threshold grid;
- p*=0.30 result as illustrative, not a universal operational threshold.

## 10.5 Uncertainty

Clearly distinguish:

- conditional/frozen-prediction bootstrap;
- development-inclusive/refit bootstrap.

Do not describe conditional intervals as model-development uncertainty.

If development-inclusive refitting is computationally blocked, report that honestly and do not imply robustness.

---

# 11. WP4 — spatial validation

Do not treat random/temporal holdout alone as spatial generalization evidence.

Implement WP4 only when data permit.

At minimum define a spatial-honesty sensitivity such as:

- leave-region/cluster-out;
- grouped spatial CV;
- predefined contiguous spatial blocks;
- department/RDHS-group holdout where appropriate.

Rules:

- folds must be defined without test outcome optimization;
- feature preprocessing must be fit inside training folds;
- calibration must obey fold structure;
- report instability across spatial folds;
- do not call Colombia national external validation.

Create:

`analysis/wp4_spatial_cv/`

with:

- frozen plan/spec;
- code;
- safe aggregate outputs;
- provenance;
- interpretation report.

If exact WP4 execution is blocked, document blocker and do not fabricate results.

---

# 12. WP5 — MAUP and population-weighted exposure

WP5 must directly address sensitivity to spatial aggregation/exposure construction.

## 12.1 Population weighting

Before building population-weighted environmental exposures, resolve the coastal WorldPop denominator issue.

Possible defensible options:

- fractional raster-cell coverage;
- centre-in-polygon with quantified bias and sensitivity;
- alternative population surface comparison.

Do not silently accept a known denominator loss.

## 12.2 MAUP interpretation

Test whether substantive conclusions change under reasonable spatial exposure constructions.

Do not overinterpret district/RDHS-aggregated features as individual-level mechanisms.

If the UHI signal disappears at coarse scale, state that scale can erase local spatial relationships.

Create:

`analysis/wp5_maup/`

with locked analysis design and result provenance.

---

# 13. Only after experiments are ready: create manuscript_v44

Do not overwrite v43.

Create:

`manuscript_v44/`

Copy v43 as a starting historical base, then make only evidence-supported changes.

## 13.1 Required v44 correction

Retire the stale Methods statement that development-inclusive proper-score intervals were not computed, because tracked results report those intervals.

State chronology honestly, for example:

- conditional proper-score analysis was first computed under the post-result design lock;
- development-inclusive refit-both-model intervals were subsequently computed as a later reviewer-responsive/post-hoc robustness analysis;
- do not imply preregistration.

## 13.2 Reframed manuscript thesis

Do not frame the paper merely as:

> “Does climate improve dengue prediction?”

Use the broader experimental question:

> **When does environmental information add useful predictive or decision value beyond recent surveillance, and how do calibration, comparator choice, temporal availability, spatial scale, and geomatics fidelity affect that conclusion?**

## 13.3 Suggested experimental narrative

A coherent v44 structure may be:

1. surveillance benchmark;
2. climate-only information;
3. hybrid models;
4. matched climate ablation;
5. proper-score + calibration + DCA robustness;
6. geomatics standalone signal (`GEO_ONLY`);
7. matched incremental geomatics ablation (`M5_PLUS_GEO` vs matched baseline);
8. static “where” vs dynamic “when” interpretation;
9. spatial validation (WP4);
10. MAUP/population-weighted exposure sensitivity (WP5);
11. integrated limits on environmental information beyond surveillance.

Do not force all stages into headline results if some remain blocked or exploratory.

## 13.4 Abstract discipline

Do not place a geomatics headline in the abstract unless:

- experiment executed;
- rows are matched;
- leakage gate passed;
- result provenance exists;
- uncertainty is reported;
- analysis status is explicit.

## 13.5 Interpretation discipline

Allowed language:

- “incremental predictive information”;
- “exploratory matched feature-block contrast”;
- “compatible with zero under development-inclusive uncertainty”;
- “sensitive to spatial aggregation”;
- “limited by finalized surveillance and retrospective design.”

Avoid:

- “climate causes outbreaks”;
- “geomatics proves environmental mechanism”;
- “nationally validated”;
- “deployment ready”;
- “operationally useful” without stakeholder utility thresholds;
- difference-in-significance arguments.

---

# 14. Build structured claim provenance

Token matching of four-decimal values is insufficient.

Create a structured claim registry, for example:

`audit/claim_registry.jsonl`

Each headline/manuscript result should contain fields such as:

```json
{
  "claim_id": "...",
  "manuscript_path": "...",
  "section": "...",
  "claim_text": "...",
  "analysis_id": "...",
  "metric": "delta_nll",
  "point_estimate": -0.0207,
  "ci_low": -0.0346,
  "ci_high": -0.0067,
  "uncertainty_type": "conditional_cluster_bootstrap",
  "analysis_status": "post_result_design_locked",
  "script": "...",
  "result_artifact": "...",
  "artifact_sha256": "...",
  "commit": "..."
}
```

The goal is:

`Manuscript claim → metric → analysis → script → result artifact → checksum → commit`

Do not infer provenance merely because the same decimal appears somewhere else.

---

# 15. Reference verification

The deterministic offline audit may continue to report `REFERENCE INTEGRITY = NOT_VERIFIED`.

For any separate network-enabled reference verification phase, verify high-stakes citations against primary publisher/DOI/PubMed/Crossref records where available.

For each important citation check:

- authors;
- title;
- year;
- DOI/identifier;
- whether source exists;
- whether source supports the manuscript sentence;
- whether citation is being used for a stronger claim than the source supports.

High-priority claims include:

- DCA novelty;
- dengue early-warning/climate literature;
- calibration/DCA methodology;
- OpenDengue provenance;
- climate/remote-sensing products;
- MAUP/spatial epidemiology claims.

Do not fabricate DOI values.

---

# 16. Clean reproducibility check

A strong reproducibility PASS requires more than lockfile/checksum presence.

Where legal/available inputs permit, create a clean-environment reproduction test that:

1. installs the minimal audit/reproduction environment;
2. runs deterministic tests;
3. regenerates selected committed aggregate outputs;
4. compares hashes or numerical tolerances;
5. records failures exactly.

If quarantined inputs prevent full reproduction, report:

`NOT_VERIFIED` or `PARTIAL`

not PASS.

Do not weaken the gate merely to obtain green CI.

---

# 17. Repository portability

The audit currently finds many machine-specific absolute paths.

Do not delete historical scripts simply to reduce the count.

Classify absolute paths into:

- active execution blocker;
- historical artifact only;
- documentation example;
- safe to parameterize;
- intentionally frozen historical path.

For active scripts, introduce configuration/CLI/path resolution without changing scientific logic.

Create:

`audit/PATH_PORTABILITY_CLASSIFICATION.md`

Do not claim portability is solved until active paths are removed or parameterized.

---

# 18. Data-provenance classification

The audit currently flags tracked CSV/JSON files under analysis directories.

Do not automatically delete them.

Classify each as:

- raw/restricted data;
- derived row-level data;
- frozen predictions;
- bootstrap replicate distributions;
- aggregate result table;
- provenance metadata;
- synthetic fixture.

Then determine whether tracking is allowed under the repository's data policy.

Create:

`audit/TRACKED_DATA_CLASSIFICATION.md`

A frozen matched-prediction table intentionally committed for reproducibility is not equivalent to accidentally leaked raw surveillance data.

The audit should distinguish these cases.

---

# 19. Final scientific reviewer stage

Only after the experiments and v44 candidate exist, run a substantive reviewer council.

Do NOT claim separate independent LLM agents unless you actually invoke them. A deterministic or single-model multi-role review is acceptable if labeled accurately.

At minimum review from these perspectives:

1. infectious-disease epidemiology;
2. statistical prediction/calibration;
3. decision-curve analysis;
4. geospatial epidemiology/MAUP;
5. remote sensing/geomatics;
6. temporal leakage/reproducibility;
7. causal-inference skeptic;
8. journal desk-rejection editor.

Each reviewer should provide:

- critical defects;
- major defects;
- minor defects;
- unsupported claims;
- whether the geomatics integration strengthens or dilutes the paper;
- concrete revision requests;
- score /10;
- accept / major revision / reject-style verdict.

Create:

`audit/V44_HARSH_REVIEW_COUNCIL.md`

and a machine-readable summary.

---

# 20. Required phase order

Execute in this order.

## PHASE A — Submission semantics

- separate software health from manuscript readiness;
- make REVIEW/PARTIAL/NOT_VERIFIED block mandatory submission gates;
- add regression tests.

## PHASE B — Gate honesty

- downgrade shallow model/calibration/spatial PASS semantics;
- rename adversarial language scan accurately;
- preserve v43 contradiction detection.

## PHASE C — Geomatics import

- import PR #1 notebooks/docs conflict-aware;
- write import provenance;
- do not claim M6 complete.

## PHASE D — Model nomenclature

- inventory historical M6/M7 labels;
- create collision-free v44 naming registry.

## PHASE E — Geomatics feature lock

- freeze features and rules before outcome access;
- commit machine-readable lock.

## PHASE F — Data comparability gates

- stage intended outcome/model row keys;
- exact row comparability;
- temporal-availability audit;
- stop if either gate fails.

## PHASE G — Geomatics modeling

- run `GEO_ONLY`;
- run matched incremental geomatics model;
- calculate calibration/proper scores/DCA;
- preserve null result if null.

## PHASE H — Development-inclusive uncertainty

- refit both matched models within cluster resamples where feasible;
- label any unavailable DI analysis honestly.

## PHASE I — WP4 spatial CV

- execute locked spatial validation;
- prevent preprocessing leakage.

## PHASE J — WP5 MAUP/population weighting

- resolve WorldPop denominator decision;
- execute spatial/exposure sensitivity where feasible.

## PHASE K — v44 manuscript

Only after G–J are sufficiently complete for the claims being made:

- create `manuscript_v44/`;
- fix the v43 stale Methods contradiction in v44 only;
- integrate geomatics honestly;
- reframe around incremental environmental information and validity.

## PHASE L — Claim provenance

- structured claim registry;
- trace headline values to artifacts/scripts/checksums/commits.

## PHASE M — Reproducibility/reference checks

- clean reproduction where possible;
- external reference verification when network is available.

## PHASE N — Harsh reviewer council

- full desk-rejection-style audit;
- no submission-ready claim unless every mandatory gate is PASS.

---

# 21. Stop rules

Stop the relevant downstream phase and document BLOCKED if any of these occur:

1. geomatics feature tables cannot be located or reconstructed;
2. exact outcome-row keys cannot be staged;
3. dynamic feature availability extends beyond forecast origin;
4. comparator row sets cannot be aligned;
5. feature specification was already tuned using test outcomes and no clean pre-outcome spec can be reconstructed;
6. population-weighted exposure denominator cannot be defended;
7. spatial-CV fold design is outcome-optimized;
8. required data are restricted/unavailable and no honest substitute exists;
9. result provenance cannot be established;
10. reference or author-supplied information is unknown.

A blocker is an acceptable result of this task.

Never replace a blocker with an invented value.

---

# 22. Required deliverables

At the end of this round, produce as many of the following as evidence allows:

### Audit/core

- repaired `agent_graph/` submission semantics;
- updated tests;
- updated `audit/CURRENT_KG_AGENT_AUDIT.{md,json}`;
- `audit/PATH_PORTABILITY_CLASSIFICATION.md`;
- `audit/TRACKED_DATA_CLASSIFICATION.md`.

### Geomatics integration

- imported notebooks from PR #1;
- `audit/GEOMATICS_IMPORT_PROVENANCE.md`;
- `docs/MODEL_NOMENCLATURE_REGISTRY.md`;
- `analysis/geomatics_v44/GEOMATICS_FEATURE_SPEC_LOCK.md`;
- `analysis/geomatics_v44/geomatics_feature_spec_lock.json`;
- `analysis/geomatics_v44/ROW_COMPARABILITY_REPORT.md`;
- `analysis/geomatics_v44/TEMPORAL_AVAILABILITY_AUDIT.md`.

### If execution is possible

- geomatics model scripts;
- safe aggregate results;
- conditional and DI uncertainty outputs;
- WP4 outputs;
- WP5 outputs.

### Manuscript

Only if evidence is ready:

- `manuscript_v44/revised_manuscript.tex`;
- supporting tables/figures required by new analyses;
- v44 change log against v43.

### Provenance/review

- `audit/claim_registry.jsonl`;
- `audit/V44_HARSH_REVIEW_COUNCIL.md`;
- final implementation report.

---

# 23. Final implementation report

Create:

`V44_ROUND3_IMPLEMENTATION_REPORT.md`

Include:

## A. Branch/commit provenance

- start branch/SHA;
- final branch/SHA;
- imported PR #1 source SHA;
- files changed.

## B. Audit changes

- readiness semantics before/after;
- gate status before/after;
- regression tests;
- whether CI ran.

## C. Geomatics import

- imported files;
- conflicts;
- unresolved dependencies.

## D. Feature lock

- final frozen feature list;
- excluded features + reasons;
- static vs dynamic classification;
- leakage rules.

## E. Row/temporal gates

- PASS/FAIL/BLOCKED;
- exact evidence.

## F. Modeling results

Only if executed.

Report all relevant metrics and uncertainty without promotional language.

## G. WP4/WP5

- completed / blocked;
- results if available;
- scientific implications.

## H. v44 manuscript

- created or not created;
- exact reason;
- major framing changes;
- whether v43 remains untouched.

## I. Remaining submission blockers

Explicit list.

## J. Harsh verdict

Provide scores:

- scientific contribution /10;
- statistical validity /10;
- temporal validity /10;
- geospatial validity /10;
- reproducibility /10;
- claim traceability /10;
- manuscript coherence /10;
- submission readiness /10.

Then give one final status:

- `NOT READY — FUNDAMENTAL SCIENTIFIC BLOCKER`
- `NOT READY — EXECUTION/PROVENANCE BLOCKERS`
- `MAJOR REVISION BEFORE SUBMISSION`
- `READY FOR HUMAN COAUTHOR REVIEW`
- `READY FOR SUBMISSION`

`READY FOR SUBMISSION` is permitted only if every mandatory release gate is PASS and author-supplied declarations are resolved.

---

# 24. Final philosophy

Do not optimize for a green badge.

Optimize for a research record in which:

- historical mistakes remain visible;
- corrections are versioned;
- exploratory work stays exploratory;
- null findings remain null;
- model comparisons are row-matched;
- satellite timing cannot leak future data;
- spatial scale limitations are explicit;
- geomatics feature choice is frozen before outcomes;
- manuscript numbers are traceable to artifacts;
- unverified claims block submission readiness;
- software PASS is never confused with scientific PASS.

The paper becomes stronger if the infrastructure makes it difficult to tell a stronger story than the evidence supports.
