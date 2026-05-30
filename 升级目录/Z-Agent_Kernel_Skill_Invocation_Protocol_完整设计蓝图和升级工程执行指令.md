# Z-Agent Kernel & Skill Invocation Protocol｜完整设计蓝图和升级工程执行指令

> **所属系统**：Z-MATRIX-OS  
> **阶段建议**：ResearchDB Phase 0.5  
> **模块定位**：Agent Kernel / Skill Invocation / Runtime Governance / Anti-Tamper / Frontend Action Queue  
> **执行对象**：OpenClaw 天师 + opencode  
> **执行等级**：A+ 可落地工程说明书  
> **核心原则**：少 Agent，多 Skill；强状态机，弱自由发挥；Agent 是受控工人，不是系统主人。  
> **硬边界**：Research Only / Paper Only / No Broker / No Runtime / No Real Trade / No Production / No Direct Agent Mutation  

---

## 0. 总裁决

Z-MATRIX 不能走“多 Agent 群聊”路线。

错误路线：

```text
很多专家 Agent
自由讨论
每个 Agent 都读全仓上下文
每个 Agent 都能写文件
每个 Agent 都能生成结论
最后再让另一个 Agent 汇总
```

这条路必然导致：

```text
1. Token 爆炸
2. 上下文污染
3. 系统状态失真
4. 专家意见互相覆盖
5. Agent 自我发挥
6. ResearchDB 被污染
7. 安全硬门被绕过
8. 审计链断裂
```

正确路线：

```text
1 个主控 Agent
少数执行 Agent
大量结构化 Skill
统一 Skill Registry
统一 Command Envelope
统一 Query Contract
统一 Proposal / Approval / Execution Pipeline
统一 Verify / Audit / Cloud Visibility Gate
```

一句话：

```text
不要建 Agent 群。
要建受控技能工厂。
```

Z-Agent Kernel 的本质不是“增加 Agent 数量”，而是：

```text
限制 Agent
约束 Agent
审计 Agent
隔离 Agent
让 Agent 只能按协议调用 Z-MATRIX 技能管线
```

---

# 第一部分：系统定位

## 1.1 为什么必须补 Z-Agent Kernel？

Z-MATRIX 现在已经有：

```text
V4.0 FINAL-HARDGATES
ResearchDB Constitution
Experiment Ledger
Factor Registry
Promotion Pipeline
No Production Runtime Lock
RC1 Safety Audit
Phase 0 ResearchDB Constitution
```

这些已经能防：

```text
production 误开
broker 误接
runtime 误启
真实交易误触发
```

但还没有系统性解决：

```text
Agent 怎么入住？
Agent 怎么注册？
Agent 有什么权限？
Agent 怎么调用技能？
Agent 怎么调用专家域？
Agent 怎么读 ResearchDB？
Agent 怎么写草稿？
Agent 怎么提交变更？
Agent 怎么防止自我提权？
Agent 怎么防止篡改硬门？
Agent 怎么避免泄露密钥？
Agent 怎么避免 token 爆炸？
Agent 怎么和前端交互？
Agent 结果如何被审计？
```

因此必须新增：

```text
ResearchDB Phase 0.5：Z-Agent Kernel & Skill Invocation Protocol
```

这是未来：

```text
AutoCaseForge 自动化
Z-G16 信息治理
Research Cockpit
月度内化
前端交互控制
LLM 后端驱动
```

的统一 Agent 入住地基。

---

## 1.2 Z-Agent Kernel 的边界

Z-Agent Kernel 允许：

```text
1. 读取已注册数据层
2. 调用已注册技能
3. 生成结构化草稿
4. 生成报告草稿
5. 提交 proposal
6. 等待人工审批
7. 执行已批准任务
8. 跑 verify
9. 写 audit ledger
10. 向前端 action queue 推送展示动作
```

Z-Agent Kernel 禁止：

```text
1. 直接接 broker
2. 直接下单
3. 直接开启 runtime
4. 直接修改 production 状态
5. 直接改 RC1 tag
6. 直接改主分支
7. 直接提交真实券商 raw 文件
8. 直接读取秘密密钥
9. 直接出站发送敏感 payload
10. 直接把未验证结果标 READY
11. 直接把 case 晋级规则
12. 直接把 proposal 当 execution
```

---

## 1.3 目标状态

完成后系统应具备：

```text
Agent 注册中心
Agent 权限矩阵
Agent 命令封装
Skill 注册中心
Skill 调用协议
专家域调用协议
Query Contract
最小上下文读取
Proposal / Approval / Execution 三段式
Agent Workspace 隔离
Agent Tamper Guard
Outbound Payload Sanitizer
Frontend Action Queue
Audit Ledger
Verify Gate
Cloud Visibility Gate
```

