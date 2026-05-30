# Z-G16 Physical Reality Layer｜ShadowBroker 架构吸收与 Z-EventBroker 协议设计 v1.0

> **所属系统**：Z-MATRIX-OS  
> **新增层级**：Z-G16 Physical Reality Layer  
> **协议名称**：Z-EventBroker Protocol  
> **吸收对象**：ShadowBroker 的 OSINT Event Hub / Event Lake / Telemetry / Geospatial Intelligence 架构思想  
> **执行对象**：OpenClaw 天师 / deepseek-v4-pro  
> **阶段性质**：架构吸收 / 协议设计 / ResearchDB Event 扩展 / AutoCaseForge 触发源扩展 / ZC35 催化验证增强  
> **当前策略**：只吸收架构，不部署 ShadowBroker，不接实时 API，不接外部数据源，不进入 production  
> **硬边界**：Research Only / Paper Only / No Broker / No Runtime / No Real Trade / No Production

---

## 0. 总裁决

ShadowBroker 对 Z-MATRIX 的价值不在于“直接部署一套 OSINT 地图系统”，而在于它验证了一种高价值架构：

```text
多源异构现实世界信号
→ 统一事件采集
→ 统一标准化
→ 统一事件账本
→ 统一时间轴
→ 统一查询接口
→ AI 分析与案例沉淀
```

Z-MATRIX 当前最应该吸收的是这套 **Event Hub / Event Lake / Telemetry Architecture**，而不是立刻接入实时 GPS、AIS、SAR、航班、船舶等外部 API。

本阶段只允许做：

```text
1. 新增 Z-G16 Physical Reality Layer 架构文档
2. 新增 Z-EventBroker 协议文档
3. 扩展 ResearchDB Event Schema
4. 定义 PhysicalSignal / NarrativeEvent / RealityCheck / NPAScore 数据结构
5. 新增 ShadowBrokerAdapterStub，只读取本地 fixture，不连外网
6. 新增 NPA 叙事-现实一致性评分器
7. 新增 RealityCheckLinker，连接 NarrativeEvent 与 PhysicalSignal
8. 新增 AutoCaseForge 触发规则扩展
9. 新增 Phase6 EventLake 扩展说明
10. 新增 tests + verify 脚本
```

本阶段禁止：

```text
1. 不部署 ShadowBroker
2. 不写 docker-compose
3. 不启动 ShadowBroker 后端
4. 不接 OpenSky / ADSB / AIS / GDELT / N2YO / SAR / GPS Jamming 等外部 API
5. 不写真实 API Key
6. 不开启实时轮询
7. 不创建 daemon
8. 不启 runtime_enabled
9. 不接 broker
10. 不生成交易建议
11. 不改 RC1 / production 状态
12. 不进入 Phase 1–10 主流程以外的扩展执行
```

最终目标：

```text
把 ShadowBroker 的“现实世界事件聚合能力”
吸收为 Z-MATRIX 的“现实世界验证层”，
为 ZC35、AutoCaseForge、ResearchDB EventLake、L25 Regime 提供新的研究信号。
```

---

## 1. 为什么当前不直接部署 ShadowBroker？

### 1.1 当前最缺的不是更多数据

Z-MATRIX 当前主线是：

```text
ResearchDB Phase 1–10
AutoCaseForge
Outcome 数据库
ZC35 事件生命周期数据库
FactorFactory 验证库
```

当前最缺的是：

```text
真实交易案例
真实事件 Outcome
真实信号验证
自动案例内化
```

不是：

```text
更多实时 OSINT 数据源
```

直接部署 ShadowBroker 会带来大量数据，但如果 ResearchDB / CaseForge / Outcome 尚未完全成型，会出现：

```text
数据越来越多
可验证案例越来越少
系统噪声越来越高
维护成本越来越重
```

### 1.2 ShadowBroker 天然偏实时，而 Z-MATRIX 应坚持中低频

ShadowBroker 原生方向偏：

```text
15s / 60s 级别更新
实时地图
实时地缘态势
实时数据流
```

Z-MATRIX 的优势战场是：

```text
Weekly / Monthly / Quarterly
中低频跨期
基本面 / 事件驱动
产业链逻辑重构
宏观水温与极端尾部风险规避
```

当前阶段必须：

```text
只吸收架构，不吸收实时噪音。
```

### 1.3 ShadowBroker 是外部感知器，不是核心生命线

Z-MATRIX 的核心生命线是：

```text
ResearchDB
Outcome DB
AutoCaseForge
ZC35
FactorFactory
B-Matrix
R-Matrix
行业/产业链知识库
个人操盘画像
```

