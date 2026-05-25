# Workflow DAG Registry v1.0 — 管线工作流契约

## 定义

Workflow DAG 把 Shared Skill 连接成有向无环图。每条 workflow 属于一条 pipeline，串联 nodes=skills/gates，定义 edges=执行顺序。

## 字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|:----:|------|
| layer | str | ✅ | 固定为 `"workflow_dag"` |
| pipeline | str | ✅ | 所属 pipeline ID，必须存在于 PIPELINE_REGISTRY |
| purpose | str | ✅ | 工作流功能说明 |
| nodes | list[str] | ✅ | 工作流节点（skill id 或 gate id） |
| edges | list[list[str]] | ✅ | 有向边 [from, to] |
| required_gates | list[str] | ✅ | 工作流必须通过的 gate |
| output_contracts | list[str] | ❌ | 工作流产出的契约标识 |
| forbidden_capabilities | list[str] | ✅ | 工作流禁止的能力 |
| contract | str | ✅ | 合约文档路径 |
| test | str | ✅ | 测试文件路径 |

## 已注册 Workflow

| workflow_id | pipeline | nodes | edges |
|-------------|----------|:-----:|:-----:|
| Z-G18.paper_z9_preview_workflow | Z-G18 | 9 | 8 |
| RC.release_verification_workflow | RC-release | 4 | 3 |
| RMatrix.cycle_validation_workflow | Z-G09 | 2 | 1 |

## 约束

- pipeline 必须存在于 PIPELINE_REGISTRY
- nodes 中的 skill 必须存在于 SHARED_SKILL_REGISTRY，gate 必须存在于 GATE_REGISTRY
- required_gates 必须存在于 GATE_REGISTRY
- 不允许环（topological_order 检测）
- forbidden_capabilities 必须包含 no-real-ops 四项

## Node Types

workflow.nodes may contain two node types:

1. **skill nodes** — must exist in `SHARED_SKILL_REGISTRY`
2. **gate nodes** — must exist in `GATE_REGISTRY`

A workflow may mix skill nodes and gate nodes when the workflow itself represents verification or release control.
