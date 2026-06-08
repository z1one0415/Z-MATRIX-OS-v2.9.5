import pytest
from skillos.capability_invocation_os.adapters.wave0.evidence import plan_controlled_readonly_evidence
def test_hash_only():
    e = plan_controlled_readonly_evidence({"action":"DENY"})
    assert "hash" in e; assert e["type"] == "controlled_readonly"
def test_no_file():
    import os; pre = set(os.listdir("."))
    plan_controlled_readonly_evidence({"test":"data"})
    assert pre == set(os.listdir("."))
