from __future__ import annotations
import ast, json
from pathlib import Path
ROOTS=["zmatrix","scripts"]; EXCLUDE={"__pycache__",".git"}; OUT=Path("data/research_db/agent/registry/skill_candidate_index.json")
def infer_domain(p):
 s=str(p).lower()
 for kw,d in [("zg16","ZG16"),("caseforge","CASEFORGE"),("cases","CASEFORGE"),("factor","FACTOR"),("dataforge","DATAFORGE"),("council","COUNCIL"),("report","REPORT"),("cockpit","COCKPIT"),("memory","MEMORY"),("governance","GOVERNANCE"),("agent","SYSTEM"),("zc35","ZC35"),("bmatrix","BMATRIX"),("dmatrix","DMATRIX"),("portfolio","PORTFOLIO")]:
  if kw in s: return d
 return "RESEARCHDB"
def infer_risk(n):
 for kw,r in [("write","R3"),("commit","R3"),("apply","R3"),("draft","R2"),("proposal","R2"),("render","R2"),("build","R2"),("annotate","R1"),("score","R1"),("calculate","R1"),("validate","R1"),("check","R1")]:
  if kw in n.lower(): return r+"_WRITE_RESEARCH_DB" if r=="R3" else r+"_DRAFT" if r=="R2" else r+"_ANNOTATE"
 return "R0_READ"
def scan_sh(path):
    domain=infer_domain(path)
    return {"candidate_id":f"CANDIDATE.{domain}.{path.stem.upper()}","module_path":str(path),"symbol_name":path.name,"candidate_type":"script","domain":domain,"suggested_skill_id":f"{domain}.{path.stem.upper()}","suggested_skill_layer":"L1_WORKFLOW","suggested_risk_level":"R1_ANNOTATE","read_layers":[],"write_layers":[],"requires_human_review":False,"production_allowed":False,"status":"CANDIDATE_ONLY","reason":"script discovered"}

def scan_py(path):
 out=[]; domain=infer_domain(path)
 try: tree=ast.parse(path.read_text("utf-8",errors="ignore"))
 except: return out
 for node in ast.walk(tree):
  if isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef)) and not node.name.startswith("_"):
   r=infer_risk(node.name); out.append({"candidate_id":f"CANDIDATE.{domain}.{node.name.upper()}","module_path":str(path),"symbol_name":node.name,"candidate_type":"function","domain":domain,"suggested_skill_id":f"{domain}.{node.name.upper()}","suggested_skill_layer":"L0_ATOMIC","suggested_risk_level":r,"read_layers":[],"write_layers":[],"requires_human_review":r not in["R0_READ","R1_ANNOTATE"],"production_allowed":False,"status":"CANDIDATE_ONLY","reason":"public function"})
 return out
def preserve_existing_order(cands):
 by_key={(c["module_path"],c["symbol_name"]):c for c in cands}
 ordered=[]; used=set()
 if OUT.exists():
  try: existing=json.loads(OUT.read_text(encoding="utf-8"))
  except Exception: existing=[]
  for item in existing:
   k=(item.get("module_path"),item.get("symbol_name"))
   if k in by_key and k not in used:
    ordered.append(by_key[k]); used.add(k)
 remaining=[c for k,c in by_key.items() if k not in used]
 remaining.sort(key=lambda c: (c["domain"], c["module_path"], c["symbol_name"], c["candidate_type"]))
 ordered.extend(remaining)
 return ordered
def main():
 cands=[]
 for r in ROOTS:
  p=Path(r)
  if not p.exists(): continue
  for f in sorted(p.rglob("*"), key=lambda x: x.as_posix()):
   if any(e in f.parts for e in EXCLUDE): continue
   if f.suffix==".py": cands.extend(scan_py(f))
   elif f.suffix==".sh": cands.append(scan_sh(f))
 seen=set(); dedup=[]
 for c in cands:
  k=(c["module_path"],c["symbol_name"])
  if k not in seen: seen.add(k); dedup.append(c)
 dedup=preserve_existing_order(dedup)
 OUT.parent.mkdir(parents=True,exist_ok=True)
 payload=json.dumps(dedup,ensure_ascii=False,indent=2)
 if not OUT.exists() or OUT.read_text(encoding="utf-8") != payload:
  OUT.write_text(payload,encoding="utf-8")
 print(f"skill candidates: {len(dedup)}")
if __name__=="__main__": main()
