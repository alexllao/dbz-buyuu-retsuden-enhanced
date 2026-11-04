"""Importable native-versus menu boot and read-only CPU-soak stop signals.

Pass the namespace created by the existing gameplay_probe header. The only
fixture writes are both actor+BE control types. No HP/CID/palette/menu-state
forcing; no gamepad input is sent once native CPU control is enabled.
"""

P1=0xE75E
P2=0xE886

def snapshot(api):
    rb,rw=api['rb'],api['rw']
    return {'gameStateE6A4':rw(0xe6a4),'substateE6A6':rw(0xe6a6),
            'sceneE71A':rw(0xe71a),'cpuGateE742':rb(0xe742),'inputGateE744':rb(0xe744),
            'stageId':rb(0xe741),'nativeSpeed':[rw(0xe756),rw(0xe758)],
            'players':[{'id':rb(base+0x58),'hp':rw(base+0x24),'action':rb(base+0x5b),
                        'controlType':rb(base+0xbe),'x':rw(base+0xa),'y':rw(base+0x10),
                        'nativeHeld':rb(base+0x1b),'nativePressed':rb(base+0x1d),
                        'aiCountersC2C3C4':[rb(base+i) for i in [0xc2,0xc3,0xc4]]}
                       for base in [P1,P2]]}

def boot_versus(api,p1_id,p2_id,settle_frames=180):
    tick,wb,rb=api['tick'],api['wb'],api['rb']
    assert 0<=p1_id<=10 and 0<=p2_id<=10
    for index,step in enumerate(api['steps'][:-1]):
        if index==9 and p1_id:
            for direction,count in [('DOWN',p1_id//3),('RIGHT',p1_id%3)]:
                for _ in range(count):
                    for _ in range(4):tick([direction])
                    for _ in range(16):tick()
        if index==11 and p2_id!=1:
            for direction,count in [('DOWN',p2_id//3),('RIGHT',p2_id%3)]:
                for _ in range(count):
                    for _ in range(4):tick([direction])
                    for _ in range(16):tick()
            for _ in range(step.get('frames',1)):tick()
            continue
        for _ in range(step.get('frames',1)):tick(step.get('buttons',[]))
    assert [rb(P1+0x58),rb(P2+0x58)]==[p1_id,p2_id]
    wb(P1+0xbe,0);wb(P2+0xbe,0)
    for _ in range(settle_frames):tick()
    before=snapshot(api)
    assert before['gameStateE6A4']==0x0c,before
    assert before['cpuGateE742']==0 and before['inputGateE744']==0,before
    assert all(p['hp']>0 for p in before['players']),before
    wb(P1+0xbe,1);wb(P2+0xbe,1)
    after=snapshot(api)
    return {'beforeCpuEnable':before,'afterCpuEnable':after,
            'writes':'P1+BE andP2+BE only:human while settling, then1 for nativeCPU.',
            'difficulty':'Native boot defaults retained; no unverified difficulty variable is changed.',
            'controllerAfterBoot':'Call tick() or tick([],[]) ONLY. Both players use native AI; no scripted bot commands.'}

def stop_after_ko(api,display_frame,first_ko_frame,fps):
    """Return (stop, first_ko_frame, reason); never writes game state.

    Latches the first native HP==0, then allows about2s of end animation.
    Caller should also enforce its own45s per-pair upper limit.
    """
    state=snapshot(api)
    if first_ko_frame is None and any(p['hp']==0 for p in state['players']):
        first_ko_frame=display_frame
    if first_ko_frame is not None and display_frame-first_ko_frame>=round(2*fps):
        return True,first_ko_frame,'Native HP0 observed; about2s of ending captured'
    return False,first_ko_frame,None
