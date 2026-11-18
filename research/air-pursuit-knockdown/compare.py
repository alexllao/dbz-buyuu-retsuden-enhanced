from pathlib import Path
import json,subprocess,hashlib
P=Path('work/air-pursuit-knockdown');D=P/'compare';O=Path('outputs/Recuperacion-K4-Combos-Aereos')
for p in [D,O]:p.mkdir(parents=True,exist_ok=True)
fps=59.92274340431231;cases=[];jobs=[]
def draw(vf,key,text,x,y,size,color='white'):
 p=D/(key+'.txt');p.write_text(text,encoding='utf-8');escaped=p.resolve().as_posix().replace(':','\\:')
 return vf+f",drawtext=fontfile='work/namek-three/arialbd.ttf':textfile='{escaped}':x={x}:y={y}:fontsize={size}:fontcolor={color}"
for index,(name,title) in enumerate([('01-goku-kame','GOKU / KAMEHAMEHA'),('02-vegeta-flash','VEGETA / FINAL FLASH'),('05-goku-super','GOKU / SUPER KAMEHAMEHA')]):
 before=Path('work/air-pursuit-landing-sfx/captures-ki')/(name+'.mp4');after=P/'captures-ki'/(name+'.mp4');a=json.loads(before.with_suffix('.json').read_text());b=json.loads(after.with_suffix('.json').read_text())
 hit=max(i for i in range(1,len(b)) if b[i]['e']['hp']<b[i-1]['e']['hp'])
 wake=next(t['f'] for t in b[hit:] if t['e']['program'] in [0xbf,0xc0,0xc1,0xc2]);settled=1+max(t['f'] for t in b[hit:wake] if t['e']['y']<448);idle=next(t['f'] for t in b[wake:] if t['e']['program'] not in [0xbf,0xc0,0xc1,0xc2])
 beforeLanding=next(i for i in range(hit+1,len(a)) if a[i-1]['e']['y']<448 and a[i]['e']['y']==448)
 assert a[beforeLanding]['e']['program']==0 and b[beforeLanding]['e']['action'] in [0x13,0x14,0x15,0x16]
 assert wake-settled>=24 and idle<330 and a[-1]['e']['hp']==b[-1]['e']['hp']
 n=330;duration=n/fps
 vf=f'[0:v]trim=start_frame=0:end_frame={n},setpts=PTS-STARTPTS,scale=640:448:flags=neighbor[l];[1:v]trim=start_frame=0:end_frame={n},setpts=PTS-STARTPTS,scale=640:448:flags=neighbor[r];[l][r]hstack=inputs=2,pad=1280:576:0:80:color=0x0b1520'
 vf=draw(vf,f'{index}-title',title,20,8,25,'0xffd46b');vf=draw(vf,f'{index}-before','ANTES / RECUPERACION INSTANTANEA',20,46,21);vf=draw(vf,f'{index}-after','AHORA / DERRIBO Y ESPERA K4',660,46,21,'0xffd46b')
 vf=draw(vf,f'{index}-footer','ROM REAL / MISMA VELOCIDAD / SE CONSERVAN REBOTE, ESPERA E INCORPORACION',20,543,21,'0xc8d9dd')
 vf+=f'[v];[1:a]atrim=start=0:end={duration},asetpts=PTS-STARTPTS[a]'
 target=D/f'{index:02}.mp4';subprocess.run(['ffmpeg','-v','error','-y','-filter_complex_threads','1','-i',str(before),'-i',str(after),'-filter_complex',vf,'-map','[v]','-map','[a]','-r',str(fps),'-c:v','libx264','-preset','veryfast','-threads','2','-crf','17','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k',str(target)],check=True);jobs.append(target)
 cases.append(dict(label=name,firstGroundBefore=beforeLanding,settled=settled,wake=wake,endGetup=idle,waitFrames=wake-settled,waitSeconds=(wake-settled)/fps,beforeSha256=hashlib.sha256(before.read_bytes()).hexdigest(),afterSha256=hashlib.sha256(after.read_bytes()).hexdigest()))
listing=D/'concat.txt';listing.write_text('\n'.join("file '"+j.resolve().as_posix()+"'" for j in jobs),encoding='utf-8');target=O/'Antes-despues-recuperacion-K4.mp4'
subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',str(listing),'-c','copy','-movflags','+faststart',str(target)],check=True);subprocess.run(['ffmpeg','-v','error','-i',str(target),'-f','null','-'],check=True)
for index,second in enumerate([3.7,9.2,14.8]):subprocess.run(['ffmpeg','-v','error','-y','-ss',str(second),'-i',str(target),'-frames:v','1',str(O/f'Comparacion-{index+1}.png')],check=True)
manifest=dict(build=json.loads((P/'build.json').read_text()),cases=cases,fps=fps,frames=990,seconds=990/fps,normalSpeed=True,gameplayUnaltered=True,sourceFormat='Direct native ROM framebuffer and audio; initial spacing/facing before capture only.',audio='After only',file=str(target.resolve()),sha256=hashlib.sha256(target.read_bytes()).hexdigest())
(O/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8');(P/'recovery-validation.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8');print(cases,flush=True)
