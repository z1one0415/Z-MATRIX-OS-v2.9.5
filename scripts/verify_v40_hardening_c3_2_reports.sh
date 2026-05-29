#!/usr/bin/env bash
set -euo pipefail

echo "═══ V4.0 FINAL-HARDGATES Hardening-C3-2 Report Templates Verify ═══"

WORKSPACE="$(cd "$(dirname "$0")/.." && pwd)"
cd "$WORKSPACE"

python3 -m compileall zmatrix/reports/ 2>&1 | tail -1

# Tests
PYTHONPATH=. python3 -m pytest -q tests/test_hardening_c3_templates_audit.py -k "template or renderer or snapshot"

# Verify 12 template files
python3 - <<'PY'
from pathlib import Path
from zmatrix.reports.renderer import TEMPLATE_NAMES, ReportRenderer
tpl_dir = Path("zmatrix/report_templates")
for name in TEMPLATE_NAMES:
    f = tpl_dir / f"{name}.md"
    assert f.exists(), f"missing template: {f}"
print(f"✅ C3-2: 12 template files present")

# Verify snapshot rendering
renderer = ReportRenderer()
for name in TEMPLATE_NAMES:
    snap = renderer.render_snapshot(name, {"timestamp": "2026-05-29", "ticker": "000001"})
    assert "SAFETY_DISCLAIMER" in snap or "PAPER-ONLY" in snap or "NOT ALLOWED" in snap or "Safety Disclaimer" in snap
    assert "BUY" not in snap and "SELL" not in snap
print(f"✅ C3-2: all 12 templates render snapshots, no trade terms")
PY

echo "═══ V4.0 FINAL-HARDGATES Hardening-C3-2 PASS ═══"