ShadowBroker 只能成为：

```text
现实世界信号增强器
```

不是替代主系统。

---

## 2. 吸收后新增能力

### 2.1 现实世界验证能力

现在系统主要依赖：

```text
新闻
公告
财报
研报
政策
行情
产业链资料
```

这些多为文本叙事。

Z-G16 增加：

```text
港口/船舶活动
航班/航空活动
GPS 干扰
能源运输
航线变化
地缘冲突物理迹象
供应链物理变化
```

使系统能够判断：

```text
文本叙事是否被现实世界信号验证。
```

### 2.2 NPA：叙事-现实一致性评分

新增指标：

```text
NPA = Narrative Physical Alignment
叙事-现实一致性评分
```

作用：

```text
评估某个财经叙事与物理现实信号是否一致。
```

示例：

```text
新闻：航运景气回升
现实：AIS 港口密度上升，航线拥堵上升，运价上升
NPA：高
```

```text
新闻：某地区供应链恢复
现实：港口密度下降，航线绕行，GPS 干扰扩大
NPA：低
```

### 2.3 预期差发现能力

当市场叙事尚未充分发酵，但物理信号已先行变化时，系统生成：

```text
PHYSICAL_PRE_SIGNAL
```

进入：

```text
ResearchDB EventLake
AutoCaseForge Review Queue
ZC35 Catalyst Candidate
```

不生成交易信号。

### 2.4 催化真实性验证能力

ZC35 原本处理：

```text
利好催化
半衰期
残余能量
卖事实风险
催化真空
```

加入 Z-G16 后，增加：

```text
物理验证
现实背书
物理背离
叙事空转
```

例如：

```text
ZC35 catalyst_grade=A
但 NPA=20
→ 降级为 narrative_only_catalyst
```

### 2.5 宏观物理水温计

对 L25 / Regime 层增加：

```text
地缘物理风险
航运物理压力
能源运输异常
供应链拥堵
区域冲突升温
```

输出：

```text
physical_regime_pressure
```

用于：

```text
L25 Regime
ZC45 Proxy Hedge
ZC50 Account Governance
```

### 2.6 AutoCaseForge 新触发源

Z-G16 不是直接给交易建议，而是自动制造研究案例：

```text
NPA低但叙事热 → NARRATIVE_REALITY_DIVERGENCE
NPA高但市场未反应 → PHYSICAL_PRE_SIGNAL
物理异常后板块上涨 → PHYSICAL_CONFIRMED_CATALYST
Scheduled event 后物理信号无变化 → SELL_ON_NEWS_RISK
```

---

## 3. 系统定位

### 3.1 新增层级

```text
Z-G16 Physical Reality Layer
```

职责：

```text
把现实世界物理信号变成可审计、可追踪、可连接 Outcome 的事件数据。
```

### 3.2 新增协议

```text
Z-EventBroker Protocol
```

职责：

```text
定义不同事件源如何进入 Z-MATRIX：
文本事件
政策事件
公告事件
行情事件
物理事件
地缘事件
供应链事件
```

### 3.3 新增评分

```text
NPA Score
Narrative Physical Alignment
叙事-现实一致性评分
```

### 3.4 新增适配器

```text
ShadowBrokerAdapterStub
```

注意：

```text
Stub 只读取本地 fixture。
不连接 ShadowBroker。
不连接外部 API。
不启动 Docker。
```

---

## 4. 总体架构

```text
External Narrative
    │
    ▼
NarrativeEvent Ledger
    │
    ├──────────────┐
    │              │
    ▼              ▼
ZC35 Catalyst   PhysicalSignal Fixture
    │              │
    ▼              ▼
CatalystState   Z-G16 Physical Reality Layer
    │              │
    └──────┬───────┘
           ▼
    RealityCheckLinker
           ▼
       NPA Scorer
           ▼
  RealityCheck Ledger
           ▼
 AutoCaseForge Trigger Extension
           ▼
 ResearchDB EventLake
           ▼
 Outcome / Case / Memory
```

---

## 5. 必须新增文件

### 5.1 文档

```text
docs/architecture/
  ZG16_PHYSICAL_REALITY_LAYER.md
  Z_EVENTBROKER_PROTOCOL.md
  NPA_SCORE_POLICY.md
  SHADOWBROKER_ABSORPTION_SCOPE.md

docs/research_db/
  PHASE6_EVENTHUB_EXTENSION.md
  PHYSICAL_SIGNAL_DATA_POLICY.md
  PHYSICAL_REALITY_NO_DEPLOYMENT_BOUNDARY.md
  ZG16_ACCEPTANCE_MATRIX.md
  ZG16_CLOSEOUT_REPORT.md
```

