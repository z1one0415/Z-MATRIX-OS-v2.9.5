#!/usr/bin/env python3
import csv,json
from pathlib import Path
cases=list(csv.DictReader(open('data/research_db/cases/case_registry_v1.csv')))
output=[]
for c in cases:
    j={}
    for k,v in c.items():
        if k is None: continue
        j[k]=True if v=='TRUE' else (False if v=='FALSE' else v)
    output.append(j)
Path('data/research_db/cases/case_registry_v1.json').write_text(json.dumps(output,indent=2,ensure_ascii=False))
print(f'{len(output)} cases synced')
