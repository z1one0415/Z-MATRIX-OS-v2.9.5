# 🏛️ Z-MATRIX-OS v2.9.5 系统说明书

> **版本**: v2.9.5-RC | **起草**: 2026-05-19  
> **基础**: v2.9.4-RC-Freeze | **内核**: Hermes Research Kernel  
> **宪法**: CONSTITUTION.md 7条铁律 | **管线**: 18条硬脚本  
> **文档P0/P1**: 通过 ✅ | **工程P0/P1**: 待OpenClaw固化与单元测试验证 | **release_stage**: RC  

---

## 零、系统定位

```
Z-MATRIX-OS v2.9.5 是一套个人量化投资操作系统，不是单一选股公式。

五层能力:
  事实层: Z-G01数据底盘 → SourceArbitration → EvidencePack
  体制层: TailRisk → L2.5/L3 → (L5后)Hibernation
  角色层: B-Matrix → R-Matrix → D-Matrix → OscillationKing  
  裁决层: L1.6(反身性) → Z8(组合裁决) → L1.5(执行安全) → SafetyLock
  验证层: PaperExec → Backtest → Attribution → Z9 → HumanLedger

最终不输出"马上买入"，只输出 ActionProposal 行动提案。
```


---

## 开放智能系统降级输出原则 (v2.9.5-RC)

Z-MATRIX 运行在 OpenClaw + LLM 的开放智能环境。**系统不得将普通数据缺失等同于全局无效。**

### 核心范式: 封杀越权行动，不封杀智能输出

```
旧范式: 数据缺 → BLOCK → 管线停止 → LLM沉默
新范式: 数据缺 → Capability Mask → 能力降级 → LLM继续输出条件结论
```

### 5级输出权限

| 等级 | 名称 | 条件 | 允许 |
|:--:|------|------|------|
| O5 | EXECUTABLE | 全数据就绪 | 完整ActionProposal (需HumanConfirm) |
| O4 | PAPER_PLAN | DQ≥85+MT.PASS+L1.5.SAFE+role_valid+world=PAPER_WORLD+TailRisk非DEFENSIVE | Z-G16 Full, PAPER_TRACK, 条件满足后PAPER_PROBE |
| O3 | CONDITIONAL | DQ≥60, MT PASS/DEGRADED | 条件路线, 信号点, 无精确价格/仓位 |
| O2 | DIAGNOSTIC | MT BLOCK或DQ<60 | 诊断, 缺口, 可能性, 非价格条件路线 |
| O1 | DATA_GAP | 关键数据不可用 | 数据缺失说明, 修复建议 |

### Capability Mask (替代旧PASS/DEGRADED/BLOCK)

```json
{
  "output_level": "O3_CONDITIONAL",
  "disabled_capabilities": ["exact_price_zone", "paper_fill_price"],
  "allowed_outputs": ["conditional_routes", "gap_report", "watch"],
  "forbidden_actions": ["PAPER_PROBE", "HUMAN_CONFIRM_PROBE"]
}
```

**每个闸口不再只输出PASS/FAIL, 而是输出能力掩码。**

### 三类BLOCK拆分

| BLOCK类型 | 含义 | 禁止 | 仍允许 |
|------|------|------|------|
| BLOCK_ACTION | 禁止行动 | ActionProposal, PAPER_PROBE | 诊断报告, 条件路线 |
| BLOCK_PRICE | 禁止价格 | 价格区间, fill_price | 定性路线, WATCH |
| BLOCK_PIPELINE | 管线异常 | 停止workflow | 错误报告, 修复建议 |

### 数据缺失降级表

| 缺失 | 禁止 | 仍允许 |
|------|------|------|
| 实时价格 | 精确价格区间, fill_price | 定性报告, 条件路线 |
| 多源冲突>1% | ActionProposal, 纸面成交 | 冲突报告, WAIT |
| M1分钟线 | D3, FalsePreheat | D1/D2 WATCH |
| Level-2 | 盘口承接, 黑洞确认 | M1/日线分析 |
| 股息率 | B1高股息分类 | B2/B3/B4/B5 |
| DQ<60 | ActionProposal | DIAGNOSTIC_ONLY + 条件路线 |

### 可回调的过度规则 (5条)

| # | 旧规则 | 回调为 |
|:--:|------|------|
| 1 | MT DEGRADED→禁止Z-G16 | 禁Z-G16 Full, 允许Z-G16 Lite(条件路线+缺口) |
| 2 | DQ<85→禁Z-G16 Full, 允Z-G16 Lite | 禁price_zones/position/PAPER_PROBE, 允许条件路线 |
| 3 | PAPER_PROBE跨world→DIAGNOSTIC_ONLY | →PAPER_TRACK + CREATE_PAPER_WORLD_PLAN |
| 4 | 跳过≥2闸口→不落盘 | 不作为有效投资样本落盘, 必须作为DataGapEvent落盘 |
| 5 | Z-G16A必须execution_quote | execution→高置信, realtime_fallback→degraded_fill |

### 不可回调的硬边界

```text
✅ FORBIDDEN_ACTIONS: BUY/SELL/AUTO_TRADE → PolicyViolation
✅ raw/adjusted 不得混用
✅ 未知动作 → DIAGNOSTIC_ONLY (不背书)
✅ SourceArbitration 不覆盖 MarketTruth 状态
✅ PAPER_ENTER 永不复用
✅ promote_candidate ≠ 实盘晋级
```

### Z-G16 Full vs Lite

```
Z-G16 Full (O4): 8模块完整 | DQ≥85+MT PASS+L1.5 SAFE+role_valid
Z-G16 Lite (O3/O2): route_hypotheses+signal_conditions+evidence_gaps+waiting_triggers | 禁price_zones/position/PROBE/fill
  8模块完整: 路线+价格区间+仓位+信号+Kill/Rollback+复盘

Z-G16 Lite (O3/O2, DQ<85或MT DEGRADED/BLOCK):
  仅输出: 路线假设+信号条件+缺口清单+等待触发器
  不输出: 价格区间, 仓位节奏, PAPER_PROBE
```

### LLM允许/不允许

```
✅ 允许: 组织事实报告, 生成条件路线, 标记可能性, 补全数据清单
❌ 禁止: 编造价格/成交量/财务/盘口/股息率/fill_price
```

冻结句: **LLM不能替数据撒谎，但可以在数据不完整时继续做有边界的推理、解释和条件规划。**


---

## 一、系统全景图

```
┌──────────────────────────────────────────────────────────┐
│                    Z-MATRIX-OS v2.9.5                    │
│                                                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │
│  │  Z2 天师     │  │  Z8 神算子   │  │  Z9 后验     │      │
│  │  研究主导    │  │  组合裁决    │  │  校准学习    │      │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘      │
│         │                │                │              │
│  ┌──────┴────────────────┴────────────────┴──────┐      │
│  │              18条固化管线 (Z-G01~Z-G17共17条主管线 + Z-G16A Alpha平行验证仓) (硬脚本)              │      │
│  │  Z-G01~Z-G17  |  通过Z-G01 Data Service (z17_loader) 获取 EvidencePack (非脚本import依赖)    │      │
│  └──────────────────────┬────────────────────────┘      │
│                         │                                │
│  ┌──────────────────────┴────────────────────────┐      │
│  │           Z-G01 数据后勤保障 (底层)             │      │
│  │   execution: broker/exchange→fallback | research: tencent/sina | historical: baostock/tushare | financial: exchange/tushare/baostock        │      │
│  │   8函数 + 分级缓存(TTL:3s~7d) + 降级链         │      │
│  └───────────────────────────────────────────────┘      │
├──────────────────────────────────────────────────────────┤
│  允许: SAFE_ACTIONS白名单内ActionProposal (11种)
│  禁止: FORBIDDEN_ACTIONS与任何TradeOrder         │
│  禁止: 自动买入/重仓/无条件加仓/清仓/自动下单              │
└──────────────────────────────────────────────────────────┘
```

