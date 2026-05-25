# System Controller MVP v1.0 — 最小系统控制器

## 功能

只负责读取 registry 并生成 execution plan。不执行真实业务。

## API

```python
plan = build_system_execution_plan(
    workflow_id: str,
    *,
    dry_run: bool = True,
) -> dict
```

## 输出结构

```python
{
    "controller_version": "v1.0",
    "workflow_id": "...",
    "pipeline_id": "...",
    "dry_run": True,
    "execution_allowed": False,    # 永远 False
    "real_ops_allowed": False,     # 永远 False
    "ordered_nodes": [...],        # 拓扑排序后的节点列表
    "required_gates": [...],
    "skill_nodes": [...],
    "gate_nodes": [...],
    "forbidden_capabilities": [...],
    "validation": {
        "workflow_exists": True/False,
        "pipeline_registered": True/False,
        "nodes_registered": True/False,
        "gates_registered": True/False,
        "no_real_ops": True/False,
        "ready_for_runtime": False,  # MVP: 永远 False
    },
    "reason": "SYSTEM_CONTROLLER_MVP_PLAN_ONLY_NO_RUNTIME_EXECUTION"
}
```

## 规则

- dry_run 默认为 True
- execution_allowed 永远 False
- real_ops_allowed 永远 False
- 不实际调用 G18 / Z9 / R-Matrix
- 不实际执行 pipeline
- 只生成 plan preview
