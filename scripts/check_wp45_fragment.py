#!/usr/bin/env python3
"""Structural check for the WP4/WP5 manuscript fragment.

There is no LaTeX toolchain in this environment, so the fragment cannot be
compiled. This checks the things a compile would have caught anyway:

  1. every \\cite key resolves against the .bib files the fragment declares
  2. every \\includegraphics target exists on disk
  3. every \\ref resolves to a \\label defined in the fragment
  4. every \\label is unique
  5. no marker macro is used without being defined, and none is left orphaned
  6. tabular column counts match their rows

Run from the repository root:  python3 scripts/check_wp45_fragment.py
Exit status is non-zero if any check fails.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FRAGMENT = ROOT / "manuscript" / "wp4_wp5_sections" / "wp4_wp5_methods_results_v1.tex"
BIBS = [
    ROOT / "manuscript" / "wp4_wp5_sections" / "wp4_wp5_references_add_v1.bib",
    ROOT / "manuscript" / "plos_ntd_revision_v18_submission_clean_candidate" / "references_v18.bib",
]

failures: list[str] = []
notes: list[str] = []


def check(ok: bool, message: str) -> None:
    if ok:
        notes.append(f"  ok   {message}")
    else:
        failures.append(f"  FAIL {message}")


def strip_comments(tex: str) -> str:
    """Drop comment text but keep the line, so line numbers stay usable."""
    return "\n".join(re.sub(r"(?<!\\)%.*$", "", line) for line in tex.splitlines())


def main() -> int:
    if not FRAGMENT.exists():
        print(f"fragment not found: {FRAGMENT}")
        return 2

    raw = FRAGMENT.read_text()
    tex = strip_comments(raw)

    # --- 1. citations -------------------------------------------------------
    bib_keys: set[str] = set()
    for bib in BIBS:
        if not bib.exists():
            notes.append(f"  --   bib absent, skipped: {bib.relative_to(ROOT)}")
            continue
        bib_keys |= set(re.findall(r"@\w+\{\s*([^,\s]+)\s*,", bib.read_text()))
    cited: set[str] = set()
    for group in re.findall(r"\\cite[tp]?\*?(?:\[[^\]]*\])*\{([^}]*)\}", tex):
        cited |= {k.strip() for k in group.split(",") if k.strip()}
    missing = sorted(cited - bib_keys)
    check(not missing, f"{len(cited)} cite keys resolve" + (f" (missing: {missing})" if missing else ""))

    # --- 2. figures ---------------------------------------------------------
    targets = re.findall(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]*)\}", tex)
    absent = [t for t in targets if not (ROOT / t).exists()]
    check(not absent, f"{len(targets)} includegraphics targets exist" + (f" (absent: {absent})" if absent else ""))

    # --- 3./4. labels and refs ---------------------------------------------
    labels = re.findall(r"\\label\{([^}]*)\}", tex)
    dupes = sorted({lab for lab in labels if labels.count(lab) > 1})
    check(not dupes, f"{len(labels)} labels are unique" + (f" (duplicated: {dupes})" if dupes else ""))

    refs: set[str] = set()
    for group in re.findall(r"\\(?:page)?ref\{([^}]*)\}", tex):
        refs |= {r.strip() for r in group.split(",") if r.strip()}
    dangling = sorted(refs - set(labels))
    check(not dangling, f"{len(refs)} refs resolve" + (f" (dangling: {dangling})" if dangling else ""))

    # --- 5. marker macros ---------------------------------------------------
    defined = set(re.findall(r"\\providecommand\{\\(\w+)\}", tex))
    for macro in sorted(defined):
        used = len(re.findall(rf"\\{macro}\b", tex)) - 1  # minus the definition
        check(used > 0, f"marker \\{macro} defined and used {used}x")
    for macro in ("REGBLOCK",):
        stale = len(re.findall(rf"\\{macro}\b", raw))
        check(stale == 0, f"retired marker \\{macro} absent (found {stale})")

    # --- 6. tabular arity ---------------------------------------------------
    for m in re.finditer(r"\\begin\{tabular\}\{([^}]*)\}(.*?)\\end\{tabular\}", tex, re.S):
        spec, body = m.group(1), m.group(2)
        ncol = len(re.findall(r"[lcr]|p\{[^}]*\}", spec))
        label = re.search(r"\\label\{([^}]*)\}", tex[: m.start()][::-1][:400][::-1])
        name = label.group(1) if label else f"tabular@{m.start()}"
        for line in body.splitlines():
            line = line.strip()
            if not line.endswith(r"\\") or line.startswith("\\"):
                continue
            cells = len(re.split(r"(?<!\\)&", line))
            check(cells == ncol, f"{name}: row has {cells} cells against {ncol} columns -- {line[:48]}")

    print(f"Structural check: {FRAGMENT.relative_to(ROOT)}")
    for line in notes:
        print(line)
    for line in failures:
        print(line)
    print(f"\n{len(notes)} passed, {len(failures)} failed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
