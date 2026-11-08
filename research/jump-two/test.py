from pathlib import Path
import sys,json,hashlib
variant=sys.argv[1];P=Path('work/jump-two');rompath=f'work/jump-two/{variant}.bin';src=Path('work/hits-hud-v3/prepare.py').read_text().split('try:\n for j,entry in enumerate(steps[:-1]):')[0].replace("romfile=BASE/'work/hits-hud-v3/candidate.bin'",f"romfile=BASE/'{rompath}'")
for old in [0x104,0x106,0x117,0x120,0x121,0x122,0x124]:src=src.replace('b+'+hex(old)+')','b+'+hex(old+0xc00)+')')
sys.argv=['prepare','0'];exec(compile(src,'jump-matrix','exec'),globals());results=[]
def actor(b):return dict(**st(b),flags=rw(b+0x20),cid=rb(b+0x58))
try:
 for port in [0,1]:
  for facing in [0,1]:
   fwd='RIGHT' if facing==0 else 'LEFT';back='LEFT' if facing==0 else 'RIGHT';a,b=(P1,P2) if port==0 else (P2,P1)
   for mode in ['vertical','forward','backward','running','backrun','air-A','air-B','running-A','running-B','flight-C']:
    restore(Path(f'work/barrage-roster/seeds/0-{port}.state').read_bytes());wb(P1+0xbe,0);wb(P2+0xbe,0)
    direction=back if mode in ['backward','backrun'] else fwd;startx=420 if direction=='LEFT' else 100
    ww(a+0xa,startx);ww(a+0xc,0);ww(b+0xa,700 if facing==0 else 20);wb(a+0x59,facing);wb(b+0x59,1-facing)
    for _ in range(20):tick()
    seq=[]
    if mode.startswith('running') or mode=='backrun':seq += [[direction]]*4+[[]]*4+[[direction]]*12
    seq += ([['C']]*3 if mode=='flight-C' else [['UP'] if mode=='vertical' else ['UP',direction]]*3)
    if mode.endswith('-A') or mode.endswith('-B'):seq += [[]]*6+[[mode[-1]]]*3
    seq += [[]]*160;r=[]
    for f,k in enumerate(seq):
     tick(k,[]) if port==0 else tick([],k);r.append(dict(f=f,p=actor(a),e=actor(b)))
    airborne=[t for t in r if t['p']['y']<448];first=next(t['f'] for t in r if t['p']['y']<448);land=next((t['f'] for t in r[first+1:] if t['p']['y']==448),None)
    result=dict(port=port+1,facing=facing,mode=mode,height=448-min(t['p']['y'] for t in r),airFrames=land-first if land else None,range=abs(r[land]['p']['x']-r[max(0,first-1)]['p']['x']) if land else None,run=any(t['p']['action'] in [7,8] for t in r),programs=sorted(set(t['p']['program'] for t in r)),end=r[-1]['p'])
    if mode=='flight-C':assert r[-1]['p']['plane'] and r[-1]['p']['y']==160,result
    else:assert land is not None and r[-1]['p']['y']==448 and r[-1]['p']['program']==0,result
    if mode.startswith('running') or mode=='backrun':assert result['run'],result
    assert all(t['p']['hp']==r[0]['p']['hp'] and t['e']['hp']==r[0]['e']['hp'] for t in r)
    (P/f'trace-{variant}-{port}-{facing}-{mode}.json').write_text(json.dumps(r));results.append(result)
 # Representantes ajenos a Goku: comparar luego las trazas completas.
 for cid in [1,2,3,5,6,7,9]:
  seed=Path(f'work/barrage-roster/seeds/{cid}-0.state') if cid in [3,5,6,7,9] else Path(f'work/responsive-v3/routes/{cid}/charged.state');restore(seed.read_bytes());wb(P1+0xbe,0);wb(P2+0xbe,0);ww(P1+0xa,100);ww(P2+0xa,700);wb(P1+0x59,0);wb(P2+0x59,1)
  for _ in range(20):tick()
  r=[]
  for f,k in enumerate([['UP','RIGHT']]*3+[[]]*160):tick(k);r.append(dict(f=f,p=actor(P1),e=actor(P2)))
  (P/f'other-{variant}-{cid}.json').write_text(json.dumps(r));assert r[-1]['p']['y']==448
 report=dict(passed=True,romSha256=hashlib.sha256(Path(rompath).read_bytes()).hexdigest(),cases=results,otherCharacterCases=7);(P/f'validation-{variant}.json').write_text(json.dumps(report,indent=2));print(variant,'PASS',len(results),'Goku cases +7 other characters')
finally:core.retro_unload_game();core.retro_deinit()
