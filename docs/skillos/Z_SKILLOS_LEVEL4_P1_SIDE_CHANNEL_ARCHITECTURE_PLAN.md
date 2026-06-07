# Z-SkillOS Level 4 P1 Side-Channel Architecture Plan

## Status

Z_SKILLOS_LEVEL4_P1_SIDE_CHANNEL_ARCHITECTURE_PLAN_READY

## Scope

FUTURE_PLAN_ONLY. No implementation. No code. No warning enablement.

## Architecture Components (Future Plan)

### 1. Warning Candidate Lifecycle

| Phase | Description | Status |
|:--|:--|:--:|
| Detection | Level 4 evaluation identifies drift/mismatch/failure | FUTURE_PLAN_ONLY |
| Classification | Assign category and severity from taxonomy | FUTURE_PLAN_ONLY |
| Filtering | Apply false-positive suppression rules | FUTURE_PLAN_ONLY |
| Routing | Route to side-channel (NOT caller, NOT envelope) | FUTURE_PLAN_ONLY |
| Delivery | Write to audit sink / operator report | FUTURE_PLAN_ONLY |

### 2. Operator-Review-Only Path

| Rule | Description |
|:--|:--|
| Output target | Operator dashboard or file, NOT caller response |
| No caller visibility | Warning data never appears in skill output |
| No envelope mutation | result_envelope unchanged |
| No stdout/stderr | No uncontrolled output |
| Human-triggered escalation | ESCALATE_REVIEW severity = human-reviewed |

### 3. Audit Sink Abstraction

| Sink Type | Description | Status |
|:--|:--|:--:|
| NoopSink | Default; no-op; zero side-effects | P0: EXISTING |
| AuditFileSink | JSONL file writer | FUTURE_PLAN_ONLY |
| OperatorReportSink | Markdown report | FUTURE_PLAN_ONLY |
| BusSink | Internal message bus | FUTURE_PLAN_ONLY |

### 4. No Caller-Visible Path

* No warning in result_envelope.status
* No warning in result_envelope.output
* No warning in result_envelope.metadata
* No warning in stdout/stderr
* No warning in exception messages

### 5. No Envelope Mutation

* result_envelope hash unchanged
* No new fields
* No removed fields
* No value changes

### 6. Enabled Path Still Not Authorized

* P0 enabled path remains placeholder
* P1 does NOT authorize changing the placeholder
* Warning enablement requires separate approval

### 7. No Runtime Integration

* No invoke_skill hook
* No main pipeline call
* No production import

### 8. No invoke_skill Hook

* Level 4 remains isolated
* No runtime observation path
* No caller notification

## All components FUTURE_PLAN_ONLY. No code. No warning enablement. Level 5 remains BLOCKED.
