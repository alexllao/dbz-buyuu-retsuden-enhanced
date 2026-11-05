; Barras nativas y contador HITS. Ventana pausada durante ataques y mareo.
; Barras AF20..AFA0 y contador AFA0..B000; no cambiar la animacion nativa.
entry:
 pea (@native_all).l
 bra.w @entry_common
entry_sat:
 pea (@native_sat).l
 bra.w @entry_common
entry_direct:
 pea (@native_direct).l
entry_common:
 .hex 40e7
 move.l (0xffffe04e).w,-(SP)
 move.l (0xffffe052).w,-(SP)
 .hex 48e7fffe
 cmpi.w #0x000c,(0xffffe6a4).w
 bne.w @draw_done
 moveq #0,D0
 move.b (0xffffe452).w,D0
 cmpi.w #0x004e,D0
 bhi.w @draw_done
 moveq #0,D5
 move.b (0xffffe452).w,D5
 lea (0xffffe04e).w,A4
 move.w D5,D0
 lsl.w #0x03,D0
 lea (0xffffe04e).w,A5
 adda.w D0,A5
 tst.w D5
 beq.w @empty_native
 move.l (A4),(A5)
 move.l (0x04,A4),(0x04,A5)
 addq.w #0x08,A5
 move.w D5,D4
 addq.w #0x01,D4
 bra.w @head_ready
empty_native:
 lea (0xffffe056).w,A5
 moveq #0x01,D4
head_ready:
 lea (@hud_map).l,A0
 move.l (A0)+,(A4)
 move.l (A0)+,(0x04,A4)
 move.b D4,(0x03,A4)
 moveq #0x00,D7
sprite_loop:
 move.l (A0)+,(A5)
 move.l (A0)+,(0x04,A5)
 addq.w #0x01,D4
 move.b D4,(0x03,A5)
 addq.w #0x08,A5
 subq.w #0x01,D7
 bpl.w @sprite_loop
 move.b D5,(-0x05,A5)
 ; Un contador activo: si el rival golpea, cierra el contador anterior.
 cmpi.w #0x004e,D5
 beq.w @draw_done
 jsr @hit_owner.l
 tst.w D0
 beq.w @draw_done
 lea (@hit_map_p1).l,A0
 cmpi.w #0x02,D0
 bne.w @hit_map_ready
 lea (@hit_map_p2).l,A0
hit_map_ready:
 move.b D4,(-0x05,A5)
 move.l (A0)+,(A5)
 move.l (A0)+,(0x04,A5)
 move.b D5,(0x03,A5)
draw_done:
 .hex 4cdf7fff
 .hex 46ef0008
 pea (@transfer_return).l
 move.l (0x0e,SP),-(SP)
 .hex 46ef0010
 rts
transfer_return:
 .hex 40e7
 ; Native720C clears head Y/link/X; restore only its original attribute word.
 move.w (0x02,SP),(0xffffe052).w
 .hex 46df
 lea (0x0e,SP),SP
 rts
pixels_entry:
 .hex 48e7fffe
 .hex 40e7
 cmpi.w #0x000c,(0xffffe6a4).w
 bne.w @pixels_done
 jsr @hud_pixels.l
pixels_done:
 .hex 46df
 .hex 4cdf7fff
 jmp 0x001ae356.l
hud_pixels:
 move.w #0x8f02,(0x00c00004).l
 lea (0x00c00000).l,A6
 lea (0xffffe75e).w,A0
 jsr @bar_pointer.l
 movea.l A0,A4
 lea (0xffffe886).w,A0
 jsr @bar_pointer.l
 movea.l A0,A5
 move.l #0x6f200002,(0x00c00004).l
 moveq #0x03,D7
bar_upload:
 move.l (A4)+,(A6)
 move.l (A4)+,(A6)
 move.l (A4)+,(A6)
 move.l (A4)+,(A6)
 move.l (0x0c,A5),(A6)
 move.l (0x08,A5),(A6)
 move.l (0x04,A5),(A6)
 move.l (A5),(A6)
 adda.w #0x10,A5
 subq.w #0x01,D7
 bpl.w @bar_upload
 jsr @hit_owner.l
 moveq #0,D1
 cmpi.w #0x01,D0
 bne.w @font_check_p2
 move.b (0xffffe87e).w,D1
 bra.w @font_number
font_check_p2:
 cmpi.w #0x02,D0
 bne.w @font_number
 move.b (0xffffe9a6).w,D1
