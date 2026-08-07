# Claude Code Execution Prompt — v44 Round 2: Real-LaTeX Audit Repair, Geomatics/M6 Execution, and Manuscript Integration

## Mission

Continue work on:

`Singati2/srilanka-dengue-ews-calibration`

Starting from the latest audit-repair implementation on branch:

`agent/v44-geomatics-integration`

This round exists because the first v44 audit repair improved the gate semantics, but a critical synthetic-test / real-document mismatch remains. The audit must be made trustworthy against the actual LaTeX manuscript before the geomatics work is allowed to drive a v44 manuscript.

The final objective is still a scientifically coherent v44 paper built around the question:

> **When does environmental information add useful predictive or decision value beyond recent dengue surveillance, and how do calibration, comparator structure, temporal information, spatial scale, and geomatics fidelity change that conclusion?**

The paper is an **incremental-information and validity-audit study**, not a causal-climate paper, not a forecasting leaderboard, and not a claim of deployment readiness.

Do not merge to `main` in this task.

---

# 0. Non-negotiable operating rules

1. **Preserve v43 as historical evidence.**
   - Do not silently edit `manuscript_v43/revised_manuscript.tex` to make tests pass.
   - v43 must remain auditable as the pre-v44 manuscript.
   - If a contradiction exists in v43, the audit must detect it as a contradiction.
   - Repair the wording only in the new v44 manuscript candidate.

2. **Never fabricate completion.**
   - No invented M6 metrics.
   - No invented spatial-CV result.
   - No invented MAUP result.
   - No invented DOI, reference support, author declaration, ethics statement, funding statement, ORCID, or public-repository verification.

3. **Do not upgrade evidence status.**
   - `post_hoc_exploratory` stays post hoc.
   - `post_result_design_locked` stays post-result design-locked.
   - reviewer-responsive work must be identified as such.
   - a green software test does not imply a scientifically validated result.

4. **Do not use test-set outcomes to choose geomatics features.**
   - Freeze the geomatics feature specification before any outcome-aware M6 fitting or feature selection.
   - If a feature is added after outcome access, mark it as post-outcome exploratory and keep it out of any stronger claim.

5. **No blind merges.**
   - Inspect every branch/PR before importing it.
   - Preserve provenance and chronology.

6. **No silent nomenclature changes.**
   - The repository contains historical M6/M7 naming that may conflict with the newer geomatics-only M6 definition.
   - Resolve this explicitly in a model registry before writing v44.

7. **Every strong PASS must mean the property was actually demonstrated.**
   - Presence-only checks are `PARTIAL`, `REVIEW`, or `NOT_VERIFIED`.

---

# 1. Current evidence and known problem you must verify yourself

## 1.1 Current v43 contradiction

The real v43 manuscript contains a Methods statement equivalent to:

> the refit-both-models pipeline was not re-executed, so development-inclusive proper-score intervals were gated and not computed.

But the Results later report development-inclusive proper-score intervals, including values such as:

- Sri Lanka ΔNLL approximately `-0.0403` to `+0.0040`
- Sri Lanka ΔBrier approximately `-0.0153` to `+0.0013`
- Colombia ΔNLL approximately `-0.0224` to `-0.0002`
- Colombia ΔBrier approximately `-0.0102` to `-0.0004`

Do not trust this prompt blindly. Verify both statements directly from `manuscript_v43/revised_manuscript.tex`.

## 1.2 Why the current detector can still miss it

The current detector uses a regex similar to:

```python
r'[+\-]?\d\.\d{3,4}\s*(?:to|,)\s*[+\-]?\d\.\d{3,4}'
```

The synthetic test uses plain text like:

```text
-0.0403 to +0.0040
```

But the real LaTeX manuscript contains constructs like:

```latex
$-0.0403$ to $+0.0040$
```

The intervening TeX math delimiters can cause a synthetic test to pass while the real document escapes detection.

Your first task is to prove or disprove this failure against the actual repository file.

---

# 2. Phase A — Repair the contradiction detector using the actual manuscript

## 2.1 Do not “repair” v43 to satisfy the test

The correct regression behavior is:

- actual `manuscript_v43/revised_manuscript.tex` → contradiction **DETECTED**;
- a corrected v44 version → contradiction **NOT detected**.