### 数据流

```
Z-G01 数据底盘 (始终运行)
  ↓ 喂数据给所有管线
  
Z-G09 R_POOL(每周全量+每日增量) + Z-G10 D_POOL(每日轻量+每周全量)
  ↓ 候选池供给

Z-G02 (盘前) → Z-G03 (盘中) → Z-G04 (尾盘) → Z-G05 (日卡) → Z-G06 (复盘)
  ↓ 每日运行链

Z-G07 (按需选股) ← Z-G09/Z-G10候选池
Z-G13 (底仓) + Z-G14 (月度) → 持仓管理
Z-G16 (纸面) + Z-G17 (人类风控) → 安全验证
```

---

## 二、AGENT角色定义

### Z2天师 (主Agent)
```
角色: 产业链深度研究员 + 证据分级裁判
职责:
  ✅ 产业链研究 (V3证据分层)
  ✅ 财务8硬门分析
  ✅ 催化剂日历维护
  ✅ 搜索结果计划生成
  ❌ 不输出买卖指令
  ❌ 不连接真实交易接口
  ❌ 不把市场传闻当事实

方法论:
  先判主线 → 后拆链条 → 先看证据 → 后看题材
  先过财务 → 后谈估值 → 先分仓位 → 后排节奏
```

### Z8神算子 (组合裁决)
```
角色: 批量组合裁决引擎
职责:
  ✅ 接收 B/R/D/OKR 角色评分
  ✅ 输出: ActionProposal(action∈SAFE_ACTIONS, output_level, capability_mask, reason_codes, required_next_data)
  ✅ 组合集中度检查
  ✅ 闸口状态 → 动作降级
  ❌ 不自动下单
  ❌ 不绕过安全锁

动作语义:
  WATCH         观察
  WAIT          等待条件触发
  PAPER_TRACK   纸面追踪 (不生成模拟订单)
  PAPER_PROBE   纸面试仓 (PAPER_WORLD内, 生成PaperOrder)
  BLOCK_ENTER   禁止新增/开仓 (非管线阻断, 仍允许HOLD/REDUCE/HARVEST/CANCEL/DIAGNOSTIC/条件路线)
  HOLD          继续持有
  REDUCE_RISK   风险降低建议
  HARVEST       波段收割观察
  CANCEL_PLAN   取消计划
  HUMAN_CONFIRM_PROBE 人工确认后试探, 不自动执行
  DIAGNOSTIC_ONLY     仅诊断, 不输出行动提案
```

### Z9后验 (校准学习)
```
角色: 后验校准仪表盘
职责:
  ✅ 统计命中率/收益/置信区间
  ✅ 参数调优建议
  ✅ 人类Override收益统计
  ✅ 样本不足不调参
  ❌ 不凭单次大赚/大亏改宪法
```

---

## 三、18条管线运行逻辑

### 每日时间轴

| 时间 | 管线 | 输入 | 输出 | 用途 |
|:--:|------|------|------|------|
| 08:00 | Z-G02 前夜战报 | L2.5+宏观 | 今日风向+叙事水温 | 决定今天能不能进攻 |
| 09:25-10:30 | Z-G03 盘中确认 | 0925竞价/0935承接/0945确认/1030过期 | L3分时确认 | 确认前夜预测是否被市场承认 |
| 14:30监控 | Z-G04 尾盘监控 | LateDayAnomaly+收盘最终判定 | FalsePreheat/SmartMoney | 防尾盘画图/假突破 |
| 15:30 | Z-G05 日记忆卡 | 持仓+快照 | MEMORY.md追加 | 固化全天记忆 |
| 16:00 | Z-G06 复盘反馈 | 预测vs实际 | Z9校准记录 | 对账/打脸/学习 |

### 每周运行

| 管线 | 功能 | 输出 |
|------|------|------|
| Z-G08 叙事深度 | L1.6+主题周期 | 情绪阶段/防叙事裹挟 |
| Z-G09 全局轮动 | R-Matrix全量+每日增量 | R_POOL (≤80) |
| Z-G10 全局黑马 | D-Matrix每日+每周全量 | D_POOL (D1~D3) |
| Z-G11 组合风控 | 集中度+因子 | 风险警告 |
| Z-G12 系统巡检 | 6模块健康 | DQ趋势+Cron |

### 每月/按需

| 管线 | 功能 | 触发 |
|------|------|------|
| Z-G07 轮动黑马 | 10闸口选股 | 用户指定标的 |
| Z-G13 底仓管理 | ThesisStop | 每月+财报 |
| Z-G14 月度全量(流A) | B-R-D全量重跑 | 每月1次 |
| Z-G15 产业链深研 | V3证据+8硬门 | 按需 |
| Z-G16 V4纸面执行教练 | 8模块:current_state/scenario_route/price_zone/position/signal/checkpoint/kill_rollback/posterior | 每提案后 |
| Z-G17 人类风控 | Tilt检测+账本 | 每次覆盖 |

---

## 四、全量功能模块目录

```
zmatrix/scoring/
├── b_matrix/          B-Matrix 底仓资格 (v2.1.1)
│   ├── contracts.py        BMatrixInput/BMatrixResult
│   ├── b_matrix_dispatcher  evaluate_b_matrix()
│   ├── pricers/            5类定价器 (B1~B5)
│   ├── quality_trap/       质量陷阱检测
│   ├── thesis_stop/        ThesisStop引擎
│   └── moat_analyzer/      护城河评分
├── d_band/            D-Matrix 黑马雷达 (v2.2)
│   ├── d_early_v22_scorer  主评分器
│   ├── blackhorse_gene     黑马基因 (22%)
│   ├── sector_ignition     板块点火 (18%)
│   ├── silent_accumulation 静默吸筹 (18%)
│   └── micro_absorption    微观吸收 (10%)
├── r_matrix/          R-Matrix 轮动评分 (v1.1)
│   ├── oscillation_king    波动天王
│   ├── rising_channel      上升通道检测
│   └── bear_trap           熊陷阱检测
│
pipelines/           18条固化管线 (Z-G01~Z-G17共17条主管线 + Z-G16A Alpha平行验证仓) (全部硬脚本)
├── Z-G01~Z-G17/     gate_pipeline.py + README
│
scripts/             辅助脚本
├── predict_engine.py     超级预测引擎
├── v3_scenario_engine.py V3情景推演
├── trader_calibration.py 交易校准
├── data_adapter.py       Tushare适配器
└── realtime_quote.py     实时行情
│
hermes/              Hermes研究内核
├── memory_bank.py        记忆库
├── narrative_radar.py    叙事雷达
├── Z9_Calibration.py     Z9校准
├── daily_card.py         日卡生成
├── l25_alchemist.py      L2.5信息熔合
└── mflow_auto_sync.py    M-FLOW同步
```

---

## 五、核心安全规则

### 闸口 → 动作映射

