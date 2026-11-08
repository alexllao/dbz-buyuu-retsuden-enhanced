; Solo tablas de ki: evitar trabajo adicional durante poses y entradas.
entry:
 jsr 0x003da272.l
 .hex 40e7
 move.l D3,-(SP)
 move.l A3,-(SP)
 move.l A4,-(SP)
 cmpa.l #0xffffe75e,A0
 beq.w @p1
 cmpa.l #0xffffe886,A0
 bne.w @done
 lea (0xfffff7b4).w,A3
 lea (0xffffe75e).w,A4
 bra.w @actor
p1:
 lea (0xfffff7b0).w,A3
 lea (0xffffe886).w,A4
actor:
 cmpi.w #0x0100,(0xffffe756).w
 bne.w @clear
 tst.b (0xbe,A0)
 bne.w @clear
 tst.w (0x24,A0)
 beq.w @clear
 btst.b #0x04,(0x1e,A0)
 bne.w @clear
 move.w (A0),D3
 cmpi.w #0x0c0f,D3
 beq.w @gohan
 cmpi.w #0x0c27,D3
 bne.w @clear
 cmpi.b #0x03,(0x58,A0)
 bne.w @clear
 bra.w @selected
gohan:
 cmpi.b #0x01,(0x58,A0)
 bne.w @clear
selected:
 ; Decidir al empezar cada ejecucion. Mantener la decision durante ella.
 tst.w (0x06,A0)
 beq.w @decide
 cmp.w (A3),D3
 beq.w @latched
 bra.w @clear
decide:
 move.w D3,(A3)
 clr.b (0x02,A3)
 move.b (0xd06,A0),D3
 andi.b #0x33,D3
 beq.w @done
 tst.b (0xd22,A0)
 beq.w @done
 move.b (0xd20,A0),D3
 andi.b #0x7f,D3
 beq.w @done
 cmpi.b #0x0b,(0x5b,A4)
 beq.w @enable
 cmpi.b #0x0c,(0x5b,A4)
 bne.w @done
enable:
 move.b #0x01,(0x02,A3)
latched:
 tst.b (0x02,A3)
 beq.w @done
 cmpi.w #0x0c0f,(A0)
 beq.w @gohan_table
 lea (@vegeta_pointer).l,A1
 suba.w #0x4e,A1
 bra.w @done
gohan_table:
 lea (@gohan_pointer).l,A1
 suba.w #0x1e,A1
 bra.w @done
clear:
 move.w (A0),(A3)
 clr.b (0x02,A3)
done:
 movea.l (SP)+,A4
 movea.l (SP)+,A3
 move.l (SP)+,D3
 .hex 46df
 rts
; Mantener D2 y poses: solo reducir primer peso y cabecera equivalente.
; Masenko:84/(3+4)=12; nuevo72/(2+4)=12.
gohan_pointer:
 .hex 0002
 .hex 0048020400505100
; Final Flash:120/(3+1+3)=17; nuevo85/(1+1+3)=17.
vegeta_pointer:
 .hex 0002
 .hex 00550101030052545300
round_reset:
 clr.l (0xfffff7b0).w
 clr.l (0xfffff7b4).w
 jmp 0x003de532.l
