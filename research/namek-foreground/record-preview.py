from pathlib import Path
import sys,json,subprocess,struct,hashlib
sys.argv=['record','0','foreground-demo']
s=Path('work/hits-hud-v3/record.py').read_text(encoding='utf-8').split('try:\n restore',1)[0]
exec(compile(s,'record-setup','exec'),globals())
D=Path('work/namek-foreground-video');D.mkdir(exist_ok=True)
oldrun=run
def run(a=(),b=()):
 oldrun(a,b);trace[-1].update(wordE722=rw(0xe722),diagnosticWords=[rw(a) for a in range(0xe6d0,0xe75e,2)])
try:
 restore((out/'charged.state').read_bytes());ww(P1+0xa,300);ww(P2+0xa,332);ww(P1+0xc,0);ww(P2+0xc,0);wb(P1+0x59,0);wb(P2+0x59,1)
 for _ in range(60):tick()
 vf="scale=640:448:flags=neighbor,pad=640:500:0:52:color=0x10151c"
 encoder=subprocess.Popen(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pixel_format','rgb565le','-video_size','320x224','-framerate',str(av.timing.fps),'-i','pipe:0','-vf',vf,'-an','-c:v','libx264','-crf','18','-pix_fmt','yuv420p',str(D/'silent.mp4')],stdin=subprocess.PIPE)
 audio_file=(D/'audio.pcm').open('wb');trace=[];phase='reposo';idle(60)
 basic_chain('AAA');phase='recuperacion';idle(40)
 phase='desplazamiento-izquierda'
 for _ in range(85):run(['LEFT'],['LEFT'])
 phase='pausa';idle(30)
 phase='desplazamiento-derecha'
 for _ in range(55):run(['RIGHT'],['RIGHT'])
 phase='pausa';idle(25)
 close_to(30);basic_chain('BAB');phase='recuperacion';idle(90)
 cross();phase='final';idle(75)
 audio_file.close();audio_file=None;encoder.stdin.close();assert encoder.wait()==0;encoder=None
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(D/'silent.mp4'),'-f','s16le','-ar',str(round(av.timing.sample_rate)),'-ac','2','-i',str(D/'audio.pcm'),'-c:v','copy','-c:a','aac','-b:a','160k','-movflags','+faststart',str(D/'source.mp4')],check=True)
 report=dict(romSha256=hashlib.sha256(rom).hexdigest(),stage=stage,frames=len(trace),fps=av.timing.fps,wordE722Range=[min(x['wordE722'] for x in trace),max(x['wordE722'] for x in trace)],damage=trace[0]['e']['hp']-trace[-1]['e']['hp'],fixture='Native HITSv3 stage6; real two-pad walking, basic attacks and cross. Snapshot cold-prepared, initial spacing/facing only. No state writes during capture. Tree not in ROM.',trace=trace)
 (D/'report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(report['frames'],report['wordE722Range'],report['damage'])
finally:
 if audio_file:audio_file.close()
 if encoder:encoder.stdin.close();encoder.wait()
 core.retro_unload_game();core.retro_deinit()
