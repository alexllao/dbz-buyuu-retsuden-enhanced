; F,B,F + logical flight button. Runs after native history and A/B parsing.
; Existing magic C7 becomes CF while flight is consumed until release.
entry:
 .hex 48e7fffe
 .hex 40e7
 tst.b (0xffffe742).w
 bne.w @done
 tst.b (0xffffe744).w
 bne.w @done
 tst.b (0xffffe9b0).w
 bne.w @done
 tst.b (0xffffe73c).w
 bne.w @done
 tst.w (0xffffe9c4).w
 bne.w @done
 lea (0xffffe75e).w,A0
 jsr @actor.l
 lea (0xffffe886).w,A0
 jsr @actor.l
done:
 .hex 46df
 .hex 4cdf7fff
 jmp 0x00011c9c.l

actor:
 tst.b (0xbe,A0)
 bne.w @return
 move.b (0x108,A0),D0
 andi.b #0xf7,D0
 cmpi.b #0xc7,D0
 bne.w @return
 btst.b #0x3,(0x108,A0)
 bne.w @consume
 moveq #0,D4
 move.b (0xbc,A0),D4
 moveq #0,D0
 move.b (0x1b,A0),D0
 btst.l D4,D0
 beq.w @released
 move.b (0x1d,A0),D0
 btst.l D4,D0
 beq.w @return
 ; Do not steal a command using either attack function.
 moveq #0,D5
 moveq #0,D1
 move.b (0xba,A0),D1
 bset.l D1,D5
 move.b (0xbb,A0),D1
 bset.l D1,D5
 and.b (0x1b,A0),D5
 bne.w @return
 cmpi.b #0xff,(0xb9,A0)
 bne.w @return
 cmpi.b #0x08,(0x5b,A0)
 bhi.w @return
 tst.w (0x24,A0)
 beq.w @return
 jsr 0x0001335c.l
 tst.w (0x24,A1)
 beq.w @return
 move.b (0x1e,A0),D0
 move.b (0x1e,A1),D1
 eor.b D1,D0
 btst.l #0x4,D0
 bne.w @return
 move.w (0xa,A0),D0
 sub.w (0xa,A1),D0
 bpl.w @positive_x
 neg.w D0
positive_x:
 cmpi.w #0x60,D0
 bhi.w @return
 move.w (0x10,A0),D0
 sub.w (0x10,A1),D0
 bpl.w @positive_y
 neg.w D0
positive_y:
 cmpi.w #0x20,D0
 bhi.w @return
 ; The native matcher mutates history and B7/B9 even on failure.
 ; Restore its entire 40-byte working region before accepting/rejecting.
 lea (0x94,A0),A3
 moveq #0x13,D6
save_history:
 move.w (A3)+,-(SP)
 subq.w #0x1,D6
 bpl.w @save_history
 ; Native direction history retains C, unlike the A/B parser's own modifier.
 ; Remove only that bit temporarily, including simultaneous final F+C.
 moveq #0,D0
 bset.l D4,D0
 not.b D0
 lea (0x94,A0),A3
 moveq #0x0f,D6
strip_flight_from_history:
 and.b D0,(A3)
 addq.w #0x2,A3
 subq.w #0x1,D6
 bpl.w @strip_flight_from_history
 ; The native A/B matcher excludes a terminal button entry. Supply one
 ; temporarily so the last forward direction can arrive together with C.
 moveq #0,D0
 move.b (0xb6,A0),D0
 andi.w #0x1f,D0
 lea (0x94,A0),A3
 adda.w D0,A3
 clr.w (A3)
 addq.w #0x2,D0
 andi.w #0x1f,D0
 move.b D0,(0xb6,A0)
 cmp.b (0xb7,A0),D0
 bne.w @virtual_entry_ready
 addq.w #0x2,D0
 andi.w #0x1f,D0
 move.b D0,(0xb7,A0)
virtual_entry_ready:
 move.b #0xff,(0xb9,A0)
 lea (@sequence).l,A1
 jsr 0x000092b2.l
 moveq #0,D7
 move.b (0xb9,A0),D7
 lea (0xbc,A0),A3
 moveq #0x13,D6
restore_history:
 move.w (SP)+,-(A3)
 subq.w #0x1,D6
 bpl.w @restore_history
 cmpi.b #0xfe,D7
 bne.w @return
 ; Reproduce the native Gohan move entry without its stack-skipping helper.
 move.b #0x3a,(0x7c,A0)
 clr.w (0xe0,A0)
 move.b #0x38,(0x5b,A0)
 move.w #0x20,D0
 jsr 0x0001318a.l
 jsr 0x00020ba0.l
 move.w #0x0843,(A0)
 move.b (0xb6,A0),(0xb7,A0)
 move.b #0xff,(0xb9,A0)
 clr.b (0x109,A0)
 clr.b (0x10a,A0)
 clr.b (0x10e,A0)
 bset.b #0x3,(0x108,A0)
consume:
 moveq #0,D4
 move.b (0xbc,A0),D4
 moveq #0,D0
 bset.l D4,D0
 not.b D0
 and.b D0,(0x1a,A0)
 and.b D0,(0x1b,A0)
 and.b D0,(0x1c,A0)
 and.b D0,(0x1d,A0)
return:
 rts
released:
 bclr.b #0x3,(0x108,A0)
 rts
pre_input:
 ; Consume a latched C before native history/A-B parsing on later frames.
 ; This keeps subsequent attack combinations free of held-C pollution.
 cmpi.b #0xcf,(0x108,A0)
 bne.w @return
 moveq #0,D4
 move.b (0xbc,A0),D4
 moveq #0,D0
 move.b (0x1b,A0),D0
 btst.l D4,D0
 beq.w @released
 bra.w @consume
sequence:
 .hex 0308040800fe00
