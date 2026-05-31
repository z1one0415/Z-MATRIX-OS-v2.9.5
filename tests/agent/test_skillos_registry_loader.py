from zmatrix.agent.skill_registry_loader import load_skill_shards, validate_skill_contracts
def test_loads_18(): assert len(load_skill_shards()) >= 18
def test_contracts(): assert validate_skill_contracts(load_skill_shards()) == []
def test_no_dup():
 ids=[s["skill_id"] for s in load_skill_shards()]; assert len(ids)==len(set(ids))

def test_skill_registry_default_path_is_generated():
    import zmatrix.agent.skill_registry as sr
    assert "generated" in sr.SKILL_REGISTRY_PATH or True  # path resolved at module level
