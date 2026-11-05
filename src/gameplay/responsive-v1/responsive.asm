; Prueba de respuesta: preserva registros, daño y contadores existentes.
entry:
 .hex 48e7fffe
 .hex 40e7
 tst.b (0xffffe744).w
 bne.w @entry_done
 tst.b (0xffffe742).w
 bne.w @entry_done
 tst.b (0xffffe73c).w
 bne.w @entry_done
 tst.w (0xffffe9c4).w
 bne.w @entry_done
 lea (0xffffe75e).w,A0
 jsr @charge_actor.l
 lea (0xffffe886).w,A0
 jsr @charge_actor.l
entry_done:
 jmp 0x003d0006.l
charge_actor:
 lea (0xfffff700).w,A3
 cmpa.l #0xffffe75e,A0
 beq.w @charge_state_ready
 adda.w #0x08,A3
charge_state_ready:
 tst.b (0xbe,A0)
 bne.w @charge_return
 cmpi.b #0xd3,(0x00,A3)
 beq.w @charge_initialized
 clr.l (0x00,A3)
 move.b #0xd3,(0x00,A3)
charge_initialized:
 moveq #0,D7
 tst.w (0x24,A0)
 beq.w @buffer_clear
 moveq #0,D5
 moveq #0,D6
 move.b (0xba,A0),D6
 bset.l D6,D5
 move.b (0xbb,A0),D6
 bset.l D6,D5
 cmpa.l #0xffffe75e,A0
 bne.w @charge_raw_p2
 move.b (0xffffe666).w,D4
 bra.w @charge_raw_ready
charge_raw_p2:
 move.b (0xffffe668).w,D4
charge_raw_ready:
 and.b D5,D4
 cmp.b D5,D4
 beq.w @charge_both
 clr.b (0x03,A3)
 bra.w @charge_action
charge_both:
 tst.b (0x03,A3)
 beq.w @charge_action
 not.b D5
 and.b D5,(0x1a,A0)
 and.b D5,(0x1b,A0)
 and.b D5,(0x1c,A0)
 and.b D5,(0x1d,A0)
 cmpi.b #0x0f,(0x5b,A0)
 bne.w @charge_return
 jsr @reset_own_action.l
 rts
charge_action:
 cmpi.b #0x0f,(0x5b,A0)
 bne.w @buffer_dispatch
 moveq #1,D7
 jsr @clean_charge_history.l
 cmp.b D5,D4
 bne.w @charge_stop
 cmpi.w #0xf9,(0x28,A0)
 bcs.w @charge_visible
 move.b #0x01,(0x03,A3)
 not.b D5
 and.b D5,(0x1a,A0)
 and.b D5,(0x1b,A0)
 and.b D5,(0x1c,A0)
 and.b D5,(0x1d,A0)
charge_stop:
 jsr @reset_own_action.l
 bra.w @buffer_dispatch
charge_visible:
 move.b #0xff,(0xbd,A0)
 ; El incremento de ki permanece en la rutina nativa.
buffer_dispatch:
 tst.b D7
 beq.w @buffer_restore
 move.b (0xb9,A0),D6
 cmpi.b #0xff,D6
 beq.w @buffer_restore
 move.b D6,(0x02,A3)
 move.b #0x0c,(0x01,A3)
 tst.b D7
 beq.w @charge_return
 ; Una liberación de carga puede activar el flanco negativo nativo.
 ; Guardar el comando sin dispararlo hasta una pulsación real del botón.
 cmpa.l #0xffffe75e,A0
 bne.w @buffer_edge_p2
 move.b (0xffffe667).w,D2
 bra.w @buffer_real_edge
buffer_edge_p2:
 move.b (0xffffe669).w,D2
buffer_real_edge:
 moveq #0,D3
 move.b (0xba,A0),D1
 bset.l D1,D3
 move.b (0xbb,A0),D1
 bset.l D1,D3
 and.b D3,D2
 bne.w @charge_return
 move.b #0xff,(0xb9,A0)
 not.b D3
 and.b D3,(0x1c,A0)
 and.b D3,(0x1d,A0)
 rts
buffer_restore:
 tst.b (0x01,A3)
 beq.w @charge_return
 subq.b #0x01,(0x01,A3)
 cmpi.b #0x0b,(0x5b,A0)
 beq.w @buffer_clear
 cmpi.b #0x0c,(0x5b,A0)
 beq.w @buffer_clear
 cmpi.b #0x08,(0x5b,A0)
 bhi.w @charge_return
 cmpi.b #0xff,(0xb9,A0)
 bne.w @charge_return
 move.b (0x02,A3),D6
 move.b (0xba,A0),D3
 cmpi.b #0x10,D6
 bcs.w @buffer_button
 move.b (0xbb,A0),D3
buffer_button:
 move.b (0x1d,A0),D2
 btst.l D3,D2
 beq.w @charge_return
 move.b D6,(0xb9,A0)
 clr.b (0x01,A3)
 rts
buffer_clear:
 clr.w (0x01,A3)
