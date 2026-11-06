; Respuesta v3: conservar entradas e historial al liberarse del agarre.
; Se evita el borrado nativo de B7, no se fabrica un comando especial.
input_p1:
 lea (0xffffe75e).w,A0
 lea (0xffffe886).w,A1
 jsr @released_thrower.l
 beq.w @p1_allowed
 jmp 0x00008f70.l
p1_allowed:
 jmp 0x00008f8c.l
input_p2:
 lea (0xffffe886).w,A0
 lea (0xffffe75e).w,A1
 jsr @released_thrower.l
 beq.w @p2_allowed
 jmp 0x00008fe4.l
p2_allowed:
 jmp 0x00009000.l
released_thrower:
 cmpi.w #0x000c,(0xffffe6a4).w
 bne.w @not_allowed
 tst.b (0xffffe744).w
 bne.w @not_allowed
 tst.b (0xffffe742).w
 bne.w @not_allowed
 tst.b (0xffffe9b0).w
 bne.w @not_allowed
 tst.b (0xffffe73c).w
 bne.w @not_allowed
 tst.w (0xffffe9c4).w
 bne.w @not_allowed
 tst.b (0xbe,A0)
 bne.w @not_allowed
 tst.w (0x24,A0)
 beq.w @not_allowed
 tst.w (0x24,A1)
 beq.w @not_allowed
 cmpi.b #0x17,(0x5b,A1)
 bne.w @not_allowed
 ; El agarre propio debe terminar. Después se siguen leyendo órdenes
 ; durante movimiento, carga y ataques, igual que frente a rival neutral.
 cmpi.b #0x3a,(0x5b,A0)
 beq.w @not_allowed
 cmpi.b #0x3b,(0x5b,A0)
 beq.w @not_allowed
 cmpi.b #0x2f,(0xe2,A0)
 beq.w @not_allowed
 .hex 003c0004
 rts
not_allowed:
 .hex 023c00fb
 rts
poll_gate:
 ; El temporizador5002 sigue su curso; solo se evita saltar lecturas.
 tst.b (0xffffe73c).w
 bne.w @poll_cinematic
 cmpi.w #0x000c,(0xffffe6a4).w
 bne.w @poll_original
 tst.b (0xffffe744).w
 bne.w @poll_original
 tst.b (0xffffe742).w
 bne.w @poll_original
 tst.b (0xffffe9b0).w
 bne.w @poll_original
 tst.w (0xffffe9c4).w
 bne.w @poll_original
 tst.b (0xffffe81c).w
 beq.w @poll_now
 tst.b (0xffffe944).w
 beq.w @poll_now
poll_original:
 jmp 0x00008d10.l
poll_cinematic:
 jmp 0x00008d1a.l
poll_now:
 jmp 0x00008d2c.l
counter_tick:
 jsr 0x003b02da.l
 tst.b (0xd21,A0)
 beq.w @counter_return
 move.w (A0),D0
 cmpi.w #0x0400,D0
 bcs.w @counter_victim
 cmpi.w #0x0880,D0
 bcs.w @counter_return
 ; Las técnicas de ki C00..C7F también conservan el contador.
 ; No incluir recuperación, guardia ni carga libre de energía.
 cmpi.w #0x0c00,D0
 bcs.w @counter_victim
 cmpi.w #0x0c80,D0
 bcc.w @counter_victim
 cmpi.b #0x38,(0x5b,A0)
 beq.w @counter_return
 cmpi.b #0x39,(0x5b,A0)
 beq.w @counter_return
counter_victim:
 jmp 0x003b0314.l
counter_return:
 rts
