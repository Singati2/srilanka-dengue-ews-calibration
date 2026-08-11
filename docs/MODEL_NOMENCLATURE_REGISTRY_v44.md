# Model nomenclature registry — v44

**Instruction:** `instruction_m6.md` §21 · §24 item 6 · also satisfies round-3 prompt §5.1
(`CLAUDE_V44_ROUND3_SUBMISSION_GATES_GEOMATICS_EXECUTION.md`) · **Written:** 2026-08-11
**Purpose:** `M6` and `M7` are each used for **two different models in two different countries**.
This registry fixes what every label means and supplies collision-free manuscript-facing names.

> **Rule adopted:** historical scripts, artifacts and logs are **not renamed** — renaming would
> break provenance. The manuscript uses descriptive names only. **Bare `M6` and bare `M7` must not
> appear in v44** without a country qualifier, because neither is unambiguous.

---

## 1. The collision, stated plainly

| Label | Meaning A | Meaning B |
|---|---|---|
| **M6** | **Colombia**, geo/SPI pilot: *cases + SPI (8/13/26 wk)* — a **hybrid** | **Sri Lanka**, 2026-08: *geomatics-only, no case history* — a **standalone comparator** |
| **M7** | **Colombia**, geo/SPI pilot: *M5 + SPI* | (unused in the Sri Lanka work) |

The two `M6`s are opposite in kind: one *adds* an environmental block to surveillance, the other
*removes* surveillance entirely. Reporting either as "M6" invites a reader to merge them.

A third, unrelated `M6/M7` usage exists in `docs/climate_data_extraction_handoff_v1.md`
("complete the M6/M7 geo hybrid") — it refers to Meaning A.

---

## 2. Registry — every model label in tracked code, docs and manuscripts

| Historical label | Country | Feature set | Implementation / code path | Status | Manuscript-facing name | In v44? |
|---|---|---|---|---|---|---|
| **M0** | SL + CO | Season only (Fourier harmonics) | frozen ladder; CO: `scripts/colombia_model_ladder_h4_75pct_M6_v1.py` | Frozen, reported | **Seasonal climatological baseline** | Yes |
| **M1** | SL | Recent cases (AR) **+ seasonal harmonics + RDHS fixed effects** | frozen ladder | Frozen, reported — the operational comparator | **Surveillance baseline (Sri Lanka)** | Yes |
| **M1** | CO | Recent-incidence lags 0,1,2,4 **only** | as above | Frozen, reported | **Surveillance baseline (Colombia)** | Yes |
| **M2** | SL + CO | Climate only | frozen ladder | Frozen, reported | **Climate-only** | Yes |
| **M3** | SL + CO | Climate + season + geographic FE | frozen ladder | Frozen, reported | **Structured climate** | Yes |
| **M4** | SL | Cases + climate (DLNM-style cross-basis), 31 features | frozen ladder | Frozen — **design-locked planned primary hybrid** (lock `1d8e268`, 2026-06-14) | **Planned primary hybrid** | Yes |
| **M4** | CO | Cases + climate | frozen ladder | Frozen, reported | **Planned primary hybrid (Colombia)** | Yes |
| **M5** | SL | M4 + seasonal harmonics + geographic FE, 60 features | frozen ladder | Frozen — pre-computation expanded/steelman sensitivity | **Expanded hybrid** | Yes |
| **M5** | CO | Cases + climate + season + dept FE | frozen ladder | Frozen, reported | **Expanded hybrid (Colombia)** | Yes |
| **M5-no-climate** | SL + CO | M5 minus the climate block, independently refit | matched-ablation pipeline | Frozen — post-hoc, exploratory; **primary climate estimand** | **Matched no-climate comparator** | Yes |
| **M6** *(Meaning A)* | **CO** | Cases + SPI (8/13/26 wk) | `analysis/m6_geo_pilot/m0_m7_comparison.md`; `scripts/colombia_model_ladder_h4_75pct_M6_v1.py` | **PILOT — explicitly not quotable**; analysis plan not frozen | **Colombia drought-index hybrid (pilot)** | **No** |
| **M7** *(Meaning A)* | **CO** | M5 + SPI | same as above | **PILOT — not quotable** | **Colombia expanded hybrid + drought index (pilot)** | **No** |
| **M6** *(Meaning B)* | **SL** | Geomatics only — Batch A terrain + B statics + C dynamic RS; 92 features; **no case history, no climate reanalysis** | `notebooks/00–08`; manifest `analysis/geomatics_integration_v1/M6_CORE_FEATURE_MANIFEST.yaml` | **`M6-core (A/B/C)`** — fitted and scored, `EXPLORATORY_RECONSTRUCTED_TARGET`; 12 of 16 planned variables (Batch D absent) | **Geomatics-core standalone (Sri Lanka)** | Only if §22 gates pass |
| *(reserved)* `M6-extended` | SL | `M6-core` + Batch D (#13 mobility, #14 wealth, #15 healthcare access, #16 phenology) | not built | **Does not exist.** Name reserved so a future build is not confused with `M6-core` | **Geomatics-extended** | No |
| *(planned)* `M5_PLUS_GEO` | SL | Matched comparator + geomatics block | **not built** — no base design matrix in this repo | **BLOCKED** (`instruction_m6.md` §8; only M5 *predictions* are available, not features) | **Surveillance + geomatics stress test** | No |
| *(planned)* `M5_NO_GEO` | SL | The same comparator without the geomatics block | not built | **BLOCKED**, same reason | **Matched no-geomatics comparator** | No |
| *(planned)* `DELTA_GEO` / $\Delta V_G$ | SL | $V(\mathcal I^{SG}) - V(\mathcal I^{S})$ | not estimated | **PENDING / NOT ESTIMATED** — consistent with `BIOMATH_NOTATION_TABLE.md` | **Incremental geomatics value** | Framework note only |
| **M18** | — | *not a model* | — | Token appears only in supporting-information file names (`…_v18.md`) | — | — |

---

## 3. Naming rules for v44

1. **Never write bare `M6` or `M7`.** Write `M6-core (Sri Lanka, geomatics-only)` or
   `Colombia SPI pilot M6`, or preferably the descriptive name from the table.
2. **`M6-core (A/B/C)` is the only name for the executed geomatics model.** Not "M6", not "the
   geomatics model", not "the 16-variable M6" (`M6_BATCH_D_AUDIT.md`).
3. **`M6-extended` is reserved, not built.** Using it for anything that exists today is a
   fabrication of completion.
4. **`M5-no-climate` ≠ `M5_NO_GEO`.** The first exists and is frozen; the second is BLOCKED. Their
   similarity is the second-most likely source of a provenance error in this repo after the M6
   collision.
5. **Country qualifier is mandatory on M1.** Sri Lanka's M1 carries seasonal harmonics and RDHS
   fixed effects; Colombia's M1 does not. A cross-country sentence about "M1" is false unless it
   says which.
6. **Pilot artifacts stay tagged.** `analysis/m6_geo_pilot/` is marked *"PILOT — NOT A QUOTABLE
   RESULT"* at the top of its own comparison file. That tag travels with any number taken from it.

---

## 4. What this registry does not do

It does not rename any file, script, column or artifact, and it does not change any result. It is a
lookup table. If a future rename is wanted, it should be a separate, single commit that touches only
names and is verified by re-running the acceptance test (`3,926/3,926`), not folded into analysis
work.
