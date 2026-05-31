from zmatrix.agent.skill_result_envelope import build_skill_success, build_skill_draft, build_skill_blocked, normalize_skill_result, assert_safe_skill_result
def test_success(): r=build_skill_success("S.T"); assert r["production_allowed"] is False and assert_safe_skill_result(r)
def test_draft(): r=build_skill_draft("C.T"); assert r["human_review_required"] and r["proposal_required"]
def test_blocked(): r=build_skill_blocked("X","n"); assert r["status"]=="BLOCKED" and assert_safe_skill_result(r)
def test_normalize(): r=normalize_skill_result("X",{"production_allowed":True}); assert r["production_allowed"] is False
