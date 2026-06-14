# Colombia Manual Alias / DIVIPOLA Crosswalk Finalization (crosswalk only — build NOT run)
*Finalizes a small, auditable crosswalk for the residual unmatched OpenDengue Colombia Admin2 units. **No outbreak labels; no models; no climate linkage; no ERA5/CHIRPS download; no AUC/PR-AUC/calibration/DCA/net-benefit/ΔNB; no prediction tables; no external validation.** Only crosswalk adjudication using already-quarantined artifacts. Small crosswalk artifacts stay in quarantine (read-only); no data files committed.*

**Date:** 2026-06-14 · **Status:** crosswalk finalization only · **Base commit:** a4ff3be · **Builds on:** `docs/colombia_boundary_climate_feasibility_report.md`.

## A. Residual unmatched units reviewed
From the **conservative** saved crosswalk (`colombia_crosswalk_v1.csv`, exact+alias tiers): **14 unmatched (department, municipality) units**, totalling **2,597 weekly observations** (1.30% of 199,458). Each was adjudicated against GADM v4.1 Admin2 (`NAME_2` + `VARNAME_2`), with **targeted and global GADM name searches** to avoid forcing matches.

## B. Manual alias decisions (full table)
| OD dept | OD municipality | GADM target | GID_2 | match_type | rec | weekly obs |
|---|---|---|---|---|---|---|
| MAGDALENA | SANTA MARTHA | Santa Marta | COL.20.26_2 | spelling_fix | include | 782 |
| CHOCO | ITSMINA | Istmina | COL.13.15_2 | spelling_fix | include | 350 |
| CORDOBA | SAN ANDRES SOTAVENTO | San Andrés de Sotavento | COL.14.20_2 | manual_alias | include | 308 |
| CORDOBA | TUCHIN | *[parent]* San Andrés de Sotavento | COL.14.20_2 | newly_created | review | 290 |
| GUAJIRA | ALBANIA | *[parent]* Maicao | COL.19.8_2 | newly_created | review | 206 |
| VALLE | DARIEN | Calima (Calima–El Darién) | COL.31.9_2 | manual_alias | include | 193 |
| BOLIVAR | NOROSI | *[parent]* Río Viejo | COL.6.26_2 | newly_created | review | 113 |
| CAUCA | GUACHENE | *[parent]* Caloto | COL.11.8_2 | newly_created | review | 88 |
| TOLIMA | VILLARICA | Villarrica | COL.30.47_2 | spelling_fix | include | 68 |
| CORDOBA | SAN JOSE DE URE | *[parent]* Montelíbano | COL.14.13_2 | newly_created | review | 66 |
| CUNDINAMARCA | SAN ANTONIO DE TEQUENDAMA | San Antonio del Tequendama | COL.15.76_2 | manual_alias | include | 63 |
| CHOCO | LITORAL DEL BAJO SAN JUAN | El Litoral del San Juan | COL.13.14_2 | manual_alias | include | 45 |
| MAGDALENA | CERRO SAN ANTONIO | Cerro de San Antonio | COL.20.4_2 | spelling_fix | include | 20 |
| BOYACA | CIENEGA | Ciénaga (Boyacá) | COL.7.23_2 | spelling_fix | include | 5 |

- **9 clean fixes → include** (5 `spelling_fix`, 4 `manual_alias`), 1,834 weekly obs. Each is the *same* municipality under a spelling/connector/seat-name variant (e.g., Itsmina↔Istmina; Darién = the municipality GADM names **Calima**; San Antonio **de**↔**del** Tequendama). The departmental capital **Santa Marta** (782 obs) is the largest and is a pure spelling fix.
- Full machine-readable table (read-only): `colombia_manual_alias_crosswalk_v1.csv`.

