# Research OS V3 — Delivery Index

**Status**: ARCHITECTURE_FREEZE | **Version**: V3 | **Date**: 2026-05-30T21:38+08:00

## Current State
- Modules: 160 (unchanged since freeze)
- Packages: 23
- Tests: 1,224 (all passing)
- Production: BLOCKED | Broker/Runtime: BLOCKED | RealTrade: BLOCKED

## Core Documents
| Document | Purpose |
|----------|---------|
| [ARCHITECTURE_FREEZE_ACCEPTANCE.md](ARCHITECTURE_FREEZE_ACCEPTANCE.md) | Freeze gate + allowed/forbidden work |
| [RESEARCH_OS_V3_FREEZE_MANIFEST.md](RESEARCH_OS_V3_FREEZE_MANIFEST.md) | Frozen baseline manifest (160/23/1224) |
| [../research_db/CAPABILITY_MAP.md](../research_db/RESEARCH_OS_CAPABILITY_MAP.md) | 6-layer architecture + dependency matrix |
| [../research_db/GOLDEN_PATH_CASE_001.md](../research_db/GOLDEN_PATH_CASE_001.md) | 600519 贵州茅台 9-stage documentation |
| [../research_db/WHITEPAPER.md](../research_db/RESEARCH_OS_V3_WHITEPAPER.md) | System goals, theory, boundaries |
| [../research_db/COMPRESSION_AUDIT.md](../research_db/COMPRESSION_AUDIT.md) | CORE/OPTIONAL/SPECIALIZED classification |

## Operations
| Entry | Command |
|-------|---------|
| Golden Path (dry run) | `bash scripts/run_golden_path_600519.sh --dry-run` |
| Golden Path (full) | `bash scripts/run_golden_path_600519.sh` |
| Architecture Freeze verify | `bash scripts/verify_research_os_architecture_freeze.sh` |
| Delivery Closeout verify | `bash scripts/verify_research_os_delivery_closeout.sh` |

## Audit Entries
| Audit | File |
|-------|------|
| Freeze Audit | [ARCHITECTURE_FREEZE_ACCEPTANCE.md](ARCHITECTURE_FREEZE_ACCEPTANCE.md) |
| Module Count | `find zmatrix/research_db -name "*.py" ! -name "__init__.py" | wc -l` |
| Test Quality | [TEST_QUALITY_AUDIT_PLAN.md](TEST_QUALITY_AUDIT_PLAN.md) |
| Golden Path Repro | `bash scripts/run_golden_path_600519.sh --dry-run` |
| Safety Scan | `PYTHONPATH=. pytest -q tests/docs/` |

## Forbidden
- ❌ New capability modules
- ❌ Broker adapter
- ❌ Runtime execution
- ❌ Real trade
- ❌ Phase 6 production simulation
- ❌ Architecture freeze violation
