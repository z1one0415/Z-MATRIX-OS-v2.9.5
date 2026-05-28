from zmatrix.governance_closeout.no_yaml_mutation_auditor import audit_no_yaml_mutation

def test_no_yaml_mutation():
    r = audit_no_yaml_mutation(base_ref="HEAD~1", head_ref="HEAD")
    assert "audit_status" in r
    assert r["production_yaml_write_allowed"] is False
