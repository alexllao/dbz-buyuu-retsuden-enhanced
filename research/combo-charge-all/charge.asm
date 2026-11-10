; Recortar SOLO el reloj de preparacion al enlazar un ataque confirmado.
; Header, unidad temporal, poses de lanzamiento y bucles siguen originales.
entry:
 .hex 48e77f3e
 movea.l A1,A4
 ; Reproducir lectura nativa de cabecera y ajuste temporal de20ADC.
 move.b (A1)+,D0
 lsr.w #0x08,D0
 move.b (A1)+,D0
 jsr 0x00020adc.l
 cmpa.l #0xffffe75e,A0
 beq.w @p1
 cmpa.l #0xffffe886,A0
 bne.w @done
 lea (0xfffff7b4).w,A3
 bra.w @actor
p1:
 lea (0xfffff7b0).w,A3
actor:
 move.w (A0),D3
 cmpi.w #0x084a,D3
 beq.w @selected
 cmpi.w #0x0c00,D3
 bcs.w @clear
 cmpi.w #0x0c7f,D3
 bcc.w @clear
selected:
 cmp.w (A3),D3
 bne.w @decide
 tst.w (0x06,A0)
 bne.w @lookup
decide:
 move.w D3,(A3)
 clr.b (0x02,A3)
 clr.b (0x03,A3)
 tst.w (0x24,A0)
 beq.w @done
 tst.b (0xd22,A0)
 beq.w @done
 move.b (0xd20,A0),D4
 andi.b #0x7f,D4
 beq.w @done
 ; No basta que HITS sea visible: hace falta ventana viva de enlace.
 tst.b (0xd24,A0)
 beq.w @done
 move.b #0x01,(0x02,A3)
lookup:
 cmpi.b #0x01,(0x02,A3)
 bne.w @done
 lea (0x003e3000).l,A5
find:
 move.l (A5),D4
 beq.w @done
 cmpa.l D4,A4
 beq.w @found
 adda.w #0x10,A5
 bra.w @find
found:
 clr.w D7
 move.b (0x03,A3),D7
 cmp.b (0x06,A5),D7
 bcc.w @finished
 ; Misma division y minimo que20AA6: no cambiar el ritmo de salida.
 move.l D0,D6
 divu.w (0x04,A5),D6
 andi.l #0x0000ffff,D6
 bne.w @unit_ready
 moveq #0x01,D6
unit_ready:
 clr.w D4
 clr.w D5
 lea (0x08,A5),A6
sum_prefix:
 tst.w D7
 beq.w @current_phase
 move.b (A6)+,D5
 add.w D5,D4
 subq.w #0x01,D7
 bra.w @sum_prefix
current_phase:
 move.w D4,D2
 mulu.w D6w,D2
 move.w (0x06,A0),D3
 sub.w D2,D3
 bcs.w @done
 ; Conservar una actualizacion de CADA pose de carga y sus callbacks.
 moveq #0x01,D7
 cmpi.b #0x01,(0x06,A5)
 bne.w @minimum_ready
 moveq #0x03,D7
minimum_ready:
 cmp.w D7,D3
 bcs.w @done
 clr.w D5
 move.b (A6),D5
 add.w D5,D4
 mulu.w D6w,D4
 cmp.w (0x06,A0),D4
 bls.w @advance
 ;209E4 incrementa antes de resolver: entrar justo ANTES del marcador.
 subq.w #0x01,D4
 move.w D4,(0x06,A0)
advance:
 addq.b #0x01,(0x03,A3)
 move.b (0x03,A3),D7
 cmp.b (0x06,A5),D7
 bcs.w @done
finished:
 ori.b #0x02,(0x02,A3)
 bra.w @done
clear:
 move.w D3,(A3)
 clr.w (0x02,A3)
done:
 .hex 4cdf7cfe
 rts

