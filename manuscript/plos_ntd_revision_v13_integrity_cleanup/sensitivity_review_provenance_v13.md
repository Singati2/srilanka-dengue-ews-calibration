# Sensitivity-review provenance (internal documentation — v13)

This note records, for internal documentation only, how the two author-authorized secondary sensitivity analyses (Colombia 2022-only; Sri Lanka wild-cluster-bootstrap-t) were reviewed before integration. It is **not** part of the manuscript, Supporting Information, cover letter, or declarations.

## Provenance statement (authoritative wording)

> An internal AI-assisted role-based review was used to identify methodological questions and cross-check the proposed implementation. It was not external human peer review and does not constitute independent validation.

## What must NOT be claimed
- Do not state that field experts or independent reviewers validated these analyses.
- Do not describe the review as external human peer review or as independent validation.
- Do not mention the number of AI agents (in the manuscript, Supporting Information, cover letter, or declarations).

## Where this applies
- Manuscript body, S9(c), S11, S12: describe the analyses as secondary, pointwise, multiplicity-unadjusted robustness checks. No claim of expert or independent-reviewer validation appears in any of these.
- The wild-cluster-bootstrap results are explicitly single-implementation (S12); the statistics and cluster-robust SEs were independently reproduced with statsmodels, but a second full wild-bootstrap implementation was not available. This is a partial computational cross-check, not independent validation of the whole procedure.

## Verification performed for v13
- Grep of all v13 manuscript and SI files confirms no occurrence of "expert-validated", "independently validated", "peer-reviewed", "external review", or any AI-agent count.
