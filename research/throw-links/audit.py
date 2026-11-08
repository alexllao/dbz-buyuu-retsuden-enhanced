from pathlib import Path
import sys,json,hashlib
P=Path('work/throw-links');P.mkdir(exist_ok=True);requested=[int(x) for x in sys.argv[1:]] or list(range(11));src=Path('work/hits-hud-v3/prepare.py').read_text().split('try:\n for j,entry in enumerate(steps[:-1]):')[0].replace("romfile=BASE/'work/hits-hud-v3/candidate.bin'","romfile=BASE/'work/barrage-roster/candidate.bin'")
for old in [0x104,0x106,0x117,0x120,0x121,0x122,0x124]:src=src.replace('b+'+hex(old)+')','b+'+hex(old+0xc00)+')')
sys.argv=['prepare','0'];exec(compile(src,'throw-audit','exec'),globals());sys.path.insert(0,str(Path('work/cpu-soak').resolve()));from menu_ai_setup import boot_versus
names=['Goku','Gohan','Piccolo','Vegeta','Trunks','Cell','A18','Krilin','Freezer','Recoome','Ginyu'];techniques=['Kamehameha','Masenko','Special Beam Cannon','Final Flash','Burning Attack','Special Beam Cannon','Energy Flame','Kamehameha','Mega Buster','Eraser Gun','Terra Smash']
def actor(b):return dict(**st(b),shotTypes=[rb(b+0xe2+30*i) for i in range(3)],pose=rb(b+4))
def fixture(seed):
 restore(seed);wb(P1+0xbe,0);wb(P2+0xbe,0)
 for b,x,facing in [(P1,300,0),(P2,332,1)]:ww(b+0xa,x);ww(b+0xc,0);wb(b+0x59,facing)
 for _ in range(8):tick()
def run_case(cid,seed,delay,guard=False,throwOnly=False):
 fixture(seed);r=[]
 def step(k=()):
  defense=['RIGHT' if rw(P2+0xa)>rw(P1+0xa) else 'LEFT'] if guard else []
  tick(k,defense);r.append(dict(frame=len(r),p=actor(P1),e=actor(P2),keys=list(k),defense=defense))
 for _ in range(3):step(['RIGHT','A'])
 assert rb(P1+0x5b)==0x3a,(cid,'not throw',rw(P1),rb(P1+0x5b))
 for _ in range(180):
  if rb(P1+0x5b)<=8:break
  step()
 release=len(r)-1
 for _ in range(delay):step()
 start=len(r);f='LEFT' if rb(P1+0x59) else 'RIGHT';b='RIGHT' if f=='LEFT' else 'LEFT';expected=0
 if not throwOnly:
  commands=json.loads(Path('repository/research/combos-v3/native-commands.json').read_text())[str(cid)];token=5 if cid==0 else 7 if cid==1 else 6;expected=next(x['program'] for x in commands if x['token']==token)
  dirs=[[b],['DOWN',b],['DOWN'],['DOWN',f],[f]] if cid==0 else [[b],['DOWN',b],['DOWN'],['DOWN',f],[f],[b]] if token==7 else [['DOWN'],['DOWN',b],[b],[f]]
  for k in [k for k in dirs for _ in range(4)]+[dirs[-1]+['A']]*4:step(k)
 for _ in range(600):step()
 events=[dict(frame=i,damage=a['e']['hp']-t['e']['hp'],y=t['e']['y'],victimAction=t['e']['action'],victimProgram=t['e']['program'],attackerProgram=t['p']['program'],hits=t['p']['hits']) for i,(a,t) in enumerate(zip(r,r[1:]),1) if t['e']['hp']<a['e']['hp']]
 accepted=next((i for i,t in enumerate(r) if t['p']['program']==expected),None) if not throwOnly else None
 projectile=next((i for i,t in enumerate(r[start:],start) if any(x>=32 for x in t['p']['shotTypes'])),None)
 firstAir=next((i for i,t in enumerate(r) if t['e']['y']<448),None);touch=next((i for i,t in enumerate(r[firstAir+1:],firstAir+1) if t['e']['y']==448),None) if firstAir is not None else None
 result=dict(cid=cid,name=names[cid],technique=techniques[cid],delay=delay,guard=guard,throwOnly=throwOnly,release=release,commandStart=start,expected=expected,accepted=accepted,projectile=projectile,firstGroundTouch=touch,totalDamage=r[0]['e']['hp']-r[-1]['e']['hp'],events=events,maxHits=max(t['p']['hits'] for t in r),finalActors=[r[-1]['p']['action'],r[-1]['e']['action']],victimYAtCommand=r[start]['e']['y'])
 label=f'{cid}-{delay}-'+('guard' if guard else 'neutral')+('-throwOnly' if throwOnly else '');(P/f'trace-{label}.json').write_text(json.dumps(r));return result
try:
 for cid in requested:
  seedPath=P/f'seeds/{cid}.state';seedPath.parent.mkdir(exist_ok=True)
  if not seedPath.exists():
   old=Path(f'work/barrage-roster/seeds/{cid}-0.state')
   if old.exists():seedPath.write_bytes(old.read_bytes())
   else:
    core.retro_reset();boot_versus(globals(),cid,0 if cid else 3);wb(P1+0xbe,0);wb(P2+0xbe,0)
    for _ in range(3000):
     tick(['A','B'])
     if rw(P1+0x28)>=240:break
    for _ in range(100):tick()
    seedPath.write_bytes(snap())
  seed=seedPath.read_bytes();baseline=run_case(cid,seed,0,throwOnly=True);results=[]
  for delay in [0,12,24,36,48,64,80,100,120]:
   result=run_case(cid,seed,delay);results.append(result);print(names[cid],delay,'release',result['release'],'accepted',result['accepted'],'projectile',result['projectile'],'damage',result['totalDamage'],'events',[(x['frame'],x['damage'],x['y']) for x in result['events']],flush=True)
  connected=[x for x in results if x['totalDamage']>baseline['totalDamage']];chosen=min(connected,key=lambda x:next(e['frame'] for e in x['events'] if e['damage']>baseline['totalDamage'])) if connected else results[0]
  for delay in sorted(set([0,chosen['delay']])):results.append(run_case(cid,seed,delay,guard=True))
  report=dict(cid=cid,name=names[cid],technique=techniques[cid],romSha256=hashlib.sha256(Path('work/barrage-roster/candidate.bin').read_bytes()).hexdigest(),baseline=baseline,cases=results,earliestUsefulDelay=chosen['delay'] if connected else None);(P/f'report-{cid}.json').write_text(json.dumps(report,indent=2));print('DONE',names[cid],'bestDelay',report['earliestUsefulDelay'],flush=True)
finally:core.retro_unload_game();core.retro_deinit()