### 5.2 数据目录

```text
data/research_db/event/physical/
  README.md

  fixtures/
    sample_ais_port_density.jsonl
    sample_gps_jamming.jsonl
    sample_shipping_route_change.jsonl
    sample_energy_transport_anomaly.jsonl
    sample_geopolitical_event.jsonl
    sample_narrative_events.jsonl

  normalized/
    physical_signal_ledger.jsonl
    reality_check_ledger.jsonl
    npa_score_ledger.csv
    physical_signal_quality_ledger.csv

  reports/
    physical_signal_report.md
    npa_score_report.md
    reality_check_report.md
    shadowbroker_absorption_report.md
```

### 5.3 代码模块

```text
zmatrix/research_db/event_physical/
  __init__.py
  physical_signal_schema.py
  narrative_event_schema.py
  reality_check_schema.py
  npa_score_schema.py
  physical_signal_loader.py
  shadowbroker_adapter_stub.py
  reality_check_linker.py
  npa_scorer.py
  physical_signal_quality_checker.py
  eventhub_extension.py
  caseforge_trigger_extension.py
  physical_signal_report.py
```

### 5.4 测试

```text
tests/research_db/event_physical/
  test_physical_signal_schema.py
  test_narrative_event_schema.py
  test_reality_check_schema.py
  test_npa_score_schema.py
  test_physical_signal_loader.py
  test_shadowbroker_adapter_stub.py
  test_reality_check_linker.py
  test_npa_scorer.py
  test_physical_signal_quality_checker.py
  test_caseforge_trigger_extension.py
  test_eventhub_extension.py
  test_no_deployment_boundary.py
```

### 5.5 Verify 脚本

```text
scripts/verify_zg16_physical_reality_layer.sh
```

---

## 6. 核心 Schema

### 6.1 PhysicalSignal

文件：

```text
physical_signal_schema.py
```

必须定义：

```python
from dataclasses import dataclass
from enum import Enum
from typing import Optional, List

class PhysicalSignalType(str, Enum):
    AIS_PORT_DENSITY = "AIS_PORT_DENSITY"
    SHIPPING_ROUTE_CHANGE = "SHIPPING_ROUTE_CHANGE"
    GPS_JAMMING = "GPS_JAMMING"
    MILITARY_AVIATION_ACTIVITY = "MILITARY_AVIATION_ACTIVITY"
    ENERGY_TRANSPORT_ANOMALY = "ENERGY_TRANSPORT_ANOMALY"
    PORT_CONGESTION = "PORT_CONGESTION"
    SATELLITE_GROUND_CHANGE = "SATELLITE_GROUND_CHANGE"
    GEOPOLITICAL_REGION_EVENT = "GEOPOLITICAL_REGION_EVENT"
    SUPPLY_CHAIN_PHYSICAL_STRESS = "SUPPLY_CHAIN_PHYSICAL_STRESS"
    UNKNOWN = "UNKNOWN"

class PhysicalSignalQuality(str, Enum):
    READY = "READY"
    PARTIAL = "PARTIAL"
    DATA_INSUFFICIENT = "DATA_INSUFFICIENT"
    CONFLICTED = "CONFLICTED"
    ERROR = "ERROR"

@dataclass
class PhysicalSignal:
    signal_id: str
    signal_type: PhysicalSignalType
    event_time: str
    geo_region: str
    source: str
    raw_value: Optional[float]
    normalized_value: Optional[float]
    baseline_value: Optional[float]
    deviation_score: Optional[float]
    confidence: float
    related_industries: List[str]
    related_chains: List[str]
    related_tickers: List[str]
    quality_status: PhysicalSignalQuality
    production_allowed: bool = False
```

必须校验：

```text
signal_id 不得为空
signal_type 必须合法
event_time 不得为空
confidence 在 0–1 之间
production_allowed 必须 false
quality_status=READY 时 normalized_value 不得为空
```

---

### 6.2 NarrativeEvent

文件：

```text
narrative_event_schema.py
```

