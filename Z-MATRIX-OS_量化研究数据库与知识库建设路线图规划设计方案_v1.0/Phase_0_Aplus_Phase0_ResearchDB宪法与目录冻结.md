# Phase 0：ResearchDB 宪法与目录冻结｜A+加固执行版

> **版本**：A+ Hardened Execution Spec
> **用途**：交给 OpenClaw 天师 / deepseek-v4-pro 执行，要求无漂移、无歧义、可测试、可审计、可长期维护。
> **重要说明**：本文档在原 Phase 设计基础上加入防漂移执行层。若原文与加固层冲突，以加固层为准。


---

# A/A+ 加固执行层｜DeepSeek-v4-Pro / OpenClaw 防漂移军规

> 本节为强制执行层。下方原始设计内容不得被摘要化、不得被自由解释、不得被“等价实现”替代。OpenClaw / deepseek-v4-pro 必须按本文档的目录、文件、函数、测试、verify、closeout 顺序落地。

## A0. 执行等级

```text
目标执行等级：A / A+
允许产出：research-only / paper-only 工程代码、schema、fixture、测试、报告、verify
禁止产出：真实交易、broker 接口、runtime daemon、production 开关、自动买卖、RC 状态变更
```

## A1. 全局硬门

所有新增代码、报告、JSON、YAML、Ledger、测试输出必须保持：

```json
{
  "real_trade_allowed": false,
  "broker_order_allowed": false,
  "runtime_enabled": false,
  "auto_buy_allowed": false,
  "auto_sell_allowed": false,
  "production_allowed": false,
  "paper_only": true,
  "human_review_required": true
}
```

禁止在业务输出中出现：

```text
BUY
SELL
STRONG_BUY
AUTO_BUY
AUTO_SELL
BROKER_ORDER
PLACE_ORDER
SEND_ORDER
EXECUTE_TRADE
PRODUCTION_READY
REAL_TRADE_READY
```

如果作为“禁止词清单”出现在文档或测试里，必须加 `allowlist: forbidden-token-definition` 注释，不得被业务模块输出。

## A2. 执行方式

```text
1. 每个 Batch 独立 commit。
2. 每个 Batch 完成后必须运行对应测试。
3. Closeout 前必须运行本 Phase verify。
4. Phase verify 失败，不得提交 Closeout。
5. 不得自动进入下一 Phase。
6. 不得顺手修其他 Phase。
7. 不得修改 RC1 / production / broker / runtime 状态。
```

## A3. 文件实现优先级

OpenClaw 必须按顺序实现：

```text
1. docs / data 目录与 README
2. schema / enum / constants
3. pure function modules
4. fixture
5. unit tests
6. report generator
7. verify script
8. acceptance matrix
9. closeout report
```

禁止先写报告再补代码，禁止只创建空文件通过验收。

## A4. 测试与验收硬规则

每个 Phase 必须至少具备：

```text
1. Schema validation tests
2. Enum validation tests
3. Missing data tests
4. Safety boundary tests
5. Verify script test
6. Report generation smoke test
7. No-production scan
8. Closeout consistency test
```

测试不得只检查“文件存在”。每个核心函数必须至少有：

```text
正常样本
缺失字段样本
非法枚举样本
边界样本
安全阻断样本
```

## A5. Closeout 输出格式

每个 Phase 完成后必须输出：

```text
commit:
branch:
phase:
status:
files_created:
files_modified:
tests_run:
verify_run:
known_limitations:
blocked_items:
safety_state:
next_phase_allowed:
```

`safety_state` 必须逐项列出：

```text
real_trade_allowed=False
broker_order_allowed=False
runtime_enabled=False
auto_buy_allowed=False
auto_sell_allowed=False
production_allowed=False
paper_only=True
human_review_required=True
```

## A6. 失败即停规则

出现以下任一情况必须停止，不得继续：

```text
1. 任何测试失败。
2. verify 脚本失败。
3. 发现 production/broker/runtime/real_trade flag。
4. 原始私有数据被 git track。
5. T20/T60 不足却被标为 ready。
6. CURRENT_SNAPSHOT_ONLY 被用于历史回测。
7. 单案例被晋级为规则。
8. LLM 输出连续主观评分。
9. 报告给出 BUY/SELL/AUTO_EXECUTE。
```

---

# 原始 Phase 设计内容

# Phase 0：ResearchDB 宪法与目录冻结

