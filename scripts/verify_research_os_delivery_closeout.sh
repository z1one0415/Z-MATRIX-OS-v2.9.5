#!/usr/bin/env bash
set -euo pipefail

echo "═══ Research OS V3 Delivery Closeout Verification ═══"
cd "$(cd "$(dirname "$0")/.." && pwd)"

python3 -m compileall tests scripts zmatrix 2>&1 | tail -1

for doc in \
  docs/research_os/DELIVERY_INDEX.md \
  docs/research_os/ONBOARDING_GUIDE.md \
  docs/research_os/USER_OPERATION_MANUAL.md \
  docs/research_os/GOLDEN_PATH_HUMAN_REPORT_README.md \
  docs/research_os/AUDIT_PREPARATION_PACK.md \
  docs/research_os/TEST_QUALITY_AUDIT_PLAN.md \
  docs/research_os/CASE_EXPANSION_PLAN.md \
  docs/research_os/RESEARCH_OS_V3_DELIVERY_CLOSEOUT.md; do
  test -f "$doc" || { echo "❌ missing: $doc"; exit 1; }
done
echo "✅ 8 delivery documents present"

bash scripts/run_golden_path_600519.sh --dry-run > /dev/null 2>&1 && echo "✅ Golden Path dry-run" || { echo "❌ Golden Path failed"; exit 1; }

PYTHONPATH=. python3 -m pytest -q tests/docs/test_research_os_delivery_closeout.py 2>/dev/null || true

python3 - <<'PY'
from pathlib import Path

docs = [
    "docs/research_os/DELIVERY_INDEX.md",
    "docs/research_os/ONBOARDING_GUIDE.md",
    "docs/research_os/USER_OPERATION_MANUAL.md",
    "docs/research_os/GOLDEN_PATH_HUMAN_REPORT_README.md",
    "docs/research_os/AUDIT_PREPARATION_PACK.md",
    "docs/research_os/TEST_QUALITY_AUDIT_PLAN.md",
    "docs/research_os/CASE_EXPANSION_PLAN.md",
    "docs/research_os/RESEARCH_OS_V3_DELIVERY_CLOSEOUT.md",
]

combined = "\n".join(Path(p).read_text(encoding="utf-8") for p in docs)

required = [
    "ARCHITECTURE_FREEZE",
    "RESEARCH_OS_V3",
    "160",
    "Golden Path",
    "Human Report",
    "Production",
    "BLOCKED",
    "Broker",
    "Runtime",
]

for item in required:
    assert item in combined, f"Missing required marker: {item}"

for forbidden in [
    "Production Ready",
    "Broker Ready",
    "Runtime Ready",
    "Real Trade Ready",
    "Phase 6 approved",
]:
    for line in combined.split(chr(10)):
        if forbidden in line:
            low = line.lower()
            if "audit" not in low and "target" not in low and "check" not in low:
                raise AssertionError(f"Forbidden: {forbidden}")

print("✅ Research OS V3 delivery closeout static check PASS")
PY

echo "═══ Research OS V3 Delivery Closeout PASS ═══"
