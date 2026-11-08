from pathlib import Path
import sys,json
P=Path('work/basic-chains');P.mkdir(exist_ok=True);variant=sys.argv[1] if len(sys.argv)>1 else 'before';rompath='work/throw-links/candidate.bin' if variant=='before' else 'work/basic-chains/candidate.bin';src=Path('work/hits-hud-v3/prepare.py').read_text().split('try:\n for j,entry in enumerate(steps[:-1]):')[0].replace("romfile=BASE/'work/hits-hud-v3/candidate.bin'",f"romfile=BASE/'{rompath}'")
for old in [0x104,0x106,0x117,0x120,0x121,0x122,0x124]:src=src.replace('b+'+hex(old)+')','b+'+hex(old+0xc00)+')')
sys.argv=['prepare','0'];exec(compile(src,'chain-probe','exec'),globals());results=[]
try:
 for pattern in ['AAA','AAB','ABA','ABB','BAA','BAB','BBA','BBB']:
  for distance in [24,32,44]:
   restore(Path('work/throw-links/seeds/0.state').read_bytes());wb(P1+0xbe,0);wb(P2+0xbe,0);ww(P1+0xa,300);ww(P1+0xc,0);ww(P2+0xa,300+distance);wb(P1+0x59,0);wb(P2+0x59,1)
   for _ in range(8):tick()
   r=[];hits=[];hp=rw(P2+0x24)
   for f in range(180):
    keys=[pattern[0]] if f<3 else []
    for i,t in enumerate(hits[:2]):
     if t+3<=f<t+6:keys=[pattern[i+1]]
    tick(keys);now=rw(P2+0x24)
    if now<hp:hits.append(f)
    hp=now;r.append(dict(f=f,keys=keys,p=st(P1),e=st(P2),pose=rb(P1+4),chain=rb(P1+0xd06),window=rb(P1+0xd07)))
   programs=[t['p']['program'] for i,t in enumerate(r) if t['p']['program']>=0x400 and (i==0 or t['p']['program']!=r[i-1]['p']['program'])];result=dict(pattern=pattern,distance=distance,hits=hits,maxHits=max(t['p']['hits'] for t in r),damage=r[0]['e']['hp']-r[-1]['e']['hp'],programs=programs,attackPoses=sorted(set(t['pose'] for t in r if 0x400<=t['p']['program']<0x800)));results.append(result);(P/f'{variant}-{pattern}-{distance}.json').write_text(json.dumps(r));print(result,flush=True)
 (P/f'{variant}-summary.json').write_text(json.dumps(results,indent=2))
finally:core.retro_unload_game();core.retro_deinit()
