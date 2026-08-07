# Claude Code Prompt — Knowledge Graph + Agent Graph for `srilanka-dengue-ews-calibration`

## Role

Act as a **senior research-software architect, statistical auditor, epidemiological methods reviewer, reproducibility engineer, and adversarial peer reviewer**.

You are working inside the GitHub repository:

```text
https://github.com/Singati2/srilanka-dengue-ews-calibration
```

Your task is **not** to invent a new dengue forecasting model and **not** to rewrite the scientific story to make the results look stronger.

Your task is to build a rigorous **Knowledge Graph + controlled Agent Graph auditing system** around the existing Sri Lanka / Colombia dengue early-warning calibration project so that:

1. every important manuscript claim can be traced to evidence;
2. every reported numerical result can be traced to code, inputs, frozen outputs, seeds, and commits where possible;
3. contradictions between manuscript sections, README files, scripts, results, tables, figures, and git history are automatically detected;
4. post-hoc, exploratory, sensitivity, design-locked, and primary analyses are never conflated;
5. citations can be checked for whether they actually support the associated claim;
6. reproducibility and submission-readiness can be assessed using explicit PASS / FAIL / REVIEW gates;
7. the system remains useful even if the final scientific conclusion is null or negative.

---

# 0. Non-negotiable scientific rules

## 0.1 Do not hallucinate

Do **not** invent:

- datasets;
- analyses;
- output files;
- numerical results;
- confidence intervals;
- references;
- DOIs;
- authors;
- software versions;
- study dates;
- data licenses;
- ethics determinations;
- preregistration status;
- repository tags;
- commit hashes;
- sample sizes;
- performance metrics;
- claims of novelty;
- claims of deployment readiness.

If something cannot be verified from the repository or a legitimate external source, label it:

```text
UNVERIFIED
```

or:

```text
AUTHOR INPUT REQUIRED
```

Do not guess.

---

## 0.2 Preserve null results

Do not optimize the interpretation toward a positive climate result.

The project must remain scientifically valid if the strongest conclusion is:

> climate adds little or no robust short-lead decision value beyond a strong recent-surveillance comparator.

Null, fragile, or calibration-sensitive findings are legitimate results.

---

## 0.3 No silent scientific changes

Never silently change:

- the alert definition;
- horizon;
- threshold;
- model family;
- climate lags;
- feature set;
- train/validation/test split;
- calibration method;
- bootstrap unit;
- seed;
- statistical estimand;
- comparator;
- primary/secondary status;
- uncertainty method.

If a change is scientifically warranted:

1. identify the problem;
2. explain why it matters;
3. classify the proposed change;
4. record whether existing results were already known;
5. do **not** execute a result-changing analysis unless it is clearly separated as a new sensitivity or repair analysis.

---

# 1. Start by inspecting the repository

Before writing code, inspect the current repository comprehensively.

At minimum inspect:

```text
README.md
data/README.md
docs/
scripts/
analysis/
audit_v42/
manuscript/
manuscript_v43/
submission/
qc_summaries/
data_dictionary/
geomatics_templates/
.gitignore
LICENSE
```

Also inspect:

- git status;
- current branch;
- latest commit;
- tags;
- important historical commits;
- tracked analysis outputs;
- frozen outputs;
- environment files;
- manuscript versions;
- audit documents;
- analysis plans;
- preregistration/design-lock documents;
- reference lists;
- figure/table-generation scripts;
- absolute local paths inside scripts;
- tests / CI configuration if present.

Do not assume the root README reflects the actual project state.

---

# 2. Known issues that MUST be independently verified

These are **audit hypotheses**, not facts to blindly accept.

Verify each directly.

## 2.1 Repository status drift

Check whether the root `README.md` still describes the project as being near the geomatics-WP1 stage while the repository now contains a substantially later manuscript and completed Sri Lanka / Colombia analyses.

If confirmed, classify:

```text
REPOSITORY_DOCUMENTATION_DRIFT
```

and identify exactly which documents disagree.

---

## 2.2 Development-inclusive proper-score inconsistency

Check the canonical/current manuscript carefully.

Determine whether one section states that development-inclusive proper-score intervals:

```text
were gated and not computed
```

while later sections state that they:

```text
were subsequently computed
```

and interpret them.

Inspect:

```text
analysis/devincl_proper_scores_v1/
audit_v42/
manuscript_v43/
```

