#!/usr/bin/env bash
set -euo pipefail

echo "═══ Post-RC1 Release Integrity Full Verification ═══"
WORKSPACE="$(cd "$(dirname "$0")/.." && pwd)"
cd "$WORKSPACE"

python3 -m compileall zmatrix tests scripts 2>&1 | tail -1

bash scripts/verify_post_rc1_tag_integrity.sh
bash scripts/verify_post_rc1_release_docs_consistency.sh
bash scripts/verify_post_rc1_safety_gates.sh

PYTHONPATH=. python3 -m pytest -q tests/release_integrity/

python3 - <<'PY'
from pathlib import Path

report = Path("docs/release_integrity/POST_RC1_RELEASE_INTEGRITY_AUDIT_REPORT.md")
score = Path("docs/release_integrity/POST_RC1_INTEGRITY_SCORECARD.md")
remote = Path("docs/release_integrity/POST_RC1_REMOTE_RELEASE_STATE.md")

assert report.exists(), "missing report"
assert score.exists(), "missing scorecard"
assert remote.exists(), "missing remote state"

text = report.read_text(encoding="utf-8") + "\n" + score.read_text(encoding="utf-8") + "\n" + remote.read_text(encoding="utf-8")

assert "v4.0-rc1" in text
assert "f8796f714740b5e8c76ab53d768888a8de87dfdd" in text
assert "BLOCKED" in text
assert "FALSE" in text or "false" in text

for forbidden in [
    "Production: READY",
    "Broker/runtime: READY",
    "Real trade: READY",
    "production_allowed=True",
    "broker_order_allowed=True",
    "real_trade_allowed=True",
    "runtime_enabled=True",
]:
    assert forbidden not in text, f"Forbidden: {forbidden}"

print("✅ Post-RC1 integrity full verification PASS")
PY

echo "═══ Post-RC1 Release Integrity PASS ═══"
