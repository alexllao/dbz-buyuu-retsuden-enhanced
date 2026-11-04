from pathlib import Path
import json,hashlib
results=[]
for cid in [0,3]:
 a=json.loads(Path(f'work/kick-combos/native/{cid}/report.json').read_text());b=json.loads(Path(f'work/kick-combos/native-regression/{cid}/report.json').read_text())
 for x,y in zip(a['results'],b['results']):
  assert x['name']==y['name'];checks={'samePrograms':x['programs']==y['programs'],'sameHitCount':len(x['hits'])==len(y['hits']),'sameFinalHP':x['trace'][-1]['enemy']['hp']==y['trace'][-1]['enemy']['hp'],'sameMinimumKi':min(t['p']['ki'] for t in x['trace'])==min(t['p']['ki'] for t in y['trace']),'sameFinalAction':x['trace'][-1]['p']['action']==y['trace'][-1]['p']['action']}
  results.append({'cid':cid,'case':x['name'],'checks':checks,'sourceHits':x['hits'],'candidateHits':y['hits'],'sourceEndKi':x['trace'][-1]['p']['ki'],'candidateEndKi':y['trace'][-1]['p']['ki'],'passed':all(checks.values())})
report={'targetSha256':hashlib.sha256(Path('work/kick-combos/candidate.bin').read_bytes()).hexdigest(),'cases':results,'passed':all(x['passed'] for x in results),'scope':'Standing kick, crouching kick and two directional B command probes per character outside new AA-B combo; native menus, actual inputs, fixed initial positions/facing only','limits':['Impact frame may differ by one; no cycle-exact timing equivalence asserted','One Goku directional-B probe ends with2 fewer ki units; minimum ki and damage match. End ki includes passive recovery and is recorded, not asserted identical. No ki writes added by this patch.']}
Path('work/kick-combos/native-regression.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report));assert report['passed']
