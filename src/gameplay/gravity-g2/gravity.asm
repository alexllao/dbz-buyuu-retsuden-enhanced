; Prueba de dos arcos de salto y recuperacion del doble toque.
; Se conserva el parser, la velocidad horizontal y la carrera nativos.
frame_entry:
 .hex 48e7fffe
 .hex 40e7
 cmpi.w #0x0c,(0xffffe6a4).w
 bne.w @frame_resume
 tst.b (0xffffe744).w
 bne.w @frame_resume
 tst.b (0xffffe742).w
 bne.w @frame_resume
 tst.b (0xffffe9b0).w
 bne.w @frame_resume
 tst.b (0xffffe73c).w
 bne.w @frame_resume
 tst.w (0xffffe9c4).w
 bne.w @frame_resume
 lea (0xffffe75e).w,A0
 lea (0xfffff740).w,A3
 jsr @dash_actor.l
 lea (0xffffe886).w,A0
 lea (0xfffff748).w,A3
 jsr @dash_actor.l
frame_resume:
 ; El cuerpo anterior conserva sus propios guardas y restaura esta pila.
 jmp 0x003d3006.l
dash_actor:
 tst.b (0xbe,A0)
 bne.w @dash_return
 cmpi.w #0xe501,(A3)
 beq.w @dash_ready
 clr.l (A3)
 clr.l (0x04,A3)
 move.w #0xe501,(A3)
dash_ready:
 tst.b (0x02,A3)
 beq.w @dash_read
 subq.b #0x01,(0x02,A3)
dash_read:
 moveq #0,D0
 move.b (0x1b,A0),D0
 cmpi.b #0x04,D0
 beq.w @dash_direction
 cmpi.b #0x08,D0
 beq.w @dash_direction
 ; Solo una liberacion horizontal desde reposo/caminar abre la ventana.
 tst.b (0x04,A3)
 beq.w @dash_other_input
 cmpi.b #0x02,(0x5b,A0)
 bhi.w @dash_other_input
 tst.b D0
 bne.w @dash_other_input
 move.b #0x10,(0x02,A3)
 move.b (0x04,A3),(0x03,A3)
dash_other_input:
 clr.b (0x04,A3)
 cmpi.b #0x02,(0x5b,A0)
 bls.w @dash_return
 clr.b (0x02,A3)
 rts
dash_direction:
 move.b (0x04,A3),D1
 move.b D0,(0x04,A3)
 tst.b D1
 bne.w @dash_return
 tst.b (0x02,A3)
 beq.w @dash_return
 cmp.b (0x03,A3),D0
 bne.w @dash_clear
 cmpi.b #0x02,(0x5b,A0)
 bhi.w @dash_clear
 tst.w (0x24,A0)
 beq.w @dash_clear
 clr.b (0x02,A3)
 moveq #0x08,D1
 tst.b (0x59,A0)
 beq.w @dash_choose
 moveq #0x04,D1
dash_choose:
 cmp.b D1,D0
 bne.w @dash_back
 jsr 0x00021d3c.l
 rts
dash_back:
 jsr 0x00021d98.l
 rts
dash_clear:
 clr.b (0x02,A3)
dash_return:
 rts

; Programa normal de salto, incluidas las variantes de Ginyu.
is_jump:
 cmpa.l #0xffffe75e,A0
 beq.w @jump_actor
 cmpa.l #0xffffe886,A0
 bne.w @not_jump
jump_actor:
 tst.b (0x58,A0)
 bne.w @not_jump
 move.w (A0),D7
 cmpi.w #0x04,D7
 bcs.w @not_jump
 cmpi.w #0x25,D7
 bcs.w @yes_jump
 cmpi.w #0x015f,D7
 bcs.w @not_jump
 cmpi.w #0x0165,D7
 bcc.w @not_jump
yes_jump:
 .hex 003c0004
 rts
not_jump:
 .hex 023c00fb
 rts

; Goku: unidad temporal2 normal /3 desde carrera. Se escala con normal/turbo.
duration:
 move.l D7,-(SP)
 jsr @is_jump.l
 bne.w @duration_native
 move.w #0x16,D0
 btst.b #0x07,(0x20,A0)
 beq.w @duration_native
 move.w #0x21,D0
duration_native:
 move.l (SP)+,D7
 jsr 0x00020adc.l
 rts

; Reproducir primero efectos/registros del movimiento nativo, y sustituir Y
; por una parabola. Solo Goku: altura normal=7/10 anterior; carrera=9/4 de la normal.
; Con tiempo20/30, ambos estilos comparten aceleracion gravitatoria.
vertical:
 move.l D1,-(SP)
 move.l D5,-(SP)
 move.l D2,-(SP)
 jsr 0x00021e9c.l
 .hex 48e7fffe
 .hex 40e7
 jsr @is_jump.l
 bne.w @vertical_done
 cmpi.w #0x01,D3
 bcs.w @vertical_done
 cmpi.w #0x04,D3
 bhi.w @vertical_done
 moveq #0,D2
 move.w (0x40,SP),D2
 beq.w @vertical_done
 moveq #0,D3
 move.w (0x48,SP),D3
 add.w (0x44,SP),D3
 mulu.w #0x07,D3
 divu.w #0x0a,D3
 andi.l #0x0000ffff,D3
 btst.b #0x07,(0x20,A0)
 beq.w @vertical_height
 mulu.w #0x09,D3
 divu.w #0x04,D3
 andi.l #0x0000ffff,D3
vertical_height:
 moveq #0,D0
 move.w (0x06,A0),D0
 sub.w D2,D0
 addq.w #0x01,D0
 bpl.w @vertical_time
 moveq #0,D0
vertical_time:
 mulu.w #0x0a,D2
 cmp.w D2,D0
 bls.w @vertical_clamped
 move.w D2,D0
vertical_clamped:
 move.w D2,D1
 sub.w D0,D1
 mulu.w D1w,D0
 lsl.l #0x02,D0
 mulu.w D3w,D0
 move.w D2,D1
 mulu.w D1w,D1
 divu.w D1w,D0
 andi.l #0x0000ffff,D0
 lsl.l #0x08,D0
 move.l #0x01c00000,D1
 btst.b #0x04,(0x1e,A0)
 beq.w @vertical_ground
 move.l #0x00a00000,D1
vertical_ground:
 sub.l D0,D1
 move.l D1,(0x10,A0)
vertical_done:
 .hex 46df
 .hex 4cdf7fff
 adda.w #0x0c,SP
 rts
