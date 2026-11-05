from pathlib import Path
import sys,json,hashlib
ROOT=Path.cwd();source=sys.argv[1];cid=int(sys.argv[2]);port=int(sys.argv[3]);turbo='--turbo' in sys.argv;tag=sys.argv[4];out=ROOT/'work/stun-break/tests'/f'{tag}-{cid}-p{port}-{int(turbo)}';out.mkdir(parents=True,exist_ok=True)
s=Path('work/side-switch/test_commands.py').read_text().split('results=[]')[0];s=s[s.index('sys.path.insert'):];exec(compile(s,'stun-test-setup','exec'),globals())
victim=P1 if port==1 else P2; attacker=P2 if port==1 else P1

def vstate():return dict(hp=rw(victim+0x24),stun=rb(victim+0x51),threshold=rb(victim+0x54),timer=rw(victim+0x36),other=rw(victim+0x38),action=rb(victim+0x5b),program=rw(victim),cursor=rw(victim+6))
def press(k=(),v=()):tick(v,k) if port==1 else tick(k,v)
try:
 for index,step in enumerate(steps[:-1]):
  if index in [9,11]:
   selected=cid if (index==9 and port==1) or (index==11 and port==2) else 0
   for direction,count in [('DOWN',selected//3),('RIGHT',selected%3)]:
    for _ in range(count):
     for _ in range(4):tick([direction])
     for _ in range(16):tick()
  keys=step.get('buttons',[]) if index!=11 else []
  if turbo and index<2:keys=list(set(keys+['A','B']))
  for _ in range(step.get('frames',1)):tick(keys)
 assert rb(victim+0x58)==cid
 wb(P1+0xbe,0);wb(P2+0xbe,0)
 for _ in range(300):tick()
 # Diagnostic fixture: safe spacing and threshold minus one. Native hit triggers actual dizzy.
 ww(attacker+0xa,300);ww(victim+0xa,332);ww(attacker+0xc,0);ww(victim+0xc,0);wb(attacker+0x59,0);wb(victim+0x59,1)
 for _ in range(8):tick()
 wb(victim+0x51,rb(victim+0x54)-1)
 trace=[]
 for f in range(320):
  press(['A'] if f<6 else []);trace.append(vstate())
  if rw(victim+0x36)>0 and rb(victim+0x5b)==13 and rb(attacker+0x5b)<=8:break
 assert rw(victim+0x36)>0 and rb(victim+0x5b)==13,trace
 nativeDizzy=vstate();baseline=snap();results=[]
 for label,button in [('first-punch','A'),('first-kick','B'),('no-hit',None),('miss','A')]:
  restore(baseline)
  if label=='miss':ww(attacker+0xa,100)
  else:ww(attacker+0xa,rw(victim+0xa)-32)
  before=vstate();rows=[];hit=None
  for f in range(120 if button else 24):
   press([button] if button and f<6 else []);row=vstate();row['f']=f;rows.append(row)
   if row['hp']<before['hp'] and hit is None:
    hit=row.copy();save_image(out/(label+'.png'))
  if label in ['first-punch','first-kick']:
   assert hit is not None,(label,rows)
   passed=hit['timer']==0 and hit['stun']==0 if tag!='previous' else hit['timer']>0
   assert passed,(label,hit)
   # Once normal hit reaction ends, no return to native dizzy without another hit.
   assert not any(r['timer']>0 for r in rows[hit['f']+1:]) if tag!='previous' else True
  else:passed=all(r['hp']==before['hp'] for r in rows) and any(r['timer']>0 for r in rows);assert passed,(label,rows)
  results.append(dict(label=label,before=before,firstHit=hit,passed=passed,trace=rows))
 # Existing ordinary hit behavior must keep accumulating natively, not erase it.
 restore(baseline);ww(victim+0x36,0);wb(victim+0x51,0);ww(victim+0x32,0)
 # Let native dizzy recovery restore neutral.
 for _ in range(35):tick()
 ww(attacker+0xa,rw(victim+0xa)-32);before=vstate();rows=[]
 for f in range(100):press(['A'] if f<6 else []);rows.append(vstate())
 hit=next(r for r in rows if r['hp']<before['hp']);assert hit['stun']>0 and hit['timer']==0,hit
 results.append(dict(label='ordinary-hit-accumulates',firstHit=hit,passed=True))
 report=dict(romSha256=hashlib.sha256(rom).hexdigest(),victimCid=cid,victimPort=port,turbo=turbo,nativeDizzy=nativeDizzy,fixture='Native menus. Human control, diagnostic spacing and threshold-1 set before a real native hit triggers dizzy. Follow-up uses actual A/B input; timer, pose and HP not forced in first-hit trials.',passed=all(r['passed'] for r in results),results=results)
 (out/'report.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(cid,port,turbo,report['passed'],flush=True)
finally:core.retro_unload_game();core.retro_deinit()
