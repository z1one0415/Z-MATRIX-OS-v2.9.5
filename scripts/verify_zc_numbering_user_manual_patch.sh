#!/usr/bin/env bash
set -euo pipefail

echo "═══ ZC Numbering & User Manual Patch Verification ═══"

TARGET="f8796f714740b5e8c76ab53d768888a8de87dfdd"
WORKSPACE="$(cd "$(dirname "$0")/.." && pwd)"
cd "$WORKSPACE"

python3 -m compileall zmatrix tests scripts 2>&1 | tail -1

test -f docs/manuals/ZMATRIX_USER_OPERATION_MANUAL_V1.md || { echo "❌ manual missing"; exit 1; }
test -f docs/architecture/ZC_NUMBERING_MAP_V1.md || { echo "❌ map missing"; exit 1; }
test -f docs/release/ZC_NUMBERING_USER_MANUAL_PATCH_CLOSEOUT.md || { echo "❌ closeout missing"; exit 1; }
test -f docs/upgrade/V40_CONTENT_ASSET_INDEX.md || { echo "❌ asset index missing"; exit 1; }

git rev-list -n 1 v4.0-rc1 | grep -q "$TARGET" && echo "✅ tag target matches $TARGET"

python3 - <<'PY'
from pathlib import Path

manual = Path("docs/manuals/ZMATRIX_USER_OPERATION_MANUAL_V1.md").read_text()
zcmap = Path("docs/architecture/ZC_NUMBERING_MAP_V1.md").read_text()
asset = Path("docs/upgrade/V40_CONTENT_ASSET_INDEX.md").read_text()
closeout = Path("docs/release/ZC_NUMBERING_USER_MANUAL_PATCH_CLOSEOUT.md").read_text()

required_zc = ["ZC00","ZC10","ZC20","ZC30","ZC31","ZC32","ZC35","ZC40","ZC45","ZC50","ZSC"]
for zc in required_zc:
    assert zc in manual, f"manual missing {zc}"
    assert zc in zcmap, f"map missing {zc}"

required_assets = [
    "ZC00_PARSER_SCORER_SPLIT_PROTOCOL_V10",
    "ZC10_RESEARCH_COUNCIL_12_SEATS_SKILL_PACK_V10",
    "ZC20_DATAFORGE_PROPRIETARY_ALT_DATA_EVIDENCE_V10",
    "ZC30_FACTOR_FACTORY_IC_RANKIC_DECILE_PROMOTION_V10",
    "ZC31_MULTI_STRATEGY_SLEEVE_WEIGHT_LIFECYCLE_V10",
    "ZC32_PORTFOLIO_OPTIMIZER_RISK_PARITY_COVARIANCE_V10",
    "ZC35_CATALYST_LIFECYCLE_ENGINE_V10",
    "ZC35_V21_RESEARCH_PROTOTYPE",
    "ZC40_EXECUTION_QUALITY_ROUTE_COMPETITION_MICRO_LITE_V10",
    "ZC45_PROXY_HEDGE_DEFENSIVE_ALLOCATION_V10",
    "ZC50_ACCOUNT_GOVERNANCE_CAPITAL_CURVE_ALPHA_V10",
    "ZSC_AUDIT_EXPORT_PACK_TRACEABILITY_V10",
    "AUTOCASEFORGE_V10",
]
for item in required_assets:
    assert item in asset, f"asset index missing {item}"

assert "V4.0-RC1_TAGGED_RESEARCH_ONLY" in asset
assert "Release tag: v4.0-rc1" in asset
assert "Production status: BLOCKED" in asset
assert "Broker/runtime status: BLOCKED" in asset
assert "Real trade status: BLOCKED" in asset

assert "ZC31_MULTI_STRATEGY_SLEEVE" in asset
assert "DEPRECATED_ALIAS_OF_ZC31" in asset
assert "AUTOCASEFORGE_V10: PLANNED_NOT_IMPLEMENTED" in asset or "PLANNED_NOT_IMPLEMENTED" in asset
assert "ZC35_V21_RESEARCH_PROTOTYPE" in asset

forbidden_tokens = [
    "Production status: READY",
    "RC1 status: APPROVED",
    "Broker/runtime status: READY",
    "Real trade status: READY",
    "ZC35-v2.1 = RC1",
    "AutoCaseForge = IMPLEMENTED",
    "Tag moved: true",
    "Tag retagged: true",
]
for token in forbidden_tokens:
    assert token not in manual + asset + zcmap + closeout, f"Forbidden: {token}"

print("✅ ZC numbering and user manual verification PASS")
PY

echo "═══ ZC Numbering & User Manual Patch PASS ═══"
