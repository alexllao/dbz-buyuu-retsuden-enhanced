; Sacudida grafica en Meteor confirmados. No cambia coordenadas de combate.
; F760 firma; F762 tiempo; F763 fuerza; F764 ultimo frame; F766 desplazamiento.
; F768 numero de contactos; F76a ultimo atacante; F76c programa; F76e victima.
event_entry:
 .hex 48e7fffe
 .hex 40e7
 cmpi.w #0x0c,(0xffffe6a4).w
 bne.w @event_resume
 cmpa.l #0xffffe75e,A0
 beq.w @event_actor
 cmpa.l #0xffffe886,A0
 bne.w @event_resume
event_actor:
 jsr 0x0001335c.l
 jsr @pulse.l
event_resume:
 jmp 0x003b0362.l

; Sonido nativo de contacto47. Permite cubrir contactos que el HUD aun omite.
; Solo con atacante Meteor y rival realmente capturado. Nunca contar HITS aqui.
cue_entry:
 clr.w D0
 move.b (0xffff5000).l,D0
 cmpi.b #0x47,D0
 bne.w @cue_return
 .hex 48e7fffe
 .hex 40e7
 lea (0xffffe75e).w,A1
 lea (0xffffe886).w,A0
 cmpi.w #0x083c,(A1)
 bcs.w @cue_p2
 cmpi.w #0x0860,(A1)
 bcs.w @cue_victim
cue_p2:
 lea (0xffffe886).w,A1
 lea (0xffffe75e).w,A0
cue_victim:
 cmpi.w #0x0883,(A0)
 bcs.w @cue_done
 cmpi.w #0x088e,(A0)
 bcc.w @cue_done
 jsr @pulse.l
cue_done:
 .hex 46df
 .hex 4cdf7fff
cue_return:
 rts

pulse:
 cmpi.w #0x0c,(0xffffe6a4).w
 bne.w @pulse_return
 move.w (A1),D0
 cmpi.w #0x083c,D0
 bcs.w @pulse_return
 cmpi.w #0x0860,D0
 bcc.w @pulse_return
 cmpi.b #0x0a,(0x58,A1)
 beq.w @pulse_return
 cmpi.w #0xa651,(0xfffff760).w
 beq.w @pulse_ready
 clr.l (0xfffff760).w
 clr.l (0xfffff764).w
 clr.l (0xfffff768).w
 move.w #0xa651,(0xfffff760).w
 move.w (0x24,A0),(0xfffff774).w
 move.w (0xffffe6a8).w,D0
 subi.w #0x0a,D0
 move.w D0,(0xfffff776).w
pulse_ready:
 moveq #0,D2
 move.w (0x24,A0),D0
 cmp.w (0xfffff774).w,D0
 bcc.w @pulse_hp
 moveq #0x01,D2
pulse_hp:
 move.w D0,(0xfffff774).w
 move.w (0xffffe6a8).w,D0
 sub.w (0xfffff776).w,D0
 cmpi.w #0x02,D0
 bls.w @pulse_strength
 move.w (0xffffe6a8).w,(0xfffff776).w
 move.w (A1),(0xfffff76c).w
 move.w (A0),(0xfffff76e).w
 move.b (0x58,A1),(0xfffff76a).w
 addq.w #0x01,(0xfffff768).w
 move.b #0x05,(0xfffff762).w
 clr.b (0xfffff763).w
pulse_strength:
 tst.w D2
 beq.w @pulse_return
 move.b #0x09,(0xfffff762).w
 move.b #0x01,(0xfffff763).w
pulse_return:
 rts

main_pre:
 jsr @pre.l
 move.w #0x0200,(0xffffe75a).w
 rts

pre:
 .hex 48e7c080
 .hex 40e7
 clr.w (0xfffff770).w
 cmpi.w #0xa651,(0xfffff760).w
 bne.w @clear
 cmpi.w #0x0c,(0xffffe6a4).w
 bne.w @clear
 tst.b (0xffffe9b0).w
 bne.w @clear
 tst.b (0xffffe742).w
 bne.w @clear
 tst.b (0xffffe744).w
 bne.w @paused
 move.w (0xffffe6a8).w,D0
 cmp.w (0xfffff764).w,D0
 beq.w @apply
 move.w D0,(0xfffff764).w
 clr.w (0xfffff766).w
 moveq #0,D0
 move.b (0xfffff762).w,D0
 beq.w @apply
 subq.b #0x01,(0xfffff762).w
 subq.w #0x01,D0
 lsl.w #0x01,D0
 lea (@pattern_soft).l,A0
 tst.b (0xfffff763).w
 beq.w @pattern
 lea (@pattern_strong).l,A0
pattern:
 move.w (0x00,A0,D0w*1),(0xfffff766).w
apply:
 move.w (0xfffff766).w,D0
 beq.w @pre_done
 move.w D0,(0xfffff770).w
 moveq #0,D1
 move.b (0xffffe452).w,D1
 move.w D1,(0xfffff772).w
 lea (0xffffe04e).w,A0
 subq.w #0x01,D1
 bmi.w @pre_done
pre_loop:
 cmpi.w #0x00a0,(A0)
 bcs.w @pre_next
 add.w D0,(0x06,A0)
 pre_next:
 adda.w #0x08,A0
 dbf D1w,@pre_loop
 bra.w @pre_done
paused:
 clr.w (0xfffff766).w
 bra.w @pre_done
clear:
 clr.b (0xfffff762).w
 clr.w (0xfffff766).w
pre_done:
 .hex 46df
 .hex 4cdf0103
 rts

scroll:
 ; El HUD superior usa el desplazamiento original. Aplicar el impulso
 ; a partir de la linea32 mediante una unica interrupcion horizontal.
 jsr 0x00007136.l
 .hex 40e7
 move.w (0xfffff766).w,(0xfffff77a).w
 tst.w (0xfffff77a).w
 beq.w @scroll_done
 move.w #0x8a1f,(0x00c00004).l
 move.w #0x8014,(0x00c00004).l
scroll_done:
 .hex 46df
 rts
hint:
 .hex 48e78002
 lea (0x00c00004).l,A6
 move.w #0x8004,(A6)
 move.w #0x8a00,(A6)
 move.w #0x8f02,(A6)
 move.l #0x68000002,(A6)
 move.w (0xffffc038).w,D0
 neg.w D0
 add.w (0xfffff77a).w,D0
 move.w D0,(0x00c00000).l
 move.w (0xffffc03a).w,D0
 neg.w D0
 add.w (0xfffff77a).w,D0
 move.w D0,(0x00c00000).l
 .hex 4cdf4001
 rte
pattern_soft:
 .hex 0000ffff0001fffe0002
pattern_strong:
 .hex 0000ffff0001fffe0002fffd0003fffc0004
