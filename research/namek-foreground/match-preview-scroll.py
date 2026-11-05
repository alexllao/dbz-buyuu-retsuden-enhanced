from pathlib import Path
import json,subprocess
D=Path('work/namek-foreground-video');r=json.loads((D/'report.json').read_text());src=D/'source.mp4'
raw=subprocess.check_output(['ffmpeg','-hide_banner','-loglevel','error','-i',str(src),'-vf','crop=640:448:0:52,scale=320:224:flags=neighbor','-pix_fmt','gray','-f','rawvideo','pipe:1'])
size=320*224;assert len(raw)//size==r['frames'];ref=raw[:size];samples=[(x,y,ref[y*320+x]) for y in range(66,118,6) for x in range(16,305,8)];shifts=[]
for f in range(0,r['frames'],4):
 off=f*size;scores=[]
 for dx in range(-200,161):
  valid=[(x,y,value) for x,y,value in samples if 0<=x+dx<320]
  scores.append((sum(abs(raw[off+y*320+x+dx]-value) for x,y,value in valid)/len(valid),abs(dx),dx))
 previous=shifts[-1]['dx'] if shifts else 0
 best=min(x for x in scores if abs(x[2]-previous)<=48);shifts.append(dict(frame=f,dx=best[2],error=best[0]))
(D/'background-motion.json').write_text(json.dumps(shifts,indent=2)+'\n',encoding='utf-8');print('Matched background displacement',min(x['dx'] for x in shifts),max(x['dx'] for x in shifts),'mean error',sum(x['error'] for x in shifts)/len(shifts));print(shifts[::25])