---

# 第二部分：Agent 数量策略

## 2.1 常驻 Agent 不超过 1 个

常驻：

```text
Z-Orchestrator Agent
```

职责：

```text
1. 接收用户意图
2. 查询系统摘要
3. 判断需要调用哪些 Skill
4. 组装 AgentCommandEnvelope
5. 提交 proposal
6. 汇总结构化结果
7. 调用报告渲染 Skill
```

禁止：

```text
直接写 ResearchDB
直接改代码
直接改配置
直接生成生产动作
```

---

## 2.2 半常驻 Agent 不超过 2 个

### Z-ReportRenderer Agent

职责：

```text
1. 把结构化 JSON / ledger / scorecard 渲染为用户可读报告
2. 生成月报、案例报告、因子报告、Cockpit Summary
```

禁止：

```text
做研究裁决
改数据
晋级规则
```

### Z-Research Assistant Agent

职责：

```text
1. 调用研究 Skill
2. 生成研究草稿
3. 提交人工 review
```

禁止：

```text
自由讨论
全仓扫描
直接写结论到主账本
```

---

## 2.3 按需 Agent

### OpenClaw Engineering Agent

职责：

```text
1. 工程升级
2. 代码补丁
3. 测试
4. Git 提交
5. 云仓同步
```

触发条件：

```text
用户明确要求工程实现
```

禁止：

```text
常驻运行
自动改系统
直接导入真实券商数据
直接执行 Phase 下一阶段
```

---

## 2.4 专家域不是 Agent，是 Skill

所有专家能力沉淀为：

```text
Reviewer Skill
```

不是常驻 Agent。

例如：

```text
reviewer.data_quality()
reviewer.risk_control()
reviewer.catalyst_timing()
reviewer.execution_quality()
reviewer.financial_quality()
reviewer.behavioral_bias()
reviewer.regime_sensitivity()
reviewer.factor_validity()
```

Reviewer Skill 只能输出：

```text
verdict
risk_flags
missing_evidence
confidence
reason_short
```

不得输出：

```text
买入
卖出
仓位
目标价
生产放行
```

---

# 第三部分：核心架构

## 3.1 总体架构图

```text
User / Frontend
    ↓
HumanIntent
    ↓
Z-Agent Gateway
    ↓
Agent Registry
    ↓
Permission Gate
    ↓
Command Envelope
    ↓
Query Contract / Skill Invocation Contract
    ↓
Proposal Ledger
    ↓
Approval Gate
    ↓
Execution Runner
    ↓
Verify Gate
    ↓
Audit Ledger
    ↓
ResearchDB / CaseForge / FactorFactory / Reports
    ↓
Frontend Action Queue
```

---

## 3.2 调用主链

```text
用户请求
  ↓
Orchestrator 生成 intent
  ↓
读取 research summary
  ↓
判断需要技能
  ↓
创建 AgentCommandEnvelope
  ↓
Permission Gate
  ↓
Skill Invocation
  ↓
返回 SkillResultEnvelope
  ↓
如需写入 → ProposalLedger
  ↓
HumanApprovalGate
  ↓
ExecutionRunner
  ↓
Verify
  ↓
Audit
  ↓
ReportRenderer
```

---

## 3.3 三段式写入原则

Agent 永远不能直接写核心系统。

必须：

```text
Proposal
→ Approval
→ Execution
```

即：

```text
Agent 提议
人或策略门审批
执行器执行
验证器验证
审计器记录
```

---

# 第四部分：必须新增目录

```text
docs/agent/
  Z_AGENT_KERNEL_BLUEPRINT.md
  AGENT_REGISTRY_POLICY.md
  AGENT_PERMISSION_POLICY.md
  AGENT_COMMAND_ENVELOPE.md
  SKILL_REGISTRY_POLICY.md
  SKILL_INVOCATION_CONTRACT.md
  EXPERT_DOMAIN_CONTRACT.md
  AGENT_QUERY_CONTRACT.md
  AGENT_PROPOSAL_APPROVAL_POLICY.md
  AGENT_TAMPER_PROTECTION_POLICY.md
  AGENT_WORKSPACE_POLICY.md
  AGENT_FRONTEND_ACTION_QUEUE.md
  AGENT_TOKEN_BUDGET_POLICY.md
  AGENT_CLOSEOUT_MATRIX.md

zmatrix/agent/
  __init__.py
  agent_registry.py
  agent_identity.py
  agent_permission.py
  command_envelope.py
  command_router.py
  query_contract.py
  skill_registry.py
  skill_invocation.py
  expert_domain_contract.py
  proposal_ledger.py
  approval_gate.py
  execution_runner.py
  verify_gate.py
  audit_ledger.py
  action_queue.py
  workspace_guard.py
  tamper_guard.py
  token_budget.py

zmatrix/agent/security/
  __init__.py
  outbound_payload_sanitizer.py
  secret_pattern_blocker.py
  command_hmac.py
  payload_digest.py

data/research_db/agent/
  README.md
  registry/
    agent_registry.json
    skill_registry.json
    expert_domain_registry.json
  ledgers/
    command_ledger.jsonl
    proposal_ledger.jsonl
    approval_ledger.jsonl
    execution_ledger.jsonl
    audit_ledger.jsonl
    action_queue.jsonl
  workspace/
    .gitkeep
  reports/
    agent_activity_report.md
    agent_security_report.md
    agent_permission_report.md
```

