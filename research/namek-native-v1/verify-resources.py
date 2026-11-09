from pathlib import Path
import sys,json,hashlib
nativeVariant=sys.argv[1] if len(sys.argv)>1 else 'porunga'
s=Path('work/namek-simulation/runtime.py').read_text().split("if __name__=='__main__':")[0].replace("N=Path('work/namek-simulation')",f"N=Path('work/namek-native/{nativeVariant}')").replace('work/combo-startup/candidate.bin',f'work/namek-native/{nativeVariant}/candidate.bin')
exec(compile(s,'native-namek-variant-test','exec'),globals())
def check_assets(label):
 data=snap();start=0x12425;vram=data[start:start+65536];linear=bytearray(len(vram));linear[0::2]=vram[1::2];linear[1::2]=vram[0::2];expected=(N/'tiles.bin').read_bytes();assert linear[:0x5c00]==expected[:0x5c00],label
 palette=(N/'palette.bin').read_bytes();expectedWords=[int.from_bytes(palette[i:i+2],'big') for i in range(0,44,2)];nativeCram=[int.from_bytes(data[start+65536+i*2:start+65536+i*2+2],'little') for i in range(32,54)];expectedCram=[((v>>1)&7)|(((v>>5)&7)<<3)|(((v>>9)&7)<<6) for v in expectedWords];assert nativeCram==expectedCram,(label,nativeCram,expectedCram)
 return dict(label=label,backgroundVramExact=True,palette22WordsExact=True,p=st(P1),e=st(P2))
try:
 boot_stage(0,8);fixture();save_image(N/'native-ground.png');checks=[check_assets('ground')];(N/'seed-0.state').write_bytes(snap())
 fixture(280)
 for _ in range(3):tick(['C'])
 for _ in range(90):tick()
 assert st(P1)['plane'];save_image(N/'native-flight.png');checks.append(check_assets('flight-one'))
 for _ in range(3):tick([],['C'])
 for _ in range(90):tick()
 assert st(P1)['plane'] and st(P2)['plane'];save_image(N/'native-both-flying.png');checks.append(check_assets('flight-both'))
 for _ in range(3):tick(['C'])
 for _ in range(90):tick()
 for _ in range(3):tick([],['C'])
 for _ in range(90):tick()
 assert not st(P1)['plane'] and not st(P2)['plane'];checks.append(check_assets('landed'))
 for _ in range(90):tick(['A','B'])
 save_image(N/'native-aura.png');checks.append(check_assets('aura'))
 (N/'runtime-check.json').write_text(json.dumps(dict(variant=nativeVariant,romSha256=hashlib.sha256(rom).hexdigest(),boot='Fresh ROM load; existing helper selects physical stage6 before loader for isolated resource test; final menu integration tested separately',checks=checks),indent=2));print('NATIVE RESOURCE PASSED',nativeVariant,[t['label'] for t in checks],flush=True)
finally:core.retro_unload_game();core.retro_deinit()
