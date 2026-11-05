from pathlib import Path
import sys,json,hashlib
BASE=Path.cwd(); stage=int(sys.argv[1]); romfile=Path(sys.argv[2]) if len(sys.argv)>2 else BASE/'work/stun-hud/candidate.bin'; tag=sys.argv[3] if len(sys.argv)>3 else 'actual'
out=BASE/'outputs/namek-paletas';out.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(BASE/'work'));sys.argv=['probe','--native','--rom',str(romfile),'--out',str(BASE/'work/stun-break/capture')]
header=(BASE/'work/gameplay_probe.py').read_text().split('try:\n for index,step in enumerate(steps[:-1]):')[0].replace('BASE=Path(__file__).resolve().parent.parent','BASE=Path.cwd()')
exec(compile(header,'capture-setup','exec'),globals())
try:
 for j,step in enumerate(steps[:-1]):
  if j==11:
   for direction in ['DOWN','DOWN','RIGHT','RIGHT']:
    for _ in range(4):tick([direction])
    for _ in range(16):tick()
  if j==13:
   wb(0xe741,stage)
  if False:
   for _ in range(stage):
    for _ in range(4):tick(['RIGHT'])
    for _ in range(12):tick()
  for _ in range(step.get('frames',1)):tick([] if j==11 else step.get('buttons',[]))
  print('STEP',j,hex(rw(0xe6a4)),rb(0xe741),flush=True)
 wb(P1+0xbe,0);wb(P2+0xbe,0)
 for _ in range(300):tick()
 print('PALETTE',[(i,hex(rw(0xe454+i*2))) for i in range(32,64)],flush=True)
 save_image(out/f'Namek-{stage}-{tag}-suelo.png')
 (BASE/f'work/stun-break/namek-{stage}-{tag}.state').write_bytes(snap())
 (BASE/f'work/stun-break/namek-{stage}-{tag}.json').write_text(json.dumps(dict(romSha256=hashlib.sha256(rom).hexdigest(),stage=rb(0xe741),requestedStage=stage,characters=[rb(P1+0x58),rb(P2+0x58)],file=f'Namek-{stage}-{tag}-suelo.png',captureSha256=hashlib.sha256((out/f'Namek-{stage}-{tag}-suelo.png').read_bytes()).hexdigest(),fixture='Native loader, stage index set before fight loading; both actors human; actual emulator capture, no pixel retouching'),indent=2))
 for _ in range(3):tick(['UP'])
 for _ in range(9):tick()
 save_image(out/f'Namek-{stage}-{tag}-salto.png')
 print(stage,tag,hashlib.sha256(rom).hexdigest(),flush=True)
finally:core.retro_unload_game();core.retro_deinit()
