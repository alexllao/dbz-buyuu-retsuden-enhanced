from pathlib import Path
import sys,json,hashlib
port=int(sys.argv[1]) if len(sys.argv)>1 else 1;expected=[3,5,9,8,3,13,3,8,3,2];damages=[35,34,43,49,40,78,33,32,32,36]
s=Path('work/gravity-probe/baseline.py').read_text().split('try:\n for j,entry')[0].replace("rompath='work/gohan-hits/candidate.bin' if which=='after' else 'work/gohan-hits/candidate.bin'","rompath='work/meteor-hits/candidate.bin'")
sys.argv=['probe','after','0'];exec(compile(s,'meteor-hits-tests','exec'),globals());P=Path('work/meteor-hits');report=[]
try:
 for cid in range(10):
  if port==1:
   folder='piccolo-hits' if cid in [0,1,2,3,5] else 'presentation-full';state='low-hp.state' if cid in [3,5] else 'charged.state';seed=Path(f'work/{folder}/routes/{cid}/{state}').read_bytes()
  else:
   # Arranque nativo nuevo para cada pareja en el segundo mando.
   core.retro_reset()
   for j,entry in enumerate(steps[:-1]):
    if j in [9,11]:
     selected=(3 if cid==0 else 0) if j==9 else cid
     for direction,count in [('DOWN',selected//3),('RIGHT',selected%3)]:
      for _ in range(count):
       for _ in range(4):tick([direction])
       for _ in range(16):tick()
    for _ in range(entry.get('frames',1)):tick([] if j==11 else entry.get('buttons',[]))
   wb(P1+0xbe,0);wb(P2+0xbe,0)
   for _ in range(300):tick()
   assert rb(P2+0x58)==cid,(cid,rb(P2+0x58))
   P1,P2=P2,P1;rawtick=tick
   def tick(a=(),b=()):rawtick(b,a)
   for _ in range(3000):
    tick(['A','B'],['A','B'])
    if min(rw(P1+0x28),rw(P2+0x28))>=235:break
   for _ in range(100):tick()
   if cid in [3,5]:
    ww(P1+0xa,300);ww(P2+0xa,332);wb(P1+0x59,0);wb(P2+0x59,1);punches=0
    while rw(P1+0x24)>45 and punches<32:
     for f in range(75):tick([],['A'] if f<6 else [])
     for _ in range(120):
      if abs(rw(P2+0xa)-rw(P1+0xa))<=28:break
      tick([],['LEFT'] if rw(P2+0xa)>rw(P1+0xa) else ['RIGHT'])
     for _ in range(4):tick()
     punches+=1
    for _ in range(650):tick()
    for _ in range(3000):
     if rw(P1+0x28)>=235:break
     tick(['A','B'])
    for _ in range(100):tick()
    assert 0<rw(P1+0x24)<=50,(cid,rw(P1+0x24))
   seed=snap();out=P/'routes-p2'/str(cid);out.mkdir(exist_ok=True,parents=True);(out/'charged.state').write_bytes(seed)
  for facing in [0,1]:
   for mode in ['hit','guard','whiff']:
    restore(seed);distance=200 if mode=='whiff' else 32;ww(P1+0xa,300+distance if facing else 300);ww(P2+0xa,300 if facing else 300+distance);wb(P1+0x59,facing);wb(P2+0x59,1-facing);f='LEFT' if facing else 'RIGHT';b='RIGHT' if facing else 'LEFT'
    for _ in range(8):tick([],[f] if mode=='guard' else [])
    hp=rw(P2+0x24);prior=hp;rr=[];drops=[];hcf=[[b],['DOWN',b],['DOWN'],['DOWN',f],[f]];hcb=[[f],['DOWN',f],['DOWN'],['DOWN',b],[b]];dirs=hcf*2 if cid==0 else [['DOWN'],['DOWN',f],[f],[b]] if cid==5 else hcb+[[f]] if cid in [1,3,4,7,9] else hcf+[[b]];btn=['A','B'] if cid==0 else ['B']
    for i,k in enumerate([k for k in dirs for _ in range(3)]+[dirs[-1]+btn]*4+[[]]*1100):
     tick(k,[f] if mode=='guard' else []);now=rw(P2+0x24)
     if now<prior:drops.append(dict(frame=i,damage=prior-now,hits=rb(P1+0xd20)&127))
     prior=now;rr.append(dict(f=i,p=st(P1),e=st(P2),keys=k,keys2=[f] if mode=='guard' else []))
    result=dict(port=port,cid=cid,facing=facing,mode=mode,maxHits=max(t['p']['hits'] for t in rr),damage=hp-rw(P2+0x24),drops=drops,end=[rw(P1),rw(P2)])
    if mode=='hit':assert result['maxHits']==expected[cid] and result['damage']==damages[cid],result
    if result['damage']==0:assert result['maxHits']==0,result
    if cid==5:assert result['maxHits']==sum(t['damage']==6 for t in drops),result
    assert rw(P1)==0 and rb(P2+0x5b)<=8,result
    report.append(result)
    if mode=='hit':(P/f'trace-{port}-{cid}-{facing}.json').write_text(json.dumps(rr))
  print('PASS',port,cid,[x['maxHits'] for x in report[-6:]],flush=True)
  if port==2:tick=rawtick;P1,P2=P2,P1
 (P/f'validation-port{port}.json').write_text(json.dumps(dict(romSha256=hashlib.sha256(rom).hexdigest(),cases=report,passed=True),indent=2))
finally:core.retro_unload_game();core.retro_deinit()
