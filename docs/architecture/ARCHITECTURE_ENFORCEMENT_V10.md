# Architecture Enforcement v1.0 — 架构硬约束审计

## 功能

对所有架构注册表做跨表硬约束验证，防止注册表之间的不一致。

## 检查项

| 检查函数 | 目标 |
|----------|------|
| `check_pipeline_allowed_skills_only()` | pipeline.allowed_skills 必须全部在 SHARED_SKILL_REGISTRY |
| `check_no_unregistered_pipeline_required_gates()` | pipeline.required_gates 必须全部在 GATE_REGISTRY |
| `check_no_duplicate_skill_modules()` | 不允许两个 skill 注册同一 module+public_function，除非 duplicate_allowed=True |
| `check_no_pipeline_declares_forbidden_capability()` | 所有 pipeline 的 forbidden_capabilities 必须包含 no-real-ops 四项 |
| `check_no_real_ops_enabled_anywhere()` | 不支持任何 entity 声明 real_trade enabled |

## 集成

`run_architecture_enforcement()` 一次性执行所有检查，返回违规列表。

## Enforcement Scope

Current version is registry-level enforcement.

It validates:
- registry cross references
- allowed_skills registration
- required_gates registration
- duplicate skill module/function declarations
- no-real-ops declarations

It does not yet perform full source-level static analysis over all pipeline implementation files.

Source-level enforcement is reserved for the next architecture hardening phase.
