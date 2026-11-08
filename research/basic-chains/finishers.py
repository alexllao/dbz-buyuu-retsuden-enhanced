from pathlib import Path
import sys,json
variant=sys.argv[1];s=Path('work/basic-chains/probe.py').read_text().split('try:\n for pattern')[0];sys.argv=['probe',variant];exec(compile(s,'finisher-header','exec'),globals());results=[]
try:
 for kind,dirs,button in [('energy',[['LEFT'],['RIGHT']],['A']),('kame',[['LEFT'],['DOWN','LEFT'],['DOWN'],['DOWN','RIGHT'],['RIGHT']],['A']),('meteor',[['LEFT'],['DOWN','LEFT'],['DOWN'],['DOWN','RIGHT'],['RIGHT']]*2,['A','B']),('kiai',[['RIGHT'],['DOWN'],['DOWN','RIGHT']],['A']),('flurry',[['DOWN'],['DOWN','LEFT'],['LEFT']],['B'])]:
  for speed in [2,3,4]:
   restore(Path('work/throw-links/seeds/0.state').read_bytes());ww(P1+0xa,300);ww(P2+0xa,332);wb(P1+0x59,0);wb(P2+0x59,1)
   for _ in range(8):tick()
   r=[];contacts=[];hp=rw(P2+0x24)
   def step(k=()):
    global hp
    tick(k);now=rw(P2+0x24)
    if now<hp:contacts.append(len(r))
    hp=now;r.append(dict(f=len(r),p=st(P1),e=st(P2),keys=list(k),pose=rb(P1+4),chain=rb(P1+0xd06)))
   for f in range(120):
    keys=['A'] if f<3 else []
    for i,t in enumerate(contacts[:2]):
     if t+3<=f<t+6:keys=[['A','B'][i]]
    step(keys)
    if len(contacts)>=3:break
   for _ in range(3):step()
   for k in [k for k in dirs for _ in range(speed)]+[dirs[-1]+button]*3:step(k)
   for _ in range(480):step()
   events=[dict(f=i,damage=a['e']['hp']-t['e']['hp'],hits=t['p']['hits'],enemyAction=t['e']['action']) for i,(a,t) in enumerate(zip(r,r[1:]),1) if t['e']['hp']<a['e']['hp']];result=dict(kind=kind,speed=speed,damage=r[0]['e']['hp']-r[-1]['e']['hp'],maxHits=max(t['p']['hits'] for t in r),events=events,programs=sorted(set(t['p']['program'] for t in r)));results.append(result);(P/f'{variant}-finisher-{kind}-{speed}.json').write_text(json.dumps(r));print(result,flush=True)
 (P/f'{variant}-finishers.json').write_text(json.dumps(results,indent=2))
finally:core.retro_unload_game();core.retro_deinit()