---

# 第五部分：核心 Schema 与函数

## 5.1 Agent Registry

文件：

```text
zmatrix/agent/agent_registry.py
```

### Agent 类型

```python
class AgentType(str, Enum):
    ORCHESTRATOR = "ORCHESTRATOR"
    ENGINEERING = "ENGINEERING"
    RESEARCH = "RESEARCH"
    REPORT_RENDERER = "REPORT_RENDERER"
    FRONTEND_ASSISTANT = "FRONTEND_ASSISTANT"
    MAINTENANCE = "MAINTENANCE"
```

### 权限等级

```python
class AgentPermissionLevel(str, Enum):
    VIEW_ONLY = "VIEW_ONLY"
    ANNOTATION_WRITER = "ANNOTATION_WRITER"
    CASE_DRAFT_WRITER = "CASE_DRAFT_WRITER"
    REPORT_DRAFT_WRITER = "REPORT_DRAFT_WRITER"
    RESEARCH_DB_PROPOSER = "RESEARCH_DB_PROPOSER"
    CODE_PATCH_PROPOSER = "CODE_PATCH_PROPOSER"
    VERIFY_RUNNER = "VERIFY_RUNNER"
    RELEASE_PROPOSER = "RELEASE_PROPOSER"
```

### AgentRegistryEntry

```python
@dataclass
class AgentRegistryEntry:
    agent_id: str
    agent_name: str
    agent_type: AgentType
    owner: str
    role: str
    permission_level: AgentPermissionLevel
    allowed_scopes: list[str]
    allowed_read_layers: list[str]
    allowed_write_layers: list[str]
    allowed_commands: list[str]
    forbidden_commands: list[str]
    max_risk_level: str
    requires_human_review: bool
    workspace_path: str
    enabled: bool
    created_at: str
    production_allowed: bool = False
```

### 必须函数

```python
def load_agent_registry(path: str) -> list[dict]:
    ...

def get_agent(agent_id: str) -> dict:
    ...

def validate_agent_entry(entry: dict) -> dict:
    ...

def assert_agent_enabled(agent_id: str) -> dict:
    ...

def assert_agent_scope(agent_id: str, scope: str) -> dict:
    ...
```

### 硬规则

```text
unknown agent → REJECT
enabled=false → REJECT
production_allowed=true → ERROR
allowed_scopes=["*"] → ERROR
requires_human_review=false 且 risk_level>=R3 → ERROR
```

---

## 5.2 Permission Gate

文件：

```text
zmatrix/agent/agent_permission.py
```

### 风险等级

```python
class CommandRiskLevel(str, Enum):
    R0_READ = "R0_READ"
    R1_ANNOTATE = "R1_ANNOTATE"
    R2_DRAFT = "R2_DRAFT"
    R3_WRITE_RESEARCH_DB = "R3_WRITE_RESEARCH_DB"
    R4_CODE_PATCH_PROPOSAL = "R4_CODE_PATCH_PROPOSAL"
    R5_RELEASE_PROPOSAL = "R5_RELEASE_PROPOSAL"
    R9_FORBIDDEN = "R9_FORBIDDEN"
```

### 函数

```python
def evaluate_agent_permission(agent: dict, command: dict) -> dict:
    ...
```

### 输出

```json
{
  "allowed": false,
  "risk_level": "R3_WRITE_RESEARCH_DB",
  "requires_human_review": true,
  "blocked_reasons": [],
  "production_allowed": false
}
```

---

## 5.3 Agent Command Envelope

文件：

```text
zmatrix/agent/command_envelope.py
```

```python
@dataclass
class AgentCommandEnvelope:
    command_id: str
    agent_id: str
    command_type: str
    created_at: str
    requested_skill: str
    input_refs: list[str]
    target_layers: list[str]
    requested_action: str
    risk_level: str
    idempotency_key: str
    dry_run: bool
    requires_human_review: bool
    production_allowed: bool = False
```