A test that expects the real v43 file to be “consistent” is historically wrong.

## 2.2 Normalize LaTeX before semantic checks

Implement a small deterministic normalization layer for audit parsing. It should preserve scientific meaning while removing formatting noise that breaks exact matching.

At minimum handle:

- `$...$` inline math delimiters;
- `\(...\)` math delimiters;
- `\texttt{...}`;
- `\emph{...}`;
- escaped percent signs;
- non-breaking `~` where relevant;
- repeated whitespace/newlines;
- simple TeX commands around symbols when needed for interval recognition.

Do **not** attempt to build a full TeX parser unless necessary.

A good pattern is:

```python
raw_tex -> normalized_semantic_text -> contradiction/query rules
```

Do not destructively strip minus signs, decimal values, or words such as “development-inclusive”, “not computed”, “refit-both-models”, “NLL”, or “Brier”.

## 2.3 Make interval recognition LaTeX-tolerant

The detector must recognize at least all of these as equivalent:

```text
-0.0403 to +0.0040
$-0.0403$ to $+0.0040$
(-0.0403, +0.0040)
[-0.0403, +0.0040]
\(-0.0403\) to \(+0.0040\)
```

Do not overfit only to the four current values.

## 2.4 Real-file regression test is mandatory

Add a test that reads the actual tracked file:

`manuscript_v43/revised_manuscript.tex`

and asserts:

```python
contradiction is True
```

Do not substitute only a synthetic string.

Synthetic tests are still useful, but they are insufficient.

Also add a targeted test against the exact LaTeX sentence/interval structure present in v43.

## 2.5 Preserve a historical audit result

Create an explicit v43 historical consistency report, for example:

`audit/V43_HISTORICAL_MANUSCRIPT_AUDIT.md`

It should state that v43 contains the proper-score Methods/Results contradiction and that v44 is intended to repair it without rewriting history.

---

# 3. Phase B — Make manuscript selection explicit

The current ingestion logic tends to assume one canonical manuscript path. That becomes unsafe once v44 is created.

Implement explicit manuscript targeting.

Preferred behavior:

```bash
python -m agent_graph.run_audit --repo . --manuscript manuscript_v43/revised_manuscript.tex
python -m agent_graph.run_audit --repo . --manuscript manuscript_v44/revised_manuscript.tex
```

If changing the CLI is impractical, implement an equally explicit deterministic configuration mechanism.

Requirements:

1. v43 and v44 must be separately auditable.
2. The knowledge graph must not silently replace the v43 manuscript node with v44.
3. Audit output must record exactly which manuscript path and SHA/commit were evaluated.
4. `SUBMISSION READY` may only refer to the explicitly targeted manuscript.

---

# 4. Phase C — Finish the false-PASS cleanup

The previous round correctly downgraded:

- TEMPORAL LEAKAGE → `NOT_VERIFIED`
- REPRODUCIBILITY → `NOT_VERIFIED`
- REFERENCE INTEGRITY → `NOT_VERIFIED`

Keep those semantics unless stronger checks are truly executed.

Now audit the remaining strong PASS gates.

## 4.1 MODEL SPECIFICATION

The current check is not sufficient if it only searches for words or simple patterns.

A strong PASS requires evidence for the actual model specification, including where applicable:

- feature blocks;
- transformations;
- lag windows;
- scaler fitting scope;
- penalty/model family;
- tuning procedure;
- split boundaries;
- fixed-effect basis;
- recalibration definition;
- comparator structure;
- outcome definition;
- horizon.

If those are not programmatically cross-checked against scripts/config/results, use `PARTIAL` or `NOT_VERIFIED`.

## 4.2 CALIBRATION

The presence of terms such as:

- calibration;
- CITL;
- slope;
- ICI;
- recalibration;

is not enough for PASS.

A strong calibration PASS requires verifying the implemented recalibration procedure and its timing rules.

At minimum distinguish:

- reporting completeness → can PASS if terms/results are present and internally consistent;
- algorithmic correctness → NOT_VERIFIED unless code and indices are checked;
- temporal deployability → NOT_VERIFIED unless the past-only availability logic is checked.

The gate may be split into subfindings if useful.

## 4.3 ADVERSARIAL REVIEW

