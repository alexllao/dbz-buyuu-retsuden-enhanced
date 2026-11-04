from pathlib import Path
import sys,subprocess,concurrent.futures
ROOT=Path('work/auras/colors-v4')
src=Path('work/auras/v3/record.py').read_text(encoding='utf-8')
src=src.replace('encoder=None\ntry:', '''
build=json.loads(Path('work/auras/colors-v4/build.json').read_text(encoding='utf-8'))
resources=json.loads(Path('work/auras/colors-v4/resources.json').read_text(encoding='utf-8'))
native_atlas=Path('work/auras/v3/tiles.bin').read_bytes()
def compact(v):return ((v>>1)&7)|(((v>>5)&7)<<3)|(((v>>9)&7)<<6)
def recolor(data,mapping):return bytes((mapping.get(v>>4,v>>4)<<4)|mapping.get(v&15,v&15) for v in data)
expected1=recolor(native_atlas[:55*32],{int(k):v for k,v in resources['styles'][str(cid)]['roles'].items()})
expected2=recolor(native_atlas[:55*32],{7:7,11:11,8:8})
expected_all=expected1+expected2+native_atlas[61*32:64*32]
def color_sample():
 state=snap();v=state[0x12425:0x22425];cram=state[0x22425:0x224a5]
 actual=b''.join(b''.join(v[i:i+2][::-1] for i in range(tile*32,tile*32+32,2)) for tile in resources['physical_tiles'])
 pal=[]
 for who,b in [('p1',P1),('p2',P2)]:
  actorcid=rb(b+0x58);alt=who=='p2' and rb(P1+0x58)==actorcid
  base=(0x801e4 if alt else 0x80064)+actorcid*32
  expected=[compact(int.from_bytes(rom[base+i*2:base+i*2+2],'big')) for i in range(16)]
  offset=0 if who=='p1' else 32
  observed=[int.from_bytes(cram[offset+i*2:offset+i*2+2],'little') for i in range(16)]
  pal.append(dict(actor=who,cid=actorcid,alternate=alt,expected=expected,observed=observed,exact=expected[1:]==observed[1:]))
 return dict(dirty=rb(P1+0x116),scene=rb(0xe73c),effect=rw(0xe9c4),atlas_exact=actual==expected_all,palettes=pal)
samples=[]
encoder=None
try:''')
src=src.replace('  if i in (29,90,91,149,150,154,158,162,175,199,229,259):save_image(out/f\'frame-{i:03}.png\')', '''  if i in (29,30,45,60,90,91,120,149,150,154,158,162,175,199,229,259):
   save_image(out/f'frame-{i:03}.png');samples.append(dict(frame=i,**color_sample()))''')
src=src.replace(" (out/'trace.json').write_text", " (out/'colors.json').write_text(json.dumps(dict(source_sha256=hashlib.sha256(rom).hexdigest(),samples=samples),indent=2))\n (out/'trace.json').write_text")
(ROOT/'record.py').write_text(src,encoding='utf-8')
def run(cid):
 out=ROOT/'runtime'/f'cid{cid:02}';out.mkdir(parents=True,exist_ok=True)
 with (out/'run.log').open('w') as log:
  r=subprocess.run([sys.executable,str(ROOT/'record.py'),str(ROOT/'candidate.bin'),str(cid),str(out)],stdout=log,stderr=subprocess.STDOUT)
 if r.returncode:raise RuntimeError((cid,(out/'run.log').read_text()))
 print('Recorded verified color candidate',cid,flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:list(pool.map(run,range(11)))
