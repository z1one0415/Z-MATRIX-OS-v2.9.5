from zmatrix.agent.skill_registry_loader import load_skill_shards, validate_skill_contracts
if __name__=="__main__":
 s=load_skill_shards(); e=validate_skill_contracts(s)
 if e: [print("ERR:",x) for x in e]; exit(1)
 print(f"valid: {len(s)}")
