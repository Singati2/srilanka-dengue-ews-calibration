# Checksum-ledger reconciliation (v10)

The v9 run reported two numbers for the **same** file (`v8_state_at_v9_start.sha256`): "ledger lines: 55" (from `wc -l`) and "47 entries / 47/47 OK" (from `sha256sum -c`). These are not in conflict; they count different things.

| Quantity | Value | How counted |
|---|---|---|
| Total physical lines | 55 | `wc -l` |
| Comment/header lines (start with `#` or `##`) | 8 | `grep -c '^#'` |
| Valid checksum records (`<64-hex>␠␠<path>`) | 47 | `grep -cE '^[0-9a-f]{64}  '` |
| Blank lines | 0 | `grep -cE '^[[:space:]]*$'` |
| Files checked (== records) | 47 | one record per file |
| Passing (`: OK`) | 47 | `sha256sum -c` |
| Failing (`: FAILED`) | 0 | `sha256sum -c` |
| Duplicate checksum paths | 0 | `awk '{print $2}' | sort | uniq -d` |
| Missing/malformed records | 0 | every non-`#` line matched the 64-hex record pattern |

**Conclusion:** 55 = 8 comment/header lines + 47 checksum records. `sha256sum -c` ignores the 8 `#` lines and validates the 47 records, all of which passed. Every expected record is accounted for; there are no duplicates, malformed, or missing records. The "55 vs 47" difference is purely line-basis (all lines) versus record-basis (checksum entries).

(The v10 ledger `v9_state_at_v10_start.sha256` is reported on the same record basis to avoid the ambiguity.)
