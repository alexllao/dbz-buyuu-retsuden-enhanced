from pathlib import Path
import sys,json
capture_variant=sys.argv[1];s=Path('work/input-v2/record.py').read_text().split('try:\n for j,entry in enumerate(steps[:-1]):')[0]
s=s.replace("root=baseDir/'work/input-v2/video'/which", "root=baseDir/'work/combo-startup/video'/which")
s=s.replace("rompath='work/input-v2/candidate.bin' if which=='after' else 'work/responsive-cancels-v1/candidate.bin'", "rompath='work/combo-startup/candidate.bin' if which=='after' else 'work/input-links/candidate.bin'")
s=s.replace("if which=='after':",'if True:').replace('for _ in range(8):tick()','for _ in range(0):tick()')
s=s.replace('keys=list(a)))','keys=list(a),types=[rb(P1+0xe2+i*30) for i in range(3)],fast=rb(0xf7b2)))')
sys.argv=['record',capture_variant];exec(compile(s,'combo-startup-record','exec'),globals());report=[]
try:
 for cid,name,expected in [(1,'Gohan',0xc0f),(3,'Vegeta',0xc27)]:
  for context in ['combo','solo']:
   restore(Path(f'work/throw-links/seeds/{cid}.state').read_bytes());wb(P1+0xbe,0);wb(P2+0xbe,0);ww(P1+0xa,300);ww(P2+0xa,332);wb(P1+0x59,0);wb(P2+0x59,1)
   for at in range(0xf7b0,0xf7b8):wb(at,0)
   for _ in range(8):tick()
   start(name+'-'+context,snap());contacts=[];hp=rw(P2+0x24)
   def step(k=()):
    global hp
    tick(k);now=rw(P2+0x24)
    if now<hp:contacts.append(len(rows)-1)
    hp=now
   if context=='combo':
    for f in range(100):
     k=['A'] if f<3 else []
     for i,t in enumerate(contacts[:2]):
      if t+3<=f<t+6:k=[['A','B'][i]]
     step(k)
     if len(contacts)>=3:break
   for _ in range(3):step()
   dirs=[['LEFT'],['DOWN','LEFT'],['DOWN'],['DOWN','RIGHT'],['RIGHT'],['LEFT']] if cid==1 else [['DOWN'],['DOWN','LEFT'],['LEFT'],['RIGHT']]
   for k in [k for k in dirs for _ in range(4)]+[dirs[-1]+['A']]*4:step(k)
   for _ in range(280):step()
   accepted=next(i for i,t in enumerate(rows) if t['p']['program']==expected);spawn=next(i for i,t in enumerate(rows) if i>=accepted and any(x>=32 for x in t['types']))
   report.append(dict(name=name,context=context,accepted=accepted,spawn=spawn,startup=spawn-accepted,damage=rows[0]['e']['hp']-hp,hits=max(t['p']['hits'] for t in rows),fast=any(t['fast'] for t in rows)));finish()
 (root/'metrics.json').write_text(json.dumps(report,indent=2));print(report,flush=True)
finally:
 if captureEncoder:captureEncoder.stdin.close();captureEncoder.wait()
 if audio_file:audio_file.close()
 core.retro_unload_game();core.retro_deinit()
