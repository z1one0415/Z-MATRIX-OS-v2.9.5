# V40 FULL SCOPE ACCEPTANCE MATRIX
# Current release status: SMOKE_PROTOTYPE
# RC1 status: NOT_APPROVED
# Production status: BLOCKED

## Status Definitions
# DONE: full impl + integration test + acceptance closeout
# SMOKE_DONE: minimum runnable skeleton + smoke test pass
# PARTIAL: partial impl, missing integration/audit/registry
# PROTOCOL_ONLY: protocol or document only
# REGISTRY_ONLY: registry or manifest only
# NOT_DONE: not implemented
# BLOCKED: blocked by platform phase or data condition

## Batch 0: Baseline Freeze + Scope Lock
| ID | Name | Status |
|---|---|---|
| V40-B0-001~017 | All Batch 0 items | DONE |

## Batch 1: Architecture + Contracts + Failover
| ID | Name | Status |
|---|---|---|
| V40-B1-020 LLMProviderFailoverPolicy | SMOKE_DONE |
| V40-B1-021 OfflineDegradedMode | SMOKE_DONE |
| V40-B1-022 CachedFactExtractionStore | PARTIAL |
| V40-B1-023 CriticalPipelineFallback | PARTIAL |

## Batch 3: DataForge + ZC35/ZC45
| ID | Name | Status |
|---|---|---|
| V40-B3-030 ProxyHedgeStressTest | SMOKE_DONE |

## Batch 4: Execution + LimitBoard
| ID | Name | Status |
|---|---|---|
| V40-B4-017 LimitBoardFillabilityGate | SMOKE_DONE |
| V40-B4-018 BoardContinuationDetector | NOT_DONE |
| V40-B4-019 OpenBoardChaseRiskDetector | NOT_DONE |

## Batch 5: Cockpit + Audit
| ID | Name | Status |
|---|---|---|
| V40-B5-020 FinalHardGatesPanel | PARTIAL |
| V40-B5-021 LLMFailoverPanel | PARTIAL |
| V40-B5-022 LimitBoardFillabilityPanel | PARTIAL |
| V40-B5-023 ProxyHedgeStressPanel | PARTIAL |

## Hardening-B Status
- H-B1 real_trade_allowed expressions: FIXED
- H-B4 gates modularized: DONE (zc40/zc45/zc35/strategy)
- H-B7 truth report: DONE
