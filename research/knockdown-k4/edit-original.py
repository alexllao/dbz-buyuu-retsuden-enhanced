from pathlib import Path
import json,subprocess,hashlib
P=Path('work/knockdown-k4');O=Path('outputs/derribos-K4');fps=59.92274340431231;clips=[];cases=[]
for name in ['Goku','Cell']:
 paths=[P/f'comparison/original/{name}.mp4',P/f'comparison/long/after/{name}.mp4'];metrics=[]
 for label,path in zip(['Original','K4'],paths):
  r=json.loads(path.with_suffix('.json').read_text());hit=next(i for i,t in enumerate(r) if t['e']['hp']<r[0]['e']['hp']);wake=next(i for i,t in enumerate(r[hit:],hit) if t['e']['action']==21);move=next(i for i,t in enumerate(r) if i>wake and t['e']['action'] in [1,2,7,8] and t['e']['x']!=r[i-1]['e']['x']);settled=wake-1
  while settled>hit and r[settled-1]['e']['y']==448:settled-=1
  metrics.append(dict(variant=label,hit=hit,wake=wake,move=move,settled=settled,lyingSeconds=(wake-settled)/fps,totalSeconds=(move-hit)/fps))
 # Sin cambiar velocidad: alinear el primer contacto, manteniendo 10 frames previos.
 starts=[m['hit']-10 for m in metrics];n=min(300-s for s in starts)
 vf=';'.join(f'[{i}:v]trim=start_frame={s}:end_frame={s+n},setpts=PTS-STARTPTS,crop=640:448:0:52[v{i}]' for i,s in enumerate(starts))+';[v0][v1]hstack=inputs=2,pad=1280:570:0:122:color=0x10151c'
 for x,label,color,m in zip([15,655],['ROM ORIGINAL','ENHANCED - K4'],['white','0xf5c667'],metrics):
  vf+=",drawtext=fontfile='C\\:/Windows/Fonts/arialbd.ttf':text='"+label+f"':x={x}:y=10:fontsize=28:fontcolor={color}"
  vf+=",drawtext=fontfile='C\\:/Windows/Fonts/arial.ttf':text='"+name+f" - golpe a caminar {m['totalSeconds']:.2f} s':x={x}:y=50:fontsize=23:fontcolor=white"
 vf+=",drawtext=fontfile='C\\:/Windows/Fonts/arial.ttf':text='Derribo normal - mismo mando - sincronizado en el impacto - velocidad normal':x=15:y=88:fontsize=21:fontcolor=0xbecbd8[v]"
 vf+=f';[1:a]atrim=start={starts[1]/fps}:end={(starts[1]+n)/fps},asetpts=PTS-STARTPTS[a]'
 out=P/f'comparison/Original-vs-K4-{name}.mp4';args=['ffmpeg','-hide_banner','-loglevel','error','-y']
 for path in paths:args+=['-i',str(path)]
 args+=['-filter_complex',vf,'-map','[v]','-map','[a]','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-shortest',str(out)];subprocess.run(args,check=True);clips.extend([out.resolve()]*2);cases.append(dict(name=name,metrics=metrics,sourceTrimFrames=starts,alignedOn='First HP loss',sameControlSequence=True))
concat=P/'comparison/original-concat.txt';concat.write_text('\n'.join("file '"+str(p).replace('\\','/')+"'" for p in clips));movie=O/'ROM-original-vs-K4-derribos.mp4'
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(concat),'-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-r',str(fps),'-fps_mode','cfr','-c:a','aac','-movflags','+faststart',str(movie)],check=True)
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss','2.6','-i',str(movie),'-frames:v','1',str(O/'original-vs-K4.png')],check=True)
(P/'original-video-cases.json').write_text(json.dumps(dict(cases=cases,nativeFps=fps,gameplaySpeedScaling=False,eachCaseRepeated=2,audio='K4',originalRomSha256=hashlib.sha256(Path('work/rom/original.bin').read_bytes()).hexdigest(),k4RomSha256=hashlib.sha256((P/'candidate.bin').read_bytes()).hexdigest()),indent=2));print(cases)