The current code is primarily an overclaim-language scanner.

Do not label a keyword lint as a full scientific adversarial review.

Either:

- rename the deterministic gate to `OVERCLAIM LANGUAGE SCAN`, or
- retain `ADVERSARIAL REVIEW` but mark it `PARTIAL` and explicitly say it is a language-level scan only.

A true scientific adversarial review belongs in the final human/LLM review report, not in a regex PASS.

## 4.4 SPATIAL CONSISTENCY

A manuscript containing the words “26 RDHS” and “31 departments” is not proof of spatial correctness.

Strong PASS requires evidence such as:

- geometry/unit count checks;
- join-key consistency;
- adjacency provenance where used;
- Ampara/Kalmunai handling;
- 31-test-department versus 32-fixed-effect-column explanation;
- area/projection checks relevant to each analysis.

Otherwise use `PARTIAL`.

## 4.5 RESULT TRACEABILITY

The current decimal-token matching can produce false associations.

Do not allow `PASS` based on matching a value appearing somewhere in a result document.

Begin moving toward structured provenance:

```text
ManuscriptClaim
  -> ResultMetric
  -> Analysis
  -> Script
  -> Input/FrozenArtifact
  -> Checksum
  -> Commit/Tag
```

At minimum create a manually curated headline-claim manifest for v44 rather than relying only on numeric-token coincidence.

---

# 5. Phase D — Add explicit scientific audit levels

Introduce a clear vocabulary such as:

- `PASS` = directly demonstrated by executed check;
- `PARTIAL` = meaningful subset demonstrated;
- `REVIEW` = suspicious/incomplete evidence requires review;
- `NOT_VERIFIED` = not tested by the current audit;
- `FAIL` = demonstrated violation/blocker.

Then document examples.

Example:

```text
CI workflow green                         = PASS for CI execution
Lockfile exists                           = PARTIAL for environment documentation
Full analysis reproduced in clean env     = PASS for that reproduction target
Citation key resolves                     = PASS for key integrity
Paper actually supports manuscript claim  = NOT_VERIFIED until source checked
No .interpolate() found                   = PARTIAL for leakage lint
Feature availability timeline verified    = PASS for that leakage dimension
```

This distinction must appear in the README/audit report so future agents do not accidentally re-inflate statuses.

---

# 6. Phase E — Import and reconcile the actual geomatics work

The geomatics work currently lives in PR #1 / branch:

`m6-geomatics-notebooks`

Observed PR head previously:

`13808979cf34719fc765f75b18ce623e5b760e59`

Re-fetch and verify the current head before importing.

Do not blindly merge.

Inspect:

- `docs/M6.md`
- `docs/study_decision_log.md`
- `notebooks/00_setup_and_geometry.ipynb`
- `notebooks/01_terrain_batchA.ipynb`
- `notebooks/02_dynamic_modis.ipynb`
- `notebooks/03_batchB_statics.ipynb`
- `notebooks/README.md`
- `notebooks_requirements_lock.txt`

Preserve the documented chronology and provenance.

## 6.1 Known geomatics findings to verify

Verify, do not merely repeat, the current documented findings:

- static A+B features cannot encode weekly “when” by themselves;
- MODIS dynamic composites must use availability-safe end dates;
- land-cover annual classification noise motivated a single-epoch decision;
- the RDHS-scale built-up/LST relationship is weak while other cross-product relationships are strong;
- this is interpreted as a spatial-scale/MAUP observation, not proof that urban heat has no effect;
- WorldPop center-in-polygon aggregation loses roughly a few percent at the coastline;
- batch-B vintages do not span the entire 2018–2025 period;
- the feature tables and rasters remain quarantined.

If any of these no longer holds after reinspection, update the decision log transparently.

---

# 7. Phase F — Resolve the M6/M7 naming collision before analysis

The repository has historical code/commits where labels such as M6/M7 were used for other geospatial/SPI model variants, while the newer `docs/M6.md` defines M6 as a geomatics-only model.

This is dangerous for the manuscript.

Create:

`docs/V44_MODEL_REGISTRY.md`

with one row per conceptual model.

Required fields:

