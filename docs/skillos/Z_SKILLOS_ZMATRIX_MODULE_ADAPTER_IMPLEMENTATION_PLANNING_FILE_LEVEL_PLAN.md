# Z-SkillOS Z-MATRIX Module Adapter Implementation Planning — FILE_LEVEL_PLAN

> **Lane**: A1 — Z-MATRIX Module Adapter Implementation Planning
> **Branch**: `plan/skillos-zmatrix-module-adapter-implementation-planning` @ `3e6ce10c`
> **Date**: 2026-06-08
> **Status**: FUTURE_PLAN_ONLY | Level 5 BLOCKED

---

## §1 — File-Level Architecture

This document defines the file-level implementation plan for the five
Z-MATRIX Module Adapters. All files are FUTURE — no code exists yet.
The plan establishes directory structure, file naming, module contracts,
and dependency ordering before any implementation begins.

---

## §2 — Directory Structure (Planned)

```
skillos/capability_invocation_os/zmatrix_adapters/
├── __init__.py                          # Package init — exports all adapters
├── _base.py                             # Abstract base adapter class
├── _contracts.py                        # Contract definitions and validators
├── _evidence.py                         # Evidence capture and hash chain
├── _permissions.py                      # Permission check decorators
├── _registry.py                         # Adapter registry and discovery
├── capability_registry_readonly.py      # Adapter 1: Registry inspection
├── z9_memory_review_readonly.py         # Adapter 2: Z9 memory recall
├── z2_research_output_readonly.py       # Adapter 3: Z2 report reading
├── local_report_reading.py              # Adapter 4: Local file inspection
├── document_generation_in_memory.py     # Adapter 5: In-memory doc gen
├── tests/
│   ├── __init__.py
│   ├── test_base.py                     # Base adapter tests
│   ├── test_contracts.py                # Contract validation tests
│   ├── test_registry.py                 # Registry tests
│   ├── test_permissions.py              # Permission enforcement tests
│   ├── test_evidence.py                 # Evidence chain tests
│   ├── test_adapter_1_registry.py       # Adapter 1 tests
│   ├── test_adapter_2_z9.py             # Adapter 2 tests
│   ├── test_adapter_3_z2.py             # Adapter 3 tests
│   ├── test_adapter_4_report.py         # Adapter 4 tests
│   └── test_adapter_5_docgen.py         # Adapter 5 tests
└── README.md                            # Package documentation
```

---

## §3 — File Dependency Graph

```
_base.py
  ├── _contracts.py (imported by _base.py)
  ├── _evidence.py  (imported by _base.py)
  └── _permissions.py (imported by _base.py)

_registry.py
  └── _base.py (imports BaseAdapter)

capability_registry_readonly.py ──► _base.py, _registry.py
z9_memory_review_readonly.py    ──► _base.py, _registry.py
z2_research_output_readonly.py  ──► _base.py, _registry.py
local_report_reading.py         ──► _base.py, _registry.py
document_generation_in_memory.py──► _base.py, _registry.py
```

---

## §4 — Implementation Order

| Phase | Files | Rationale |
|-------|-------|-----------|
| Phase 0 | `_contracts.py`, `_evidence.py`, `_permissions.py` | Foundation contracts |
| Phase 1 | `_base.py` | Abstract adapter class |
| Phase 2 | `_registry.py` | Adapter discovery |
| Phase 3 | Adapters 1-5 | Concrete implementations |
| Phase 4 | `tests/` | Full test suite |

---

## §5 — Module Contract (per file)

Each adapter file MUST implement:
1. A class inheriting from `BaseAdapter`
2. `adapter_name: str` — unique identifier
3. `adapter_version: str` — semver
4. `risk_tier: int` — 0 (read-only) or 1 (in-memory write)
5. `execute(**kwargs) -> AdapterResult` — main entry point
6. `validate_input(**kwargs) -> bool` — input validation
7. `capture_evidence() -> EvidenceChain` — evidence trace

---

## §6 — Naming Convention

| Element | Convention | Example |
|---------|-----------|---------|
| File name | `snake_case.py` | `z9_memory_review_readonly.py` |
| Class name | `PascalCase` | `Z9MemoryReviewReadonlyAdapter` |
| Test file | `test_adapter_N_shortname.py` | `test_adapter_2_z9.py` |
| Doc file | `Z_SKILLOS_*_PLANNING_*.md` | This file |

---

## §7 — Governance

All files are FUTURE_PLAN_ONLY. No file shall be created until the planning,
review, and merge gates are passed. Each file must have a corresponding test
file created simultaneously (TDD). File creation is gated by the MERGE_CLOSEOUT
document achieving APPROVED status.

---

> **Signature**: ☯️ Z2天师 — Hermes Research Kernel
> **Pipeline**: Z-G14 | Lane A1: File Level Plan
