# Z-Agent Kernel Blueprint

## Status
- Phase: ResearchDB Phase 0.5
- Mode: STUB_ONLY
- Production: BLOCKED
- Broker/runtime: BLOCKED
- Real trade: BLOCKED

## Architecture
```
User/Frontend → Z-Agent Gateway → Agent Registry → Permission Gate
→ Command Envelope → Skill Invocation → Proposal Ledger
→ Approval Gate → Execution Runner → Verify Gate → Audit Ledger
```

## Core Principle
Agent 是受控工人，不是系统主人。少 Agent，多 Skill。

## Agent Limits
- 常驻: 1 (Z-Orchestrator)
- 半常驻: 2 (ReportRenderer, ResearchAssistant)
- 按需: openclaw-engineering
- 专家域 → Reviewer Skill (not Agent)
