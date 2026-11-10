from pathlib import Path
import sys,json,hashlib
sys.path.insert(0,'work/simulation-deps')
from PIL import Image
import numpy as np
from collections import deque

A=Path('repository/assets/concepts/namek-native-r9')
source=Path('repository/assets/concepts/namek-house-soft-outline/prueba-borde-suave.png')
im=Image.open(source).convert('RGB');roi=(270,110,1475,774)
crop=im.crop(roi);rgb=np.asarray(crop).astype(float)
# Import the approved artwork: key the surrounding green sky/blue grass,
# then retain enclosed blue doors/windows as opaque building pixels.
warm=(rgb[:,:,0]>rgb[:,:,2]*1.1)&(rgb[:,:,1]>=rgb[:,:,2]*.95)&(rgb[:,:,0]>=rgb[:,:,1]*.95)
outside=np.zeros_like(warm);todo=deque()
hh,ww=warm.shape
for y,x in [(0,x) for x in range(ww)]+[(hh-1,x) for x in range(ww)]+[(y,0) for y in range(hh)]+[(y,ww-1) for y in range(hh)]:
 if not warm[y,x] and not outside[y,x]:outside[y,x]=True;todo.append((y,x))
while todo:
 y,x=todo.popleft()
 for dy,dx in [(0,1),(0,-1),(1,0),(-1,0)]:
  yy,xx=y+dy,x+dx
  if 0<=yy<hh and 0<=xx<ww and not warm[yy,xx] and not outside[yy,xx]:outside[yy,xx]=True;todo.append((yy,xx))
mask=~outside
rgba=np.dstack((np.asarray(crop),mask.astype(np.uint8)*255))
house=Image.fromarray(rgba);box=house.getchannel('A').getbbox();house=house.crop(box);house.save(A/'house-source.png')
report=dict(houseSource=source.as_posix(),houseSourceSha256=hashlib.sha256(source.read_bytes()).hexdigest(),sourceROI=roi,alphaBox=box,alphaMethod='Sky/grass color key plus enclosed windows. No forced black contour.',dragonSource='namek-likeness-study/porunga-anime-study.png',houseTarget=[58,32],dragonTarget=[57,80],sourceApproval='User accepts soft house outline and anime-based Porunga direction. Native result pending review.')
(A/'import.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report))
