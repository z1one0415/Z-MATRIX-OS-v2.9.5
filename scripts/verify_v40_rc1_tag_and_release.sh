#!/usr/bin/env bash
set -euo pipefail

echo "═══ V4.0-RC1 Tag & Release Verification ═══"

WORKSPACE="$(cd "$(dirname "$0")/.." && pwd)"
cd "$WORKSPACE"

TARGET="f8796f714740b5e8c76ab53d768888a8de87dfdd"

# Verify tag
echo "[1] Tag verification..."
git rev-list -n 1 v4.0-rc1 | grep -q "$TARGET" && echo "  ✅ tag points to $TARGET"
git ls-remote --tags origin v4.0-rc1 | grep -q "v4.0-rc1" && echo "  ✅ tag exists on remote"

# Verify docs
echo "[2] Document verification..."
test -f docs/release/V4_0_RC1_MANIFEST.md && echo "  ✅ manifest"
test -f docs/release/V4_0_RC1_RELEASE_NOTE.md && echo "  ✅ release note"
test -f docs/rc1_audit/RC1_CLOUD_EVIDENCE_LOCK.json && echo "  ✅ evidence lock"

# Deep check
echo "[3] Content integrity..."
python3 /dev/stdin << 'ENDSCRIPT'
import json
from pathlib import Path

manifest = Path("docs/release/V4_0_RC1_MANIFEST.md").read_text(encoding="utf-8")
note = Path("docs/release/V4_0_RC1_RELEASE_NOTE.md").read_text(encoding="utf-8")
audit = Path("docs/rc1_audit/RC1_READINESS_AUDIT_REPORT.md").read_text(encoding="utf-8")
lock = json.loads(Path("docs/rc1_audit/RC1_CLOUD_EVIDENCE_LOCK.json").read_text(encoding="utf-8"))

combined = (manifest + "\n" + note + "\n" + audit).lower()

required = ["v4.0-rc1", "research-only", "not production-ready", "blocked", "paper-only", "human review"]
for item in required:
    assert item in combined, f"Missing: {item}"

forbidden = ["production: ready", "broker/runtime: ready", "real trade: ready", "autonomous trading ready",
             "production_allowed=true", "broker_order_allowed=true", "real_trade_allowed=true", "runtime_enabled=true"]
for item in forbidden:
    assert item not in combined, f"Forbidden: {item}"

assert lock["rc1_tag_created"] is True
assert lock["rc1_tag"] == "v4.0-rc1"
assert lock["rc1_tag_target"] == "f8796f714740b5e8c76ab53d768888a8de87dfdd"
assert lock["production_status"] == "BLOCKED"
assert lock["broker_runtime_status"] == "BLOCKED"
assert lock["real_trade_status"] == "BLOCKED"

print("✅ V4.0-RC1 tag/release docs PASS")
ENDSCRIPT

echo "═══ V4.0-RC1 Tag & Release PASS ═══"
