from pathlib import Path
import sys,json,hashlib
variant=sys.argv[1];port2='port2' in sys.argv;s=Path('work/basic-chains/probe.py').read_text().split('try:\n for pattern')[0];sys.argv=['probe',variant];exec(compile(s,'chain-matrix','exec'),globals());P=P/('port2' if port2 else 'port1');P.mkdir(exist_ok=True)
if port2:
 P1,P2=P2,P1;raw_tick=tick
 def tick(a=(),b=()):raw_tick(b,a)
results=[]
try:
 for facing in [0,1]:
  for pattern in ['AAA','AAB','ABA','ABB','BAA','BAB','BBA','BBB']:
   for mode in ['hit','guard','whiff']:
    restore(Path('work/barrage-roster/seeds/0-1.state' if port2 else 'work/throw-links/seeds/0.state').read_bytes());wb(P1+0xbe,0);wb(P2+0xbe,0);ww(P1+0xa,300 if facing==0 else 420);ww(P1+0xc,0);ww(P2+0xa,(332 if facing==0 else 388) if mode!='whiff' else (470 if facing==0 else 250));wb(P1+0x59,facing);wb(P2+0x59,1-facing)
    for _ in range(8):tick()
    r=[];contacts=[];hp=rw(P2+0x24)
    for f in range(180):
     if mode=='hit':
      keys=[pattern[0]] if f<3 else []
      for i,t in enumerate(contacts[:2]):
       if t+3<=f<t+6:keys=[pattern[i+1]]
     else:keys=[pattern[0]] if f<3 else [pattern[1]] if 25<=f<28 else [pattern[2]] if 50<=f<53 else []
     defense=['RIGHT' if facing==0 else 'LEFT'] if mode=='guard' else [];tick(keys,defense);now=rw(P2+0x24)
     if now<hp:contacts.append(f)
     hp=now;r.append(dict(f=f,keys=keys,p=st(P1),e=st(P2),pose=rb(P1+4),chain=rb(P1+0xd06)))
    starts=[dict(frame=i,program=t['p']['program'],action=t['p']['action'],chain=t['chain']) for i,t in enumerate(r) if 0x400<=t['p']['program']<0x800 and (i==0 or t['p']['program']!=r[i-1]['p']['program'])]
    summary=dict(port=2 if port2 else 1,facing=facing,pattern=pattern,mode=mode,contacts=contacts,damage=r[0]['e']['hp']-r[-1]['e']['hp'],maxHits=max(t['p']['hits'] for t in r),starts=starts,returnedToIdle=r[-1]['p']['program']==0)
    assert summary['returnedToIdle'],summary
    if mode=='hit':assert len(contacts)==3 and summary['maxHits']==3 and summary['damage']==36,summary
    else:assert not contacts and summary['maxHits']==0,summary
    if variant=='after' and mode=='hit':
     if pattern[1]=='A':assert starts[1]['program']==0x401,summary
     if pattern[2]=='B':assert starts[2]['program']==0x404,summary
    results.append(summary);(P/f'trace-{variant}-{facing}-{pattern}-{mode}.json').write_text(json.dumps(r))
 (P/f'validation-{variant}.json').write_text(json.dumps(dict(passed=True,romSha256=hashlib.sha256(Path(rompath).read_bytes()).hexdigest(),cases=results),indent=2));print(variant,'port',2 if port2 else 1,'PASS',len(results))
finally:core.retro_unload_game();core.retro_deinit()
