from pathlib import Path
import sys,json,subprocess,struct
abWhich=sys.argv[1];abRom=Path('work/namek-native')/('porunga-nodither' if abWhich=='before' else 'porunga')/'candidate.bin';abOut=Path('work/namek-native/dither-video')/abWhich;abOut.mkdir(parents=True,exist_ok=True)
s=Path('work/input-v2/record.py').read_text().split('try:\n for j,entry in enumerate(steps[:-1]):')[0].replace("rompath='work/input-v2/candidate.bin' if which=='after' else 'work/responsive-cancels-v1/candidate.bin'","rompath='"+abRom.as_posix()+"'").replace("if which=='after':",'if True:')
sys.argv=['record','after'];exec(compile(s,'native-dither-record-setup','exec'),globals());setup=Path('work/namek-simulation/runtime.py').read_text().split('def boot_stage',1)[1].split("if __name__=='__main__':")[0];exec('def boot_stage'+setup,globals());nativeRows=[];nativeProc=None

def tick(a=(),b=()):
 rawtick(a,b)
 if nativeProc:
  w,h,pitch,data=latest;nativeProc.stdin.write(b''.join(data[y*pitch:y*pitch+w*2] for y in range(h)));nativeRows.append(dict(p=st(P1),e=st(P2)))

def record_take(label,seq):
 global nativeProc,audio_file,nativeRows
 nativeRows=[];nativeProc=subprocess.Popen(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pixel_format','rgb565le','-video_size','320x224','-framerate',str(av.timing.fps),'-i','pipe:0','-an','-c:v','libx264','-crf','14','-preset','veryfast','-pix_fmt','yuv420p',str(abOut/(label+'-silent.mp4'))],stdin=subprocess.PIPE);audio_file=(abOut/(label+'.pcm')).open('wb')
 for a,b in seq:tick(a,b)
 nativeProc.stdin.close();assert nativeProc.wait()==0;nativeProc=None;audio_file.close();audio_file=None
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(abOut/(label+'-silent.mp4')),'-f','s16le','-ar','44100','-ac','2','-i',str(abOut/(label+'.pcm')),'-c:v','copy','-c:a','aac','-b:a','128k','-shortest','-movflags','+faststart',str(abOut/(label+'.mp4'))],check=True)
 (abOut/(label+'.json')).write_text(json.dumps(nativeRows));print('RECORDED NATIVE',abWhich,label,len(nativeRows),flush=True)
try:
 boot_stage(0,8);baseline=snap();fixture(280)
 old=json.loads(Path('work/namek-simulation/video/simulation/01-vuelo.json').read_text());record_take('01-vuelo',[(r['keys1'],r['keys2']) for r in old]);save_image(abOut/'flight-end.png')
 restore(baseline);fixture(32);old=json.loads(Path('work/namek-simulation/video/simulation/02-goku.json').read_text());record_take('02-goku',[(r['keys1'],r['keys2']) for r in old]);assert any(r['p']['program']==0xc04 for r in nativeRows);save_image(abOut/'combat-end.png')
 (abOut/'rom-sha256.txt').write_text(__import__('hashlib').sha256(rom).hexdigest())
finally:
 if nativeProc:nativeProc.stdin.close();nativeProc.wait()
 if audio_file:audio_file.close()
 core.retro_unload_game();core.retro_deinit()
