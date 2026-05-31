from __future__ import annotations
import json; from pathlib import Path
SKILLS_DIR=Path("data/research_db/agent/registry/skills"); LEGACY=Path("data/research_db/agent/registry/skill_registry.json"); GENERATED=Path("data/research_db/agent/registry/skill_registry.generated.json")
def load_skill_shards(d=SKILLS_DIR):
 s=[]
 if d.exists():
  for p in sorted(d.glob("*_skills.json")): s.extend(json.loads(p.read_text("utf-8")))
 if not s and LEGACY.exists(): s=json.loads(LEGACY.read_text("utf-8"))
 return s
def validate_skill_contracts(skills):
 errors,seen=[],set()
 req=["skill_id","skill_name","domain","version","input_schema_ref","output_schema_ref","risk_level","read_layers","write_layers","requires_human_review","production_allowed"]
 for s in skills:
  sid=s.get("skill_id","")
  if sid in seen: errors.append(f"dup:{sid}")
  seen.add(sid)
  for k in req:
   if k not in s: errors.append(f"{sid}:missing {k}")
  if s.get("production_allowed") is True: errors.append(f"{sid}:production=true")
  if s.get("write_layers") and s.get("requires_human_review") is not True: errors.append(f"{sid}:write no review")
  if str(s.get("risk_level","")).startswith(("R3","R4","R5","R6")) and s.get("proposal_required") is not True: errors.append(f"{sid}:R3+ no proposal")
 return errors
def build_generated_registry():
 s=load_skill_shards(); e=validate_skill_contracts(s)
 if e: raise ValueError("\n".join(e))
 GENERATED.parent.mkdir(parents=True,exist_ok=True); GENERATED.write_text(json.dumps(s,ensure_ascii=False,indent=2),encoding="utf-8")
 return s