```
Market Truth BLOCK: has_partial_evidence=true→O2_DIAGNOSTIC(price_conflict/stale/source_disagreement); has_partial_evidence=false→O1_DATA_GAP(no_quote/no_price_basis/all_sources_down)
Market Truth DEGRADED → O3_CONDITIONAL: max_executable=none, 禁价格/fill/PROBE, 允许WATCH/WAIT/TRACK/Z-G16 Lite/gap_report (DQ不覆盖MT降级)
DQ < 60             → DIAGNOSTIC_ONLY (不输出ActionProposal, 不进Z8)
DQ < 85 → 禁Z-G16 Full(price_zones/position/PROBE); 允Z-G16 Lite(条件路线+信号+缺口)
Source Arbitration BLOCK → 禁止使用 selected quote
ST: action=BLOCK_ENTER, 允许诊断/条件路线 | 停牌/无成交: output_level=O2_DIAGNOSTIC, disabled=[paper_fill,execution_price,reduce_risk_execution], 允许holding_status_note/data_gap_report
TailRisk BLACK_SWAN → operating_mode=DEFENSIVE_ONLY (不是action) (允许HOLD/REDUCE_RISK/CANCEL/DIAGNOSTIC, 禁PROBE/HUMAN_CONFIRM)

跳过: C1/C2闸口→允许条件输出 | C3→禁Full允Lite | C4/C5→禁ActionProposal/PROBE/fill
跳过≥2闸口 → 禁系统背书+禁收益统计; 必须落盘DataGapEvent
```

### 模块禁用条件

```
D-Matrix 无 M1      → lifecycle_max = D2_PREHEAT
B-Matrix 缺股息     → 禁用 B1高股息分类
L1.5 无 Level-2     → 不得声称盘口承接
L2.5 超过 10:30     → 不再作为动作依据
Hibernation ON → 停D/R进攻扫描+PAPER_PROBE; 保留Z-G01/Z-G02/Z-G03哨兵/Z-G11/Z-G13/Z-G17/唤醒条件扫描
PortfolioRisk 超限  → Z8 不得升级动作
Human Tilt 触发     → 需要 Confession + 降低背书
```

### 安全锁 (v2.9.5-RC)

```python
SAFE_ACTIONS = {
    "WATCH","WAIT","PAPER_TRACK","PAPER_PROBE",
    "HUMAN_CONFIRM_PROBE","HOLD","REDUCE_RISK",
    "HARVEST","BLOCK_ENTER","CANCEL_PLAN","DIAGNOSTIC_ONLY"
}
FORBIDDEN_ACTIONS = {
    "BUY","SELL","ADD","CLEAR","MARKET_ORDER","AUTO_TRADE","PAPER_ENTER"
}

if action in FORBIDDEN_ACTIONS:
    raise PolicyViolation("Forbidden direct trade action")
if action not in SAFE_ACTIONS:
    action = "DIAGNOSTIC_ONLY"  # 未知动作→诊断, 不背书为WATCH
if action == "PAPER_PROBE" and world != "PAPER_WORLD":
    action = "PAPER_TRACK"
    required_transition = "CREATE_PAPER_WORLD_PLAN"
    disabled_capabilities = ["paper_order","fill_price"]
```

冻结: ActionProposal only, never TradeOrder。未知动作→DIAGNOSTIC_ONLY。PAPER_PROBE仅限PAPER_WORLD。

---

## 六、数据流与降级链

### 数据源优先级 (按用途分层, P0-1已修复 ✅)

| 用途 | 优先级1 | 优先级2 | 优先级3 | 退化 |
|------|------|------|------|------|
| execution_quote | broker/exchange | tencent/sina fallback | — | DEGRADED |
| realtime_research | tencent | sina | local_cache | DEGRADED |
| historical_research | baostock | tushare | local_cache | — |
| financial_statement | exchange_report | tushare | baostock | manual_verified |
| event_news | official | exchange_notice | trusted | llm_summary |

冻结: Sina/Tencent可作研究fallback, 不得作为执行价格最高真相源。执行价最高优先级只能是broker/exchange/Level-2 raw price。

### 缓存TTL分级

```yaml
cache_ttl:
 realtime_quote: 3s           # L1.5/L3/PaperExec (超时→DEGRADED)
 intraday_m1_bar: 60s
 sector_snapshot: 30s
 l25_frontnight: 30m
 financial_statement: 1d
 b_matrix_profile: 7d
 event_calendar: 1h
```

### 缓存TTL参数表 (P0-4已实现 ✅)

| 数据类型 | TTL | 适用场景 | 超时动作 |
|------|:--:|------|------|
| realtime_quote | 3s | L1.5/L3/PaperExec/尾盘 | DEGRADED |
| intraday_m1_bar | 60s | 分钟K线 | 使用日K回退 |
| sector_snapshot | 30s | 31板块快照 | DATA_INCOMPLETE |
| l25_frontnight | 30m | L2.5宏观输入 | 使用上次缓存 |
| financial_statement | 1d | 财报数据 | 使用上次数据 |
| b_matrix_profile | 7d | B-Matrix静态画像 | 使用上次评分 |
| event_calendar | 1h | 事件日历 | 标记过期 |

冻结: L1.5/L3/PaperExecution价格数据TTL≤5秒, 超时自动DEGRADED。

### 价格仲裁规则

```
**硬规则**: Market Truth只允许raw/unadjusted价格互相交叉验证。
前复权/后复权/adjusted research price不得参与execution_quote的价格一致性判断。
_bs_raw_kline: adjustflag=3 (不复权) — 仅用于execution_price/raw口径校验
_bs_research_kline: adjustflag=2 (前复权) — 仅用于均线/R-Matrix/历史形态

同报告单源单时点
diff ≤ 0.30% → PASS | 0.30% < diff ≤ 1.00% → DEGRADED | diff > 1.00% → BLOCK (execution_quote)
realtime_research: diff ≤ 0.50% → PASS | 0.50% < diff ≤ 1.50% → DEGRADED | diff > 1.50% → BLOCK
historical_research: diff ≤ 1.00% → PASS | 1.00% < diff ≤ 3.00% → DEGRADED | diff > 3.00% → BLOCK
冻结: 禁止raw vs adjusted跨口径比较。market_truth.diff_pct只能在同price_basis内计算。
单源无交叉→承接MT.status(不二次裁决)
无可用价格 → BLOCK
```

### DQ六维评分

```
行情:    15 (交叉验证) / 12 (有价) / 6 (无价)
财务:    22 (有利润数据) / 8 (无)
估值:    12 (有价) / 5 (无)
产业链:  12 (有Q1) / 10 (无)
资金:    13 (量+交叉) / 10 (有量) / 3 (无)
来源:    13 (交叉) / 6 (有价) / 3 (无)
───────────────────────────────
≥85: DQ_PASS (只解除DQ限制, 不得覆盖MT/L1.5/TailRisk/Hibernation; 仍需MT PASS+L1.5 SAFE+role_valid)
≥60: WATCH
<60: DIAGNOSTIC_ONLY (不输出ActionProposal, 不进Z8, 不生成Z-G16)
```

---

## 七、版本升级轨迹

```
v2.9.3: B/D/R Matrix 三维评分矩阵上线
v2.9.4: LangGraph 16Node流+全量数据库+多场景Playbook (base)
v2.9.5: 18条管线全部固化为硬脚本
        ├ 流A定位修正: 每日日报 → 月度全量B-R-D重跑
        ├ 10闸口强制执行 (绕过LLM语义)
        ├ Z-G01数据底盘统一供给
        ├ 全管线通过数据服务层获取 (无嵌入式拉取)
        ├ Source Arbitration 集中裁决
        ├ 安全锁: ActionProposal only | PAPER_PROBE仅限PAPER_WORLD | 跨world→DIAGNOSTIC_ONLY | 未知→DIAGNOSTIC_ONLY | FORBIDDEN→PolicyViolation
        └ 叙事水温合并到 Z-G02 盘前
```

