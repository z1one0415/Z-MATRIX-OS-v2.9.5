# allowlist: forbidden-token-definition
"""Integration schemas — readiness status, layers, required pipelines/gates"""
from __future__ import annotations

READINESS_STATUS = frozenset({"READY_FOR_ALPHA", "PREVIEW_ONLY", "BLOCKED", "NEEDS_REVIEW"})

INTEGRATION_LAYER = frozenset({
    "WORKSPACE", "EVENT_STORE", "HERMES_MEMORY", "APPROVAL_LOOP",
    "PROMPT_MIDDLEWARE", "TAIL_RISK", "SYSTEM_CONTROLLER",
})

ALPHA_REQUIRED_PIPELINES = frozenset({
    "Z-EventStore", "Z-HermesMemoryKernel", "Z-ApprovalReflectionLoop",
    "Z-PromptMiddlewarePreview", "Z-TailRiskAutonomicGates",
})

ALPHA_REQUIRED_WORKFLOWS = frozenset({
    "Z-EventStore.unified_event_ledger_workflow",
    "Z-Hermes.memory_kernel_preview_workflow",
    "Z-Approval.reflection_loop_workflow",
    "Z-Prompt.middleware_preview_workflow",
    "Z-TailRisk.autonomic_gates_preview_workflow",
})

ALPHA_FORBIDDEN_CAPABILITIES = frozenset({
    "real_trade", "broker_order", "auto_buy", "auto_sell", "auto_cancel",
    "auto_position_close", "real_z9_write", "hermes_memory_write",
    "auto_calibration", "prompt_auto_injection", "system_prompt_write",
    "runtime_prompt_injection", "real_market_fetch", "external_api_default_on",
})

ALPHA_REQUIRED_GATES = frozenset({
    "safety.no_real_trade", "event.schema.valid", "event.safety.valid",
    "event.lineage.valid", "event.append_only.valid",
    "hermes.read_only.valid", "hermes.preview_only.valid",
    "hermes.no_memory_write.valid", "hermes.no_auto_calibration.valid",
    "hermes.no_prompt_auto_injection.valid",
    "approval.request.valid", "approval.decision.valid",
    "approval.no_auto_effect.valid", "approval.human_required.valid",
    "prompt.preview_only.valid", "prompt.no_runtime_injection.valid",
    "prompt.no_system_prompt_write.valid", "prompt.no_auto_injection.valid",
    "prompt.audit.valid",
    "tail_risk.signal.valid", "tail_risk.preview_only.valid",
    "tail_risk.no_broker_order.valid", "tail_risk.no_real_trade.valid",
    "tail_risk.action_degradation.valid", "tail_risk.no_auto_sell.valid",
})

DEFAULT_INTEGRATION_SAFETY = {
    "real_trade_allowed": False, "broker_order_allowed": False,
    "auto_buy_allowed": False, "auto_sell_allowed": False,
    "auto_position_close_allowed": False, "real_z9_write_allowed": False,
    "hermes_memory_write_allowed": False, "auto_calibration_allowed": False,
    "prompt_auto_injection_allowed": False, "system_prompt_write_allowed": False,
    "runtime_injection_allowed": False, "external_api_default_on": False,
    "alpha_runtime_allowed": False, "readiness_check_only": True,
}
