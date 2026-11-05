from pathlib import Path
import sys,json
root=Path('work/responsive-cancels-v1');which=sys.argv[1] if len(sys.argv)>1 else 'after';cid=int(sys.argv[2]) if len(sys.argv)>2 else 0
rompath='work/responsive-cancels-v1/candidate.bin' if which=='after' else 'work/hits-hud-v3/candidate.bin'
sys.argv=['prepare',str(cid)]
header=Path('work/hits-hud-v3/prepare.py').read_text().split('try:\n for j,entry in enumerate(steps[:-1]):')[0].replace("romfile=BASE/'work/hits-hud-v3/candidate.bin'",f"romfile=BASE/'{rompath}'")
exec(compile(header,'responsive-test-header','exec'),globals())
def row():return dict(p=st(P1),e=st(P2),aura=rb(P1+0xbd),fade=rb(P1+0x111),token=rb(P1+0xb9),ttl=rb(0xf701),stored=rb(0xf702),latch=rb(0xf703),magic=rb(0xf700),held=rw(P1+0x1a),rawpad=rb(0xe666),history=[rb(P1+0x94+i) for i in range(32)],histpos=rb(P1+0xb6),histstart=rb(P1+0xb7),lastbutton=rb(P1+0xb5))
results={};clips={}
def collect(label,schedule):
 rows=[]
 for keys in schedule:tick(keys);rows.append(dict(keys=keys,**row()))
 results[label]=rows
 return rows
try:
 for j,entry in enumerate(steps[:-1]):
  if j in [9,11]:
   selected=cid if j==9 else 3
   for direction,count in [('DOWN',selected//3),('RIGHT',selected%3)]:
    for _ in range(count):
     for _ in range(4):tick([direction])
     for _ in range(16):tick()
  for _ in range(entry.get('frames',1)):tick([] if j==11 else entry.get('buttons',[]))
 wb(P1+0xbe,0);wb(P2+0xbe,0)
 for _ in range(300):tick()
 baseline=snap()
 r=collect('charge',[['A','B']]*90+[['RIGHT']]*35)
 print('CHARGE',which,cid,'aura',next((i for i,t in enumerate(r[:90]) if t['aura']),None),'movement',next((i for i,t in enumerate(r[90:]) if t['p']['action'] in [1,2]),None),flush=True)
 restore(baseline);collect('short-charge',[['A','B']]*4+[['RIGHT']]*30)
 restore(baseline)
 r=collect('buffer',[['A','B']]*60+[['A','B','DOWN']]*4+[['A','B','DOWN','RIGHT']]*4+[['A','B','RIGHT']]*4+[[]]*3+[['A']]*3+[[]]*180)
 print('BUFFER',which,cid,sorted(set(t['p']['program'] for t in r)),[(i,t['token'],t['ttl']) for i,t in enumerate(r) if t['token']!=255][:15],flush=True)
 restore(baseline)
 for _ in range(2000):
  tick(['A','B'])
  if rw(P1+0x28)>=249:break
 r=collect('full-charge',[['A','B']]*60+[[]]*60)
 print('FULL',which,cid,[(r[i]['p']['ki'],r[i]['p']['action']) for i in [0,10,59,69]],flush=True)
 charged=snap()
 if cid==0:
  commands={'kame':(['DOWN','DR','RIGHT'],'A'),'super':(['DOWN','DR','RIGHT','DOWN','DR','RIGHT'],'A'),'energy':(['LEFT','RIGHT'],'A'),'flurry':(['DOWN','DL','LEFT'],'B'),'kiai':(['RIGHT','DOWN','DR'],'A'),'elbow':(['DOWN','DL','LEFT'],'A'),'solar':(['DOWN','NEUTRAL','DOWN'],'A'),'barrage':(['LEFT','DL','DOWN','DR','RIGHT'],'A'),'knee':(['RIGHT','DOWN','DR'],'B'),'slide':(['DOWN','DR','RIGHT'],'B'),'meteor':(['DOWN','DR','RIGHT','DOWN','DR','RIGHT'],'B'),'teleport':(['RIGHT','LEFT','RIGHT'],'B')}
  for name,(dirs,button) in commands.items():
   restore(charged)
   schedule=[]
   for d in dirs:schedule += [{'DR':['DOWN','RIGHT'],'DL':['DOWN','LEFT'],'NEUTRAL':[]}.get(d,[d])]*4
   schedule += [schedule[-1]+[button]]*3+[[]]*210
   r=collect('command-'+name,schedule)
   print('COMMAND',name,'programs',sorted(set(t['p']['program'] for t in r)),'tokens',sorted(set(t['token'] for t in r if t['token']!=255)),flush=True)
 restore(charged);ww(P1+0xa,300);ww(P2+0xa,332);wb(P1+0x59,0);wb(P2+0x59,1)
 for _ in range(8):tick()
 rows=[];contacts=[];lastHP=rw(P2+0x24)
 for f in range(150):
  keys=['A'] if f<3 else []
  for idx,t in enumerate(contacts[:2]):
   if t+3<=f<t+6:keys=[['B','A'][idx]]
  tick(keys);rows.append(dict(keys=keys,**row()))
  hp=rw(P2+0x24)
  if hp<lastHP:contacts.append(f)
  lastHP=hp
 results['combo']=rows;print('COMBO',which,cid,'contacts',contacts,'programs',sorted(set(t['p']['program'] for t in rows)),flush=True)
 (root/f'runtime-{which}-{cid}.json').write_text(json.dumps(results,indent=2))
finally:core.retro_unload_game();core.retro_deinit()
