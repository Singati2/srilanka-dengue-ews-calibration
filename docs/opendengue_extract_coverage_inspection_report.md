# OpenDengue Extract Coverage-Inspection Report (Brazil & Colombia, feasibility only)
*Extract-level coverage inspection to confirm exact Brazil/Colombia weekly subnational coverage for **one** external-replication arm. **No models fit; no AUC/calibration/DCA/net-benefit; no outbreak labels; no ERA5/CHIRPS climate linkage; no external-validation tables. Only descriptive coverage counts (rows, years, units, resolution, missingness) were computed.** The OpenDengue extract is stored only in quarantine (read-only); no data files committed.*

**Date:** 2026-06-14

## 1. What was downloaded (minimum needed, provenance)
- **Source:** `https://raw.githubusercontent.com/OpenDengue/master-repo/main/data/releases/V1.3/Temporal_extract_V1_3.zip` (the "best temporal resolution" extract — where weekly data live).
- **Downloaded to quarantine only** (`~/data_quarantine/opendengue_extract_inspection_v1/`, **read-only chmod 444**): `Temporal_extract_V1_3.zip`, **54,872,272 bytes** — **exact match to the catalog size (not larger than expected)**.
  - **sha256:** `7f5df2174404313a36596342bb26e4614c3c08577fab75550725e195326bcda6`.
- Inner CSV `Temporal_extract_V1_3.csv` (504,447,270 bytes) was **read in-memory in chunks from the zip — never extracted to disk**, so quarantine footprint stays at the 53 MB zip.
- **Spatial_extract NOT downloaded** — unnecessary: the Temporal extract already contains **weekly Admin2** for both Brazil and Colombia. This is the minimum download to answer the question.

## 2. Method (descriptive only)
Filtered the 504 MB CSV to `adm_0_name ∈ {BRAZIL, COLOMBIA}` (country names are UPPERCASE in the data). Computed per country: row counts, nonmissing `dengue_total`, year span, `S_res × T_res` cross-tab (spatial × temporal resolution), Admin1/Admin2 unit counts, and — for the finest weekly tier — by-year row counts, missingness, and units-per-year (stability). **No labels, no models, no climate linkage, no metrics.**

## 3. Coverage findings

### 3.1 Brazil
| Item | Value |
|---|---|
| Total rows (Brazil) | 2,390,016 |
| Nonmissing `dengue_total` (rows present) | 2,390,016 (**0% NaN among existing rows** — does **not** mean every municipality-week is covered) |
| Year span (all tiers) | 1980–2024 (45 distinct years) |
| Spatial resolution (`S_res`) | Admin2 = 2,388,678; Admin1 = 719; Admin0 = 619 |
| Temporal resolution (`T_res`) | Week = 1,896,112; Month = 493,859; Year = 45 |
| **Weekly Admin2 tier** | **1,895,538 rows · 5,239 municipalities · years 2013–2024** |
| # Admin1 units | 27 (matches Brazil's 26 states + DF) |
| # Admin2 units | 5,250 municipalities |
| Units-per-year (weekly Admin2) | 3,551 → 4,972 municipalities/year (**varies → unbalanced panel**) |
| **Unit persistence (weekly Admin2)** | **2,187 / 5,239 municipalities (42%) report in every year; median 11 of 12 years per unit** |

- **Per-year weekly Admin2 (rows; 0% NaN among present rows):** 2013: 3,690 (partial); 2014: 191,880; 2015: 226,772; 2016: 236,392; 2017: 172,892; 2018: 165,699; 2019: 225,161; 2020: 211,952; 2021: 196,248; **2022: 76,855; 2023: 76,816**; 2024: 111,181.
- **Honest characterization (revised):** `dengue_total` has **0% missing among the rows that exist**, but this is **not** complete coverage of every municipality-week. **Absent rows are implicit coverage gaps**: only 42% of municipalities report in every year (median 11/12), and the **2022–2023 weekly-Admin2 row counts drop sharply** (~77k vs ~200k) — reduced municipal weekly coverage those two years. Treat Brazil as an **unbalanced surveillance panel**, not a balanced one. A clean train/test window can avoid relying on 2022–2023 (e.g., train 2014–2019, test 2020–2021).