> **所属总路线**：Z-MATRIX-OS｜量化研究数据库与知识库建设路线图  
> **阶段编号**：Phase 0  
> **阶段名称**：ResearchDB Constitution & Directory Freeze  
> **执行对象**：OpenClaw 天师 / deepseek-v4-pro  
> **阶段性质**：数据库治理地基 / 目录冻结 / 数据可信度宪法  
> **阶段目标**：在导入任何 5 年实盘数据之前，先冻结 ResearchDB 的目录结构、数据边界、可信度等级、PIT 规则、Outcome Horizon 规则、Promotion 规则和 No-Production 安全边界。  
> **硬边界**：Research Only / Paper Only / No Broker / No Runtime / No Real Trade / No Production

---

## 0. 总裁决

Phase 0 不是“导入数据”，也不是“写策略代码”。

Phase 0 的唯一目标是：

```text
先给 ResearchDB 建宪法、建目录、建字段规范、建可信度等级、建验证脚本。
```

如果 Phase 0 没做好，后续 5 年实盘数据、行业映射、因子验证、案例记忆都会变成不可治理的数据泥潭。

本阶段只允许做：

```text
1. 创建 docs/research_db/ 宪法文件
2. 创建 data/research_db/ 标准目录骨架
3. 创建 zmatrix/research_db/ 基础 schema / registry / policy 模块
4. 创建 tests/research_db/ 验证测试
5. 创建 scripts/verify_research_db_phase0.sh
6. 输出 Phase 0 closeout 文档
```

本阶段禁止：

```text
1. 不导入真实交易数据
2. 不接入 broker
3. 不开启 runtime
4. 不生成实盘交易信号
5. 不修改 RC1 结论
6. 不修改 production 状态
7. 不做行业深研
8. 不写因子有效性结论
9. 不自动晋级任何规则
```

---

# 一、Phase 0 的必要性

Z-MATRIX-OS 当前已经有 v4.0 治理骨架，但 ResearchDB 将承载更长期、更复杂、更高价值的数据资产：

```text
过去 5 年实盘交易
观察仓和候选仓
信号结果验证
行业/产业链映射
财务截面
事件催化
CaseForge 案例
个人操盘画像
```

这些数据一旦开始积累，最怕三类污染：

## 1. 时间污染

例如：

```text
当前财务截面被误用于历史回测
未来结果被误用于过去信号判断
T20 不足却用最后价格代替
```

## 2. 证据污染

例如：

```text
人工判断、网络新闻、公告、财报、行情数据混在一起
没有 source / as_of_date / ingested_at
不知道哪些数据可信、哪些只可观察
```

## 3. 晋级污染

例如：

```text
一个案例就沉淀成规则
一个规则候选直接进入因子
一个 paper-only 信号被误读为交易信号
研究结论误进入 production
```

Phase 0 的任务就是从制度上阻断这些污染。

---

# 二、Phase 0 总目标

建立 7 个基础治理能力：

```text
1. ResearchDB 目录标准
2. 数据可信度等级
3. PIT 安全规则
4. Outcome Horizon 规则
5. 数据源能力地图
6. 规则晋级政策
7. No-Production 硬边界
```

最终输出：

```text
ResearchDB 可以开始安全接收 5 年实盘数据。
```

但仍然：

```text
不允许生产
不允许实盘
不允许 broker
不允许 runtime
不允许自动交易
```

---

# 三、必须创建的目录结构

## 3.1 docs 目录

```text
docs/research_db/
  RESEARCH_DB_CONSTITUTION.md
  DATA_TRUST_LEVEL_POLICY.md
  PIT_SAFETY_POLICY.md
  OUTCOME_HORIZON_POLICY.md
  DATA_SOURCE_CAPABILITY_POLICY.md
  RESEARCH_DB_PROMOTION_POLICY.md
  NO_PRODUCTION_BOUNDARY.md
  RESEARCH_DB_DIRECTORY_STANDARD.md
  PHASE0_ACCEPTANCE_MATRIX.md
  PHASE0_CLOSEOUT_REPORT.md
```

## 3.2 data 目录

```text
data/research_db/
  README.md

  account/
    README.md
    .gitkeep

  universe/
    README.md
    .gitkeep

  market/
    README.md
    .gitkeep

  finance/
    README.md
    .gitkeep

  signal/
    README.md
    .gitkeep

  outcome/
    README.md
    .gitkeep

  factor/
    README.md
    .gitkeep

  event/
    README.md
    .gitkeep

  caseforge/
    README.md
    .gitkeep

  knowledge/
    README.md
    methodology/
      .gitkeep
    industries/
      .gitkeep
    chains/
      .gitkeep
    company_profiles/
      .gitkeep
    false_signal_library/
      .gitkeep
```

