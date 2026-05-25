# Z9 Calibration Policy Preview v1.0 — Contract Freeze (Batch D-4)

## 输入
- Z9_OUTCOME_BACKFILL_TASK v1.0 (含 outcome_fields)

## 输出
- CALIBRATION_POLICY_PREVIEW v1.0

## 核心字段

| 字段 | 类型 | 说明 |
|------|------|------|
| preview_version | str | "v1.0" |
| preview_type | str | "CALIBRATION_POLICY_PREVIEW" |
| preview_id | str | CP_{task_id}_{timestamp} |
| task_id | str | 来源 backfill task id |
| ticker | str | 股票代码 |
| source_backfill_task | dict | 来源 backfill task 快照 |
| idempotency | dict | 幂等 key (基于 task_id + ticker + outcome 值) |
| outcome_summary | dict | outcome 统计摘要 |
| policy_domains | dict | 三个校准域预览 |
| state | dict | 状态机 |
| validation | dict | 校验结果 |
| write_policy | dict | 写入策略（均 False） |
| forbidden_real_trade_checked | bool | True |

## policy_domains

三个校准域：

### ev_calibration (Evidence Weight)
- direction: WAITING_FOR_OUTCOME / STRENGTHEN_POSITIVE / REVIEW_NEGATIVE / STABLE
- confidence: NONE / LOW / MEDIUM / HIGH
- 针对 FQS/BVS/ISS/EVL/VSS/CFS/CTS 七维度的权重方向建议

### r_matrix_calibration
- direction: WAITING_FOR_OUTCOME / MAINTAIN_OR_LIGHTEN / TIGHTEN_EXIT / REVIEW
- confidence: NONE / LOW / MEDIUM
- 针对 SHORT_TERM / MEDIUM_TERM / LONG_TERM 周期的建议

### g18_rule_calibration
- direction: WAITING_FOR_OUTCOME / MAINTAIN_PROBABILITY_THRESHOLD / REVIEW_RULES / STABLE
- confidence: NONE / LOW / MEDIUM / HIGH
- calibratable_rules: ["G09_SELL_OVERRIDE", "G09_HARD_BLOCKS", "G11_STRONG_WARNING_ONLY", "Z16_PRICE_GATE", "G17_ACCOUNT_CONFIRMATION", "PROBABILITY_THRESHOLD"]

## 状态机

| 状态 | 含义 |
|------|------|
| AWAITING_BACKFILL | outcome_fields 未回填，无法生成校准方向 |
| POLICY_PREVIEW_GENERATED | outcome 已就绪，校准方向预览已生成 |
| REJECTED | 输入验证失败 |

## 幂等规则

- `calibration_policy_key = sha256(task_id + ticker + outcome_actual_values)[:32]`
- outcome 值变化时 key 必须变化
- 同一 outcome 多次生成 key 一致

## write_policy

- ev_write_allowed: False
- r_matrix_write_allowed: False
- g18_write_allowed: False
- z9_write_allowed: False
- D-4 只生成校准建议预览，不真实调参

## 边界声明

- auto_calibration_allowed: False
- 不真实修改 EV 权重
- 不真实修改 R-Matrix 参数
- 不真实修改 G18 规则
- 不真实写 Z9
- 不真实交易
- D-4 仅生成校准方向预览
