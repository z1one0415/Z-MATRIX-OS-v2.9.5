# Impl ✓ OVERVIEW

## Status: IMPLEMENTATION_PLANNING_OVERVIEW_READY
Phase: WAVE0_ENABLEMENT_IMPLEMENTATION_PLANNING | Branch: `plan/...impl-planning` | Baseline: postmerge @ `5e7dbe5` | Level 5: BLOCKED

## Scope
为 3 个 Wave0 只读 Adapter 的启用实现制定完整蓝图：
1. **GitHub Readonly Adapter** — 只读公开 repo 访问
2. **Document Generation Adapter** — 模板化文档生成
3. **Report Reading Adapter** — 已有报告解析

### Out of Scope
代码编写(Phase 12) | runtime execution | network calls | file writes | Z-MATRIX imports | invoke_skill/result_envelope mutation | Level 5

## Evidence
E1: WAVE0_READONLY_ADAPTER_P0 skeleton merged | E2: 3 adapter templates in `adapters/wave0/` | E3: Adapter Framework P0 interface standard (Phase 7) | E4: 10 prior phases merged to postmerge | E5: 228/232 tests

## Decision Options
GO_FOR_IMPL_PLANNING(当前) | NO_GO | SKIP_TO_IMPL(驳回:违反门禁)

## Rejected: RUNTIME | ADAPTER_CALL | FILE_WRITE | ZMATRIX_IMPORT | WARNING_ENABLE | PRODUCTION | TAG | LEVEL5_PLANNING

## Boundary: 仅 Markdown docs(33份) | 无代码/测试/配置 | git 仅 docs/skillos/ 变更

## Next: 33 docs 达标 → REVIEW_GATE → human review → merge decision

> Cap OS Phase 11 | Level 5 BLOCKED | No code | No runtime | No exec