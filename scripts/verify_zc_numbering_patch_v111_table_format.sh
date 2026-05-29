#!/usr/bin/env bash
set -euo pipefail

echo "═══ ZC Numbering Patch v1.1.1 Table Format Verification ═══"

python3 - <<'PY'
from pathlib import Path

asset = Path("docs/upgrade/V40_CONTENT_ASSET_INDEX.md").read_text(encoding="utf-8")
closeout = Path("docs/release/ZC_NUMBERING_USER_MANUAL_PATCH_CLOSEOUT.md").read_text(encoding="utf-8")

assert "| Asset ID | Name | Batch | Status |" in asset
assert "|---|---|---|---|" in asset
assert "|---|---:|---|" not in asset

required_status = [
    "Current status: V4.0-RC1_TAGGED_RESEARCH_ONLY",
    "Production status: BLOCKED",
    "Broker/runtime status: BLOCKED",
    "Real trade status: BLOCKED",
    "ZC31_MULTI_STRATEGY_SLEEVE",
    "DEPRECATED_ALIAS_OF_ZC31",
    "AUTOCASEFORGE_V10",
    "PLANNED_NOT_IMPLEMENTED",
    "ZC35_V21_RESEARCH_PROTOTYPE",
    "RESEARCH_PROTOTYPE_EXCLUDED_FROM_RC1",
]
for item in required_status:
    assert item in asset, f"Missing: {item}"

assert "Patch v1.1.1 — Markdown Table Format Fix" in closeout
assert "No business logic changed." in closeout
assert "No tag moved." in closeout

for forbidden in [
    "Production status: READY",
    "Broker/runtime status: READY",
    "Real trade status: READY",
    "Tag moved: true",
    "Tag retagged: true",
]:
    assert forbidden not in asset + closeout, f"Forbidden: {forbidden}"

print("✅ ZC Numbering Patch v1.1.1 table format verification PASS")
PY

echo "═══ ZC Numbering Patch v1.1.1 PASS ═══"
