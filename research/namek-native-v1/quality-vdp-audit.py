from pathlib import Path
import sys,json
s=Path('work/gameplay_probe.py').read_text().split('try:\n for index,step in enumerate(steps[:-1]):')[0].replace('BASE=Path(__file__).resolve().parent.parent','BASE=Path.cwd()');sys.argv=['audit','--native','--rom','work/namek-native/integrated.bin'];exec(compile(s,'readonly-vdp-audit-runtime','exec'),globals())
sys.path.insert(0,'work/namek-simulation');from vdp import layers,np,VOFF

def inspect(label):
 state=snap();ly=layers(state);r=ly['regs'];v=np.frombuffer(state,np.uint8,count=65536,offset=VOFF);words=np.frombuffer(state,'<u2',count=32768,offset=VOFF);raw=v.reshape(-1,2)[:,::-1].ravel();pats=np.stack((raw>>4,raw&15),axis=1).reshape(2048,8,8)
 def plane(b,x,y):
  attr=words[b//2+(y//8)*64+x//8];px=np.where(attr&0x800,7-(x&7),x&7);py=np.where(attr&0x1000,7-(y&7),y&7);return pats[attr&2047,py,px],((attr>>13)&3)*16
 aa,ab=plane((int(r[2])&0x38)<<10,ly['ax'],ly['ay']);bb,bbank=plane((int(r[4])&7)<<13,ly['bx'],ly['by']);Y,X=np.indices((224,320));mask=(X<160)&(Y>=32)&~ly['foreground'];fall=(aa==0)&(bb!=0)&mask;back=(aa==0)&(bb==0)&mask
 # Native framebuffer agrees with lower-plane/background resolution, not opaque A index0.
 w,h,pitch,pixels=latest;native=np.frombuffer(pixels,'<u2').reshape(h,pitch//2)[:,:w];cram=np.frombuffer(state,'<u2',count=64,offset=VOFF+65536);rl=np.array([0,4,8,12,17,21,25,29],np.uint16);gl=np.array([0,8,17,25,34,42,51,59],np.uint16);rgb565=(rl[cram&7]<<11)|(gl[(cram>>3)&7]<<5)|rl[(cram>>6)&7];resolved=rgb565[bbank+bb];matches=int((native[fall]==resolved[fall]).sum())
 return dict(scene=label,x=[rw(P1+10),rw(P2+10)],plane=[bool(rb(P1+0x1e)&16),bool(rb(P2+0x1e)&16)],AZeroBVisiblePixels=int(fall.sum()),AAndBZeroPixels=int(back.sum()),nativeMatchesLowerPlane=matches,AZeroBVisibleOnBottomGrass=int((fall&(Y>=144)).sum()),backgroundSamples=int(mask.sum()))
try:
 restore(Path('work/namek-native/states/porunga/seed-0.state').read_bytes());tick();report=[inspect('ground-close')]
 for _ in range(300):tick(['LEFT'])
 for _ in range(10):tick()
 report.append(inspect('separated-ground'))
 for _ in range(3):tick(['C'])
 for _ in range(90):tick()
 report.append(inspect('P1-flight'))
 Path('work/namek-quality-audit/vdp-transparency.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
finally:core.retro_unload_game();core.retro_deinit()