; El juego desactiva ambas cajas receptoras durante reaccion B/C.
; Para un KI enlazado recuperar SOLO la ultima caja nativa del mismo
; personaje/orientacion/plano. Guardia, invulnerabilidad especial y caidas
; no se alteran. Los proyectiles conservan su consumo/contacto nativo.
boxes:
 jsr @native_boxes.l
 .hex 48e7fffe
 .hex 40e7
 cmpa.l #0xffffe75e,A0
 beq.w @boxes_p1
 cmpa.l #0xffffe886,A0
 bne.w @boxes_done
 lea (0xfffff7e0).w,A2
 lea (0xffffe75e).w,A6
 lea (0xfffff7b0).w,A3
 bra.w @boxes_actor
boxes_p1:
 lea (0xfffff7d0).w,A2
 lea (0xffffe886).w,A6
 lea (0xfffff7b4).w,A3
boxes_actor:
 tst.w (0x24,A0)
 beq.w @boxes_done
 cmpi.b #0x0b,(0x5b,A0)
 beq.w @boxes_restore
 cmpi.b #0x0c,(0x5b,A0)
 beq.w @boxes_restore
 cmpi.b #0x80,(0x6c,A0)
 beq.w @boxes_done
 move.l (0x6c,A0),(A2)
 move.l (0x70,A0),(0x04,A2)
 move.b (0x58,A0),(0x08,A2)
 move.b (0x59,A0),(0x09,A2)
 move.b (0x1e,A0),D0
 andi.b #0x10,D0
 move.b D0,(0x0a,A2)
 move.b #0x01,(0x0b,A2)
 bra.w @boxes_done
boxes_restore:
 cmpi.b #0x01,(0x0b,A2)
 bne.w @boxes_done
 move.b (0x58,A0),D0
 cmp.b (0x08,A2),D0
 bne.w @boxes_done
 move.b (0x59,A0),D0
 cmp.b (0x09,A2),D0
 bne.w @boxes_done
 move.b (0x1e,A0),D0
 andi.b #0x10,D0
 cmp.b (0x0a,A2),D0
 bne.w @boxes_done
 cmpi.b #0x03,(0x02,A3)
 bne.w @boxes_done
 move.w (A6),D0
 cmpi.w #0x0c00,D0
 bcs.w @boxes_done
 cmpi.w #0x0c7f,D0
 bcc.w @boxes_done
 tst.b (0xd22,A6)
 beq.w @boxes_done
 tst.b (0xe2,A6)
 bne.w @boxes_apply
 tst.b (0x100,A6)
 bne.w @boxes_apply
 tst.b (0x11e,A6)
 beq.w @boxes_done
boxes_apply:
 move.l (A2),(0x6c,A0)
 move.l (0x04,A2),(0x70,A0)
boxes_done:
 .hex 46df
 .hex 4cdf7fff
 rts
native_boxes:
 clr.w D0
 move.b (0x58,A0),D0
 jmp 0x00011c24.l
; El filtro original descarta proyectiles durante reaccion B/C salvo
; algunos tipos. Permitir SOLO el KI cuyo enlace ya fue confirmado.
projectile_p1:
 cmpi.b #0x03,(0xfffff7b2).w
 bne.w @projectile_p1_original
 ; La ventana queda enclavada al aceptar el comando, no al impactar.
 jmp 0x00011f08.l
projectile_p1_original:
 jmp 0x003d03ae.l
projectile_p2:
 cmpi.b #0x03,(0xfffff7b6).w
 bne.w @projectile_p2_original
 jmp 0x000120e0.l
projectile_p2_original:
 jmp 0x003d03cc.l
round_reset:
 clr.l (0xfffff7d0).w
 clr.l (0xfffff7d4).w
 clr.l (0xfffff7d8).w
 clr.l (0xfffff7dc).w
 clr.l (0xfffff7e0).w
 clr.l (0xfffff7e4).w
 clr.l (0xfffff7e8).w
 clr.l (0xfffff7ec).w
 jmp 0x003df128.l
