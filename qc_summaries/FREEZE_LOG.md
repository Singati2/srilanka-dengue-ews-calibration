# FREEZE LOG — WER Current-Week Dengue Outcome Dataset

## v2.0-frozen — 2026-06-10
- **Event:** Froze the validated current-week WER dengue outcome dataset.
- **Frozen file:** `frozen/wer_dengue_currentweek_rdhs_2018_2025_v2.0-frozen.csv`
- **SHA256:** `99f0b9b122460c7d24a6672bbc933176af250789c4b492b421852c2626af3e99`
- **Size:** 593,674 bytes
- **Rows:** 10,790 (415 issues × 26 RDHS)
- **Permissions:** read-only (`-r--r--r--`)
- **Source file (byte-identical):** `processed_quarantine/wer_dengue_rdhs_2018_2025_quarantine_v2.csv` (verified via `cmp`)

### Basis for freeze
- Structural QC: 415/415 issues at 26 rows.
- Current-week QC: 0 invalid values across 10,757 real cells.
- Manual/double-entry QC: 33 sampled issues, **0 mismatches** (~624 cells independently verified; all eras covered).
- Documented missingness accepted: 33 NA cells (Gampaha 2018 wk23–52; Puttalam ×3) + 2022 wk44.

### Scope constraints honored at freeze
- No climate/exposure linkage. No models. Preregistration unmodified.
- Cumulative field NOT used for analysis (QC-only).
- No pre-2018 extraction. No OCR. OpenDengue remains quarantined negative.
- Institutional email remains optional/upside (not blocking).
- Dataset remains in QUARANTINE (frozen copy created; not promoted to a final analysis directory).

### Integrity-check command (re-verify anytime)
```
sha256sum -c <<< "99f0b9b122460c7d24a6672bbc933176af250789c4b492b421852c2626af3e99  wer_dengue_currentweek_rdhs_2018_2025_v2.0-frozen.csv"
```

### Change policy
- The frozen CSV is immutable. Any correction (e.g., OCR recovery of the 33 NA cells, or institutional-feed replacement) must produce a **new versioned freeze** (v2.1-frozen / v3.0-frozen) with its own checksum and a new log entry. Do not edit v2.0-frozen in place.
