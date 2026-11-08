from pathlib import Path
import json,subprocess
P=Path('work/throw-links');O=Path('outputs/enlaces-lanzamiento-especial');O.mkdir(parents=True,exist_ok=True);fps=59.92274340431231;names=['Goku','Gohan','Piccolo','Vegeta','Trunks','Cell','A18','Krilin','Freezer','Recoome','Ginyu'];techs=['Kamehameha','Masenko','Special Beam Cannon','Final Flash','Burning Attack','Special Beam Cannon','Energy Flame','Kamehameha','Mega Buster','Eraser Gun','Terra Smash'];show=[];compare=[];cases=[]
def metrics(path):
 r=json.loads(path.with_suffix('.json').read_text());events=[dict(frame=i,damage=a['e']['hp']-t['e']['hp'],victimAction=t['e']['action'],y=t['e']['y']) for i,(a,t) in enumerate(zip(r,r[1:]),1) if t['e']['hp']<a['e']['hp']];return dict(damage=sum(x['damage'] for x in events),hits=max(t['p']['hits'] for t in r),events=events)
def concat(paths,out):
 f=P/'video'/(out.stem+'.txt');f.write_text('\n'.join("file '"+str(p.resolve()).replace('\\','/')+"'" for p in paths));subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(f),'-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-r',str(fps),'-fps_mode','cfr','-c:a','aac','-movflags','+faststart',str(out)],check=True)
for cid,name in enumerate(names):
 source=P/f'video/after/link-{name}.mp4';m=metrics(source);assert m['hits']==2 and len(m['events'])==2,(name,m)
 vf="trim=end_frame=380,setpts=PTS-STARTPTS,crop=640:448:0:52,scale=960:672:flags=neighbor,pad=960:800:0:128:color=0x10151c"
 vf+=",drawtext=fontfile='C\\:/Windows/Fonts/arialbd.ttf':text='"+name.upper()+' / LANZAMIENTO + '+techs[cid].upper()+"':x=15:y=10:fontsize=23:fontcolor=0xf5c667"
 vf+=",drawtext=fontfile='C\\:/Windows/Fonts/arial.ttf':text='"+f"{m['hits']} impactos reales - {m['damage']} dano total':x=15:y=46:fontsize=24:fontcolor=white"
 vf+=",drawtext=fontfile='C\\:/Windows/Fonts/arial.ttf':text='Rival sin botones - momento ajustado por personaje - velocidad normal':x=15:y=83:fontsize=20:fontcolor=0xbecbd8,drawtext=fontfile='C\\:/Windows/Fonts/arial.ttf':text='No todas las secuencias impiden defenderse; ver comparacion contra guardia':x=15:y=108:fontsize=17:fontcolor=0xbecbd8"
 out=P/f'video/show-{name}.mp4';subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),'-vf',vf,'-t',str(380/fps),'-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-c:a','aac',str(out)],check=True);show.append(out);cases.append(dict(cid=cid,name=name,technique=techs[cid],metrics=m))
def comparison(label,left,right,title,leftTitle,rightTitle,footer,frames):
 paths=[P/f'video/{left}.mp4',P/f'video/{right}.mp4'];mm=list(map(metrics,paths));vf=';'.join(f'[{i}:v]trim=end_frame={frames},setpts=PTS-STARTPTS,crop=640:448:0:52[v{i}]' for i in range(2))+';[v0][v1]hstack=inputs=2,pad=1280:578:0:130:color=0x10151c'
 for x,heading,m,color in zip([15,655],[leftTitle,rightTitle],mm,['white','0xf5c667']):
  vf+=",drawtext=fontfile='C\\:/Windows/Fonts/arialbd.ttf':text='"+heading+f"':x={x}:y=10:fontsize=24:fontcolor={color}"
  vf+=",drawtext=fontfile='C\\:/Windows/Fonts/arial.ttf':text='"+f"{m['damage']} dano - {m['hits']} impactos':x={x}:y=48:fontsize=23:fontcolor=white"
 vf+=",drawtext=fontfile='C\\:/Windows/Fonts/arial.ttf':text='"+title+"':x=15:y=85:fontsize=21:fontcolor=white,drawtext=fontfile='C\\:/Windows/Fonts/arial.ttf':text='"+footer+"':x=15:y=110:fontsize=17:fontcolor=0xbecbd8[v]"
 out=P/f'video/compare-{label}.mp4';subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(paths[0]),'-i',str(paths[1]),'-filter_complex',vf,'-map','[v]','-map','1:a','-t',str(frames/fps),'-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-c:a','aac',str(out)],check=True);compare.append(out);cases.append(dict(label=label,metrics=mm,source=[left,right]))
for name in ['Goku','Krilin']:comparison('fix-'+name,'before/fix-'+name,'after/early-'+name,name.upper()+' - ESPECIAL DEMASIADO PRONTO - DANO DEL LANZAMIENTO','ANTES - DANO MEZCLADO','CORREGIDO - DANO PROPIO','Mismo comando y momento; el especial que no conecta no debe cambiar el dano del lanzamiento',300)
for name in ['Goku','Gohan','Vegeta']:comparison('timing-'+name,'after/early-'+name,'after/link-'+name,name.upper()+' - MOMENTO DE EJECUTAR EL ESPECIAL','DEMASIADO PRONTO','ENLACE BIEN MEDIDO','Ambas tomas con la correccion - diferentes momentos del mando - velocidad normal',380)
comparison('guard','after/guard-Goku-timed','after/guard-Goku-late','GOKU - EL RIVAL MANTIENE ATRAS EN AMBAS TOMAS','VENTANA AJUSTADA','TARDE - PUEDE BLOQUEAR','El especial bloqueado reduce dano y no suma otro HIT - no se fabrican contactos',460)
concat(show,O/'Lanzamiento-a-especial-once-personajes.mp4');concat(compare,O/'Lanzamiento-especial-tiempo-dano-y-defensa.mp4');(P/'video-cases.json').write_text(json.dumps(cases,indent=2))
for n,t in [('Lanzamiento-a-especial-once-personajes',4),('Lanzamiento-especial-tiempo-dano-y-defensa',3)]:subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss',str(t),'-i',str(O/(n+'.mp4')),'-frames:v','1',str(O/(n+'.png'))],check=True)
print('VIDEOS READY',flush=True)
