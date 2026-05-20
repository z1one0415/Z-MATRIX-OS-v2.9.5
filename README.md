# ☯️ Z-MATRIX-OS v2.9.5-RC

> 状态: release-ready candidate | 全部测试通过
> 管线: 12条核心可执行(🟢) + 3条轻量可执行(🟢-light) + 3条原型(🟡) = 18/18入口齐全
> 注意: Z-G04/Z-G11/Z-G17 为 executable-light (有入口可运行但仍是轻量实现)
> Z-G13/Z-G14/Z-G15 为 prototype (需升级)

个人量化投资操作系统 | OpenClaw 固化管线版

## 18条固化管线

```
Z-G01  🟢        数据后勤保障 (Data Service Layer)
Z-G02  🟡        前夜战报+叙事水温
Z-G03  🟡        盘中确认
Z-G04  🟢-light  尾盘过滤 (日线volume已接入, M1尾盘待增强)
Z-G05  🟢        日记忆卡
Z-G06  🟢        复盘反馈
Z-G07  🟢        轮动+黑马选股 (10闸口, 已调用Z-G01)
Z-G08  🟡        叙事雷达深度
Z-G09  🟢        全局轮动筛选 (R-Matrix v1.1, UniverseProvider 6种universe)
Z-G10  🟢        全局黑马筛选 (D-Matrix v2.2, UniverseProvider)
Z-G11  🟢-light  组合风控 (集中度可用, 现金未接入)
Z-G12  🟢        系统巡检
Z-G13  🟢-light  底仓管理 (B-Matrix v2.1.1 5类真评分, 数据源字段待补)
Z-G14  🟢-light  月度全量选股 (B/R/D真评分, A_SHARE_ALL强制, fail-closed)
Z-G15  🟡        产业链深研 (V3证据分层 原型)
Z-G16  🟢        V4纸面执行教练 (Full/Lite双模式)
Z-G16A 🟢        Alpha平行验证仓
Z-G17  🟢-light  人类风控 (Tilt账本可用, 心理风控待增强)
```

> 🟢 = 核心可执行 / 🟢-light = 有入口可运行但轻量 / 🟡 = 原型需升级 / 🔴 = 待建


## ⚠️ 适用边界

**当前版本适用:**
- 投研分析 (Z-G09/Z-G10/Z-G13 候选池筛选)
- 纸面执行计划 (Z-G16 路线/触发/观察)
- Alpha 平行验证仓 (Z-G16A 纸面验证, 不涉及实盘)
- 盘前/盘后 系统化复盘

**当前版本不适用:**
- 自动实盘下单
- 无人工确认的买卖执行
- M1级别盘口/尾盘最终裁决 (Z-G03/Z-G04 为日线OHLCV代理)
- 完整账户级组合风控 (Z-G11 现金未接入)

> Z-G03/Z-G04: DAILY_OHLCV_PROXY, M1待接入
> Z-G10: D-Matrix v2.2已接入, Theme Seed/Micro数据仍待增强
> Z-G13: B-Matrix v2.1.1已接入, 财务全字段数据源仍为stub

## 核心原则

封杀越权行动 | 保留条件推理 | 禁止伪造事实 | 允许降级输出

## 运行

```bash
cd pipelines
python3 Z-G07_轮动黑马选股/gate_pipeline.py --tickers 002463 --mode watch
```
