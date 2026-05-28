from zmatrix.governance_closeout.parameter_change_governance import build_parameter_change_governance

def test_no_param_change():
    r = build_parameter_change_governance(yaml_audit={"sensitive_changed_files":[]})
    assert r["governance_status"] == "NO_PARAMETER_CHANGE"
    assert r["human_approval_required"] is False

def test_param_change_detected():
    r = build_parameter_change_governance(yaml_audit={"sensitive_changed_files":["params/threshold.yaml"]})
    assert r["parameter_change_detected"] is True
    assert r["human_approval_required"] is True
