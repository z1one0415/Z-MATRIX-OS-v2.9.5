# OpenClaw + opencode｜Z-Agent Kernel 6轮工程执行 + 1轮云仓人工审计计划书

> **配套主文档**：《Z-Agent Kernel & Skill Invocation Protocol｜完整设计蓝图和升级工程执行指令.md》  
> **执行对象**：OpenClaw 天师 + opencode  
> **目标阶段**：ResearchDB Phase 0.5｜Z-Agent Kernel & Skill Invocation Protocol  
> **执行方式**：6轮工程实现 + 1轮云仓人工审计  
> **执行原则**：少 Agent，多 Skill；强权限，强审计；所有 Agent 只能受控调用 Skill，不得直接篡改系统。  
> **硬边界**：Research Only / Paper Only / No Broker / No Runtime / No Real Trade / No Production / No Direct Agent Mutation  

---

## 0. 总执行裁决

本任务不是开发一个“多 Agent 群聊系统”。

本任务是为 Z-MATRIX-OS 建立：

```text
Agent 入住层
Agent 权限层
Skill 调用层
Proposal / Approval / Execution 三段式
防篡改层
防泄密层
前端动作队列
审计闭环
```

执行过程中必须始终坚持：

```text
Agent 是受控工人，不是系统主人。
Skill 是结构化工具，不是自由人格。
ResearchDB 是真相源，不是 LLM 记忆。
所有写入必须 proposal → approval → execution → verify → audit。
```

---

## 1. 全局禁止项

整个 6 轮执行期间，禁止：

```text
1. 不接 broker
2. 不启 runtime
3. 不生成真实交易建议
4. 不生成 BUY / SELL / AUTO_EXECUTE
5. 不允许 Agent 直接修改 ResearchDB
6. 不允许 Agent 直接修改代码主链
7. 不允许 Agent 直接改 production / runtime / broker flags
8. 不允许 Agent 读取 data/research_db/account/raw/
9. 不允许提交真实券商数据
10. 不允许提交 API key / token / cookie
11. 不允许 allowed_scopes=["*"]
12. 不允许 production_allowed=True
13. 不允许 requires_human_review=false 用于 R3+ 风险动作
14. 不允许跳过 verify
15. 不允许自动进入 Z-G16 v1.2
```

---

## 2. 分工原则

### 2.1 OpenClaw 天师职责

OpenClaw 作为总控工程 Agent，负责：

```text
1. 阅读主文档与本计划书
2. 拆分本轮任务
3. 调用 opencode 完成局部实现
4. 运行测试
5. 运行 verify
6. 提交 git commit
7. 推送云仓
8. 输出本轮完成报告
```

OpenClaw 不得：

```text
1. 自行扩展未授权功能
2. 自行进入下一轮
3. 自行修改阶段边界
4. 自行接入真实外部 Agent 框架
5. 自行接 broker/runtime/production
```

### 2.2 opencode 职责

opencode 只做局部代码执行器，负责：

```text
1. 按 OpenClaw 指定文件修改代码
2. 修复测试失败
3. 做局部重构
4. 补 fixture
5. 补 schema
6. 补安全扫描
```

opencode 不得：

```text
1. 自行改变模块边界
2. 自行新增外部依赖
3. 自行接入 Agent 框架
4. 自行创建 runtime daemon
5. 自行跳过测试
```

---

## 3. 分支与提交规则

建议新建独立分支：

```bash
git checkout -b researchdb-phase-0-5-agent-kernel
```

每轮一个 commit group。

提交命名：

```text
agent-kernel-r1: add scope lock docs and directory skeleton
agent-kernel-r2: implement registry permission and command envelope
agent-kernel-r3: implement skill invocation and query contract
agent-kernel-r4: implement proposal approval execution audit pipeline
agent-kernel-r5: add workspace tamper security and action queue
agent-kernel-r6: close z-agent kernel foundation
```

禁止：

```text
1. 一个大 commit 完成全部
2. 混入无关 Phase
3. 混入 Z-G16 真实实现
4. 混入真实账户数据
5. 修改 RC1 tag
```

---

# Round 1：Scope Lock + Docs + Directory Skeleton

