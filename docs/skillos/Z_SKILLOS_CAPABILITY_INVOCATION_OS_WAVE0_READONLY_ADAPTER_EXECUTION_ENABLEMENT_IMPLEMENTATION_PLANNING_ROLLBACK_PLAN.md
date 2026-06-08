# Impl ✓ ROLLBACK_PLAN

## Status: IMPLEMENTATION_PLANNING_ROLLBACK_PLAN_READY
Phase: WAVE0_ENABLEMENT_IMPLEMENTATION_PLANNING | Level 5: BLOCKED

## Rollback Scenarios
**Scenario A: Adapter Bug(代码级)**: Set enabled=False → cherry-pick revert → re-run 228 tests → 可选回Phase 11
**Scenario B: Runtime异常**: Activate kill switch(L1/L2/L3) → 分析evidence sink → 修复 → remove kill switch
**Scenario C: 外部依赖不可用**: GitHub API down→ERROR(不阻塞其他) | 模板缺失→TemplateNotFoundError | pandoc缺失→降级Markdown-only | 报告删除→FileNotFoundError
**Scenario D: 安全事件**: L3 kill switch → revoke GitHub token → rotate credentials → audit evidence sink → 修复

## Safety Properties
原子性(kill switch单操作) | 可逆性(remove sentinel→恢复) | 无数据损失(只读) | 无级联影响(adapter独立) | 优雅降级(不抛未捕获异常)

## Phase 11 Rollback: `git checkout postmerge/... && git branch -D plan/...`

> Cap OS Phase 11 | Rollback Plan | 4 scenarios | Level 5 BLOCKED