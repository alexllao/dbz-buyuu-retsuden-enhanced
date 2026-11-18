from pathlib import Path
import sys,json,subprocess,hashlib
setup=Path('work/combo-charge-all/runtime.py').read_text().replace('work/combo-charge-all/candidate.bin','work/air-recovery/candidate.bin')
sys.argv=['record','after'];exec(compile(setup,'defense-record-runtime','exec'),globals());exec(compile(Path('work/air-recovery/recovery-sequences.py').read_text(),'defense-sequences','exec'),globals())
sys.path.insert(0,str(Path('work/namek-native-r10').resolve()));from resource_check import inspect
O=Path('work/air-recovery/captures');O.mkdir(parents=True,exist_ok=True);writer=None;reports=[];checks=[]
def tick(a=(),b=()):
 rawtick(a,b);w,h,pitch,data=latest;assert (w,h)==(320,224)
 writer.stdin.write(b''.join(data[y*pitch:y*pitch+w*2] for y in range(h)))
 rows.append(dict(f=len(rows),attacker=st(AP),defender=st(DP),aPhase=rb(AS),dPhase=rb(DS),airHits=rb(AS+2),used=rb(DS+0x2a),window=rb(DS+0x2b),pose=rb(DP+4),keys=list(a),keys2=list(b),stage=rb(0xe741),variant=rb(0xf7c0)))
 if len(rows) in [60,85,95,110,125,150,180,210,240,270,300,330]:save_image(O/f'{label}-{len(rows):03}.png')
 if rb(DS)==6 and not any(c['label']==label+'-recover' for c in checks):checks.append(inspect(snap(),Path('work/namek-native-r10'),slug,label+'-recover'))
try:
 for label,cid,slug,side,port in [('01-goku-escape',0,'normal',0,1),('02-vegeta-escape',3,'porunga',1,1),('03-goku-escape',0,'porunga',1,2),('04-vegeta-escape',3,'normal',0,2)]:
  prep_recovery(cid,side,port,slug);checks.append(inspect(snap(),Path('work/namek-native-r10'),slug,label+'-start'))
  writer=subprocess.Popen(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pixel_format','rgb565le','-video_size','320x224','-framerate',str(fps),'-i','pipe:0','-an','-c:v','libx264','-preset','veryfast','-threads','2','-crf','16','-pix_fmt','yuv420p',str(O/(label+'-silent.mp4'))],stdin=subprocess.PIPE)
  audio_file=(O/(label+'.pcm')).open('wb');r=run_recovery(cid,side,port,slug,prepared=True)
  writer.stdin.close();assert writer.wait()==0;writer=None;audio_file.close();audio_file=None
  capturePath=O/(label+'.mp4')
  subprocess.run(['ffmpeg','-v','error','-y','-i',str(O/(label+'-silent.mp4')),'-f','s16le','-ar',str(round(av.timing.sample_rate)),'-ac','2','-i',str(O/(label+'.pcm')),'-c:v','copy','-c:a','aac','-b:a','160k','-shortest','-movflags','+faststart',str(capturePath)],check=True)
  (O/(label+'.json')).write_text(json.dumps(rows));r.update(label=label,romSha256=hashlib.sha256(rom).hexdigest(),videoSha256=hashlib.sha256(capturePath.read_bytes()).hexdigest(),lastCounterContact=max(i for i in range(1,len(rows)) if rows[i]['attacker']['hp']<rows[i-1]['attacker']['hp']))
  reports.append(r);print(r,flush=True)
 (O/'manifest.json').write_text(json.dumps(dict(romSha256=hashlib.sha256(rom).hexdigest(),fps=fps,takes=reports,resources=checks,method='Native ROM framebuffer/audio. Scripted human ports, native menu seeds. Only spacing/facing before a take; no position, HP, KI, action, palette or timer writes during capture.'),indent=2))
finally:
 if writer:writer.stdin.close();writer.wait()
 if audio_file:audio_file.close()
 core.retro_unload_game();core.retro_deinit()
