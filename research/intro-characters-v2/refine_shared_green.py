import json
from pathlib import Path
p=Path('work/intro-body-refined/target-mapping.json');m=json.loads(p.read_text())
for values in m.values():
 for k,v in values.items():
  if v==0x0486:values[k]=0x0484
  if v==0x06ca:values[k]=0x06c6
p.write_text(json.dumps(m,indent=2)+'\n');print('colors',len(set(v for d in m.values() for v in d.values())))