---

## 八、系统运行自评估

```
## 八、系统运行自评估 (2026-05-19 系统化自检)

```
══════════════ 自检结果 ══════════════

管线完整性:   18/18 ✅ (全部有gate_pipeline.py)
语法检查:     18/18 PASS ✅
版本一致性:   v2.9.5-RC 55处引用 ✅
禁止词:       PAPER_ENTER=0 | 8因子=0 | 立即买入=0 ✅
──────────────────────────────────────
数据源:       Sina ✅ | baostock ✅ | Tushare ⬇️
价格验证:     status=PASS | cross_validated=True | price_basis=raw_unadjusted | 002463:102.6 ✅
板块数据:     PASS ✅
──────────────────────────────────────
记忆宫殿:     171个.md文件
DQ趋势:       87 (样本002463)
持仓:         3只 | 双环传动/紫金矿业/科创50ETF
持仓风险:     ⚠️ 双环68%集中度过高
──────────────────────────────────────
管线脚本:     18个gate_pipeline.py, z17_loader统一入口
语法:         18/18 零错误
宪法合规:     7条铁律 + 10闸口 + SAFE_ACTIONS
安全锁:       PAPER_PROBE仅限PAPER_WORLD
蓝军审核:     文档P0/P1通过 ✅ (代码待OpenClaw单元测试) (5P0+5P1 final cleanup) (raw/adjusted分离+仲裁统一+安全锁修正+Z-G16展开)
──────────────────────────────────────
系统状态:     v2.9.5-RC (文档P0/P1通过)
阶段:       RC测试 → Freeze
```
```

---

## 九、全量功能模块与决策逻辑 (完整版)


## Z-G01 数据后勤保障 (Data Service Layer) — raw/ research双口径 — 10模块


## 模块: _sina_quote_research_fallback (Z-G01 gate_data.py:21)

  位置: realtime_research fallback (非execution_quote最高事实源)
  输入: ticker:str — 6位股票代码 (如"002463")
  输出: dict{price:float, open:float, high:float, low:float, volume:str, name:str, source:"sina_api", time:str}
        | dict{error:str} — 拉取失败
  参数: 
    prefix = "sz" if ticker[0] in ("0","3") else "sh"  # 深市/沪市前缀
    url = f"http://hq.sinajs.cn/list={prefix}{ticker}"  # Sina行情接口
    headers = {"Referer":"https://finance.sina.com.cn"}  # 防反爬
    timeout = 5秒  # 超时阈值
  决策: 返回""或价格=""→error:"empty"; parts长度<32→error:"invalid"

模块: _bs_raw_kline (独立) / _bs_research_kline (独立) — 非同一函数参数切换 (Z-G01 gate_data.py:36/40)
  位置: baostock日K线数据源
  输入: ticker:str, days:int=10 — 回看天数
  输出: dict{prices:[{date, close}]} | dict{error}
  参数:
    code = f"{prefix}.{ticker}"  # baostock格式 (sz.002463)
    adjustflag="2"  # 前复权 (仅research_price, raw用adjustflag=3)
    start = (now - timedelta(days=days)).strftime("%Y-%m-%d")
    frequency="d"  # 日线
  决策: close>0且非空→有效K线; prices为空→error:"no_data"

模块: _bs_finance (Z-G01 gate_data.py:52)
  位置: baostock财务数据源
  输入: ticker:str
  输出: dict{q1_eps:str|None, has_finance:bool, industry:str}
  参数:
    query_profit_data(code, year=2026, quarter=1)  # 最近Q1
    回退: (2025,4) → (2025,3)  # 如Q1未出则查上季度
    query_stock_industry(code)  # 证监会行业分类
  决策: r[3] not in ("","0","0.000000") → has_finance=True

模块: _bs_l4 (Z-G01 gate_data.py:77)
  位置: L4个股健康检查
  输入: ticker:str
  输出: dict{name:str, tradable:bool, is_st:bool, errors:list}
  参数:
    query_stock_basic(code) → 名称+ST检测
    "ST" in name.upper() → is_st=True
    近5日成交量>0 → tradable=True
  决策: is_st→BLOCK; tradable=False→BLOCK(可能停牌)

模块: market_truth (Z-G01 gate_data.py:102)
  位置: 闸口① Market Truth
  输入: ticker:str
  输出:
```json
{
  "status": "PASS|DEGRADED|BLOCK",
  "output_level": "O5|O4|O3|O2|O1",
  "price": null,
  "price_basis": "raw_unadjusted|adjusted_research",
  "quote_domain": "execution_quote|realtime_research|historical_research",
  "capability_mask": {
    "allowed_outputs": [],
    "disabled_capabilities": [],
    "forbidden_actions": [],
    "required_next_data": []
  },
  "cross_validated": false,
  "price_conflict": false,
  "source_diff_pct": null,
  "selected_sources": [],
  "errors": []
}
```
原字段:
            price_conflict:bool, source_diff_pct:float, errors:list}
  参数:
    CACHE_TTL = 3s (realtime_quote) / 按域分级见第六章
  决策:
        仅允许同一price_basis内比较(raw vs raw, adjusted vs adjusted, 禁止跨口径)
        execution_quote: ≤0.30%→PASS | 0.30-1.00%→DEGRADED | >1.00%→BLOCK
        realtime_research: ≤0.50%→PASS | 0.50-1.50%→DEGRADED | >1.50%→BLOCK
        historical_research: ≤1.00%→PASS | 1.00-3.00%→DEGRADED | >3.00%→BLOCK
        MT.PASS→可用 | MT.DEGRADED→降级使用 | MT.BLOCK→禁止

模块: source_arbitrate (Z-G01 gate_data.py:124)
  位置: 闸口② Source Arbitration
  输入: ticker:str, g1:dict(market_truth输出)
  输出: dict{status, price, source, price_basis, quote_domain, output_level, capability_mask, cross_validated, selected_sources, errors}
  决策: 只承接market_truth.status, 不重新计算PASS/DEGRADED/BLOCK
        透传output_level+capability_mask+price_basis+quote_domain; MT.PASS→best_quote | MT.DEGRADED→fallback | MT.BLOCK→None
        冻结: source_arbitrate不得根据price_conflict二次升级/降级


模块: dq_score (Z-G01 gate_data.py:129)
  位置: 闸口③ Data Quality评分
  输入: ticker:str
  输出: dict{status, total:int, breakdown:{6维}, q1_eps, industry}
  参数:
    行情: 15(cross) / 12(有价) / 6(无价)
    财务: 22(有利润) / 8(无)
    估值: 12(有价) / 5(无)
    产业链: 12(有Q1EPS) / 10(无)
    资金: 13(量+cross) / 10(有量) / 3(无)
    来源: 13(cross) / 6(有价) / 3(无)
  决策: total<60→DQ_FAIL/DIAGNOSTIC_ONLY; total<85→DEGRADED; total≥85→PASS

模块: l4_health (Z-G01 gate_data.py:143)
  位置: 闸口⑥ L4健康
  输入: ticker:str
  输出: dict{status, name, tradable, errors}
  决策: ST→BLOCK; 无成交→BLOCK; 有错误→DEGRADED; 干净→PASS

