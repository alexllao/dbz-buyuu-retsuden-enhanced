; Salida de aturdimiento al primer impacto aceptado y no bloqueado.
; El motor ya calculo el dano y descarto los impactos no validos.
; A0 es la victima. No cambiar la reaccion, dano ni animacion nativa.
break_stun_on_hit:
 tst.w (0x36,A0)
 bne.w @clear_active_stun
 cmpi.w #0x007d,(0x28,A0)
 jmp 0x00021a14.l
clear_active_stun:
 jsr 0x00020914.l
 jmp 0x00021a64.l
