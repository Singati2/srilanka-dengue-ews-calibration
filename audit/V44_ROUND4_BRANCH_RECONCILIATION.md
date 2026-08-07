# v44 Round 4 — branch reconciliation record (§3)

**Starting branch/SHA:** `agent/v44-pi-decisions-methods-fix` @ `8573512` → new branch
`agent/v44-round4-geomatics-execution`.

## Compared branches (git diff base = agent/v44-round2-impl)
| Branch | Carries | Disposition |
|---|---|---|
| `agent/v44-round2-impl` | LaTeX-tolerant contradiction detector, explicit manuscript targeting, KG+agents | **base** (inherited) |
| `agent/v44-pi-decisions-methods-fix` | + `docs/PI_DECISIONS_v44_ratified.md`, `manuscript_v44/` draft | **retained** (built on) |
| `agent/v44-round3-submission-gates-geomatics-prompt` | the round-3 *prompt* (instructions only, never executed) | **NOT merged**; its still-missing gate requirements are implemented directly here |

## Imported files / changes this round
- Implemented the previously-unexecuted round-3/round-4 gate work (submission-readiness semantics
  §5; shallow-PASS downgrades §6) directly in `agent_graph/` + `knowledge_graph/schema.py`.
- Corrected the WorldPop decision (§4.1): fractional-coverage sensitivity is MANDATORY; the coastal
  shortfall may not be called negligible until quantified.
- Preserved the PI-decisions files and the v44 Methods correction; v43 remains untouched.

## Conflicts
None — the round-3 prompt branch was intentionally not merged (avoids importing 1250 lines of
instructions as if they were code). All changes are additive to the round-2/PI-decisions base.

## Blocked (documented, not faked)
Geomatics execution (§7-23): M6/WP4/WP5 + real v44 manuscript require the quarantined geomatics
features (co-author mid-build under the two ratified decisions). Not run this round.