```text
stable_id
historical_label
current_manuscript_label
country
feature_blocks
contains_recent_cases
contains_reanalysis_climate
contains_remote_sensing
contains_static_geomatics
contains_geographic_fixed_effects
calibration
analysis_status
source_script/notebook
notes
```

Do not reuse the same manuscript label for two scientifically different models.

A safe option is to use new v44-specific identifiers such as:

- `G0` = geomatics-only;
- `G1` = surveillance + geomatics;
- `G2` = full matched model + geomatics;

while retaining historical filenames/labels in the registry.

Do not adopt those labels blindly if another clearer scheme fits the repository better.

The key requirement is unambiguous identity.

---

# 8. Phase G — Freeze the geomatics experiment before outcome access

Before joining the dengue outcome table, write and commit a geomatics analysis lock:

`analysis/geomatics_v44/ANALYSIS_LOCK.md`

This lock must be committed before the first outcome-aware model fit.

It must specify:

1. exact feature set;
2. exact source/vintage for every feature;
3. static vs dynamic classification;
4. transformations;
5. lag construction;
6. missingness handling;
7. past-only fill rules;
8. model family;
9. regularization/tuning plan;
10. train/validation/test split;
11. outcome threshold construction;
12. forecast horizon;
13. primary metric(s);
14. secondary metric(s);
15. calibration method;
16. cluster-bootstrap unit and seed;
17. row-comparability rule;
18. stop rules;
19. analysis status (`post_hoc_exploratory` unless evidence supports another label);
20. which analyses are standalone-signal versus incremental-ablation questions.

## 8.1 Decide A+B+C versus A+B+C+D before outcomes

Batch D may still be incomplete.

Make the decision **before outcome access**:

- complete D using outcome-blind acquisition, or
- lock a clearly named A+B+C geomatics-v1 feature set and state that D is outside the present experiment.

Do not look at outcome performance and then decide whether D is “needed.”

---

# 9. Phase H — Define two different geomatics questions

A standalone geomatics model and an incremental geomatics ablation answer different questions.

The paper should not conflate them.

## 9.1 Standalone geomatics question

A geomatics-only model asks:

> Does landscape + remotely sensed environmental information carry standalone predictive signal for future elevated dengue activity?

This is useful, but it does **not** estimate the incremental geomatics contribution beyond surveillance.

## 9.2 Incremental geomatics question

To support the v44 reframe, also define a matched incremental contrast if technically feasible:

```text
base model
vs
same base model + geomatics block
```

Examples could be:

- surveillance-only vs surveillance + geomatics;
- matched no-geomatics hybrid vs same hybrid + geomatics.

The exact base model must be chosen before outcome-aware optimization and must preserve identical rows, preprocessing, model family, tuning logic, and recalibration except for the geomatics block.

Do not call an unmatched comparison a “geomatics effect.”

## 9.3 Static “where” vs dynamic “when”

Explicitly separate:

- static/slow geomatics = mostly spatial “where” information;
- dynamic remote sensing = potential temporal “when” information.

Do not interpret weak weekly performance of static-only features as evidence that the underlying environmental factor is scientifically irrelevant.

A useful decomposition, if locked before outcomes, is:

```text
G_static
G_dynamic
G_full = static + dynamic
```

Only do this if it is locked before outcome inspection and sample size supports it.

---

# 10. Phase I — Stage the identical evaluation rows

This is the hard comparability gate.

M6/geomatics must be evaluated on the intended same analysis rows as the relevant comparator.

Locate the authoritative frozen row keys used by M1/M2/M5.

Create a row manifest such as:

`analysis/geomatics_v44/ROW_MANIFEST.json`

It should record:

- row-key definition;
- N total;
- N train/validation/test;
- unit count;
- test event count/prevalence;
- outcome threshold provenance;
- horizon;
- checksum of row IDs;
- checksum of outcome vector if legally/ethically safe to store as metadata only;
- comparator row-key checksum;
- exact equality result.

Require:

```text
geomatics_test_row_keys == comparator_test_row_keys
```

for any claim of direct performance comparison.

If remote-sensing availability forces a smaller sample, do **not** casually compare against the original full-row M1/M5 metrics.

Instead either:

- rebuild all relevant comparators on the shared complete-case mask, or
- label the geomatics analysis as a separate subset experiment.

Never mix denominators silently.

