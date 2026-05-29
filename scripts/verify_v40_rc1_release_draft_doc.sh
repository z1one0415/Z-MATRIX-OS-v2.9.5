#!/usr/bin/env bash
set -euo pipefail

echo "═══ V4.0-RC1 GitHub Release Draft Doc Verification ═══"
cd "$(cd "$(dirname "$0")/.." && pwd)"

test -f docs/release/V4_0_RC1_GITHUB_RELEASE_DRAFT.md

python3 - <<'PY'
from pathlib import Path
text = Path("docs/release/V4_0_RC1_GITHUB_RELEASE_DRAFT.md").read_text()
required = [
    "Research-only Release Candidate",
    "not production-ready",
    "does not enable broker runtime",
    "does not allow real trade execution",
    "Paper-only: TRUE",
    "Human review required: TRUE",
    "Production: BLOCKED",
    "Broker/runtime: BLOCKED",
    "Real trade: BLOCKED",
    "f8796f714740b5e8c76ab53d768888a8de87dfdd",
    "26629922144",
    "POST_RC1_INTEGRITY_PASS",
]
for item in required:
    assert item in text, f"Missing: {item}"
for forbidden in ["Production: READY","Broker/runtime: READY","Real trade: READY","production_allowed=True","broker_order_allowed=True","real_trade_allowed=True","runtime_enabled=True","Autonomous trading ready"]:
    assert forbidden not in text, f"Forbidden: {forbidden}"
print("✅ V4.0-RC1 release draft doc PASS")
PY
echo "═══ V4.0-RC1 Release Draft Doc PASS ═══"
