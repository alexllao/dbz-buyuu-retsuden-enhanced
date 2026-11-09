from pathlib import Path
import sys,json,hashlib
promoArgs=sys.argv[1:];promos=promoArgs or ['original','normal','aldea','porunga']
s=Path('work/namek-simulation/runtime.py').read_text().split("if __name__=='__main__':")[0].replace('work/combo-startup/candidate.bin','work/namek-native-r7/integrated.bin');exec(compile(s,'native-promo-preparation','exec'),globals());PREP=Path('work/namek-native-r7/states-final');selectionProof=[]

def press(keys,n=3,wait=20):
 for _ in range(n):tick(keys)
 for _ in range(wait):tick()

def boot_stage(cid,enemy):
 core.retro_reset()
 for j,entry in enumerate(steps[:15]):
  if j in [9,11]:
   selected=cid if j==9 else enemy
   for direction,count in [('DOWN',selected//3),('RIGHT',selected%3)]:
    for _ in range(count):press([direction],4,16)
  for _ in range(entry.get('frames',1)):tick([] if j==11 else entry.get('buttons',[]))
 for f in range(2400):
  if rw(0xe6a4)==0x20 and rw(0xe750)==3:break
  tick(['C'] if f%120<3 else [])
 assert rw(0xe6a4)==0x20 and rw(0xe750)==3,(cid,enemy,'menu not reached',rw(0xe6a4),rw(0xe750))
 assert [rb(P1+0x58),rb(P2+0x58)]==[cid,enemy],(cid,enemy,rb(P1+0x58),rb(P2+0x58))
 press(['DOWN']);assert rw(0xe9f6)==1
 count={'original':6,'normal':3,'aldea':2,'porunga':1}[promoSlug]
 for _ in range(count):press(['B'],3,120)
 variant={'original':0,'normal':1,'aldea':2,'porunga':3}[promoSlug];assert rb(0xe741)==6 and rb(0xf7c0)==variant
 selectionProof.append(dict(scenario=promoSlug,cid=cid,enemy=enemy,stage=rb(0xe741),variant=rb(0xf7c0),selection='Native menu buttons only; no stage/variant/palette writes'))
 press(['START'],3,20)
 for f in range(1200):
  if rw(0xe6a4)==0xc:
   wb(P1+0xbe,0);wb(P2+0xbe,0)
  tick(['C'] if f%120<3 else [])
 wb(P1+0xbe,0);wb(P2+0xbe,0)
 for _ in range(2400):
  tick(['A','B'],['A','B'])
  if min(rw(P1+0x28),rw(P2+0x28))>=237:break
 for _ in range(90):tick()
 assert [rb(P1+0x58),rb(P2+0x58)]==[cid,enemy]

try:
 for promoSlug in promos:
  N=PREP/promoSlug;N.mkdir(parents=True,exist_ok=True)
  for cid,enemy in [(0,8)]:
   prepare_seed(cid,enemy)
   if cid in [3,5]:
    p=N/f'critical-{cid}.state';restore(p.read_bytes());fixture()
    for _ in range(1800):
     if rb(P1+0x5b)<=8 and not rw(P1+0x36) and not rw(P1+0x38):break
     tick()
    for _ in range(2400):
     if rw(P1+0x28)>=237:break
     tick(['A','B'])
    for _ in range(90):tick()
    p.write_bytes(snap())
   print('NATIVE PROMO SEED',promoSlug,cid,st(P1),flush=True)
 (PREP/'selection-proof.json').write_text(json.dumps(dict(romSha256=hashlib.sha256(rom).hexdigest(),cases=selectionProof,fixtureScope='After native stage selection: actors control bytes human, initial spacing/facing only. Critical HP obtained by real P2 punches and natural recovery; ki by native charge inputs.'),indent=2))
finally:core.retro_unload_game();core.retro_deinit()
