"""V13.F5.0.1.1 — Test README scope and typo fixes."""
import re

def test_no_monitore_typo():
    with open("research/factor_library/interface/v1/README.md") as f:
        content = f.read()
    # Check for standalone 'monitore' (not part of 'monitored')
    import re
    standalone = re.search(r'\bmonitore\b', content)
    assert standalone is None, "Typo 'monitore' found in README"

def test_monitored_present():
    with open("research/factor_library/interface/v1/README.md") as f:
        content = f.read()
    assert "monitored" in content

def test_batch3_explicit_pre_interface():
    with open("research/factor_library/interface/v1/README.md") as f:
        content = f.read()
    assert "V13.F5.1.2" in content
    assert "pre-interface" in content

def test_batch1_not_current_blocker():
    """README should not claim Batch1/Batch2 are current blockers for F5.1.2."""
    with open("research/factor_library/interface/v1/README.md") as f:
        content = f.read()
    # The old string "All Batch1/Batch2/Batch3 artifacts are pre-interface until backfilled" should be gone
    assert "All Batch1/Batch2/Batch3" not in content

def test_scope_mentions_backfill():
    with open("research/factor_library/interface/v1/README.md") as f:
        content = f.read()
    assert "backfill" in content

def test_no_alpha_claim_allowed_true():
    """Verify no schema allows alpha_claim_allowed=true."""
    import glob, json
    for fpath in glob.glob("research/factor_library/interface/v1/schemas/*.json"):
        schema = json.loads(open(fpath).read())
        props = schema.get("properties", {})
        if "alpha_claim_allowed" in props:
            ac = props["alpha_claim_allowed"]
            assert ac.get("const") is False or ac.get("enum") == [False] or (ac.get("type") == "boolean" and ac.get("const") is False), f"{fpath}: alpha_claim_allowed not pinned to false"
