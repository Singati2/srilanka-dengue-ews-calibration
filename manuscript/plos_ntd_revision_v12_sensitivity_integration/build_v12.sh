#!/usr/bin/env bash
# Fail-fast build for PLOS NTD revision v12 (sensitivity integration). Produces THREE PDFs:
#   1) dengue_ews_v12_internal_author_review.pdf   (line numbers OFF; author standing preference)
#   2) dengue_ews_v12_line_numbered_review.pdf      (continuous line numbers ON)
#   3) dengue_ews_v12_line_numbered_review_grayscale.pdf  (grayscale of #2)
# References are an inline Vancouver thebibliography (no BibTeX dependency); guards still verify
# the bibliography is non-empty and that no citation/reference is unresolved.
set -euo pipefail
cd "$(dirname "$0")"
TEX="dengue_ews_plos_ntd_v12.tex"
SIDIR="supporting_information"

fail() { echo "FAIL: $1"; exit 1; }

# --- SI-file-existence guard: every S-item the manuscript lists must exist as a real file ---
for s in S1_STROBE_checklist_v12 S2_S3_TRIPOD_AI_PROBAST_v12 S4_analysis_plan_chronology_v12 \
         S5_country_model_specification_v12 S6_bootstrap_protocol_v12 S7_srilanka_sensitivity_grid_v12 \
         S8_srilanka_targeted_value_v12 S9_colombia_threshold_horizon_v12 S10_reproducibility_inventory_v12 \
         S11_srilanka_wild_cluster_bootstrap_t_v12 S12_srilanka_wild_bootstrap_method_v12; do
  [ -f "$SIDIR/$s.md" ] || fail "listed SI file absent: $SIDIR/$s.md"
done
# machine-readable full-precision results file must exist (cited by S11)
[ -f "$SIDIR/S11_srilanka_wild_cluster_bootstrap_t_results.csv" ] || fail "machine-readable S11 results file absent"

check_log() {
  local log="$1"
  grep -q "Undefined control sequence" "$log" && fail "undefined control sequence"
  grep -qi "LaTeX Error" "$log" && fail "LaTeX error"
  grep -q "Citation .* undefined" "$log" && fail "undefined citation"
  grep -q "Reference .* undefined" "$log" && fail "undefined reference"
  grep -q "There were undefined references" "$log" && fail "undefined references"
  local over10
  over10=$(grep "Overfull \\\\hbox" "$log" | grep -oE "\(([0-9]+)\." | grep -oE "[0-9]+" | awk '$1>=10' | wc -l || true)
  [ "${over10:-0}" -eq 0 ] || fail "overfull hbox >= 10pt ($over10) — table/figure may exceed margin"
}

build() {  # $1=jobname  $2=preamble-def
  local job="$1" def="$2"
  rm -f "$job.aux" "$job.out" "$job.log" "$job.pdf"
  for i in 1 2 3; do
    pdflatex -interaction=nonstopmode -halt-on-error -jobname="$job" "$def\\input{$TEX}" >/dev/null 2>&1 \
      || { echo "--- $job pass $i failed ---"; tail -n 30 "$job.log"; exit 1; }
  done
  check_log "$job.log"
  pdftotext "$job.pdf" - 2>/dev/null | grep -q "\[?\]" && fail "literal [?] in $job.pdf"
  grep -q "begin{thebibliography}" "$TEX" || fail "no bibliography"
  local nbib; nbib=$(grep -c "^\\\\bibitem" "$TEX" || true)
  [ "$nbib" -ge 30 ] || fail "bibliography too small ($nbib)"
  echo "OK $job.pdf: pages=$(pdfinfo "$job.pdf" 2>/dev/null | awk '/Pages/{print $2}') bibitems=$nbib overfull=$(grep -c 'Overfull \\\\hbox' "$job.log" || true) underfull=$(grep -c 'Underfull \\\\hbox' "$job.log" || true)"
}

# 1) internal author review (no line numbers)
build "dengue_ews_v12_internal_author_review" ""
# 2) line-numbered review
build "dengue_ews_v12_line_numbered_review" "\\def\\linenumberedcopy{}"

# 3) grayscale of the line-numbered review
GRAY="dengue_ews_v12_line_numbered_review_grayscale.pdf"
rm -f "$GRAY"
if command -v gs >/dev/null 2>&1; then
  gs -q -o "$GRAY" -sDEVICE=pdfwrite -sColorConversionStrategy=Gray \
     -dProcessColorModel=/DeviceGray -dOverrideICC -dNOPAUSE -dBATCH \
     "dengue_ews_v12_line_numbered_review.pdf" >/dev/null 2>&1 || fail "grayscale (gs) conversion failed"
elif command -v pdftocairo >/dev/null 2>&1; then
  pdftocairo -pdf -gray "dengue_ews_v12_line_numbered_review.pdf" "$GRAY" >/dev/null 2>&1 || fail "grayscale (pdftocairo) conversion failed"
else
  fail "no grayscale tool (gs or pdftocairo) available"
fi
[ -f "$GRAY" ] || fail "grayscale PDF not produced"
echo "OK $GRAY: pages=$(pdfinfo "$GRAY" 2>/dev/null | awk '/Pages/{print $2}')"

echo "BUILD OK: internal_author_review + line_numbered_review + grayscale"
