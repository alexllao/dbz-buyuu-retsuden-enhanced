from pathlib import Path
import sys,json,hashlib
short_root=Path('work/short-roster-links');short_root.mkdir(exist_ok=True);s=Path('work/input-v2/record.py').read_text().split('try:\n for j,entry in enumerate(steps[:-1]):')[0]
s=s.replace("root=baseDir/'work/input-v2/video'/which", "root=baseDir/'work/short-roster-links/video'/which")
s=s.replace("rompath='work/input-v2/candidate.bin' if which=='after' else 'work/responsive-cancels-v1/candidate.bin'", "rompath='work/input-links/candidate.bin'")
s=s.replace("if which=='after':",'if True:').replace('for _ in range(8):tick()','for _ in range(0):tick()')
sys.argv=['record','after'];exec(compile(s,'roster-short-native-record','exec'),globals())
names=['Goku','Gohan','Piccolo','Vegeta','Trunks','Cell','A18','Krilin','Freezer','Recoome','Ginyu'];report=[]
try:
 for cid in range(11):
  restore(Path(f'work/throw-links/seeds/{cid}.state').read_bytes());wb(P1+0xbe,0);wb(P2+0xbe,0);ww(P1+0xa,300);ww(P2+0xa,332);wb(P1+0x59,0);wb(P2+0x59,1)
  for _ in range(8):tick()
  start(names[cid],snap());pattern='A' if cid in [2,6,8] else 'AAB';contacts=[];hp=rw(P2+0x24)
  def step(k=()):
   global hp
   tick(k);now=rw(P2+0x24)
   if now<hp:contacts.append(len(rows)-1)
   hp=now
  for f in range(100):
   k=[pattern[0]] if f<3 else []
   for i,t in enumerate(contacts[:len(pattern)-1]):
    if t+3<=f<t+6:k=[pattern[i+1]]
   step(k)
   if len(contacts)>=len(pattern):break
  assert len(contacts)==len(pattern),(cid,contacts)
  for _ in range(3):step()
  dirs=[['LEFT'],['DOWN','LEFT'],['DOWN'],['DOWN','RIGHT'],['RIGHT']] if cid==0 else [['LEFT'],['DOWN','LEFT'],['DOWN'],['DOWN','RIGHT'],['RIGHT'],['LEFT']] if cid==1 else [['DOWN'],['DOWN','LEFT'],['LEFT'],['RIGHT']]
  for k in [k for k in dirs for _ in range(4)]+[dirs[-1]+['A']]*4:step(k)
  for _ in range(260):step()
  expected=next(x['program'] for x in json.loads(Path('repository/research/combos-v3/native-commands.json').read_text())[str(cid)] if x['token']==(5 if cid==0 else 7 if cid==1 else 6))
  assert any(t['p']['program']==expected for t in rows),(cid,'special not started')
  assert len(contacts)>len(pattern),(cid,'no extra contact')
  result=dict(cid=cid,name=names[cid],pattern=pattern,damage=rows[0]['e']['hp']-hp,maxHits=max(t['p']['hits'] for t in rows),contactFrames=contacts,expected=expected,romSha256=hashlib.sha256(rom).hexdigest());report.append(result);finish();print(result,flush=True)
 (short_root/'takes.json').write_text(json.dumps(report,indent=2))
finally:
 if captureEncoder:captureEncoder.stdin.close();captureEncoder.wait()
 if audio_file:audio_file.close()
 core.retro_unload_game();core.retro_deinit()
