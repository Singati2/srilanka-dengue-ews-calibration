#!/usr/bin/env bash
# =====================================================================
# Fail-fast build for the v44 biomath-reframe candidate.
# Builds two PDFs from one source via command-line flags (no file edits):
#   1) revised_manuscript_biomath_internal_review.pdf  (line numbers on)
#   2) revised_manuscript_biomath_grayscale.pdf        (gray color model)
#
# Fail-fast: set -euo pipefail; verify toolchain; -halt-on-error; verify each
# PDF exists and is non-empty. BUILD ONLY: runs no analysis, changes no source.
# Figures (submission_figs/*.pdf) are gitignored and absent; \safeincludegraphics
# renders a labeled placeholder so the candidate still compiles for review.
# =====================================================================
set -euo pipefail

JOB="revised_manuscript_biomath"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$HERE"

if ! command -v pdflatex >/dev/null 2>&1; then
  for d in "$HOME/Library/TinyTeX/bin/universal-darwin" \
           "$HOME/Library/TinyTeX/bin/x86_64-darwin" \
           "$HOME/Library/TinyTeX/bin/aarch64-darwin" "$HOME/bin"; do
    [ -x "$d/pdflatex" ] && export PATH="$d:$PATH" && break
  done
fi
command -v pdflatex >/dev/null 2>&1 || { echo "FATAL: pdflatex not found." >&2; exit 1; }
[ -f "${JOB}.tex" ] || { echo "FATAL: ${JOB}.tex not found in $HERE." >&2; exit 1; }
echo ">> pdflatex: $(command -v pdflatex)"

compile () {  # $1 output jobname  $2 \def flags
  local out="$1"; local flags="${2:-}"
  echo ">> building ${out}.pdf (flags: '${flags}')"
  for pass in 1 2; do
    pdflatex -interaction=nonstopmode -halt-on-error \
      -jobname="${out}" "${flags}\input{${JOB}.tex}" >/dev/null \
      || { echo "FATAL: pdflatex failed on ${out} (pass ${pass}); see ${out}.log." >&2; exit 1; }
  done
  [ -s "${out}.pdf" ] || { echo "FATAL: ${out}.pdf missing/empty." >&2; exit 1; }
  echo "   OK  ${out}.pdf ($(wc -c < "${out}.pdf") bytes)"
}

compile "${JOB}_internal_review" "\def\linenumberedcopy{}"
compile "${JOB}_grayscale"       "\def\grayscalecopy{}\def\linenumberedcopy{}"

rm -f "${JOB}_internal_review".{aux,log,out} "${JOB}_grayscale".{aux,log,out} 2>/dev/null || true
echo ">> DONE: ${JOB}_internal_review.pdf and ${JOB}_grayscale.pdf"
