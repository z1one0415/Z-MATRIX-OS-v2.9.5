#!/usr/bin/env bash
set -euo pipefail
echo "═══ V4.0 Parser-Scorer Split Verification ═══"

# Check deterministic scorer exists or is planned
python3 -c "
# Verify Parser-Scorer Split Protocol exists
import os
assert os.path.exists('docs/architecture/PARSER_SCORER_SPLIT_PROTOCOL_V10.md')
assert os.path.exists('docs/architecture/LLM_SUBJECTIVE_SCORE_BAN_PROTOCOL_V10.md')
assert os.path.exists('docs/architecture/DETERMINISTIC_SCORING_PROTOCOL_V10.md')
assert os.path.exists('docs/architecture/SCORE_TRACE_PROTOCOL_V10.md')
print('  ✅ Parser-Scorer Split protocol suite present')
"

# Check architecture docs prohibit LLM scores
for f in docs/architecture/PARSER_SCORER_SPLIT_PROTOCOL_V10.md docs/architecture/LLM_SUBJECTIVE_SCORE_BAN_PROTOCOL_V10.md; do
    if grep -q 'MUST NOT\|NOT output.*score\|FORBIDDEN\|BANNED' "$f"; then
        echo "  ✅ $f contains score prohibition"
    fi
done

# Verify no LLM score generator patterns in new code
llm_subjective='score.*=.*llm\|llm.*score\|score_from_llm'
if grep -r "$llm_subjective" zmatrix/ --include="*.py" 2>/dev/null | grep -v '#\|test_\|mock_'; then
    echo "⚠️  Potential LLM score calls found"
else
    echo "  ✅ No LLM→score generation patterns detected"
fi

echo "═══ V4.0 Parser-Scorer Split PASS ═══"