### 函数

```python
def create_command_envelope(payload: dict) -> dict:
    ...

def validate_command_envelope(envelope: dict) -> dict:
    ...

def calculate_command_digest(envelope: dict) -> str:
    ...
```

硬规则：

```text
command_id 必须唯一
agent_id 必须存在
requested_skill 必须注册
target_layers 必须合法
production_allowed 必须 false
risk_level=R9_FORBIDDEN 直接拒绝
```

---

## 5.4 Skill Registry

文件：

```text
zmatrix/agent/skill_registry.py
```

### SkillRegistryEntry

```python
@dataclass
class SkillRegistryEntry:
    skill_id: str
    skill_name: str
    domain: str
    version: str
    input_schema_ref: str
    output_schema_ref: str
    allowed_callers: list[str]
    risk_level: str
    requires_human_review: bool
    read_layers: list[str]
    write_layers: list[str]
    verify_script: str | None
    enabled: bool
    production_allowed: bool = False
```

### Skill Domain

```text
ACCOUNT_TRUTH
MARKET_OUTCOME
FACTOR_FACTORY
AUTOCASEFORGE
ZC35_CATALYST
B_MATRIX
R_MATRIX
D_MATRIX
Z_G16_PHYSICAL
REPORTING
RESEARCH_COUNCIL
COCKPIT
SYSTEM_VERIFY
```

### 函数

```python
def load_skill_registry(path: str) -> list[dict]:
    ...

def get_skill(skill_id: str) -> dict:
    ...

def validate_skill_entry(skill: dict) -> dict:
    ...

def assert_skill_callable(agent_id: str, skill_id: str) -> dict:
    ...
```

硬规则：

```text
unknown skill → REJECT
enabled=false → REJECT
production_allowed=true → ERROR
skill write_layers 非空 → requires_human_review=true
verify_script 缺失且 risk_level>=R3 → ERROR
```

---

## 5.5 Skill Invocation Contract

文件：

```text
zmatrix/agent/skill_invocation.py
```

### 输入

```python
def invoke_skill(command_envelope: dict, context_slice: dict) -> dict:
    ...
```

### 输出

```json
{
  "skill_id": "CASEFORGE.CREATE_CASE_DRAFT",
  "status": "DRAFT_CREATED",
  "output_ref": "case_id:ZCASE-001",
  "evidence_refs": [],
  "quality_status": "PARTIAL",
  "blocked_reason": null,
  "human_review_required": true,
  "production_allowed": false
}
```

硬规则：

```text
SkillResult 必须结构化
不得输出 BUY / SELL / AUTO_EXECUTE
不得输出 READY_FOR_PRODUCTION
不得绕过 ProposalLedger
```

---

## 5.6 Expert Domain Contract

文件：

```text
zmatrix/agent/expert_domain_contract.py
```

### ReviewerSkillOutput

```python
@dataclass
class ReviewerSkillOutput:
    reviewer_id: str
    target_ref: str
    verdict: str
    confidence: float
    risk_flags: list[str]
    missing_evidence: list[str]
    reason_short: str
    production_allowed: bool = False
```

### Verdict 枚举

```text
PASS
WATCH
BLOCK
DATA_INSUFFICIENT
CONFLICTED
NEEDS_HUMAN_REVIEW
```

硬规则：

```text
Reviewer Skill 不得输出交易动作
Reviewer Skill 不得写 ResearchDB
Reviewer Skill 只生成审查结论
```

---

## 5.7 Query Contract

文件：

```text
zmatrix/agent/query_contract.py
```

### 函数

```python
def get_research_summary() -> dict:
    ...

def get_layer_versions() -> dict:
    ...

def get_changed_layers(since_versions: dict) -> dict:
    ...

def get_layer_slice(layer_ids: list[str], since_versions: dict | None = None, limit: int = 100) -> dict:
    ...

def query_case(case_id: str) -> dict:
    ...

def query_event_window(target_id: str, start: str, end: str) -> dict:
    ...

def query_factor(factor_id: str) -> dict:
    ...

def query_hypotheses(filters: dict) -> dict:
    ...
```

### Token 防爆规则

```text
默认不允许全仓扫描
默认 limit <= 100
任何 query 必须返回 token_estimate
超过 token_budget → 返回 NEED_NARROWER_QUERY
```

---

## 5.8 Proposal Ledger

文件：

```text
zmatrix/agent/proposal_ledger.py
```

### Proposal