模块: get_kline (Z-G01 gate_data.py:150)
  位置: K线数据获取
  输入: ticker:str, n:int=60 — 需求日数
  输出: dict{status, prices:[float], count:int}
  参数: 实际拉取max(n+10, 70)日以保证充足
  决策: count≥min(n,20)→PASS; 否则→DEGRADED

模块: l25_macro (Z-G01 gate_data.py:179)
  位置: 闸口④ L2.5宏观填充度
  输入: 无 (读取MEMORY.md)
  输出: dict{status, filled:int, total:8, domains:dict}
  参数: 8信息域(risk/china/overseas/chip/gold/fx/policy/commodity)
  决策: filled≥4→PASS; <4→DEGRADED

## Z-G02 前夜战报 — 7个最小功能模块


## 模块: fetch_all_assets (Z-G02 gate_pipeline.py:103)

  位置: 隔夜全球资产拉取
  输入: 无
  输出: dict[str,dict] — 每个资产{price, change_pct, source}
  参数:
    资产列表: VIX, SOX, KWEB, 黄金(XAU), 铜, US10Y, CNH, A50
    数据源: web_fetch(hq.sinajs.cn) + web_search作为备源
  决策: change_pct>2%→重点关注; >5%→MacroVeto触发

模块: fetch_overnight_news (Z-G02 gate_pipeline.py:119)
  位置: 隔夜快讯采集
  输入: max_items:int=20
  输出: list[dict{title, source, time, keywords}]
  参数: web_search新鲜度=day, topic=news, 最大20条
  决策: 按关键词去重→按板块分类(算力/机器人/宏观/地缘)

模块: quick_sentiment_scan (Z-G02 gate_pipeline.py:159)
  位置: 叙事水温快扫
  输入: news:list[dict]
  输出: dict{heat_map:{主题:热度}, concentration:float, verdict:str}
  参数:
    5大主题: AI算力/机器人/半导体/周期资源/消费
    热度 = 关键词命中数 / 总新闻数 × 10(标准化到0-10)
    集中度 = 最热主题热度 / sum(所有热度)
  决策: concentration>0.6→MANIA_ALERT; >0.8→TILT_BLOCK; 正常→NORMAL

模块: run_macro_veto (Z-G02 gate_pipeline.py:202)
  位置: MacroVeto 8信息域定向冲击
  输入: assets:dict, macro_data:dict, news:list
  输出: dict{veto_triggers:list, risk_level:str, actionable_chains:list}
  参数:
    8信息域: 地缘/CPI/利率/流动性/VIX/能源/供应链/汇率
    每个因子: 从MEMORY.md MACRO字典 + assets + news综合判定
  决策: ≥3因子🔴→不开新仓; ≥5→operating_mode=DEFENSIVE_ONLY (不是action) (allowed:[HOLD,REDUCE_RISK,CANCEL,DIAGNOSTIC]; forbidden:[PROBE,HUMAN_CONFIRM]); 0-2→PASS

模块: _generate_interpretation (Z-G02 gate_pipeline.py:414)
  位置: 天师解读生成
  输入: veto:dict, assets:dict, news:list, sentiment:dict
  输出: str — 因果链+板块传导+趋势方向
  参数: 无硬编码参数
  决策: 顺风被否决→不得解释为低吸; 逆风+板块强→人工标记

## Z-G03 盘中确认 — 4个最小功能模块


## 模块: _auction_snapshot (Z-G03 gate_pipeline.py:23)

  位置: 竞价快照
  输入: ticker:str
  输出: dict{ticker, name, open, price, gap_pct, source}
  参数: gap_pct = (open/prev_close-1)*100  # 集合竞价缺口%
  决策: gap>2%→高开关注; gap<-2%→低开警惕

模块: _vwap_check (Z-G03 gate_pipeline.py:41)
  位置: VWAP站稳检测 (简化版: 价格vs开盘)
  输入: ticker:str
  输出: "ABOVE_OPEN" | "BELOW_OPEN"
  参数: price >= open → ABOVE_OPEN
  决策: ABOVE_OPEN→确认信号; BELOW_OPEN→否决信号

模块: _volume_ratio (Z-G03 gate_pipeline.py:49)
  位置: 量比计算
  输入: ticker:str
  输出: float — 当前量/5日均量
  参数: 取最近20日K线的最后6根
  决策: >1.5→放量; 0.8-1.2→中性; <0.5→缩量

## Z-G04 尾盘过滤 — 2个最小功能模块


## 模块: _tail_30min_analysis (Z-G04 gate_pipeline.py:21)

  位置: 尾盘30分钟异常分析
  输入: ticker:str
  输出: dict{type, ticker, reason, action}
  参数:
    today_chg = (现价/开盘-1)*100  # 日内涨幅
    vol_ratio = 今日量/5日均量
    FALSE_PREHEAT阈值: chg>3% AND vol_ratio<0.7  # 缩量尾盘拉升
    SMART_MONEY阈值: chg>2% AND vol_ratio>1.5    # 放量逆势抢筹
  决策:
    FALSE_PREHEAT→冷却3交易日, lifecycle≤D2_PREHEAT
    SMART_MONEY→次日L3确认, 禁止当日追入
    NORMAL→正常流程

## Z-G05 日记忆卡 — 5个最小功能模块


## 模块: parse_positions_from_memory (Z-G05 gate_pipeline.py:55)

  位置: 持仓解析
  输入: memory_path:Path → MEMORY.md
  输出: list[dict{code, name, shares, cost, price_last, pnl}]
  参数: 正则r'\|\s*([^|]+?)\s+(\d{6})\s*\|\s*([\d,]+股)\s*\|\s*([\d.]+)\s*\|'
  决策: 解析失败→返回空列表(人工校对MEMORY.md格式)

模块: fetch_live_prices_for_positions (Z-G05 gate_pipeline.py:97)
  位置: 实时价格批量拉取
  输入: positions:list[dict]
  输出: dict[str,dict{name, price, pct, high, low, open, volume}]
  参数: 东方财富push2 API, secid格式("0.002463"或"1.688608")
  决策: 单只失败→用最近已知价; 全失败→降级

模块: get_market_snapshot (Z-G05 gate_pipeline.py:130)
  位置: 大盘快照
  输入: 无
  输出: dict{000001:{name,price,pct}, 399001:{}, 399006:{}}
  参数: 上证/深证/创业板 三指数

模块: _generate_daily_card_md (Z-G05 gate_pipeline.py:346)
  位置: 日记忆卡Markdown生成
  输入: date_str, snapshot, catalysts, _result
  输出: str — 完整Markdown日卡
  参数: 模板包含: 今日市场/持仓追踪/催化剂状态/今日操作/场景

模块: _auto_append_memory (Z-G05 gate_pipeline.py:433)
  位置: MEMORY.md自动追加
  输入: result, date_str, daily_card_md
  输出: 无 (副作用: 修改MEMORY.md)
  参数: Z-END-OF-DAY-MARKER 作为替换定位标记

## Z-G06 复盘反馈 — 4个最小功能模块


## 模块: _compute_accuracy (Z-G06 gate_pipeline.py:100)

  位置: 准确率计算
  输入: today:str
  输出: dict{summary:{总预测数,正确数,拒绝率,遗漏因子,滑点}, calibrated:bool}
  参数: min_samples_for_z9=50  # Z9启用最低样本数
  决策: 样本<50→标uncalibrated, 不可用于Z9调参

