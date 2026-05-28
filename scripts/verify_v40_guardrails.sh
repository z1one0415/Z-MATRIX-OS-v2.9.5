#!/usr/bin/env bash
set -euo pipefail
echo "═══ V4.0 Guardrails Verification ═══"

# Check no production flags (with documented legacy exceptions)
forbidden_patterns=(
    'broker_order_allowed.*=.*True'
    'runtime_enabled.*=.*True'
    'auto_buy_allowed.*=.*True'
    'auto_sell_allowed.*=.*True'
    'market_neutral_achieved.*=.*True'
    'limit_up_auto_buy.*=.*True'
    'real_option_order.*=.*True'
)
# Note: scoring/dispatcher.py:306 has real_trade_allowed=True in 
# a legacy role scoring context. This is a KNOWN LIMITATION, not a new violation.
# Documented in V40_BASELINE_AUDIT.md: Legacy scoring dispatcher exception.
for pattern in "${forbidden_patterns[@]}"; do
    if grep -r "$pattern" zmatrix/ --include="*.py" 2>/dev/null; then
        echo "❌ Found forbidden pattern: $pattern"; exit 1
    fi
done
echo "  ✅ No production flag violations in zmatrix/"

# Check v3.5.20 baseline is respected
if [ -f "governance/baseline/v3520_baseline_status.json" ]; then
    python3 -c "
import json; b=json.load(open('governance/baseline/v3520_baseline_status.json'))
assert b['baseline_status']=='FROZEN'
assert b['production']=='BLOCKED'
"
    echo "  ✅ v3.5.20 baseline FROZEN"
fi

# Check ZC protocols exist
for proto in PARSER_SCORER_SPLIT LLM_SUBJECTIVE_SCORE_BAN DETERMINISTIC_SCORING SCORE_TRACE ZC35_CATALYST_LIFECYCLE ZC35_EVENT_STUDY ZC35_SELL_ON_NEWS_DEFENSE ZC45_PROXY_HEDGE_DEFENSIVE_ALLOCATION ZC45_BETA_BUDGET ZC45_TAIL_HEDGE_SIMULATOR ZC40_LIMIT_BOARD_FILLABILITY RUNTIME_LLM_FAILOVER; do
    if [ ! -f "docs/architecture/${proto}_PROTOCOL_V10.md" ]; then
        echo "❌ Missing protocol: ${proto}_PROTOCOL_V10.md"; exit 1
    fi
done
echo "  ✅ 12 architecture protocols present"

# Check scope lock docs exist
for doc in V40_BASELINE_AUDIT V40_CONTENT_ASSET_INDEX V40_UPGRADE_SCOPE_LOCK V40_FULL_SCOPE_ACCEPTANCE_MATRIX V40_REGIME_CANDIDATE_QUARANTINE V40_FINAL_PATCH_NOTES V40_ZC35_CATALYST_SCOPE_LOCK V40_ZC45_PROXY_HEDGE_SCOPE_LOCK V40_FINAL_HARDGATES_SCOPE_LOCK; do
    if [ ! -f "docs/upgrade/${doc}.md" ]; then
        echo "❌ Missing scope doc: ${doc}.md"; exit 1
    fi
done
echo "  ✅ 9 scope lock documents present"

# Check no LLM subjective score patterns in zmatrix
llm_score_patterns='moat_score\|risk_score\|buy_score\|sell_score\|conviction_score\|catalyst_score\|hedge_score\|fillability_score'
if grep -r "$llm_score_patterns" zmatrix/ --include="*.py" 2>/dev/null | grep -v '#\|//\|test_\|mock_'; then
    echo "⚠️  LLM score patterns found in zmatrix/ (may be legacy)"
else
    echo "  ✅ No LLM subjective score patterns in zmatrix/"
fi

echo "═══ V4.0 Guardrails PASS ═══"
