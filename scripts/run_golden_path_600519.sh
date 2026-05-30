#!/usr/bin/env bash
set -euo pipefail

echo "═══ Research OS V3 — Golden Path: 贵州茅台 (600519) ═══"
cd "$(cd "$(dirname "$0")/.." && pwd)"

MODE="run"
if [[ "${1:-}" == "--dry-run" ]]; then
    MODE="dry-run"
    echo "Mode: DRY RUN (no output files)"
fi

python3 -m compileall zmatrix/research_os/ 2>&1 | tail -1

PYTHONPATH=. python3 zmatrix/research_os/golden_path_runner.py ${1:-}

if [ "$MODE" != "dry-run" ]; then
    echo ""
    echo "═══ Output ═══"
    for f in runtime_reports/golden_path/golden_path_600519.json runtime_reports/golden_path/golden_path_600519.md golden_path_human_report.md; do
        if [ -f "$f" ]; then
            echo "✅ $f ($(wc -c < "$f") bytes)"
        fi
    done
fi

echo ""
echo "═══ Golden Path PASS ═══"
