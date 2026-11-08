from pathlib import Path
import subprocess,json
P=Path('work/combo-startup');O=Path('outputs/Especiales-rapidos-en-combo');O.mkdir(exist_ok=True,parents=True);fps=59.92274340431231;clips=[]
metrics={v:{t['name']+'-'+t['context']:t for t in json.loads((P/f'video/{v}/metrics.json').read_text())} for v in ['before','after']}
for name,context,title in [('Gohan','combo','MASENKO ENLAZADO A TRES BASICOS'),('Vegeta','combo','FINAL FLASH ENLAZADO A TRES BASICOS'),('Gohan','solo','MASENKO SUELTO - PREPARACION NATIVA'),('Vegeta','solo','FINAL FLASH SUELTO - PREPARACION NATIVA')]:
 label=name+'-'+context;paths=[P/f'video/{v}/{label}.mp4' for v in ['before','after']];a,b=[metrics[v][label] for v in ['before','after']]
 start=0 if context=='combo' else max(0,a['accepted']-8);frames=220 if context=='combo' else 175
 vf=';'.join(f'[{i}:v]trim=start_frame={start}:end_frame={start+frames},setpts=PTS-STARTPTS,crop=640:448:0:52[v{i}]' for i in range(2))+';[v0][v1]hstack=inputs=2,pad=1280:590:0:142:color=0x10151c'
 for x,heading,m in [(15,'ANTES',a),(655,'PRUEBA NUEVA',b)]:
  vf+=",drawtext=fontfile='C\\:/Windows/Fonts/arialbd.ttf':text='"+heading+f"':x={x}:y=12:fontsize=26:fontcolor=white"
  caption=f"Preparacion {m['startup']} f / {m['startup']/fps:.2f} s"
  vf+=",drawtext=fontfile='C\\:/Windows/Fonts/arial.ttf':text='"+caption+f"':x={x}:y=48:fontsize=24:fontcolor=0xffd35a"
 vf+=",drawtext=fontfile='C\\:/Windows/Fonts/arialbd.ttf':text='"+title+"':x=15:y=87:fontsize=22:fontcolor=white,drawtext=fontfile='C\\:/Windows/Fonts/arial.ttf':text='Mismo mando y ritmo / velocidad normal / poses de lanzamiento y proyectil nativos':x=15:y=117:fontsize=18:fontcolor=0xcbd6e4[v]"
 vf+=f';[1:a]atrim=start={start/fps}:end={(start+frames)/fps},asetpts=PTS-STARTPTS[a]'
 out=P/f'video/comparison-{label}.mp4';subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(paths[0]),'-i',str(paths[1]),'-filter_complex',vf,'-map','[v]','-map','[a]','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-t',str(frames/fps),str(out)],check=True);clips.extend([out.resolve()]*(2 if context=='combo' else 1))
lst=P/'video/comparison-concat.txt';lst.write_text('\n'.join("file '"+str(p).replace('\\','/')+"'" for p in clips));out=O/'Gohan-Vegeta-especiales-en-combo-antes-despues.mp4'
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(lst),'-c','copy','-movflags','+faststart',str(out)],check=True)
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss',str(100/fps),'-i',str(out),'-frames:v','1',str(O/'comparacion.png')],check=True);print('Video listo',out)
