# DATA_FACT_LAYER v1.0 — Contract

## 输入

参考 schemas.py 中对应字段定义。

## 输出

参考对应模块输出字段定义。

## 边界

- real_trade_allowed: False
- real_z9_write_allowed: False
- external_api: disabled by default
- 数据不足时返回 degraded=True 或 INSUFFICIENT_DATA
- 不得伪造 outcome
- 不得生成交易信号