font_number:
 andi.w #0x007f,D1
 tst.w D1
 beq.w @font_done
 cmp.b (0xffffe881).w,D1
 beq.w @font_done
 move.b D1,(0xffffe881).w
 mulu.w #0x0060,D1
 lea (0x003b6000).l,A0
 adda.l D1,A0
 move.l #0x6fa00002,(0x00c00004).l
 moveq #0x17,D7
font_upload:
 move.l (A0)+,(A6)
 subq.w #0x01,D7
 bpl.w @font_upload
font_done:
 rts
bar_pointer:
 moveq #0,D2
 moveq #0,D0
 move.w (0x36,A0),D0
 beq.w @accumulating
 moveq #0x02,D2
 move.w #0x0168,D1
 mulu.w (0xffffe758).w,D1
 lsr.l #0x08,D1
 bra.w @ratio
accumulating:
 move.b (0x51,A0),D0
 moveq #0,D1
 move.b (0x54,A0),D1
ratio:
 tst.w D1
 beq.w @zero
 mulu.w #0x001e,D0
 divu.w D1w,D0
 andi.l #0x0000ffff,D0
 cmpi.w #0x001e,D0
 bls.w @clamped
 move.w #0x001e,D0
clamped:
 tst.w D2
 bne.w @resource
 cmpi.w #0x0017,D0
 bcs.w @resource
 moveq #0x01,D2
 bra.w @resource
zero:
 moveq #0,D0
resource:
 mulu.w #0x001f,D2
 add.w D2,D0
 lsl.l #0x06,D0
 lea (0x003b4000).l,A0
 adda.l D0,A0
 rts
native_all:
 .hex 4df900c00004
 jmp 0x00006f2e.l
native_sat:
 .hex 4df900c00004
 jmp 0x00007022.l
native_direct:
 .hex 23fc6c00000200c00004
 jmp 0x00007078.l
hud_map:
 .hex 015c0c00e579008a
 .hex 015c0c00fd790196

; Salida de aturdimiento al primer impacto aceptado y no bloqueado.
; El motor ya calculo el dano y descarto los impactos no validos.
; A0 es la victima. No cambiar la reaccion, dano ni animacion nativa.
break_stun_on_hit:
 ; Ruta de impacto aceptado, despues de separar bloqueos nativos.
 jsr @count_hit.l
 tst.w (0x36,A0)
 bne.w @clear_active_stun
 clr.w (0x32,A0)
 cmpi.w #0x007d,(0x28,A0)
 jmp 0x00021a14.l
clear_active_stun:
 jsr 0x00020914.l
 jmp 0x00021a64.l

; Se conserva el prefijo original de side-advantage-v1 y su pila.
frame_entry:
 .hex 48e7fffe
 .hex 40e7
 cmpi.w #0x000c,(0xffffe6a4).w
 bne.w @frame_continue
 tst.b (0xffffe744).w
 bne.w @frame_continue
 tst.b (0xffffe73c).w
 bne.w @frame_continue
 tst.w (0xffffe9c4).w
 bne.w @frame_continue
 lea (0xffffe75e).w,A0
 jsr @tick_counter.l
 lea (0xffffe886).w,A0
 jsr @tick_counter.l
frame_continue:
 jmp 0x003e0006.l
counter_init:
 btst.b #0x07,(0x120,A0)
 bne.w @counter_ready
 clr.l (0x120,A0)
 clr.w (0x124,A0)
 move.b #0x80,(0x120,A0)
counter_ready:
 rts
tick_counter:
 jsr @counter_init.l
 tst.b (0x121,A0)
 beq.w @counter_return
 ; Pausar la ventana durante la ejecucion de un ataque o cruce.
 ; No aumentar stun ni prolongar las animaciones para mantener la cuenta.
 move.w (A0),D0
 cmpi.w #0x0400,D0
 bcs.w @counter_check_victim
 cmpi.w #0x0880,D0
 bcs.w @counter_return
counter_check_victim:
 jsr 0x0001335c.l
 tst.w (0x36,A1)
 bne.w @counter_return
 cmpi.w #0x0880,(A1)
 bcs.w @counter_decay
 cmpi.w #0x0890,(A1)
 bcs.w @counter_return
counter_decay:
 subq.b #0x01,(0x121,A0)
 bne.w @counter_return
 clr.b (0x122,A0)
counter_return:
 rts
