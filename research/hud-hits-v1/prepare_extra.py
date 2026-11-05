from pathlib import Path
import sys,json
src=Path('work/hits-hud/prepare.py').read_text().split('try:\n for j,entry in enumerate(steps[:-1]):')[0];exec(compile(src,'reuse-route-engine','exec'),globals())
try:
 restore((out/'charged.state').read_bytes())
 if cid in [3,5]:
  ww(P1+0xa,300);ww(P2+0xa,332);ww(P1+0xc,0);ww(P2+0xc,0);wb(P1+0x59,0);wb(P2+0x59,1)
  for _ in range(8):tick()
  attacks=0
  while rw(P1+0x24)>45 and attacks<30:
   for f in range(70):tick([],['A'] if f<6 else [])
   # Follow the knockback by ordinary walking.
   for _ in range(120):
    if abs(rw(P2+0xa)-rw(P1+0xa))<=30:break
    tick([],['LEFT'] if rw(P2+0xa)>rw(P1+0xa) else ['RIGHT'])
   attacks+=1
  for _ in range(500):tick()
  while rw(P1+0x28)<230:tick(['A','B'])
  for _ in range(100):tick()
  assert 0<rw(P1+0x24)<=50,(cid,rw(P1+0x24))
  (out/'low-hp-charged.state').write_bytes(snap())
  print('PREPARED',cid,'HP',rw(P1+0x24),'KI',rw(P1+0x28),'native attacks',attacks,flush=True)
 baseline=snap();results=[]
 for label in ['AAA','ABB','BAB','cambio-meteor-cerca','comboAAA-cambio-meteor-cerca','comboAAA-cambio-especial']:
  restore(baseline);ww(P1+0xa,300);ww(P2+0xa,332);ww(P1+0xc,0);ww(P2+0xc,0);wb(P1+0x59,0);wb(P2+0x59,1)
  for _ in range(8):tick()
  trace=[];phase='inicio';idle(20)
  if label in ['AAA','ABB','BAB']:basic_chain(label)
  else:
   if label.startswith('comboAAA'):basic_chain('AAA')
   cross()
   if label.endswith('cerca'):close_to(30)
   if 'meteor' in label:
    if cid==5:
     phase='meteor';f=forward();b=backward();dirs=[['DOWN'],['DOWN',f],[f],[b]]
     for k in [k for k in dirs for _ in range(4)]+[dirs[-1]+['B']]*4:run(k)
    else:move_command('meteor')
   else:move_command('downB')
  phase='recuperacion'
  for _ in range(700):
   run()
   if len(trace)>300 and rb(P1+0x5b)<=8 and rb(P2+0x5b)<=8:break
  idle(40);hits=[dict(frame=y['f'],phase=y['phase'],delta=x['e']['hp']-y['e']['hp']) for x,y in zip(trace,trace[1:]) if y['e']['hp']<x['e']['hp']]
  summ=dict(label=label,startHP=trace[0]['p']['hp'],startKi=trace[0]['p']['ki'],damage=trace[0]['e']['hp']-trace[-1]['e']['hp'],hits=hits,programs=sorted(set(t['p']['program'] for t in trace)),frames=len(trace),final=[trace[-1]['p']['action'],trace[-1]['e']['action']])
  (out/('extra-'+label+'.json')).write_text(json.dumps(dict(summary=summ,trace=trace),indent=2));results.append(summ);print(cid,summ,flush=True)
 (out/'extra-report.json').write_text(json.dumps(dict(cid=cid,results=results),indent=2))
finally:core.retro_unload_game();core.retro_deinit()
