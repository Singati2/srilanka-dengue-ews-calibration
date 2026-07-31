#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
B=dengue_ews_plos_ntd_v4
pdflatex -interaction=nonstopmode -halt-on-error "$B.tex"
bibtex "$B"
pdflatex -interaction=nonstopmode -halt-on-error "$B.tex"
pdflatex -interaction=nonstopmode -halt-on-error "$B.tex"
grep -Eiq "undefined citation|citation.*undefined|There were undefined references" "$B.log" && { echo "GUARD FAIL: undefined cite/ref"; exit 1; } || true
grep -Eiq "error|warning--I didn't find|I couldn't open database" "$B.blg" && { echo "GUARD FAIL: bibtex"; exit 1; } || true
pdftotext "$B.pdf" - | grep -qE '\[\?( \?)*\]' && { echo "GUARD FAIL: literal [?] in PDF"; exit 1; } || true
echo "BUILD OK: $B.pdf"
