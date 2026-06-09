# Z2 Research Report Node Implementation Planning — DEGRADATION

> Status: PLANNING_COMPLETE
> Seal: Z_SKILLOS_Z2_RESEARCH_REPORT_NODE_IMPLEMENTATION_PLANNING_SEALED
> Date: 2026-06-09
> Branch: plan/skillos-z2-research-report-node-implementation-planning
> Base: c5f69f5

---

## 1. Status

| Field | Value |
|-------|-------|
| Phase | Planning (docs-only) |
| Confidence | HIGH_WITH_STRUCTURE_ONLY |
| Degradation mode | DENY_Z2_OUTPUTS_UNSAFE |
| Trigger | Kill-switch OR input validation failure OR runtime error |

## 2. Scope

This document defines the degradation strategy for the Z2 Research Report Node. When the node cannot produce a valid research report, it MUST degrade gracefully rather than emit partial/incorrect data.

### Degradation Modes

| Mode | Trigger | Behavior |
|------|---------|----------|
| DENY_Z2_OUTPUTS_UNSAFE | Kill-switch active | Return empty response with degradation status |
| INPUT_INVALID | B1 CompositionGraphResponse fails validation | Return degradation with reason |
| SECTION_BUILD_FAILURE | Section builder throws | Return partial report with degradation flag |
| EVIDENCE_INSUFFICIENT | Evidence count below threshold | Return report with evidence warning |
| TIMEOUT_EXCEEDED | Execution exceeds 30s | Return whatever completed with timeout flag |
| INTERNAL_ERROR | Unexpected exception | Return degradation with sanitized error |

### Degradation Response Structure

```
ReportDegradationStatus:
    mode: DegradationMode (enum)
    reason: str (human-readable)
    timestamp: datetime (UTC)
    request_id: str (UUID, for correlation)
    partial_sections_completed: int
    total_sections_expected: int
    is_recoverable: bool
    suggested_retry_after_ms: Optional[int]
```

### Degradation Escalation

| Level | Condition | Action |
|-------|-----------|--------|
| L1 - Warn | Single section fails | Continue with remaining sections, flag partial |
| L2 - Degrade | >50% sections fail | Emit degradation response |
| L3 - Deny | Kill-switch active | DENY_Z2_OUTPUTS_UNSAFE, no partial data |
| L4 - Panic | Unrecoverable state | Log critical, return L3 response |

## 3. Dependency

- Kill-switch state from config/environment
- B1 CompositionGraphResponse validation from upstream contract
- Z9 contract requires explicit degradation signaling
- postmerge HEAD = c5f69f5

## 4. Boundary

- Degradation NEVER emits partial trading signals
- Degradation NEVER silently succeeds (always flagged)
- Degradation response is always JSON-serializable
- Degradation logs are always emitted (even in silent mode)
- No retry logic inside the node (caller decides)

## 5. Forbidden

Even in degraded state, these fields MUST NOT appear:
alpha_claim, expected_return_claim, buy_signal, sell_signal, position_weight, order_signal, trade_instruction, paper_trade_order, broker_action, portfolio_rebalance, real_trade_order, production_decision, real_pnl, trade_result

## 6. Proof

- test_degradation.py will verify each degradation mode triggers correctly (planned)
- test_degradation.py will verify degradation response schema (planned)
- test_degradation.py will verify no forbidden fields in degraded output (planned)
- test_degradation.py will verify escalation logic (L1→L4) (planned)
- Integration test: kill-switch → DENY_Z2_OUTPUTS_UNSAFE (planned)

## 7. Next

- degradation.py implements DegradationMode enum and handler
- Degradation tests are Batch 2 priority
- Monitoring integration for degradation alerting (future)
- Degradation rate tracking for health dashboard (future)

---

**SEAL: Z_SKILLOS_Z2_RESEARCH_REPORT_NODE_IMPLEMENTATION_PLANNING_SEALED**