```python
@dataclass
class AgentProposal:
    proposal_id: str
    command_id: str
    agent_id: str
    target_files: list[str]
    target_layers: list[str]
    proposed_changes: dict
    risk_level: str
    policy_result: dict
    human_review_required: bool
    status: str
    created_at: str
    production_allowed: bool = False
```

### 状态

```text
DRAFT
SUBMITTED
APPROVED
REJECTED
DEFERRED
EXECUTED
VERIFY_FAILED
CLOSED
```

硬规则：

```text
append-only
不得覆盖历史 proposal
proposal_id 唯一
approval 前不得 execution
```

---

## 5.9 Approval Gate

文件：

```text
zmatrix/agent/approval_gate.py
```

函数：

```python
def evaluate_approval_requirement(proposal: dict) -> dict:
    ...

def approve_proposal(proposal_id: str, approver: str, reason: str) -> dict:
    ...

def reject_proposal(proposal_id: str, approver: str, reason: str) -> dict:
    ...
```

硬规则：

```text
R3+ 必须 approval
R4/R5 必须人工 approval
R9 禁止 approval
```

---

## 5.10 Execution Runner

文件：

```text
zmatrix/agent/execution_runner.py
```

执行范围：

```text
approved proposal only
dry_run first
write allowed only to approved target_layers
```

函数：

```python
def execute_approved_proposal(proposal_id: str, dry_run: bool = True) -> dict:
    ...
```

硬规则：

```text
未批准不得执行
dry_run 失败不得 real run
执行后必须 verify
```

---

## 5.11 Verify Gate

文件：

```text
zmatrix/agent/verify_gate.py
```

函数：

```python
def run_verify_for_proposal(proposal_id: str) -> dict:
    ...
```

必须支持：

```text
proposal-specific verify
phase verify
forbidden scan
cloud visibility check placeholder
```

---

## 5.12 Audit Ledger

文件：

```text
zmatrix/agent/audit_ledger.py
```

记录：

```text
command
permission decision
proposal
approval
execution
verify
final status
```

append-only。

---

## 5.13 Workspace Guard

文件：

```text
zmatrix/agent/workspace_guard.py
```

Agent 默认只能写：

```text
runtime/agent_workspace/{agent_id}/
```

禁止直接写：

```text
zmatrix/
docs/
scripts/
data/research_db/account/raw/
.github/
```

除非走 proposal。

---

## 5.14 Tamper Guard

文件：

```text
zmatrix/agent/tamper_guard.py
```

必须扫描：

```text
real_trade_allowed=True
broker_order_allowed=True
runtime_enabled=True
auto_buy_allowed=True
auto_sell_allowed=True
production_allowed=True
production_strategy_modified=True
allowed_scopes=["*"]
requires_human_review=false
subprocess
os.system
eval(
exec(
curl
requests.post
httpx.post
api_key
token
secret
```

注意：

```text
requests/httpx 不是全局禁用。
但在 Agent 未授权模块中出现外部 POST 必须阻断。
```

---

## 5.15 Outbound Payload Sanitizer

文件：

```text
zmatrix/agent/security/outbound_payload_sanitizer.py
```

必须识别并 redact：

```text
OPENAI_API_KEY
ANTHROPIC_API_KEY
GOOGLE_API_KEY
GEMINI_API_KEY
DEEPSEEK_API_KEY
GITHUB_TOKEN
BROKER_TOKEN
EMAIL_TOKEN
COOKIE
Authorization
Bearer
sk-
sk-ant-
AIza
xai-
hf_
```

函数：

```python
def sanitize_payload(payload: dict | str) -> dict:
    ...

def contains_secret(payload: dict | str) -> bool:
    ...

def block_if_account_raw(payload: dict | str) -> dict:
    ...
```

---

## 5.16 Frontend Action Queue

文件：

```text
zmatrix/agent/action_queue.py
```

Action 类型：

```text
OPEN_CASE
FOCUS_TICKER
SHOW_EVENT_WINDOW
SHOW_FACTOR_REPORT
SHOW_HYPOTHESIS
SHOW_ANALYSIS_ZONE
ASK_HUMAN_REVIEW
SHOW_AGENT_PROPOSAL
SHOW_VERIFY_RESULT
SHOW_DATA_QUALITY_WARNING
REQUEST_USER_DECISION
```

硬规则：

```text
Action Queue 只控制前端展示
不得改变 ResearchDB
不得触发交易
不得自动 approval
读取后可 destructive pop
```

---

## 5.17 Token Budget

文件：

```text
zmatrix/agent/token_budget.py
```

策略：

```text
每个 command 有 max_input_tokens
每个 skill 有 max_context_items
每个 query 有 limit
超过预算必须返回 NEED_NARROWER_QUERY
```

函数：

