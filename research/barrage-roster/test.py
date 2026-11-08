from pathlib import Path
import sys,json,hashlib
which=sys.argv[1];quick='quick' in sys.argv;port2='port2' in sys.argv;P=Path('work/barrage-roster')/('port2' if port2 else 'port1');P.mkdir(exist_ok=True);rompath='work/knockdown-k4/candidate.bin' if which=='before' else 'work/barrage-roster/candidate.bin'
src=Path('work/hits-hud-v3/prepare.py').read_text().split('try:\n for j,entry in enumerate(steps[:-1]):')[0].replace("romfile=BASE/'work/hits-hud-v3/candidate.bin'",f"romfile=BASE/'{rompath}'")
for old in [0x104,0x106,0x117,0x120,0x121,0x122,0x124]:src=src.replace('b+'+hex(old)+')','b+'+hex(old+0xc00)+')')
sys.argv=['prepare','0'];exec(compile(src,'roster-test','exec'),globals());results=[]
if port2:
 P1,P2=P2,P1
 native_tick=tick
 def tick(a=(),b=()):native_tick(b,a)
programs={0:0xc01,3:0xc23,5:0xc3a,6:0xc46,7:0xc52,9:0xc6a}
def info(b):return dict(**st(b),cid=rb(b+0x58),projectileType=rb(b+0x7c),shot=rb(b+0x3a),types=[rb(b+0xe2+i*30) for i in range(3)],nativeCost=rw(b+0xe0))
try:
 for cid,expectedProgram in programs.items():
  for facing in ([0] if quick else [0,1]):
   fwd='RIGHT' if facing==0 else 'LEFT';back='LEFT' if facing==0 else 'RIGHT'
   for distance,mode in ([(120,'hit')] if quick else [(32,'hit'),(120,'hit'),(180,'hit'),(120,'guard'),(120,'whiff')]):
    restore(Path(f'work/barrage-roster/seeds/{cid}-{1 if port2 else 0}.state').read_bytes());wb(P1+0xbe,0);wb(P2+0xbe,0)
    for b,x,facevalue in [(P1,300 if not facing else 480,facing),(P2,300+distance if not facing else 480-distance,1-facing)]:ww(b+0xa,x);ww(b+0xc,0);wb(b+0x59,facevalue)
    if mode=='whiff':wb(P2+0x1e,rb(P2+0x1e)^16)
    for _ in range(15):tick()
    seq=([['DOWN']]*4+[['DOWN',fwd]]*4+[[fwd]]*4+[[fwd,'A']]*3) if cid==0 else ([['DOWN']]*110+[['DOWN',back]]*4+[[back]]*4+[[back,'A']]*4)
    seq += [[]]*400;r=[];shots=[];events=[];last=info(P1);hp=rw(P2+0x24)
    for f,k in enumerate(seq):
     tick(k,[fwd] if mode=='guard' else []);now=info(P1);enemy=info(P2)
     if now['shot']>last['shot']:shots.append(dict(frame=f,number=now['shot'],previousType=last['types'][last['shot']%3],ki=now['ki']))
     if enemy['hp']<hp:events.append(dict(frame=f,damage=hp-enemy['hp'],hits=now['hits']))
     r.append(dict(f=f,p=now,e=enemy));last=now;hp=enemy['hp']
    result=dict(cid=cid,facing=facing,distance=distance,mode=mode,programs=sorted(set(t['p']['program'] for t in r)),shots=shots,events=events,maxHits=max(t['p']['hits'] for t in r),returned=r[-1]['p']['program']==0)
    print(which,cid,facing,distance,mode,'shots',len(shots),'events',events,'programs',[hex(x) for x in result['programs']],flush=True)
    (P/f'trace-{which}-{cid}-{facing}-{distance}-{mode}.json').write_text(json.dumps(r));results.append(result)
    assert expectedProgram in result['programs'],result
    assert len(shots)==(3 if which=='before' else 5),result
    assert not any(x['previousType'] in [32,33] for x in shots),result
    assert result['returned'],result
    # Cell/A18 conservan dano residual nativo al bloquear; nunca son HITS.
    if mode=='guard':assert result['maxHits']==0,result
 (P/f'validation-{which}{"-quick" if quick else ""}.json').write_text(json.dumps(dict(passed=True,romSha256=hashlib.sha256(Path(rompath).read_bytes()).hexdigest(),cases=results),indent=2))
finally:core.retro_unload_game();core.retro_deinit()