## C. Unresolved / excluded units
- **0 unresolved**, **0 forced**, **0 corregimiento-departamental** in this residual set.
- **5 `newly_created` municipalities are genuinely absent from GADM v4.1** — verified by global GADM search returning **no in-department polygon**: **Tuchín** (2007), **Albania–La Guajira** (2000), **Norosí** (2007), **Guachené** (2006), **San José de Uré** (2007). GADM's only "Albania" polygons are in Caquetá/Santander (wrong geography) — **not** force-matched.
- **Handling (primary vs sensitivity — not forced):** each daughter municipality has an **unambiguous GADM parent** polygon (the municipality it was carved from), but the daughter itself has **no polygon** in GADM v4.1.
  - **Primary build:** **do not force-match** newly-created municipalities absent from GADM v4.1 in the primary climate-linked analysis; **exclude/flag them in the primary build.**
  - **Sensitivity:** as a sensitivity, **assign climate exposure using the documented parent polygon**, keeping the newly-created municipality as its **own outcome unit** (cases never double-counted).
  - **Why:** they account for only **763 observations, 0.383%** of the Colombia weekly Admin2 data, so **primary exclusion has negligible impact and avoids boundary approximation.**

## D. Post-manual match rate
| Scenario | Matched units | Unit % | Unmatched weekly obs | Unmatched % |
|---|---|---|---|---|
| Auto only (conservative base) | 1,057 / 1,071 | 98.69% | 2,597 | 1.30% |
| **B — PRIMARY (9 includes; 5 newly-created excluded/flagged)** | **1,066 / 1,071** | **99.53%** | **763** | **0.383%** |
| **A — SENSITIVITY (newly-created via parent polygon)** | **1,071 / 1,071** | **100.0%** | **0** | **0.000%** |

## E. Unmatched observation share
**0.000% (Scenario A) to 0.383% (Scenario B).** Either way ≤ 763 of 199,458 weekly observations, all in 5 small newly-created municipalities.

## F. >5% stop-gate
**PASS in both scenarios** (0.000%–0.383% ≪ 5%).

## G. DIVIPOLA feasibility
- **No code bridge in GADM:** GADM v4.1 `CC_2` is empty and `GID_2` is GADM's own identifier (e.g., `COL.31.9_2`) — neither is DIVIPOLA. Confirmed again here.
- **DANE DIVIPOLA municipality code table** (~1,100 rows: department + municipality + 5-digit code) is publicly available and small. **Not downloaded** (out of scope; not needed for the primary label).
- **Likely linkage route (documented, not run):** a **name-based department+municipality join** reusing this crosswalk's normalization (accent/case/space-insensitive + the alias table above), since no code key exists. Expected to be high-yield given the same normalization already reaches ~99.5–100% here.
- **Label policy unchanged:** the **count-based 75th-pct outbreak label remains PRIMARY** (denominator-free). The **incidence label stays an OPTIONAL pre-registered sensitivity**, contingent on a later small DANE/DIVIPOLA name crosswalk. **Incidence is not made primary.**

## H. Recommendation for next step (separately gated)
- **Crosswalk is finalized and the stop-gate passes with large margin.** Proceed (when approved) to the **gated ERA5-Land + CHIRPS download + zonal aggregation** to the matched Admin2 polygons, using:
  - the auto-matched 1,057 units **plus** the 9 manual `include` fixes = **1,066 polygon-matched units** for the **primary** build, **excluding/flagging** the 5 `newly_created` daughters (763 obs, 0.383%); **as a sensitivity only**, route those 5 daughters to their documented parent polygon (Scenario A).
- The DANE/DIVIPOLA name crosswalk is only needed **if** the optional incidence-label sensitivity is later activated.
- **None of that is run now.**

## I. Quarantined outputs (read-only; NOT committed) + SHA256 (16-char) / size
- `colombia_manual_alias_crosswalk_v1.csv` — `dc4e3fadc30a0be3…` — 2,341 B
- `colombia_crosswalk_final_summary_v1.json` — `3db5ef80179b7f33…` — 880 B
- (inputs reused, unchanged: `colombia_crosswalk_v1.csv`, `colombia_admin2_metadata_v1.csv`, `gadm41_COL_2.json.zip`)
- All under `~/data_quarantine/colombia_external_replication_feasibility_v1/`, chmod 444.

## J. Confirmations
- **Crosswalk finalization only:** no outbreak labels, no models, no climate linkage, **no ERA5-Land/CHIRPS download**, no AUC/PR-AUC/calibration/DCA/net-benefit/ΔNB, no prediction tables, no external validation.
- **No DANE data downloaded** (availability assessed only).
- **No Sri Lanka frozen data or prior outputs read for modeling, modified, or overwritten;** inputs reused read-only.
- **No data files committed** — only this markdown report is proposed for commit (pending your approval).
