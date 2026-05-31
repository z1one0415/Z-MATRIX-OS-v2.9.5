def test_system_status_all_stages_present():
    from zmatrix.research_db.zg16_system_integration_cockpit import build_zg16_system_status
    r = build_zg16_system_status("600519")
    assert r["zg16_stage_status"] == "G16_1_to_8_STUB_INTEGRATION"
    assert r["agent_kernel_status"] == "ZK_READY_FOR_ZG16_STUB_INTEGRATION"
    assert r["production_allowed"] is False
    assert r["trade_allowed"] is False
    assert r["external_api_used"] is False
    assert r["runtime_ledgers_empty"] is True
    assert len(r["available_agent_skills"]) >= 13
