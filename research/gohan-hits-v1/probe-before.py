from pathlib import Path
import json,sys,hashlib
src=Path('work/responsive-v3/probe-chain.py').read_text().split('try:\n routeRoot=')[0].replace('work/responsive-v3/candidate.bin','work/piccolo-hits/candidate.bin')
sys.argv=['probe','after','0'];exec(compile(src,'cross-probe-setup','exec'),globals());root=Path('work/fast-cross');root.mkdir(exist_ok=True)
try:
 restore(Path('work/piccolo-hits/routes/1/charged.state').read_bytes());ww(P1+0xa,300);ww(P2+0xa,332);wb(P1+0x59,0);wb(P2+0x59,1)
 for _ in range(8):tick()
 rr=[];dirs=[['RIGHT'],['DOWN','RIGHT'],['DOWN'],['DOWN','LEFT'],['LEFT'],['RIGHT']]
 for k in [k for k in dirs for _ in range(4)]+[dirs[-1]+['B']]*4+[[]]*420:
  tick(k);rr.append(dict(p=st(P1),e=st(P2),pose=rb(P1+4),cb=rb(P1+0xcb),sound=rb(0x5000)))
 events=[]
 for i,t in enumerate(rr):
  prev=rr[i-1] if i else t
  if t['p']['program']!=prev['p']['program'] or t['e']['program']!=prev['e']['program'] or t['e']['hp']!=prev['e']['hp'] or (t['p']['program']==0x842 and (t['cb']&1) and not(prev['cb']&1)):
   events.append(dict(frame=i,p=hex(t['p']['program']),e=hex(t['e']['program']),pose=hex(t['pose']),cb=t['cb'],sound=t['sound'],hp=t['e']['hp'],y=t['e']['y'],hits=t['p']['hits']))
 Path('work/fast-cross/gohan-trace.json').write_text(json.dumps(dict(romSha256=hashlib.sha256(rom).hexdigest(),events=events,trace=rr),indent=2));print(json.dumps(events,indent=2),flush=True)
finally:core.retro_unload_game();core.retro_deinit()
