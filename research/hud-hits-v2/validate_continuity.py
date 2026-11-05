from pathlib import Path
import json,hashlib
P=Path('work/hits-hud-v2');reports=[]
def load(route):return json.loads((P/'video'/route/'report.json').read_text())
for route in ['0-meteor-solo','0-comboAAA-cambio-meteor','0-combo-mareo-meteor','5-comboAAA-cambio-meteor','3-contra-P2','0-cambio-meteor-guardia','0-combo-espera-meteor']:
 r=load(route);t=r['trace'];actor='e' if route.startswith('3-') else 'p'
 active=lambda x:x[actor]['hits'] if x[actor]['hitTTL'] else 0
 expected={'0-meteor-solo':3,'0-comboAAA-cambio-meteor':6,'0-combo-mareo-meteor':10,'5-comboAAA-cambio-meteor':16,'3-contra-P2':3,'0-cambio-meteor-guardia':0,'0-combo-espera-meteor':3}[route]
 assert max(map(active,t))==expected,(route,max(map(active,t)))
 assert r['controlReturned'] and r['romSha256']==hashlib.sha256((P/'candidate.bin').read_bytes()).hexdigest()
 if route=='0-meteor-solo':
  increments=[x for prev,x in zip(t,t[1:]) if x['p']['hits']>prev['p']['hits']]
  assert [x['p']['hits'] for x in increments]==[1,2,3]
  assert increments[-1]['f']-increments[0]['f']>150
  for x in t[increments[0]['f']:increments[-1]['f']+1]:assert x['p']['hitTTL']==90
 if route=='0-combo-mareo-meteor':
  pause=[x for x in t if x['phase']=='mareo-conserva-HITS'];assert len(pause)==120
  assert all(x['p']['hits']==6 and x['p']['hitTTL']==90 and x['e']['dizzyTimer']>0 for x in pause)
  follow=next(x for x in t if x['phase']=='golpe-tras-mareo' and x['p']['hits']==7)
  assert follow['e']['dizzyTimer']==0
 if route=='3-contra-P2':
  first=next(x for x in t if x['e']['hitTTL'] and x['e']['hits']==1)
  assert first['p']['hitTTL']==0
 if route=='0-combo-espera-meteor':
  wait=[x for x in t if x['phase']=='espera-agota-ventana'];assert wait[-1]['p']['hitTTL']==0
  meteor=[x for x in t if x['phase']=='final-y-recuperacion'];assert max(x['p']['hits'] for x in meteor)==3
 reports.append(dict(route=route,passed=True,activeMaximum=expected,frames=r['frames'],damage=r['damage'],controlReturned=r['controlReturned']))
result=dict(passed=True,romSha256=hashlib.sha256((P/'candidate.bin').read_bytes()).hexdigest(),minimumVisibleHits=2,windowEligibleUpdates=90,freezeDuringAttackAndDizzy=True,crossAddsHits=False,gokuMeteorContacts=3,examples=reports,fixture='Cold prepared candidate ROM. Actual pads and native hits; initial spacing/facing only. Native stun reached with six real punches in recorded test. No timing/HP/ki/stun writes during capture; no accelerated animation.')
(P/'continuity-validation.json').write_text(json.dumps(result,indent=2));print('PASS: siete secuencias, Meteor3, combo6, mareo10, Cell16, P2 y caducidad')