## 3.3 代码目录

```text
zmatrix/research_db/
  __init__.py
  constitution.py
  directory_registry.py
  trust_level.py
  pit_policy.py
  outcome_horizon_policy.py
  data_source_capability.py
  promotion_policy.py
  no_production_boundary.py
  research_db_status.py
```

## 3.4 测试目录

```text
tests/research_db/
  test_phase0_directory_standard.py
  test_data_trust_level_policy.py
  test_pit_safety_policy.py
  test_outcome_horizon_policy.py
  test_data_source_capability_policy.py
  test_promotion_policy.py
  test_no_production_boundary.py
  test_phase0_acceptance_matrix.py
```

## 3.5 脚本

```text
scripts/verify_research_db_phase0.sh
```

---

# 四、ResearchDB 宪法文件要求

## 4.1 RESEARCH_DB_CONSTITUTION.md

必须写明：

```text
ResearchDB 是 Z-MATRIX-OS 的长期研究数据底座。
ResearchDB 不是 production 数据库。
ResearchDB 不是 broker 数据库。
ResearchDB 不生成真实交易指令。
ResearchDB 的所有数据默认 research_only / paper_only。
```

必须包含 10 条宪法原则：

```text
1. 事实先于结论
2. 数据先于叙事
3. 时间戳先于回测
4. 证据等级先于评分
5. 结果验证先于规则晋级
6. 单案例不得形成规则
7. 当前截面不得伪装历史 PIT
8. Paper-only 不得变成 production
9. 人工裁决高于系统自动晋级
10. 所有数据变更必须可审计
```

---

## 4.2 DATA_TRUST_LEVEL_POLICY.md

必须定义数据可信度等级：

```text
T0_RAW_IMPORT
T1_FORMAT_VALIDATED
T2_SOURCE_VALIDATED
T3_CROSS_SOURCE_VALIDATED
T4_OUTCOME_VALIDATED
T5_RESEARCH_ACCEPTED
```

### 等级定义

```text
T0_RAW_IMPORT：
原始导入数据，仅完成文件接收，不可用于判断。

T1_FORMAT_VALIDATED：
字段格式正确，但来源未校验。

T2_SOURCE_VALIDATED：
来源可信，字段解释清楚，可用于 research。

T3_CROSS_SOURCE_VALIDATED：
跨源一致，可用于高置信研究。

T4_OUTCOME_VALIDATED：
已与后验结果完成验证，可用于因子/案例分析。

T5_RESEARCH_ACCEPTED：
经过跨案例/跨样本验证，可成为 research rule。
```

### 禁止

```text
任何 T0/T1 数据不得进入因子晋级。
任何 T0/T1 数据不得用于结论性报告。
任何未标记 trust_level 的数据不得进入 ResearchDB 主流程。
```

---

## 4.3 PIT_SAFETY_POLICY.md

必须定义：

```text
PIT = Point-in-Time
```

即：

```text
在某个 trade_date 当时已经可知的数据。
```

### PIT 状态枚举

```text
PIT_SAFE
PIT_UNSAFE
CURRENT_SNAPSHOT_ONLY
UNKNOWN_PIT_STATUS
BLOCKED_FOR_BACKTEST
```

### 规则

```text
1. 当前财务截面默认 CURRENT_SNAPSHOT_ONLY。
2. 没有 as_of_date 的数据默认 UNKNOWN_PIT_STATUS。
3. as_of_date > trade_date 的数据必须 BLOCKED_FOR_BACKTEST。
4. 新闻/公告必须有 event_time 或 publish_time。
5. 手工补录数据必须标记 manual_reconstructed=true。
6. PIT_UNSAFE 数据不得进入历史回测。
7. UNKNOWN_PIT_STATUS 不得进入因子验证。
```

---

## 4.4 OUTCOME_HORIZON_POLICY.md

必须写死：

```text
T1  = 1 个 forward trading day
T3  = 3 个 forward trading days
T5  = 5 个 forward trading days
T10 = 10 个 forward trading days
T20 = 20 个 forward trading days
T60 = 60 个 forward trading days
```

### 严格规则

```text
T20 必须严格需要 20 个 forward trading days。
T60 必须严格需要 60 个 forward trading days。
不足不能用最后价格代替。
```

