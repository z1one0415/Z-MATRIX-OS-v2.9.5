# Z-MATRIX-OS V4-PRO Product Acceptance Standard

Status: Productization target contract
Scope: personal investment research workstation
Safety posture: research only, no alpha claim, no promotion, no broker, no real trade

## 1. Product Target

Z-MATRIX-OS V4-PRO must move from a research asset repository into an installable, runnable, cockpit-driven personal investment research product.

The finished product must let a normal local user:

- install the system from a packaged release;
- configure local data sources and API keys without committing secrets;
- start the backend research service;
- open the cockpit UI and use the research workflow from the browser;
- interact with built-in agents through natural language;
- inspect system status, factor status, evidence chains, research tasks, safety gates, and report outputs;
- run local smoke checks and monthly research refresh jobs;
- export research reports;
- clearly see that the product cannot connect to brokers, cannot perform real trade, cannot promote alpha, and cannot bypass human review.

## 2. Non-Negotiable Safety Boundary

Every product package and runtime must preserve these hard gates:

- no-alpha-claim;
- no-promotion;
- no-execution;
- no-broker;
- no-real-trade;
- human review required before any higher-risk interpretation;
- all broker/runtime trade surfaces blocked by default;
- secrets stay outside git history and packaged artifacts.

These gates are product features, not temporary limitations. A release is blocked if users can confuse the system with a trading terminal.

## 3. Installable Product Standard

A product-grade release must include:

- one documented install path for macOS local use;
- backend Python dependency installation;
- frontend cockpit dependency installation or prebuilt assets;
- `.env.example` files for all configurable services;
- local data directory bootstrap;
- packaged default sample packets for offline demo mode;
- a single smoke command that verifies backend, cockpit packets, tests, and safety gates;
- clear failure messages when keys, data, or optional services are missing.

Minimum user journey:

```text
install -> configure -> start backend -> open cockpit -> run smoke -> inspect research evidence -> export report
```

## 4. Backend Runtime Standard

The backend must expose product-level capabilities, not only scripts:

- service health and version status;
- data source readiness and data quality audit;
- factor registry and factor evidence status;
- historical OOS result index;
- Forward OOS waiting queue and monthly refresh status;
- factor survival and decay state;
- candidate alpha research evidence, with no promotion claim;
- portfolio research sandbox results;
- risk, cost, liquidity, and industry neutralization analysis;
- report generation and export;
- gatekeeper audit results;
- agent invocation status and audit trail.

The backend may be implemented as CLI plus local API at first, but the cockpit must consume stable packets or endpoints rather than ad hoc files.

## 5. Cockpit Standard

The cockpit is the primary user surface. It must be able to show:

- system status;
- data freshness;
- factor library status;
- historical OOS results;
- Forward OOS queue and monthly refresh state;
- alpha candidate evidence chain;
- factor survival and decay;
- portfolio research sandbox;
- risk, cost, liquidity, and neutralization panels;
- report export center;
- gatekeeper audit panel;
- agent chat/control panel;
- explicit safety state: broker blocked, real trade blocked, alpha promotion blocked.

The cockpit must support offline demo packets and live local backend packets. Visual polish matters, but data truth and safety clarity are release blockers.

## 6. Agent Interaction Standard

Built-in agents must be exposed as controlled research assistants:

- natural-language query over system state and research evidence;
- scoped tool invocation through registered skills only;
- read-only or draft-only default behavior;
- full audit log for user-visible actions;
- no direct broker path;
- no hidden external writes;
- no silent upgrade of research evidence into alpha claim;
- clear refusal when the user asks for unsupported trading operations.

Hermes/Z2 can remain the primary resident research agent. Additional agents are admitted only after registry, safety gate, invocation tests, and audit retention pass.

## 7. Research Pipeline Standard

The product must support:

- local market data ingestion and manifesting;
- data quality audit and coverage score;
- factor materialization;
- historical OOS validation;
- Forward OOS registry;
- monthly research refresh;
- factor decay and survival analysis;
- risk/cost/liquidity/neutralization analysis;
- report generation;
- reproducible evidence packs.

Every research result must carry:

- input data manifest;
- method version;
- as-of date;
- test horizon;
- evidence status;
- safety status;
- limitations.

## 8. Packaging Standard

A release package must contain:

- source archive;
- backend service entrypoint;
- frontend cockpit build or install instructions;
- sample cockpit packets;
- product README;
- install guide;
- run guide;
- smoke test guide;
- safety boundary statement;
- verification evidence;
- artifact checksums.

The package must exclude:

- API keys;
- raw private account records unless explicitly packaged by the user outside git;
- large raw market vendor dumps;
- runtime scratch reports not intended for release;
- cache files.

## 9. Product Smoke Gate

The final smoke gate must verify:

- Python modules compile;
- backend health command returns OK;
- cockpit packet export succeeds;
- cockpit frontend tests pass;
- cockpit build succeeds;
- factor registry validates;
- historical OOS index is readable;
- Forward OOS queue is readable;
- monthly refresh command can run in dry mode;
- report export can produce a sample artifact;
- all safety gates remain blocked for broker and real trade;
- no secrets appear in tracked files or release package.

## 10. Release Readiness Levels

### R0 Research Asset

Scripts, tests, docs, and evidence exist, but ordinary users cannot install and use the product through a coherent flow.

### R1 Local Workstation Preview

One local install path exists. Cockpit can open. Backend packets are exportable. Smoke checks pass. Research outputs remain partly script-driven.

### R2 Product RC

Backend service, cockpit, local config, smoke gate, data manifests, report export, and agent interaction are integrated. A user can complete the core journey without reading internal engineering docs.

### R3 Personal Product Release

Packaged release is reproducible, documented, checksummed, and runnable from a clean checkout or release archive. The cockpit is the default surface. Research pipelines and safety gates are visible and repeatable.

## 11. Current Direction Of Work

Immediate engineering convergence should proceed in this order:

1. Product install/run skeleton: bootstrap, environment examples, backend service entrypoint, cockpit start path.
2. Data foundation: local vendor ingestion, manifest, data quality audit, no secret leakage.
3. Research service packets: factors, OOS, Forward OOS, decay, risk, sandbox, reports, gates.
4. Cockpit full connection: replace static/demo-only panels with backend packets while preserving demo mode.
5. Agent bridge: natural-language control over read-only and draft-only registered research skills.
6. Product smoke gate: one command verifies installability, runtime readiness, cockpit build, and safety.
7. Release package: source, cockpit build, sample packets, docs, checksums, evidence.

## 12. Final Verdict Standard

A build may be called Z-MATRIX-OS V4-PRO Product RC only if:

- a new user can install it locally;
- backend research service can start;
- cockpit can be opened and used as the main surface;
- data and research status are visible;
- agent interaction is available through controlled skills;
- smoke gate passes from a clean workspace;
- package contains no secrets or raw private data;
- all no-alpha-claim/no-promotion/no-execution/no-broker/no-real-trade gates are visibly enforced.

If any item above fails, the system remains a research asset package, not a product release.
