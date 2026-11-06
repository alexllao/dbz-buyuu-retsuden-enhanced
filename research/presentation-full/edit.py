from pathlib import Path
import subprocess,json,hashlib
P=Path('work/presentation-full');O=Path('outputs/presentacion-completa-v1.0');O.mkdir(parents=True,exist_ok=True)
old=Path('work/piccolo-hits/video');fresh=P/'video';sha=lambda b:hashlib.sha256(b).hexdigest()
plan=[
 (fresh,'title','ALEX LLAO','PRESENTA'),(fresh,'intro','BUYUU RETSUDEN','MEGA DRIVE / GENESIS'),
 (fresh,'aura-0','GOKU','ENERGIA'),(old,'02 combo cruce meteor','GOKU','COMBO / CRUCE / METEOR'),
 (fresh,'combo-3-ABA-meteor','VEGETA','CADENA / CRUCE / METEOR'),(fresh,'special-4','TRUNKS','BURNING ATTACK'),
 (fresh,'combo-0-AAB-flurry','GOKU','PUNOS / PATADAS / REMATE'),(fresh,'combo-1-ABA-masenko','GOHAN','COMBO / MASENKO'),
 (fresh,'aura-2','PICCOLO','ENERGIA'),(old,'06 piccolo meteor','PICCOLO','METEOR'),
 (fresh,'special-6','ANDROIDE 18','ENERGY FLAME'),(old,'11 cruces y meteor','DOS JUGADORES','CRUCES RAPIDOS / METEOR'),
 (fresh,'special-7','KRILIN','KAMEHAMEHA'),(fresh,'combo-0-ABA-kame','GOKU','CADENA / KAMEHAMEHA'),
 (fresh,'aura-8','FREEZER','ENERGIA'),(fresh,'special-8','FREEZER','MEGA BUSTER'),
 (old,'07 lanzamiento masenko','GOHAN','LANZAMIENTO / MASENKO'),(fresh,'special-9','RECOOME','ERASER GUN'),
 (fresh,'combo-0-ABB-super','GOKU','COMBO / SUPER KAMEHAMEHA'),(fresh,'aura-10','GINYU','ENERGIA'),
 (fresh,'special-10','GINYU','TERRA SMASH'),(fresh,'combo-0-BAB-meteor','GOKU','COMBO / CRUCE / METEOR'),
 (old,'05 vegeta meteor','VEGETA','METEOR'),(fresh,'gohan-meteor','GOHAN','METEOR'),
 (old,'08 lanzamiento final flash','VEGETA','LANZAMIENTO / FINAL FLASH'),(old,'03 rafaga tres impactos','GOKU','TRES PROYECTILES'),
 (fresh,'aura-6','ANDROIDE 18','ENERGIA'),(fresh,'p2-crosses-meteor','GOHAN Y GOKU','CRUCES / RESPUESTA DE P2'),
 (old,'09 lanzamiento kamehameha','GOKU','LANZAMIENTO / KAMEHAMEHA'),(fresh,'combo-5-ABA-meteor','CELL','COMBO / CRUCE / NEEDLE RUSH'),
 (old,'12 cierre','EN DESARROLLO','ALEX LLAO')]
romsha=sha(Path('work/piccolo-hits/candidate.bin').read_bytes());assert romsha=='d3ea94bb78553b545b1db56da8e67a87b69ca8fa67621b6597a31b5ec75e813a'
fps=59.92274340431231;chapters=[];edited=[];elapsed=0
def draw(s,x,y,size,color='white',bold=True):
 font='arialbd.ttf' if bold else 'arial.ttf'
 return ",drawtext=fontfile='C\\:/Windows/Fonts/"+font+"':text='"+s+f"':x={x}:y={y}:fontsize={size}:fontcolor={color}"
for i,(folder,label,name,action) in enumerate(plan):
 if label.startswith('aura-'):continue
 source=folder/(label+'.mp4');trace=json.loads((folder/(label+'.json')).read_text());end=len(trace)
 damageFrames=[j for j,(a,b) in enumerate(zip(trace,trace[1:]),1) if b['p']['hp']<a['p']['hp'] or b['e']['hp']<a['e']['hp']]
 if damageFrames:
  last=damageFrames[-1]
  # Keep the complete finish and landing; omit prolonged idle/dizzy waiting.
  for j in range(last+30,len(trace)):
   t=trace[j]
   if all(t[k]['program']<0x400 and t[k]['y']==448 for k in ['p','e']) and (t['p']['action']<=8 or t['e']['action']<=8):
    end=min(len(trace),j+30);break
 if label.startswith('aura-'):end=64
 vf=f"trim=end_frame={end},setpts=PTS-STARTPTS,crop=640:448:0:52,scale=960:672:flags=neighbor,pad=1280:720:160:24:color=0x0b1018"
 vf+=draw('DRAGON BALL Z  /  BUYUU RETSUDEN ENHANCED','(w-tw)/2',3,18)
 vf+=draw(name+'  /  MOD DE ALEX LLAO  /  V1.0','(w-tw)/2',697,16,'0xf5c667')
 for j,w in enumerate(action.split(' / ')):
  lines=w.split(' ') if len(w)>13 else [w]
  for k,line in enumerate(lines):vf+=draw(line,12,275+j*70+k*23,15,'0xf5c667')
 for j,line in enumerate(['JUEGO REAL','VELOCIDAD','NORMAL']):vf+=draw(line,1130,290+j*26,14,'0xbac6d5')
 seconds=end/fps;af=f'atrim=duration={seconds},asetpts=PTS-STARTPTS,afade=t=in:d=0.035,afade=t=out:st={max(0,seconds-.1)}:d=0.1'
 dest=P/f'edit-{i:02}.mp4'
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),'-vf',vf,'-af',af,'-c:v','libx264','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k',str(dest)],check=True)
 clip=dict(index=i,label=label,character=name,action=action,startSeconds=elapsed,frames=end,sourceFrames=len(trace),seconds=seconds,maxHitsP1=max(t['p']['hits'] for t in trace[:end]),maxHitsP2=max(t['e']['hits'] for t in trace[:end]),damageP1=trace[0]['p']['hp']-trace[end-1]['p']['hp'],damageP2=trace[0]['e']['hp']-trace[end-1]['e']['hp'],source=str(source),traceSha256=sha((folder/(label+'.json')).read_bytes()))
 chapters.append(clip);edited.append(dest.resolve());elapsed+=seconds;print('EDIT',i,label,round(seconds,2),flush=True)
(P/'concat.txt').write_text('\n'.join("file '"+str(t).replace('\\','/')+"'" for t in edited),encoding='utf8')
output=O/'DBZ-Buyuu-Retsuden-Enhanced-Presentacion-completa-v1.0.mp4'
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(P/'concat.txt'),'-c','copy','-movflags','+faststart',str(output)],check=True)
report=dict(romSha256=romsha,version='1.0',buildId='20261106-105411',romChanged=False,nativeAudio=True,nativeHitsHud=True,gameplayTimeScaling=False,seconds=elapsed,chapters=chapters,video=dict(path='assets/media/presentation-full/'+output.name,sha256=sha(output.read_bytes())),staging='Real emulator footage with scripted human ports. Positions prepared before capture; ki charged natively; critical HP earned by taking actual hits before capture. Cuts may omit prolonged recovery/dizzy waiting, never speed up attacks. No authored hit overlays or extra damage.')
(P/'presentation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss','12','-i',str(output),'-frames:v','1',str(O/'captura.png')],check=True)
print('PRESENTATION',elapsed,'seconds',output,flush=True)
