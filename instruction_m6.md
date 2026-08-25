# M6 Follow-up Instructions — Before Manuscript Integration

## Purpose

This file gives the next execution instructions after commit:

`ff6287d0e336ab4e3a3d178593d3bb28e3f33a21`

on branch:

`m6-geomatics-notebooks`

The recent push is a major advance: notebooks 04–08 now execute, M6 is fitted and evaluated on the 3,926-row Sri Lanka test panel, WP4 has fold-geometry/autocorrelation work, and WP5 has a population-weight field plus an initial temperature-displacement result.

However, **do not integrate M6/WP4/WP5 into the final v44 manuscript yet**. Several scientific-governance and estimand issues must be resolved first.

The goal is not to make M6 look successful. The goal is to make every geomatics conclusion defensible.

---

# 1. Preserve the current result exactly as an exploratory result

Do not change, tune, select, or redesign M6 because its current standalone performance is weak.

The current reported result is acceptable as an honest exploratory null:

- M6 geomatics-only AUC approximately 0.601;
- M6 NB at `p*=0.30` approximately 0.058;
- M5 full AUC approximately 0.771;
- M5 full NB approximately 0.145;
- M5 no-climate AUC approximately 0.751;
- M5 no-climate NB approximately 0.135.

Preserve this result as a frozen exploratory artifact with:

- source commit;
- row keys;
- feature-set identity;
- exact environment;
- seeds;
- metric artifact hashes;
- figure hashes;
- notebook hashes.

Do **not** rerun feature engineering or model selection in search of better test performance.

---

# 2. Rename the current scientific object correctly: M6-core, unless Batch D is actually present

The original M6 plan described 16 geomatics variables including Batch D items such as:

- connectivity/mobility;
- relative wealth;
- healthcare access;
- rice/cropland phenology.

The currently executed workflow is clearly built from the completed A/B/C workstream unless there is separate evidence that Batch D was incorporated.

Therefore:

- audit the actual columns in the final M6 design matrix;
- compare them against `docs/M6.md`;
- create a feature manifest;
- if Batch D is absent, call the executed model **M6-core (A/B/C)** rather than implying that the complete originally planned 16-variable M6 was run.

If Batch D is later added, call that version **M6-extended** and treat it as a separately versioned sensitivity.

Do not silently redefine historical M6.

---

# 3. Critical target-provenance issue: do not treat recovered test-constrained thresholds as equivalent to the original frozen training target

The current workflow reconstructs the Sri Lanka incidence thresholds using the known frozen test outcomes as constraints and reports exact 3,926/3,926 test-label agreement.

That is useful as a verification exercise, but it is **not automatically equivalent to recovering the original training-only threshold artifact**.

The concern is especially important for the districts where the empirical training quantile was clamped to a feasible interval determined using frozen test labels.

Potential dependency:

`test outcome labels -> feasible threshold interval -> selected threshold -> reconstructed training labels -> M6 fit`

This is not ordinary predictor leakage, but it is **test-dependent target reconstruction**.

Before calling the M6 development pipeline fully frozen/comparable, do one of the following, in order of preference:

## Preferred Route A — recover the original frozen threshold table

Locate and use the exact threshold artifact that produced the original Sri Lanka labels.

Record:

- path;
- hash;
- creation commit/date;
- threshold definition;
- row mask used to estimate it.

Then confirm 3,926/3,926 test-label identity without any test-informed threshold fitting.

## Preferred Route B — reconstruct the exact training-only threshold procedure

Recover the exact frozen training panel, including the original:

- outcome-missing mask;
- exposure-missing mask;
- population-missing mask;
- 2018–2022 training rows;
- annual denominator values.

Compute the 75th-percentile incidence thresholds from training data only.

Then verify test labels.

## Route C — if A/B cannot be recovered

Keep the existing reconstruction but label the M6 result explicitly as:

> `EXPLORATORY_RECONSTRUCTED_TARGET`

and state that the target threshold reconstruction was constrained by frozen test labels.

Do not describe this as an exact independent redevelopment of the original frozen target.

Do not rewrite chronology to make the reconstruction look prespecified.

---

# 4. Recover the original frozen training data if possible

The new machine's WER restaging is not byte-identical to the original freeze because 2018 week 4 is now image-only and loses 26 training district-weeks.

The frozen M5 models and the new M6 model therefore do not currently have perfectly identical development data histories.

Preferred fix:

- recover the original frozen v2.0 Sri Lanka linked/outcome artifact;
- use the exact same training rows as the original pipeline;
- rerun M6 only if this can be done without changing the frozen feature definition.

If the original frozen training artifact cannot be recovered:

- keep the current run;
- quantify the effect of the 26-row training difference;
- call it a parallel exploratory redevelopment;
- do not claim full development-protocol identity with M5.

---

