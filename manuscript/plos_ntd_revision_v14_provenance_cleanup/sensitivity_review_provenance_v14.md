# AI-review provenance (internal documentation — v14)

This note records, for internal documentation only, how (a) the two author-authorized secondary sensitivity analyses and (b) the v13 integrity edits were reviewed. It is **not** part of the manuscript, Supporting Information, cover letter, or declarations.

## Provenance statement (authoritative wording)

For the v13 edits:

> An internal AI-assisted role-based adversarial review was used to identify inconsistencies and cross-check the v13 edits. It was not external human peer review or independent expert validation.

For the sensitivity analyses:

> An internal AI-assisted role-based review was used to identify methodological questions and cross-check the proposed implementation. It was not external human peer review and does not constitute independent validation.

## What must NOT be claimed
- Do not describe the review as a field-expert panel, a harsh peer-review panel, expert validation, or independent peer review.
- Do not state that field experts or independent reviewers validated any analysis or edit.
- Do not add AI-panel claims or the number of AI agents to the manuscript, Supporting Information, cover letter, or declarations.

## Scope
- These reviews were internal AI-assisted role-based adversarial cross-checks only. Any earlier internal wording that referred to a "field-expert panel" or a "harsh peer-review panel" is superseded by the authoritative wording above.
- The wild-cluster-bootstrap results are explicitly single-implementation (S12); the studentized statistics and cluster-robust SEs were independently reproduced with statsmodels, but a second full wild-bootstrap implementation was not available — a partial computational cross-check, not independent validation of the whole procedure.

## Verification performed for v14
- The manuscript and Supporting Information contain no "expert-validated", "independently validated", "peer-reviewed", "external review", "field-expert", "harsh peer", or AI-agent-count statements (grep-confirmed across the v14 tex and SI).
- This AI-review provenance correction applies to internal audit reports only.
