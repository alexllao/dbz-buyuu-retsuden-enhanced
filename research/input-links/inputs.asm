; Reconocedor humano de Goku y correcciones de respuesta v2.
frame_entry:
 .hex 48e7fffe
 .hex 40e7
 tst.b (0xffffe744).w
 bne.w @frame_done
 tst.b (0xffffe742).w
 bne.w @frame_done
 tst.b (0xffffe73c).w
 bne.w @frame_done
 tst.w (0xffffe9c4).w
 bne.w @frame_done
 lea (0xffffe75e).w,A0
 lea (0xfffff710).w,A3
 jsr @walking.l
 lea (0xffffe886).w,A0
 lea (0xfffff714).w,A3
 jsr @walking.l
frame_done:
 .hex 46df
 .hex 4cdf7fff
 jmp 0x003d2000.l
walking:
 tst.b (0xbe,A0)
 bne.w @walk_clear
 tst.w (0x24,A0)
 beq.w @walk_clear
 cmpa.l #0xffffe75e,A0
 bne.w @walk_p2
 move.b (0xffffe666).w,D1
 bra.w @walk_keys
walk_p2:
 move.b (0xffffe668).w,D1
walk_keys:
 andi.b #0x0c,D1
 bne.w @walk_clear
 tst.b (A3)
 bne.w @walk_coast
 move.w (A0),D0
 cmpi.w #0x01,D0
 beq.w @walk_stop
 cmpi.w #0x02,D0
 bne.w @walk_return
walk_stop:
 move.b (0x59,A0),D1
 cmpi.w #0x02,D0
 bne.w @walk_direction
 eori.b #0x01,D1
walk_direction:
 move.b D1,(0x01,A3)
 jsr 0x003d21fa.l
 move.b #0x04,(A3)
walk_coast:
 tst.b (0x5b,A0)
 bne.w @walk_clear
 moveq #0,D0
 move.b (A3),D0
 mulu.w #0x30,D0
 tst.b (0x01,A3)
 bne.w @coast_left
 jsr 0x00020e04.l
 bra.w @coast_done
coast_left:
 jsr 0x00020e2c.l
coast_done:
 subq.b #0x01,(A3)
 rts
walk_clear:
 clr.w (A3)
walk_return:
 rts
matcher:
 tst.b (0x58,A0)
 bne.w @native_matcher
 tst.b (0xbe,A0)
 bne.w @native_matcher
 .hex 48e7fffe
 .hex 40e7
 lea (0xfffff720).w,A3
 cmpa.l #0xffffe75e,A0
 beq.w @matcher_state
 adda.w #0x10,A3
matcher_state:
 cmpi.w #0xd501,(A3)
 beq.w @matcher_initialized
 clr.l (A3)
 clr.l (0x04,A3)
 clr.b (0x0d,A3)
 clr.b (0x0e,A3)
 clr.b (0x0f,A3)
 move.w #0xd501,(A3)
matcher_initialized:
 clr.b (0x0a,A3)
 move.b #0xff,(0xb9,A0)
 clr.b (0xb5,A0)
 move.b (0x59,A0),D0
 cmp.b (0x05,A3),D0
 beq.w @matcher_facing
 move.b D0,(0x05,A3)
 clr.b (0x0e,A3)
 move.b (0xb6,A0),(0xb7,A0)
 clr.w (0x02,A3)
matcher_facing:
 cmpa.l #0xffffe75e,A0
 bne.w @matcher_p2
 move.b (0xffffe666).w,D0
 bra.w @matcher_held
matcher_p2:
 move.b (0xffffe668).w,D0
matcher_held:
 moveq #0,D4
 moveq #0,D1
 move.b (0xba,A0),D1
 btst.l D1,D0
 beq.w @held_b
 bset.l #0,D4
held_b:
 move.b (0xbb,A0),D1
 btst.l D1,D0
 beq.w @held_ready
 bset.l #1,D4
held_ready:
 move.b (0x04,A3),D5
 move.b D4,(0x04,A3)
 move.b D5,D0
 not.b D0
 and.b D4,D0
 beq.w @pending_age
 move.b D4,(0x02,A3)
 move.b #0x06,(0x03,A3)
pending_age:
 tst.b (0x03,A3)
 beq.w @try_charge_release
 subq.b #0x01,(0x03,A3)
 move.b (0x02,A3),D0
 bra.w @choose_table
try_charge_release:
 cmpi.b #0x0f,(0x5b,A0)
 bne.w @matcher_done
 cmpi.b #0x03,D5
 bne.w @matcher_done
 cmpi.b #0x03,D4
 beq.w @matcher_done
 ; La salida de carga entrega el gesto al buffer corto existente.
 move.b #0x01,(0x0a,A3)
 moveq #1,D0
