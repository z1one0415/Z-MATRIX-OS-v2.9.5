# Z-MATRIX-OS v2.9.5-RC

> 状态: release-ready candidate | 发布验证: contract(9/9)+core smoke(7/7)+18条manifest smoke 已接入
> 18条管线 manifest smoke 全部通过 ✅

个人量化投资操作系统 | OpenClaw 固化管线版

## 18条固化管线

```
Z-G01  数据后勤保障 (Data Service Layer)
Z-G02  前夜战报+叙事水温
Z-G03  盘中确认
Z-G04  尾盘过滤
Z-G05  日记忆卡
Z-G06  复盘反馈
Z-G07  轮动+黑马选股 (10闸口)
Z-G08  叙事雷达深度
Z-G09  全局轮动筛选 (R-Matrix全量)
Z-G10  全局黑马筛选 (D-Matrix全量)
Z-G11  组合风控
Z-G12  系统巡检
Z-G13  底仓管理 (B-Matrix+ThesisStop)
Z-G14  月度全量选股 (流A)
Z-G15  产业链深研 (V3证据分层)
Z-G16  V4纸面执行教练 (Full/Lite双模式)
Z-G16A Alpha平行验证仓
Z-G17  人类风控
```

## 核心原则

封杀越权行动 | 保留条件推理 | 禁止伪造事实 | 允许降级输出

## 运行

```bash
cd pipelines
python3 Z-G07_轮动黑马选股/gate_pipeline.py --tickers 002463 --mode watch
```
