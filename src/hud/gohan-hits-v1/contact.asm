; El sonido nativo47 se emite una vez por contacto, tras comprobar CB.0.
; Solo contar los golpes de842 con la victima realmente capturada en885.
; El golpe inicial y el remate final ya pasan por los contadores existentes.
entry:
 .hex 48e7fffe
 .hex 40e7
 cmpi.w #0x0842,(A0)
 bne.w @done
 jsr 0x0001335c.l
 cmpi.w #0x0885,(A1)
 bne.w @done
 movea.l A1,A0
 jsr 0x003b035c.l
done:
 .hex 46df
 .hex 4cdf7fff
 move.b #0x47,(0xffff5000).l
 rts