choose_table:
 move.b D0,(0x0b,A3)
 clr.b (0x0c,A3)
 lea (@table_a).l,A1
 cmpi.b #0x01,D0
 beq.w @scan_table
 lea (@table_ab).l,A1
 cmpi.b #0x02,D0
 bne.w @scan_table
 move.b #0x01,(0x0c,A3)
scan_table:
 moveq #0,D7
 move.b (A1)+,D7
 cmpi.b #0xff,D7
 bne.w @scan_pattern
 tst.b (0x0c,A3)
 beq.w @matcher_done
 bra.w @fallback_b
scan_pattern:
 moveq #0,D6
 move.b (A1)+,D6
 movea.l A1,A4
 ; El anillo nativo conserva direcciones; no consumirlo al fallar.
 moveq #0,D2
 move.b (0xb6,A0),D2
 moveq #0,D3
 move.b (0xb7,A0),D3
 sub.w D3,D2
 andi.w #0x1f,D2
 lsr.w #1,D2
 beq.w @pattern_failed
 moveq #0,D3
 move.b (0xb6,A0),D3
 subq.w #2,D3
 andi.w #0x1f,D3
 lea (0x94,A0),A2
 cmpi.b #0x08,(0xb8,A0)
 bhi.w @pattern_failed
 moveq #0,D5
 move.b #0x01,(0x07,A3)
 clr.b (0x06,A3)
 ; Excluir registros neutros recientes, sin aceptar gestos antiguos.
skip_tail_zero:
 move.b (0,A2,D3w*1),D1
 andi.b #0x0f,D1
 bne.w @pattern_step
 jsr @previous_direction.l
 bcs.w @pattern_failed
 bra.w @skip_tail_zero
pattern_step:
 move.b (A1)+,D0
 beq.w @pattern_matched
 move.b D0,D4
 andi.b #0x0f,D4
 cmp.b D4,D1
 beq.w @step_matched
 ; Direcciones cardinales: aceptar su componente en una diagonal.
 move.b D4,D0
 subq.b #1,D0
 and.b D4,D0
 bne.w @step_not_equal
 move.b D1,D0
 and.b D4,D0
 bne.w @step_matched
step_not_equal:
 move.b D1,D0
 and.b (0x06,A3),D0
 beq.w @pattern_failed
 ; Repeticiones y diagonales de la fase anterior no rompen el gesto.
 subq.l #1,A1
 jsr @previous_direction.l
 bcs.w @pattern_failed
 move.b (0,A2,D3w*1),D1
 andi.b #0x0f,D1
 bra.w @pattern_step
step_matched:
 clr.b (0x07,A3)
 ; Duración del primer sentido del gesto libre; resto acotado.
 tst.b (A1)
 beq.w @pattern_matched
 moveq #0,D0
 move.b (0x01,A2,D3w*1),D0
 cmpi.w #0x12,D0
 bhi.w @pattern_failed
 add.w D0,D5
 cmp.w D6,D5
 bhi.w @pattern_failed
 move.b D4,(0x06,A3)
next_distinct:
 jsr @previous_direction.l
 bcs.w @pattern_failed
 move.b (0,A2,D3w*1),D1
 andi.b #0x0f,D1
 beq.w @next_distinct
 bra.w @pattern_step
pattern_failed:
 movea.l A4,A1
skip_pattern:
 tst.b (A1)+
 bne.w @skip_pattern
 bra.w @scan_table
pattern_matched:
 cmpi.b #0x19,D7
 bne.w @check_air_command
 tst.b (0x0c,A3)
 beq.w @check_air_command
 cmpi.b #0x04,(0x03,A3)
 bcc.w @chord_wait
 bra.w @fallback_b
check_air_command:
 cmpi.b #0x14,D7
 bne.w @commit_command
 cmpi.b #0x04,(0x5b,A0)
 bcs.w @pattern_failed
 cmpi.b #0x08,(0x5b,A0)
 bhi.w @pattern_failed
commit_command:
 ; Margen breve para A+B: no disparar Super al llegar A antes que B.
 cmpi.b #0x06,D7
 bne.w @command_startup
 cmpi.b #0x01,(0x04,A3)
 bne.w @command_startup
 cmpi.b #0x04,(0x03,A3)
 bcc.w @chord_wait
command_startup:
 ; Botón algo anticipado: reconducir el arranque de un básico aún
 ; inactivo, antes del contacto. No cancelar técnicas ni golpes activos.
 tst.b (0x03,A3)
 beq.w @command_ready
 cmpi.w #0x0400,(A0)
 bcs.w @command_ready
 cmpi.w #0x0800,(A0)
 bcc.w @command_ready
 cmpi.w #0x04,(0x06,A0)
 bhi.w @command_ready
 btst.b #0x07,(0x1e,A0)
 bne.w @command_ready
 jsr 0x003d21fa.l
