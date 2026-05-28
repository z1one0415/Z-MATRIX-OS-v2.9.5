#!/usr/bin/env bash
set -euo pipefail
echo "═══ V4.0-B2 Research Council + Report Library Verification ═══"
python3 -c "
from zmatrix.research_council.council import RESEARCH_COUNCIL_SEATS, REPORT_TEMPLATES, HARD_GATE_REPORT_BLOCKS
assert len(RESEARCH_COUNCIL_SEATS)==12, f'Expected 12 seats, got {len(RESEARCH_COUNCIL_SEATS)}'
assert len(REPORT_TEMPLATES)==12, f'Expected 12 templates, got {len(REPORT_TEMPLATES)}'
assert len(HARD_GATE_REPORT_BLOCKS)>=3
for seat_id, seat in RESEARCH_COUNCIL_SEATS.items():
    assert seat.get('parser_scorer_policy') in ('PARSER_ONLY','DETERMINISTIC_SCORER_ONLY','PARSER_THEN_SCORER','NO_LLM'), f'{seat_id} invalid parser_scorer_policy'
    assert seat.get('real_trade_allowed') != True if 'real_trade_allowed' in seat else True
print(f'  ✅ {len(RESEARCH_COUNCIL_SEATS)} research council seats')
print(f'  ✅ {len(REPORT_TEMPLATES)} report templates')
print(f'  ✅ {len(HARD_GATE_REPORT_BLOCKS)} hard gate blocks')
print(f'  ✅ All seats have parser_scorer_policy')
print(f'  ✅ All seats default real_trade_allowed=False')
"
echo "═══ V4.0-B2 PASS ═══"
