# Impl ✓ NO_SIDE_EFFECT_PLAN

## Status: IMPLEMENTATION_PLANNING_NO_SIDE_EFFECT_PLAN_READY
Phase: WAVE0_ENABLEMENT_IMPLEMENTATION_PLANNING | Level 5: BLOCKED

## Side Effect Taxonomy
| 类别 | Wave0允许? | 检测 |
|:--|:--:|:--|
| File Write | ❌ | FileGuard |
| File Read | ✅(report_reader) | Allowed dirs whitelist |
| Network Write(POST/PUT/DELETE) | ❌ | NetGuard |
| Network GET | ✅(github only) | URL whitelist |
| Global State Mutate | ❌ | Runtime审计 |
| Env Var Set | ❌ | EnvGuard |
| DB Write | ❌ | 无DB adapter |
| Process Spawn | ❌(doc_gen特例pandoc,需审批) | ProcessGuard |
| Telemetry Send | ❌ | 无telemetry adapter |

## Per-Adapter Matrix
| Side Effect | GitHub | Doc Gen | Report Reader |
|:--|:--:|:--:|:--:|
| File Read | ❌ | ✅(templates) | ✅(reports) |
| File Write | ❌ | ✅(gated) | ❌ |
| Network GET | ✅(GitHub API) | ❌ | ❌ |
| Subprocess | ❌ | ✅(pandoc,gated) | ❌ |

**Doc Gen 特例**: 写文件仅 memory/ 目录, md/txt/json 格式, 需 human approval

## Detection: SideEffectGuard.before_call/after_call → 任何违反→立即拒绝

> Cap OS Phase 11 | No-Side-Effect | Wave0=readonly | Doc gen exception needs approval