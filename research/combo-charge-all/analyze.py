from pathlib import Path
import json
P=Path('work/combo-charge-all');a=json.loads((P/'before-cases.json').read_text());b=json.loads((P/'after-cases.json').read_text());assert len(a)==len(b)==24
result=[]
for x,y in zip(a,b):
 assert (x['kind'],x['context'])==(y['kind'],y['context'])
 assert x['damage']==y['damage'],(x,y)
 assert y['returnedToIdle']
 if x['context'] in ['solo','late','guard','whiff']:assert not y['fastUsed'],y
 row=dict(kind=y['kind'],context=y['context'],before=x['startup'],after=y['startup'],damage=y['damage'],hitsBefore=x['maxHits'],hitsAfter=y['maxHits'],fast=y['fastUsed'])
 if y['kind']=='cell':
  row['postLaunchHitIntervalsBefore']=[q-p for p,q in zip(x['relativeHits'],x['relativeHits'][1:])]
  row['postLaunchHitIntervalsAfter']=[q-p for p,q in zip(y['relativeHits'],y['relativeHits'][1:])]
 result.append(row)
(P/'comparison.json').write_text(json.dumps(result,indent=2));print(json.dumps([r for r in result if r['context']=='cross' or r['context']=='combo'],indent=2))
