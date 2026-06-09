# Z2 Research Report Node Implementation Planning — FUTURE CODE MAP

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
| Source files planned | 12 |
| Test files planned | 9 |
| Implementation batches | 3 |

## 2. Scope

This document maps all future code files that will be created during implementation. NO CODE IS CREATED IN THIS PLANNING PHASE.

### Source Files (12)

| # | File | Batch | Purpose |
|---|------|-------|---------|
| 1 | skillos/capability_invocation_os/research_report_node/__init__.py | 1 | Module initialization; public exports |
| 2 | skillos/capability_invocation_os/research_report_node/constants.py | 1 | Magic numbers, limits, enums |
| 3 | skillos/capability_invocation_os/research_report_node/config.py | 1 | Configuration schema and defaults |
| 4 | skillos/capability_invocation_os/research_report_node/kill_switch.py | 1 | Disabled-by-default kill-switch |
| 5 | skillos/capability_invocation_os/research_report_node/models.py | 1 | All 8 Pydantic models |
| 6 | skillos/capability_invocation_os/research_report_node/contracts.py | 1 | Input/output contract validation |
| 7 | skillos/capability_invocation_os/research_report_node/section_builder.py | 2 | Section construction pipeline |
| 8 | skillos/capability_invocation_os/research_report_node/evidence.py | 2 | Evidence validation and structuring |
| 9 | skillos/capability_invocation_os/research_report_node/degradation.py | 2 | Degradation handler |
| 10 | skillos/capability_invocation_os/research_report_node/report_builder.py | 3 | Report orchestration |
| 11 | skillos/capability_invocation_os/research_report_node/z9_snapshot.py | 3 | Z9 snapshot projection |
| 12 | skillos/capability_invocation_os/research_report_node/registry.py | 3 | Node registration |

### Test Files (9)

| # | File | Batch | Covers |
|---|------|-------|--------|
| 1 | tests/skillos/capability_invocation_os/research_report_node/test_disabled_default.py | 1 | kill_switch.py |
| 2 | tests/skillos/capability_invocation_os/research_report_node/test_models.py | 1 | models.py |
| 3 | tests/skillos/capability_invocation_os/research_report_node/test_contracts.py | 1 | contracts.py |
| 4 | tests/skillos/capability_invocation_os/research_report_node/test_section_builder.py | 2 | section_builder.py |
| 5 | tests/skillos/capability_invocation_os/research_report_node/test_evidence.py | 2 | evidence.py |
| 6 | tests/skillos/capability_invocation_os/research_report_node/test_degradation.py | 2 | degradation.py |
| 7 | tests/skillos/capability_invocation_os/research_report_node/test_report_builder.py | 3 | report_builder.py |
| 8 | tests/skillos/capability_invocation_os/research_report_node/test_z9_snapshot.py | 3 | z9_snapshot.py |
| 9 | tests/skillos/capability_invocation_os/research_report_node/test_no_forbidden_imports.py | 1 | All source files (import scan) |

### Implementation Batch Plan

| Batch | Files | Dependencies | Gate |
|-------|-------|-------------|------|
| Batch 1 | __init__, constants, config, kill_switch, models, contracts + test_disabled_default, test_models, test_contracts, test_no_forbidden_imports | None (foundational) | All tests green |
| Batch 2 | section_builder, evidence, degradation + test_section_builder, test_evidence, test_degradation | Batch 1 merged | All tests green |
| Batch 3 | report_builder, z9_snapshot, registry + test_report_builder, test_z9_snapshot | Batch 2 merged | All tests green + integration |

## 3. Dependency

- File structure follows SkillOS convention from sealed upstream
- Test structure mirrors source structure
- postmerge HEAD = c5f69f5

## 4. Boundary

- All files within skillos/capability_invocation_os/research_report_node/
- All tests within tests/skillos/capability_invocation_os/research_report_node/
- No files outside these directories
- No shared utility files (all self-contained)

## 5. Forbidden

- No code file may contain forbidden fields
- No test file may use forbidden fields as valid test data
- Negative tests for forbidden fields use assertion of rejection

## 6. Proof

- File count: 12 source + 9 test = 21 total files planned
- Batch dependencies are acyclic
- Test coverage target: ≥95% per batch
- Every source file has at least one dedicated test file

## 7. Next

- Batch 1 begins after planning review approval
- Each batch has its own branch and review cycle
- No batch starts until previous batch is merged
- Code map updates if scope changes during implementation

---

**SEAL: Z_SKILLOS_Z2_RESEARCH_REPORT_NODE_IMPLEMENTATION_PLANNING_SEALED**
