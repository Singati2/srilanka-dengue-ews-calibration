#!/usr/bin/env bash
# Fail-fast build for the Path B validity-corrected candidate. Recomputes nothing scientific.
set -e
J=paper1_validity_corrected
pdflatex -interaction=nonstopmode -halt-on-error $J.tex >b1.log 2>&1
bibtex $J >bib.log 2>&1 || true
pdflatex -interaction=nonstopmode -halt-on-error $J.tex >b2.log 2>&1
pdflatex -interaction=nonstopmode -halt-on-error $J.tex >b3.log 2>&1
echo "MAIN: $(grep -E 'Output written' b3.log)"
# grayscale
if command -v gs >/dev/null; then
  gs -sDEVICE=pdfwrite -sProcessColorModel=DeviceGray -sColorConversionStrategy=Gray \
     -dOverrideICC -o ${J}_grayscale.pdf $J.pdf >gs.log 2>&1 && echo "GRAYSCALE: ok"
else echo "GRAYSCALE: gs not available"; fi