### 3.2 Colombia
| Item | Value |
|---|---|
| Total rows (Colombia) | 203,770 |
| Nonmissing `dengue_total` (rows present) | 203,770 (**0% NaN among existing rows** — does **not** mean every municipality-week is covered) |
| Year span (all tiers) | 1960–2024 (56 distinct years) |
| Spatial resolution (`S_res`) | Admin2 = 199,488; Admin1 = 3,654; Admin0 = 628 |
| Temporal resolution (`T_res`) | Week = 203,398; Year = 372 |
| **Weekly Admin2 tier** | **199,458 rows · 989 municipalities · years 2006–2022** |
| # Admin1 units | **33 in the weekly-Admin2 working tier** (Colombia's 32 departments + Bogotá; verified clean list) — *not* 42 (see note) |
| # Admin2 units | 992 municipalities |
| Units-per-year (weekly Admin2) | 677 → 834 municipalities/year (**varies → unbalanced panel**) |
| **Unit persistence (weekly Admin2)** | **127 / 989 municipalities (13%) report in every year; median 14 of 17 years per unit** |

- **Per-year weekly Admin2 (rows; 0% NaN among present rows), 2008–2022:** 8,251–19,316 rows/year; ~700–830 municipalities/year; no year below ~8k obs.
- **Admin1 count note:** the working **weekly-Admin2** tier groups into exactly **33 standard Admin1 names** (departments + Bogotá), verified by listing them. The **42** figure arises only when the broader **mixed-resolution** Admin1/Year-level rows are included; **42 should not be used for the external-validation working tier — use 33.**
- **Honest characterization (revised):** as with Brazil, `dengue_total` has **0% missing among existing rows** but this is **not** complete municipality-week coverage — **absent rows are implicit coverage gaps**: only 13% of municipalities report in every year (median 14/17). Treat Colombia as an **unbalanced surveillance panel**. Weekly Admin2 **ends in 2022** (no 2023–2024); train/test must sit within 2006–2022 (ample, and with no Brazil-like coverage dip).

## 4. Per-country feasibility checklist (the requested fields)
| Criterion | Brazil | Colombia |
|---|---|---|
| Temporal resolution | **Weekly** (also Month/Year) | **Weekly** (essentially all weekly) |
| Spatial resolution | **Admin2 (municipality)** | **Admin2 (municipality)** |
| Years available (weekly Admin2) | **2013–2024** (2014–2021 + 2024 dense; 2022–23 thin) | **2006–2022** (2008–2022 dense) |
| # Admin1 units (weekly-Admin2 tier) | 27 | **33** (42 only across mixed tiers — do not use) |
| # Admin2 units | 5,250 (≈5,239 in weekly tier) | 992 (≈989 in weekly tier) |
| # observations (weekly Admin2) | 1,895,538 | 199,458 |
| Value completeness of present rows | **0% NaN** in `dengue_total` | **0% NaN** in `dengue_total` |
| Coverage completeness | **Incomplete — implicit gaps** (absent rows; 2022–23 thinning) | **Incomplete — implicit gaps** (absent rows) |
| Units stable over time? | **Unbalanced panel** — 42% present every year; median 11/12 | **Unbalanced panel** — 13% present every year; median 14/17 |
| **Weekly h=4 feasible?** | **Yes** | **Yes** |
| **75th-pct outbreak label feasible?** | **Yes** (large counts; see denominator note) | **Yes** (see denominator note) |
| **Train/test split feasible?** | **Yes** (e.g., 2014–2019 / 2020–2021) | **Yes** (e.g., 2008–2017 / 2018–2022) |
| **≥10 spatial clusters for cluster bootstrap?** | **Yes — overwhelmingly** (27 states or thousands of munis) | **Yes** (33 departments or ~700–830 munis) |

