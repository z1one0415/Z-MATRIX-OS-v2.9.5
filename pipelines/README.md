# 🏛️ Z-MATRIX-OS v2.9.5-RC 流程管线专用空间

> **版本**: v2.9.5-RC release-ready candidate | **18条管线**

## 管线索引

| 编号 | 名称 | 状态 | 说明 |
|:--:|------|:--:|------|
| Z-G01 | 数据后勤保障 | 🟢 | Data Service Layer, 8函数+分级TTL+降级链 |
| Z-G02 | 前夜战报+叙事水温 | 🟡 | L2.5+MacroVeto+情绪快扫 |
| Z-G03 | 盘中确认 | 🟢-light | DAILY_OHLCV_PROXY, VWAP+量比已接入; M1真实盘中待增强 |
| Z-G04 | 尾盘过滤 | 🟢-light | DAILY_OHLCV_PROXY, volume已接入; M1尾盘待增强 |
| Z-G05 | 日记忆卡 | 🟢 | 持仓追踪+MEMORY自动追加 |
| Z-G06 | 复盘反馈 | 🟢 | Z9校准+模式检测+Hermes |
| Z-G07 | 轮动+黑马选股 | 🟢 | 10闸口全量, 已调用Z-G01统一数据层, 3模式(full/lite/watch) |
| Z-G08 | 叙事雷达深度 | 🟡 | 原型 |
| Z-G09 | 全局轮动筛选 | 🟢 | R-Matrix OscillationKing v1.1 Type A/B 双模式 |
| Z-G10 | 全局黑马筛选 | 🟢 | D-Matrix v2.2 源点雷达, OHLCV enriched; Theme/Micro数据待增强 |
| Z-G11 | 组合风控 | 🟢-light | 集中度可用；现金/账户实盘数据待接入(NOT_CONNECTED) |
| Z-G12 | 系统巡检 | 🟢 | 6模块+DQ+Cron |
| Z-G13 | 底仓管理 | 🟢-light | B-Matrix v2.1.1已接入 5类真评分；数据源(get_financials)字段仍为stub |
| Z-G14 | 月度全量选股(流A) | 🟡 | B-R-D全量重跑, 原型 |
| Z-G15 | 产业链深研 | 🟡 | V3证据分层 |
| Z-G16 | V4纸面执行教练 | 🟢 | Full/Lite双模式，PAPER_PROBE conditional_output |
| Z-G16A | Alpha平行验证仓 | 🟢 | PAPER_WORLD+幽灵基准 |
| Z-G17 | 人类风控 | 🟢-light | Tilt账本可用；完整心理风控待增强 |

## 状态说明
🟢 = 核心可执行 / 契约较完整 | 🟢-light = 有入口可运行但轻量 | 🟡 = 原型 / 需升级 | 🔴 = 待建