```python
class NarrativeEventType(str, Enum):
    POLICY_SIGNAL = "POLICY_SIGNAL"
    INDUSTRY_NEWS = "INDUSTRY_NEWS"
    EARNINGS_EVENT = "EARNINGS_EVENT"
    PRODUCT_BREAKTHROUGH = "PRODUCT_BREAKTHROUGH"
    SUPPLY_CHAIN_NEWS = "SUPPLY_CHAIN_NEWS"
    GEOPOLITICAL_NEWS = "GEOPOLITICAL_NEWS"
    COMMODITY_NEWS = "COMMODITY_NEWS"
    SHIPPING_NEWS = "SHIPPING_NEWS"
    ENERGY_NEWS = "ENERGY_NEWS"
    UNKNOWN = "UNKNOWN"
```

字段：

```text
narrative_id
event_type
event_time
title
summary
source
narrative_strength
related_industries
related_chains
related_tickers
zc35_catalyst_id
production_allowed=false
```

---

### 6.3 RealityCheck

文件：

```text
reality_check_schema.py
```

```python
class RealityCheckStatus(str, Enum):
    ALIGNED = "ALIGNED"
    DIVERGENT = "DIVERGENT"
    PHYSICAL_PRE_SIGNAL = "PHYSICAL_PRE_SIGNAL"
    NARRATIVE_ONLY = "NARRATIVE_ONLY"
    PHYSICAL_ONLY = "PHYSICAL_ONLY"
    DATA_INSUFFICIENT = "DATA_INSUFFICIENT"
```

字段：

```text
reality_check_id
narrative_id
linked_signal_ids
npa_score
status
explanation
confidence
case_trigger_candidate
human_review_required=true
production_allowed=false
```

---

### 6.4 NPA Score

文件：

```text
npa_score_schema.py
```

```python
@dataclass
class NPAScore:
    npa_id: str
    narrative_id: str
    score: float
    narrative_strength: float
    physical_alignment: float
    physical_confidence: float
    contradiction_penalty: float
    data_quality_penalty: float
    status: str
    production_allowed: bool = False
```

分数范围：

```text
0–100
```

等级：

```text
80–100：STRONG_ALIGNMENT
60–79：MODERATE_ALIGNMENT
40–59：WEAK_ALIGNMENT
20–39：DIVERGENCE
0–19：STRONG_DIVERGENCE
```

---

## 7. ShadowBrokerAdapterStub

文件：

```text
shadowbroker_adapter_stub.py
```

职责：

```text
读取本地 fixture，模拟未来 ShadowBroker 物理信号输入。
```

禁止：

```text
不发 HTTP 请求
不读 API key
不启动 Docker
不连接外部服务
不使用 requests/httpx/aiohttp 访问外网
```

函数：

```python
def load_fixture_signals(path: str) -> list[dict]:
    ...

def query_physical_signals(
    signal_type: str | None = None,
    geo_region: str | None = None,
    start_time: str | None = None,
    end_time: str | None = None,
) -> list[dict]:
    ...

def adapter_healthcheck() -> dict:
    ...
```

`adapter_healthcheck()` 必须返回：

```json
{
  "adapter": "ShadowBrokerAdapterStub",
  "mode": "STUB_ONLY",
  "external_api_enabled": false,
  "docker_required": false,
  "runtime_enabled": false,
  "production_allowed": false
}
```

---

## 8. NPA 评分器

文件：

```text
npa_scorer.py
```

### 8.1 输入

```python
def calculate_npa_score(
    narrative_event: dict,
    physical_signals: list[dict],
    config: dict | None = None,
) -> dict:
    ...
```

### 8.2 默认公式

```text
physical_alignment = weighted_mean(signal.normalized_value * signal.confidence)
contradiction_penalty = penalty when narrative_strength high but physical_alignment low
data_quality_penalty = penalty when signal coverage insufficient

npa_score =
  0.45 * physical_alignment
+  0.25 * physical_confidence
+  0.20 * narrative_physical_direction_match
-  0.10 * data_quality_penalty
```

最终归一化为 0–100。

### 8.3 输出

```json
{
  "npa_id": "NPA-20260601-001",
  "narrative_id": "NAR-20260601-001",
  "score": 82.5,
  "status": "STRONG_ALIGNMENT",
  "physical_alignment": 0.86,
  "physical_confidence": 0.9,
  "contradiction_penalty": 0.0,
  "data_quality_penalty": 0.05,
  "production_allowed": false,
  "human_review_required": true
}
```

---

## 9. RealityCheckLinker

文件：

```text
reality_check_linker.py
```

职责：

```text
把 NarrativeEvent 与 PhysicalSignal 按行业、产业链、地理区域、时间窗口关联。
```

函数：

```python
def link_narrative_to_physical_signals(
    narrative_event: dict,
    physical_signals: list[dict],
    max_days_gap: int = 10,
) -> dict:
    ...
```