Determine:

- whether the analyses actually exist;
- whether they were executed;
- whether outputs exist;
- whether outputs are tracked;
- whether numbers in the manuscript correspond to those outputs;
- whether the Methods text is stale;
- whether the Discussion/Abstract is stale;
- whether the analysis is post-hoc/reviewer-responsive;
- whether the evidentiary status is described correctly.

Do not simply rewrite text. Establish the provenance first.

---

## 2.3 Absolute machine-specific paths

Search all analysis scripts for paths such as:

```text
/home/mpcrlab/...
```

Determine which scripts cannot run on a clean checkout because of hard-coded local paths.

Classify those scripts as:

```text
PORTABLE
PARTIALLY_PORTABLE
LOCAL_ONLY
```

Do not claim full reproducibility if critical analyses require undocumented machine-specific directories.

---

## 2.4 Environment lock quality

Inspect:

```text
analysis/environment/requirements-lock.txt
```

Determine whether it is:

- a minimal project dependency lock;
- or a full workstation-wide `pip freeze`.

If it includes hundreds of unrelated packages, flag it as an environment-reconstruction weakness.

Recommend a minimal analysis-specific environment in addition to retaining the historical lock.

Do not delete historical evidence.

---

## 2.5 CI / automated testing

Check whether GitHub Actions or another CI system exists.

If no meaningful CI exists, flag:

```text
CI_NOT_ESTABLISHED
```

The new Knowledge Graph / Agent Graph infrastructure must include deterministic tests that can run without private/raw data.

---

## 2.6 Submission placeholders

Search the canonical manuscript for:

```text
AUTHOR INPUT REQUIRED
```

and other unresolved placeholders.

Examples may include:

- ethics;
- funding;
- competing interests;
- CRediT roles;
- acknowledgments;
- ORCID;
- Zenodo DOI;
- data-version identifier;
- code license.

Generate an exact unresolved-submission checklist.

Never fill these from inference.

---

# 3. Build a project Knowledge Graph

Create:

```text
knowledge_graph/
├── README.md
├── schema/
│   ├── entities.yaml
│   ├── relations.yaml
│   └── constraints.yaml
├── ingest/
│   ├── ingest_repository.py
│   ├── ingest_git_history.py
│   ├── ingest_manuscript.py
│   ├── ingest_results.py
│   ├── ingest_scripts.py
│   ├── ingest_references.py
│   └── ingest_audit_docs.py
├── graph/
│   ├── project_graph.json
│   └── project_graph_summary.json
├── queries/
│   ├── unsupported_claims.py
│   ├── contradictory_claims.py
│   ├── untraceable_numbers.py
│   ├── stale_documents.py
│   ├── unresolved_placeholders.py
│   ├── provenance_breaks.py
│   └── analysis_status_conflicts.py
└── tests/
    ├── test_schema.py
    ├── test_ingestion.py
    ├── test_claim_traceability.py
    └── test_constraints.py
```

Prefer a lightweight implementation.

Do **not** introduce Neo4j, cloud infrastructure, or a heavy database unless clearly necessary.

A JSON / JSONL graph plus Python graph logic is acceptable.

`networkx` is acceptable if justified.

---

# 4. Knowledge Graph entities

The schema should support at least the following entity types.

```text
Project
Country
StudySetting
Dataset
DatasetVersion
DataSource
SpatialUnit
TemporalUnit
Outcome
OutcomeDefinition
AlertThreshold
ForecastHorizon
Feature
FeatureBlock
ClimateVariable
Model
ModelFamily
Comparator
CalibrationMethod
Analysis
SensitivityAnalysis
PrimaryAnalysis
SecondaryAnalysis
PostHocAnalysis
BootstrapProcedure
StatisticalEstimand
Metric
Result
ConfidenceInterval
Figure
Table
Manuscript
ManuscriptSection
ManuscriptClaim
Reference
DOI
Script
Function
FrozenArtifact
Checksum
Environment
Seed
GitCommit
GitTag
AuditFinding
ReleaseGate
AuthorInput
```

Do not create meaningless entities merely to make the graph large.

---

# 5. Required relationships

At minimum support relationships like:

```text
USES
DERIVED_FROM
GENERATED_BY
EXECUTED_WITH
EVALUATED_ON
SPLIT_INTO
CALIBRATED_BY
COMPARES
ABLATES
PRODUCES
SUPPORTS
CONTRADICTS
APPEARS_IN
CITED_BY
CITES
HAS_CHECKSUM
FROZEN_AT
INTRODUCED_IN
MODIFIED_IN
REPORTED_IN
DEPENDS_ON
VALIDATES
REPRODUCES
FAILS_TO_REPRODUCE
CLASSIFIED_AS
SUPERSEDES
REQUIRES_AUTHOR_INPUT
```

Relationships should preserve enough metadata to explain **why** an edge exists.

---

# 6. Represent the actual scientific structure

The graph must capture the real scientific question.

Conceptually:

```text
Climate
  ↓
mosquito / transmission environment
  ↓
dengue transmission
  ↓
recent dengue surveillance
  ↓
future dengue activity
```

This matters because recent surveillance may already encode part of the information carried by climate.

Represent the matched comparison explicitly:

```text
M5
= recent cases
+ seasonality
+ geographic structure
+ climate

M5_no_climate
= recent cases
+ seasonality
+ geographic structure
```

Then:

```text
MatchedClimateAblation
COMPARES
M5 ↔ M5_no_climate
```

The graph must distinguish this from a weaker/non-nested comparison such as:

```text
M5 vs M1
```

when structural components differ beyond climate.

---

# 7. Analysis-status ontology

Every analysis must receive one explicit status.

Use controlled labels such as:

```text
PRESPECIFIED
DESIGN_LOCKED
POST_RESULT_DESIGN_LOCKED
POST_HOC
REVIEWER_RESPONSIVE
SENSITIVITY
DIAGNOSTIC
RECONSTRUCTION
REPRODUCIBILITY_GATE
PILOT_NOT_FOR_QUOTING
```

Multiple labels may apply if logically necessary.

The graph must never treat:

```text
POST_HOC
```

as equivalent to:

```text
PRESPECIFIED
```

---

# 8. Claim-level provenance

This is one of the most important requirements.

For each important numerical claim in:

- Abstract;
- Results;
- Discussion;
- Conclusion;
- headline tables;
- figure captions;

attempt to build a provenance path:

```text
ManuscriptClaim
    ↓ SUPPORTED_BY
Result
    ↓ PRODUCED_BY
Analysis
    ↓ GENERATED_BY
Script
    ↓ EVALUATED_ON
DatasetVersion / FrozenArtifact
    ↓ HAS_CHECKSUM
Checksum

Analysis
    ↓ EXECUTED_WITH
Seed / Environment / model specification
```

For every numerical claim classify:

```text
TRACEABLE
PARTIALLY_TRACEABLE
UNTRACEABLE
CONTRADICTORY
```

Generate a machine-readable result.

---

# 9. Detect manuscript contradictions

Implement checks for contradictions such as:

```text
Methods:
analysis not computed

versus

Discussion:
analysis interpreted
```

Other examples:

```text
README says project stage X
current manuscript implies project stage Y

Table says CI A
Abstract says CI B

Methods says municipality bootstrap
script uses department bootstrap

Text says B=10,000
script or output uses B=1,000

Text says post-hoc
another section implies prespecified

Text says Colombia climate block is linear
another section implies DLNM primary block
```

Do not flag harmless wording differences as scientific contradictions.

Provide severity:

```text
CRITICAL
MAJOR
MODERATE
MINOR
INFO
```

---

# 10. Build the controlled Agent Graph

Create:

```text
agent_graph/
├── README.md
├── run_audit.py
├── state.py
├── gates.py
├── agents/
│   ├── coordinator.py
│   ├── repository_agent.py
│   ├── data_provenance_agent.py
│   ├── temporal_leakage_agent.py
│   ├── spatial_agent.py
│   ├── statistical_agent.py
│   ├── calibration_agent.py
│   ├── reproducibility_agent.py
│   ├── claim_agent.py
│   ├── reference_agent.py
│   ├── manuscript_consistency_agent.py
│   ├── adversarial_reviewer.py
│   └── release_agent.py
└── tests/
    ├── test_agent_order.py
    ├── test_release_gates.py
    └── test_failure_propagation.py
```

The Agent Graph must be a **controlled DAG/state machine**, not agents talking indefinitely.

Recommended flow:

```text
Coordinator
    |
    +--> Repository Agent
    +--> Data Provenance Agent
    +--> Temporal Leakage Agent
    +--> Spatial Agent
    +--> Statistical Agent
    +--> Calibration Agent
    +--> Reproducibility Agent
    +--> Reference Agent
             |
             v
       Claim Agent
             |
             v
 Manuscript Consistency Agent
             |
             v
   Adversarial Reviewer
             |
             v
       Release Agent
```

Agents may share the Knowledge Graph as common structured state.

---

# 11. Agent responsibilities

## 11.1 Repository Agent

Check:

- repo structure;
- branch / commit / tags;
- stale docs;
- duplicate manuscript versions;
- untracked scientific outputs;
- code/data separation;
- naming/version ambiguity.

---

## 11.2 Data Provenance Agent

Trace:

### Sri Lanka

```text
WER
WorldPop
Sri Lanka Census
ERA5-Land
CHIRPS
administrative boundaries
```

### Colombia

```text
OpenDengue
climate sources
GADM / spatial boundaries
```

Check:

- source;
- version;
- retrieval date where available;
- checksum;
- license statement;
- local-only dependence;
- regeneration instructions.

---

## 11.3 Temporal Leakage Agent

Check:

- train/validation/test isolation;
- target construction;
- four-week-ahead target;
- direction of lag construction;
- week alignment;
- WER issue week vs ISO climate week;
- scaling;
- penalty selection;
- threshold construction;
- recalibration;
- whether test outcomes leak into predictor generation.

This agent must fail loudly on possible future-information leakage.

---

## 11.4 Spatial Agent

Check:

- 26 RDHS units;
- Ampara/Kalmunai split;
- boundary provenance;
- Colombia GID_2 / department logic;
- selected common-complete subset;
- clustering unit;
- residual spatial-autocorrelation analyses;
- spatial-block bootstrap claims;
- MAUP/change-of-support limitations.

---

## 11.5 Statistical Agent

Verify implementation and interpretation of:

```text
AUC
PR-AUC
Brier score
negative log loss
CITL
calibration slope
decision-curve net benefit
matched ΔNB
conditional bootstrap
development-inclusive bootstrap
wild-cluster sensitivity
spatial-block sensitivity
```

Do not treat “CI excludes zero” as equivalent to:

```text
operationally important
```

or:

```text
clinically/public-health meaningful
```

---

## 11.6 Calibration Agent

Check:

### Sri Lanka

- rolling 52-week past-only intercept recalibration;
- cross-fitted optimistic sensitivity if present.

### Colombia

- validation-period Platt scaling;
- calibration intercept shift sensitivity.

Ensure no non-prospective recalibration is described as deployable.

---

## 11.7 Reproducibility Agent

Classify each important analysis:

```text
FULLY_REPRODUCIBLE_FROM_PUBLIC_SOURCES
REPRODUCIBLE_WITH_LOCAL_REGENERATED_DATA
REPRODUCIBLE_FROM_FROZEN_PREDICTIONS
RECONSTRUCTABLE_WITH_DOCUMENTED_PATHS
LOCAL_MACHINE_DEPENDENT
NOT_REPRODUCED
```

Do not collapse these categories into a generic “reproducible”.

---

## 11.8 Reference Agent

For each high-impact literature claim:

1. verify title;
2. authors;
3. year;
4. journal;
5. DOI;
6. whether the cited source actually supports the associated sentence.

Special attention to claims about:

- dengue climate forecasting;
- calibration;
- decision-curve analysis;
- EWARS-csd;
- OpenDengue;
- external validation prevalence;
- climate vs autoregressive forecasting;
- TRIPOD+AI;
- PROBAST / PROBAST+AI;
- stakeholder threshold interpretation.

Do not use citation count as evidence of correctness.

---

## 11.9 Claim Agent

Extract manuscript claims and attach them to evidence.

Flag:

```text
UNSUPPORTED_NUMERICAL_CLAIM
UNSUPPORTED_NOVELTY_CLAIM
OVERSTATED_CAUSAL_CLAIM
OVERSTATED_GENERALIZABILITY
OVERSTATED_DEPLOYMENT_CLAIM
POSTHOC_PRESENTED_AS_CONFIRMATORY
```

---

## 11.10 Manuscript Consistency Agent

Cross-check:

```text
Title
Abstract
Methods
Results
Discussion
Conclusion
Tables
Figures
Supporting Information
Data availability
Code availability
README
analysis chronology
```

The same analysis must have one scientifically coherent status everywhere.

