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
| Nonmissing `dengue_total` | 2,390,016 (**0% missing**) |
| Year span (all tiers) | 1980–2024 (45 distinct years) |
| Spatial resolution (`S_res`) | Admin2 = 2,388,678; Admin1 = 719; Admin0 = 619 |
| Temporal resolution (`T_res`) | Week = 1,896,112; Month = 493,859; Year = 45 |
| **Weekly Admin2 tier** | **1,895,538 rows · 5,239 municipalities · years 2013–2024 · 0% missing** |
| # Admin1 units | 27 (matches Brazil's 26 states + DF) |
| # Admin2 units | 5,250 municipalities |
| Units-per-year (weekly Admin2) | 3,551 → 4,972 municipalities/year (stable, large) |

- **Per-year weekly Admin2 (rows, all 0% missing):** 2013: 3,690 (partial); 2014: 191,880; 2015: 226,772; 2016: 236,392; 2017: 172,892; 2018: 165,699; 2019: 225,161; 2020: 211,952; 2021: 196,248; **2022: 76,855; 2023: 76,816**; 2024: 111,181.
- **Honest caveat:** 2022–2023 weekly-Admin2 row counts are markedly lower (~77k vs ~200k), suggesting **reduced municipal weekly coverage those two years** (fewer municipalities/weeks reported, not missing values — the rows present are complete). 2014–2021 and 2024 are dense. A clean train/test window can avoid relying on 2022–2023 (e.g., train 2014–2019, test 2020–2021), or treat 2022–2023 cautiously.

### 3.2 Colombia
| Item | Value |
|---|---|
| Total rows (Colombia) | 203,770 |
| Nonmissing `dengue_total` | 203,770 (**0% missing**) |
| Year span (all tiers) | 1960–2024 (56 distinct years) |
| Spatial resolution (`S_res`) | Admin2 = 199,488; Admin1 = 3,654; Admin0 = 628 |
| Temporal resolution (`T_res`) | Week = 203,398; Year = 372 |
| **Weekly Admin2 tier** | **199,458 rows · 989 municipalities · years 2006–2022 · 0% missing** |
| # Admin1 units | 42 (departments + special districts) |
| # Admin2 units | 992 municipalities |
| Units-per-year (weekly Admin2) | 677 → 834 municipalities/year (stable) |

- **Per-year weekly Admin2 (rows, all 0% missing), 2008–2022:** 8,251–19,316 rows/year; ~700–830 municipalities/year; no year below ~8k obs.
- **Honest caveat:** Colombia weekly Admin2 **ends in 2022** in this extract (no 2023–2024 weekly Admin2). Train/test must sit within 2006–2022 (ample).

## 4. Per-country feasibility checklist (the requested fields)
| Criterion | Brazil | Colombia |
|---|---|---|
| Temporal resolution | **Weekly** (also Month/Year) | **Weekly** (essentially all weekly) |
| Spatial resolution | **Admin2 (municipality)** | **Admin2 (municipality)** |
| Years available (weekly Admin2) | **2013–2024** (2014–2021 + 2024 dense; 2022–23 thin) | **2006–2022** (2008–2022 dense) |
| # Admin1 units | 27 | 42 |
| # Admin2 units | 5,250 (≈5,239 in weekly tier) | 992 (≈989 in weekly tier) |
| # observations (weekly Admin2) | 1,895,538 | 199,458 |
| # nonmissing case counts | **100% (0% missing)** | **100% (0% missing)** |
| Missingness by year | 0% every weekly-Admin2 year | 0% every weekly-Admin2 year |
| Units stable over time? | Yes (3.5k–5.0k munis/yr; thinner 2022–23) | Yes (677–834 munis/yr) |
| **Weekly h=4 feasible?** | **Yes** | **Yes** |
| **75th-pct outbreak label feasible?** | **Yes** (large counts; see denominator note) | **Yes** (see denominator note) |
| **Train/test split feasible?** | **Yes** (e.g., 2014–2019 / 2020–2021) | **Yes** (e.g., 2008–2017 / 2018–2022) |
| **≥10 spatial clusters for cluster bootstrap?** | **Yes — overwhelmingly** (27 states or thousands of munis) | **Yes** (42 departments or ~700–830 munis) |

**Label denominator note (honest, build-time):** Sri Lanka used a per-RDHS **75th-percentile incidence** label, which needs population denominators. OpenDengue provides **case counts only**. Two clean options: (a) compute the 75th-pct label on **case counts** per municipality (train-only) — no denominators needed; or (b) link municipal population (IBGE for Brazil, DANE for Colombia) for incidence. Option (a) keeps the external arm self-contained; this is a design choice, not a blocker.

## 5. Recommendation
- **Both Brazil and Colombia are FEASIBLE** for a weekly-Admin2 external replication of the decision-evaluation framework — both deliver **weekly municipality-level counts, 0% missing, stable units, ample years, and far more than 10 spatial clusters**. This *exceeds* what the catalog memo could confirm.
- **Recommended primary: Brazil** — largest (1.9M weekly obs, 5,239 municipalities, through 2024), strongest cluster bootstrap, most-cited in the dengue-forecasting literature. **Caveat to manage:** the 2022–2023 weekly thinning (pick a train/test window in the dense years).
- **Recommended as the clean second/backup: Colombia** — 199k weekly obs, ~989 municipalities, dense 2008–2022, **0% missing throughout**, and a direct climate-EWS precedent (EWARS-csd municipal, Schlesinger 2024). Colombia is arguably the *cleaner single window* (no coverage dip), just smaller.
- **Scope discipline:** do **one** country for the first external arm (Brazil), with Colombia as a ready fast-follow / second arm — not a multi-country sweep.
- **Include in this paper vs Paper 2:** the data are confirmed clean, so an external arm is now a **concrete, low-risk build** (the remaining real effort is GADM Admin2 boundaries + ERA5/CHIRPS linkage + the local re-fit). If you want to lift the venue tier and can invest that build, **include Brazil as a one-country external-replication arm**; if you want to submit sooner, keep single-country and make Brazil the **Paper 2 / fast-follow** — either way the transportability claim is now backed by verified coverage, not assumption.

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