### 不足窗口返回

```json
{
  "ready": false,
  "blocked_reason": "INSUFFICIENT_FORWARD_TRADING_DAYS",
  "fallback_last_price_allowed": false
}
```

---

## 4.5 DATA_SOURCE_CAPABILITY_POLICY.md

必须定义数据源能力字段：

```csv
data_source,coverage,historical_depth,pit_safe,cost,license,refresh_frequency,usable_for_backtest,usable_for_current_snapshot,usable_for_production
```

### 第一批数据源

```text
manual_trade_import
broker_export_file
daily_price_csv
industry_mapping_manual
financial_current_snapshot
event_manual_input
caseforge_auto_event
research_note_manual
```

### 默认规则

```text
manual_trade_import：usable_for_backtest=true, usable_for_production=false
financial_current_snapshot：usable_for_backtest=false, usable_for_current_snapshot=true
event_manual_input：usable_for_backtest=conditional
caseforge_auto_event：usable_for_backtest=false, usable_for_research=true
```

---

## 4.6 RESEARCH_DB_PROMOTION_POLICY.md

必须定义晋级路径：

```text
RAW_DATA
→ FORMAT_VALIDATED
→ SOURCE_VALIDATED
→ CROSS_SOURCE_VALIDATED
→ OUTCOME_VALIDATED
→ RESEARCH_ACCEPTED
→ PAPER_RULE_CANDIDATE
```

### 禁止直跳

```text
RAW_DATA 不得直接进入 OUTCOME_VALIDATED。
单案例不得直接进入 RESEARCH_ACCEPTED。
RESEARCH_ACCEPTED 不得直接 production。
PAPER_RULE_CANDIDATE 不得自动 production。
```

### 案例晋级军规

```text
单案例：LESSON_ONLY
3 个同类案例：RULE_CANDIDATE
10 个跨标的案例：RESEARCH_RULE
20 个跨标的 + 跨行情案例：PAPER_RULE
任何案例：PRODUCTION_ALLOWED=false
```

---

## 4.7 NO_PRODUCTION_BOUNDARY.md

必须写死：

```text
ResearchDB 永远不直接执行交易。
ResearchDB 永远不连接 broker。
ResearchDB 永远不生成 broker_order。
ResearchDB 永远不启 runtime。
ResearchDB 永远不自动 buy/sell。
```

全局硬字段：

```json
{
  "real_trade_allowed": false,
  "broker_order_allowed": false,
  "runtime_enabled": false,
  "auto_buy_allowed": false,
  "auto_sell_allowed": false,
  "production_allowed": false,
  "paper_only": true,
  "human_review_required": true
}
```

---

# 五、代码模块要求

## 5.1 trust_level.py

必须定义：

```python
from enum import Enum

class DataTrustLevel(str, Enum):
    T0_RAW_IMPORT = "T0_RAW_IMPORT"
    T1_FORMAT_VALIDATED = "T1_FORMAT_VALIDATED"
    T2_SOURCE_VALIDATED = "T2_SOURCE_VALIDATED"
    T3_CROSS_SOURCE_VALIDATED = "T3_CROSS_SOURCE_VALIDATED"
    T4_OUTCOME_VALIDATED = "T4_OUTCOME_VALIDATED"
    T5_RESEARCH_ACCEPTED = "T5_RESEARCH_ACCEPTED"
```

必须提供：

```python
def can_enter_factor_validation(level: DataTrustLevel) -> bool:
    ...

def can_enter_research_report(level: DataTrustLevel) -> bool:
    ...

def can_enter_promotion(level: DataTrustLevel) -> bool:
    ...
```

规则：

```text
T0/T1 不得进入 factor_validation
T0/T1 不得进入 research_report 主结论
T4 及以上才可进入 promotion
```

---

## 5.2 pit_policy.py

必须定义：

```python
class PITStatus(str, Enum):
    PIT_SAFE = "PIT_SAFE"
    PIT_UNSAFE = "PIT_UNSAFE"
    CURRENT_SNAPSHOT_ONLY = "CURRENT_SNAPSHOT_ONLY"
    UNKNOWN_PIT_STATUS = "UNKNOWN_PIT_STATUS"
    BLOCKED_FOR_BACKTEST = "BLOCKED_FOR_BACKTEST"
```

必须提供：

```python
def evaluate_pit_status(trade_date: str, as_of_date: str | None, current_snapshot: bool = False) -> PITStatus:
    ...
```