---

## 11.11 Adversarial Reviewer

Act like a skeptical reviewer for:

```text
PLOS Global Public Health
PLOS Neglected Tropical Diseases
BMC Public Health
Lancet Regional Health–Southeast Asia
Scientific Reports
```

Do not imitate any specific real reviewer.

Attempt to reject the manuscript based on:

- weak novelty;
- post-hoc analysis;
- selection bias;
- temporal leakage;
- threshold arbitrariness;
- weak comparator;
- calibration misuse;
- inappropriate inference;
- spatial dependence;
- lack of external validation;
- lack of prospective validation;
- COVID-era Colombia test period;
- dataset/version ambiguity;
- irreproducibility;
- manuscript inconsistencies;
- overclaiming.

For each criticism classify:

```text
VALID
PARTLY_VALID
NOT_SUPPORTED
```

and explain why.

---

# 12. Release gates

Implement explicit release gates.

At minimum:

```text
G01_DATA_PROVENANCE
G02_TEMPORAL_LEAKAGE
G03_MODEL_SPECIFICATION
G04_ANALYSIS_STATUS
G05_RESULT_TRACEABILITY
G06_MANUSCRIPT_RESULT_MATCH
G07_REFERENCE_INTEGRITY
G08_REPRODUCIBILITY
G09_REPOSITORY_DOCUMENTATION
G10_SUBMISSION_DECLARATIONS
G11_NO_UNRESOLVED_CRITICAL_CONTRADICTIONS
G12_NO_UNSUPPORTED_HEADLINE_CLAIMS
```

Each gate returns:

```text
PASS
FAIL
REVIEW
NOT_APPLICABLE
```

A CRITICAL contradiction must prevent:

```text
SUBMISSION_READY = TRUE
```

---

# 13. Required audit output

Create:

```text
audit/CURRENT_KG_AGENT_AUDIT.md
audit/CURRENT_KG_AGENT_AUDIT.json
```

The markdown report must contain:

## A. Repository identity

- branch;
- commit;
- date;
- canonical manuscript identified;
- important tags.

## B. Executive verdict

Example format:

```text
Scientific coherence:       PASS / REVIEW / FAIL
Result traceability:        PASS / REVIEW / FAIL
Reproducibility:            PASS / REVIEW / FAIL
Manuscript consistency:     PASS / REVIEW / FAIL
Reference integrity:        PASS / REVIEW / FAIL
Submission declarations:    PASS / REVIEW / FAIL

SUBMISSION READY: YES / NO
```

## C. Critical findings

Only genuine submission blockers.

## D. Major findings

Important but not necessarily fatal.

## E. Minor findings

Documentation / cleanup issues.

## F. Numerical claim traceability matrix

Columns:

```text
Claim
Manuscript location
Value
Result source
Script
Input/frozen artifact
Seed
Status
```

## G. Analysis-status matrix

Columns:

```text
Analysis
Primary / secondary
Prespecified?
Design locked?
Post hoc?
Reviewer responsive?
Sensitivity?
Manuscript wording correct?
```

## H. Reproducibility matrix

Columns:

```text
Analysis
Inputs public?
Inputs committed?
Outputs committed?
Script portable?
Environment specified?
Expected runtime class
Reproducibility status
```

## I. Reference audit

## J. Manuscript contradictions

## K. Unresolved author inputs

## L. Exact recommended fixes

For each fix give:

```text
file
location
problem
recommended correction
whether correction changes scientific interpretation
```

---

# 14. Create a stale-document detector

Implement logic to detect repository documentation whose stated status predates the analyses now present.

For example:

```text
README:
Next phase = geomatics WP1

but repository contains:
v43 manuscript
matched ablation
proper-score analysis
development-inclusive bootstrap
spatial sensitivity
```

Flag:

```text
STALE_STATUS_DOCUMENT
```

Do not automatically delete historical docs.

---

# 15. Build numerical-claim extraction conservatively

Do not attempt magical semantic parsing.

Start with:

- LaTeX numerical statements;
- table cells;
- confidence interval expressions;
- `ΔNB`;
- `NLL`;
- `Brier`;
- `AUC`;
- sample sizes;
- event counts;
- prevalence;
- bootstrap replicate counts;
- seeds.

Use deterministic regex + explicit mappings where possible.

Human-readable mappings are preferable to unreliable LLM-generated mappings.