匹配维度：

```text
related_industries
related_chains
related_tickers
geo_region
event_time
signal_type
```

输出：

```json
{
  "narrative_id": "NAR-001",
  "linked_signal_ids": ["PHY-001", "PHY-002"],
  "link_quality": "READY",
  "missing_dimensions": [],
  "production_allowed": false
}
```

---

## 10. AutoCaseForge 触发扩展

文件：

```text
caseforge_trigger_extension.py
```

新增 4 条触发规则。

### G16-R1：叙事强但现实弱

```text
条件：
narrative_strength >= 70
NPA_score < 30

触发：
NARRATIVE_REALITY_DIVERGENCE
```

生成 case：

```text
case_type = NARRATIVE_REALITY_DIVERGENCE
status = AUTO_DRAFT
human_review_required = true
production_allowed = false
```

---

### G16-R2：现实先行但市场未反应

```text
条件：
NPA_score >= 80
physical_signal_deviation >= 2.0
market_reaction_score < 30

触发：
PHYSICAL_PRE_SIGNAL
```

生成 case：

```text
case_type = PHYSICAL_PRE_SIGNAL
```

---

### G16-R3：物理信号确认催化

```text
条件：
ZC35 catalyst exists
NPA_score >= 70
T5 alpha_vs_industry > 0

触发：
PHYSICAL_CONFIRMED_CATALYST
```

---

### G16-R4：日程事件后物理无变化

```text
条件：
scheduled_event = true
narrative_strength >= 70
physical_alignment < 30
T0/T1 price weakness

触发：
SELL_ON_NEWS_RISK_PHYSICAL_UNCONFIRMED
```

---

## 11. ResearchDB EventLake 扩展

新增表：

```text
physical_signal_ledger.jsonl
reality_check_ledger.jsonl
npa_score_ledger.csv
physical_signal_quality_ledger.csv
```

### 11.1 physical_signal_ledger.jsonl

```json
{
  "signal_id": "PHY-20260601-AIS-001",
  "signal_type": "AIS_PORT_DENSITY",
  "event_time": "2026-06-01T00:00:00",
  "geo_region": "SINGAPORE_PORT",
  "source": "fixture",
  "raw_value": 1250,
  "baseline_value": 900,
  "normalized_value": 0.82,
  "deviation_score": 2.1,
  "confidence": 0.85,
  "related_industries": ["SHIPPING", "EXPORT_CHAIN"],
  "related_chains": ["GLOBAL_LOGISTICS"],
  "related_tickers": [],
  "quality_status": "READY",
  "production_allowed": false
}
```

### 11.2 reality_check_ledger.jsonl

```json
{
  "reality_check_id": "RCHECK-20260601-001",
  "narrative_id": "NAR-20260601-001",
  "linked_signal_ids": ["PHY-20260601-AIS-001"],
  "npa_score": 82.5,
  "status": "ALIGNED",
  "case_trigger_candidate": true,
  "human_review_required": true,
  "production_allowed": false
}
```

### 11.3 npa_score_ledger.csv

```csv
npa_id,narrative_id,date,score,status,physical_alignment,physical_confidence,contradiction_penalty,data_quality_penalty,quality_status,production_allowed
```

---

## 12. 报告要求

新增：

```text
physical_signal_report.md
npa_score_report.md
reality_check_report.md
shadowbroker_absorption_report.md
```

### 12.1 physical_signal_report.md

必须包含：

```text
物理信号总数
按 signal_type 分布
按 geo_region 分布
READY/PARTIAL/DATA_INSUFFICIENT 分布
高 deviation 信号
低 confidence 信号
```

### 12.2 npa_score_report.md

必须包含：

```text
NPA 样本数
STRONG_ALIGNMENT 数量
DIVERGENCE 数量
STRONG_DIVERGENCE 数量
叙事强但现实弱案例
现实强但市场弱案例
```

### 12.3 reality_check_report.md

必须包含：

```text
NarrativeEvent 总数
已连接 PhysicalSignal 数
未连接数
ALIGNED / DIVERGENT / PHYSICAL_PRE_SIGNAL 分布
Case trigger candidate 清单
```

### 12.4 shadowbroker_absorption_report.md

必须明确：

```text
ShadowBroker deployed: FALSE
External API enabled: FALSE
Docker used: FALSE
Runtime enabled: FALSE
Adapter mode: STUB_ONLY
Production: BLOCKED
Broker/runtime: BLOCKED
Real trade: BLOCKED
```

---

## 13. Fixture 要求

必须创建：

