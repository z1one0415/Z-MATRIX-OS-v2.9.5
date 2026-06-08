# Impl ✓ EVIDENCE_SINK_PLAN

## Status: IMPLEMENTATION_PLANNING_EVIDENCE_SINK_PLAN_READY
Phase: WAVE0_ENABLEMENT_IMPLEMENTATION_PLANNING | Level 5: BLOCKED

## Architecture (概念级)
Adapter.call() → Guard Pipeline(10-stage) → Permission → Config → Contract → [EVIDENCE_SINK] → create_evidence → evidence_store.append → rotate if >1000

## Evidence Record Schema
call_id(UUID) | timestamp(UTC) | adapter("github_readonly"|"doc_gen"|"report_reader") | operation | params_hash(SHA256) | result_status("OK"|"DENIED"|"ERROR"|"TIMEOUT") | result_size_bytes | duration_ms | guard_decisions | permission_granted | error_message

## Lifecycle: CREATE(每次call) → ACCUMULATE(内存list) → ROTATE(>1000条) → PRUNE(过期清理)

## Constraints
内存中(不落盘) | 内容脱敏(params仅hash) | 只读(不修改result_envelope) | 非阻塞(失败不影响adapter) | 不发送(无外部telemetry)

## Evidence: E1: Level 3 audit sink 已存在 | E2: P1 runtime evidence bus skeleton merged | E3: Adapter Framework P0 预留 evidence hook

## Next: EVIDENCE_SINK_PLAN finalized → Plan 层产出

> Cap OS Phase 11 | Evidence Sink Plan | Memory-only | No file write