# 5. Feature-lock chronology must be demonstrated, not retroactively invented

The PI-approved geomatics plan requires the feature and selection specification to be frozen before outcome access.

Search the git history and notebook chronology for a real pre-outcome lock.

Create:

`analysis/geomatics_integration_v1/M6_FEATURE_CHRONOLOGY.md`

Record:

- first commit containing the A/B/C feature specification;
- first commit containing each notebook;
- first outcome-access event;
- first model-fit event;
- any feature changes after outcome access;
- any feature removals/additions after viewing M6 performance.

If a genuine pre-outcome lock exists, create:

`analysis/geomatics_integration_v1/M6_CORE_FEATURE_LOCK.yaml`

and record the historical commit/hash that proves it.

If no formal lock existed, **do not fabricate one retroactively**.

Instead state:

> The feature set was developed before/alongside the outcome-stage workflow but was not formally cryptographically frozen before all outcome access; therefore M6 remains post-hoc exploratory.

A retrospective manifest is still useful, but it must not be called a preregistration.

---

# 6. Freeze the current M6-core artifact now

Regardless of historical chronology, freeze the present result so it cannot drift further.

Create a manifest such as:

`analysis/geomatics_integration_v1/M6_CORE_FROZEN_MANIFEST.yaml`

Include:

- commit SHA `ff6287d0...` or the exact final freeze SHA;
- notebook hashes 00–08;
- feature column list;
- training/test row counts;
- test row-key hash;
- target artifact hash;
- comparator prediction hashes;
- model hyperparameters;
- selected regularization value;
- calibration method;
- bootstrap seed and B;
- MODIS gap rule;
- output artifact hashes;
- figure hashes.

No future result should overwrite this version.

---

# 7. Do not call the present M6-vs-M5 contrast “incremental geomatics value”

Current contrasts are approximately:

`M6 geomatics-only vs M5 full`

and

`M6 geomatics-only vs M5 no-climate`.

These answer:

> Can geomatics alone compete with surveillance-containing hybrid models?

They do **not** answer:

> Does geomatics add incremental information beyond recent surveillance?

Therefore manuscript language must distinguish these questions.

Allowed:

> The geomatics-only comparator showed substantially lower standalone discrimination and decision value than the surveillance-containing matched models.

Not allowed:

> Geomatics adds no value beyond surveillance.

The latter requires a matched geomatics block ablation.

---

# 8. Build the matched geomatics estimand if scientifically feasible

The strongest v44 geomatics question is:

> Does adding the locked geomatics block improve performance beyond an otherwise identical surveillance-based model?

Construct a matched comparison analogous to the climate ablation.

For example:

`BASE + GEOMATICS`

versus

`BASE WITHOUT GEOMATICS`

The two models must share:

- identical recent-case history;
- identical seasonal structure;
- identical geographic structure;
- identical row mask;
- identical preprocessing;
- identical estimator family;
- identical hyperparameter search space;
- identical development protocol;
- identical calibration strategy;
- identical evaluation code.

Only the geomatics block should differ.

Do not use test performance to choose the base specification.

The base must be justified from the frozen manuscript model architecture or a clearly predeclared stress-test rung.

If exact matched construction is not possible, mark:

`MATCHED_GEOMATICS_ABLATION = BLOCKED`

and explain why.

Do not substitute M6-vs-M5 and rename it incremental value.

---

# 9. Resolve the registered M0/M1/M2 contrast mismatch transparently

`docs/M6.md` originally asks whether geomatics-only M6 beats season M0 and climate-only M2.

The current frozen comparator artifact apparently contains M5 full and M5 no-climate predictions but not M0/M1/M2 on the identical row universe.

Do not silently rewrite the original question after seeing M6 performance.

Do one of these:

## Option A — recover M0/M1/M2 frozen predictions on the same 3,926 rows

Preferred if possible.

## Option B — document a protocol deviation

Create a deviation note explaining:

- original contrast;
- unavailable artifact;
- available contrast;
- why the substitute contrast was used;
- why it does not answer the original registered question.

Keep the current M6-vs-M5 comparisons exploratory.

---

# 10. Calibration comparability must be repaired or clearly separated

The current note states that M6 is Platt-recalibrated while the comparators use rolling-52-week recalibration, which is why raw predictions are treated as primary.

That is sensible, but the calibrated models are not methodologically matched.

For manuscript comparison:

- keep **raw** comparison as the primary fair standalone contrast;
- do not directly interpret differences between differently recalibrated models as purely model-information differences.

If a calibrated contrast is required, apply a common leakage-safe calibration protocol to both sides of the comparison.

For any recalibrated matched geomatics ablation, use exactly the same recalibration algorithm on both models.

Document calibration windows and observability.

---

# 11. MODIS 2025 gap: backfill if practical, but do not compromise row identity