```text
tests/fixtures/event_physical/
  sample_ais_port_density.jsonl
  sample_gps_jamming.jsonl
  sample_shipping_route_change.jsonl
  sample_energy_transport_anomaly.jsonl
  sample_geopolitical_event.jsonl
  sample_narrative_events.jsonl
  sample_market_reaction.jsonl
```

### 13.1 sample_narrative_events.jsonl

```json
{"narrative_id":"NAR-001","event_type":"SHIPPING_NEWS","event_time":"2026-06-01","title":"Shipping congestion narrative","narrative_strength":85,"related_industries":["SHIPPING"],"related_chains":["GLOBAL_LOGISTICS"],"production_allowed":false}
```

### 13.2 sample_ais_port_density.jsonl

```json
{"signal_id":"PHY-AIS-001","signal_type":"AIS_PORT_DENSITY","event_time":"2026-06-01","geo_region":"SINGAPORE_PORT","source":"fixture","raw_value":1250,"baseline_value":900,"normalized_value":0.82,"deviation_score":2.1,"confidence":0.85,"related_industries":["SHIPPING"],"related_chains":["GLOBAL_LOGISTICS"],"related_tickers":[],"quality_status":"READY","production_allowed":false}
```

### 13.3 sample_gps_jamming.jsonl

```json
{"signal_id":"PHY-GPS-001","signal_type":"GPS_JAMMING","event_time":"2026-06-01","geo_region":"RED_SEA","source":"fixture","raw_value":0.76,"baseline_value":0.20,"normalized_value":0.88,"deviation_score":3.0,"confidence":0.80,"related_industries":["SHIPPING","ENERGY"],"related_chains":["GLOBAL_LOGISTICS","OIL_TRANSPORT"],"related_tickers":[],"quality_status":"READY","production_allowed":false}
```

---

## 14. 测试要求

新增：

```text
tests/research_db/event_physical/
  test_physical_signal_schema.py
  test_narrative_event_schema.py
  test_reality_check_schema.py
  test_npa_score_schema.py
  test_physical_signal_loader.py
  test_shadowbroker_adapter_stub.py
  test_reality_check_linker.py
  test_npa_scorer.py
  test_physical_signal_quality_checker.py
  test_caseforge_trigger_extension.py
  test_eventhub_extension.py
  test_no_deployment_boundary.py
```

### 14.1 必测断言

#### schema

```text
signal_id 为空 → ERROR
confidence > 1 → ERROR
production_allowed=True → ERROR
quality_status=READY 但 normalized_value 缺失 → ERROR
```

#### adapter stub

```text
adapter_healthcheck.external_api_enabled == false
adapter_healthcheck.docker_required == false
adapter_healthcheck.runtime_enabled == false
adapter_healthcheck.production_allowed == false
query_physical_signals 只读 fixture
代码中不得 import requests/httpx/aiohttp 用于外部调用
```

#### NPA scorer

```text
强 narrative + 强 physical → STRONG_ALIGNMENT
强 narrative + 弱 physical → DIVERGENCE
弱 narrative + 强 physical → PHYSICAL_PRE_SIGNAL
缺物理信号 → DATA_INSUFFICIENT
score 必须在 0–100
production_allowed=false
```

#### RealityCheck linker

```text
相同行业/链条/时间窗口 → linked
无匹配 → DATA_INSUFFICIENT
link_quality 正确
```

#### CaseForge trigger

```text
NPA < 30 + narrative_strength >= 70 → NARRATIVE_REALITY_DIVERGENCE
NPA >= 80 + market_reaction < 30 → PHYSICAL_PRE_SIGNAL
所有 case production_allowed=false
human_review_required=true
```

#### no deployment boundary

```text
不得出现 docker-compose
不得出现 SHADOWBROKER_API_KEY
不得出现 external_api_enabled=True
不得出现 runtime_enabled=True
不得出现 production_allowed=True
```

---

## 15. Verify 脚本

新增：

```text
scripts/verify_zg16_physical_reality_layer.sh
```

内容必须执行：

