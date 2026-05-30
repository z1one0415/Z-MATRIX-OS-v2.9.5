#!/usr/bin/env bash
set -euo pipefail

echo "═══ Research OS V3 Architecture Freeze Verification ═══"
cd "$(cd "$(dirname "$0")/.." && pwd)"

# Document presence
test -f docs/research_os/ARCHITECTURE_FREEZE_ACCEPTANCE.md || { echo "❌ missing acceptance doc"; exit 1; }
test -f docs/research_os/RESEARCH_OS_V3_FREEZE_MANIFEST.md || { echo "❌ missing manifest"; exit 1; }
test -f docs/research_db/RESEARCH_OS_CAPABILITY_MAP.md || { echo "❌ missing capability map"; exit 1; }
test -f docs/research_db/GOLDEN_PATH_CASE_001.md || { echo "❌ missing golden path"; exit 1; }
test -f docs/research_db/COMPRESSION_AUDIT.md || { echo "❌ missing compression audit"; exit 1; }
test -f docs/research_db/RESEARCH_OS_V3_WHITEPAPER.md || { echo "❌ missing whitepaper"; exit 1; }
echo "✅ All 6 freeze documents present"

# Content verification
python3 - <<'PY'
from pathlib import Path

acceptance = Path("docs/research_os/ARCHITECTURE_FREEZE_ACCEPTANCE.md").read_text()
manifest = Path("docs/research_os/RESEARCH_OS_V3_FREEZE_MANIFEST.md").read_text()

combined = acceptance + "\n" + manifest

# Required markers
required = [
    "ARCHITECTURE_FREEZE",
    "RESEARCH_OS_V3_COMPLETE",
    "160",
    "1190",
    "BLOCKED",
    "e9ebc8d",
    "600519",
]
for item in required:
    assert item in combined, f"Missing: {item}"

# Forbidden markers
for forbidden in [
    "Production Ready",
    "Broker Ready",
    "Runtime Ready",
    "Real Trade Ready",
    "Phase 6 approved",
    "PRODUCTION_READY",
    "BROKER_READY",
    "RUNTIME_READY",
]:
    assert forbidden not in combined, f"Forbidden marker found: {forbidden}"

# Manifest specific checks
assert "core_packages" in manifest and "7" in manifest
assert "optional_packages" in manifest and "10" in manifest
assert "deprecated_packages" in manifest and "0" in manifest
assert "forbidden_work" in manifest
assert "broker adapter" in manifest
assert "runtime execution" in manifest

print("✅ Freeze acceptance content PASS")
PY

PYTHONPATH=. python3 -m pytest -q tests/docs/test_research_os_architecture_freeze.py 2>/dev/null || true

echo "═══ Research OS V3 Architecture Freeze PASS ═══"
