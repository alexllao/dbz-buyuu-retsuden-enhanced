from pathlib import Path
import sys,json,hashlib
cid=int(sys.argv[1]);P=Path('work/knockdown-k1/port1');P.mkdir(parents=True,exist_ok=True);P.mkdir(exist_ok=True)
sys.argv=['probe','--native','--rom','work/knockdown-k1/candidate.bin','--out',str(P/str(cid))]
sys.path.insert(0,str(Path('work/cpu-soak').resolve()))
header=Path('work/gameplay_probe.py').read_text().split('try:\n for index,step in enumerate(steps[:-1]):')[0].replace('BASE=Path(__file__).resolve().parent.parent','BASE=Path.cwd()');exec(compile(header,'knockdown-measure','exec'),globals())
from menu_ai_setup import boot_versus

def actor(b):return dict(cid=rb(b+0x58),program=rw(b),pose=rb(b+4),cursor=rw(b+6),action=rb(b+0x5b),hp=rw(b+0x24),x=rw(b+0xa),y=rw(b+0x10),hitstop=rw(b+0x40))
try:
 boot_versus(globals(),cid,0);wb(P1+0xbe,0);wb(P2+0xbe,0)
 P1,P2=P2,P1;rawtick=tick
 def tick(a=(),b=()):rawtick(b,a)
 for b,x,face in [(P1,300,0),(P2,348,1)]:ww(b+0xa,x);ww(b+0xc,0);wb(b+0x59,face)
 for _ in range(3):tick()
 for _ in range(20):tick(['DOWN'])
 seed=snap();runs=[]
 for delay in [0,1,2]:
  restore(seed)
  for _ in range(delay):tick(['DOWN'])
  rows=[]
  for f in range(500):
   tick(['DOWN','B'] if f<2 else [],[]);rows.append(dict(frame=f,p=actor(P1),e=actor(P2)))
  (P/f'raw-{cid}-{delay}.json').write_text(json.dumps(rows))
  hit=next(i for i,t in enumerate(rows) if t['e']['hp']<rows[0]['e']['hp']);wake=next(i for i,t in enumerate(rows[hit:],hit) if t['e']['action']==21 or 0xc0<=t['e']['program']<=0xc8);idle=next(i for i,t in enumerate(rows[wake:],wake) if t['e']['program']==0)
  posekey=(rows[wake-1]['e']['program'],rows[wake-1]['e']['pose']);floor=wake-1
  while floor>hit and (rows[floor-1]['e']['program'],rows[floor-1]['e']['pose'])==posekey:floor-=1
  assert rows[floor]['e']['y']==448,(cid,delay,rows[floor])
  settled=wake-1
  while settled>hit and rows[settled-1]['e']['y']==448:settled-=1
  airborne=next(i for i,t in enumerate(rows[hit:wake],hit) if t['e']['y']<448);firstTouch=next(i for i,t in enumerate(rows[airborne:wake],airborne) if t['e']['y']==448)
  # Verificar con una direccion mantenida alrededor de la recuperacion.
  restore(seed)
  for _ in range(delay):tick(['DOWN'])
  moved=None;cx=None
  for f in range(idle+25):
   k2=['LEFT'] if f>=wake else []
   tick(['DOWN','B'] if f<2 else [],k2)
   if f==wake-1:cx=rw(P2+0xa)
   if f>=wake and rb(P2+0x5b) in [1,2,7,8] and rw(P2+0xa)!=cx:
    moved=f;break
  result=dict(settledOnGround=settled,lyingFrames=wake-settled,settledThroughIdleFrames=idle-settled,settledThroughMovementFrames=moved-settled if moved is not None else None,delay=delay,hit=hit,firstGroundTouch=firstTouch,finalLyingStart=floor,wakeStart=wake,idle=idle,firstMovement=moved,reaction=hex(rows[hit]['e']['program']),floorPose=hex(posekey[1]),wakeProgram=hex(rows[wake]['e']['program']),floorFrames=wake-floor,wakeFrames=idle-wake,groundThroughIdleFrames=idle-floor,hitThroughIdleFrames=idle-hit,firstTouchThroughIdleFrames=idle-firstTouch,fps=float(av.timing.fps))
  assert moved is not None,result
  runs.append(result);(P/f'trace-{cid}-{delay}.json').write_text(json.dumps(rows))
 report=dict(cid=cid,romSha256=hashlib.sha256(rom).hexdigest(),romBuild='K1 trial',attack='Goku crouching sweep: DOWN20 then DOWN+B2 frames; normal speed; manual human ports',runs=runs)
 (P/f'report-{cid}.json').write_text(json.dumps(report,indent=2));print(cid,[(t['lyingFrames'],t['wakeFrames'],t['settledThroughMovementFrames'],t['firstMovement']-t['hit']) for t in runs],flush=True)
finally:core.retro_unload_game();core.retro_deinit()