```python
def estimate_tokens(text: str) -> int:
    ...

def enforce_token_budget(payload: dict, budget: int) -> dict:
    ...
```

---

# 第六部分：测试目录

```text
tests/agent/
  test_agent_registry.py
  test_agent_permission.py
  test_command_envelope.py
  test_skill_registry.py
  test_skill_invocation.py
  test_expert_domain_contract.py
  test_query_contract.py
  test_proposal_ledger.py
  test_approval_gate.py
  test_execution_runner.py
  test_verify_gate.py
  test_audit_ledger.py
  test_workspace_guard.py
  test_tamper_guard.py
  test_outbound_payload_sanitizer.py
  test_action_queue.py
  test_token_budget.py
  test_no_direct_agent_mutation.py
```

---

## 6.1 必测断言

### Agent Registry

```text
unknown agent → REJECT
disabled agent → REJECT
allowed_scopes=["*"] → ERROR
production_allowed=true → ERROR
```

### Permission Gate

```text
VIEW_ONLY agent 调 R3 → REJECT
R3 requires human review
R9 always blocked
```

### Skill Registry

```text
unknown skill → REJECT
disabled skill → REJECT
write skill without verify_script → ERROR
production_allowed=true → ERROR
```

### Query Contract

```text
get_research_summary returns compact summary
get_layer_slice respects limit
full scan rejected
over token budget → NEED_NARROWER_QUERY
```

### Proposal / Approval

```text
proposal append-only
unapproved proposal cannot execute
approved proposal can execute dry_run
R4 requires human approval
```

### Tamper Guard

```text
forbidden production flag blocked
self-elevation blocked
secret token blocked
workspace escape blocked
```

### Action Queue

```text
OPEN_CASE allowed
APPROVE_PROPOSAL only creates approval request
action queue cannot mutate ResearchDB
destructive pop works
```

---

# 第七部分：Verify 脚本

新增：

```text
scripts/verify_z_agent_kernel.sh
```

内容：

```bash
#!/usr/bin/env bash
set -euo pipefail

echo "═══ Z-Agent Kernel Verification ═══"

python -m compileall zmatrix tests scripts

PYTHONPATH=. python3 -m pytest -q tests/agent/

python3 - <<'PY'
from pathlib import Path

forbidden = [
    "real_trade_allowed=True",
    "broker_order_allowed=True",
    "runtime_enabled=True",
    "auto_buy_allowed=True",
    "auto_sell_allowed=True",
    "production_allowed=True",
    "production_strategy_modified=True",
    "allowed_scopes=['*']",
    'allowed_scopes=["*"]',
]

for root in ["zmatrix/agent", "docs/agent", "scripts"]:
    for p in Path(root).rglob("*"):
        if p.is_file() and p.suffix in {".py", ".md", ".sh", ".json", ".yaml", ".yml"}:
            text = p.read_text(encoding="utf-8", errors="ignore")
            for token in forbidden:
                assert token not in text, f"Forbidden token {token} in {p}"

print("✅ Z-Agent Kernel forbidden scan PASS")
PY

echo "═══ Z-Agent Kernel PASS ═══"
```

---

# 第八部分：Acceptance Matrix

新增：

```text
docs/agent/AGENT_KERNEL_ACCEPTANCE_MATRIX.md
```

内容：

```markdown
# Z-Agent Kernel Acceptance Matrix

| Item | Requirement | Status |
|---|---|---|
| A0 | Agent Kernel blueprint | DONE |
| A1 | Agent Registry | DONE |
| A2 | Permission Gate | DONE |
| A3 | Command Envelope | DONE |
| A4 | Skill Registry | DONE |
| A5 | Skill Invocation Contract | DONE |
| A6 | Expert Domain Contract | DONE |
| A7 | Query Contract | DONE |
| A8 | Proposal Ledger | DONE |
| A9 | Approval Gate | DONE |
| A10 | Execution Runner | DONE |
| A11 | Verify Gate | DONE |
| A12 | Audit Ledger | DONE |
| A13 | Workspace Guard | DONE |
| A14 | Tamper Guard | DONE |
| A15 | Outbound Payload Sanitizer | DONE |
| A16 | Frontend Action Queue | DONE |
| A17 | Token Budget | DONE |
| A18 | Tests | DONE |
| A19 | Verify Script | DONE |
| A20 | No direct agent mutation | DONE |

Final Status: Z_AGENT_KERNEL_READY_STUB_ONLY  
Production: BLOCKED  
Broker/runtime: BLOCKED  
Real trade: BLOCKED  
Agent direct mutation: BLOCKED  
```

---

# 第九部分：Closeout Report

新增：

