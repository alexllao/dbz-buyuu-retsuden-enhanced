; Contactos confirmados que faltaban en el contador de los Meteor.
; La rutina de sonido nativa ya protege cada evento con CB.0.
; Se conservan el golpe inicial y el remate contabilizados por el motor.
a18:
 .hex 48e7fffe
 .hex 40e7
 cmpi.w #0x084c,(A0)
 bne.w @done
 ; Fase4: golpe intermedio. Fase6 ya esta cubierta por el remate nativo.
 cmpi.b #0x04,(0xffffe9b6).w
 bne.w @done
 jsr 0x0001335c.l
 cmpi.w #0x0889,(A1)
 bne.w @done
 bra.w @actor_contact
freezer:
 .hex 48e7fffe
 .hex 40e7
 cmpi.w #0x0850,(A0)
 bne.w @done
 ; Pose3B: contacto intermedio. Los55 pertenecen al remate ya contado.
 cmpi.b #0x3b,D5
 bne.w @done
 jsr 0x0001335c.l
 cmpi.w #0x088b,(A1)
 bne.w @done
actor_contact:
 movea.l A1,A0
 jsr @count_only.l
 bra.w @done
krilin:
 .hex 48e7fffe
 .hex 40e7
 ; Solo las seis reacciones17 de la victima, no la3F final.
 cmpi.w #0x088a,(A0)
 bne.w @done
 jsr 0x0001335c.l
 cmpi.w #0x084e,(A1)
 bne.w @done
 jsr @count_only.l
 bra.w @done
trunks:
 .hex 48e7fffe
 .hex 40e7
 cmpi.w #0x0888,(A0)
 bne.w @done
 jsr 0x0001335c.l
 cmpi.w #0x0849,(A1)
 bne.w @done
 jsr @count_only.l
done:
 .hex 46df
 .hex 4cdf7fff
 move.b #0x47,(0xffff5000).l
 rts

; Correccion solo visual del contador: no reiniciar la recuperacion de stun.
count_only:
 move.w (0x32,A0),-(SP)
 jsr 0x003b035c.l
 move.w (SP)+,(0x32,A0)
 rts
