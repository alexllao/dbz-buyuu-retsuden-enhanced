from pathlib import Path
import sys,json,hashlib
cid=int(sys.argv[1]);root=Path('work/ki-startup');root.mkdir(exist_ok=True)
src=Path('work/responsive-v3/test-super-hold.py').read_text().split('try:\n route=')[0]
sys.argv=['probe','after',str(cid)];exec(compile(src,'ki-probe-setup','exec'),globals())
root=Path('work/ki-startup')
try:
 restore(Path(f'work/ki-startup/routes/{cid}/charged.state').read_bytes());seed=snap();cases=[]
 for distance in [64,280,400]:
  restore(seed);ww(P1+0xa,300);ww(P2+0xa,300+distance);wb(P1+0x59,0);wb(P2+0x59,1)
  for _ in range(8):tick()
  dirs=[['LEFT'],['DOWN','LEFT'],['DOWN'],['DOWN','RIGHT'],['RIGHT']]+([['LEFT']] if cid==1 else [])
  rr=[]
  for k in [k for k in dirs for _ in range(4)]+[dirs[-1]+['A']]*4+[[]]*400:
   tick(k);rr.append(dict(p=st(P1),e=st(P2),pose=rw(P1+4),phase=rw(P1+0x3a),proj=rb(P1+0xe2),eproj=rb(P2+0xe2),event=rb(0xe9b6),split=rw(0xe71e),cinema=rb(0xe73c),flags=rw(0xe9c4)))
  start=next(i for i,t in enumerate(rr) if t['p']['program'] in [0xc04,0xc0f])
  transitions=[dict(frame=i-start,**{k:t[k] for k in ['pose','phase','proj','eproj','event','split','cinema','flags']},program=t['p']['program'],cursor=t['p']['cursor']) for i,t in enumerate(rr) if i>=start and (i==start or any(t[k]!=rr[i-1][k] for k in ['pose','phase','proj','eproj','event','split','cinema','flags']) or t['p']['program']!=rr[i-1]['p']['program'])]
  result=dict(cid=cid,distance=distance,start=start,transitions=transitions);cases.append(result);print(json.dumps(result),flush=True)
 (root/f'startup-{cid}.json').write_text(json.dumps(dict(romSha256=hashlib.sha256(rom).hexdigest(),cases=cases),indent=2))
finally:core.retro_unload_game();core.retro_deinit()
