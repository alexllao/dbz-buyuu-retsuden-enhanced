from pathlib import Path
import sys,json,subprocess,hashlib
setup=Path('work/combo-charge-all/runtime.py').read_text().replace('work/combo-charge-all/candidate.bin','work/air-pursuit-fall/candidate.bin')
sys.argv=['record','after'];exec(compile(setup,'air-record-runtime','exec'),globals());exec(compile(Path('work/air-pursuit-fall/sequences.py').read_text(),'air-sequences','exec'),globals())
sys.path.insert(0,str(Path('work/namek-native-r10').resolve()));from resource_check import inspect
O=Path('work/air-pursuit-fall/captures');O.mkdir(parents=True,exist_ok=True);writer=None;reports=[];checks=[]
def tick(a=(),b=()):
 rawtick(a,b)
 w,h,pitch,data=latest;assert (w,h)==(320,224)
 writer.stdin.write(b''.join(data[y*pitch:y*pitch+w*2] for y in range(h)))
 rows.append(dict(f=len(rows),p=st(P1),e=st(P2),phase=rb(0xf800),victimPhase=rb(0xf840),airHits=rb(0xf802),pose=rb(P1+4),enemyPose=rb(P2+4),keys=list(a),keys2=list(b),stage=rb(0xe741),variant=rb(0xf7c0)))
 if len(rows) in [55,70,85,100,120,145,180,240,360,420,480]:save_image(O/f'{label}-qa-{len(rows):03}.png')
 if rb(0xf800)==3 and not any(c['label']==label+'-air' for c in checks):checks.append(inspect(snap(),Path('work/namek-native-r10'),slug,label+'-air'))
try:
 for label,cid,slug,side,finish,expected in [('01-goku-meteor',0,'normal',0,'meteor',0x83e),('02-vegeta-meteor',3,'aldea',0,'meteor',0x846),('03-goku-meteor',0,'porunga',1,'meteor',0x83e),('04-vegeta-meteor',3,'porunga',1,'meteor',0x846)]:
  prepare(cid,slug,side,critical=cid==3 and finish=='meteor');checks.append(inspect(snap(),Path('work/namek-native-r10'),slug,label+'-start'))
  writer=subprocess.Popen(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pixel_format','rgb565le','-video_size','320x224','-framerate',str(fps),'-i','pipe:0','-an','-c:v','libx264','-preset','veryfast','-threads','2','-crf','16','-pix_fmt','yuv420p',str(O/(label+'-silent.mp4'))],stdin=subprocess.PIPE)
  audio_file=(O/(label+'.pcm')).open('wb')
  r=sequence(cid,finish,side,slug,prepared=True)
  assert r['second'] and expected in r['programs'],r
  writer.stdin.close();assert writer.wait()==0;writer=None;audio_file.close();audio_file=None
  capturePath=O/(label+'.mp4')
  subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(O/(label+'-silent.mp4')),'-f','s16le','-ar',str(round(av.timing.sample_rate)),'-ac','2','-i',str(O/(label+'.pcm')),'-c:v','copy','-c:a','aac','-b:a','160k','-shortest','-movflags','+faststart',str(capturePath)],check=True)
  (O/(label+'.json')).write_text(json.dumps(rows))
  r.update(label=label,scenario=slug,side=side,romSha256=hashlib.sha256(rom).hexdigest(),videoSha256=hashlib.sha256(capturePath.read_bytes()).hexdigest(),lastDamageFrame=max(i for i in range(1,len(rows)) if rows[i]['e']['hp']<rows[i-1]['e']['hp']),airFinisher=finish!='meteor' and any(t['p']['program']==expected and t['p']['y']<448 for t in rows))
  reports.append(r);print(r,flush=True)
 (O/'manifest.json').write_text(json.dumps(dict(romSha256=hashlib.sha256(rom).hexdigest(),fps=fps,takes=reports,resources=checks,method='Direct ROM framebuffer/audio, scripted human ports. Initial spacing/facing only before capture; no position/action/HP/KI/timer writes during a take. Menu seeds from native selection.'),indent=2))
finally:
 if writer:writer.stdin.close();writer.wait()
 if audio_file:audio_file.close()
 core.retro_unload_game();core.retro_deinit()



