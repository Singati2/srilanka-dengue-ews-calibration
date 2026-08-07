# v44 §3 audit repair (KG + Agent hardening)

Implements §2–§3 of `prompts/CLAUDE_V44_GEOMATICS_INTEGRATION_REFRAME_AND_AUDIT.md`.
§5–§9 (M6 integration + manuscript reframe) are **deferred/BLOCKED** — the geomatics
features are a quarantined pilot still being built (notebooks 00–03 done; 05–08 blocked on
PI decisions), so completing M6 now would violate §1.3 ("no invented completion").

## What was repaired (all with regression tests, §3.3)
1. **Semantic contradiction detector (§3.1).** Replaced the brittle single-literal match with
   `detect_proper_score_contradiction()`: flags when a doc BOTH reports development-inclusive
   proper-score intervals AND claims they were "not computed / gated / not re-executed /
   not available". Catches the v43 contradiction; the repaired v43/v44 text passes.
2. **Honest gate statuses (§3.2).** Added `NOT_VERIFIED` / `PARTIAL`. Presence-only checks no
   longer earn a strong PASS:
   - REPRODUCIBILITY → NOT_VERIFIED (lockfile/checksum present but not re-executed; quarantined
     inputs cannot be recomputed in-audit).
   - REFERENCE INTEGRITY → NOT_VERIFIED (citation-key integrity checked; DOI/metadata + claim
     support require a network verifier).
   - TEMPORAL LEAKAGE → NOT_VERIFIED (static scan only; composite-availability dates,
     threshold/scaling/recal windows, lag & outcome timing not verifiable statically) +
     `composite_leaks_if_joined_by_start()` rule for MODIS start-vs-end joins.
3. **Six regression tests (§3.3)** — contradiction, unsupported-citation NOT_VERIFIED,
   presence-only reproducibility not-strong-PASS, MODIS composite-end leakage, token-based
   traceability not-strong-PASS, and one genuinely-demonstrated PASS. **13/13 pass.**

## Current audit
`SUBMISSION READY: NO` — blocker: 8 author declarations + DOI. TEMPORAL LEAKAGE / REPRODUCIBILITY
/ REFERENCE INTEGRITY are now honestly NOT_VERIFIED (need out-of-audit checks), not false PASS.
