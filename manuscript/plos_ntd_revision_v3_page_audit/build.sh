#!/usr/bin/env bash
# Fail-fast v3 build. No bibtex error suppression.
set -euo pipefail
cd "$(dirname "$0")"
B=dengue_ews_plos_ntd_v3
pdflatex -interaction=nonstopmode -halt-on-error "$B.tex"
bibtex "$B"
pdflatex -interaction=nonstopmode -halt-on-error "$B.tex"
pdflatex -interaction=nonstopmode -halt-on-error "$B.tex"
# guards
grep -Eiq "undefined citation|citation.*undefined|There were undefined references" "$B.log" && { echo "GUARD FAIL: undefined citation/reference"; exit 1; } || true
grep -Eiq "error|warning--I didn't find|I couldn't open database" "$B.blg" && { echo "GUARD FAIL: bibtex error"; exit 1; } || true
echo "BUILD OK: $B.pdf"