If the necessary outcome table cannot be located, stop this phase with an exact blocker report instead of inventing a substitute.

---

# 11. Phase J — Temporal leakage audit for geomatics

Before fitting, create an executable temporal-availability audit.

## 11.1 MODIS composites

For every dynamic composite used at forecast origin `t`:

```text
composite_end <= forecast_origin
```

must hold under the retrospective availability approximation.

Never join by composite start date if the composite extends past the forecast origin.

## 11.2 Fill rules

No bidirectional interpolation across missing weeks.

Allowed only if locked and justified:

- carry-forward from prior available values;
- past-only rolling summaries;
- missingness indicators.

No `bfill`.

No interpolation using future composites.

## 11.3 Product publication latency

Composite end date is not necessarily real-world release time.

If exact MODIS product latency is not modeled, state clearly that the analysis enforces observation-window availability but not necessarily operational publication latency.

If feasible, add a latency-buffer sensitivity without choosing the buffer based on test performance.

## 11.4 Training-only operations

Verify that the following use no test information:

- scaling;
- imputation parameters;
- feature screening;
- regularization/tuning;
- target threshold construction;
- calibration fit;
- baseline climatology.

## 11.5 Recalibration observability

For rolling recalibration, a previous forecast-outcome pair is usable only when its outcome would have become observable before the next forecast origin.

Check this explicitly for `h=4` rather than assuming all previous calendar weeks are available.

Create:

`analysis/geomatics_v44/TEMPORAL_AVAILABILITY_AUDIT.md`

and machine-readable JSON where possible.

A temporal-leakage PASS for geomatics is allowed only if these executed checks pass.

---

# 12. Phase K — Fit and evaluate geomatics only after all gates above pass

Use the same scientific discipline as the matched climate analysis.

Minimum primary evaluation set:

- AUC;
- PR-AUC;
- Brier score;
- NLL/log loss;
- CITL;
- calibration slope;
- ICI if used consistently;
- net benefit across the threshold grid;
- reference `p*=0.30` only as the existing illustrative threshold;
- comparison against alert-all and alert-none.

Report both point estimates and uncertainty with the correct interpretation.

Do not turn zero-exclusion into a claim of operational importance.

## 12.1 Bootstrap

Use the scientifically appropriate cluster unit.

For Sri Lanka, likely RDHS-level clustering unless the locked design states otherwise.

Conditional bootstrap is not equivalent to development-inclusive refitting.

If development-inclusive geomatics refits are computationally feasible, run them under a locked protocol.

If not, explicitly state that geomatics uncertainty is conditional only and do not compare its robustness directly to a DI climate result as if they were equivalent.

## 12.2 Sensitivities

Only after the primary geomatics result is frozen may you run planned sensitivities such as:

- 90th-percentile outcome;
- alternate horizons;
- static vs dynamic block;
- product-latency buffer;
- population-boundary weighting;
- alternate calibration.

Each must retain an explicit analysis-status label.

---

# 13. Phase L — WP4 spatial validation

Integrate WP4 only if the required data and code are available.

Do not call ordinary random CV “spatial validation.”

Where feasible, implement or complete the preplanned spatial-honest evaluation using blocked or held-out spatial units.

Required questions:

1. Does model performance fall when evaluated on spatially separated units?
2. Does the incremental environmental block survive spatial separation?
3. Is residual spatial autocorrelation still present?
4. Are conclusions sensitive to the spatial unit definition?

If the existing WP4 plan cannot be executed because necessary staged data are missing, create a precise blocker report and do not invent results.

---

# 14. Phase M — WP5 MAUP / population-weighting sensitivity

Address the documented WorldPop coastline issue before using population-weighted exposure as a strong result.

At minimum compare:

- existing center-in-polygon population allocation;
- fractional-coverage/boundary-aware allocation if feasible.

Quantify whether differences materially change:

- population denominators;
- climate/remote-sensing exposure summaries;
- matched environmental increments;
- model ranking.

Keep the interpretation narrow:

MAUP / boundary sensitivity shows dependence on spatial aggregation and exposure construction. It does not prove a biological mechanism.

If WP5 remains blocked, keep it as an explicit future/ongoing analysis rather than pretending completion.

---

# 15. Phase N — Create a v44 manuscript only after evidence gates are satisfied

