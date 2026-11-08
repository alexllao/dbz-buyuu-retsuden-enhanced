from pathlib import Path
import json
r=Path('work/input-links/candidate.bin').read_bytes()
for c,p in [(1,0xc0f),(3,0xc27)]:
 at=0x2025c+(p-0xc00)*2;t=at+int.from_bytes(r[at:at+2],'big',signed=True);print(c,hex(p),hex(t),r[t:t+12].hex())
 for pattern in ['A','AAB']:
  a=json.loads(Path(f'work/input-roster/trace-before-{c}-{pattern}-4-3.json').read_text())
  print(pattern,[(v['f'],hex(v['p']['combo']),v['e']['action'],v['p']['hits'],v['p']['hitOpen'],v['p']['cursor']) for i,v in enumerate(a) if v['p']['program']==p and (i==0 or a[i-1]['p']['program']!=p)])