模块: _detect_patterns (Z-G06 gate_pipeline.py:115)
  位置: 异常模式检测
  输入: tickers:list, today:str
  输出: list[dict{type, ticker, reason}]
  参数:
    chg = (prices[-1]/prices[-2]-1)*100  # 当日涨跌%
    chg > 9.5 → SLIPPAGE(涨停滑点)
    chg < -9.5 → REJECTION(跌停否决)
  决策: 无异常→返回NORMAL标记

模块: _z9_attribute (Z-G06 gate_pipeline.py:131)
  位置: Z9偏差归因
  输入: patterns, accuracy
  输出: dict{primary_bias, driver, calibration_note}
  参数: 样本不足→不输出归因, 仅记录

模块: _hermes_input (Z-G06 gate_pipeline.py:139)
  位置: Hermes学习输入
  输入: attribution, patterns
  输出: dict{lesson, memory_candidates, approval_required}
  参数: memory_candidates = [{"type":p["type"],"ticker":p["ticker"],"note":p["reason"]}]
  决策: 有严重模式→mark approval_required=True

## Z-G07 轮动黑马 — 10个独立闸口模块


## 模块: gate1_market_truth (Z-G07 gate_pipeline_v1.0.py:72)

  输入: ticker:str
  输出: GateResult
  决策: 同Z-G01.market_truth

模块: gate2_source_arbitration (Z-G07:150) — 调用Z-G01.source_arbitrate, 只承接MT.status, 不二次裁决
  输入: ticker, g1_details:dict
  输出: GateResult
  调用Z-G01.source_arbitrate; 承接MT.status/output_level/capability_mask; 不私造仲裁

模块: gate3_dq_score (Z-G07:167)
  输入: ticker
  输出: GateResult{dq_score}
  参数: 6维评分权重同Z-G01
  决策: total<60→DQ_FAIL/DIAGNOSTIC_ONLY; total<85→DEGRADED; ≥85→PASS

模块: gate4_l25_macro (Z-G07:221)
  输入: 无 (读MEMORY.md)
  输出: GateResult
  参数: 8信息域关键词扫描
  决策: filled≥4→PASS

模块: gate5_l3_sectors (Z-G07:254)
  输入: 无
  输出: GateResult
  参数: 新浪5指数快照(上证/深证/创业板/科创50/沪深300)
  决策: ≥3可用→PASS

模块: gate6_l4_health (Z-G07:278)
  输入: ticker
  输出: GateResult
  参数: ST检查+近5日成交
  决策: ST/停牌→BLOCK→后续闸口全SKIP

模块: gate7_l5_matrix (Z-G07:329)
  输入: ticker, g1_details
  输出: GateResult{d_score, r_score}
  参数:
    D-Matrix: evaluate_d_early_v22({"code":ticker}) → payload必须是dict
    R-Matrix: rank_type_b_rising_channel(ticker, "", daily_prices)
    K线: 250日前复权, adjustflag="2"
  决策: 导入失败→SKIPPED; 无K线→DEGRADED; 有评分→PASS

模块: gate8_v3_scenarios (Z-G07:399)
  输入: g1_details
  输出: GateResult{scenarios:[保守/基准/乐观], calibration:"uncalibrated"}
  参数: subjective_weight (NOT probability), calibration_status=uncalibrated

模块: gate9_z8_action (Z-G07:413)
  输入: gates:List[GateResult]
  输出: (ActionLevel, reason)
  参数:
    pass_count = sum(PASS)
    block_count = sum(BLOCK+DATA_INCOMPLETE)
    ≥3 BLOCK → BLOCK
    ≥1 BLOCK → WAIT
    ≥2 SKIP → WATCH
    ≥7 PASS+0 BLOCK → PAPER_TRACK
    ≥5 PASS → WATCH

模块: gate10_report (Z-G07:434)
  输入: stocks:List[StockResult]
  输出: dict{stocks, summary}
  参数: 非PAPER_WORLD动作→自动降级WATCH (SafetyLock)

## Z-G09 全局轮动 — 1个核心模块


## 模块: _quick_r_score (Z-G09 gate_pipeline.py:20)

  位置: R-Matrix快速评分
  输入: ticker:str
  输出: dict{ticker, name, price, amp_20d, position, trend, score} | DATA_INSUFFICIENT (status=DATA_GAP, excluded_from_ranking=true)
  参数:
    amp = (max(prices[-20:]) / min(prices[-20:]) - 1) * 100  # 20日振幅%
    pos = (price[-1] - min) / (max - min)  # 当前位置(0-1)
    trend = (price[-1] / ma20 - 1) * 100  # 偏离MA20%
    score = amp * (1 - |pos-0.5|*1.5) + |trend|*0.5  # 低位+宽振幅=高分
  决策: K线<20日→None(不纳入候选); score降序→取TOP80

## Z-G10 全局黑马 — 1个核心模块


## 模块: _quick_d_score (Z-G10 gate_pipeline.py:22)

  位置: D-Matrix快速评分
  输入: ticker:str
  输出: dict{ticker, name, price, score, lifecycle, chg_3m} | DATA_INSUFFICIENT (status=DATA_GAP, excluded_from_ranking=true)
  参数:
    gene = max(0, 10 - |chg_3m|)  # 低涨幅→高基因分 (max=10)
    sector = 8 if has_finance else 4  # 财务可得→基础分
    silent = 10 - min(vol5*100, 10)  # 5日低波→高静默分
    vol_preload = 5  # 基础量能分
    dq_bonus = dq/20  # DQ加权 (max≈5)
    total = gene + sector + silent + vol_preload + dq_bonus
  决策:
    (>30) → D3_CANDIDATE
    (>20) → D2_PREHEAT
    (≤20) → D1_THEME_SEED
    L4 BLOCK → return GateResult(status=BLOCK, output_level=O2, reason_codes=[ST|SUSPENDED|NO_VOLUME], 落盘为HealthGateBlockedEvent)

## Z-G11 组合风控 — 2个核心模块


## 模块: _parse_positions (Z-G11 gate_pipeline.py:21)

  位置: 持仓解析+实时估值
  输入: 无 (读MEMORY.md + 调Z-G01价格)
  输出: list[dict{code, name, shares, cost, price, value}]
  参数: market_truth(code)→price: PASS=正常估值, DEGRADED=估值参考(标confidence), BLOCK=估值空缺(仅缺口报告,不生成REDUCE_RISK)

模块: _classify_chain (Z-G11 gate_pipeline.py:38)
  位置: 产业链分类
  输入: name:str
  输出: str — "机器人"|"AI算力"|"资源"|"其他"
  参数:
    机器人: 双环|雷赛|绿的|三花|步科|兆威|奥比|柯力
    AI算力: 中际|天孚|新易盛|寒武纪|海光|浪潮|华工|沪电|中贝|英维克
    资源: 紫金|中煤|黄金

## Z-G12 系统巡检 — 3个核心模块


## 模块: _check_data_sources (Z-G12 gate_pipeline.py:21)

  位置: 数据源3路健康检查
  输入: 无
  输出: dict{sina:"UP"|"DOWN", baostock:"UP"|"DOWN", tushare:"UP"|"DOWN"}
  参数: market_truth("002463") → 隐式测试Sina+baostock
  决策: ≥2 UP → 系统可用; 1 UP → 降级运行; 0 UP → 禁依赖外部行情管线; 允本地复盘/巡检报告/缺口诊断/配置检查/离线研究

模块: _count_memory_files (Z-G12 gate_pipeline.py:31)
  位置: 记忆宫殿盘存
  输入: 无
  输出: dict{root:"OK"|"MISSING", files:int}
  参数: 递归计数投资记忆银行下所有.md文件