Create:

`manuscript_v44/revised_manuscript.tex`

by copying v43 and then editing the copy.

Do not overwrite v43.

Before full prose rewriting, create:

`docs/V44_REFRAME_BLUEPRINT.md`

with:

- central question;
- experimental sequence;
- primary versus exploratory components;
- manuscript section map;
- exact claims each experiment can support;
- exact claims each experiment cannot support.

## 15.1 Required v44 Methods correction

Retire the stale v43 sentence saying development-inclusive proper-score intervals were not computed if the repository evidence shows they were subsequently computed.

Use provenance-supported wording such as:

- conditional proper-score intervals were first computed on frozen predictions;
- a later reviewer-responsive development-inclusive refit-both-model analysis was subsequently executed;
- both analyses are post-result/post-hoc as appropriate;
- the DI result weakens the Sri Lanka evidence and leaves Colombia boundary-adjacent.

Use the exact chronology after verifying commits/scripts/results.

## 15.2 Reframed experimental sequence

A coherent v44 structure should consider:

1. surveillance benchmark;
2. climate-only and hybrid ladder;
3. matched climate ablation;
4. calibration and threshold-free proper-score robustness;
5. geomatics-only standalone signal;
6. matched incremental geomatics contrast, if successfully executed;
7. static “where” vs dynamic “when” interpretation;
8. spatial-CV robustness, if completed;
9. MAUP/population-weighting sensitivity, if completed;
10. integrated conclusion about incremental environmental information.

Do not force every item into the paper if the experiment is incomplete or weakly supported.

## 15.3 Reframe without overclaiming

The likely high-level interpretation, subject to the new results, is:

> recent surveillance contains strong short-lead information; environmental blocks can add modest incremental probability or decision information in some settings, but their apparent utility depends on comparator structure, calibration, model-development uncertainty, temporal availability, and spatial aggregation.

Do not write this as a final conclusion until the geomatics results are known.

## 15.4 Geomatics null results are acceptable

If geomatics-only or incremental geomatics performance is weak, report that honestly.

A scientifically useful conclusion may be that:

- static landscape features encode spatial risk context but little weekly timing;
- dynamic remote sensing carries some timing information but may add little beyond recent surveillance;
- coarse administrative aggregation suppresses local physical relationships such as UHI;
- adding more environmental variables does not guarantee operational early-warning value.

Do not try to rescue a weak result with selective feature additions after outcome inspection.

---

# 16. Phase O — Build a structured v44 claim manifest

Create:

`audit/V44_CLAIM_MANIFEST.yaml`

For every headline numerical or scientific claim, include:

```yaml
claim_id:
  manuscript_section:
  exact_claim_text:
  analysis_status:
  country:
  estimand:
  metric:
  point_estimate:
  interval:
  result_file:
  result_key_or_row:
  generating_script:
  input_artifacts:
  input_checksums:
  seed:
  environment:
  git_commit_or_tag:
  verification_status:
  limitations:
```

The goal is to reduce reliance on decimal-token matching.

At minimum cover:

- Sri Lanka matched climate ΔNB;
- Colombia matched climate ΔNB;
- proper-score ΔNLL/ΔBrier headline values;
- DI proper-score intervals;
- 90th-percentile matched results;
- any geomatics headline metric;
- any spatial-CV headline metric;
- any MAUP sensitivity headline metric.

---

# 17. Phase P — Reference verification

The deterministic audit may remain `NOT_VERIFIED` for scientific reference support unless actual source checking is performed.

If network access is available, verify high-stakes claims against authoritative sources.

Prioritize:

- OpenDengue version/provenance;
- climate-data product papers and official product documentation;
- DCA methodological claims;
- TRIPOD+AI / PROBAST+AI statements;
- novelty claims;
- geomatics/MAUP methodological claims;
- MODIS temporal/composite interpretation;
- WorldPop methodological statements.

For each high-stakes reference, verify:

- title;
- authors;
- year;
- journal/source;
- DOI/identifier;
- whether the source actually supports the manuscript sentence.

Do not invent missing DOIs.

Create:

`audit/V44_REFERENCE_VERIFICATION.md`

with VERIFIED / PARTIAL / NOT_VERIFIED / CONTRADICTED statuses.

---

