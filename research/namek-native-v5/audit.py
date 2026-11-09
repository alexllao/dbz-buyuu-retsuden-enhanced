from pathlib import Path
import json,hashlib
P=Path('work/namek-native-v5');OLD=Path('work/namek-native-v4');cases=[]
for slug in ['normal','aldea','porunga']:
 assert (P/slug/'palette.bin').read_bytes()==(OLD/slug/'palette.bin').read_bytes()
 for label in ['01-vuelo','02-goku']:
  a=json.loads((OLD/'promo'/slug/(label+'.json')).read_text());b=json.loads((P/'promo'/slug/(label+'.json')).read_text())
  keys=['p','e','keys1','keys2','scene','cinema','physicalStage','nativeVariant']
  mismatch=[i for i,(x,y) in enumerate(zip(a,b)) if any(x[k]!=y[k] for k in keys)]
  assert len(a)==len(b) and not mismatch,(slug,label,len(a),len(b),mismatch[:10])
  cases.append(dict(variant=slug,clip=label,frames=len(b),actorStatesAndInputsExact=True,paletteV4Exact=True))
(P/'audit.json').write_text(json.dumps(dict(cases=cases,verifiedAgainst='V4 actor trace, input route and approved palette bytes'),indent=2));print('All6 input/actor traces match V4 exactly; palettes unchanged')
