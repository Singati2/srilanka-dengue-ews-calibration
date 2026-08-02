#!/usr/bin/env bash
# Fail-fast build for PLOS NTD revision v5.
# References are an inline Vancouver thebibliography (no Vancouver .bst installed),
# so the build does not depend on BibTeX; guards still verify the bibliography is
# non-empty and that no citation/reference is unresolved.
set -euo pipefail

BASE="dengue_ews_plos_ntd_v6"
TEX="$BASE.tex"
LOG="$BASE.log"

cd "$(dirname "$0")"

# Clean prior aux artifacts for a clean-directory compile.
rm -f "$BASE.aux" "$BASE.out" "$BASE.toc" "$LOG" "$BASE.pdf"

run() { pdflatex -interaction=nonstopmode -halt-on-error "$TEX" >/dev/null 2>&1 || {
          echo "FAIL: pdflatex returned an error (see $LOG)"; tail -n 40 "$LOG"; exit 1; }; }

run   # pass 1 (writes .aux with bibitem labels)
run   # pass 2 (resolves \cite and \ref)
run   # pass 3 (stabilizes line numbers / page refs)

fail() { echo "FAIL: $1"; exit 1; }

grep -q "Undefined control sequence" "$LOG" && fail "undefined control sequence"
grep -qi "LaTeX Error" "$LOG" && fail "LaTeX error present"
grep -q "Citation .* undefined" "$LOG" && fail "undefined citation"
grep -q "Reference .* undefined" "$LOG" && fail "undefined reference"
grep -q "There were undefined references" "$LOG" && fail "undefined references"
# Literal [?] in the rendered PDF (broken cite/ref)
pdftotext "$BASE.pdf" - 2>/dev/null | grep -q "\[?\]" && fail "literal [?] in PDF"
# Bibliography must be present and non-empty
grep -q "begin{thebibliography}" "$TEX" || fail "no bibliography environment"
NBIB=$(grep -c "^\\\\bibitem" "$TEX" || true)
[ "$NBIB" -ge 30 ] || fail "bibliography too small / empty ($NBIB entries)"
# Line numbers: enabled for submission, intentionally disabled in this review copy.
if grep -qE "^\\\\linenumbers" "$TEX"; then
  echo "note: continuous line numbers ENABLED"
else
  echo "note: line numbers disabled for review copy (re-enable \\linenumbers before submission)"
fi
# Unapproved bare placeholders outside the declarations block
if pdftotext "$BASE.pdf" - 2>/dev/null | grep -Eq "TODO|FIXME|XXX|\\[TO CONFIRM"; then
  fail "unapproved placeholder token in PDF"
fi

PAGES=$(pdfinfo "$BASE.pdf" 2>/dev/null | awk '/Pages/{print $2}')
OVERFULL=$(grep -c "Overfull \\\\hbox" "$LOG" || true)
UNDERFULL=$(grep -c "Underfull \\\\hbox" "$LOG" || true)
OVER10=$(grep "Overfull \\\\hbox" "$LOG" | grep -oE "\(([0-9]+)\." | grep -oE "[0-9]+" | awk '$1>=10' | wc -l || true)

echo "BUILD OK: $BASE.pdf"
echo "pages=$PAGES bibitems=$NBIB overfull=$OVERFULL (>=10pt: $OVER10) underfull=$UNDERFULL"
[ "${OVER10:-0}" -eq 0 ] || fail "overfull hbox >= 10pt present ($OVER10)"
