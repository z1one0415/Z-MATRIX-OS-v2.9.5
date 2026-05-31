#!/usr/bin/env bash
set -euo pipefail
cd "$(cd "$(dirname "$0")/../.." && pwd)"
echo "═══ Core 12 Ticker-Specific Golden Path Run ═══"
mkdir -p runtime_reports/cases/core_12
PYTHONPATH=. python3 -c "
import shutil, os
for root, dirs, files in os.walk('.'):
    for d in dirs:
        if d == '__pycache__' and ('zmatrix' in root or 'scripts' in root):
            shutil.rmtree(os.path.join(root, d), ignore_errors=True)
"
PYTHONPATH=. python3 scripts/cases/run_core_12_batch.py
PYTHONPATH=. python3 scripts/cases/summarize_core_12_run.py
echo ""
echo "═══ Core 12 Complete ═══"
