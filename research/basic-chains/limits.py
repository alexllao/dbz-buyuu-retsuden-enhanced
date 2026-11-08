from pathlib import Path
import sys,json,hashlib
variant=sys.argv[1];s=Path('work/basic-chains/probe.py').read_text().split('try:\n for pattern')[0];sys.argv=['probe',variant];exec(compile(s,'limit-header','exec'),globals());results=[]
try:
 for mode in ['held-A','fourth-A','fourth-B','guard-after-third','spam-A','low-ki']:
  restore(Path('work/throw-links/seeds/0.state').read_bytes());ww(P1+0xa,300);ww(P2+0xa,332);wb(P1+0x59,0);wb(P2+0x59,1)
  for _ in range(8):tick()
  if mode=='low-ki':ww(P1+0x28,20)
  contacts=[];hp=rw(P2+0x24);r=[]
  for f in range(360):
   keys=['A'] if f<3 else []
   if mode=='held-A':keys=['A']
   elif mode=='spam-A':keys=['A'] if f%12<3 else []
   else:
    for i,t in enumerate(contacts[:2]):
     if t+3<=f<t+6:keys=[['A','B'][i]]
    if len(contacts)>=3 and contacts[2]+3<=f<contacts[2]+6:keys=['B' if mode=='fourth-B' else 'A']
   tick(keys,['RIGHT'] if mode=='guard-after-third' and len(contacts)>=3 else []);now=rw(P2+0x24)
   if now<hp:contacts.append(f)
   hp=now;r.append(dict(f=f,p=st(P1),e=st(P2),chain=rb(P1+0xd06),keys=keys))
  starts=[dict(f=i,program=t['p']['program'],chain=t['chain']) for i,t in enumerate(r) if t['p']['program']>=0x400 and (i==0 or t['p']['program']!=r[i-1]['p']['program'])];eligible=[x for x in starts if x['chain']&0xfc==0x8c]
  assert all((x['chain']&3) in [1,2] for x in eligible)
  if mode=='held-A':assert len(contacts)==1
  results.append(dict(mode=mode,contacts=contacts,damage=r[0]['e']['hp']-r[-1]['e']['hp'],maxHits=max(t['p']['hits'] for t in r),starts=starts,assistedStarts=eligible));(P/f'{variant}-limit-{mode}.json').write_text(json.dumps(r))
 # Otros diez personajes: A-B-A, sin aplicar variantes de Goku.
 others=[]
 for cid in range(1,11):
  restore(Path(f'work/throw-links/seeds/{cid}.state').read_bytes());ww(P1+0xa,300);ww(P2+0xa,332);wb(P1+0x59,0);wb(P2+0x59,1)
  for _ in range(8):tick()
  contacts=[];hp=rw(P2+0x24);r=[]
  for f in range(180):
   keys=['A'] if f<3 else []
   for i,t in enumerate(contacts[:2]):
    if t+3<=f<t+6:keys=[['B','A'][i]]
   tick(keys);now=rw(P2+0x24)
   if now<hp:contacts.append(f)
   hp=now;r.append(dict(f=f,p=st(P1),e=st(P2),pose=rb(P1+4)))
  (P/f'other-{variant}-{cid}.json').write_text(json.dumps(r));others.append(dict(cid=cid,damage=r[0]['e']['hp']-r[-1]['e']['hp'],maxHits=max(t['p']['hits'] for t in r)))
 (P/f'{variant}-limits.json').write_text(json.dumps(dict(passed=True,romSha256=hashlib.sha256(Path(rompath).read_bytes()).hexdigest(),cases=results,otherCharacters=others),indent=2));print(variant,[(x['mode'],len(x['contacts']),len(x['assistedStarts'])) for x in results])
finally:core.retro_unload_game();core.retro_deinit()
