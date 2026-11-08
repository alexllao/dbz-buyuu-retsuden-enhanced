from pathlib import Path
import json
P=Path('work/throw-links/after');extra=json.loads((P/'extras.json').read_text())
for cid in [0,7]:
 p=P/f'report-{cid}.json';d=json.loads(p.read_text());cases={(x['delay'],x['guard']):x for x in d['cases']}
 for x in extra:
  if x['cid']==cid:cases[(x['delay'],x['guard'])]=x
 d['cases']=list(cases.values())
 if cid==7:d['earliestUsefulDelay']=76
 p.write_text(json.dumps(d,indent=2))
