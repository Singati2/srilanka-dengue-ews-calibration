#!/usr/bin/env bash
# Fail-fast build for v18 (submission-clean candidate). The submission metadata gate has
# FAILED (submission_metadata_gate_v18.md), so NO submission-ready PDF is produced. Two PDFs:
#   1) dengue_ews_v18_internal_author_completion.pdf         (internal notice: unresolved metadata)
#   2) dengue_ews_v18_scientifically_clean_not_submission_ready.pdf (discreet not-ready notice)
# Both build with line numbers OFF (author reading-copy preference); the eventual PLOS
# submission build should enable \linenumberedcopy once the gate passes.
set -euo pipefail
cd "$(dirname "$0")"
TEX="dengue_ews_plos_ntd_v18.tex"
SIDIR="supporting_information"
fail() { echo "FAIL: $1"; exit 1; }

for s in S1_STROBE_checklist_v18 S2_S3_TRIPOD_AI_PROBAST_v18 S4_analysis_plan_chronology_v18 \
         S5_country_model_specification_v18 S6_bootstrap_protocol_v18 S7_srilanka_sensitivity_grid_v18 \
         S8_srilanka_targeted_value_v18 S9_colombia_threshold_horizon_v18 S10_reproducibility_inventory_v18 \
         S11_srilanka_wild_cluster_bootstrap_t_v18 S12_srilanka_wild_bootstrap_method_v18; do
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
  over10=$(grep "Overfull \\hbox" "$log" | grep -oE "\(([0-9]+)\." | grep -oE "[0-9]+" | awk '$1>=10' | wc -l || true)
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
  local nbib; nbib=$(grep -c '^\\bibitem' "$TEX" || true)
  [ "$nbib" -ge 30 ] || fail "bibliography too small ($nbib)"
  echo "OK $job.pdf: pages=$(pdfinfo "$job.pdf" 2>/dev/null | awk '/Pages/{print $2}') bibitems=$nbib overfull=$(grep -c 'Overfull \\hbox' "$job.log" || true) underfull=$(grep -c 'Underfull \\hbox' "$job.log" || true)"
}

# 1) internal author-completion copy
build "dengue_ews_v18_internal_author_completion" "\\def\\internalcompletion{}"
# 2) scientifically-cleaned, not-submission-ready copy (default notice)
build "dengue_ews_v18_scientifically_clean_not_submission_ready" ""

echo "BUILD OK: internal_author_completion + scientifically_clean_not_submission_ready (no submission-ready PDF; gate failed)"
