from pathlib import Path
import sys,json,hashlib
port=int(sys.argv[1]) if len(sys.argv)>1 else 1
src=Path('work/responsive-v3/probe-chain.py').read_text().split('try:\n routeRoot=')[0].replace('work/responsive-v3/candidate.bin','work/piccolo-hits/candidate.bin')
sys.argv=['test','after','2'];exec(compile(src,'piccolo-test-setup','exec'),globals());root=Path('work/piccolo-hits')
try:
 if port==2:
  for j,entry in enumerate(steps[:-1]):
   if j in [9,11]:
    selected=0 if j==9 else 2
    for direction,count in [('DOWN',selected//3),('RIGHT',selected%3)]:
     for _ in range(count):
      for _ in range(4):tick([direction])
      for _ in range(16):tick()
   for _ in range(entry.get('frames',1)):tick([] if j==11 else entry.get('buttons',[]))
  wb(P1+0xbe,0);wb(P2+0xbe,0)
  for _ in range(300):tick()
  P1,P2=P2,P1;rawtick=tick
  def tick(a=(),b=()):rawtick(b,a)
  for _ in range(3000):
   tick(['A','B'])
   if rw(P1+0x28)>=235:break
  for _ in range(80):tick()
 else:restore(Path('work/piccolo-hits/routes/2/charged.state').read_bytes())
 assert rb(P1+0x58)==2;seed=snap();reports=[]
 for facing in [0,1]:
  for mode in ['hit','guard','whiff']:
   restore(seed);distance=160 if mode=='whiff' else 32;ww(P1+0xa,300+distance if facing else 300);ww(P2+0xa,300 if facing else 300+distance);wb(P1+0x59,facing);wb(P2+0x59,1-facing)
   f='LEFT' if facing else 'RIGHT';b='RIGHT' if f=='LEFT' else 'LEFT'
   for _ in range(8):tick([],[f] if mode=='guard' else [])
   rr=[];hp=rw(P2+0x24);dirs=[[b],['DOWN',b],['DOWN'],['DOWN',f],[f],[b]]
   for k in [k for k in dirs for _ in range(4)]+[dirs[-1]+['B']]*4+[[]]*440:
    tick(k,[f] if mode=='guard' else []);rr.append(dict(p=st(P1),e=st(P2),pose=rb(P1+4),cb=rb(P1+0xcb)))
   cues=[i for i,t in enumerate(rr) if t['p']['program']==0x845 and t['e']['program']==0x886 and t['cb']&1 and (i==0 or not rr[i-1]['cb']&1)]
   result=dict(port=port,facing=facing,mode=mode,contacts=cues,maxHits=max(t['p']['hits'] for t in rr),damage=hp-rw(P2+0x24));reports.append(result)
   assert (result['maxHits']==9 and result['damage']==43 and len(cues)==7) if mode=='hit' else result['maxHits']==0,result
   (root/f'trace-{port}-{facing}-{mode}.json').write_text(json.dumps(rr))
 (root/f'validation-port{port}.json').write_text(json.dumps(dict(passed=True,romSha256=hashlib.sha256(rom).hexdigest(),cases=reports),indent=2));print('PICCOLO_TESTS',port,reports,flush=True)
finally:core.retro_unload_game();core.retro_deinit()