规则：

```text
as_of_date is None → UNKNOWN_PIT_STATUS
current_snapshot=True → CURRENT_SNAPSHOT_ONLY
as_of_date > trade_date → BLOCKED_FOR_BACKTEST
as_of_date <= trade_date → PIT_SAFE
```

---

## 5.3 outcome_horizon_policy.py

必须定义：

```python
HORIZON_DAYS = {
    "T1": 1,
    "T3": 3,
    "T5": 5,
    "T10": 10,
    "T20": 20,
    "T60": 60,
}
```

必须提供：

```python
def validate_forward_window(horizon: str, available_forward_days: int) -> dict:
    ...
```

返回：

```python
{
    "horizon": "T20",
    "required_days": 20,
    "available_days": 18,
    "ready": False,
    "blocked_reason": "INSUFFICIENT_FORWARD_TRADING_DAYS",
    "fallback_last_price_allowed": False
}
```

---

## 5.4 data_source_capability.py

必须定义：

```python
@dataclass
class DataSourceCapability:
    data_source: str
    coverage: str
    historical_depth: str
    pit_safe: bool
    cost: str
    license: str
    refresh_frequency: str
    usable_for_backtest: bool
    usable_for_current_snapshot: bool
    usable_for_production: bool = False
```

必须提供第一批注册表：

```python
DATA_SOURCE_CAPABILITY_REGISTRY = {
    ...
}
```

所有 source 的 `usable_for_production` 必须是 False。

---

## 5.5 promotion_policy.py

必须定义：

```python
class PromotionStage(str, Enum):
    RAW_DATA = "RAW_DATA"
    FORMAT_VALIDATED = "FORMAT_VALIDATED"
    SOURCE_VALIDATED = "SOURCE_VALIDATED"
    CROSS_SOURCE_VALIDATED = "CROSS_SOURCE_VALIDATED"
    OUTCOME_VALIDATED = "OUTCOME_VALIDATED"
    RESEARCH_ACCEPTED = "RESEARCH_ACCEPTED"
    PAPER_RULE_CANDIDATE = "PAPER_RULE_CANDIDATE"
```

必须提供：

```python
def can_promote_case(case_count: int, cross_ticker_count: int, regime_count: int) -> dict:
    ...
```

规则：

```text
case_count < 3 → LESSON_ONLY
case_count >= 3 → RULE_CANDIDATE
cross_ticker_count >= 10 → RESEARCH_RULE
cross_ticker_count >= 20 and regime_count >= 2 → PAPER_RULE
production_allowed=False 永远保持
```

---

## 5.6 no_production_boundary.py

必须定义：

```python
NO_PRODUCTION_BOUNDARY = {
    "real_trade_allowed": False,
    "broker_order_allowed": False,
    "runtime_enabled": False,
    "auto_buy_allowed": False,
    "auto_sell_allowed": False,
    "production_allowed": False,
    "paper_only": True,
    "human_review_required": True,
}
```

必须提供：

```python
def assert_no_production(payload: dict) -> dict:
    ...
```

任何 payload 如果包含：

```text
real_trade_allowed=True
broker_order_allowed=True
runtime_enabled=True
auto_buy_allowed=True
auto_sell_allowed=True
production_allowed=True
```

必须返回：

```json
{
  "status": "BLOCKED",
  "blocked_reason": "PRODUCTION_FLAG_FORBIDDEN"
}
```

---

## 5.7 directory_registry.py

必须定义目录注册表：

```python
RESEARCH_DB_DIRECTORIES = [
    "data/research_db/account",
    "data/research_db/universe",
    "data/research_db/market",
    "data/research_db/finance",
    "data/research_db/signal",
    "data/research_db/outcome",
    "data/research_db/factor",
    "data/research_db/event",
    "data/research_db/caseforge",
    "data/research_db/knowledge",
]
```

必须提供：

```python
def validate_research_db_directories(root: str = ".") -> dict:
    ...
```

---

# 六、测试要求

## 6.1 test_phase0_directory_standard.py

必须验证：

```text
1. docs/research_db/ 存在
2. data/research_db/ 存在
3. 10 个数据子目录存在
4. 10 个宪法文档存在
5. zmatrix/research_db/ 模块存在
```

## 6.2 test_data_trust_level_policy.py

必须验证：

```text
1. T0/T1 不得进入 factor_validation
2. T4/T5 可进入 promotion
3. 未知 trust_level 必须阻断
```

