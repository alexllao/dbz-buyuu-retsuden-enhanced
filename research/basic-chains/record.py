from pathlib import Path
import sys,json
which=sys.argv[1];src=Path('work/input-v2/record.py').read_text().split('try:\n for j,entry in enumerate(steps[:-1]):')[0].replace("root=baseDir/'work/input-v2/video'/which","root=baseDir/'work/basic-chains/video'/which").replace("rompath='work/input-v2/candidate.bin' if which=='after' else 'work/responsive-cancels-v1/candidate.bin'","rompath='work/basic-chains/candidate.bin' if which=='after' else 'work/throw-links/candidate.bin'").replace("if which=='after':","if True:").replace('for _ in range(8):tick()','for _ in range(0):tick()').replace('keys=list(a)))','keys=list(a),defense=list(b),pose=rb(P1+4),chain=rb(P1+0xd06)))')
sys.argv=['record',which];exec(compile(src,'new-chain-video','exec'),globals())
def setup(cid=0,source=None,distance=32):
 seed=Path(source) if source else Path(f'work/throw-links/seeds/{cid}.state');restore(seed.read_bytes());wb(P1+0xbe,0);wb(P2+0xbe,0);ww(P1+0xa,300);ww(P2+0xa,300+distance);ww(P1+0xc,0);wb(P1+0x59,0);wb(P2+0x59,1)
 for _ in range(8):tick()
 return snap()
def chain(pattern,kind=None,guard=False,distance=32):
 start(pattern+('-'+kind if kind else '')+('-guard' if guard else '')+('-far' if distance==44 else ''),setup(distance=distance));contacts=[];hp=rw(P2+0x24)
 def step(k=()):
  nonlocal hp
  tick(k,['RIGHT'] if guard and len(contacts)>=3 else []);now=rw(P2+0x24)
  if now<hp:contacts.append(len(rows)-1)
  hp=now
 for f in range(120):
  k=[pattern[0]] if f<3 else []
  for i,t in enumerate(contacts[:2]):
   if t+3<=f<t+6:k=[pattern[i+1]]
  step(k)
  if len(contacts)>=3:break
 if kind:
  for _ in range(3):step()
  hcf=[['LEFT'],['DOWN','LEFT'],['DOWN'],['DOWN','RIGHT'],['RIGHT']]
  dirs=hcf*2 if kind=='meteor' else hcf if kind=='kame' else [['LEFT'],['RIGHT']];buttons=['A','B'] if kind=='meteor' else ['A']
  for k in [k for k in dirs for _ in range(3)]+[dirs[-1]+buttons]*3:step(k)
 for _ in range(400 if kind=='meteor' else 220):step()
 finish()
def meteor(cid,label,source):
 start(label,setup(cid,source));hcf=[['LEFT'],['DOWN','LEFT'],['DOWN'],['DOWN','RIGHT'],['RIGHT']];hcb=[['RIGHT'],['DOWN','RIGHT'],['DOWN'],['DOWN','LEFT'],['LEFT']];dirs=hcb+[['RIGHT']] if cid in [1,3,4,7,9] else hcf+[['LEFT']]
 for k in [k for k in dirs for _ in range(3)]+[dirs[-1]+['B']]*4+[[]]*700:tick(k)
 finish()
try:
 for pattern in ['AAB','AAA','ABB']:chain(pattern,distance=44 if pattern=='ABB' else 32)
 if which=='after':
  for kind in ['energy','kame','meteor']:chain('AAB',kind)
  chain('AAB','kame',guard=True)
  meteor(3,'Vegeta-Meteor','work/piccolo-hits/routes/3/low-hp.state');meteor(2,'Piccolo-Meteor','work/piccolo-hits/routes/2/charged.state');meteor(6,'A18-Meteor','work/presentation-full/routes/6/charged.state');meteor(8,'Freezer-Meteor','work/presentation-full/routes/8/charged.state')
  start('Cell-cinco-disparos',setup(5))
  for k in [['DOWN']]*110+[['DOWN','LEFT']]*4+[['LEFT']]*4+[['LEFT','A']]*4+[[]]*340:tick(k)
  finish()
  start('Gohan-lanzamiento-Masenko',setup(1))
  for _ in range(3):tick(['RIGHT','A'])
  for _ in range(180):
   if rb(P1+0x5b)<=8:break
   tick()
  for _ in range(48):tick()
  f='LEFT' if rb(P1+0x59) else 'RIGHT';b='RIGHT' if f=='LEFT' else 'LEFT'
  for k in [k for k in [[b],['DOWN',b],['DOWN'],['DOWN',f],[f],[b]] for _ in range(4)]+[[b,'A']]*4+[[]]*400:tick(k)
  finish()
 (root/'chapters.json').write_text(json.dumps(chapters,indent=2))
finally:
 if captureEncoder:captureEncoder.stdin.close();captureEncoder.wait()
 if audio_file:audio_file.close()
 core.retro_unload_game();core.retro_deinit()
