# Z-SkillOS Level 4 Implementation File-Level Design

## Status

Z_SKILLOS_LEVEL4_IMPLEMENTATION_FILE_LEVEL_DESIGN_READY

## Scope

Proposed file structure for a future Level 4 implementation phase. No files are created or modified in this phase. All entries are marked FUTURE_PLAN_ONLY.

## Explicit Statement

No code files are created in this phase. No runtime path is changed in this phase. No result_envelope field is modified in this phase.

## Proposal: Config Layer

| Proposed Path | Type | Purpose | Status |
|:--|:--|:--|:--:|
| `configs/skillos/level4_defaults.json` | Config | LEVEL4_WARNING_ENABLED default false | FUTURE_PLAN_ONLY |
| `configs/skillos/level4_thresholds.json` | Config | Severity escalation thresholds | FUTURE_PLAN_ONLY |
| `configs/skillos/level4_rollback.json` | Config | Rollback kill-switch settings | FUTURE_PLAN_ONLY |

## Proposal: Contract Layer

| Proposed Path | Type | Purpose | Status |
|:--|:--|:--|:--:|
| `skillos/level4/contract/warning_contract.py` | Source | Warning schema and validation | FUTURE_PLAN_ONLY |
| `skillos/level4/contract/severity_contract.py` | Source | Severity level definitions | FUTURE_PLAN_ONLY |
| `skillos/level4/contract/rollback_contract.py` | Source | Rollback control interface | FUTURE_PLAN_ONLY |

## Proposal: Audit Layer

| Proposed Path | Type | Purpose | Status |
|:--|:--|:--|:--:|
| `skillos/level4/audit/audit_writer.py` | Source | Internal audit file writer | FUTURE_PLAN_ONLY |
| `skillos/level4/audit/operator_reporter.py` | Source | Operator review report generator | FUTURE_PLAN_ONLY |
| `skillos/level4/audit/delivery_guard.py` | Source | Side-channel delivery boundary guard | FUTURE_PLAN_ONLY |

## Proposal: Evaluation Layer

| Proposed Path | Type | Purpose | Status |
|:--|:--|:--|:--:|
| `skillos/level4/eval/evaluator.py` | Source | Warning evaluation pipeline | FUTURE_PLAN_ONLY |
| `skillos/level4/eval/severity_escalator.py` | Source | INFO→NOTICE→WARN→ESCALATE state machine | FUTURE_PLAN_ONLY |
| `skillos/level4/eval/false_positive_tracker.py` | Source | FP detection and suppression | FUTURE_PLAN_ONLY |

## Proposal: Config Contract Draft

| Proposed Path | Type | Purpose | Status |
|:--|:--|:--|:--:|
| `skillos/level4/config/gate_config.py` | Source | Level 4 config reader | FUTURE_PLAN_ONLY |

## Proposal: Side-Channel Audit Draft

| Proposed Path | Type | Purpose | Status |
|:--|:--|:--|:--:|
| `runtime_audit/level4_warnings.jsonl` | Runtime data | Internal audit file | FUTURE_PLAN_ONLY |
| `runtime_reports/level4_operator_review.md` | Runtime data | Operator review report | FUTURE_PLAN_ONLY |

## Proposal: Proof Harness Draft

| Proposed Path | Type | Purpose | Status |
|:--|:--|:--|:--:|
| `tests/skillos/test_level4_disabled_emits_nothing.py` | Test | Gate-1: disabled-by-default | FUTURE_PLAN_ONLY |
| `tests/skillos/test_level4_envelope_unchanged.py` | Test | Gate-2: envelope immutability | FUTURE_PLAN_ONLY |
| `tests/skillos/test_level4_no_blocking_paths.py` | Test | Gate-3: no blocking | FUTURE_PLAN_ONLY |
| `tests/skillos/test_level4_no_production_linkage.py` | Test | Gate-4: no production linkage | FUTURE_PLAN_ONLY |
| `tests/skillos/test_level4_warning_delivery_boundary.py` | Test | Gate-5: side-channel only | FUTURE_PLAN_ONLY |
| `tests/skillos/test_level4_kill_switch_rollback.py` | Test | Gate-6: rollback safety | FUTURE_PLAN_ONLY |
| `tests/skillos/test_level4_severity_escalation_flow.py` | Test | Gate-7: severity escalation | FUTURE_PLAN_ONLY |
| `tests/skillos/test_level4_false_positive_loop.py` | Test | Gate-8: FP loop | FUTURE_PLAN_ONLY |

## Design Principles

1. **Read-only access to existing systems** — Level 4 modules may read config and evidence, but never mutate existing structures
2. **Side-channel only** — Warning output goes to audit files and operator reports, never to caller or envelope
3. **Fail-safe default** — All config defaults to disabled; parse failure = disabled
4. **Exception boundary** — All Level 4 code wrapped in try/except that returns CONTINUE
5. **Import guard** — Production/broker/real_trade imports permanently blocked
6. **Rollback-first** — Disable must fully restore Level 3 behavior
