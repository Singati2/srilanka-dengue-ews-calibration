# 26-RDHS Adjacency Graph (BYM2) Build Report (Geomatics WP1)
*Documents an adjacency-graph build performed **locally**. The edge CSV / neighbors JSON and all geometry stay in git-ignored quarantine and are **NOT committed**. No climate data, no outcome↔exposure linkage, no models, preregistration untouched, frozen outcome dataset unchanged. No new packages installed.*

**Date:** 2026-06-11
**Purpose:** build the spatial neighbour structure for the BYM2 spatial random effect over the 26 RDHS units.

## Method
- Geometry: `rdhs_26_v1.gpkg` (layer `rdhs_26`, EPSG:4326).
- **Queen contiguity** via pure **geopandas + shapely** (libpysal not installed/needed); connectivity verified with networkx. Each candidate pair classified by polygon intersection: **rook** (shared edge) vs **queen_point** (point-only); shared-boundary length in EPSG:32644 (metres). Keyed on `geometry_id` (+ `rdhs_name`).

## QC results
| Check | Result |
|---|---|
| Nodes | **26** ✅ |
| Edges (undirected) | **60** |
| Self-neighbors / duplicate edges | 0 / 0 ✅ |
| Isolated nodes | **NONE** ✅ |
| Connected components | **1** ✅ |
| Topology overlaps | none ✅ |
| Edge type | all **rook** (no point-only links) |
| Degree min / median / max | **2 / 4 / 9** |
| geometry_ids match crosswalk | ✅ (26/26) |
| Cross-sea links | **none** |

## Suspicious-link review (reported, not silently fixed)
Two Ampara links looked geographically surprising and were checked against their shared-boundary length:
- **Ampara–Matale: ~11.9 km** (Wasgamuwa/Mahaweli area) → **genuine**.
- **Ampara–Hambantota: ~15.5 km** (Yala/Kumana area) → **genuine**.
- Shortest edge overall: **Jaffna–Mullaitivu 984 m** (real land border at the peninsula base). **0 edges < 100 m** → no spurious tripoint/point artifacts.
Conclusion: the base queen graph contains no spurious links; **no edges removed**.

## Ampara & Kalmunai neighbours
- **Kalmunai (LK52K):** Batticaloa, Ampara — **degree 2** (graph minimum), geographically justified (coastal strip, east = sea).
- **Ampara (LK52A):** Batticaloa, Polonnaruwa, Badulla, Moneragala, Kalmunai, Matale, Hambantota — degree 7, all genuine shared land borders.

## Coastal / island review
All edges are real shared land borders (≥ 984 m); none cross sea. Kalmunai (coastal) and Jaffna (peninsula, neighbours Killinochchi + Mullaitivu by land) connect only via land. No isolated units; the graph is a single connected component — appropriate for a BYM2 structure (the BYM2 ICAR component requires a connected adjacency).

## Sensitivity (not applied; report-only)
No edge removal needed. Optional robustness checks (deferred): drop the single sub-1 km border (Jaffna–Mullaitivu) or alter point-touch handling — both expected to leave the graph connected.

## Output (quarantined, NOT committed)
- `~/data_quarantine/geomatics/adjacency/rdhs_26_adjacency_edges.csv` (60 edges)
- `~/data_quarantine/geomatics/adjacency/rdhs_26_adjacency_neighbors.json` (keyed by geometry_id)
- `…/rdhs_26_adjacency.meta.md`

## Status & next step
- Adjacency graph built and QC-clean (quarantined). With this, **WP1 (spatial backbone: geometry + denominators + adjacency) is complete.**
- The project is now at the gate **before** any climate download, exposure construction, outcome↔exposure linkage, modeling, or preregistration finalization — all of which remain pending explicit approval.