count_hit:
 .hex 48e7fffe
 .hex 40e7
 cmpa.l #0xffffe75e,A0
 beq.w @count_valid
 cmpa.l #0xffffe886,A0
 bne.w @count_done
count_valid:
 jsr @counter_init.l
 clr.w (0x32,A0)
 jsr 0x0001335c.l
 movea.l A0,A5
 movea.l A1,A0
 jsr @counter_init.l
 movea.l A0,A1
 movea.l A5,A0
 moveq #0,D0
 tst.b (0x121,A1)
 beq.w @count_new
 tst.b (0x122,A1)
 beq.w @count_new
 move.b (0x120,A1),D0
 andi.w #0x007f,D0
count_new:
 addq.w #0x01,D0
 cmpi.w #0x0063,D0
 bls.w @count_clamped
 move.w #0x0063,D0
count_clamped:
 ori.b #0x80,D0
 move.b D0,(0x120,A1)
 move.b #0x5a,(0x121,A1)
 move.b #0x01,(0x122,A1)
 move.w (A1),(0x124,A1)
 clr.b (0x121,A0)
 clr.b (0x122,A0)
count_done:
 .hex 46df
 .hex 4cdf7fff
 rts
; Inicio de una secuencia cinematica confirmada: no se cuentan poses/particulas.
cinematic_entry:
 ; La ruta normal no guarda todos los registros: mantener bajo el coste.
 cmpi.b #0x14,D1
 bne.w @cinematic_resume
 cmpa.l #0xffffe75e,A0
 beq.w @cinematic_valid_actor
 cmpa.l #0xffffe886,A0
 bne.w @cinematic_resume
cinematic_valid_actor:
 cmp.w (A0),D0
 beq.w @cinematic_resume
 cmpi.w #0x0883,D0
 bcs.w @cinematic_resume
 cmpi.w #0x088d,D0
 bcc.w @cinematic_resume
 .hex 48e7fffe
 .hex 40e7
 jsr @count_hit.l
 tst.w (0x36,A0)
 beq.w @cinematic_done
 jsr 0x00020914.l
cinematic_done:
 .hex 46df
 .hex 4cdf7fff
cinematic_resume:
 ; Tailcall: conservar el retorno especial del motor y la entrada20B7E.
 jmp 0x00020b7a.l
hit_owner:
 moveq #0,D0
 tst.b (0xffffe87f).w
 beq.w @owner_p2
 move.b (0xffffe87e).w,D1
 andi.b #0x7f,D1
 cmpi.b #0x02,D1
 bcs.w @owner_p2
 moveq #0x01,D0
 rts
owner_p2:
 tst.b (0xffffe9a7).w
 beq.w @owner_return
 move.b (0xffffe9a6).w,D1
 andi.b #0x7f,D1
 cmpi.b #0x02,D1
 bcs.w @owner_return
 moveq #0x02,D0
owner_return:
 rts
hit_map_p1:
 .hex 014f0800e57d008a
hit_map_p2:
 .hex 014f0800e57d019e

round_counter_reset:
 ; Nueva ronda: no conservar el numero de una demostracion o combate anterior.
 clr.l (0xffffe87e).w
 clr.w (0xffffe882).w
 clr.l (0xffffe9a6).w
 clr.w (0xffffe9aa).w
 move.b #0xff,(0x83,A0)
 rts

; Goku Meteor: rodillazo confirmado + patada intermedia + remate.
; La patada emite su sonido nativo al entrar en el sprite41, sin restar
; vida todavia. Contarla una vez, solo con la victima en programa884.
goku_meteor_contact:
 .hex 48e7fffe
 .hex 40e7
 cmpi.b #0x41,D5
 bne.w @goku_contact_done
 cmpi.w #0x083f,(A0)
 bne.w @goku_contact_done
 btst.b #0x01,(0x122,A0)
 bne.w @goku_contact_done
 jsr 0x0001335c.l
 cmpi.w #0x0884,(A1)
 bne.w @goku_contact_done
 movea.l A1,A0
 jsr @count_hit.l
 jsr 0x0001335c.l
 bset.b #0x01,(0x122,A1)
goku_contact_done:
 .hex 46df
 .hex 4cdf7fff
 ; Reproducir los seis bytes sustituidos y sus destinos.
 cmpi.b #0x41,D5
 beq.w @goku_native_sound
 jmp 0x000162f6.l
goku_native_sound:
 jmp 0x000162fc.l
