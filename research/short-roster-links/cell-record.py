from pathlib import Path
import sys,json,hashlib
escape_demo='jump' in sys.argv;guard_demo='guard' in sys.argv or escape_demo;route_phase='inicio'
s=Path('work/input-v2/record.py').read_text().split('try:\n for j,entry in enumerate(steps[:-1]):')[0]
s=s.replace("root=baseDir/'work/input-v2/video'/which", "root=baseDir/'work/long-chain/video'/which")
s=s.replace("rompath='work/input-v2/candidate.bin' if which=='after' else 'work/responsive-cancels-v1/candidate.bin'", "rompath='work/input-links/candidate.bin'")
s=s.replace("if which=='after':",'if True:').replace('for _ in range(8):tick()','for _ in range(0):tick()')
s=s.replace('keys=list(a)))','keys=list(a),keys2=list(b),phase=route_phase,scene=rb(0xe73c),cinema=rw(0xe9c4)))')
sys.argv=['record','jump' if escape_demo else 'guard' if guard_demo else 'after'];exec(compile(s,'cell-long-video','exec'),globals())
try:
 restore(Path('work/piccolo-hits/routes/5/low-hp.state').read_bytes());wb(P1+0xbe,0);wb(P2+0xbe,0);ww(P1+0xa,300);ww(P2+0xa,332);wb(P1+0x59,0);wb(P2+0x59,1)
 for _ in range(8):tick()
 start('Cell-16-impactos',snap());contacts=[];hp=rw(P2+0x24);route_phase='basicos'
 def step(k=()):
  global hp
  defense=['RIGHT' if rw(P2+0xa)>rw(P1+0xa) else 'LEFT'] if guard_demo and len(contacts)>=3 else []
  if escape_demo and len(contacts)>=3:defense=['UP']
  tick(k,defense);now=rw(P2+0x24)
  if now<hp:contacts.append(len(rows)-1)
  hp=now
 def face():
  f='LEFT' if rb(P1+0x59) else 'RIGHT';return f,'RIGHT' if f=='LEFT' else 'LEFT'
 def cmd(dirs,btn,speed=3):
  for k in [k for k in dirs for _ in range(speed)]+[dirs[-1]+btn]*3:step(k)
 for f in range(120):
  k=['A'] if f<3 else []
  for i,t in enumerate(contacts[:2]):
   if t+3<=f<t+6:k=[['A','B'][i]]
  step(k)
  if len(contacts)>=3:break
 route_phase='cruce'
 for _ in range(120):
  if rb(P1+0x5b)<=8:break
  step()
 f,b=face();cmd([[f],[b],[f]],['C'],2)
 for _ in range(100):
  if rw(P1)!=0x843 and rb(P1+0x5b)<=8:break
  step()
 route_phase='meteor';f,b=face();cmd([['DOWN'],['DOWN',f],[f],[b]],['B']);steady=0
 for _ in range(1100):
  step()
  free=rb(P1+0x5b)<=8 and rb(P2+0x5b)<=10 and not rb(0xe73c) and not rw(0xe9c4)
  steady=steady+1 if free else 0
  if steady>=35:break
 result=dict(romSha256=hashlib.sha256(rom).hexdigest(),guard=guard_demo,escapeJump=escape_demo,frames=len(rows),damage=rows[0]['e']['hp']-hp,maxHits=max(t['p']['hits'] for t in rows),contactFrames=contacts,programs=sorted(set(t['p']['program'] for t in rows)),startHP=rows[0]['p']['hp'],startKi=rows[0]['p']['ki'],controlReturned=steady>=35)
 assert result['controlReturned']
 if not guard_demo:assert result['maxHits']==16 and result['damage']==105 and 0x84a in result['programs'],result
 finish();(root/'report.json').write_text(json.dumps(result,indent=2));print(result,flush=True)
finally:
 if captureEncoder:captureEncoder.stdin.close();captureEncoder.wait()
 if audio_file:audio_file.close()
 core.retro_unload_game();core.retro_deinit()
