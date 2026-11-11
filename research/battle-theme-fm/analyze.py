from pathlib import Path
import os,sys,json
os.environ['OPENBLAS_NUM_THREADS']='2';sys.path.insert(0,'work/simulation-deps')
import numpy as np
P=Path('work/battle-theme-fm');sr=22050;hop=256;nfft=4096
x=np.fromfile(P/'source.f32',dtype='<f4');x=np.pad(x,(nfft//2,nfft//2));frames=np.lib.stride_tricks.sliding_window_view(x,nfft)[::hop]
V=np.abs(np.fft.rfft(frames*np.hanning(nfft),axis=1)).T.astype(np.float32)
# Mascara armonica: extraer notas sostenidas y medir percusion aparte.
H=np.empty_like(V)
for start in range(0,len(V),128):
 block=np.pad(V[start:start+128],((0,0),(8,8)),mode='edge')
 H[start:start+128]=np.median(np.lib.stride_tricks.sliding_window_view(block,17,axis=1),axis=2)
per=np.median(np.lib.stride_tricks.sliding_window_view(np.pad(V,((8,8),(0,0)),mode='edge'),17,axis=0),axis=2)
mask=H**2/(H**2+per**2+1e-9);harm=V*mask
notes=np.arange(36,97);freq=np.fft.rfftfreq(nfft,1/sr);W=np.zeros((len(freq),len(notes)),np.float32)
for j,note in enumerate(notes):
 f0=440*2**((note-69)/12)
 for h in range(1,10):
  f=f0*h
  if f>9000:break
  W[:,j]+=np.exp(-0.5*((freq-f)/(sr/nfft*1.1))**2)/h**1.3
whiten=1/(np.mean(harm,axis=1)+0.2)**0.40;whiten[freq<40]=0;whiten[freq>9000]=0
W*=whiten[:,None];W/=np.linalg.norm(W,axis=0,keepdims=True)+1e-9
target=np.sqrt(harm)*whiten[:,None];B=W.T@target;G=W.T@W
A=np.maximum(B,1e-4)
for _ in range(85):A*=B/(G@A+1e-5)
def track(lo,hi,penalty):
 ids=np.flatnonzero((notes>=lo)&(notes<=hi));a=A[ids];obs=np.log(a+np.max(a)*0.015)
 obs-=obs.max(axis=0,keepdims=True)
 trans=-np.abs(notes[ids,None]-notes[None,ids])*penalty
 dp=obs[:,0];back=np.empty((len(ids),a.shape[1]),np.int16);back[:,0]=0
 for t in range(1,a.shape[1]):
  scores=dp[:,None]+trans;back[:,t]=scores.argmax(axis=0);dp=scores.max(axis=0)+obs[:,t]
 path=np.empty(a.shape[1],int);path[-1]=dp.argmax()
 for t in range(len(path)-2,-1,-1):path[t]=back[path[t+1],t+1]
 return notes[ids[path]],a[path,np.arange(len(path))]
lead,leadpower=track(57,88,0.24);bass,basspower=track(36,59,0.30)
fps=59.92274340431231;count=round(25*fps);times=np.arange(count)/fps;idx=np.minimum(np.round(times*sr/hop).astype(int),A.shape[1]-1)
level=np.sqrt(np.mean(frames**2,axis=1));levelAt=level[idx];voices=[];lastpad=[60,64,67]
for t,k in enumerate(idx):
 mel=int(lead[k]);low=int(bass[k]);a=A[:,k].copy();pads=[]
 a[(notes<48)|(notes>83)]=0
 for n in [mel,low]:a[(notes%12)==(n%12)]=0
 for _ in range(3):
  best=int(a.argmax());v=int(notes[best]);strength=float(a[best]);pads.append(v if strength>np.max(A[:,k])*.12 else -1);a[(notes%12)==(v%12)]=0
 # Ordenar voces para reducir saltos de asignacion entre acordes.
 pads=sorted(pads)
 active=levelAt[t]>max(float(levelAt.max())*.025,.001)
 voices.append([mel,low,*pads] if active else [-1]*5)
voices=np.asarray(voices,int)
# Eliminar cambios aislados de un unico fotograma, conservando notas articuladas.
for ch in range(5):
 for t in range(1,count-1):
  if voices[t-1,ch]==voices[t+1,ch] and voices[t,ch]!=voices[t-1,ch]:voices[t,ch]=voices[t-1,ch]
def onsets(lo,hi,percentile,gap):
 band=V[(freq>=lo)&(freq<hi)];flux=np.maximum(np.diff(band,axis=1,prepend=band[:,:1]),0).sum(axis=0);q=flux[idx]
 events=[];last=-100
 threshold=np.percentile(q,percentile)
 for t in range(2,count-2):
  if t-last>=gap and q[t]>threshold and q[t]>=q[t-1] and q[t]>=q[t+1]:events.append(t);last=t
 return events
kick=onsets(40,160,86,10);snare=onsets(250,3200,91,9);hat=onsets(5500,10000,89,5)
score=dict(seconds=25,fps=fps,voices=voices.tolist(),kick=kick,snare=snare,hat=hat,analysis='Automatic harmonic transcription draft; five pitched FM parts and one FM kick, PSG noise percussion. Requires listening and manual musical refinement; not a note-perfect arrangement.',sourceOffset=0,sourceSeconds=92.238367)
(P/'score.json').write_text(json.dumps(score,indent=1));np.savez_compressed(P/'analysis.npz',activation=A,notes=notes,lead=lead,bass=bass,frameTimes=np.arange(A.shape[1])*hop/sr)
print('Frames',count,'percussion',len(kick),len(snare),len(hat),'lead',sorted(zip(*np.unique(voices[:,0],return_counts=True)),key=lambda t:-t[1])[:8])
