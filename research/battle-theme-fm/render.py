from pathlib import Path
import sys,json,wave,hashlib
audit_mode=sys.argv[1] if len(sys.argv)>1 else 'draft';P=Path('work/battle-theme-fm');metadata=json.loads((P/(audit_mode+'-stream.json')).read_text())
rawout=(P/(audit_mode+'.pcm')).open('wb')
source=Path('work/emulator/check_rom.py').read_text().split('\ntry:\n for step in steps:')[0]
source=source.replace('ROOT=Path(__file__).resolve().parent',"ROOT=Path('work/emulator').resolve()")
source=source.replace('def audio(l,r):pass','def audio(l,r):rawout.write(struct.pack("<hh",l,r))')
source=source.replace('def batch(data,frames):return frames','def batch(data,frames):\n rawout.write(C.string_at(data,frames*4))\n return frames')
sys.argv=['render',str(P/(audit_mode+'.bin')),'work/auras/controlled.json']
exec(compile(source,'standalone-fm-runtime','exec'),globals())
try:
 for _ in range(metadata['frames']+6):core.retro_run()
 counter=ram[0xf000^1]*256+ram[0xf001^1]
 assert counter>=metadata['frames'],(counter,metadata['frames'])
finally:rawout.close();core.retro_unload_game();core.retro_deinit()
data=(P/(audit_mode+'.pcm')).read_bytes();wavfile=P/(audit_mode+'.wav')
with wave.open(str(wavfile),'wb') as w:w.setnchannels(2);w.setsampwidth(2);w.setframerate(round(av.timing.sample_rate));w.writeframes(data)
sys.path.insert(0,'work/simulation-deps');import numpy as np
pcm=np.frombuffer(data,dtype='<i2').astype(float).reshape(-1,2)/32768;mono=pcm.mean(axis=1)
qa=dict(mode=audit_mode,emulator=info.name.decode(),coreVersion=info.version.decode(),sampleRate=av.timing.sample_rate,fps=av.timing.fps,seconds=len(pcm)/av.timing.sample_rate,peak=float(np.abs(pcm).max()),rms=float(np.sqrt(np.mean(pcm**2))),clippedSamples=int(np.sum(np.abs(pcm)>=32767/32768)),playerFrameCounter=counter,romSha256=hashlib.sha256(rom).hexdigest(),wavSha256=hashlib.sha256(wavfile.read_bytes()).hexdigest())
assert qa['rms']>.002 and qa['peak']<1 and qa['clippedSamples']==0,qa
if audit_mode=='tone':
 segment=mono[round(av.timing.sample_rate*.3):round(av.timing.sample_rate*1.6)];spec=np.abs(np.fft.rfft(segment*np.hanning(len(segment))));freq=np.fft.rfftfreq(len(segment),1/av.timing.sample_rate)
 peak=float(freq[spec.argmax()]);qa['calibrationHz']=peak;assert abs(peak-440)<2,qa
(P/(audit_mode+'-render.json')).write_text(json.dumps(qa,indent=2));print(json.dumps(qa,indent=2))
