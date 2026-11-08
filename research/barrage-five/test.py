from pathlib import Path
import sys,json,hashlib
P=Path('work/barrage-five');which=sys.argv[1];rompath='work/knockdown-k4/candidate.bin' if which=='before' else 'work/barrage-five/candidate.bin'
src=Path('work/hits-hud-v3/prepare.py').read_text().split('try:\n for j,entry in enumerate(steps[:-1]):')[0].replace("romfile=BASE/'work/hits-hud-v3/candidate.bin'",f"romfile=BASE/'{rompath}'")
for old in [0x104,0x106,0x117,0x120,0x121,0x122,0x124]:src=src.replace('b+'+hex(old)+')','b+'+hex(old+0xc00)+')')
sys.argv=['prepare','0'];exec(compile(src,'barrage-test','exec'),globals());sys.path.insert(0,str(Path('work/cpu-soak').resolve()));from menu_ai_setup import boot_versus
def info(b):return dict(**st(b),shot=rb(b+0x3a),types=[rb(b+0xe2+i*30) for i in range(3)])
def frame(a=(),b=()):tick(a,b)
results=[]
try:
 seeds=[Path('work/responsive-v3/routes/0/charged.state').read_bytes()]
 boot_versus(globals(),3,0);wb(P1+0xbe,0);wb(P2+0xbe,0)
 for _ in range(1800):
  tick([],['A','B'])
  if rw(P2+0x28)>=240:break
 for _ in range(70):tick()
 seeds.append(snap())
 for port in [0,1]:
  attacker,defender=(P1,P2) if port==0 else (P2,P1)
  for facing in [0,1]:
   fwd='RIGHT' if facing==0 else 'LEFT';back='LEFT' if facing==0 else 'RIGHT'
   for distance,mode in [(32,'hit'),(64,'hit'),(120,'hit'),(180,'hit'),(240,'hit'),(360,'hit'),(120,'guard'),(120,'whiff')]:
    restore(seeds[port]);wb(P1+0xbe,0);wb(P2+0xbe,0)
    for b,x,facevalue in [(attacker,300 if not facing else 480,facing),(defender,(300+distance) if not facing else (480-distance),1-facing)]:ww(b+0xa,x);ww(b+0xc,0);wb(b+0x59,facevalue)
    if mode=='whiff':wb(defender+0x1e,rb(defender+0x1e)^16)
    for _ in range(15):tick()
    seq=[['DOWN']]*4+[['DOWN',fwd]]*4+[[fwd]]*4+[[fwd,'A']]*3+[[]]*320;events=[];shots=[];previous=info(attacker);hp=rw(defender+0x24);r=[]
    for index,k in enumerate(seq):
     guards=[fwd] if mode=='guard' else []
     tick(k,guards) if port==0 else tick(guards,k)
     now=info(attacker);enemy=info(defender)
     if now['shot']>previous['shot']:
      slot=previous['shot']%3;shots.append(dict(frame=index,number=now['shot'],slot=slot,previousType=previous['types'][slot],newType=now['types'][slot]))
     if enemy['hp']<hp:events.append(dict(frame=index,damage=hp-enemy['hp'],hits=now['hits']))
     r.append(dict(f=index,p=now,e=enemy));hp=enemy['hp'];previous=now
    (P/f'test-{which}-{port}-{facing}-{distance}-{mode}.json').write_text(json.dumps(r))
    expected=3 if which=='before' else 5
    assert len(shots)==expected,(port,facing,distance,mode,shots)
    assert not any(x['previousType'] in [32,33] for x in shots),(port,facing,distance,mode,'live slot overwrite',shots)
    assert sum(e['damage'] for e in events)<=30,(port,facing,distance,mode,events)
    if distance<=120 and mode=='hit':assert len(events)==expected and max(t['p']['hits'] for t in r)==expected,(port,facing,distance,mode,events)
    if mode=='guard':assert not events and max(t['p']['hits'] for t in r)==0,(port,facing,events)
    result=dict(port=port+1,facing=facing,distance=distance,mode=mode,shots=shots,events=events,damage=sum(e['damage'] for e in events),maxHits=max(t['p']['hits'] for t in r),returnedToIdle=r[-1]['p']['program']==0);assert result['returnedToIdle'];results.append(result)
    (P/f'test-{which}-{port}-{facing}-{distance}-{mode}.json').write_text(json.dumps(r))
 print(which,'PASS',len(results),'cases',flush=True);(P/f'validation-{which}.json').write_text(json.dumps(dict(passed=True,romSha256=hashlib.sha256(Path(rompath).read_bytes()).hexdigest(),cases=results),indent=2))
finally:core.retro_unload_game();core.retro_deinit()