## 6.3 test_pit_safety_policy.py

必须验证：

```text
1. as_of_date <= trade_date → PIT_SAFE
2. as_of_date > trade_date → BLOCKED_FOR_BACKTEST
3. as_of_date None → UNKNOWN_PIT_STATUS
4. current_snapshot=True → CURRENT_SNAPSHOT_ONLY
```

## 6.4 test_outcome_horizon_policy.py

必须验证：

```text
1. T20 available=20 → ready=True
2. T20 available=19 → ready=False
3. T60 available=60 → ready=True
4. T60 available=59 → ready=False
5. fallback_last_price_allowed 永远 False
```

## 6.5 test_data_source_capability_policy.py

必须验证：

```text
1. 所有 source production=false
2. financial_current_snapshot 不可 backtest
3. manual_trade_import 可 backtest
4. 每个 source 必须有 pit_safe 字段
```

## 6.6 test_promotion_policy.py

必须验证：

```text
1. case_count=1 → LESSON_ONLY
2. case_count=3 → RULE_CANDIDATE
3. cross_ticker_count=10 → RESEARCH_RULE
4. cross_ticker_count=20 and regime_count=2 → PAPER_RULE
5. production_allowed=false
```

## 6.7 test_no_production_boundary.py

必须验证：

```text
1. 默认 NO_PRODUCTION_BOUNDARY 全部正确
2. real_trade_allowed=True 被阻断
3. broker_order_allowed=True 被阻断
4. runtime_enabled=True 被阻断
5. production_allowed=True 被阻断
```

---

# 七、verify 脚本要求

新增：

```text
scripts/verify_research_db_phase0.sh
```

内容必须执行：

```bash
#!/usr/bin/env bash
set -euo pipefail

echo "═══ ResearchDB Phase 0 Verification ═══"

python -m compileall zmatrix tests scripts

PYTHONPATH=. python3 -m pytest -q tests/research_db/

python3 - <<'PY'
from pathlib import Path

required_docs = [
    "docs/research_db/RESEARCH_DB_CONSTITUTION.md",
    "docs/research_db/DATA_TRUST_LEVEL_POLICY.md",
    "docs/research_db/PIT_SAFETY_POLICY.md",
    "docs/research_db/OUTCOME_HORIZON_POLICY.md",
    "docs/research_db/DATA_SOURCE_CAPABILITY_POLICY.md",
    "docs/research_db/RESEARCH_DB_PROMOTION_POLICY.md",
    "docs/research_db/NO_PRODUCTION_BOUNDARY.md",
    "docs/research_db/RESEARCH_DB_DIRECTORY_STANDARD.md",
    "docs/research_db/PHASE0_ACCEPTANCE_MATRIX.md",
    "docs/research_db/PHASE0_CLOSEOUT_REPORT.md",
]

for path in required_docs:
    assert Path(path).exists(), f"Missing required doc: {path}"

required_dirs = [
    "data/research_db/account",
    "data/research_db/universe",
    "data/research_db/market",
    "data/research_db/finance",
    "data/research_db/signal",
    "data/research_db/outcome",
    "data/research_db/factor",
    "data/research_db/event",
    "data/research_db/caseforge",
    "data/research_db/knowledge",
]

for path in required_dirs:
    assert Path(path).exists(), f"Missing required dir: {path}"

for p in Path("zmatrix/research_db").rglob("*.py"):
    text = p.read_text(encoding="utf-8", errors="ignore")
    for token in [
        "real_trade_allowed=True",
        "broker_order_allowed=True",
        "runtime_enabled=True",
        "auto_buy_allowed=True",
        "auto_sell_allowed=True",
        "production_allowed=True",
    ]:
        assert token not in text, f"Forbidden token {token} in {p}"

print("✅ ResearchDB Phase 0 verification PASS")
PY

echo "═══ ResearchDB Phase 0 PASS ═══"
```

---

# 八、Acceptance Matrix

新增：

```text
docs/research_db/PHASE0_ACCEPTANCE_MATRIX.md
```

内容：