```bash
#!/usr/bin/env bash
set -euo pipefail

echo "═══ Z-G16 Physical Reality Layer Verification ═══"

python -m compileall zmatrix tests scripts

PYTHONPATH=. python3 -m pytest -q tests/research_db/event_physical/

python3 - <<'PY'
from pathlib import Path

required_modules = [
    "zmatrix/research_db/event_physical/physical_signal_schema.py",
    "zmatrix/research_db/event_physical/narrative_event_schema.py",
    "zmatrix/research_db/event_physical/reality_check_schema.py",
    "zmatrix/research_db/event_physical/npa_score_schema.py",
    "zmatrix/research_db/event_physical/physical_signal_loader.py",
    "zmatrix/research_db/event_physical/shadowbroker_adapter_stub.py",
    "zmatrix/research_db/event_physical/reality_check_linker.py",
    "zmatrix/research_db/event_physical/npa_scorer.py",
    "zmatrix/research_db/event_physical/physical_signal_quality_checker.py",
    "zmatrix/research_db/event_physical/eventhub_extension.py",
    "zmatrix/research_db/event_physical/caseforge_trigger_extension.py",
    "zmatrix/research_db/event_physical/physical_signal_report.py",
]

for p in required_modules:
    assert Path(p).exists(), f"Missing module: {p}"

for p in Path("zmatrix/research_db/event_physical").rglob("*.py"):
    text = p.read_text(encoding="utf-8", errors="ignore")
    forbidden = [
        "external_api_enabled=True",
        "docker_required=True",
        "runtime_enabled=True",
        "real_trade_allowed=True",
        "broker_order_allowed=True",
        "auto_buy_allowed=True",
        "auto_sell_allowed=True",
        "production_allowed=True",
        "SHADOWBROKER_API_KEY",
        "docker-compose",
    ]
    for token in forbidden:
        assert token not in text, f"Forbidden token {token} in {p}"

print("✅ Z-G16 Physical Reality Layer verification PASS")
PY

echo "═══ Z-G16 PASS ═══"
```

---

## 16. 执行批次

### Batch G16-A：文档与范围锁

创建：

```text
ZG16_PHYSICAL_REALITY_LAYER.md
Z_EVENTBROKER_PROTOCOL.md
NPA_SCORE_POLICY.md
SHADOWBROKER_ABSORPTION_SCOPE.md
PHYSICAL_REALITY_NO_DEPLOYMENT_BOUNDARY.md
```

Commit：

```bash
git add .
git commit -m "zg16-a: add physical reality layer architecture and scope lock"
```

---

### Batch G16-B：数据目录与 Schema

创建：

```text
data/research_db/event/physical/
zmatrix/research_db/event_physical/*schema.py
```

Commit：

```bash
git add .
git commit -m "zg16-b: add physical signal schemas and event lake extension"
```

---

### Batch G16-C：Adapter Stub + Loader

实现：

```text
physical_signal_loader.py
shadowbroker_adapter_stub.py
```

硬门：

```text
只读 fixture
不外呼 API
healthcheck 标明 STUB_ONLY
```

Commit：

```bash
git add .
git commit -m "zg16-c: implement shadowbroker adapter stub"
```

---

### Batch G16-D：NPA + RealityCheck

实现：

```text
reality_check_linker.py
npa_scorer.py
physical_signal_quality_checker.py
eventhub_extension.py
```

Commit：

```bash
git add .
git commit -m "zg16-d: implement npa scoring and reality check linking"
```

---

### Batch G16-E：CaseForge Trigger Extension + Reports

实现：

```text
caseforge_trigger_extension.py
physical_signal_report.py
reports/*
```

Commit：

```bash
git add .
git commit -m "zg16-e: add caseforge physical signal triggers and reports"
```

---

### Batch G16-F：Fixtures + Tests + Verify

创建：

```text
tests/fixtures/event_physical/
tests/research_db/event_physical/
scripts/verify_zg16_physical_reality_layer.sh
```

Commit：

```bash
git add .
git commit -m "zg16-f: add physical reality tests and verification"
```

---

### Batch G16-G：Closeout

创建：

```text
docs/research_db/ZG16_ACCEPTANCE_MATRIX.md
docs/research_db/ZG16_CLOSEOUT_REPORT.md
```

Commit：

```bash
git add .
git commit -m "zg16-g: close physical reality layer absorption"
```

---

## 17. Acceptance Matrix

文件：

```text
docs/research_db/ZG16_ACCEPTANCE_MATRIX.md
```

内容：

```markdown
# Z-G16 Physical Reality Layer Acceptance Matrix

| Item | Requirement | Status |
|---|---|---|
| G16-1 | Architecture scope lock | DONE |
| G16-2 | No-deployment boundary | DONE |
| G16-3 | PhysicalSignal schema | DONE |
| G16-4 | NarrativeEvent schema | DONE |
| G16-5 | RealityCheck schema | DONE |
| G16-6 | NPA score schema | DONE |
| G16-7 | ShadowBrokerAdapterStub | DONE |
| G16-8 | RealityCheckLinker | DONE |
| G16-9 | NPA scorer | DONE |
| G16-10 | CaseForge trigger extension | DONE |
| G16-11 | EventLake extension | DONE |
| G16-12 | Fixtures | DONE |
| G16-13 | Tests | DONE |
| G16-14 | Verify script | DONE |
| G16-15 | No external API / no Docker / no runtime | DONE |

Final Status: ZG16_STUB_READY  
ShadowBroker deployed: FALSE  
External API enabled: FALSE  
Production: BLOCKED  
Broker/runtime: BLOCKED  
Real trade: BLOCKED
```