## 目标

建立 Agent Kernel 的文档、目录、账本骨架，不实现复杂逻辑。

## 必须创建文档

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
```

## 必须创建目录

```text
zmatrix/agent/
zmatrix/agent/security/
data/research_db/agent/
data/research_db/agent/registry/
data/research_db/agent/ledgers/
data/research_db/agent/workspace/
data/research_db/agent/reports/
tests/agent/
```

## 必须创建占位文件

```text
zmatrix/agent/__init__.py
zmatrix/agent/security/__init__.py
data/research_db/agent/README.md
data/research_db/agent/workspace/.gitkeep
```

## 不得实现

```text
不得实现真实执行器
不得实现外部 Agent 接入
不得接 LangGraph / AutoGen / CrewAI / Hermes runtime
```

## 本轮测试

```bash
python -m compileall zmatrix tests scripts
git status --short
```

## 本轮安全扫描

```bash
grep -R "real_trade_allowed=True\|broker_order_allowed=True\|runtime_enabled=True\|auto_buy_allowed=True\|auto_sell_allowed=True\|production_allowed=True" docs/agent zmatrix/agent data/research_db/agent tests/agent || true
```

必须无危险业务输出。

## 提交

```bash
git add .
git commit -m "agent-kernel-r1: add scope lock docs and directory skeleton"
```

## Round 1 完成报告

```text
## Agent Kernel Round 1 完成报告

commit:
branch:

### Completed
- docs/agent:
- zmatrix/agent skeleton:
- data/research_db/agent skeleton:
- tests/agent skeleton:

### Safety
- production flags:
- broker/runtime:
- real trade:
- agent direct mutation:

### Verify
- compileall:
- forbidden scan:

