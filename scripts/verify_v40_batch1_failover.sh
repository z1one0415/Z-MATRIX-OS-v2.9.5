#!/usr/bin/env bash
set -euo pipefail
echo "═══ V4.0-B1 Failover + Contracts Verification ═══"
PYTHONPATH=. python3 -c "
from zmatrix.runtime.failover import LLMProviderFailoverPolicy, CircuitBreaker, OfflineDegradedMode
from zmatrix.contracts.batch1_contracts import SubjectiveScoreBanValidator, FactExtractionContract, FailoverContract
# Smoke
fp = LLMProviderFailoverPolicy()
cb = CircuitBreaker()
od = OfflineDegradedMode()
sv = SubjectiveScoreBanValidator()
fc = FactExtractionContract()
fc2 = FailoverContract()
print('  ✅ All Batch-1 modules importable')
"
PYTHONPATH=. python3 tests/runtime/test_batch1_failover_contracts.py
echo "  ✅ Failover + Contracts tests PASS"
bash scripts/verify_v40_guardrails.sh 2>&1 | tail -1
bash scripts/verify_v40_parser_scorer_split.sh 2>&1 | tail -1
echo "═══ V4.0-B1 PASS ═══"
