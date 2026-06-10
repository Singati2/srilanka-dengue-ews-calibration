# srilanka-dengue-ews-calibration

**Calibration and decision-curve evaluation of climate-driven dengue early-warning models in Sri Lanka.**

> ⚠️ **This repository contains CODE and DOCUMENTATION only. No surveillance data, raw PDFs, climate rasters, or the frozen outcome dataset are committed here.** See [`data/README.md`](data/README.md).

## Project goal
Evaluate, using **existing published model classes** (not a new forecasting model), whether two climate-driven dengue early-warning systems with comparable discrimination (AUC) lead to **different public-health alert decisions** under calibration and decision-curve / net-benefit analysis in Sri Lanka. The methodological contribution is empirical and regional: external validation, **calibration**, **recalibration**, and **decision-curve / net-benefit** evaluation of outbreak alerts, plus spatial decision-support. We explicitly do **not** claim methodological novelty (see `docs/osf_prereg_skeleton.md` for the prior-work positioning, incl. Tozan 2023 cost-loss/net-benefit lineage).

## What is frozen (held locally, NOT in this repo)
A validated **current-week WER dengue outcome dataset**:
- Source: Sri Lanka Epidemiology Unit, Weekly Epidemiological Reports (WER), Table 1.
- Years **2018–2025**, spatial unit **26 RDHS divisions**, temporal unit **epidemiological week / WER issue**.
- Rows **10,790**; real current-week cells **10,757**; documented **NA cells 33**; missing full issue **2022 week 44**; invalid current-week values **0**.
- Manual QC: **33 sampled issues, 0 mismatches**.
- Primary outcome field: `dengue_current_week`. The `dengue_cumulative` field is **QC-only, not for analysis**.
- **SHA256 of frozen CSV:** `99f0b9b122460c7d24a6672bbc933176af250789c4b492b421852c2626af3e99`

The freeze metadata/log is in [`qc_summaries/FREEZE_LOG.md`](qc_summaries/FREEZE_LOG.md). The data dictionary is in [`data_dictionary/`](data_dictionary/).

## What is NOT included in this repository
Raw WER PDFs · the frozen outcome CSV · `data_quarantine/` and `raw_bulk/` contents · climate rasters (ERA5/CHIRPS/MODIS, `.nc/.tif/...`) · any `.zip/.tar/.gz/.xz/.h5/.nc/.tif/.pdf` data file · credentials · private emails / institutional correspondence. These are blocked by [`.gitignore`](.gitignore).

## Repository layout
```
README.md                  LICENSE                .gitignore
docs/                      project overview, data-access plan, geomatics SOW,
                           OSF prereg skeleton, PROBAST/TRIPOD instrument
scripts/                  WER harvest + extraction (v2) + QC scripts
data_dictionary/          field-level documentation of the outcome dataset
qc_summaries/             extraction QC, manual-QC report, freeze log
geomatics_templates/      RDHS crosswalk template (WP1)
data/README.md            how to obtain/place the data locally (no data committed)
```

## Reproducibility
The pipeline is reproducible from public sources using `scripts/`:
1. `wer_bulk_harvest.py` — harvest WER issue URLs (both URL schemes), download, validate `content-type`, record a manifest with checksums.
2. `wer_bulk_extract_dengue_v2.py` — extract RDHS × dengue current-week from Table 1 (`pdftotext -layout` + plain-text fallback + NA-fill).
3. `wer_qc_report_v2.py` — structural + current-week + cumulative QC.

Re-running against the public WER archive reproduces the local frozen dataset; verify integrity against the SHA256 above. Tooling: Python 3 + poppler (`pdftotext`). No data is required to read the docs/QC.

## Current status
- ✅ Outcome dataset built, QC-validated, and **frozen** (local).
- ✅ OpenDengue evaluated and recorded as a **quarantined negative** (Sri Lanka not available at district/RDHS-weekly).
- ⬜ Geomatics **WP1** (RDHS boundary crosswalk + population denominators) — planning in place (`geomatics_templates/`, `docs/geomatics_scope_of_work.md`).

## Next phase
**Geomatics WP1:** finalize the RDHS↔district/province crosswalk and boundary vintage, resolve the **Kalmunai/Ampara split**, and assign **annual population denominators** (WorldPop + census). No climate download, no exposure construction, and no outcome↔exposure linkage until WP1 is complete and the preregistration is finalized.

## Data source & citation
Dengue counts: **Sri Lanka Epidemiology Unit, Ministry of Health — Weekly Epidemiological Report** (https://www.epid.gov.lk/weekly-epidemiological-report). Please cite the Epidemiology Unit as the data source in any output. The data are not redistributed here.

## ⚠️ Data-handling warning
Raw surveillance PDFs and the frozen outcome dataset are **deliberately not committed**. Do not add them. The `.gitignore` blocks data formats and the quarantine folders; always run the forbidden-file guard (see `docs/project_overview.md`) before committing.
