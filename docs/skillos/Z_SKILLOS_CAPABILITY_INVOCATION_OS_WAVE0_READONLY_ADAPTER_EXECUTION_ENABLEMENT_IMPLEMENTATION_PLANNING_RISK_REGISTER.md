# Impl ✓ RISK_REGISTER

## Status: IMPLEMENTATION_PLANNING_RISK_REGISTER_READY
Phase: WAVE0_ENABLEMENT_IMPLEMENTATION_PLANNING | Level 5: BLOCKED | Items: 12

## Risk Matrix
| # | 风险 | 概率 | 影响 | 等级 | 缓解 |
|:--|:--|:--:|:--:|:--:|:--|
| R1 | Planning→Code转换失真 | M | H | 🔴HIGH | File-level plan详细指定每个文件 |
| R2 | Network call不慎启用 | L | C | 🟡MED | NetGuard+URL whitelist+mock-only tests |
| R3 | File write副作用 | L | C | 🔴HIGH | SideEffectGuard+allowed_dirs+FS快照测试 |
| R4 | Production误接 | L | C | 🔴CRIT | Level5永远BLOCKED+CI enforce |
| R5 | Adapter间状态泄漏 | L | M | 🟢LOW | 独立实例+无共享状态+测试验证 |
| R6 | 文档与实现不一致 | M | M | 🟡MED | 每Phase审批gate+seal记录 |
| R7 | Level5边界被突破 | L | C | 🔴CRIT | 多层guard+CI+human approval gate |
| R8 | Config drift(enabled意外True) | L | H | 🟡MED | Config immutability guard+CI检查 |
| R9 | Evidence sink过载OOM | L | L | 🟢LOW | MAX1000条rotate+仅存近期 |
| R10 | GitHub token泄漏 | L | C | 🔴CRIT | Kill switch+scope最小化(read-only)+env var非明文 |
| R11 | Phase scope creep(11→12跳级) | M | H | 🔴HIGH | Gate flow强制执行+review gate |
| R12 | Adapter测试覆盖不足 | M | M | 🟡MED | 39 tests+29 proof matrix items |

## Summary: 3 CRITICAL(R4,R7,R10) | 3 HIGH(R1,R3,R11) | 4 MEDIUM | 2 LOW
> Cap OS Phase 11 | Risk Register | 12 risks | 3 CRITICAL