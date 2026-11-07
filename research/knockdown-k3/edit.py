from pathlib import Path
import json,subprocess
P=Path('work/knockdown-k3');O=Path('outputs/derribos-K3');O.mkdir(exist_ok=True,parents=True);fps=59.92274340431231;clips=[];cases=[]
for name in ['Goku','Cell']:
 sourcePaths=[Path(f'work/knockdown-k2/comparison/before/{name}.mp4'),Path(f'work/knockdown-k2/comparison/after/{name}.mp4'),P/f'comparison/after/{name}.mp4'];sources=[json.loads(p.with_suffix('.json').read_text()) for p in sourcePaths];report=[]
 for label,r in zip(['K1','K2','K3'],sources):
  hit=next(i for i,t in enumerate(r) if t['e']['hp']<r[0]['e']['hp']);w=next(i for i,t in enumerate(r[hit:],hit) if t['e']['action']==21);idle=next(i for i,t in enumerate(r[w:],w) if t['e']['program']==0);move=next(i for i,t in enumerate(r[hit+1:],hit+1) if t['e']['action'] in [1,2,7,8] and t['e']['x']!=r[i-1]['e']['x']);report.append(dict(variant=label,hit=hit,wake=w,idle=idle,movement=move,getupSeconds=(idle-w)/fps,totalSeconds=(move-hit)/fps,damage=r[0]['e']['hp']-r[-1]['e']['hp']))
 w=report[0]['wake'];same=all(x['wake']==w for x in report) and all(all(all(a['e'][k]==b['e'][k] for k in ['program','cursor','x','y','hp']) for a,b in zip(sources[0][:w+1],r[:w+1])) for r in sources[1:]);assert same;cases.append(dict(name=name,identicalThroughWakeStart=same,comparison=report))
 full=P/'comparison'/('full-'+name+'.mp4');vf="[0:v]crop=640:448:0:52[l];[1:v]crop=640:448:0:52[r];[l][r]hstack=inputs=2,pad=1440:696:80:150:color=0x10151c,drawtext=fontfile='C\\:/Windows/Fonts/arialbd.ttf':text='K2 - INTERMEDIA':x=95:y=15:fontsize=25:fontcolor=white,drawtext=fontfile='C\\:/Windows/Fonts/arialbd.ttf':text='K3 - INCORPORACION ORIGINAL':x=735:y=15:fontsize=25:fontcolor=0xf5c667,drawtext=fontfile='C\\:/Windows/Fonts/arial.ttf':text='"+name+" - misma caida y espera - despues detalle ampliado de K1 K2 K3':x=95:y=60:fontsize=22:fontcolor=white[v]"
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(sourcePaths[1]),'-i',str(sourcePaths[2]),'-filter_complex',vf,'-map','[v]','-map','1:a','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-shortest',str(full)],check=True);clips.append(full.resolve())
 start=w-6;n=max(x['idle'] for x in report)+20-start;detail=P/'comparison'/('detail-'+name+'.mp4')
 vf=';'.join(f'[{i}:v]trim=start_frame={start}:end_frame={start+n},setpts=PTS-STARTPTS,crop=240:300:400:200,scale=480:600:flags=neighbor[v{i}]' for i in range(3))+';[v0][v1][v2]hstack=inputs=3,pad=1440:696:0:96:color=0x10151c'
 for x,label,color in [(15,'K1 - RAPIDA','white'),(495,'K2 - INTERMEDIA','white'),(975,'K3 - ORIGINAL','0xf5c667')]:vf+=",drawtext=fontfile='C\\:/Windows/Fonts/arialbd.ttf':text='"+label+"':x="+str(x)+":y=8:fontsize=25:fontcolor="+color
 title=name+' - incorporacion '+ ' / '.join(f"{x['getupSeconds']:.2f} s" for x in report)
 vf+=",drawtext=fontfile='C\\:/Windows/Fonts/arial.ttf':text='"+title+"':x=15:y=43:fontsize=21:fontcolor=white,drawtext=fontfile='C\\:/Windows/Fonts/arial.ttf':text='Detalle ampliado - repetido 4 veces - velocidad normal':x=15:y=70:fontsize=18:fontcolor=0xbecbd8[v]"
 vf+=f';[2:a]atrim=start={start/fps}:end={(start+n)/fps},asetpts=PTS-STARTPTS[a]'
 args=['ffmpeg','-hide_banner','-loglevel','error','-y']
 for p in sourcePaths:args+=['-i',str(p)]
 args+=['-filter_complex',vf,'-map','[v]','-map','[a]','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-shortest',str(detail)];subprocess.run(args,check=True);clips += [detail.resolve()]*4
(P/'comparison/concat.txt').write_text('\n'.join("file '"+str(t).replace('\\','/')+"'" for t in clips));out=O/'Incorporacion-K1-K2-K3-detalle-y-juego.mp4';subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(P/'comparison/concat.txt'),'-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-r',str(fps),'-fps_mode','cfr','-c:a','aac','-movflags','+faststart',str(out)],check=True);(P/'video-cases.json').write_text(json.dumps(cases,indent=2));print(out,cases,flush=True)
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss','4.0','-i',str(out),'-frames:v','1',str(O/'comparacion.png')],check=True)