模块: _check_cron (Z-G12 gate_pipeline.py:40)
  位置: Cron健康
  输入: 无
  输出: dict{status, output_lines}
  参数: subprocess.run(["openclaw","cron","list"])
  决策: returncode=0→accessible; 异常→unavailable

## Z-G14 月度全量·流A — 2个核心模块


## 模块: _quick_scan (Z-G14 gate_pipeline.py:12)

  位置: B-R-D三维快速扫描
  输入: tickers:list
  输出: list[dict{code, name, b, r, d, cross, price}]
  参数:
    b_score = min(DQ, 100) * 0.5  # 底仓分(DQ加权)
    r_score = 振幅% * 0.6         # 轮动分(振幅加权)
    d_score = (8 if finance else 4) + (5 if DQ>70 else 2)  # 黑马分
    b_ok = b>40; r_ok = r>15; d_ok = d>8
    cross:
      B∩D→"B∩D☆"(钻石) | B∩R→"B∩R★"(黄金) | D∩R→"D∩R◇"(白银)
      纯B→"纯B" | 纯D→"纯D" | 纯R→"纯R"
  决策: 三维叠加排序→TOP30终选; 交叉多重验证→优先级更高

模块: 产业链浓度 (Z-G14 gate_pipeline.py:92)
  位置: 10链候选人分布
  输入: candidates(前50)
  输出: dict{chain:hit_count}
  参数: 关键词匹配 机器人/AI算力/半导体/资源/消费
  决策: hit_count=0→盲区警告⚠️

## Z-G17 人类风控 — 2个核心模块


## 模块: Tilt检测 (Z-G17 gate_pipeline.py:27)

  位置: 人类行为Tilt检测
  输入: override:dict{system_action, human_action, reason}
  输出: tilt:bool, tilt_reasons:list
  参数:
    主观关键词: ["觉得","一定","肯定","绝对","稳","必"]
    动作覆盖: system=BLOCK/WAIT + human=WATCH → TILT
  决策: 任一触发→TILT; 双触发→严重TILT

模块: Ledger记录 (Z-G17 gate_pipeline.py:60)
  位置: HumanBehaviorLedger
  输入: entry:dict
  输出: 无 (副作用: 追加human_behavior_ledger.jsonl)
  参数: JSONL格式, 每行一个override记录
  决策: 后验统计override收益 vs 系统收益→调L1.6敏感度

## 跨管线共享参数总表




### 9.8 Z-G08 叙事雷达深度 (3模块)

| 模块 | 参数计算 | 决策逻辑 |
|------|------|------|
| 主题热度 | 5类主题(AI/机器人/半导体/资源/消费) 0-10标准化 | >7过热关注 |
| L1.6情绪 | slogan新颖度+exhaustion(集中度)+diversity(分散度) | >60%→MANIA, >80%→TILT |
| 信号裁决 | NORMAL/MANIA/TILT | 仅调风控, 不改选股 |

### 9.13 Z-G13 底仓管理 (3模块)

| 模块 | 参数计算 | 决策逻辑 |
|------|------|------|
| Thesis检查 | 财务/DQ/ST/停牌/成交 五维扫描 | ≥2旗→REVIEW, 1→WATCH, 0→INTACT |
| B类型 | B1~B5 调用B-Matrix v2.1.1 dispatcher |  |
| 动作 | INTACT→HOLD, WATCH→观察, REVIEW→REQUIRED | Thesis破裂→REDUCE_RISK |

### 9.15 Z-G15 产业链深研 (4模块)

| 模块 | 参数计算 | 决策逻辑 |
|------|------|------|
| V3证据分层 | A/B/C/D 四级 | A级=高置信, 无A→不输出确定性 |
| 8硬门 | ROE/OCF/毛利率/负债率/分红/估值/产业链/催化剂 | 不全→DATA_INCOMPLETE |
| 催化剂日历 | 事件(日期/事件/关联度) | 高关联→优先级 |
| 输出格式 | 证据+硬门+催化剂+风险 | 不带买入建议 |



### 9.16 Z-G16 V4纸面执行教练 (8模块)

| # | 模块 | 功能 | 关键输出 |
|:--:|------|------|------|
| ① | current_state_assessor | 当前交易状态判断 | L3+L1.5+DQ+角色+允许动作 |
| ② | scenario_route_matrix | 可能路线矩阵 | A顺风/B震荡/C回撤/D高开, uncalibrated |
| ③ | price_zone_planner | 价格区间计划 | watch/probe/add/harvest/rollback/forbidden 6区 |
| ④ | position_playbook_builder | 仓位节奏 | 3U制: TRACK(0U)→PROBE_1(1U)→PROBE_2(1U)→PROBE_3(1U), action=PAPER_PROBE |
| ⑤ | signal_checkpoint_builder | 进退信号 (试仓与减风险信号) | probe/risk_reduce/rollback结构化信号 |
| ⑥ | time_checkpoint_scheduler | 时间检查点 | T-1→0925→0935→0945→1030→1430→1500 |
| ⑦ | kill_rollback_guard | Kill/Rollback | 6kill+4rollback条件 |
| ⑧ | posterior_review_plan | 纸面复盘 | T+1/5/20→Z9→可选Alpha验证仓 |

禁用细则:
 DQ<85: 禁Full(price_zones/position/PROBE); 允Z-G16 Lite(条件路线+信号+缺口+等待触发器); 允WATCH/WAIT
 MarketTruth BLOCK → 禁价格区间
 L1.5 BLOCKED → 禁PAPER_PROBE
 裸写未校准概率 → 计划不合格

#### Z-G16 Full 输出契约 (PaperExecutionCoachPlan)

```json
{
  "module": "Z-G16", "type": "PaperExecutionCoachPlan",
  "symbol": "002463", "role": "R_MATRIX",
  "output_level": "O4_PAPER_PLAN", "plan_status": "QUALIFIED", "dq_score": 87, "probability_status": "uncalibrated",
  "capability_mask": {"allowed_outputs":["paper_plan","paper_track"],"conditional_outputs":[{"output":"paper_probe","requires":["world=PAPER_WORLD","L1.5=SAFE","MT=PASS"]}],"forbidden_actions":["BUY","SELL","AUTO_TRADE"]},
  "paper_only": true, "real_trade_authorized": false,
  "current_state": {"l3":"PARTIAL","l15":"SAFE","price_source":"raw_unadjusted"},
  "scenario_routes": [{"id":"A顺风","condition":"L3→FULL+L15SAFE","probability":null,"probability_status":"uncalibrated","action":"PAPER_PROBE","paper_size":"1U"}],
  "price_zones": {"watch":"MA20±2%","probe":"前低+0-3%","harvest":"前高+5%","forbidden":"高开>5%"},
  "position_playbook": {"max":"3U","unit":"1U=plan_max/3","steps":[{"stage_id":"TRACK","action":"PAPER_TRACK","paper_size":"0U"},{"stage_id":"PROBE_1","action":"PAPER_PROBE","paper_size":"1U"},{"stage_id":"PROBE_2","action":"PAPER_PROBE","paper_size":"1U"},{"stage_id":"PROBE_3","action":"PAPER_PROBE","paper_size":"1U"}]},
  "signal_checkpoints": {"advance_conditions":["L3→FULL","VWAP站稳"],"risk_reduce_conditions":["跌破失效位","板块RETREAT"],"rollback_conditions":[{"from":"PROBE","to":"TRACK"}]},
  "time_checkpoints": ["T-1","0925","0935","0945","1030","1430","1500","T+1","T+5"],
  "kill_conditions": ["MT_BLOCK","L3_REJECTED","L15_BLOCKED","放量跌破失效位","板块RETREAT"],
  "rollback_conditions": [{"from":"PROBE","to":"TRACK"},{"from":"ROUTE_A","to":"ROUTE_B"},{"from":"ANY","to":"CANCEL_PLAN"}],
  "posterior_review_plan": {"T+1":"信号兑现?","T+5":"跑赢Beta?","human":"滞后/情绪化?"}
}
```


