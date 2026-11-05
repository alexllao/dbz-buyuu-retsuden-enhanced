; Cuatro patrones comparten ambas barras: cuatro filas para cada jugador.
; P2 usa H/V flip; aY220 solo se ven cuatro filas en el modo nativo224.
; No reutilizar la tabla de ventana: dibuja tambien el fondo derecho.
; No enganchar6EE8: puede interrumpir una carga grafica del juego.
; Barras inferiores de aturdimiento: solo lectura de los valores nativos.
; Dos sprites temporales; patrones unicamente enAF20..AFA0.
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
draw_done:
 .hex 4cdf7fff
 .hex 46ef0008
 pea (@transfer_return).l
 move.l (0x0e,SP),-(SP)
 .hex 46ef0010
 rts
transfer_return:
 .hex 40e7
 ;720C borra Y/enlace/X de la cabecera; restaurar solo su atributo original.
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
