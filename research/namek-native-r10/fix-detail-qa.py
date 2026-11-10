from pathlib import Path
import sys,json
sys.path.insert(0,'work/simulation-deps')
from PIL import Image,ImageDraw,ImageFont
import numpy as np
from numpy.lib.stride_tricks import sliding_window_view
T=Path('work/namek-native-r10');OLD=Path('work/namek-native-r9');O=Path('outputs/Namek-R10-revision')
out=Image.new('RGB',(640,556),'#10151c');draw=ImageDraw.Draw(out);font=ImageFont.truetype('work/namek-three/arialbd.ttf',15)
items=[('VENTANA','normal','02-goku',(368,64,512,146),2,0),('NUBE Y ARBOL','porunga','01-vuelo',(320,80,640,288),1,190),('SUELO','porunga','01-vuelo',(344,344,496,388),2,426)]
for title,slug,label,box,scale,y in items:
 for i,(root,tag) in enumerate([(OLD,'ANTES R9'),(T,'AHORA R10')]):
  im=Image.open(root/'promo'/slug/(label+'-qa-0001.png')).convert('RGB').crop(box)
  if scale!=1:im=im.resize((im.width*scale,im.height*scale),Image.Resampling.NEAREST)
  draw.text((i*320+6,y+3),tag+' - '+title,font=font,fill='white');out.paste(im,(i*320,y+24))
out.save(O/'Correcciones-R9-R10-ROM.png')
bad=np.asarray(Image.open(T/'reported-stamp-R9-1x.png').convert('RGB'))
counts=[]
for root in [OLD,T]:
 im=np.asarray(Image.open(root/'promo/porunga/01-vuelo-qa-0001.png').convert('RGB').resize((320,224),Image.Resampling.NEAREST))
 w=sliding_window_view(im,(5,16),axis=(0,1));count=int((w==bad.transpose(2,0,1)).all((2,3,4)).sum());counts.append(count)
assert counts[0]>0 and counts[1]==0,counts
report=dict(matchedNativePose=True,oldRenderedStampCount=counts[0],newRenderedStampCount=counts[1],sourceFrames=['R9 porunga 01-vuelo frame1','R10 porunga 01-vuelo frame1'],integerCropsOnly=True)
(T/'detail-validation.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