Current workflow reports a source/catalogue gap from approximately 2025-07-04 to 2025-11-17 and forward-filled features for about 11.3% of test rows.

The fresh-MODIS sensitivity gives the same qualitative conclusion, which is reassuring.

Next steps:

1. Check NASA's authoritative archive for the missing Terra granules.
2. If recoverable, backfill them under a new frozen feature version.
3. Re-run only as a prespecified missingness sensitivity; do not overwrite the original M6-core result.
4. Compare:
   - original forward-fill run;
   - NASA-backfilled run;
   - fresh-MODIS subset.

Report the differences.

If the granules remain unavailable, keep the present sensitivity and state the limitation.

---

# 12. Preserve the important temporal-leakage discovery

The current implementation reports that a naive composite-start join would leak in approximately 91.4% of district-weeks.

This is an important methodological finding.

Freeze a dedicated leakage audit artifact containing:

- composite start;
- composite end;
- forecast origin;
- allowed/disallowed flag;
- number and percentage of rows that would leak under start-date joining;
- tests enforcing the correct availability rule.

This belongs in the methods/provenance discussion because it illustrates why nominal timestamp alignment is insufficient for remote-sensing forecasting.

Do not use product release latency language stronger than the data support. If actual publication latency is not modeled, say that composite-end gating is a retrospective availability approximation.

---

# 13. Preserve and test the pandas `merge_asof` alignment bug fix

The detected `merge_asof` ordering/scrambling failure is serious because the output can remain plausible while being assigned to the wrong district-week rows.

Add a deterministic regression test that:

- constructs a small multi-district time panel;
- performs the intended temporal join;
- verifies exact key alignment after merge;
- fails if values are reassigned by positional `.values` semantics.

Also retain the cross-feature variance diagnostic that exposed the bug.

Do not rely only on range/seasonality checks.

---

# 14. WP4 is not yet “spatial CV complete” unless model performance has been evaluated under the folds

The current push has strong WP4 groundwork:

- fold geometry;
- boundary-distance buffers;
- leakage checks;
- power table;
- residual Moran's I / variogram analysis;
- proposed adjacency/minimum buffer.

But this should be described as:

> WP4 fold design and spatial-range analysis complete

until models are actually trained/evaluated under the spatially held-out folds.

To complete WP4:

1. Ratify the buffer rule before model performance is viewed under competing radii.
2. Freeze the selected radius.
3. Run the registered reference model under buffered LOOCV.
4. If feature selection is part of the geomatics stress test, perform selection **inside each training fold**.
5. Report fold-level performance, variability, calibration, and failure/degeneracy counts.
6. Compare against ordinary temporal holdout carefully; do not claim external validation.

Sri Lanka remains a compact-country spatial sensitivity, not a national external validation study.

---

# 15. WP4 autocorrelation language must remain conservative

Allowed:

> Residual spatial autocorrelation was not detectably different from the permutation null at the evaluated distance bands.

Allowed:

> The observed residual spatial correlation was small under the tested representation.

Avoid:

> spatial autocorrelation is zero.

Avoid:

> spatial dependence is absent.

The current n=26 design has limited power for small spatial structure.

---

# 16. WP5: distinguish weight-field evidence from completed climate-exposure evidence

The current push reports that population weighting can shift temperature exposure by roughly -1.75 to +0.83 °C using the weight/elevation-lapse construction.

This is scientifically interesting, but do not call WP5 complete until actual climate/exposure products are staged and compared.

Complete WP5 with the intended exposure products.

At minimum evaluate:

- area-weighted temperature;
- population-weighted temperature;
- fractional-overlap population weighting;
- precipitation where planned and available;
- any other preregistered exposure variable.

Report exposure differences before inspecting model performance.

---

# 17. WorldPop coastal sensitivity remains mandatory

The center-in-polygon approach loses approximately 3.5% of national population, concentrated near coastal areas.

Do not assume within-unit normalization makes this harmless.

Implement fractional/boundary-aware weighting and calculate, for each unit and exposure:

`Delta X_i = X_fractional_i - X_center_i`

Report:

- median absolute difference;
- maximum absolute difference;
- relative difference where meaningful;
- rank correlation;
- most affected RDHS units;
- whether downstream model results change.

Only after this analysis may the coastal shortfall be described as negligible, if supported.

---

# 18. Revisit the `all_touched` finding before final exposure construction

The current work reports that the `all_touched` mask can misallocate a substantial fraction of coarse-grid weight relative to fractional overlap.

Treat this as a methodological warning.

For final WP5 exposure estimates:

- prefer fractional cell-polygon overlap for coarse grids when computationally feasible;
- compare against the previous mask approach;
- quantify the difference;
- choose the primary method on validity grounds, not forecasting performance.

---

# 19. Do not overinterpret UHI at RDHS scale

Retain the scale-specific finding:

