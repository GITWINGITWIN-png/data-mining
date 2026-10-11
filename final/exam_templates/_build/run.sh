#!/usr/bin/env bash
# usage: bash run.sh t01 t02 ...   → build + execute each notebook (dm-exam kernel), print errors
set -e
cd "$(dirname "$0")"
PY="$(cd ../.. && pwd)/.venv/bin/python"
for t in "$@"; do
  out=$("$PY" "$t.py" 2>/dev/null | sed -n 's/^wrote \.\.\/\(.*\.ipynb\).*/\1/p')
  echo "== $t → $out"
  (cd .. && "$PY" -m jupyter nbconvert --to notebook --execute --inplace \
      --ExecutePreprocessor.kernel_name=dm-exam --ExecutePreprocessor.timeout=900 "$out" 2>&1 | grep -v -E 'TCP without|Converting' || true)
done
rm -f ../t0*_*.csv ../t1*_*.csv
"$PY" make_cellmap.py
