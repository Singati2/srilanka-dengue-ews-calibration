# PAIRED_ROW_AUDIT.md
Canonical paired-row manifest: `PAIRED_ROW_MANIFEST.csv` (34,574 rows = 2 settings × 2 states).
Per-state audit (from `logs/paired_audit.json`): identical observation keys & outcomes for
both models (single row carries both probabilities), 0 duplicate canonical keys, 0 missing
probabilities, temporal order preserved, cluster labels preserved.

| setting_state | n | events | prevalence | clusters | dup_keys | missing full/noclim |
|---|---|---|---|---|---|---|
| Colombia_raw | 13361 | 5015 | 0.3753 | 475 | 0 | 0/0 |
| Colombia_recal | 13361 | 5015 | 0.3753 | 475 | 0 | 0/0 |
| SriLanka_raw | 3926 | 1321 | 0.3365 | 26 | 0 | 0/0 |
| SriLanka_recal | 3926 | 1321 | 0.3365 | 26 | 0 | 0/0 |

Ordered/unordered row-key SHA-256 and canonical-table SHA-256 recorded in
`logs/paired_audit.json`. Models align exactly; no rows dropped.
