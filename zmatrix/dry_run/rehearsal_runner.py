"""Rehearsal Runner — build v3.0-alpha dry-run rehearsal by calling real builders"""
from __future__ import annotations
import hashlib
from datetime import datetime, timezone

from zmatrix.dry_run.schemas import DRY_RUN_VERSION, DRY_RUN_STEPS, DEFAULT_DRY_RUN_SAFETY

from zmatrix.event_store.adapters import build_paper_ledger_event, build_outcome_backfill_event
from zmatrix.hermes_memory.memory_candidate_preview import build_memory_candidate_preview
from zmatrix.approval_loop.approval_request import build_approval_request
from zmatrix.approval_loop.approval_decision import build_human_approval_decision
from zmatrix.prompt_middleware.patch_request import build_prompt_patch_request
from zmatrix.prompt_middleware.renderer import render_prompt_patch_preview
from zmatrix.tail_risk.tail_risk_controller import build_tail_risk_controller_preview
from zmatrix.integration.readiness_report import build_v3_alpha_readiness_report


def build_v3_alpha_dry_run_rehearsal() -> dict:
    """Build a full v3.0-alpha dry-run rehearsal.

    Calls real builders from v2.9.10~v2.9.16 modules.
    Does NOT append EventStore.
    Does NOT write Hermes memory.
    Does NOT write Z9.
    Does NOT inject prompts.
    Does NOT enable runtime.
    """
    # Step 1-2: EventStore events (build only, no append)
    paper = build_paper_ledger_event({
        "ticker": "002472", "role": "B_MID_ROTATION",
        "entry_price": 45.0, "paper_action": "PAPER_TRACK",
    })
    outcome = build_outcome_backfill_event({
        "ticker": "002472", "actual_return_t20": 3.2,
        "outcome_status": "READY",
    }, parent_event_id=paper["event_id"])

    # Step 3: MemoryCandidatePreview
    memory_candidate = build_memory_candidate_preview(
        source_event={"event_id": outcome["event_id"], "event_type": "OutcomeBackfillEvent", "payload": {}},
        attribution={"mistake_type": "early_buy", "severity": "MEDIUM", "confidence": "LOW", "evidence_event_ids": []},
        proposed_lesson="wait for confirmation before entry",
    )

    # Step 4: ApprovalRequest
    approval_req = build_approval_request(
        request_type="MEMORY_CANDIDATE_APPROVAL",
        source_preview={"memory_candidate_id": memory_candidate.get("memory_candidate_id", ""), "severity": "MEDIUM"},
        reason="review candidate lesson",
    )

    # Step 5: HumanApprovalDecision
    human_decision = build_human_approval_decision(
        approval_request=approval_req,
        decision="APPROVE",
        human_operator="test_admin",
        rationale="lesson acknowledged",
    )

    # Step 6: PromptPatchRequest
    prompt_req = build_prompt_patch_request(
        task_context={"task_type": "paper_decision", "ticker": "002472"},
        prompt_patch_preview={"patch_id": "p" * 32, "prompt_patch_text": "test discipline"},
        approval_decision=human_decision,
    )

    # Step 7: PromptRenderPreview
    render = render_prompt_patch_preview(prompt_patch_request=prompt_req)

    # Step 8: TailRiskControllerPreview
    tail_risk = build_tail_risk_controller_preview(market_signals={})

    # Step 9: V3AlphaReadinessReport
    readiness = build_v3_alpha_readiness_report()

    artifacts = {
        "paper_ledger_event": paper,
        "outcome_backfill_event": outcome,
        "memory_candidate_preview": memory_candidate,
        "approval_request": approval_req,
        "human_approval_decision": human_decision,
        "prompt_patch_request": prompt_req,
        "prompt_render_preview": render,
        "tail_risk_controller_preview": tail_risk,
        "v3_alpha_readiness_report": readiness,
    }

    lineage = []
    for i, (name, artifact) in enumerate(artifacts.items()):
        eid = artifact.get("event_id") or artifact.get("approval_request_id") or \
              artifact.get("approval_decision_id") or artifact.get("prompt_patch_request_id") or \
              artifact.get("render_id") or artifact.get("controller_id") or \
              artifact.get("memory_candidate_id") or artifact.get("candidate_id") or ""
        parent = artifact.get("parent_event_id") or artifact.get("source_event_id") or (
            list(artifacts.values())[i - 1].get("event_id") if i > 0 else None
        )
        lineage.append({
            "step": DRY_RUN_STEPS[i] if i < len(DRY_RUN_STEPS) else name,
            "artifact_name": name,
            "artifact_id": eid[:16] if len(eid) > 16 else eid,
            "parent_id": parent[:16] if parent and len(str(parent)) > 16 else parent,
        })

    seed = f"dry_run|{datetime.now(timezone.utc).isoformat()}"
    dry_run_id = hashlib.sha256(seed.encode()).hexdigest()[:32]
    created_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    return {
        "dry_run_id": dry_run_id,
        "dry_run_version": DRY_RUN_VERSION,
        "mode": "DRY_RUN_ONLY",
        "created_at": created_at,
        "steps": DRY_RUN_STEPS,
        "lineage": lineage,
        "artifacts": artifacts,
        "safety": dict(DEFAULT_DRY_RUN_SAFETY),
        "real_trade_allowed": False,
        "broker_order_allowed": False,
        "real_z9_write_allowed": False,
        "hermes_memory_write_allowed": False,
        "auto_calibration_allowed": False,
        "prompt_auto_injection_allowed": False,
        "system_prompt_write_allowed": False,
        "runtime_enabled": False,
    }