**Label denominator note (honest, build-time):** Sri Lanka used a per-RDHS **75th-percentile incidence** label, which needs population denominators. OpenDengue provides **case counts only**. Two clean options: (a) compute the 75th-pct label on **case counts** per municipality (train-only) — no denominators needed; or (b) link municipal population (IBGE for Brazil, DANE for Colombia) for incidence. Option (a) keeps the external arm self-contained; this is a design choice, not a blocker.

## 5. Recommendation
- **Both Brazil and Colombia are FEASIBLE** for a weekly-Admin2 external replication of the decision-evaluation framework — both deliver **weekly municipality-level counts, value-complete present rows, ample years, and far more than 10 spatial clusters**. Both are **unbalanced surveillance panels** (intermittent unit reporting), which the build must handle — this is normal for surveillance data, not a blocker.
- **Recommended first external-replication arm: Colombia (the manageable arm).** A smaller, cleaner **single 2006–2022 weekly-Admin2 window**: 199k weekly obs, **989 municipalities grouped into 33 standard Admin1 departments**, **no Brazil-like 2022–2023 coverage dip**, and a direct climate-EWS precedent (**EWARS-csd Colombia municipal — citation to re-verify before manuscript use**). Smaller footprint → less GADM boundary-sourcing and ERA5/CHIRPS linkage effort for the first build. Handle the 13%-present-every-year intermittency as an unbalanced panel.
- **Retained as high-power follow-up / second arm: Brazil.** Much larger and more powerful — 1.9M weekly obs, **5,239 municipalities (27 states)**, through 2024, strongest cluster bootstrap, most-cited in the dengue-forecasting literature — but it carries a heavier workload: **deliberate handling of the 2022–2023 weekly thinning** plus larger boundary/climate-linkage effort. Best used to **confirm at scale** what the Colombia arm establishes.
- **Scope discipline:** do **one** country for the first external arm (Colombia), with Brazil as a ready high-power follow-up — not a multi-country sweep.
- **Include in this paper vs Paper 2:** coverage is now verified (feasible, unbalanced-panel caveats explicit), so an external arm is a **concrete, moderate-effort build** (remaining work: GADM Admin2 boundaries + ERA5/CHIRPS linkage + the local re-fit). If you want to lift the venue tier and can invest that build, **include Colombia as a one-country external-replication arm**; if you want to submit sooner, keep single-country and make Colombia the **Paper 2 / fast-follow**, with Brazil as the scale-up — either way the transportability claim is backed by verified coverage, not assumption.

## 6. Output / provenance
- **Downloaded (quarantine, read-only):** `~/data_quarantine/opendengue_extract_inspection_v1/Temporal_extract_V1_3.zip` — 54,872,272 bytes — sha256 `7f5df2174404313a36596342bb26e4614c3c08577fab75550725e195326bcda6`.
- Inner CSV read in-memory only; **not extracted to disk**; **Spatial extract not downloaded**.
- No quarantined output CSVs were written for this step (descriptive console inspection only). This markdown report is the only proposed commit.

## 7. Confirmations
- **Coverage inspection only:** no models, no metrics, no outbreak labels, no climate linkage, no external-validation tables, no train/test fitting.
- **Minimum download:** only the 54.9 MB Temporal extract (exact catalog size; not larger than expected) — Spatial extract avoided as unnecessary.
- **Downloaded extract stored only in quarantine, set read-only (chmod 444); sha256 recorded.**
- **No frozen outcome/exposure/population, no v1/v2 analysis table, and no prior pilot/sensitivity/recalibration/CI/DLNM/hybrid/Stage-1A output was read for modeling, modified, or overwritten.**
- **No data files committed** — only this markdown report is proposed for commit. No external-validation claim is made.
