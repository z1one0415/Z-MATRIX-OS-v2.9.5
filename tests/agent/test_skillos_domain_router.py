from zmatrix.agent.skill_domain_registry import get_skill_domain, has_domain_router; from zmatrix.agent.domain_skill_router import route_skill_by_domain
def test_domain(): assert get_skill_domain("ZG16.GET_SOURCE_REGISTRY")=="ZG16"
def test_zg16_has(): assert has_domain_router("ZG16.GET_SOURCE_REGISTRY") is True
def test_unknown_blocks():
 r=route_skill_by_domain("UNKNOWN.DO",{},{})
 assert r["status"]=="BLOCKED"