---

# 16. Reference verification architecture

Create a reference registry such as:

```text
knowledge_graph/graph/reference_registry.json
```

Fields:

```text
citation_key
authors
title
year
journal
doi
verification_status
supports_claim_ids
notes
```

If web access is available, verify references using reliable sources such as:

- DOI/Crossref;
- journal pages;
- PubMed;
- official dataset repositories;
- official organizational sources.

Do not rely on random web summaries.

---

# 17. Do not add LLM dependence to deterministic scientific checks

The core audit must run without an LLM API.

The Knowledge Graph and release gates should be deterministic.

If an LLM-assisted review layer is added, it must be optional, e.g.:

```text
agent_graph/optional_llm_review.py
```

and clearly separated from deterministic validation.

The repository must not require Anthropic/OpenAI API keys merely to audit itself.

---

# 18. Add tests

Create tests that use synthetic fixtures and tracked metadata only.

Tests must not require:

- private surveillance files;
- raw PDFs;
- huge ERA5 datasets;
- CHIRPS rasters;
- local `/home/mpcrlab/...` directories.

Tests should cover:

1. schema validity;
2. duplicate IDs;
3. invalid relation types;
4. unsupported claim detection;
5. contradictory analysis-status detection;
6. unresolved placeholder detection;
7. stale README detection;
8. release-gate propagation;
9. proper classification of post-hoc analyses;
10. hard-coded local-path detection.

---

# 19. CI

If CI does not exist, add a minimal GitHub Actions workflow that runs:

```bash
python -m pytest knowledge_graph/tests agent_graph/tests
python -m knowledge_graph.queries.unsupported_claims
python -m knowledge_graph.queries.contradictory_claims
python -m knowledge_graph.queries.unresolved_placeholders
```

The CI must operate only on tracked, legally distributable repository content.

Do not download surveillance or climate data in CI.

---

# 20. Portability repair strategy

Do not rewrite every existing historical script.

Instead:

1. preserve historical scripts;
2. identify machine-specific paths;
3. add a central configuration layer for future executions.

Suggested:

```text
config/
├── paths.example.yaml
└── project_config.py
```

No private machine paths should be committed in a personal config file.

Use:

```text
paths.local.yaml
```

as git-ignored if needed.

---

# 21. Environment repair strategy

Preserve the existing historical environment lock.

Also create a minimal environment for the audit infrastructure:

```text
requirements-audit.txt
```

and, if possible, a minimal scientific-reconstruction file:

```text
analysis/environment/requirements-analysis-minimal.txt
```

Only include packages actually needed by the relevant pipelines.

Do not pretend this recreates the original environment bit-for-bit if it does not.

---

# 22. Scientific interpretation rules

The Agent Graph must enforce the following.

## 22.1 Association is not causation

Do not say:

```text
climate causes X
```

based on the matched predictive feature-block ablation.

Use:

```text
incremental predictive contribution attributed to the climate feature block
```

where appropriate.

---

## 22.2 Statistical ≠ operational importance

A positive ΔNB is not automatically operationally meaningful.

The project lacks a stakeholder-derived minimum worthwhile ΔNB unless such evidence is actually present.

---

## 22.3 Conditional vs development-inclusive uncertainty

Never merge these.

The report must distinguish:

```text
conditional on frozen predictions
```

from:

```text
development-inclusive / refit-both-models
```

---

## 22.4 Colombia is not national external validation

If the analysis uses a selected higher-incidence, better-reporting complete-case subset, do not generalize to all municipalities or all Colombia.

---

## 22.5 Sri Lanka is not deployment validation

A retrospective evaluation using finalized surveillance is not prospective deployment validation.

---

# 23. Protect the chronology

Use git history and audit documents to reconstruct the scientific chronology.

Important distinctions may include:

```text
original analysis
design lock
proper-score design lock
proper-score execution
calibration sensitivity
matched ablation
development-inclusive bootstrap
90th-percentile sensitivity
reviewer-responsive analyses
v43 manuscript repair
```

Create:

```text
knowledge_graph/graph/analysis_chronology.json
```

Every analysis should record, if knowable:

```text
date
commit
tag
status
whether previous results were already known
```

---

# 24. Fix documentation only after evidence is established

After the first audit is generated, correct only documentation inconsistencies that are objectively supported by repository evidence.

Good examples:

- root README project stage;
- stale Methods sentence saying an analysis was not computed when it was later computed;
- incorrect path references;
- wrong analysis-status labels;
- outdated reproducibility wording.

Do **not** rewrite interpretation merely to sound stronger.

Before changing manuscript wording, record the old and new provenance state in the audit.

---

# 25. Do not alter the canonical numerical results unless a bug is demonstrated

If a code bug is discovered:

1. stop;
2. document it;
3. state affected analyses;
4. state affected manuscript claims;
5. create a separate repair analysis;
6. do not overwrite historical frozen evidence;
7. compare old vs corrected results;
8. update the Knowledge Graph with:

```text
SUPERSEDES
```

relationships.

---

# 26. Expected command interface

Aim for:

```bash
python -m knowledge_graph.ingest.ingest_repository
python -m agent_graph.run_audit
```

or one top-level command:

```bash
python -m agent_graph.run_audit --repo .
```

Expected terminal summary:

```text
DATA PROVENANCE              PASS
TEMPORAL LEAKAGE             PASS
SPATIAL CONSISTENCY          REVIEW
MODEL SPECIFICATION          PASS
RESULT TRACEABILITY          REVIEW
REFERENCE INTEGRITY          REVIEW
MANUSCRIPT CONSISTENCY       FAIL
REPOSITORY DOCUMENTATION     FAIL
SUBMISSION DECLARATIONS      FAIL

SUBMISSION READY: NO
```

These are only formatting examples.

Use the actual findings.

---

# 27. Deliverables

At completion provide:

```text
knowledge_graph/
agent_graph/
audit/CURRENT_KG_AGENT_AUDIT.md
audit/CURRENT_KG_AGENT_AUDIT.json
requirements-audit.txt
.github/workflows/research-audit.yml   # if appropriate
```

Also provide:

```text
KG_AGENT_IMPLEMENTATION_REPORT.md
```

with:

1. files created;
2. files modified;
3. tests run;
4. test results;
5. graph statistics;
6. critical contradictions found;
7. reproducibility blockers;
8. manuscript blockers;
9. unresolved author inputs;
10. exact next actions.

---

# 28. Mandatory final peer-review section

End `KG_AGENT_IMPLEMENTATION_REPORT.md` with:

```text
# Harsh External-Reviewer Verdict
```

Assess:

```text
Scientific question
Novelty
Study design
Comparator fairness
Calibration
Decision-curve analysis
Statistical inference
Spatial validity
Generalizability
Reproducibility
Transparency
Manuscript consistency
Submission readiness
```

Score each from:

```text
1–10
```

Explain each score.

Then provide:

```text
Overall recommendation:
ACCEPT
MINOR REVISION
MAJOR REVISION
REJECT / NOT READY FOR SUBMISSION
```

Do not inflate the score.

---

# 29. Important interpretation target

The infrastructure should help determine whether the repository supports a defensible statement approximately like:

> In two retrospective settings, adding climate to a structurally matched recent-surveillance model produced at most modest incremental probability or decision value at short forecast horizons, with the apparent benefit sensitive to calibration, comparator structure, model-development uncertainty, and setting-specific limitations.

Do **not** force this conclusion.

If repository evidence supports a different conclusion, report the evidence.

---

# 30. Final execution order

Follow this order strictly:

```text
PHASE 1
Repository inventory

PHASE 2
Scientific chronology reconstruction

PHASE 3
Knowledge Graph schema

PHASE 4
Repository/manuscript/result ingestion

PHASE 5
Contradiction + provenance queries

PHASE 6
Agent Graph implementation

PHASE 7
Deterministic tests

PHASE 8
CI

PHASE 9
First complete audit

PHASE 10
Evidence-supported documentation repairs

PHASE 11
Re-run complete audit

PHASE 12
Harsh peer-review verdict
```

Do not skip directly to rewriting the manuscript.

---

# Final instruction

The objective is **not** to make this repository look sophisticated.

The objective is to make it **difficult for an incorrect, unsupported, stale, contradictory, or unreproducible scientific claim to survive into submission**.

Prefer:

```text
clear provenance
small deterministic tools
explicit failures
transparent null results
traceable analysis chronology
```

over:

```text
agent complexity
LLM theatrics
large frameworks
unverifiable automation
```

When uncertain, preserve the existing evidence, flag the uncertainty, and ask for author input rather than inventing an answer.