### Final
ROUND1_PASS / ROUND1_BLOCKED
```

---

# Round 2：Agent Registry + Command Envelope + Permission Gate

## 目标

让系统能够识别 Agent、校验权限、封装命令、拒绝越权行为。

## 必须实现

```text
zmatrix/agent/agent_registry.py
zmatrix/agent/agent_identity.py
zmatrix/agent/agent_permission.py
zmatrix/agent/command_envelope.py
```

## 必须创建 registry fixture

```text
data/research_db/agent/registry/agent_registry.json
```

第一批默认 Agent：

```json
[
  {
    "agent_id": "z-orchestrator",
    "agent_name": "Z-Orchestrator",
    "agent_type": "ORCHESTRATOR",
    "permission_level": "VIEW_ONLY",
    "allowed_scopes": ["research_summary", "layer_query", "skill_draft"],
    "allowed_read_layers": ["*READ_ONLY_REGISTRY"],
    "allowed_write_layers": [],
    "allowed_commands": ["QUERY", "CREATE_DRAFT_COMMAND"],
    "forbidden_commands": ["REAL_TRADE", "BROKER_ORDER", "AUTO_BUY", "AUTO_SELL", "PRODUCTION_MUTATION"],
    "max_risk_level": "R2_DRAFT",
    "requires_human_review": true,
    "workspace_path": "runtime/agent_workspace/z-orchestrator",
    "enabled": true,
    "production_allowed": false
  },
  {
    "agent_id": "openclaw-engineering",
    "agent_name": "OpenClaw Engineering Agent",
    "agent_type": "ENGINEERING",
    "permission_level": "CODE_PATCH_PROPOSER",
    "allowed_scopes": ["code_patch_proposal", "verify_runner"],
    "allowed_read_layers": ["docs", "zmatrix", "tests", "scripts"],
    "allowed_write_layers": ["runtime/agent_workspace/openclaw-engineering"],
    "allowed_commands": ["CREATE_PATCH_PROPOSAL", "RUN_VERIFY_DRY"],
    "forbidden_commands": ["REAL_TRADE", "BROKER_ORDER", "AUTO_BUY", "AUTO_SELL", "DIRECT_MAIN_PUSH", "PRODUCTION_MUTATION"],
    "max_risk_level": "R4_CODE_PATCH_PROPOSAL",
    "requires_human_review": true,
    "workspace_path": "runtime/agent_workspace/openclaw-engineering",
    "enabled": true,
    "production_allowed": false
  }
]
```

注意：

```text
allowed_read_layers 中出现 *READ_ONLY_REGISTRY 是占位字符串，不是 wildcard 权限。
禁止 allowed_scopes=["*"]。
```

## 必须测试

```text
tests/agent/test_agent_registry.py
tests/agent/test_agent_permission.py
tests/agent/test_command_envelope.py
```

测试断言：

```text
1. unknown agent → REJECT
2. disabled agent → REJECT
3. production_allowed=true → ERROR
4. allowed_scopes=["*"] → ERROR
5. VIEW_ONLY agent 调 R3 → REJECT
6. R3 requires human review
7. R9 always blocked
8. command digest 稳定
9. command_id 必填
10. requested_skill 必填
```

## 本轮命令

```bash
python -m compileall zmatrix tests scripts
PYTHONPATH=. python3 -m pytest -q tests/agent/test_agent_registry.py tests/agent/test_agent_permission.py tests/agent/test_command_envelope.py
```

## 提交

```bash
git add .
git commit -m "agent-kernel-r2: implement registry permission and command envelope"
```

---

# Round 3：Skill Registry + Skill Invocation + Expert Domain + Query Contract + Token Budget

## 目标

让 Agent 不能直接调用代码，只能通过 Skill Registry 调用已注册技能，并强制最小上下文查询。

## 必须实现

```text
zmatrix/agent/skill_registry.py
zmatrix/agent/skill_invocation.py
zmatrix/agent/expert_domain_contract.py
zmatrix/agent/query_contract.py
zmatrix/agent/token_budget.py
```

## 必须创建 registry fixture

```text
data/research_db/agent/registry/skill_registry.json
data/research_db/agent/registry/expert_domain_registry.json
```

第一批 Skill：

```text
SYSTEM.GET_RESEARCH_SUMMARY
SYSTEM.GET_LAYER_VERSIONS
SYSTEM.GET_LAYER_SLICE
CASEFORGE.CREATE_CASE_DRAFT
REPORT.RENDER_DRAFT
VERIFY.RUN_DRY
```

第一批 Reviewer Skill：

```text
REVIEWER.DATA_QUALITY
REVIEWER.RISK_CONTROL
REVIEWER.CATALYST_TIMING
REVIEWER.EXECUTION_QUALITY
```

## 必须实现的 Query Contract

```text
get_research_summary()
get_layer_versions()
get_changed_layers()
get_layer_slice()
query_case()
query_event_window()
query_factor()
query_hypotheses()
```

## Token Budget 硬规则

```text
默认 limit <= 100
默认不允许全仓扫描
返回 token_estimate
超过预算返回 NEED_NARROWER_QUERY
```

## 必须测试

```text
tests/agent/test_skill_registry.py
tests/agent/test_skill_invocation.py
tests/agent/test_expert_domain_contract.py
tests/agent/test_query_contract.py
tests/agent/test_token_budget.py
```

测试断言：

```text
1. unknown skill → REJECT
2. disabled skill → REJECT
3. write skill without verify_script → ERROR
4. production_allowed=true → ERROR
5. Reviewer Skill 不得输出 BUY/SELL
6. get_layer_slice respects limit
7. full scan rejected
8. over token budget → NEED_NARROWER_QUERY
```

## 本轮命令

```bash
python -m compileall zmatrix tests scripts
PYTHONPATH=. python3 -m pytest -q tests/agent/test_skill_registry.py tests/agent/test_skill_invocation.py tests/agent/test_expert_domain_contract.py tests/agent/test_query_contract.py tests/agent/test_token_budget.py
```

## 提交

```bash
git add .
git commit -m "agent-kernel-r3: implement skill invocation and query contract"
```

---

# Round 4：Proposal / Approval / Execution / Verify / Audit Pipeline

## 目标

完成 Agent 写入三段式闭环。

```text
Proposal
→ Approval
→ Execution
→ Verify
→ Audit
```

## 必须实现

```text
zmatrix/agent/proposal_ledger.py
zmatrix/agent/approval_gate.py
zmatrix/agent/execution_runner.py
zmatrix/agent/verify_gate.py
zmatrix/agent/audit_ledger.py
```

## 必须创建账本

```text
data/research_db/agent/ledgers/command_ledger.jsonl
data/research_db/agent/ledgers/proposal_ledger.jsonl
data/research_db/agent/ledgers/approval_ledger.jsonl
data/research_db/agent/ledgers/execution_ledger.jsonl
data/research_db/agent/ledgers/audit_ledger.jsonl
```

## 硬规则

```text
1. proposal append-only
2. approval 前不得 execution
3. R3+ 必须 approval
4. R4/R5 必须人工 approval
5. R9 禁止 approval
6. execution 默认 dry_run=True
7. dry_run 失败不得 real run
8. 执行后必须 verify
9. verify 失败 status=VERIFY_FAILED
10. audit append-only
```

## 必须测试

```text
tests/agent/test_proposal_ledger.py
tests/agent/test_approval_gate.py
tests/agent/test_execution_runner.py
tests/agent/test_verify_gate.py
tests/agent/test_audit_ledger.py
```

测试断言：

```text
1. unapproved proposal cannot execute
2. approved proposal dry_run works
3. R4 requires human approval
4. R9 cannot approve
5. verify failure blocks closeout
6. audit ledger append-only
```

## 本轮命令

```bash
python -m compileall zmatrix tests scripts
PYTHONPATH=. python3 -m pytest -q tests/agent/test_proposal_ledger.py tests/agent/test_approval_gate.py tests/agent/test_execution_runner.py tests/agent/test_verify_gate.py tests/agent/test_audit_ledger.py
```

## 提交

```bash
git add .
git commit -m "agent-kernel-r4: implement proposal approval execution audit pipeline"
```

---

# Round 5：Workspace Guard + Tamper Guard + Payload Sanitizer + HMAC + Action Queue

## 目标

补齐 Agent 防篡改、防泄漏、工作区隔离、前端动作队列。

## 必须实现

```text
zmatrix/agent/workspace_guard.py
zmatrix/agent/tamper_guard.py
zmatrix/agent/action_queue.py
zmatrix/agent/security/outbound_payload_sanitizer.py
zmatrix/agent/security/secret_pattern_blocker.py
zmatrix/agent/security/command_hmac.py
zmatrix/agent/security/payload_digest.py
```

## Workspace Guard 硬规则

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

除非走：

```text
proposal → approval → execution
```

## Tamper Guard 必须扫描

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
api_key
token
secret
```

