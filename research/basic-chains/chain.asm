; Variantes de basicos, solo Goku humano y enlaces ya confirmados del modulo.
; No acortar secuencias, desplazar cuerpos ni modificar reaccion del rival.
dispatch:
 move.l D2,-(SP)
 cmpa.l #0xffffe75e,A0
 beq.w @actor
 cmpa.l #0xffffe886,A0
 bne.w @original
actor:
 cmpi.w #0x0100,(0xffffe756).w
 bne.w @original
 tst.b (0x58,A0)
 bne.w @original
 tst.b (0xbe,A0)
 bne.w @original
 btst.b #0x04,(0x1e,A0)
 bne.w @original
 move.b (0xd06,A0),D2
 andi.b #0xfc,D2
 cmpi.b #0x8c,D2
 bne.w @original
 move.b (0xd06,A0),D2
 andi.b #0x03,D2
 cmpi.b #0x01,D2
 bne.w @third
 ; Segundo punetazo: recto nativo de media distancia (401 / accion21).
 cmpi.w #0x0400,D0
 bne.w @original
 cmpi.b #0x20,D1
 bne.w @original
 move.w #0x0401,D0
 move.b #0x21,D1
 bra.w @original
third:
 cmpi.b #0x02,D2
 bne.w @original
 ; Tercera entrada B: patada nativa de mayor alcance (404 / accion24).
 cmpi.w #0x0403,D0
 bne.w @original
 cmpi.b #0x23,D1
 bne.w @original
 move.w #0x0404,D0
 move.b #0x24,D1
original:
 move.l (SP)+,D2
 move.b D1,(0x5b,A0)
 cmpi.b #0x20,D1
 rts
