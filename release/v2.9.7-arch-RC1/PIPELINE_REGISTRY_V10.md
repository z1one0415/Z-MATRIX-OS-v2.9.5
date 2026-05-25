# Pipeline Registry v1.0 — Z-MATRIX-OS 三层架构第二层

## 定义

Pipeline Registry 是管线组合应用层的注册表，记录所有公开管线的元信息、允许技能、禁止能力。

## 字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|:----:|------|
| layer | str | ✅ | 固定为 `"pipeline_application"` |
| pipeline_path | str | ✅ | 管线入口文件路径 |
| purpose | str | ✅ | 管线功能说明 |
| allowed_skills | list[str] | ✅ | 允许调用的 shared skill id 列表 |
| required_gates | list[str] | ✅ | 管线必须通过的安全闸门 |
| forbidden_capabilities | list[str] | ✅ | 管线禁止的能力（必须含 real_trade / real_z9_write / real_market_fetch / auto_calibration） |
| owner | str | ✅ | 管线归属方 |
| contract | str | ✅ | 合约文档路径 |
| test | str | ✅ | 测试文件路径 |

## 已注册管线

| pipeline_id | owner | 允许技能数 | 路径 |
|-------------|-------|:----------:|------|
| Z-G18 | G18 | 10 | `pipelines/Z-G18_天机引擎/gate_pipeline.py` |
| RC-release | RC | 1 | `scripts/verify_rc_candidate.sh` |
| Z-G09 | R-Matrix | 1 | `pipelines/Z-G09_全局轮动筛选/gate_pipeline.py` |
| Z-G14 | R-Matrix | 1 | `pipelines/Z-G14_月度全量选股/gate_pipeline.py` |

## 约束

- `allowed_skills` 必须全部存在于 `SHARED_SKILL_REGISTRY`
- pipeline 只能通过 registry 调用技能，不得私造同类能力
- `forbidden_capabilities` 必须包含 no-real-ops 四项（real_trade / real_z9_write / real_market_fetch / auto_calibration）
- 所有 pipeline 必须同时存在 contract 和 test
