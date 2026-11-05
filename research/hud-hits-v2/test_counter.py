from pathlib import Path
import sys,json,hashlib
ROOT=Path.cwd();source=sys.argv[1];cid=int(sys.argv[2]);port=int(sys.argv[3]);turbo='--turbo' in sys.argv;out=ROOT/'work/hits-hud-v2/tests'/f'{cid}-p{port}-{int(turbo)}';out.mkdir(parents=True,exist_ok=True)
s=Path('work/side-switch/test_commands.py').read_text().split('results=[]')[0];s=s[s.index('sys.path.insert'):];exec(compile(s,'counter-test-setup','exec'),globals())
a=P1 if port==1 else P2;e=P2 if port==1 else P1

def st(b):return dict(hp=rw(b+0x24),program=rw(b),action=rb(b+0x5b),hits=rb(b+0x120)&127,ttl=rb(b+0x121),chain=rb(b+0x122),stun=rb(b+0x51),dizzy=rw(b+0x36),periodic=rw(b+0x32),x=rw(b+0xa))
def step(k=(),other=()):tick(k,other) if port==1 else tick(other,k)
try:
 for j,entry in enumerate(steps[:-1]):
  if j in [9,11]:
   selected=cid if (j==9 and port==1) or (j==11 and port==2) else (3 if cid==0 else 0)
   for direction,count in [('DOWN',selected//3),('RIGHT',selected%3)]:
    for _ in range(count):
     for _ in range(4):tick([direction])
     for _ in range(16):tick()
  keys=entry.get('buttons',[]) if j!=11 else []
  if turbo and j<2:keys=list(set(keys+['A','B']))
  for _ in range(entry.get('frames',1)):tick(keys)
 wb(P1+0xbe,0);wb(P2+0xbe,0)
 for _ in range(300):tick()
 assert rb(a+0x58)==cid
 assert (rb(P1+0x120)&127)==0 and (rb(P2+0x120)&127)==0,'round counter not reset'
 baseline=snap();results=[]
 for label,button,distance,guard in [('punch','A',32,False),('kick','B',32,False),('guard','A',32,True),('miss','A',160,False)]:
  restore(baseline);ww(a+0xa,300);ww(e+0xa,300+distance);ww(a+0xc,0);ww(e+0xc,0);wb(a+0x59,0);wb(e+0x59,1)
  for _ in range(8):tick()
  rows=[];before=st(e)
  for f in range(240):
   step([button] if f<6 else [],['RIGHT'] if guard else []);rows.append(dict(f=f,p=st(a),e=st(e)))
   if f in [12,24,48,96]:
    snapdata=snap();v=snapdata[0x12425:0x22425];v=bytes(x for i in range(0,len(v),2) for x in [v[i+1],v[i]]);idx=0;seen=set();fontVisible=False
    while idx not in seen and idx<80:
     seen.add(idx);q=0xac00+idx*8;attr=int.from_bytes(v[q+4:q+6],'big');fontVisible|=(attr&0x7ff)==0x57d
     idx=v[q+3]&127
     if idx==0:break
    if (rb(a+0x120)&127)<2 and rb(e+0x121)==0:assert not fontVisible,'single hit must not be shown'
   if f==24 and cid==0:save_image(out/(label+'.png'))
  active=max(r['p']['hits'] if r['p']['ttl'] else 0 for r in rows);damage=before['hp']-rows[-1]['e']['hp']
  checks=dict(noBlockedOrMissCount=(active==0 if guard or label=='miss' else True),acceptedHitCounted=(active>=1 and damage>0 if not guard and label!='miss' else True),counterExpires=rows[-1]['p']['ttl']==0,stunActivityResetsOnHit=all(r['e']['periodic']<=2 for prev,r in zip([dict(e=before)]+rows,rows) if r['e']['hp']<prev['e']['hp']) if not guard else True)
  assert all(checks.values()),(cid,port,label,active,damage,checks)
  results.append(dict(label=label,checks=checks,activeMax=active,damage=damage,trace=rows))
 report=dict(romSha256=hashlib.sha256(rom).hexdigest(),cid=cid,port=port,turbo=turbo,passed=True,results=results,fixture='Native menus and round reset; both human pads. Initial positions/facing only. Actual A/B/back inputs; no count, HP, ki or timer forcing.')
 (out/'report.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(cid,port,turbo,'PASS',flush=True)
finally:core.retro_unload_game();core.retro_deinit()
