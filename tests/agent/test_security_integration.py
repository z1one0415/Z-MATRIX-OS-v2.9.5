"""Security integration tests — cross-module safety chain verification"""

def test_proposal_payload_with_secret_blocked_by_sanitizer():
    from zmatrix.agent.security.outbound_payload_sanitizer import contains_secret
    payload = {"OPENAI_API_KEY": "sk-abc123", "data": "clean"}
    assert contains_secret(payload) is True

def test_bearer_token_detected():
    from zmatrix.agent.security.outbound_payload_sanitizer import contains_secret
    payload = {"Authorization": "Bearer xyz"}
    assert contains_secret(payload) is True

def test_proposal_target_workspace_escape_blocked():
    from zmatrix.agent.workspace_guard import validate_write_target
    result = validate_write_target("agent-1", "/etc/passwd")
    assert result["allowed"] is False

def test_account_raw_outbound_blocked():
    from zmatrix.agent.security.outbound_payload_sanitizer import block_if_account_raw
    result = block_if_account_raw({"path": "data/research_db/account/raw/trades.csv"})
    assert result["blocked"] is True

def test_tamper_guard_detects_production_flag():
    from zmatrix.agent.tamper_guard import scan_for_forbidden_flags
    content = "production_allowed = True"
    findings = scan_for_forbidden_flags(content)
    assert len(findings) >= 1

def test_clean_draft_proposal_can_enter_proposal_stage():
    from zmatrix.agent.proposal_ledger import create_proposal, submit_proposal
    p = create_proposal(
        "agent-1", "cmd-1",
        target_files=["runtime/agent_workspace/agent-1/draft.md"],
        target_layers=["drafts"],
        proposed_changes={"content": "safe draft"},
        risk_level="R2_DRAFT",
    )
    assert p["status"] == "DRAFT"
    p2 = submit_proposal(p["proposal_id"])
    assert p2["status"] in ("SUBMITTED", "DRAFT")

def test_unapproved_proposal_cannot_execute():
    from zmatrix.agent.execution_runner import execute_approved_proposal
    try:
        result = execute_approved_proposal("nonexistent-id", dry_run=True)
        assert result["status"] != "EXECUTED"
    except (KeyError, ValueError):
        pass  # raised by get_proposal — valid behavior for nonexistent proposal