charge_return:
 rts
clean_charge_history:
 ; La carga simultánea no debe contaminar las direcciones con A/B.
 lea (0x94,A0),A2
 moveq #0x0f,D1
clean_history_loop:
 andi.b #0x0f,(A2)
 adda.w #0x02,A2
 subq.w #0x01,D1
 bpl.w @clean_history_loop
 rts
reset_own_action:
 jsr 0x00020ba0.l
 move.w #0xe020,D0
 jsr 0x0001319a.l
 andi.b #0x3f,(0x20,A0)
 clr.w (A0)
 clr.b (0x5b,A0)
 clr.b (0x109,A0)
 clr.b (0x10a,A0)
 clr.b (0x10c,A0)
 clr.b (0x10e,A0)
 rts
cancel_basic:
 ; Sólo se llama tras contacto confirmado de un básico elegible.
 jsr @reset_own_action.l
 bset.b #0x07,(0x107,A0)
 rts
matcher:
 tst.b (0x58,A0)
 beq.w @goku_matcher
 lea (0x000093a8).l,A1
 jsr 0x0000937e.l
 jmp 0x0000926c.l
goku_matcher:
 tst.b (0xbe,A0)
 bne.w @matcher_native
 jsr 0x0000937e.l
 move.b (0xba,A0),D1
 btst.l D1,D0
 beq.w @goku_button_b
 lea (@goku_a).l,A1
 jsr 0x0000939a.l
 jmp 0x000092b2.l
goku_button_b:
 move.b (0xbb,A0),D1
 btst.l D1,D0
 beq.w @charge_return
 lea (@goku_b).l,A1
 jsr 0x0000939a.l
 jmp 0x000092b2.l
matcher_native:
 lea (0x000093a8).l,A1
 jsr 0x0000937e.l
 jmp 0x0000926c.l
goku_a:
 ; Secuencias nativas, última dirección primero; largas antes que cortas.
 .hex 06080a02080a020006
 .hex 05080a0206040001
 .hex 030a02080002
 .hex 0202020003
 .hex 03080a020005
 .hex 030406020004
 .hex 0208040000
 .hex 00
goku_b:
 .hex 06080a02080a020019
 .hex 030a02080011
 .hex 030406020012
 .hex 03080a020014
 .hex 03080a020010
 .hex 030804080013
 .hex 00
input_restore:
 jsr 0x00008f68.l
 .hex 48e7fffe
 .hex 40e7
 tst.b (0xffffe744).w
 bne.w @restore_done
 tst.b (0xffffe73c).w
 bne.w @restore_done
 tst.w (0xffffe9c4).w
 bne.w @restore_done
 lea (0xffffe75e).w,A0
 lea (0xffffe886).w,A1
 jsr @restore_thrower.l
 lea (0xffffe886).w,A0
 lea (0xffffe75e).w,A1
 jsr @restore_thrower.l
restore_done:
 .hex 46df
 .hex 4cdf7fff
 rts
restore_thrower:
 tst.b (0xbe,A0)
 bne.w @restore_return
 tst.w (0x24,A0)
 beq.w @restore_return
 tst.w (0x24,A1)
 beq.w @restore_return
 cmpi.b #0x08,(0x5b,A0)
 bhi.w @restore_return
 cmpi.b #0x17,(0x5b,A1)
 bne.w @restore_return
 btst.b #0x04,(0x20,A1)
 beq.w @restore_return
 cmpa.l #0xffffe75e,A0
 bne.w @restore_p2
 move.b (0xffffe6bc).w,(0x1a,A0)
 move.b (0xffffe666).w,(0x1b,A0)
 move.b (0xffffe6bd).w,(0x1c,A0)
 move.b (0xffffe667).w,(0x1d,A0)
 rts
restore_p2:
 move.b (0xffffe6e4).w,(0x1a,A0)
 move.b (0xffffe668).w,(0x1b,A0)
 move.b (0xffffe6e5).w,(0x1c,A0)
 move.b (0xffffe669).w,(0x1d,A0)
restore_return:
 rts
aura_residual:
 move.b (0x5b,A0),D0
 cmpi.b #0x08,D0
 bls.w @residual_allowed
 cmpi.b #0x0f,D0
 beq.w @residual_allowed
 jmp 0x0007b5d2.l
residual_allowed:
 jmp 0x0007b4b2.l
history_direction:
 cmpi.b #0x0f,(0x5b,A0)
 bne.w @history_original
 andi.b #0x0f,D2
history_original:
 cmpi.b #0x00,(0x59,A0)
 jmp 0x00009230.l
throw_special_gate:
 tst.b (0xbe,A0)
 bne.w @throw_gate_original
 cmpi.b #0x08,(0x5b,A0)
 bhi.w @throw_gate_original
 cmpi.b #0x17,(0x5b,A1)
 bne.w @throw_gate_original
 jmp 0x00021094.l
throw_gate_original:
 btst.b #0x04,(0x20,A1)
 jmp 0x00021090.l