---

## 18. Closeout Report

文件：

```text
docs/research_db/ZG16_CLOSEOUT_REPORT.md
```

必须包含：

```markdown
# Z-G16 Physical Reality Layer Closeout Report

## Final Status

Z-G16 Physical Reality Layer: PASS  
Mode: STUB_ONLY  
ShadowBroker deployed: FALSE  
External API enabled: FALSE  
Docker used: FALSE  
Runtime enabled: FALSE  

## Completed

- Architecture scope lock
- Z-EventBroker protocol
- PhysicalSignal schema
- NarrativeEvent schema
- RealityCheck schema
- NPA score schema
- ShadowBrokerAdapterStub
- RealityCheckLinker
- NPA scorer
- CaseForge trigger extension
- EventLake extension
- Fixtures
- Tests
- Verify script

## Safety

Production: BLOCKED  
Broker/runtime: BLOCKED  
Real trade: BLOCKED  
Auto buy/sell: BLOCKED  

## Next Step

Do not deploy ShadowBroker.

Next allowed steps:
1. Continue ResearchDB Phase 1–6.
2. Use Z-G16 fixture output as Phase 6 EventLake extension.
3. Re-evaluate real ShadowBroker deployment only after AutoCaseForge and EventLake have stable sample volume.
```

---

## 19. 完成报告格式

天师完成后必须输出：

```text
## Z-G16 Physical Reality Layer 完成报告

commit:
branch:

### Scope
- ShadowBroker deployed:
- External API enabled:
- Docker used:
- Runtime enabled:
- Adapter mode:

### Docs
- ZG16_PHYSICAL_REALITY_LAYER:
- Z_EVENTBROKER_PROTOCOL:
- NPA_SCORE_POLICY:
- SHADOWBROKER_ABSORPTION_SCOPE:
- PHYSICAL_REALITY_NO_DEPLOYMENT_BOUNDARY:

### Code
- physical_signal_schema:
- narrative_event_schema:
- reality_check_schema:
- npa_score_schema:
- shadowbroker_adapter_stub:
- reality_check_linker:
- npa_scorer:
- caseforge_trigger_extension:

### Fixtures
- AIS:
- GPS jamming:
- shipping route:
- energy transport:
- geopolitical:
- narrative events:

### Tests
- tests/research_db/event_physical:
- verify_zg16_physical_reality_layer:

### Safety
- Production:
- Broker/runtime:
- Real trade:
- Auto buy/sell:
- External API:
- Docker:

### Final Decision
ZG16_STUB_READY / ZG16_BLOCKED
```

---

## 20. 未来真实部署条件

只有满足以下条件，才允许讨论真实部署 ShadowBroker：

```text
1. ResearchDB Phase 1–6 已完成
2. AutoCaseForge 能稳定自动建案
3. EventLake 至少已有 1000 个事件样本
4. ZC35 至少已有 100 个催化案例
5. NPA Stub 已证明有研究价值
6. 系统能证明物理信号能改善 CaseForge / ZC35 / Regime 判断
7. 仍保持 no production / no broker / no runtime 交易硬门
```

到那时才可新增：

```text
ShadowBrokerBridge
PhysicalSignalCollector
OSINTFeedRegistry
RateLimiter
CacheStore
APIKeyVaultPolicy
```

当前全部禁止。

---

## 21. 最终裁决

Z-G16 的本质不是“接入 ShadowBroker”。

而是：

```text
把 ShadowBroker 的多源现实世界事件聚合思想，
吸收到 Z-MATRIX 的事件研究系统里。
```

它给 Z-MATRIX 增加的不是交易按钮，而是：

```text
现实验证能力
叙事一致性评分
物理预期差信号
宏观物理水温
事件案例新来源
```

当前最优执行策略：

```text
只做协议
只做 stub
只做 fixture
只进 ResearchDB/EventLake
只触发 AutoCaseForge 草稿
不部署
不外呼
不生产
```

这才符合 Z-MATRIX 当前阶段的最优工程路径。
