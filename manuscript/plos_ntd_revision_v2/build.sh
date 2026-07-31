#!/usr/bin/env bash
# Build the PLOS NTD revision PDF (local only; no commit/push).
# Usage: bash build.sh
set -euo pipefail
cd "$(dirname "$0")"
B=dengue_ews_plos_ntd_v2
pdflatex -interaction=nonstopmode "$B.tex"
bibtex "$B" || true
pdflatex -interaction=nonstopmode "$B.tex"
pdflatex -interaction=nonstopmode "$B.tex"
echo "Built $B.pdf"
# Open placeholders report:
echo "Open author-confirmation placeholders:"
grep -c 'AUTHOR CONFIRMATION REQUIRED' "$B.tex" || true