```markdown
# ResearchDB Phase 0 Acceptance Matrix

| Item | Requirement | Status |
|---|---|---|
| P0-1 | ResearchDB Constitution | DONE |
| P0-2 | Data Trust Level Policy | DONE |
| P0-3 | PIT Safety Policy | DONE |
| P0-4 | Outcome Horizon Policy | DONE |
| P0-5 | Data Source Capability Policy | DONE |
| P0-6 | Promotion Policy | DONE |
| P0-7 | No Production Boundary | DONE |
| P0-8 | Directory Standard | DONE |
| P0-9 | Code Policy Modules | DONE |
| P0-10 | Tests | DONE |
| P0-11 | Verify Script | DONE |

Final Status: PHASE0_READY_FOR_ACCOUNT_TRUTH_IMPORT  
Production: BLOCKED  
Broker/runtime: BLOCKED  
Real trade: BLOCKED  
```

---

# 九、Closeout Report

新增：

```text
docs/research_db/PHASE0_CLOSEOUT_REPORT.md
```

内容必须包含：

```markdown
# ResearchDB Phase 0 Closeout Report

## Final Status

ResearchDB Phase 0: PASS  
Next Phase: Phase 1 Account Truth Import  
Production: BLOCKED  
Broker/runtime: BLOCKED  
Real trade: BLOCKED  

## Completed

- Constitution docs
- Directory freeze
- Data trust level policy
- PIT safety policy
- Outcome horizon policy
- Data source capability policy
- Promotion policy
- No production boundary
- Tests
- Verify script

## Hard Boundaries

- No real trade
- No broker
- No runtime
- No production
- No automatic rule promotion
- No case-to-rule direct jump

## Next Step

Proceed to Phase 1: Account Truth Import.

Phase 1 may import:
- account_daily_snapshot.csv
- trade_ledger.csv
- position_ledger.csv
- cashflow_ledger.csv

Phase 1 must not:
- produce trade signal
- enable production
- modify RC1 status
```

---

# 十、执行批次

## Batch P0-A：目录与文档

```text
创建 docs/research_db/
创建 data/research_db/
创建所有 README.md / .gitkeep
创建 10 份宪法文档
```

Commit：

```bash
git add .
git commit -m "researchdb-phase0-a: add constitution docs and directory skeleton"
```

## Batch P0-B：代码模块

```text
创建 zmatrix/research_db/
实现 trust_level / pit_policy / outcome_horizon / data_source / promotion / no_production / directory_registry
```

Commit：

```bash
git add .
git commit -m "researchdb-phase0-b: implement research db policy modules"
```

## Batch P0-C：测试与 verify

```text
创建 tests/research_db/
创建 verify_research_db_phase0.sh
跑全量测试
```

Commit：

```bash
git add .
git commit -m "researchdb-phase0-c: add phase0 tests and verification"
```

## Batch P0-D：Closeout

```text
更新 PHASE0_ACCEPTANCE_MATRIX.md
更新 PHASE0_CLOSEOUT_REPORT.md
跑 verify
```

Commit：

```bash
git add .
git commit -m "researchdb-phase0-d: close phase0 and approve account truth import"
```

---

# 十一、运行命令

OpenClaw 必须执行：

```bash
python -m compileall zmatrix tests scripts

PYTHONPATH=. python3 -m pytest -q tests/research_db/

bash scripts/verify_research_db_phase0.sh
```

如果任何一条失败：

```text
不得提交 closeout。
不得进入 Phase 1。
```

---

# 十二、完成报告格式

OpenClaw 完成后必须输出：

```text
## ResearchDB Phase 0 完成报告

commit:
branch:

### Docs
- RESEARCH_DB_CONSTITUTION:
- DATA_TRUST_LEVEL_POLICY:
- PIT_SAFETY_POLICY:
- OUTCOME_HORIZON_POLICY:
- DATA_SOURCE_CAPABILITY_POLICY:
- RESEARCH_DB_PROMOTION_POLICY:
- NO_PRODUCTION_BOUNDARY:
- DIRECTORY_STANDARD:

### Directory
- account:
- universe:
- market:
- finance:
- signal:
- outcome:
- factor:
- event:
- caseforge:
- knowledge:

### Code
- trust_level:
- pit_policy:
- outcome_horizon_policy:
- data_source_capability:
- promotion_policy:
- no_production_boundary:
- directory_registry:

### Tests
- tests/research_db:
- verify_research_db_phase0.sh:

### Safety
- real_trade_allowed:
- broker_order_allowed:
- runtime_enabled:
- auto_buy_allowed:
- auto_sell_allowed:
- production_allowed:

### Final Status
ResearchDB Phase 0: PASS / FAIL
Next Phase: Phase 1 Account Truth Import
Production: BLOCKED
Broker/runtime: BLOCKED
Real trade: BLOCKED
```

---