# 18. Phase Q — Tests required before claiming audit repair complete

The test suite must include at least the following.

## 18.1 Real v43 contradiction

```python
real_v43 -> contradiction == True
```

## 18.2 Corrected v44 consistency

Once v44 exists:

```python
real_v44 -> contradiction == False
```

## 18.3 LaTeX formatting variants

Tests for intervals with:

- `$...$`;
- `\(...\)`;
- parentheses;
- brackets;
- comma-separated CIs;
- `to` CIs.

## 18.4 Gate semantics

- lockfile-only reproducibility must not PASS;
- citation-key-only reference integrity must not PASS;
- keyword-only calibration must not PASS;
- keyword-only model specification must not PASS;
- overclaim regex scan alone must not earn “full scientific adversarial review PASS”.

## 18.5 M6 temporal availability

Use synthetic dates to prove:

```text
composite_start < t < composite_end
```

is rejected.

Also test exact equality edge cases.

## 18.6 Row identity

Test that the direct-comparison gate fails if even one test row differs.

## 18.7 Historical manuscript immutability

Add a checksum or git-diff guard ensuring v43 is not modified during v44 construction unless an explicit historical correction commit is separately authorized.

---

# 19. Phase R — Final audit statuses

At the end, produce both:

`audit/V44_FINAL_KG_AGENT_AUDIT.md`

and:

`audit/V44_FINAL_KG_AGENT_AUDIT.json`

The report must distinguish:

- software tests;
- scientific result reproduction;
- temporal-validity checks;
- reference verification;
- manuscript consistency;
- author-supplied submission declarations.

Do not write:

> “blocked only by paperwork”

unless all scientific gates really are demonstrated.

---

# 20. Phase S — Harsh multi-perspective review

After v44 exists and the executable analyses are complete, produce:

`V44_HARSH_REVIEW_AND_INTEGRATION_REPORT.md`

Use these perspectives:

1. epidemiologic forecasting reviewer;
2. biostatistics / uncertainty reviewer;
3. calibration / prediction-model reviewer;
4. geospatial / GIS / MAUP reviewer;
5. remote-sensing temporal-validity reviewer;
6. reproducibility / research-software reviewer;
7. causal-inference skeptic;
8. journal editor / desk-rejection reviewer.

Each reviewer must report:

- strongest contribution;
- critical flaw;
- major concerns;
- minor concerns;
- claims that are too strong;
- missing experiment if any;
- accept / minor / major / reject recommendation;
- score 1–10.

Then provide a consensus verdict.

Do not simulate unanimity if reviewers would reasonably disagree.

---

# 21. Required deliverables

At minimum, this round should produce or update:

```text
prompts/CLAUDE_V44_ROUND2_REAL_LATEX_AUDIT_AND_M6_EXECUTION.md

audit/V43_HISTORICAL_MANUSCRIPT_AUDIT.md
audit/V44_CLAIM_MANIFEST.yaml
audit/V44_REFERENCE_VERIFICATION.md
audit/V44_FINAL_KG_AGENT_AUDIT.md
audit/V44_FINAL_KG_AGENT_AUDIT.json

docs/V44_MODEL_REGISTRY.md
docs/V44_REFRAME_BLUEPRINT.md

analysis/geomatics_v44/ANALYSIS_LOCK.md
analysis/geomatics_v44/ROW_MANIFEST.json
analysis/geomatics_v44/TEMPORAL_AVAILABILITY_AUDIT.md

manuscript_v44/revised_manuscript.tex

V44_HARSH_REVIEW_AND_INTEGRATION_REPORT.md
```

Some downstream files may legitimately remain absent if the corresponding analysis is blocked. If so, create a blocker report rather than a fake placeholder result.

---

# 22. Git workflow

1. Work on a dedicated branch descended from the current v44 implementation branch.
2. Do not merge to `main`.
3. Keep commits logically separated, for example:
   - real-LaTeX audit repair;
   - gate-semantics repair;
   - geomatics import/model registry;
   - geomatics analysis lock;
   - row/temporal audit;
   - M6 execution;
   - WP4/WP5 execution;
   - v44 manuscript integration;
   - final audit/report.
4. Never bundle generated raw data or quarantined surveillance/rasters into git.
5. Push the branch and open/update a draft PR when the work reaches a reviewable state.

