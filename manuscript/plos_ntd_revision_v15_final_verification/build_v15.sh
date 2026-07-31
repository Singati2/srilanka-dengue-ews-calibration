#!/usr/bin/env bash
# Fail-fast build for PLOS NTD revision v15 (integrity cleanup). Produces THREE PDFs:
#   1) dengue_ews_v15_internal_author_review.pdf   (line numbers OFF)
#   2) dengue_ews_v15_line_numbered_review.pdf      (continuous line numbers ON)
#   3) dengue_ews_v15_line_numbered_review_grayscale.pdf  (grayscale of #2)
set -euo pipefail
cd "$(dirname "$0")"
TEX="dengue_ews_plos_ntd_v15.tex"
SIDIR="supporting_information"

fail() { echo "FAIL: $1"; exit 1; }

for s in S1_STROBE_checklist_v15 S2_S3_TRIPOD_AI_PROBAST_v15 S4_analysis_plan_chronology_v15 \
         S5_country_model_specification_v15 S6_bootstrap_protocol_v15 S7_srilanka_sensitivity_grid_v15 \
         S8_srilanka_targeted_value_v15 S9_colombia_threshold_horizon_v15 S10_reproducibility_inventory_v15 \
         S11_srilanka_wild_cluster_bootstrap_t_v15 S12_srilanka_wild_bootstrap_method_v15; do
  [ -f "$SIDIR/$s.md" ] || fail "listed SI file absent: $SIDIR/$s.md"
done
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
  [ "${over10:-0}" -eq 0 ] || fail "overfull hbox >= 10pt ($over10)"
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

build "dengue_ews_v15_internal_author_review" ""
build "dengue_ews_v15_line_numbered_review" "\\def\\linenumberedcopy{}"

GRAY="dengue_ews_v15_line_numbered_review_grayscale.pdf"
rm -f "$GRAY"
if command -v gs >/dev/null 2>&1; then
  gs -q -o "$GRAY" -sDEVICE=pdfwrite -sColorConversionStrategy=Gray \
     -dProcessColorModel=/DeviceGray -dOverrideICC -dNOPAUSE -dBATCH \
     "dengue_ews_v15_line_numbered_review.pdf" >/dev/null 2>&1 || fail "grayscale (gs) conversion failed"
elif command -v pdftocairo >/dev/null 2>&1; then
  pdftocairo -pdf -gray "dengue_ews_v15_line_numbered_review.pdf" "$GRAY" >/dev/null 2>&1 || fail "grayscale (pdftocairo) conversion failed"
else
  fail "no grayscale tool (gs or pdftocairo) available"
fi
[ -f "$GRAY" ] || fail "grayscale PDF not produced"
echo "OK $GRAY: pages=$(pdfinfo "$GRAY" 2>/dev/null | awk '/Pages/{print $2}')"

echo "BUILD OK: internal_author_review + line_numbered_review + grayscale"