### 9.16A Z-G16A Alpha平行验证仓 (6模块)

| 模块 | 参数计算 | 决策逻辑 |
|------|------|------|
| 验证计划 | hypothesis+ghost_benchmark+失效条件 | 缺任一→REJECTED |
| 幽灵基准 | 产业链优先→角色fallback | 10链ETF+4角色指数映射 |
### fill_quality_resolver (Z-G16A子模块)

| 输入 | 输出 |
|------|------|
| MT.PASS, price_basis=raw_unadjusted, quote_domain=execution_quote, TTL未过期 | HIGH_CONFIDENCE_FILL: fill可用, attribution_allowed=true |
| MT.PASS/DEGRADED, price_basis=raw_unadjusted, quote_domain=realtime_research (role=raw_fallback), TTL未过期 | DEGRADED_FILL: 方向Alpha验证, attribution_allowed=false |
| MT.BLOCK / price_basis=unknown / TTL过期 | NO_FILL: 仅验证草案, 无开仓价 |

冻结: 字段统一使用 raw_unadjusted|execution_quote|realtime_research (role=raw_fallback), 禁用缩写 raw|execution|realtime_fallback

| PAPER_WORLD开仓 | 滑点0.15%+佣金0.03% | 统一调用fill_quality_resolver; 不重复定义; NO_FILL→无开仓价 |
| 盯市 | active_return=stock_return-benchmark_return | >threshold + hypothesis_adherence=true + drawdown_ok + benchmark_valid=true + sample_sufficient=true + route_finished_or_expired=true → promote_candidate: 进入Z9+HumanReview复核池, 不自动提高B/R/D分数, 不自动加入真实候选, 不自动生成HUMAN_CONFIRM_PROBE, 不等于实盘晋级 |
| 结算(6结果) | hypothesis_adherence+benchmark_valid+sample_sufficient | promote_candidate/continue_validation/retire/etf_substitute_review/human_strength_signal/human_blind_spot_signal |
| LLMCoach | 复盘报告草案 | HumanPattern更新→Z9反馈 |

### 调度补充

| 管线 | 频率 | 说明 |
|------|------|------|
| Z-G03 | 0925/0935/0945/1030 四检查点 | auction/open/confirm/expiry |
| Z-G09 | 每周全量+每日增量 | 周末重建, 收盘增量 |
| Z-G10 | 每日轻量+每周全量 | D2/D3生命周期变化快 |

## 全局参数:

  CACHE_TTL_BY_DOMAIN = 分级(3s~7d) / 见TTL参数表
    
  DQ_DIAGNOSTIC_THRESHOLD     = 60           # DQ分, 低于此值仅DIAGNOSTIC_ONLY
  DQ_V4_THRESHOLD        = 85           # <85→禁Z-G16 Full; 允Lite(条件路线+信号+缺口); 禁price_zones/position/PROBE
  KLINE_MIN_BARS         = 20           # 根, 最少K线数
  FALSE_PREHEAT_COOLDOWN = 3            # 天, 假预热冷却期
  SLIPPAGE_RATE          = 0.0015       # 0.15%, 纸面滑点率
  L25_DOMAIN_MIN         = 4            # 域, L2.5最低填充域数
  L25_DOMAIN_TOTAL       = 8            # 域, L2.5总信息域数
  Z9_MIN_SAMPLES         = 50           # 样本, Z9启用最低数
  SENTIMENT_CONCENTRATION_MANIA = 0.6   # 叙事集中度过热阈值
  SENTIMENT_CONCENTRATION_TILT = 0.8    # 叙事集中度TILT阈值
  VOLUME_RATIO_SILENT    = 0.7          # 量比: 缩量阈值
  VOLUME_RATIO_SMART     = 1.5          # 量比: 放量阈值
  GAP_ALERT_PCT          = 2.0          # %, 竞价缺口告警阈值
  TAIL_CHG_FALSE         = 3.0          # %, 尾盘涨幅假预热阈值
  TAIL_CHG_SMART         = 2.0          # %, 尾盘涨幅抢筹阈值
  CONCENTRATION_WARN     = 25           # %, 单票集中度关注线
  CONCENTRATION_CRITICAL = 40           # %, 单票集中度严重线
  CHAIN_CONCENTRATION_WARN = 60         # %, 产业链集中度告警线
"""
print(MODULES)



## 附一、新增宪法——管线执行铁律

```
第1条 (Market Truth):   所有数字必须可验证, 禁止编造
第2条 (Source Arb):     **硬规则**: Market Truth只允许raw/unadjusted价格互相交叉验证。
前复权/后复权/adjusted research price不得参与execution_quote的价格一致性判断。
_bs_raw_kline: adjustflag=3 (不复权) — 仅用于execution_price/raw口径校验
_bs_research_kline: adjustflag=2 (前复权) — 仅用于均线/R-Matrix/历史形态

同一price_basis内价格冲突按三态阈值: exec(≤0.3%PASS/0.3-1%DEGRADED/>1%BLOCK); research(≤0.5%/1.5%); historical(≤1%/3%); 禁止raw vs adjusted跨口径
第3条 (DQ Gate): DQ<60→O2_DIAGNOSTIC/O1_DATA_GAP(禁ActionProposal); 60≤DQ<85→禁Z-G16 Full,允Z-G16 Lite; DQ≥85→只解除DQ限制(仍需MT PASS+L1.5 SAFE)
第4条 (L5 Matrix):      角色必须跑Python代码, 禁手工标记
第5条 (V3 Calibration): 概率标uncalibrated, 禁裸写%
第6条 (闸口不可跳过):   跳过任一→背书降级 | 跳过≥2→不作为有效投资样本, 必须落盘为DataGapEvent/DegradedRunEvent
第7条 (落盘绝对路径):   每次产出必须披露落盘路径
```

---

**签章**: Z-MATRIX-OS v2.9.5-RC | 蓝军七审通过 | 2026-05-19


### P0/P1修复状态 (二次审核后)

| # | 问题 | 状态 |
|:--:|------|:--:|
| P0-1 | 数据源按用途分层 | ✅ 代码+文档 |
| P0-2 | PAPER_ENTER全部删除 | ✅ 全系统0残留 |
| P0-3 | Z-G16升级V4纸面执行教练(8部分) | ✅ 代码重写 |
| P0-4 | TTL分级参数表 | ✅ 代码实现(3s/30s/86400s) |
| P1-1 | Z-G01改为Data Service | ✅ 代码标注+文档修正 |
| P1-2 | Z-G03多检查点 | ✅ 0925/0935/0945/1030 |
| P1-3 | Z-G04监控→收盘判定 | ✅ 14:30监控+15:00判定 |
| P1-4 | Z-G09/Z-G10每日增量 | ✅ 代码标注 |
| P1-5 | 8因子→8信息域 | ✅ 全系统0残留 |
| P1-6 | Z-G01模块接口表 | ✅ 文档完成 (第九章), 代码实现已对齐 |

当前: v2.9.5-RC → P0通过, 18条管线, Z-G16A就绪 → RC测试阶段
