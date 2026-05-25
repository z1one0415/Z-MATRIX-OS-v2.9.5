# Gate Registry v1.0 — Z-MATRIX-OS 三层架构第三层组件

## 定义

Gate Registry 是系统控制层的 gate 注册表。所有安全边界、contract validation、preview-only、RC verification 闸门必须注册于此。

gate 是系统控制层组件，**不得实现业务判断**。

## 字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|:----:|------|
| layer | str | ✅ | 固定为 `"system_control"` |
| gate_type | str | ✅ | gate 类型：safety / write_boundary / contract / release / data_contract |
| purpose | str | ✅ | gate 功能说明 |
| owner | str | ✅ | gate 归属方 |
| applies_to | list[str] | ✅ | 受此 gate 约束的 pipeline ID 列表 |
| enforced_by | str | ✅ | 执行此 gate 的代码/脚本/测试路径 |
| blocking | bool | ✅ | 是否为阻塞 gate |
| degradable | bool | ✅ | 是否允许降级通过 |
| contract | str | ✅ | 合约文档路径 |
| test | str | ✅ | 测试文件路径 |

## 已注册 Gate

| gate_id | owner | type | blocking | applies_to |
|---------|-------|:----:|:--------:|------------|
| `safety.no_real_trade` | SystemCore | safety | ✅ | Z-G18, Z-G09, Z-G14, RC-release |
| `z9.preview_only` | Z9 | write_boundary | ✅ | Z-G18 |
| `contract.validation` | SystemCore | contract | ✅ | Z-G18, RC-release |
| `rc.packaging` | RC | release | ✅ | RC-release |
| `rc.verification` | RC | release | ✅ | RC-release |
| `r_matrix.cycle_valid` | R-Matrix | data_contract | ✅ | Z-G09, Z-G14 |
| `safety.boundary_scan` | SystemCore | safety | ✅ | RC-release |

## 约束

- `pipeline.required_gates` 必须全部存在于 `GATE_REGISTRY`
- gate 不得实现业务判断逻辑
- blocking gate 不可降级通过
- 所有 gate 必须同时存在 contract 和 test
