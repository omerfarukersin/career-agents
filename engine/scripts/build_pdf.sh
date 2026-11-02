#!/usr/bin/env bash
# Compile a .tex file to PDF next to it and report the page count.
# Usage: engine/scripts/build_pdf.sh path/to/file.tex [max_pages]
# Exits 2 if the PDF is longer than max_pages (default: 1 for cover letters, 2 for anything else).
set -euo pipefail
tex="$1"
dir="$(cd "$(dirname "$tex")" && pwd)"
base="$(basename "$tex" .tex)"
case "$base" in *letter*) default_max=1 ;; *) default_max=2 ;; esac
max="${2:-$default_max}"
cd "$dir"
if ! pdflatex -interaction=nonstopmode -halt-on-error "$base.tex" > "$base.buildlog" 2>&1; then
  echo "BUILD FAILED: last lines of log:"
  grep -E '^!|^l\.[0-9]+' "$base.buildlog" | head -20 || true
  exit 1
fi
pages="$(grep -oE 'Output written on .* \(([0-9]+) page' "$base.buildlog" | grep -oE '[0-9]+ page' | grep -oE '[0-9]+' || echo 0)"
grep -q 'Overfull \\hbox' "$base.buildlog" && echo "WARNING: overfull lines (text running into margin); shorten them."
rm -f "$base.aux" "$base.log" "$base.out" "$base.buildlog"
if [ "$pages" -gt "$max" ]; then
  echo "TOO LONG: $dir/$base.pdf has $pages page(s), limit $max. Cut content; don't shrink fonts."
  exit 2
fi
echo "OK: $dir/$base.pdf ($pages page(s))"
