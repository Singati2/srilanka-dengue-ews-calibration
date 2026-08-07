"""Knowledge-graph schema: entity types, relation types, analysis-status ontology.

Deterministic vocabularies only. Matches prompt sections 4, 5, 7.
"""

ENTITY_TYPES = [
    "Project", "Country", "StudySetting", "Dataset", "DatasetVersion", "DataSource",
    "SpatialUnit", "TemporalUnit", "Outcome", "OutcomeDefinition", "AlertThreshold",
    "ForecastHorizon", "Feature", "FeatureBlock", "ClimateVariable", "Model",
    "ModelFamily", "Comparator", "CalibrationMethod", "Analysis", "SensitivityAnalysis",
    "PrimaryAnalysis", "SecondaryAnalysis", "PostHocAnalysis", "BootstrapProcedure",
    "StatisticalEstimand", "Metric", "Result", "ConfidenceInterval", "Figure", "Table",
    "Manuscript", "ManuscriptSection", "ManuscriptClaim", "Reference", "DOI", "Script",
    "Function", "FrozenArtifact", "Checksum", "Environment", "Seed", "GitCommit",
    "GitTag", "AuditFinding", "ReleaseGate", "AuthorInput", "NumericClaim",
]

RELATION_TYPES = [
    "USES", "DERIVED_FROM", "GENERATED_BY", "EXECUTED_WITH", "EVALUATED_ON",
    "SPLIT_INTO", "CALIBRATED_BY", "COMPARES", "ABLATES", "PRODUCES", "SUPPORTS",
    "CONTRADICTS", "APPEARS_IN", "CITED_BY", "CITES", "HAS_CHECKSUM", "FROZEN_AT",
    "INTRODUCED_IN", "MODIFIED_IN", "REPORTED_IN", "DEPENDS_ON", "VALIDATES",
    "REPRODUCES", "FAILS_TO_REPRODUCE", "CLASSIFIED_AS", "SUPERSEDES",
    "REQUIRES_AUTHOR_INPUT",
]

# Analysis-status ontology (prompt s7). Every Analysis must receive exactly one.
ANALYSIS_STATUSES = [
    "prespecified_primary",
    "prespecified_secondary",
    "internally_design_locked",      # design-locked but not registered
    "post_hoc_exploratory",
    "post_result_design_locked",     # locked after primary results known
    "sensitivity",
    "diagnostic",
]

# Statuses that MUST NOT be described with stronger words in the manuscript.
STATUS_FORBIDDEN_UPGRADES = {
    "post_hoc_exploratory": ["prespecified", "primary", "confirmatory", "registered", "validated", "prospective"],
    "post_result_design_locked": ["prespecified", "primary", "confirmatory", "registered", "prospective"],
    "sensitivity": ["primary", "confirmatory"],
}

# Overclaim vocabulary the Adversarial Reviewer scans for (context-checked in agents).
OVERCLAIM_TERMS = [
    "deployment ready", "deployment-ready", "operationally useful", "clinically useful",
    "externally validated", "national generalizab", "nationally generaliz",
    "causal climate", "proves", "cases prevented", "outbreaks prevented",
    "significantly better",  # net-benefit significance testing is contested (Vickers 2023)
]

# Author-supplied fields that block submission if left as placeholders (prompt s2.6).
REQUIRED_AUTHOR_FIELDS = [
    "ethics", "funding", "competing interest", "author contribution", "orcid",
    "corresponding author", "data availability", "archival doi", "license",
]

# Substrings (bracket/colon-agnostic) — the real manuscript uses
# "[AUTHOR INPUT REQUIRED: <field>]", so match the stable core, not the exact brackets.
PLACEHOLDER_MARKERS = ["AUTHOR INPUT REQUIRED", "[DOI to verify]", "XXXX", "\\todo{"]
