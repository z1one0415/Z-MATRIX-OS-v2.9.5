#!/usr/bin/env bash
# allowlist: forbidden-token-definition
set -euo pipefail
echo "═══ V4.0-0 Platform Hardgate Verification ═══"

# Constitution files
for f in BASELINE_FREEZE_POLICY.md V3520_BASELINE_IMPORT_MANIFEST.md VERSION_CEILING.md PRODUCTION_BLOCK_POLICY.md RESEARCH_MODE_POLICY.md PARAMETER_TRUST_POLICY.md DATA_PIT_POLICY.md ROLE_TAXONOMY_POLICY.md; do
    if [ ! -f "constitution/$f" ]; then echo "❌ Missing constitution/$f"; exit 1; fi
done
echo "  ✅ 8 constitution files"

# Baseline status
if [ ! -f "governance/baseline/v3520_baseline_status.json" ]; then echo "❌ Missing baseline status"; exit 1; fi
echo "  ✅ Baseline status"

# Check baseline values
python3 -c "
import json
b=json.load(open('governance/baseline/v3520_baseline_status.json'))
assert b['baseline_version']=='v3.5.20', 'wrong baseline version'
assert b['baseline_status']=='FROZEN', 'not frozen'
assert b['production']=='BLOCKED', 'production not blocked'
assert b['real_trade']=='BLOCKED', 'real trade not blocked'
assert b['broker_runtime']=='BLOCKED', 'broker not blocked'
assert b['classifier_production_chain']=='FROZEN', 'classifier not frozen'
print('  ✅ Baseline values verified')
"

# Check no production fields
for pattern in 'real_trade_allowed=True' 'broker_order_allowed=True' 'runtime_enabled=True' 'auto_buy_allowed=True' 'production_strategy_modified=True' 'classifier_production_modified=True'; do
    if grep -r "$pattern" constitution/ governance/ --include="*.md" --include="*.json" 2>/dev/null; then
        echo "❌ Found $pattern in constitution/governance"; exit 1
    fi
done
echo "  ✅ No production field violations"

# Acceptance matrix
if [ ! -f "governance/V400_ACCEPTANCE_MATRIX.md" ]; then echo "❌ Missing acceptance matrix"; exit 1; fi
echo "  ✅ Acceptance matrix"

echo "═══ V4.0-0 Platform Hardgate PASS ═══"
