# data/ — intentionally empty (no data committed)

This directory is a placeholder. **No surveillance data, raw PDFs, climate rasters, or the frozen outcome CSV are stored in this repository.**

## Why
- The dengue counts are the property of the **Sri Lanka Epidemiology Unit** and are subject to that source's terms of use.
- Raw PDFs and the frozen CSV are large and/or governed; they live only in a local, git-ignored quarantine (`data_quarantine/`).

## How to obtain / regenerate the data locally
1. Run `scripts/wer_bulk_harvest.py` to harvest and download the public WER PDFs (2018–2025) into a local quarantine folder.
2. Run `scripts/wer_bulk_extract_dengue_v2.py` to extract the RDHS × dengue current-week outcome.
3. Run `scripts/wer_qc_report_v2.py` for QC.
4. Freeze the validated current-week CSV and verify its SHA256 against the value in the top-level `README.md` / `qc_summaries/FREEZE_LOG.md`:
   `99f0b9b122460c7d24a6672bbc933176af250789c4b492b421852c2626af3e99`

## Expected local (git-ignored) layout
```
data_quarantine/
  wer_srilanka/
    raw_bulk/        # downloaded WER PDFs (ignored)
    processed_quarantine/
    frozen/          # frozen current-week CSV + metadata (CSV ignored)
    qc/
  geomatics/         # crosswalk fill, boundaries (ignored)
```

Place data only under git-ignored paths. Never commit `.pdf`, `*-frozen.csv`, rasters, or `data_quarantine/` contents.