## Payload Sanitizer 必须拦截

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

## Action Queue 类型

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

Action Queue 只能控制前端展示，不得改变 ResearchDB。

## 必须测试

```text
tests/agent/test_workspace_guard.py
tests/agent/test_tamper_guard.py
tests/agent/test_outbound_payload_sanitizer.py
tests/agent/test_action_queue.py
tests/agent/test_no_direct_agent_mutation.py
```

测试断言：

```text
1. workspace escape rejected
2. secret redacted
3. forbidden production flags blocked
4. self-elevation blocked
5. action queue cannot mutate ResearchDB
6. destructive pop works
```

## 本轮命令

```bash
python -m compileall zmatrix tests scripts
PYTHONPATH=. python3 -m pytest -q tests/agent/test_workspace_guard.py tests/agent/test_tamper_guard.py tests/agent/test_outbound_payload_sanitizer.py tests/agent/test_action_queue.py tests/agent/test_no_direct_agent_mutation.py
```

## 提交

```bash
git add .
git commit -m "agent-kernel-r5: add workspace tamper security and action queue"
```

---

# Round 6：Verify Script + Acceptance + Closeout

## 目标

完成 Phase 0.5 收口，不进入下一阶段。

## 必须新增

```text
scripts/verify_z_agent_kernel.sh
docs/agent/AGENT_KERNEL_ACCEPTANCE_MATRIX.md
docs/agent/AGENT_KERNEL_CLOSEOUT_REPORT.md
data/research_db/agent/reports/agent_activity_report.md
data/research_db/agent/reports/agent_security_report.md
data/research_db/agent/reports/agent_permission_report.md
```

## verify_z_agent_kernel.sh 必须执行

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

## 必须运行

