# V4.0 FINAL-HARDGATES Hardening-C3 Scope Lock

## Scope

Hardening-C3 只允许完成以下4项：

1. **12 reviewer independent files/configs** — Research Council独立审查员文件
2. **12 markdown templates snapshot rendering** — 报告模板快照渲染
3. **audit zip real file export** — 审计ZIP真实文件导出
4. **IRF-02/05/06/07/08 chain integration** — 剩余5条IRF链路集成

## Hard Boundaries

Hardening-C3 不允许：

1. ❌ RC1 approval
2. ❌ production ready
3. ❌ broker ready
4. ❌ runtime ready
5. ❌ real trade ready

## Allowed Status Transitions

- `INTEGRATION_SMOKE_CANDIDATE` → `INTEGRATION_COMPLETE_CANDIDATE` (C3-5 closeout only)

## Forbidden Status Transitions

- ❌ → `RC1_APPROVED`
- ❌ → `PRODUCTION_READY`
- ❌ → `BROKER_READY`
- ❌ → `RUNTIME_READY`
- ❌ → `REAL_TRADE_READY`

## Current Baseline

```
commit: 680d288
Current release status: INTEGRATION_SMOKE_CANDIDATE
RC1 status: NOT_APPROVED
Production status: BLOCKED
Broker/runtime status: BLOCKED
Real trade status: BLOCKED
```

## Phase Order

```
C3-0 → C3-1 → C3-2 → C3-3 → C3-4 → C3-5
```

Each phase must pass verify before proceeding to next.
