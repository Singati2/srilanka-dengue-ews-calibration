# v20 reviews (Panel-2 + STORM) — resolution (v20 -> v20b)

Both v20 reviews independently confirmed **clean arithmetic / no fabricated numbers / defensible core** and both returned **MAJOR REVISION**. Both named the SAME single blocking scientific fix.

## THE blocking scientific fix — RESOLVED (computed, not just disclosed)
Both reviews: compute a **department-resampled CONDITIONAL** interval for the Colombia matched increment (frozen predictions) so the comparison to the department-resampled REFIT interval isolates refitting from the cluster-level change.

Computed (gate reproduced dNB_climate = +0.00783 = frozen; script `colombia_dept_conditional/`):
| Interval | Result |
|---|---|
| Municipality conditional (475 units) | [+0.0039, +0.0119] (reproduces reported) |
| **Department conditional (31 depts)** | **[+0.0038, +0.0115]** |
| Department refit (development-inclusive) | [-0.0001, +0.0244] |

**Finding:** the department-conditional is essentially identical to the municipality-conditional, so the cluster-level change contributes negligibly; the widening to the development-inclusive interval (same department unit) is attributable to **model refitting**, not clustering. This is the exact like-for-like comparison both reviews requested — and it **vindicates** the model-development attribution the reviewers suspected was confounded. The manuscript now reports the department-conditional interval and states this resolution (replacing the earlier hedge).

## Other verified fixes applied (v20b, + v20)
- Reporting-delay finding promoted to the abstract (Panel-2 C1's "most policy-relevant" result): three-week-lag matched increment +0.0049, the regime an EWS operates in.
- Conclusion "operational" language softened ("Evaluations should...", "decision-relevant threshold range").
- (v20) per-100 error corrected (matched 0.8 not 1.9); "same meaning"->"structurally analogous"; "same sign" softened; "structure>climate" -> point-estimate; duplicated intro deleted; "net benefit is our arbiter" removed; Methods dAUC example trimmed; Discussion 19%/10% mirrored; abstract compressed 477->454.

Build: 38 pp, exit 0, 0 undefined, 0 errors, 0 figure-box leakage, 0 broken refs. 0 distinct numbers lost.

## Independent audits (both reviews + my figure/table/ref auditor): CLEAN
No fabricated or contradictory numbers; all tables/figures/references reconcile; external anchors (PAHO 4.2M, EWARS-csd, Beal 2025) confirmed.

## NOT applied (PI-level reframe / new analysis / author-action — flagged, not faked)
- Methodological-framing pivot (F1); reframe around the "doomed prespecified primary" (A1) - PI-level.
- Differential-shrinkage sensitivity (A2, fixed-penalty/single-fit nested) and power/MDE analysis (A3) - new analyses.
- Figure rebuilds (matched Fig 2; past-only-primary Fig 3; combined forest incl. department-conditional in Fig 5; geography/completeness figure); table redesigns; compression to 25-28 pp.
- Author-owned blockers: ethics determination, data/code DOI + checksums, pinned Python env, S1-S18 files, CRediT/ORCID/declarations, PROBAST->PROBAST+AI, local-engagement statement.