```text
docs/agent/AGENT_KERNEL_CLOSEOUT_REPORT.md
```

必须包含：

```markdown
# Z-Agent Kernel Closeout Report

## Final Status

Z-Agent Kernel: PASS  
Mode: STUB_ONLY  
Production: BLOCKED  
Broker/runtime: BLOCKED  
Real trade: BLOCKED  
Agent direct mutation: BLOCKED  

## Completed

- Agent Registry
- Permission Gate
- Command Envelope
- Skill Registry
- Skill Invocation Contract
- Expert Domain Contract
- Query Contract
- Proposal Ledger
- Approval Gate
- Execution Runner
- Verify Gate
- Audit Ledger
- Workspace Guard
- Tamper Guard
- Outbound Payload Sanitizer
- Frontend Action Queue
- Token Budget
- Tests
- Verify Script

## Safety

- No direct ResearchDB mutation by Agent
- No direct code patch by Agent
- No direct production mutation
- No broker/runtime
- No real trade
- No raw account data access
- No secret leakage

## Next Step

Allowed:
1. Connect Z-G16 v1.2 to Agent Kernel.
2. Register first batch of read-only skills.
3. Register CaseForge draft skill as R2_DRAFT.
4. Register verify runner skill.

Forbidden:
1. Do not enable autonomous runtime.
2. Do not enable production.
3. Do not connect broker.
4. Do not allow direct Agent write.
```

---

# 第十部分：OpenClaw + opencode 最小分步执行轮次计划

## 10.1 执行原则

目标是最少轮次，但不能牺牲安全。

推荐：

```text
6 轮主执行
每轮一个可审计 commit group
每轮必须跑局部测试
第 6 轮跑总 verify
```

不要一次性丢全量实现给 OpenClaw。  
原因：

```text
文件多
安全门多
测试多
容易漏掉 proposal/approval/verify/audit 闭环
```

---

## 10.2 OpenClaw 与 opencode 分工

### OpenClaw

负责：

```text
理解工程说明书
拆任务
修改仓库
生成代码
生成文档
跑测试
提交 GitHub
输出完成报告
```

### opencode

负责：

```text
更细粒度的代码编辑
跨文件重构
测试失败修复
局部 patch
静态扫描
```

推荐模式：

```text
OpenClaw 做总控和提交
opencode 做局部代码实现和修复
```

---

## 10.3 最小 6 轮执行计划

### Round 1：Scope Lock + Docs + Registry Skeleton

目标：

```text
只建文档和目录，不实现复杂逻辑。
```

执行内容：

```text
docs/agent/*
data/research_db/agent/*
zmatrix/agent/__init__.py
zmatrix/agent/security/__init__.py
tests/agent/ 目录
```

新增：

```text
Z_AGENT_KERNEL_BLUEPRINT.md
AGENT_REGISTRY_POLICY.md
AGENT_PERMISSION_POLICY.md
SKILL_REGISTRY_POLICY.md
SKILL_INVOCATION_CONTRACT.md
AGENT_QUERY_CONTRACT.md
```

提交：

```bash
git add .
git commit -m "agent-kernel-r1: add scope lock docs and directory skeleton"
```

验收：

```text
目录完整
无 production flags
无 broker/runtime
```

---

### Round 2：Agent Registry + Command Envelope + Permission Gate

目标：

```text
先让 Agent 能被注册、识别、授权、拒绝。
```

实现：

```text
agent_registry.py
agent_identity.py
agent_permission.py
command_envelope.py
```

测试：

```text
test_agent_registry.py
test_agent_permission.py
test_command_envelope.py
```

提交：

```bash
git add .
git commit -m "agent-kernel-r2: implement registry permission and command envelope"
```

验收：

```text
unknown agent rejected
self-elevation rejected
R3 requires human review
production_allowed true rejected
```

---

### Round 3：Skill Registry + Invocation + Expert Domain + Query Contract

目标：

```text
让 Agent 只能通过 Skill Registry 调技能，并用最小上下文读取系统。
```

实现：

```text
skill_registry.py
skill_invocation.py
expert_domain_contract.py
query_contract.py
token_budget.py
```

测试：

```text
test_skill_registry.py
test_skill_invocation.py
test_expert_domain_contract.py
test_query_contract.py
test_token_budget.py
```

提交：

```bash
git add .
git commit -m "agent-kernel-r3: implement skill invocation and query contract"
```

验收：

```text
unknown skill rejected
full scan rejected
token budget enforced
Reviewer Skill cannot emit trade action
```

---

### Round 4：Proposal / Approval / Execution / Verify / Audit

目标：

```text
完成 Agent 写入三段式闭环。
```

实现：

