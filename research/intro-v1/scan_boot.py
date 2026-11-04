from pathlib import Path
import sys,json,hashlib
ROOT=Path.cwd();romfile=sys.argv[1];out=ROOT/'work/intro-consistency/boot'/Path(romfile).stem;out.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(ROOT/'work'));sys.argv=['probe','--native','--rom',romfile,'--out',str(out)]
header=(ROOT/'work/gameplay_probe.py').read_text().split('try:\n for index,step in enumerate(steps[:-1]):')[0].replace('BASE=Path(__file__).resolve().parent.parent','BASE=Path.cwd()')
exec(compile(header,'boot-scan','exec'),globals())
samples=[]
try:
 for frame in range(1,4001):
  # Do not execute an attract-mode CPU fight; only inspect preceding artwork.
  if rw(0xe6a4)==0x0c:break
  tick()
  if frame%120==0:
   path=out/f'F{frame:04}.png';save_image(path)
   (out/f'F{frame:04}.ram').write_bytes(bytes(ram))
   samples.append({'frame':frame,'state':hex(rw(0xe6a4)),'substate':hex(rw(0xe6a6)),'image':str(path),'paletteShadow':bytes(rb(0xe454+i) for i in range(128)).hex()})
 report={'romSha256':hashlib.sha256(rom).hexdigest(),'frames':frame,'samples':samples,'fixture':'Cold boot, no buttons, no RAM writes, stop before battle state0C; no CPU combat autoplay'}
 (out/'report.json').write_text(json.dumps(report,indent=2));print(json.dumps({'frames':frame,'states':[(s['frame'],s['state'],s['substate']) for s in samples]}))
finally:core.retro_unload_game();core.retro_deinit()