---

# 23. Stop conditions

Stop and report rather than improvise if any of the following occurs:

- identical comparator row keys cannot be reconstructed;
- target-threshold provenance is ambiguous;
- dynamic feature timestamps cannot be made availability-safe;
- required raw/quarantined data are missing;
- feature definitions would have to be chosen after seeing outcomes;
- a historical M6/M7 naming collision cannot be resolved unambiguously;
- a manuscript number cannot be traced to a result artifact;
- a reference cannot be verified;
- WP4/WP5 requires data that are not staged;
- a result only exists as an unverified prose statement.

A precise blocker is a valid scientific result of the audit.

---

# 24. Final response format

When finished, report:

## A. Branch / commits
- branch name
- commit SHAs
- PR if created

## B. Audit repair
- real v43 contradiction detected? YES/NO
- corrected v44 contradiction absent? YES/NO/NOT YET
- tests passed / failed
- gate-status changes

## C. Geomatics import
- PR/branch imported
- exact notebooks/scripts incorporated
- data/quarantine integrity
- feature-set lock commit SHA

## D. Comparability
- row-key equality
- target/horizon equality
- split equality
- temporal-availability result

## E. M6 / geomatics results
For each experiment:
- analysis status
- N / units / events
- AUC
- PR-AUC
- Brier
- NLL
- calibration metrics
- net benefit
- conditional uncertainty
- development-inclusive uncertainty if run

## F. Spatial / MAUP
- WP4 status
- WP5 status
- quantitative effect on conclusions

## G. Manuscript
- v43 untouched? YES/NO
- v44 created? YES/NO
- title
- central claim
- claims removed/softened
- unresolved placeholders

## H. Reproducibility
- which analyses actually reran
- which are reconstruction-only
- which remain NOT_VERIFIED

## I. Harsh reviewer verdict
- overall score /10
- submission readiness YES/NO
- exact blockers

---

# 25. Scientific interpretation guardrails

Never convert:

- predictive association → causation;
- environmental feature importance → biological mechanism;
- selected Colombia subset → national validation;
- retrospective finalized surveillance → prospective deployment;
- conditional bootstrap → development-inclusive uncertainty;
- zero-excluding interval → operational importance;
- zero-crossing interval → proof of no effect;
- weak district-level UHI correlation → no urban heat island;
- static geomatics weak weekly prediction → environmental irrelevance;
- software test PASS → scientific validation;
- DOI present → reference supports claim.

---

# 26. Desired v44 endpoint

A scientifically defensible v44 should make it possible for a skeptical reviewer to follow this chain:

```text
What information is available at forecast origin?
        ↓
What does recent surveillance predict?
        ↓
What does climate add under a matched comparator?
        ↓
Does that survive calibration and redevelopment uncertainty?
        ↓
What does geomatics/remote sensing add standalone?
        ↓
What does geomatics add beyond the matched base model?
        ↓
How much depends on static vs dynamic environmental information?
        ↓
How much depends on spatial separation / aggregation / population weighting?
        ↓
What remains useful after all those validity checks?
```

The contribution is not “we found a better dengue model.”

The contribution is a rigorous assessment of **when environmental information appears to add value, how fragile that value is to modeling and spatial choices, and what evidence is required before calling it useful for early warning.**

If the final answer is mostly null, small, or setting-dependent, preserve it. That is preferable to manufacturing a stronger story.

---

# 27. First commands / immediate order of work

Start by doing this in order:

1. verify current branch and clean/dirty state;
2. inspect the actual v43 Methods and Results contradiction;
3. run the current detector on the real v43 file and demonstrate whether it currently fails;
4. fix normalization/detection;
5. add the real-file regression test expecting v43 contradiction = TRUE;
6. run the complete audit test suite;
7. downgrade remaining false-strong PASS gates;
8. only then import/reconcile the geomatics branch;
9. create model registry;
10. freeze geomatics analysis plan before outcome access;
11. stage row manifest and temporal-availability audit;
12. execute M6 only if those gates pass;
13. proceed to WP4/WP5 only if inputs exist;
14. create v44 from v43 only after the evidence is ready;
15. run the final audit and harsh review.

Do not skip directly to manuscript rewriting.