```text
proposal_ledger.py
approval_gate.py
execution_runner.py
verify_gate.py
audit_ledger.py
```

测试：

```text
test_proposal_ledger.py
test_approval_gate.py
test_execution_runner.py
test_verify_gate.py
test_audit_ledger.py
```

提交：

```bash
git add .
git commit -m "agent-kernel-r4: implement proposal approval execution audit pipeline"
```

验收：

```text
unapproved proposal cannot execute
approved proposal dry_run works
execution requires verify
audit append-only
```

---

### Round 5：Workspace Guard + Tamper Guard + Payload Sanitizer + Action Queue

目标：

```text
补 Agent 防篡改、防泄漏、前端动作队列。
```

实现：

```text
workspace_guard.py
tamper_guard.py
security/outbound_payload_sanitizer.py
security/secret_pattern_blocker.py
security/command_hmac.py
security/payload_digest.py
action_queue.py
```

测试：

```text
test_workspace_guard.py
test_tamper_guard.py
test_outbound_payload_sanitizer.py
test_action_queue.py
test_no_direct_agent_mutation.py
```

提交：

```bash
git add .
git commit -m "agent-kernel-r5: add workspace tamper security and action queue"
```

验收：

```text
workspace escape rejected
secret redacted
forbidden flags blocked
action queue cannot mutate ResearchDB
```

---

### Round 6：Verify Script + Acceptance + Closeout

目标：

```text
收口 Phase 0.5。
```

新增：

```text
scripts/verify_z_agent_kernel.sh
docs/agent/AGENT_KERNEL_ACCEPTANCE_MATRIX.md
docs/agent/AGENT_KERNEL_CLOSEOUT_REPORT.md
```

执行：

```bash
python -m compileall zmatrix tests scripts
PYTHONPATH=. python3 -m pytest -q tests/agent/
bash scripts/verify_z_agent_kernel.sh
```

提交：

```bash
git add .
git commit -m "agent-kernel-r6: close z-agent kernel foundation"
```

验收：

```text
Z_AGENT_KERNEL_READY_STUB_ONLY
Production BLOCKED
Broker/runtime BLOCKED
Real trade BLOCKED
Agent direct mutation BLOCKED
```

---

## 10.4 每轮必须输出的报告格式

```text
## Agent Kernel Round X 完成报告

commit:
branch:

### Completed
- files:
- modules:
- tests:

### Safety
- production:
- broker/runtime:
- real trade:
- agent direct mutation:
- raw account data access:

### Verify
- pytest:
- compileall:
- forbidden scan:

### Blockers
- none / list

### Next Round
- allowed:
- forbidden:
```

---

## 10.5 最少轮次裁决

最少可以 6 轮。  
不建议压到 3 轮。

原因：

```text
Agent Kernel 是系统未来安全中枢。
一旦压缩执行，最容易漏：
1. 权限边界
2. Proposal/Approval/Execution 分离
3. Tamper Guard
4. Token Budget
5. Query Contract
```

最优：

```text
6轮工程执行
1轮人工云仓审计
```

即：

```text
OpenClaw执行 6 轮
你让我审计 1 轮
再进入 Z-G16 v1.2 接入
```

---

# 第十一部分：完成后如何与 Z-G16 v1.2 衔接

Agent Kernel 完成后，Z-G16 v1.2 不再直接写模块，而是注册技能：

```text
skill_id: ZG16.LOAD_PHYSICAL_SIGNAL_FIXTURE
risk_level: R1_ANNOTATE

skill_id: ZG16.CALCULATE_NPA_SCORE
risk_level: R1_ANNOTATE

skill_id: ZG16.CREATE_REALITY_CHECK
risk_level: R2_DRAFT

skill_id: ZG16.CREATE_HYPOTHESIS
risk_level: R2_DRAFT

skill_id: CASEFORGE.CREATE_CASE_DRAFT
risk_level: R2_DRAFT
requires_human_review: true
```

这样 Z-G16 就会被 Agent Kernel 管住。

---

# 第十二部分：最终裁决

Z-Agent Kernel 是 Z-MATRIX 进入 Agent 时代的前置地基。

它的目标不是让系统变得更“自动”，而是让系统在自动化前先具备：

```text
权限
门禁
审计
隔离
审批
防篡改
防泄密
最小上下文
技能路由
前端动作队列
```

最终原则：

```text
Agent 少
Skill 多
状态机强
上下文短
证据链硬
审计不可缺
```

完成本阶段后，Z-MATRIX 才有资格进入：

```text
Z-G16 v1.2
AutoCaseForge 自动化
Research Cockpit
前端交互控制
月度自动内化
```

否则，不是智能化，而是系统失控。