# 十三、通过标准

Phase 0 只有在以下全部满足时通过：

```text
1. 10 份 ResearchDB 宪法文档存在。
2. data/research_db/ 标准目录存在。
3. zmatrix/research_db/ 政策模块存在。
4. tests/research_db/ 全部通过。
5. verify_research_db_phase0.sh 通过。
6. PIT 规则可测试。
7. T20/T60 strict horizon 可测试。
8. Promotion 规则可测试。
9. No Production Boundary 可测试。
10. PHASE0_CLOSEOUT_REPORT 明确允许进入 Phase 1。
```

---

# 十四、阶段结束后的状态

Phase 0 完成后，系统状态应为：

```text
ResearchDB Phase 0: PASS
ResearchDB Status: READY_FOR_ACCOUNT_TRUTH_IMPORT
Production: BLOCKED
Broker/runtime: BLOCKED
Real trade: BLOCKED
RC1 status: unchanged
```

下一阶段：

```text
Phase 1：5年实盘真相库 / Account Truth Import
```

但 Phase 1 仍然只能：

```text
导入、清洗、校验、重建账户曲线
```

不得：

```text
生成交易建议
进入 production
连接 broker
修改 RC1
```

---

# 十五、最终裁决

Phase 0 的本质是：

```text
先给未来所有研究数据建立法治系统。
```

没有 Phase 0，后续数据越多，系统越危险。  
完成 Phase 0 后，Z-MATRIX-OS 才能安全进入真正有价值的阶段：

```text
把过去 5 年实盘数据变成可学习、可验证、可复盘、可长期内化的个人研究资产。
```


---

# Phase 0 A+ 额外加固项

## P0-A+ 必须新增机器可读 Manifest

除原文档要求外，必须新增：

```text
docs/research_db/PHASE0_MACHINE_MANIFEST.json
```

结构：

```json
{
  "phase": "ResearchDB Phase 0",
  "status": "PHASE0_READY_FOR_ACCOUNT_TRUTH_IMPORT",
  "docs_required": [],
  "dirs_required": [],
  "modules_required": [],
  "tests_required": [],
  "verify_script": "scripts/verify_research_db_phase0.sh",
  "production_allowed": false,
  "next_phase_allowed_by_machine": false,
  "human_approval_required": true
}
```

`next_phase_allowed_by_machine` 必须为 false。进入 Phase 1 只能由人工批准。

## P0-A+ 状态一致性测试

新增：

```text
tests/research_db/test_phase0_manifest_consistency.py
```

必须验证：

```text
1. Manifest 中 docs_required 全部存在。
2. Manifest 中 dirs_required 全部存在。
3. Manifest 中 modules_required 全部存在。
4. Acceptance Matrix 不得出现 DONE 但文件不存在。
5. Closeout 不得声明 production ready。
```


---

# A/A+ 统一防漂移验收清单

OpenClaw 完成本文档后，必须逐项自检：

```text
[ ] 是否严格按本文档目录创建文件？
[ ] 是否所有 schema 都有 enum 与 required fields？
[ ] 是否所有核心函数都有明确返回结构？
[ ] 是否所有 fixture 都是虚构或非私有样本？
[ ] 是否所有真实私有 raw 数据已被 .gitignore 阻断？
[ ] 是否所有 tests 都运行通过？
[ ] 是否 verify 脚本运行通过？
[ ] 是否 Acceptance Matrix 与真实完成状态一致？
[ ] 是否 Closeout Report 没有夸大完成度？
[ ] 是否 production/broker/runtime/real_trade 全部 BLOCKED？
[ ] 是否没有自动进入下一 Phase？
```

最终状态只能是：

```text
PASS：全部完成，允许人工裁决进入下一 Phase
PARTIAL：有非阻断缺口，不能进入下一 Phase
BLOCKED：存在硬门失败，必须修复
```

---

# 交付给用户的完成报告模板

```text
## <Phase Name> 完成报告

commit:
branch:

### Scope
- phase:
- mode: Research Only / Paper Only
- production:
- broker/runtime:
- real trade:

### Implementation
- docs:
- data directories:
- code modules:
- fixtures:
- reports:

### Tests
- pytest:
- verify script:
- safety scan:

### Acceptance Matrix
- DONE:
- PARTIAL:
- BLOCKED:

### Known Limitations
- ...

### Final Decision
PASS / PARTIAL / BLOCKED

### Next Step
等待人工批准是否进入下一 Phase。
```