command_ready:
 ; Retener solo comandos reconocidos durante un basico de pie.
 ; No cancelar aqui: esperar al despacho natural o al asistente existente.
 clr.b (0x0e,A3)
 cmpi.w #0x0100,(0xffffe756).w
 bne.w @queue_ready
 btst.b #0x04,(0x1e,A0)
 bne.w @queue_ready
 cmpi.w #0x0400,(A0)
 bcc.w @queue_program
 cmpi.b #0x08,(0x5b,A0)
 bhi.w @queue_ready
 tst.b (0x0f,A3)
 beq.w @queue_ready
 bra.w @queue_store
queue_program:
 cmpi.w #0x0800,(A0)
 bcc.w @queue_ready
queue_store:
 move.b D7,(0x0d,A3)
 move.b #0x06,(0x0e,A3)
queue_ready:
 move.b D7,(0xb9,A0)
 tst.b (0x0a,A3)
 bne.w @keep_charge_gesture
 move.b (0xb6,A0),(0xb7,A0)
keep_charge_gesture:
 clr.w (0x02,A3)
 bra.w @matcher_done
fallback_b:
 clr.b (0x0c,A3)
 lea (@table_b).l,A1
 bra.w @scan_table
chord_wait:
 moveq #0,D0
 moveq #0,D1
 move.b (0xba,A0),D1
 bset.l D1,D0
 move.b (0xbb,A0),D1
 bset.l D1,D0
 not.b D0
 and.b D0,(0x1c,A0)
 and.b D0,(0x1d,A0)
matcher_done:
 ; Seis actualizaciones maximas. Un golpe recibido, cambio de sentido,
 ; vuelo o tecnica iniciada descartan la orden. Solo reemitir en neutral.
 tst.b (0x0e,A3)
 beq.w @queue_done
 tst.w (0x24,A0)
 beq.w @queue_clear
 btst.b #0x04,(0x1e,A0)
 bne.w @queue_clear
 cmpi.b #0x0b,(0x5b,A0)
 beq.w @queue_clear
 cmpi.b #0x0c,(0x5b,A0)
 beq.w @queue_clear
 cmpi.w #0x0800,(A0)
 bcc.w @queue_clear
 subq.b #0x01,(0x0e,A3)
 cmpi.b #0xff,(0xb9,A0)
 bne.w @queue_done
 cmpi.b #0x08,(0x5b,A0)
 bhi.w @queue_done
 move.b (0x0d,A3),(0xb9,A0)
 bra.w @queue_done
queue_clear:
 clr.b (0x0e,A3)
queue_done:
 ; Recordar un basico en la lectura anterior: la rutina nativa puede
 ; finalizarlo antes de que el reconocedor vea el boton de este frame.
 clr.b (0x0f,A3)
 cmpi.w #0x0400,(A0)
 bcs.w @queue_exit
 cmpi.w #0x0800,(A0)
 bcc.w @queue_exit
 move.b #0x01,(0x0f,A3)
queue_exit:
 .hex 46df
 .hex 4cdf7fff
 rts
previous_direction:
 subq.w #1,D2
 beq.w @previous_empty
 subq.w #2,D3
 andi.w #0x1f,D3
 .hex 023c00fe
 rts
previous_empty:
 .hex 003c0001
 rts
native_matcher:
 lea (0x000093a8).l,A1
 jsr 0x0000937e.l
 jmp 0x0000926c.l
; Token, tiempo total máximo, gesto inverso, 0. Bit7=diagonal opcional.
table_a:
 .hex 065008020408020400
 .hex 052808020400
 .hex 02200a020800
 .hex 0120080200
 .hex 0420040200
 .hex 0320020200
 .hex 0018080400
 .hex ff
table_b:
 .hex 11200a020800
 .hex 1220040200
 .hex 1420080200
 .hex 1020080200
 .hex 132008040800
 .hex ff
table_ab:
 .hex 195008020408020400
 .hex ff
 .hex 00
 .hex 00
history_direction:
 tst.b (0x58,A0)
 bne.w @history_original
 tst.b (0xbe,A0)
 bne.w @history_original
 andi.b #0x0f,D2
history_original:
 jmp 0x003d23da.l
round_reset:
 .hex 48e7fffe
 .hex 40e7
 lea (0xfffff462).w,A1
 moveq #0x08,D0
clear_p1:
 clr.l (A1)+
 subq.w #1,D0
 bpl.w @clear_p1
 lea (0xfffff58a).w,A1
 moveq #0x08,D0
clear_p2:
 clr.l (A1)+
 subq.w #1,D0
 bpl.w @clear_p2
 lea (0xfffff700).w,A1
 moveq #0x0f,D0
clear_inputs:
 clr.l (A1)+
 subq.w #1,D0
 bpl.w @clear_inputs
 .hex 46df
 .hex 4cdf7fff
 jmp 0x003b0488.l
