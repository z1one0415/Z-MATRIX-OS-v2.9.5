import pytest
from skillos.capability_invocation_os.adapters.wave0.evidence import plan_controlled_readonly_evidence

def test_evidence_hash_only():
    evidence = plan_controlled_readonly_evidence({"action": "DENY"})
    assert "hash" in evidence
    assert evidence["type"] == "controlled_readonly"
    assert "action" not in evidence

def test_evidence_no_file():
    import os
    pre = set(os.listdir("."))
    plan_controlled_readonly_evidence({"test": "data"})
    post = set(os.listdir("."))
    assert pre == post
