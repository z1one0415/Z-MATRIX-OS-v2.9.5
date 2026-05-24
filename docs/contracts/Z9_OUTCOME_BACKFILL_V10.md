# Z9 Outcome Backfill v1.0 — Contract Freeze (Batch D-3)

## 输入
- Z9_INGESTION_QUEUE_ITEM v1.0

## 输出
- Z9_OUTCOME_BACKFILL_TASK v1.0

## 核心字段

| 字段 | 类型 | 说明 |
|------|------|------|
| task_version | str | "v1.0" |
| task_type | str | "Z9_OUTCOME_BACKFILL_TASK" |
| task_id | str | BF_{queue_id}_{timestamp} |
| run_id | str | 运行批次id |
| queue_id | str | 来源 queue item id |
| sample_id | str | 来源样本id |
| ticker | str | 股票代码 |
| source_queue_item | dict | 来源 queue item 快照 |
| idempotency | dict | 幂等 key 族 |
| required_market_data | dict | 回填所需行情数据定义 |
| outcome_fields | dict | T1/T5/T20 回填结果骨架 |
| state | dict | 状态机 |
| validation | dict | 校验结果 |
| write_policy | dict | 写入策略（均 False） |
| calibration_policy | dict | 校准策略（均 False） |
| forbidden_real_trade_checked | bool | True |

## required_market_data

定义未来行情数据的 pull 规格：

- horizons: ["T1", "T5", "T20"]
- required_fields: ["close_T0", "close_T1", "close_T5", "close_T20", "low_T5", "low_T20", "high_T5", "high_T20"]
- data_status: "NOT_CONNECTED"
- real_fetch_allowed: False（D-3 不真实拉行情）

## outcome_fields

填充目标（未来由 D-4/D-5 实现真实回填时写入）：

- actual_return_T1 / T5 / T20
- max_drawdown_T5 / T20
- max_runup_T5 / T20
- decision_outcome: PENDING_BACKFILL → BACKFILLED
- rule_hit_accuracy / false_positive_flags / false_negative_flags

## 状态机

| 状态 | 含义 | 入口 |
|------|------|------|
| WAITING_MARKET_DATA | 默认；等待市场数据积累 | queue item 通过验证 |
| READY_FOR_BACKFILL | 市场数据已到位，可回填 | 未来 D-4 入口 |
| BACKFILLED_PREVIEW | 回填已完成（预览模式） | 可用于测试 |
| REJECTED | 必要字段缺失 | 验证失败 |

## backfill_task_key 幂等规则

- 公式: `sha256(queue_id + sample_id + ticker + idempotency_key)[:32]`
- 同一个 queue_item 多次生成必须一致
- queue_id 或 idempotency_key 改变时必须变化
- 输出到: `idempotency.backfill_task_key`

## write_policy

- outcome_write_allowed: False（D-3 不写 outcome）
- z9_write_allowed: False（D-3 不写 Z9）
- queue_update_allowed: False（D-3 不更新 queue）
- D-3 只生成 preview

## calibration_policy

- auto_calibration_allowed: False（D-3 不校准）
- ev_calibration_allowed: False
- r_matrix_calibration_allowed: False
- g18_rule_calibration_allowed: False
- D-4 才能做参数校准自动化

## 边界声明

- D-3 不真实拉行情
- D-3 不真实写 Z9
- D-3 不真实写 queue
- D-3 不自动调参
- D-4 预留做参数校准自动化
