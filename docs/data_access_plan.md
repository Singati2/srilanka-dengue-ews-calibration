# Sri Lanka Dengue Pilot — Data-Access & Data-Management Plan

**Status:** Final pre-data artifact. Governs *how* outcome data will be obtained, preserved, cleaned, and reconciled — **before** any download, linkage, or modeling.
**Pairs with:** `osf_prereg_srilanka_pilot.md`, `geomatics_scope_of_work.md`, `probast_tripod_scoring_instrument.md`.
**Hard rule:** No data is downloaded, no model is run, and the preregistration is not modified while this plan is being written or reviewed. This document is a plan, not an execution.

---

## A. Purpose
1. Define exactly **what outcome data** the pilot requires, from **which sources**, at **what spatial/temporal resolution**, and to **what minimum quality bar** — fixed in advance so the bar is not quietly lowered to fit whatever is available.
2. Make the **MOH-division vs district** decision an **explicit, pre-committed rule** (Section O), decided on data availability, not convenience.
3. Specify raw-data preservation, cleaning, missing-data, and boundary-reconciliation rules so the outcome dataset is auditable and leakage-safe.
4. Define the **stop conditions** under which the pilot is not viable (Section P) — so "insufficient data" is a pre-agreed outcome, not an improvised compromise.

## B. Primary outcome data needed
- **Weekly dengue case counts** per spatial unit, as a continuous time series over the study window.
- Minimum fields per record: spatial-unit identifier, epidemiological week (and the source's week-numbering convention), case count.
- Desired additional fields where available: suspected vs confirmed/laboratory status; reporting completeness flags; population denominator if published.
- The outcome is **count data**; no individual-level records are sought or needed (see N).

## C. Preferred spatial unit
**MOH-division × epidemiological week** dengue counts. Preferred because finer areal units make change-of-support, the spatial adjacency graph, and the spatial decision-flip analysis statistically meaningful (per `geomatics_scope_of_work.md`).

## D. Fallback spatial unit
**District × epidemiological week** dengue counts (25 districts). Used **only if** the MOH-level series fails the minimum requirements in Section E, per the decision rule in Section O.

## E. Minimum acceptable data requirements (do NOT soften)
A spatial unit is **eligible** only if it meets **all** of:
1. **Temporal length:** ≥ **8 years** of continuous weekly reporting within the study window.
2. **Completeness:** < **10%** missing weeks over its series (missing = absent or non-numeric).
3. **Resolution match:** counts reported at the candidate spatial unit (MOH-division for preferred; district for fallback) without aggregation ambiguity.
4. **Temporal alignment:** weeks mappable to a single, documented epidemiological-week convention (ISO or CDC/MMWR), consistently across the series.
5. **Denominator availability:** a population denominator obtainable for the unit and period (from census/WorldPop) for incidence and offset.

**Dataset-level minimum (preferred MOH path):** the MOH-level data is usable **only if ≥ 80% of MOH-divisions** individually meet criteria 1–5. Otherwise the preferred path fails and the fallback rule (O) is triggered.

**Dataset-level minimum (fallback district path):** ≥ **20 of 25 districts** meet criteria 1–5.

These thresholds are **fixed here and frozen at OSF registration**. They are not adjusted after seeing the data.

## F. Data sources to check (in priority order)
1. **Sri Lanka Epidemiology Unit** (epid.gov.lk) — the authoritative national source; weekly dengue surveillance, district and (where published) sub-district returns; historical archives.
2. **Ministry of Health weekly epidemiological reports** (WER / "Weekly Epidemiological Report") — weekly bulletins; cross-check against Epidemiology Unit figures.
3. **Open weekly dengue bulletins / dashboards** — National Dengue Control Unit (NDCU) releases; any official dashboard exports.
4. **Official downloadable surveillance archive** — any structured archive (CSV/Excel/PDF tables) from the above; note format, granularity, and time coverage.
For each source, record: URL, granularity (district vs MOH), time coverage, file format, week convention, access method (download vs request), and any terms of use.

## G. Information to extract from each source
For every candidate source, populate an **inventory row** capturing:
- **Spatial unit** present (district / MOH-division / other) and its identifier scheme.
- **Week/date** field and its convention (ISO vs MMWR vs calendar; year-boundary handling).
- **Dengue count** field(s) and units.
- **Suspected vs confirmed/laboratory** status, if distinguished.
- **Missing weeks** — explicit gaps vs implicit (absent rows).
- **Boundary definitions / vintage** referenced (which administrative boundary version the counts correspond to).
- Source-specific caveats (revisions, provisional vs final figures, reporting-delay notes).

## H. Data dictionary template
One row per field in the assembled outcome dataset:

| Field name | Description | Type | Units / format | Allowed values | Source field | Week convention | Notes |
|---|---|---|---|---|---|---|---|
| `unit_id` | Stable spatial-unit ID | string | frozen ID scheme | — | — | — | crosswalk to boundary vintage |
| `unit_name` | MOH-division / district name | string | — | — | — | — | |
| `epi_year` | Epidemiological year | int | YYYY | — | — | ISO/MMWR (record which) | |
| `epi_week` | Epidemiological week | int | 1–53 | 1–53 | — | ISO/MMWR | |
| `week_start` | Week start date | date | YYYY-MM-DD | — | — | — | derived, documented |
| `cases_total` | Reported dengue cases | int | count | ≥ 0 | — | — | suspected+confirmed unless split |
| `cases_confirmed` | Lab-confirmed cases | int | count | ≥ 0 / NA | — | — | NA if not distinguished |
| `case_status` | Suspected / confirmed / mixed | string | — | {suspected, confirmed, mixed} | — | — | |
| `missing_flag` | Week missing/imputed | bool | — | {0,1} | — | — | see L |
| `population` | Unit denominator | int | persons | > 0 | census/WorldPop | — | vintage-matched |
| `boundary_vintage` | Admin boundary version | string | — | frozen version | — | — | |
| `source` | Provenance | string | — | — | — | — | source + retrieval date |

## I. File naming & versioning conventions
- **Raw (immutable):** `raw/{source}_{granularity}_{coverage}_{retrievaldate}.{ext}` — e.g. `raw/epidunit_district_2007-2024_2026-06-15.csv`. Never edited.
- **Interim:** `interim/{step}_{description}_v{n}.csv` — each cleaning step a new version.
- **Processed (analysis-ready outcome):** `processed/outcome_{unit}_{window}_v{n}.csv` — e.g. `processed/outcome_mohdiv_2009-2023_v1.csv`.
- **Crosswalks/boundaries:** `geo/boundary_{vintage}.gpkg`, `geo/crosswalk_{from}_{to}.csv`.
- Every processed file carries the **git commit hash** and a checksum in a sidecar `.meta` file.
- Semantic versions only increment on documented changes; the **frozen** analysis dataset is tagged (e.g. `outcome_v1.0-frozen`).

## J. Raw-data preservation rules
1. Raw downloads are stored **read-only** in `raw/`, with retrieval date, URL, and checksum recorded.
2. Raw files are **never modified in place** — all transformations occur downstream and are scripted.
3. PDFs/tables that require manual transcription are preserved as the original PDF **plus** a transcription file with a transcription-audit log (who, when, double-entry result).
4. Provenance for every raw artifact recorded in a `data_provenance` table (feeds QC item R2 / Table T1).
5. Raw data is backed up before any processing begins.

## K. Cleaning rules
- All cleaning is **scripted and re-runnable** raw → processed; no manual spreadsheet edits.
- Standardize unit names → stable `unit_id` via the frozen crosswalk (M).
- Harmonize all weeks to **one** declared epidemiological-week convention; document year-boundary handling (week 52/53).
- Resolve suspected/confirmed: default `cases_total` = suspected+confirmed (or "reported"), keep `cases_confirmed` separate where available; **the primary outcome field is declared once and fixed**.
- De-duplicate overlapping source records (Epidemiology Unit vs WER) with a **pre-declared source-precedence rule** (Epidemiology Unit primary; WER for cross-check/gap-fill only).
- Flag, do not silently drop, anomalies (negative counts, impossible weeks, revisions); record in a cleaning log.

## L. Missing-data rules
- Distinguish **explicit** (reported as missing) vs **implicit** (absent row) missingness; both set `missing_flag = 1`.
- **Primary analysis:** units exceeding the 10% missing-week threshold (E) are **excluded**, not imputed into eligibility.
- For eligible units with sparse gaps (< 10%), the gap-fill method is **pre-declared** (e.g., flagged seasonal-structure imputation) and gap-filled weeks remain flagged for sensitivity analysis.
- **No imputation of the outcome is used to manufacture eligibility.** Imputation never converts an ineligible unit into an eligible one.
- Missingness is reported (counts, pattern) for TRIPOD item R6.

## M. Boundary & spatial-unit reconciliation rules
- **Freeze one administrative boundary vintage** for the entire study; record its version ID.
- Build an explicit **crosswalk** between the boundary vintage used by the surveillance counts and the analysis boundary (handle splits/merges/renames of MOH-divisions or districts over time).
- Units whose boundaries changed within the study window and **cannot** be unambiguously crosswalked are **excluded** (or analyzed only over their stable sub-period) — decided by rule, not case-by-case convenience.
- The geospatial lead validates topology, ensures stable IDs, and reconciles MOH-division ↔ district hierarchy (`geomatics_scope_of_work.md` WP1).
- Coastal/island boundaries handled so no spurious adjacency arises downstream.

## N. Privacy / ethics considerations
- Only **aggregate count data** at MOH-division/district level are sought — **no individual-level or identifiable records**. Re-identification risk is negligible at these aggregations.
- Use only **publicly released** surveillance aggregates and/or data obtained under the source's stated terms; record terms of use per source.
- If any source requires formal request or data-use agreement, obtain it **before** download; do not scrape data whose terms forbid it.
- Confirm whether institutional ethics review is required for secondary use of public aggregate surveillance data; if a determination of exemption is needed, secure it before analysis. Record the determination.
- Attribute the Epidemiology Unit / Ministry of Health as data source per their citation requirements.

## O. Decision rule: MOH-level vs district-level (explicit, binding)
Evaluated **once**, on data-availability evidence, **before** outcome–exposure linkage, and recorded with a timestamp:

```
IF  MOH-division weekly dengue counts are obtainable
    AND ≥ 80% of MOH-divisions meet ALL minimum requirements (E.1–E.5)
    AND boundaries are crosswalkable to a single frozen vintage (M)
THEN  analysis unit = MOH-division (preferred, Section C)

ELSE IF  district weekly dengue counts are obtainable
         AND ≥ 20 of 25 districts meet ALL minimum requirements (E.1–E.5)
THEN  analysis unit = district (fallback, Section D)

ELSE  pilot is not viable at the required standard → trigger STOP (Section P)
```

The decision and its supporting counts (how many units passed each criterion) are logged and become part of the OSF freeze. The unit is **not** re-decided after seeing results.

## P. Stop conditions (pilot not viable)
Declare the pilot **non-viable** (and do not proceed to engineering pilot / registration) if **any** hold:
1. Neither the MOH-level (≥80% units) nor the district-level (≥20/25) dataset-minimum is met.
2. No usable population denominator can be obtained for the eligible units/period.
3. Weeks cannot be reconciled to a single epidemiological-week convention.
4. Boundaries cannot be crosswalked to a stable vintage for a sufficient set of units.
5. Data are obtainable only under terms that forbid the planned research use.

On STOP: document the specific failure, do **not** lower the Section E thresholds to rescue viability, and report the pilot as infeasible at the required standard. (Optional downgrade, not a workaround: a clearly-labeled **exploratory** descriptive study could be considered separately, but it does **not** satisfy this preregistered pilot.)

## Q. Task ownership
| Task | Owner |
|---|---|
| Source inventory (F) + provenance table | PI / data lead |
| Outcome extraction, week harmonization, cleaning scripts (G, K, L) | PI / data lead |
| Suspected/confirmed handling, source-precedence, dedup (K) | PI / data lead |
| **Boundary freeze, crosswalk, unit-ID reconciliation (M)** | **Geomatics engineer** |
| **MOH↔district hierarchy validation, topology, stable IDs** | **Geomatics engineer** |
| **Population denominator assembly (census/WorldPop, vintage-matched)** | **Geomatics engineer** (with data lead) |
| Eligibility evaluation against Section E | PI + Geomatics jointly |
| Decision rule O computation + logging | PI (recorded, witnessed) |
| Privacy/terms/ethics determination (N) | PI |
| Data dictionary (H) completion | Data lead + Geomatics |

## R. Checklist before linking outcome data to climate/exposure data
All must be ✔ before **any** linkage:
- ☐ Outcome dataset assembled, cleaned, and frozen (`outcome_*_v1.0-frozen`).
- ☐ Section E minimums verified; eligible-unit list fixed.
- ☐ Decision rule O executed and logged; analysis unit fixed.
- ☐ Boundary vintage frozen; crosswalk complete; stable IDs assigned.
- ☐ Epidemiological-week convention declared and applied uniformly.
- ☐ Population denominators attached and vintage-matched.
- ☐ Missing-data flags set; ineligible units excluded (not imputed in).
- ☐ Primary outcome field (`cases_total`) and outbreak-relevant counts declared.
- ☐ Privacy/terms/ethics determination recorded.
- ☐ Provenance table + data dictionary complete.
- ☐ Quarantined engineering-pilot subset designated and **set aside** (per prereg §Z.2) so it does not contaminate confirmatory analysis.

Linkage to exposure (`geomatics_scope_of_work.md` WP2) proceeds **only** after every box is ✔.

## S. What must be frozen before OSF registration
- The **assembled, cleaned outcome dataset** (tagged frozen) and its checksum.
- The **analysis spatial unit** (output of decision rule O) and the eligible-unit list.
- **Study window** (start/end dates) and the epidemiological-week convention.
- **Section E thresholds** (length, completeness, dataset-minimum percentages) — already fixed here.
- **Boundary vintage** and crosswalk.
- **Source-precedence and missing-data/gap-fill rules.**
- **Primary outcome field** definition.
- The **quarantined subset** designation.

## T. What must NOT be changed after OSF registration
- The minimum data requirements (Section E) — no post-hoc loosening to admit more units or rescue viability.
- The analysis spatial unit and eligible-unit list (no swapping MOH↔district after results).
- The study window, week convention, and outbreak-relevant outcome definitions.
- The boundary vintage and crosswalk.
- Source-precedence, cleaning, and missing-data rules.
- The quarantined-subset boundary (debug data never enters confirmatory analysis).
Any change to the above after registration renders the analysis **exploratory** (per prereg §Z.5 and the PROBAST exploratory trigger), and must be disclosed as such.
