from pathlib import Path
import json,hashlib
P=Path('work/hits-hud-v3');expected={'0-combo-mareo-meteor':5,'0-comboAAA-cambio-meteor':6,'0-meteor-solo':3,'0-combo-espera-meteor':3,'0-cambio-meteor-guardia':0};examples=[]
for route,maximum in expected.items():
 r=json.loads((P/'video'/route/'report.json').read_text());t=r['trace']
 assert r['controlReturned'] and r['romSha256']==hashlib.sha256((P/'candidate.bin').read_bytes()).hexdigest()
 assert max(x['p']['hits'] if x['p']['hitTTL'] else 0 for x in t)==maximum
 if route=='0-combo-mareo-meteor':
  events=[x for prev,x in zip(t,t[1:]) if x['e']['hp']<prev['e']['hp']]
  assert [x['p']['hits'] for x in events[:6]]==[1]*6
  pause=[x for x in t if x['phase']=='mareo-conserva-HITS']
  assert len(pause)==120 and all(x['p']['hits']==1 and x['p']['link']==30 and x['e']['dizzyTimer']>0 for x in pause)
  assert events[6]['p']['hits']==2 and events[6]['e']['dizzyTimer']==0
 if route=='0-combo-espera-meteor':
  wait=[x for x in t if x['phase']=='espera-agota-ventana'];assert wait[-1]['p']['link']==0 and wait[-1]['p']['hitTTL']>0 and wait[-1]['p']['hits']==3
 examples.append(dict(route=route,activeMaximum=maximum,passed=True,frames=r['frames']))
v=json.loads((P/'continuity-validation.json').read_text());v['examples']=examples
(P/'continuity-validation.json').write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8');print('PASS: aislados1, enlace6, Meteor3, caducidad separada de lectura y mareo sin sumar golpes anteriores')
