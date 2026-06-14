# OpenDengue Catalog-Inspection Report (feasibility, no external run)
*Catalog/metadata inspection only to decide whether one clean OpenDengue external-replication arm is feasible. **No models fit; no AUC/calibration/DCA/net-benefit; no outbreak labels; no ERA5/CHIRPS linkage; no external-validation tables.** Only two small metadata JSONs (~8 KB total) were downloaded to quarantine; the full case datasets (≈54 MB extracts) were **NOT** downloaded. No data files committed.*

**Date:** 2026-06-14

## 1. What was inspected (sources)
- OpenDengue GitHub `OpenDengue/master-repo` (default branch `main`), via GitHub contents API (folder listing + sizes only).
- Downloaded to quarantine (`~/data_quarantine/opendengue_catalog_inspection_v1/`, read-only): `metadata_main.json` (4,535 B), `metadata_source.json` (3,153 B).
- Authoritative descriptor: Clarke et al., *Scientific Data* 2024 (DOI 10.1038/s41597-024-03120-7) — verified earlier this session.

## 2. Confirmed catalog facts
- **Codebook (metadata_main.json):** `adm_0_name` (country), `adm_1_name` (Admin1), `adm_2_name` (Admin2), `full_name`, `ISO_A0`, temporal-resolution fields, dengue case counts.
- **Three global summary extracts** (V1.3 release): `National_extract` (best national; 316 KB zip), `Temporal_extract` (**best temporal resolution** — where weekly lives; **54.9 MB** zip), `Spatial_extract` (**best spatial resolution** — where Admin2 lives; **54.7 MB** zip).
- **Coverage (paper):** 56M+ cases, 102 countries, 1924–2023; **>95% weekly or monthly**; **subnational for 40 countries**.
- **Weekly Admin2 countries (paper, explicit):** **Brazil, Colombia**, Philippines, China, Taiwan report weekly case counts at the **second administrative level**.
- **Implication:** the weekly-subnational data we need are inside the **Temporal/Spatial extracts (≈54 MB)** = a **full-dataset download** → per the gating rule, that step is deferred (stop-and-ask).

## 3. Keep/drop table (catalog inspection)
*"Confirmed" = stated in the verified paper/metadata. "Verify in extract" = needs the Temporal/Spatial extract (a gated full download) to confirm exact units/years.*

| Candidate | Temporal res. | Spatial res. | Years | # units | ~Obs | Units stable? | ≥ train/test yrs? | 75th-pct label feasible? | h=4 weekly feasible? | Climate linkage? | Keep/Drop | Reason |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Brazil** | **weekly (confirmed)** | **Admin2 (confirmed)** | through 2023 (span verify) | many municipalities/27 states | very large | likely (verify) | yes (verify) | yes (large counts) | **yes** | yes (GADM Admin2 + ERA5/CHIRPS) | **KEEP — primary** | Weekly Admin2 confirmed; largest contributor; many clusters → strong cluster bootstrap |
| **Colombia** | **weekly (confirmed)** | **Admin2 (confirmed)** | through 2023 (span verify) | dozens of municipalities | large | likely (verify) | yes (verify) | yes | **yes** | yes | **KEEP — primary/backup** | Weekly Admin2 confirmed; EWARS-csd municipal precedent (Schlesinger 2024) |
| Vietnam | weekly/monthly — **verify in extract** | Admin1 likely (province) | through 2023 | ~63 provinces | large | likely | yes | yes | yes if weekly; else monthly-scoped | yes | **CONDITIONAL** | Not in the paper's weekly-Admin2 list; literature shows province (Admin1) weekly 2002–2020 (Colón-González 2021) — confirm OpenDengue resolution |
| Mexico | **verify in extract** | Admin1/2 — verify | through 2023 | 32 states | large | likely | yes | yes | verify | yes | **CONDITIONAL** | Not in paper's weekly-Admin2 list; EWARS operational precedent — confirm resolution |
| Philippines / China / Taiwan | weekly (confirmed) | Admin2 (confirmed) | through 2023 | many | large | verify | yes | yes | yes | yes | **Backup KEEP** | Weekly Admin2 confirmed (paper) — available alternatives |

## 4. Recommendation
- **Best one-country external-replication candidate: Brazil** — weekly Admin2 confirmed, largest counts, most spatial units (strongest RDHS-analog cluster bootstrap), widely used in the literature.
- **Backup: Colombia** — weekly Admin2 confirmed, with a direct climate-EWS precedent (EWARS-csd).
- **Is external replication feasible now?** **Yes, in principle** — weekly subnational coverage is **confirmed** for Brazil and Colombia, satisfying the core criteria (weekly → h=4; Admin2 → many clusters; long span → train/test). **However, building the dataset requires a full extract download (≈54 MB Temporal/Spatial), plus per-country Admin2 boundaries (GADM) and ERA5/CHIRPS linkage** — real, non-trivial effort. Per the gating rule, the extract download is the **next gated step → stop and ask before downloading.**
- **Include in this paper or save for Paper 2?** **Strongly recommended as the highest-leverage strengthener, but not required for first submission.** Practical guidance:
  - If you want to **lift the tier** and can invest the build effort: include **one clean country (Brazil)** as an external-replication arm in this paper.
  - If you want to **submit sooner**: keep this paper single-country (publishable as methods/decision-evaluation/data-resource) and make the Brazil/Colombia external replication **Paper 2 / fast-follow** (the catalog confirms it's feasible, so it's a credible "future work" with a concrete plan).

## 5. Honest limitations of this inspection
- Exact per-country **year spans, unit counts, and unit stability** were **not** confirmed (they live in the 54 MB extracts, not downloaded). Marked "verify in extract."
- OpenDengue is **through 2023**; the external train/test split must sit within each country's coverage (not aligned to Sri Lanka's 2018–2025). This is a *replication of the framework*, not coefficient transfer.
- Climate linkage feasibility is asserted (ERA5-Land/CHIRPS are global) but requires sourcing per-country Admin2 boundaries — an effort, not free.

## 6. Confirmations
- **Catalog inspection only:** no models, no metrics, no labels, no climate linkage, no external-validation tables.
- **Only small metadata downloaded** (`metadata_main.json` 4.5 KB, `metadata_source.json` 3.2 KB) to quarantine, read-only; **full case datasets (54 MB extracts) NOT downloaded** — that is the gated next step.
- **No data files committed** — only this markdown report is proposed for commit. No external-validation claim made.

## 7. Next step (gated)
On approval: **download the V1.3 Temporal (or Spatial) extract (~54 MB)** to quarantine, confirm Brazil (and Colombia) exact weekly Admin2 span/units/stability, then — separately — design and run the single-country replication. Each step approval-gated; the full extract download requires your explicit go-ahead.
