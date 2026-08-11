# V44_VS_BIOMATH_DECISION_MEMO

Direct comparison to help choose a canonical direction. Empirical science is **identical** across all three columns (same numbers, models, hierarchy); they differ only in framing/formalization.

| Dimension | Plain v44 | Current biomath (V1) | Tightened biomath (this pass) |
|---|---|---|---|
| Scientific clarity | High | High | High |
| Estimand clarity | Medium — matched ablation described in prose | High — $\Delta V_C$ named but unoriented | **Highest** — $\Delta V_{C,k}$, metric-oriented, one glance |
| Mathematical rigor | Low (by design) | Medium, some ornament | Medium, **ornament removed**; nesting evidenced |
| Epidemiology readability | Highest | Medium (equation-dense Methods) | High (leaner Methods) |
| Desk-rejection risk | Low at epi venues | Medium (math may read as decoration) | Low–medium |
| Methods transparency | Medium | High | **Highest** (matched-comparator doc) |
| Novelty communication | Prose "first DCA" (hedged) | Same + integration framing | Same, framed as joint architecture |
| Equation-decoration risk | None | **Real** | **Mitigated** |
| Journal fit | PLOS GPH / NTD | Methodology/decision + geo-epi | PLOS GPH / GeoHealth / BMC Med Res Methodol / Diag Progn Res |

## Recommendation
**`ADOPT_HYBRID_LIGHT_FORMALIZATION`** — the tightened biomath candidate.

Rationale: it delivers the one thing plain v44 lacks (a crisp, metric-oriented statement of the central estimand and the ranking/probability/decision distinction) without the decoration risk that made V1 a liability. The cost is ~one page of framework; the benefit is that a methodology or geo-epi reviewer can identify $\Delta V_{C,k}=V_k(\mathcal I^{SC})-V_k(\mathcal I^{S})$ and the matched-comparator logic immediately.

Caveats:
- If the target is a **pure clinical/epi venue that dislikes formalism**, plain v44 is safer — keep the tightened framework as a short "decision-analytic framework" Methods subsection that can be cut to a paragraph.
- Do **not** market as mechanistic mathematical biology anywhere.
- The novelty sentence stays hedged and `NEEDS_EXTERNAL_VERIFICATION` regardless of column.

## Practical next step
Author picks the venue; the tightened candidate is venue-flexible (drop the framework subsection to a paragraph for a strict epi venue; keep it for a methodology/decision or applied-math-epi venue). No further analysis is required to submit either way; the open blockers are author-owned (ethics, ORCIDs, funding, COI, Zenodo DOI/license, OpenDengue v1.3 record id).