> At the 26-RDHS aggregation, built-up fraction shows little linear association with district-mean daytime LST.

Do not write:

- Sri Lanka has no urban heat island;
- urbanization has no thermal effect;
- built environment is unrelated to dengue.

Treat this as a spatial-support/MAUP result.

---

# 20. Land-cover annual instability remains a measurement issue

Do not use noisy year-to-year land-cover class changes as a biological urbanization trajectory.

Use a defensible frozen epoch for the primary static feature set unless a validated temporal-change method is developed independently of outcomes.

Retain annual tables as sensitivity/provenance evidence.

---

# 21. Add a model-nomenclature registry before integration

Historical M6/M7 labels are already overloaded in this repository.

Create:

`docs/MODEL_NOMENCLATURE_REGISTRY_v44.md`

For every model label record:

- original name;
- country;
- feature set;
- code path;
- historical/current status;
- manuscript-facing descriptive name.

Prefer descriptive names in the manuscript rather than overloaded M6/M7 identifiers.

Suggested names:

- Surveillance baseline
- Climate-only
- Full climate hybrid
- Matched no-climate comparator
- Geomatics-core standalone
- Surveillance + geomatics stress test
- Matched no-geomatics comparator

---

# 22. Do not move the new results into v44 until these gates are resolved

Before editing the final v44 title, abstract, Results, Discussion, or conclusion, require explicit status for:

- M6-core feature manifest;
- target-provenance issue;
- original training-row mismatch;
- feature-lock chronology;
- matched geomatics estimand;
- registered contrast deviation;
- common calibration protocol if calibrated contrasts are used;
- WP4 actual spatial-CV performance;
- WP5 actual exposure comparison;
- fractional WorldPop sensitivity;
- reference verification;
- result-to-artifact provenance.

Each item should be:

- PASS
- REVIEW
- BLOCKED
- NOT_VERIFIED

Do not treat unresolved items as implicit PASS.

---

# 23. Manuscript framing if the current qualitative result survives

If the final validated evidence remains similar, the appropriate conclusion is not:

> geomatics failed.

A stronger and more defensible interpretation is:

> Standalone landscape and remotely sensed geomatics features carried substantially less short-lead decision value than surveillance-containing models, while exposure construction itself was sensitive to spatial weighting. This suggests that environmental early-warning conclusions depend not only on which environmental variables are included, but also on their temporal information content, comparator strength, and spatial support.

This is compatible with an honest null M6 result.

Do not imply causal environmental effects.

---

# 24. Recommended execution order

Execute in this order:

1. Freeze current `ff6287d0...` M6-core outputs and hashes.
2. Audit the exact feature columns and label the model M6-core if Batch D is absent.
3. Build the target-provenance report.
4. Attempt recovery of the original frozen threshold/training artifact.
5. Build the feature chronology and determine whether a genuine pre-outcome lock existed.
6. Create the model nomenclature registry.
7. Recover M0/M1/M2 frozen predictions if possible, or document the protocol deviation.
8. Define and freeze the matched geomatics ablation base before running it.
9. Run the matched geomatics comparison only on identical rows with matched machinery.
10. Complete WP4 actual buffered-LOOCV model performance.
11. Complete WP5 climate exposure staging.
12. Run fractional WorldPop/boundary sensitivity.
13. Run MODIS-backfill/fresh-data sensitivity if feasible.
14. Create a final claim-to-artifact provenance table.
15. Only then integrate the geomatics/spatial findings into `manuscript_v44`.

---

# 25. Stop conditions

Stop and report `BLOCKED` rather than improvising if:

- the original target artifact cannot be recovered and independent training-only reconstruction cannot be verified;
- the matched geomatics base cannot be specified without outcome-driven choice;
- evaluation rows differ between compared models;
- spatial-CV fold selection is changed after viewing performance;
- WP5 exposure methods are selected based on predictive performance;
- missing MODIS data require future-informed imputation;
- Batch D is absent but the model is being described as the full original M6;
- provenance/hashes cannot establish which artifact produced a manuscript number.

---

# 26. Final scientific standard

The M6 work should survive the following questions from a hostile reviewer:

1. Was the feature set fixed before the outcome influenced model design?
2. Was the target reconstructed without using test labels to define training labels?
3. Were the models compared on exactly the same rows?
4. Does the contrast actually estimate incremental geomatics value, or only standalone performance?
5. Was calibration handled comparably?
6. Was temporal availability leakage prevented?
7. Was spatial generalization actually evaluated rather than inferred from Moran's I?
8. Was population weighting validated with fractional coastal coverage?
9. Are all headline numbers traceable to frozen artifacts?
10. Would the conclusions remain unchanged if M6 stays null?

The correct answer to question 10 must be **yes**.

Do not optimize the work for a positive geomatics result.

Optimize it for a result that is reproducible, interpretable, and defensible.