```bash
python -m compileall zmatrix tests scripts
PYTHONPATH=. python3 -m pytest -q tests/agent/
bash scripts/verify_z_agent_kernel.sh
```

## 提交

```bash
git add .
git commit -m "agent-kernel-r6: close z-agent kernel foundation"
git push
```

## Round 6 完成报告

```text
## Agent Kernel Round 6 完成报告

commit:
branch:

### Closeout
- verify_z_agent_kernel.sh:
- AGENT_KERNEL_ACCEPTANCE_MATRIX:
- AGENT_KERNEL_CLOSEOUT_REPORT:

### Tests
- tests/agent:
- compileall:
- forbidden scan:

### Safety
- Production:
- Broker/runtime:
- Real trade:
- Agent direct mutation:
- Raw account data access:
- Secret leakage:

### Final Decision
Z_AGENT_KERNEL_READY_STUB_ONLY / BLOCKED
```

---

# 第 7 轮：云仓人工审计计划

## 审计对象

审计分支：

```text
researchdb-phase-0-5-agent-kernel
```

审计重点：

```text
1. 6 个 commit 是否真实在云仓
2. 是否存在无关功能混入
3. docs/agent 是否完整
4. zmatrix/agent 是否完整
5. tests/agent 是否完整
6. verify_z_agent_kernel.sh 是否真实执行 pytest
7. 是否存在假阳性测试
8. 是否存在 forbidden flags
9. 是否存在 allowed_scopes=["*"]
10. 是否存在生产/交易/运行时绕过
11. 是否存在真实券商数据
12. 是否存在密钥泄漏
13. 是否自动进入 Z-G16 v1.2
```

## 云仓人工审计命令

```bash
git fetch origin

git checkout researchdb-phase-0-5-agent-kernel

git log --oneline --decorate -10

python -m compileall zmatrix tests scripts

PYTHONPATH=. python3 -m pytest -q tests/agent/

bash scripts/verify_z_agent_kernel.sh

grep -R "real_trade_allowed=True\|broker_order_allowed=True\|runtime_enabled=True\|auto_buy_allowed=True\|auto_sell_allowed=True\|production_allowed=True\|production_strategy_modified=True" zmatrix/agent docs/agent scripts || true

grep -R "allowed_scopes=.*\*" zmatrix/agent docs/agent data/research_db/agent || true

git ls-files | grep "data/research_db/account/raw" || true

git status --short
```

## 人工审计通过标准

必须全部满足：

```text
1. 6轮 commit 均可见
2. tests/agent 全部通过
3. verify_z_agent_kernel.sh 通过
4. 无 forbidden production flags
5. 无 allowed_scopes=["*"]
6. 无真实 raw account 文件
7. 无 API key / token 泄漏
8. 无 broker/runtime/real trade
9. AGENT_KERNEL_CLOSEOUT_REPORT 标记 PASS
10. Final Status = Z_AGENT_KERNEL_READY_STUB_ONLY
```

## 审计结果格式

```text
## Z-Agent Kernel 云仓人工审计报告

branch:
latest_commit:

### Commit Chain
- R1:
- R2:
- R3:
- R4:
- R5:
- R6:

### Verify
- compileall:
- tests/agent:
- verify_z_agent_kernel:
- forbidden scan:

### Safety
- production flags:
- broker/runtime:
- real trade:
- allowed_scopes wildcard:
- raw account data:
- secrets:

### Scope
- Agent Kernel only:
- Z-G16 not started:
- Phase 1 not affected:
- RC1 not modified:

### Decision
APPROVED_FOR_ZG16_V12_INTEGRATION / BLOCKED
```

---

# 最终执行口径

天师现在只能执行：

```text
ResearchDB Phase 0.5：
Z-Agent Kernel & Skill Invocation Protocol
```

不得执行：

```text
Z-G16 v1.2
AutoCaseForge 自动化
Research Cockpit
任何真实 Agent runtime
任何真实 broker/runtime/production
```

完成并通过云仓审计后，下一步才允许：

```text
Z-G16 v1.2 接入 Agent Kernel
```

一句话：

```text
先建门禁和工牌系统，再让 Agent 入厂。
```
